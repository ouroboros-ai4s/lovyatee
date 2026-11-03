---
tags:
  - context
---

# SRC_R59_BINDCRAFT 数据说明

## 数据集身份

- `source_id`：`SRC_R59_BINDCRAFT`
- `source_version`：`snapshot-2025-08-27`
- 原作者或发布机构：Martin Pacesa、Lennart Nickel、Christian Schellhaas 等；Bruno E. Correia 团队及论文共同作者

## 实验设计和数据口径

BindCraft 设计的是 de novo 蛋白 binder，不能自动归为抗体。流程先针对输入靶点结构用 AlphaFold2 引导序列/结构优化，随后 ProteinMPNN 优化非界面序列并作结构自洽性筛选，再进行表达、结合筛选以及部分候选的 BLI/SPR 和结构验证。公开包混合计算结构、模型分数、筛选结果和少量测定汇总，没有统一公开的逐条仪器原始记录。

正式 Supplementary Data 1 包含 212 行、13 个 Target、212 条唯一 Sequence；论文主体以 12 个基准靶点讨论性能，表另含 HER2/AAV 等实验，不能机械把表内 Target 数当成同一个基准口径。Binding=1 有 65 行、=0 有 87 行、空值 60 行。空值表示该表没有公开二元结果，不是失败；0 不给出统一可比较的数值亲和力或删失检测界限。

Affinity_nM 非空仅 20 行，全部 Binding=1，其中 10 条带 `*`。该列是实验亲和力汇总（nM，越小越强），星号涉及表注/正文中的拟合或多价表观效应，必须逐实验保留；不转成精确单价 KD。其余 192 行缺失 Affinity，不是零或无结合。PD1_b2 表中 `1*` 与正文低于 1 nM/多价 Fc 构型叙述应一并阅读，不能据此建立精确 1 nM 真值。

216 个模型指标来自 36 个指标族各六列（`Average_` 与 `1_`–`5_`），模型编号不是六组独立实验。`dG` 是计算评分，不是测定自由能；pLDDT 在本文件以 0–1 量级呈现，PAE 等不得在没有上游缩放证据时直接声明单位为 Å。不同 Trajectory/序列可能共享设计历史或相同靶点，切分应同时考虑靶点、序列相似性、trajectory parent 与上游预训练结构，避免让同靶点优化结果进入独立测试集。

| Target 原始编码 | 设计行数 |
| --- | --- |
| BBF-14 | 14 |
| BetV1 | 7 |
| CbAgo | 12 |
| CD45 | 16 |
| CLDN1 | 17 |
| DerF7 | 11 |
| DerF21 | 10 |
| IFNAR2 | 20 |
| PD-L1 | 21 |
| Sas6 | 11 |
| SpCas9 | 10 |
| PD1 | 53 |
| HER2 | 10 |

## 论文原文

### Nature 主文

- 标题：One-shot design of functional protein binders with BindCraft
- 作者：Martin Pacesa、Lennart Nickel、Christian Schellhaas 等（完整作者列表见主文）
- 载体与版本：Nature 646, 483–492；正式出版 PDF
- 发布日期：2025-08-27（在线）；2025-10-09（卷期）
- DOI：10.1038/s41586-025-09429-6
- PMID / PMCID：PMID 40866699 / PMCID PMC12507698（Europe PMC DOI 检索核验）
- 本地文件：`articles/BindCraft_2025-08-27_Nature.pdf`
- 文件大小：47088961 bytes
- SHA-256：`f88a57a85af6b5c875371960338255a6cf64813511cada29b6e231c49112d88f`
- 文本许可：CC BY-NC-ND 4.0（正式 PDF 明示）
- 补充材料：Supplementary Information、Reporting Summary、Peer Review 三份 PDF 另列本地身份；Supplementary Data 1 CSV、Data 2 XLSX 属 payload

### 补充说明

- 标题：One-shot design of functional protein binders with BindCraft — 补充说明
- 作者：Martin Pacesa、Lennart Nickel、Christian Schellhaas 等（完整作者列表见主文）
- 载体与版本：Nature 正式论文对应附件；15 页 PDF
- 发布日期：2025-08-27（随正式出版记录）
- DOI：10.1038/s41586-025-09429-6（主文 DOI；附件无独立 DOI）
- PMID / PMCID：无独立编号；对应主文
- 本地文件：`articles/BindCraft_2025-08-27_Nature-SupplementaryInformation.pdf`
- 文件大小：8349078 bytes
- SHA-256：`faf09b8749f1d1785ab46beb917ad4d44b122904e4678c3a748f8dd4a600b2cd`
- 文本许可：未发现独立更宽授权；按 publisher/主文 CC BY-NC-ND 4.0 边界处理
- 补充材料：本文件自身为主文附件；无其他独立子附件

### 研究报告摘要

- 标题：One-shot design of functional protein binders with BindCraft — 研究报告摘要
- 作者：Martin Pacesa、Lennart Nickel、Christian Schellhaas 等（完整作者列表见主文）
- 载体与版本：Nature 正式论文对应附件；3 页 PDF
- 发布日期：2025-08-27（随正式出版记录）
- DOI：10.1038/s41586-025-09429-6（主文 DOI；附件无独立 DOI）
- PMID / PMCID：无独立编号；对应主文
- 本地文件：`articles/BindCraft_2025-08-27_Nature-ReportingSummary.pdf`
- 文件大小：1758434 bytes
- SHA-256：`e1ad17ab49575fe16ada9b6eeee890e0abc41ac274ebfa82e2eeefe10c636abf`
- 文本许可：未发现独立更宽授权；按 publisher/主文 CC BY-NC-ND 4.0 边界处理
- 补充材料：本文件自身为主文附件；无其他独立子附件

### 公开审稿文件

- 标题：One-shot design of functional protein binders with BindCraft — 公开审稿文件
- 作者：匿名审稿人与论文作者；由 Nature 发布
- 载体与版本：Nature 正式论文对应附件；28 页 PDF
- 发布日期：2025-08-27（随正式出版记录）
- DOI：10.1038/s41586-025-09429-6（主文 DOI；附件无独立 DOI）
- PMID / PMCID：无独立编号；对应主文
- 本地文件：`articles/BindCraft_2025-08-27_Nature-PeerReview.pdf`
- 文件大小：1494054 bytes
- SHA-256：`c62871e165ab336a008899ca6afdcfc19d4346edd285638623dbbc3e8996d19d`
- 文本许可：未发现独立更宽授权；按 publisher/主文 CC BY-NC-ND 4.0 边界处理
- 补充材料：本文件自身为主文附件；无其他独立子附件

## 仓库内容

[论文](https://www.nature.com/articles/s41586-025-09429-6)直接引用 [Zenodo record 14249738](https://zenodo.org/records/14249738)，该固定记录日期 2024-11-30、DOI `10.5281/zenodo.14249738`。选择论文引用版本，不追随最新记录。正式 publisher 五份补充文件与这一 ZIP 组成选择性公开组合包，版本 `snapshot-2025-08-27` 以正式论文在线日期为锚点，ZIP 自身仍冻结较早的记录。

ZIP 官方大小 14,541,120 bytes、MD5 `66364e7ce957da7f9e8cb938d5bd7ca4`，本地核验一致；保留完整归档未展开。没有把 BindCraft 软件仓库整体混入此实验来源。

```text
snapshot-2025-08-27/
└── BindCraft/
    ├── DesignModels.zip
    ├── BindCraft_2025-08-27_Nature-SupplementaryData1.csv
    └── BindCraft_2025-08-27_Nature-SupplementaryData2.xlsx
```

表格、归档与其记录关系见数据结构；上游说明、许可或嵌入资源保留原始内容。

## 数据结构

### 表格与设计模型关系

ZIP 共 429 members（428 文件和 1 目录），未压缩总量 67,690,361 bytes，真正模型为 `DesignModels/` 内的 212 个 PDB。`__MACOSX/` 下同名 `.pdb` 是 resource fork，不是额外 212 个设计；归档内另有 `SupplementaryTable1.csv` 和系统资源文件。模型是计算预测结构，不是这 212 个设计均有实验结构。

ZIP 内 CSV 与正式 publisher CSV 具有同样 212 个 DesignName 和 225 列，但 16 个名称涉及 1,022 个单元格差异：9 个 PD-L1 的 Sequence/Trajectory 发生名称重排，另 7 个 Sas6 的筛选标记变化；Affinity_nM 一致。旧表 Binding 计数为 65 个 1、80 个 0、67 个空；不能当作正式表的替代。保留两个原始版本，不改写标签。

逐模型完整链 B 序列与正式表 Sequence 作唯一精确匹配，覆盖全部 212 条。文件名直接 join 会错配 9 个 PD-L1 名称；BBF-14 文件名前缀与表的 BBF 前缀也不同。以下映射来自完整序列比对，只在 README 说明，没有派生模型文件或 sidecar：

| ZIP 模型文件 | 正式表 DesignName（完整链 B 序列匹配） |
| --- | --- |
| DesignModels/PD-L1_b10.pdb | PD-L1_b8 |
| DesignModels/PD-L1_b8.pdb | PD-L1_b3 |
| DesignModels/PD-L1_b9.pdb | PD-L1_b4 |
| DesignModels/PD-L1_b2.pdb | PD-L1_b9 |
| DesignModels/PD-L1_b3.pdb | PD-L1_b5 |
| DesignModels/PD-L1_b7.pdb | PD-L1_b2 |
| DesignModels/PD-L1_b6.pdb | PD-L1_b10 |
| DesignModels/PD-L1_b4.pdb | PD-L1_b6 |
| DesignModels/PD-L1_b5.pdb | PD-L1_b7 |

Data 2 有 24 个 worksheet：2 个靶点比较矩阵和 11 个靶点各两张 binder TMscore/SeqIdentity 矩阵；没有 HER2 的 binder 矩阵。矩阵还可能含参考/对照条目；维度不能替代独立设计数。完整 worksheet 尺寸列于下表。

| worksheet | 行数（含标签） | 列数 | 非空行 |
| --- | --- | --- | --- |
| Targets_TMscore | 14 | 14 | 14 |
| Targets_SeqIdentity | 14 | 14 | 14 |
| BBF-14_binders_TMscore | 15 | 15 | 15 |
| BBF-14_binders_SeqIdentity | 15 | 15 | 15 |
| BetV1_binders_TMscore | 9 | 9 | 9 |
| BetV1_binders_SeqIdentity | 9 | 9 | 9 |
| CbAgo_binders_TMscore | 13 | 13 | 13 |
| CbAgo_binders_SeqIdentity | 13 | 13 | 13 |
| CD45_binders_TMscore | 17 | 17 | 17 |
| CD45_binders_SeqIdentity | 17 | 17 | 17 |
| CLDN1_binders_TMscore | 19 | 19 | 19 |
| CLDN1_binders_SeqIdentity | 19 | 19 | 19 |
| DerF7_binders_TMscore | 12 | 12 | 12 |
| DerF7_binders_SeqIdentity | 12 | 12 | 12 |
| DerF21_binders_TMscore | 11 | 11 | 11 |
| DerF21_binders_SeqIdentity | 11 | 11 | 11 |
| IFNAR2_binders_TMscore | 22 | 22 | 22 |
| IFNAR2_binders_SeqIdentity | 22 | 22 | 22 |
| PD-L1_binders_TMscore | 12 | 12 | 12 |
| PD-L1_binders_SeqIdentity | 12 | 12 | 12 |
| PD1_binders_TMscore | 55 | 55 | 55 |
| PD1_binders_SeqIdentity | 55 | 55 | 55 |
| Sas6_binders_TMscore | 12 | 12 | 12 |
| Sas6_binders_SeqIdentity | 12 | 12 | 12 |
| SpCas9_binders_TMscore | 15 | 15 | 15 |
| SpCas9_binders_SeqIdentity | 15 | 15 | 15 |

公开设计模型 ZIP 已逐个解析原子坐标并验证 212 条完整 binder 链 B 序列；链 A 是各模型所包含的靶点构建体，不保证等同于实验表达的全长靶点。它们属于上游 payload 的预测模型，不计作 RCSB 外部结构补充。

### 字段说明

| 核心字段或族 | 含义与边界 |
| --- | --- |
| Target | 靶点原始分组名称，共 13 个值 |
| DesignName | 本正式表行标识；跨 ZIP 必须用完整序列确认 |
| Trajectory | 生成/优化历史 ID，字符串唯一不等于独立 parent |
| Binding | 实验筛选标记；1/0/空，不能和模型分数互换 |
| Affinity_nM | 20 条实验亲和力，10 条带星号；保留原字符串和实验注释 |
| Length / Sequence | binder 全序列及长度，212 条均为标准 20 字母且长度一致 |
| MPNN_score / MPNN_seq_recovery | 计算序列优化指标，无直接实验亲和力含义 |
| `Average_` / `1_` / `2_` / `3_` / `4_` / `5_` | 36 族计算指标的汇总和模型序号；非实验 replicate |
| InterfaceAAs | 字符串形式的界面残基统计，不使用 eval 执行 |
| Data 2 TMscore / SeqIdentity | 成对计算结构/序列比较，含标签；不是测量 KD |

全部 36 个指标后缀：`pLDDT`、`pTM`、`i_pTM`、`pAE`、`i_pAE`、`i_pLDDT`、`ss_pLDDT`、`Unrelaxed_Clashes`、`Relaxed_Clashes`、`Binder_Energy_Score`、`Surface_Hydrophobicity`、`ShapeComplementarity`、`PackStat`、`dG`、`dSASA`、`dG/dSASA`、`Interface_SASA_%`、`Interface_Hydrophobicity`、`n_InterfaceResidues`、`n_InterfaceHbonds`、`InterfaceHbondsPercentage`、`n_InterfaceUnsatHbonds`、`InterfaceUnsatHbondsPercentage`、`Interface_Helix%`、`Interface_BetaSheet%`、`Interface_Loop%`、`Binder_Helix%`、`Binder_BetaSheet%`、`Binder_Loop%`、`InterfaceAAs`、`Hotspot_RMSD`、`Target_RMSD`、`Binder_pLDDT`、`Binder_pTM`、`Binder_pAE`、`Binder_RMSD`。前缀与后缀笛卡尔组合精确定义其余 216 个原始字段。CSV 原始类型均为文本：Target/DesignName/Trajectory/Sequence 是字符串，Length 是整数字符串，Binding 是 1/0/空；Affinity_nM 是可带 * 的数值字符串或空，MPNN 与大部分模型指标为浮点数字文本，InterfaceAAs 为带引号的字典文本。XLSX 比较矩阵的行/列标签为字符串，矩阵数值为计算比较结果。计算指标没有统一实验单位或检测边界，空字段不转为数值零。

### 数据示例

正式表中 BBF_b4 的实际记录摘录；这是一个设计，不是六个计算指标副本对应六次实验：

| 字段 | 原始值 |
| --- | --- |
| Target | `BBF-14` |
| DesignName | `BBF_b4` |
| Binding | `1` |
| Affinity_nM | `20.9` |
| Length | `140` |
| Sequence | `SPIQEEIQKKVRELLEKLIEYLEELKEKAKPPFKEKLEEVIEGLERLKEEVDKVQLNMNLIVFEGLEVDEEGRVWFIVKEMLHATTEEEALENMDKFLESWEKVFKELLEYHFEHNDTSPTFDFFLDFLWWQLYGEPMPK` |
| MPNN_score | `1.04` |
| Average_pLDDT | `0.9` |

## PDB 数据库

另补充 17 个 RCSB 原始条目，每个同时有完整 entity FASTA 和完整 mmCIF，不裁剪为上游输入的区间，也不嫁接 binder 序列。

8 个论文 Data Availability 输入/模板锚点为 2LAG、5FMV、9HAG、3UV1、5YNY、6QZK、1N8Z、4ZT0。4 个本文实验复合物为 9HAC（BBF-14/binder4）、9HAD（DerF21/binder10）、9HAE 与 9HAF（DerF7/binder2 的不同晶型），不是 212 条逐对象覆盖。7MXL 是 BetV1/商业抗体参考。Supplementary Fig. 5b 明示 6IFO、5VW1、8YE6、8YE9 为天然 anti-CRISPR 比较复合物，不能标为本研究设计结构。

Supplementary Table 1 指出 PD1、PD-L1、CrSAS-6、BetV1 等使用 AF2 prediction；CD45/DerF7/DerF21/CbAgo 等也有预测/模板/截段步骤。没有为无 accession 的预测输入臆配实验结构；表内范围与当前完整 RCSB 条目不同。2LAG 保存完整 NMR 模型，不把 conformer 当成独立样本；6QZK 保留 DNA，4ZT0 保留 RNA，1N8Z 保留原生 Fab。下表列全部 polymer entity 的 author chains 与字面描述以核实角色。

论文另报 cryo-EM 图 EMD-53510/53511，本次没有取得 EMDB map；当前声明限于 ZIP、五份 publisher 补充材料及 FASTA/mmCIF，不声称完整研究底层结构证据。

获取/核验日期 2026-09-18。每个编号使用 RCSB `https://www.rcsb.org/fasta/entry/<PDB_ID>/download` 与 `https://files.rcsb.org/download/<PDB_ID>.cif`。校验 FASTA entity ID 集合及全序列与 mmCIF canonical entity 全序列严格相等，并核对 entry.id、非空原子坐标和 author-chain。共 17 个完整对，34 个文件，29,136,925 bytes。按相对路径排序拼接 `relative_path<TAB>bytes<TAB>sha256<LF>` 后 inventory SHA-256 为 `a59b5f41bac5d4de68d64bd5c9f1c1a6f074bc6b94546b8e2a450a55da2fa06f`。

| PDB | FASTA bytes | FASTA SHA-256 | mmCIF bytes | mmCIF SHA-256 |
| --- | --- | --- | --- | --- |
| 2LAG | 519 | `2c80ab38eb5c660131b3dd0cd71be1ddaecf8066782642f62c5bc460cff3645c` | 5526408 | `50e7775c3296ec15817572935b31d5494df1567407ab8ccbfffc719fa08aaca4` |
| 5FMV | 447 | `fbd4c116de2598a5e5a1be2592ba992876f60db7a0301bf18c266dc709ba3d1f` | 1115883 | `e78546855da168f46ab4ad41d495cc3f6a4fbaaca3a5c9f3f7933fef94bb12bd` |
| 9HAG | 174 | `ac96121c00421666e7622675e93a4fe5016c73ca3fdaea7ed0d52bb666c0ab68` | 341415 | `891bc906fe4ae4fc65e77a04bc63700aa6606e48d2c7c6bf2cf7eb43c5d28182` |
| 3UV1 | 266 | `47d84fef74f813380a702a2faf9974838f200059fa25e7892948e80c11667853` | 375279 | `32f5abb482f037be25fa95c649c735120c6f76d93e131167c440712430d8206a` |
| 5YNY | 205 | `fd6baf4d6d8c248db2c06c0528a7ac09df643dd9b74596b476bbc376d112c4ee` | 734801 | `bb0b2eea0c1d3519d4ab3dee8ef8a707216e93a66c4913c3598f84b034e852a3` |
| 6QZK | 1106 | `0dd9b2995aea7744e96812011cba6264b3f9120bbdf3843618ada9875da9dd55` | 1404919 | `39aa0c51732df1ad1bd483ca75186758fed14d7800d5ce70fd19e10577a86eee` |
| 1N8Z | 1272 | `52eadcc9b098be1ac5beedb0ed931fc2b2b4d958f4095d0154b4b881eb240aa9` | 845613 | `9f22f02b6e514de56dab8a48bc31a16302a51397779e64c398ad3a7f05cb19a2` |
| 4ZT0 | 1609 | `1ffc01538ebbf7d583c3edd03469b0c0ff2f990fa72a546288340b2b77dd9f1a` | 4887299 | `b2cc12c84595e8a3ad3613b75ea124b401f4eff66f79025db3f3291ad98ac5a0` |
| 9HAC | 405 | `2aaf9e92d324e226f5857a69983eb2bb36f46a1c27adb9f222c1eb55f7d59e76` | 906824 | `02f3f383de8c6872ae7e031765e155b12cde5641ed900848c2b019599e50a1b1` |
| 9HAD | 386 | `ab27aee7d4234e6740a79b25526864ffad8bb2675831ee6fc15f04e6a84cad66` | 814658 | `14a19146253bc093a61e29d8ca6bedefbad61d068a61c8357eb5f53ee34b1d2b` |
| 9HAE | 437 | `7348a5a057881d7bc92df7cf490d4bc6c4ed67d53ebe39c1aa36a9c493ab44d0` | 955459 | `e150e11b25a809f1159536fd282b13bcb7abfa1911960109e66536f01216fe19` |
| 9HAF | 443 | `b3f3794fc10f51cbb2faae7967b353bbfc512892500c2814f48b8892774af16e` | 1354691 | `bdb0c458a1b5932e35f4bc8920ff67e698a62be1c32c2758de32d28438f954e1` |
| 7MXL | 2056 | `bdca16d9584b4409fe8c38d4b3ec51759e89499f4a1481225a1f4c52a1a38ba1` | 1231637 | `95b8d0390942ce0102b70f22cb68d326946e11677b90c48d47b0a939498d362b` |
| 6IFO | 1845 | `3e89b0830cef9f36659c645bf0ca2e237adafcda6513e43972c30466d7fe5d46` | 2898234 | `af6d90816c7f834e5eab551dc429d506522b3eb88a9c16b1444a4a277c5a6826` |
| 5VW1 | 1817 | `171f059af76d8155c765d3f5ef58387aca40586b36cab9225a9058a93b9eff0e` | 2769435 | `f4e3e509249203562ab9f94cacc0693172581df5ad050bfb650c1b7e23f29c16` |
| 8YE6 | 1821 | `37d61202ad127fa3fb95ff5d718dde744131e12907d136ce259d6fc82dc2ac69` | 1477071 | `898c62c76212d1f6f3b8173af7750a8e597be21fab65918b8b0170e73c883711` |
| 8YE9 | 1799 | `18ca8aa891cece8f76560ba06456f55dae110e278603e064cc41125e4cb2b8a8` | 1480692 | `0eb30a49b33f22d66362750d5c44e9aa10ce54afd68c4582603a5c39dbcbea90` |

原生 polymer entity 角色（entity ID、作者链、字面描述）：

| PDB | entity | author chains | 原生实体描述 |
| --- | --- | --- | --- |
| 2LAG | 1 | B | Interferon alpha/beta receptor 2 |
| 2LAG | 2 | A | Interferon alpha-2 |
| 5FMV | 1 | A,B | RECEPTOR-TYPE TYROSINE-PROTEIN PHOSPHATASE C |
| 9HAG | 1 | A | BBF-14 |
| 3UV1 | 1 | A,B | Der f 7 allergen |
| 5YNY | 1 | A,B,C,D | Allergen Der f 21 |
| 6QZK | 1 | A | Protein argonaute |
| 6QZK | 2 | B | siDNA guide (5'-D(P*CP*GP*AP*GP*GP*TP*AP*GP*TP*AP*GP*GP*TP*TP*GP*TP*AP*TP*AP*GP*T)-3') |
| 6QZK | 3 | C | DNA target (5'-D(T*AP*TP*AP*CP*AP*AP*CP*CP*TP*AP*CP*TP*AP*CP*CP*TP*CP*T)-3') |
| 1N8Z | 1 | A | Herceptin Fab (antibody) - light chain |
| 1N8Z | 2 | B | Herceptin Fab (antibody) - heavy chain |
| 1N8Z | 3 | C | Receptor protein-tyrosine kinase erbB-2 |
| 4ZT0 | 1 | A,C | CRISPR-associated endonuclease Cas9 |
| 4ZT0 | 2 | B,D | single-guide RNA |
| 9HAC | 1 | A,C | BBF-14 |
| 9HAC | 2 | B,D | BBF-14_binder4 |
| 9HAD | 1 | A,B | Mite allergen Der f 21.0101 |
| 9HAD | 2 | C,D | DerF21_binder10 |
| 9HAE | 1 | A,C | Mite allergen Der f 7 |
| 9HAE | 2 | B,D | DerF7_binder2 |
| 9HAF | 1 | A,C,E | Mite allergen Der f 7 |
| 9HAF | 2 | B,D,F | DerF7_binder2 |
| 7MXL | 1 | A | REGN5713 antibody Fab fragment heavy chain |
| 7MXL | 2 | B | REGN5713 antibody Fab fragment light chain |
| 7MXL | 3 | C | Major pollen allergen Bet v 1-A |
| 7MXL | 4 | J | REGN5715 antibody Fab fragment heavy chain |
| 7MXL | 5 | K | REGN5715 antibody Fab fragment light chain |
| 7MXL | 6 | L | REGN5714 antibody Fab fragment light chain |
| 7MXL | 7 | H | REGN5714 antibody Fab fragment heavy chain |
| 6IFO | 1 | A,B | CRISPR-associated endonuclease Cas9/Csn1 |
| 6IFO | 2 | C,D | RNA (99-MER) |
| 6IFO | 3 | F,E | AcrIIA2 |
| 5VW1 | 1 | A | CRISPR-associated endonuclease Cas9/Csn1 |
| 5VW1 | 2 | C | sgRNA |
| 5VW1 | 3 | B | anti-CRISPR protein AcrIIA4 |
| 8YE6 | 1 | B | A32 |
| 8YE6 | 2 | A | CRISPR-associated endonuclease Cas9/Csn1 |
| 8YE6 | 3 | C | RNA (92-MER) |
| 8YE9 | 1 | A | CRISPR-associated endonuclease Cas9/Csn1 |
| 8YE9 | 2 | C | RNA (98-MER) |
| 8YE9 | 3 | B | A25 |

## 使用方式

依赖见接入代码 requirements；以下仅从原始文件读取。

```python
import csv
from pathlib import Path
# dataset_root 由调用者赋值为该 source version 目录。
path = Path(dataset_root) / "BindCraft/BindCraft_2025-08-27_Nature-SupplementaryData1.csv"
with path.open(encoding="utf-8-sig", newline="") as stream:
    records = list(csv.DictReader(stream))
print(len(records), records[0]["DesignName"])
```

## 采集过程记录

1. 2026-09-18：读取项目/开发者身份、执行清单与一手来源；由配置读取共享存储根，代码和文档只写本人 workspace。
2. 固定上游版本并在对应 `.staging/snapshot-2025-08-27` 下载，使用断点续传、HTTP 长度及可得的官方校验；遇到环境直连失败采用现有 HTTP 路由回退。
3. 首轮 publisher 备用地址混入相对 `#MOESM` 链接，requests 拒绝无 schema URL；纠正为实际 HTTPS MediaObjects 入口，未把 HTML 错误页当数据。PDB 接口曾 TLS EOF/超时，重试后原始文件通过核验。下载 opaque MOESM 文件后依据出版页附件角色统一命名为来源、日期、载体、补充角色，逐份比较改名前后 bytes/SHA-256，全部相同。

   实际读取发现 ZIP/正式 CSV 的 1,022 个单元格差异；完整序列连接又发现 9 个模型文件名的 PD-L1 重排。保留上游差异并在本文记录，未“修复”原 CSV/ZIP。继续审读补充 PDF 后发现四个天然 anti-CRISPR 比较 PDB，并补齐其原生文件。
4. 解析全部实际表/归档，独立核对文件集合、完整格式、哈希与 PDB 两层，保留上游差异。
5. README 工作稿每次写入立即同步共享目录；发布器复核固定格式、同步 hash 和 pinned markdownlint 0 errors 后原子发布。已于 2026-09-18T20:48:14.899306+00:00 从 staging 原子发布，当前为 final；本次修订 README 在同一次写入中覆盖同步 final，并重新审计和 lint。

依据来源、可核验日期、载体和附件角色整理 opaque 名称，改名前后 bytes/SHA-256 相同；中间名保留实际修订历史。附件名称按正式出版日期及实际角色整理。具体映射如下：

| 上游原名 | 中间名（如有） | 本地相对路径 | 核对 bytes | 核对 SHA-256 |
| --- | --- | --- | --- | --- |
| 41586_2025_9429_MOESM1_ESM.pdf | BindCraft_2025-08-27_41586_2025_9429_MOESM1_ESM.pdf | articles/BindCraft_2025-08-27_Nature-SupplementaryInformation.pdf | 8349078 | `faf09b8749f1d1785ab46beb917ad4d44b122904e4678c3a748f8dd4a600b2cd` |
| 41586_2025_9429_MOESM2_ESM.pdf | BindCraft_2025-08-27_41586_2025_9429_MOESM2_ESM.pdf | articles/BindCraft_2025-08-27_Nature-ReportingSummary.pdf | 1758434 | `e1ad17ab49575fe16ada9b6eeee890e0abc41ac274ebfa82e2eeefe10c636abf` |
| 41586_2025_9429_MOESM3_ESM.pdf | BindCraft_2025-08-27_41586_2025_9429_MOESM3_ESM.pdf | articles/BindCraft_2025-08-27_Nature-PeerReview.pdf | 1494054 | `c62871e165ab336a008899ca6afdcfc19d4346edd285638623dbbc3e8996d19d` |
| 41586_2025_9429_MOESM4_ESM.csv | 无 | BindCraft/BindCraft_2025-08-27_Nature-SupplementaryData1.csv | 283408 | `c87fd6cd0a54fe57d840938be07449394abbd55318494c8cc0292b6417c16b4f` |
| 41586_2025_9429_MOESM5_ESM.xlsx | 无 | BindCraft/BindCraft_2025-08-27_Nature-SupplementaryData2.xlsx | 99632 | `c47e007749f832d85f431a02811aec2ffb013616d41957a1ba7d0131c9155ac4` |

2026-09-18 逐条复审后：补齐全部已取得 PDB 的条目和原始结构论文主引用，以及涉及的上游汇编/对照引用。把 ZIP 模型说明移回数据结构，补正真实 publisher 原名与中间名修订痕迹。相应修改同步个人状态、事实台账和交接，未取得的材料继续标明 partial/blocked。

## 参考文献

- [正式主文及附件](https://www.nature.com/articles/s41586-025-09429-6)
- [论文引用 Zenodo 固定记录](https://zenodo.org/records/14249738)

### PDB 条目与原始结构论文

以下主引用直接读取归档 mmCIF 的 `_citation` 元数据，按同一主引用合并；每个 PDB 链接均指向该原始条目，不把输入结构论文算作本来源的新实验。

| 原始 PDB 条目 | 结构论文主引用（标题、期刊、年份） | DOI / PMID |
| --- | --- | --- |
| [1N8Z](https://www.rcsb.org/structure/1N8Z) | Structure of the Extracellular Region of HER2 Alone and in Complex with the Herceptin Fab；Nature；2003 | [DOI 10.1038/nature01392](https://doi.org/10.1038/nature01392)；[PMID 12610629](https://pubmed.ncbi.nlm.nih.gov/12610629/) |
| [2LAG](https://www.rcsb.org/structure/2LAG) | Observation of Intermolecular Interactions in Large Protein Complexes by 2D-Double Difference Nuclear Overhauser Enhancement Spectroscopy: Application to the 44 kDa Interferon-Receptor Complex.；J.Am.Chem.Soc.；2011 | [DOI 10.1021/ja205480v](https://doi.org/10.1021/ja205480v)；[PMID 21819146](https://pubmed.ncbi.nlm.nih.gov/21819146/) |
| [3UV1](https://www.rcsb.org/structure/3UV1) | Crystal Structure of Der f 7, a Dust Mite Allergen from Dermatophagoides farinae.；Plos One；2012 | [DOI 10.1371/journal.pone.0044850](https://doi.org/10.1371/journal.pone.0044850)；[PMID 22970319](https://pubmed.ncbi.nlm.nih.gov/22970319/) |
| [4ZT0](https://www.rcsb.org/structure/4ZT0) | A Cas9-guide RNA complex preorganized for target DNA recognition.；Science；2015 | [DOI 10.1126/science.aab1452](https://doi.org/10.1126/science.aab1452)；[PMID 26113724](https://pubmed.ncbi.nlm.nih.gov/26113724/) |
| [5FMV](https://www.rcsb.org/structure/5FMV) | Initiation of T Cell Signaling by Cd45 Segregation at 'Close Contacts'.；Nat.Immunol.；2016 | [DOI 10.1038/NI.3392](https://doi.org/10.1038/NI.3392)；[PMID 26998761](https://pubmed.ncbi.nlm.nih.gov/26998761/) |
| [5VW1](https://www.rcsb.org/structure/5VW1) | Inhibition Mechanism of an Anti-CRISPR Suppressor AcrIIA4 Targeting SpyCas9.；Mol. Cell；2017 | [DOI 10.1016/j.molcel.2017.05.024](https://doi.org/10.1016/j.molcel.2017.05.024)；[PMID 28602637](https://pubmed.ncbi.nlm.nih.gov/28602637/) |
| [5YNY](https://www.rcsb.org/structure/5YNY) | Crystal structure and epitope analysis of house dust mite allergen Der f 21.；Sci Rep；2019 | [DOI 10.1038/s41598-019-40879-x](https://doi.org/10.1038/s41598-019-40879-x)；[PMID 30894561](https://pubmed.ncbi.nlm.nih.gov/30894561/) |
| [6IFO](https://www.rcsb.org/structure/6IFO) | Phage AcrIIA2 DNA Mimicry: Structural Basis of the CRISPR and Anti-CRISPR Arms Race.；Mol. Cell；2019 | [DOI 10.1016/j.molcel.2018.11.011](https://doi.org/10.1016/j.molcel.2018.11.011)；[PMID 30606466](https://pubmed.ncbi.nlm.nih.gov/30606466/) |
| [6QZK](https://www.rcsb.org/structure/6QZK) | DNA-guided DNA cleavage at moderate temperatures by Clostridium butyricum Argonaute.；Nucleic Acids Res.；2019 | [DOI 10.1093/nar/gkz306](https://doi.org/10.1093/nar/gkz306)；[PMID 31069393](https://pubmed.ncbi.nlm.nih.gov/31069393/) |
| [7MXL](https://www.rcsb.org/structure/7MXL) | Targeting immunodominant Bet v 1 epitopes with monoclonal antibodies prevents the birch allergic response.；J.Allergy Clin.Immunol.；2022 | [DOI 10.1016/j.jaci.2021.05.038](https://doi.org/10.1016/j.jaci.2021.05.038)；[PMID 34126155](https://pubmed.ncbi.nlm.nih.gov/34126155/) |
| [8YE6](https://www.rcsb.org/structure/8YE6)、[8YE9](https://www.rcsb.org/structure/8YE9) | Inhibition mechanisms of CRISPR-Cas9 by AcrIIA25.1 and AcrIIA32.；Sci China Life Sci；2024 | [DOI 10.1007/s11427-024-2607-8](https://doi.org/10.1007/s11427-024-2607-8)；[PMID 38842649](https://pubmed.ncbi.nlm.nih.gov/38842649/) |
| [9HAC](https://www.rcsb.org/structure/9HAC)、[9HAD](https://www.rcsb.org/structure/9HAD)、[9HAE](https://www.rcsb.org/structure/9HAE)、[9HAF](https://www.rcsb.org/structure/9HAF) | One-shot design of functional protein binders with BindCraft.；Nature；2025 | [DOI 10.1038/s41586-025-09429-6](https://doi.org/10.1038/s41586-025-09429-6)；[PMID 40866699](https://pubmed.ncbi.nlm.nih.gov/40866699/) |
| [9HAG](https://www.rcsb.org/structure/9HAG) | Structural characterization of a designed beta barrel protein with a hydrophobic pore；To Be Published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |

## 其他

### 数据范围和限制

已验证目标公开组合包；完整研究数据获得仍为未完成，EMDB 图和逐条仪器明细没有在当前包。正式表应是定量/二元标签入口，ZIP 旧表和模型文件名不能直接当同一版本标签。

### 完整性与验收

payload 共 3 文件、14,924,160 bytes；同样排序 inventory SHA-256 为 `219e3f23cbf9df4c107050f8c774846ffb54715016648bf6779ce0f783996aa9`。独立审计要求 config 中目标文件集合与实际完全一致（允许 source README，保留上游自己的 README），拒绝 symlink、旁路 JSON/API/manifest、partial 文件或缺少任何可公开 PDB 层。PDF 页数/签名、XLSX 全部 worksheet、ZIP 全部 CRC 与安全成员均按文件类型核验；研究审计结果只保存本人 context，不发布为 raw sidecar。

上游 payload 文件身份；SHA-256 为获取后固定的本地值：

| payload 文件 | bytes | SHA-256 |
| --- | --- | --- |
| BindCraft_2025-08-27_Nature-SupplementaryData1.csv | 283408 | `c87fd6cd0a54fe57d840938be07449394abbd55318494c8cc0292b6417c16b4f` |
| BindCraft_2025-08-27_Nature-SupplementaryData2.xlsx | 99632 | `c47e007749f832d85f431a02811aec2ffb013616d41957a1ba7d0131c9155ac4` |
| DesignModels.zip | 14541120 | `81d427a4a907bf5ffa9996661edab49435d606ad6c7df546ce38dd0177ea66a3` |

### 许可和再分发边界

Zenodo record 的模型 ZIP 为 CC BY 4.0；Nature 正式主文 PDF 明示 CC BY-NC-ND 4.0，publisher 补充材料未发现独立更宽授权，不默认采用 Zenodo 许可。BindCraft 代码 MIT 只说明软件权利。本包在非商业研究归档中保留原字节、引用与分层许可，后续派生数据再分发需另核对各组成部分条款。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 212 个设计 | 正式 CSV：212 条完整 binder Sequence；ZIP：212 个真正模型 | 已包含 |
| 结合与定量亲和力 | 65 个 1、87 个 0、60 个空；20 个非空 Affinity_nM | 部分设计有测量，不是 212 个 KD |
| publisher 五份附件 | 3 PDF + CSV + XLSX；独立主文 PDF | 已包含 |
| 4 个新实验 PDB与参考输入 | 17 份原生 FASTA/mmCIF 对，含输入/商业/天然对照角色 | 已包含；非逐设计结构 |
| cryo-EM map、完整仪器 raw | 本次未取得 EMD-53510/53511 与逐条原始曲线 | 未获得完整研究范围 |
