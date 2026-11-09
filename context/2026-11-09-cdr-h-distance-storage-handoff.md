---
tags:
  - context
---

# CDR-H 距离数据存储方案 —— Handoff

## 下一步要做的事

在**不做 pairwise 全量存储**的前提下，设计一个仍能保留足量 CDR-H 编辑距离数据的方案。

约束：`/data_new` 只剩 1.7 T 空余，三个 1,172,563 索引的上三角矩阵共需 2.06 TB。

## 待执行的原始任务

见 [[2026-11-07-ab-ag-sequence-data-analysis-design]]，层 1 与 ETL 输出的对接见 [[2026-11-07-etl-output-handoff]]。

## 已定事项

| 项 | 结论 |
|---|---|
| 抗体对象 | IMGT unique numbering 的 CDR-H1 / H2 / H3；插入位点只留在编号层，不进入序列 |
| 度量 | **按 IMGT 编号对齐的逐位置比较**（非 Levenshtein） |
| 矩阵索引 | 1,172,563 条 unique VH，上三角 |
| 缺失策略 | CDR 缺失处为 null，不参与该对的距离 |

度量选择的实测依据：400 条 H3 上，对齐法与 Levenshtein 完全相等的对占 48%，相关 0.971，平均差 0.83，p95 差 3。

## 已完成

主机 `3x5090`，目录 `/data_new/ywy/analysis/l1/`：

- `vh_distinct.parquet` — 1,172,563 条 unique VH，列 `vh, n_rows, n_ab, ag_ids`
- `cdr_all.parquet`（30 MB）— 单次 ANARCI pass，298 s。列 `vh, n_rows, n_ab, {h1,h2,h3}_{seq,n,key,err}`；`key` 为 IMGT 位置串
- `cdr_all.py`、`cmp_lev_ham.py` — 生成与度量对比脚本

CDR 提取结果：

| CDR | 成功 | distinct | 长度范围 | null |
|---|---|---|---|---|
| H1 | 1,172,414 | 48,474 | 1–19 | 149 |
| H2 | 1,172,513 | 63,233 | 1–22 | 50 |
| H3 | 1,172,031 | 711,337 | 2–63 | 532 |

null 来源：3 条无 ANARCI domain（三个 CDR 全 null）；其余为空 CDR（H1 146、H2 47、H3 529）。

## 未完成

三个矩阵均未生成。仅跑过 400×400 的度量对比，未跑过全量距离计算。

## 阻塞点：磁盘

| 项 | 数值 |
|---|---|
| 上三角对数 | 6.875×10¹¹ |
| 每个值 | 1 字节（最长 CDR 63 aa） |
| 单矩阵 | 687 GB |
| 三个矩阵 | 2.06 TB |
| `/data_new` 空余 | 1.7 T |
| 缺口 | 约 0.36 TB |

`/data_new` 总计 7.3 T，已用 4.3 T，其中 `/data_new/ywy` 仅占 676 G，其余 3.6 T 在其他用户目录下（根目录无读权限）。

## 数据占用

| 类别 | 路径 | 大小 |
|---|---|---|
| 原始数据 | `/data_new/ywy/dataset-abag`（76 个 SRC） | 643 G |
| 处理输出 | `etl_out` | 13 G |
| | `pm_rerun` | 8.2 G |
| | `_tmp_paircalc` | 4.3 G |
| | `abag_final` | 3.3 G |
| | `analysis/l1` | 132 M |
| | `pm_hf` / `protein_mesh_hf` / `tmp` / `_rev_tmp` | 100 M |

## 环境

- 所有工作在主机 `3x5090` 的 `/data_new/ywy` 下进行，经 `ssh 3x5090`
- 长任务用远端 `nohup` + log
- 本地机器无 VPN，不可访问外网
- 宿主访问 HF 需代理 `http://127.0.0.1:17890`，`hf` 在 `/data_new/ywy/envs/etl/bin/hf`，`HF_TOKEN` 由环境变量传入（不落盘）。

## Suggested skills

- `ponytail` — 方案设计阶段保持最小实现
- `superpowers:brainstorming` — 存储替代方案的发散与收敛
