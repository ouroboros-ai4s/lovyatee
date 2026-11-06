"""R75 HER2-aff-large / Buzz：CDR-only 亲和力表，含多个研究的子集。

主表与 HER2 外部子集只有 10 aa 的 CDR-H3。抗体侧经 mutate.apply_region
从 1N8Z 重链补全 VH（IMGT 107-116 由本行序列替换）并保留 parent VL；
抗原固定为 HER2（1N8Z entity 3，链 C）。决策文件 etl/decisions/R75.yaml。

观察值：
- her2_aff_large：class 与 label 各成一条 observation
- mason_et_al：只有 label
- shanehsazzadeh_et_al / shanehsazzaddeh_and_her2_aff_large_neg：
  affinity 有值时产出，缺失退回 label
- 流感 CR6261 / CR9114：每个抗原的 *_mean 各成一条 observation，分属不同 pair；
  *_label 不产出（aff 方案第 2 项）

同一 fastq 派生多个 split 目录，0.7_0.15_0.15 三份 split 之和即完整表，只读这一组。
"""
from __future__ import annotations

import csv
from pathlib import Path

from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R75"
DATA = Path("/data_new/ywy/etl_out/SRC_R75/data/data/affinity_data")
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")
SPAN = (107, 116)
SOURCE_ROWS = 759059
REF_STRUCT = "1N8Z"


def _parent_chains():
    from etl.core.structref import open_structure
    st = open_structure(REF_STRUCT)
    return (st.chains["B"].full_seq, st.chains["A"].full_seq,
            st.chains["C"].full_seq, str(st.file))


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as fh:
        yield from csv.DictReader(fh)


def _dir_of(subset: str) -> Path:
    """subset 名到目录：HER2 四个子集在 her2/ 下，其余在顶层。"""
    her2 = {"her2_aff_large", "mason_et_al", "shanehsazzadeh_et_al",
            "shanehsazzaddeh_and_her2_aff_large_neg"}
    return DATA / ("her2" if subset in her2 else "") / subset


def _split_files(subset: str):
    base = _dir_of(subset) / "processed" / "remove_overlap"
    for mode in ("clonotype_split", "random_split"):
        root = base / mode / "0.7_0.15_0.15"
        if root.is_dir():
            return sorted(root.glob("*.csv"))
    return sorted((_dir_of(subset) / "processed").glob("*.csv"))


def _build(subset, path_name, row_n, cdr, ref, vh, vl, her2, obs):
    loc = locator(SRC, "%s/%s" % (subset, path_name), "row=" + str(row_n))
    return Record(
        key="%s/%s:row=%d" % (subset, path_name, row_n),
        h_raw=vh, l_raw=vl, ag_raw=(her2,), obs=tuple(obs),
        ab_evidence={"seqs": {"h": vh, "l": vl},
                     "region": {"span": list(SPAN), "replacement": cdr,
                                "chain": "H", "edit_id": subset},
                     "placeholders": list(PLACEHOLDERS),
                     "structure": {"structure_id": REF_STRUCT, "file_ref": ref,
                                   "chain_map": {"H": "B", "L": "A"}},
                     "structure_rank": 10},
        ag_evidence={"chains": [{"key": "C", "seq": her2, "entity": "3"}],
                     "placeholders": list(PLACEHOLDERS),
                     "structure": {"structure_id": REF_STRUCT, "file_ref": ref,
                                   "chain_map": {"C": "C"}},
                     "structure_rank": 10,
                     "notes": ["decision=R75:C2"]})


def _her2_obs(subset, row, loc):
    obs = []
    if subset == "her2_aff_large":
        cls = (row.get("class") or "").strip()
        label = (row.get("label") or "").strip()
        if cls:
            obs.append({"label": cls, "assay": "yeast_display",
                        "condition": "her2_aff_large (class)", "replicate": None,
                        "lineage": [join(loc, kv("col", "class"))]})
        if label:
            obs.append({"label": label, "assay": "yeast_display",
                        "condition": "her2_aff_large (label)", "replicate": None,
                        "lineage": [join(loc, kv("col", "label"))]})
        return obs
    if subset in ("shanehsazzadeh_et_al", "shanehsazzaddeh_and_her2_aff_large_neg"):
        aff = (row.get("affinity") or "").strip()
        label = (row.get("label") or "").strip()
        if aff:
            obs.append({"label": aff, "assay": None, "condition": subset,
                        "replicate": None,
                        "lineage": [join(loc, kv("col", "affinity"))]})
        elif label:
            obs.append({"label": label, "assay": None, "condition": subset,
                        "replicate": None,
                        "lineage": [join(loc, kv("col", "label"))]})
        return obs
    label = (row.get("label") or "").strip()
    if label:
        obs.append({"label": label, "assay": None, "condition": subset,
                    "replicate": None, "lineage": [join(loc, kv("col", "label"))]})
    return obs


def _influenza(name, path, row, row_n, hseq):
    """流感体系：每个抗原的 *_mean 一条 observation，分属不同 pair（branch 区分）。"""
    loc = locator(SRC, "influenza/%s/%s" % (name, path.name), "row=" + str(row_n))
    out = []
    for col, antigen in (("h1_mean", "h1"), ("h9_mean", "h9"),
                         ("h3_mean", "h3"), ("fluB_mean", "fluB")):
        value = (row.get(col) or "").strip()
        if value:
            out.append((antigen, {"label": value, "assay": None,
                                  "condition": "%s (%s)" % (name, antigen),
                                  "replicate": None,
                                  "lineage": [join(loc, kv("col", col))]}))
    return out


def adapt():
    vh, vl, her2, ref = _parent_chains()
    records, rejects, seen = [], [], set()

    for subset in ("her2_aff_large", "mason_et_al", "shanehsazzadeh_et_al",
                   "shanehsazzaddeh_and_her2_aff_large_neg"):
        for path in _split_files(subset):
            for n, row in enumerate(_rows(path), start=2):
                key = "%s/%s:row=%d" % (subset, path.name, n)
                cdr = (row.get("seq") or "").strip()
                if not cdr:
                    rejects.append(reject("adapt", "missing_sequence", SRC, key,
                                          {"subset": subset}))
                    continue
                # 三个 split 是同一批 CDR 的不同划分，同一 CDR 不会跨 split 出现；
                # 这里只防同一行重复（例如 adapter 被调用两次），不按序列去重
                if (subset, path.name, n) in seen:
                    continue
                seen.add((subset, path.name, n))
                loc = locator(SRC, "%s/%s" % (subset, path.name), "row=" + str(n))
                obs = _her2_obs(subset, row, loc)
                if not obs:
                    rejects.append(reject("adapt", "no_observation", SRC, key,
                                          {"subset": subset}))
                    continue
                records.append(_build(subset, path.name, n, cdr, ref,
                                      vh, vl, her2, obs))

    for name in ("CR6261", "CR9114"):
        root = DATA / "influenza/phillips_et_al/processed" / name / "train500_val151"
        for path in sorted(root.glob("*.csv")):
            for n, row in enumerate(_rows(path), start=2):
                hseq = (row.get("H_seq") or "").strip()
                key = "influenza/%s/%s:row=%d" % (name, path.name, n)
                if not hseq:
                    rejects.append(reject("adapt", "missing_sequence", SRC, key,
                                          {"dataset": name}))
                    continue
                parts = _influenza(name, path, row, n, hseq)
                if not parts:
                    rejects.append(reject("adapt", "no_observation", SRC, key,
                                          {"dataset": name}))
                    continue
                for antigen, obs in parts:
                    tag = "%s_%s" % (name, antigen)
                    records.append(Record(
                        key=key + ":" + antigen, h_raw=hseq, l_raw=None,
                        ag_raw=(tag,), obs=(obs,), branch=antigen,
                        ab_evidence={"seqs": {"h": hseq, "l": None},
                                     "placeholders": list(PLACEHOLDERS),
                                     "structure": None, "structure_rank": None},
                        ag_evidence={"chains": [{"key": tag, "seq": ""}],
                                     "placeholders": list(PLACEHOLDERS),
                                     "structure": None, "structure_rank": None}))
    return records, rejects
