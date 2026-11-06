"""共享 resolver：evidence → ab_entity / ag_entity。供各 adapter 复用，不含 SRC 分支。

evidence 只放影响清洗、且要进缓存键的内容（小字符串）。体积大的 parent 编号表放在
record 的 ctx 里，不进键，只在 resolver 内使用。

ab evidence:
  {"seqs": {"h": raw, "l": raw}, "hints": {"h": {...}, "l": {...}},
   "placeholders": [...], "edits": [...], "parent_ref": "...", "entity": "ab",
   "structure": {...}, "structure_rank": 1, "notes": [...]}
ab ctx: {"parents": {链: {"seq": ..., "numberings": {方案: [[pos, ins, idx], ...]}}}}

ag evidence:
  {"chains": [{"key","seq","is_protein","order","entity","boundaries":[[s,e,label,level]],
               "observed":[...]}], "placeholders": [...], "structure": {...},
   "structure_rank": 1, "notes": [...]}
"""
from __future__ import annotations

import json

from etl.core import ids
from etl.core.antigen_bound import Boundary, Chain, SeqCandidate, bound
from etl.core.mutate import Edit, ParentChain, apply_point
from etl.core.seqnorm import normalize
from etl.core.vdomain import Hints, pair_slots

DEFAULT_PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\")


def clean(raw, placeholders):
    """源字符串 → (seq, lineage_frags, flags)。值为空算 placeholder。"""
    if raw is None or not str(raw).strip():
        return None, (), ("placeholder",)
    norm = normalize(str(raw), placeholders)
    return norm.seq, norm.lineage, norm.flags


def _hints(spec):
    if not spec:
        return None
    spans = spec.get("spans")
    return Hints(linker=spec.get("linker"),
                 spans=tuple(tuple(s) for s in spans) if spans else None)


def _parents(ctx):
    out = {}
    for chain, spec in (ctx.get("parents") or {}).items():
        schemes = {name: {(int(row[0]), str(row[1])): int(row[2]) for row in rows}
                   for name, rows in (spec.get("numberings") or {}).items()}
        out[chain] = ParentChain(spec["seq"], schemes)
    return out


def ab_entity(row: dict) -> dict:
    ev = json.loads(row["evidence"])
    ctx = row.get("_ctx") or {}
    ph = tuple(ev.get("placeholders") or DEFAULT_PLACEHOLDERS)
    seqs = dict(ev.get("seqs") or {})
    lineage = []

    h_seq, h_lin, _ = clean(seqs.get("h"), ph)
    l_seq, l_lin, _ = clean(seqs.get("l"), ph)
    lineage += list(h_lin) + list(l_lin)

    edits_done = []
    if ev.get("edits"):
        edits = [Edit(e["id"], e["chain"], e["orig"], int(e["pos"]), e["new"],
                      e["numbering"], e.get("ins", "")) for e in ev["edits"]]
        res = apply_point(ev.get("entity", "ab"), _parents(ctx), edits)
        lineage += list(res.lineage)
        if res.reason:
            return {"reason_code": res.reason, "lineage": lineage}
        h_seq, h_lin, _ = clean(res.chains.get("H") or res.chains.get("h"), ph)
        l_seq, l_lin, _ = clean(res.chains.get("L") or res.chains.get("l"), ph)
        lineage += list(h_lin) + list(l_lin)
        edits_done = [e["id"] for e in ev["edits"]]

    hints = ev.get("hints") or {}
    c = pair_slots(h_seq, l_seq, _hints(hints.get("h")), _hints(hints.get("l")))
    lineage += list(c.lineage)
    if c.reason:
        return {"reason_code": c.reason, "lineage": lineage}
    return {"AB_ID": ids.ab_id(c.vh, c.vl), "vh": c.vh, "vl": c.vl,
            "structure": ev.get("structure"),
            "structure_rank": ev.get("structure_rank"),
            "lineage": lineage, "applied_edits": edits_done}


def ag_entity(row: dict) -> dict:
    ev = json.loads(row["evidence"])
    ph = tuple(ev.get("placeholders") or DEFAULT_PLACEHOLDERS)
    lineage, chains = [], []
    for spec in ev.get("chains") or []:
        seq, lin, flags = clean(spec.get("seq"), ph)
        lineage += list(lin)
        if seq is None:
            return {"reason_code": flags[0] if flags else "no_sequence", "lineage": lineage}
        chains.append(Chain(
            spec["key"], is_protein=spec.get("is_protein", True),
            order=spec.get("order"), entity=spec.get("entity"),
            candidates=(SeqCandidate("source_native", seq),),
            boundaries=tuple(Boundary(b[3], int(b[0]), int(b[1]), b[2])
                             for b in spec.get("boundaries") or ()),
            observed_segments=tuple(spec["observed"]) if spec.get("observed") else None))
    b = bound(chains)
    lineage += list(b.lineage)
    if b.reason:
        return {"reason_code": b.reason, "lineage": lineage}
    return {"AG_ID": ids.ag_id(list(b.chains)), "sequence": list(b.chains),
            "structure": ev.get("structure"),
            "structure_rank": ev.get("structure_rank"),
            "lineage": lineage, "applied_edits": []}
