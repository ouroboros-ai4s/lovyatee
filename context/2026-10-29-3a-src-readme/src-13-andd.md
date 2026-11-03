---
- tags:
  - context
---

# SRC_R13_ANDD 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [原始交付与记录](#原始交付与记录)
  - [字段说明](#字段说明)
  - [数据示例](#数据示例)
- [PDB 数据库](#pdb-数据库)
- [采集过程记录](#采集过程记录)
- [参考文献](#参考文献)
- [其他](#其他)
  - [完整性与验收](#完整性与验收)
  - [许可和再分发边界](#许可和再分发边界)
  - [公开范围对照](#公开范围对照)
- [待解决问题与处理进展](#待解决问题与处理进展)

## 数据集身份

- `source_id`：`SRC_R13_ANDD`
- `source_version`：`snapshot-2026-01-05`
- 原作者或发布机构：Fudan University Human Phenome Institute 的 Yikai Wu 等及论文合作者

### 来源方背景

[复旦大学人类表型组研究院](https://hupi.fudan.edu.cn/53179/list.htm)于 2017 年组建，研究跨尺度表型测量、数据整合与标准化。其官网介绍了覆盖逾 1,000 人、每人测量 24,000 余种表型指标的深度表型队列，以及多组学标准物质“中华家系 1 号”；[复旦大学成果报道](https://hupi.fudan.edu.cn/a0/0a/c53241a761866/page.htm)记录了该标准物质中 8 项获得国家一级标准物质批准。

ANDD 则是另一项跨机构合作：[正式论文](https://pubmed.ncbi.nlm.nih.gov/41723205/)列出该院的 Yikai Wu，以及复旦大学、上海交通大学和默克的合作者。它将不同来源的抗体与纳米抗体信息组织为统一研究资源，展示了团队在多源生物数据整合方面的工作。

## 实验设计和数据口径

ANDD 汇编抗体、VHH、scFv 等序列、结构、抗原和亲和力注释。固定 v2 XLSX 的 Sheet3 实际有 48,800 条非空记录；Predicted_or_Not 中 real 7,294 条、predicted 2,271 条、字面反斜杠 39,235 条。这些是文件标签，不把 real 自动解释成全部合法可比的定量 KD，也不把缺失注释当成阴性。论文报告 48,683 条序列、9,557 个亲和力值，与本表口径有差异。ANTIPASTI 预测亲和力必须和实验值分开。多源再收录、相同序列的不同结构/测量以及构建体差异需要在 processed 层处理。

## 论文原文

- 标题：A Unified Dataset for Antibody and Nanobody Design Including Sequence, Structure, and Binding Affinity Data
- 作者：Yikai Wu；Xuejiao Liu；Karin Hrovatin；Dezhi Wu；Stephanie Linker；Mathias Winkel；Feng Tan
- 发表来源：Scientific Data
- 归档文本版本：正式发表版（出版方 PDF）
- 发布日期：2026-02-21
- DOI：`10.1038/s41597-026-06878-0`
- PMID / PMCID：未在本记录核验 / 未在本记录核验
- 本地文件：`articles/ANDD_2026-02-21_ScientificData-published.pdf`
- 文件大小：2.67 MiB（2,802,744 bytes）
- SHA-256：f388a5dcf1c7038256f82500e979d4d56fa4718edd516dc7eda56b4514062b39
- 文本许可：见出版方原文及 Crossref license URL；未把论文许可移用于数据
- 补充材料：经 19 页正式主文 PDF 检查，未列独立 supplementary information/material 下载文件；其中 supplement 用语描述数据补充。结构、XLSX、字典和质量报告作为 Zenodo payload 保留，不能冒充独立论文附件。
- 引用数（查询快照）：1（[OpenAlex W7130845052](https://openalex.org/W7130845052)，查询于 2026-09-21）

## 仓库内容

来源身份：

- `kind`：`zenodo`
- `record`：`18151718`
- `publication_date`：`2026-01-05`

版本日期来自 Zenodo record 的正式发布日期；正式版本名保留该日期锚点。以下树只展示已下载并验收的上游 payload，不展示项目 README、论文及 PDB 补充。本 source version 以 `partial` 状态正式发布：Zenodo payload 完整，PDB 补充存在下述 6 个不可恢复的原生 FASTA 缺口。

```text
snapshot-2026-01-05/
└── ANDD/
    ├── Data_quality_control_report.pdf
    ├── ANDD_pdb.zip
    ├── Antibody and Nanobody Design Dataset (ANDD)_v2.xlsx
    ├── Data_dictionary.csv
```

## 数据结构

### 原始交付与记录

| 原始文件 / sheet | 非空记录数 | 字段数 | 精确重复行 |
| --- | --- | --- | --- |
| `ANDD/Antibody and Nanobody Design Dataset (ANDD)_v2.xlsx:Sheet3` | 48800 | 49 | 398 |

只统计实际已解析的文件，未把来源介绍规模当作本次落盘统计。

完整 ZIP 有 8,214 个 .pdb 文件（无 AppleDouble）：8,214 个四字符条目名；表格接受 7,785 个 ID。其中 ZIP 独有 642 个、表格独有 213 个，来源锚点并集为 8,427。ZIP 独有条目保持 archive-level 映射，不制造不存在的行级连接。原 ZIP 内容可能是上游处理坐标，canonical 参考不证明其逐链或逐构建体等同。

### 字段说明

Sheet3 有 49 个原样字段。PDB_ID/PDB_ID_Changed 连接 entry；H/L_Chain Entity ID、Asym ID、Auth Asym ID 区分 polymer entity、label chain 和 author chain。Ab/Nano H_Chain AA、Ab/Nano L_Chain AA、Ag_Seq 为来源序列。实际 KD 列以 Affinity_Kd(M), 开头并带条件长说明；∆Gbinding(kJ/mol), 同样带长说明。Predicted_or_Not 的 real/predicted 区分声明来源，Reason_Code 与 Provenance 保存缺失原因和追溯。NA、N/A、unknown 和字面反斜杠须原样保留并单独解释。GB18030 字典的字段名与 XLSX 的空格、大小写、条件后缀并不完全一致。

按语义读取时，可用下表将后列出的 49 个原始表头映射回字段组。表中“文本”指 XLSX 中的字符单元格，`␠` 表示一个 ASCII 空格；ID 或数值列仍须按每格原始类型读取，不把空单元格、`NA`、`N/A`、`unknown` 或字面反斜杠统一转成零。

| 字段组 | 对应原始表头 | 表示、单位与来源 |
| --- | --- | --- |
| 来源与记录状态 | `Source`、`Update_Date`、`Reason_Code`、`Predicted_or_Not`、`Provenance` | 来源/追溯文本、日期及来源方状态标记；`real`、`predicted` 和字面反斜杠保留各自含义 |
| 结构身份 | `PDB_ID`、`PDB_ID_Changed`、`Experimental_Method`、`Structure_Title`、`Complex_Structure`、`Ab_or_Nano`、`Source_Organism` | 条目号、变更标记、方法、题名及构建体分类；PDB 连接为 entry 级，不自动落实到某一条链 |
| 重链、轻链和抗原结构注释 | 所有 `H_Chain␠`、`L_Chain␠`、`Ag_` 前缀列 | entity、label asym、author asym、数据库编号与蛋白名/来源；ID 是结构映射键，不是测量值；`Ag_Seq` 为序列文本 |
| 抗体序列及突变 | 所有 `Ab/Nano` 前缀列、`CDR Nomenclature` | 突变注释、H/L 全序列、六条 CDR 与编号体系；缺失分布见下列逐字段统计 |
| 结合数据 | 以 `Affinity_Kd(M),` 开头的列、以 `∆Gbinding(kJ/mol),` 开头的列、`Affinity_Method` | 来源方汇编的 KD（M）、结合自由能（kJ/mol）及测定方法；预测和实验记录需按 `Predicted_or_Not` 分开 |

实际表头（保留原始字段名）：

- `ANDD/Antibody and Nanobody Design Dataset (ANDD)_v2.xlsx:Sheet3`：`Source`、`Update_Date`、`PDB_ID`、`PDB_ID_Changed`、`Experimental_Method`、`Structure_Title`、`Complex_Structure`、`Ab_or_Nano`、`Source_Organism`、`H_Chain Entity ID`、`H_Chain Asym ID`、`H_Chain Auth Asym ID`、`H_Chain Database Name`、`H_Chain Accession Code(s)`、`H_Chain Sequence Cluster ID`、`H_Chain Sequence Cluster Identity Threshold`、`H_Chain Macromolecule Name`、`L_Chain Entity ID`、`L_Chain Asym ID`、`L_Chain Auth Asym ID`、`L_Chain Database Name`、`L_Chain Accession Code(s)`、`L_Chain Sequence Cluster ID`、`L_Chain Sequence Cluster Identity Threshold`、`L_Chain Macromolecule Name`、`Ag_Entity ID`、`Ag_Asym ID`、`Ag_Auth Asym ID`、`Ag_Database Name`、`Ag_Accession Code(s)`、`Ag_Name`、`Ag_Seq`、`Ag_Source Organism`、`Ab/Nano_Mutation`、`Ab/Nano H_Chain AA`、`Ab/Nano L_Chain AA`、`Ab/Nano_CDR H1`、`Ab/Nano_CDR H2`、`Ab/Nano_CDR H3`、`Ab/Nano_CDR L1`、`Ab/Nano_CDR L2`、`Ab/Nano_CDR L3`、`CDR Nomenclature`、`Affinity_Kd(M), (the near-physiological conditions, with controlled temperatures (20-25 °C or 37 °C) and buffered aqueous systems)`、`∆Gbinding(kJ/mol),(the near-equilibrium conditions at constant temperatures (20-25 °C) )`、`Affinity_Method`、`Reason_Code`、`Predicted_or_Not`、`Provenance`

字段原始表示与缺失统计（只统计审计解析结果，不在 raw 中填零）：

- `ANDD/Antibody and Nanobody Design Dataset (ANDD)_v2.xlsx:Sheet3`：缺失/特殊表示计数 `{"Ag_Entity ID": 31005, "Ag_Asym ID": 31005, "Ag_Auth Asym ID": 31007, "Ag_Database Name": 34737, "Ag_Accession Code(s)": 34737, "Ag_Name": 36326, "Ag_Seq": 36183, "Ab/Nano_CDR H3": 13716, "Affinity_Kd(M), (the near-physiological conditions, with controlled temperatures (20-25 °C or 37 °C) and buffered aqueous systems)": 40758, "∆Gbinding(kJ/mol),(the near-equilibrium conditions at constant temperatures (20-25 °C) )": 45918, "Affinity_Method": 46349, "Predicted_or_Not": 39235, "Update_Date": 8381, "Ab/Nano_CDR H1": 11480, "Ab/Nano_CDR H2": 11454, "Ab/Nano_CDR L1": 38491, "Ab/Nano_CDR L2": 38496, "Ab/Nano_CDR L3": 38491, "CDR Nomenclature": 9730, "Reason_Code": 9565, "H_Chain Database Name": 45596, "H_Chain Accession Code(s)": 45596, "H_Chain Entity ID": 26996, "H_Chain Asym ID": 26992, "H_Chain Auth Asym ID": 26992, "H_Chain Sequence Cluster ID": 29619, "H_Chain Sequence Cluster Identity Threshold": 29619, "H_Chain Macromolecule Name": 29615, "Ab/Nano H_Chain AA": 360, "L_Chain Database Name": 45397, "L_Chain Accession Code(s)": 45397, "L_Chain Entity ID": 32477, "L_Chain Asym ID": 32477, "L_Chain Auth Asym ID": 32477, "L_Chain Sequence Cluster ID": 32481, "L_Chain Sequence Cluster Identity Threshold": 32481, "L_Chain Macromolecule Name": 32477, "Ab/Nano L_Chain AA": 31435, "PDB_ID": 27952, "PDB_ID_Changed": 27952, "Experimental_Method": 23225, "Structure_Title": 23642}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

### 数据示例

来自 `ANDD/Antibody and Nanobody Design Dataset (ANDD)_v2.xlsx:Sheet3` 的第一条真实记录；这里只摘录字段，不改写原始文件。

| 字段 | 原样值 |
| --- | --- |
| `Source` | `abYbank_ab` |
| `Update_Date` | `2024-09-16 00:00:00` |
| `PDB_ID` | `12E8` |
| `PDB_ID_Changed` | `No` |
| `Experimental_Method` | `X-RAY DIFFRACTION` |
| `Structure_Title` | `2E8 FAB FRAGMENT` |
| `Complex_Structure` | `True` |

每行按该来源的测量、配对或结构实例口径解释，不把结构表示或 replicate 当作新实验。完整字段保留在 payload 中。

## PDB 数据库

Sheet3 PDB_ID/PDB_ID_Changed; source columns provide entity IDs, label asym and author asym IDs. Canonical entry files are not predicted mutant or generated structures. Also include exact four-character accession filenames from the fully verified All_structures ZIP; archive-only entries remain archive-level references, not invented row mappings. Official removed-holdings API confirms 53 obsolete/superseded original accessions; original IDs are retained. Preserve obsolete full coordinates and literal historical RCSB SEQRES records only when full author-chain coverage and exact full-polymer canonical equality pass. Current replacements are separate references, not substitutes for the original entry.

当前接受锚点清单为 8427 个。完整 mmCIF 覆盖 8427/8427，原生 FASTA 覆盖 8421/8427；只有这 8421 个两层完整锚点可视为同时具备 FASTA 与 mmCIF。缺少原生 FASTA 的原 accession 为 `5USI`、`6CSY`、`6ERX`、`7KGL`、`7N01`、`7N0S`。每个锚点取原样 RCSB FASTA 和完整 mmCIF，不嫁接 CDR、不生成逐变体重建序列。原始 header 保留不改写；现行接口提供 polymer entity/chain 注释，历史 SEQRES 提供 author chain、mol 和 length。原始 mol:na 核酸记录同样全序列核对；不猜测伙伴角色。

六个原条目的 superseded replacement 分别为 `5USI`→`6B9J`、`6CSY`→`6MXT`、`6ERX`→`6FXN`、`7KGL`→`7MFV`、`7N01`→`7RW2`、`7N0S`→`7R98`。replacement 只记录上游替代关系，不是原 accession 的原生序列替代品，也不计入原条目的 FASTA 覆盖。

PDB 文件审计摘要：16848 个文件，10.82 GiB（11,612,715,809 bytes）；inventory SHA-256：`adf2b439d11a905e65bbfcb3fff4f4ede450116eb07aeb4f8a4db258d4559a51`。摘要按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接计算。缓存最初包含选择链/重写 header 的 FASTA，已清理本轮这类 staging 副本；现在只接受 RCSB 原始 header 和字面完整序列。

obsolete/superseded 条目的历史原始序列例外：从已验收的 RCSB SEQRES 历史归档复制该 entry 的全部字面记录，保留原始 header、换行和序列字节。以完整 obsolete mmCIF 的明确 author-chain 集合及 canonical 全序列逐链核对，缺链、重复链、长度或序列不一致均不通过，不从坐标生成 FASTA。上述 per-entry/entity header 描述适用于现行端点文件，历史记录保留 RCSB 的 chain/molecule/length header。归档来源：<https://raw.githubusercontent.com/piercelab/antibody_benchmark/e788056bbedb4be83fa1f934feb2007ffb18ec59/scripts/example/pdb_seqres_8_2020.fa.tar.gz>；归档 SHA-256 `fcfac4ddc495b81da23e9f25b1adddf448f3dd10316c7eefa4dd769434a47aae`；成员 `pdb_seqres_8_2020.fa` 为 174.72 MiB（183,211,395 bytes）。

官方 RCSB 不可变历史快照按 S3 原始 size、单段或多段 ETag、完整 gzip CRC/trailer 验收。每个补入 entry 的全部字面记录必须与所选完整原始 entry 坐标逐链一致；不以替代条目补序列。快照身份：

- `20140102`：<https://pdbsnapshots.s3.amazonaws.com/20140102/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 14.84 MiB（15,565,148 bytes）；SHA-256 `be704831421a521ba30f1031e00365440cccfe52b520df39c2ec3b079b7e72ff`。
- `20141203`：<https://pdbsnapshots.s3.amazonaws.com/20141203/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 16.40 MiB（17,195,910 bytes）；SHA-256 `656c638c8901173b215a7637758b4fb1340bd2a23b251d806423a075b1e67ad4`。
- `20150102`：<https://pdbsnapshots.s3.amazonaws.com/20150102/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 16.39 MiB（17,186,552 bytes）；SHA-256 `d26a246aabec43bca0c683335cc17c7a6573e0ad7376ffc192b44ab12c32f772`。
- `20160101`：<https://pdbsnapshots.s3.amazonaws.com/20160101/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 18.23 MiB（19,114,411 bytes）；SHA-256 `63c54b5369af7b7ee1f66426f7d08dd4d12572c7cf939c5992a18cb872c2349b`。
- `20170101`：<https://pdbsnapshots.s3.amazonaws.com/20170101/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 20.58 MiB（21,575,551 bytes）；SHA-256 `9ad80eabc633433217993db4dc52a2ca85b550ca619ab7c47be42891a0512785`。
- `20170710`：<https://pdbsnapshots.s3.amazonaws.com/20170710/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 21.86 MiB（22,917,231 bytes）；SHA-256 `4d31f2245b95b6c3104c6b6d28caf20f954cb5a3dee7f5a7d8be5eae9b0f379f`。
- `20180101`：<https://pdbsnapshots.s3.amazonaws.com/20180101/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 23.01 MiB（24,130,308 bytes）；SHA-256 `c973a526c30de771837fccdf45cde35dcff6464c73849343a09bb38295d33994`。
- `20190101`：<https://pdbsnapshots.s3.amazonaws.com/20190101/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 25.61 MiB（26,857,360 bytes）；SHA-256 `055a10bd392391156a0a88bcc5cda5e1f3674e415977c417901dd2713bf2b827`。
- `20200722`：<https://pdbsnapshots.s3.amazonaws.com/20200722/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 30.30 MiB（31,768,833 bytes）；SHA-256 `9be6c03243187f2ecbdaa68f7262b1d69de85ce36ea5a4a729e137e3807e59b7`。
- `20210105`：<https://pdbsnapshots.s3.amazonaws.com/20210105/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 32.59 MiB（34,177,430 bytes）；SHA-256 `567ceb743a5ec6da30bc5c95a1462993c781adca7dfce737df889a249d5eaeaa`。
- `20230102`：<https://pdbsnapshots.s3.amazonaws.com/20230102/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 41.51 MiB（43,523,160 bytes）；SHA-256 `9c9b08fa5ad62e015d4331bd0124f35e04a31119a29ab388de381aa206f54120`。
- `20240101`：<https://pdbsnapshots.s3.amazonaws.com/20240101/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 46.62 MiB（48,889,608 bytes）；SHA-256 `91d0291d19dab4ab66f79ee4fad99c94ca190c27d87d3427182c5ed084d1c03a`。

`4OZ4` 使用同一官方 `20210105` 历史版本的全链 native FASTA 与完整 mmCIF，二者全 canonical 序列一致。坐标来自 <https://pdbsnapshots.s3.amazonaws.com/20210105/pub/pdb/data/structures/divided/mmCIF/oz/4oz4.cif.gz>；完整 CIF SHA-256 `c5d8a46a94e8ce1a706f15e125009bbb0ac62afce15dbd694336bbf5500a89d4`；FASTA SHA-256 `eb61e8d9a0e395fa2ab1bd00dd1ada7dc089049b93b657bc41306a3211b68d4f`。较晚 obsolete 坐标与历史序列有差异，其原文件与 hash 保留在 cache，未修改历史字节或宣称采用了较晚 canonical 修订。

## 采集过程记录

2026-09-18：读取项目规范和执行清单，解析一手 API/tree/Drive 对象 metadata，固定本轮版本与文件身份。下载到共享 source 下 `.staging/<version>.partial`；HTTP 大文件使用精确 byte range 和全文件上游 checksum，Drive 保留对象 ID、MIME 与字节数，失败部分可续传。2026-09-18 按用户要求调整本轮 HTTP 为直连优先、连接失败回退环境代理，15 分钟后重试直连；各线程复用连接且保留 TLS/CA 校验。重启任务保留所有文件断点。

独立 audit 重新计算 hash、完整解析已取得表格并检查 PDB 两层文件；归档只有完成逐成员/CRC 与路径安全检查后才通过。PMC 访问被拒绝、非 OA XML 不可得和间歇代理连接失败均保留缺口，未关闭 TLS 验证。PDB 缓存原始性检查发现错误后清理本轮衍生 header 文件并重做。

README 草稿每次写入后立即同步到 staging 同名文件，随后运行 skill 固定 Markdownlint 配置。2026-09-20 经用户明确批准，以 `partial` 状态原子发布 `snapshot-2026-01-05`；该状态只表示 Zenodo payload 已完整验收并正式落盘，不表示 PDB 覆盖完整，也不表示完整研究底层数据已经取得。

2026-09-18：主文从 `ANDD_s41597-026-06878-0.pdf` 改名为 `ANDD_2026-02-21_ScientificData-published.pdf`，日期取该论文版本发布日期，改名前后大小和 SHA-256 一致。

2026-09-18：旧 staging 名 `zenodo-18151718` 不符合版本规则，改为 `snapshot-2026-01-05`。先停止本来源写入，逐文件核对大小与 SHA-256 后原子重命名，再同步配置并恢复管理器；record ID 仅作来源身份。

2026-09-18 继续补齐：官方 RCSB historical S3 snapshots 按原始 size、单段/多段 ETag、完整 gzip CRC/trailer 验收，字面记录与原始全坐标逐链全序列核对，累计补齐47/53个obsolete/superseded 原始条目。4OZ4 较晚 obsolete canonical 序列与历史 SEQRES 有 E/Q 差异，未替换或推断残基；从同一官方20210105快照取得完整 original4OZ4 CIF及全部原始FASTA，二者一致，较晚CIF留cache。剩余6项的 released→removed 时间分别为5USI2017-09-20→2017-11-22、6CSY2018-10-24→2018-11-14、6ERX2018-01-31→2018-04-04、7KGL2021-02-03→2021-06-02、7N012021-08-04→2021-09-01、7N0S2021-06-09→2021-07-07；没有可用年度 SEQRES 快照覆盖，20180321特殊快照无derived_data序列对象，现行polymer_entity API逐一404。替代ID只作已有独立参考，不覆盖原始缺口。 2026-09-19再次枚举官方pdbsnapshots S3根目录全部33个日期前缀；没有任何快照落在这6项各自released→removed窗口内，故不是遗漏了可用快照。现有完整坐标/PDBML不转换为FASTA。 官方obsolete mmCIF的OBSLTE记录给出替代关系：5USI→6B9J、6CSY→6MXT、6ERX→6FXN、7KGL→7MFV、7N01→7RW2、7N0S→7R98。前五项details字段为未知值`?`；7N01只注明Replaced by 7RW2/EMD-24708，也没有给出科学或技术原因。wwPDB术语为obsolete/superseded，不表述为彻底withdrawn。

2026-09-22 按最新版字段要求复核 Sheet3 的 49 个原始表头并补充语义分组；Zenodo 四个 payload 文件的 MD5 与既存官方清单一致，`pdb/` 的 16,848 个文件重新逐项计算 inventory SHA-256，与本文记录一致。六个 obsolete 原条目的 FASTA 缺口仍在，未改变 `partial` 状态。

2026-10-09：复核新版动态待办与论文附件范围；修正公开范围表中沿用的“额外补充待核验”旧状态。六个原生 FASTA 缺口、论文与 Zenodo 原件以及结构文件均未改动。

2026-10-09：为 `Q02` 直接读取固定 v2 XLSX `Sheet3` 的 48,800 个数据行，按原样 `NA` 判断两列亲和力有值情况：仅 KD 6,683 行、仅 ΔG 1,523 行、两者都有 1,359 行、两者均无 39,235 行。亲和力并集为 9,565 行，较论文 9,557 多 8；整行完全去重为 48,402 行，仍不能解释论文 48,683 条序列。没有改变原始文件或推定筛选规则，差额保留在动态待办。

## 参考文献

- <https://www.nature.com/articles/s41597-026-06878-0.pdf>
- <https://doi.org/10.1038/s41597-026-06878-0>
- <https://zenodo.org/records/18151718>
- <https://www.rcsb.org/>
- <https://data.rcsb.org/rest/v1/holdings/removed/1OM3>
- <https://data.rcsb.org/rest/v1/holdings/removed/1OP3>
- <https://data.rcsb.org/rest/v1/holdings/removed/1OP5>
- <https://data.rcsb.org/rest/v1/holdings/removed/1ZLS>
- <https://data.rcsb.org/rest/v1/holdings/removed/1ZLU>
- <https://data.rcsb.org/rest/v1/holdings/removed/1ZLV>
- <https://data.rcsb.org/rest/v1/holdings/removed/1ZLW>
- <https://data.rcsb.org/rest/v1/holdings/removed/2F5A>
- <https://data.rcsb.org/rest/v1/holdings/removed/3J69>
- <https://data.rcsb.org/rest/v1/holdings/removed/3J6A>
- <https://data.rcsb.org/rest/v1/holdings/removed/3L5Y>
- <https://data.rcsb.org/rest/v1/holdings/removed/3LOH>
- <https://data.rcsb.org/rest/v1/holdings/removed/3QOS>
- <https://data.rcsb.org/rest/v1/holdings/removed/3QOT>
- <https://data.rcsb.org/rest/v1/holdings/removed/3RVV>
- <https://data.rcsb.org/rest/v1/holdings/removed/3RVW>
- <https://data.rcsb.org/rest/v1/holdings/removed/3RVX>
- <https://data.rcsb.org/rest/v1/holdings/removed/3SM5>
- <https://data.rcsb.org/rest/v1/holdings/removed/3W14>
- <https://data.rcsb.org/rest/v1/holdings/removed/3WXV>
- <https://data.rcsb.org/rest/v1/holdings/removed/3WXW>
- <https://data.rcsb.org/rest/v1/holdings/removed/4K4M>
- <https://data.rcsb.org/rest/v1/holdings/removed/4NX3>
- <https://data.rcsb.org/rest/v1/holdings/removed/4OZ4>
- <https://data.rcsb.org/rest/v1/holdings/removed/4PP1>
- <https://data.rcsb.org/rest/v1/holdings/removed/4PP2>
- <https://data.rcsb.org/rest/v1/holdings/removed/4Q5Z>
- <https://data.rcsb.org/rest/v1/holdings/removed/4WGV>
- <https://data.rcsb.org/rest/v1/holdings/removed/4WGW>
- <https://data.rcsb.org/rest/v1/holdings/removed/4X4Y>
- <https://data.rcsb.org/rest/v1/holdings/removed/5B3C>
- <https://data.rcsb.org/rest/v1/holdings/removed/5E99>
- <https://data.rcsb.org/rest/v1/holdings/removed/5F45>
- <https://data.rcsb.org/rest/v1/holdings/removed/5KMV>
- <https://data.rcsb.org/rest/v1/holdings/removed/5KNA>
- <https://data.rcsb.org/rest/v1/holdings/removed/5USI>
- <https://data.rcsb.org/rest/v1/holdings/removed/5UWE>
- <https://data.rcsb.org/rest/v1/holdings/removed/6CSY>
- <https://data.rcsb.org/rest/v1/holdings/removed/6ERX>
- <https://data.rcsb.org/rest/v1/holdings/removed/6F5G>
- <https://data.rcsb.org/rest/v1/holdings/removed/6H7K>
- <https://data.rcsb.org/rest/v1/holdings/removed/6MF7>
- <https://data.rcsb.org/rest/v1/holdings/removed/6NUY>
- <https://data.rcsb.org/rest/v1/holdings/removed/6NUZ>
- <https://data.rcsb.org/rest/v1/holdings/removed/6NV0>
- <https://data.rcsb.org/rest/v1/holdings/removed/7EVW>
- <https://data.rcsb.org/rest/v1/holdings/removed/7KGL>
- <https://data.rcsb.org/rest/v1/holdings/removed/7N01>
- <https://data.rcsb.org/rest/v1/holdings/removed/7N0S>
- <https://data.rcsb.org/rest/v1/holdings/removed/7NY5>
- <https://data.rcsb.org/rest/v1/holdings/removed/7SIX>
- <https://data.rcsb.org/rest/v1/holdings/removed/7XOX>
- <https://data.rcsb.org/rest/v1/holdings/removed/8BPK>
- <https://pdbsnapshots.s3.amazonaws.com/20140102/pub/pdb/derived_data/pdb_seqres.txt.gz>
- <https://pdbsnapshots.s3.amazonaws.com/20141203/pub/pdb/derived_data/pdb_seqres.txt.gz>
- <https://pdbsnapshots.s3.amazonaws.com/20150102/pub/pdb/derived_data/pdb_seqres.txt.gz>
- <https://pdbsnapshots.s3.amazonaws.com/20160101/pub/pdb/derived_data/pdb_seqres.txt.gz>
- <https://pdbsnapshots.s3.amazonaws.com/20170101/pub/pdb/derived_data/pdb_seqres.txt.gz>
- <https://pdbsnapshots.s3.amazonaws.com/20170710/pub/pdb/derived_data/pdb_seqres.txt.gz>
- <https://pdbsnapshots.s3.amazonaws.com/20180101/pub/pdb/derived_data/pdb_seqres.txt.gz>
- <https://pdbsnapshots.s3.amazonaws.com/20190101/pub/pdb/derived_data/pdb_seqres.txt.gz>
- <https://pdbsnapshots.s3.amazonaws.com/20200722/pub/pdb/derived_data/pdb_seqres.txt.gz>
- <https://pdbsnapshots.s3.amazonaws.com/20210105/pub/pdb/derived_data/pdb_seqres.txt.gz>
- <https://pdbsnapshots.s3.amazonaws.com/20230102/pub/pdb/derived_data/pdb_seqres.txt.gz>
- <https://pdbsnapshots.s3.amazonaws.com/20240101/pub/pdb/derived_data/pdb_seqres.txt.gz>

## 其他

### 完整性与验收

上游声明 4 个文件；最近审计通过 4 个，待取得/核验 0 个。

本 source version 已以 `partial` 状态正式发布。Zenodo 声明的 4 个 payload 文件全部通过官方 MD5 与字节数核验；PDB 子任务为 8421/8427 个 FASTA+mmCIF 双层完整锚点。不得将本发布描述为 verified complete PDB coverage 或 complete-study acquisition。没有独立 manifest/API 响应/审计 JSON 发布在 source version 中；临时产物只保存在共享 cache。

逐项审阅尚未解决的缺口：

- 六个 obsolete/superseded 原条目仍缺少字面完整原生序列：`5USI`、`6CSY`、`6ERX`、`7KGL`、`7N01`、`7N0S`。现行 RCSB entry/FASTA 与 polymer-entity API 均不再保留这些原序列；官方 pdbsnapshots S3 全部日期中没有快照落入各条目的 released-to-removed 窗口，特殊 `20180321` 快照也没有 derived_data SEQRES 对象。一手入口已穷尽，现有来源无法恢复这六条原生序列；后续需等待新的上游一手来源。不得从坐标/PDBML 推导 FASTA，也不得用 replacement 序列冒充原 accession。

### 许可和再分发边界

Zenodo v2 标为 CC BY 4.0；论文也需保留其引用。汇编中 PDBbind、专利和其他上游来源的许可不能用该标签直接替代。

### 公开范围对照

| 目标组成 | 当前证据 | 状态 |
| --- | --- | --- |
| 固定上游 payload | Zenodo 官方 MD5、大小与独立文件/格式审计 | 4/4 完成并正式发布 |
| 论文原文 | 正式主文 PDF 已归档；19 页正文未列独立论文附件 | 本次论文范围已核对；Zenodo 字典和质量报告按数据 payload 另计 |
| PDB 原始序列与全坐标 | 接受锚点两层配对审计 | partial：mmCIF 8427/8427，原生 FASTA 8421/8427；6 项为上游不可恢复缺口 |
| 完整研究底层数据 | 当前公开范围限于汇编或处理包；底层实验材料未全部取得 | 未宣称获得 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-22；等待上游原生序列）：8,427 个接受锚点的完整 mmCIF 已取得，`5USI`、`6CSY`、`6ERX`、`7KGL`、`7N01`、`7N0S` 六个 obsolete/superseded 原条目仍缺原生 FASTA。已核对 RCSB 当前接口、官方历史快照和替代条目关系；现有一手来源不能恢复原 accession 的原生序列。本版本保持 `partial`，仅将 8,421 个锚点计为双层完整；后续若出现可信历史归档，再按原始全链与坐标逐一验收。
- `Q02`（最近更新：2026-10-09；待口径核对）：固定 v2 Sheet3 有 48,800 条记录，论文报道 48,683 条序列和 9,557 个亲和力值。独立逐格重算：KD 非 `NA` 为 8,042 行，ΔG 非 `NA` 为 2,882 行，两列交集 1,359 行，并集 9,565 行，比论文数多 8；整行完全去重后为 48,402 行，也不等于论文序列数。当前按原表保留记录、序列及两类亲和力字段，不强行统一口径。取得论文所用版本和筛选/去重规则，复算至 48,683 与 9,557 后关闭。
- `Q03`（最近更新：2026-09-22；待逐来源权利核验）：Zenodo v2 标为 CC BY 4.0，但表中还包含 PDBbind、专利及其他来源的再汇编记录。已保留来源字段和 Zenodo 许可声明；商业训练或对外发布子集前，应按拟使用记录核对原始来源的再利用条件，不能仅以 Zenodo 总标签替代逐来源判断。
