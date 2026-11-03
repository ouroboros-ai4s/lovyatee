---
tags:
  - context
---

# SRC_R68_CH65_COMBLIB 数据说明

- [数据集身份](#数据集身份)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [文件组与记录关系](#文件组与记录关系)
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

- `source_id`：`SRC_R68_CH65_COMBLIB`
- `source_version`：`snapshot-2023-02-01`
- 原作者或发布机构：Angela Phillips 团队；仓库维护者为 amphilli
- 上游固定 commit：`cea336dfd05fa31d675f79038428bf7f0d177e78`

## 实验设计和数据口径

本 source 是 CH65 抗流感抗体的组合突变 Tite-Seq 研究公开交付物。成熟 CH65 相对
UCA 共报告 18 个 mutation，其中 16 个被纳入二元组合库，理论空间为 `2^16 = 65,536`
个 genotype。实验使用 yeast-displayed scFv，分别对 MA90、MA90-G189E 和 SI06 测量
表达及结合。仓库同时保存原始流式事件、样本/replicate metadata、拟合的
`-log10(K_D [M])`、delta-Kd、epistasis 和 pathway inference 产物。

`QCfilt.csv` 是 65,536 个 genotype 的 QC 表；`QCfilt_REPfilt.csv` 是更严格 replicate
过滤后的 65,535 个 genotype。后者三个抗原的 `*_mean` 非缺失数分别为 MA90 65,530、
SI06 64,619、MA90-G189E 63,840。数值越大表示亲和力越强；值 `6.0` 是检测下界钉扎，
不是缺失。空值、`NaN` 和未覆盖的 genotype 必须与检测下界分开处理。

论文主图的 `62,926` 是三抗原联合展示时 poor `K_D` measurements 过滤后的集合，不能
替代每个文件的行数，也不能替代未下载的 ENA reads。仓库的 processed tables、count
table、浏览器资产、图形和 notebooks 是不同表示或派生产物；公开文件没有提供每个
ENA run 到每个 bin 的完整语义连接。

## 论文原文

- 标题：*Hierarchical sequence-affinity landscapes shape the evolution of breadth in an anti-influenza receptor binding site antibody*
- 作者：Angela Phillips 等
- 发表来源：eLife 12:e83628
- 归档文本版本：eLife Version of Record，2023-01-10
- 发布日期：2023-01-10
- DOI：`10.7554/eLife.83628`
- PMID / PMCID：本轮未单独核验
- 本地文件：`articles/CH65-comblib_2023-01-10_eLife-VOR.pdf`
- 文件大小：20.14 MiB（21,121,767 bytes）
- SHA-256：`4d2c2613def0d12b73858e4df2c9223d1c52a6cb02642d28bc1a7b1d3aa388d6`
- 文本许可：论文页面及 Crossref 标记为 CC BY 4.0；不把该许可扩展为 ENA reads 的单独再分发许可
- 补充材料：`articles/` 内保留 eLife API 枚举的 8 个对象：`elife-83628-supp1-v3.zip` 至
  `supp7-v3.zip`，以及 `elife-83628-mdarchecklist1-v3.docx`；这些文件逐项以字节数和 SHA-256 验收

## 仓库内容

固定 commit 的 Git tree 是完整上游快照，共 626 个 blob，保留上游路径和带冒号的文件名。
source version 下的上游 payload 如下；项目生成的 `README.md`、论文附件和 PDB 补充不列入
这棵树。

```text
snapshot-2023-02-01/
└── CH65-comblib/
    ├── CH65_browser/
    ├── Epistasis_Inference/
    ├── Figures/
    ├── Isogenic_Kd/
    ├── Kd_Inference/
    ├── Pathway_Inference/
    ├── LICENSE
    └── README.md
```

`CH65_browser/` 是静态浏览器和四个浏览器数据资产；`Isogenic_Kd/` 保存四个实验条件的
流式导出及 revertant 汇总；`Kd_Inference/` 保存样本 metadata、count、拟合和 QC 结果；
`Epistasis_Inference/`、`Pathway_Inference/` 和 `Figures/` 是分析与图形产物。仓库无
submodule、无 Git LFS pointer；根 `LICENSE` 是 MIT。

## 数据结构

### 文件组与记录关系

固定 tree 中共有 281 个 CSV/TSV 文本文件，实际归为以下文件组。除特别注明外，原始
字段均按文本读取，不在 raw source 中填零、改名或把派生值回写原文件。

| 文件组 | 数量和粒度 | 主要内容与关系 |
| --- | ---: | --- |
| `Isogenic_Kd/` 流式导出 | 197 个 event-level CSV | 每个事件一行，字段为 `FSC-A/H/W`、`SSC-A/H/W`、`FITC-A`、`PE-A`、`Time`；按 replicate、抗原和 plate 文件夹组织 |
| `Isogenic_Kd/` 清单与汇总 | 13 个 CSV | `concentrations-list.csv`、`mut-list.csv`、`run-list.csv` 和 revertant/拟合汇总；连接键是 well、shortname、genotype、antigen、replicate |
| `Kd_Inference/metadata/` | 2 个 TSV | `replicate_info.tsv` 描述 6 个 Tite-Seq replicate；`sample_info.tsv` 描述样本、浓度、bin、index 和 cell count |
| `Kd_Inference/results_CH65/` | 11 个主结果文件 | count、fluorescence、16 位点 mutation metadata、6 个 replicate Kd 表及汇总 |
| `Kd_Inference/results_CH65/Kd_processed/` | 10 个 CSV/TSV | QC、replicate-filtered QC、三份 browser TSV、三份 delta-Kd 表和两份相关性表 |
| `Kd_Inference/results_CH65/stats/` | 4 个 TSV | fastq、UMI/count、indexing、genotype 读段处理统计 |
| `Epistasis_Inference/` | 6 个 CSV | 每抗原 biochemical/statistical 的 `r2` 交叉验证表，字段为 `fold_nb`、`order`、`train`、`test` |
| `Pathway_Inference/` | 30 个 CSV | 22 个 probability 表共享 16 个 `Order` 字段和 `Mutation`；8 个 `likelihoods_*` 是无规范 header 的矩阵输出 |
| `Figures/` | 19 个 CSV | 结构 epistasis、表达、拟合和绘图中间表；不视为独立实验样本 |
| `CH65_browser/data/` | 1 个 CSV + 3 个 Arrow | `CH65.csv` 是 65,536 genotype 的网页汇总；Arrow 为 MA90、SI06、G189E 的二进制浏览器数据 |

`Kd_processed/20221008_CH65_MA90_browser.tsv`、`..._SI06_browser.tsv` 和
`..._G189E_browser.tsv` 是三个抗原的浏览器拟合表，分别有 65,530、65,514、65,536
行。`CH65_browser/data/CH65.csv` 保留完整理论空间，并额外带布局坐标和每个突变的
delta-Kd；它与三个 browser TSV 不是一一行数相同的副本。

### 字段说明

- `Isogenic_Kd/` 的 197 个 event CSV 使用统一九列：`FSC-A`、`FSC-H`、`FSC-W`、
  `SSC-A`、`SSC-H`、`SSC-W` 为流式散射通道，`FITC-A`、`PE-A` 为荧光通道，`Time`
  为事件时间；均为原始数值文本，缺失或异常值不自动删除。
- `mut-list.csv` 的原始表头为一个无名首列、`shortname`、`geno`；无名列是导出索引。
  `run-list.csv` 为 `directory`、`row`、`shortname`、`mutant`、`antigen`、`replicate`、
  `prefix`，记录 well/文件到突变和抗原的连接。`concentrations-list.csv` 为 `well column`
  加条件浓度列，MA90/SI06 条件使用 `MA`、`SI`，G189E 条件使用 `MA_189`、`MA_193`。
- `replicate_info.tsv` 字段为 `replicate`、`solute`、`sequencing_data_subdir`、
  `cytometry_data_subdir`、`collection_date`、`construct`；replicate 字母为 a/b、d/e、g/h，
  不能直接当作独立抗原。`sample_info.tsv` 为 `sample_id`、`construct`、`solute`、
  `replicate`、`concentration`、`concentration_float`、`bin`、`sample_name`、`P5`、`P7`、
  `col_i`、`row_i`、`cell count`。
- `count_table.tsv` 首列 `geno` 覆盖 65,536 个 16-bit 二元 genotype；其余列按
  `CH65_<replicate>_<bin>`、`CH65_<replicate>_unsorted` 模式表示各 replicate/bin 的 reads。
  它是 count 输入，不是已归一化亲和力。`fluorescence.tsv` 字段为 `sample_name`、
  `sample_id`、`construct`、`solute`、`replicate`、`concentration`、`bin`、
  `mean_log10_PEs`、`std_log10_PEs`、`mean_log10_FITCs`、`std_log10_FITCs`。
- `mutation_list.tsv` 字段为 `mut_name`、`nt_pos`、`codon_0`、`codon_1`、`aa_0`、
  `aa_1`、`aa_pos`、`synonymous`，共 16 行。`V98I` 行保留上游原样冲突：`aa_0=R`、
  `aa_1=R`、`aa_pos=53`、`synonymous=True`；不能依据名称静默改成 V98I。
- 六个 `Kds_CH65*.tsv` 和 `Kds_CH65a_f3jrem.csv` 使用拟合字段：`geno`、`log10Kd`、
  `A`、`B`、`r2`、`sigma`、`mean_log10PE0..9`、`std_log10PE0..9`；带 replicate 后缀的
  列对应 a/b/d/e/g/h，另有 `Mean fluorescence expression`、`Std fluorescence expression`、
  `err_log10Kd`、`mean_sigma`、`log10Kd_pinned` 和 expression normalization 列。
- QC 表 `20221008_CH65_QCfilt.csv` 与 `..._REPfilt.csv` 的核心字段为 `geno`、两组
  replicate 值及 `MA90_mean/sem`、`SI06_mean/sem`、`G189E_mean/sem`、`pos1..pos16`、
  `som_mut`。`pos1..pos16` 是 genotype 位点列，`som_mut` 是突变位点计数。空值表示
  缺失；`6.0` 保留为下界钉扎。
- 三个 browser TSV 的公共字段模式是 `geno`、每个 replicate 的 `log10Kd`/`A`/`B`/`r2`/
  `sigma`、十个 `mean_log10PE` 与十个 `std_log10PE`，以及合并 Kd、误差、`mean_sigma`、
  `log10Kd_pinned` 和表达列。文件的 `log10Kd` 命名沿用上游，但本 README 按论文语义将
  其解释为 `-log10(K_D [M])`。
- 三个 `dKd` CSV 及 `20221008_CH65_dExp.csv` 使用 `Mutation`、`deltaKd` 或 `dexp`、
  `Number of mutations`、误差、`source`、`target`、`pos1..pos16`；delta 值是背景 genotype
  到目标 genotype 的派生效应。`dKd_summary.csv`、expression/Kd 相关表保留各抗原的
  mean/sem、replicate correlation 和 layout 字段。
- stats TSV 的字段分别为：`fastq_stats.tsv` 的 `sample`、`fastq_file`、总 reads、匹配
  reads、接受比例；`count_stats.tsv` 的 `sample`、reads/UMI/drop/count genotype；
  `indexing_stats.tsv` 的 index corrected/clean/thrown out 计数和接受比例；
  `geno_stats.tsv` 的 unmatched、mutation error、indel、substitution、accepted 计数。
- `Pathway_Inference/` 的 22 个 probability 表固定使用 `Order 1` 至 `Order 16` 和
  `Mutation`，行是突变阶次/名称的概率输出。8 个 `likelihoods_*` 文件第一行是实际矩阵
  数据而非稳定 schema header；列表示条件/序列组合的 likelihood，必须按矩阵读取，不能
  把第一行数值改作字段名。
- `Epistasis_Inference/` 的 `r2_CV_*` 字段为 `fold_nb`、`order`、`train`、`test`。
  `Figures/Epistasis_figures/structural_info.csv` 为 `residue`、`HA_contact`、
  `CDR3_contact`；`2ndorder_summary*.csv` 为 `labels`、`distance`、`epistasis`。表达图、
  Kd 图和 browser 图文件是可复算的绘图输入，不产生新的样本粒度。
- `CH65_browser/data/CH65.csv` 的字段以 `variant`、三抗原的 `*_log10Kd`/误差、表达、
  `fdl_x`/`fdl_y` 和各突变 `*_deltaKd` 为主；3 个 Arrow 文件是同一浏览器的二进制列式
  表示。网页 `index.html`、`yoda.js`、`yoda.css` 只负责展示，不改变数值。

### 数据示例

来自 `Kd_Inference/results_CH65/Kd_processed/20221008_CH65_QCfilt_REPfilt.csv` 的首行：

```text
geno=0000000000000000, MA90_mean=8.55177343972209, SI06_mean=6.0, G189E_mean=6.0, som_mut=0
```

该行代表完整 16 位点 genotype 的一个汇总标签，不是一个单独流式事件。来自
`mutation_list.tsv` 的前两行分别为 `N26D`（`AAC` 到 `GAT`）和 `S29R`（`AGT` 到
`CGG`）；这些是 mutation metadata，不是测量行。来自 event-level CSV 的每行则是
一个流式事件，不能与 genotype 行一一对应。

## PDB 数据库

本 source 补充保存三个 RCSB entry 的完整 FASTA 和 mmCIF，共 6 个文件：`5UGY`、`8EK6`
和 `8EKH` 各一对。`5UGY` 是 CH65–influenza HA 复合物，entity 级包含 HA1/HA2、CH65
heavy/light；它是论文结构映射的成熟 CH65 共享参考。`8EK6` 是 UCA Y35N unbound Fab，
`8EKH` 是 I-2 Y35N/H35N unbound Fab，二者是构象参考，不是当前三个 HA 的复合物。

文件验收结果如下：

| Entry | FASTA bytes / SHA-256 | mmCIF bytes / SHA-256 | 映射强度 |
| --- | --- | --- | --- |
| `5UGY` | 1,307 / `359b8864deab8fe88fbebceafb83fc98a8c9e3b48b59c1ecda2b325628d65fab` | 4,247,969 / `aa76b84eb84677f9d0eeedb7517739e8b77e598cb144656d1b1e2bf89094a493` | CH65/HA entry/entity；三等价副本未指定单一 copy |
| `8EK6` | 584 / `4473885ef18507aec18560824491f1f1349edf9e2b6d4c9c6e5193329ff77f1f` | 762,132 / `cd296089181cb474afad303e71caa0445d7f4fe51572743ba73dd841ac4b6cd6` | UCA Fab entry/entity |
| `8EKH` | 584 / `a2006a37d1d954a7fef8e6fff7b2f10ab0f7431fbbba62d992c7a61eae22b861` | 706,864 / `1be4c89b1f6c3b8af5eb4b0c661f3ff047b5c1afff8fe5c34c8eaa7930fd34ca` | I-2 Fab entry/entity |

`3SM5` 已被 RCSB 标为 obsolete，由 `5UGY` 替代，未纳入当前 payload；`4HKX` 是 CH67
Fab–HA，不是 CH65，也未纳入。由于论文未指定 5UGY 三个等价复合物副本中的一个，当前
不生成猜测性的单链角色 config；PDB 子任务保持 `partial`，可复用完整 entry/entity
文件进行后续 chain-copy 审计。

## 采集过程记录

- 2026-09-24：在仓库 `main` 直接执行，没有创建 branch 或 worktree。固定 Git commit/tree，
  在 Linux `ab02` 解包并逐文件以 Git blob SHA-1 验收 626 个路径和 1,309,420,145 bytes。
- 2026-09-24：保存 eLife VOR、8 个 additional files、ENA `PRJNA886089` inventory 和
  `5UGY`/`8EK6`/`8EKH` FASTA/mmCIF 到 staging 或远端 metadata。论文附件、PDB 文件逐项
  以 bytes/SHA-256 验收；inventory 为 180 runs、360 FASTQ、152,821,573,045 bytes。
- 2026-09-24：启动 ENA FASTQ 串行下载后，首个对象速率过低，预计超过可接受窗口；停止
  FASTQ 分支，删除未完成 `.partial` 文件和空的 `sra/PRJNA886089/` 目录。该失败过程
  不被写成 reads 已获得，source 状态为 `partial`。
- 2026-09-24：增强 Python 3.6 兼容的 validator，加入论文附件、PDB 六文件、`.partial`
  残留检查；README 每次修改后同步到 staging 根目录，再运行固定 markdownlint。
- 2026-09-24：staging 验收通过后，将 `.staging/snapshot-2023-02-01.partial` 原子重命名
  为正式 `snapshot-2023-02-01`，并在正式目录重跑同一 validator。验证 JSON 和远端缓存
  留在 `/data/ab02/yangwuyu/work/r69-ch65/`，不进入 source version 或 Git。

## 参考文献

- 论文：<https://doi.org/10.7554/eLife.83628>
- Git 仓库固定 commit：<https://github.com/amphilli/CH65-comblib/tree/cea336dfd05fa31d675f79038428bf7f0d177e78>
- Software Heritage revision：<https://archive.softwareheritage.org/swh:1:rev:cea336dfd05fa31d675f79038428bf7f0d177e78;origin=https://github.com/amphilli/CH65-comblib>
- ENA BioProject：<https://www.ebi.ac.uk/ena/browser/view/PRJNA886089>
- RCSB：<https://www.rcsb.org/structure/5UGY>、<https://www.rcsb.org/structure/8EK6>、<https://www.rcsb.org/structure/8EKH>

## 其他

### 数据范围和限制

本次正式发布是 `partial`：Git/论文/processed package/PDB 已取得并验收，但 360 个 ENA
FASTQ 未下载。inventory 的 bytes、论文中的 65,536/62,926 和仓库的 count table 都不能
被解释为完整 reads acquisition。replicate、抗原、bin、genotype 和结构 entry 属于不同
粒度，未经明确映射不能互相扩展。

### 完整性与验收

validator 检查固定 Git tree、论文 9 文件、ENA inventory、QC/REP-filtered genotype、
三份 browser TSV、count table、`V98I` metadata 冲突和三组 PDB FASTA/mmCIF。由于 FASTQ
分支停止，本次命令不使用 `--require-fastq`；报告中的 `fastq.present` 为 0，
`fastq.required` 为 false。正式目录必须与 staging 通过同一 validator。

### 许可和再分发边界

上游仓库根 `LICENSE` 声明 MIT，适用于其仓库代码和文档；论文和补充材料按 eLife 页面
标记为 CC BY 4.0。ENA FASTQ 的访问、使用和再分发应分别遵守 NCBI/ENA 条款；本 README
不把 Git 或论文许可推断为 FASTQ 的许可。PDB 文件按 RCSB 使用条款引用原始 entry。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 16 位点、65,536 个二元组合 | `mutation_list.tsv`、`QCfilt.csv`、`count_table.tsv` | 已验收 |
| 论文主图 62,926 共同过滤集合 | 论文 PDF；仓库保存分析输入但未将该数当作各表行数 | 论文报告，未独立重现 |
| FASTQ 位于 `PRJNA886089` | ENA inventory 180 runs/360 objects | inventory 已验收，reads 未取得 |
| 新报告 Fab 结构 `8EK6`、`8EKH` | RCSB FASTA/mmCIF 成对文件 | entry/entity 已验收，单链角色待审计 |
| CH65–HA 结构映射 | `5UGY` 完整 entry FASTA/mmCIF | entry/entity 已验收，等价副本未选定 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-24；部分完成）：ENA 180 runs 的 360 个 FASTQ 尚未获取。已核实
  inventory、总 bytes 和逐文件 MD5；已尝试串行下载并因传输速率过低停止，当前保留
  `partial` 状态和可追踪 inventory。下一步需要稳定传输窗口与足够 staging 空间，完成后
  才能把 `fastq.present` 改为完整并重新验收；在此之前不得声明 complete-study acquisition。
- `Q02`（最近更新：2026-09-24；待审计）：`5UGY` 有三个等价复合物副本，尚无证据指定
  单一 author/label chain copy。当前只提供完整 entry/entity 文件，不生成角色化单链 config；
  下一步需取得论文或 assembly 级证据后再决定是否补充 config。
- `Q03`（最近更新：2026-09-24；待复现）：论文 Figure 1 的 62,926 联合过滤集合尚未由
  notebook 独立逐行重现。当前 README 明确区分论文报告数与各 raw/processed 文件行数；下一步
  需固定 notebook/environment 后再报告集合等价性。
