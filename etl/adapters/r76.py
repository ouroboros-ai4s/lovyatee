"""R76 TDC AntibodyAff：protein_sabdab.csv，X1 = [重链, 轻链] 列表字符串。

值保持源的原样：X1 两元素原字符串进 h_raw/l_raw，X2 原字符串进 ag_raw，
Y 原字符串进 label（无单位无 assay，按 aff 方案第 3 项只写 col=Y）。
"""
from __future__ import annotations

import ast
import csv
from pathlib import Path

from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R76"
DATA = Path("/data_new/ywy/dataset-abag/SRC_R76_TDC_ANTIBODYAFF/dataverse-v105")
FILE = "protein_sabdab.csv"
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")


def _slots(x1: str) -> tuple[str | None, str | None]:
    try:
        parts = ast.literal_eval(x1)
    except (ValueError, SyntaxError):
        return None, None
    if not isinstance(parts, (list, tuple)):
        return None, None
    h = str(parts[0]) if len(parts) > 0 and parts[0] else None
    l = str(parts[1]) if len(parts) > 1 and parts[1] else None
    return h, l


def adapt() -> tuple[list[Record], list[dict]]:
    records, rejects = [], []
    with (DATA / FILE).open(encoding="utf-8", newline="") as fh:
        for n, row in enumerate(csv.DictReader(fh), start=1):
            key = f"row={n}"
            h, l = _slots(row["X1"])
            # X1 必须正好两个槽位；否则是源格式异常，进 adapt reject
            try:
                parts = ast.literal_eval(row["X1"])
            except (ValueError, SyntaxError):
                parts = None
            if not isinstance(parts, (list, tuple)) or len(parts) != 2:
                rejects.append(reject("adapt", "bad_slot_list", SRC, key,
                                      {"X1": row["X1"]}))
                continue
            x2 = row["X2"]
            y = row["Y"]
            if not h or not l or not x2 or not x2.strip():
                rejects.append(reject("adapt", "missing_sequence", SRC, key,
                                      {"h": h, "l": l, "x2": x2}))
                continue
            if not y or not y.strip():
                rejects.append(reject("adapt", "no_observation", SRC, key, {"Y": y}))
                continue
            loc = locator(SRC, FILE, key, "ID1=" + row["ID1"])
            obs = {"label": y.strip(), "assay": None, "condition": None, "replicate": None,
                   "lineage": [join(loc, kv("col", "Y"))]}
            records.append(Record(
                key=key, h_raw=h, l_raw=l, ag_raw=(x2,), obs=(obs,),
                ab_evidence={"seqs": {"h": h, "l": l}, "placeholders": list(PLACEHOLDERS),
                             "structure": {"structure_id": row["ID1"].upper(),
                                           "file_ref": None,
                                           "chain_map": {"H": "H", "L": "L"}},
                             "structure_rank": 10},
                ag_evidence={"chains": [{"key": "A", "seq": x2}], "placeholders": list(PLACEHOLDERS),
                             "structure": None, "structure_rank": None},
                ab_notes=(join(kv("ID1", row["ID1"])),), ag_notes=(join(kv("ID2", row["ID2"])),)))
    return records, rejects
