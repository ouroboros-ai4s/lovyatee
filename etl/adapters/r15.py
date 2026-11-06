"""R15 SKEMPI 2.0：`skempi_v2.csv`（分号分隔）7,085 行，突变数据库。

- `#Pdb` 形如 `1CSE_E_I`：PDB 加两侧链组，按顺序是 Protein 1 / Protein 2。
- 两侧序列都由随包结构恢复；抗体侧用 ANARCI 判定，另一侧是抗原。
- `Mutation(s)_PDB` 形如 `LI45G`（链 + 原残基 + 位置 + 新残基），插入码可为字母，
  多突变用逗号分隔，可以落在任一侧。
- 每个源行产出两条 record：`mut` 用突变后序列与 `Affinity_mut`，`wt` 不改序列、
  用 `Affinity_wt`（problem_aff 第 2 项）。
- 两侧都无法编号成免疫球蛋白域时按 `no_antigen_binding` 排除。
- `n.b` / `unf` 不成立；`<` `>` 边界值成立并原样保留。
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

from etl.b import structure_parents as sp
from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R15"
ROOT = Path("/data_new/ywy/dataset-abag/SRC_R15_SKEMPI2/2.0")
DATA = ROOT / "SKEMPI2"
FILE = "skempi_v2.csv"
STRUCT = ROOT / "pdb" / "structures"
SOURCE_ROWS = 7085
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")
# aff 方案第 1 项：n.b / n.b. 是"检测不到结合"的定性判定，成立；unf 是实验失败，不成立
NOT_VALID = ("unf", "nan", "NA", "N/A", "")
# SKEMPI 写法：<原残基><链><位置><插入码><新残基>，例如 LI45G 是链 I 第 45 位 L->G
MUT = re.compile(r"^([A-Z])([A-Za-z])(\d+)([A-Za-z]?)([A-Z])$")


def _ref(pdb: str):
    for cand in (STRUCT / pdb, STRUCT / (pdb + ".pdb"), STRUCT / (pdb + ".cif"),
                 STRUCT / (pdb + ".cif.gz")):
        if cand.exists():
            return cand
    return pdb


def _parse_mutations(text: str):
    out = []
    for raw in (text or "").split(","):
        raw = raw.strip()
        if not raw:
            continue
        m = MUT.match(raw)
        if not m:
            return []
        orig, head, pos, ins, new = m.groups()
        out.append((head, orig, int(pos), ins, new))
    return out


def _valid_affinity(value: str) -> bool:
    text = (value or "").strip()
    if not text or text.lower() in NOT_VALID:
        return False
    if text.lower() in ("n.b", "n.b."):
        return True                 # 定性判定，原字符串进 label
    try:
        float(text.lstrip("<>"))
    except ValueError:
        return False
    return True


def _is_antibody(ref, chain: str) -> bool:
    from etl.core.vdomain import parse
    try:
        rec = sp.chain(ref, chain)
    except Exception:
        return False
    return rec.is_protein and bool(parse(rec.full_seq).domains)


def _expand(group: str):
    return list(group) if len(group) > 1 else [group]


def adapt():
    records, rejects = [], []
    with (DATA / FILE).open(encoding="latin-1", newline="") as fh:
        for n, row in enumerate(csv.DictReader(fh, delimiter=";"), start=2):
            pdb_field = row["#Pdb"].strip()
            base = "%s:row=%d" % (pdb_field, n)
            parts = pdb_field.split("_")
            pdb = parts[0].upper()
            chains_1 = _expand(parts[1]) if len(parts) > 1 else []
            chains_2 = _expand(parts[2]) if len(parts) > 2 else []
            ref = _ref(pdb)

            ab1 = [c for c in chains_1 if _is_antibody(ref, c)]
            ab2 = [c for c in chains_2 if _is_antibody(ref, c)]
            ab = ab1 or ab2
            ag = chains_2 if ab1 else (chains_1 if ab2 else [])
            if not ab or not ag:
                rejects.append(reject("adapt", "no_antigen_binding", SRC, base,
                                      {"pdb": pdb_field,
                                       "protein1": row["Protein 1"],
                                       "protein2": row["Protein 2"]}))
                continue

            muts = _parse_mutations(row["Mutation(s)_PDB"])
            if not muts:
                rejects.append(reject("adapt", "mutation_unassigned", SRC, base,
                                      {"mutation": row["Mutation(s)_PDB"]}))
                continue
            ab_edits, ag_edits, bad = [], [], []
            for i, (head, orig, pos, ins, new) in enumerate(muts):
                if head not in ab and head not in ag:
                    bad.append(head + orig + str(pos) + ins + new)
                    continue
                edit = {"id": "m%d" % i, "chain": head, "orig": orig,
                        "pos": pos, "new": new, "numbering": "pdb_author",
                        "ins": ins}
                (ab_edits if head in ab else ag_edits).append(edit)
            if bad:
                rejects.append(reject("adapt", "mutation_unassigned", SRC, base,
                                      {"unassigned": bad}))
                continue

            try:
                parents = {c: sp.parent_chain(ref, c) for c in ab + ag}
            except Exception as exc:
                rejects.append(reject("adapt", "unresolved", SRC, base,
                                      {"pdb": pdb_field,
                                       "error": type(exc).__name__}))
                continue

            h_chain = next((c for c in ab if c.upper() == "H"), ab[0])
            l_chain = next((c for c in ab if c.upper() == "L"), None)
            ag_chains = [c for c in ag if parents[c]["seq"]]
            if not ag_chains:
                rejects.append(reject("adapt", "no_antigen_binding", SRC, base,
                                      {"pdb": pdb_field, "antigen_chains": ag}))
                continue

            method = row["Method"] or None
            temp = row["Temperature"] or None
            loc = locator(SRC, FILE, "row=" + str(n), "PDB=" + pdb_field,
                          "method=" + (method or "NA"),
                          "temperature=" + (temp or "NA"))
            for branch, text, col in (
                    ("mut", row["Affinity_mut (M)"], "Affinity_mut (M)"),
                    ("wt", row["Affinity_wt (M)"], "Affinity_wt (M)")):
                if not _valid_affinity(text):
                    rejects.append(reject("adapt", "no_observation", SRC,
                                          base,
                                          {"value": text, "col": col,
                                           "branch": branch}))
                    continue
                obs = {"label": text.strip(), "assay": method,
                       "condition": row["Protein 2"] or None, "replicate": None,
                       "lineage": [join(loc, kv("col", col), kv("branch", branch))]}
                records.append(Record(
                    key=base + ":" + branch,
                    h_raw=parents[h_chain]["seq"],
                    l_raw=parents[l_chain]["seq"] if l_chain else None,
                    ag_raw=tuple(parents[c]["seq"] for c in ag_chains),
                    obs=(obs,), branch=branch, row_key=base,
                    ab_evidence={
                        "seqs": {"h": parents[h_chain]["seq"],
                                 "l": parents[l_chain]["seq"] if l_chain else None},
                        "placeholders": list(PLACEHOLDERS),
                        "edits": ab_edits if branch == "mut" else [],
                        "entity": "ab",
                        "structure": {"structure_id": pdb, "file_ref": str(ref),
                                      "chain_map": {"H": h_chain,
                                                    "L": l_chain or ""}},
                        "structure_rank": 10},
                    ag_evidence={
                        "chains": [{"key": c, "seq": parents[c]["seq"]}
                                   for c in ag_chains],
                        "placeholders": list(PLACEHOLDERS),
                        "edits": ag_edits if branch == "mut" else [],
                        "entity": "ag",
                        "structure": {"structure_id": pdb, "file_ref": str(ref),
                                      "chain_map": {c: c for c in ag_chains}},
                        "structure_rank": 10},
                    ab_ctx={"ref": str(ref), "chains": ab,
                            "h_chain": h_chain, "l_chain": l_chain or ""},
                    ag_ctx={"ref": str(ref), "chains": ag_chains},
                    ab_notes=(join(kv("protein", row["Protein 1"]),
                                   kv("mutation", row["Mutation(s)_PDB"])),),
                    ag_notes=(join(kv("protein", row["Protein 2"])),)))
    return records, rejects
