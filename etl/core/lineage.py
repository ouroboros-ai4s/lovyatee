"""lineage 字符串：以 " | " 连接的片段，定位片段在前，其余为 key=value。"""
import re

SEP = " | "
SRC_RE = re.compile("^SRC_R[0-9]+$")
BS = chr(92)   # ponytail: chr(92) 而非 "\\\\"，避免写入路径上的转义层级混乱


def _esc(value: object) -> str:
    s = str(value).replace("\r", " ").replace("\n", " ")
    return s.replace(BS, BS + BS).replace("|", BS + "|")


def _unesc(s: str) -> str:
    return s.replace(BS + "|", "|").replace(BS + BS, BS)


def kv(key: str, value: object) -> str:
    return key + "=" + _esc(value)


def locator(src: str, file: str, *frags: str) -> str:
    if not SRC_RE.match(src):
        raise ValueError("bad src: %r" % (src,))
    return SEP.join((src, _esc(file)) + tuple(_esc(f) for f in frags))


def step(name: str, *frags: str) -> str:
    return SEP.join(("step=" + _esc(name),) + tuple(_esc(f) for f in frags))


def join(*frags: str) -> str:
    return SEP.join(frags)


def split(s: str) -> list[str]:
    out, buf, i = [], [], 0
    while i < len(s):
        if s[i] == BS and i + 1 < len(s):
            buf.append(s[i:i + 2])
            i += 2
            continue
        if s.startswith(SEP, i):
            out.append("".join(buf))
            buf = []
            i += len(SEP)
            continue
        buf.append(s[i])
        i += 1
    out.append("".join(buf))
    return out


def get(s: str, key: str) -> str | None:
    prefix = key + "="
    for frag in split(s):
        if frag.startswith(prefix):
            return _unesc(frag[len(prefix):])
    return None
