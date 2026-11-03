---
- tags:
  - context
---

# SRC_R65_BID 数据说明

## 数据集身份

- `source_id`：`SRC_R65_BID`
- `source_version`：`snapshot-2009-10-30`
- 原作者或发布机构：Texas A&M University Department of Biochemistry & Biophysics 的 BID 团队（Tiffany B. Fischer、Jerry Tsai 等）；当前可复核突变子集由 Stefano Lise、Christopher Archambeau、Massimiliano Pontil 和 David T. Jones 整理发表

### 来源方背景

BID 团队在 2003 年论文中列出的 15 位作者均来自 Texas A&M University Department of Biochemistry & Biophysics，Jerry Tsai 为通讯作者，Tiffany Fischer与 Tsai 是数据库接收新蛋白条目的联系人。团队从原始科学文献中整理蛋白界面信息，并在 BID 中以表格、接触图和功能描述呈现；[OUP 正式页面](https://doi.org/10.1093/bioinformatics/btg163)记录了这一责任主体和数据库目标。

历史官网的 2003—2005 年页面显示，BID 持续汇编丙氨酸扫描与定点突变文献，并逐步扩充相互作用蛋白对。2009 年，University College London 的 Lise 等为热点评测从 BID 另行提取了一个小型子集，并在开放获取论文的 Additional file 4 中公开。当前 source version 同时保存历史官网的有限证据和这份可逐条复核的派生子集，责任主体分别在下文区分。

## 实验设计和数据口径

BID 没有开展一套统一的新实验。原团队从既有蛋白质相互作用研究中人工汇编界面、文献、结构和突变效应。历史首页说明其来源包含丙氨酸扫描和定点突变；默认详情页则把一对相互作用蛋白的 Gene ID、名称、物种、PDB ID、说明、野生型测量和文献组织在一起。当前保存的 10 个首页内容版本从“168 对、超过 1,100 个 mutations”增长到“467 对、超过 7,006 个 hot spots”。这些数字是各页面当时的整体规模声明，术语从 `mutations` 变化为 `hot spots`，且当前文件不含支撑全部规模声明的逐记录导出。

BID 对突变效应使用 `Strong`、`Intermediate`、`Weak`、`Negative`、`Negative-Strong`、`Negative-Intermediate`、`Negative-Weak` 和 `Insignificant` 分类。Lise 等指出，分类可能来自动力学或热力学实验，多数原 BID 条目只有动力学量，且原分类规则和跨实验一致性没有完整公开。少数条目给出结合自由能变化 ΔΔG；按照 2009 年论文的热点评测口径，ΔΔG 大于等于 2 kcal/mol 视为热点。

2009 年派生子集排除了蛋白质-肽相互作用，只保留具有扩展界面的蛋白质-蛋白质相互作用。Additional file 4 包含三张结构化表：Table S7 汇总 9 个 PDB 复合物及两侧链和突变数；Data set S2 给出 41 条丙氨酸突变；Table S8 汇总 TSVM 模型在两种标签口径下的 P、R、F1 和 MCC。41 行中有 19 行来自 1FAK，并带实测 ΔΔG；其余 22 行的 ΔΔG 为 `NA`。`TSVM score` 是 Lise 等模型产生的预测分数，正分表示预测 ΔΔG 大于等于 2 kcal/mol，不能作为 BID 的实验测量。

当前 41 行观察到 10 个 `Int`、10 个 `Str`、4 个 `Weak` 和 17 个 `Insg`。同一 PDB 内多行是同一复合物上的不同突变，不能作为独立复合物拆分。Table S7、Data set S2 和外部结构之间有两个需特别处理的差异：Data set S2 的 `1FO8` 经同文件 Table S7 和 RCSB 验证应连接 `1FOE`；1MQ8 的逐突变记录明确落在 chain B residue 206 Thr，但 Table S7 把该单条突变计入 protein 1 / chain A 一侧，后者仍缺少来源方说明。

## 论文原文

### BID 2003 数据库论文

- 标题：The binding interface database (BID): a compilation of amino acid hot spots in protein interfaces
- 作者：T. B. Fischer 等，J. Tsai 为通讯作者
- 发表来源：*Bioinformatics* 19(11), 1453–1454
- 归档文本版本：OUP 正式发表页面的元数据与摘要；PDF 全文未归档
- 发布日期：2003-07-22
- DOI：[10.1093/bioinformatics/btg163](https://doi.org/10.1093/bioinformatics/btg163)
- PMID / PMCID：PMID `12874065`；无 PMCID
- 正文在线入口：[Oxford Academic 正式页面](https://academic.oup.com/bioinformatics/article/19/11/1453/220366)
- 本地归档：PDF 全文未归档
- 期刊页面记录：`articles/BID_2003-07-22_Bioinformatics-PublicPage.html`，31.56 KiB（32,316 bytes），SHA-256 `03a4fe3abed623fca6eac09ca64398aa9c162cfd4727a934e9ede5dba2f39916`
- 文本许可：页面标注 © Oxford University Press 2003，未标明开放许可
- 补充材料：未发现该论文的补充材料

### 2009 BID 派生子集论文

- 标题：Prediction of hot spot residues at protein-protein interfaces by combining machine learning and energy-based methods
- 作者：Stefano Lise、Christopher Archambeau、Massimiliano Pontil、David T. Jones
- 发表来源：*BMC Bioinformatics* 10, Article 365
- 归档文本版本：BioMed Central / Springer Nature 正式发表版
- 发布日期：2009-10-30
- DOI：[10.1186/1471-2105-10-365](https://doi.org/10.1186/1471-2105-10-365)
- PMID / PMCID：PMID `19878545`；PMCID `PMC2777894`
- 本地文件：`articles/BID-derived_2009-10-30_BMC-Bioinformatics-FullText.pdf`
- 文件大小：797.38 KiB（816,522 bytes）
- SHA-256：`76661e215a071aecd5cac10e30cb930b5dbd1f97f0c70d42085a5c27abe27914`
- 文本许可：[Creative Commons Attribution 2.0](https://creativecommons.org/licenses/by/2.0/)
- 补充材料：`articles/BID-derived_2009-10-30_BMC-Bioinformatics-Additional-file-4.doc`，即包含 BID 说明、Table S7、Table S8 和 Data set S2 的上游文件；127.50 KiB（130,560 bytes），SHA-256 `793ff1d31bee3e67147e71536e8d744d7fe4a5f17d2d9dfc4622e0c1d43adc71`，上游文件名为 `12859_2009_3095_MOESM4_ESM.doc`

## 仓库内容

BID 的历史入口是 `http://tsailab.org/BID/`，当前已不能作为数据库导出端点使用。本版本通过 [Internet Archive CDX](https://web.archive.org/cdx/search/cdx?url=tsailab.org%2FBID%2F%2A&output=json&filter=statuscode%3A200&fl=timestamp%2Coriginal%2Cmimetype%2Cstatuscode%2Cdigest%2Clength&collapse=digest&limit=10000)核查到 80 个原始 URL、98 个去重内容快照；落盘范围为根页面全部 10 个不同内容快照，以及 2005-03-22 的 Protein G / IgG Fc（PDB 1FCC）详情页，用于固定首页规模变化和详情页 schema。

`source_version` 使用 `snapshot-2009-10-30`，日期来自包含 41 条 BID 派生记录的 BMC 正式论文及其 Additional file 4 的发布日期。历史官网页面的捕获时间为 2003-02-15 至 2005-11-09，属于选择性历史归档，不表示 2009-10-30 的原 BID 全库状态。

```text
snapshot-2009-10-30/
└── BID-historical-site/
    └── captures/
        ├── home-628de58da8/
        │   └── 10 个 HTML 内容快照
        └── getinfo-pone-1065200-ptwo-1065199-9a9a1c8555/
            └── 20050322233251.html
```

`BID-historical-site/` 共 11 个 HTML 文件、96.51 KiB（98,825 bytes）；确定性 inventory SHA-256 为 `9f9e425b94cfa1fafe38ec8d13cf33eebcd17b27aa4a484967d8d2466b4973b3`。可逐条使用的 41 条突变位于论文补充文件中，按项目规则随所属论文归档在 `articles/`。

## 数据结构

### BID 历史官网页面

`home-628de58da8/` 中每个文件名是 Internet Archive 的 14 位捕获时间。页面主体是数据库说明和当时的汇总规模；10 个文件是同一入口的不同时点表示，不能相加为记录数。当前观察到的规模序列为 168/1,100、245/1,500、285/2,727、341/4,172、405/5,514、455/6,417、455/6,417、458/6,535、464/6,748 和 467/7,006，前一个数为相互作用蛋白对，后一个数按页面原词为 mutations 或 hot spots。

`getinfo-.../20050322233251.html` 是一条默认详情视图，描述 Protein G 与 IgG Fc fragment。它包含两侧蛋白信息、共享 PDB 1FCC、相互作用说明、野生型 `Kd= 0.24 uM` 和 PMID `10452608`。页面存在 `Download Interactions` 链接，但该下载对象没有进入当前 Internet Archive 捕获集合。

### BID 派生突变子集

Additional file 4 是 OLE Compound File 格式的 Word 97—2003 `.doc`。文件按顺序包含 BID 口径说明、Table S7、Table S8 和 Data set S2。当前验收以原始 DOC 为准，没有在 raw 层转写为 CSV，也没有改正文件中的 PDB 或链计数文本。

Table S7 的 9 行以复合物为粒度；Data set S2 的 41 行以“一个 PDB author chain 上一个野生型残基被替换为 alanine”为粒度；Table S8 的 2 行是对全部 41 条记录的模型评测汇总。Data set S2 没有单独的突变后残基字段，来源说明全部为丙氨酸突变。

### 字段说明

**历史详情页字段（`20050322233251.html`）**

| 原始标签 | 原始表示、单位与来源 | 含义及特殊值 |
| --- | --- | --- |
| `Gene ID` | 两列字符串；文献/数据库注释 | Protein I 与 Protein II 的 NCBI protein 标识；示例为 `1065200`、`1065199` |
| `Protein Name` | 两列文本；人工或文献注释 | 两侧蛋白名称 |
| `Shift Information` | 两列文本；人工注释 | 原编号与页面使用编号的偏移；`-` 表示页面未给偏移 |
| `Organism` | 两列文本；人工或文献注释 | 两侧来源物种 |
| `Protein Data Bank ID` | 两列 PDB 链接 | 与蛋白对相连的结构标识；该页两侧均为 `1FCC` |
| `Protein Description` | 两列自由文本；文献汇编 | 两侧蛋白的结构和功能说明 |
| `Interaction Description` | 跨两列自由文本；文献汇编 | 相互作用界面及关键残基的叙述 |
| `Wild Type Info.` | 自由文本；实验文献值 | 野生型结合信息，原单位和格式保留；该页为 `Kd= 0.24 uM` |
| `Reference(s)` | PMID 链接列表 | 支撑该详情页的文献；该页为 `10452608` |

首页没有稳定表头；其可解析字段是捕获时间、页面自报的 interacting protein pair 数及 mutations/hot spots 数。捕获时间来自 Internet Archive，两个规模数字来自原 BID 页面正文。

Table S7（Additional file 4；9 个复合物）的字段如下：

| 原始字段 | 原始表示、单位与来源 | 含义及特殊值 |
| --- | --- | --- |
| `PDB ID` | 4 字符字符串；Lise 等从 BID 整理 | 复合物结构标识；当前表中为 9 个唯一值 |
| `Chain protein 1` | 大写 author chain ID 串 | protein 1 的一条或多条链，例如 `AC` 表示 A、C |
| `Chain Protein 2` | 大写 author chain ID 串 | protein 2 的一条或多条链，例如 `BD` 表示 B、D |
| `Number of mutations Protein 1` | 非负整数，单位为突变记录 | Data set S2 应落在 protein 1 一侧的条数；1MQ8 与逐条表存在差异 |
| `Number of mutations Protein 2` | 非负整数，单位为突变记录 | Data set S2 应落在 protein 2 一侧的条数 |

Table S8（Additional file 4；2 个评测口径）的字段如下：

| 原始字段 | 原始表示、单位与来源 | 含义及方向 |
| --- | --- | --- |
| `Hot spot identification` | 分类文本；模型评测定义 | `Str` 只把 Strong 作为热点；`Int or Str` 同时把 Intermediate 和 Strong 作为热点 |
| `P` | 0—1 浮点；模型评测派生 | precision，越高表示预测阳性中真热点比例越高 |
| `R` | 0—1 浮点；模型评测派生 | recall，越高表示真实热点被找回的比例越高 |
| `F1` | 0—1 浮点；模型评测派生 | precision 与 recall 的调和平均，越高越好 |
| `MCC` | 浮点；模型评测派生 | Matthews correlation coefficient，正向越高表示分类一致性越强 |

Data set S2（Additional file 4；41 条突变）的字段如下：

| 原始字段 | 原始表示、单位与来源 | 含义及特殊值 |
| --- | --- | --- |
| `Pdb id` | 4 字符字符串；从 BID 整理 | 结构标识；一行原样写作 `1FO8`，结构核验采用 `1FOE` |
| `Chain` | 单个大写 author chain ID | 突变所在 PDB author chain |
| `PDB residue number` | 整数字符串；PDB author 编号 | 突变位点编号，须和 `Pdb id`、`Chain` 联合解释 |
| `Residue type` | 单字母氨基酸代码 | 变为 alanine 前的野生型残基；41 行均与接受的 mmCIF 坐标一致 |
| `Effect of mutation` | BID 分类缩写；人工/文献注释 | 当前版本观察到的全部取值见下表 |
| `Observed ΔΔG (kcal/mol)` | 十进制数或 `NA`；实验值 | 结合自由能变化；数值越大表示丙氨酸突变越削弱结合；19 行有值、22 行为 `NA` |
| `TSVM score` | 有符号十进制数；模型预测 | Lise 等 Transductive SVM 分数；正值预测 ΔΔG 大于等于 2 kcal/mol |

**`Effect of mutation`（Data set S2；取值范围依据：当前 source version 扫描）**

| 原始取值 | 当前记录数 | 含义 |
| --- | ---: | --- |
| `Str` | 10 | BID 的 Strong 分类 |
| `Int` | 10 | BID 的 Intermediate 分类 |
| `Weak` | 4 | BID 的 Weak 分类 |
| `Insg` | 17 | BID 的 Insignificant 分类 |

BID 说明还定义了 `Negative`、`Negative-Strong`、`Negative-Intermediate` 和 `Negative-Weak`，但这四种值没有出现在当前 41 行派生子集中。

### 数据示例

以下为 Data set S2 中的真实行，保留原始标识和值：

| `Pdb id` | `Chain` | `PDB residue number` | `Residue type` | `Effect of mutation` | `Observed ΔΔG (kcal/mol)` | `TSVM score` |
| --- | --- | ---: | --- | --- | ---: | ---: |
| `1ES7` | `A` | 26 | `V` | `Int` | `NA` | -1.21 |
| `1FAK` | `T` | 20 | `K` | `Str` | 2.6 | 0.07 |
| `1FO8` | `B` | 41 | `S` | `Int` | `NA` | 0.31 |
| `1MQ8` | `B` | 206 | `T` | `Str` | `NA` | -0.49 |

每行是一条特定位点的丙氨酸突变。`1FO8` 是原 DOC 的写法；结构配对使用 1FOE chain B residue 41 Ser。1MQ8 这一行的 chain B 与坐标一致，但 Table S7 把该复合物的一个突变计入 protein 1 / chain A。

Table S8 的真实两行如下：

| `Hot spot identification` | `P` | `R` | `F1` | `MCC` |
| --- | ---: | ---: | ---: | ---: |
| `Str` | 0.31 | 0.40 | 0.35 | 0.10 |
| `Int or Str` | 0.77 | 0.55 | 0.61 | 0.38 |

这两行是同一 41 条记录在不同热点定义下的 TSVM 汇总指标，不是两条结合实验。

## PDB 数据库

PDB 锚点来自 Additional file 4 的 Table S7 和 Data set S2。9 个接受的复合物均保存 RCSB 直接下载的完整 entry FASTA 和完整 mmCIF；FASTA 保留 RCSB 原始字节，未做选链或改写 header。链角色沿用 Table S7 的 `protein 1` / `protein 2`，没有根据结构名称另行改写生物学角色。

Data set S2 将一行写作 `1FO8` chain B residue 41 Ser，而 RCSB 1FO8 只有 author chain A，条目为 N-acetylglucosaminyltransferase I；同文件 Table S7 写作 `1FOE`。RCSB 1FOE 是 RAC1–TIAM1 复合物，并具有 chain B residue 41 Ser，因此接受 1FOE、拒绝 1FO8。raw DOC 中的原值保持不变。应用这一项文献内纠错后，41 条 `Chain`、`PDB residue number` 和 `Residue type` 均与接受 mmCIF 的 `_atom_site` author 编号和残基类型一致。

| PDB ID | Table S7 protein 1 / protein 2 chains | 突变数（protein 1 / protein 2） | FASTA 大小与 SHA-256 | mmCIF 大小与 SHA-256 |
| --- | --- | --- | --- | --- |
| `1ES7` | `AC` / `BD` | 3 / 0 | 355 bytes；`7a6fe85daee56c916e2435d499889ae96ea28449528268361f0762689c913b50` | 336.18 KiB（344,245 bytes）；`b21dad1f0a44ef9337bd81c39ebb6217842102e850f312b473222239a520595d` |
| `1FAK` | `HL` / `T` | 0 / 19 | 959 bytes；`d521e2f5ef286ab6d7cb1b79e1cea392a5f9000f628978e6a7cdbbe30777176f` | 551.00 KiB（564,228 bytes）；`2a4a1d2742f3a07df09caf90e666b11c765cab1fc5cc7c80b976ae723a7d714e` |
| `1FE8` | `A` / `LH` | 4 / 0 | 883 bytes；`90952e87e64a6262143b699c030c8b5e2724f722aca70836128a62fdb44b74c1` | 1.49 MiB（1,563,223 bytes）；`e026bf4ce47c9d65e49e867cd2f96e44b9d14bfc7f7fbe4ec095b04e45af967e` |
| `1FOE` | `A` / `B` | 0 / 1 | 744 bytes；`dbbbecd481f3d0694ea4a7bb9199707cbbfc7508db5c3d3378375e1265fa5ee8` | 1.77 MiB（1,854,751 bytes）；`8dfab11f3b9ae48058e5cdf28641cdc63419c2303a2d771bd30c9f860448226b` |
| `1GL4` | `A` / `B` | 7 / 0 | 538 bytes；`05ffc3ca55b76d0003ff601a3a077ea6ee50fbde0975a9d5b0bd2ef7e3452e0e` | 356.85 KiB（365,416 bytes）；`198508e7bc9a981b70a55d8ec7dc7cea31124d955c2b810bc6c1dd987f067ca9` |
| `1MQ8` | `A` / `B` | 1 / 0 | 601 bytes；`6c5d1728dc3d001cd11a45abf0904796137be6ec93db84911564560eda1f5961` | 649.22 KiB（664,803 bytes）；`725753c1021025bf127b1deffcfa6e1585b93d6af71f209e44a11885ee1f3738` |
| `1NFI` | `AB` / `F` | 0 / 2 | 790 bytes；`6e1ebd5e1cae556597fda230d088f19f81fb641825320cc78d844f1c0ff97442` | 979.50 KiB（1,003,010 bytes）；`f311678213e3b513278430c7668bd3c0ac3b9eb14421efb8cacfe15f349844b3` |
| `1NUN` | `A` / `B` | 3 / 0 | 523 bytes；`022ffb455c90286f414f3641f877419cae93d11c43722e1a970a0882df6143f6` | 342.59 KiB（350,817 bytes）；`5daf36b04b3fc8f3b119730b4ccca910cff394729dce68985f84fb8b71f60e90` |
| `1UB4` | `A` / `C` | 0 / 1 | 305 bytes；`846f42afcec50a3277ee4c9a9dd62008afb05c115b9b99ed0d5d2d9f85159d6b` | 289.61 KiB（296,559 bytes）；`0ddfc9cb6369cf509472bde6e4021cb21be342bcc5544a2b498c5ee630519e89` |

`pdb/` 共 18 个文件、6.69 MiB（7,012,750 bytes）：9 个 FASTA 合计 5,698 bytes，9 个 mmCIF 合计 6.68 MiB（7,007,052 bytes）。确定性 inventory SHA-256 为 `57796f6d0efc2ca99158a13b8535c8e1e7e71cec6cdd24d75f21e1a66f408032`。每个 FASTA 的 canonical polymer entities 与同一 mmCIF 的 `_entity_poly.pdbx_seq_one_letter_code_can` 完全一致，所有接受链均存在，所有 mmCIF 均含坐标。结构覆盖强度是“派生子集逐复合物且逐突变坐标连接”；它不覆盖原 BID 自报的全部 467 个蛋白对或 7,006 个 hot spots。

## 采集过程记录

1. 2026-09-22 首次核查 R65。原论文给出的 `http://tsailab.org/BID/` 已不能提供数据库导出，期刊页面只有摘要和聚合规模；当时仅将 OUP 页面写入 `.staging/snapshot-2003-07-22/`，并将任务保持为 blocked。该日期来自论文发表，不是可验证的数据版本，未发布。
2. 2026-09-25 扩展检索正式论文、PubMed/Europe PMC、Springer Nature 补充材料和 Internet Archive。CDX 返回 80 个历史 URL、98 个不同内容快照；Lise 等 2009 年正式论文的 Additional file 4 明确包含从 BID 提取的 9 个复合物、41 条突变，形成可固定的公开部分包。
3. 2026-09-25 以 BMC 论文及其数据附件的发布日期建立 `.staging/snapshot-2009-10-30/`。从 Springer Nature 取得 816,522-byte 正式 PDF 和 130,560-byte Additional file 4；从旧 staging 重新核验并纳入 32,316-byte OUP 页面。三者逐文件字节数和 SHA-256 均通过。
4. 2026-09-25 Internet Archive 的并发 replay 在下载 20 余项后出现 TLS 中断和长时间重试。停止并发后重新界定最小可解释归档：保留全部 10 个根页面内容版本及与 2009 年说明直接关联的 1FCC 详情示例，删除其余试下载文件和空目录；最终 11 个文件均按固定 capture timestamp、原始 URL、字节数和 SHA-256 配置复核。
5. 2026-09-25 为读取上游 Word 97—2003 文件，将 Debian `antiword 0.37` 解包到个人隔离工具目录，没有修改系统 Python 或原 DOC。独立审计得到 Table S7 的 9 个复合物、Data set S2 的 41 行、四种观察标签和 19/22 条 ΔΔG 有值/缺失分布。
6. 2026-09-25 审计 PDB 时发现 Data set S2 的 `1FO8` 与 Table S7 冲突。RCSB API 与 mmCIF 显示 1FO8 缺少 chain B，而 1FOE chain B residue 41 为 Ser；配置据此拒绝 1FO8 并接受 1FOE。随后下载 9 个完整 entry FASTA/mmCIF 对，验证 canonical entities、author chains、坐标和 41 条突变残基。另记录 1MQ8 的 Table S7 链计数差异，不改 raw 文件。
7. 2026-09-25 生成本地 README 并同步至 staging，执行固定 markdownlint、配置化 acquisition 重跑、独立语义审计、workspace 范围检查和原子发布。旧的 provisional staging 只在新版本发布并复核后清理。

## 参考文献

- Fischer TB, et al. [The binding interface database (BID): a compilation of amino acid hot spots in protein interfaces](https://doi.org/10.1093/bioinformatics/btg163). *Bioinformatics*. 2003;19(11):1453–1454.
- Lise S, Archambeau C, Pontil M, Jones DT. [Prediction of hot spot residues at protein-protein interfaces by combining machine learning and energy-based methods](https://doi.org/10.1186/1471-2105-10-365). *BMC Bioinformatics*. 2009;10:365.
- [Springer Nature Additional file 4 原始下载](https://media.springernature.com/original/springer-static/esm/art%3A10.1186%2F1471-2105-10-365/MediaObjects/12859_2009_3095_MOESM4_ESM.doc).
- [BID 2005-11-09 历史首页](https://web.archive.org/web/20051109230834id_/http://tsailab.org:80/BID/)；[1FCC 详情页](https://web.archive.org/web/20050322233251id_/http://tsailab.org:80/BID/getinfo.php?pone=1065200&ptwo=1065199).
- RCSB PDB entries：[1ES7](https://www.rcsb.org/structure/1ES7)、[1FAK](https://www.rcsb.org/structure/1FAK)、[1FE8](https://www.rcsb.org/structure/1FE8)、[1FOE](https://www.rcsb.org/structure/1FOE)、[1GL4](https://www.rcsb.org/structure/1GL4)、[1MQ8](https://www.rcsb.org/structure/1MQ8)、[1NFI](https://www.rcsb.org/structure/1NFI)、[1NUN](https://www.rcsb.org/structure/1NUN)、[1UB4](https://www.rcsb.org/structure/1UB4)。
- [RCSB PDB Usage Policies](https://www.rcsb.org/pages/usage-policy).

## 其他

### 数据范围和限制

当前版本是可验证的历史公开部分包。它提供 BID 首页随时间变化的规模证据、一条原官网详情页、2009 年公开的 41 条 BID 派生突变，以及这 9 个复合物的 PDB 数据。它不含原 BID 自报的全部蛋白对、交互下载文件、全部突变值、全部参考文献映射或 wikiBID 内容。

41 条记录经过 Lise 等针对“扩展蛋白质-蛋白质界面”的选择，排除了蛋白质-肽相互作用，因此存在明确选择偏差。BID 分类混合动力学与热力学来源；只有 1FAK 的 19 条记录带 ΔΔG。分类标签适合按来源原口径复现，不应直接解释为同一测量条件下的连续亲和力标签。

### 完整性与验收

历史 payload 共 11 个 HTML，论文区共 3 个文件；两部分合计 14 个文件、1.03 MiB（1,078,223 bytes），确定性 inventory SHA-256 为 `55e200e32efca14fadf7008d85d269835991b096d437cf157c9d61ec7d472084`。PDF 可解析为 17 页并含题名、DOI、许可和 Additional file 4 说明；DOC 通过 OLE 文件头、内部文本、antiword 表格解析、行数和值域检查；历史页面逐页验证标题、规模数字及 1FCC 详情字段。

PDB 共 18 个文件、9 个成对条目，FASTA/mmCIF entity 序列、ID、链和坐标均通过独立检查。`1FO8` 到 `1FOE` 的纠错只影响外部结构映射，未改写上游 DOC。发布目录不包含 API 响应、临时 inventory、转换文本、partial 文件或旁路 manifest。

### 许可和再分发边界

2009 年 BMC 正式论文明确采用 CC BY 2.0；当前保存的 Additional file 4 是该论文由 Springer Nature 提供的电子补充材料，使用时保留论文引用与署名。2003 年 OUP 页面标注 © Oxford University Press 2003，未标出开放许可；当前只保存公开页面，不声称其文本可按开放许可再利用。

原 BID 历史页面没有发现覆盖数据库记录的独立许可。页面当年称数据库可免费访问，但“免费访问”没有给出商用、衍生或再分发授权。现有公开入口没有发现与本次按原样保存历史页面明确冲突的条款，因此该许可缺口不阻塞此部分包接入；超出研究存档的再利用仍需核实权利。Internet Archive 仅承担历史网页保存和 replay，未被视为原数据发布方。

RCSB 直接下载的 PDB archive 数据文件按 [CC0 1.0](https://www.rcsb.org/pages/usage-policy)提供；原结构作者及 RCSB PDB 仍应按其引用政策署名。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 2003 年论文：170 个相互作用蛋白对、超过 1,300 个突变 | OUP 正式页面摘要 | 规模声明已归档，逐记录数据未取得 |
| 2005 年历史首页：467 个相互作用蛋白对、超过 7,006 个 hot spots | 2005-11-09 原站捕获 | 规模声明已归档，逐记录数据未取得 |
| Internet Archive CDX：80 个 URL、98 个不同内容快照 | CDX 查询与固定 capture metadata | 当前选择性保存 10 个首页版本和 1 个详情页 |
| 2009 年 Additional file 4：9 个复合物、41 条 BID 派生突变 | 原始 DOC 的 Table S7 与 Data set S2 | 已完整取得并通过语义验收 |
| 41 条记录中的 1FAK 含 19 个 ΔΔG | Data set S2 | 19 个数值完整，其他 22 行原样为 `NA` |
| 派生子集的结构锚点 | Table S7、Data set S2 与 RCSB | 9 个有效 FASTA/mmCIF 对完整；1FO8 按证据连接 1FOE |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-25；不阻塞当前部分包，阻塞完整 BID 获得）：原 BID 全库导出、完整记录清单和 wikiBID 对应版本仍未取得。已核实原站失效、CDX 仅有不完整抓取、2009 年文件只含 41 条选择性子集；当前按部分覆盖发布并保留历史规模证据。下一步是从原维护团队、Texas A&M 机构存档或带来源链的正式档案取得完整导出、版本日期和对象清单，取得后建立新的 source version，而不覆盖本快照。
- `Q02`（最近更新：2026-09-25；不阻塞当前部分包，影响 2003 年方法全文复核）：OUP 的 2003 正式 PDF 路由在当前环境返回 HTTP 403，Europe PMC 标记该记录无可用 PDF/补充文件。已归档 OUP 正式页面、摘要、书目信息和 DOI，并以 2009 年开放全文解释派生数据。下一步是取得可核验且许可允许归档的 OUP 正式 PDF或作者版本，并比对正文后补入 `articles/`；关闭条件是文件版本、字节数、hash 和文本身份均通过验证。
- `Q03`（最近更新：2026-09-25；不阻塞当前部分包，影响进一步再利用）：原 BID 数据和历史网页没有独立许可说明。已区分 BMC CC BY 2.0、OUP © 2003、原 BID 页面及 RCSB CC0 的对象范围；当前按公开入口保存原样材料，不把许可沉默解释为商用或衍生授权。下一步是获得原维护方或机构档案的明确条款；关闭条件是许可文本能对应到具体 BID 数据对象和再分发范围。
- `Q04`（最近更新：2026-09-25；不阻塞发布，影响 1MQ8 的 protein-side 分组）：Table S7 将 1MQ8 的一个突变计入 protein 1 / chain A，Data set S2 则写 chain B residue 206 Thr，后者与 1MQ8 mmCIF 一致。当前逐突变使用 Data set S2 的 chain B，汇总表仍原样保留 1/0。下一步是查找作者勘误、原 BID 条目或原维护者确认；关闭条件是取得能解释该计数归属的一手证据。
