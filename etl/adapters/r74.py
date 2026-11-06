"""R74 AbDesign 2.0：pd_1/affinity.csv，576 条 A 类重链单点突变 + 2 条 assay 对照。

抗原为固定 PD-1，序列取自 5GGS entity 3 chain Y（决策文件 R74 C1）。
`kd` 有值 → 只产出 `kd`；`kd` 空且 `binding` 有值 → 只产出 `binding`；
kon/koff/r2 不产出（aff 方案第 2 项）。突变名只进 lineage。
"""
from __future__ import annotations

import csv
from pathlib import Path

from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R74"
DATA = Path("/data_new/ywy/dataset-abag/SRC_R74_ABDESIGN2/snapshot-2026-02-23")
FILE = "pd_1/affinity.csv"
SOURCE_ROWS = 578
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")

# 决策文件 R74 C1 的 value；verify_decisions 已核对与 5GGS entity 3 逐字一致
PD1 = ("DSPDRPWNPPTFSPALLVVTEGDNATFTCSFSNTSESFVLNWYRMSPSNQTDKLAAFPEDRSQPGQDSRFRVTQLPNGRDFHMSVVRAR"
       "RNDSGTYLCGAISLAPKAQIKESLRAELRVTERR")


def adapt() -> tuple[list[Record], list[dict]]:
    records, rejects = [], []
    with (DATA / FILE).open(encoding="utf-8", newline="") as fh:
        for n, row in enumerate(csv.DictReader(fh), start=2):
            key = "row=" + str(n)
            h, l = row["heavy_sequence"], row["light_sequence"]
            if not h.strip() or not l.strip():
                rejects.append(reject("adapt", "no_sequence", SRC, key, {"name": row["name"]}))
                continue
            kd, binding = row["kd"], row["binding"]
            loc = locator(SRC, FILE, key, "name=" + row["name"])
            if kd.strip():
                obs = [{"label": kd.strip(), "assay": None, "condition": "Group 1 (kd)",
                        "replicate": None, "lineage": [join(loc, kv("col", "kd"))]}]
            elif binding.strip():
                obs = [{"label": binding.strip(), "assay": None,
                        "condition": "Group 1 (binding)", "replicate": None,
                        "lineage": [join(loc, kv("col", "binding"))]}]
            else:
                rejects.append(reject("adapt", "no_observation", SRC, key,
                                      {"kd": kd, "binding": binding}))
                continue
            records.append(Record(
                key=key, h_raw=h, l_raw=l, ag_raw=(PD1,), obs=tuple(obs),
                ab_evidence={"seqs": {"h": h, "l": l}, "placeholders": list(PLACEHOLDERS),
                             "structure": {"structure_id": "5GGS", "file_ref": None,
                                           "chain_map": {"H": "A", "L": "B"}},
                             "structure_rank": 50},
                ag_evidence={"chains": [{"key": "Y", "seq": PD1, "entity": "3"}],
                             "placeholders": list(PLACEHOLDERS),
                             "structure": {"structure_id": "5GGS", "file_ref": None,
                                           "chain_map": {"Y": "Y"}},
                             "structure_rank": 50,
                             "notes": ["decision=R74:C1"]},
                ab_notes=(join(kv("name", row["name"])),)))
    return records, rejects
