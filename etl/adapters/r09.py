"""R09 FLAb：86 张 binding 表、30 个 study，约 463 万行。

列名逐表不同，按语义识别：
- 抗体：`heavy` / `HC` / `Ab_heavy_chain_seq` / `VH`；轻链 `light` / `LC` / ...
  只有单链构建体（scFv 全串、VHH）时只填 H 槽，由 `vdomain` 的 `single_chain` 处理。
- 抗原：`Ag_seq` / `Antigen`（后者多为名字，取序列列优先）。
- 读数列按表的标签列名识别，各成一条 observation；`fitness`、取对数与单位换算列
  不产出（aff 方案第 2 项）。kothiwal 的 SPR KD 与 Cell Display EC50 是两个独立读数。
- 行内没有可解析读数的行进 adapt reject。
"""
from __future__ import annotations

import csv
import io
import zipfile
from pathlib import Path

from etl.b.pipeline import Record, reject
from etl.core.lineage import join, kv, locator

SRC = "SRC_R09"
FLAB = Path("/data_new/ywy/dataset-abag/SRC_R09_FLAB/snapshot-2026-08-17/FLAb/data/binding")
EXTRACTED = Path("/data_new/ywy/etl_out/SRC_R09/data")
SOURCE_ROWS = 4627533
SHARDED = True
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")
EMPTY = ("", "NA", "N/A", "nan", "None", "NULL")

HEAVY_COLS = ("heavy", "hc", "vh", "ab_heavy_chain_seq", "heavy_sequence",
              "heavy chain", "hchain", "vh_sequence")
LIGHT_COLS = ("light", "lc", "vl", "ab_light_chain_seq", "light_sequence",
              "light chain", "lchain", "vl_sequence")
AG_SEQ_COLS = ("ag_seq", "antigen_sequence", "antigen seq", "ag_sequence")
# 读数列：名字里带这些词的列各成一条 observation
LABEL_HINTS = ("kd", "ic50", "ec50", "affinity", "pred_affinity", "mean",
               "neg_log", "label", "fitness")
SKIP_HINTS = ("count", "ngs", "replicate", "round", "edit_distance", "margin")


def _col(header, names):
    lower = {h.lower(): h for h in header if h}
    for name in names:
        if name in lower:
            return lower[name]
    return None


def _label_cols(header):
    """挑出读数列：名字含义像 label、且不是计数/条件类。"""
    out = []
    for h in header:
        if not h:
            continue
        low = h.lower()
        if any(s in low for s in SKIP_HINTS):
            continue
        if any(s in low for s in LABEL_HINTS) and "parsed" not in low:
            out.append(h)
    return out


def _valid(value) -> bool:
    text = "" if value is None else str(value).strip()
    if text in EMPTY:
        return False
    try:
        float(text.lstrip("<>"))
    except ValueError:
        return False
    return True


def _table(name: str):
    """返回 (表名, 文本流)。已解压的优先，否则从 zip 里读，避免解包到根分区。"""
    local = EXTRACTED / name
    if local.exists():
        return local.open(encoding="utf-8", errors="replace")
    zipped = FLAB / (name + ".zip")
    if zipped.exists():
        with zipfile.ZipFile(zipped) as z:
            inner = next(n for n in z.namelist() if n.endswith(".csv")
                         and not n.startswith("__MACOSX"))
            return io.TextIOWrapper(z.open(inner), encoding="utf-8", errors="replace")
    raise FileNotFoundError(name)


def _tables():
    names = sorted(p.name for p in EXTRACTED.glob("*.csv"))
    names += sorted(p.name.removesuffix(".zip") for p in FLAB.glob("*.zip"))
    return names


def adapt():
    return _stream(), adapt.rejects


def _stream():
    for name in _tables():
        try:
            fh = _table(name)
        except (FileNotFoundError, StopIteration, zipfile.BadZipFile):
            adapt.rejects.append(reject("adapt", "missing_file", SRC, name, {}))
            continue
        with fh:
            reader = csv.DictReader(fh)
            header = reader.fieldnames or []
            h_col = _col(header, HEAVY_COLS)
            l_col = _col(header, LIGHT_COLS)
            ag_col = _col(header, AG_SEQ_COLS)
            labels = _label_cols(header)
            if not h_col and not l_col:
                adapt.rejects.append(reject("adapt", "no_sequence", SRC, name,
                                            {"header": header[:10]}))
                continue
            if not labels:
                adapt.rejects.append(reject("adapt", "no_observation", SRC, name,
                                            {"header": header[:10]}))
                continue
            for n, row in enumerate(reader, start=2):
                key = "%s:row=%d" % (name, n)
                h = (row.get(h_col) or "").strip() if h_col else ""
                l = (row.get(l_col) or "").strip() if l_col else ""
                ag = (row.get(ag_col) or "").strip() if ag_col else ""
                if not h and not l:
                    adapt.rejects.append(reject("adapt", "no_sequence", SRC, key,
                                                {"table": name}))
                    continue
                if not ag or not ag.isalpha():
                    adapt.rejects.append(reject("adapt", "no_antigen_sequence",
                                                SRC, key,
                                                {"table": name, "ag": ag[:40]}))
                    continue
                loc = locator(SRC, name, "row=" + str(n))
                obs = []
                for col in labels:
                    value = (row.get(col) or "").strip()
                    if not _valid(value):
                        continue
                    obs.append({"label": value, "assay": None, "condition": name,
                                "replicate": (row.get("Replicate")
                                              or row.get("replicate") or None),
                                "lineage": [join(loc, kv("col", col))]})
                if not obs:
                    adapt.rejects.append(reject("adapt", "no_observation", SRC, key,
                                                {"table": name}))
                    continue
                yield Record(
                    key=key, h_raw=h, l_raw=l, ag_raw=(ag,), obs=tuple(obs),
                    ab_evidence={"seqs": {"h": h, "l": l or None},
                                 "placeholders": list(PLACEHOLDERS),
                                 "hints": {"h": {"single_chain": True}}
                                 if not l else None,
                                 "structure": None, "structure_rank": None},
                    ag_evidence={"chains": [{"key": "A", "seq": ag}],
                                 "placeholders": list(PLACEHOLDERS),
                                 "structure": None, "structure_rank": None})


adapt.rejects = []
