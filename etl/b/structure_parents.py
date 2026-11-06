"""结构型 SRC 的 parent 恢复：`(结构文件, 链)` -> 链记录，只做一次。

R14 / R15 / R50 共享。adapter 给出结构引用与链名；本模块用 `structref` 打开结构，
缓存 `ChainRecord`，并把**作者编号**映射提供成 `mutate.ParentChain` 需要的形状。
每个编辑的编号方案由 adapter 指定（AB-Bind / SKEMPI 用 `pdb_author`）。
"""
from __future__ import annotations

import gzip
from pathlib import Path

_CACHE: dict = {}


def _open(ref: str | Path):
    path = Path(ref)
    if path.suffix == ".gz":            # 随包结构常是 cif.gz
        out = Path("/data_new/ywy/cache/rcsb") / path.name.removesuffix(".gz")
        if not out.exists():
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(gzip.decompress(path.read_bytes()))
        path = out
    from etl.core.structref import open_structure
    return open_structure(path)


def structure(ref: str | Path):
    key = str(ref)
    if key not in _CACHE:
        try:
            _CACHE[key] = _open(ref)
        except Exception as exc:
            _CACHE[key] = exc
    return _CACHE[key]


def chain(ref: str | Path, chain_id: str):
    st = structure(ref)
    if isinstance(st, Exception):
        raise st
    return st.chains[chain_id]


def parent_chain(ref: str | Path, chain_id: str) -> dict:
    """返回 `{"seq": ..., "numberings": {"pdb_author": [[pos, ins, idx], ...]}}`。"""
    rec = chain(ref, chain_id)
    return {"seq": rec.full_seq,
            "numberings": {"pdb_author": [[p, ins, i] for (p, ins), i in rec.index_of.items()]}}


def observed_segments(ref: str | Path, chain_id: str) -> list[str]:
    return list(chain(ref, chain_id).observed_segments())


def is_protein(ref: str | Path, chain_id: str) -> bool:
    return chain(ref, chain_id).is_protein
