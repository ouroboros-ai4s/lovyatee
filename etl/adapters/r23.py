"""R23 MIT-LL AlphaSeq：MITLL_AAlphaBio_Ab_Binding_dataset.csv，1,259,700 行。

- 抗体：HC / LC 两列逐行给可变域序列。`Sequence` 是 HC-G4S-LC 的完整 scFv，不另用。
- 抗原：固定 14 aa 肽 PDVDLGDISGINAS（决策文件 R23 C1），CSV 无逐行抗原字段。
  4 个 Target：MIT_Target 是正靶，AlphaNeg1~3 是负对照且没有来源序列，
  按 no_antigen_binding 排除（决策文件 C2）。
- 观察值：Pred_affinity（log10 Kd nM）唯一读数；空值不成立。
- Assay 与 Replicate 进 observation 的 assay / replicate 字段。
"""
from __future__ import annotations

import csv
from pathlib import Path

from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R23"
DATA = Path("/data_new/ywy/etl_out/SRC_R23/data/"
            "mit-ll-AlphaSeq_Antibody_Dataset-18c7c07/"
            "MITLL_AAlphaBio_Ab_Binding_dataset.csv")
FILE = DATA.name
SOURCE_ROWS = 1259700
SHARDED = True
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")
EMPTY = ("", "NA", "N/A", "nan", "None", "NULL")
POSITIVE = "MIT_Target"
PEPTIDE = "PDVDLGDISGINAS"      # 决策文件 R23 C1


def _valid(value) -> bool:
    text = "" if value is None else str(value).strip()
    if text in EMPTY:
        return False
    try:
        float(text)
    except ValueError:
        return False
    return True


def adapt():
    return _stream(), adapt.rejects


def _stream():
    with DATA.open(encoding="utf-8", newline="") as fh:
        for n, row in enumerate(csv.DictReader(fh), start=2):
            key = "row=%d" % n
            target = (row.get("Target") or "").strip()
            if target != POSITIVE:
                adapt.rejects.append(reject("adapt", "no_antigen_binding", SRC, key,
                                            {"Target": target,
                                             "decision": "R23:C2"}))
                continue
            h = (row.get("HC") or "").strip()
            l = (row.get("LC") or "").strip()
            if not h and not l:
                adapt.rejects.append(reject("adapt", "no_sequence", SRC, key,
                                            {"POI": row.get("POI")}))
                continue
            value = (row.get("Pred_affinity") or "").strip()
            if not _valid(value):
                adapt.rejects.append(reject("adapt", "no_observation", SRC, key,
                                            {"Target": target,
                                             "Pred_affinity": value}))
                continue
            assay = (row.get("Assay") or "").strip() or None
            replicate = (row.get("Replicate") or "").strip() or None
            loc = locator(SRC, FILE, key, "Target=" + target,
                          "Assay=" + (assay or "NA"))
            obs = {"label": value, "assay": None,
                   "condition": "%s assay %s" % (target, assay or "NA"),
                   "replicate": replicate,
                   "lineage": [join(loc, kv("col", "Pred_affinity"),
                                    kv("POI", row.get("POI") or "NA"))]}
            yield Record(
                key=key, h_raw=h, l_raw=l, ag_raw=(PEPTIDE,), obs=(obs,),
                ab_evidence={"seqs": {"h": h, "l": l},
                             "placeholders": list(PLACEHOLDERS),
                             "structure": None, "structure_rank": None},
                ag_evidence={"chains": [{"key": "P", "seq": PEPTIDE}],
                             "placeholders": list(PLACEHOLDERS),
                             "structure": {"structure_id": "6LXT", "file_ref": None,
                                           "chain_map": {"P": "A"}},
                             "structure_rank": 50,
                             "notes": ["decision=R23:C1"]})


adapt.rejects = []
