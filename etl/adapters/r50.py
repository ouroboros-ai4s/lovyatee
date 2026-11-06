"""R50 Graphinity：两张计算突变表，共 963,552 行。全部是计算 ddG，非实验。

- Synthetic_FoldX_ddG_942723.csv：942,723 行，1,409 PDB。complex 后缀是
  <原残基><链><位置><新残基>，例如 1adq_DH31A 指链 H 第 31 位 D 变 A。
- Synthetic_FlexddG_ddG_20829.csv：20,829 行，1,246 PDB。complex 写法是
  <pdb>_<抗体链组>_<抗原链组>_<原残基><链><位置><新残基>。
- 两层键：parent 与 vdomain 按 (结构, 链) 只做一次；点突变按作者编号落在 parent 上，
  长度不变，域边界按位置继承（problem_ab 第 9 项）。
- 产出：FoldX 的 foldx_ddg；Flex 的 flexddg_ddg 与 flexddg_ddg-talaris2014 各成一条
  observation（不同打分函数）。flexddg_ddg-talaris2014-gam 与 flexddg_ddg 逐行相等，
  不产出。AB-Bind 645 / SKEMPI 608 两张实验表不产出（原始值由 R14、R15 提供）。
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

from etl.b import structure_parents as sp
from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R50"
ROOT = Path("/data_new/ywy/dataset-abag/SRC_R50_GRAPHINITY/v1/Graphinity")
FOLDX = "Synthetic_FoldX_ddG_942723.csv"
FLEX = "Synthetic_FlexddG_ddG_20829.csv"
SOURCE_ROWS = 942723 + 20829
SHARDED = True      # 94 万行按 10 万一片跑
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")
MUT_TAIL = re.compile(r"([A-Z])([A-Za-z])(\d+)([A-Za-z]?)([A-Z])$")


_REF_CACHE: dict = {}
_PARENT_CACHE: dict = {}


def _ref(pdb: str):
    """每个 PDB 只解析一次结构路径（解 tar + gzip 展开都只做一次）。"""
    if pdb not in _REF_CACHE:
        from etl.adapters import r20
        try:
            _REF_CACHE[pdb] = r20.structure_path(pdb.upper())
        except Exception:
            _REF_CACHE[pdb] = pdb.upper()
    return _REF_CACHE[pdb]


def _parent(ref, chain: str):
    """按 (结构引用, 链) 只恢复一次 parent；这是两层键的第一层。"""
    key = (str(ref), chain)
    if key not in _PARENT_CACHE:
        _PARENT_CACHE[key] = sp.parent_chain(ref, chain)
    return _PARENT_CACHE[key]


def _parse_complex(complex_id: str, pdb: str):
    tail = complex_id[len(pdb):].lstrip("_")
    m = MUT_TAIL.search(tail)
    if not m:
        return None
    orig, chain, pos, ins, new = m.groups()
    prefix = tail[: m.start()].strip("_")
    if prefix:
        parts = prefix.split("_")
        ab_group = parts[0] if parts else ""
        ag_group = parts[1] if len(parts) > 1 else ""
    else:
        ab_group, ag_group = "", ""
    return ab_group, ag_group, orig, chain, int(pos), ins, new


def _is_antibody(ref, chain: str) -> bool:
    from etl.core.vdomain import parse
    try:
        rec = sp.chain(ref, chain)
    except Exception:
        return False
    return rec.is_protein and bool(parse(rec.full_seq).domains)


def _walk(name: str, label_cols):
    """产出 (record, reject)；reject 为 None 时是正常 record。

    生成器而非列表：94 万行若整表驻留，每条都带完整链序列，内存会到 GB 级。
    """
    with (ROOT / name).open(encoding="utf-8", newline="") as fh:
        for n, row in enumerate(csv.DictReader(fh), start=2):
            pdb_raw = row["pdb"].strip()
            pdb = pdb_raw.upper()
            complex_id = row["complex"].strip()
            key = "%s:row=%d" % (name, n)
            parsed = _parse_complex(complex_id, pdb_raw)
            if parsed is None:
                yield None, reject("adapt", "mutation_unassigned", SRC, key,
                                      {"complex": complex_id})
                continue
            ab_group, ag_group, orig, chain, pos, ins, new = parsed
            ab_chains = list(ab_group) if ab_group else list(row["ab_chain"].strip())
            ag_chains = list(ag_group) if ag_group else list(row["ag_chain"].strip())
            if not ab_chains or not ag_chains:
                yield None, reject("adapt", "mutation_unassigned", SRC, key,
                                      {"complex": complex_id,
                                       "ab_chain": row["ab_chain"],
                                       "ag_chain": row["ag_chain"]})
                continue
            ref = _ref(pdb)
            try:
                parents = {c: _parent(ref, c) for c in ab_chains + ag_chains}
            except Exception as exc:
                yield None, reject("adapt", "unresolved", SRC, key,
                                      {"pdb": pdb, "error": type(exc).__name__})
                continue
            # 计算 ddG 不依赖突变后序列：突变只进 lineage（A 类处理）。
            # FoldX 的 orig 取自 Graphinity 自己的参考序列，与 PDB entity 残基常不一致，
            # 用 apply_point 重建会被 orig_mismatch 挡掉九成行。
            if chain not in ab_chains and chain not in ag_chains:
                yield None, reject("adapt", "mutation_unassigned", SRC, key,
                                      {"complex": complex_id, "chain": chain})
                continue
            ab_edits, ag_edits = [], []
            h_chain = next((c for c in ab_chains if c.upper() == "H"), ab_chains[0])
            l_chain = next((c for c in ab_chains if c.upper() == "L"), None)
            loc = locator(SRC, name, "row=" + str(n), "complex=" + complex_id)
            obs = []
            for col in label_cols:
                value = (row.get(col) or "").strip()
                if not value:
                    continue
                try:
                    float(value)
                except ValueError:
                    continue
                obs.append({"label": value, "assay": "computational",
                            "condition": complex_id, "replicate": None,
                            "lineage": [join(loc, kv("col", col))]})
            if not obs:
                yield None, reject("adapt", "no_observation", SRC, key,
                                      {"complex": complex_id})
                continue
            yield Record(
                key=key,
                h_raw=parents[h_chain]["seq"],
                l_raw=parents[l_chain]["seq"] if l_chain else None,
                ag_raw=tuple(parents[c]["seq"] for c in ag_chains),
                obs=tuple(obs),
                ab_evidence={"seqs": {"h": parents[h_chain]["seq"],
                                      "l": parents[l_chain]["seq"] if l_chain else None},
                             "placeholders": list(PLACEHOLDERS),
                             "edits": ab_edits, "entity": "ab",
                             "structure": {"structure_id": pdb, "file_ref": str(ref),
                                           "chain_map": {"H": h_chain,
                                                         "L": l_chain or ""}},
                             "structure_rank": 10},
                ag_evidence={"chains": [{"key": c, "seq": parents[c]["seq"]}
                                        for c in ag_chains],
                             "placeholders": list(PLACEHOLDERS),
                             "edits": ag_edits, "entity": "ag",
                             "structure": {"structure_id": pdb, "file_ref": str(ref),
                                           "chain_map": {c: c for c in ag_chains}},
                             "structure_rank": 10},
                ab_ctx={"ref": str(ref), "chains": ab_chains,
                        "h_chain": h_chain, "l_chain": l_chain or ""},
                ag_ctx={"ref": str(ref), "chains": ag_chains},
                ab_notes=(join(kv("complex", complex_id),
                               kv("mutation", "%s%s%s%s" % (orig, chain, pos, new))),)), None


def adapt():
    """返回生成器；run() 分块消费，94 万行不整表驻留。

    `records` 为 Record 迭代器，`reject_rows` 在生成结束时才完整——因此这里把
    reject 收集到闭包列表里，run() 读完 records 后再取 `adapt.rejects`。
    """
    return _stream(), adapt.rejects


def _stream():
    from itertools import chain
    for item in chain(_walk(FOLDX, ("foldx_ddg",)),
                      _walk(FLEX, ("flexddg_ddg", "flexddg_ddg-talaris2014"))):
        rec, rej = item
        if rej is not None:
            adapt.rejects.append(rej)
        else:
            yield rec


adapt.rejects = []
