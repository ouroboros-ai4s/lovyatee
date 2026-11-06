"""原始序列字符串 → 规范序列或 None，附排除标记。不做源特有的清洗。"""
from typing import Collection, NamedTuple

from etl.core.lineage import kv, step

GAP_CHARS = "-.*"
UNKNOWN_RESIDUES = set("XBZJUO")
FLAG_ORDER = ("placeholder", "gap", "unknown_residue", "illegal_char", "multi_record")


class SeqNorm(NamedTuple):
    seq: str | None
    flags: tuple[str, ...]

    @property
    def lineage(self) -> tuple[str, ...]:
        if not self.flags:
            return ()
        ordered = [f for f in FLAG_ORDER if f in self.flags]
        return (step("seqnorm", kv("flags", ",".join(ordered))),)


def normalize(raw: str | None, placeholders: Collection[str] = ()) -> SeqNorm:
    if raw is None:
        return SeqNorm(None, ("placeholder",))
    lines = raw.splitlines()
    headers = sum(1 for line in lines if line.startswith(">"))
    body = "".join(line for line in lines if not line.startswith(">"))
    seq = "".join(body.split()).upper()
    if headers > 1:
        return SeqNorm(None, ("multi_record",))
    if not seq:
        return SeqNorm(None, ("placeholder",))
    if any(seq == p.strip().upper() for p in placeholders):
        return SeqNorm(None, ("placeholder",))
    if any(c in GAP_CHARS for c in seq):
        return SeqNorm(None, ("gap",))
    if not seq.isalpha() or not seq.isascii():
        return SeqNorm(None, ("illegal_char",))
    if any(c in UNKNOWN_RESIDUES for c in seq):
        return SeqNorm(seq, ("unknown_residue",))
    return SeqNorm(seq, ())
