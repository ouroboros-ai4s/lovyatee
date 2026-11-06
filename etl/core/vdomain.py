"""ANARCI(IMGT) 编号 → 可变域区间、残余分类、VH/VL 槽位。"""
import functools
import re
from dataclasses import dataclass
from typing import Mapping, Sequence

from anarci import anarci

from etl.core.lineage import kv, step

LINKERS = ("GGGGSGGGGSGGGGS", "GGGGSGGGGSGGGGSGGGGS")      # 另匹配 (GGGGS)+ 重复
TAGS = {"His6": "HHHHHH", "FLAG": "DYKDDDDK", "HA": "YPYDVPDYA", "Myc": "EQKLISEEDL",
        "V5": "GKPIPNPLLGLDST", "StrepII": "WSHPQFEK", "AviTag": "GLNDIFEAQKIEWHE",
        "TwinStrep": "WSHPQFEKGGGSGGGSGGSAWSHPQFEK"}
_G4S = re.compile("(GGGGS)+")
_SEQ = re.compile("[A-Z]+")
ALLOW = ["H", "K", "L"]     # TCR 链型不在其中，视为无域


@dataclass(frozen=True)
class Hints:
    linker: str | None = None
    spans: tuple[tuple[int, int], ...] | None = None   # 0 起，右开，坐标同输入序列


@dataclass(frozen=True)
class Domain:
    start: int
    end: int                                          # 右开
    chain_type: str                                   # "H" | "K" | "L"
    residue_index: Mapping[tuple[int, str], int]      # IMGT (编号, 插入码) -> 输入序列 0 起下标
    anarci_span: tuple[int, int] | None = None        # 用 hints.spans 且与 ANARCI 边界不同


@dataclass(frozen=True)
class Parse:
    seq: str
    domains: tuple[Domain, ...]                       # 按 start 升序


@dataclass(frozen=True)
class Construct:
    vh: str | None
    vl: str | None
    reason: str | None
    lineage: tuple[str, ...]


def _number(seqs: Sequence[str]) -> list[list[Domain]]:
    """一次 ANARCI 调用，返回每个输入（可能为空列表）的域。"""
    # 非氨基酸字符的输入不送 ANARCI（hmmscan 会直接报错），按无域处理
    good = [(str(i), s) for i, s in enumerate(seqs) if s and _SEQ.fullmatch(s)]
    out: list[list[Domain]] = [[] for _ in seqs]
    if not good:
        return out
    numbered, details, _ = anarci(good, scheme="imgt", allow=ALLOW,
                                  assign_germline=False, ncpu=1)
    for slot, (gid, _seq) in enumerate(good):
        if not numbered[slot]:
            continue
        doms = []
        for k, (numbering, start, _end) in enumerate(numbered[slot]):
            index, pos = {}, start
            for (num, ins), aa in numbering:
                if aa == "-":
                    continue
                index[(num, ins.strip())] = pos
                pos += 1
            if not index:
                continue
            doms.append(Domain(min(index.values()), max(index.values()) + 1,
                               details[slot][k]["chain_type"], index))
        out[int(gid)] = doms
    return out


def _parse_spans(seq: str, spans: Sequence[tuple[int, int]]) -> tuple[Domain, ...]:
    """按来源边界逐段编号；域边界取 span，ANARCI 边界不同则记 anarci_span。"""
    found = _number([seq[s:e] for s, e in spans])
    doms = []
    for offset, (s, e) in enumerate(spans):
        subs = found[offset]
        if not subs:
            continue
        d = subs[0]
        anarci = None if (d.start, d.end) == (0, e - s) else (s + d.start, s + d.end)
        doms.append(Domain(s, e, d.chain_type,
                           {(p, i): s + idx for (p, i), idx in d.residue_index.items()}, anarci))
    return tuple(doms)


@functools.lru_cache(maxsize=100_000)
def _parse_cached(seq: str, spans: tuple[tuple[int, int], ...] | None) -> Parse:
    if spans:
        return Parse(seq, _parse_spans(seq, spans))
    return Parse(seq, tuple(_number([seq])[0]))


def parse(seq: str, hints: Hints | None = None) -> Parse:
    return _parse_cached(seq or "", hints.spans if hints else None)


def parse_batch(seqs: Sequence[str], hints: Sequence[Hints | None] | None = None) -> list[Parse]:
    if hints is not None and any(h and h.spans for h in hints):
        return [parse(s, h) for s, h in zip(seqs, hints)]
    return [Parse(s or "", tuple(doms)) for s, doms in zip(seqs, _number(list(seqs)))]


def _find_linker(residual: str, hint: str | None) -> tuple[int, int, str] | None:
    """两域之间找 linker：优先 hints，其次内置库与 (GGGGS)+。"""
    if hint:
        at = residual.find(hint)
        if at >= 0:
            return at, at + len(hint), hint
    for linker in LINKERS:
        at = residual.find(linker)
        if at >= 0:
            return at, at + len(linker), linker
    m = _G4S.search(residual)
    if m:
        return m.start(), m.end(), m.group()
    return None


def _tags_in(residuals: Sequence[str]) -> tuple[str, ...]:
    """按序列长度降序匹配标签，已被较长标签覆盖的区段不再匹配。"""
    found = []
    for pos, residual in enumerate(residuals):
        taken = [False] * len(residual)
        for name, seq in sorted(TAGS.items(), key=lambda item: -len(item[1])):
            at = residual.find(seq)
            while at >= 0:
                if not any(taken[at:at + len(seq)]):
                    for j in range(at, at + len(seq)):
                        taken[j] = True
                    found.append((pos, at, name))
                at = residual.find(seq, at + 1)
    return tuple(name for _, _, name in sorted(found))


def _boundary(seq: str, d: Domain) -> str | None:
    n_res, c_res = seq[:d.start], seq[d.end:]
    if not (n_res or c_res or d.anarci_span):
        return None
    frags = ["span=%d-%d" % (d.start, d.end), kv("n_len", len(n_res)), kv("c_len", len(c_res))]
    names = _tags_in((n_res, c_res))
    if names:
        frags.append(kv("c_tag", "+".join(names)))
    if d.anarci_span:
        frags += ["conflict=1", kv("anarci_span", "%d-%d" % d.anarci_span)]
    return step("trim", *frags)


def derive(p: Parse, hints: Hints | None = None) -> Construct:
    seq, doms = p.seq, p.domains
    if not doms:
        return Construct(None, None, "no_domain", ())
    trim = tuple(t for t in (_boundary(seq, d) for d in doms) if t)
    types = [d.chain_type for d in doms]
    if len(doms) == 1:
        d = doms[0]
        v = seq[d.start:d.end]
        if d.chain_type == "H":
            return Construct(v, None, None, trim)
        if d.chain_type in ("K", "L"):
            return Construct(None, v, None, trim)
        return Construct(None, None, "unresolved", trim)
    if len(doms) == 2 and types in (["H", "K"], ["H", "L"], ["K", "H"], ["L", "H"]):
        a, b = doms
        split = _find_linker(seq[a.end:b.start], hints.linker if hints else None)
        if split is None:
            return Construct(None, None, "unresolved", trim)
        at, stop, linker = split
        first, second = seq[:a.end + at], seq[a.end + stop:b.end]
        if types[0] == "H":
            vh, vl, orientation = first, second, "VH-VL"
        else:
            vh, vl, orientation = second, first, "VL-VH"
        return Construct(vh, vl, None,
                         trim + (step("split", kv("orientation", orientation), kv("linker", linker)),))
    return Construct(None, None, "unresolved", trim)


def to_fv(seq: str, hints: Hints | None = None) -> Construct:
    return derive(parse(seq, hints), hints)


def _slot(seq: str | None, hints: Hints | None) -> Construct:
    if not seq or not seq.strip():
        return Construct(None, None, None, ())
    return to_fv(seq, hints)


def pair_slots(h: str | None, l: str | None,
               h_hints: Hints | None = None, l_hints: Hints | None = None) -> Construct:
    hs, ls = (h or "").strip().upper(), (l or "").strip().upper()
    if hs and ls and hs == ls:
        c = to_fv(h, h_hints)
        if c.reason is None and c.vh and c.vl:
            return Construct(c.vh, c.vl, None, (step("slot_single"),) + c.lineage)
        return Construct(None, None, "slot_collision", ())
    if hs and ls:
        ch, cl = _slot(h, h_hints), _slot(l, l_hints)
        for c in (ch, cl):
            if c.reason:
                return Construct(None, None, c.reason, ())
        if ch.vh and cl.vl and not ch.vl and not cl.vh:
            return Construct(ch.vh, cl.vl, None, ch.lineage + cl.lineage)
        if ch.vl and cl.vh and not ch.vh and not cl.vl:
            return Construct(cl.vh, ch.vl, None, (step("slot_swap"),) + ch.lineage + cl.lineage)
        return Construct(None, None, "unresolved", ())
    return _slot(h, h_hints) if hs else _slot(l, l_hints)
