# SRC_R33_IEDB_BCELL 数据说明

## 数据集身份

- `source_id`：`SRC_R33_IEDB_BCELL`
- `source_version`：`snapshot-2026-09-13`
- 原作者或发布机构：Immune Epitope Database（IEDB）；由 La Jolla Institute for Immunology 的 IEDB 团队及合作机构维护

### 来源方背景

IEDB 是美国 NIAID 资助的公共免疫表位知识库，成立于 2004 年，主导机构为 La Jolla Institute for Immunology。它持续接收同行评议文献的人工整理结果和直接提交。[2024 年更新论文](https://doi.org/10.1093/nar/gkae1092)报告当时已整理超过 25,000 篇文献；该数字只描述论文时点的运营规模，不代替本快照的逐表统计。

截至本次复核，[官方导出页](https://www.iedb.org/database_export_v3.php)仍按周滚动更新，受体数据也继续维护；[2026 年预印本](https://doi.org/10.64898/2026.06.03.728549)进一步记录了全库受体字段的重算、人工复核和 AIRR 导出改进。因此这里把 IEDB 视为持续运营的数据库来源方，而不是一次实验的作者团队。

## 实验设计和数据口径

IEDB 从发表研究和直接提交中人工整理 epitope、免疫受体、实验对象/条件和结果，不是一次统一设计/测量的库。B-cell 表的一行是一个 curated assay 记录；可以是抗体结合、解离常数、动力学、结构、功能或定性结果。不能把所有 Positive/Negative、quantitative measurement 或抗体名称都当成同一亲和力 label。

本次 B-cell 导出有 1,692,185 个唯一 assay IRI，只有 30,783 行有非空 quantitative measurement。其中 KD(nM) 有 14,503 行，off rate 5,324 行、on rate 5,208 行，3D structure(angstroms) 有 4,039 行；KA、功能和其他单位另列。必须联合 Assay Response measured、Units、Measurement Inequality 与 Method 解释数值：KD 越低越强，KA 越高越强，结构分辨率不是 binding affinity；本快照出现的 `>` 和 `>=` 是删失边界，不能一律当精确测量。定性结果可支持分类，但也必须按 assay 类型分层。

BCR 行是受体/epitope/引用/assay 关联，Group IRI 不是完整重轻链序列的唯一 ID。10,461 行对应 6,409 个 Receptor ID、5,888 个 Group IRI 和 9,004 个 receptor–epitope 对；6,745 行同时有两条 Protein Sequence，7,844 行至少有一条，6,914 行同时有 calculated V domains。Protein Sequence 的长度和范围异质，可能是 Fab/变量区或部分链；不能普遍称为完整 IgG。Curated 与 Calculated CDR/V gene 是不同来源，计算注释不是新增实验。epitope 可以是线性肽、不连续残基或非蛋白对象，不能统一当全长抗原。

文章/提交、epitope、受体 group、共享抗体和多次 assay 具有强相关性；不同表中的重复 BCR 交付不是新样本。后续 processed 才进行 B-cell/量纲/序列覆盖筛选与连接；raw 不生成标准化训练表、不修复 XML、不推断拼接重轻链。

## 论文原文

### IEDB 2024 更新论文

- 标题：The Immune Epitope Database (IEDB): 2024 update
- 作者：Randi Vita；Nina Blazeska；Daniel Marrama；IEDB Curation Team Members；Sebastian Duesing；Jason Bennett；Jason Greenbaum；Marcus De Almeida Mendes；Jarjapu Mahita；Daniel K Wheeler；Jason R Cantrell；James A Overton；Darren A Natale；Alessandro Sette；Bjoern Peters
- 发表来源：Nucleic Acids Research，53(D1)，D436–D443
- 归档文本版本：Europe PMC 正式发表版全文 XML
- 发布日期：2024-11-18
- DOI：[10.1093/nar/gkae1092](https://doi.org/10.1093/nar/gkae1092)
- PMID / PMCID：39558162 / PMC11701597
- 本地文件：`articles/IEDB_2024-11-18_EuropePMC-published.xml`
- 文件大小：87.19 KiB（89,286 bytes）
- SHA-256：`febaf1aa243064d73297768b11efc69c149156a548d2b2952cca6d137ed45332`
- 文本许可：CC BY 4.0；第三方材料仍按原标注处理
- 补充材料：论文没有单独列出的科学补充文件

这篇正式论文说明 IEDB 的整体收录、人工整理流程、维护方式和数据库规模，是理解来源方与全库口径的主要依据；其中的历史统计不是本次 2026-09-13 快照行数。

### IEDB 受体数据标准化预印本

- 标题：Revised Adaptive Immune Receptor Data in the Immune Epitope Database
- 作者：Lonneke Scheffer；Eve M Richardson；Randi Vita；Laura Zarebski；Nina Blazeska；Daniel K Wheeler；Jason R Cantrell；Sebastian N Deleuran；William D Lees；Scott Christley；Brian Corrie；Lindsay G Cowell；Alessandro Sette；Bjoern Peters
- 发表来源：bioRxiv
- 归档文本版本：bioRxiv v1 预印本全文 XML（Europe PMC 公共存档；尚未经过期刊同行评议）
- 发布日期：2026-06-06
- DOI：[10.64898/2026.06.03.728549](https://doi.org/10.64898/2026.06.03.728549)
- PMID / PMCID：42282728 / PMC13252180
- 本地文件：`articles/IEDBReceptor_2026-06-06_EuropePMC-bioRxiv-v1.xml`
- 文件大小：115.13 KiB（117,895 bytes）
- SHA-256：`799f2c5b47f6675222c53b88151967c91536b29bfcc8613277cc588c91218fd8`
- 文本许可：CC0
- 补充材料：`articles/IEDBReceptor_2026-06-06_bioRxiv-v1-Supplement.pdf`（8 页；2.09 MiB（2,189,369 bytes）；SHA-256 `c1a9b39dd67fa339e0dec3c86316cd020486cd47e96c07ea37ed4dff08dc5c62`；上游成员名 `media-1.pdf`）

这篇预印本直接解释当前 BCR/TCR 导出中的 curated 与 calculated 字段、CDR3 与 Junction 的定义差异、受体分组和标准化流程，因此与本数据源的字段理解直接相关。论文分析使用 2026-05-28 导出；本批数据冻结于 2026-09-13，两者的记录数不要求相同。补充 PDF 包含受体类型、物种和输入字段覆盖等汇总表，不是逐 assay 的另一份原始数据库。

## 仓库内容

一手入口为 IEDB `database_export_v3.php`，`export_data_v3.php` 的公开 JSON 清单给出具体官方 ZIP。本批获取时页面 footer 的 weekly `site_data` 为 September 13, 2026，因此版本固定为 `snapshot-2026-09-13`；实际 CSV/XML 对象的 Last-Modified 为 9 月 14–15 日，逐项保留。2026-09-24 复核时同一滚动页面已更新为 September 20, 2026，文件大小和 ETag 也已变化。为保持内部一致性，没有把新字节混入已经冻结的 9 月 13 日版本。

这些 URL 指向滚动对象，不是不可变 release；配置中保存的 ETag、大小与本次 SHA-256 共同固定实得字节身份，不能据同一 URL 推定以后仍返回同一版本。

```text
snapshot-2026-09-13/
└── IEDB/
    ├── iedb_export.zip
    ├── bcell_full_v3_single_file.zip
    ├── bcr_full_v3.zip
    ├── receptor_full_v3.zip
    ├── iedb_3d_full.zip
    ├── antigen_full_v3.zip
    ├── epitope_full_v3.zip
    └── reference_full_v3.zip
```

保留 full XML 和与 B-cell/BCR 连接相关的 CSV 交付，没有下载等价 TSV/MySQL 全表示，也没有把全库 XML 称为抗体筛选后的子集。

## 数据结构

### 关联导出与记录粒度

所有 CSV 保留两行原始 header：第一行分组，第二行字段。必须联合解释列名，多个 IEDB IRI / Protein Sequence / Type 不可按扁平同名覆盖。B-cell 是 131 列，BCR 是 74 列；3D ZIP 含 BCR/TCR/MHC 三张不同 schema 的表。receptor_full_v3.zip 再次包含同样的 BCR 表，不能重复计数。

| 归档 / 原生 CSV | 数据行 | 列数 |
| --- | --- | --- |
| IEDB/bcr_full_v3.zip!bcr_full_v3.csv | 10,461 | 74 |
| IEDB/receptor_full_v3.zip!tcr_full_v3.csv | 301,598 | 74 |
| IEDB/receptor_full_v3.zip!bcr_full_v3.csv | 10,461 | 74 |
| IEDB/iedb_3d_full.zip!bcr_3d_assays.csv | 5,947 | 48 |
| IEDB/iedb_3d_full.zip!tcr_3d_assays.csv | 449 | 67 |
| IEDB/iedb_3d_full.zip!mhc_3d_assays.csv | 1,585 | 43 |
| IEDB/antigen_full_v3.zip!antigen_full_v3.csv | 106,506 | 7 |
| IEDB/epitope_full_v3.zip!epitope_full_v3.csv | 2,752,537 | 32 |
| IEDB/reference_full_v3.zip!reference_full_v3.csv | 27,108 | 9 |
| IEDB/bcell_full_v3_single_file.zip!bcell_full_v3.csv | 1,692,185 | 131 |

B-cell 用 Assay ID/Reference/Epitope IRI 连接引用和 epitope；BCR 的 Assay IEDB IDs 可为逗号列表，和 B-cell IRI 中的字面 ID 对应，不是每行唯一一个 assay。Antigen/epitope/reference 导出有其原生 ID 与 IRI，不能以同名 antigen 自动连接。BCR 与 3D 的 chain 字段不能保证所有 B-cell assay 都有两链或严格 construct 映射。

### 原始 XML 与格式失败

完整 XML ZIP 有 27,106 个 reference XML 成员，解压后声明合计 26.62 GiB（28,583,964,611 bytes）；所有成员已完整读取且 ZIP CRC 通过。严格 XML parser 成功解析 27,028 份，78 份失败，存在非法控制字符等上游文本问题。例如 376.xml 第 97 行第 73 列有 XML 1.0 不允许的 U+0001；原始 member hash 和 hex 诊断留在运行证据，不在 raw 发布旁路报告。没有用容错 parser 或删除控制字符将失败伪装成通过。

因此 full XML 的内容验收为 partial，完整 byte archive 下载不等于全部 XML 可解析。CSV 层单独按原始字段通过扫描；两个层次的状态分开保留。

### 字段说明

以下清单按每张实际 CSV 的两层表头覆盖全部字段。`receptor_full_v3.zip` 中的 `bcr_full_v3.csv` 与独立 BCR ZIP 相同，故不重复列一遍；同包的 TCR 表和 3D ZIP 中随包交付的 TCR/MHC 表仍列出，但它们不是本数据源后续 BCR/PDB 筛选的核心对象。

| 文件 | 第一层分组 | 第二层字段（完整清单） | 含义与边界 |
| --- | --- | --- | --- |
| `bcell_full_v3.csv` | `Assay ID` | `IEDB IRI` | assay 主键 |
| | `Reference` | `IEDB IRI`、`Type`、`PMID`、`Submission ID`、`Authors`、`Journal`、`Date`、`Title` | 文献或提交来源及连接键 |
| | `Epitope` | `IEDB IRI`、`Object Type`、`Name`、`Reference Name`、`Modified residues`、`Modifications`、`Starting Position`、`Ending Position`、`IRI`、`Synonyms`、`Source Molecule`、`Source Molecule IRI`、`Molecule Parent`、`Molecule Parent IRI`、`Source Organism`、`Source Organism IRI`、`Species`、`Species IRI`、`Comments` | 表位身份、来源与范围 |
| | `Related Object` | `Epitope Relation`、`Object Type`、`Name`、`Starting Position`、`Ending Position`、`IRI`、`Synonyms`、`Source Molecule`、`Source Molecule IRI`、`Molecule Parent`、`Molecule Parent IRI`、`Source Organism`、`Source Organism IRI`、`Species`、`Species IRI` | 与表位相关的对象及其来源 |
| | `Host` | `Name`、`IRI`、`Geolocation`、`Geolocation IRI`、`Sex`、`Age`、`MHC Present` | 宿主信息 |
| | `1st in vivo Process` | `Process Type`、`Disease`、`Disease IRI`、`Disease Stage` | 第一次体内过程 |
| | `1st immunogen` | `Epitope Relation`、`Object Type`、`Name`、`Reference Name`、`Starting Position`、`Ending Position`、`IRI`、`Source Molecule`、`Source Molecule IRI`、`Molecule Parent`、`Molecule Parent IRI`、`Source Organism`、`Source Organism IRI`、`Species`、`Species IRI`、`Adjuvants`、`Route`、`Dose Schedule` | 第一次免疫原 |
| | `2nd in vivo Process` | `Process Type`、`Disease`、`Disease IRI`、`Disease Stage` | 第二次体内过程 |
| | `2nd immunogen` | `Epitope Relation`、`Object Type`、`Name`、`Reference Name`、`Starting Position`、`Ending Position`、`IRI`、`Source Molecule`、`Source Molecule IRI`、`Molecule Parent`、`Molecule Parent IRI`、`Source Organism`、`Source Organism IRI`、`Species`、`Species IRI`、`Adjuvants`、`Route`、`Dose Schedule` | 第二次免疫原 |
| | `Adoptive Transfer` | `Flag`、`Comments` | 过继转移标志与备注 |
| | `Immunization` | `Comments` | 免疫过程备注 |
| | `Assay` | `Location of Assay Data in Reference`、`Method`、`Response measured`、`Units`、`IRI`、`Qualitative Measure`、`Measurement Inequality`、`Quantitative measurement`、`Number of Subjects Tested`、`Number of Subjects Positive`、`Response Frequency (%)`、`Comments` | 实验方法、结果、单位和样本统计 |
| | `Assay Antibody` | `Antibody Source Material`、`Immunoglobulin Domain`、`Purification Status`、`Antibody Name`、`Heavy chain isotype`、`Light chain isotype` | 被测抗体注释 |
| | `Complex` | `PDB ID` | 结构连接键 |
| | `Assay Antigen` | `Epitope Relation`、`Object Type`、`Name`、`Reference Name`、`Starting Position`、`Ending Position`、`IRI`、`Source Molecule`、`Source Molecule IRI`、`Molecule Parent`、`Molecule Parent IRI`、`Source Organism`、`Source Organism IRI`、`Species`、`Species IRI` | 实验所用抗原对象 |
| `bcr_full_v3.csv` | `Receptor` | `Group IRI`、`IEDB Receptor ID`、`Reference Name`、`Type` | 受体分组、ID、名称与类型 |
| | `Reference` | `IEDB IRI` | 文献或提交来源及连接键 |
| | `Epitope` | `IEDB IRI`、`Name`、`Source Molecule`、`Source Organism` | 表位身份、来源与范围 |
| | `Assay` | `Type`、`IEDB IDs`、`MHC Allele Names` | 实验方法、结果、单位和样本统计 |
| | `Chain 1` | `Type`、`Organism IRI`、`Nucleotide Sequence`、`Curated V Gene`、`Calculated V Gene`、`Curated D Gene`、`Calculated D Gene`、`Curated J Gene`、`Calculated J Gene`、`Protein Sequence`、`Protein IRI`、`CDR3 Curated`、`CDR3 Calculated`、`Junction Calculated`、`CDR3 Start Curated`、`CDR3 End Curated`、`CDR3 Start Calculated`、`CDR3 End Calculated`、`CDR1 Curated`、`CDR1 Calculated`、`CDR1 Start Curated`、`CDR1 End Curated`、`CDR1 Start Calculated`、`CDR1 End Calculated`、`CDR2 Curated`、`CDR2 Calculated`、`CDR2 Start Curated`、`CDR2 End Curated`、`CDR2 Start Calculated`、`CDR2 End Calculated`、`V Domain Calculated` | 第一条受体链的原始与计算注释 |
| | `Chain 2` | `Type`、`Organism IRI`、`Nucleotide Sequence`、`Curated V Gene`、`Calculated V Gene`、`Curated D Gene`、`Calculated D Gene`、`Curated J Gene`、`Calculated J Gene`、`Protein Sequence`、`Protein IRI`、`CDR3 Curated`、`CDR3 Calculated`、`Junction Calculated`、`CDR3 Start Curated`、`CDR3 End Curated`、`CDR3 Start Calculated`、`CDR3 End Calculated`、`CDR1 Curated`、`CDR1 Calculated`、`CDR1 Start Curated`、`CDR1 End Curated`、`CDR1 Start Calculated`、`CDR1 End Calculated`、`CDR2 Curated`、`CDR2 Calculated`、`CDR2 Start Curated`、`CDR2 End Curated`、`CDR2 Start Calculated`、`CDR2 End Calculated`、`V Domain Calculated` | 第二条受体链的原始与计算注释 |
| `tcr_full_v3.csv` | `Receptor` | `Group IRI`、`IEDB Receptor ID`、`Reference Name`、`Type` | 受体分组、ID、名称与类型 |
| | `Reference` | `IEDB IRI` | 文献或提交来源及连接键 |
| | `Epitope` | `IEDB IRI`、`Name`、`Source Molecule`、`Source Organism` | 表位身份、来源与范围 |
| | `Assay` | `Type`、`IEDB IDs`、`MHC Allele Names` | 实验方法、结果、单位和样本统计 |
| | `Chain 1` | `Type`、`Organism IRI`、`Nucleotide Sequence`、`Curated V Gene`、`Calculated V Gene`、`Curated D Gene`、`Calculated D Gene`、`Curated J Gene`、`Calculated J Gene`、`Protein Sequence`、`Protein IRI`、`CDR3 Curated`、`CDR3 Calculated`、`Junction Calculated`、`CDR3 Start Curated`、`CDR3 End Curated`、`CDR3 Start Calculated`、`CDR3 End Calculated`、`CDR1 Curated`、`CDR1 Calculated`、`CDR1 Start Curated`、`CDR1 End Curated`、`CDR1 Start Calculated`、`CDR1 End Calculated`、`CDR2 Curated`、`CDR2 Calculated`、`CDR2 Start Curated`、`CDR2 End Curated`、`CDR2 Start Calculated`、`CDR2 End Calculated`、`V Domain Calculated` | 第一条受体链的原始与计算注释 |
| | `Chain 2` | `Type`、`Organism IRI`、`Nucleotide Sequence`、`Curated V Gene`、`Calculated V Gene`、`Curated D Gene`、`Calculated D Gene`、`Curated J Gene`、`Calculated J Gene`、`Protein Sequence`、`Protein IRI`、`CDR3 Curated`、`CDR3 Calculated`、`Junction Calculated`、`CDR3 Start Curated`、`CDR3 End Curated`、`CDR3 Start Calculated`、`CDR3 End Calculated`、`CDR1 Curated`、`CDR1 Calculated`、`CDR1 Start Curated`、`CDR1 End Curated`、`CDR1 Start Calculated`、`CDR1 End Calculated`、`CDR2 Curated`、`CDR2 Calculated`、`CDR2 Start Curated`、`CDR2 End Curated`、`CDR2 Start Calculated`、`CDR2 End Calculated`、`V Domain Calculated` | 第二条受体链的原始与计算注释 |
| `bcr_3d_assays.csv` | `Reference` | `B Cell Assay IRI`、`Reference IRI` | 文献或提交来源及连接键 |
| | `Assay` | `Method/Technique` | 实验方法、结果、单位和样本统计 |
| | `1st in vivo Process` | `Process Type`、`Immunogen` | 第一次体内过程 |
| | `Host` | `Name`、`Host IRI` | 宿主信息 |
| | `Epitope` | `Epitope IRI`、`Epitope Description`、`Antigen Name`、`Antigen IRI`、`Antigen Sequence`、`Organism Name`、`Organism IRI`、`Parent Antigen ID`、`Parent Antigen Name`、`Parent Organism IRI`、`Parent Organism Name` | 表位身份、来源与范围 |
| | `Antibody` | `Receptor ID`、`Antibody Type`、`Antibody Name`、`Chain 1 Organism Name`、`Chain 1 Organism IRI`、`Chain 2 Organism Name`、`Chain 2 Organism IRI`、`Assayed Antibody`、`Heavy Chain Type`、`Light Chain Type`、`Chain 1 type`、`Chain 2 type`、`Chain 1 Sequence`、`Chain 2 Sequence` | BCR/抗体链与构建体注释 |
| | `3D Complex` | `Complex ID`、`PDB ID`、`Resolution (Angstrom)`、`Antibody PDB Chain 1`、`Antibody PDB Chain 2`、`Antigen PDB Chain(s)`、`Curated Epitope Residues`、`Curated Paratope Residues`、`Calculated Epitope Residues`、`Calculated Paratope Residues`、`Calculated Atom Pairs`、`Curated Antigen Buried Surface Area`、`Curated Antibody Buried Surface Area`、`Calculated Antigen Buried Surface Area`、`Calculated Antibody Buried Surface Area`、`Comments` | PDB、author-chain、接触残基和埋藏面积 |
| `tcr_3d_assays.csv` | `Reference` | `T Cell Assay IRI`、`Reference IRI` | 文献或提交来源及连接键 |
| | `Assay` | `Method/Technique` | 实验方法、结果、单位和样本统计 |
| | `1st in vivo Process` | `Process Type`、`Immunogen` | 第一次体内过程 |
| | `Host` | `Name` | 宿主信息 |
| | `Epitope` | `Epitope IRI`、`Epitope Description`、`Antigen Name`、`Antigen IRI`、`Antigen Sequence`、`Starting Position`、`Ending Position`、`Epitope Sequence`、`Organism`、`Organism IRI`、`Parent Antigen ID`、`Parent Antigen Name`、`Parent Organism IRI`、`Parent Organism name` | 表位身份、来源与范围 |
| | `TCR` | `Receptor ID`、`TCR Type`、`TCR Name`、`Chain 1 Organism Name`、`Chain 1 Organism IRI`、`Chain 2 Organism Name`、`Chain 2 Organism IRI`、`Chain 1 type`、`Chain 2 type`、`Chain 1 Sequence`、`Chain 2 Sequence` | TCR 链注释 |
| | `MHC` | `MHC Allele`、`MHC Class`、`MHC IRI`、`MHC Chain1`、`MHC Chain2`、`MHC Chain1 IRI`、`MHC Chain1 Sequence`、`MHC Chain2 IRI`、`MHC Chain2 Sequence` | MHC 链、等位基因和序列 |
| | `3D Complex` | `Complex ID`、`PDB ID`、`Resolution (Angstrom)`、`TCR PDB Chain 1`、`TCR PDB Chain 2`、`MHC PDB Chain1`、`MHC PDB Chain2`、`Antigen PDB Chain(s)`、`Curated Epitope Residues Interacting with TCR`、`Curated Epitope Residues Interacting with MHC`、`Curated TCR Residues Interacting with Epitope`、`Curated TCR Residues Interacting with MHC`、`Curated MHC Residues Interacting with TCR`、`Curated MHC Residues Interacting with Epitope`、`Calculated Epitope Residues`、`Calculated Epitope Residues Interacting with TCR`、`Calculated Epitope Residues Interacting with MHC`、`Calculated TCR Residues Interacting with Epitope`、`Calculated TCR Residues Interacting with MHC`、`Calculated MHC Residues Interacting with Epitope`、`Calculated MHC Residues Interacting with TCR`、`Calculated Atom Pairs`、`Curated Antigen Buried Surface Area`、`Curated TCR Buried Surface Area`、`Calculated Antigen Buried Surface Area`、`Calculated TCR Buried Surface Area`、`Comments` | PDB、author-chain、接触残基和埋藏面积 |
| `mhc_3d_assays.csv` | `Reference` | `MHC Assay IRI`、`Reference IRI` | 文献或提交来源及连接键 |
| | `Assay` | `Method/Technique` | 实验方法、结果、单位和样本统计 |
| | `Epitope` | `Epitope IRI`、`Epitope Description`、`Antigen Name`、`Antigen IRI`、`Antigen Sequence`、`Starting Position`、`Ending Position`、`Epitope Sequence`、`Organism Name`、`Organism IRI`、`Parent Antigen ID`、`Parent Antigen Name`、`Parent Organism IRI`、`Parent Organism name` | 表位身份、来源与范围 |
| | `MHC` | `MHC Class`、`MHC Allele`、`MHC IRI`、`Chain1 Type`、`Chain2 Type`、`Chain1 IRI`、`Chain 1 Sequence`、`Chain2 IRI`、`Chain 2 Sequence` | MHC 链、等位基因和序列 |
| | `3D Complex` | `Complex ID`、`PDB ID`、`Resolution (Angstrom)`、`MHC PDB Chain 1`、`MHC PDB Chain 2`、`Antigen PDB Chain(s)`、`Curated Epitope Residues`、`Curated MHC Residues Interacting With Epitope`、`Calculated Epitope Residues`、`Calculated Epitope Residues Interacting With MHC`、`Calculated MHC Residues Interacting With Epitope`、`Calculated Atom Pairs`、`Curated Antigen Buried Surface Area`、`Curated MHC Buried Surface Area`、`Calculated Antigen Buried Surface Area`、`Calculated MHC Buried Surface Area`、`Comments` | PDB、author-chain、接触残基和埋藏面积 |
| `antigen_full_v3.csv` | `Antigen` | `Antigen Name`、`Antigen IRI`、`Organism Name`、`Organism IRI`、`# Epitopes`、`# Assays`、`# References` | 抗原及聚合计数 |
| `epitope_full_v3.csv` | `Epitope ID` | `IEDB IRI` | 表位主键 |
| | `Epitope` | `Object Type`、`Name`、`Modified Residue(s)`、`Modifications`、`Starting Position`、`Ending Position`、`IRI`、`Synonyms`、`Source Molecule`、`Source Molecule IRI`、`Molecule Parent`、`Molecule Parent IRI`、`Source Organism`、`Source Organism IRI`、`Species`、`Species IRI` | 表位身份、来源与范围 |
| | `Related Object` | `Epitope Relation`、`Object Type`、`Name`、`Starting Position`、`Ending Position`、`IRI`、`Synonyms`、`Source Molecule`、`Source Molecule IRI`、`Molecule Parent`、`Molecule Parent IRI`、`Source Organism`、`Source Organism IRI`、`Species`、`Species IRI` | 与表位相关的对象及其来源 |
| `reference_full_v3.csv` | `Reference ID` | `IEDB IRI` | 按原始两层表头解释；IRI 保留为连接键 |
| | `Reference` | `Type`、`PMID`、`Submission ID`、`Alternate IRIs`、`Authors`、`Journal`、`Date`、`Title` | 文献或提交来源及连接键 |

下表列的是本快照实际观察到的全部低基数或受控类别值及行数，不把它们外推为 IEDB 将来版本永不变化的固定词表。`<空>` 表示原始空值；它不是一个阴性类别。

| 文件 | 字段 | 本快照全部已观察值（含行数） | 含义与使用边界 |
| --- | --- | --- | --- |
| `bcell_full_v3.csv` | `Assay / Method` | `microarray`（924,130 行）；`phage display`（277,492 行）；`High throughput multiplexed assay`（173,855 行）；`ELISA`（171,357 行）；`western blot`（37,929 行）；`biological activity`（29,523 行）；`surface plasmon resonance (SPR)`（14,160 行）；`inhibition by antigen`（11,035 行）；`bio-layer interferometry assay`（7,866 行）；`immuno staining`（7,028 行）；`in vivo assay`（6,675 行）；`flow cytometry`（6,040 行）；`radio immuno assay (RIA)`（4,612 行）；`x-ray crystallography`（4,051 行）；`electron microscopy`（2,784 行）；`binding assay`（2,516 行）；`immunoprecipitation`（1,838 行）；`cross blocking`（1,548 行）；`inhibition by antigen (~ IC50)`（1,413 行）；`quenching`（1,026 行）；`immunohistochemistry`（886 行）；`footprinting assay`（858 行）；`mass spectrometry`（795 行）；`any method`（696 行）；`calorimetry`（629 行）；`chromatography`（616 行）；`hydrogen/deuterium exchange footprinting assay`（315 行）；`ELISPOT`（263 行）；`nuclear magnetic resonance (NMR)`（199 行）；`antigen inhibition`（21 行）；`small-angle scattering assay`（18 行）；`quartz crystal microbalance`（6 行）；`hydroxyl-radical footprinting assay`（5 行） | 实验技术名称；不同方法的直接观察量和灵敏度不同，须与 `Response measured` 联合解释。 |
| `bcell_full_v3.csv` | `Assay / Response measured` | `qualitative binding`（1,449,408 行）；`antibody binding`（174,548 行）；`neutralization`（23,839 行）；`dissociation constant KD`（14,513 行）；`3D structure`（6,214 行）；`off rate`（5,324 行）；`on rate`（5,208 行）；`hemagglutination inhibition`（1,436 行）；`secondary in vitro activity`（1,106 行）；`pathogen burden after challenge after adoptive transfer`（1,101 行）；`survival after pathogen challenge after adoptive transfer`（920 行）；`association constant KA`（772 行）；`antibody-dependent cellular cytotoxicity`（671 行）；`hypersensitivity`（634 行）；`protection from pathogen challenge`（589 行）；`survival from pathogen challenge`（553 行）；`pathogen burden after challenge`（533 行）；`complement-dependent cytotoxicity`（511 行）；`opsonization`（494 行）；`decreased disease`（484 行）；`histamine release`（412 行）；`antigen activation`（410 行）；`agglutination`（360 行）；`disease exacerbation`（313 行）；`decreased disease after adoptive transfer`（248 行）；`survival from challenge after adoptive transfer`（228 行）；`tolerance`（217 行）；`antibody activity inhibition`（213 行）；`protection from pathogen challenge after adoptive transfer`（212 行）；`tumor burden after challenge after adoptive transfer`（164 行）；`disease exacerbation after adoptive transfer`（104 行）；`protection from fertility`（101 行）；`in vivo activity`（71 行）；`survival from challenge`（55 行）；`hypersensitivity after adoptive transfer`（36 行）；`tumor burden after challenge`（31 行）；`protection from other challenge`（29 行）；`protection from other challenge after adoptive transfer`（26 行）；`tolerance after adoptive transfer`（22 行）；`survival from tumor challenge`（19 行）；`protection from challenge`（17 行）；`survival after tumor challenge after adoptive transfer`（16 行）；`protection from challenge after adoptive transfer`（10 行）；`protection from tumor challenge after adoptive transfer`（7 行）；`protection from tumor challenge`（6 行） | 实际测量终点；定性结合、KD、KA、动力学、结构和功能结果分属不同量纲。 |
| `bcell_full_v3.csv` | `Assay / Units` | `<空>`（1,662,317 行）；`nM`（14,513 行）；`1/s`（5,324 行）；`M^-1s^-1`（5,208 行）；`angstroms`（4,051 行）；`1/nM`（772 行） | `nM` 为 KD 浓度，`1/nM` 为 KA，`1/s` 为解离速率，`M^-1s^-1` 为结合速率，`angstroms` 为结构分辨率；空值表示未给单位。 |
| `bcell_full_v3.csv` | `Assay / Qualitative Measure` | `Negative`（1,239,285 行）；`Positive`（394,184 行）；`Positive-Low`（45,454 行）；`Positive-High`（8,972 行）；`Positive-Intermediate`（4,290 行） | `Negative` 为阴性；`Positive` 未细分强度；`Positive-Low`、`Positive-Intermediate`、`Positive-High` 是来源整理的定性层级，不能跨 assay 当作统一亲和力刻度。 |
| `bcell_full_v3.csv` | `Assay / Measurement Inequality` | `<空>`（1,682,460 行）；`=`（9,265 行）；`>`（412 行）；`>=`（48 行） | 空值表示没有记录不等关系；`=` 表示按所列数值记录；`>` 与 `>=` 保留来源中的比较关系，所列数值不能当作等号条件下的精确测量值。 |
| `bcr_full_v3.csv` | `Receptor / Type` | `heavylight`（7,121 行）；`construct`（1,756 行）；`heavy`（950 行）；`scFv`（369 行）；`heavyheavy`（210 行）；`lightlight`（26 行）；`IgNAR`（17 行）；`light`（12 行） | `heavylight` 为重轻链组合，`scFv` 为单链可变片段，`IgNAR` 为鲨鱼新抗原受体；`heavy`、`light`、`heavyheavy`、`lightlight` 和 `construct` 是来源保留的类别，具体链构成与完整性还需结合 Chain 1/2 字段判断。 |
| `bcr_full_v3.csv` | `Assay / Type` | `B cell`（10,461 行） | 本 BCR 文件只观察到 `B cell`，表示关联的是 B-cell assay。 |
| `bcr_full_v3.csv` | `Chain 1 / Type` | `heavy`（10,376 行）；`lambda_light`（31 行）；`<空>`（23 行）；`IgNAR`（17 行）；`construct`（10 行）；`light`（2 行）；`kappa_light`（2 行） | 第一条链的角色；`heavy`、`light`、`kappa_light`、`lambda_light`、`IgNAR` 和 `construct` 保留原分类，空值表示未提供。 |
| `bcr_full_v3.csv` | `Chain 2 / Type` | `kappa_light`（5,720 行）；`<空>`（2,089 行）；`lambda_light`（1,960 行）；`light`（535 行）；`heavy`（153 行）；`construct`（4 行） | 第二条链的角色；`heavy`、`light`、`kappa_light`、`lambda_light` 和 `construct` 保留原分类，空值表示未提供。 |

模型使用时最关键的字段关系如下：

| 原始字段（第一行 / 第二行） | 表示、单位与来源 | 缺失与边界 |
| --- | --- | --- |
| Assay ID / IEDB IRI；Reference / IEDB IRI；Epitope / IEDB IRI | curated 记录连接键 | 保留 http/https 原始拼写；后续按字面 ID核对，不靠标题猜连接 |
| Assay / Method、Response measured、Units | 技术、测量对象与单位 | KD、KA、动力学、结构、功能不同量纲，不能合并 |
| Assay / Qualitative Measure、Measurement Inequality、Quantitative measurement | 实验整理标签、删失关系与原始数值字符串 | 空值不是 0；Positive 不保证强 affinity；本快照中的 > / >= 保留 |
| Assay Antibody / Antibody Name、Heavy chain isotype | 抗体注释 | B-cell 表本身没有一对完整 VH/VL 序列列 |
| Complex / PDB ID | 结构连接键 | 共享结构多对一；不是每个 assay 都有结构 |
| Receptor / Group IRI、IEDB Receptor ID、Type | 分组、受体 ID 和 heavy/light 等类型 | group 与 receptor ID 不同，不能互当唯一全抗体 |
| Chain 1/2 / Protein Sequence、Protein IRI | 作者整理链序列及外部 accession | 范围异质、允许缺链，不能宣称所有序列完整 |
| Chain 1/2 / CDR3 Curated、CDR3 Calculated、V Domain Calculated | curated 文献注释 vs 计算派生注释 | 缺失未补齐，不把 calculated 当独立实验 |
| 3D Complex / PDB ID、Antibody PDB Chain 1/2、Antigen PDB Chain(s) | 结构与 author-chain 键 | 全部完整 PDB 另取；不可依据 chain 编号猜角色 |

### 数据示例

B-cell 真实首行：Assay IRI=`http://www.iedb.org/assay/5`，Reference IRI=`http://www.iedb.org/reference/271`，Epitope IRI=`http://www.iedb.org/epitope/77408`，Method=`x-ray crystallography`，Units=`angstroms`，Qualitative Measure=`Positive`，Measurement Inequality=`=`，Quantitative measurement=`3`，Antibody Name=`F9.13.7`，PDB ID=`1FBI`。这是 1FBI 的 3 Å 结构实验记录，不是 3 nM 的 KD。把 quantitative 列统一当 affinity 会把它误标为强 binder。

## PDB 数据库

仅从 B-cell `Complex / PDB ID`、`bcr_3d_assays.csv` 的 `PDB ID` 以及 BCR 的字面 PDB-chain `Protein IRI` 接受锚点。TCR/MHC 专属结构不计入 BCR 覆盖。`B Cell Assay IRI`、`IEDB Receptor ID`、`Epitope IRI` 和原表 author-chain 字段保留多对多连接关系；同一结构只下载一对文件。B-cell 表和 3D/BCR 表的锚点集并不完全一致，已取并集。

获取日期为 2026-09-18。一手入口为 RCSB 的 `https://www.rcsb.org/fasta/entry/<PDB_ID>/download` 与 `https://files.rcsb.org/download/<PDB_ID>.cif.gz`。复用共享缓存时保留其原始 `.cif` 或 `.cif.gz` 字节；缓存未通过身份检查时重新获取。保存完整条目的全部 polymer entities 和完整坐标，不筛链、不拼接变体序列。验证 entry ID、FASTA entity ID、canonical 序列与 mmCIF `_entity_poly.pdbx_seq_one_letter_code_can` 一致，并确认存在原子坐标。

接受 5,517 个唯一 ID，5,515 对通过配对检查，11,030 个已验收文件，共 4.50 GiB（4,831,813,929 bytes）。按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接的 inventory SHA-256：`b1d7c621b91e69081169247bf28d3b0e34f94befb5cb503dd1fa2294a5301518`。PDB 子任务状态为 `partial`。

未取得原始 ID 的完整配对：`4UD3`, `4UDZ`。保留 partial；没有用 successor ID 覆盖原始键。RCSB removed holdings 返回的 supersession 是后续重新核对 construct/chain 的线索，不能直接代替原始结构。

| 原始 PDB ID | removed API 状态 | RCSB 标明的 successor |
| --- | --- | --- |
| 4UD3 | 200 | 5AAM |
| 4UDZ | 200 | 5AAW |

撤销条目 `1OP3`, `1OP5`, `1ZLS`, `1ZLU`, `1ZLV`, `2DTG`, `3J69`, `3J6A`, `3L5Y`, `3RVV`, `3RVW`, `3RVX`, `3SM5`, `3WXV`, `3WXW`, `3X2D`, `4K4M`, `4NX3`, `4PP1`, `4PP2`, `4WGV`, `4WGW`, `5F45`, `9RIT` 使用撤销前的 RCSB 官方 `pdb_seqres` 快照 FASTA 与 wwPDB obsolete mmCIF。保存批量对象身份及逐条原始记录哈希，并要求完整 author-chain 集合和 canonical 序列逐项相等；未用 successor 覆盖原始键，也未从 mmCIF 生成 FASTA。

外部条目中的链角色以 entity 描述和 `_entity_poly.pdbx_strand_id` 核对；这里保存全部链。上游表给出的角色链与具体实验序列仍须逐构建体验证，不能用相同 PDB ID 自动推定所有抗体序列或抗原构建体相同。

## 使用方式

```python
import zipfile
import pandas as pd

with zipfile.ZipFile(dataset_root / "IEDB/bcell_full_v3_single_file.zip") as archive:
    with archive.open("bcell_full_v3.csv") as stream:
        data = pd.read_csv(stream, header=[0, 1], dtype=str)
```

dataset_root 由调用者指定；full XML 中有 78 份格式失败，不能默认整 ZIP 严格解析通过。

## 采集过程记录

1. 2026-09-18，读取官方 export 页面、JS 中的公开 EXPORT_DATA_URL 和 export_data_v3.php 清单，核对 weekly build 与对象 metadata；最初猜 bcell_full_v3.zip 返回 404，改用清单中的 bcell_full_v3_single_file.zip。不是从名称推定访问成功。
2. 默认 requests UA/HEAD 多次返回 403；公开浏览器路由的 GET 使用 Mozilla UA 可正常获取。使用官方 doc 文件 URL，If-Match 保证对象身份；大文件按 16 MiB 精确 ranges 核对 Content-Range，拼接后检查官方大小和本地 SHA-256，小文件可断点续传。没有使用登录、私有 token 或忽略 TLS。
3. 八个 ZIP 逐个清点并完整读取，校验 CRC 和所有 CSV。初次 XML parser 遇到 376.xml 的非法控制字符后中止；修正审计器使其继续检查剩余成员，但保留每一条 parse failure，最终 27,028 有效文档与 78 个失败，raw 未清洗。
4. 单独扫描 B-cell 与 BCR 的连接键、量纲/删失和序列覆盖；核实 B-cell 表 quantitative 的首行是结构分辨率而不是 KD。完整 XML 与 CSV 的格式状态分别记录，未导出一个自造抗体 affinity 表。
5. 扫描 BCR/3D 和 B-cell 字面 PDB 键；先发现 5,376 ID，再补齐 B-cell-only 141 ID，合计 5,517。5,491 个现行条目直接通过 full-entry FASTA/mmCIF 核对；另从 RCSB 官方 `pdb_seqres` 历史快照恢复 24 个 obsolete 原始 ID，逐 author-chain 与 wwPDB obsolete mmCIF 完整比对，未用 successor 覆盖原键。
6. 4UD3 仅在 2015-07-29 至 2015-08-05 有效，4UDZ 仅在 2015-07-29 至 2015-09-30 有效；其有效期没有带 FASTA 的 RCSB 官方快照。wwPDB versioned removed 目录保留原始 mmCIF/PDBML，但没有独立 FASTA 对象；PDBe 官方序列下载对两者明确返回“None of the provided ID's seem to be a valid released IDs”。没有从坐标生成 FASTA 冒充上游原始序列，因此结构子任务停在 5,515/5,517。
7. IEDB 2024 update 正式全文以 2024-11-18 在线发布日期归档；另补充与当前 BCR 字段直接相关的 2026-06-06 bioRxiv v1 全文和 8 页补充 PDF。预印本使用 2026-05-28 导出，其统计不替代本快照统计。
8. 2026-09-24 重新执行八包全量审计、科学口径统计、论文材料和 5,517 个 PDB 锚点检查；同时确认官方滚动导出已经前进到 2026-09-20。保持 9 月 13 日对象集合不变，工作稿同步 staging README 并执行固定 Markdownlint。XML 格式与两个短期原结构 ID 仍有缺口，保留 partial，不执行原子发布。

## 参考文献

- [官方数据库导出说明与许可](https://www.iedb.org/database_export_v3.php)
- [官方当前导出清单](https://www.iedb.org/export_data_v3.php)
- [IEDB 2024 update 原论文](https://doi.org/10.1093/nar/gkae1092)
- [受体数据标准化预印本（bioRxiv v1）](https://doi.org/10.64898/2026.06.03.728549)
- [IEDB 的 BCR/TCR 字段说明](https://discuss.iedb.org/t/tcr-and-bcr-antibody-sequence-data/168)
- [IEDB CoreTrustSeal 申请与运营信息](https://discuss.iedb.org/t/iedb-coretrustseal-approved-application/205)
- [RCSB Data API 文档](https://data.rcsb.org/)，条目引用保留各 PDB 原始结构论文
- [wwPDB 4UD3 版本化 removed 目录](https://files-versioned.wwpdb.org/pdb_versioned/data/removed/ud/pdb_00004ud3/)
- [PDBj 官方 snapshot 保存策略](https://pdbj.org/info/archive?lang=en)

## 其他

### 数据范围和限制

状态为 partial：八个声明 ZIP 均已下载且 CRC/CSV 核验通过，但本次冻结的官方包内有 78 个 XML 严格解析失败；5,517 个原始 PDB 锚点中 5,515 个完整配对，4UD3/4UDZ 的有效期跨不过任何官方 FASTA 快照，PDBe 也明确不交付。IEDB 是滚动 curated 数据库，Complete-study acquisition 不适用于把所有被引用原始研究材料都称为已获得。任何 XML 修复/标准化输出应进入 processed，不覆盖 raw。

### 完整性与验收

| payload | 大小 | SHA-256 |
| --- | --- | --- |
| `IEDB/iedb_export.zip` | 629.59 MiB（660,171,993 bytes） | `05b8146ad9b8f789b7a37b5e4e9cb10e8f77ffe9100d03a7dc260a89cc96579a` |
| `IEDB/bcr_full_v3.zip` | 1.30 MiB（1,360,127 bytes） | `114d849db33b122ee86e3adcf2930c4ad0db418ec8fedcd32288d320dd388ef9` |
| `IEDB/receptor_full_v3.zip` | 10.00 MiB（10,489,109 bytes） | `4ad7389eac65eb316213a968cf5634be3a48712640e11d42a6af5a95309a69bd` |
| `IEDB/iedb_3d_full.zip` | 5.21 MiB（5,465,355 bytes） | `633c1b13301da251eabca81b56d41d54f184ef5d43761bc4ae2e8e1c6929d4f4` |
| `IEDB/antigen_full_v3.zip` | 2.51 MiB（2,631,074 bytes） | `066281603105aedd8fb070a04afee7321a93c85d68e531f2f5ce7a2f6ae47a5e` |
| `IEDB/epitope_full_v3.zip` | 102.40 MiB（107,372,250 bytes） | `af0882317565ff55897f4f0b6b00b3bd94a5f4f06620a6c5acda3a44838e00ba` |
| `IEDB/reference_full_v3.zip` | 3.15 MiB（3,305,818 bytes） | `d12fb9d74c2e89264707dd404081e3443ac10cb7fe91a38ae351fad8b70daf44` |
| `IEDB/bcell_full_v3_single_file.zip` | 86.78 MiB（90,994,458 bytes） | `09b46ff151a356565e9dc6cd18868bf572ff7183e35c06bb3ddbf94676faecf5` |

已取得 payload 共 8 个、840.94 MiB（881,790,184 bytes）；排序拼接的 inventory SHA-256：`29c1857a08898f8ec34d7919d1ca8df25d634ddf6410cc3fa8d8eb09091f1856`。上游未给出 checksum 的交付只将 SHA-256 作为本次字节身份，不能称为官方校验和。归档按成员检查重复/逃逸路径、链接和膨胀范围，逐个读取正规成员；ZIP 校验 CRC，gzip 校验尾部。表格按原始 encoding、header 和列宽检查，保留所有原值。

存在语义或格式验收失败；详见数据结构和采集过程。没有修复 raw 值，也没有把失败对象发布到正式目录。

### 许可和再分发边界

IEDB 导出页面明确数据采用 CC BY 4.0，可在保留适当署名和许可说明的条件下复制、修改和用于商业用途；仍应保留数据库以及原始研究/提交的引用。2024 更新论文文本为 CC BY 4.0，2026 bioRxiv v1 正文和补充材料按其 PMC 记录为 CC0。外部 accession 序列和 PDB 各依对应数据政策。许可范围与数据完整性是两件事：不能据许可补齐缺失序列、统一实验量纲或修复 raw XML。

### 公开范围对照

| 论文或来源声称的内容 | 实际公开文件证据 | 状态 |
| --- | --- | --- |
| B-cell curated assay | 1,692,185 唯一 assay；30,783 非空 quantitative | 包含；标签异质 |
| 可作 KD 的量纲行 | KD/nM 14,503 行，须同时看 inequality/Method | 需 processed 筛选 |
| 所有 BCR 都有完整双链 | 6,745/10,461 行同时有两条 Protein Sequence | 部分且范围异质 |
| 完整 XML 可解析 | 27,028 通过、78 失败，CRC 全通过 | 语义 partial |
| 原始结构锚点全部配对 | 5,515/5,517；24 个 obsolete 已从官方快照恢复 | PDB partial；2 个短期条目缺 FASTA |
| 全量数据库所有表示 | XML + 相关 CSV；未取等价 TSV/MySQL | 选择性公开范围 |

## 待解决问题与处理进展

### Q01 reference XML 格式问题

- 当前判断：八个官方 ZIP 的字节、成员读取和 CRC 均通过；27,106 份 reference XML 中 27,028 份可严格解析，78 份含非法控制字符等上游格式问题。
- 影响范围：CSV 导出和整包字节身份不受影响，但不能声称 full XML 的每个成员都已通过语义解析，也不能把当前 staging 发布为完整验收版本。
- 已完成处理：保留每个失败成员、解析位置和原始哈希；没有删除字符或用容错 parser 把失败伪装为通过。
- 关闭条件：取得 IEDB 更正后的同一口径导出，或在 processed 层建立保留原始成员、修复规则和逐文件 provenance 的可复核转换；raw 不覆盖。

### Q02 原始 PDB FASTA 缺口

- 当前判断：5,517 个结构锚点中 5,515 个已有完整 entry FASTA/mmCIF 配对。`4UD3` 和 `4UDZ` 是存续期很短的撤销条目；wwPDB 保留原始坐标，RCSB 标明 successor，但其有效期没有可用的官方 `pdb_seqres` 快照，PDBe 也不再返回原条目序列。
- 影响范围：两条原始 PDB 键不能满足“独立上游 FASTA + 完整 mmCIF”的结构验收要求；用 successor 或从 mmCIF 自行生成 FASTA 都会改变证据口径。
- 已完成处理：核对 RCSB removed metadata、wwPDB versioned removed 目录、RCSB 历史快照、PDBe 与 PDBj 公开入口；保留 5,515 对已验证文件和两条缺口证据。
- 关闭条件：找到能明确归属于撤销前原条目的官方历史 FASTA，或取得权威来源对原序列、链集合及替代条目关系的可验证说明。
