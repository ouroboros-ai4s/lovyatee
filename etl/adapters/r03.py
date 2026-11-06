"""R03 AbDesign 1.0：AbDesign/datasets_mut.csv 1,303 行（逐行完整重/轻链 + 抗原序列）。

每个突变体行就是一个 pair：A 类序列直接搬入，突变字段只进 lineage。
`affinity_type` 是长表类型列（`ddg` / `elisa_mut_to_wt_ratio`），按 aff 方案第 3 项
以 `affinity_type=<取值>` 写进该 observation 的 lineage。
`datasets_wt.csv` 的 57 行是 WT 参照、无 label，不产出 observation，逐行进 adapt reject。
"""
from __future__ import annotations

import csv
from pathlib import Path

from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R03"
DATA = Path("/data_new/ywy/dataset-abag/SRC_R03_ABDESIGN_DB/snapshot-2025-08-26/AbDesign")
MUT = "datasets_mut.csv"
WT = "datasets_wt.csv"
SOURCE_ROWS = 1303 + 57
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")


def _mut_name(row: dict) -> str:
    return "%s%s%s>%s" % (row["mutation_chain_id"], row["mutation_pos"],
                          row["orig_residue"], row["new_residue"])


def adapt() -> tuple[list[Record], list[dict]]:
    records, rejects = [], []
    with (DATA / MUT).open(encoding="utf-8", newline="") as fh:
        for n, row in enumerate(csv.DictReader(fh), start=2):
            key = "row=" + str(n)
            h, l, ag = row["heavy_sequence"], row["light_sequence"], row["antigen_sequence"]
            if not h.strip() or not l.strip() or not ag.strip():
                rejects.append(reject("adapt", "no_sequence", SRC, key,
                                      {"pdb": row["pdb_name"], "dataset": row["dataset"]}))
                continue
            if not row["affinity"].strip():
                rejects.append(reject("adapt", "no_observation", SRC, key,
                                      {"affinity": row["affinity"]}))
                continue
            loc = locator(SRC, MUT, key, "pdb_name=" + row["pdb_name"],
                          "method=" + row["method"])
            obs = {"label": row["affinity"].strip(),
                   "assay": row["method"] or None,
                   "condition": row["dataset"] or None, "replicate": None,
                   "lineage": [join(loc, kv("col", "affinity"),
                                    kv("affinity_type", row["affinity_type"]))]}
            records.append(Record(
                key=key, h_raw=h, l_raw=l, ag_raw=(ag,), obs=(obs,),
                ab_evidence={"seqs": {"h": h, "l": l}, "placeholders": list(PLACEHOLDERS),
                             "structure": {"structure_id": row["pdb_name"].upper(),
                                           "file_ref": None,
                                           "chain_map": {"H": row["orig_heavy_chain_id"],
                                                         "L": row["orig_light_chain_id"]}},
                             "structure_rank": 50},
                ag_evidence={"chains": [{"key": row["orig_antigen_chain_id"] or "A", "seq": ag}],
                             "placeholders": list(PLACEHOLDERS),
                             "structure": {"structure_id": row["pdb_name"].upper(),
                                           "file_ref": None,
                                           "chain_map": {row["orig_antigen_chain_id"] or "A": "A"}},
                             "structure_rank": 50},
                ab_notes=(join(kv("mutation", _mut_name(row))),)))
    # WT 参照行：无 label，不产出 observation（aff 方案第 1 项 类 1）
    with (DATA / WT).open(encoding="utf-8", newline="") as fh:
        for n, row in enumerate(csv.DictReader(fh), start=2):
            rejects.append(reject("adapt", "no_observation", SRC, WT + ":row=" + str(n),
                                  {"pdb_name": row["pdb_name"], "reason": "wt_reference"}))
    return records, rejects
