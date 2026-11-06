"""单个 SRC 的完成判据 1–6：`python -m etl.b.check SRC_R76`。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import duckdb
import pyarrow.parquet as pq

from etl.core.merge import PAIR_SCHEMA, merge

OUT = Path("/data_new/wyy".replace("wyy", "wyy"))


def _p(src_dir: Path, name: str) -> Path:
    return src_dir / name


def check(src: str, out_root: Path = Path("/data_new/ywy/etl_out")) -> dict:
    d = out_root / src
    result = {}
    rec = json.loads((d / "reconcile.json").read_text())
    result["reconcile"] = rec

    rej = pq.read_table(d / "reject_log.parquet").to_pylist()
    # 同一源行只应记一次 adapt reject；key 已含文件前缀，按完整 key 去重
    # 行级 adapt reject 的 key 含 `row=`；表级（整表无标签、文件缺失）不占源行配额
    row_rej = {r["key"] for r in rej if r["stage"] == "adapt" and "row=" in r["key"]}
    table_rej = {r["key"] for r in rej if r["stage"] == "adapt" and "row=" not in r["key"]}
    adapt_rej = len(row_rej)
    if table_rej:
        rec["adapt_table_rejects"] = sorted(table_rej)
    covered = rec["records"] + adapt_rej
    src_rows = rec.get("source_rows")
    result["check1_adapt"] = {
        "source_rows": src_rows, "records": rec["records"], "adapt_rejects": adapt_rej,
        "covered": covered,
        "ok": (covered == src_rows) if src_rows is not None else None,
        "note": None if src_rows is not None else "adapter 未声明 SOURCE_ROWS",
    }

    ab = pq.read_table(d / "ab_entity.parquet").to_pylist()
    ag = pq.read_table(d / "ag_entity.parquet").to_pylist()
    result["check2_ab"] = {"keys": len(ab),
                           "ok": len(ab) == sum(1 for r in ab if not r["reason_code"])
                           + sum(1 for r in ab if r["reason_code"])}
    result["check2_ag"] = {"keys": len(ag),
                           "ok": len(ag) == sum(1 for r in ag if not r["reason_code"])
                           + sum(1 for r in ag if r["reason_code"])}

    pair = pq.read_table(d / "pair.parquet", schema=PAIR_SCHEMA)
    asm_rej = sum(1 for r in rej if r["stage"] == "assemble")
    result["check3_assemble"] = {"records": rec["records"], "pairs": pair.num_rows,
                                 "rejects": asm_rej,
                                 "ok": rec["records"] == pair.num_rows + asm_rej}

    mg = out_root / src / "merge_check"
    rep = merge(str(d / "pair.parquet"), mg, reject_glob=str(d / "reject_log.parquet"),
                shards=1, qa_per_stratum=10)
    n_obs = sum(len(o) for o in pair.column("obs").to_pylist())
    con = duckdb.connect()
    got = con.execute('select sum(len(affinity)) from read_parquet(?)',
                      [str(mg / "3a" / "*.parquet")]).fetchone()[0]
    result["check4_merge"] = {"n_pairs": rep.n_pairs, "n_3a": rep.n_3a,
                              "n_obs_pairs": n_obs, "sum_affinity": got,
                              "ok": got == n_obs and rep.n_obs == n_obs,
                              "merged": rep.n_pairs - rep.n_3a}

    reasons = {}
    for r in rej:
        reasons[r["reason_code"]] = reasons.get(r["reason_code"], 0) + 1
    total = max(1, rec["records"] + adapt_rej)
    result["check5_reasons"] = {k: {"n": v, "share": round(v / total, 4)}
                                for k, v in sorted(reasons.items(), key=lambda t: -t[1])}
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    args = ap.parse_args(argv)
    print(json.dumps(check(args.src), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
