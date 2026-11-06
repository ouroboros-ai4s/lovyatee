"""R80 ANTIPASTI：sabdab_summary_all.tsv 1,266 行；抗体与抗原序列均由随包 PDB 重建。

- 抗体：Hchain / Lchain 指向结构内链；scfv=True 的行把单链放 H 槽，由 pair_slots
  按单链处理（含 linker 时走 split）。Lchain 为 NA 的行只给 H 槽。
- 抗原：antigen_chain 可以是多链（E | G），按顺序全部入库，链序参与 AG_ID。
- antigen_type 不是 protein / peptide 的行按 non_protein 排除；结构里链不存在或
  无法重建的行按 unresolved。
- affinity 产出，delta_g 不产出（aff 方案第 2 项）。
"""
from __future__ import annotations

import csv
from pathlib import Path

from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R80"
ROOT = Path("/data_new/ywy/dataset-abag/SRC_R80_ANTIPASTI/v1")
FILE = "ANTIPASTI/data/sabdab_summary_all.tsv"
PDBDIR = ROOT / "mendeley-data"
SOURCE_ROWS = 1266
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")
PROTEIN_TYPES = ("protein", "peptide")


def _structure(pdb: str):
    from etl.core.structref import open_structure
    return open_structure(PDBDIR / (pdb.lower() + ".pdb"))


def _chains(spec: str) -> list[str]:
    return [c.strip() for c in (spec or "").split("|")
            if c.strip() not in ("", "NA")]


def adapt() -> tuple[list[Record], list[dict]]:
    with (ROOT / FILE).open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    records, rejects, cache = [], [], {}
    for n, row in enumerate(rows, start=2):
        key = "row=" + str(n)
        pdb = row["pdb"].strip().upper()
        ag_type = (row["antigen_type"] or "").strip()
        if not any(ag_type.startswith(t) for t in PROTEIN_TYPES):
            rejects.append(reject("adapt", "non_protein", SRC, key,
                                  {"pdb": pdb, "antigen_type": ag_type}))
            continue
        if not row["affinity"].strip():
            rejects.append(reject("adapt", "no_observation", SRC, key,
                                  {"affinity": row["affinity"]}))
            continue
        if pdb not in cache:
            try:
                cache[pdb] = _structure(pdb)
            except Exception as exc:
                cache[pdb] = exc
        st = cache[pdb]
        if isinstance(st, Exception):
            rejects.append(reject("adapt", "unresolved", SRC, key,
                                  {"pdb": pdb, "error": type(st).__name__}))
            continue

        h_id, l_id = row["Hchain"].strip(), row["Lchain"].strip()
        ag_ids = _chains(row["antigen_chain"])
        missing = [c for c in [h_id, l_id] + ag_ids
                   if c not in ("", "NA") and c not in st.chains]
        if missing:
            rejects.append(reject("adapt", "unresolved", SRC, key,
                                  {"pdb": pdb, "missing_chains": missing}))
            continue

        is_scfv = row["scfv"].strip().lower() == "true"
        h_rec = st.chains.get(h_id) if h_id not in ("", "NA") else None
        l_rec = st.chains.get(l_id) if l_id not in ("", "NA") else None
        ag_recs = [st.chains[c] for c in ag_ids]
        if not ag_recs or not all(r.is_protein for r in ag_recs):
            rejects.append(reject("adapt", "non_protein", SRC, key,
                                  {"pdb": pdb, "antigen_chain": row["antigen_chain"]}))
            continue
        if not h_rec and not l_rec:
            rejects.append(reject("adapt", "unresolved", SRC, key,
                                  {"pdb": pdb, "Hchain": h_id, "Lchain": l_id}))
            continue

        loc = locator(SRC, FILE, key, "pdb=" + pdb)
        obs = {"label": row["affinity"].strip(),
               "assay": (row["affinity_method"]
                         if row["affinity_method"] not in ("NA", "") else None),
               "condition": None, "replicate": None,
               "lineage": [join(loc, kv("col", "affinity"))]}
        ref = str(PDBDIR / (pdb.lower() + ".pdb"))
        ab_ev = {
            "seqs": {"h": h_rec.full_seq if h_rec else None,
                     "l": None if is_scfv else (l_rec.full_seq if l_rec else None)},
            "placeholders": list(PLACEHOLDERS),
            "hints": ({"h": {"single_chain": True}, "l": {"single_chain": True}}
                      if is_scfv else None),
            "structure": {"structure_id": pdb, "file_ref": ref,
                          "chain_map": {"H": h_id, "L": l_id}},
            "structure_rank": 10,
        }
        ag_ev = {
            "chains": [{"key": r.chain_id, "seq": r.full_seq,
                        "observed": list(r.observed_segments()), "entity": r.entity_id}
                       for r in ag_recs],
            "placeholders": list(PLACEHOLDERS),
            "structure": {"structure_id": pdb, "file_ref": ref,
                          "chain_map": {r.chain_id: r.chain_id for r in ag_recs}},
            "structure_rank": 10,
        }
        records.append(Record(
            key=key,
            h_raw=h_rec.full_seq if h_rec else None,
            l_raw=l_rec.full_seq if l_rec else None,
            ag_raw=tuple(r.full_seq for r in ag_recs), obs=(obs,),
            ab_evidence=ab_ev, ag_evidence=ag_ev,
            ab_notes=(join(kv("pdb", pdb), kv("scfv", is_scfv)),),
            ag_notes=(join(kv("antigen_name", row["antigen_name"])),)))
    return records, rejects
