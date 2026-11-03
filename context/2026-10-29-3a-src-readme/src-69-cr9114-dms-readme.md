---
tags:
  - context
---

# SRC_R69_CR9114_DMS 数据说明

## 数据集身份

- `source_id`：`SRC_R69_CR9114_DMS`
- `source_version`：`v1.0.0`
- 原作者或发布机构：University of Illinois Urbana-Champaign 的 Nicholas C. Wu 团队；仓库维护者为 `nicwulab`

### 来源方背景

论文作者单位为美国伊利诺伊大学厄巴纳–香槟分校，通讯作者 Nicholas C. Wu 关联该校
生物化学系、Carl R. Woese Institute for Genomic Biology 和 Carle Illinois College
of Medicine，见[论文作者机构信息](https://europepmc.org/article/PMC/PMC12637573)。
截至 2026-09-26，[校方个人页](https://mcb.illinois.edu/directory/profile/nicwu)
列明其为生物化学副教授，研究方向包括蛋白结构、生物信息学和抗体特异性。
[校方 Cancer Center 介绍](https://cancer.illinois.edu/people/nicholas-wu/)
说明该团队研究抗体–抗原相互作用的生物物理表征。该团队维护
[CR9114_DMS 正式数据与代码发布](https://github.com/nicwulab/CR9114_DMS/tree/v1.0.0)。

## 实验设计和数据口径

本 source 是 CR9114 抗流感广谱抗体的重链可变区单氨基酸突变扫描。实验把成熟
CR9114 light chain 固定，并分别构建 germline heavy chain 与 somatic/mature heavy
chain 的 yeast-displayed Fab 库。每个库的目标空间是 120 个位置乘以 20 种 amino
acid 和 stop，再加一条 `WT`，即 2,521 个 mutation IDs。四个 Tite-Seq assay 必须
分开处理：

| assay | 抗体背景 | 抗原 | final 行数 | 有限 `minus_log_Kd` | 低 input frequency |
| --- | --- | --- | ---: | ---: | ---: |
| germline–H1 | germline heavy + mature light | Brisbane/59/2007 H1 stem #4900 | 2,521 | 2,421 | 120 |
| somatic–H1 | mature CR9114 | Brisbane/59/2007 H1 stem #4900 | 2,516 | 2,476 | 111 |
| somatic–H3 | mature CR9114 | Singapore/INFIMH-16-0019/2016 H3 | 2,504 | 2,498 | 166 |
| somatic–BHA | mature CR9114 | B/Lee/1940 HA | 2,509 | 2,503 | 210 |

每项 Tite-Seq 使用两个 biological replicates，通过多个抗原浓度的 FACS bins 和 NGS
拟合 apparent affinity。`minus_log_Kd` 表示 `-log10(K_D [M])`，越大亲和力越强；
`minus_delta_log_Kd = log10(KD_WT) - log10(KD_mutant)`，越低表示突变破坏越强。
拟合脚本范围为 `5e-14` 到 `1e-5` M，因此精确等于 `5` 的 `minus_log_Kd` 是弱端
检测边界，不是精确的 10 µM 测量。四张 final 表中该边界分别有 5、0、6、55 行。

论文说 input frequency `<0.01%` 的变体不进入下游分析；作者 final tables 仍保留这些
行，绘图脚本再使用 `ipt_freq >= 0.0001` 过滤。本 source 不删除低覆盖行，也不把
空 affinity、边界值或理论上缺失的 mutation ID 补成实验值。

单独的 BLI 表给出 mature CR9114 对 H1 `<0.1 nM`、H3 `36 nM`、B/Lee40 `110 nM`
的验证值；论文另报告 germline–H1 `185 nM`。这些少量 BLI 结果与 Tite-Seq 的逐突变
apparent affinity 不是同一记录粒度。

## 论文原文

- 标题：*Vulnerability in the breadth evolution of an influenza broadly neutralizing antibody*
- 作者：Katrine E. Dailey 等；通讯作者 Nicholas C. Wu
- 版本：bioRxiv v1，2025-11-04
- DOI：`10.1101/2025.11.03.686356`
- PMID / PMCID：`41279651` / `PMC12637573`
- 文本许可：CC BY 4.0
- 正文归档：`articles/CR9114_DMS_2025-11-04_bioRxiv-v1.pdf`（32 页）及同版本 XML

主文 PDF 由 [PMC 官方 v1 存档](https://pmc-oa-opendata.s3.amazonaws.com/PMC12637573.1/PMC12637573.1.pdf)
取得；[版本元数据](https://pmc-oa-opendata.s3.amazonaws.com/PMC12637573.1/PMC12637573.1.json)
将 DOI、题名和 bioRxiv v1 对应到该对象。文件通过官方 MD5
`0f65bd2fac25094e9700ae004b23983f`、PDF metadata 题名及全部 32 页解析检查。
`articles/` 实际保存的六个对象如下：

| 文件 | 大小 | SHA-256 |
| --- | ---: | --- |
| `CR9114_DMS_2025-11-04_bioRxiv-v1.pdf` | 4.88 MiB（5,114,421 bytes） | `beba33f5cbca7dc27a5d6d70c38510f3bd5ae666f348bd4318ab412dbc5a4b35` |
| `CR9114_DMS_2025-11-04_bioRxiv-v1.xml` | 136.36 KiB（139,637 bytes） | `721db13a423e07c64547cfc61721d4a41c785493de63dfa33c485a7aca390464` |
| `CR9114_DMS_2025-11-04_bioRxiv-v1-supplement-1.pdf` | 5.38 MiB（5,645,811 bytes） | `ebf5e1f8a3e8a06459ebdf1604ac5896349f72fd1d0ea029ba304dfb7eea51b8` |
| `CR9114_DMS_2025-11-04_bioRxiv-v1-supplement-2-table-s1.xlsx` | 776.32 KiB（794,949 bytes） | `3b1dbf5cf503aff2676938ba3bf29dcef799a0ec27bf4c5eef55a7adb7b0d946` |
| `CR9114_DMS_2025-11-04_bioRxiv-v1-supplement-3-table-s2.xlsx` | 18.75 KiB（19,202 bytes） | `889903b7dc624856687b95e9ea01b4ace57b2bc975fdf2f7fd462f514680ec46` |
| `CR9114_DMS_2025-11-04_bioRxiv-v1-supplement-4-table-s3.xlsx` | 10.10 KiB（10,344 bytes） | `0d2bc8975dafc83da6ab3b26ece4921e5e42f491fb9e14fd2ba49125459a1360` |

Supplement 2 / Table S1 有 9,898 条数据记录：germline–H1 2,421、somatic–H1
2,476、somatic–H3 2,498、somatic–BHA 2,503。validator 已将这些记录按 experiment
和 Kabat mutation ID 与作者 final tables 的全部有限 mean affinity 逐项对照，数值一致。

## 仓库内容

作者仓库上游 tag 为 `v1.0.0`，固定 commit 为
`b290a3fcf6a2d24c388e535977d87adbd34db0cc`，Git tree 为
`17b8dd7db504ab6f28a05ce5c092dd529acacc6d`；项目 source version 沿用上游正式版本名。
同一版本的 ENA 原始测序对象增补于 `sra/`。

固定 commit 的 Git tree 是完整上游快照：146 个文件、98.62 MiB（103,408,904 bytes）；无 symlink、
submodule 或 Git LFS pointer。Git blob tree fingerprint 为
`f35a80fb0259967693962b1c7a2906d8bb600dfb9eafed2aa8bc856a83357b1e`，内容
SHA-256 inventory fingerprint 为
`6d5ca47a7b8668109c992827ca9ec4d85e3cf1b3e029c1fcc4d42c1d7c6abd10`。

```text
v1.0.0/
├── CR9114_DMS/
│   ├── Fasta/
│   ├── data/
│   ├── doc/
│   ├── graph/
│   ├── primer/
│   ├── result/
│   ├── script/
│   └── README.md
└── sra/
    ├── SRR34309012_1.fastq.gz
    ├── SRR34309012_2.fastq.gz
    └── ...（共 606 个文件）
```

`Fasta/` 保存 germline/somatic heavy chain 的 nucleotide 与 120-aa peptide；`primer/`
保存建库引物和 barcode；`doc/` 保存 FACS 条件与 IGHV1-69 HA-stem antibody 工作簿；
`result/` 保存 counts、拟合、final summary、BLI 对照和 Kabat 映射；`data/` 保存 SHM、
thermal shift 与 barcode 表；`script/` 是构建表和制图代码；`graph/` 的 61 个对象是
派生图片及 `.DS_Store`。仓库不含 event-level FCS，也不含运行级 FASTQ。

## 数据结构

### 文件组与记录关系

作者仓库共有 47 个 CSV/TSV，归并为 24 种实际 header schema，共出现 669 个原始字段名。
宽 count 表中的浓度、gate、replicate 字段按实验条件展开，不能把每一列当作独立变体。

| 文件组 | 数量或行数 | 记录粒度与关系 |
| --- | ---: | --- |
| `Fasta/` | 4 文件 | GL/WT heavy chain nucleotide 和 peptide；WT 即 somatic/mature 背景 |
| `doc/` | 3 XLSX | FACS 浓度/样本说明与 IGHV1-69 HA-stem antibody 汇总 |
| `data/CR9114_SHMheatmap.tsv` | 18 行 | germline 到 somatic CR9114 的 18 个 heavy-chain substitutions |
| `data/CR9114_mut_neut.tsv` | mutation-level | 突变中和/选择分析输入 |
| `data/CR9114_thermal_shift.csv` | 342 行 | thermal-shift measurement/summary 行 |
| `data/IGHV1-69_HAstem_Abs_SHM.csv` | 160 行 | 公布的 IGHV1-69 HA-stem antibodies 与 SHM 注释 |
| `data/barcodes_GL.tsv`、`barcodes_WT.tsv` | 各 241 行 | barcode 与样本/引物连接；不是 affinity 标签 |
| 六张顶层 count 表 | 2,506–183,288 行 | amino-acid 或 nucleotide mutation 的 input/assay wide counts |
| 四个 `*/HC_count_table_norm.csv` | 2,504–2,521 行 | 按浓度、gate、replicate 展开的 normalized counts |
| 四个 `*/clean_count_table.tsv` | 20,000–24,920 行 | `mut × conc` 汇总后的三个 bin-mean 列 |
| 13 个 `HC_KD_table_*.csv` | 2,455–2,503 行 | mean 或 replicate 的 `Kd`、`Kd_SE`、`p.value` 拟合结果 |
| 四张 `*_summary_rep.csv` | 2,491–2,503 行 | 两 replicate 的 Kd/SE/p-value 横向连接 |
| 四张 `*_summary_kabat.csv` | 2,504–2,521 行 | 最终 mutation、binding、affinity、input frequency 汇总 |
| `HC_WT_expression_score_kabat.csv` | 2,517 行 | somatic 库的 expression fields；发布的 `exp_score` 等同 rep1 |
| `IGHV1-69_HAstem_Ab_SHM_KD.tsv` | 1,956 行 | antibody SHM 对 germline landscape 的派生映射 |
| `KD_compare_BLI_DMS.tsv` | 40 行 | BLI 与 DMS 的小规模对照 |
| 两张 Kabat wide CSV | 各 1 行 | sequence metadata 加 Kabat-numbered residue columns |
| `sra/*.fastq.gz` | 606 文件 / 303 paired runs | 每 run 的两个 mate 各一个 gzip FASTQ；文件名保留 ENA accession |

四项 assay 的输入浓度 panel 不同。Germline–H1 使用 16、5、1.6、0.5、0.16、0.05、
0.016、0.005 nM；somatic–H1 使用 10 到 0.003 nM；H3 使用 100 到 0.033 nM；BHA
使用 200 到 0.067 nM。Somatic 原始 count 中另有 30 nM，但相应 R Markdown 明确将其
注释并排除在拟合之外。

已有 DNA 参考各 423 nt；按 `check_barcode.py` 定义的区域读取，它们分别编码
`CR9114_HC_GL.pep` / `CR9114_HC_WT.pep` 的全部 120 aa。`compile_TiteSeq.py`
指定的另一个文件名及 GL/WT 记录 ID 未在公开包提供；指定输入与已有 DNA 参考的
对应关系及 `codon_dist` 差异由 `Q05` 跟踪。

### 字段说明

- `sra/*.fastq.gz` 采用 FASTQ 四行记录：read identifier、read sequence、`+` 分隔行、
  base-quality string。`_1` 和 `_2` 文件由同一 ENA run 的配对对象清单关联；run 级 URL、
  bytes 和 MD5 固定在采集 cache，原始测序字节未改写。
- final `*_summary_kabat.csv` 的 `mut` 是线性位置 mutation ID，`mut_kabat` 是 Kabat
  编号 ID；`codon_dist` 是参考 codon 到能编码目标 amino acid 的 codon 的最小 nucleotide distance；`region` 为
  `FR1`、`CDR1`、`FR2`、`CDR2`、`FR3`、`DE Loop`、`CDR3`、`FR4` 或 `WT`；
  `mut_class` 为 `WT`、`silent`、`missense` 或 `nonsense`。
- `bind_score`、`bind_score_rep1`、`bind_score_rep2` 是作者归一化 binding score；
  `minus_delta_log_Kd` 及两个 replicate 列是相对 WT 的 affinity change；
  `minus_log_Kd` 及两个 replicate 列是 `-log10(K_D [M])`。空值表示无法获得相应拟合，
  不能写成 0；精确值 `5` 是弱端 boundary。
- `ipt_freq` 是 input-library frequency。Somatic final tables 同时保留
  `ipt_freq_rep1`、`ipt_freq_rep2`，germline 表只有合并 `ipt_freq`。`0.0001` 是论文下游
  QC 阈值，不是仓库原文件的删除阈值。
- germline final 表另有 `exp_score`、`exp_score_rep1`、`exp_score_rep2`。Somatic 的
  expression 位于独立 `HC_WT_expression_score_kabat.csv`，字段包含 `mut`、`mut_class`、
  `exp_score_rep1` 至 `exp_score_rep6`、`exp_score`；上游 final `exp_score` 实际由 rep1
  直接赋值再归一化，不能解释为六列平均。
- 顶层 amino-acid count 表以 `mut`、`mut_class` 起始，其余宽列编码采集日期、抗原
  concentration、gate/bin 和 replicate；nucleotide input 表以 nucleotide mutation
  sequence/ID 和 count 为粒度。`CR9114HC_WT_count_nuc_ipt.tsv` 有 183,288 行。
- `HC_count_table_norm.csv` 保留一个无名导出索引列、`mut`、`mut_class`，以及条件化
  normalized count columns。列名中的日期、`rep1`/`rep2`、浓度和 `gate1..4` 是实验
  维度，不能拆成新的 sequence labels。
- `clean_count_table.tsv` 的 `mut` 是 mutation ID，`conc` 为抗原浓度，`mut_class` 为
  mutation class；`bin_mean1`、`bin_mean2` 是两 replicate 的估计 mean bin，`bin_mean`
  是作者合并值。
- `HC_KD_table_mean.csv`、`HC_KD_table_rep1.csv`、`HC_KD_table_rep2.csv` 的共同字段为
  `mut`、`Kd`、`Kd_SE`、`p.value`。这里 `Kd` 沿用上游拟合内部参数名；正式解释应通过
  final table 的 `minus_log_Kd` 与 R Markdown 公式，不要仅凭列名假定线性摩尔单位。
- `HC_KD_table_summary_rep.csv` 使用 `Kd.x`、`Kd_SE.x`、`p.value.x` 和 `.y` 对应另一次
  replicate，`position` 是 mutation position。`.x/.y` 是 merge 后缀，不是 x/y 坐标。
- Table S1 的字段为原样拼写 `experimen t`、`mutation`、`type`、
  `minus_delta_log_Kd`、`minus_delta_log_Kd_rep1`、`minus_delta_log_Kd_rep2`、
  `input_freq`；其中 `mutation` 对应 final 表 `mut_kabat`，`input_freq` 对应
  `ipt_freq`。
- 两个 Kabat wide files 以 sequence/chain metadata 开头，随后每个 Kabat position
  一个字段；它们是单条编号映射，不是逐突变测量。`CR9114_SHMheatmap.tsv` 的行记录
  Kabat mutation 与结构/区域标签。
- `IGHV1-69_HAstem_Abs_SHM.csv` 的 28 个字段覆盖 antibody 名称、IGHV/IGHJ、CDR3、
  germline/somatic mutation、HA group/subtype、breadth/neutralization 和文献来源；
  缺失注释不能从 CR9114 推断填入。
- `IGHV1-69_HAstem_Ab_SHM_KD.tsv` 字段为 `ab_name`、`SHM`、`in_CR9114`、
  `minus_delta_log_KD (GL)`；这是把其他 antibody SHM 映射到 germline landscape 的
  派生表，不是 1,956 次独立 affinity 实验。
- `KD_compare_BLI_DMS.tsv` 的 8 个字段记录 mutation、antigen、BLI/DMS affinity 及
  delta 比较；只有 40 行，不能代表四个全库。`thermal_shift` 表为独立 stability
  表征，不能与 binding `Kd` 合并成同一标签。
- `barcodes_GL.tsv`、`barcodes_WT.tsv` 的 barcode、primer、sample/condition 字段用于
  demultiplexing。`primer/*.fa` 和 `doc/*FACS_info.xlsx` 是实验元数据，不是 mutation
  labels。`graph/*.png` 是派生可视化，不增加实验记录。

`codon_dist` 的原始值按上游保留。已有 DNA 参考可以完全对应 peptide，但不能完全
复现该字段：GL–H1 14 行、WT 三个 assay 各 494 行不符（合计 1,496 个表格行）。
这里的差异计数按 assay 行计算，不代表同样数量的独立变体。该字段的具体编码参考和
生成版本待作者确认。

### 数据示例

Germline–H1 final 表首行保留原始值：

```text
mut=A24A, mut_kabat=A24A, mut_class=silent,
minus_delta_log_Kd=0.03340389389808429,
minus_log_Kd=9.488967686755482,
ipt_freq=0.0002172293193377885
```

Somatic–H1 final 表的 `WT` 行为：

```text
mut=WT, mut_kabat=WT, region=WT, mut_class=WT,
minus_delta_log_Kd=-0.15536064635985802,
minus_log_Kd=9.145078078680317,
ipt_freq=0.03968406030658364
```

这些行分别是一个 mutation/background/antigen 的 summary，不是单个 read、FACS event
或 BLI trace。Somatic–H1 理论空间缺 `D109E`、`D109H`、`D109N`、`D109Q`、`D109V`；
Somatic–H3 缺 17 个 D109 mutation IDs，Somatic–BHA 缺 12 个。validator 精确检查这些
缺口，raw source 不补齐。

## PDB 数据库

论文 Figure 4 直接用 `4FQI` 分析 CR9114 结构。该 entry 是 mature CR9114–H5 HA
复合物，不是本研究 H1/H3/BHA assay 的精确抗原构建，也不是逐突变结构。完整 entry
保留四个 polymer entities：HA1 author chain A（334 aa）、HA2 chain B（177 aa）、
CR9114 heavy chain H（230 aa）、light chain L（216 aa）。R69 somatic peptide 120 aa
与 heavy chain H 的前 120 aa 完全一致。

| 文件 | 大小 | SHA-256 | 验收 |
| --- | ---: | --- | --- |
| `pdb/sequences/rcsb_pdb_4FQI.fasta` | 1.20 KiB（1,227 bytes） | `5b8ff6a0c9105190397118bcb3dde505f0f85015248f78014739a4c88a344cb4` | 4 polymer records；heavy prefix 精确匹配 |
| `pdb/structures/4FQI.cif` | 914.73 KiB（936,682 bytes） | `b437010518bc4ced413aa08bf21f965855a9704164e10b8bc0a7ef0084f60c8f` | Biopython 完整解析 1 model、8,365 atoms |

由于没有四项 assay 的 exact matched complex，本 PDB 子任务是 accepted reference-level
anchor，而不是 complete per-assay structural coverage。不得把 H5 entity 写成 H1/H3/BHA
实验抗原，也不得把同一结构复制到每个 mutant 伪装成实验结构。

## 采集过程记录

- 2026-09-24：核验 Git default branch、tag 和 commit；确认共享存储无 R69 正式目录。
- 2026-09-25：下载固定 codeload archive 到 source cache；archive 为 20.11 MiB（21,083,880 bytes），
  SHA-256 `c191e02ba48029e3eca9cc4de4b18f5798309b539507650655e0654c05f987a0`。
- 2026-09-25：从 Europe PMC 保存 full-text XML 与 supplementary bundle；bundle CRC
  通过，提取 Supplement 1 和 Table S1–S3，API wrapper ZIP 只留 cache，不发布。
- 2026-09-25：从 ENA 固定 `PRJNA1284397` inventory。文件为 118.30 KiB（121,138 bytes），SHA-256
  `6aa7a82c1a2b94f5444e6b8755c72e6f9b9519798093fbc458ed0935c223d601`；303 runs
  均为 paired Illumina NovaSeq 6000 AMPLICON/SYNTHETIC/PCR，共 606 个 FASTQ、
  104.37 GiB（112,068,045,801 bytes）。最小对象测试速率约 0.294 MB/s，完整串行下载估计约 4.4 天，
  因此最初接入范围暂不启动全量 reads 下载。
- 2026-09-25：后续 FASTQ 获取被固定为 direct-only：下载器清除继承的 HTTP/HTTPS/
  ALL/FTP proxy 变量，并为 curl 设置 `--noproxy '*'`。当前 ENA 直连探测在 10 秒后
  超时（HTTP `000`），因此不启动下载，也不自动回退到代理。
- 2026-09-25：保存 `4FQI` FASTA/mmCIF 并验证 sequence mapping 和结构可解析性；没有
  纳入论文未直接使用的候选 PDB。
- 2026-09-25：在 staging 运行独立 validator；按固定 README 合同 lint 后原子发布，
  再在正式目录运行相同 validator。cache 中的 archive/API inventory/validation JSON
  不进入 source version。

- 2026-09-26：用户明确允许代理试用，下载器仅在 `R70_NETWORK_MODE=proxy` 时
  使用现有代理环境。直连和代理断连证据保存在项目执行记录；代理凭据未写入脚本或日志。
- 2026-09-26：全部 606 个 FASTQ 下载完成，合计 104.37 GiB
  （112,068,045,801 bytes），下载进程退出 0。独立 validator 使用
  `--require-fastq` 重新读取每个对象，官方 bytes/MD5、303 runs 的配对文件集合及其他
  已发布材料全部通过；`Q01` 结案，原始文件保持 ENA 文件名和字节。
- 2026-09-26：首次 SSH 验收因默认 Python 缺少 Biopython 未通过结构解析门槛；
  切换到已有 Conda Python 3.14.6 / Biopython 1.85 后完整复验通过，没有新增系统依赖。
- 2026-09-26：复核论文作者单位、校方介绍与正式仓库，补入来源方背景和相应 TOC。
  `Q06` 的 reference-level 结构覆盖边界已由现有证据明确，正文保留其适用范围，
  从动态未决清单移除该稳定边界。

- 2026-09-26：使用 Linux `renameat2(RENAME_EXCHANGE)` 将完整增补包原子发布到
  `SRC_R69_CR9114_DMS/v1.0.0`，原上游文件逐项保持不变。正式目录复验采用相同
  `--require-fastq` 门槛；旧包仅保留至正式目录复验通过，随后清理重复 staging。

- 2026-09-26：从 PMC 官方开放存储取得主文 PDF v1，官方 MD5、版本身份与 32 页
  解析通过，`Q03` 结案。同一上游 v1.0.0 只增补论文归档和 README，既有原文件不改写；
  使用独立 README 与既有 payload 硬链接准备 staging，按独立验收及原子目录交换发布。
- 2026-09-26：复核作者当前完整 tree、唯一分支、唯一 release 与目标 FASTA 路径历史，
  并核对论文 Data Availability 及 PMC v1 附件。未发现缺失 FASTA 或 FCS 的公开入口；
  更新 `Q05`，新增 `Q07`，保存未发送的作者询问草稿。验证报告分别记录公开包接入和
  完整研究获取状态，替代单个固定 `partial` 标记。

- 2026-09-26：按用户决定，将 `Q07` FCS 标为跳过获取；核对论文 v1 的数据/代码
  公开声明没有明确承诺提供 FCS，在待处理清单保留该事实及未获取边界。
  作者材料询问草稿同步移除 FCS 请求，当前仍主动跟踪的缺失文件为 `Q05` 原输入 FASTA。

- 2026-09-27：核验已有 GL/WT DNA、peptide、作者参考区域和公开 `codon_dist`。
  DNA 对应的 peptide 完全一致，但 10,046 条非 WT 注释有 1,496 个表格行不符，
  分别为 GL–H1 14 行和 WT 三个 assay 各 494 行。`Q05` 修订为指定输入路径/ID 与
  注释生成依据待确认；原始文件保持不变，未生成替代 FASTA。

- 2026-09-27：按用户要求汇总全部未决事项，补全 `Q02` 许可与 `Q04` 表达汇总的
  当前处理、下一步和关闭条件；`Q05` 保留指定输入/ID 与距离标注差异，`Q07`
  保留 FCS 跳过决定。作者邮件重写为输入和标注、表达汇总、许可三组询问，
  草稿未发送。现有 DNA/蛋白一致及结合结果与 Table S1 的对照通过事实保持有效。

- 2026-09-27：复核作者联系记录。邮件草稿和飞书副本均已准备；用户实际发送状态
  尚未确认，`Q02`、`Q04`、`Q05` 保留待作者澄清状态。取得用户的已发送确认或
  可核对的发送记录后，再注明发信日期和“已邮件询问，等待作者回复”。

## 参考文献

- 预印本：<https://doi.org/10.1101/2025.11.03.686356>
- Europe PMC：<https://europepmc.org/article/PMC/PMC12637573>
- 作者固定 tag：<https://github.com/nicwulab/CR9114_DMS/tree/v1.0.0>
- 作者固定 commit：<https://github.com/nicwulab/CR9114_DMS/tree/b290a3fcf6a2d24c388e535977d87adbd34db0cc>
- ENA BioProject：<https://www.ebi.ac.uk/ena/browser/view/PRJNA1284397>
- NCBI BioProject：<https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1284397>
- RCSB `4FQI`：<https://www.rcsb.org/structure/4FQI>

## 其他

### 数据范围和限制

本次公开包达到 `verified public-package onboarding`：作者固定 processing package、
主文 PDF 与 XML、全部四份补充材料、`4FQI` 结构对，以及 303 runs 的 606 个
ENA FASTQ 已取得并验收。FASTQ 合计 104.37 GiB（112,068,045,801 bytes），按来源原样保存于 `sra/`。

`complete-study acquisition` 仍为 `partial`：作者脚本指定的
`Fasta/CR9114_original_seq.fa` 及其与已有 DNA 参考的等价关系尚待确认，由 `Q05`
跟踪。GL/WT 两份参考 DNA 已公开，编码区域与各自 peptide 一致，但其计算出的
`codon_dist` 与部分公开注释不符。event-level FCS
也未取得；作者在论文 v1 的公开声明中没有明确承诺提供该类文件，用户于
2026-09-26 决定跳过获取，`Q07` 保留事实记录，不再作为本次主动获取待办。
缺少 FCS 不阻碍直接使用已发布序列及处理后结合标签训练；它限制对逐事件流式
测量和筛选过程的重新核查。公开 wide count/fitted tables 和 FASTQ 的处理层级分别保留。

四个 assay、两个 antibody backgrounds、BLI 验证、expression、thermal stability 和
structure 属于不同标签与粒度。任何训练前整合必须保留 antigen identity、background、
assay type、replicate 和 boundary/QC 状态。

### 完整性与验收

validator 检查 146-file Git tree、47 张 CSV/TSV 的 schema inventory、四个 final assays、
理论 mutation IDs、raw/clean counts、9,898 条 Table S1 对照、expression 上游异常、
缺失 FASTA 引用、六个 article 对象、`4FQI` FASTA/mmCIF 和 ENA inventory。本次增补
独立验收已使用 `--require-fastq`，606 个 FASTQ 的官方 bytes/MD5 全部通过，
文件集合无缺失、额外对象或 `.partial` 残留。

### 许可和再分发边界

论文正文明确采用 CC BY 4.0。作者 Git 仓库没有 `LICENSE` 或 `COPYING`，不能把论文
文本许可自动推广到 repository payload。上游未特别说明覆盖仓库数据的许可，使用与
再分发范围不明确；该未说明事项不阻塞当前公开入口的本地接入发布。对外再分发、
商业或衍生使用判断仍需作者或正式条款提供覆盖该对象的许可。ENA reads、RCSB 文件和其中第三方来源分别遵守其数据库
条款；本 README 不替代原始权利声明。

### 与 R43 的边界

R43 是 2021 年的 CR9114 组合 landscape：16 个选择的自然成熟位点、`2^16` genotype、
yeast scFv、三个 replicates，抗原为 New Caledonia H1、Wisconsin H3 和 Ohio influenza B。
R69 是 120 位点单替换 landscape、yeast Fab、两个 biological replicates，抗原为
Brisbane H1 stem、Singapore H3 和 Lee40 BHA。R43 从 18 个 mature substitutions 中排除
了 A24S/E46D；R69 保留全部 18 个背景差异。

因此 R69 中 16 个 germline single substitutions 在 sequence level 可对应 R43 的 one-bit
genotypes，但不是相同 assay record。跨 source 划分训练/验证集时，应按 antibody lineage、
mutation sequence 和 antigen family 联合防泄漏，不能简单把它们当作独立无关样本或重复
实验求平均。

## 待解决问题与处理进展

- `Q02`（最近更新：2026-09-27；待确认，非接入发布阻塞）：作者仓库没有独立许可证。
  论文 CC BY 4.0 不自动覆盖仓库数据或代码，已分别记录对象范围。未特别说明许可
  不阻塞当前公开入口的本地接入发布；AI 研究、衍生数据、对外再分发及商用的具体
  条件仍需一手条款支持。当前保留公开文件原样及许可未确认状态，作者询问草稿
  已纳入数据和代码各自的许可问题，实际发送状态待确认。下一步请作者指明正式许可及适用对象；
  关闭条件为获得明确覆盖相应对象且能确定使用与再分发范围的条款或作者授权。
- `Q04`（最近更新：2026-09-27；已定位，汇总口径待作者确认）：论文方法称
  expression final 是两次 biological replicates 的平均，但 `compile_TiteSeq.py`
  合并 rep1–rep6 后显式令 `exp_score = exp_score_rep1` 并归一化；发布表也与该结果一致。
  当前按上游保留字段原值及各 replicate columns，未将原始 `exp_score` 解释为重复平均。
  作者询问草稿已纳入该差异，实际发送状态待确认；下一步请作者确认发布版实际采用的重复汇总方式、
  论文方法与代码的版本关系，以及是否存在对应的更新表格或脚本。
  关闭条件为取得可核验的汇总定义及对应版本，使论文、代码和发布表的口径关系明确。
- `Q05`（最近更新：2026-09-27；指定输入路径/ID 及注释生成依据待确认）：
  `compile_TiteSeq.py` 引用的 `Fasta/CR9114_original_seq.fa` 不在固定 tree；
  它期望 `CR9114_GL` / `CR9114_WT` 记录。已有 `Fasta/CR9114_HC_GL.fa` 和
  `Fasta/CR9114_HC_WT.fa` 两份参考 DNA，记录名分别带 `HC`，各 423 nt。
  按作者参考区域定义读取后，它们分别与公开 120 aa peptide 完全对应。
  对 10,050 条 final records 中 10,046 条非 WT 记录独立核算 `codon_dist`，GL–H1
  有 14 行不符，WT–H1/H3/fluB 各有 494 行不符，共 1,496 个表格行；参考残基均一致。
  因此已有参考序列覆盖，但不能将这些文件直接认定为缺失输入的等价替代；
  指定文件身份和差异产生原因仍未知。现有结合结果与 Table S1 的独立对照仍通过。
  下一步请作者说明原文件是否为旧引用、正确记录/区域对应关系，以及生成公开
  `codon_dist` 的编码参考和处理版本；询问草稿已修订，实际发送状态待确认。
  关闭条件为取得可核验的原输入或作者明确的替代关系，并解释上述注释差异。
  上游 DNA、结果值及脚本均保持原样。
- `Q07`（最近更新：2026-09-26；已注明并按用户决定跳过获取）：event-level FCS
  尚未取得。论文 v1 的 [Data Availability / Code Availability](https://pmc-oa-opendata.s3.amazonaws.com/PMC12637573.1/PMC12637573.1.pdf#page=22)
  列出 PRJNA1284397 测序库及作者代码仓库，没有明确承诺公开 FCS，也没有给出该类
  文件的存档或入口。作者完整 tree、分支、release assets 和 PMC v1 media 清单未发现 FCS。
  用户于 2026-09-26 决定跳过这类材料，保留未获取及公开承诺范围的事实记录，
  不再主动下载、追踪入口或就 FCS 联系作者。缺少该文件不阻碍使用作者已发布的序列及
  处理后结合标签训练；当前归档无法独立复核逐事件流式测量和筛选过程。
  若未来用户重新纳入获取范围，再按作者正式入口或访问条件执行。
