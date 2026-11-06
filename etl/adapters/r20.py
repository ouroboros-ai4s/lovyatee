"""R20 SAbDab / SAbDab2：结构资源适配器，不产出 3A。

`SAbDab2/sabdab_search_structures_*.tar` 里每个 `full_structures/pdb_*.cif.gz` 是一条
抗体结构条目；`sabdab2_summary.csv` 给出 PDB / 链 / 抗原链的索引。本模块只提供
`open(pdb_id)`，把 tar 里的结构解到 `/data_new/ywy/cache/rcsb/` 后交给 `structref`，
其他 SRC 通过 `structure_path(pdb_id)` 或 `open_structure(pdb_id)` 取得结构。
"""
from __future__ import annotations

import csv
import tarfile
from functools import lru_cache
from pathlib import Path

SRC = "SRC_R20"
ROOT = Path("/data_new/ywy/dataset-abag/SRC_R20_SABDAB/snapshot-2026-09-11/SAbDab2")
SUMMARY = ROOT / "sabdab2_summary.csv"
CACHE = Path("/data_new/ywy/cache/rcsb")
STRUCTURES = ROOT / "sabdab_search_structures_20260918T143233.tar"
SOURCE_ROWS = 22264        # sabdab2_summary.csv 数据行；本 SRC 不产出 3A


@lru_cache(maxsize=1)
def index() -> dict[str, dict]:
    """PDB ID -> 该条目的第一条 summary 行（链映射与抗原信息）。"""
    out: dict[str, dict] = {}
    with SUMMARY.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            # PDB 列形如 PDB_000010BT：前缀后是八位编号，后四位是常见的 PDB ID
            pdb = row["PDB"].upper().removeprefix("PDB_")[-4:]
            out.setdefault(pdb, row)
    return out


def structure_path(pdb_id: str) -> Path:
    """把 tar 里的 `<pdb>_sabdab.cif.gz` 解到缓存目录（gzip 展开）并返回路径。

    缓存命中直接返回；未收录的 ID 抛 KeyError，调用方再走 `structref` 的 RCSB 下载。
    """
    pdb = pdb_id.strip().upper()
    target = CACHE / (pdb + ".cif")
    if target.exists():
        return target
    # 成员名是补零到八位的小写 PDB ID，例如 10BT -> pdb_000010bt
    member = "full_structures/pdb_" + pdb.lower().rjust(8, "0") + "_sabdab.cif.gz"
    CACHE.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(".cif.tmp")
    with tarfile.open(STRUCTURES) as tar:
        src = tar.extractfile(member)
        if src is None:
            raise KeyError(pdb)
        tmp.write_bytes(src.read())
    import gzip
    data = gzip.decompress(tmp.read_bytes())
    tmp.write_bytes(data)
    tmp.replace(target)
    return target


def open_structure(pdb_id: str, cache_dir: Path | None = None):
    """优先用本地 tar，未收录时退回 `etl.core.structref.open_structure`（RCSB）。"""
    from etl.core.structref import open_structure as rcsb
    try:
        return rcsb(structure_path(pdb_id), cache_dir=cache_dir)
    except (KeyError, tarfile.TarError, OSError):
        return rcsb(pdb_id, cache_dir=cache_dir)


def adapt() -> tuple[list, list]:
    """资源适配器不产生 pair；返回空表，保留接口一致。"""
    return [], []
