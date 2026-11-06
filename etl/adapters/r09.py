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
SOURCE_ROWS = 4606788     # 实测可解析数据行；inventory 记 4,627,533，差 20,745 是
                          # 其口径含被跳过的表头与 DISCLAIMER 行，非数据丢失
SHARDED = True
PLACEHOLDERS = ("NA", "N/A", "None", "nan", "NULL", "\\", "")
EMPTY = ("", "NA", "N/A", "nan", "None", "NULL")

HEAVY_COLS = ("heavy", "hc", "vh", "ab_heavy_chain_seq", "heavy_sequence",
              "heavy chain", "hchain", "vh_sequence", "vhh_sequence")
LIGHT_COLS = ("light", "lc", "vl", "ab_light_chain_seq", "light_sequence",
              "light chain", "lchain", "vl_sequence")
AG_SEQ_COLS = ("ag_seq", "antigen_seq", "antigen_sequence", "antigen seq",
               "ag_sequence", "target_seq", "target_sequence")
# 读数列：名字里带这些词的列各成一条 observation
LABEL_HINTS = ("kd", "ic50", "ec50", "affinity", "pred_affinity", "mean",
               "neg_log", "label", "fitness", "binding")
SKIP_HINTS = ("count", "ngs", "replicate", "round", "edit_distance", "margin",
              "quality", "pass", "distribution", "material")


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


def _header_line(fh) -> "csv.DictReader":
    """把 fh 定位到表头后返回 DictReader；表头取前 30 行中非空单元格最多者。"""
    start = fh.tell() if fh.seekable() else 0
    rows = []
    for i, cells in enumerate(csv.reader(fh)):
        rows.append(cells)
        if i >= 30:
            break
    best, best_n = 0, -1
    for i, cells in enumerate(rows):
        if any(len(c) > 60 for c in cells):
            continue                       # 一行里出现长句，是说明文字不是表头
        n = sum(1 for c in cells if c and c.strip())
        if n > best_n:
            best, best_n = i, n
    if fh.seekable():
        fh.seek(start)
    for _ in range(best):
        fh.readline()
    return csv.DictReader(fh)


def _table(name: str):
    """返回文本流。顺序：本地解压副本 -> 包内 CSV -> zip 内 CSV。"""
    for cand in (EXTRACTED / name, FLAB / name):
        if cand.exists():
            return cand.open(encoding="utf-8", errors="replace")
    zipped = FLAB / (name + ".zip")
    if zipped.exists():
        with zipfile.ZipFile(zipped) as z:
            inner = next(n for n in z.namelist() if n.endswith(".csv")
                         and not n.startswith("__MACOSX"))
            return io.TextIOWrapper(z.open(inner), encoding="utf-8", errors="replace")
    raise FileNotFoundError(name)


def _tables():
    """解压过的优先，zip 里未解压的补上；同名只留一份，否则每张表被处理两次。"""
    # 80 张已在包内解压为 csv；6 张 zip 我另解到 EXTRACTED，两者都算，同名只留一份
    names = {p.name for p in FLAB.glob("*.csv")}
    names |= {p.name.removesuffix(".zip") for p in FLAB.glob("*.zip")}
    return sorted(names)


def adapt():
    return _stream(), adapt.rejects


# 可核验的固定靶：li2023 与 R23 同批测量（决策文件 R09 C2）
FIXED_ANTIGEN = {
    "li2023machine_scFv-SARS-CoV-2_affinity1.csv": "PDVDLGDISGINAS",
    "li2023machine_scFv-SARS-CoV-2_affinity2.csv": "PDVDLGDISGINAS",
}


def _stream():
    for name in _tables():
        try:
            fh = _table(name)
        except (FileNotFoundError, StopIteration, zipfile.BadZipFile):
            adapt.rejects.append(reject("adapt", "missing_file", SRC, name, {}))
            continue
        with fh:
            # 有些表带 DISCLAIMER 前置行（li2023 affinity2 前 6 行）：
            # 取前 30 行里非空单元格最多的那一行当表头
            header_line = _header_line(fh)
            reader = csv.DictReader(fh)
            header = reader.fieldnames or []
            h_col = _col(header, HEAVY_COLS)
            l_col = _col(header, LIGHT_COLS)
            ag_col = _col(header, AG_SEQ_COLS)
            labels = _label_cols(header)
            # AbRank 的 fitness 是 neg log Kd 的派生副本（aff 方案第 2 项要求不产出）；
            # tsuruta 的 fitness 是该表唯一的 0/1 读数，保留
            if "fitness" in labels and len(labels) > 1:
                labels = [c for c in labels if c.lower() != "fitness"]
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
                if not ag:
                    ag = FIXED_ANTIGEN.get(name, "")
                if not h and not l:
                    adapt.rejects.append(reject("adapt", "no_sequence", SRC, key,
                                                {"table": name}))
                    continue
                if not ag or not ag.isalpha():
                    # 决策文件 R09 C3：无来源序列的固定靶表按 no_antigen_binding 排除
                    adapt.rejects.append(reject("adapt", "no_antigen_binding", SRC, key,
                                                {"table": name, "ag": ag[:40],
                                                 "decision": "R09:C3"}))
                    continue
                loc = locator(SRC, name, "row=" + str(n))
                obs = []
                for col in labels:
                    value = (row.get(col) or "").strip()
                    if not _valid(value):
                        continue
                    # 派生副本：与同表另一标签列取值相同（AbRank 的 fitness 就是 neg log SPR Kd）
                    if any(c != col and (row.get(c) or "").strip() == value
                           for c in labels):
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
