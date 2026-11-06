"""R14 AB-Bind：突变体目录，逐行只有亲本 PDB 名与突变列表。

- 亲本：`AB-Bind-Database/<PDB>.pdb`（32 个，含 4 个 `HM_` 同源模型）。
- 抗体链与抗原链：`Partners(A_B)` 是 `链_链`；链名 H/L 直接说明抗体侧，其余按
  `Protein-1/2` 文本判断。抗体链进 `seqs`，其余链进抗原。
- 突变 `链:原残基位置新残基`（作者编号，插入码可为字母）。按链归属分别交给
  `mutate.apply_point`；无法归属的记 `mutation_unassigned`。
- `Fc-only` 排除：1T83、3WJJ。
- `ddG(kcal/mol)` 是唯一 label，`Assay Name` 进 assay。
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

from etl.b import structure_parents as sp
from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R14"
ROOT = Path("/data_new/ywy/dataset-abag/SRC_R14_ABBIND/snapshot-2019-04-10")
DATA = ROOT / "AB-Bind-Database"
FILE = "AB-Bind_experimental_data.csv"
SOURCE_ROWS = 1101          # 数据行 1,100；行号从 2 起，覆盖到 1,101
EXCLUDE = {"1T83", "3WJJ"}
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")
MUT = re.compile(r"([A-Za-z0-9]+):([A-Z])(\d+)([A-Za-z]?)([A-Z])")
AB_HINTS = ("mab", "fab", "fv", "igg", "antibody", "herceptin", "cetuximab",
            "d1.3", "b12", "vrc01", "cr1", "ar2", "jel42", "a6", "e5.2", "ab")


def _parse_mutations(text):
    out = []
    for part in (text or "").split(","):
        part = part.strip()
        if not part or "(" in part:
            continue
        m = MUT.fullmatch(part)
        if m:
            chain, orig, pos, ins, new = m.groups()
            out.append((chain, orig, int(pos), ins, new))
    return out


def _is_antibody(ref, chain):
    """用 ANARCI 判定：能编号成 H / K / L 域的链就是抗体链。"""
    from etl.core.vdomain import parse
    try:
        rec = sp.chain(ref, chain)
    except Exception:
        return False
    return rec.is_protein and bool(parse(rec.full_seq).domains)


def _expand(partners):
    """`A_HL` -> ['A','H','L']；`AB_CD` -> ['A','B','C','D']。下划线两侧各是链组。"""
    out = []
    for group in partners.split("_"):
        out.extend(list(group.strip())) if len(group) > 1 else out.append(group.strip())
    return [c for c in out if c]


def _split_sides(ref, partners):
    """返回 (抗体链, 抗原链)。链名只作兜底，主判据是 ANARCI 是否认出免疫球蛋白域。"""
    chains = _expand(partners)
    ab = [c for c in chains if _is_antibody(ref, c) or c.upper() in ("H", "L")]
    ag = [c for c in chains if c not in ab]
    return ab, ag


def adapt():
    records, rejects = [], []
    with (DATA / FILE).open(encoding="latin-1", newline="") as fh:
        for n, row in enumerate(csv.DictReader(fh), start=2):
            pdb = row["#PDB"].strip().upper()
            key = "%s:row=%d" % (pdb, n)
            if pdb in EXCLUDE:
                rejects.append(reject("adapt", "no_antigen_binding", SRC, key,
                                      {"reason": "Fc-only", "pdb": pdb}))
                continue
            ddg = row["ddG(kcal/mol)"].strip()
            if not ddg:
                rejects.append(reject("adapt", "no_observation", SRC, key, {"pdb": pdb}))
                continue
            ref = DATA / (row["#PDB"].strip() + ".pdb")
            if not ref.exists():
                rejects.append(reject("adapt", "unresolved", SRC, key,
                                      {"pdb": pdb, "reason": "no structure file"}))
                continue
            partners = row["Partners(A_B)"].strip()
            ab, ag = _split_sides(ref, partners)
            if not ab:
                rejects.append(reject("adapt", "unresolved", SRC, key,
                                      {"pdb": pdb, "partners": partners}))
                continue
            if not ag:
                rejects.append(reject("adapt", "no_antigen_binding", SRC, key,
                                      {"pdb": pdb, "partners": partners}))
                continue
            muts = _parse_mutations(row["Mutation"])
            if not muts:
                rejects.append(reject("adapt", "mutation_unassigned", SRC, key,
                                      {"mutation": row["Mutation"]}))
                continue
            ab_edits, ag_edits, unassigned = [], [], []
            for i, (chain, orig, pos, ins, new) in enumerate(muts):
                slot = "H" if chain.upper() == "H" else ("L" if chain.upper() == "L" else chain)
                edit = {"id": "m%d" % i, "chain": slot, "orig": orig, "pos": pos,
                        "new": new, "numbering": "pdb_author", "ins": ins}
                if chain in ab:
                    ab_edits.append(edit)
                elif chain in ag:
                    ag_edits.append(edit)
                else:
                    unassigned.append(chain + ":" + orig + str(pos) + ins + new)
            if unassigned:
                rejects.append(reject("adapt", "mutation_unassigned", SRC, key,
                                      {"unassigned": unassigned, "pdb": pdb}))
                continue
            try:
                parents = {c: sp.parent_chain(ref, c) for c in ab + ag}
            except Exception as exc:
                rejects.append(reject("adapt", "unresolved", SRC, key,
                                      {"pdb": pdb, "error": type(exc).__name__}))
                continue
            h_chain = next((c for c in ab if c.upper() == "H"), ab[0])
            l_chain = next((c for c in ab if c.upper() == "L"), None)
            ag_chains = [c for c in ag if parents.get(c, {}).get("seq")]
            if not ag_chains:
                rejects.append(reject("adapt", "no_antigen_binding", SRC, key,
                                      {"pdb": pdb, "antigen_chains": ag}))
                continue
            loc = locator(SRC, FILE, "row=" + str(n), "PDB=" + pdb)
            obs = {"label": ddg, "assay": row["Assay Name"] or None,
                   "condition": row["Protein-2"] or None, "replicate": None,
                   "lineage": [join(loc, kv("col", "ddG(kcal/mol)"),
                                    kv("mutation", row["Mutation"]))]}
            records.append(Record(
                key=key,
                h_raw=parents[h_chain]["seq"],
                l_raw=parents[l_chain]["seq"] if l_chain else None,
                ag_raw=tuple(parents[c]["seq"] for c in ag_chains), obs=(obs,),
                ab_evidence={"seqs": {"h": parents[h_chain]["seq"],
                                      "l": parents[l_chain]["seq"] if l_chain else None},
                             "placeholders": list(PLACEHOLDERS),
                             "edits": ab_edits, "entity": "ab",
                             "structure": {"structure_id": pdb, "file_ref": str(ref),
                                           "chain_map": {"H": h_chain,
                                                         "L": l_chain or ""}},
                             "structure_rank": 10},
                ag_evidence={"chains": [{"key": c, "seq": parents[c]["seq"]}
                                        for c in ag_chains],
                             "placeholders": list(PLACEHOLDERS),
                             "edits": ag_edits, "entity": "ag",
                             "structure": {"structure_id": pdb, "file_ref": str(ref),
                                           "chain_map": {c: c for c in ag_chains}},
                             "structure_rank": 10},
                ab_ctx={"parents": {c: parents[c] for c in ab},
                        "h_chain": h_chain, "l_chain": l_chain or ""},
                ag_ctx={"parents": {c: parents[c] for c in ag_chains}},
                ab_notes=(join(kv("protein", row["Protein-1"])),),
                ag_notes=(join(kv("protein", row["Protein-2"])),)))
    return records, rejects
