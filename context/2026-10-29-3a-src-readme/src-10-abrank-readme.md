---
- tags:
  - context
---

# SRC_R10_ABRANK 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [主表](#主表)
  - [序列 FASTA](#序列-fasta)
  - [预测结构](#预测结构)
  - [Benchmark split](#benchmark-split)
  - [原始来源材料](#原始来源材料)
  - [预计算图对象](#预计算图对象)
  - [registry 与 splits](#registry-与-splits)
  - [官方实现代码](#官方实现代码)
  - [字段说明](#字段说明)
  - [数据示例](#数据示例)
- [PDB 数据库](#pdb-数据库)
- [使用方式](#使用方式)
- [采集过程记录](#采集过程记录)
- [参考文献](#参考文献)
- [其他](#其他)
  - [数据范围和限制](#数据范围和限制)
  - [完整性与验收](#完整性与验收)
  - [许可和再分发边界](#许可和再分发边界)
  - [公开范围对照](#公开范围对照)
- [待解决问题与处理进展](#待解决问题与处理进展)

## 数据集身份

- `source_id`：`SRC_R10_ABRANK`
- `source_version`：`snapshot-2025-07-08`
- 原作者或发布机构：University College London 与 IBM Research Europe
  合作团队（Chunan Liu、Aurelien Pelissier；PI 为 Andrew C. R. Martin 与
  Maria Rodriguez Martinez）

### 来源方背景

AbRank 由 UCL 结构生物信息团队与 IBM Research Europe 计算团队共同完成。
Andrew C. R. Martin 长期维护抗体序列与结构注释资源
[abYsis](http://www.abysis.org/)，并参与抗体编号与 CDR 定义相关工具建设。
Maria Rodriguez Martinez 在 IBM Research Europe 从事计算系统生物学与机器
学习方法研究。

同一团队此前发布抗原表位预测数据集 AsEP 与图神经网络方法 WALLE
（[arXiv 2407.18184](https://arxiv.org/abs/2407.18184)）。本 source 的官方
实现 `AbRank-WALLE-Affinity` 是同一方法族在亲和力排序任务上的延续，代码与
数据交付沿用同名 `waffle` 包命名空间。

## 实验设计和数据口径

AbRank 不产生新的湿实验测量。它把八个已发表的抗体-抗原结合测量来源重新
汇编成统一的排序标度，并改造为排序（ranking）任务基准。因此理解本数据需要同时
追踪两层派生：上游各来源自身的测量方法，以及 AbRank 在其上做的单位换算、
聚类与 pairwise 构造。

主表 `Source` 字段标出八个上游来源。各来源行数（按既有验收记录）：

| `Source` | 行数 | 上游测量性质 |
| --- | ---: | --- |
| `RBD-escape` | 192,559 | SARS-CoV-2 RBD 深度突变扫描，escape fraction |
| `CATNAP` | 74,540 | HIV 中和抗体数据库，多为中和滴度 |
| `AlphaSeq` | 71,834 | 酵母展示高通量定量结合 |
| `AbCoV` | 1,392 | CoV-AbDab 派生 SARS-CoV-2 抗体汇编 |
| `SKEMPIv2` | 935 | 蛋白-蛋白突变热力学，ΔΔG |
| `AbSci` | 758 | HER2 设计抗体 SPR 测量 |
| `SabDab` | 249 | 结构抗体数据库附带亲和力注记 |
| `OVA-binders` | 89 | 卵清蛋白结合体测量 |

这八类物理量不同质：中和滴度、KD、escape fraction 与 ΔΔG 在量纲和有利方向
上都不一致。AbRank 的公开主表给出派生标度 `log_Aff`，并用 `Aff_op`
标记等式或不等式关系，以承载检测边界造成的删失。当前已核对字段和上游
来源类别，尚未逐来源复现所有原始读出到 `log_Aff` 的转换链；它不能视为统一
物理单位下的实验 KD。

标签口径要点：

1. `log_Aff` 是派生量，不是原始读数。原始 `IC50 [ug/mL]` 与
   `Affinity_Kd [nM]` 两列大量为 `NA`，因为不同来源只报告其中一种或都不报告。
2. `Aff_op` 必须与 `log_Aff` 配对读取。取不等号时该行是检测边界删失，数值
   只是边界而非实测值；把这类行当作精确值使用会引入系统性偏差。
3. 任务设计面向 pairwise ranking，不是绝对值回归。论文核心指标建立在「同一
   抗原下哪个抗体结合更强」这类相对判断上，`log(Kd_ratio)` 与 `escape` 字段
   服务于该构造。
4. 结构字段混合实验结构与预测结构。`AbRank_structures/Ags-Boltz1/` 下的抗原
   结构来自 Boltz-1 预测模型，不是实验测定结构。

split 泄漏是本数据集的核心设计关切。主表为抗体侧与抗原侧分别提供多套层级
聚类标签（`Ab_Lev3_cluster`、`Ab10/25/50_cluster` 及抗原侧对应列），用于按
序列相似度分组而非随机切分。官方 benchmark 因此给出三档难度：`Balanced`
（常规切分）、`Hard_Ab`（抗体侧留出）、`Hard_Ag`（抗原侧留出）。忽略这些
聚类列而做随机切分会因同源抗体跨 train/test 泄漏而显著高估性能。

规模口径差异：论文摘要称汇编超过 380,000 次 binding assays，而 Kaggle v4
主表实际为 342,356 行。两者口径不同，不可互相替换；本 README 一律以实际
文件行数为准。

## 论文原文

- 标题：AbRank: A Benchmark Dataset and Metric-Learning Framework for
  Antibody-Antigen Affinity Ranking
- 作者：Chunan Liu、Aurelien Pelissier、Yanjun Shao、Lilian Denzler、
  Andrew C. R. Martin、Brooks Paige、Maria Rodriguez Martinez
- 发表来源：arXiv 预印本 2506.17857
- 归档文本版本：预印本 v2
- 发布日期：2025-08-13
- DOI：无独立期刊 DOI，以 arXiv ID 2506.17857v2 作为版本锚点
- PMID / PMCID：无
- 本地文件：`articles/AbRank_2025-08-13_arXiv-v2.pdf`
- 文件大小：818.99 KiB（838,643 bytes）
- SHA-256：
  `f6d1dea324639cbdc45b4aeb00444ede8f40af0f57f431949d78b389a2e9f2ee`
- 文本许可：CC BY 4.0
- 补充材料：无独立补充文件；附录随主文 PDF 一并归档

v1 于 2025-06-21 首次提交，本目录归档的是 v2。论文文本版本与数据目录
`source_version` 是两回事：`snapshot-2025-07-08` 取自作者仓库 commit 日期，
与论文 v2 日期无关。

## 仓库内容

复现官方 benchmark 需要四个彼此独立的上游入口，缺一不可：

- 作者仓库：<https://github.com/biochunan/AbRank-WALLE-Affinity>
  - 固定 commit：`216a112d8f93b5011e5c2040dc2c02e95cd43f68`
  - Git tree：`86498573a55172ae0500de533bf9f0b57553b43b`
  - commit 日期：2025-07-08；commit message：`updated google drive ids`
  - 仓库许可：CC BY-NC-SA 4.0
- Kaggle 数据集 `aurlienplissier/abrank` version 4，更新于 2025-05-16
- Google Drive 文件夹 `13BXfJW-hfbqx-wKrvei5sCuvXBV6m0kJ`（预计算图对象）
- 固定 commit 中 dataset class 记录的 6 个 Drive 对象（registry 与 splits）

`source_version` 命名依据是上述固定 commit 的提交日期，不是 Kaggle 版本
日期，也不是下载日期。原始交付是跨来源组合而非单一仓库快照：作者仓库只含
代码，实际数据分散在 Kaggle 与两组 Drive 对象中。

```text
snapshot-2025-07-08/
└── AbRank/
    ├── abrank-kaggle-v4.zip
    ├── AbRank-WALLE-Affinity/
    ├── pairdata/
    │   ├── 00.tar.zst
    │   ├── ... （01 至 08）
    │   └── 09.tar.zst
    └── waffle_api_raw/
        ├── md5sum.txt
        ├── md5sum-regression.txt
        ├── registry.tar.gz
        ├── registry-regression.tar.gz
        ├── splits.tar.gz
        └── splits-regression.tar.gz
```

`abrank-kaggle-v4.zip` 是数据主体，按项目约定保留原始归档不展开，内含主表、
序列 FASTA、预测结构、benchmark split 与原始来源材料。
`AbRank-WALLE-Affinity/` 是官方实现的完整 worktree，70 个文件。
`pairdata/` 是 10 个预计算图对象分卷，合计 136.50 GiB（146,566,584,799 bytes），为四个
交付中体积最大者。`waffle_api_raw/` 是 ranking 与 regression 两条任务线各自
的 registry 与 split 定义，附两份上游 MD5 清单。

## 数据结构

本节描述上游 payload 的 schema。`pdb/` 下由本项目补取的 RCSB 文件不在此节，
见「PDB 数据库」。

### 主表

`AbRank_dataset.csv`，282.51 MiB（296,229,792 bytes），342,356 条记录加表头，28 个字段。

该文件扩展名为 `.csv`，但实际分隔符是 tab 而非逗号。用默认逗号分隔读取会
得到单列结果。这是本 source 最容易踩的坑。

### 序列 FASTA

`Ab_Hseqs.fasta`、`Ab_Lseqs.fasta`、`Ag_seqs.fasta` 三个顶层文件分别保存抗体
重链、轻链与抗原序列，通过 `Ab_name`、`Ag_name` 与主表关联。它们是主表内联
序列列的等价表示，不是额外样本。

### 预测结构

`AbRank_structures/Ags-Boltz1/` 下是抗原的 Boltz-1 预测 PDB 文件。同一 entry
常有成对命名（如 `1yy9.pdb` 与 `1yy9_A.pdb`），分别为全结构与指定链。这些是
预测模型，不是 RCSB 实验结构，也不构成独立测量样本。

### Benchmark split

`Benchmarks/` 下有 10 个 split CSV，以及 `AF3_test_complex_structures/` 与
`Boltz1_test_complex_structures/` 两组预测复合物结构目录。CSV 行数：

| 文件 | 行数 |
| --- | ---: |
| `Benchmarks/Balanced_train.csv` | 168,469 |
| `Benchmarks/Balanced_train_regression.csv` | 61,611 |
| `Benchmarks/Hard_Ab_train.csv` | 130,851 |
| `Benchmarks/Hard_Ab_train_regression.csv` | 42,958 |
| `Benchmarks/Hard_Ag_train.csv` | 12,610 |
| `Benchmarks/Hard_Ag_train_regression.csv` | 1,986 |
| `Benchmarks/test_perturbation.csv` | 706 |
| `Benchmarks/test_regression.csv` | 1,506 |
| `Benchmarks/train_regression.csv` | 304,437 |
| `Benchmarks/test_unrelated.csv` | 1,200 |

带 `_regression` 后缀者属回归任务线，其余属排序任务线。各 train 文件行数之和
远超主表行数，因为 pairwise 构造让同一条测量参与多个对比；这些行不是独立
测量。

### 原始来源材料

`Raw_data_processing/Raw_data_processing/Original_data/` 下按来源分目录保存
汇编前的上游材料，含 `AbCoV/`、`AlphaSeq/`、`CATNAP/`、`HER2_binders/`、
`OVA_binders/`、`RBD_Escape_Bloom/`、`SKEMPIv2/`。其中 `SKEMPIv2/mutant-seqres/`
下是逐突变体 FASTA。这一层用于追溯主表来源，不应与主表合并计数。

该层与本项目其他 source 存在重叠：`HER2_binders/` 对应
`SRC_R02_ABSCI_HER2`，`AlphaSeq/` 对应 `SRC_R23_ALPHASEQ`，`SKEMPIv2/` 对应
`SRC_R15_SKEMPI2`。跨 source 合并训练集时必须去重，否则同批测量会被重复计入。

### 预计算图对象

`pairdata/` 下 10 个 `tar.zst` 分卷，是官方代码由序列与结构预计算得到的
PyTorch Geometric graph pair，不是新测量。

| 文件 | 大小 |
| --- | ---: |
| `00.tar.zst` | 3.72 GiB（3,995,051,761 bytes） |
| `01.tar.zst` | 503.09 MiB（527,526,139 bytes） |
| `02.tar.zst` | 508.58 MiB（533,283,197 bytes） |
| `03.tar.zst` | 474.14 MiB（497,172,387 bytes） |
| `04.tar.zst` | 18.14 GiB（19,479,304,384 bytes） |
| `05.tar.zst` | 24.20 GiB（25,988,402,624 bytes） |
| `06.tar.zst` | 24.86 GiB（26,692,495,178 bytes） |
| `07.tar.zst` | 24.30 GiB（26,095,149,974 bytes） |
| `08.tar.zst` | 23.65 GiB（25,394,080,641 bytes） |
| `09.tar.zst` | 16.17 GiB（17,364,118,514 bytes） |

合计 136.50 GiB（146,566,584,799 bytes），与上游 README 标称 146.57 GB 一致。raw 层保留
原始归档，不展开为 `.pt` 文件。

### registry 与 splits

| 文件 | 大小 | 任务线 |
| --- | ---: | --- |
| `registry.tar.gz` | 6.51 MiB（6,827,922 bytes） | ranking |
| `splits.tar.gz` | 20.78 MiB（21,790,410 bytes） | ranking |
| `md5sum.txt` | 98 bytes | ranking 校验清单 |
| `registry-regression.tar.gz` | 908.66 KiB（930,471 bytes） | regression |
| `splits-regression.tar.gz` | 1.50 MiB（1,572,459 bytes） | regression |
| `md5sum-regression.txt` | 120 bytes | regression 校验清单 |

### 官方实现代码

`AbRank-WALLE-Affinity/` 是固定 commit 的完整 worktree，70 个文件。
`waffle/` 下有 `train-abrank-ranking.py` 与 `train-abrank-regression.py` 两个
训练入口，以及 `config/`、`models/`、`data/`、`utils/`、`scripts/` 子目录。
`conda-env/waffle-gpu.yaml` 是官方环境定义。该 worktree 本身不含实际数据。

### 字段说明

`AbRank_dataset.csv` 的 28 个 tab-separated 字段，按文件中实际顺序。缺失值
统一编码为字面 `NA`。

| # | 字段 | 类型 | 单位与方向 | 含义与来源 |
| ---: | --- | --- | --- | --- |
| 1 | `Ab_name` | str | 无 | 抗体标识，连接键 |
| 2 | `Ag_name` | str | 无 | 抗原标识，连接键 |
| 3 | `Ag_name_details` | str | 无 | 抗原描述文本 |
| 4 | `IC50 [ug/mL]` | float 或 `NA` | µg/mL，越小越强 | 上游原始 IC50，多数行为 `NA` |
| 5 | `Affinity_Kd [nM]` | float 或 `NA` | nM，越小越强 | 上游原始 KD，多数行为 `NA` |
| 6 | `Ag_epitope_restrictions` | str 或 `NA` | 无 | 表位限制注记 |
| 7 | `Ab_heavy_chain_seq` | str | 无 | 抗体重链氨基酸序列 |
| 8 | `Ab_light_chain_seq` | str | 无 | 抗体轻链氨基酸序列 |
| 9 | `Ag_seq` | str | 无 | 抗原氨基酸序列 |
| 10 | `Ab_structure_method` | 枚举 | 无 | 抗体结构来源，如 `Crystalized` |
| 11 | `Ag_structure_method` | 枚举 | 无 | 抗原结构来源，含预测方法 |
| 12 | `bound_AbAg_structure_method` | 枚举 | 无 | 复合物结构来源 |
| 13 | `Ab_PDB_ID` | str 或 `NA` | 无 | 抗体侧 PDB 锚点 |
| 14 | `Ag_PDB_ID` | str 或 `NA` | 无 | 抗原侧 PDB 锚点 |
| 15 | `bound_AbAg_PDB_ID` | str 或 `NA` | 无 | 复合物 PDB 锚点 |
| 16 | `Ab_Lev3_cluster` | int | 无 | 抗体 Levenshtein 层级聚类 ID |
| 17 | `Source` | 枚举 | 无 | 八个上游来源之一 |
| 18 | `escape` | float 或 `NA` | 无量纲 | escape 派生值，仅 DMS 来源有 |
| 19 | `log(Kd_ratio)` | float 或 `NA` | log 比值 | KD 比值对数，pairwise 用 |
| 20 | `Ab10_cluster` | int | 无 | 抗体 10% 相似度聚类 ID |
| 21 | `Ab25_cluster` | int | 无 | 抗体 25% 相似度聚类 ID |
| 22 | `Ab50_cluster` | int | 无 | 抗体 50% 相似度聚类 ID |
| 23 | `Ag_Lev3_cluster` | int | 无 | 抗原 Levenshtein 层级聚类 ID |
| 24 | `Ag10_cluster` | int | 无 | 抗原 10% 相似度聚类 ID |
| 25 | `Ag25_cluster` | int | 无 | 抗原 25% 相似度聚类 ID |
| 26 | `Ag50_cluster` | int | 无 | 抗原 50% 相似度聚类 ID |
| 27 | `log_Aff` | float | 统一 log 标度 | AbRank 折算的统一亲和力标度，派生量 |
| 28 | `Aff_op` | 枚举 | 无 | `log_Aff` 的关系运算符，`=` 或不等号 |

字段来源分层：第 4、5、18、19 列源自上游实验测量或其派生；第 10 至 12 列是
结构来源注记，混合实验与预测；第 16、20 至 26 列是 AbRank 自行计算的聚类
标签；第 27、28 列是 AbRank 的折算结果与删失标记。

`Aff_op` 必须与 `log_Aff` 配对读取。取 `=` 时 `log_Aff` 是点估计；取不等号时
该行为检测边界删失，`log_Aff` 只是边界值，不是实测量。

### 数据示例

主表第一条记录（tab 分隔，此处按字段换行展示）：

```text
Ab_name                     Sab-2ny3_DC
Ag_name                     Ag-2ny3_A
Ag_name_details             envelope glycoprotein gp120
IC50 [ug/mL]                NA
Affinity_Kd [nM]            815.0
Ag_epitope_restrictions     NA
Ab_heavy_chain_seq          EVQLVESGAEVKKPGSSVKVSCKASGDTFIRYSFTWVRQAPGQGLEWMG...
Ab_light_chain_seq          DIVMTQSPATLSVSPGERATLSCRASESVSSDLAWYQQKPGQAPRLLIY...
Ag_seq                      EVVLVNVTENFNMWKNDMVEQMHEDIISLWDQSLKPCVKLTPLCVGAGS...
Ab_structure_method         Crystalized
Ag_structure_method         Crystalized
bound_AbAg_structure_method Crystalized
Ab_PDB_ID                   2ny3
Ag_PDB_ID                   2ny3
bound_AbAg_PDB_ID           2ny3
Ab_Lev3_cluster             13
Source                      SabDab
escape                      NA
log(Kd_ratio)               NA
Ab10_cluster                28
Ab25_cluster                3
Ab50_cluster                1
Ag_Lev3_cluster             29
Ag10_cluster                19
Ag25_cluster                2
Ag50_cluster                1
log_Aff                     2.9112
Aff_op                      =
```

三条序列已截断展示，原文件为完整序列。

该行代表一次配对测量：来自 SAbDab 的 anti-gp120 抗体与 HIV-1 gp120 的结合，
KD 为 815.0 nM，折算 `log_Aff` 为 2.9112，`Aff_op` 为 `=` 故为点估计。三个
PDB 字段同指 `2ny3`，说明抗体、抗原与复合物结构出自同一条目。`escape` 与
`log(Kd_ratio)` 为 `NA`，因为这两列只对特定来源有值。

每行代表一次配对测量，不是一个独立抗体或抗原。同一抗体会在不同抗原下重复
出现，反之亦然。

## PDB 数据库

本节只涵盖从 RCSB 外部补取的结构文件。Kaggle payload 自带的 Boltz-1 与 AF3
预测结构属上游 payload，见「数据结构/预测结构」。

审计范围是主表三个结构锚点字段（`Ab_PDB_ID`、`Ag_PDB_ID`、
`bound_AbAg_PDB_ID`）的全部字面取值。主表有 564 个字面候选，`7N01`
已被 RCSB 撤回。当前目录对其余 563 个 entry 取得双层文件，并从
`SRC_R13_ANDD` 已验收的 RCSB obsolete 原条目补入 `7N01` 完整 mmCIF。
`7N01` 仍是来源记录中的锚点，原生 FASTA 尚不可得。本 source 的其余文件
复用 `SRC_R09_FLAB` 已验证的 RCSB 原始文件，并重新核对覆盖一致性。

覆盖情况：

| 项目 | 数量 | 大小 |
| --- | ---: | ---: |
| `pdb/sequences/` FASTA | 563 | 666.52 KiB（682,513 bytes） |
| `pdb/structures/` mmCIF | 564 | 880.59 MiB（923,369,782 bytes） |

563 个 entry 同时具备 FASTA 与 mmCIF；`7N01` 只有原条目坐标，因此相对主表
564 个字面候选，PDB 子任务仍为 partial。`7N01.cif` 为 2.77 MiB
（2,902,896 bytes），SHA-256 为
`3d2fab695e703f93ce9b978253db9666c20f822149df6fe72c12b52a1f31f5eb`。
全部 1,127 个 PDB 文件共 881.24 MiB（924,052,295 bytes），按
`relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接的 inventory SHA-256 为
`e1fff3ecaa27b812d9f5fcd0a4795e8af3d3cd39c5665eabd9eeae008f625872`。
`7N01` 的原 accession 原生 FASTA 尚未取得，不能以替代条目或坐标推导序列
充当其原始序列。

映射强度与边界：

- 这是 entry 级映射，不是逐行映射。主表多行可共享同一 PDB 锚点。
- `Ab_PDB_ID` 与 `Ag_PDB_ID` 常指向同一复合物条目的不同链。
- FASTA 保留 RCSB 原始 header 与字面完整序列，未做链选择或 header 重写，
  因此一个 entry 的 FASTA 可能包含该条目全部 polymer entity，而非仅抗体或
  抗原链。
- 参考结构不等于数据集样本的实验构建体。主表大量行（尤其 `RBD-escape`、
  `AlphaSeq`、`SKEMPIv2` 突变体）没有自己的晶体结构，其 PDB 字段指向的是
  野生型或参考复合物。把参考结构当作该行变体的实际结构会造成误导。

## 使用方式

读取主表必须显式指定 tab 分隔，并避免把序列或标识符中的字面值误判为缺失：

```python
import pandas as pd

main = pd.read_csv(
    f"{dataset_root}/AbRank/abrank-kaggle-v4.zip",
    compression={"method": "zip", "archive_name": "AbRank_dataset.csv"},
    sep="\t",
    keep_default_na=False,
    na_values=["NA"],
)
```

`pairdata/` 分卷需用 zstd 解码后按 tar 流读取，不要整体展开到磁盘。

## 采集过程记录

2026-09-18：读取项目规范与执行清单，确定来源身份。以作者仓库 commit
`216a112d8f93b5011e5c2040dc2c02e95cd43f68` 与 Git tree
`86498573a55172ae0500de533bf9f0b57553b43b` 固定代码身份，按 commit 日期命名
`snapshot-2025-07-08`。下载统一先落 `.staging/snapshot-2025-07-08.partial`。

2026-09-18：ab02 直连 Kaggle 在 Google Storage TLS 握手处失败。改由本地匿名
下载后以 `scp -O` 中继，远端重新核对字节数与 SHA-256，双端一致。

2026-09-18：ab02 系统 Python 3.6 只能装旧版 `gdown`，而旧版无法解析 Google
当前的下载确认页。将 `gdown` 5.2.0 纯 Python 包与兼容依赖安装到
`/data/ab02/yangwuyu/tools/` 后小型 Drive 对象下载恢复，未写入 `/home`。
6 个 registry/splits 对象完整下载，两份上游 MD5 清单均通过。

2026-09-18：经代理下载大分卷约每路 0.3 MB/s，改为本地匿名链路下载再中继。
`01`、`02`、`03` 三卷完整取得，双端 SHA-256 一致。当日 16:56（Asia/Shanghai）
配额窗口短暂恢复，取得 `00.tar.zst`，双端字节数与 SHA-256 均一致，zstd/tar
流式验收得 6,988 个成员、成员总大小 20.38 GiB（21,879,137,884 bytes）。

2026-09-18：`04` 至 `09` 的全量请求返回 1.96 KiB（2,009 bytes）的「Too many users have
viewed or downloaded this file recently」HTML 页，属上游全局配额阻断，不是
账号登录要求。显式 64 MiB Range 请求曾累计取得 `04` 的 384.00 MiB（402,653,184 bytes）与
`05` 的 192.00 MiB（201,326,592 bytes）后同样被阻断。所有响应在追加前均核对字节数与
`Content-Range`，错误页未写入 `.part`。因 10 卷只完成 4 卷，当时判定为
staging partial 状态，不发布。

2026-09-19 至 2026-09-21：配额窗口陆续恢复，`04` 至 `09` 经本地
`scripts/download_r10_abrank_range.ps1` 按现有 `.part` 长度续传，逐块核对
起止偏移与对象总字节数，并以单实例文件锁防止并发写同一目标。`09.tar.zst`
于 2026-09-21 09:41 落盘，10 卷齐备。

2026-09-22：核查 staging 实际状态，确认 10 卷逐卷字节数与上游声明一致，
合计 136.50 GiB（146,566,584,799 bytes）。清理下载残留：`00`、`01`、`02` 的 `.part` 碎片
与 `04.tar.zst.uploading`（合计约 441 MB），以及 `articles/` 下因 CRLF 命名
污染产生的重复 PDF 副本。顺带删除 `SRC_R13_ANDD` 发布后遗留的空 `.staging`
目录。

2026-09-22：ab02 全部 conda 环境均缺 `zstandard`，而 `--validate-zstd` 依赖
它。经 mihomo 代理向 `pthahnix-base` 安装 `zstandard==0.25.0`。首次全量校验
运行约 22 分钟后在末段断言失败，原因是 validator 要求目录内已存在
`README.md`，而当时 README 尚未写入；字节数、哈希与 zstd 成员校验本身已经
执行完毕。据此调整顺序：先完成 README，再重跑全量校验。

2026-09-22：评估解压可行性。按 `00.tar.zst` 实测压缩比 5.48
（3,995,051,761 → 21,879,137,884），146.6 GB 全量展开约需 806 GB。ab02
`/data` 剩 142 GB，ab03 剩 803 GB，且两节点挂载同一 41.31 TB 文件系统，
换节点不增加可用空间。全量展开会把共享盘填满，故未执行，维持 raw 层保留
原始归档的既定设计。

2026-09-22：补写 staging README 后重跑独立验收。第二次运行完成 10 卷
`pairdata` 的 SHA-256 与 zstd/tar 流式遍历，输出 `status: complete`、
`pairdata_missing: []`、`temporary_residuals: []`；04 至 09 的首次计算哈希
已写入 `validate_r10_abrank.py`，作为后续复核基准。

2026-09-23：使用更新后的哈希基准再次验收 staging，输出仍为
`status: complete`、`pairdata_missing: []`、`temporary_residuals: []`。确认
顶层仅含 `AbRank/`、`articles/`、`pdb/` 和 `README.md` 后，将
`.staging/snapshot-2025-07-08.partial` 原子重命名为正式目录
`snapshot-2025-07-08`；`.staging/` 已清空，资源状态表同步为已发布。

2026-10-09：复核验证器的状态口径。此前记录的 `status: complete` 是旧版
验证器针对公开 payload 的实际输出，未计入撤回条目 `7N01` 的 PDB 缺口。
现将输出拆分为 `public_payload_status: complete` 与 `pdb_status: partial`，
总状态为 `partial`，并明确报告 564 个候选及缺失的 `7N01`。历史验收的
文件身份和哈希结论不变；本次状态修正不代表补得了该条目的原生双层文件。

2026-10-09：从 `SRC_R13_ANDD` 已验收的 RCSB obsolete 原条目复制完整
`7N01.cif`，复制前后字节数和 SHA-256 一致；未采用 replacement `7RW2`
充当原条目。重新逐文件计算 R10 `pdb/` inventory 为 1,127 文件、
924,052,295 bytes、SHA-256
`e1fff3ecaa27b812d9f5fcd0a4795e8af3d3cd39c5665eabd9eeae008f625872`。
原 README 的序列和坐标分层总字节数各多记 20,480 bytes，现按文件重算更正；
旧版总 inventory 断言 921,149,399 bytes 本身正确。

## 参考文献

- AbRank 论文：[arXiv 2506.17857](https://arxiv.org/abs/2506.17857)
- 官方实现固定 commit：
  [biochunan/AbRank-WALLE-Affinity@216a112](https://github.com/biochunan/AbRank-WALLE-Affinity/tree/216a112d8f93b5011e5c2040dc2c02e95cd43f68)
- Kaggle 数据集 version 4：
  <https://www.kaggle.com/datasets/aurlienplissier/abrank>
- 预计算图对象 Drive 文件夹：
  <https://drive.google.com/drive/folders/13BXfJW-hfbqx-wKrvei5sCuvXBV6m0kJ>
- 同团队前作 AsEP 与 WALLE：
  [arXiv 2407.18184](https://arxiv.org/abs/2407.18184)
- 被汇编的上游来源须按各自原始出处引用：CoV-AbDab、CATNAP、AlphaSeq、
  SKEMPI v2、Absci HER2 设计抗体、SAbDab、Bloom 实验室 RBD escape DMS、
  OVA binders。
- RCSB PDB：563 个 entry 的 FASTA 与 mmCIF，另有 `7N01` 原条目 mmCIF；
  使用时须引用各条目原始结构论文。
- 本项目内相关 source：`SRC_R09_FLAB`（PDB 审计来源）、
  `SRC_R02_ABSCI_HER2`、`SRC_R15_SKEMPI2`、`SRC_R23_ALPHASEQ`（原始材料重叠）。

## 其他

### 数据范围和限制

AbRank 是二次汇编，不含新的湿实验测量。跨八个来源的测量在量纲与精度上不
同质，`log_Aff` 只是统一折算的派生标度，不能当作绝对 KD 值跨来源直接比较。

`pairdata/` 内的图对象是由序列与结构预计算得到的派生表示。raw 层保留原始
归档而不展开为 `.pt` 文件：展开后体积约为压缩态的 5.48 倍（约 806 GB），且
不产生新信息。跨 source 构建训练集时必须对重叠的原始材料去重。

### 完整性与验收

已通过独立核验的部分：

- `abrank-kaggle-v4.zip`：523.41 MiB（548,837,142 bytes），SHA-256
  `b481a25ec34ba5a9232df3c68aa14ee96f74da7d7c447805200b9b23f7334789`，
  4,190 个成员，CRC 全量测试通过，展开后总计 3.62 GiB（3,888,282,854 bytes）。
- 论文 PDF：818.99 KiB（838,643 bytes）与固定 SHA-256 一致。
- 6 个 registry/splits 对象：逐项字节数与 SHA-256 通过，两份上游 MD5 清单
  通过。
- `pairdata` 的 10 个分卷：逐卷字节数、SHA-256 与上游声明一致，合计
  136.50 GiB（146,566,584,799 bytes）；10 卷均经 zstd/tar 流式验收并记录成员数与成员总字节数。
- `pdb/`：563 个 entry 的 FASTA 与 mmCIF 全部取得并可解析，`7N01`
  仅有原条目 mmCIF。

上述 PDB 数量只覆盖 564 个字面候选中的 563 个，不能据此声明全部锚点双层完成。

验证产物不随数据发布。正式 source version 只含 `AbRank/`、`articles/`、
`pdb/`、`README.md`。

### 许可和再分发边界

作者仓库与 Kaggle 页面均标示 CC BY-NC-SA 4.0（非商业、相同方式共享）。论文
文本为 CC BY 4.0。两者不同，不可混用。

关键边界：AbRank 的 CC BY-NC-SA 4.0 不能覆盖被它汇编进来的上游来源。
CATNAP、SKEMPI v2、CoV-AbDab、AlphaSeq 等各有独立许可与引用要求，部分比
AbRank 本身更严格。再分发任何子集前须回查该子集的原始许可。

### 公开范围对照

| 目标组成 | 当前证据 | 状态 |
| --- | --- | --- |
| 主表与序列 | Kaggle v4 ZIP，342,356 行、28 字段 | 已取得 |
| benchmark split | 10 个 CSV 加两组预测复合物结构 | 已取得 |
| 原始来源材料 | `Original_data/` 按来源分目录 | 已取得 |
| 官方实现 | 固定 commit worktree，70 文件 | 已取得 |
| 预计算图对象 | 10 卷，136.50 GiB（146,566,584,799 bytes） | 已取得 |
| registry 与 splits | 6 个对象，MD5 通过 | 已取得 |
| 论文 | arXiv v2 PDF | 已取得 |
| PDB 补充 | 564 个字面候选中 563 个双层完整；`7N01` 仅有原条目 mmCIF | partial |
| 上游各来源一手数据 | 仅 AbRank 转存副本 | 未独立取得 |

最后一行是本 source 的主要范围缺口：这里包含的只是 AbRank 自己转存的上游
材料副本，不等于已独立取得 CATNAP、SKEMPI v2 等来源的完整一手数据。需要
那些来源的完整内容时，应按各自独立 source 分别接入。

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-09；影响跨来源标签解释）：主表与论文确认了八个上游来源及统一的 `log_Aff`、`Aff_op` 字段，但尚未逐来源核对原始观察量、删失处理与转换公式的完整生成链。当前按来源分别解释原始端点，只把 `log_Aff` 用作作者提供的派生排序标度；取得可复现代码或逐来源方法并核对样本后关闭。
- `Q02`（最近更新：2026-10-09；PDB 子任务 partial）：主表 564 个字面锚点中的 `7N01` 已被 RCSB 撤回，正式目录有其完整原条目 mmCIF 和其余 563 对 FASTA/mmCIF，仍缺 `7N01` 原生 FASTA。现行 RCSB FASTA/entity API 返回 404，已检查的官方历史快照没有落在该条目 2021-08-04 至 2021-09-01 的 released-to-removed 窗口；当前保留原字段及坐标，不以 `7RW2` 或坐标推导序列替代。取得可核验的原 accession 全链原生 FASTA 并与现存 mmCIF 的 canonical polymer 逐链比对后关闭。该缺口不否定已验收的公开 payload，但不允许声明完整 PDB 覆盖。
