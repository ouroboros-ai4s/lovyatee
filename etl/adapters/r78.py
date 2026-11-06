"""R78 MochiBind 采样：7 张 AlphaSeq 采样表，共 33,454 行。

- 抗体：`hc` / `lc`（VHH72 系列无 `lc`）；`mata_sequence` 是 scFv 全序列，不另用。
- 抗原：`antigen` 列逐行给直接序列，4 个活动固定构建体。
- 观察值：`alphaseq_affinity`（实验读出 log10 Kd nM）与 `predicted_affinity`（模型输出）
  各成一条 observation（aff 方案第 4 项）。`parental_*`、`avg_off_target_affinity` 不产出。
"""
from __future__ import annotations

import csv
from pathlib import Path

from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R78"
DATA = Path("/data_new/ywy/dataset-abag/SRC_R78_MOCHIBIND/snapshot-2026-05-19/"
            "ab-binding-eval/data")
SOURCE_ROWS = 33454
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")
EMPTY = ("", "NA", "N/A", "nan", "None", "NULL")


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
    for path in sorted(DATA.glob("*.csv")):
        table = path.name
        activity = table.split("_")[1] if "_" in table else table
        with path.open(encoding="utf-8", newline="") as fh:
            for n, row in enumerate(csv.DictReader(fh), start=2):
                key = "%s:row=%d" % (table, n)
                h = (row.get("hc") or "").strip()
                l = (row.get("lc") or "").strip()
                ag = (row.get("antigen") or "").strip()
                if not h or not ag:
                    rejects.append(reject("adapt", "no_sequence", SRC, key,
                                          {"table": table}))
                    continue
                loc = locator(SRC, table, "row=" + str(n), "activity=" + activity)
                obs = []
                for col in ("alphaseq_affinity", "predicted_affinity"):
                    value = (row.get(col) or "").strip()
                    if not _valid(value):
                        continue
                    obs.append({"label": value,
                                "assay": "NGS_seq" if col == "alphaseq_affinity"
                                         else "computational",
                                "condition": "%s %s" % (activity, table),
                                "replicate": None,
                                "lineage": [join(loc, kv("col", col))]})
                if not obs:
                    rejects.append(reject("adapt", "no_observation", SRC, key,
                                          {"table": table}))
                    continue
                records.append(Record(
                    key=key, h_raw=h, l_raw=l or None, ag_raw=(ag,), obs=tuple(obs),
                    ab_evidence={"seqs": {"h": h, "l": l or None},
                                 "placeholders": list(PLACEHOLDERS),
                                 "structure": None, "structure_rank": None},
                    ag_evidence={"chains": [{"key": "A", "seq": ag}],
                                 "placeholders": list(PLACEHOLDERS),
                                 "structure": None, "structure_rank": None},
                    ag_notes=(join(kv("antigen_activity", activity)),)))
    return records, rejects
