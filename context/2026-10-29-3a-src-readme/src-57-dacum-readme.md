---
tags:
  - context
---

# SRC_R57_DACUM 数据说明

## 数据集身份

- `source_id`：`SRC_R57_DACUM`
- `source_version`：`snapshot-2019-03-08`
- 原作者或发布机构：Cunliang Geng、Anna Vangone、Alexandre M. J. J. Bonvin；HADDOCK 作者团队

### 来源方背景

DACUM 出自 Utrecht University 的 Bonvin 计算结构生物学团队。团队长期结合结构和生化数据研究生物分子相互作用，并开发广泛使用的 [HADDOCK 复合物建模软件](https://ubc.uu.nl/computational-structural-biology/)。负责人 Alexandre Bonvin 自 2009 年起任计算结构生物学教授，曾任 Bijvoet Centre 科学主任；[乌得勒支大学介绍](https://www.uu.nl/en/news/alexandre-bonvin-new-scientific-director-of-the-bijvoet-centre)记载 HADDOCK 已被世界各地众多研究者使用。DACUM 将这一团队的结构建模经验用于梳理突变亲和力实验与预测方法之间的关系。

## 实验设计和数据口径

DACUM 是 SKEMPI 经清理得到的蛋白复合物突变亲和力变化汇编，不是新开展的单一实验。作者仓库说明先汇集文献实验，再统一单位、处理突变编号和结构区域，按实验方法考察预测器表现。记录粒度是一条复合物单点突变记录；本表两种 Mutation 字段均未含分号/逗号多突变列表。多条记录共享相同野生型、PDB 或原始文献。两个版本均有 1,872 个 SKEMPI_ID，147 个 Protein 编码和 147 个唯一 PDB，不能把两个版本相加为独立样本。

1.1 的 Kd_mut/Kd_wt 是实验解离常数（M，越小结合越强）；dG、ddG 是由亲和力得到的自由能量（kcal/mol）。方向为 ΔΔG = ΔG_mut − ΔG_wt，正值表示突变使结合减弱。用 R = 0.0019872 kcal/(mol·K) 和 Temperature（K）核对 R·T·ln(Kd_mut/Kd_wt)，最大绝对差 0.045985 kcal/mol，2 条超过 0.03、无条超过 0.1；保留上游舍入值，不重算 raw。所有 Kd、ddG、Temperature 字段均有数值，不能据此推断每条记录没有实验误差或检测边界。

15 个 Method 类别来自不同测定方式，SPR 有 357 条，ITC 有 58 条，ELISA 有 24 条；完整计数见下表。Hold_out_type 的 AB 有 222 条、PI,AB 有 79 条，共 301 条带 AB 标记，但这不是 301 组新抗体实验。PI 有 844 条，空值 727 条。构建训练/验证切分时应考虑共享 Protein、野生型、突变组合、Reference 及 SKEMPI/AB-Bind 等上游重叠。

四个动力学字段各缺失 1,489 条（383 条非空），四个焓/熵字段各缺失 1,789 条（83 条非空）；空单元格表示没有公开该值，不是零。Notes 缺失 800 条、Notes_method 缺失 1,848 条。没有统一 sensorgram、测序事件、重复测量明细或完整突变体序列；变体来源及编号应按原始 Mutation 字符串与文献理解，不扩展为 SKEMPI 的其他多突变记录。已读取机构仓储正式版的 Methods、数据下载说明、Table I/II 和 Fig. 1–3 captions，以及六页合订 Supplementary material 中的 Table S1–S3 和 Figure S1–S2：作者从 SKEMPI 1.1 选择仅单点且具有唯一实验亲和力值的记录，人工核对原始文献方法，纠正 44 个误报值；将 COR/SUP/RIM 合并为 ITF、INT/SUR 合并为 NIF。论文报告 1,580 条 ITF 与 292 条 NIF，15 种方法来自 119 篇引用。HADDOCK/mCSM 的计算评分属于论文评估流程，不等于这两份 CSV 均公开了每条预测分数或建模输出；部分按方法训练后在同一组报告的性能不能当独立测试。

| Method 原始编码 | 记录数 |
| --- | --- |
| IASP | 190 |
| SFFL | 113 |
| SPR | 357 |
| IAFL | 27 |
| FL | 312 |
| ITC | 58 |
| RA | 102 |
| IAGE | 7 |
| IARA | 50 |
| EMSA | 6 |
| SFSP | 10 |
| SP | 564 |
| CSPRIA | 43 |
| ELFA | 9 |
| ELISA | 24 |

## 论文原文

- 标题：Exploring the interplay between experimental methods and the performance of predictors of binding affinity change upon mutations in protein complexes
- 作者：Cunliang Geng、Anna Vangone、Alexandre M. J. J. Bonvin
- 载体与版本：Protein Engineering, Design and Selection 29(8), 291–299；Utrecht 仓储公开的 Publisher version，10 页（含机构封面）
- 发布日期：PDF Advance Access：2016-05-11；机构卷期：2016-08；publisher 网页：2016-07-20；Europe PMC firstPublicationDate：2016-06-09。保留各字段差异，不推断同一事件。
- DOI：10.1093/protein/gzw020
- PMID / PMCID：PMID 27284087；未找到 PMCID，已从作者机构取得正式版全文
- 本地文件：`articles/DACUM_2016-05-11_PEDS-PublisherVersion.pdf`
- 文件大小：3.53 MiB（3,706,380 bytes）
- SHA-256：`8fb5e8b298ff6cf5f8a689a3db03c80f8dbb11d3baefc29f503b9ff69a9cecc8`
- 文本许可：PDF 明示 © The Author 2016 / OUP All rights reserved；机构记录标作 Taverne，公开访问不代表改授 CC BY；保留权利，不作开放再分发声明
- 补充材料：`articles/DACUM_2016-05-11_PEDS-SupplementaryMaterial.pdf`，6 页，657.87 KiB（673,657 bytes），SHA-256 `e72319755c7a163d75d13e9235b10e79fdb92ab190fb6325fe7f99264b39ae44`；这是一个合订附件，完整包含 Table S1–S3 与 Figure S1–S2，并非五个独立文件

## 仓库内容

一手入口为 [作者固定仓库](https://github.com/haddocking/DACUM/tree/7fb4d77a97030f36921d26c6b4f66c0d870e7641)。commit `7fb4d77a97030f36921d26c6b4f66c0d870e7641`、tree `6be520c8966efc08d0176c56877a9e34929c6ee6`，commit 日期 2019-03-08 决定目录名 `snapshot-2019-03-08`，不是本次获取日期。四个普通 Git blob 全部保存；tree 没有 submodule、符号链接或 LFS 指针。这里是完整四文件 commit 快照，不包括外链 SKEMPI 全库；论文正式版另归档于 articles，不混入仓库 payload。

```text
snapshot-2019-03-08/
└── DACUM/
    ├── DACUM_1.0.csv
    ├── DACUM_1.1.csv
    ├── LICENSE
    └── README.md
```

表格、归档与其记录关系见数据结构；上游说明、许可或嵌入资源保留原始内容。

## 数据结构

### 版本与记录关系

两个 CSV 都以分号分隔，UTF-8 可解码。1.0 为 6 列，1.1 为 28 列；两版 SKEMPI_ID 集合相同且各自唯一。1.0 保留原始 `Rerference` 拼写和 Unicode `∆∆G(kcal/mol)` 字段，不能照论文或新版本改名覆盖上游文件。1.1 的 cleaned 与 PDB 编号是两套坐标，位置不能直接混用。

1.0 全部字段：`SKEMPI_ID`、`∆∆G(kcal/mol)`、`Position`、`Method`、`Rerference`、`Comments`。

### 字段说明

| 1.1 原始字段 | 原始类型 | 含义 | 空值数 |
| --- | --- | --- | --- |
| `SKEMPI_ID` | CSV 字符串，如 `1CSE_E_I_LI45G` | SKEMPI 记录连接键，本表唯一；不是跨所有来源的全局实验 ID | 0 |
| `Protein` | CSV 字符串 | PDB_结合方1作者链组_结合方2作者链组；共享结构连接键 | 0 |
| `Mutation_PDB` | CSV 字符串 | 单点突变编码；PDB 与 cleaned 编号不同，保留原始字符串 | 0 |
| `Mutation_cleaned` | CSV 字符串 | 单点突变编码；PDB 与 cleaned 编号不同，保留原始字符串 | 0 |
| `Location` | CSV 字符串 | 上游结构区域/位置注释，非独立实验标签 | 0 |
| `Position` | CSV 字符串 | 上游结构区域/位置注释，非独立实验标签 | 0 |
| `Kd_mut (M)` | CSV 数字文本，可解析为浮点数 | 实验解离常数，M；越小结合越强 | 0 |
| `Kd_wt (M)` | CSV 数字文本，可解析为浮点数 | 实验解离常数，M；越小结合越强 | 0 |
| `dG_mut (kcal mol^(-1))` | CSV 数字文本，可解析为浮点数 | 亲和力派生自由能，kcal/mol；ddG 为突变减野生型 | 0 |
| `dG_wt (kcal mol^(-1))` | CSV 数字文本，可解析为浮点数 | 亲和力派生自由能，kcal/mol；ddG 为突变减野生型 | 0 |
| `ddG (kcal mol^(-1))` | CSV 数字文本，可解析为浮点数 | 亲和力派生自由能，kcal/mol；ddG 为突变减野生型 | 0 |
| `Temperature` | CSV 数字文本，可解析为浮点数 | 测定温度，K | 0 |
| `Method` | CSV 字符串 | 上游方法分类代码；跨方法不可假定同一测量误差 | 0 |
| `Hold_out_type` | CSV 字符串 | 上游切分类型或同源蛋白组注释；不是训练独立性的证明 | 727 |
| `Hold_out_proteins` | CSV 字符串 | 上游切分类型或同源蛋白组注释；不是训练独立性的证明 | 0 |
| `Protein 1` | CSV 字符串 | 结合方名称；复合物可含酶抑制剂等非抗体体系 | 0 |
| `Protein 2` | CSV 字符串 | 结合方名称；复合物可含酶抑制剂等非抗体体系 | 0 |
| `kon_mut (M^(-1)s^(-1))` | CSV 数字文本，可解析为浮点数 | 缔合速率常数，M^(-1)s^(-1)，非空 383 条 | 1489 |
| `kon_wt (M^(-1)s^(-1))` | CSV 数字文本，可解析为浮点数 | 缔合速率常数，M^(-1)s^(-1)，非空 383 条 | 1489 |
| `koff_mut (s^(-1))` | CSV 数字文本，可解析为浮点数 | 解离速率常数，s^(-1)，非空 383 条 | 1489 |
| `koff_wt (s^(-1))` | CSV 数字文本，可解析为浮点数 | 解离速率常数，s^(-1)，非空 383 条 | 1489 |
| `dH_mut (kcal mol^(-1))` | CSV 数字文本，可解析为浮点数 | 结合焓，kcal/mol，非空 83 条 | 1789 |
| `dH_wt (kcal mol^(-1))` | CSV 数字文本，可解析为浮点数 | 结合焓，kcal/mol，非空 83 条 | 1789 |
| `dS_mut (cal mol^(-1) K^(-1))` | CSV 数字文本，可解析为浮点数 | 结合熵，cal/(mol·K)，非空 83 条 | 1789 |
| `dS_wt (cal mol^(-1) K^(-1))` | CSV 数字文本，可解析为浮点数 | 结合熵，cal/(mol·K)，非空 83 条 | 1789 |
| `Reference` | CSV 字符串 | 上游文献引用键；需按原作者引用解析 | 0 |
| `Notes` | CSV 字符串 | 原作者备注；空值不代表没有实验限制 | 800 |
| `Notes_method` | CSV 字符串 | 原作者备注；空值不代表没有实验限制 | 1848 |

1.0 的 `SKEMPI_ID` 为含 PDB、链与突变编码的字符串连接键；`∆∆G(kcal/mol)` 为亲和力派生的浮点数字文本，正值表示结合减弱；`Position`、`Method`、`Rerference`、`Comments` 为上游位置、方法、文献与备注字符串。两版都保留空字段；不把空备注或未给出的检测界限解释为零。

### 数据示例

实际首条记录摘录；一次突变与野生型对照共享一个参考复合物：

| 字段 | 原始值 |
| --- | --- |
| SKEMPI_ID | `1CSE_E_I_LI45G` |
| Protein | `1CSE_E_I` |
| Mutation_PDB | `LI45G` |
| Mutation_cleaned | `LI38G` |
| Location | `COR` |
| Kd_mut (M) | `5.26e-11` |
| Kd_wt (M) | `1.12e-12` |
| ddG (kcal mol^(-1)) | `2.25e+00` |
| Temperature | `294` |
| Method | `IASP` |
| Reference | `9048543` |

## PDB 数据库

逐行连接通过 Protein 的 PDB 与 author-chain 编码。147 个唯一 PDB 的完整 entity FASTA 与完整 mmCIF 均已取得；所有上游链组在 mmCIF `_entity_poly.pdbx_strand_id` 中存在。多记录共享一份 PDB，本任务没有生成逐突变体结构或重建突变体全长序列。mmCIF 中构建体/缺失残基和 cleaned 编号仍需在 processed 阶段严格映射，存在链不等于逐残基突变编号已验证。

例如 `1CSE_E_I` 对应作者链 E/I；FASTA 保存该条目全部 polymer entity，而非截取链序列或删除配体。坐标保留所有原子、模型和伴侣。

获取/核验日期 2026-09-18。每个编号使用 RCSB `https://www.rcsb.org/fasta/entry/<PDB_ID>/download` 与 `https://files.rcsb.org/download/<PDB_ID>.cif`。校验 FASTA entity ID 集合及全序列与 mmCIF canonical entity 全序列严格相等，并核对 entry.id、非空原子坐标和 author-chain。共 147 个完整对，294 个文件，67.27 MiB（70,541,683 bytes）。按相对路径排序拼接 `relative_path<TAB>bytes<TAB>sha256<LF>` 后 inventory SHA-256 为 `a8d757b73ac1216c6f81f5b1a441f1942e64756c771ceeb28d2d9c0dc7a9001f`。

## 采集过程记录

1. 2026-09-18：读取项目/开发者身份、执行清单与一手来源；由配置读取共享存储根，代码和文档只写本人 workspace。
2. 固定上游版本并在对应 `.staging/snapshot-2019-03-08` 下载，使用断点续传、HTTP 长度及可得的官方校验；遇到环境直连失败采用现有 HTTP 路由回退。
3. 初轮 Utrecht research-portal 的 `Exploring.pdf` 与 `pre_print.pdf` 返回 403，publisher PDF 与补充入口也受访问限制。2026-09-18 从当前 DSpace handle `1874/337454` 取得机构公开正式版，核验标题、作者、DOI和页码，并完整读取 Methods、数据下载说明、主表与图 captions。正式 PDF 明示 Advance Access 2016-05-11，机构卷期为 2016-08，publisher 页面为 2016-07-20，Europe PMC firstPublicationDate 为 2016-06-09；分别保留元数据含义，不自行统一日期。2026-09-19 再查时，DSpace ORIGINAL bundle 仅有 `pre_print.pdf` 和 `Exploring.pdf`；预印本仍只引用 SI–SIII/S1–S2，未内嵌附件。OUP issue 的 Supplementary data 链接匿名跳转到 `article-minimal/2462288`，响应标记 `UserHasAccess=False` 且没有附件清单；Crossref、Unpaywall、Internet Archive/Arquivo 只定位主文或无 capture。因此不用作者 CSV 或重算图表冒充原附件。结构下载曾出现 2VLJ TLS/连接错误；重试后所有 147 对文件通过 entity 序列核验。
4. 2026-09-20：用户从 OUP 论文页的 Supplementary data 区域人工取得 `gzw020supp.pdf`。独立检查 PDF 魔数、EOF、六页解析与逐页渲染，标题和作者与 DOI `10.1093/protein/gzw020` 一致；附件完整包含 Figure S1–S2 和 Table S1–S3。按内容身份归档为 `articles/DACUM_2016-05-11_PEDS-SupplementaryMaterial.pdf`，原始字节未改写。该补充材料关闭附件缺口，但不补足未公开的 sensorgram、重复测量明细或其他底层实验原始记录。
5. 解析全部实际表/归档，独立核对文件集合、完整格式、哈希与 PDB 两层，保留上游差异。
6. README 工作稿每次写入立即同步共享目录；发布器复核固定格式、同步 hash 和 pinned markdownlint 0 errors 后原子发布。已于 2026-09-18T20:47:47.593268+00:00 从 staging 原子发布，当前为 final；本次修订 README 在同一次写入中覆盖同步 final，并重新审计和 lint。

依据来源、可核验日期、载体和附件角色整理 opaque 名称，改名前后 bytes/SHA-256 相同；中间名保留实际修订历史。正式版名称日期取 PDF 明示的 Advance Access 2016-05-11。具体映射如下：

| 上游原名 | 中间名（如有） | 本地相对路径 | 核对 大小 | 核对 SHA-256 |
| --- | --- | --- | --- | --- |
| Exploring.pdf | DACUM_2016-08_PEDS-PublisherVersion.pdf | articles/DACUM_2016-05-11_PEDS-PublisherVersion.pdf | 3.53 MiB（3,706,380 bytes） | `8fb5e8b298ff6cf5f8a689a3db03c80f8dbb11d3baefc29f503b9ff69a9cecc8` |
| gzw020supp.pdf | 无 | articles/DACUM_2016-05-11_PEDS-SupplementaryMaterial.pdf | 657.87 KiB（673,657 bytes） | `e72319755c7a163d75d13e9235b10e79fdb92ab190fb6325fe7f99264b39ae44` |

2026-09-18 逐条复审后：补齐全部已取得 PDB 的条目和原始结构论文主引用，以及涉及的上游汇编/对照引用。取得并归档机构正式版，阅读 Methods、数据说明与主表/图 captions，补齐论文 bytes/hash 和原始字段类型。2026-09-20 补入并验收独立 Supplementary，论文附件缺口关闭；底层实验原始记录仍未公开，不宣称 complete-study acquisition。

2026-09-22 复核两版 CSV 首行与 `SKEMPI_ID` 全列，发现旧字段说明误写为“整数字符串”；原字段实际为 `1CSE_E_I_LI45G` 一类复合物/突变编码。已修正字段类型说明，原始 CSV 未改动。

2026-09-22 按正式版 PDF 所载 Advance Access 日期，将附件从 `DACUM_2016_PEDS-SupplementaryMaterial.pdf` 改名为 `DACUM_2016-05-11_PEDS-SupplementaryMaterial.pdf`。改名前后 673,657 bytes 与 SHA-256 均一致，正文和附件内容未改写。

2026-09-22 重新逐项计算 147 对 RCSB FASTA/mmCIF 的 294 文件 inventory SHA-256，与“PDB 数据库”记录一致；两版 CSV 的 1,872 条 `SKEMPI_ID` 均为唯一的非纯数字文本。

## 参考文献

- [固定仓库](https://github.com/haddocking/DACUM/tree/7fb4d77a97030f36921d26c6b4f66c0d870e7641)
- [正式出版页](https://academic.oup.com/peds/article-abstract/29/8/291/2462288)
- [作者机构记录](https://research-portal.uu.nl/en/publications/exploring-the-interplay-between-experimental-methods-and-the-perf/)
- [机构公开正式版与预印本](https://dspace.library.uu.nl/handle/1874/337454)
- [机构许可说明](https://www.uu.nl/en/university-library/license-and-reuse-conditions)
- [Moal & Fernández-Recio (2012), SKEMPI: a Structural Kinetic and Energetic database of Mutant Protein Interactions and its use in empirical models](https://doi.org/10.1093/bioinformatics/bts489)

### PDB 条目与原始结构论文

以下主引用直接读取归档 mmCIF 的 `_citation` 元数据，按同一主引用合并；每个 PDB 链接均指向该原始条目，不把输入结构论文算作本来源的新实验。

| 原始 PDB 条目 | 结构论文主引用（标题、期刊、年份） | DOI / PMID |
| --- | --- | --- |
| [1A22](https://www.rcsb.org/structure/1A22) | Structural and functional analysis of the 1:1 growth hormone:receptor complex reveals the molecular basis for receptor affinity.；J.Mol.Biol.；1998 | [DOI 10.1006/jmbi.1998.1669](https://doi.org/10.1006/jmbi.1998.1669)；[PMID 9571026](https://pubmed.ncbi.nlm.nih.gov/9571026/) |
| [1A4Y](https://www.rcsb.org/structure/1A4Y) | Molecular recognition of human angiogenin by placental ribonuclease inhibitor--an X-ray crystallographic study at 2.0 A resolution.；EMBO J.；1997 | [DOI 10.1093/emboj/16.17.5162](https://doi.org/10.1093/emboj/16.17.5162)；[PMID 9311977](https://pubmed.ncbi.nlm.nih.gov/9311977/) |
| [1ACB](https://www.rcsb.org/structure/1ACB) | Crystal and molecular structure of the bovine alpha-chymotrypsin-eglin c complex at 2.0 A resolution.；J.Mol.Biol.；1992 | [DOI 10.1016/0022-2836(92)91029-O](https://doi.org/10.1016/0022-2836(92)91029-O)；[PMID 1583684](https://pubmed.ncbi.nlm.nih.gov/1583684/) |
| [1AHW](https://www.rcsb.org/structure/1AHW) | The mechanism of an inhibitory antibody on TF-initiated blood coagulation revealed by the crystal structures of human tissue factor, Fab 5G9 and TF.5G9 complex.；J.Mol.Biol.；1998 | [DOI 10.1006/jmbi.1997.1512](https://doi.org/10.1006/jmbi.1997.1512)；[PMID 9480775](https://pubmed.ncbi.nlm.nih.gov/9480775/) |
| [1AK4](https://www.rcsb.org/structure/1AK4) | Crystal structure of human cyclophilin A bound to the amino-terminal domain of HIV-1 capsid.；Cell(Cambridge,Mass.)；1996 | [DOI 10.1016/S0092-8674(00)81823-1](https://doi.org/10.1016/S0092-8674(00)81823-1)；[PMID 8980234](https://pubmed.ncbi.nlm.nih.gov/8980234/) |
| [1B2S](https://www.rcsb.org/structure/1B2S)、[1B2U](https://www.rcsb.org/structure/1B2U)、[1B3S](https://www.rcsb.org/structure/1B3S) | Structural response to mutation at a protein-protein interface.；J.Mol.Biol.；1999 | [DOI 10.1006/jmbi.1998.2559](https://doi.org/10.1006/jmbi.1998.2559)；[PMID 10064711](https://pubmed.ncbi.nlm.nih.gov/10064711/) |
| [1BRS](https://www.rcsb.org/structure/1BRS) | Protein-protein recognition: crystal structural analysis of a barnase-barstar complex at 2.0-A resolution.；Biochemistry；1994 | [DOI 10.1021/bi00196a004](https://doi.org/10.1021/bi00196a004)；[PMID 8043575](https://pubmed.ncbi.nlm.nih.gov/8043575/) |
| [1CBW](https://www.rcsb.org/structure/1CBW) | Crystal structures of bovine chymotrypsin and trypsin complexed to the inhibitor domain of Alzheimer's amyloid beta-protein precursor (APPI) and basic pancreatic trypsin inhibitor (BPTI): engineering of inhibitors with altered specificities.；Protein Sci.；1997 | [PMID 9300481](https://pubmed.ncbi.nlm.nih.gov/9300481/) |
| [1CHO](https://www.rcsb.org/structure/1CHO) | Crystal and molecular structures of the complex of alpha-chymotrypsin with its inhibitor turkey ovomucoid third domain at 1.8 A resolution.；J.Mol.Biol.；1987 | [DOI 10.1016/0022-2836(87)90659-0](https://doi.org/10.1016/0022-2836(87)90659-0)；[PMID 3477645](https://pubmed.ncbi.nlm.nih.gov/3477645/) |
| [1CSE](https://www.rcsb.org/structure/1CSE) | The high-resolution X-ray crystal structure of the complex formed between subtilisin Carlsberg and eglin c, an elastase inhibitor from the leech Hirudo medicinalis. Structural analysis, subtilisin structure and interface geometry.；Eur.J.Biochem.；1987 | [DOI 10.1111/j.1432-1033.1987.tb13566.x](https://doi.org/10.1111/j.1432-1033.1987.tb13566.x)；[PMID 3301348](https://pubmed.ncbi.nlm.nih.gov/3301348/) |
| [1CSO](https://www.rcsb.org/structure/1CSO)、[1CT0](https://www.rcsb.org/structure/1CT0)、[1CT2](https://www.rcsb.org/structure/1CT2)、[1CT4](https://www.rcsb.org/structure/1CT4) | Deleterious effects of beta-branched residues in the S1 specificity pocket of Streptomyces griseus proteinase B (SGPB): crystal structures of the turkey ovomucoid third domain variants Ile18I, Val18I, Thr18I, and Ser18I in complex with SGPB.；Protein Sci.；2000 | [PMID 10739250](https://pubmed.ncbi.nlm.nih.gov/10739250/) |
| [1DAN](https://www.rcsb.org/structure/1DAN) | The crystal structure of the complex of blood coagulation factor VIIa with soluble tissue factor.；Nature；1996 | [DOI 10.1038/380041a0](https://doi.org/10.1038/380041a0)；[PMID 8598903](https://pubmed.ncbi.nlm.nih.gov/8598903/) |
| [1DQJ](https://www.rcsb.org/structure/1DQJ) | Three-dimensional structures of the free and antigen-bound Fab from monoclonal antilysozyme antibody HyHEL-63(,).；Biochemistry；2000 | [DOI 10.1021/bi000054l](https://doi.org/10.1021/bi000054l)；[PMID 10828942](https://pubmed.ncbi.nlm.nih.gov/10828942/) |
| [1DVF](https://www.rcsb.org/structure/1DVF) | Crystal structure of an Fv-Fv idiotope-anti-idiotope complex at 1.9 A resolution.；J.Mol.Biol.；1996 | [DOI 10.1006/jmbi.1996.0629](https://doi.org/10.1006/jmbi.1996.0629)；[PMID 8950273](https://pubmed.ncbi.nlm.nih.gov/8950273/) |
| [1E96](https://www.rcsb.org/structure/1E96) | Structure of the TPR domain of p67phox in complex with Rac.GTP.；Mol.Cell；2000 | [DOI 10.1016/s1097-2765(05)00091-2](https://doi.org/10.1016/s1097-2765(05)00091-2)；[PMID 11090627](https://pubmed.ncbi.nlm.nih.gov/11090627/) |
| [1EAW](https://www.rcsb.org/structure/1EAW) | Catalytic Domain Structures of Mt-Sp1/Matriptase, a Matrix-Degrading Transmembrane Serine Proteinase.；J.Biol.Chem.；2002 | [DOI 10.1074/JBC.M109830200](https://doi.org/10.1074/JBC.M109830200)；[PMID 11696548](https://pubmed.ncbi.nlm.nih.gov/11696548/) |
| [1EFN](https://www.rcsb.org/structure/1EFN) | Crystal structure of the conserved core of HIV-1 Nef complexed with a Src family SH3 domain.；Cell(Cambridge,Mass.)；1996 | [DOI 10.1016/S0092-8674(00)81276-3](https://doi.org/10.1016/S0092-8674(00)81276-3)；[PMID 8681387](https://pubmed.ncbi.nlm.nih.gov/8681387/) |
| [1EMV](https://www.rcsb.org/structure/1EMV) | Specificity in protein-protein interactions: the structural basis for dual recognition in endonuclease colicin-immunity protein complexes.；J.Mol.Biol.；2000 | [DOI 10.1006/jmbi.2000.3945](https://doi.org/10.1006/jmbi.2000.3945)；[PMID 10966813](https://pubmed.ncbi.nlm.nih.gov/10966813/) |
| [1F47](https://www.rcsb.org/structure/1F47) | The bacterial cell-division protein ZipA and its interaction with an FtsZ fragment revealed by X-ray crystallography.；EMBO J.；2000 | [DOI 10.1093/emboj/19.13.3179](https://doi.org/10.1093/emboj/19.13.3179)；[PMID 10880432](https://pubmed.ncbi.nlm.nih.gov/10880432/) |
| [1F5R](https://www.rcsb.org/structure/1F5R)、[1FY8](https://www.rcsb.org/structure/1FY8)、[3TGK](https://www.rcsb.org/structure/3TGK) | The energetic cost of induced fit catalysis: Crystal structures of trypsinogen mutants with enhanced activity and inhibitor affinity.；Protein Sci.；2001 | [DOI 10.1110/ps.44101](https://doi.org/10.1110/ps.44101)；[PMID 11420435](https://pubmed.ncbi.nlm.nih.gov/11420435/) |
| [1FC2](https://www.rcsb.org/structure/1FC2) | Crystallographic refinement and atomic models of a human Fc fragment and its complex with fragment B of protein A from Staphylococcus aureus at 2.9- and 2.8-A resolution.；Biochemistry；1981 | [DOI 10.1021/bi00512a001](https://doi.org/10.1021/bi00512a001)；[PMID 7236608](https://pubmed.ncbi.nlm.nih.gov/7236608/) |
| [1FCC](https://www.rcsb.org/structure/1FCC) | Crystal structure of the C2 fragment of streptococcal protein G in complex with the Fc domain of human IgG.；Structure；1995 | [DOI 10.1016/S0969-2126(01)00157-5](https://doi.org/10.1016/S0969-2126(01)00157-5)；[PMID 7788293](https://pubmed.ncbi.nlm.nih.gov/7788293/) |
| [1FFW](https://www.rcsb.org/structure/1FFW) | Further insights into the mechanism of function of the response regulator CheY from crystallographic studies of the CheY--CheA(124--257) complex.；Acta Crystallogr.,Sect.D；2001 | [DOI 10.1107/S090744490001492X](https://doi.org/10.1107/S090744490001492X)；[PMID 11134926](https://pubmed.ncbi.nlm.nih.gov/11134926/) |
| [1FR2](https://www.rcsb.org/structure/1FR2) | CRYSTAL STRUCTURE OF THE E9 DNASE DOMAIN WITH A MUTANT IMMUNITY PROTEIN IM9(E41A)；To be Published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |
| [1GC1](https://www.rcsb.org/structure/1GC1) | Structure of an HIV gp120 envelope glycoprotein in complex with the CD4 receptor and a neutralizing human antibody.；Nature；1998 | [DOI 10.1038/31405](https://doi.org/10.1038/31405)；[PMID 9641677](https://pubmed.ncbi.nlm.nih.gov/9641677/) |
| [1GCQ](https://www.rcsb.org/structure/1GCQ) | Novel recognition mode between Vav and Grb2 SH3 domains.；EMBO J.；2001 | [DOI 10.1093/emboj/20.12.2995](https://doi.org/10.1093/emboj/20.12.2995)；[PMID 11406576](https://pubmed.ncbi.nlm.nih.gov/11406576/) |
| [1GL0](https://www.rcsb.org/structure/1GL0)、[1GL1](https://www.rcsb.org/structure/1GL1) | Complexation of Two Proteic Insect Inhibitors to the Active Site of Chymotrypsin Suggests Decoupled Roles for Binding and Selectivity；J.Biol.Chem.；2001 | [DOI 10.1074/JBC.M105707200](https://doi.org/10.1074/JBC.M105707200)；[PMID 11495915](https://pubmed.ncbi.nlm.nih.gov/11495915/) |
| [1GRN](https://www.rcsb.org/structure/1GRN) | Structures of Cdc42 bound to the active and catalytically compromised forms of Cdc42GAP.；Nat.Struct.Biol.；1998 | [DOI 10.1038/4156](https://doi.org/10.1038/4156)；[PMID 9846874](https://pubmed.ncbi.nlm.nih.gov/9846874/) |
| [1H9D](https://www.rcsb.org/structure/1H9D) | The Leukemia-Associated Aml1 (Runx1)-Cbfbeta Complex Functions as a DNA-Induced Molecular Clamp；Nat.Struct.Biol.；2001 | [DOI 10.1038/86264](https://doi.org/10.1038/86264)；[PMID 11276260](https://pubmed.ncbi.nlm.nih.gov/11276260/) |
| [1HE8](https://www.rcsb.org/structure/1HE8) | Crystal Structure and Functional Analysis of Ras Binding to its Effector Phosphoinositide 3-Kinase Gamma；Cell(Cambridge,Mass.)；2000 | [DOI 10.1016/S0092-8674(00)00196-3](https://doi.org/10.1016/S0092-8674(00)00196-3)；[PMID 11136978](https://pubmed.ncbi.nlm.nih.gov/11136978/) |
| [1IAR](https://www.rcsb.org/structure/1IAR) | Crystal structure of the interleukin-4/receptor alpha chain complex reveals a mosaic binding interface.；Cell(Cambridge,Mass.)；1999 | [DOI 10.1016/S0092-8674(00)80736-9](https://doi.org/10.1016/S0092-8674(00)80736-9)；[PMID 10219247](https://pubmed.ncbi.nlm.nih.gov/10219247/) |
| [1JCK](https://www.rcsb.org/structure/1JCK) | Crystal structure of a T-cell receptor beta-chain complexed with a superantigen.；Nature；1996 | [DOI 10.1038/384188a0](https://doi.org/10.1038/384188a0)；[PMID 8906797](https://pubmed.ncbi.nlm.nih.gov/8906797/) |
| [1JRH](https://www.rcsb.org/structure/1JRH) | Neutralizing epitopes on the extracellular interferon gamma receptor (IFNgammaR) alpha-chain characterized by homolog scanning mutagenesis and X-ray crystal structure of the A6 fab-IFNgammaR1-108 complex.；J.Mol.Biol.；1997 | [DOI 10.1006/jmbi.1997.1336](https://doi.org/10.1006/jmbi.1997.1336)；[PMID 9367779](https://pubmed.ncbi.nlm.nih.gov/9367779/) |
| [1JTG](https://www.rcsb.org/structure/1JTG) | Crystal structure and kinetic analysis of beta-lactamase inhibitor protein-II in complex with TEM-1 beta-lactamase.；Nat.Struct.Biol.；2001 | [DOI 10.1038/nsb1001-848](https://doi.org/10.1038/nsb1001-848)；[PMID 11573088](https://pubmed.ncbi.nlm.nih.gov/11573088/) |
| [1KAC](https://www.rcsb.org/structure/1KAC) | Structural analysis of the mechanism of adenovirus binding to its human cellular receptor, CAR.；Science；1999 | [DOI 10.1126/science.286.5444.1579](https://doi.org/10.1126/science.286.5444.1579)；[PMID 10567268](https://pubmed.ncbi.nlm.nih.gov/10567268/) |
| [1KIP](https://www.rcsb.org/structure/1KIP)、[1KIQ](https://www.rcsb.org/structure/1KIQ)、[1KIR](https://www.rcsb.org/structure/1KIR) | Hydrogen bonding and solvent structure in an antigen-antibody interface. Crystal structures and thermodynamic characterization of three Fv mutants complexed with lysozyme.；Biochemistry；1996 | [DOI 10.1021/bi961709e](https://doi.org/10.1021/bi961709e)；[PMID 8952503](https://pubmed.ncbi.nlm.nih.gov/8952503/) |
| [1KTZ](https://www.rcsb.org/structure/1KTZ) | Crystal structure of the human TbetaR2 ectodomain--TGF-beta3 complex.；Nat.Struct.Biol.；2002 | [PMID 11850637](https://pubmed.ncbi.nlm.nih.gov/11850637/) |
| [1LFD](https://www.rcsb.org/structure/1LFD) | Structural basis for the interaction of Ras with RalGDS.；Nat.Struct.Biol.；1998 | [DOI 10.1038/nsb0698-422](https://doi.org/10.1038/nsb0698-422)；[PMID 9628477](https://pubmed.ncbi.nlm.nih.gov/9628477/) |
| [1M9E](https://www.rcsb.org/structure/1M9E) | Structural insights into the catalytic mechanism of cyclophilin A；Nat.Struct.Biol.；2003 | [DOI 10.1038/nsb927](https://doi.org/10.1038/nsb927)；[PMID 12730686](https://pubmed.ncbi.nlm.nih.gov/12730686/) |
| [1MAH](https://www.rcsb.org/structure/1MAH) | Acetylcholinesterase inhibition by fasciculin: crystal structure of the complex.；Cell(Cambridge,Mass.)；1995 | [DOI 10.1016/0092-8674(95)90128-0](https://doi.org/10.1016/0092-8674(95)90128-0)；[PMID 8521480](https://pubmed.ncbi.nlm.nih.gov/8521480/) |
| [1N8O](https://www.rcsb.org/structure/1N8O) | Crystal Structure of a Complex Between Bovine Chymotrypsin and Ecotin at 2.0 A Resolution；To be Published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |
| [1NCA](https://www.rcsb.org/structure/1NCA) | Refined crystal structure of the influenza virus N9 neuraminidase-NC41 Fab complex.；J.Mol.Biol.；1992 | [DOI 10.1016/0022-2836(92)90687-F](https://doi.org/10.1016/0022-2836(92)90687-F)；[PMID 1381757](https://pubmed.ncbi.nlm.nih.gov/1381757/) |
| [1NMB](https://www.rcsb.org/structure/1NMB) | The structure of a complex between the NC10 antibody and influenza virus neuraminidase and comparison with the overlapping binding site of the NC41 antibody；Structure；1994 | [DOI 10.1016/S0969-2126(00)00074-5](https://doi.org/10.1016/S0969-2126(00)00074-5)；[PMID 7994573](https://pubmed.ncbi.nlm.nih.gov/7994573/) |
| [1P69](https://www.rcsb.org/structure/1P69)、[1P6A](https://www.rcsb.org/structure/1P6A) | Structural basis for variation in adenovirus affinity for the cellular coxsackievirus and adenovirus receptor.；J.Biol.Chem.；2003 | [DOI 10.1074/jbc.M301492200](https://doi.org/10.1074/jbc.M301492200)；[PMID 12716886](https://pubmed.ncbi.nlm.nih.gov/12716886/) |
| [1PPF](https://www.rcsb.org/structure/1PPF) | X-ray crystal structure of the complex of human leukocyte elastase (PMN elastase) and the third domain of the turkey ovomucoid inhibitor.；EMBO J.；1986 | [PMID 3640709](https://pubmed.ncbi.nlm.nih.gov/3640709/) |
| [1R0R](https://www.rcsb.org/structure/1R0R) | Structure and energetics of protein-protein interactions: the role of conformational heterogeneity in OMTKY3 binding to serine proteases；J.Mol.Biol.；2003 | [DOI 10.1016/S0022-2836(03)00783-6](https://doi.org/10.1016/S0022-2836(03)00783-6)；[PMID 12888355](https://pubmed.ncbi.nlm.nih.gov/12888355/) |
| [1REW](https://www.rcsb.org/structure/1REW) | Molecular recognition of BMP-2 and BMP receptor IA.；Nat.Struct.Mol.Biol.；2004 | [DOI 10.1038/nsmb756](https://doi.org/10.1038/nsmb756)；[PMID 15064755](https://pubmed.ncbi.nlm.nih.gov/15064755/) |
| [1S0W](https://www.rcsb.org/structure/1S0W) | The modular architecture of protein-protein binding interfaces.；Proc.Natl.Acad.Sci.USA；2005 | [DOI 10.1073/pnas.0407280102](https://doi.org/10.1073/pnas.0407280102)；[PMID 15618400](https://pubmed.ncbi.nlm.nih.gov/15618400/) |
| [1S1Q](https://www.rcsb.org/structure/1S1Q) | Ubiquitin recognition by the human TSG101 protein；Mol.Cell；2004 | [DOI 10.1016/S1097-2765(04)00129-7](https://doi.org/10.1016/S1097-2765(04)00129-7)；[PMID 15053872](https://pubmed.ncbi.nlm.nih.gov/15053872/) |
| [1SBB](https://www.rcsb.org/structure/1SBB) | Three-dimensional structure of the complex between a T cell receptor beta chain and the superantigen staphylococcal enterotoxin B.；Immunity；1998 | [DOI 10.1016/S1074-7613(00)80646-9](https://doi.org/10.1016/S1074-7613(00)80646-9)；[PMID 9881971](https://pubmed.ncbi.nlm.nih.gov/9881971/) |
| [1SBN](https://www.rcsb.org/structure/1SBN)、[1SIB](https://www.rcsb.org/structure/1SIB) | Refined crystal structures of subtilisin novo in complex with wild-type and two mutant eglins. Comparison with other serine proteinase inhibitor complexes.；J.Mol.Biol.；1991 | [DOI 10.1016/0022-2836(91)90549-L](https://doi.org/10.1016/0022-2836(91)90549-L)；[PMID 1992167](https://pubmed.ncbi.nlm.nih.gov/1992167/) |
| [1SGD](https://www.rcsb.org/structure/1SGD)、[1SGY](https://www.rcsb.org/structure/1SGY)、[2SGQ](https://www.rcsb.org/structure/2SGQ) | Recruitment of a Buried K+ Ion to Stabilize the Negative Charge of Ionized P1 in the Hydrophobic Pocket: Crystal Structures of Glu18, Gln18, Asp18 and Asn18 Variants of Turkey Ovomucoid Inhibitor Third Domain Complexed with Streptomyces griseus Protease B at Various pH's；To be Published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |
| [1SGE](https://www.rcsb.org/structure/1SGE)、[1SGN](https://www.rcsb.org/structure/1SGN) | Recruitment of a Buried K+ Ion to Stabilize the Negative Charge of Ionized P1 in the Hydrophobic Pocket: Crystal Structures of Glu18, Gln18, Asp18 and Asn18 Variants of Turkey Ovomucoid Inhibitor Third Domain Complexed with Streptomyces griseus Protease B at Various pHs；To be Published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |
| [1SGP](https://www.rcsb.org/structure/1SGP)、[1SGQ](https://www.rcsb.org/structure/1SGQ) | Water molecules participate in proteinase-inhibitor interactions: crystal structures of Leu18, Ala18, and Gly18 variants of turkey ovomucoid inhibitor third domain complexed with Streptomyces griseus proteinase B.；Protein Sci.；1995 | [PMID 8535235](https://pubmed.ncbi.nlm.nih.gov/8535235/) |
| [1SMF](https://www.rcsb.org/structure/1SMF) | Studies on an artificial trypsin inhibitor peptide derived from the mung bean trypsin inhibitor: chemical synthesis, refolding, and crystallographic analysis of its complex with trypsin.；J.Biochem.(Tokyo)；1994 | [PMID 7798176](https://pubmed.ncbi.nlm.nih.gov/7798176/) |
| [1TM1](https://www.rcsb.org/structure/1TM1)、[1TM3](https://www.rcsb.org/structure/1TM3)、[1TM4](https://www.rcsb.org/structure/1TM4)、[1TM5](https://www.rcsb.org/structure/1TM5)、[1TM7](https://www.rcsb.org/structure/1TM7)、[1TMG](https://www.rcsb.org/structure/1TMG)、[1TO1](https://www.rcsb.org/structure/1TO1) | Binding, Proteolytic, and Crystallographic Analyses of Mutations at the Protease-Inhibitor Interface of the Subtilisin BPN'/Chymotrypsin Inhibitor 2 Complex(,).；Biochemistry；2004 | [DOI 10.1021/bi048797k](https://doi.org/10.1021/bi048797k)；[PMID 15504027](https://pubmed.ncbi.nlm.nih.gov/15504027/) |
| [1UUZ](https://www.rcsb.org/structure/1UUZ) | Structure and Evolution of the Ivy Protein Family, Unexpected Lysozyme Inhibitors in Gram-Negative Bacteria.；Proc.Natl.Acad.Sci.USA；2007 | [DOI 10.1073/PNAS.0611019104](https://doi.org/10.1073/PNAS.0611019104)；[PMID 17405861](https://pubmed.ncbi.nlm.nih.gov/17405861/) |
| [1VFB](https://www.rcsb.org/structure/1VFB) | Bound water molecules and conformational stabilization help mediate an antigen-antibody association.；Proc.Natl.Acad.Sci.USA；1994 | [DOI 10.1073/pnas.91.3.1089](https://doi.org/10.1073/pnas.91.3.1089)；[PMID 8302837](https://pubmed.ncbi.nlm.nih.gov/8302837/) |
| [1X1W](https://www.rcsb.org/structure/1X1W)、[1X1X](https://www.rcsb.org/structure/1X1X) | Water-mediated interaction at a protein-protein interface；Chem.Phys.；2004 | [PMID -1](https://pubmed.ncbi.nlm.nih.gov/-1/) |
| [1XD3](https://www.rcsb.org/structure/1XD3) | Structure of the Ubiquitin Hydrolase UCH-L3 Complexed with a Suicide Substrate；J.Biol.Chem.；2005 | [DOI 10.1074/jbc.M410770200](https://doi.org/10.1074/jbc.M410770200)；[PMID 15531586](https://pubmed.ncbi.nlm.nih.gov/15531586/) |
| [1Y1K](https://www.rcsb.org/structure/1Y1K)、[1Y33](https://www.rcsb.org/structure/1Y33)、[1Y34](https://www.rcsb.org/structure/1Y34)、[1Y3B](https://www.rcsb.org/structure/1Y3B)、[1Y3C](https://www.rcsb.org/structure/1Y3C)、[1Y3D](https://www.rcsb.org/structure/1Y3D)、[1Y48](https://www.rcsb.org/structure/1Y48) | Role of the intramolecular hydrogen bond network in the inhibitory power of chymotrypsin inhibitor 2；Biochemistry；2005 | [DOI 10.1021/bi047301w](https://doi.org/10.1021/bi047301w)；[PMID 15865427](https://pubmed.ncbi.nlm.nih.gov/15865427/) |
| [1Z7X](https://www.rcsb.org/structure/1Z7X) | Inhibition of human pancreatic ribonuclease by the human ribonuclease inhibitor protein.；J.Mol.Biol.；2007 | [DOI 10.1016/j.jmb.2007.02.005](https://doi.org/10.1016/j.jmb.2007.02.005)；[PMID 17350650](https://pubmed.ncbi.nlm.nih.gov/17350650/) |
| [2A9K](https://www.rcsb.org/structure/2A9K) | Crystal structure of the C3bot-RalA complex reveals a novel type of action of a bacterial exoenzyme.；Embo J.；2005 | [DOI 10.1038/sj.emboj.7600813](https://doi.org/10.1038/sj.emboj.7600813)；[PMID 16177825](https://pubmed.ncbi.nlm.nih.gov/16177825/) |
| [2AJF](https://www.rcsb.org/structure/2AJF) | Structure of SARS coronavirus spike receptor-binding domain complexed with receptor.；Science；2005 | [DOI 10.1126/science.1116480](https://doi.org/10.1126/science.1116480)；[PMID 16166518](https://pubmed.ncbi.nlm.nih.gov/16166518/) |
| [2B0Z](https://www.rcsb.org/structure/2B0Z)、[2B10](https://www.rcsb.org/structure/2B10)、[2B11](https://www.rcsb.org/structure/2B11)、[2B12](https://www.rcsb.org/structure/2B12) | Effects of interface mutations on association modes and electron-transfer rates between proteins；Proc.Natl.Acad.Sci.Usa；2005 | [DOI 10.1073/pnas.0505176102](https://doi.org/10.1073/pnas.0505176102)；[PMID 16227441](https://pubmed.ncbi.nlm.nih.gov/16227441/) |
| [2B42](https://www.rcsb.org/structure/2B42) | Identification of structural determinants for inhibition strength and specificity of wheat xylanase inhibitors TAXI-IA and TAXI-IIA.；Febs J.；2009 | [DOI 10.1111/j.1742-4658.2009.07105.x](https://doi.org/10.1111/j.1742-4658.2009.07105.x)；[PMID 19769747](https://pubmed.ncbi.nlm.nih.gov/19769747/) |
| [2BTF](https://www.rcsb.org/structure/2BTF) | The structure of crystalline profilin-beta-actin.；Nature；1993 | [DOI 10.1038/365810a0](https://doi.org/10.1038/365810a0)；[PMID 8413665](https://pubmed.ncbi.nlm.nih.gov/8413665/) |
| [2C0L](https://www.rcsb.org/structure/2C0L) | Recognition of a Functional Peroxisome Type 1 Target by the Dynamic Import Receptor Pex5P.；Mol.Cell；2006 | [DOI 10.1016/J.MOLCEL.2006.10.024](https://doi.org/10.1016/J.MOLCEL.2006.10.024)；[PMID 17157249](https://pubmed.ncbi.nlm.nih.gov/17157249/) |
| [2FTL](https://www.rcsb.org/structure/2FTL) | Rigidification of a Flexible Protease Inhibitor Variant upon Binding to Trypsin.；J.Mol.Biol.；2007 | [DOI 10.1016/j.jmb.2006.11.003](https://doi.org/10.1016/j.jmb.2006.11.003)；[PMID 17157870](https://pubmed.ncbi.nlm.nih.gov/17157870/) |
| [2G2U](https://www.rcsb.org/structure/2G2U)、[2G2W](https://www.rcsb.org/structure/2G2W) | Structural and Computational Characterization of the SHV-1 beta-Lactamase-beta-Lactamase Inhibitor Protein Interface.；J.Biol.Chem.；2006 | [DOI 10.1074/jbc.M603878200](https://doi.org/10.1074/jbc.M603878200)；[PMID 16809340](https://pubmed.ncbi.nlm.nih.gov/16809340/) |
| [2GYK](https://www.rcsb.org/structure/2GYK) | Crystal structures of the complexes of the Colicin E9 DNase domain with mutant immunity proteins；To be Published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |
| [2HLE](https://www.rcsb.org/structure/2HLE) | Structural and Biophysical Characterization of the EphB4-EphrinB2 Protein-Protein Interaction and Receptor Specificity.；J.Biol.Chem.；2006 | [DOI 10.1074/jbc.M605766200](https://doi.org/10.1074/jbc.M605766200)；[PMID 16867992](https://pubmed.ncbi.nlm.nih.gov/16867992/) |
| [2HRK](https://www.rcsb.org/structure/2HRK) | Structural basis of yeast aminoacyl-tRNA synthetase complex formation revealed by crystal structures of two binary sub-complexes.；Nucleic Acids Res.；2006 | [DOI 10.1093/nar/gkl560](https://doi.org/10.1093/nar/gkl560)；[PMID 16914447](https://pubmed.ncbi.nlm.nih.gov/16914447/) |
| [2I26](https://www.rcsb.org/structure/2I26) | Maturation of Shark Single-domain (IgNAR) Antibodies: Evidence for Induced-fit Binding.；J.Mol.Biol.；2007 | [DOI 10.1016/j.jmb.2006.12.045](https://doi.org/10.1016/j.jmb.2006.12.045)；[PMID 17258766](https://pubmed.ncbi.nlm.nih.gov/17258766/) |
| [2I9B](https://www.rcsb.org/structure/2I9B) | Structural basis of interaction between urokinase-type plasminogen activator and its receptor.；J.Mol.Biol.；2006 | [DOI 10.1016/j.jmb.2006.08.063](https://doi.org/10.1016/j.jmb.2006.08.063)；[PMID 16979660](https://pubmed.ncbi.nlm.nih.gov/16979660/) |
| [2J0T](https://www.rcsb.org/structure/2J0T) | Crystal Structure of the Catalytic Domain of Matrix Metalloproteinase-1 in Complex with the Inhibitory Domain of Tissue Inhibitor of Metalloproteinase-1.；J.Biol.Chem.；2007 | [DOI 10.1074/JBC.M607625200](https://doi.org/10.1074/JBC.M607625200)；[PMID 17050530](https://pubmed.ncbi.nlm.nih.gov/17050530/) |
| [2J12](https://www.rcsb.org/structure/2J12)、[2J1K](https://www.rcsb.org/structure/2J1K) | Structural and Mutational Analysis of Human Ad37 and Canine Adenovirus 2 Fiber Heads in Complex with the D1 Domain of Coxsackie and Adenovirus Receptor.；J.Biol.Chem.；2006 | [DOI 10.1074/JBC.M605316200](https://doi.org/10.1074/JBC.M605316200)；[PMID 16923808](https://pubmed.ncbi.nlm.nih.gov/16923808/) |
| [2JEL](https://www.rcsb.org/structure/2JEL) | The 2.5 A resolution structure of the jel42 Fab fragment/HPr complex；J.Mol.Biol.；1998 | [DOI 10.1006/jmbi.1998.1888](https://doi.org/10.1006/jmbi.1998.1888)；[PMID 9671553](https://pubmed.ncbi.nlm.nih.gov/9671553/) |
| [2NU0](https://www.rcsb.org/structure/2NU0) | Molecular structures of the complexes of SGPB with OMTKY3 aromatic P1 variants Trp18I, His18I, Phe18I, and Tyr18I；To be Published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |
| [2NU1](https://www.rcsb.org/structure/2NU1) | Molecular structures of the complexes of SGPB with OMTKY3 aromatic P1 variants Trp18I, His18I, Phe18I and Tyr18I；To be Published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |
| [2NU2](https://www.rcsb.org/structure/2NU2)、[2NU4](https://www.rcsb.org/structure/2NU4) | Accommodation of positively-charged residues in a hydrophobic specificity pocket: Crystal structures of SGPB in complex with OMTKY3 variants Lys18I and Arg18I；To be Published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |
| [2O3B](https://www.rcsb.org/structure/2O3B) | The nuclease a-inhibitor complex is characterized by a novel metal ion bridge.；J.Biol.Chem.；2007 | [DOI 10.1074/jbc.M605986200](https://doi.org/10.1074/jbc.M605986200)；[PMID 17138564](https://pubmed.ncbi.nlm.nih.gov/17138564/) |
| [2OOB](https://www.rcsb.org/structure/2OOB) | Structural basis for ubiquitin-mediated dimerization and activation of the ubiquitin protein ligase Cbl-b.；Mol.Cell；2007 | [DOI 10.1016/j.molcel.2007.06.023](https://doi.org/10.1016/j.molcel.2007.06.023)；[PMID 17679095](https://pubmed.ncbi.nlm.nih.gov/17679095/) |
| [2PCB](https://www.rcsb.org/structure/2PCB)、[2PCC](https://www.rcsb.org/structure/2PCC) | Crystal structure of a complex between electron transfer partners, cytochrome c peroxidase and cytochrome c.；Science；1992 | [PMID 1334573](https://pubmed.ncbi.nlm.nih.gov/1334573/) |
| [2SGP](https://www.rcsb.org/structure/2SGP) | Contribution of peptide bonds to inhibitor-protease binding: crystal structures of the turkey ovomucoid third domain backbone variants OMTKY3-Pro18I and OMTKY3-psi[COO]-Leu18I in complex with Streptomyces griseus proteinase B (SGPB) and the structure of the free inhibitor, OMTKY-3-psi[CH2NH2+]-Asp19I；J.Mol.Biol.；2001 | [DOI 10.1006/jmbi.2000.4343](https://doi.org/10.1006/jmbi.2000.4343)；[PMID 11162096](https://pubmed.ncbi.nlm.nih.gov/11162096/) |
| [2SIC](https://www.rcsb.org/structure/2SIC) | Refined crystal structure of the complex of subtilisin BPN' and Streptomyces subtilisin inhibitor at 1.8 A resolution.；J.Mol.Biol.；1991 | [PMID 1920411](https://pubmed.ncbi.nlm.nih.gov/1920411/) |
| [2VIR](https://www.rcsb.org/structure/2VIR)、[2VIS](https://www.rcsb.org/structure/2VIS) | Antigen distortion allows influenza virus to escape neutralization.；Nat.Struct.Biol.；1998 | [DOI 10.1038/nsb0298-119](https://doi.org/10.1038/nsb0298-119)；[PMID 9461077](https://pubmed.ncbi.nlm.nih.gov/9461077/) |
| [2VLJ](https://www.rcsb.org/structure/2VLJ)、[2VLR](https://www.rcsb.org/structure/2VLR) | The Structural Dynamics and Energetics of an Immunodominant T-Cell Receptor are Programmed by its Vbeta Domain；Immunity；2008 | [DOI 10.1016/J.IMMUNI.2007.12.018](https://doi.org/10.1016/J.IMMUNI.2007.12.018)；[PMID 18275829](https://pubmed.ncbi.nlm.nih.gov/18275829/) |
| [2VLN](https://www.rcsb.org/structure/2VLN)、[2VLO](https://www.rcsb.org/structure/2VLO)、[2VLP](https://www.rcsb.org/structure/2VLP)、[2VLQ](https://www.rcsb.org/structure/2VLQ) | Experimental and Computational Analyses of the Energetic Basis for Dual Recognition of Immunity Proteins by Colicin Endonucleases.；J.Mol.Biol.；2008 | [DOI 10.1016/J.JMB.2008.03.055](https://doi.org/10.1016/J.JMB.2008.03.055)；[PMID 18471830](https://pubmed.ncbi.nlm.nih.gov/18471830/) |
| [2WPT](https://www.rcsb.org/structure/2WPT) | The Structural and Energetic Basis for High Selectivity in a High-Affinity Protein-Protein Interaction.；Proc.Natl.Acad.Sci.USA；2010 | [DOI 10.1073/PNAS.0910756107](https://doi.org/10.1073/PNAS.0910756107)；[PMID 20479265](https://pubmed.ncbi.nlm.nih.gov/20479265/) |
| [3BK3](https://www.rcsb.org/structure/3BK3) | Crystal structure analysis reveals how the Chordin family member crossveinless 2 blocks BMP-2 receptor binding；Dev.Cell；2008 | [DOI 10.1016/j.devcel.2008.02.017](https://doi.org/10.1016/j.devcel.2008.02.017)；[PMID 18477456](https://pubmed.ncbi.nlm.nih.gov/18477456/) |
| [3BN9](https://www.rcsb.org/structure/3BN9) | Structure of an Fab-protease complex reveals a highly specific non-canonical mechanism of inhibition；J.Mol.Biol.；2008 | [DOI 10.1016/j.jmb.2008.05.009](https://doi.org/10.1016/j.jmb.2008.05.009)；[PMID 18514224](https://pubmed.ncbi.nlm.nih.gov/18514224/) |
| [3BP8](https://www.rcsb.org/structure/3BP8) | Analyses of Mlc-IIBGlc interaction and a plausible molecular mechanism of Mlc inactivation by membrane sequestration；Proc.Natl.Acad.Sci.Usa；2008 | [DOI 10.1073/pnas.0709295105](https://doi.org/10.1073/pnas.0709295105)；[PMID 18319344](https://pubmed.ncbi.nlm.nih.gov/18319344/) |
| [3BTD](https://www.rcsb.org/structure/3BTD)、[3BTE](https://www.rcsb.org/structure/3BTE)、[3BTF](https://www.rcsb.org/structure/3BTF)、[3BTG](https://www.rcsb.org/structure/3BTG)、[3BTH](https://www.rcsb.org/structure/3BTH)、[3BTM](https://www.rcsb.org/structure/3BTM)、[3BTQ](https://www.rcsb.org/structure/3BTQ)、[3BTT](https://www.rcsb.org/structure/3BTT)、[3BTW](https://www.rcsb.org/structure/3BTW) | The crystal structures of the complexes between bovine beta-trypsin and ten P1 variants of BPTI.；J.Mol.Biol.；1999 | [DOI 10.1006/jmbi.1999.2654](https://doi.org/10.1006/jmbi.1999.2654)；[PMID 10222201](https://pubmed.ncbi.nlm.nih.gov/10222201/) |
| [3HFM](https://www.rcsb.org/structure/3HFM) | Structure of an antibody-antigen complex: crystal structure of the HyHEL-10 Fab-lysozyme complex.；Proc.Natl.Acad.Sci.USA；1989 | [DOI 10.1073/pnas.86.15.5938](https://doi.org/10.1073/pnas.86.15.5938)；[PMID 2762305](https://pubmed.ncbi.nlm.nih.gov/2762305/) |
| [3NPS](https://www.rcsb.org/structure/3NPS) | A reverse binding motif that contributes to specific protease inhibition by antibodies.；J.Mol.Biol.；2012 | [DOI 10.1016/j.jmb.2011.11.036](https://doi.org/10.1016/j.jmb.2011.11.036)；[PMID 22154938](https://pubmed.ncbi.nlm.nih.gov/22154938/) |
| [3SGB](https://www.rcsb.org/structure/3SGB) | Structure of the complex of Streptomyces griseus protease B and the third domain of the turkey ovomucoid inhibitor at 1.8-A resolution.；Biochemistry；1983 | [DOI 10.1021/bi00288a012](https://doi.org/10.1021/bi00288a012)；[PMID 6414511](https://pubmed.ncbi.nlm.nih.gov/6414511/) |
| [4CPA](https://www.rcsb.org/structure/4CPA) | Refined crystal structure of the potato inhibitor complex of carboxypeptidase A at 2.5 A resolution.；J.Mol.Biol.；1982 | [DOI 10.1016/0022-2836(82)90309-6](https://doi.org/10.1016/0022-2836(82)90309-6)；[PMID 7154070](https://pubmed.ncbi.nlm.nih.gov/7154070/) |

## 其他

### 数据范围和限制

公开四文件 commit 和 PDB 补充已核验；主文正式版和六页合订 Supplementary material 均已归档。论文附件范围已取得，但未公开的底层实验原始记录仍不在本 source 中。该二次汇编与 SKEMPI 重叠，不能以来源 ID 不同充当独立外部验证集。

### 完整性与验收

payload 共 4 文件、497.03 KiB（508,958 bytes）；同样排序 inventory SHA-256 为 `f0162fa1163b6189dfc0bb89a68e9a518c4a6d33ff76f208902454d749fac0d2`。独立审计要求 config 中目标文件集合与实际完全一致（允许 source README，保留上游自己的 README），拒绝 symlink、旁路 JSON/API/manifest、partial 文件或缺少任何可公开 PDB 层。PDF 页数/签名、XLSX 全部 worksheet、ZIP 全部 CRC 与安全成员均按文件类型核验；研究审计结果只保存本人 context，不发布为 raw sidecar。

上游 payload 文件身份；SHA-256 为获取后固定的本地值：

| payload 文件 | 大小 | SHA-256 |
| --- | --- | --- |
| DACUM_1.0.csv | 74.75 KiB（76,539 bytes） | `1ea2138e976e51aa1cab590737ea55a2ffcbe6777bbf183f181718651ebb47c2` |
| DACUM_1.1.csv | 404.35 KiB（414,058 bytes） | `477fc9700498851b93da0207523fd2ac375f31040e8e3390620f82113a57d79b` |
| LICENSE | 11.09 KiB（11,357 bytes） | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |
| README.md | 6.84 KiB（7,004 bytes） | `ffae26cfd45d43e8646076efe3fb2117a42e10946f3ed1f798b8240c8e01c37b` |

### 许可和再分发边界

仓库保留 Apache-2.0 LICENSE。SKEMPI 原始汇编/文献实验数据的权利应单独核实，不将代码许可证扩展为所有上游实验或论文的再分发授权。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 固定 commit 四文件 | 两版 CSV、README、LICENSE；全部 Git blob 与 size 一致 | 已包含 |
| 1,872 条突变记录 | 两个版本同一 SKEMPI_ID 集合 | 已包含；不能相加 |
| 147 个参考结构 | 147 份 native FASTA + 147 份完整 mmCIF | 已包含；非逐突变体结构 |
| 论文主文 | 机构公开正式版 10 页已归档并读完主文 | 已包含 |
| 独立补充附件 | OUP Supplementary data 区域取得的六页合订 PDF，含 Table S1–S3 与 Figure S1–S2 | 已取得并验收 |
| 底层实验原始记录 | 仓库与论文附件均未提供 sensorgram、重复测量明细或完整仪器输出 | 未获得，未宣称完整研究获取 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-22；待权利核验）：作者仓库保留 Apache-2.0 LICENSE，DACUM 又汇编 SKEMPI 与原始文献实验数据；目前没有逐来源的商业再利用授权对照。已保留原始引用和仓库许可证，当前不将代码许可证扩展为所有实验数据的许可。商业训练、再分发或公开衍生物前，应按拟使用的记录核对 SKEMPI 及原文条款，并记录权利方或法务结论。

逐实验 sensorgram、重复测量和突变体完整序列未随公开包提供，已在“数据范围和限制”写明；这项已知公开边界不被解释为文件下载失败。若未来取得更底层材料，应核对与本版本的对应关系并更新本节。
