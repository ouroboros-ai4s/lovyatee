"""抗原链候选 → 有序的裁剪后链列表。不做实验抗原归属判断。"""
from dataclasses import dataclass
from typing import Sequence

from etl.core.lineage import kv, step
from etl.core.resolve import LEVELS, Candidate, resolve


@dataclass(frozen=True)
class SeqCandidate:
    level: str
    seq: str


@dataclass(frozen=True)
class Boundary:
    level: str
    start: int
    end: int
    label: str      # signal_peptide、tag、mature_chain、domain 等


@dataclass(frozen=True)
class Chain:
    key: str
    is_protein: bool = True
    order: int | None = None
    entity: str | None = None
    candidates: tuple[SeqCandidate, ...] = ()
    boundaries: tuple[Boundary, ...] = ()
    observed_segments: tuple[str, ...] | None = None


@dataclass(frozen=True)
class Bound:
    chains: tuple[str, ...] | None
    keys: tuple[str, ...]
    reason: str | None
    lineage: tuple[str, ...]


def _sequence(chain: Chain) -> tuple[str | None, tuple[str, ...], bool]:
    """该链的序列、lineage、是否同级冲突。"""
    cands = tuple(Candidate(c.level, c.seq) for c in chain.candidates if c.seq)
    if not cands:
        return None, (), False
    r = resolve(cands, LEVELS, on_tie="reject")
    if r.selected is None:
        return None, (step("resolve", kv("chain", chain.key), *r.lineage_frags()),), True
    frags = [step("resolve", kv("chain", chain.key), *r.lineage_frags())] if r.conflict else []
    return str(r.selected.value), tuple(frags), False


def _trimmed(chain: Chain, seq: str) -> tuple[str | None, tuple[str, ...]]:
    """按边界裁剪；(None, lineage) 表示该链失败。"""
    if not chain.boundaries:
        return seq, ()
    cands = tuple(Candidate(b.level, (b.start, b.end)) for b in chain.boundaries)
    r = resolve(cands, LEVELS, on_tie="reject")
    if r.selected is None:
        return None, ("boundary_ambiguous",)
    start, end = r.selected.value
    if not (0 <= start < end <= len(seq)):
        return None, ("boundary_out_of_range",)
    label = next(b.label for b in chain.boundaries
                 if b.level == r.selected.source and (b.start, b.end) == (start, end))
    line = step("trim", kv("chain", chain.key), "span=%d-%d" % (start, end),
                kv("label", label), kv("removed_n", start), kv("removed_c", len(seq) - end))
    return seq[start:end], (line,)


def bound(chains: Sequence[Chain]) -> Bound:
    """按 ag 方案第 3、4、6 项：选序列、裁边界、核对结构、定链序。"""
    if not chains:
        return Bound(None, (), "no_sequence", ())
    if any(not c.is_protein for c in chains):
        return Bound(None, (), "non_protein", ())
    sequences, lineage, keys = [], [], []
    for chain in chains:
        seq, frags, tied = _sequence(chain)
        if seq is None:
            return Bound(None, (), "sequence_conflict" if tied else "no_sequence", ())
        seq, trim = _trimmed(chain, seq)
        if seq is None:
            return Bound(None, (), trim[0], ())
        sequences.append(seq)
        keys.append(chain.key)
        lineage.extend(trim)
        lineage.extend(frags)
        if chain.observed_segments is not None:
            ok = all(seg in seq for seg in chain.observed_segments)
            lineage.append(step("structure_check", kv("chain", chain.key),
                                "structure=" + ("consistent" if ok else "mismatch")))
    orders = [c.order for c in chains]
    if any(o is not None for o in orders):
        if any(o is None for o in orders) or len(set(orders)) != len(orders):
            return Bound(None, (), "order_ambiguous", ())
        order = sorted(range(len(chains)), key=lambda i: orders[i])
        sequences = [sequences[i] for i in order]
        keys = [keys[i] for i in order]
    else:
        order = sorted(range(len(chains)), key=lambda i: (chains[i].entity or "", chains[i].key))
        sequences = [sequences[i] for i in order]
        keys = [keys[i] for i in order]
    return Bound(tuple(sequences), tuple(keys), None, tuple(lineage))
