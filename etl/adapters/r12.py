"""R12 ASD / AgAb DB：20 个 parquet 分片，1,177,819 行。

- 抗体：`chains.antibody_chains` 是 [(类型, 序列)]，类型 `heavy` / `light` /
  `scfv` / `nanobody` 等；`nanobody` / `scfv` 两个布尔列给出构建体标记。
- 抗原：`chains.target_chains` 是 [(类型, 序列)]，`full` / `_` 等。
- 观察值：`affinity` 逐行一条；`affinity_type` 是长表类型列，按 aff 方案第 3 项
  以 `affinity_type=<取值>` 写进 lineage。
- `processed_measurement` 不产出。`delta_g` 是计算 ΔG，保留并以 lineage 标明。
"""
from __future__ import annotations

import glob
from pathlib import Path

import pyarrow.parquet as pq

from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R12"
ROOT = Path("/data_new/ywy/dataset-abag/SRC_R12_ASD/2.0/asd_2.0")
SHARDS = sorted(glob.glob(str(ROOT / "*.parquet")))
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")
NOT_VALID = ("nan", "I.C.", "NA", "N/A", "", "None", "NULL")
SOURCE_ROWS = 1177819
SHARDED = True      # 118 万行按 10 万一片跑


def _valid(value) -> bool:
    text = "" if value is None else str(value).strip()
    if text in NOT_VALID:
        return False
    try:
        float(text.lstrip("<>"))
    except ValueError:
        return False
    return True


def _slot(chains, kind):
    """取指定类型的第一条序列；scfv / nanobody 也归到 heavy 槽。"""
    for name, seq in chains or []:
        if name == kind and seq:
            return seq
    return None


def adapt():
    """返回生成器；reject 收集到 adapt.rejects，run_src 读完 record 流后才取用。"""
    return _stream(), adapt.rejects


def _stream():
    for shard in SHARDS:
        table = pq.read_table(shard)
        name = Path(shard).name
        for n, row in enumerate(table.to_pylist(), start=2):
            key = "%s:row=%d" % (name, n)
            chains = row.get("chains") or {}
            ab = chains.get("antibody_chains") or []
            ag = chains.get("target_chains") or []
            h = _slot(ab, "heavy") or _slot(ab, "scfv") or _slot(ab, "nanobody")
            l = _slot(ab, "light")
            if not h and not l:
                # 单链构建体也可能只存在别的类型名
                h = next((s for _, s in ab if s), None)
            if not h and not l:
                adapt.rejects.append(reject("adapt", "no_sequence", SRC, key,
                                            {"dataset": row.get("dataset")}))
                continue
            ag_seqs = tuple(s for _, s in ag if s)
            if not (h or l) or not ag_seqs:
                adapt.rejects.append(reject("adapt", "no_sequence", SRC, key,
                                      {"dataset": row.get("dataset"),
                                       "ab_chains": [k for k, _ in ab],
                                       "ag_chains": [k for k, _ in ag]}))
                continue
            value = row.get("affinity")
            if not _valid(value):
                adapt.rejects.append(reject("adapt", "no_observation", SRC, key,
                                      {"affinity": value,
                                       "dataset": row.get("dataset")}))
                continue
            loc = locator(SRC, name, "row=" + str(n),
                          "dataset=" + str(row.get("dataset") or "NA"))
            obs = {"label": str(value).strip(),
                   "assay": None,
                   "condition": row.get("dataset") or None, "replicate": None,
                   "lineage": [join(loc, kv("col", "affinity"),
                                    kv("affinity_type",
                                       row.get("affinity_type") or "NA"))]}
            meta = row.get("metadata") or {}
            yield Record(
                key=key, h_raw=h, l_raw=l, ag_raw=ag_seqs, obs=(obs,),
                ab_evidence={"seqs": {"h": h, "l": l},
                             "placeholders": list(PLACEHOLDERS),
                             "structure": None, "structure_rank": None},
                ag_evidence={"chains": [{"key": "A" + str(i), "seq": s}
                                        for i, s in enumerate(ag_seqs)],
                             "placeholders": list(PLACEHOLDERS),
                             "structure": None, "structure_rank": None},
                ab_notes=(join(kv("nanobody", str(row.get("nanobody"))),
                               kv("scfv", str(row.get("scfv")))),),
                ag_notes=(join(kv("target", meta.get("target_name") or "NA")),))


adapt.rejects = []
