"""R77 Akbar SAbDab Kd：与 R76 同源的 493 行，列名为 Antibody_ID / Antibody /
Antigen_ID / Antigen / Y。写法同 R76，值保持源的原样。"""
from __future__ import annotations

import ast
import csv
from pathlib import Path

from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R77"
DATA = Path("/data_new/ywy/dataset-abag/SRC_R77_AKBAR_SABDAB_KD/zenodo-13120765")
FILE = "antibody_affinity_protein_sabdab.csv"
SOURCE_ROWS = 493
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")


def adapt() -> tuple[list[Record], list[dict]]:
    records, rejects = [], []
    with (DATA / FILE).open(encoding="utf-8", newline="") as fh:
        for n, row in enumerate(csv.DictReader(fh), start=1):
            key = f"row={n}"
            try:
                parts = ast.literal_eval(row["Antibody"])
            except (ValueError, SyntaxError):
                parts = None
            if not isinstance(parts, (list, tuple)) or len(parts) != 2:
                rejects.append(reject("adapt", "bad_slot_list", SRC, key,
                                      {"Antibody": row["Antibody"]}))
                continue
            h = str(parts[0]) if parts[0] else None
            l = str(parts[1]) if parts[1] else None
            ag, y = row["Antigen"], row["Y"]
            if not h or not l or not ag or not ag.strip():
                rejects.append(reject("adapt", "missing_sequence", SRC, key,
                                      {"h": h, "l": l, "Antigen": ag}))
                continue
            if not y or not y.strip():
                rejects.append(reject("adapt", "no_observation", SRC, key, {"Y": y}))
                continue
            loc = locator(SRC, FILE, key, "Antibody_ID=" + row["Antibody_ID"])
            obs = {"label": y.strip(), "assay": None, "condition": None, "replicate": None,
                   "lineage": [join(loc, kv("col", "Y"))]}
            records.append(Record(
                key=key, h_raw=h, l_raw=l, ag_raw=(ag,), obs=(obs,),
                ab_evidence={"seqs": {"h": h, "l": l}, "placeholders": list(PLACEHOLDERS),
                             "structure": {"structure_id": row["Antibody_ID"].upper(),
                                           "file_ref": None,
                                           "chain_map": {"H": "H", "L": "L"}},
                             "structure_rank": 10},
                ag_evidence={"chains": [{"key": "A", "seq": ag}],
                             "placeholders": list(PLACEHOLDERS),
                             "structure": None, "structure_rank": None},
                ab_notes=(join(kv("Antibody_ID", row["Antibody_ID"])),),
                ag_notes=(join(kv("Antigen_ID", row["Antigen_ID"])),)))
    return records, rejects
