"""R08 AVIDa-hTNFa：5,580 行 VHH + 单一固定抗原 TNFa-WT-beads。

抗原序列来自 antigen_sequences.csv（决策文件 R08 C1）。`corpus-hTNFa.csv` 无 label，
其行按 aff 方案第 1 项不成立，进 adapt reject 而不是静默丢弃。
"""
from __future__ import annotations

import csv
from pathlib import Path

from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R08"
DATA = Path("/data_new/ywy/dataset-abag/SRC_R08_AVIDA_HTNFA/snapshot-2025-06-26/AVIDa-hTNFa")
FILE = "AVIDa-hTNFa.csv"
CORPUS = "corpus-hTNFa.csv"
SOURCE_ROWS = 5580 + 216225
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")


def _antigen() -> str:
    with (DATA / "antigen_sequences.csv").open(encoding="utf-8", newline="") as fh:
        row = next(csv.DictReader(fh))
    return row["Ag_sequence"]


def adapt() -> tuple[list[Record], list[dict]]:
    ag = _antigen()
    records, rejects = [], []
    with (DATA / FILE).open(encoding="utf-8", newline="") as fh:
        for n, row in enumerate(csv.DictReader(fh), start=1):
            key = f"row={n}"
            seq, label = row["VHH_sequence"], row["label"]
            if not seq or not seq.strip():
                rejects.append(reject("adapt", "missing_sequence", SRC, key, {"VHH_sequence": seq}))
                continue
            if label is None or not str(label).strip():
                # 有记录无值：空不是 negative（aff 方案第 1 项）
                rejects.append(reject("adapt", "no_observation", SRC, key, {"label": label}))
                continue
            loc = locator(SRC, FILE, key)
            obs = {"label": str(label).strip(), "assay": None,
                   "condition": row["Ag_label"], "replicate": None,
                   "lineage": [join(loc, kv("col", "label"))]}
            records.append(Record(
                key=key, h_raw=seq, ag_raw=(ag,), obs=(obs,),
                ab_evidence={"seqs": {"h": seq, "l": None},
                             "placeholders": list(PLACEHOLDERS),
                             "structure": None, "structure_rank": None},
                ag_evidence={"chains": [{"key": "A", "seq": ag}],
                             "placeholders": list(PLACEHOLDERS),
                             "structure": {"structure_id": "1TNF", "file_ref": None,
                                           "chain_map": {"A": "A"}},
                             "structure_rank": 50,
                             "notes": ["decision=R08:C1"]},
                ag_notes=(join(kv("Ag_label", row["Ag_label"])),)))
    # 无 label 语料：整源不成立，逐行进 reject 以便对账
    with (DATA / CORPUS).open(encoding="utf-8", newline="") as fh:
        for n, row in enumerate(csv.DictReader(fh), start=1):
            rejects.append(reject("adapt", "no_observation", SRC, f"{CORPUS}:row={n}",
                                  {"source": CORPUS}))
    return records, rejects
