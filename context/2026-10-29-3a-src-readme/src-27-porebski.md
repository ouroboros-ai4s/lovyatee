# SRC_R27_POREBSKI 数据说明

- [数据集身份](#数据集身份)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [原始交付与记录粒度](#原始交付与记录粒度)
  - [论文交付数据表](#论文交付数据表)
  - [字段说明](#字段说明)
  - [数据示例](#数据示例)
- [PDB 数据库](#pdb-数据库)
- [使用方式](#使用方式)
- [采集过程记录](#采集过程记录)
- [参考文献](#参考文献)
- [其他](#其他)
  - [完整性与验收](#完整性与验收)
  - [许可和再分发边界](#许可和再分发边界)
  - [公开范围对照](#公开范围对照)

## 数据集身份

- `source_id`：`SRC_R27_POREBSKI`
- `source_version`：`snapshot-2023-11-14`
- 原作者或发布机构：Bruno T. Porebski 等；Holliger group / 合作者

## 实验设计和数据口径

研究对 HEL VHH、IL7 scFv 和 HER2 scFv 文库进行 ribosome display / affinity screening，深度测序并按筛选过程处理，再用小规模表达与 BLI 测量验证候选，训练模型并发布 checkpoint。公开 TAR 是处理后训练/分析数据，不等于全部底层实验原始文件。

筛选/测序派生分数、计数和富集是条件相关的代理标签；BLI 候选 KD 是另一测量层，不能将少量验证值推广到全库。不同抗原/亲本、筛选轮次与重复以及序列共享会造成泄漏。论文补充含 oligo 和候选表，源数据 XLSX 中的失败/未测/特殊编码保持原样，不变成零。公开包行数、论文文库规模与独立抗体规模分别报告。 实际处理包五表合计8796184条条形码记录：HER2 ml=2688992、affmat=297655，HEL MACS=2980379、FACS=442085，IL7=2387073。每表barcode唯一，但同一read片段重复出现；HER2 ml中只有199741条唯一read 1，不能把8796184行当独立抗体。

## 论文原文

- 标题：Rapid discovery of high-affinity antibodies via massively parallel sequencing, ribosome display and affinity screening.
- 作者：Porebski BT, Balmforth M, Browne G, Riley A, Jamali K, Fürst MJLJ, Velic M, Buchanan A, Minter R, Vaughan T, Holliger P.
- 载体与版本：Nat Biomed Eng
- 发布日期：2023-10-09
- DOI：10.1038/s41551-023-01093-3
- PMID / PMCID：37814006 / PMC10963267
- 本地文件：`articles/POREBSKI_2023-10-09_EuropePMC-published.xml`
- 文件大小：POREBSKI_2023-10-09_EuropePMC-published.xml：276710 bytes
- SHA-256：POREBSKI_2023-10-09_EuropePMC-published.xml：`8b8bb30d63c441bd70540f32ef19b7f652f6cb15f4a725cec896a5544f312e20`
- 文本许可：CC BY 4.0
- 补充材料：已归档 5 个文件。

| 本地文件 | 角色 | bytes | SHA-256 |
| --- | --- | --- | --- |
| `articles/POREBSKI_2023-10-09_NatureBiomedicalEngineering-published-supplement-1.pdf` | Supplementary Information (download PDF ) | 5631062 | `b4701b2fe063897823c8839f67d1f9cc4a9823bdc35dd3099e6c078f819aa965` |
| `articles/POREBSKI_2023-10-09_NatureBiomedicalEngineering-published-supplement-2.pdf` | Reporting Summary (download PDF ) | 106468 | `71f4497d9d38c5abce6ec43ba510064d9c84a0874a6b78766e7b35ec2ddef303` |
| `articles/POREBSKI_2023-10-09_NatureBiomedicalEngineering-published-supplement-3.csv` | Supplementary Data 1 (download CSV ) | 878800 | `28ee75812505a4302b0262572927d23463939821857486b830917817c896df92` |
| `articles/POREBSKI_2023-10-09_NatureBiomedicalEngineering-published-supplement-4.xlsx` | Source Data Figs. 2–5 and Extended Data Figs. 1 and 3 (download XLSX ) | 44620 | `d101ed5c82619e6bc3764c18fc8351253f69f42d9f7c335b7904bd2eb72e0e4d` |
| `articles/POREBSKI_2023-10-09_NatureBiomedicalEngineering-published-supplement-5.xlsx` | Source Data Extended Data Fig. 1 (download XLSX ) | 14064 | `1e8249fd092f49f16d763160fbdcdd60ddf0c6bf11efc327b6ee9706b2d4b7f0` |

未取得的文件：primary PDF。已取得的 XML 是一手完整正文，不声称已取得 PDF。

## 仓库内容

- 一手入口：<https://zenodo.org/records/10123621>；record `10123621`；上游日期 2023-10-09。

全部三个公开 Zenodo 文件和公开论文补充；论文称体积过大的底层原始实验数据需向作者合理申请，本次未取得该受限部分，也未发送申请。

上游未给整个数据交付包提供正式版本名；`snapshot-2023-11-14` 取自固定 Zenodo record 10123621 的 `created=2023-11-14T10:04:43.096030+00:00`，表示这条具体版本记录的创建日期。元数据 `publication_date=2023-10-09` 另行保留，不与该日期混用；不使用本次下载日期。原交付归档保持压缩格式，验收时读取所有成员，不在 raw 中重新生成数据表。

```text
snapshot-2023-11-14/
  porebski/
    checkpoint-bsf24_bert_base-epoch=00-val_loss=0.13.ckpt
    porebski_et_al_2023_datasets.tar.gz
    LICENSE.md
```

## 数据结构

### 原始交付与记录粒度

Zenodo 正式交付：porebski_et_al_2023_datasets.tar.gz、checkpoint-bsf24_bert_base-epoch=00-val_loss=0.13.ckpt 和 LICENSE.md；模型为计算产物，不执行 pickle/训练加载。补充 CSV 原始字段是 CDR_VH3_prot_seq、lib、seed、hd（CDRH3 设计序列/文库/亲本/距离），XLSX 是候选测量与 Sanger CDR 证据，保留原文表头/多段布局。 公开TAR实际含5个CSV：HEL MACS/FACS、IL7 和 HER2 affmat/ml 库，字段 barcode、read 1（有的另含 read 2/read 3）及 intensity 0…N。read字段是翻译后的局部片段（可能含`*`终止标记），不是全长抗体；intensity索引未在表头编码浓度/步骤，不能按序号猜assay条件。

| 原始表或 sheet | 非空数据行 | 列数 |
| --- | --- | --- |
| `porebski/porebski_et_al_2023_datasets.tar.gz!porebski_et_al_2023_datasets/3.HER2_scFv/fc081_fc082_her2_ml_lib_paired_translated.csv` | 2688992 | 16 |
| `porebski/porebski_et_al_2023_datasets.tar.gz!porebski_et_al_2023_datasets/3.HER2_scFv/fc079_fc080_her2_affmat_paired_translated.csv` | 297655 | 17 |
| `porebski/porebski_et_al_2023_datasets.tar.gz!porebski_et_al_2023_datasets/1.HEL_Nb/fc071_hs065_r3_macs_paired_avg_translated.csv` | 2980379 | 16 |
| `porebski/porebski_et_al_2023_datasets.tar.gz!porebski_et_al_2023_datasets/1.HEL_Nb/fc069_fc070_r3_facs_paired_translated.csv` | 442085 | 18 |
| `porebski/porebski_et_al_2023_datasets.tar.gz!porebski_et_al_2023_datasets/2.IL7_scFv/fc059_hs064_il7_paired_translated.csv` | 2387073 | 8 |

### 论文交付数据表

以下是实际归档补充数据的原始工作表/CSV；工作表计数包括表头、注释与多段布局，不是独立样本数。公式保留原字符串，未重算；展示第一条非空原始行便于识别入口，标题行不能误作科学表头。

| 补充数据工作表 | 非空行（含表头/注释） | 首条原始行 / 公式单元格 / 特殊码 |
| --- | --- | --- |
| `articles/POREBSKI_2023-10-09_NatureBiomedicalEngineering-published-supplement-4.xlsx#Nb _HEL` | 40 | Deep Screening, Octet / 0 / {} |
| `articles/POREBSKI_2023-10-09_NatureBiomedicalEngineering-published-supplement-4.xlsx#scFv_IL7` | 22 | Deep Screening, Octet, Expression, Purification, Inhibition assay / 20 / {} |
| `articles/POREBSKI_2023-10-09_NatureBiomedicalEngineering-published-supplement-4.xlsx#scFv_Her2` | 32 | Deep Screening, Published SPR kinetics, Octet (this paper), SPR, Octet, Expression, Purification / 48 / {} |
| `articles/POREBSKI_2023-10-09_NatureBiomedicalEngineering-published-supplement-5.xlsx#Sheet1` | 87 | Clone ID, CDR1 nt, CDR2 nt, CDR3 nt, CDR1 prot, CDR2 prot, CDR3 prot / 0 / {} |

| 补充数据表 | parser 行数 | 首行原始内容（须按具体布局读） |
| --- | --- | --- |
| `articles/POREBSKI_2023-10-09_NatureBiomedicalEngineering-published-supplement-3.csv` | 25039 | CDR_VH3_prot_seq, lib, seed, hd |

表行数包含重复条件、示例和派生副本，不求和作为独立生物对象。下表列名保持原始拼写；空表头以 `（空列名）` 标出，未修改文件。

### 字段说明

序列/抗原/轮次字段：对象与实验条件；counts、enrichment 或筛选分数：测序派生 readout，单位和方向依其具体表定义；BLI KD：验证候选浓度数值，单位以工作表/论文为准，小值有利；缺失/ND/NB 等为未测或失败编码，不作阴性推断；checkpoint 是预测模型权重。 验证 XLSX 第一行为 Deep Screening/Octet 等分层标题，第二行为具体字段；KDapp (M) 与 Octet KD (M) 不同，KD 是平衡浓度、Ka (1/Ms) 是关联速率、Kd (1/s) 是解离速率，大小写不可混读。Nb _HEL / scFv_IL7 / scFv_Her2 包含不同 assay 的同一候选列；补充 CSV 实测25039行，字段 CDR_VH3_prot_seq、lib、seed、hd，不能当仪器读数。 主CSV barcode 为核苷酸条形码，read 1/read 2/read 3 为翻译片段，intensity 0…N 是处理后荧光测量，未从表头推断其精确条件；不是直接KD，也不删含`*`的原始片段。

| 原始表或 sheet | 字段（原始顺序） | 原始表示与特殊值 |
| --- | --- | --- |
| `porebski/porebski_et_al_2023_datasets.tar.gz!porebski_et_al_2023_datasets/3.HER2_scFv/fc081_fc082_her2_ml_lib_paired_translated.csv` | `barcode`, `read 1`, `intensity 0`, `intensity 1`, `intensity 2`, `intensity 3`, `intensity 4`, `intensity 5`, `intensity 6`, `intensity 7`, `intensity 8`, `intensity 9`, `intensity 10`, `intensity 11`, `intensity 12`, `intensity 13` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `porebski/porebski_et_al_2023_datasets.tar.gz!porebski_et_al_2023_datasets/3.HER2_scFv/fc079_fc080_her2_affmat_paired_translated.csv` | `barcode`, `read 1`, `intensity 0`, `intensity 1`, `intensity 2`, `intensity 3`, `intensity 4`, `intensity 5`, `intensity 6`, `intensity 7`, `intensity 8`, `intensity 9`, `intensity 10`, `intensity 11`, `intensity 12`, `intensity 13`, `intensity 14` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `porebski/porebski_et_al_2023_datasets.tar.gz!porebski_et_al_2023_datasets/1.HEL_Nb/fc071_hs065_r3_macs_paired_avg_translated.csv` | `barcode`, `read 1`, `read 2`, `read 3`, `intensity 0`, `intensity 1`, `intensity 2`, `intensity 3`, `intensity 4`, `intensity 5`, `intensity 6`, `intensity 7`, `intensity 8`, `intensity 9`, `intensity 10`, `intensity 11` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `porebski/porebski_et_al_2023_datasets.tar.gz!porebski_et_al_2023_datasets/1.HEL_Nb/fc069_fc070_r3_facs_paired_translated.csv` | `barcode`, `read 1`, `read 2`, `read 3`, `intensity 0`, `intensity 1`, `intensity 2`, `intensity 3`, `intensity 4`, `intensity 5`, `intensity 6`, `intensity 7`, `intensity 8`, `intensity 9`, `intensity 10`, `intensity 11`, `intensity 12`, `intensity 13` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `porebski/porebski_et_al_2023_datasets.tar.gz!porebski_et_al_2023_datasets/2.IL7_scFv/fc059_hs064_il7_paired_translated.csv` | `barcode`, `read 1`, `read 2`, `intensity 0`, `intensity 1`, `intensity 2`, `intensity 3`, `intensity 4` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |

### 数据示例

来自 `porebski/porebski_et_al_2023_datasets.tar.gz!porebski_et_al_2023_datasets/3.HER2_scFv/fc081_fc082_her2_ml_lib_paired_translated.csv` 的第一条真实非空数据行：

| 原始字段 | 原始值 |
| --- | --- |
| barcode | GGTGTTGGCGGCAACGTTAGTGGGAATT |
| read 1 | HDFSYCSSQRCLTKPEYRQHW |
| intensity 0 | 108.02723 |
| intensity 1 | 107.82694 |
| intensity 2 | 104.72246 |
| intensity 3 | 101.31062 |
| intensity 4 | 111.767654 |
| intensity 5 | 107.21744 |
| intensity 6 | 106.75236 |
| intensity 7 | 101.63111 |
| intensity 8 | 120.03716 |
| intensity 9 | 110.89189 |
| intensity 10 | 117.10722 |
| intensity 11 | 115.27282 |
| intensity 12 | 105.64674 |
| intensity 13 | 114.81174 |

这是该原始表的一条记录；粒度按前述定义，不把结构表示、重复或归档成员当独立抗体。

## PDB 数据库

1LYZ（hen egg-white lysozyme）、1N8Z（HER2 / trastuzumab）、3DI2（human IL7 / IL7R）对应研究靶点的代表结构。它们是共享参考，不是这些筛选 VHH/scFv 的逐变体复合物；是否与任一亲本序列严格匹配未做假定。所有链保留，不把 IL7R 当抗 IL7 抗体。

本次审计接受 3 个唯一锚点，每个都有 RCSB 完整 entry FASTA 与完整 mmCIF（原样 .cif 或 .cif.gz），共 6 个文件 / 407302 bytes。逐对检查 entry ID、非空 _atom_site 及 canonical polymer 序列一致。FASTA 保留 RCSB entity ID、原始头和序列，没有从坐标重建序列；坐标保留完整原文件。author/label chain 与 entity 的原始映射在 FASTA 头及 mmCIF `_struct_asym`、`_entity_poly`、`_atom_site.auth_asym_id` 中，不臆造链角色。

文件路径为 `pdb/sequences/rcsb_pdb_<PDB>.fasta`、`pdb/structures/<PDB>.cif.gz` 或 `<PDB>.cif`；复用已有完整未压缩 RCSB 原文件时不重新压缩。确定性 inventory SHA-256：`1d5edbb5bda9c327c0cca98ec01b13c7078c53a202e24c7505981f05d010c716`；算法为按相对路径排序，逐文件组成 `path<TAB>bytes<TAB>sha256<LF>`（UTF-8）再计算 SHA-256。

| PDB | FASTA bytes / SHA-256 | mmCIF.gz bytes / SHA-256 |
| --- | --- | --- |
| 1LYZ | 190 / `bd71bd464c5247807690c913b1183b196c3ac97c76175d6c00a56a98cf6a8c50` | 55627 / `5867ae21180bf1466378572bd1a9bf213651c740ff46d09a1243a54c2acf772f` |
| 1N8Z | 1272 / `52eadcc9b098be1ac5beedb0ed931fc2b2b4d958f4095d0154b4b881eb240aa9` | 212354 / `3a59b29e39203f1bacc9147a8b143071c77b103c597a0a9e3bdfc6c965b70951` |
| 3DI2 | 510 / `3fd77f729a66c5fa94bb8c22f0b7acfd65c50c93aaece2c9a30f1b94383eefb8` | 137349 / `6c7355745295abb4f8690bb2be9e9849d8cadc6df42cf582a3280114f46906c7` |

## 使用方式

由调用者将 `dataset_root` 赋为该 source_version 目录。以下仅读原始入口，不清洗、换算或修补 raw。

```python
import tarfile
with tarfile.open(dataset_root / "porebski/porebski_et_al_2023_datasets.tar.gz") as archive:
    print(archive.getnames()[:5])
```

## 采集过程记录

2026-09-18：按固定 Zenodo record 10123621 取得 processed TAR、checkpoint 和原 LICENSE，全部遍历五张处理表与公开论文附件；不加载执行 checkpoint。保留数据/权重 NC-ND 与论文 CC BY 的区别。底层原始实验文件需合理申请，本次没有取得或发送申请。PDB 仅补充三个有证据的共享靶点参考。

2026-09-18：全部正式 payload 按来源身份、大小和官方/本地 checksum 独立验收；原始表与附件已读取，FASTA 和完整 mmCIF 逐对核验。工作 README 同步共享版本，规定的 markdownlint 为零错误后发布。具体 API、原始下载日志、失败和重试记录保存在共享本批采集目录，未向任何作者发送消息或申请。

2026-09-18：复核 skill 版本规则，将不符合命名规则的 `zenodo-10123621` 原子重命名为 `snapshot-2023-11-14`。同步来源配置、PDB 配置、工作与共享 README 及当前结构化验收/发布记录；旧文档和原验收记录保留在 runs 的 version-migration-history。修订前后按相对路径、字节数和 SHA-256 比对全部科学文件，内容保持原样；修订 README 使用规定的 markdownlint 配置验收。

2026-09-18：README 工作稿迁入由 developer.user 定位的个人 docs/readme。初版采集记录混用了跨来源的通用描述，本次按实际来源、下载与重试记录修订。论文及附件命名补齐平台和版本。以下名称变更均核对原文件字节数及 SHA-256，内容未改写；原始文件名与下载 URL 保留在采集记录中。

- `articles/POREBSKI_2023-10-09_EuropePMC.xml` → `articles/POREBSKI_2023-10-09_EuropePMC-published.xml`；276710 bytes，SHA-256 `8b8bb30d63c441bd70540f32ef19b7f652f6cb15f4a725cec896a5544f312e20`。
- `articles/POREBSKI_2023-10-09_supplement-1.pdf` → `articles/POREBSKI_2023-10-09_NatureBiomedicalEngineering-published-supplement-1.pdf`；5631062 bytes，SHA-256 `b4701b2fe063897823c8839f67d1f9cc4a9823bdc35dd3099e6c078f819aa965`。
- `articles/POREBSKI_2023-10-09_supplement-2.pdf` → `articles/POREBSKI_2023-10-09_NatureBiomedicalEngineering-published-supplement-2.pdf`；106468 bytes，SHA-256 `71f4497d9d38c5abce6ec43ba510064d9c84a0874a6b78766e7b35ec2ddef303`。
- `articles/POREBSKI_2023-10-09_supplement-3.csv` → `articles/POREBSKI_2023-10-09_NatureBiomedicalEngineering-published-supplement-3.csv`；878800 bytes，SHA-256 `28ee75812505a4302b0262572927d23463939821857486b830917817c896df92`。
- `articles/POREBSKI_2023-10-09_supplement-4.xlsx` → `articles/POREBSKI_2023-10-09_NatureBiomedicalEngineering-published-supplement-4.xlsx`；44620 bytes，SHA-256 `d101ed5c82619e6bc3764c18fc8351253f69f42d9f7c335b7904bd2eb72e0e4d`。
- `articles/POREBSKI_2023-10-09_supplement-5.xlsx` → `articles/POREBSKI_2023-10-09_NatureBiomedicalEngineering-published-supplement-5.xlsx`；14064 bytes，SHA-256 `1e8249fd092f49f16d763160fbdcdd60ddf0c6bf11efc327b6ee9706b2d4b7f0`。

旧文档和结构化报告保存在共享 runs/documentation-reorganization；修订后本地与共享 README 同步并执行规定的 Markdownlint。

- 上游原始名称 `fullTextXML`；入口 <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10963267/fullTextXML>。
- 上游原始名称 `41551_2023_1093_MOESM1_ESM.pdf`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41551-023-01093-3/MediaObjects/41551_2023_1093_MOESM1_ESM.pdf>。
- 上游原始名称 `41551_2023_1093_MOESM2_ESM.pdf`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41551-023-01093-3/MediaObjects/41551_2023_1093_MOESM2_ESM.pdf>。
- 上游原始名称 `41551_2023_1093_MOESM4_ESM.csv`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41551-023-01093-3/MediaObjects/41551_2023_1093_MOESM4_ESM.csv>。
- 上游原始名称 `41551_2023_1093_MOESM5_ESM.xlsx`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41551-023-01093-3/MediaObjects/41551_2023_1093_MOESM5_ESM.xlsx>。
- 上游原始名称 `41551_2023_1093_MOESM6_ESM.xlsx`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41551-023-01093-3/MediaObjects/41551_2023_1093_MOESM6_ESM.xlsx>。

## 参考文献

- [数据源固定版本/入口](https://zenodo.org/records/10123621)
- [归档主文 DOI](https://doi.org/10.1038/s41551-023-01093-3)
- [primary full-text XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10963267/fullTextXML)
- [Supplementary Information (download PDF )](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41551-023-01093-3/MediaObjects/41551_2023_1093_MOESM1_ESM.pdf)
- [Reporting Summary (download PDF )](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41551-023-01093-3/MediaObjects/41551_2023_1093_MOESM2_ESM.pdf)
- [Supplementary Data 1 (download CSV )](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41551-023-01093-3/MediaObjects/41551_2023_1093_MOESM4_ESM.csv)
- [Source Data Figs. 2–5 and Extended Data Figs. 1 and 3 (download XLSX )](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41551-023-01093-3/MediaObjects/41551_2023_1093_MOESM5_ESM.xlsx)
- [Source Data Extended Data Fig. 1 (download XLSX )](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41551-023-01093-3/MediaObjects/41551_2023_1093_MOESM6_ESM.xlsx)
- [PDB 1LYZ（条目含原始结构论文）](https://www.rcsb.org/structure/1LYZ)
- [PDB 1N8Z（条目含原始结构论文）](https://www.rcsb.org/structure/1N8Z)
- [PDB 3DI2（条目含原始结构论文）](https://www.rcsb.org/structure/3DI2)

## 其他

### 完整性与验收

| payload | bytes | SHA-256 |
| --- | --- | --- |
| `porebski/checkpoint-bsf24_bert_base-epoch=00-val_loss=0.13.ckpt` | 1035991483 | `b30e190893603f817b52ea48fd1993d7e6833774eef274c1bfcdfd26d472b644` |
| `porebski/porebski_et_al_2023_datasets.tar.gz` | 611075767 | `5f7c64a8930a9571303a1b1a68bb78f5082fc1434089b952710254daea207ce7` |
| `porebski/LICENSE.md` | 13261 | `042f771689233d6ea7f730554cc7620f74b0f5eef9bde9a02f8bf152c0b55dfc` |

原始 payload 合计 1647080511 bytes；inventory SHA-256 `cc5804e46b6440ad6732665093ab732651626ad0457d91f3599f66d619ae3757`（与 PDB 同一算法）。归档成员全部读取；统计与 API/验收报告保存于共享 runs，不作为 raw 附属 manifest 发布。每个文件与论文/PDB 身份均可重验，不执行交付包中的训练代码或模型反序列化。

### 许可和再分发边界

交付 LICENSE.md 明确 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0（CC BY-NC-ND 4.0），版权 MRC Laboratory of Molecular Biology；Zenodo 元数据 other-nc。论文 CC BY 4.0 不覆盖数据/权重的非商业、禁止演绎限制。

### 公开范围对照

| 范围 | 本次证据与状态 |
| --- | --- |
| 已取得的公开部分 | 全部三个公开 Zenodo 文件和公开论文补充；论文称体积过大的底层原始实验数据需向作者合理申请，本次未取得该受限部分，也未发送申请。 |
| 论文/来源未公开或未取得部分 | 仅按本文具体缺口报告；未访问限制不冒称完成。 |
| processed / release | 未生成；本层仅上游原样输入。 |
