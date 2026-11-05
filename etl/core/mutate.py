"""两种编辑：apply_point（结构型 SRC 的点突变）与 apply_region（指定区间替换）。"""
from dataclasses import dataclass, field
from typing import Literal, Mapping, NamedTuple, Sequence

from etl.core.lineage import kv, step
from etl.core.seqnorm import normalize
from etl.core.vdomain import parse, to_fv

SEQ_NUMBERING = "seq_1based"


class Edit(NamedTuple):
    id: str
    chain: str       # "" 表示未指定
    orig: str
    pos: int
    new: str
    numbering: str
    ins: str = ""


@dataclass(frozen=True)
class ParentChain:
    seq: str
    numberings: Mapping[str, Mapping[tuple[int, str], int]] = field(default_factory=dict)


@dataclass(frozen=True)
class PointResult:
    cls: Literal["B", "C"]
    chains: dict[str, str] | None
    reason: str | None
    lineage: tuple[str, ...]
    sites: tuple[tuple[str, str, int], ...]      # (edit.id, 链, 0 起下标)


@dataclass(frozen=True)
class RegionResult:
    vh: str | None
    vl: str | None
    reason: str | None
    lineage: tuple[str, ...]


def _numbering(pc: ParentChain, name: str) -> Mapping[tuple[int, str], int] | None:
    if name == SEQ_NUMBERING:
        return {(i + 1, ""): i for i in range(len(pc.seq))}
    return pc.numberings.get(name)


def _matches(edit: Edit, pc: ParentChain) -> int | None:
    """该链上 edit 的落点；编号方案缺失、位点不可映射、原残基不符都返回 None。"""
    table = _numbering(pc, edit.numbering)
    if table is None or (edit.pos, edit.ins) not in table:
        return None
    idx = table[(edit.pos, edit.ins)]
    return idx if 0 <= idx < len(pc.seq) and pc.seq[idx] == edit.orig else None


def _reason(edit: Edit, parent: Mapping[str, ParentChain]) -> str:
    """C 类原因：先看编号方案是否存在，再看位点，再看原残基。"""
    for pc in parent.values():
        if _numbering(pc, edit.numbering) is None:
            return "no_numbering"
    for pc in parent.values():
        if (edit.pos, edit.ins) not in _numbering(pc, edit.numbering):
            return "unmapped_position"
    return "orig_mismatch"


def apply_point(entity: Literal["ab", "ag"], parent: Mapping[str, ParentChain],
                edits: Sequence[Edit]) -> PointResult:
    """每个 edit 必须有唯一可映射且原残基一致的链；否则 C 类。长度不变。"""
    if not edits:
        return PointResult("B", {k: v.seq for k, v in parent.items()}, None, (), ())
    chains = {k: v.seq for k, v in parent.items()}
    sites: list[tuple[str, str, int]] = []
    applied: dict[tuple[str, int], str] = {}
    tags = []
    for edit in edits:
        if len(edit.new) != 1 or not ("A" <= edit.new <= "Z"):
            return PointResult("C", None, "unsupported_edit", (), ())
        candidates = [(edit.chain or k, _matches(edit, pc))
                      for k, pc in parent.items() if not edit.chain or k == edit.chain]
        hits = [(chain, idx) for chain, idx in candidates if idx is not None]
        if not hits:
            return PointResult("C", None, "ambiguous_chain" if not edit.chain and len(candidates) > 1
                               else _reason(edit, {k: parent[k] for k, _ in candidates}), (), ())
        if len(hits) > 1:
            return PointResult("C", None, "ambiguous_chain", (), ())
        chain, idx = hits[0]
        if applied.get((chain, idx), edit.new) != edit.new:
            return PointResult("C", None, "conflicting_edits", (), ())
        applied[(chain, idx)] = edit.new
        chains[chain] = chains[chain][:idx] + edit.new + chains[chain][idx + 1:]
        sites.append((edit.id, chain, idx))
        tags.append("%s:%s%s%s>%s" % (chain, edit.orig, edit.pos, edit.ins, edit.new))
    lineage = (step("mutation_rebuild", kv("entity", entity), "class=B",
                    kv("numbering", edits[0].numbering), kv("edits", ",".join(tags))),)
    return PointResult("B", chains, None, lineage, tuple(sites))


def apply_region(parent_h: str, parent_l: str | None, span: tuple[int, int], replacement: str,
                 chain: Literal["H", "L"] = "H") -> RegionResult:
    """把一条链的 IMGT 闭区间换成 replacement；另一条链原样保留，返回 parent 的 VH/VL。"""
    start, end = span
    clean = normalize(replacement)
    if clean.seq is None:
        return RegionResult(None, None, "bad_replacement", ())
    target = parent_h if chain == "H" else (parent_l or "")
    wanted = ("H",) if chain == "H" else ("K", "L")
    p = parse(target)
    doms = [d for d in p.domains if d.chain_type in wanted]
    if len(doms) != 1:
        return RegionResult(None, None, "no_domain", ())
    dom = doms[0]
    a, b = dom.residue_index.get((start, "")), dom.residue_index.get((end, ""))
    if a is None or b is None or b < a:
        return RegionResult(None, None, "region_boundary_missing", ())
    b += 1
    edited = p.seq[:a] + clean.seq + p.seq[b:]
    after = parse(edited)
    bad = (len(after.domains) != len(p.domains)
           or after.domains[0].chain_type != dom.chain_type
           or to_fv(edited).reason is not None)
    if bad:
        return RegionResult(None, None, "region_mismatch", ())
    new_dom = after.domains[0]
    lineage = (step("mutation_rebuild", kv("chain", chain), "class=B",
                    kv("region", "%d-%d" % (start, end)), kv("length", len(clean.seq))),)
    if chain == "H":
        vh = edited[new_dom.start:new_dom.end]
        vl = to_fv(parent_l).vl if parent_l else None
    else:
        vh = to_fv(parent_h).vh if parent_h else None
        vl = edited[new_dom.start:new_dom.end]
    return RegionResult(vh, vl, None, lineage)
