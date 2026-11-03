# SRC_R58_DBMPIKT 数据说明

## 数据集身份

- `source_id`：`SRC_R58_DBMPIKT`
- `source_version`：`snapshot-2018-11-27`
- 原作者或发布机构：安徽大学牵头的 dbMPIKT 作者团队（Quanya Liu、Peng Chen 等）

### 来源方背景

正式论文的作者单位显示，dbMPIKT 由安徽大学物质科学与信息技术研究院的 Quanya Liu、通讯作者 Peng Chen 等牵头，并有安徽工业大学、安徽大学电子工程与自动化学院及澳大利亚悉尼科技大学研究者参与。历史数据库入口使用安徽大学域名；当前可核验的正式论文和五份补充材料由 BMC/Springer Nature 发布。来源方角色依据[正式论文作者与单位](https://pmc.ncbi.nlm.nih.gov/articles/PMC6260753/)和[安徽大学官网](https://www.ahu.edu.cn/)记录；本轮没有找到仍在维护的独立 dbMPIKT 团队主页，因此不推断当前维护状态。

## 实验设计和数据口径

dbMPIKT 是蛋白相互作用突变动力学/热力学汇编。正式论文描述从 SKEMPI、AB-Bind、BID 与文献汇合记录、统一单位并提供突变及复合物检索，覆盖非抗体体系。作者报告 5,291 条突变：SKEMPI 3,046、AB-Bind 815、BID 256、文献 1,174；233 个 PDB、245 个复合物、12 个无 PDB 复合物。这些是论文描述的数据库规模，不是本次实际获得的逐记录测量数。

本次取得的公开 payload 是正式论文的五份补充材料：Additional File 1 把 PDB、突变串、论文题名和 PubMed 引用作为几组长度不同的独立清单并排保存，公式列把各清单转换为带前缀的展示文本；同行单元格通常不是同一条数据库记录。Additional File 2 是复合物、链、蛋白名称和物种来源目录；Additional File 3 是来源与突变类型的聚合计数；File 4/5 是两张汇总图。公开附件没有给出 5,291 条记录逐条对应的 Kd、kon、koff、ΔG、ΔΔG 或不确定性字段。

同一 PDB 可有多链、多突变、多文献；Additional File 2 还会用续行展开同一复合物的不同链。1,183 是 File 1 的格式范围行数，实际只有 379 行至少含一个非空单元格，且并排清单之间没有公开逐项连接关系。因而当前子包适合核对来源构成、复合物目录和结构覆盖，不能形成 5,291 条定量训练记录。与 SKEMPI、AB-Bind、BID 合并时还须按上游对象去重。

## 论文原文

- 标题：dbMPIKT: a database of kinetic and thermodynamic mutant protein interactions
- 作者：Quanya Liu、Peng Chen、Bing Wang、Jun Zhang、Jinyan Li
- 发表来源：BMC Bioinformatics 19:455
- 归档文本版本：正式发表版 PDF（BMC/Springer Nature）
- 发布日期：2018-11-27
- DOI：10.1186/s12859-018-2493-7
- PMID / PMCID：PMID 30482172 / PMCID PMC6260753
- 本地文件：`articles/dbMPIKT_2018-11-27_BMC.pdf`
- 文件大小：1.05 MiB (1,096,109 bytes)
- SHA-256：`e081654931aed5e8cea5d390f8232b5be7943260f18ad1a9723fd45e2a861368`
- 文本许可：CC BY 4.0；论文声明文章所提供的数据适用 CC0，另有说明者除外
- 补充材料：5 个独立 Figshare v1 对象：3 个 XLSX 与 2 个 PNG；均已按官方大小和 MD5 复核
- 引用数（查询快照）：39（OpenAlex work W2903116334，查询于 2026-09-24）

## 仓库内容

一手入口为 [正式论文](https://link.springer.com/article/10.1186/s12859-018-2493-7)及其 [Springer Nature Figshare collection 4315598](https://springernature.figshare.com/collections/_/4315598)。collection 当前枚举的五个附件均为 2018-11-27 发布的 v1 对象；配置固定各对象的官方字节数与 MD5。版本名 `snapshot-2018-11-27` 取正式论文及附件发布日期。这是五份补充材料组成的公开子集和独立论文归档，不是历史网站中的 dbMPIKT 全库导出。

```text
snapshot-2018-11-27/
└── dbMPIKT/
    ├── dbMPIKT_2018-11-27_BMC-AdditionalFile1.xlsx
    ├── dbMPIKT_2018-11-27_BMC-AdditionalFile2.xlsx
    ├── dbMPIKT_2018-11-27_BMC-AdditionalFile3.xlsx
    ├── dbMPIKT_2018-11-27_BMC-AdditionalFile4.png
    └── dbMPIKT_2018-11-27_BMC-AdditionalFile5.png
```

表格、归档与其记录关系见数据结构；上游说明、许可或嵌入资源保留原始内容。

## 数据结构

### 补充表与聚合层级

Additional File 1 的 Sheet1 格式范围是 1,183×13，其中 379 行至少有一个非空单元格、共有 480 个公式。A–D 列为空；E、H、J、L 分别保存长度不同的 PDB、突变串、论文题名和 PubMed 引用清单，F、I、K、M 是跨行引用这些清单并添加前缀的公式。工作簿没有给出把四组清单恢复为逐记录数据库表的主键或行级映射。Additional File 2 的 Sheet1 是 510×7，500 个非空行；Additional File 3 的 Sheet1 是 22×21，7 个非空行，Sheet2 与 Sheet3 无非空行。Additional File 4/5 是论文氨基酸突变分布图与蛋白相互作用网络 PNG，不提供额外逐条实验值。

File 1 有 Unicode 文献文本；File 2 有全角逗号链分隔符；File 3 保留来源标签内的回车，如 `SKEMPI\r`。公式与 cached value 是两种读取模式，空缓存不表示公式不存在；本次保留原工作簿，没有计算或改写公式。PDB、链、Protein/Source、突变串、标题与 Reference 是字符串（PubMed 号也以文本保存），F/I/K/M 为公式字符串，File 3 计数为整数单元格。计数布局包含 Data Sources、Single mutant、Double mutant、Multiple mutant、Total，前三种突变层级各分 alanine/other 子列；字面 `None`、空格、空单元格与数值 0 保持区别。

计数表存在上游算术不一致：dbMPIKT 六类别 673+338+49+88+15+12=1,175，但 Total 单元格为 1,174；来源行重算 Single mutant/alanine 合计 2,253，但 Total 行写 2,453；Total 行六类别相加为 5,492，与该行总计 5,291 不同。原始数值全部保留，不把这些聚合差异用作新增个体记录。

### 字段说明

| 文件与列 | 原始标题或结构 | 读取含义 |
| --- | --- | --- |
| File 1 / A–D | 无标题且全为空 | 保留的空白布局列 |
| File 1 / E | Protein | PDB 编号独立清单；本次 PDB 锚点来源之一 |
| File 1 / F | Protein | 公式 `=$G$2&E<row>`，把 E 列值加上固定前缀 |
| File 1 / G | P: 或空 | F 列使用的展示前缀单元格 |
| File 1 / H | Mutation(s)_PDB | 突变串独立清单；单元格可含分号或斜杠，但没有逐突变 Kd |
| File 1 / I | Mutations name | 公式从不同 H 行取值并添加 `M:`；不是同行记录连接键 |
| File 1 / J | Title | 论文题名独立清单 |
| File 1 / K | Title | 公式从不同 J 行取值并添加 `T:` |
| File 1 / L | Reference | PubMed ID 独立清单，以文本保存 |
| File 1 / M | PubMed ID | 公式从不同 L 行取值并添加 `D:` |
| File 2 / A | PDB ID | 复合物编码，首四位为 PDB；续行可能空 |
| File 2 / B | Chain ID | 原始作者链或分隔链组，续行仍属于前一复合物 |
| File 2 / C/D | Protein / Source | 蛋白名称与生物来源 |
| File 2 / E–G | 无统一表头 | 多链布局中的辅助单元格，保留原始 workbook |
| File 3 / 21 列布局 | Data Sources；Single/Double/Multiple mutant 的 alanine、other 与小计；Total | 整数是聚合记录数，不是结合强度；空单元格不解释为零 |
| File 4/5 | PNG 像素 | 聚合分布图和相互作用网络图，不是定量测量表 |

### 数据示例

File 1 第 2 行恰好同时出现 E=`3W2D`、H=`YA46F;YA46L;KA71R;KA71N`、J=`Structural basis for the neutralization...` 和 L=`24423621`；但后续公式会分别跳转到 H6、J6、L6 等不同位置，说明这些列按独立清单组织。没有公开依据把同行四个值当作一条 dbMPIKT 测量，也不能把 H2 的四个突变展开为四条带 Kd 的记录。

File 2 首复合物为 `1A22_A_B`，首行链 A 为 Human growth hormone，续行链 B 为 hGH binding protein，两者来源 Homo sapiens；续行的 PDB ID 单元格为空不表示无法确认其复合物。

File 3 的 SKEMPI 来源分类计数为 1,057、1,259、211、153、62、304，总计 3,046；不是六种亲和力值。

## PDB 数据库

从 File 1 的 Protein/PDB 列提取 94 个唯一编号，从 File 2 的 PDB ID 列提取 226 个，合并为 230 个候选锚点。只从指定列提取，拒绝在全表文本里抓取貌似 PDB 的字符串：例如抗体名称 7D12 不是在本表中给出的结构 accession。

其中 229 个具有完整 RCSB FASTA/mmCIF。2026-09-24 复核时，1TPQ 的官方 holdings API 仍返回 `UNRELEASED`、`WDRN`，`update_id=2026_38`，FASTA 与 mmCIF 文件接口均为 404；未找到由来源材料支持的替代 accession。因此 PDB 子任务是 partial：229/230 对，缺失项明确为 1TPQ。

File 2 的链组按 `/`、ASCII 逗号、全角逗号分隔核验；1BJ1 的原始 `JH` 结合实体描述和完整 author chains 验证为 J/H 组合。全部公开条目的链选择均与 `_entity_poly.pdbx_strand_id` 比对；原始链单元格仍在 workbook 中，未重写。锚点来自复合物目录，不等于逐测量构建体或逐突变结构。无逐突变体序列重建。

最近获取/核验日期 2026-09-24。每个可得编号使用 RCSB `https://www.rcsb.org/fasta/entry/<PDB_ID>/download` 与 `https://files.rcsb.org/download/<PDB_ID>.cif`。校验 FASTA entity ID 集合及全序列与 mmCIF canonical entity 全序列严格相等，并核对 entry.id、非空原子坐标和 author-chain。共 229 个完整对，458 个文件，221.94 MiB (232,721,636 bytes)。按相对路径排序拼接 `relative_path<TAB>bytes<TAB>sha256<LF>` 后 inventory SHA-256 为 `e3d2c6031e8a797aa005ac4e7e5ffe5f3aa525c8836b73f4549d618f076c6013`。

## 使用方式

依赖见接入代码 requirements；以下仅从原始文件读取。

```python
from pathlib import Path
from openpyxl import load_workbook
# dataset_root 由调用者赋值为该 source version 目录。
book = load_workbook(Path(dataset_root) / "dbMPIKT/dbMPIKT_2018-11-27_BMC-AdditionalFile1.xlsx",
                     read_only=True, data_only=False)
sheet = book["Sheet1"]
for column in ("E", "H", "J", "L"):
    values = [cell.value for cell in sheet[column] if cell.value is not None]
    print(column, len(values), values[:2])  # 四组独立清单，不能按行 zip。
book.close()
```

## 采集过程记录

1. 2026-09-18：读取项目/开发者身份、执行清单与一手来源；由配置读取共享存储根，代码和文档只写本人 workspace。
2. 固定上游版本并在对应 `.staging/snapshot-2018-11-27` 下载，使用断点续传、HTTP 长度及可得的官方校验；遇到环境直连失败采用现有 HTTP 路由回退。
3. 历史 `http://DeepLearner.ahu.edu.cn/web/dbMPIKT/`、对应 HTTPS 地址与 `http://210.45.212.128/lqy/index.php` 在 2026-09-24 复核时均未能建立可用响应，未恢复数据库导出。Springer Nature Figshare collection `4315598` 仍只列当前 3 个 XLSX 与 2 个 PNG；2026-09-19 对 DataCite、GitHub、Zenodo、Hugging Face、Harvard Dataverse、Internet Archive 和 Arquivo 的追查也没有找到 5,291 条原库 dump。下游论文公开的 dbMPIKT-derived 热点子集没有原库的完整记录身份，因此未混入本 source。最初按单链解析 `A/B` 等组合链名失败，核查原始单元格及 mmCIF 后修正解析，不修改 raw。2026-09-24 再查 1TPQ，RCSB holdings 仍为 `UNRELEASED/WDRN`，FASTA/mmCIF 均为 404，继续保留 partial 结论。
4. 解析全部实际表/归档，独立核对文件集合、完整格式、哈希与 PDB 两层，保留上游差异。
5. README 工作稿每次写入立即同步共享目录；发布器复核固定格式、同步 hash 和 pinned markdownlint 0 errors 后原子发布。本次仍在 staging；1TPQ 缺少原生两层文件，发布器拒绝原子发布。

依据来源、可核验日期、载体和附件角色整理 opaque 名称，改名前后 bytes/SHA-256 相同；中间名保留实际修订历史。附件名称按正式出版日期及实际角色整理。具体映射如下：

| 上游原名 | 中间名（如有） | 本地相对路径 | 核对大小 | 核对 SHA-256 |
| --- | --- | --- | --- | --- |
| 12859_2018_2493_MOESM1_ESM.xlsx | 无 | dbMPIKT/dbMPIKT_2018-11-27_BMC-AdditionalFile1.xlsx | 60.77 KiB (62,228 bytes) | `6dd7450bf1b8021e0d84d974ccbd7cdff333b7a8b1dd4ef577b7ff679dc6cb78` |
| 12859_2018_2493_MOESM2_ESM.xlsx | 无 | dbMPIKT/dbMPIKT_2018-11-27_BMC-AdditionalFile2.xlsx | 38.11 KiB (39,022 bytes) | `51305fd105cb4c2306a7cd511282806287a22b9281b5cf194e18355fbb825b60` |
| 12859_2018_2493_MOESM3_ESM.xlsx | 无 | dbMPIKT/dbMPIKT_2018-11-27_BMC-AdditionalFile3.xlsx | 10.62 KiB (10,875 bytes) | `e2854a2f593572cc51cb5bd23e714627de512980686b036715475d915e4b897b` |
| 12859_2018_2493_MOESM4_ESM.png | 无 | dbMPIKT/dbMPIKT_2018-11-27_BMC-AdditionalFile4.png | 22.21 KiB (22,744 bytes) | `c5a3918de92cce6090dea22ed840e1678cba44f825df9e7f3b5b96cc82fd7ab5` |
| 12859_2018_2493_MOESM5_ESM.png | 无 | dbMPIKT/dbMPIKT_2018-11-27_BMC-AdditionalFile5.png | 71.78 KiB (73,504 bytes) | `06e9cf0fb09ac6c805a8219ca53b2eee5cb2c0964ea37189d63502a553968f74` |

2026-09-18 逐条复审后：补齐全部已取得 PDB 的条目和原始结构论文主引用，以及涉及的上游汇编/对照引用。补齐上游数据库论文和原字段类型，保留 1TPQ 及真实 staging 状态。相应修改同步个人状态、事实台账和交接，未取得的材料继续标明 partial/blocked。

## 参考文献

- [正式论文与补充材料](https://link.springer.com/article/10.1186/s12859-018-2493-7)
- [开放全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC6260753/)
- [Springer Nature Figshare collection 4315598](https://springernature.figshare.com/collections/_/4315598)
- [OpenAlex 正式论文记录](https://openalex.org/W2903116334)
- [1TPQ 官方状态](https://data.rcsb.org/rest/v1/holdings/status/1TPQ)
- [Moal & Fernández-Recio (2012), SKEMPI: a Structural Kinetic and Energetic database of Mutant Protein Interactions and its use in empirical models](https://doi.org/10.1093/bioinformatics/bts489)
- [Sirin et al. (2016), AB-Bind: Antibody binding mutational database for computational affinity predictions](https://doi.org/10.1002/pro.2829)
- [Fischer et al. (2003), The binding interface database (BID): a compilation of amino acid hot spots in protein interfaces](https://doi.org/10.1093/bioinformatics/btg163)
- [Thorn & Bogan (2001), ASEdb: a database of alanine mutations and their effects on the free energy of binding in protein interactions](https://doi.org/10.1093/bioinformatics/17.3.284)
- [Kumar & Gromiha (2006), PINT: Protein–protein Interactions Thermodynamic Database](https://doi.org/10.1093/nar/gkj017)

### PDB 条目与原始结构论文

以下主引用直接读取归档 mmCIF 的 `_citation` 元数据，按同一主引用合并；每个 PDB 链接均指向该原始条目，不把输入结构论文算作本来源的新实验。

| 原始 PDB 条目 | 结构论文主引用（标题、期刊、年份） | DOI / PMID |
| --- | --- | --- |
| [1A22](https://www.rcsb.org/structure/1A22) | Structural and functional analysis of the 1:1 growth hormone:receptor complex reveals the molecular basis for receptor affinity.；J.Mol.Biol.；1998 | [DOI 10.1006/jmbi.1998.1669](https://doi.org/10.1006/jmbi.1998.1669)；[PMID 9571026](https://pubmed.ncbi.nlm.nih.gov/9571026/) |
| [1A4Y](https://www.rcsb.org/structure/1A4Y) | Molecular recognition of human angiogenin by placental ribonuclease inhibitor--an X-ray crystallographic study at 2.0 A resolution.；EMBO J.；1997 | [DOI 10.1093/emboj/16.17.5162](https://doi.org/10.1093/emboj/16.17.5162)；[PMID 9311977](https://pubmed.ncbi.nlm.nih.gov/9311977/) |
| [1ACB](https://www.rcsb.org/structure/1ACB) | Crystal and molecular structure of the bovine alpha-chymotrypsin-eglin c complex at 2.0 A resolution.；J.Mol.Biol.；1992 | [DOI 10.1016/0022-2836(92)91029-O](https://doi.org/10.1016/0022-2836(92)91029-O)；[PMID 1583684](https://pubmed.ncbi.nlm.nih.gov/1583684/) |
| [1AHW](https://www.rcsb.org/structure/1AHW) | The mechanism of an inhibitory antibody on TF-initiated blood coagulation revealed by the crystal structures of human tissue factor, Fab 5G9 and TF.5G9 complex.；J.Mol.Biol.；1998 | [DOI 10.1006/jmbi.1997.1512](https://doi.org/10.1006/jmbi.1997.1512)；[PMID 9480775](https://pubmed.ncbi.nlm.nih.gov/9480775/) |
| [1AK4](https://www.rcsb.org/structure/1AK4) | Crystal structure of human cyclophilin A bound to the amino-terminal domain of HIV-1 capsid.；Cell(Cambridge,Mass.)；1996 | [DOI 10.1016/S0092-8674(00)81823-1](https://doi.org/10.1016/S0092-8674(00)81823-1)；[PMID 8980234](https://pubmed.ncbi.nlm.nih.gov/8980234/) |
| [1AXI](https://www.rcsb.org/structure/1AXI) | Structural plasticity in a remodeled protein-protein interface.；Science；1997 | [DOI 10.1126/science.278.5340.1125](https://doi.org/10.1126/science.278.5340.1125)；[PMID 9353194](https://pubmed.ncbi.nlm.nih.gov/9353194/) |
| [1B2S](https://www.rcsb.org/structure/1B2S) | Structural response to mutation at a protein-protein interface.；J.Mol.Biol.；1999 | [DOI 10.1006/jmbi.1998.2559](https://doi.org/10.1006/jmbi.1998.2559)；[PMID 10064711](https://pubmed.ncbi.nlm.nih.gov/10064711/) |
| [1BGS](https://www.rcsb.org/structure/1BGS) | Recognition between a bacterial ribonuclease, barnase, and its natural inhibitor, barstar.；Structure；1993 | [DOI 10.1016/0969-2126(93)90018-C](https://doi.org/10.1016/0969-2126(93)90018-C)；[PMID 16100951](https://pubmed.ncbi.nlm.nih.gov/16100951/) |
| [1BJ1](https://www.rcsb.org/structure/1BJ1) | VEGF and the Fab fragment of a humanized neutralizing antibody: crystal structure of the complex at 2.4 A resolution and mutational analysis of the interface.；Structure；1998 | [DOI 10.1016/S0969-2126(98)00116-6](https://doi.org/10.1016/S0969-2126(98)00116-6)；[PMID 9753694](https://pubmed.ncbi.nlm.nih.gov/9753694/) |
| [1BXI](https://www.rcsb.org/structure/1BXI) | Crystal Structure of the E.Coli Colicin E9 DNase Domain With its Cognate Immunity Protein Im9；Thesis；1998 | 原始条目列出主引用，但未提供 DOI/PMID；见条目引用元数据 |
| [1CBW](https://www.rcsb.org/structure/1CBW) | Crystal structures of bovine chymotrypsin and trypsin complexed to the inhibitor domain of Alzheimer's amyloid beta-protein precursor (APPI) and basic pancreatic trypsin inhibitor (BPTI): engineering of inhibitors with altered specificities.；Protein Sci.；1997 | [PMID 9300481](https://pubmed.ncbi.nlm.nih.gov/9300481/) |
| [1CDL](https://www.rcsb.org/structure/1CDL) | Target enzyme recognition by calmodulin: 2.4 A structure of a calmodulin-peptide complex.；Science；1992 | [PMID 1519061](https://pubmed.ncbi.nlm.nih.gov/1519061/) |
| [1CHO](https://www.rcsb.org/structure/1CHO) | Crystal and molecular structures of the complex of alpha-chymotrypsin with its inhibitor turkey ovomucoid third domain at 1.8 A resolution.；J.Mol.Biol.；1987 | [DOI 10.1016/0022-2836(87)90659-0](https://doi.org/10.1016/0022-2836(87)90659-0)；[PMID 3477645](https://pubmed.ncbi.nlm.nih.gov/3477645/) |
| [1CSE](https://www.rcsb.org/structure/1CSE) | The high-resolution X-ray crystal structure of the complex formed between subtilisin Carlsberg and eglin c, an elastase inhibitor from the leech Hirudo medicinalis. Structural analysis, subtilisin structure and interface geometry.；Eur.J.Biochem.；1987 | [DOI 10.1111/j.1432-1033.1987.tb13566.x](https://doi.org/10.1111/j.1432-1033.1987.tb13566.x)；[PMID 3301348](https://pubmed.ncbi.nlm.nih.gov/3301348/) |
| [1CSO](https://www.rcsb.org/structure/1CSO) | Deleterious effects of beta-branched residues in the S1 specificity pocket of Streptomyces griseus proteinase B (SGPB): crystal structures of the turkey ovomucoid third domain variants Ile18I, Val18I, Thr18I, and Ser18I in complex with SGPB.；Protein Sci.；2000 | [PMID 10739250](https://pubmed.ncbi.nlm.nih.gov/10739250/) |
| [1CZ8](https://www.rcsb.org/structure/1CZ8) | Selection and analysis of an optimized anti-VEGF antibody: crystal structure of an affinity-matured Fab in complex with antigen.；J.Mol.Biol.；1999 | [DOI 10.1006/jmbi.1999.3192](https://doi.org/10.1006/jmbi.1999.3192)；[PMID 10543973](https://pubmed.ncbi.nlm.nih.gov/10543973/) |
| [1DAN](https://www.rcsb.org/structure/1DAN) | The crystal structure of the complex of blood coagulation factor VIIa with soluble tissue factor.；Nature；1996 | [DOI 10.1038/380041a0](https://doi.org/10.1038/380041a0)；[PMID 8598903](https://pubmed.ncbi.nlm.nih.gov/8598903/) |
| [1DDM](https://www.rcsb.org/structure/1DDM) | Multiple modes of peptide recognition by the PTB domain of the cell fate determinant Numb.；EMBO J.；2000 | [DOI 10.1093/emboj/19.7.1505](https://doi.org/10.1093/emboj/19.7.1505)；[PMID 10747019](https://pubmed.ncbi.nlm.nih.gov/10747019/) |
| [1DFJ](https://www.rcsb.org/structure/1DFJ) | A structural basis of the interactions between leucine-rich repeats and protein ligands.；Nature；1995 | [DOI 10.1038/374183a0](https://doi.org/10.1038/374183a0)；[PMID 7877692](https://pubmed.ncbi.nlm.nih.gov/7877692/) |
| [1DQJ](https://www.rcsb.org/structure/1DQJ) | Three-dimensional structures of the free and antigen-bound Fab from monoclonal antilysozyme antibody HyHEL-63(,).；Biochemistry；2000 | [DOI 10.1021/bi000054l](https://doi.org/10.1021/bi000054l)；[PMID 10828942](https://pubmed.ncbi.nlm.nih.gov/10828942/) |
| [1DVA](https://www.rcsb.org/structure/1DVA) | Peptide exosite inhibitors of factor VIIa as anticoagulants.；Nature；2000 | [DOI 10.1038/35006574](https://doi.org/10.1038/35006574)；[PMID 10761907](https://pubmed.ncbi.nlm.nih.gov/10761907/) |
| [1DVF](https://www.rcsb.org/structure/1DVF) | Crystal structure of an Fv-Fv idiotope-anti-idiotope complex at 1.9 A resolution.；J.Mol.Biol.；1996 | [DOI 10.1006/jmbi.1996.0629](https://doi.org/10.1006/jmbi.1996.0629)；[PMID 8950273](https://pubmed.ncbi.nlm.nih.gov/8950273/) |
| [1DX5](https://www.rcsb.org/structure/1DX5) | Structural Basis for the Anticoagulant Activity of the Thrombin-Thrombomodulin Complex；Nature；2000 | [DOI 10.1038/35006683](https://doi.org/10.1038/35006683)；[PMID 10761923](https://pubmed.ncbi.nlm.nih.gov/10761923/) |
| [1DZI](https://www.rcsb.org/structure/1DZI) | Structural Basis of Collagen Recognition by Integrin Alpha2Beta1；Cell(Cambridge,Mass.)；2000 | [DOI 10.1016/S0092-8674(00)80622-4](https://doi.org/10.1016/S0092-8674(00)80622-4)；[PMID 10778855](https://pubmed.ncbi.nlm.nih.gov/10778855/) |
| [1E96](https://www.rcsb.org/structure/1E96) | Structure of the TPR domain of p67phox in complex with Rac.GTP.；Mol.Cell；2000 | [DOI 10.1016/s1097-2765(05)00091-2](https://doi.org/10.1016/s1097-2765(05)00091-2)；[PMID 11090627](https://pubmed.ncbi.nlm.nih.gov/11090627/) |
| [1EAW](https://www.rcsb.org/structure/1EAW) | Catalytic Domain Structures of Mt-Sp1/Matriptase, a Matrix-Degrading Transmembrane Serine Proteinase.；J.Biol.Chem.；2002 | [DOI 10.1074/JBC.M109830200](https://doi.org/10.1074/JBC.M109830200)；[PMID 11696548](https://pubmed.ncbi.nlm.nih.gov/11696548/) |
| [1EBP](https://www.rcsb.org/structure/1EBP) | Functional mimicry of a protein hormone by a peptide agonist: the EPO receptor complex at 2.8 A.；Science；1996 | [PMID 8662530](https://pubmed.ncbi.nlm.nih.gov/8662530/) |
| [1EFN](https://www.rcsb.org/structure/1EFN) | Crystal structure of the conserved core of HIV-1 Nef complexed with a Src family SH3 domain.；Cell(Cambridge,Mass.)；1996 | [DOI 10.1016/S0092-8674(00)81276-3](https://doi.org/10.1016/S0092-8674(00)81276-3)；[PMID 8681387](https://pubmed.ncbi.nlm.nih.gov/8681387/) |
| [1EMV](https://www.rcsb.org/structure/1EMV) | Specificity in protein-protein interactions: the structural basis for dual recognition in endonuclease colicin-immunity protein complexes.；J.Mol.Biol.；2000 | [DOI 10.1006/jmbi.2000.3945](https://doi.org/10.1006/jmbi.2000.3945)；[PMID 10966813](https://pubmed.ncbi.nlm.nih.gov/10966813/) |
| [1ES7](https://www.rcsb.org/structure/1ES7) | Crystal structure of the BMP-2-BRIA ectodomain complex.；Nat.Struct.Biol.；2000 | [DOI 10.1038/75903](https://doi.org/10.1038/75903)；[PMID 10881198](https://pubmed.ncbi.nlm.nih.gov/10881198/) |
| [1F47](https://www.rcsb.org/structure/1F47) | The bacterial cell-division protein ZipA and its interaction with an FtsZ fragment revealed by X-ray crystallography.；EMBO J.；2000 | [DOI 10.1093/emboj/19.13.3179](https://doi.org/10.1093/emboj/19.13.3179)；[PMID 10880432](https://pubmed.ncbi.nlm.nih.gov/10880432/) |
| [1F5R](https://www.rcsb.org/structure/1F5R)、[1FY8](https://www.rcsb.org/structure/1FY8)、[3TGK](https://www.rcsb.org/structure/3TGK) | The energetic cost of induced fit catalysis: Crystal structures of trypsinogen mutants with enhanced activity and inhibitor affinity.；Protein Sci.；2001 | [DOI 10.1110/ps.44101](https://doi.org/10.1110/ps.44101)；[PMID 11420435](https://pubmed.ncbi.nlm.nih.gov/11420435/) |
| [1FC2](https://www.rcsb.org/structure/1FC2) | Crystallographic refinement and atomic models of a human Fc fragment and its complex with fragment B of protein A from Staphylococcus aureus at 2.9- and 2.8-A resolution.；Biochemistry；1981 | [DOI 10.1021/bi00512a001](https://doi.org/10.1021/bi00512a001)；[PMID 7236608](https://pubmed.ncbi.nlm.nih.gov/7236608/) |
| [1FCC](https://www.rcsb.org/structure/1FCC) | Crystal structure of the C2 fragment of streptococcal protein G in complex with the Fc domain of human IgG.；Structure；1995 | [DOI 10.1016/S0969-2126(01)00157-5](https://doi.org/10.1016/S0969-2126(01)00157-5)；[PMID 7788293](https://pubmed.ncbi.nlm.nih.gov/7788293/) |
| [1FFW](https://www.rcsb.org/structure/1FFW) | Further insights into the mechanism of function of the response regulator CheY from crystallographic studies of the CheY--CheA(124--257) complex.；Acta Crystallogr.,Sect.D；2001 | [DOI 10.1107/S090744490001492X](https://doi.org/10.1107/S090744490001492X)；[PMID 11134926](https://pubmed.ncbi.nlm.nih.gov/11134926/) |
| [1FOE](https://www.rcsb.org/structure/1FOE) | Crystal structure of Rac1 in complex with the guanine nucleotide exchange region of Tiam1.；Nature；2000 | [DOI 10.1038/35047014](https://doi.org/10.1038/35047014)；[PMID 11130063](https://pubmed.ncbi.nlm.nih.gov/11130063/) |
| [1FR2](https://www.rcsb.org/structure/1FR2) | CRYSTAL STRUCTURE OF THE E9 DNASE DOMAIN WITH A MUTANT IMMUNITY PROTEIN IM9(E41A)；To be Published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |
| [1GC1](https://www.rcsb.org/structure/1GC1) | Structure of an HIV gp120 envelope glycoprotein in complex with the CD4 receptor and a neutralizing human antibody.；Nature；1998 | [DOI 10.1038/31405](https://doi.org/10.1038/31405)；[PMID 9641677](https://pubmed.ncbi.nlm.nih.gov/9641677/) |
| [1GCQ](https://www.rcsb.org/structure/1GCQ) | Novel recognition mode between Vav and Grb2 SH3 domains.；EMBO J.；2001 | [DOI 10.1093/emboj/20.12.2995](https://doi.org/10.1093/emboj/20.12.2995)；[PMID 11406576](https://pubmed.ncbi.nlm.nih.gov/11406576/) |
| [1GL0](https://www.rcsb.org/structure/1GL0)、[1GL1](https://www.rcsb.org/structure/1GL1) | Complexation of Two Proteic Insect Inhibitors to the Active Site of Chymotrypsin Suggests Decoupled Roles for Binding and Selectivity；J.Biol.Chem.；2001 | [DOI 10.1074/JBC.M105707200](https://doi.org/10.1074/JBC.M105707200)；[PMID 11495915](https://pubmed.ncbi.nlm.nih.gov/11495915/) |
| [1GL4](https://www.rcsb.org/structure/1GL4) | Structural Basis for the High-Affinity Interaction of Nidogen-1 with Immunoglobulin-Like Domain 3 of Perlecan；Embo J.；2001 | [DOI 10.1093/EMBOJ/20.19.5342](https://doi.org/10.1093/EMBOJ/20.19.5342)；[PMID 11574465](https://pubmed.ncbi.nlm.nih.gov/11574465/) |
| [1GRN](https://www.rcsb.org/structure/1GRN) | Structures of Cdc42 bound to the active and catalytically compromised forms of Cdc42GAP.；Nat.Struct.Biol.；1998 | [DOI 10.1038/4156](https://doi.org/10.1038/4156)；[PMID 9846874](https://pubmed.ncbi.nlm.nih.gov/9846874/) |
| [1H9D](https://www.rcsb.org/structure/1H9D) | The Leukemia-Associated Aml1 (Runx1)-Cbfbeta Complex Functions as a DNA-Induced Molecular Clamp；Nat.Struct.Biol.；2001 | [DOI 10.1038/86264](https://doi.org/10.1038/86264)；[PMID 11276260](https://pubmed.ncbi.nlm.nih.gov/11276260/) |
| [1HE8](https://www.rcsb.org/structure/1HE8) | Crystal Structure and Functional Analysis of Ras Binding to its Effector Phosphoinositide 3-Kinase Gamma；Cell(Cambridge,Mass.)；2000 | [DOI 10.1016/S0092-8674(00)00196-3](https://doi.org/10.1016/S0092-8674(00)00196-3)；[PMID 11136978](https://pubmed.ncbi.nlm.nih.gov/11136978/) |
| [1IAR](https://www.rcsb.org/structure/1IAR) | Crystal structure of the interleukin-4/receptor alpha chain complex reveals a mosaic binding interface.；Cell(Cambridge,Mass.)；1999 | [DOI 10.1016/S0092-8674(00)80736-9](https://doi.org/10.1016/S0092-8674(00)80736-9)；[PMID 10219247](https://pubmed.ncbi.nlm.nih.gov/10219247/) |
| [1ILP](https://www.rcsb.org/structure/1ILP) | Structure of a CXC chemokine-receptor fragment in complex with interleukin-8.；Structure Fold.Des.；1999 | [DOI 10.1016/S0969-2126(99)80022-7](https://doi.org/10.1016/S0969-2126(99)80022-7)；[PMID 10368283](https://pubmed.ncbi.nlm.nih.gov/10368283/) |
| [1JAT](https://www.rcsb.org/structure/1JAT) | Molecular insights into polyubiquitin chain assembly: crystal structure of the Mms2/Ubc13 heterodimer.；Cell(Cambridge,Mass.)；2001 | [DOI 10.1016/S0092-8674(01)00387-7](https://doi.org/10.1016/S0092-8674(01)00387-7)；[PMID 11440714](https://pubmed.ncbi.nlm.nih.gov/11440714/) |
| [1JCK](https://www.rcsb.org/structure/1JCK) | Crystal structure of a T-cell receptor beta-chain complexed with a superantigen.；Nature；1996 | [DOI 10.1038/384188a0](https://doi.org/10.1038/384188a0)；[PMID 8906797](https://pubmed.ncbi.nlm.nih.gov/8906797/) |
| [1JRH](https://www.rcsb.org/structure/1JRH) | Neutralizing epitopes on the extracellular interferon gamma receptor (IFNgammaR) alpha-chain characterized by homolog scanning mutagenesis and X-ray crystal structure of the A6 fab-IFNgammaR1-108 complex.；J.Mol.Biol.；1997 | [DOI 10.1006/jmbi.1997.1336](https://doi.org/10.1006/jmbi.1997.1336)；[PMID 9367779](https://pubmed.ncbi.nlm.nih.gov/9367779/) |
| [1JTD](https://www.rcsb.org/structure/1JTD)、[1JTG](https://www.rcsb.org/structure/1JTG) | Crystal structure and kinetic analysis of beta-lactamase inhibitor protein-II in complex with TEM-1 beta-lactamase.；Nat.Struct.Biol.；2001 | [DOI 10.1038/nsb1001-848](https://doi.org/10.1038/nsb1001-848)；[PMID 11573088](https://pubmed.ncbi.nlm.nih.gov/11573088/) |
| [1K4U](https://www.rcsb.org/structure/1K4U) | Diverse recognition of non-PxxP peptide ligands by the SH3 domains from p67(phox), Grb2 and Pex13p.；EMBO J.；2002 | [DOI 10.1093/emboj/cdf428](https://doi.org/10.1093/emboj/cdf428)；[PMID 12169629](https://pubmed.ncbi.nlm.nih.gov/12169629/) |
| [1K8R](https://www.rcsb.org/structure/1K8R) | The Ras-Byr2RBD complex: structural basis for Ras effector recognition in yeast.；Structure；2001 | [DOI 10.1016/S0969-2126(01)00674-8](https://doi.org/10.1016/S0969-2126(01)00674-8)；[PMID 11709168](https://pubmed.ncbi.nlm.nih.gov/11709168/) |
| [1KAC](https://www.rcsb.org/structure/1KAC) | Structural analysis of the mechanism of adenovirus binding to its human cellular receptor, CAR.；Science；1999 | [DOI 10.1126/science.286.5444.1579](https://doi.org/10.1126/science.286.5444.1579)；[PMID 10567268](https://pubmed.ncbi.nlm.nih.gov/10567268/) |
| [1KBH](https://www.rcsb.org/structure/1KBH) | Mutual synergistic folding in recruitment of CBP/p300 by p160 nuclear receptor coactivators.；Nature；2002 | [DOI 10.1038/415549a](https://doi.org/10.1038/415549a)；[PMID 11823864](https://pubmed.ncbi.nlm.nih.gov/11823864/) |
| [1KIP](https://www.rcsb.org/structure/1KIP) | Hydrogen bonding and solvent structure in an antigen-antibody interface. Crystal structures and thermodynamic characterization of three Fv mutants complexed with lysozyme.；Biochemistry；1996 | [DOI 10.1021/bi961709e](https://doi.org/10.1021/bi961709e)；[PMID 8952503](https://pubmed.ncbi.nlm.nih.gov/8952503/) |
| [1KTZ](https://www.rcsb.org/structure/1KTZ) | Crystal structure of the human TbetaR2 ectodomain--TGF-beta3 complex.；Nat.Struct.Biol.；2002 | [PMID 11850637](https://pubmed.ncbi.nlm.nih.gov/11850637/) |
| [1LFD](https://www.rcsb.org/structure/1LFD) | Structural basis for the interaction of Ras with RalGDS.；Nat.Struct.Biol.；1998 | [DOI 10.1038/nsb0698-422](https://doi.org/10.1038/nsb0698-422)；[PMID 9628477](https://pubmed.ncbi.nlm.nih.gov/9628477/) |
| [1LQB](https://www.rcsb.org/structure/1LQB) | Structural basis for the recognition of hydroxyproline in HIF-1 alpha by pVHL.；Nature；2002 | [DOI 10.1038/nature00767](https://doi.org/10.1038/nature00767)；[PMID 12050673](https://pubmed.ncbi.nlm.nih.gov/12050673/) |
| [1M9E](https://www.rcsb.org/structure/1M9E) | Structural insights into the catalytic mechanism of cyclophilin A；Nat.Struct.Biol.；2003 | [DOI 10.1038/nsb927](https://doi.org/10.1038/nsb927)；[PMID 12730686](https://pubmed.ncbi.nlm.nih.gov/12730686/) |
| [1MAH](https://www.rcsb.org/structure/1MAH) | Acetylcholinesterase inhibition by fasciculin: crystal structure of the complex.；Cell(Cambridge,Mass.)；1995 | [DOI 10.1016/0092-8674(95)90128-0](https://doi.org/10.1016/0092-8674(95)90128-0)；[PMID 8521480](https://pubmed.ncbi.nlm.nih.gov/8521480/) |
| [1MHP](https://www.rcsb.org/structure/1MHP) | Crystal Structure of the alpha 1 beta 1 Integrin I Domain in Complex with an Antibody Fab Fragment；J.Mol.Biol.；2003 | [DOI 10.1016/S0022-2836(03)00203-1](https://doi.org/10.1016/S0022-2836(03)00203-1)；[PMID 12662928](https://pubmed.ncbi.nlm.nih.gov/12662928/) |
| [1MLC](https://www.rcsb.org/structure/1MLC) | Three-dimensional structures of the free and the antigen-complexed Fab from monoclonal anti-lysozyme antibody D44.1.；J.Mol.Biol.；1994 | [DOI 10.1016/0022-2836(94)90046-9](https://doi.org/10.1016/0022-2836(94)90046-9)；[PMID 7966295](https://pubmed.ncbi.nlm.nih.gov/7966295/) |
| [1MQ8](https://www.rcsb.org/structure/1MQ8) | Structures of the aL I domain and its complex with ICAM-1 reveal a shape-shifting pathway for integrin regulation；Cell(Cambridge,Mass.)；2003 | [DOI 10.1016/S0092-8674(02)01257-6](https://doi.org/10.1016/S0092-8674(02)01257-6)；[PMID 12526797](https://pubmed.ncbi.nlm.nih.gov/12526797/) |
| [1MTN](https://www.rcsb.org/structure/1MTN) | Crystal structure of the bovine alpha-chymotrypsin:Kunitz inhibitor complex. An example of multiple protein:protein recognition sites.；J.Mol.Recog.；1997 | [DOI 10.1002/(SICI)1099-1352(199701/02)10:1<26::AID-JMR351>3.0.CO;2-N](https://doi.org/10.1002/(SICI)1099-1352(199701/02)10:1<26::AID-JMR351>3.0.CO;2-N)；[PMID 9179777](https://pubmed.ncbi.nlm.nih.gov/9179777/) |
| [1N8O](https://www.rcsb.org/structure/1N8O) | Crystal Structure of a Complex Between Bovine Chymotrypsin and Ecotin at 2.0 A Resolution；To be Published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |
| [1N8Z](https://www.rcsb.org/structure/1N8Z) | Structure of the Extracellular Region of HER2 Alone and in Complex with the Herceptin Fab；Nature；2003 | [DOI 10.1038/nature01392](https://doi.org/10.1038/nature01392)；[PMID 12610629](https://pubmed.ncbi.nlm.nih.gov/12610629/) |
| [1NCA](https://www.rcsb.org/structure/1NCA) | Refined crystal structure of the influenza virus N9 neuraminidase-NC41 Fab complex.；J.Mol.Biol.；1992 | [DOI 10.1016/0022-2836(92)90687-F](https://doi.org/10.1016/0022-2836(92)90687-F)；[PMID 1381757](https://pubmed.ncbi.nlm.nih.gov/1381757/) |
| [1NFI](https://www.rcsb.org/structure/1NFI) | Structure of an IkappaBalpha/NF-kappaB complex.；Cell(Cambridge,Mass.)；1998 | [DOI 10.1016/S0092-8674(00)81698-0](https://doi.org/10.1016/S0092-8674(00)81698-0)；[PMID 9865693](https://pubmed.ncbi.nlm.nih.gov/9865693/) |
| [1NMB](https://www.rcsb.org/structure/1NMB) | The structure of a complex between the NC10 antibody and influenza virus neuraminidase and comparison with the overlapping binding site of the NC41 antibody；Structure；1994 | [DOI 10.1016/S0969-2126(00)00074-5](https://doi.org/10.1016/S0969-2126(00)00074-5)；[PMID 7994573](https://pubmed.ncbi.nlm.nih.gov/7994573/) |
| [1NVU](https://www.rcsb.org/structure/1NVU) | Structural evidence for feedback activation by RasGTP of the Ras-specific nucleotide exchange factor SOS；Cell(Cambridge,Mass.)；2003 | [DOI 10.1016/S0092-8674(03)00149-1](https://doi.org/10.1016/S0092-8674(03)00149-1)；[PMID 12628188](https://pubmed.ncbi.nlm.nih.gov/12628188/) |
| [1P69](https://www.rcsb.org/structure/1P69) | Structural basis for variation in adenovirus affinity for the cellular coxsackievirus and adenovirus receptor.；J.Biol.Chem.；2003 | [DOI 10.1074/jbc.M301492200](https://doi.org/10.1074/jbc.M301492200)；[PMID 12716886](https://pubmed.ncbi.nlm.nih.gov/12716886/) |
| [1PPF](https://www.rcsb.org/structure/1PPF) | X-ray crystal structure of the complex of human leukocyte elastase (PMN elastase) and the third domain of the turkey ovomucoid inhibitor.；EMBO J.；1986 | [PMID 3640709](https://pubmed.ncbi.nlm.nih.gov/3640709/) |
| [1R0R](https://www.rcsb.org/structure/1R0R) | Structure and energetics of protein-protein interactions: the role of conformational heterogeneity in OMTKY3 binding to serine proteases；J.Mol.Biol.；2003 | [DOI 10.1016/S0022-2836(03)00783-6](https://doi.org/10.1016/S0022-2836(03)00783-6)；[PMID 12888355](https://pubmed.ncbi.nlm.nih.gov/12888355/) |
| [1REW](https://www.rcsb.org/structure/1REW) | Molecular recognition of BMP-2 and BMP receptor IA.；Nat.Struct.Mol.Biol.；2004 | [DOI 10.1038/nsmb756](https://doi.org/10.1038/nsmb756)；[PMID 15064755](https://pubmed.ncbi.nlm.nih.gov/15064755/) |
| [1S0W](https://www.rcsb.org/structure/1S0W) | The modular architecture of protein-protein binding interfaces.；Proc.Natl.Acad.Sci.USA；2005 | [DOI 10.1073/pnas.0407280102](https://doi.org/10.1073/pnas.0407280102)；[PMID 15618400](https://pubmed.ncbi.nlm.nih.gov/15618400/) |
| [1S1Q](https://www.rcsb.org/structure/1S1Q) | Ubiquitin recognition by the human TSG101 protein；Mol.Cell；2004 | [DOI 10.1016/S1097-2765(04)00129-7](https://doi.org/10.1016/S1097-2765(04)00129-7)；[PMID 15053872](https://pubmed.ncbi.nlm.nih.gov/15053872/) |
| [1S78](https://www.rcsb.org/structure/1S78) | Insights into ErbB signaling from the structure of the ErbB2-pertuzumab complex.；Cancer Cell；2004 | [DOI 10.1016/S1535-6108(04)00083-2](https://doi.org/10.1016/S1535-6108(04)00083-2)；[PMID 15093539](https://pubmed.ncbi.nlm.nih.gov/15093539/) |
| [1SBB](https://www.rcsb.org/structure/1SBB) | Three-dimensional structure of the complex between a T cell receptor beta chain and the superantigen staphylococcal enterotoxin B.；Immunity；1998 | [DOI 10.1016/S1074-7613(00)80646-9](https://doi.org/10.1016/S1074-7613(00)80646-9)；[PMID 9881971](https://pubmed.ncbi.nlm.nih.gov/9881971/) |
| [1SBN](https://www.rcsb.org/structure/1SBN)、[1SIB](https://www.rcsb.org/structure/1SIB) | Refined crystal structures of subtilisin novo in complex with wild-type and two mutant eglins. Comparison with other serine proteinase inhibitor complexes.；J.Mol.Biol.；1991 | [DOI 10.1016/0022-2836(91)90549-L](https://doi.org/10.1016/0022-2836(91)90549-L)；[PMID 1992167](https://pubmed.ncbi.nlm.nih.gov/1992167/) |
| [1SGD](https://www.rcsb.org/structure/1SGD) | Recruitment of a Buried K+ Ion to Stabilize the Negative Charge of Ionized P1 in the Hydrophobic Pocket: Crystal Structures of Glu18, Gln18, Asp18 and Asn18 Variants of Turkey Ovomucoid Inhibitor Third Domain Complexed with Streptomyces griseus Protease B at Various pH's；To be Published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |
| [1SMF](https://www.rcsb.org/structure/1SMF) | Studies on an artificial trypsin inhibitor peptide derived from the mung bean trypsin inhibitor: chemical synthesis, refolding, and crystallographic analysis of its complex with trypsin.；J.Biochem.(Tokyo)；1994 | [PMID 7798176](https://pubmed.ncbi.nlm.nih.gov/7798176/) |
| [1T83](https://www.rcsb.org/structure/1T83) | The structure of a human type III Fcgamma receptor in complex with Fc；J.Biol.Chem.；2001 | [DOI 10.1074/jbc.M100350200](https://doi.org/10.1074/jbc.M100350200)；[PMID 11297532](https://pubmed.ncbi.nlm.nih.gov/11297532/) |
| [1TM1](https://www.rcsb.org/structure/1TM1) | Binding, Proteolytic, and Crystallographic Analyses of Mutations at the Protease-Inhibitor Interface of the Subtilisin BPN'/Chymotrypsin Inhibitor 2 Complex(,).；Biochemistry；2004 | [DOI 10.1021/bi048797k](https://doi.org/10.1021/bi048797k)；[PMID 15504027](https://pubmed.ncbi.nlm.nih.gov/15504027/) |
| [1U0S](https://www.rcsb.org/structure/1U0S) | In different organisms, the mode of interaction between two signaling proteins is not necessarily conserved；Proc.Natl.Acad.Sci.USA；2004 | [DOI 10.1073/pnas.0401038101](https://doi.org/10.1073/pnas.0401038101)；[PMID 15289606](https://pubmed.ncbi.nlm.nih.gov/15289606/) |
| [1U7F](https://www.rcsb.org/structure/1U7F) | Structural basis of heteromeric smad protein assembly in tgf-Beta signaling；Mol.Cell；2004 | [DOI 10.1016/j.molcel.2004.07.016](https://doi.org/10.1016/j.molcel.2004.07.016)；[PMID 15350224](https://pubmed.ncbi.nlm.nih.gov/15350224/) |
| [1UB4](https://www.rcsb.org/structure/1UB4) | Crystal Structure of the MazE/MazF Complex. Molecular Bases of Antidote-Toxin Recognition；Mol.Cell；2003 | [DOI 10.1016/S1097-2765(03)00097-2](https://doi.org/10.1016/S1097-2765(03)00097-2)；[PMID 12718874](https://pubmed.ncbi.nlm.nih.gov/12718874/) |
| [1UUZ](https://www.rcsb.org/structure/1UUZ) | Structure and Evolution of the Ivy Protein Family, Unexpected Lysozyme Inhibitors in Gram-Negative Bacteria.；Proc.Natl.Acad.Sci.USA；2007 | [DOI 10.1073/PNAS.0611019104](https://doi.org/10.1073/PNAS.0611019104)；[PMID 17405861](https://pubmed.ncbi.nlm.nih.gov/17405861/) |
| [1VFB](https://www.rcsb.org/structure/1VFB) | Bound water molecules and conformational stabilization help mediate an antigen-antibody association.；Proc.Natl.Acad.Sci.USA；1994 | [DOI 10.1073/pnas.91.3.1089](https://doi.org/10.1073/pnas.91.3.1089)；[PMID 8302837](https://pubmed.ncbi.nlm.nih.gov/8302837/) |
| [1X1W](https://www.rcsb.org/structure/1X1W) | Water-mediated interaction at a protein-protein interface；Chem.Phys.；2004 | 原始条目列出主引用，但未提供 DOI/PMID；见条目引用元数据 |
| [1XD3](https://www.rcsb.org/structure/1XD3) | Structure of the Ubiquitin Hydrolase UCH-L3 Complexed with a Suicide Substrate；J.Biol.Chem.；2005 | [DOI 10.1074/jbc.M410770200](https://doi.org/10.1074/jbc.M410770200)；[PMID 15531586](https://pubmed.ncbi.nlm.nih.gov/15531586/) |
| [1XXM](https://www.rcsb.org/structure/1XXM) | The modular architecture of protein-protein binding interfaces；Proc.Natl.Acad.Sci.USA；2005 | [DOI 10.1073/pnas.0407280102](https://doi.org/10.1073/pnas.0407280102)；[PMID 15618400](https://pubmed.ncbi.nlm.nih.gov/15618400/) |
| [1Y1K](https://www.rcsb.org/structure/1Y1K) | Role of the intramolecular hydrogen bond network in the inhibitory power of chymotrypsin inhibitor 2；Biochemistry；2005 | [DOI 10.1021/bi047301w](https://doi.org/10.1021/bi047301w)；[PMID 15865427](https://pubmed.ncbi.nlm.nih.gov/15865427/) |
| [1YCR](https://www.rcsb.org/structure/1YCR) | Structure of the MDM2 oncoprotein bound to the p53 tumor suppressor transactivation domain.；Science；1996 | [DOI 10.1126/science.274.5289.948](https://doi.org/10.1126/science.274.5289.948)；[PMID 8875929](https://pubmed.ncbi.nlm.nih.gov/8875929/) |
| [1YCS](https://www.rcsb.org/structure/1YCS) | Structure of the p53 tumor suppressor bound to the ankyrin and SH3 domains of 53BP2.；Science；1996 | [DOI 10.1126/science.274.5289.1001](https://doi.org/10.1126/science.274.5289.1001)；[PMID 8875926](https://pubmed.ncbi.nlm.nih.gov/8875926/) |
| [1YY9](https://www.rcsb.org/structure/1YY9) | Structural basis for inhibition of the epidermal growth factor receptor by cetuximab；Cancer Cell；2005 | [DOI 10.1016/j.ccr.2005.03.003](https://doi.org/10.1016/j.ccr.2005.03.003)；[PMID 15837620](https://pubmed.ncbi.nlm.nih.gov/15837620/) |
| [1Z7X](https://www.rcsb.org/structure/1Z7X) | Inhibition of human pancreatic ribonuclease by the human ribonuclease inhibitor protein.；J.Mol.Biol.；2007 | [DOI 10.1016/j.jmb.2007.02.005](https://doi.org/10.1016/j.jmb.2007.02.005)；[PMID 17350650](https://pubmed.ncbi.nlm.nih.gov/17350650/) |
| [2A9K](https://www.rcsb.org/structure/2A9K) | Crystal structure of the C3bot-RalA complex reveals a novel type of action of a bacterial exoenzyme.；Embo J.；2005 | [DOI 10.1038/sj.emboj.7600813](https://doi.org/10.1038/sj.emboj.7600813)；[PMID 16177825](https://pubmed.ncbi.nlm.nih.gov/16177825/) |
| [2ABZ](https://www.rcsb.org/structure/2ABZ) | Study of a major intermediate in the oxidative folding of leech carboxypeptidase inhibitor: contribution of the fourth disulfide bond；J.Mol.Biol.；2005 | [DOI 10.1016/j.jmb.2005.07.065](https://doi.org/10.1016/j.jmb.2005.07.065)；[PMID 16126224](https://pubmed.ncbi.nlm.nih.gov/16126224/) |
| [2AJF](https://www.rcsb.org/structure/2AJF) | Structure of SARS coronavirus spike receptor-binding domain complexed with receptor.；Science；2005 | [DOI 10.1126/science.1116480](https://doi.org/10.1126/science.1116480)；[PMID 16166518](https://pubmed.ncbi.nlm.nih.gov/16166518/) |
| [2B0Z](https://www.rcsb.org/structure/2B0Z) | Effects of interface mutations on association modes and electron-transfer rates between proteins；Proc.Natl.Acad.Sci.Usa；2005 | [DOI 10.1073/pnas.0505176102](https://doi.org/10.1073/pnas.0505176102)；[PMID 16227441](https://pubmed.ncbi.nlm.nih.gov/16227441/) |
| [2B42](https://www.rcsb.org/structure/2B42) | Identification of structural determinants for inhibition strength and specificity of wheat xylanase inhibitors TAXI-IA and TAXI-IIA.；Febs J.；2009 | [DOI 10.1111/j.1742-4658.2009.07105.x](https://doi.org/10.1111/j.1742-4658.2009.07105.x)；[PMID 19769747](https://pubmed.ncbi.nlm.nih.gov/19769747/) |
| [2BTF](https://www.rcsb.org/structure/2BTF) | The structure of crystalline profilin-beta-actin.；Nature；1993 | [DOI 10.1038/365810a0](https://doi.org/10.1038/365810a0)；[PMID 8413665](https://pubmed.ncbi.nlm.nih.gov/8413665/) |
| [2C0L](https://www.rcsb.org/structure/2C0L) | Recognition of a Functional Peroxisome Type 1 Target by the Dynamic Import Receptor Pex5P.；Mol.Cell；2006 | [DOI 10.1016/J.MOLCEL.2006.10.024](https://doi.org/10.1016/J.MOLCEL.2006.10.024)；[PMID 17157249](https://pubmed.ncbi.nlm.nih.gov/17157249/) |
| [2FTL](https://www.rcsb.org/structure/2FTL) | Rigidification of a Flexible Protease Inhibitor Variant upon Binding to Trypsin.；J.Mol.Biol.；2007 | [DOI 10.1016/j.jmb.2006.11.003](https://doi.org/10.1016/j.jmb.2006.11.003)；[PMID 17157870](https://pubmed.ncbi.nlm.nih.gov/17157870/) |
| [2G2U](https://www.rcsb.org/structure/2G2U) | Structural and Computational Characterization of the SHV-1 beta-Lactamase-beta-Lactamase Inhibitor Protein Interface.；J.Biol.Chem.；2006 | [DOI 10.1074/jbc.M603878200](https://doi.org/10.1074/jbc.M603878200)；[PMID 16809340](https://pubmed.ncbi.nlm.nih.gov/16809340/) |
| [2GOX](https://www.rcsb.org/structure/2GOX) | A structural basis for complement inhibition by Staphylococcus aureus.；Nat.Immunol.；2007 | [DOI 10.1038/ni1450](https://doi.org/10.1038/ni1450)；[PMID 17351618](https://pubmed.ncbi.nlm.nih.gov/17351618/) |
| [2GYK](https://www.rcsb.org/structure/2GYK) | Crystal structures of the complexes of the Colicin E9 DNase domain with mutant immunity proteins；To be Published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |
| [2HHB](https://www.rcsb.org/structure/2HHB) | The crystal structure of human deoxyhaemoglobin at 1.74 A resolution；J.Mol.Biol.；1984 | [DOI 10.1016/0022-2836(84)90472-8](https://doi.org/10.1016/0022-2836(84)90472-8)；[PMID 6726807](https://pubmed.ncbi.nlm.nih.gov/6726807/) |
| [2HLE](https://www.rcsb.org/structure/2HLE) | Structural and Biophysical Characterization of the EphB4-EphrinB2 Protein-Protein Interaction and Receptor Specificity.；J.Biol.Chem.；2006 | [DOI 10.1074/jbc.M605766200](https://doi.org/10.1074/jbc.M605766200)；[PMID 16867992](https://pubmed.ncbi.nlm.nih.gov/16867992/) |
| [2HRK](https://www.rcsb.org/structure/2HRK) | Structural basis of yeast aminoacyl-tRNA synthetase complex formation revealed by crystal structures of two binary sub-complexes.；Nucleic Acids Res.；2006 | [DOI 10.1093/nar/gkl560](https://doi.org/10.1093/nar/gkl560)；[PMID 16914447](https://pubmed.ncbi.nlm.nih.gov/16914447/) |
| [2I26](https://www.rcsb.org/structure/2I26) | Maturation of Shark Single-domain (IgNAR) Antibodies: Evidence for Induced-fit Binding.；J.Mol.Biol.；2007 | [DOI 10.1016/j.jmb.2006.12.045](https://doi.org/10.1016/j.jmb.2006.12.045)；[PMID 17258766](https://pubmed.ncbi.nlm.nih.gov/17258766/) |
| [2I9B](https://www.rcsb.org/structure/2I9B) | Structural basis of interaction between urokinase-type plasminogen activator and its receptor.；J.Mol.Biol.；2006 | [DOI 10.1016/j.jmb.2006.08.063](https://doi.org/10.1016/j.jmb.2006.08.063)；[PMID 16979660](https://pubmed.ncbi.nlm.nih.gov/16979660/) |
| [2J0T](https://www.rcsb.org/structure/2J0T) | Crystal Structure of the Catalytic Domain of Matrix Metalloproteinase-1 in Complex with the Inhibitory Domain of Tissue Inhibitor of Metalloproteinase-1.；J.Biol.Chem.；2007 | [DOI 10.1074/JBC.M607625200](https://doi.org/10.1074/JBC.M607625200)；[PMID 17050530](https://pubmed.ncbi.nlm.nih.gov/17050530/) |
| [2J12](https://www.rcsb.org/structure/2J12)、[2J1K](https://www.rcsb.org/structure/2J1K) | Structural and Mutational Analysis of Human Ad37 and Canine Adenovirus 2 Fiber Heads in Complex with the D1 Domain of Coxsackie and Adenovirus Receptor.；J.Biol.Chem.；2006 | [DOI 10.1074/JBC.M605316200](https://doi.org/10.1074/JBC.M605316200)；[PMID 16923808](https://pubmed.ncbi.nlm.nih.gov/16923808/) |
| [2JEL](https://www.rcsb.org/structure/2JEL) | The 2.5 A resolution structure of the jel42 Fab fragment/HPr complex；J.Mol.Biol.；1998 | [DOI 10.1006/jmbi.1998.1888](https://doi.org/10.1006/jmbi.1998.1888)；[PMID 9671553](https://pubmed.ncbi.nlm.nih.gov/9671553/) |
| [2KSO](https://www.rcsb.org/structure/2KSO) | Structure and function of the EphA2:SHIP2 SAM domain heterodimer；To be Published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |
| [2MVM](https://www.rcsb.org/structure/2MVM) | Evolutionarily Conserved Binding of Translationally Controlled Tumor Protein to Eukaryotic Elongation Factor 1B.；J.Biol.Chem.；2015 | [DOI 10.1074/jbc.M114.628594](https://doi.org/10.1074/jbc.M114.628594)；[PMID 25635048](https://pubmed.ncbi.nlm.nih.gov/25635048/) |
| [2NMB](https://www.rcsb.org/structure/2NMB) | Structure of a Numb PTB domain-peptide complex suggests a basis for diverse binding specificity.；Nat.Struct.Biol.；1998 | [DOI 10.1038/4185](https://doi.org/10.1038/4185)；[PMID 9846878](https://pubmed.ncbi.nlm.nih.gov/9846878/) |
| [2NOJ](https://www.rcsb.org/structure/2NOJ) | Characterization of Ehp, a Secreted Complement Inhibitory Protein from Staphylococcus aureus.；J.Biol.Chem.；2007 | [DOI 10.1074/jbc.M704247200](https://doi.org/10.1074/jbc.M704247200)；[PMID 17699522](https://pubmed.ncbi.nlm.nih.gov/17699522/) |
| [2NU0](https://www.rcsb.org/structure/2NU0) | Molecular structures of the complexes of SGPB with OMTKY3 aromatic P1 variants Trp18I, His18I, Phe18I, and Tyr18I；To be Published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |
| [2NY7](https://www.rcsb.org/structure/2NY7) | Structural definition of a conserved neutralization epitope on HIV-1 gp120.；Nature；2007 | [DOI 10.1038/nature05580](https://doi.org/10.1038/nature05580)；[PMID 17301785](https://pubmed.ncbi.nlm.nih.gov/17301785/) |
| [2NYY](https://www.rcsb.org/structure/2NYY)、[2NZ9](https://www.rcsb.org/structure/2NZ9) | Molecular evolution of antibody cross-reactivity for two subtypes of type A botulinum neurotoxin.；Nat.Biotechnol.；2007 | [DOI 10.1038/nbt1269](https://doi.org/10.1038/nbt1269)；[PMID 17173035](https://pubmed.ncbi.nlm.nih.gov/17173035/) |
| [2O3B](https://www.rcsb.org/structure/2O3B) | The nuclease a-inhibitor complex is characterized by a novel metal ion bridge.；J.Biol.Chem.；2007 | [DOI 10.1074/jbc.M605986200](https://doi.org/10.1074/jbc.M605986200)；[PMID 17138564](https://pubmed.ncbi.nlm.nih.gov/17138564/) |
| [2OOB](https://www.rcsb.org/structure/2OOB) | Structural basis for ubiquitin-mediated dimerization and activation of the ubiquitin protein ligase Cbl-b.；Mol.Cell；2007 | [DOI 10.1016/j.molcel.2007.06.023](https://doi.org/10.1016/j.molcel.2007.06.023)；[PMID 17679095](https://pubmed.ncbi.nlm.nih.gov/17679095/) |
| [2PCB](https://www.rcsb.org/structure/2PCB)、[2PCC](https://www.rcsb.org/structure/2PCC) | Crystal structure of a complex between electron transfer partners, cytochrome c peroxidase and cytochrome c.；Science；1992 | [PMID 1334573](https://pubmed.ncbi.nlm.nih.gov/1334573/) |
| [2PTC](https://www.rcsb.org/structure/2PTC) | The Geometry of the Reactive Site and of the Peptide Groups in Trypsin, Trypsinogen and its Complexes with Inhibitors；Acta Crystallogr.,Sect.B；1983 | 原始条目列出主引用，但未提供 DOI/PMID；见条目引用元数据 |
| [2QJ9](https://www.rcsb.org/structure/2QJ9) | Structure analysis of bone morphogenetic protein-2 type I receptor complexes reveals a mechanism of receptor inactivation in juvenile polyposis syndrome.；J.Biol.Chem.；2008 | [DOI 10.1074/jbc.M706029200](https://doi.org/10.1074/jbc.M706029200)；[PMID 18160401](https://pubmed.ncbi.nlm.nih.gov/18160401/) |
| [2REX](https://www.rcsb.org/structure/2REX) | Crystal structure of the effector domain of PLXNB1 bound with Rnd1 GTPase.；To be Published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |
| [2RF9](https://www.rcsb.org/structure/2RF9) | Inhibition of the EGF receptor by binding of MIG6 to an activating kinase domain interface.；Nature；2007 | [DOI 10.1038/nature05998](https://doi.org/10.1038/nature05998)；[PMID 18046415](https://pubmed.ncbi.nlm.nih.gov/18046415/) |
| [2SGP](https://www.rcsb.org/structure/2SGP) | Contribution of peptide bonds to inhibitor-protease binding: crystal structures of the turkey ovomucoid third domain backbone variants OMTKY3-Pro18I and OMTKY3-psi[COO]-Leu18I in complex with Streptomyces griseus proteinase B (SGPB) and the structure of the free inhibitor, OMTKY-3-psi[CH2NH2+]-Asp19I；J.Mol.Biol.；2001 | [DOI 10.1006/jmbi.2000.4343](https://doi.org/10.1006/jmbi.2000.4343)；[PMID 11162096](https://pubmed.ncbi.nlm.nih.gov/11162096/) |
| [2SIC](https://www.rcsb.org/structure/2SIC) | Refined crystal structure of the complex of subtilisin BPN' and Streptomyces subtilisin inhibitor at 1.8 A resolution.；J.Mol.Biol.；1991 | [PMID 1920411](https://pubmed.ncbi.nlm.nih.gov/1920411/) |
| [2V55](https://www.rcsb.org/structure/2V55) | Mechanism of Multi-Site Phosphorylation from a Rock-I:Rhoe Complex Structure.；Embo J.；2008 | [DOI 10.1038/EMBOJ.2008.226](https://doi.org/10.1038/EMBOJ.2008.226)；[PMID 18946488](https://pubmed.ncbi.nlm.nih.gov/18946488/) |
| [2VIR](https://www.rcsb.org/structure/2VIR) | Antigen distortion allows influenza virus to escape neutralization.；Nat.Struct.Biol.；1998 | [DOI 10.1038/nsb0298-119](https://doi.org/10.1038/nsb0298-119)；[PMID 9461077](https://pubmed.ncbi.nlm.nih.gov/9461077/) |
| [2VLJ](https://www.rcsb.org/structure/2VLJ) | The Structural Dynamics and Energetics of an Immunodominant T-Cell Receptor are Programmed by its Vbeta Domain；Immunity；2008 | [DOI 10.1016/J.IMMUNI.2007.12.018](https://doi.org/10.1016/J.IMMUNI.2007.12.018)；[PMID 18275829](https://pubmed.ncbi.nlm.nih.gov/18275829/) |
| [2VLN](https://www.rcsb.org/structure/2VLN) | Experimental and Computational Analyses of the Energetic Basis for Dual Recognition of Immunity Proteins by Colicin Endonucleases.；J.Mol.Biol.；2008 | [DOI 10.1016/J.JMB.2008.03.055](https://doi.org/10.1016/J.JMB.2008.03.055)；[PMID 18471830](https://pubmed.ncbi.nlm.nih.gov/18471830/) |
| [2WPT](https://www.rcsb.org/structure/2WPT) | The Structural and Energetic Basis for High Selectivity in a High-Affinity Protein-Protein Interaction.；Proc.Natl.Acad.Sci.USA；2010 | [DOI 10.1073/PNAS.0910756107](https://doi.org/10.1073/PNAS.0910756107)；[PMID 20479265](https://pubmed.ncbi.nlm.nih.gov/20479265/) |
| [2X0B](https://www.rcsb.org/structure/2X0B) | A Redox Switch in Angiotensinogen Modulates Angiotensin Release.；Nature；2010 | [DOI 10.1038/NATURE09505](https://doi.org/10.1038/NATURE09505)；[PMID 20927107](https://pubmed.ncbi.nlm.nih.gov/20927107/) |
| [3A5C](https://www.rcsb.org/structure/3A5C) | Inter-subunit interaction and quaternary rearrangement defined by the central stalk of prokaryotic V1-ATPase；Embo Rep.；2009 | [DOI 10.1038/embor.2009.202](https://doi.org/10.1038/embor.2009.202)；[PMID 19779483](https://pubmed.ncbi.nlm.nih.gov/19779483/) |
| [3BDY](https://www.rcsb.org/structure/3BDY)、[3BE1](https://www.rcsb.org/structure/3BE1) | Variants of the antibody herceptin that interact with HER2 and VEGF at the antigen binding site；Science；2009 | [DOI 10.1126/science.1165480](https://doi.org/10.1126/science.1165480)；[PMID 19299620](https://pubmed.ncbi.nlm.nih.gov/19299620/) |
| [3BIW](https://www.rcsb.org/structure/3BIW) | Structures of Neuroligin-1 and the Neuroligin-1/Neurexin-1beta Complex Reveal Specific Protein-Protein and Protein-Ca(2+) Interactions.；Neuron；2007 | [DOI 10.1016/j.neuron.2007.12.002](https://doi.org/10.1016/j.neuron.2007.12.002)；[PMID 18093522](https://pubmed.ncbi.nlm.nih.gov/18093522/) |
| [3BK3](https://www.rcsb.org/structure/3BK3) | Crystal structure analysis reveals how the Chordin family member crossveinless 2 blocks BMP-2 receptor binding；Dev.Cell；2008 | [DOI 10.1016/j.devcel.2008.02.017](https://doi.org/10.1016/j.devcel.2008.02.017)；[PMID 18477456](https://pubmed.ncbi.nlm.nih.gov/18477456/) |
| [3BN9](https://www.rcsb.org/structure/3BN9) | Structure of an Fab-protease complex reveals a highly specific non-canonical mechanism of inhibition；J.Mol.Biol.；2008 | [DOI 10.1016/j.jmb.2008.05.009](https://doi.org/10.1016/j.jmb.2008.05.009)；[PMID 18514224](https://pubmed.ncbi.nlm.nih.gov/18514224/) |
| [3BP8](https://www.rcsb.org/structure/3BP8) | Analyses of Mlc-IIBGlc interaction and a plausible molecular mechanism of Mlc inactivation by membrane sequestration；Proc.Natl.Acad.Sci.Usa；2008 | [DOI 10.1073/pnas.0709295105](https://doi.org/10.1073/pnas.0709295105)；[PMID 18319344](https://pubmed.ncbi.nlm.nih.gov/18319344/) |
| [3BTD](https://www.rcsb.org/structure/3BTD) | The crystal structures of the complexes between bovine beta-trypsin and ten P1 variants of BPTI.；J.Mol.Biol.；1999 | [DOI 10.1006/jmbi.1999.2654](https://doi.org/10.1006/jmbi.1999.2654)；[PMID 10222201](https://pubmed.ncbi.nlm.nih.gov/10222201/) |
| [3D5R](https://www.rcsb.org/structure/3D5R) | Electrostatic contributions drive the interaction between Staphylococcus aureus protein Efb-C and its complement target C3d.；Protein Sci.；2008 | [DOI 10.1110/ps.036624.108](https://doi.org/10.1110/ps.036624.108)；[PMID 18687868](https://pubmed.ncbi.nlm.nih.gov/18687868/) |
| [3HFM](https://www.rcsb.org/structure/3HFM) | Structure of an antibody-antigen complex: crystal structure of the HyHEL-10 Fab-lysozyme complex.；Proc.Natl.Acad.Sci.USA；1989 | [DOI 10.1073/pnas.86.15.5938](https://doi.org/10.1073/pnas.86.15.5938)；[PMID 2762305](https://pubmed.ncbi.nlm.nih.gov/2762305/) |
| [3HHR](https://www.rcsb.org/structure/3HHR) | Human growth hormone and extracellular domain of its receptor: crystal structure of the complex.；Science；1992 | [PMID 1549776](https://pubmed.ncbi.nlm.nih.gov/1549776/) |
| [3K2M](https://www.rcsb.org/structure/3K2M) | A potent and highly specific FN3 monobody inhibitor of the Abl SH2 domain.；Nat.Struct.Mol.Biol.；2010 | [DOI 10.1038/nsmb.1793](https://doi.org/10.1038/nsmb.1793)；[PMID 20357770](https://pubmed.ncbi.nlm.nih.gov/20357770/) |
| [3MBW](https://www.rcsb.org/structure/3MBW) | Architecture of Eph receptor clusters.；Proc.Natl.Acad.Sci.USA；2010 | [DOI 10.1073/pnas.1004148107](https://doi.org/10.1073/pnas.1004148107)；[PMID 20505120](https://pubmed.ncbi.nlm.nih.gov/20505120/) |
| [3NGB](https://www.rcsb.org/structure/3NGB) | Structural basis for broad and potent neutralization of HIV-1 by antibody VRC01.；Science；2010 | [DOI 10.1126/science.1192819](https://doi.org/10.1126/science.1192819)；[PMID 20616231](https://pubmed.ncbi.nlm.nih.gov/20616231/) |
| [3NPS](https://www.rcsb.org/structure/3NPS) | A reverse binding motif that contributes to specific protease inhibition by antibodies.；J.Mol.Biol.；2012 | [DOI 10.1016/j.jmb.2011.11.036](https://doi.org/10.1016/j.jmb.2011.11.036)；[PMID 22154938](https://pubmed.ncbi.nlm.nih.gov/22154938/) |
| [3Q3J](https://www.rcsb.org/structure/3Q3J) | Crystal structure of plexin A2 RBD in complex with Rnd1；to be published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |
| [3SAK](https://www.rcsb.org/structure/3SAK) | Improving the Packing and Accuracy of NMR Structure with a Pseudopotential for the Radius of Gyration；J.Am.Chem.Soc.；1999 | [DOI 10.1021/ja9843730](https://doi.org/10.1021/ja9843730) |
| [3SE8](https://www.rcsb.org/structure/3SE8)、[3SE9](https://www.rcsb.org/structure/3SE9) | Focused evolution of HIV-1 neutralizing antibodies revealed by structures and deep sequencing.；Science；2011 | [DOI 10.1126/science.1207532](https://doi.org/10.1126/science.1207532)；[PMID 21835983](https://pubmed.ncbi.nlm.nih.gov/21835983/) |
| [3SGB](https://www.rcsb.org/structure/3SGB) | Structure of the complex of Streptomyces griseus protease B and the third domain of the turkey ovomucoid inhibitor at 1.8-A resolution.；Biochemistry；1983 | [DOI 10.1021/bi00288a012](https://doi.org/10.1021/bi00288a012)；[PMID 6414511](https://pubmed.ncbi.nlm.nih.gov/6414511/) |
| [3W2D](https://www.rcsb.org/structure/3W2D) | Structural basis for the neutralization and specificity of Staphylococcal enterotoxin B against its MHC Class II binding site.；MAbs；2014 | [DOI 10.4161/mabs.27106](https://doi.org/10.4161/mabs.27106)；[PMID 24423621](https://pubmed.ncbi.nlm.nih.gov/24423621/) |
| [3WJJ](https://www.rcsb.org/structure/3WJJ) | Engineered antibody Fc variant with selectively enhanced Fc gamma RIIb binding over both Fc gamma RIIaR131 and Fc gamma RIIaH131.；Protein Eng.Des.Sel.；2013 | [DOI 10.1093/protein/gzt022](https://doi.org/10.1093/protein/gzt022)；[PMID 23744091](https://pubmed.ncbi.nlm.nih.gov/23744091/) |
| [3ZJY](https://www.rcsb.org/structure/3ZJY) | Structural Basis for the Nuclear Export Activity of Importin13.；Embo J.；2013 | [DOI 10.1038/EMBOJ.2013.29](https://doi.org/10.1038/EMBOJ.2013.29)；[PMID 23435562](https://pubmed.ncbi.nlm.nih.gov/23435562/) |
| [4BFI](https://www.rcsb.org/structure/4BFI) | Structures of Cd200/Cd200 Receptor Family and Implications for Topology, Regulation, and Evolution；Structure；2013 | [DOI 10.1016/J.STR.2013.03.008](https://doi.org/10.1016/J.STR.2013.03.008)；[PMID 23602662](https://pubmed.ncbi.nlm.nih.gov/23602662/) |
| [4BJ5](https://www.rcsb.org/structure/4BJ5)、[4BJT](https://www.rcsb.org/structure/4BJT) | Rif1 and Rif2 Shape Telomere Funcation and Architecture Through Multivalent RAP1 Interactions；Cell(Cambridge,Mass.)；2013 | [DOI 10.1016/J.CELL.2013.05.007](https://doi.org/10.1016/J.CELL.2013.05.007)；[PMID 23746845](https://pubmed.ncbi.nlm.nih.gov/23746845/) |
| [4BKL](https://www.rcsb.org/structure/4BKL) | Epitope-Specific Antibody Response is Controlled by Immunoglobulin Vh Polymorphisms.；J.Exp.Med.；2014 | [DOI 10.1084/JEM.20130968](https://doi.org/10.1084/JEM.20130968)；[PMID 24534192](https://pubmed.ncbi.nlm.nih.gov/24534192/) |
| [4BKX](https://www.rcsb.org/structure/4BKX) | Class I Hdacs Share a Common Mechanism of Regulation by Inositol Phosphates.；Mol.Cell；2013 | [DOI 10.1016/J.MOLCEL.2013.05.020](https://doi.org/10.1016/J.MOLCEL.2013.05.020)；[PMID 23791785](https://pubmed.ncbi.nlm.nih.gov/23791785/) |
| [4BPX](https://www.rcsb.org/structure/4BPX) | Structures of Human Primase Reveal Design of Nucleotide Elongation Site and Mode of Pol Alpha Tethering；Proc.Natl.Acad.Sci.USA；2013 | [DOI 10.1073/PNAS.1311185110](https://doi.org/10.1073/PNAS.1311185110)；[PMID 24043831](https://pubmed.ncbi.nlm.nih.gov/24043831/) |
| [4BRU](https://www.rcsb.org/structure/4BRU) | Structural Analysis of the Yeast Dhh1-Pat1 Complex Reveals How Dhh1 Engages Pat1, Edc3 and RNA in Mutually Exclusive Interactions；Nucleic Acids Res.；2013 | [DOI 10.1093/NAR/GKT600](https://doi.org/10.1093/NAR/GKT600)；[PMID 23851565](https://pubmed.ncbi.nlm.nih.gov/23851565/) |
| [4BSR](https://www.rcsb.org/structure/4BSR) | Structure of Stem Cell Growth Factor R-Spondin 1 in Complex with the Ectodomain of its Receptor Lgr5.；Cell Rep.；2013 | [DOI 10.1016/J.CELREP.2013.06.009](https://doi.org/10.1016/J.CELREP.2013.06.009)；[PMID 23809763](https://pubmed.ncbi.nlm.nih.gov/23809763/) |
| [4CPA](https://www.rcsb.org/structure/4CPA) | Refined crystal structure of the potato inhibitor complex of carboxypeptidase A at 2.5 A resolution.；J.Mol.Biol.；1982 | [DOI 10.1016/0022-2836(82)90309-6](https://doi.org/10.1016/0022-2836(82)90309-6)；[PMID 7154070](https://pubmed.ncbi.nlm.nih.gov/7154070/) |
| [4EKC](https://www.rcsb.org/structure/4EKC) | Structural and functional analysis of the regulator of G protein signaling 2-g alpha q complex.；Structure；2013 | [DOI 10.1016/j.str.2012.12.016](https://doi.org/10.1016/j.str.2012.12.016)；[PMID 23434405](https://pubmed.ncbi.nlm.nih.gov/23434405/) |
| [4FZA](https://www.rcsb.org/structure/4FZA) | Structure of the MST4 in Complex with MO25 Provides Insights into Its Activation Mechanism；Structure；2013 | [DOI 10.1016/j.str.2013.01.007](https://doi.org/10.1016/j.str.2013.01.007)；[PMID 23434407](https://pubmed.ncbi.nlm.nih.gov/23434407/) |
| [4GKO](https://www.rcsb.org/structure/4GKO) | Ca2+-dependent Structural Changes in the B-cell Receptor CD23 Increase Its Affinity for Human Immunoglobulin E.；J.Biol.Chem.；2013 | [DOI 10.1074/jbc.M113.480657](https://doi.org/10.1074/jbc.M113.480657)；[PMID 23775083](https://pubmed.ncbi.nlm.nih.gov/23775083/) |
| [4GNK](https://www.rcsb.org/structure/4GNK) | Full-length G alpha (q)-phospholipase C-beta 3 structure reveals interfaces of the C-terminal coiled-coil domain.；Nat.Struct.Mol.Biol.；2013 | [DOI 10.1038/nsmb.2497](https://doi.org/10.1038/nsmb.2497)；[PMID 23377541](https://pubmed.ncbi.nlm.nih.gov/23377541/) |
| [4GU0](https://www.rcsb.org/structure/4GU0) | Structural insight into substrate recognition by histone demethylase LSD2/KDM1b；Cell Res.；2013 | [DOI 10.1038/cr.2013.17](https://doi.org/10.1038/cr.2013.17)；[PMID 23357850](https://pubmed.ncbi.nlm.nih.gov/23357850/) |
| [4HMY](https://www.rcsb.org/structure/4HMY) | Structural Basis for Recruitment and Activation of the AP-1 Clathrin Adaptor Complex by Arf1.；Cell(Cambridge,Mass.)；2013 | [DOI 10.1016/j.cell.2012.12.042](https://doi.org/10.1016/j.cell.2012.12.042)；[PMID 23415225](https://pubmed.ncbi.nlm.nih.gov/23415225/) |
| [4HSA](https://www.rcsb.org/structure/4HSA) | Crystal structures of interleukin 17A and its complex with IL-17 receptor A.；Nat Commun；2013 | [DOI 10.1038/ncomms2880](https://doi.org/10.1038/ncomms2880)；[PMID 23695682](https://pubmed.ncbi.nlm.nih.gov/23695682/) |
| [4IDJ](https://www.rcsb.org/structure/4IDJ) | Mechanism of Action and In Vivo Efficacy of a Human-Derived Antibody against Staphylococcus aureus alpha-Hemolysin.；J.Mol.Biol.；2013 | [DOI 10.1016/j.jmb.2013.02.008](https://doi.org/10.1016/j.jmb.2013.02.008)；[PMID 23416200](https://pubmed.ncbi.nlm.nih.gov/23416200/) |
| [4IOF](https://www.rcsb.org/structure/4IOF) | Conformational states and recognition of amyloidogenic peptides of human insulin-degrading enzyme.；Proc.Natl.Acad.Sci.USA；2013 | [DOI 10.1073/pnas.1304575110](https://doi.org/10.1073/pnas.1304575110)；[PMID 23922390](https://pubmed.ncbi.nlm.nih.gov/23922390/) |
| [4J2L](https://www.rcsb.org/structure/4J2L) | Structural basis of protein complex formation and reconfiguration by polyglutamine disease protein Ataxin-1 and Capicua；Genes Dev.；2013 | [DOI 10.1101/gad.212068.112](https://doi.org/10.1101/gad.212068.112)；[PMID 23512657](https://pubmed.ncbi.nlm.nih.gov/23512657/) |
| [4JEU](https://www.rcsb.org/structure/4JEU) | Syntaxin1a variants lacking an N-peptide or bearing the LE mutation bind to Munc18a in a closed conformation.；Proc.Natl.Acad.Sci.USA；2013 | [DOI 10.1073/pnas.1303753110](https://doi.org/10.1073/pnas.1303753110)；[PMID 23858467](https://pubmed.ncbi.nlm.nih.gov/23858467/) |
| [4JGH](https://www.rcsb.org/structure/4JGH) | Structural basis of intersubunit recognition in elongin BC-cullin 5-SOCS box ubiquitin-protein ligase complexes.；Acta Crystallogr.,Sect.D；2013 | [DOI 10.1107/S0907444913011220](https://doi.org/10.1107/S0907444913011220)；[PMID 23897481](https://pubmed.ncbi.nlm.nih.gov/23897481/) |
| [4KRM](https://www.rcsb.org/structure/4KRM)、[4KRO](https://www.rcsb.org/structure/4KRO)、[4KRP](https://www.rcsb.org/structure/4KRP) | Structural Evaluation of EGFR Inhibition Mechanisms for Nanobodies/VHH Domains.；Structure；2013 | [DOI 10.1016/j.str.2013.05.008](https://doi.org/10.1016/j.str.2013.05.008)；[PMID 23791944](https://pubmed.ncbi.nlm.nih.gov/23791944/) |
| [4L72](https://www.rcsb.org/structure/4L72) | Structure of MERS-CoV spike receptor-binding domain complexed with human receptor DPP4；Cell Res.；2013 | [DOI 10.1038/cr.2013.92](https://doi.org/10.1038/cr.2013.92)；[PMID 23835475](https://pubmed.ncbi.nlm.nih.gov/23835475/) |
| [4LRX](https://www.rcsb.org/structure/4LRX) | Coiled-Coil Helix Rotation Selects Repressing or Activating State of Transcriptional Regulator DhaR.；Structure；2014 | [DOI 10.1016/j.str.2013.11.012](https://doi.org/10.1016/j.str.2013.11.012)；[PMID 24440518](https://pubmed.ncbi.nlm.nih.gov/24440518/) |
| [4MYW](https://www.rcsb.org/structure/4MYW) | Crystal structure of herpes simplex virus 2 gD bound to nectin-1 reveals a conserved mode of receptor recognition.；J.Virol.；2014 | [DOI 10.1128/JVI.01906-14](https://doi.org/10.1128/JVI.01906-14)；[PMID 25231300](https://pubmed.ncbi.nlm.nih.gov/25231300/) |
| [4NM8](https://www.rcsb.org/structure/4NM8) | A common solution to group 2 influenza virus neutralization.；Proc.Natl.Acad.Sci.USA；2014 | [DOI 10.1073/pnas.1319058110](https://doi.org/10.1073/pnas.1319058110)；[PMID 24335589](https://pubmed.ncbi.nlm.nih.gov/24335589/) |
| [4NZW](https://www.rcsb.org/structure/4NZW)、[4O27](https://www.rcsb.org/structure/4O27) | Structural insights into regulatory mechanisms of MO25-mediated kinase activation.；J.Struct.Biol.；2014 | [DOI 10.1016/j.jsb.2014.04.005](https://doi.org/10.1016/j.jsb.2014.04.005)；[PMID 24746913](https://pubmed.ncbi.nlm.nih.gov/24746913/) |
| [4OFY](https://www.rcsb.org/structure/4OFY) | Extracellular Architecture of the SYG-1/SYG-2 Adhesion Complex Instructs Synaptogenesis.；Cell(Cambridge,Mass.)；2014 | [DOI 10.1016/j.cell.2014.01.004](https://doi.org/10.1016/j.cell.2014.01.004)；[PMID 24485456](https://pubmed.ncbi.nlm.nih.gov/24485456/) |
| [4OZG](https://www.rcsb.org/structure/4OZG) | T-cell receptor recognition of HLA-DQ2-gliadin complexes associated with celiac disease.；Nat.Struct.Mol.Biol.；2014 | [DOI 10.1038/nsmb.2817](https://doi.org/10.1038/nsmb.2817)；[PMID 24777060](https://pubmed.ncbi.nlm.nih.gov/24777060/) |
| [4P23](https://www.rcsb.org/structure/4P23)、[4P5T](https://www.rcsb.org/structure/4P5T) | Effect of CDR3 Sequences and Distal V Gene Residues in Regulating TCR-MHC Contacts and Ligand Specificity.；J Immunol.；2014 | [DOI 10.4049/jimmunol.1303209](https://doi.org/10.4049/jimmunol.1303209)；[PMID 24813203](https://pubmed.ncbi.nlm.nih.gov/24813203/) |
| [4P4Q](https://www.rcsb.org/structure/4P4Q) | Chemical constraints on the radical cation center of cytochrome c peroxidase for long-range electron transfer；to be published； | 原始条目主引用标作待发表；没有可列出的正式论文 DOI/PMID |
| [4PJ8](https://www.rcsb.org/structure/4PJ8) | A molecular basis underpinning the T cell receptor heterogeneity of mucosal-associated invariant T cells.；J.Exp.Med.；2014 | [DOI 10.1084/jem.20140484](https://doi.org/10.1084/jem.20140484)；[PMID 25049336](https://pubmed.ncbi.nlm.nih.gov/25049336/) |
| [4PWX](https://www.rcsb.org/structure/4PWX) | Crystal structure of ATP-bound Get3-Get4-Get5 complex reveals regulation of Get3 by Get4.；Nat.Struct.Mol.Biol.；2014 | [DOI 10.1038/nsmb.2813](https://doi.org/10.1038/nsmb.2813)；[PMID 24727835](https://pubmed.ncbi.nlm.nih.gov/24727835/) |
| [4QT8](https://www.rcsb.org/structure/4QT8) | Structural basis for the binding specificity of human Recepteur d'Origine Nantais (RON) receptor tyrosine kinase to macrophage-stimulating protein.；J.Biol.Chem.；2014 | [DOI 10.1074/jbc.M114.594341](https://doi.org/10.1074/jbc.M114.594341)；[PMID 25193665](https://pubmed.ncbi.nlm.nih.gov/25193665/) |
| [4QTI](https://www.rcsb.org/structure/4QTI) | Stabilizing a flexible interdomain hinge region harboring the SMB binding site drives uPAR into its closed conformation.；J.Mol.Biol.；2015 | [DOI 10.1016/j.jmb.2015.01.022](https://doi.org/10.1016/j.jmb.2015.01.022)；[PMID 25659907](https://pubmed.ncbi.nlm.nih.gov/25659907/) |
| [4R2G](https://www.rcsb.org/structure/4R2G) | Structural Evolution of Glycan Recognition by a Family of Potent HIV Antibodies.；Cell(Cambridge,Mass.)；2014 | [DOI 10.1016/j.cell.2014.09.009](https://doi.org/10.1016/j.cell.2014.09.009)；[PMID 25259921](https://pubmed.ncbi.nlm.nih.gov/25259921/) |
| [4RA0](https://www.rcsb.org/structure/4RA0) | An engineered Axl 'decoy receptor' effectively silences the Gas6-Axl signaling axis.；Nat.Chem.Biol.；2014 | [DOI 10.1038/nchembio.1636](https://doi.org/10.1038/nchembio.1636)；[PMID 25242553](https://pubmed.ncbi.nlm.nih.gov/25242553/) |
| [4RWS](https://www.rcsb.org/structure/4RWS) | Structural biology. Crystal structure of the chemokine receptor CXCR4 in complex with a viral chemokine.；Science；2015 | [DOI 10.1126/science.1261064](https://doi.org/10.1126/science.1261064)；[PMID 25612609](https://pubmed.ncbi.nlm.nih.gov/25612609/) |
| [4U2X](https://www.rcsb.org/structure/4U2X) | Ebola Virus VP24 Targets a Unique NLS Binding Site on Karyopherin Alpha 5 to Selectively Compete with Nuclear Import of Phosphorylated STAT1.；Cell Host Microbe；2014 | [DOI 10.1016/j.chom.2014.07.008](https://doi.org/10.1016/j.chom.2014.07.008)；[PMID 25121748](https://pubmed.ncbi.nlm.nih.gov/25121748/) |
| [4U6H](https://www.rcsb.org/structure/4U6H) | Potent neutralization of vaccinia virus by divergent murine antibodies targeting a common site of vulnerability in l1 protein.；J.Virol.；2014 | [DOI 10.1128/JVI.01491-14](https://doi.org/10.1128/JVI.01491-14)；[PMID 25031354](https://pubmed.ncbi.nlm.nih.gov/25031354/) |
| [4UWQ](https://www.rcsb.org/structure/4UWQ) | Structural Basis for Specificity and Promiscuity in a Carrier Protein/Enzyme System from the Sulfur Cycle；Proc.Natl.Acad.Sci.USA；2015 | [DOI 10.1073/PNAS.1506386112](https://doi.org/10.1073/PNAS.1506386112)；[PMID 26655737](https://pubmed.ncbi.nlm.nih.gov/26655737/) |
| [4V0M](https://www.rcsb.org/structure/4V0M) | Structural Basis for Membrane Targeting of the Bbsome by Arl6；Nat.Struct.Mol.Biol.；2014 | [DOI 10.1038/NSMB.2920](https://doi.org/10.1038/NSMB.2920)；[PMID 25402481](https://pubmed.ncbi.nlm.nih.gov/25402481/) |
| [4X4M](https://www.rcsb.org/structure/4X4M) | Structure of Fc gamma RI in complex with Fc reveals the importance of glycan recognition for high-affinity IgG binding.；Proc.Natl.Acad.Sci.USA；2015 | [DOI 10.1073/pnas.1418812112](https://doi.org/10.1073/pnas.1418812112)；[PMID 25561553](https://pubmed.ncbi.nlm.nih.gov/25561553/) |
| [4XHJ](https://www.rcsb.org/structure/4XHJ) | A site of varicella-zoster virus vulnerability identified by structural studies of neutralizing antibodies bound to the glycoprotein complex gHgL.；Proc.Natl.Acad.Sci.USA；2015 | [DOI 10.1073/pnas.1501176112](https://doi.org/10.1073/pnas.1501176112)；[PMID 25918416](https://pubmed.ncbi.nlm.nih.gov/25918416/) |
| [4Y61](https://www.rcsb.org/structure/4Y61) | Structure of Slitrk2-PTP delta complex reveals mechanisms for splicing-dependent trans-synaptic adhesion.；Sci Rep；2015 | [DOI 10.1038/srep09686](https://doi.org/10.1038/srep09686)；[PMID 25989451](https://pubmed.ncbi.nlm.nih.gov/25989451/) |
| [4YEB](https://www.rcsb.org/structure/4YEB) | Structural and Mechanistic Insights into the Latrophilin3-FLRT3 Complex that Mediates Glutamatergic Synapse Development.；Structure；2015 | [DOI 10.1016/j.str.2015.06.022](https://doi.org/10.1016/j.str.2015.06.022)；[PMID 26235031](https://pubmed.ncbi.nlm.nih.gov/26235031/) |
| [4YFD](https://www.rcsb.org/structure/4YFD)、[4YH7](https://www.rcsb.org/structure/4YH7) | Mechanisms of splicing-dependent trans-synaptic adhesion by PTP delta-IL1RAPL1/IL-1RAcP for synaptic differentiation.；Nat Commun；2015 | [DOI 10.1038/ncomms7926](https://doi.org/10.1038/ncomms7926)；[PMID 25908590](https://pubmed.ncbi.nlm.nih.gov/25908590/) |
| [4YPG](https://www.rcsb.org/structure/4YPG) | Structural Insights into the Neutralization Properties of the Fully Human, Anti-interferon Monoclonal Antibody Sifalimumab.；J.Biol.Chem.；2015 | [DOI 10.1074/jbc.M115.652156](https://doi.org/10.1074/jbc.M115.652156)；[PMID 25925951](https://pubmed.ncbi.nlm.nih.gov/25925951/) |
| [4ZGQ](https://www.rcsb.org/structure/4ZGQ) | Cdc123, a Cell Cycle Regulator Needed for eIF2 Assembly, Is an ATP-Grasp Protein with Unique Features.；Structure；2015 | [DOI 10.1016/j.str.2015.06.014](https://doi.org/10.1016/j.str.2015.06.014)；[PMID 26211610](https://pubmed.ncbi.nlm.nih.gov/26211610/) |
| [4ZS6](https://www.rcsb.org/structure/4ZS6) | Structural basis for the neutralization of MERS-CoV by a human monoclonal antibody MERS-27；Sci Rep；2015 | [DOI 10.1038/srep13133](https://doi.org/10.1038/srep13133)；[PMID 26281793](https://pubmed.ncbi.nlm.nih.gov/26281793/) |
| [5C6T](https://www.rcsb.org/structure/5C6T) | Structure of HCMV glycoprotein B in the postfusion conformation bound to a neutralizing human antibody.；Nat Commun；2015 | [DOI 10.1038/ncomms9176](https://doi.org/10.1038/ncomms9176)；[PMID 26365435](https://pubmed.ncbi.nlm.nih.gov/26365435/) |
| [5CYK](https://www.rcsb.org/structure/5CYK) | The structure of Erb1-Ytm1 complex reveals the functional importance of a high-affinity binding between two beta-propellers during the assembly of large ribosomal subunits in eukaryotes.；Nucleic Acids Res.；2015 | [DOI 10.1093/nar/gkv1043](https://doi.org/10.1093/nar/gkv1043)；[PMID 26476442](https://pubmed.ncbi.nlm.nih.gov/26476442/) |
| [5D3I](https://www.rcsb.org/structure/5D3I) | Structural basis for inhibition of TLR2 by staphylococcal superantigen-like protein 3 (SSL3).；Proc.Natl.Acad.Sci.USA；2015 | [DOI 10.1073/pnas.1502026112](https://doi.org/10.1073/pnas.1502026112)；[PMID 26283364](https://pubmed.ncbi.nlm.nih.gov/26283364/) |
| [5DWU](https://www.rcsb.org/structure/5DWU) | CSL311, a novel, potent, therapeutic monoclonal antibody for the treatment of diseases mediated by the common beta chain of the IL-3, GM-CSF and IL-5 receptors.；Mabs；2016 | [DOI 10.1080/19420862.2015.1119352](https://doi.org/10.1080/19420862.2015.1119352)；[PMID 26651396](https://pubmed.ncbi.nlm.nih.gov/26651396/) |
| [5E6P](https://www.rcsb.org/structure/5E6P) | Secondary PDZ domain-binding site on class B plexins enhances the affinity for PDZ-RhoGEF.；Proc.Natl.Acad.Sci.USA；2015 | [DOI 10.1073/pnas.1508931112](https://doi.org/10.1073/pnas.1508931112)；[PMID 26627240](https://pubmed.ncbi.nlm.nih.gov/26627240/) |
| [5K39](https://www.rcsb.org/structure/5K39) | Diverse specificity of cellulosome attachment to the bacterial cell surface.；Sci Rep；2016 | [DOI 10.1038/srep38292](https://doi.org/10.1038/srep38292)；[PMID 27924829](https://pubmed.ncbi.nlm.nih.gov/27924829/) |

## 其他

### 数据范围和限制

当前公开子包仍位于 staging，五份附件及其中可验证的 229 个 PDB 锚点已经验收；完整数据库恢复和 1TPQ 原生两层仍未完成。该子包可用于来源目录、聚合计数与结构覆盖核对，不能作为论文所述 5,291 条定量记录使用。

### 完整性与验收

payload 共 5 文件、203.49 KiB (208,373 bytes)；同样排序 inventory SHA-256 为 `2c15ac8f003ab038c1a24c5fdde329b2986097676585700ba7894b302b2aa38f`。独立审计要求 config 中目标文件集合与实际完全一致（允许 source README，保留上游自己的 README），拒绝 symlink、旁路 JSON/API/manifest、partial 文件或缺少任何可公开 PDB 层。PDF 页数/签名、XLSX 全部 worksheet、ZIP 全部 CRC 与安全成员均按文件类型核验；研究审计结果只保存本人 context，不发布为 raw sidecar。

上游 payload 文件身份；SHA-256 为获取后固定的本地值：

| payload 文件 | 大小 | 上游校验 | 本地 SHA-256 |
| --- | --- | --- | --- |
| dbMPIKT_2018-11-27_BMC-AdditionalFile1.xlsx | 60.77 KiB (62,228 bytes) | `md5:7af781e1955d88e573ea628a437d7796` | `6dd7450bf1b8021e0d84d974ccbd7cdff333b7a8b1dd4ef577b7ff679dc6cb78` |
| dbMPIKT_2018-11-27_BMC-AdditionalFile2.xlsx | 38.11 KiB (39,022 bytes) | `md5:bf5fea6cbe826e19f95f05dc7116d5c6` | `51305fd105cb4c2306a7cd511282806287a22b9281b5cf194e18355fbb825b60` |
| dbMPIKT_2018-11-27_BMC-AdditionalFile3.xlsx | 10.62 KiB (10,875 bytes) | `md5:e7b534af7c3c5dae693880171f3b12df` | `e2854a2f593572cc51cb5bd23e714627de512980686b036715475d915e4b897b` |
| dbMPIKT_2018-11-27_BMC-AdditionalFile4.png | 22.21 KiB (22,744 bytes) | `md5:a0924992da3f4ddf885f4eaa60a33334` | `c5a3918de92cce6090dea22ed840e1678cba44f825df9e7f3b5b96cc82fd7ab5` |
| dbMPIKT_2018-11-27_BMC-AdditionalFile5.png | 71.78 KiB (73,504 bytes) | `md5:6cc1bce71327203e69dabcb1751783b9` | `06e9cf0fb09ac6c805a8219ca53b2eee5cb2c0964ea37189d63502a553968f74` |

### 许可和再分发边界

正式文章采用 CC BY 4.0，并声明文章所提供的数据适用 CC0（另有说明者除外）；五个 Figshare v1 对象的许可元数据为 CC BY + CC0。该声明覆盖当前正式附件，不据此推定已消失的历史全库导出或 SKEMPI、AB-Bind、BID 等上游原始数据均获得同一再分发许可。

### 公开范围对照

| 论文或来源所述内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 论文报告的 5,291 条突变个体测量 | 当前附件只含独立清单、复合物目录、聚合计数和图片；历史服务不可用 | 未获得全库 |
| 正式论文五份附件 | Figshare collection 的 3 XLSX + 2 PNG 均按官方大小和 MD5 验收；主文 PDF 已归档 | 已包含 |
| 论文报告 233 个 PDB | 附件可识别 230 个唯一候选；229 个有完整 RCSB FASTA/mmCIF | 部分包含；论文与附件的 3 个差额无公开逐项映射 |
| 1TPQ | 2026-09-24 官方状态仍为 WDRN/UNRELEASED，FASTA/mmCIF 404 | 不可公开取得 |

## 待解决问题与处理进展

- **Q1｜完整 dbMPIKT 逐记录导出尚未取得（阻塞完整研究获取）**：论文报告 5,291 条突变记录，但 Figshare collection 仅有五份补充附件，历史站点在 2026-09-24 仍不可用，公开仓储与历史存档追查也未发现原库 dump。当前只按 `public-subset` 保存并解释附件，不从并排清单或下游子集重建测量表。下一步是联系论文通讯作者或数据库维护方索取带 schema、单位、版本和许可说明的原始 export；取得后须核对 5,291 条记录、四个来源计数、缺失值及哈希，另建或更新可追溯版本。更新于 2026-09-24。
- **Q2｜1TPQ 没有可取得的原生序列和坐标（阻塞当前 PDB 完整发布）**：该编号由 Additional File 2 明确给出，但 RCSB holdings 为 `UNRELEASED/WDRN`，FASTA 与 mmCIF 均为 404。当前保留 229/230 的 partial 状态，不删除锚点、不猜测替代结构。关闭条件是 RCSB 发布 1TPQ，或来源方提供能够逐项证明替代 accession 的一手映射；随后补取并验收 FASTA/mmCIF。更新于 2026-09-24。
- **Q3｜论文 PDB 总数与附件可识别编号相差 3 个（影响结构覆盖口径）**：论文报告 233 个 PDB，两个附件指定列的并集为 230 个，公开材料没有给出差额的逐项身份。当前分别报告两种计数，不把数量差额推成具体 accession。若取得全库导出或作者映射，应重新审计唯一 PDB 集合及与 12 个无 PDB 复合物的关系。更新于 2026-09-24。
