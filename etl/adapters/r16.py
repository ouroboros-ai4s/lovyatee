"""R16 GUEST：42 个 docking case 的 Kd，抗体与抗原都由随包 PDB/FASTA 重建。

- 抗体：`Antibody PDB` 形如 `1L7I_HL`（H/L 两条链）或 `1N8Z_BAC` 这类多链写法；
  后缀字母按顺序对应结构的链，最后一位是抗原链的由 case 表决定。
  `5C2B` 是单链 scFv（单条 254 aa 链），按单链构建体处理。
- 抗原：`Antigen PDB` 形如 `2A91_A`，后缀字母是抗原链，可多链（`1TNF_ABC`）。
- observation：`Kd (nM)` 产出；`ΔG (kcal/mol)` 不产出（plan 的额外核对要求只产出 Kd）。
"""
from __future__ import annotations

import csv
from pathlib import Path

from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R16"
ROOT = Path("/data_new/ywy/dataset-abag/SRC_R16_GUEST/snapshot-2020-11-17")
CASES = ROOT / "antibody_benchmark/antibody_antigen_cases.txt"
AFFINITY = ROOT / "antibody_benchmark/antibody_antigen_affinities.txt"
PDB = ROOT / "pdb/structures"
SOURCE_ROWS = 42
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")


def _split(spec: str) -> tuple[str, str]:
    """`1L7I_HL` -> ('1L7I', 'HL')；`2A91_A` -> ('2A91','A')；
    `1J0S_A(6)` 这类括号后缀是 case 内编号，去掉。"""
    clean = spec.strip().split("(")[0]
    pdb, _, chains = clean.partition("_")
    return pdb.upper(), chains.upper()


def _open(pdb: str):
    from etl.core.structref import open_structure
    path = PDB / (pdb + ".cif.gz")
    if path.exists():
        import gzip, os
        out = Path("/data_new/ywy/cache/rcsb") / (pdb + ".cif")
        if not out.exists():
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(gzip.decompress(path.read_bytes()))
        return open_structure(out)
    return open_structure(pdb)


def adapt() -> tuple[list[Record], list[dict]]:
    cases = {}
    with CASES.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            cases[row["Complex PDB"].split("_")[0].upper()] = row
    records, rejects, cache = [], [], {}
    with AFFINITY.open(encoding="utf-8", newline="") as fh:
        for n, row in enumerate(csv.DictReader(fh, delimiter="\t"), start=2):
            case, kd = row["Case"].strip().upper(), row["Kd (nM)"].strip()
            key = "case=" + case
            if not kd:
                rejects.append(reject("adapt", "no_observation", SRC, key, {"Kd": kd}))
                continue
            meta = cases.get(case)
            if meta is None:
                rejects.append(reject("adapt", "unresolved", SRC, key,
                                      {"reason": "case 描述表无此 case"}))
                continue
            ab_pdb, ab_chains = _split(meta["Antibody PDB"])
            ag_pdb, ag_chains = _split(meta["Antigen PDB"])
            for pid in {ab_pdb, ag_pdb}:
                if pid not in cache:
                    try:
                        cache[pid] = _open(pid)
                    except Exception as exc:
                        cache[pid] = exc
            st_ab, st_ag = cache[ab_pdb], cache[ag_pdb]
            bad = [p for p, s in ((ab_pdb, st_ab), (ag_pdb, st_ag))
                   if isinstance(s, Exception)]
            if bad:
                rejects.append(reject("adapt", "unresolved", SRC, key,
                                      {"missing_structure": bad}))
                continue

            # 后缀里的 H / L 字母直接给出链型（可见 `3G6A_LH`）；没有字母时按结构链名取
            h_id = "H" if "H" in ab_chains else (ab_chains[0] if ab_chains else "")
            l_id = "L" if "L" in ab_chains else (ab_chains[1] if len(ab_chains) > 1 else "")
            single = len(ab_chains) <= 1
            h_rec = st_ab.chains.get(h_id)
            l_rec = None if single else st_ab.chains.get(l_id)
            ag_ids = list(ag_chains)
            ag_recs = [st_ag.chains.get(c) for c in ag_ids]
            if not all(ag_recs) or not any((h_rec, l_rec)):
                rejects.append(reject("adapt", "unresolved", SRC, key,
                                      {"antibody": meta["Antibody PDB"],
                                       "antigen": meta["Antigen PDB"]}))
                continue

            loc = locator(SRC, AFFINITY.name, key)
            obs = {"label": kd, "assay": None, "condition": None, "replicate": None,
                   "lineage": [join(loc, kv("col", "Kd (nM)"))]}
            ab_ev = {"seqs": {"h": h_rec.full_seq if h_rec else None,
                              "l": l_rec.full_seq if l_rec else None},
                     "placeholders": list(PLACEHOLDERS),
                     "hints": ({"h": {"single_chain": True}} if single else None),
                     "structure": {"structure_id": ab_pdb,
                                   "file_ref": str(PDB / (ab_pdb + ".cif.gz")),
                                   "chain_map": {"H": h_id, "L": l_id}},
                     "structure_rank": 10}
            ag_ev = {"chains": [{"key": r.chain_id, "seq": r.full_seq,
                                 "observed": list(r.observed_segments()),
                                 "entity": r.entity_id} for r in ag_recs],
                     "placeholders": list(PLACEHOLDERS),
                     "structure": {"structure_id": ag_pdb,
                                   "file_ref": str(PDB / (ag_pdb + ".cif.gz")),
                                   "chain_map": {r.chain_id: r.chain_id for r in ag_recs}},
                     "structure_rank": 10}
            records.append(Record(
                key=key, h_raw=h_rec.full_seq if h_rec else None,
                l_raw=l_rec.full_seq if l_rec else None,
                ag_raw=tuple(r.full_seq for r in ag_recs), obs=(obs,),
                ab_evidence=ab_ev, ag_evidence=ag_ev,
                ab_notes=(join(kv("antibody", meta["Antibody"])),),
                ag_notes=(join(kv("antigen", meta["Antigen"])),)))
    return records, rejects
