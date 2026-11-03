---
- tags:
  - context
---

# SRC_R75_BUZZ 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [原始测序数据](#原始测序数据)
  - [处理后亲和力数据集](#处理后亲和力数据集)
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

- `source_id`：`SRC_R75_BUZZ`
- `source_version`：`zenodo-10831512`
- 原作者或发布机构：Chinery L、Hummer AM、Mehta BB、Akbar R、Rawat P、Slabodkin A、Le Quy K、Lund-Johansen F、Greiff V、Jeliazkov JR、Deane CM（University of Oxford、University of Oslo、GSK R&D）；数据由 University of Oslo 团队于 Zenodo 发布

### 来源方背景

本来源由牛津大学 Deane 课题组主导， Oslo 大学 Greiff 课题组与 GSK R&D 参与。Charlotte M. Deane 是牛津大学统计系教授，长期从事抗体计算研究，OPIG（Oxford Protein Informatics Group）是其课题组，公开产出了 SAbDab、ANARCI、ABodyBuilder2、Humatch 等抗体资源与工具。论文的代码入口 `github.com/oxpig/Tzher2 affinity and beyond` 即 OPIG 组织仓库。Victor Greiff 是 Oslo 大学免疫信息学教授，其团队负责本数据的测序与文库部分；Zenodo 记录的五位作者均标 University of Oslo。

本来源既非公司发布，也不依赖单一机构的独立基础设施：实验由牛津完成，测序与数据发布于 Oslo。机构背景只用于说明数据产出方，不替代对具体实验方法和公开范围的核对。

## 实验设计和数据口径

本来源研究 Trastuzumab 重链 CDR-H3（IMGT 107—116 位，10 个残基）的大规模替换文库，靶点为 HER2。实验体系为酵母表面展示的 scFv：scFv 展示在酵母细胞表面，用荧光标记的 HER2 抗原染色，再按结合强度分选。

### 从文库到三档标签

论文描述的分选流程是：细胞先用抗 V5 荧光抗体（标记 scFv 表达）与链霉亲和素-PE 标记的抗原共同染色，随后按 PE 信号分选。第一轮取最强的 V5 阳性、抗原结合（PE 阳性）群体，标为高亲和力；其余细胞再依次分出中、低两档。三档因此是相对同一染色条件下的门限划分，不是三次独立测定的绝对 KD。

分选后的三个样品各做一轮 Illumina NovaSeq 6000 测序（300 cycles，S2 试剂盒），得到 Zenodo 上的六个 fastq 文件（每个样品 R1/R2 各一个）。论文把这些原始测序数据描述为已存入 Zenodo；`data.zip` 旁的说明则指出所有处理后数据与权重都在 `data.zip` 中。

### 处理后数据集的对象与量

公开的处理后主表是 `her2_aff_large`，共 524,346 条记录，其中 524,261 条为独特 CDR-H3 序列，85 条为重复。论文报告的三档计数是 178,160（high）、196,392（medium）、171,732（low），合计 546,284，比处理后表的 524,261 多 22,023 条。这一差额来自 `remove_overlap` 步骤：处理流程去掉了与 Mason et al. 数据集重叠的序列，论文表格给的是重叠移除之前的库规模。`data/affinity_data/her2/her2_aff_large/raw/` 下三个 `unique_cdr3s_sample_*.csv` 的行数恰好等于论文的三个档位计数，说明原始计数在 `raw/` 中保留，处理后的 `processed/` 才是去重结果。

处理后表的实际档位分布是 high 172,121、mid 189,981、low 162,159，与论文的三个数字各自相差约 6,000—9,600 条，符合去重叠的预期，但公开材料没有给出逐档的重叠条数。

### 二进制标签只对应“高”档

处理后 CSV 的 `label` 列是二值的，取值分布是：`class=high` 的 172,121 条全部 `label=1`，`class=mid` 的 189,981 条与 `class=low` 的 162,159 条全部 `label=0`。也就是说 `label` 不是“结合/不结合”，而是“高亲和力档 / 其余两档”。把 mid 与 low 合并成阴性会得到一个 32.8% 正例的极不平衡二分类目标，且阴性类内部仍包含真实的中等结合者。

这个构造直接影响可做的事：本数据适合“从 CDR-H3 序列预测是否落在最高亲和力档”，不适合回归绝对 KD，也不适合区分中与低。论文自身在做亲和力分类任务时也这样使用。

### 其他处理后子集

`data.zip` 中还包含三个与 HER2 相关的额外子集和一个流感对照体系，各自的记录粒度与标签不同：

- `her2/mason_et_al/`：Mason et al. 的 Trastuzumab 变体数据，移除与本数据集重叠的部分后按同一套 split 方案重排。`train70_val15/train.csv` 有 70 行、`weight` 无、字段为 `seq,label,edit_distance`，没有 `class` 与 `affinity`。
- `her2/shanehsazzadeh_et_al/`：仅一个 `test.csv`，198 行，字段含连续 `affinity`（6.24—9.03）且全部 `label=1`，是设计变体的外部验证集。
- `her2/shanehsazzaddeh_and_her2_aff_large_neg/`：401/86/87 的 train/val/test，字段含 `affinity`，正例 138/401，是正负混合的小型外部集；其目录名中的 `shanehsazzaddeh` 是上游拼写，未更正。
- `influenza/phillips_et_al/`：CR6261 与 CR9114 两条广谱流感抗体的结合数据，字段为 `H_seq` 与三个抗原（h1/h3/fluB）的平均信号与二值标签，属于与本数据不同的抗体-抗原体系。

这四组不是 `her2_aff_large` 的子集或重复测量，而是不同研究、不同抗体背景的数据，混用会把跨体系差异当成同体系排序。

### split 方案

`her2_aff_large/processed/remove_overlap/` 下提供两种切分策略，各 9 种规模（`0.7_0.15_0.15` 与八种 `trainN_valM`）：

- `random_split`：按行随机划分。
- `clonotype_split`：按 CDR-H3 序列聚类后整簇划分，`test.csv` 额外带 `cluster_centre` 列，当前 0.7/0.15/0.15 的测试集含 706 个簇。

两种策略在 0.7/0.15/0.15 下的测试集序列有 11,977 条重合，说明两者不是互斥的样本划分，而是同一批 524,346 条记录的不同切法。clonotype 版本把同簇近邻放在同一侧，随机版本则会把高度相似的 CDR-H3 分散到训练与测试，用随机版本报告的指标会偏高。这一点是本数据用于评价泛化时最关键的口径差异。

```text
zenodo-10831512/
├── 1-TZLIB-1_S2_L002_R1/R2_001.fastq.gz   样品 1（强结合）
├── 2-TZLIB-2_S3_L002_R1/R2_001.fastq.gz   样品 2（中等结合）
├── 3-TZLIB-3_S1_L002_R1/R2_001.fastq.gz   样品 3（弱结合）
└── data.zip
    └── data/
        ├── affinity_data/
        │   ├── her2/
        │   │   ├── her2_aff_large/raw/        3 个 CDR3 计数表
        │   │   ├── her2_aff_large/processed/  18 种 split × train/val/test + 权重
        │   │   ├── mason_et_al/processed/     8 种 split
        │   │   ├── shanehsazzadeh_et_al/processed/   1 个 test 表
        │   │   └── shanehsazzaddeh_and_her2_aff_large_neg/processed/  401/86/87
        │   ├── influenza/phillips_et_al/       CR6261 与 CR9114 的 5 种 split
        │   └── example/                        560/120/5,000 的小型示例
        ├── proteinmpnn_output/design_3000H3s_temp0pt3.fa   3,001 条 ProteinMPNN 设计
        └── esm_weights/.gitkeep                占位文件，无可下载内容
```

## 论文原文

### bioRxiv 预印本 v1

- 标题：*Baselining the Buzz. Trastuzumab-HER2 Affinity, and Beyond!*
- 作者：Lewis Chinery, Alissa M. Hummer, Brij Bhushan Mehta, Rahmad Akbar, Puneet Rawat, Andrei Slabodkin, Khang Le Quy, Fridtjof Lund-Johansen, Victor Greiff, Jeliazko R. Jeliazkov, Charlotte M. Deane
- 发表来源：bioRxiv
- 归档文本版本：预印本 v1（2024-03-29 发布）
- 发布日期：2024-03-29
- DOI：`10.1101/2024.03.26.586756`
- PMID / PMCID：无（Europe PMC 预印本记录 `PPR828678`）
- 本地文件：`articles/Buzz_2024-03-29_bioRxiv-v1.pdf`
- 文件大小：6.43 MiB（6,743,459 bytes）
- SHA-256：`926e7ab105b34dccf6b20ca6f6f7b89e41b14405eaaa67de10649bbecb157e97`
- 文本许可：CC BY 4.0（bioRxiv 页面标注）
- 补充材料：未本地归档；预印本正文指向 bioRxiv 在线补充材料

该预印本在 Europe PMC 的题名与 bioRxiv 不同：`PPR828678` 记录为 *Simple computational methods can outperform deep learning in designing diverse, binder-enriched antibody libraries*，DOI 与正文一致。本次核验以 DOI 对应关系和 PDF 内题名 *Baselining the Buzz. Trastuzumab-HER2 Affinity, and Beyond!* 为准，题名差异见 `Q05`。

本次未检索到与 DOI `10.1101/2024.03.26.586756` 对应的正式发表版；Europe PMC 中 Chinery 与 Deane 的共同署名论文不含本研究的期刊版。因此本 README 以预印本 v1 为唯一解释依据，不将其与同组的其他论文混用。

归档文件由发布方的原始文件名 `2024.03.26.586756.full.pdf` 改名而来，字节数与 SHA-256 未变。改名依据是发布方文件名只反映 DOI 中的投稿日期与版本，不反映数据集标识。

## 仓库内容

上游是 Zenodo record `10831512`，属于 concept `10549114` 的唯一版本（`relations.version[0].is_last = true`，`index = 1`）。记录创建于 2024-03-18，最后更新 2024-03-29，`metadata.version` 未填。`source_version` 因此使用不可变 record 号 `zenodo-10831512`，不按下载日期命名。

Record 共 7 个对象，全部为普通文件、无登录要求：六个 `*.fastq.gz` 与一个 `data.zip`。官方 MD5 与字节数已在 Zenodo API 中给出并逐项核对（见“完整性与验收”）。

```text
zenodo-10831512/
├── 1-TZLIB-1_S2_L002_R1_001.fastq.gz
├── 1-TZLIB-1_S2_L002_R2_001.fastq.gz
├── 2-TZLIB-2_S3_L002_R1_001.fastq.gz
├── 2-TZLIB-2_S3_L002_R2_001.fastq.gz
├── 3-TZLIB-3_S1_L002_R1_001.fastq.gz
├── 3-TZLIB-3_S1_L002_R2_001.fastq.gz
└── data.zip
```

`data.zip` 未在 raw 层解包：解包后总量为 3,952,636,154 bytes（约 3.68 GiB），保留压缩包可同时避免与既有字节重复占用。下游读取应按成员路径流式访问或解包到工作目录。

`data.zip` 内 201 个文件，含 106 个 CSV、42 个 HDF5 权重（`.h5`）、18 个 pickle 权重（`.pkl`）、1 个 FASTA。ZAIP 安全属性已检查：无绝对路径、无 `..` 穿越、无重复成员名。最大的几个成员是 `flaml_saved_weights.pkl`（316 MB、329 MB 两个）与多个约 173 MB 的 `.h5` 权重，权重合计约 2.98 GiB，占解包总量的绝大部分。

## 数据结构

### 原始测序数据

六个 fastq 文件是双端测序的原始读数，R1/R2 分别对应读段 1 与 2，均以 `@A01447:19:HGLFYDRXY:...` 形式的 Illumina 标识开头，末端带 8 碱基 i5/i7 组合索引（如 `CCGCGGTT+CTAGCGCT`）。三个样品各一对：

| 样品 | R1 文件 | R2 文件 | 读段数 |
| --- | --- | --- | ---: |
| 1（强结合） | `1-TZLIB-1_S2_L002_R1_001.fastq.gz` | `1-TZLIB-1_S2_L002_R2_001.fastq.gz` | 152,519,856 |
| 2（中等结合） | `2-TZLIB-2_S3_L002_R1_001.fastq.gz` | `2-TZLIB-2_S3_L002_R2_001.fastq.gz` | 139,702,556 |
| 3（弱结合） | `3-TZLIB-3_S1_L002_R1_001.fastq.gz` | `3-TZLIB-3_S1_L002_R2_001.fastq.gz` | 128,620,103 |

读段数由解压后行数除以 4 得到，六个文件的行数在各自 R1/R2 对内完全一致，说明双端配对完整。三条读段数只是测序深度，不是候选数：同一条 CDR-H3 会被多次读到，`her2_aff_large/raw/` 中的 `count` 列才是每条的读数。原始读数到 CDR-H3 计数、再到分档标签的转换脚本未包含在公开包中。

### 处理后亲和力数据集

`her2_aff_large` 是主数据集，两种 split 策略 × 九种规模。每种规模的 `train.csv`/`val.csv`/`test.csv` 三个文件合起来覆盖同一批 524,346 条记录，不同规模只是切法不同。所有 split 的合计都是 524,346，说明数据集本身未被重新抽样。

`her2_aff_large/raw/` 的三个文件是分档后的 CDR-H3 计数表，字段为 `aa_cdr3_seq` 与 `count`，行数分别为 178,160、196,392、171,732，与论文三档计数逐一相同。这些计数是测序读数的聚合，不是独立的实验测量。

`example/` 是 560/120/5,000 的小型示例集，字段与 `her2_aff_large` 相同（`seq,class,label,edit_distance`），可用于快速跑通代码而不必加载 500 万条。

### 字段说明

两套 schema 并存：HER2 主表用 `seq,class,label,edit_distance`（clonotype 版测试集另有 `cluster_centre`），流感子集用 `binary_id,str_aa_id,edit_distance,H_seq,h1_mean,h3_mean,fluB_mean,h1_label,h3_label,fluB_label`。

**HER2 处理表（`her2_aff_large`、`mason_et_al`、`example`）**

| 原始字段 | 表示、单位与来源 | 缺失与特殊编码 |
| --- | --- | --- |
| `seq` | CDR-H3 氨基酸序列，10 aa（IMGT 107—116 位） | 无缺失；`her2_aff_large` 中 524,261 条独特、85 条重复 |
| `class` | 分档名称，字符串 | `mason_et_al` 表无此列 |
| `label` | 二值标签，整数 | 无缺失；含义见下方取值表 |
| `edit_distance` | 相对亲本 CDR-H3 的编辑距离，整数 1—10 | 无缺失；`mason_et_al` 可达 10 |
| `cluster_centre` | 所属序列簇的中心序列 | 仅 `clonotype_split` 的测试集有；`random_split` 无此列 |

**`class`（`her2_aff_large`；取值范围依据：上游论文定义与当前版本观察）**

| 原始取值 | 含义 |
| --- | --- |
| `high` | 分选时的最高亲和力档 |
| `mid` | 中间档 |
| `low` | 最低档 |

**`label`（`her2_aff_large`；取值范围依据：当前版本观察）**

| 原始取值 | 当前记录数 | 含义 |
| --- | ---: | --- |
| `1` | 172,121 | `class=high`，即最高亲和力档 |
| `0` | 352,140 | `class` 为 `mid` 或 `low` |

`label` 与 `class` 是同一信息的两种编码，不是两个独立标签；`label=0` 包含两个不同的亲和力档。

**`shanehsazzadeh` 两个子表的字段**

| 原始字段 | 表示、单位与来源 | 缺失与特殊编码 |
| --- | --- | --- |
| `seq` | CDR-H3 序列 | 无缺失 |
| `affinity` | 连续亲和力值，6.24—9.03 | `shanehsazzaddeh_and_her2_aff_large_neg` 中 263 条负例为空 |
| `label` | 二值标签 | 无缺失；`shanehsazzadeh_et_al` 全部为 `1` |
| `class` | 分档名称 | `shanehsazzadeh_et_al` 无此列；`neg` 子集中有值但分布未展开 |
| `edit_distance` | 编辑距离，整数 | 无缺失 |

`affinity` 的单位未在公开材料中说明，取值 6.24—9.03 落在常见 `−log10(KD)` 或转换后的打分区间；本 README 不将其解释为 KD，相关疑问见 `Q03`。

**流感子集（`influenza/phillips_et_al`）**

| 原始字段 | 表示、单位与来源 | 缺失与特殊编码 |
| --- | --- | --- |
| `binary_id` | 16 位二进制串，表示抗体在各可变位点的氨基酸选择 | 无缺失 |
| `str_aa_id` | 与 `binary_id` 对应的氨基酸串，16 aa | 无缺失 |
| `edit_distance` | 相对亲本的编辑距离，整数 | 无缺失 |
| `H_seq` | 重链可变区全长序列 | 无缺失 |
| `h1_mean`、`h3_mean`、`fluB_mean` | 对三个抗原的平均结合信号 | 无缺失；量纲未在公开材料中说明 |
| `h1_label`、`h3_label`、`fluB_label` | 对三个抗原的二值结合标签，`0`/`1` | 无缺失 |

流感子集是另一抗体体系的独立数据，`h1/h3/fluB` 三个抗原各自有标签，不能与 HER2 的 `label` 合并成一个目标。

**`proteinmpnn_output/design_3000H3s_temp0pt3.fa`**

FASTA，3,001 条记录：第 1 条是模板（`trastuzumab_ABB2_model`，带 `X` 掩码），其余 3,000 条是 ProteinMPNN 在温度 0.3 下的设计，header 含 `T`、`sample`、`score`、`seq_recovery`。这些是计算设计序列，不含实验测量，与三个分档表不是同一层数据。

### 数据示例

`her2_aff_large` 测试集的一条记录：

```text
seq=YGDCHMYMYA,class=mid,label=0,edit_distance=8
```

它表示一个与亲本相差 8 个残基的 CDR-H3，被分入中间档，因此 `label=0`。该行来自 `random_split/train70_val15/test.csv`，只是 524,261 个独特序列中的一个，不是一次独立测量。

clonotype split 的同名文件多一列：

```text
seq=WAADGFYSIE,label=1,edit_distance=5,class=high,cluster_centre=WAAGRFYSLE
```

`cluster_centre` 指向该序列所属簇的中心；同簇的所有序列在 clonotype split 中落在同一侧，这是与 random split 的关键差异。

`her2_aff_large/raw/` 的一条计数记录：

```text
aa_cdr3_seq=WAAGRFYTFD,count=93576395
```

这是强结合样品中某条 CDR-H3 的测序读数次数，一条序列在这个样品里被读到 9,357 万次，属于测序深度而非独立实验重复。

## PDB 数据库

本来源的处理后数据只含 CDR-H3 序列与分档标签，不含任何 PDB ID 字段。锚点来自论文正文：预处理与结构建模以 Trastuzumab–HER2 复合物晶体结构 [1N8Z](https://www.rcsb.org/structure/1N8Z) 为起点；论文的 EGNN 基线用 FoldX BuildModel 在该结构上引入 CDRH3 突变，ProteinMPNN 部分则使用 ABodyBuilder2 预测的 Trastuzumab 结构。

映射强度是“共享参考复合物”：524,346 条记录没有逐条的实验结构，全部共享同一个亲本复合物。论文明确说明 FoldX 不建模骨架变化，因此由它生成的结构对突变效应只是近似，不能当作 524,261 个设计变体的实测或可靠预测结构。

项目从 RCSB 取得 1N8Z 的 entry 级 FASTA 与完整 mmCIF，未做选链或重建：

| 文件 | 大小 | SHA-256 |
| --- | ---: | --- |
| `pdb/sequences/rcsb_pdb_1N8Z.fasta` | 1.24 KiB（1,272 bytes） | `52eadcc9b098be1ac5beedb0ed931fc2b2b4d958f4095d0154b4b881eb240aa9` |
| `pdb/structures/1N8Z.cif` | 825.79 KiB（845,613 bytes） | `9f22f02b6e514de56dab8a48bc31a16302a51397779e64c398ad3a7f05cb19a2` |

FASTA 有 3 条 entity：`1N8Z_3`（HER2，chain C）、`1N8Z_2`（Herceptin Fab 重链，chain B）、`1N8Z_1`（Herceptin Fab 轻链，chain A）。`pdb/` 合计 2 个文件、846,885 bytes（0.81 MiB），inventory SHA-256 为 `ffebdad860bcd684a90815ab7264b35288af07f9ef45c8f5dcec627fe355c635`。未发布独立 PDB manifest。

论文的蛋白语言模型与结构基线使用 1N8Z 的抗体抗原界面原子；本 README 只保存该条目的原始序列与坐标，不包含论文生成的 FoldX 或 ABodyBuilder2 模型。

## 采集过程记录

- 2026-10-28 用户指定存储根 `G:\abag-datasets`。项目当前无 `project.toml`、`developer.local.toml` 与 `workspace/`，因此未按 skill 的 `workspace/users/<user>/docs/readme/` 生成草稿，README 直接写入 source version 目录；该偏差已获用户同意。
- 2026-10-28 首次从 Zenodo 直连下载 `data.zip`，40 秒内只到 53 MB 后连接重置（curl 退出码 56）。改走 FlClash 代理 `127.0.0.1:7892` 后单流稳定在约 1.3 MB/s，随即改为 7 个文件并发的每文件独立断点续传。
- 2026-10-28 一次失败的批量下载曾把 6 个 fastq 与 `data.zip` 停在部分字节，且留下 `.part` 残留。清理后在 `tmp/dl_r76.py` 中以「按当前文件大小发 Range 请求 → 达到声明字节数 → 校验 MD5」的循环重跑，逐文件打印进度。
- 2026-10-29 全部 7 个文件到达 Zenodo 声明的字节数，MD5 与 record metadata 逐个一致。
- 2026-10-29 从 bioRxiv 取预印本 PDF。首次请求返回 HTTP 429；改用带浏览器 UA 的完整路径 `.../early/2024/03/29/2024.03.26.586756.full.pdf` 后取得，字节数 6,743,459。Europe PMC 的 `fulltextRepo` 与 `?pdf=render` 入口均返回 403，未采用。
- 2026-10-29 独立验收：核对 7 个文件的字节数与 MD5；解压统计 `data.zip` 的 201 个成员与 3,952,636,154 bytes 解包总量；检查 zip 无绝对路径、无 `..`、无重复成员；按行数统计六个 fastq 的读段数并确认 R1/R2 配对一致；解析 `her2_aff_large` 全部 18 种 split 并与 `raw/` 三档计数、论文三档计数三方对照。
- 2026-10-29 按 PDB 硬性要求从论文正文定位锚点 1N8Z，取得 entry FASTA 与完整 mmCIF 并计算逐文件 SHA-256 与 inventory。
- 2026-10-29 发现处理后 `label` 只标记 `class=high`，`mid` 与 `low` 合并为 0；论文三档计数合计 546,284 与处理后 524,261 相差 22,023，差额可由 `remove_overlap` 解释但逐档条数未公开。两者分别转入 `Q01`、`Q02`。

## 参考文献

- Zenodo record：<https://zenodo.org/records/10831512>，DOI `10.5281/zenodo.10831512`
- Zenodo concept：<https://doi.org/10.5281/zenodo.10549114>
- 作者代码仓库（论文指明，未纳入本 payload）：`github.com/oxpig/Tzher2 affinity and beyond`
- 预印本：Chinery et al., *Baselining the Buzz. Trastuzumab-HER2 Affinity, and Beyond!*，bioRxiv，DOI `10.1101/2024.03.26.586756`
- Europe PMC 预印本记录：<https://europepmc.org/article/PPR/PPR828678>
- 参考结构：RCSB PDB [1N8Z](https://www.rcsb.org/structure/1N8Z)，Herceptin Fab 与 HER2 复合物；原始结构论文见该条目页 Primary Citation
- 被用于重叠移除的上游数据：Mason et al. 的 Trastuzumab 变体集（`data.zip` 内 `her2/mason_et_al/`）
- 本包引入的外部设计集：Shanehsazzadeh et al. 的 Trastuzumab 设计变体（`data.zip` 内 `her2/shanehsazzadeh_et_al/`）
- 流感对照数据：Phillips et al. 的 CR6261/CR9114 结合数据（`data.zip` 内 `influenza/phillips_et_al/`）

## 其他

### 数据范围和限制

本数据是单抗体（Trastuzumab）、单区域（重链 CDR-H3 的 10 个 IMGT 位点）、单抗原（HER2）的深度扫描。它不覆盖其他 CDR、轻链或抗原体系；任何跨抗体家族的结论都需要额外数据支持。

三档标签来自一次分选实验的门限划分，不是独立测量；同一序列在不同档位间的界限由染色与门控决定，公开包未给出各档对应的具体荧光区间或排序规则。二值 `label` 进一步把 mid 与 low 合并，削弱了数据对中等亲和力的分辨力。

`data.zip` 内同时打包了五个不同研究的处理后数据与 60 个模型权重文件。权重是本论文训练出的模型输出，不能与数据本身混为一谈；把它们当作原始数据会重复计算论文的建模结论。

### 完整性与验收

| 文件 | 大小 | MD5（Zenodo 官方） |
| --- | ---: | --- |
| `1-TZLIB-1_S2_L002_R1_001.fastq.gz` | 4.03 GiB（4,330,090,397 bytes） | `f4404263fb087c69286a4ba219767034` |
| `1-TZLIB-1_S2_L002_R2_001.fastq.gz` | 3.75 GiB（4,028,152,617 bytes） | `9aeb009f5538e573dfd888447def84a9` |
| `2-TZLIB-2_S3_L002_R1_001.fastq.gz` | 3.92 GiB（4,204,256,464 bytes） | `6d002f6d5fe1087ee5b609782c90482b` |
| `2-TZLIB-2_S3_L002_R2_001.fastq.gz` | 3.84 GiB（4,123,501,154 bytes） | `cfa5718726536a8bdc8dcda0a8f010c9` |
| `3-TZLIB-3_S1_L002_R1_001.fastq.gz` | 4.66 GiB（4,999,164,501 bytes） | `d8d3c2eb6a16fe7ed0cd051be8e0717e` |
| `3-TZLIB-3_S1_L002_R2_001.fastq.gz` | 3.95 GiB（4,244,555,629 bytes） | `bf6a0f68ff91147ed6d3968d5b4a73df` |
| `data.zip` | 2.36 GiB（2,537,190,576 bytes） | `3d5a61767dd5c3084ed015edb9b23cd7` |

七个文件的字节数与 MD5 均由 Zenodo record metadata 给出，本次下载后逐项复核一致。本地另计算了 SHA-256 以便后续不依赖 MD5：

| 文件 | SHA-256 |
| --- | --- |
| `1-TZLIB-1_S2_L002_R1_001.fastq.gz` | `08ed102c9e4852db757042f16f372f2c4823b8748ecd1b80d08793f60fb488f0` |
| `1-TZLIB-1_S2_L002_R2_001.fastq.gz` | `640b71fbfd0a330d71f99c7e5ce9ad66e7cae6a42fb786c8464123b5de36c389` |
| `2-TZLIB-2_S3_L002_R1_001.fastq.gz` | `54d278d14309754d8de2d78c4065edbf140678faddf0820239cc7865dd6c5500` |
| `2-TZLIB-2_S3_L002_R2_001.fastq.gz` | `282daa5b44d0f0b40c987a1f2ccb0edc525cf34953848b200b26410aa0ba49a9` |
| `3-TZLIB-3_S1_L002_R1_001.fastq.gz` | `f2c296e331b5665bbf29b5fdb3f2dabd6c222b4107cb419c0ff27e5a3c817d4e` |
| `3-TZLIB-3_S1_L002_R2_001.fastq.gz` | `c8432dfba20834a897d1cac6b36d34465eaf72fada44be24ca3b7696b672d405` |
| `data.zip` | `7528fb619db7f07461dd15075102579fc2d52955df3fd77cce84883f354dadbf` |

`data.zip` 的归档安全与内部结构均已检查；六个 fastq 均能完整解压并读出，R1/R2 行数在各自对内相等。`pdb/` 的完整性见“PDB 数据库”。

### 许可和再分发边界

Zenodo record 的 metadata 标注 `CC BY 4.0`，覆盖本 record 的七个对象。预印本文本的许可是 bioRxiv 页面标注的 CC BY 4.0；两者不是同一层，但方向一致，均允许署名下的再分发与衍生。

`data.zip` 内打包了来自其他研究的数据：`mason_et_al`、`shanehsazzadeh_et_al`、`influenza/phillips_et_al` 各有自己的原始出处与条款，Zenodo 记录的 CC BY 4.0 是否覆盖这些转载部分，上游未单独说明。下游若只用数据、不重分发，影响有限；若再分发 `data.zip` 整体，应按本文“参考文献”追溯各组件的原始许可。

`pdb/` 内的 RCSB 文件适用 RCSB 自身条款，使用时应保留 1N8Z 的原始结构引用。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 超过 524,000 个 Trastuzumab 变体 | `her2_aff_large` 处理后表 524,346 行、524,261 条独特序列 | 已包含 |
| 三档计数 178,160 / 196,392 / 171,732 | `her2_aff_large/raw/` 三个计数表行数逐一相同 | 已包含（去重叠前口径） |
| 原始测序读数存于 Zenodo | 六个 fastq.gz，按样品成对，合计约 4.21 亿条读段 | 已包含 |
| 处理后数据与权重在 `data.zip` | 201 个成员，含 106 CSV、60 权重 | 已包含 |
| CDR-H3 限制在 IMGT 107—116 位 | 所有 `seq` 与 `str_aa_id` 长度均为 10 aa | 已包含 |
| ProteinMPNN 设计与 ESM/CNN 权重 | `proteinmpnn_output/` 3,001 条 FASTA，42 个 `.h5` 与 18 个 `.pkl` | 已包含 |
| 逐候选的绝对 KD 测量 | 未发现；处理后只有分档与二值标签 | 未公开 |
| 原始读数到 CDR-H3 计数的转换脚本 | 未发现 | 未公开 |
| Mason 重叠移除的逐档条数 | 未发现；只能从论文与处理后表总数反推 22,023 | 部分包含 |
| 预印本的正式发表版 | 未检索到对应期刊版本 | 待确认 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-29；待上游说明）：处理后 `label` 只把 `class=high` 标为 `1`，`mid` 与 `low` 全部标为 `0`。已核实 172,121 条 high 全为 1，189,981 条 mid 与 162,159 条 low 全为 0，无交叉。影响：`label` 是一个 32.8% 正例的档位二分类目标，不是结合/不结合；把 `label=0` 当作非结合会误判 18.9 万条中等结合者。当前处理：README 在字段说明中明确两种编码的对应关系。下一步：确认上游是否有“结合/不结合”的独立标签，或 `mid` 是否应并入正例。
- `Q02`（最近更新：2026-10-29；待上游说明）：论文报告三档合计 546,284，处理后表 524,261，差 22,023。已核实 `raw/` 三个计数表行数等于论文三档计数，处理后表因 `remove_overlap` 减少，且 `raw` 与 `processed` 的档位差约 6,000—9,600 条不等。影响：任何以论文 546,284 为分母的比例推算都会与公开表不符。当前处理：README 同时给出两个口径并注明差额来源。下一步：取得逐档重叠条数后补全。
- `Q03`（最近更新：2026-10-29；待字段定义）：`shanehsazzadeh_et_al` 与 `neg` 子集的 `affinity` 取值 6.24—9.03，单位与方向未在公开材料给出。已核实它只出现在这两个外部子集，`her2_aff_large` 没有该列。影响：不能把 `affinity` 换算成 KD 或与其他子集的排序混用。当前处理：字段说明只记录数值范围并标为未定。下一步：核对上游代码或论文补充材料确认是否为 `−log10(KD)`。
- `Q04`（最近更新：2026-10-29；待方法细节）：`her2_aff_large` 同时提供 `random_split` 与 `clonotype_split` 两套切法，0.7/0.15/0.15 下测试集序列重合 11,977 条。已核实两种策略的 train/val/test 合计都是 524,346，说明是同一批记录的不同切法而非两个样本集。影响：用 random split 报告的性能会因近邻序列跨侧而偏高；选择哪套 split 直接决定评价结论。当前处理：README 明确两套切法的差异与适用场景。下一步：确认论文主表用的是哪一套，以及 clonotype 聚类的阈值。
- `Q05`（最近更新：2026-10-29；待上游澄清）：Europe PMC 记录 `PPR828678` 的题名 *Simple computational methods can outperform deep learning in designing diverse, binder-enriched antibody libraries* 与 bioRxiv PDF 内题名 *Baselining the Buzz. Trastuzumab-HER2 Affinity, and Beyond!* 不同，但 DOI 相同。已核实两者指向同一 DOI 且 PDF 内容包含 "Baselining the Buzz" 标题。影响：引用时若采用 Europe PMC 题名会与本地归档文件不一致。当前处理：以 PDF 内题名为准，两者都记录在“论文原文”。下一步：确认是否为预印本改名，或 Europe PMC 采用了投稿时的题名。
- `Q06`（最近更新：2026-10-29；待上游说明）：`data.zip` 打包了四个外部研究的数据（Mason、Shanehsazzadeh ×2、Phillips）与 60 个模型权重，Zenodo 记录的 CC BY 4.0 是否覆盖这些转载部分，上游未单独说明。已核实各组件的目录与字段均可独立识别。影响：若整体再分发 `data.zip`，需要为每个组件追溯原始许可。当前处理：在许可章节分层说明，不在 raw 层拆分这些组件。下一步：核对各组件原始论文的 Data Availability 后补全许可对照。
