"""R10 AbRank：AbRank_dataset.csv（制表符分隔）342,356 行。

- 抗体：Ab_heavy_chain_seq / Ab_light_chain_seq；抗原：Ag_seq。逐行序列。
- 三个读数列：IC50 [ug/mL]、Affinity_Kd [nM]、escape，部分行多列并存，各成一条
  observation（aff 方案第 2 项）。值保持字符串原样，`>` / `<` 留在字符串里。
- log_Aff、log(Kd_ratio)、Aff_op 是派生列，不产出。
- 空值与 NA 不成立，记 adapt reject。
"""
from __future__ import annotations

from pathlib import Path

import csv

from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R10"
DATA = Path("/data_new/ywy/etl_out/SRC_R10/data/AbRank_dataset.csv")
FILE = "AbRank_dataset.csv"
SOURCE_ROWS = 342356
SHARDED = True
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")
EMPTY = ("", "NA", "N/A", "nan", "None", "NULL")
LABELS = ("Affinity_Kd [nM]", "IC50 [ug/mL]", "escape")


def _valid(value) -> bool:
    text = "" if value is None else str(value).strip()
    if text in EMPTY:
        return False
    try:
        float(text.lstrip("<>"))
    except ValueError:
        return False
    return True


def adapt():
    return _stream(), adapt.rejects


def _stream():
    with DATA.open(encoding="utf-8", newline="") as fh:
        for n, row in enumerate(csv.DictReader(fh, delimiter="\t"), start=2):
            key = "%s:row=%d" % (FILE, n)
            h = (row.get("Ab_heavy_chain_seq") or "").strip()
            l = (row.get("Ab_light_chain_seq") or "").strip()
            ag = (row.get("Ag_seq") or "").strip()
            if not h and not l:
                adapt.rejects.append(reject("adapt", "no_sequence", SRC, key,
                                            {"Ab_name": row.get("Ab_name")}))
                continue
            # RBD-escape 的 Ag_seq 实际是突变标记串（如 SARS-CoV2_(A410E)），不是序列；
            # 其余行的 Ag_seq 才是氨基酸串。只接受纯字母的抗原序列。
            if not ag or not ag.isalpha():
                adapt.rejects.append(reject("adapt", "no_antigen_sequence", SRC, key,
                                            {"Ag_name": row.get("Ag_name"),
                                             "Source": row.get("Source"),
                                             "Ag_seq": ag[:40]}))
                continue
            source = (row.get("Source") or "").strip() or "unknown"
            loc = locator(SRC, FILE, key, "Source=" + source,
                          "Ab_name=" + (row.get("Ab_name") or "NA"))
            obs = []
            for col in LABELS:
                value = (row.get(col) or "").strip()
                if not _valid(value):
                    continue
                obs.append({"label": value, "assay": None, "condition": source,
                            "replicate": None,
                            "lineage": [join(loc, kv("col", col))]})
            if not obs:
                adapt.rejects.append(reject("adapt", "no_observation", SRC, key,
                                            {"Source": source}))
                continue
            yield Record(
                key=key, h_raw=h, l_raw=l, ag_raw=(ag,), obs=tuple(obs),
                ab_evidence={"seqs": {"h": h, "l": l},
                             "placeholders": list(PLACEHOLDERS),
                             "structure": {"structure_id": row.get("Ab_PDB_ID") or None,
                                           "file_ref": None,
                                           "chain_map": {"H": "H", "L": "L"}}
                             if row.get("Ab_PDB_ID") not in (None, "", "NA") else None,
                             "structure_rank": 50},
                ag_evidence={"chains": [{"key": "A", "seq": ag}],
                             "placeholders": list(PLACEHOLDERS),
                             "structure": {"structure_id": row.get("Ag_PDB_ID") or None,
                                           "file_ref": None,
                                           "chain_map": {"A": "A"}}
                             if row.get("Ag_PDB_ID") not in (None, "", "NA") else None,
                             "structure_rank": 50},
                ab_notes=(join(kv("source", source)),),
                ag_notes=(join(kv("Ag_name", row.get("Ag_name") or "NA")),))


adapt.rejects = []
