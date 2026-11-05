"""AB_ID / AG_ID / 3A_ID。canonical 字符串即传给 H 的完整输入，含版本前缀。"""
import re
from hashlib import sha256
from typing import Iterable, Sequence

ID_VERSION = "v1"
_SEQ = re.compile("^[A-Z]+$")


class IdCollision(Exception):
    """同一 ID 对应不同 canonical 字符串。"""


def H(s: str) -> str:
    return sha256(s.encode("utf-8")).hexdigest()[:32]


def _seq(value: str | None) -> str | None:
    if not value:
        return None
    if not _SEQ.match(value):
        raise ValueError("sequence must match ^[A-Z]+$: %r" % (value,))
    return value


def ab_canonical(vh: str | None, vl: str | None) -> str:
    vh, vl = _seq(vh), _seq(vl)
    if vh is None and vl is None:
        raise ValueError("vh and vl both empty")
    return "ab/%s:%s<SEP>%s" % (ID_VERSION, vh or "<NONE>", vl or "<NONE>")


def ag_canonical(chains: Sequence[str]) -> str:
    seqs = [_seq(c) for c in chains]
    if not seqs or any(s is None for s in seqs):
        raise ValueError("chains must be a non-empty sequence of sequences")
    return "ag/%s:%s" % (ID_VERSION, "<SEP>".join(seqs))


def ab_id(vh: str | None, vl: str | None) -> str:
    return H(ab_canonical(vh, vl))


def ag_id(chains: Sequence[str]) -> str:
    return H(ag_canonical(chains))


def three_a_id(ab: str, ag: str) -> str:
    return H("3a/%s:%s|%s" % (ID_VERSION, ab, ag))


def check_collisions(pairs: Iterable[tuple[str, str]]) -> None:
    seen: dict[str, str] = {}
    for id_, canonical in pairs:
        prev = seen.setdefault(id_, canonical)
        if prev != canonical:
            raise IdCollision("%s: %r != %r" % (id_, prev, canonical))
