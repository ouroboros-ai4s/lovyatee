"""B 层驱动：adapter 搬值，本模块负责 distinct 键、缓存、对账与写 Parquet。

阶段 adapt → ab → ag → assemble。ab / ag 按 distinct 键处理，产物旁写 `.key`；
键覆盖规则版本、`etl/core` 的 commit、决策文件 hash 与本阶段全部输入键。
"""
from __future__ import annotations

import hashlib
import json
import multiprocessing as mp
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Sequence

import pyarrow as pa
import pyarrow.parquet as pq

from etl.core import ids
from etl.core.merge import PAIR_SCHEMA, REJECT_SCHEMA

RULES_VERSION = "v1"
DEFAULT_OUT = Path("/data_new/ywy/etl_out")

RAW_AB_SCHEMA = pa.schema([
    ("src", pa.string()), ("record_key", pa.string()), ("ab_key", pa.string()),
    ("h_raw", pa.string()), ("l_raw", pa.string()),
    ("evidence", pa.string()), ("notes", pa.list_(pa.string())),
])
RAW_AG_SCHEMA = pa.schema([
    ("src", pa.string()), ("record_key", pa.string()), ("ag_key", pa.string()),
    ("branch", pa.string()), ("seq_raw", pa.list_(pa.string())),
    ("evidence", pa.string()), ("notes", pa.list_(pa.string())),
])
RAW_OBS_SCHEMA = pa.schema([
    ("src", pa.string()), ("record_key", pa.string()), ("label", pa.string()),
    ("assay", pa.string()), ("condition", pa.string()), ("replicate", pa.string()),
    ("lineage", pa.list_(pa.string())),
])
AB_ENTITY_SCHEMA = pa.schema([
    ("ab_key", pa.string()), ("AB_ID", pa.string()), ("vh", pa.string()), ("vl", pa.string()),
    ("structure", pa.string()), ("structure_rank", pa.int32()),
    ("lineage", pa.list_(pa.string())), ("applied_edits", pa.list_(pa.string())),
    ("reason_code", pa.string()),
])
AG_ENTITY_SCHEMA = pa.schema([
    ("ag_key", pa.string()), ("AG_ID", pa.string()), ("sequence", pa.list_(pa.string())),
    ("structure", pa.string()), ("structure_rank", pa.int32()),
    ("lineage", pa.list_(pa.string())), ("applied_edits", pa.list_(pa.string())),
    ("reason_code", pa.string()),
])


@dataclass
class Record:
    """一行源记录；raw 值保持源的原样。"""
    key: str
    h_raw: str | None = None
    l_raw: str | None = None
    ag_raw: tuple[str, ...] = ()
    obs: tuple[dict, ...] = ()
    ab_evidence: dict = field(default_factory=dict)
    ag_evidence: dict = field(default_factory=dict)
    ab_notes: tuple[str, ...] = ()
    ag_notes: tuple[str, ...] = ()
    branch: str = "main"
    ab_ctx: dict = field(default_factory=dict)     # 体积大的辅助数据，不进键
    ag_ctx: dict = field(default_factory=dict)


def _h(*parts) -> str:
    return ids.H("kv/v1:" + "\x1f".join(str(p) for p in parts))


def ab_key(rec: Record) -> str:
    return _h(rec.h_raw, rec.l_raw, json.dumps(rec.ab_evidence, sort_keys=True))


def ag_key(rec: Record) -> str:
    return _h(rec.branch, list(rec.ag_raw), json.dumps(rec.ag_evidence, sort_keys=True))


def core_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD", "--", "etl/core"], text=True,
            cwd=Path(__file__).resolve().parents[2]).strip()[:12]
    except (subprocess.CalledProcessError, OSError):
        return "unknown"


def decision_hash(paths: Sequence[Path]) -> str:
    h = hashlib.sha256()
    for p in sorted(Path(x) for x in paths):
        h.update(p.name.encode())
        h.update(p.read_bytes())
    return h.hexdigest()[:16]


def stage_key(*parts) -> str:
    return _h(RULES_VERSION, core_commit(), *parts)


def _key_hit(stamp: Path, key: str, outputs: Sequence[Path]) -> bool:
    return (stamp.exists() and stamp.read_text().strip() == key
            and all(o.exists() for o in outputs))


def _write(path: Path, rows: list[dict], schema: pa.Schema) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    table = (pa.Table.from_pylist(rows, schema=schema) if rows else schema.empty_table())
    pq.write_table(table, path, compression="zstd")


def _chunk(items: list, n: int) -> list[list]:
    size = max(1, (len(items) + n - 1) // n)
    return [items[i:i + size] for i in range(0, len(items), size)]


def _task(args):
    fn, items = args
    return [fn(x) for x in items]


def _map_batch(fn, items: list, workers: int) -> list:
    if workers <= 1 or len(items) < 2:
        return [fn(x) for x in items]
    chunks = _chunk(items, workers)
    if len(chunks) < 2:
        return [fn(x) for x in items]
    with mp.Pool(len(chunks)) as pool:
        parts = pool.map(_task, [(fn, c) for c in chunks])
    return [x for part in parts for x in part]


def reject(stage: str, reason: str, src: str, key: str, detail) -> dict:
    return {"stage": stage, "reason_code": reason, "src": src, "key": key,
            "detail": detail if isinstance(detail, str)
            else json.dumps(detail, ensure_ascii=False, sort_keys=True)}


def _count(values) -> dict:
    out = {}
    for v in values:
        out[v] = out.get(v, 0) + 1
    return dict(sorted(out.items()))


def _struct(value):
    if not value:
        return None
    if isinstance(value, str):
        value = json.loads(value)
    chain_map = value.get("chain_map")
    return {"structure_id": value.get("structure_id"), "file_ref": value.get("file_ref"),
            "chain_map": chain_map if isinstance(chain_map, str)
            else json.dumps(chain_map, sort_keys=True)}


def _dump(obj) -> str:
    return json.dumps(obj, sort_keys=True)


def _stage_entities(out: Path, stage: str, src: str, dec: str, raw: list[dict],
                    key_col: str, resolver: Callable, schema: pa.Schema,
                    workers: int, ctx_by_key: dict) -> dict:
    keys = sorted({row[key_col] for row in raw})
    rows_by_key = {row[key_col]: row for row in raw}
    stamp = out / (stage + "_entity.parquet.key")
    target = out / (stage + "_entity.parquet")
    key = stage_key(src, stage, dec, keys)
    if _key_hit(stamp, key, [target]):
        return {row[key_col]: row for row in pq.read_table(target).to_pylist()}

    tasks = [dict(rows_by_key[k], _ctx=ctx_by_key.get(k, {})) for k in keys]
    resolved = _map_batch(resolver, tasks, workers)
    rows = []
    for k, ent in zip(keys, resolved):
        row = {name: None for name in schema.names}
        row[key_col] = k
        if ent.get("reason_code"):
            row["reason_code"] = ent["reason_code"]
        else:
            for name in schema.names:
                if ent.get(name) is not None:
                    row[name] = ent[name]
        row["lineage"] = list(ent.get("lineage") or [])
        row["applied_edits"] = list(ent.get("applied_edits") or [])
        for name, typ in zip(schema.names, schema.types):
            if pa.types.is_string(typ) and isinstance(row.get(name), (dict, list)):
                row[name] = json.dumps(row[name], sort_keys=True)
        rows.append(row)
    _write(target, rows, schema)
    stamp.write_text(key + "\n")
    return {row[key_col]: row for row in rows}


def run(src: str, records: Sequence[Record], reject_rows: Sequence[dict],
        resolve_ab: Callable[[dict], dict], resolve_ag: Callable[[dict], dict],
        out_root: Path | str = DEFAULT_OUT, workers: int = 32,
        decisions: Sequence[Path] = ()) -> dict:
    """跑一个 SRC 的 adapt → ab → ag → assemble，返回对账摘要。

    resolver 接收 raw 行（含 `_ctx`），返回业务字段；AB_ID / AG_ID 由 resolver 用
    `etl.core.ids` 计算，本模块只搬运与写盘。
    """
    out = Path(out_root) / src
    out.mkdir(parents=True, exist_ok=True)
    dec = decision_hash(decisions)

    raw_ab = [{"src": src, "record_key": r.key, "ab_key": ab_key(r),
               "h_raw": r.h_raw, "l_raw": r.l_raw,
               "evidence": _dump(r.ab_evidence), "notes": list(r.ab_notes)}
              for r in records]
    raw_ag = [{"src": src, "record_key": r.key, "ag_key": ag_key(r), "branch": r.branch,
               "seq_raw": list(r.ag_raw), "evidence": _dump(r.ag_evidence),
               "notes": list(r.ag_notes)} for r in records]
    raw_obs = [{"src": src, "record_key": r.key, "label": o["label"],
                "assay": o.get("assay"), "condition": o.get("condition"),
                "replicate": o.get("replicate"), "lineage": list(o["lineage"])}
               for r in records for o in r.obs]
    _write(out / "raw_ab.parquet", raw_ab, RAW_AB_SCHEMA)
    _write(out / "raw_ag.parquet", raw_ag, RAW_AG_SCHEMA)
    _write(out / "raw_obs.parquet", raw_obs, RAW_OBS_SCHEMA)

    ab_ent = _stage_entities(out, "ab", src, dec, raw_ab, "ab_key", resolve_ab,
                             AB_ENTITY_SCHEMA, workers,
                             {ab_key(r): r.ab_ctx for r in records})
    ag_ent = _stage_entities(out, "ag", src, dec, raw_ag, "ag_key", resolve_ag,
                             AG_ENTITY_SCHEMA, workers,
                             {ag_key(r): r.ag_ctx for r in records})

    pair_rows, asm_rejects = [], []
    for r in records:
        ak, gk = ab_key(r), ag_key(r)
        a, g = ab_ent[ak], ag_ent[gk]
        detail = {"ab_reason": a["reason_code"], "ag_reason": g["reason_code"],
                  "ab_key": ak, "ag_key": gk}
        reason = a["reason_code"] or g["reason_code"]
        if reason:
            asm_rejects.append(reject("assemble", reason, src, r.key, detail))
            continue
        if not r.obs:
            asm_rejects.append(reject("assemble", "no_observation", src, r.key, detail))
            continue
        pair_rows.append({
            "src": src, "record_key": r.key,
            "AB_ID": a["AB_ID"], "AG_ID": g["AG_ID"],
            "3A_ID": ids.three_a_id(a["AB_ID"], g["AG_ID"]),
            "vh": a["vh"], "vl": a["vl"],
            "ab_structure": _struct(a["structure"]), "ab_structure_rank": a["structure_rank"],
            "ab_lineage": list(a["lineage"]) + list(r.ab_notes),
            "ag_sequence": list(g["sequence"]),
            "ag_structure": _struct(g["structure"]), "ag_structure_rank": g["structure_rank"],
            "ag_lineage": list(g["lineage"]) + list(r.ag_notes),
            "obs": [dict(o) for o in r.obs],
        })

    _write(out / "pair.parquet", pair_rows, PAIR_SCHEMA)
    rejects = list(reject_rows) + asm_rejects
    _write(out / "reject_log.parquet", rejects, REJECT_SCHEMA)

    summary = {
        "src": src,
        "records": len(records),
        "adapt_rejects": len(reject_rows),
        "ab_keys": len(ab_ent),
        "ab_ok": sum(1 for v in ab_ent.values() if not v["reason_code"]),
        "ab_rejected": sum(1 for v in ab_ent.values() if v["reason_code"]),
        "ag_keys": len(ag_ent),
        "ag_ok": sum(1 for v in ag_ent.values() if not v["reason_code"]),
        "ag_rejected": sum(1 for v in ag_ent.values() if v["reason_code"]),
        "pairs": len(pair_rows),
        "assemble_rejects": len(asm_rejects),
        "observations": sum(len(r["obs"]) for r in pair_rows),
        "distinct_3a": len({r["3A_ID"] for r in pair_rows}),
        "reasons": _count(x["reason_code"] for x in rejects),
    }
    (out / "reconcile.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary
