"""决策文件自查：`python -m etl.b.verify_decisions [SRC]`。

逐条核对 AI 接缝要求：`file` / `snapshot_file` 存在，`quote` 在其内逐字出现，
`value` 中的序列出现在引用文件或 `structure` 指向的结构 entity 中。任一条不过即非零退出。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DECISIONS = Path("etl/decisions")
DATA = Path("/data_new/ywy/dataset-abag")
SRC_DIR = {
    "SRC_R03": "SRC_R03_ABDESIGN_DB", "SRC_R08": "SRC_R08_AVIDA_HTNFA",
    "SRC_R09": "SRC_R09_FLAB", "SRC_R10": "SRC_R10_ABRANK",
    "SRC_R11": "SRC_R11_ABBIBENCH", "SRC_R12": "SRC_R12_ASD",
    "SRC_R13": "SRC_R13_ANDD", "SRC_R14": "SRC_R14_ABBIND",
    "SRC_R15": "SRC_R15_SKEMPI2", "SRC_R16": "SRC_R16_GUEST",
    "SRC_R20": "SRC_R20_SABDAB", "SRC_R23": "SRC_R23_ALPHASEQ",
    "SRC_R50": "SRC_R50_GRAPHINITY", "SRC_R74": "SRC_R74_ABDESIGN2",
    "SRC_R75": "SRC_R75_ABDESIGN2", "SRC_R78": "SRC_R78_MOCHIBIND",
    "SRC_R79": "SRC_R79_ALPHABIND", "SRC_R80": "SRC_R80_ANTIPASTI",
}
SEQ = re.compile("[ACDEFGHIKLMNPQRSTVWY]{8,}")
_CACHE: dict = {}


def _root(src: str) -> Path:
    d = DATA / SRC_DIR[src]
    snaps = sorted(p for p in d.iterdir() if p.is_dir())
    return snaps[-1] if snaps else d


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _structure_text(spec: dict) -> str:
    """结构 entity 的 full_seq 与 observed_seq 拼起来，供序列逐字核对。"""
    key = (spec["id"].upper(), spec.get("chain"))
    if key not in _CACHE:
        try:
            from etl.core.structref import open_structure
            st = open_structure(key[0])
            recs = [st.chains[key[1]]] if key[1] else list(st.chains.values())
            _CACHE[key] = "\n".join(r.full_seq + "\n" + r.observed_seq
                                    for r in recs if r.is_protein)
        except Exception:                     # 下载/解析失败按证据缺失处理
            _CACHE[key] = ""
    return _CACHE[key]


def verify(path: Path) -> list[str]:
    doc = json.loads(path.read_text())
    root = _root(doc["src"])
    problems = []
    ids = [c.get("id") for c in doc.get("claims") or []]
    if len(ids) != len(set(ids)):
        problems.append("duplicate claim ids")
    for claim in doc.get("claims") or []:
        cid = claim.get("id")
        ev = claim.get("evidence") or {}
        ref = ev.get("snapshot_file") or ev.get("file")
        if not ref:
            problems.append(cid + ": no file or snapshot_file")
            continue
        target = root / ref
        if not target.exists():
            problems.append(cid + ": missing " + ref)
            continue
        text, where = _read(target), ref
        quote = ev.get("quote")
        if quote is not None and quote not in text:
            problems.append(cid + ": quote not verbatim in " + where)
        for seq in _value_seqs(claim):
            if seq in text:
                continue
            spec = claim.get("structure")
            if spec and seq in _structure_text(spec):
                continue
            problems.append(cid + ": value sequence not in " + where)
    return problems


def _value_seqs(claim) -> list[str]:
    value = claim.get("value")
    out = [v for v in ([value] if isinstance(value, str) else []) if len(v) >= 8]
    if isinstance(value, str):
        if len(value) > 200 and SEQ.fullmatch(value):
            pass                                    # 长序列已整体参与核对
    return out


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    files = sorted(DECISIONS.glob("*" + argv[0] + "*.yaml")) if argv else sorted(DECISIONS.glob("*.yaml"))
    bad = 0
    for f in files:
        problems = verify(f)
        print(f.name + ": " + ("ok" if not problems else "FAIL"))
        for p in problems:
            print("  -", p)
        bad += bool(problems)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
