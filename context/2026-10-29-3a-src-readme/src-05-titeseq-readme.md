---
- tags:
  - context
---

# SRC_R05_TITESEQ 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
  - [文库和实验主线](#文库和实验主线)
  - [公开产物和记录关系](#公开产物和记录关系)
  - [数值标签和建模边界](#数值标签和建模边界)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [Tite-Seq replicate 表](#tite-seq-replicate-表)
  - [低通量与模拟表](#低通量与模拟表)
  - [FCS、工作簿与上游结构](#fcs工作簿与上游结构)
  - [字段说明](#字段说明)
  - [数据示例](#数据示例)
- [PDB 数据库](#pdb-数据库)
- [采集过程记录](#采集过程记录)
- [参考文献](#参考文献)
- [其他](#其他)
  - [数据范围和限制](#数据范围和限制)
  - [完整性与验收](#完整性与验收)
  - [许可和再分发边界](#许可和再分发边界)
  - [公开范围对照](#公开范围对照)
- [待解决问题与处理进展](#待解决问题与处理进展)

## 数据集身份

- `source_id`：`SRC_R05_TITESEQ`
- `source_version`：`snapshot-2017-09-24`
- 原作者或发布机构：Justin B. Kinney 课题组（Cold Spring Harbor Laboratory）与 Rhys M. Adams、Thierry Mora、Aleksandra M. Walczak 等合作者

### 来源方背景

Justin B. Kinney 于 2010 年进入 [Cold Spring Harbor Laboratory](https://www.cshl.edu/research/faculty-staff/justin-kinney/) 从事定量生物学研究；截至 2026-09-21，该机构列其为教授及 Simons Center for Quantitative Biology 主任。他的团队结合数学理论、机器学习和实验研究序列与生物功能的定量关系。该机构的介绍还指出，他在研究生时期共同发明了大规模平行报告实验（MPRA），这也是其后续高通量测量方法研究的背景。

Tite-Seq 是 Kinney 与法国 CNRS/高等师范学院的 Rhys M. Adams、Thierry Mora 和 Aleksandra M. Walczak 等人合作发表的[跨机构研究](https://elifesciences.org/articles/23156)，将高通量测序与抗体亲和力定量测量结合起来。

## 实验设计和数据口径

### 文库和实验主线

研究对象是抗 fluorescein 的 4-4-20 单链抗体可变片段（scFv）。作者以 WT 4-4-20 为背景分别构建两套文库：1H 文库只改变覆盖 CDR1H 的 10 aa 区域，CDR3H 保持 WT；3H 文库只改变覆盖 CDR3H 的 10 aa 区域，CDR1H 保持 WT。论文描述每套文库包含 600 个单密码子变体、1,100 个随机双密码子变体和 150 个随机三密码子变体。**这不是让普通文库成员同时改变 CDR1H 和 CDR3H 的组合设计。** 两套文库分别克隆、在酵母表面展示，实验时等量混合，并加入 WT、超高亲和力 OPT 和带大段缺失的无功能 Δ 对照；这三个对照不是本轮文库设计出的候选。

混合酵母文库分别与 11 个 fluorescein 浓度孵育，包括 `0 M` 和 `10^-9.5` 至 `10^-5` M 的十个非零浓度；每个浓度按抗原结合产生的 PE 荧光分入 4 个 FACS bin。另一路 Sort-Seq 用 c-Myc/BV 荧光把展示量分成 4 个 bin。因此每次实验有 44 个结合分箱和 4 个表达分箱；每个分箱中的细胞重新培养、提取 DNA，对 1H–3H 区域做条形码 PCR 和 paired-end Illumina 测序。作者在三个不同日期独立重复整套实验，并对每个序列、每个 replicate 单独拟合滴定曲线。

主实验和公开产物的关系可概括为：

```text
4-4-20 WT scFv
├── 1H 文库：只改变 CDR1H；CDR3H 保持 WT
└── 3H 文库：只改变 CDR3H；CDR1H 保持 WT
        └── 两套文库等量混合 + WT / OPT / Δ 对照
            ├── 11 个 fluorescein 浓度 × 4 个结合分箱
            └── 1 个独立表达条件 × 4 个表达分箱
                  └── 分箱计数与概率 ── 滴定曲线拟合
                      └── 三张 replicate CSV：每次重复分别给出 KD 和 expression

文库克隆抽样与初步 Tite-Seq 结果 ── 选取克隆做常规流式滴定
                                    └── titration_curves.csv：16 个编号克隆 + 3 个对照

实测参数驱动的算法模拟 ── ideal_*.csv：仅用于验证推断流程
```

### 公开产物和记录关系

`CDR_library_July_5_2013_sequences.txt` 有 3,900 行设计寡核苷酸，其中 1H、3H 各 1,950 行；去除文件内重复后分别有 1,839 和 1,843 个唯一 30 nt 变异片段，合计 3,682 个唯一设计。按论文的构建方式把变异片段与另一段 WT CDR 配对后，与三张 replicate 表的核酸序列对并集比较：结果表保留了其中 3,679 个设计，并另外包含 WT、OPT 和 Δ 三个对照；设计文件中另有 3 个唯一变体没有出现在任何 replicate 表。两边总数都恰好为 3,682，**但不是逐条完全相同的集合**，公开材料也没有说明这 3 个设计缺失的原因。

三张 replicate 表分别有 3,679、3,680 和 3,680 行，合计 11,039 行；这些行是相同序列集合在三次实验中的重复记录，不是 11,039 个独立抗体。核酸序列对跨表并集为 3,682、交集为 3,676；翻译为氨基酸后，因同义变体合并，并集为 2,807、交集为 2,802。replicate CSV 没有单独的 `library` 或 `control` 字段，必须结合 WT 序列和论文给出的对照序列识别记录；尤其 Δ 含大段缺失，表中的两个 30 nt 字段不能解释为其真实、完整 CDR。

`titration_curves.csv` 是独立的低通量 flow-cytometry 验证表，共 73 行、19 个名称，具体为 16 个编号克隆以及 WT（`pJK36`）、OPT、Δ 三个对照。同一名称在不同日期重复测量；16 个编号克隆和 OPT 各 3 行，WT 有 10 行，Δ 有 12 行。因此这 73 行既不是 73 个独立抗体，也不是三张高通量 replicate 表的第四次重复。三个 `ideal_*.csv` 则是不同 sampling rate 下的模拟结果，`true_KD` 是仿真真值，不是实验测量。

### 数值标签和建模边界

Tite-Seq 先根据分箱 read count 和每个 bin 的流式荧光估计各浓度下的平均荧光，再以非协同 Hill 曲线同时推断序列的解离常数 `fit_KD`、饱和幅度和文库占比。`fit_KD` 单位为 M，越小通常表示亲和力越强。论文给出的可靠范围为 `10^-9.5` 至 `10^-5` M；三张表中 7,247 行等于上限 `1e-5`，164 行等于下限 `10^-9.5`，共 7,411 行带有检测边界和删失语义。下限值应读作约 `KD ≤ 10^-9.5 M`，上限值应读作约 `KD ≥ 10^-5 M`，都不是边界处的精确测量。`replicate_2.csv` index 2288 的四个拟合字段为空，raw 层保留这些空值。

**本 source 没有独立的 binder/non-binder 标签。** 高通量表提供的是连续 KD 拟合及其边界值，低通量表中弱结合或无功能对照也可能得到超出主要量程的数值拟合；不能仅凭“字段有数值”认定为 binder，也不能把所有 `fit_KD=1e-5` 直接当作经过独立实验确认的 non-binder。`expression` 是另一条 Sort-Seq 测得的展示量表型，不是结合标签。

用于序列到亲和力的建模时，同一 CDR 序列对的不同 replicate 必须放在同一数据切分侧，并明确是先汇总重复还是显式建模重复。若任务定义为仅从序列预测亲和力，参与生成 `fit_KD` 的分箱计数、概率、拟合参数和同一实验得到的 expression 都不能再作为预测输入，否则会泄漏测量结果。

当前 source 同时保存作者处理后的 KD、expression 和测序计数表，以及 44 个事件级 FCS；原始 sequencing FASTQ 已在 SRA 公开，但本版本未下载。因此当前目录可以复核已取得的处理结果、流式事件和作者分析代码，不能从原始 reads 完整重建测序计数表。

## 论文原文

- 标题：*Measuring the sequence-affinity landscape of antibodies with massively parallel titration curves*
- 作者：Rhys M. Adams, Thierry Mora, Aleksandra M. Walczak, Justin B. Kinney
- 发表来源：eLife 5:e23156
- 归档文本版本：正式发表版，eLife version 3
- 发布日期：2016-12-30
- DOI：`10.7554/eLife.23156`
- PMID / PMCID：`28035901` / `PMC5268739`
- 本地文件：`articles/TiteSeq_2016-12-30_eLife-v3.pdf`
- 文件大小：1.30 MiB（1,364,020 bytes）
- SHA-256：`36399e0a3215f635b711993337e66cda11a88122798833615dd3dc6fbf2c4b05`
- 文本许可：CC BY 4.0
- 补充材料：无独立落盘文件；主 PDF 共 27 页并包含论文的补充说明入口
- 引用数（查询快照）：159（[OpenAlex W2238330501](https://openalex.org/W2238330501)，查询于 2026-09-24）

## 仓库内容

上游仓库 `jbkinney/16_titeseq` 没有 tag 或 release。本 source 固定 commit `54130c8fc6081bbfa8301c41e1afcfa6a5d79590`，author/committer date 均为 2017-09-24，因此命名为 `snapshot-2017-09-24`。交付目录由 `git archive` 生成，不含 `.git` internals，但 114 个文件逐项匹配固定 tree 的 blob identity。

```text
snapshot-2017-09-24/
└── 16_titeseq/
    ├── data/
    │   ├── replicate_1.csv
    │   ├── replicate_2.csv
    │   ├── replicate_3.csv
    │   ├── titration_curves.csv
    │   ├── ideal_*.csv
    │   ├── *.fcs
    │   ├── fcs1/
    │   ├── fcs2/
    │   ├── fcs3/
    │   ├── bar_codes.xlsx
    │   └── sort_counts_*.txt
    ├── structure/
    │   ├── 4-4-20.pdb
    │   ├── figure6.png
    │   └── figure_6.pse
    ├── illustrations/
    ├── pdfs/
    └── *.py
```

固定 tree 共 114 个普通 blob、45.35 MiB（47,548,678 bytes），无 Git LFS 或 submodule。`data/` 有 58 个文件、38.60 MiB（40,475,168 bytes）。仓库根目录与 `data/` 下各有一份逐字节相同的 `CDR13_positions.txt`、`all_aas.txt` 和 `CDR_library_July_5_2013_sequences.txt`；这是上游原始重复布局，raw 层未删除或改名。

## 数据结构

### Tite-Seq replicate 表

`data/replicate_1.csv`、`replicate_2.csv`、`replicate_3.csv` schema 相同，均为 110 列。每行表示一对 CDR1H/CDR3H 核酸文本在一次 replicate 中的测序、表达和滴定拟合结果；普通 1H/3H 设计与 WT、OPT、Δ 对照使用同一 schema，表内没有独立的记录类型字段。首列是上游写出的无列名行 index。

| 文件 | 行数 | 有限 `fit_KD` | 唯一 nucleotide pair | 唯一 amino-acid pair |
| --- | ---: | ---: | ---: | ---: |
| `replicate_1.csv` | 3,679 | 3,679 | 3,679 | 2,805 |
| `replicate_2.csv` | 3,680 | 3,679 | 3,680 | 2,805 |
| `replicate_3.csv` | 3,680 | 3,680 | 3,680 | 2,805 |

### 低通量与模拟表

`data/titration_curves.csv` 有 73 行、22 列，记录 clone 名称、日期、两条 CDR 核酸/氨基酸序列、expression、11 个浓度点的荧光值、`KD` 和曲线参数。同一 clone 可出现多次，是实验重复而非独立序列。

`ideal_0_0.001.csv`、`ideal_0_1.0.csv`、`ideal_0_10000.0.csv` 分别有 3,679、3,679、374 行，是不同 sampling rate 下的模拟拟合结果。模拟表必须与实验 replicate 分开使用。

### FCS、工作簿与上游结构

44 个 FCS 文件均为 FCS3.0、list mode、float data。8 个饱和条件文件有 7 个参数；`fcs1/`、`fcs2/`、`fcs3/` 的 36 个文件有 11 个参数。29 个文件有 10,000 events，13 个有 30,000 events，另有 1,635 和 4,515 events 各一个。

`data/bar_codes.xlsx` 有一个 `Sheet1`，60 行、16 列，记录三次 replicate 和 re-sample barcode。三个 `sort_counts_*.txt` 各 14 行，记录相应日期的 FACS sort counts。

上游 `structure/4-4-20.pdb` 的 HEADER 标识 PDB `1FLR`，含 H、L 和 ligand chain `1`，是 WT 4-4-20 Fab-fluorescein 参考复合物，不是 3,682 个 variant 的逐样本实验结构。它属于上游 payload；从 RCSB 补取的标准文件另在“PDB 数据库”说明。

### 字段说明

三张 replicate CSV 各有 110 列。下表使用明确的取值集合还原批量列名：`{浓度}` 依次取 `0`、`10^-9.5`、`10^-9`、`10^-8.5`、`10^-8`、`10^-7.5`、`10^-7`、`10^-6.5`、`10^-6`、`10^-5.5`、`10^-5`，`{bin}` 取 `0`–`3`。`titration_curves.csv` 除 `name` 外的列名前均有一个 ASCII 空格，下表用 `␠` 表示，以保留原始拼写。

| 文件或表 | 原始字段 | 表示、单位与来源 | 缺失及特殊编码 |
| --- | --- | --- | --- |
| replicate | 空表头列、`CDR1H`、`CDR3H`、`CDR1H_AA`、`CDR3H_AA` | 上游行索引、两段各 30 nt 的核酸序列及各 10 aa 的翻译序列 | 序列字段无空值；空表头为原始索引列 |
| replicate | `basal` | Hill 曲线中的背景荧光 `B`，由零抗原浓度估计；作者拟合输入 | 本文件无空值 |
| replicate | `cmyc0`、`cmyc1`、`cmyc2`、`cmyc3` | c-Myc 表达分箱的测序计数，整数文本；实验测序汇总 | 计数零保留为零，不替换为空值 |
| replicate | `expression`、`prob_cmyc0`、`prob_cmyc1`、`prob_cmyc2`、`prob_cmyc3` | Sort-Seq 表达估计和四个表达分箱概率；由计数估计 | `expression` 与四个概率列分别有 24、25、20 行空值（replicate 1/2/3） |
| replicate | `fit_KD`、`fit_KD_sigma`、`fit_fraction`、`fit_saturation` | Tite-Seq 拟合的 KD（M）、`log(KD)` 不确定度的推断标准差、文库中该序列的估计占比 `P_s` 和饱和荧光幅度 `A_s`；作者计算结果 | replicate 2 各有一行空值；`fit_KD` 的检测边界需按删失值解释 |
| replicate | `fluorescein{浓度}bin{bin}`（44 列） | 11 个浓度 × 4 个 FACS bin 的 read count；实验测序汇总 | 计数零保留为零；列名中的浓度为原始字符串 |
| replicate | `prob_fluorescein{浓度}bin{bin}`（44 列） | 对应 44 个浓度/分箱的概率估计，无单位 | 不同浓度有不同空值数量；不能把空概率填零 |
| replicate | `unsorted`、`unsorted_CDR1H`、`unsorted_CDR3H` | 未分选 library 总计数及按两段 CDR 的计数；实验测序汇总 | 无空值；同一行三项计数不代表三次独立实验 |
| 低通量曲线 | `name`、`␠date`、`␠CDR1H`、`␠CDR3H`、`␠CDR1HAA`、`␠CDR3HAA` | clone ID、日期、核酸及氨基酸序列；实验记录 | 同一 clone 可重复测量，字段名前缀空格需保留 |
| 低通量曲线 | `␠expression`、`␠PE_log10_fluorescein={指数}`（11 列） | expression 与各浓度流式荧光汇总；指数取 `0`、`-9.5`、`-9`、`-8.5`、`-8`、`-7.5`、`-7`、`-6.5`、`-6`、`-5.5`、`-5` | 原表均有数值；各浓度属于同一滴定曲线 |
| 低通量曲线 | `␠mu_0`、`␠KD`、`␠mu_1`、`␠wt_synonymous` | 曲线参数、拟合 KD（M）和 WT 同义标注；作者汇总 | `␠wt_synonymous` 的 73 行均为空；弱结合曲线的数值可超出主要检测范围 |
| 三张模拟表 | 空表头列、`fit_KD`、`fit_KD_std`、`true_KD` | 模拟行索引、拟合 KD、拟合不确定性和仿真真值；与实验标签隔离 | 四列无空值；不能与 replicate 表的 `fit_KD_sigma` 混为同名字段 |

其他直接承载实验或结构数据的文件采用以下结构：

| 文件 | 实际结构与记录口径 | 缺失及特殊编码 |
| --- | --- | --- |
| `CDR_library_July_5_2013_sequences.txt` | 无表头，每行一个带固定侧翼的 DNA oligo；1H 的 1,950 行以 `GTGT` 开头、长度 61 nt，3H 的 1,950 行以 `GTGA` 开头、长度 68 nt。上游代码以字符区间 `[17:47]` 取出中间 30 nt 变异片段 | 3,900 行均只含 `A/C/G/T`；文件内有重复行，去重后为 1,839 个 1H 和 1,843 个 3H 片段；无样本 ID 或表头 |
| `CDR13_positions.txt` | 204 条 PDB fixed-column 记录：179 条 heavy-chain `ATOM` 覆盖 CDR1H 28–37 和 CDR3H 100–109，另有 25 条 fluorescein `HETATM` | 无显式表头；字段位置按 PDB 格式解释 |
| `all_aas.txt` | 3,350 条 PDB fixed-column `ATOM`：heavy chain 1,654 条、light chain 1,696 条，用于结构接触分析 | 不含 fluorescein `HETATM`；无显式表头 |
| `sort_counts_*.txt` | 首行为 replicate 注释，随后字段为 `condition`、`Bin1`–`Bin4`；12 个条件包括 Expression、`0 M` 和十个非零抗原浓度，数值为各分箱细胞数 | 每文件共 14 行，无空值；科学计数法按数值解析 |
| `bar_codes.xlsx:Sheet1` | 四个并排的小表，第二行重复使用 `template`、`forward barcode`、`reverse barcode`，re-sample 区另有 `replicate`；第一行记录三个 replicate 日期和 re-sample 说明 | 60 行、16 列；空白单元格保留，不前向填充 |

44 个 FCS 的事件参数与 `$PAR`、`$TOT`、`$MODE`、`$DATATYPE` 等 FCS 元数据一起保留在二进制文件中；通道名和列顺序按下面的实际 `$PnN` 记录解释。

已逐个读取 44 个 FCS 的 `$PnN`。6 个早期文件依次为 `Time`、`FSC-A`、`SSC-A`、`FITC-A`、`PE-A`、`APC-A`、`Alexa Fluor 405-A`；另 2 个早期文件将 `Time` 放在末列，其余六列顺序不变。`fcs1/`–`fcs3/` 的 36 个文件依次为 `Time`、`FSC-A`、`FSC-H`、`FSC-W`、`SSC-A`、`SSC-H`、`SSC-W`、`FITC-A`、`PE-A`、`APC-A`、`Brilliant Violet 421-A`。这些是仪器事件级荧光/散射通道，原始流式强度无统一物理单位；全部 `$PnS` 标签为空。建模若直接读取 FCS，仍须按文件读取补偿、增益和门控条件，不能按列位置跨 44 个文件合并。

### 数据示例

`replicate_1.csv` index 0 的真实核心字段为：

```text
index=0
CDR1H_AA=TFGDYWMNWV
CDR3H_AA=GSYYGMDYWG
expression=10.3023426065
fit_KD=1.57579602274e-09
```

本表按 replicate 记录，每行对应其中一次测量。

`titration_curves.csv` 中 clone `18` 在 2016-04-18 的真实记录包含：

```text
name=18,date=16.4.18,CDR1HAA=TFSDYSMNWV,CDR3HAA=GSYYGMDYWG,expression=8276.26948,KD=0.00191946
```

同一 clone 还在其他日期重复测量，不能按行当成不同序列。

## PDB 数据库

外部 PDB 锚点为 `1FLR`，由上游 `structure/4-4-20.pdb` 的 HEADER 和论文 WT 4-4-20 Fab–fluorescein 系统共同确认。它提供 WT 4-4-20 的 heavy/light chain 与 fluorescein 复合物，是整份来源共享的参考结构；实验使用的是由相应可变域构成的 yeast-displayed scFv，因此该 PDB 不是完整展示构建体，也不是逐 variant 结构映射。

`1FLR` 的 antibody light chain 是 polymer entity 1、author chain `L`、label asym `A`，heavy chain 是 polymer entity 2、author chain `H`、label asym `B`；RCSB canonical sequence 均为 219 aa。论文和上游结构文件共同把 heavy-chain 28–37、100–109 对应到本研究的 CDR1H、CDR3H 变异区；mmCIF 另保留 fluorescein non-polymer entity 3。2026-09-17 从 [RCSB entry FASTA](https://www.rcsb.org/fasta/entry/1FLR/download) 和 [完整 mmCIF](https://files.rcsb.org/download/1FLR.cif) 获取两层信息。`pdb/sequences/rcsb_pdb_1FLR.fasta` 由项目选取 RCSB canonical H/L 序列并加入角色、author chain 和 label asym header 生成，不是 RCSB 原始 entry FASTA 的逐字节副本；`pdb/structures/1FLR.cif` 原样保存完整 mmCIF。

两文件共 424.51 KiB（434,703 bytes）；FASTA SHA-256 为 `e95fc1c58e33295f0cf9eb4537adb08846233fc03bf8100850237440a7ec067f`，mmCIF SHA-256 为 `3523749d0d6fd1367a96cb878659b00457abc88a7659e00c1ea87f6d6f345157`。按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接后的 inventory SHA-256 为 `5dbb4ed121bca20e09f52ed15c60e84d951ecd1204b00492b5f314a49b95b87d`。

对普通 1H/3H 文库成员，可以把 CSV 中相应的 10 aa 片段放回 WT 可变域来理解突变位置，但公开表没有给出逐条完整 scFv 构建体序列。OPT 还含有 1H/3H 之外的突变，Δ 则有大段缺失，二者尤其不能由两段 CDR 字段加 `1FLR` 唯一重建。RCSB 文件用于统一外部参考布局，不新增任何 variant 结构，也不替代上游 PDB 文件的固定 Git blob identity。

## 采集过程记录

- 2026-09-17 在 ab02 通过 mihomo `127.0.0.1:17890` clone/fetch 上游仓库，固定 commit `54130c8fc6081bbfa8301c41e1afcfa6a5d79590`，再用 `git archive` 生成不含 `.git` 的 worktree。工具和工作数据均位于 `/data/ab02/yangwuyu`，未写入 `/home/yangwuyu`。
- 下载脚本、验证脚本和 README 通过本地二进制 tar 管道经 SSH 同步，本地与远端 SHA-256 逐项一致。
- 独立验收固定 tree 的 114 个文件、CSV schema、FCS header/data offset、XLSX ZIP、上游 1FLR PDB 和论文 PDF。`bar_codes.xlsx` 读取时 openpyxl 提示未知扩展将被忽略，但 ZIP 和工作簿结构可读，raw 文件未改写。
- 通过 ENA inventory 核验 BioProject `PRJNA344711` 的 4 个 run、8 个 paired FASTQ 和官方 MD5；本轮未下载约 99 GiB 的 FASTQ，并明确将状态限定为 public-package onboarding。
- staging 验收后原子发布到正式目录，再次运行完整验证；`.staging/` 清空。API 响应和验证清单保留在工作区或清理，不随 source version 发布。
- 按项目 PDB 硬性要求，从 RCSB 补齐 1FLR 的 canonical FASTA 与完整 mmCIF，并把字节数和哈希写入本 README。
- eLife v3 PDF 从出版方文件名 `elife-23156-v3.pdf` 改为 `TiteSeq_2016-12-30_eLife-v3.pdf`，以来源简称、论文发布日期和版本标识归档；内容按固定 SHA-256 验收。
- 2026-09-22：逐列复核 replicate、低通量、模拟和 44 个 FCS 的原始表头/通道；修正旧字段说明中把 `basal` 误写成计数的问题。`basal` 是零抗原浓度的基线荧光估计，原始文件未修改。同日澄清当前包同时含处理表与事件级 FCS，FASTQ 已公开但未纳入本版本；不再用单一的 `processed-public` 标签概括整个包。
- 2026-09-24：按最新版 source README 规范重新核对论文、作者代码和全部数据格式。修正“同时变异两段 CDR”的歧义，明确 1H/3H 两套单支路文库、三类对照、主实验与低通量/模拟产物的关系；逐条比对设计 oligo 与 replicate 并集，补充 TXT/XLSX/FCS 字段口径、PDB 到 scFv 的映射边界、缺失 FASTQ 的逐文件 ENA inventory，并刷新 OpenAlex 引用快照。重新运行完整验证通过，上游 payload 未改写。
- 2026-10-08：复核正式目录、当前验证脚本、RCSB 选链 FASTA header 和 PDF 下载脚本；补记 PDB FASTA 的项目生成来源、RCSB 获取入口及论文 PDF 原始文件名，未改写上游 payload。

## 参考文献

- 作者仓库：<https://github.com/jbkinney/16_titeseq>
- 固定 commit：<https://github.com/jbkinney/16_titeseq/commit/54130c8fc6081bbfa8301c41e1afcfa6a5d79590>
- eLife 论文：<https://elifesciences.org/articles/23156>
- SRA BioProject：<https://www.ncbi.nlm.nih.gov/bioproject/PRJNA344711>
- ENA BioProject：<https://www.ebi.ac.uk/ena/browser/view/PRJNA344711>
- RCSB 1FLR：<https://www.rcsb.org/structure/1FLR>
- 1FLR 原始结构论文：Whitlow et al., *1.85 Å structure of anti-fluorescein 4-4-20 Fab*，<https://doi.org/10.1093/protein/8.8.749>

## 其他

### 数据范围和限制

ENA inventory 显示 `PRJNA344711` 有 4 个 run、8 个 paired FASTQ，总计 98.96 GiB（106,259,545,868 bytes）：`SRR4340516` 为 29.89 GiB（32,092,799,212 bytes），`SRR4340517` 为 29.22 GiB（31,379,915,729 bytes），`SRR4340518` 为 27.18 GiB（29,181,694,814 bytes），`SRR4340519` 为 12.67 GiB（13,605,136,113 bytes）。2026-09-24 复核到的逐文件 inventory 如下：

| Run | FASTQ | bytes | ENA MD5 |
| --- | --- | ---: | --- |
| `SRR4340516` | `SRR4340516_1.fastq.gz` | 13,075,080,501 | `92c9ff92d84b30a2136e048e42c61e19` |
| `SRR4340516` | `SRR4340516_2.fastq.gz` | 19,017,718,711 | `0452f3ab7ca7ca3ac24651ef4125a55a` |
| `SRR4340517` | `SRR4340517_1.fastq.gz` | 12,785,189,040 | `f8ecf23fe79aeb6bd1b33312bba63b1b` |
| `SRR4340517` | `SRR4340517_2.fastq.gz` | 18,594,726,689 | `f2028e15c5e8fdfecbd36807c5fb2c2d` |
| `SRR4340518` | `SRR4340518_1.fastq.gz` | 11,728,113,223 | `ab0f6612c8b34f4255e9dd024f9e039e` |
| `SRR4340518` | `SRR4340518_2.fastq.gz` | 17,453,581,591 | `07ed5d1d95bf18afec0aa3a68ebbc226` |
| `SRR4340519` | `SRR4340519_1.fastq.gz` | 6,427,978,904 | `182ce1c61ab818b79400ca311b77a7f6` |
| `SRR4340519` | `SRR4340519_2.fastq.gz` | 7,177,157,209 | `15aae298c555c659bc3609e92cfbb813` |

这些 FASTQ 未下载，因此当前目录不能从原始 reads 完整重建 read-count tables；上表只是外部公开文件的可追溯 inventory，不表示文件已经纳入本 source。

### 完整性与验收

- 114 个 repository 文件、45.35 MiB（47,548,678 bytes），全部匹配固定 commit 的 Git blob SHA-1 和 size。
- 7 个 CSV 均可严格解析；三份 replicate 的 schema、序列字符、长度、行数和边界统计通过。
- 44 个 FCS 的版本、metadata 和 data offset 通过；XLSX ZIP 无损坏成员。
- 上游 `4-4-20.pdb` 以 `END` 结束，含 3,665 个 ATOM/HETATM 记录。
- eLife v3 PDF 为 27 页，字节数与 SHA-256 见“论文原文”。
- 当前版本目录共 118 个文件：114 个固定 Git tree 文件、1 个 source README、1 个论文 PDF、1 个 RCSB FASTA 和 1 个 RCSB mmCIF；路径均唯一，未发布旁路验证产物。

### 许可和再分发边界

eLife 论文由 Crossref/eLife 标注 CC BY 4.0。GitHub 仓库没有根 LICENSE，也没有对 `data/`、FCS 或分析脚本的独立许可说明；上游未特别说明覆盖这些对象的许可，使用与再分发范围不明确，论文许可不能自动替代仓库许可。未发现与当前公开包接入明确冲突的条款，此未决项本身不阻塞本项目的接入验收。

当前 source 用于内部研究和可复核保存。接入验收不构成商业使用、衍生物发布或对外再分发授权；上述用途前应联系作者确认各对象的许可，并保留论文、固定 commit、SRA accession 和 PDB 引用。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 三次 Tite-Seq processed result | `replicate_1.csv` 至 `replicate_3.csv` | 已包含 |
| FACS event data | `data/*.fcs`、`data/fcs1/` 至 `fcs3/` | 已包含 |
| library oligo 与 barcode | TXT 和 `bar_codes.xlsx` | 已包含 |
| 低通量 flow titration validation | `data/titration_curves.csv` | 已包含 |
| analysis scripts 和论文图形 | repository worktree | 已包含 |
| WT 4-4-20-fluorescein 参考结构 | 上游 PDB 与 RCSB FASTA/mmCIF | 已包含 |
| raw sequencing reads | SRA `PRJNA344711`，8 个 FASTQ | 未包含 |
| GitHub 数据明确许可 | 仓库无 LICENSE | 未确认 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-08；非阻塞，待权利方说明）：固定 Git 仓库未附根许可证或 `data/`、FCS、分析脚本的独立许可；eLife 论文的 CC BY 4.0 标注只覆盖论文。已核对仓库文件与论文许可，未发现与当前公开包接入明确冲突的条款；许可未说明不阻塞接入，但不授权商业训练、衍生物发布或上游文件再分发。上述用途前向作者确认各对象的授权范围，并保存可核验答复。
- `Q02`（最近更新：2026-09-24；待获取范围决策）：ENA inventory 确认 BioProject `PRJNA344711` 有 8 个公开 paired FASTQ，合计约 98.96 GiB；当前 source 已保存作者处理表与 FCS，未下载这些原始测序文件。逐文件名称、大小和官方 MD5 已记录在“数据范围和限制”，现阶段不能从 reads 完整重建结果表。若项目需要测序级复现，应先确定存储与传输预算，再按 run 下载并逐文件验收 MD5；否则维持当前已取得的公开包范围并保留此缺口。
- `Q03`（最近更新：2026-09-24；待上游说明）：设计 oligo 去重后有 3,682 个唯一变体，其中 3,679 个能在三张 replicate 表的并集中找到；另 3 个设计未出现，而结果表加入了 WT、OPT、Δ 三个对照。公开论文、仓库 README 和代码没有说明这 3 个设计缺失的具体阶段或原因。当前只按实际发布行建模，不补造缺失结果，也不把相同的 3,682 总数解释为逐条完全对应。
