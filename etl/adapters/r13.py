"""R13 ANDD：ANDD_v2.xlsx 单表 48,800 行。

- 抗体：`Ab/Nano H_Chain AA` / `Ab/Nano L_Chain AA`，占位 `\` 与 `N/A`。
- 抗原：`Ag_Seq`，多链以 `/` 分隔，按顺序入库（链序参与 AG_ID）。
- observation：`Affinity_Kd(M)...` 有值产出 Kd；否则 `∆Gbinding(kJ/mol)...` 有值产出 ΔG；
  两列都空的行不成立。`Predicted_or_Not` 写进 lineage（aff 方案第 4 项）。
- 恒定区由 `vdomain` 裁剪；H/L 槽内的 scFv 由 `pair_slots` 按单链处理。
"""
from __future__ import annotations

import openpyxl
from pathlib import Path

from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R13"
DATA = Path("/data_new/ywy/dataset-abag/SRC_R13_ANDD/snapshot-2026-01-05/ANDD")
FILE = "Antibody and Nanobody Design Dataset (ANDD)_v2.xlsx"
COL_H = "Ab/Nano H_Chain AA"
COL_L = "Ab/Nano L_Chain AA"
COL_AG = "Ag_Seq"
COL_KD = ("Affinity_Kd(M), (the near-physiological conditions, with controlled temperatures "
          "(20-25 °C or 37 °C) and buffered aqueous systems)")
COL_DG = ("∆Gbinding(kJ/mol),(the near-equilibrium conditions at constant temperatures "
          "(20-25 °C) )")
COL_PRED = "Predicted_or_Not"
COL_METHOD = "Affinity_Method"
COL_SRC = "Source"
COL_PDB = "PDB_ID"
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")
EMPTY = ("", "NA", "N/A", "\\", "None", "nan", "NULL")


def _text(value) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return None if text in EMPTY else text


SOURCE_ROWS = 48800     # 已核对：xlsx 单表 48,800 条数据行


def adapt() -> tuple[list[Record], list[dict]]:
    wb = openpyxl.load_workbook(DATA / FILE, read_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = ws.iter_rows(values_only=True)
    header = list(next(rows))
    ix = {name: i for i, name in enumerate(header)}
    records, rejects = [], []
    n = 0
    for n, row in enumerate(rows, start=2):
        key = "row=" + str(n)
        h, l = _text(row[ix[COL_H]]), _text(row[ix[COL_L]])
        ag_raw = _text(row[ix[COL_AG]])
        if not h and not l:
            rejects.append(reject("adapt", "no_sequence", SRC, key, {"H": h, "L": l}))
            continue
        if not ag_raw:
            rejects.append(reject("adapt", "no_antigen_sequence", SRC, key, {"Ag_Seq": ag_raw}))
            continue
        kd, dg = _text(row[ix[COL_KD]]), _text(row[ix[COL_DG]])
        predicted = _text(row[ix[COL_PRED]]) or "\\"
        method = _text(row[ix[COL_METHOD]])
        source = _text(row[ix[COL_SRC]]) or "unknown"
        loc = locator(SRC, FILE, key, "Source=" + source,
                      "PDB_ID=" + (_text(row[ix[COL_PDB]]) or "NA"))
        if kd is not None:
            col, label = COL_KD, kd
        elif dg is not None:
            col, label = COL_DG, dg
        else:
            rejects.append(reject("adapt", "no_observation", SRC, key,
                                  {"Kd": kd, "dG": dg, "Predicted_or_Not": predicted}))
            continue
        obs = {"label": label,
               "assay": method,
               "condition": source, "replicate": None,
               "lineage": [join(loc, kv("col", col), kv("Predicted_or_Not", predicted))]}
        chains = [c.strip() for c in ag_raw.split("/") if c.strip()]
        records.append(Record(
            key=key, h_raw=h, l_raw=l, ag_raw=tuple(chains), obs=(obs,),
            ab_evidence={"seqs": {"h": h, "l": l}, "placeholders": list(PLACEHOLDERS),
                         "structure": None, "structure_rank": None},
            ag_evidence={"chains": [{"key": "A" + str(i) if i else "A", "seq": c}
                                    for i, c in enumerate(chains)],
                         "placeholders": list(PLACEHOLDERS),
                         "structure": None, "structure_rank": None}))
    return records, rejects
