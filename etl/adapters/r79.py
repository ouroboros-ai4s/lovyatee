"""R79 AlphaBind：8 张 AlphaSeq 表，共 209,924 行，4 个抗体活动。

- 抗体：`mata_sequence` 是单链可变序列（scFv 含 linker，VHH 单域），跑 `vdomain`。
- 抗原：表内无序列字段，逐 campaign 从 SRC_R78 的原始文件取（决策文件 R79 C1-C3）。
  trastuzumab 活动的 HER2-OPT 与 R78 的 HER2 片段不是同一构建体，按
  `no_antigen_binding` 排除（C4）。
- 观察值：`alphaseq_affinity`（实验）与 `predicted_affinity`（模型）各成一条
  observation；`parental_*`、`avg_off_target_affinity` 不产出。
"""
from __future__ import annotations

import csv
from pathlib import Path

from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R79"
ROOT = Path("/data_new/ywy/dataset-abag/SRC_R79_ALPHABIND/snapshot-2025-07-24/"
            "alphabind/manuscript/data/alphaseq")
R78 = Path("/data_new/ywy/dataset-abag/SRC_R78_MOCHIBIND/snapshot-2026-05-19/"
           "ab-binding-eval/data")
SOURCE_ROWS = 209924
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")
EMPTY = ("", "NA", "N/A", "nan", "None", "NULL")

# campaign -> R78 原始文件（决策文件 R79 C1-C3）
ANTIGEN_SOURCE = {
    "aab-pp489": "df_pp489_sampled_5k_clean.csv",
    "pembrolizumab-scfv": "df_pem_sampled_5k_clean.csv",
    "vhh72": "df_vhh72_sampled_5k_clean.csv",
}
# trastuzumab 的 HER2-OPT 无对应构建体（决策文件 R79 C4）
EXCLUDED = {"trastuzumab-scfv-cdr", "trastuzumab-scfv-full"}


def _antigen(campaign: str) -> str | None:
    name = ANTIGEN_SOURCE.get(campaign)
    if not name:
        return None
    with (R78 / name).open(encoding="utf-8") as fh:
        return next(csv.DictReader(fh))["antigen"].strip()


def _valid(value) -> bool:
    text = "" if value is None else str(value).strip()
    if text in EMPTY:
        return False
    try:
        float(text)
    except ValueError:
        return False
    return True


def adapt():
    records, rejects = [], []
    cache = {}
    for path in sorted(ROOT.glob("*/*.csv")):
        campaign = path.name.split("_")[0].replace("_alphaseq", "")
        table = path.name
        if campaign in EXCLUDED:
            with path.open(encoding="utf-8") as fh:
                for n, row in enumerate(csv.DictReader(fh), start=2):
                    rejects.append(reject("adapt", "no_antigen_binding", SRC,
                                          "%s:row=%d" % (table, n),
                                          {"campaign": campaign,
                                           "matalpha": row.get("matalpha_description"),
                                           "decision": "R79:C4"}))
            continue
        if campaign not in cache:
            cache[campaign] = _antigen(campaign)
        ag = cache[campaign]
        if not ag:
            with path.open(encoding="utf-8") as fh:
                for n, row in enumerate(csv.DictReader(fh), start=2):
                    rejects.append(reject("adapt", "no_antigen_binding", SRC,
                                          "%s:row=%d" % (table, n),
                                          {"campaign": campaign}))
            continue
        with path.open(encoding="utf-8") as fh:
            for n, row in enumerate(csv.DictReader(fh), start=2):
                key = "%s:row=%d" % (table, n)
                seq = (row.get("mata_sequence") or "").strip()
                if not seq:
                    rejects.append(reject("adapt", "no_sequence", SRC, key,
                                          {"campaign": campaign}))
                    continue
                loc = locator(SRC, table, "row=" + str(n), "campaign=" + campaign)
                obs = []
                for col in ("alphaseq_affinity", "predicted_affinity"):
                    value = (row.get(col) or "").strip()
                    if not _valid(value):
                        continue
                    obs.append({"label": value,
                                "assay": "NGS_seq" if col == "alphaseq_affinity"
                                         else "computational",
                                "condition": "%s (%s)" % (campaign,
                                                          row.get("matalpha_description")),
                                "replicate": None,
                                "lineage": [join(loc, kv("col", col))]})
                if not obs:
                    rejects.append(reject("adapt", "no_observation", SRC, key,
                                          {"campaign": campaign}))
                    continue
                records.append(Record(
                    key=key, h_raw=seq, l_raw=None, ag_raw=(ag,), obs=tuple(obs),
                    ab_evidence={"seqs": {"h": seq, "l": None},
                                 "placeholders": list(PLACEHOLDERS),
                                 "hints": {"h": {"single_chain": True}},
                                 "structure": None, "structure_rank": None},
                    ag_evidence={"chains": [{"key": "A", "seq": ag}],
                                 "placeholders": list(PLACEHOLDERS),
                                 "structure": None, "structure_rank": None,
                                 "notes": ["decision=R79:C1"]},
                    ag_notes=(join(kv("campaign", campaign)),)))
    return records, rejects
