"""R11 AbBiBench：17 张 binding_affinity 表，每张是 `(pdb, antigen_chains)` 体系。

- 抗体：`heavy_chain_seq` / `light_chain_seq`（逐行序列）。
- 抗原：由 `metadata.json` 的 `pdb_path` + `antigen_chains` 从随包 PDB 重建，
  按 `structref` 取 entity 全长；同一体系的多行共享同一个抗原序列。
- observation：`binding_score`（逐文件归一化，无单位无 assay，按 aff 方案第 3 项
  只写 `col=binding_score` 与表名进 condition）。
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R11"
ROOT = Path("/data_new/ywy/dataset-abag/SRC_R11_ABBIBENCH/snapshot-2026-05-02/"
            "Antibody_Binding_Benchmark_Dataset")
META = ROOT / "metadata.json"
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")
SOURCE_ROWS = 215699    # 17 张表合计，已与 inventory 核对


def _antigen(meta: dict, cache: dict) -> tuple[list[str], str | None, str | None]:
    """(链序列, 结构 ID, 文件路径)。同一 pdb_path 只解析一次。"""
    ref = meta["pdb_path"]
    key = (ref, tuple(meta["antigen_chains"]))
    if key in cache:
        return cache[key]
    from etl.core.structref import open_structure
    # metadata 的路径以数据集根为基准（data/complex_structure/...），去掉 data/ 前缀
    rel = ref.split("data/", 1)[-1]
    path = (ROOT / rel).resolve()
    if not path.exists():      # 随包结构文件名大小写与 metadata 不一致（AAYL50_bca.pdb）
        parent, name = path.parent, path.name.lower()
        match = [f for f in parent.iterdir() if f.name.lower() == name]
        path = match[0] if match else path
    st = open_structure(path)
    # 非蛋白链（3gbn 的链 A 是糖/非蛋白实体）没有全长序列，剔除；是否仍有抗原由调用方判断
    chains = [st.chains[c] for c in meta["antigen_chains"] if c in st.chains]
    seqs = [c.full_seq for c in chains if c.is_protein and c.full_seq]
    keys = [c.chain_id for c in chains if c.is_protein and c.full_seq]
    cache[key] = (list(zip(keys, seqs)), st.structure_id, str(path))
    return cache[key]


def adapt() -> tuple[list[Record], list[dict]]:
    global SOURCE_ROWS
    metas = json.loads(META.read_text())
    cache: dict = {}
    records, rejects = [], []
    total = 0
    for dataset, meta in sorted(metas.items()):
        for rel in meta["affinity_data"]:
            # metadata 的路径以数据集根为基准（data/...），实际目录是 binding_affinity/
            raw = Path(rel)
            path = (ROOT / raw).resolve()
            if not path.exists():
                path = (ROOT / "binding_affinity" / raw.name).resolve()
            if not path.exists():
                rejects.append(reject("adapt", "missing_file", SRC,
                                      Path(rel).name, {"file": rel}))
                continue
            table = path.name
            try:
                seqs, structure_id, ref = _antigen(meta, cache)
            except Exception as exc:
                rejects.append(reject("adapt", "unresolved", SRC,
                                      Path(rel).name,
                                      {"file": rel, "error": type(exc).__name__}))
                continue
            if not seqs:
                rejects.append(reject("adapt", "no_antigen_sequence", SRC,
                                      Path(rel).name,
                                      {"file": rel, "antigen_chains": meta["antigen_chains"]}))
                continue
            keys, seqs = [k for k, _ in seqs], [v for _, v in seqs]
            with path.open(encoding="utf-8", newline="") as fh:
                for n, row in enumerate(csv.DictReader(fh), start=2):
                    total += 1
                    key = table + ":row=" + str(n)
                    h, l = row["heavy_chain_seq"], row["light_chain_seq"]
                    score = row.get("binding_score")
                    if not h.strip() or not l.strip():
                        rejects.append(reject("adapt", "no_sequence", SRC, key, {"file": table}))
                        continue
                    if score is None or not str(score).strip():
                        rejects.append(reject("adapt", "no_observation", SRC, key,
                                              {"file": table}))
                        continue
                    loc = locator(SRC, table, "row=" + str(n), "dataset=" + dataset,
                                  "pdb=" + meta["pdb"])
                    obs = {"label": str(score).strip(), "assay": None,
                           "condition": dataset, "replicate": None,
                           "lineage": [join(loc, kv("col", "binding_score"))]}
                    records.append(Record(
                        key=key, h_raw=h, l_raw=l, ag_raw=tuple(seqs), obs=(obs,),
                        ab_evidence={"seqs": {"h": h, "l": l},
                                     "placeholders": list(PLACEHOLDERS),
                                     "structure": None, "structure_rank": None},
                        ag_evidence={"chains": [{"key": k, "seq": v}
                                                for k, v in zip(keys, seqs)],
                                     "placeholders": list(PLACEHOLDERS),
                                     "structure": {"structure_id": structure_id,
                                                   "file_ref": ref,
                                                   "chain_map": {k: k for k in keys}},
                                     "structure_rank": 10,
                                     "notes": ["structure_recover=antigen_from_pdb",
                                               "decision=R11:C1"]}))
    SOURCE_ROWS = total
    return records, rejects
