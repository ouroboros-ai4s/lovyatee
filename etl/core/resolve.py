"""候选按优先级择优；同级冲突按 on_tie 处置，冲突本身只记录不丢候选。"""
from dataclasses import dataclass
from typing import Callable, Literal, Sequence

LEVELS = ("source_native", "source_fasta_or_rebuilt", "structure_canonical",
          "structure_observed", "external_accession")


@dataclass(frozen=True)
class Candidate:
    source: str
    value: object


@dataclass(frozen=True)
class Resolved:
    selected: Candidate | None
    candidates: tuple[Candidate, ...]
    conflict: bool

    def lineage_frags(self) -> list[str]:
        frags = ["resolved=" + (self.selected.source if self.selected else "none"),
                 "candidates=" + ";".join("%s:%s" % (c.source, c.value) for c in self.candidates)]
        if self.conflict:
            frags.append("conflict=1")
        return frags


def resolve(candidates: Sequence[Candidate], order: Sequence[str],
            on_tie: Literal["pick_top", "reject"],
            tie_break: Callable[[Sequence[Candidate]], Candidate | None] | None = None) -> Resolved:
    unknown = [c for c in candidates if c.source not in order]
    if unknown:
        raise ValueError("unknown source: %r" % (unknown[0].source,))
    ordered = tuple(sorted(candidates, key=lambda c: order.index(c.source)))
    if not ordered:
        return Resolved(None, (), False)
    top = order.index(ordered[0].source)
    level = tuple(c for c in ordered if order.index(c.source) == top)
    conflict = len({c.value for c in ordered}) > 1
    if len({c.value for c in level}) == 1:
        return Resolved(level[0], ordered, conflict)
    if on_tie == "reject":
        return Resolved(None, ordered, True)
    if on_tie != "pick_top":
        raise ValueError("bad on_tie: %r" % (on_tie,))
    picked = tie_break(level) if tie_break else level[0]
    return Resolved(picked, ordered, True)
