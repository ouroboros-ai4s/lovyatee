# SRC_R60_ALPHAPROTEO 数据说明

## 数据集身份

- `source_id`：`SRC_R60_ALPHAPROTEO`
- `source_version`：`snapshot-2024-09-12`
- 原作者或发布机构：Vinicius Zambaldi 等；Google DeepMind、Francis Crick Institute 及论文共同作者

## 实验设计和数据口径

AlphaProteo 为 de novo 蛋白 binder 设计研究，不是抗体突变数据。先生成候选并以预测复合物指标筛选，随后 yeast display 评估结合命中；部分命中进入表达纯化，再用 HTRF 拟合亲和力，并对部分候选用 BLI 与结构验证。病毒抑制 EC50 是功能测定，不能与靶点结合 KD 合并为同一标签。

主表报告八个实验靶点的 861 个测试候选：BHRF1 94、SC2RBD 172、IL7RA 94、PD-L1 159、TrkA 131、IL17A 63、VEGFA 94、TNFα 54。TNFα 没有观察到设计命中；861 是测试规模，不是公开序列数。S1 还列两个仅计算比较靶点，因此其 10 个输入不能等同于 10 个成功湿实验靶点。

S7 有 32 行：25 个 GDM 设计、7 个对照。28 行有字面完整序列（25 个设计加 3 个 RFdiffusion 对照），4 个对照只给出处，未公开该表中的字面序列。25 个设计的靶点计数为 BHRF1 3、SC2RBD 6、IL7RA 3、PDL1 3、TrkA 3、VEGFA 4、IL17A 3；这是筛选/表达后选出的样本，不能代表全部 861 个候选或全部负例。

S7 的 KD_mean 是 HTRF 汇总 nM，越小结合越强；σ_replicas 描述重复间差异，σ_fit 描述拟合误差，不是两份独立实验标签。Replicas 实際范围 1–20；caption 写 1–18，但 RFD_PDL1_76 对照为 20，保留矛盾。RFD_TrkA_88 单次重复的 σ_replicas 为 `-`，不是零。不同 assay、对照构型和删失范围不自动统一；S4 的 EC50（μM）与标准误是病毒抑制结果。

SC2RBD、PDL1、TrkA 用于开发/筛选规则优化；这些靶点的测试表现不能全部视为盲测外部泛化。共享靶点、相似序列、重复与结构训练先验应在模型评估切分中记录。本次公开材料是 PDF/HTML 中的处理后表与图，不是全候选库或仪器最底层 raw。

## 论文原文

- 标题：De novo design of high-affinity protein binders with AlphaProteo
- 作者：Vinicius Zambaldi 等（完整作者列表见归档主文）
- 载体与版本：arXiv:2409.08022v1；45 页 PDF 与同版 HTML
- 发布日期：2024-09-12（arXiv v1 提交）；PDF 内部报告日期为 2024-09-05
- DOI：10.48550/arXiv.2409.08022
- PMID / PMCID：无（本版本为 arXiv 预印本）
- 本地文件：`articles/AlphaProteo_2024-09-12_arXiv-v1.pdf`
- 文件大小：12333400 bytes
- SHA-256：`953b35644c0fa06ff090d7614c2e19525831f8fde50242e176d54474133c5a42`
- 文本许可：CC BY-NC-SA 4.0（arXiv 页面）
- 补充材料：S1–S7 与补充正文包含在同一 45 页 PDF/HTML，不另造 XLSX/CSV

## 仓库内容

一手入口为 [arXiv 固定 v1](https://arxiv.org/abs/2409.08022v1)，版本目录 `snapshot-2024-09-12` 由 arXiv 提交日期决定，不能用 PDF 内部 2024-09-05 或本次下载日期替代。HTML 是同版完整上游页面原字节，不是项目导出的表格。选择性公开包保存全文及其公开嵌入表，没有拿未公开全候选库冒充完整数据包。

执行清单给出的 Figshare `439fdd59488215753bc3` 位于正文 S4.1，明确是 RFdiffusion 对照序列下载；不能作为 AlphaProteo 原研究整包来源。本次未将该对照下载混入 AlphaProteo payload。

```text
snapshot-2024-09-12/
└── AlphaProteo/
    └── AlphaProteo_2024-09-12_arXiv-v1.html
```

表格、归档与其记录关系见数据结构；上游说明、许可或嵌入资源保留原始内容。

## 数据结构

### 嵌入表与连接关系

HTML 的完整表保留公式、rowspan 和空续行；读取时需要理解每个表的粒度。S7 的表 ID 为 `Ax3.T7.3`，并非只搜 figure wrapper 就能找到的标准附件文件。S3 是 yeast 命中、表达与 HTRF 测试阶段的聚合数量表，不是逐设计 BLI KD 表。

| 原表 | HTML table ID | 实际内容 |
| --- | --- | --- |
| 主 Table 1 | S2.T1.3 | 八靶点测试量、成功率等聚合汇总 |
| S1 | Ax3.T1.3 | 10 个靶点输入、作者链与残基区间、模型设定 |
| S2 | Ax3.T2.3 | 模型/方法/过滤方案比较的聚合结果 |
| S3 | Ax3.T3.3 | yeast 命中、表达、HTRF 阶段的数量；非 BLI 逐设计标签 |
| S4 | Ax3.T4.3 | 16 个设计×病毒变体×重复的 EC50 结果，续行继承名称 |
| S5 | Ax3.T5.3 | 四个 cryo-EM 设计的结构采集/重构统计 |
| S6 | Ax3.T6.3 | VEGFA 设计 71 的晶体学统计 |
| S7 | Ax3.T7.3 | 32 条设计/对照的 KD、误差、重复数、序列 |

HTML 中有 18 个 U+200B zero-width space、13 个 U+2061 数学函数符号；它们主要来自公式/注释排版。原始字符计数与 DOM 可见文本计数不同：去 annotation 的解析副本中，U+200B 出现在 S2.T1.3（1）、A1.EGx2（4）、Ax3.T2.3（5）、Ax3.T4.3（1）；U+2061 出现在 A1.EGx1（4）、Ax3.T6.3（1）、Ax3.T7.3（3）。剩余字符位于表外正文或 annotation；没有混入 S7 设计序列。MathML 的 annotation 会重复公式语义文本。审计只在解析 DOM 副本中去掉 annotation，不修改原始 HTML，也不把公式排版字符默默合并进生物序列。S7 的 25 条 GDM Sequence 均仅含标准 20 氨基酸字符。

### 字段说明

| S7 原字段（DOM 文本） | 语义别名（非原字段） | 原始类型与含义 |
| --- | --- | --- |
| Design | design_name | 字符串；GDM 设计或外部对照名称，按前缀/引用区分 |
| μ ⁡ ( K D ) (nM) | KD_mean | 数字文本；HTRF 平均解离常数，nM，越小越强；不是 EC50 |
| σ ⁡ ( K D ) repl. | σ_replicas | 数字文本或 -；重复间标准差，nM，单次测量的 - 不作零 |
| σ ⁡ ( K D ) fit | σ_fit | 数字文本；拟合不确定性，nM，与重复差异分开 |
| Replicas | replicate_count | 整数字符串；实际表 1–20，不是新增设计数 |
| Sequence | sequence_or_reference | 字符串；完整设计序列或对照文献引用，不能把引用填成臆造序列 |

数值表头含 MathML 下标；以上保留去掉重复 annotation 后的原始 DOM 文本与 U+2061。展示形式分别为 μ(K_D)、σ(K_D) repl.、σ(K_D) fit。语义别名仅供本文解释，没有改写 HTML。S1 的 PDB/Chains/Residues 是输入编号、作者链和残基区间字符串；S4 的 EC50/SE 为实验功能抑制与标准误数字文本（μM），不与 nM KD 合并。

### 数据示例

S7 实际行 `GDM_IL7RA_70`：KD_mean=`0.082` nM，σ_replicas=`0.007` nM，σ_fit=`0.01` nM，Replicas=`2`；这是一条设计的汇总，不是两条独立候选。

Sequence 原文：

```text
MTKVEEAKELVDKIMEAAKAKDLEKVNKLRTEFFELVNSLSLEEAEEVRKYADKKGEEWYKEQL
```

S4 中同一设计的不同变体/重复具有独立功能测量行，不能复制 S7 KD 作为每个病毒变体的真值。

## PDB 数据库

S1 给出 10 个输入结构锚点，另以 S1.8/S12 引用的 7ZBU 商业抗体复合物作为结构比较参考，共 11 份完整 RCSB FASTA/mmCIF 对。S1 的作者链和区间只描述模型输入，文件仍保留完整条目全部 entity、原子和伴侣，未裁剪或嫁接公开设计序列。

2WH6 A 对应 BHRF1，6M0J E 对应 SC2RBD，3DI3 B 对应 IL7RA，5O45 A 对应 PD-L1，1WWW X 对应 TrkA，4ZXB E 为原表标作 Insulin 的比较输入，但该链实体字面描述为 insulin receptor（保留原标签与解释），5VLI A/B 为 H1 比较输入，1BJ1 V/W 对应 VEGFA，4HSA A/B 对应 IL17A，1TNF A/B/C 对应 TNF。输入中原生 Fab/受体/其他伴侣不是 GDM binder；7ZBU 亦不是本文新设计复合物。

论文称新 cryo-EM 结构将提交，未给出可验证的新设计 PDB accession。本次在 RCSB 官方 Search API 检索 `GDM_VEGFA_71`、`AlphaProteo` 与论文完整标题，返回 204/no hits；该检索不能证明以后不会有结构，仅说明此次无法建立可靠新设计 accession 映射。PDB 输入/参考补充已完成，新设计实验复合物映射仍为 partial。

获取/核验日期 2026-09-18。每个编号使用 RCSB `https://www.rcsb.org/fasta/entry/<PDB_ID>/download` 与 `https://files.rcsb.org/download/<PDB_ID>.cif`。校验 FASTA entity ID 集合及全序列与 mmCIF canonical entity 全序列严格相等，并核对 entry.id、非空原子坐标和 author-chain。共 11 个完整对，22 个文件，9,496,033 bytes。按相对路径排序拼接 `relative_path<TAB>bytes<TAB>sha256<LF>` 后 inventory SHA-256 为 `133608690b529462f5db26e00dd97faad038ac53d42fd7334280f102f1a4e5f6`。

| PDB | FASTA bytes | FASTA SHA-256 | mmCIF bytes | mmCIF SHA-256 |
| --- | --- | --- | --- | --- |
| 2WH6 | 339 | `0db767bf56449cfe790105cc8038bf80ece1205219262500d964f6537b045617` | 229144 | `149d06ba396c29129b810e54137ddb9f9c193eaf23e08ff89a158a1063b40ad9` |
| 6M0J | 1001 | `0c00927ac0ba87015372fc0c25bfdaa1ab72528aff30789d49bfe2757821c7de` | 739607 | `ec1bbd3e64524f4ec91803781fb065bc8bb7559a67b60fcc2bfb5a08dae3cba6` |
| 3DI3 | 502 | `5c52237977b8b234a443aea5c93fb4eec5e33d53f241218a7bbe1370724cfcf5` | 312813 | `04ff2f0e75713307824e6cdbf9674a5920b194bcf086a782fbee7a529ab43eb1` |
| 5O45 | 319 | `2dfd85005468bcfea13556c4646b2f910a920c46009a6d7ef96b84b020474ac6` | 498156 | `25ca22e457201020ff0635ff3b52088493403f087df7d86fbf6de2a8eee01d03` |
| 1WWW | 389 | `48ee7313a040b6f8fe2ae93865c4a93c2a74b49f8ffab158371d74188b99c698` | 403710 | `5ffccf33eede677e90647e84b9ddfaa28b33205a6535ce1b8931e8ebf0ba04a9` |
| 4ZXB | 2058 | `6f6efe48a834960bc1237d8c9240b11900238e0ac5668aef85405b6ac0a3b84b` | 2539573 | `71032662335eb268246c8c0a055976af43d4b1688c9b2bf41c5685ab00e6aa88` |
| 5VLI | 820 | `4e3030f3b8c1c9c0db74f861ba3537dd5f5b08658e9963363bb665d9fea4d059` | 916277 | `2d4c5d6ec272732ec1da14a93e3d26658c043bd08f6812c5f5e78aa246eb3653` |
| 1BJ1 | 809 | `af710f4d53a466ccc0ed75e663a0bb198ddb5107c35100d404de07472317d2e6` | 922131 | `48c431a465d467b1ca3ba092b4e3d875b70c10832a0bc8d866de5a38b7cc3d96` |
| 4HSA | 553 | `6c26fc271ac1e2e5f2ff1ca992a0e160991fd8d058ebecc7afebc1d8fe499768` | 1552585 | `50e785677a3f201712996938cfba25372685408b7c09e53a3a960f12ce7ce806` |
| 1TNF | 229 | `d241260d039a9f0d18af880e97a1a27ff8ad9756aafda0bc2c8cbecdf42788c0` | 383234 | `c86bc5041124d7cdcc0585ded990b489ef603b0f0d2b6dbb45a0f76856594ba5` |
| 7ZBU | 1984 | `6a17204c2fa7fd6db30c1f6048c766f855b4b88c89ed4e450596a960f6f4e611` | 989800 | `1774c9cccd24ea7234013157c11529123b451a863f6b5b6e94d45e2372a63caa` |

原生 polymer entity 角色（entity ID、作者链、字面描述）：

| PDB | entity | author chains | 原生实体描述 |
| --- | --- | --- | --- |
| 2WH6 | 1 | A | EARLY ANTIGEN PROTEIN R |
| 2WH6 | 2 | B | BCL-2-LIKE PROTEIN 11 |
| 6M0J | 1 | A | Angiotensin-converting enzyme 2 |
| 6M0J | 2 | E | Spike protein S1 |
| 3DI3 | 1 | A | Interleukin-7 |
| 3DI3 | 2 | B | Interleukin-7 receptor subunit alpha |
| 5O45 | 1 | A | Programmed cell death 1 ligand 1 |
| 5O45 | 2 | B | PHE-MEA-9KK-SAR-ASP-VAL-MEA-TYR-SAR-TRP-TYR-LEU-CCS-GLY-NH2 |
| 1WWW | 1 | V,W | PROTEIN (NERVE GROWTH FACTOR) |
| 1WWW | 2 | X,Y | PROTEIN (TRKA RECEPTOR) |
| 4ZXB | 1 | A | Fab 83-7 heavy chain |
| 4ZXB | 2 | B | Fab 83-7 light chain |
| 4ZXB | 3 | C | Fab 83-14 heavy chain |
| 4ZXB | 4 | D | Fab 83-14 light chain |
| 4ZXB | 5 | E | Insulin receptor |
| 5VLI | 1 | A | Hemagglutinin |
| 5VLI | 2 | B | Hemagglutinin |
| 5VLI | 3 | C | Computationally designed peptide HB1.6928.2.3 |
| 1BJ1 | 1 | L,J | Fab fragment, light chain |
| 1BJ1 | 2 | H,K | Fab fragment, heavy chain |
| 1BJ1 | 3 | V,W | Vascular endothelial growth factor A |
| 4HSA | 1 | A,B,D,E | Interleukin-17A |
| 4HSA | 2 | C,F | Interleukin-17 receptor A |
| 1TNF | 1 | A,B,C | TUMOR NECROSIS FACTOR-ALPHA |
| 7ZBU | 1 | A | Spike glycoprotein |
| 7ZBU | 2 | H | P008_60 antibody, Heavy chain |
| 7ZBU | 3 | L | P008_60 antibody, Light chain |

## 使用方式

依赖见接入代码 requirements；以下仅从原始文件读取。

```python
from pathlib import Path
from bs4 import BeautifulSoup
# dataset_root 由调用者赋值为该 source version 目录。
soup = BeautifulSoup((Path(dataset_root) / "AlphaProteo/AlphaProteo_2024-09-12_arXiv-v1.html").read_bytes(), "html.parser")
for annotation in soup.select("annotation"):
    annotation.decompose()  # 仅解析副本；保留原始 HTML。
print(soup.find("table", id="Ax3.T7.3").get_text(" ", strip=True))
```

## 采集过程记录

1. 2026-09-18：读取项目/开发者身份、执行清单与一手来源；由配置读取共享存储根，代码和文档只写本人 workspace。
2. 固定上游版本并在对应 `.staging/snapshot-2024-09-12` 下载，使用断点续传、HTTP 长度及可得的官方校验；遇到环境直连失败采用现有 HTTP 路由回退。
3. Figshare 初次访问出现 TLS EOF；审读 S4.1 后发现来源归属错误，不把网络失败解释为不存在 AlphaProteo 数据，也不下载对照后假称本研究原始包。执行清单更正仅准备个人 workspace 补丁。

   PDF 全文提取出现上游图形对象 float 与 XObject 数量警告；45 页 PDF 有效，改用同版 HTML 交叉检查 Methods 与完整表，避免只按不完整提取文本下结论。表解析发现 MathML annotation 重复、续行空值和 S7 非标准 wrapper，采用副本解析并保留原字节。PDB 接口曾 TLS/连接失败，重试后 11 个输入/参考条目全部通过核验。
4. 解析全部实际表/归档，独立核对文件集合、完整格式、哈希与 PDB 两层，保留上游差异。
5. README 工作稿每次写入立即同步共享目录；发布器复核固定格式、同步 hash 和 pinned markdownlint 0 errors 后原子发布。已于 2026-09-18T20:48:41.372749+00:00 从 staging 原子发布，当前为 final；本次修订 README 在同一次写入中覆盖同步 final，并重新审计和 lint。

依据来源、可核验日期、载体和附件角色整理 opaque 名称，改名前后 bytes/SHA-256 相同；中间名保留实际修订历史。HTML 与 v1 提交日期一致，重命名同时更新下载器、审计器和读取示例路径。具体映射如下：

| 上游原名 | 中间名（如有） | 本地相对路径 | 核对 bytes | 核对 SHA-256 |
| --- | --- | --- | --- | --- |
| 2409.08022v1.html | 无 | AlphaProteo/AlphaProteo_2024-09-12_arXiv-v1.html | 690383 | `cc76ffb3e89c08788c5ea1c06d6dcf367c384c73548829e76b54b703a9356d2b` |

2026-09-18 逐条复审后：补齐全部已取得 PDB 的条目和原始结构论文主引用，以及涉及的上游汇编/对照引用。恢复 S7 真实表头，解释语义别名和 Unicode 位置，按来源/日期重命名 HTML 且保留原字节。相应修改同步个人状态、事实台账和交接，未取得的材料继续标明 partial/blocked。

## 参考文献

- [arXiv 固定版本](https://arxiv.org/abs/2409.08022v1)
- [同版 HTML 与 S7](https://arxiv.org/html/2409.08022v1#Ax3.T7)
- [官方 PDB Search API](https://search.rcsb.org/)
- [RFdiffusion 对照数据出处：Bennett et al. (2023), Improving de novo protein binder design with deep learning](https://doi.org/10.1038/s41467-023-38328-5)
- [BINDI 对照原论文：Procko et al. (2014)](https://doi.org/10.1016/j.cell.2014.04.034)
- [LCB1 对照原论文：Cao et al. (2020), De novo design of picomolar SARS-CoV-2 miniprotein inhibitors](https://doi.org/10.1126/science.abd9909)

### PDB 条目与原始结构论文

以下主引用直接读取归档 mmCIF 的 `_citation` 元数据，按同一主引用合并；每个 PDB 链接均指向该原始条目，不把输入结构论文算作本来源的新实验。

| 原始 PDB 条目 | 结构论文主引用（标题、期刊、年份） | DOI / PMID |
| --- | --- | --- |
| [1BJ1](https://www.rcsb.org/structure/1BJ1) | VEGF and the Fab fragment of a humanized neutralizing antibody: crystal structure of the complex at 2.4 A resolution and mutational analysis of the interface.；Structure；1998 | [DOI 10.1016/S0969-2126(98)00116-6](https://doi.org/10.1016/S0969-2126(98)00116-6)；[PMID 9753694](https://pubmed.ncbi.nlm.nih.gov/9753694/) |
| [1TNF](https://www.rcsb.org/structure/1TNF) | The structure of tumor necrosis factor-alpha at 2.6 A resolution. Implications for receptor binding.；J.Biol.Chem.；1989 | [PMID 2551905](https://pubmed.ncbi.nlm.nih.gov/2551905/) |
| [1WWW](https://www.rcsb.org/structure/1WWW) | Crystal structure of nerve growth factor in complex with the ligand-binding domain of the TrkA receptor.；Nature；1999 | [DOI 10.1038/43705](https://doi.org/10.1038/43705)；[PMID 10490030](https://pubmed.ncbi.nlm.nih.gov/10490030/) |
| [2WH6](https://www.rcsb.org/structure/2WH6) | Structural basis for apoptosis inhibition by Epstein-Barr virus BHRF1.；PLoS Pathog.；2010 | [DOI 10.1371/journal.ppat.1001236](https://doi.org/10.1371/journal.ppat.1001236)；[PMID 21203485](https://pubmed.ncbi.nlm.nih.gov/21203485/) |
| [3DI3](https://www.rcsb.org/structure/3DI3) | Structural and Biophysical Studies of the Human IL-7/IL-7Ralpha Complex.；Structure；2009 | [DOI 10.1016/j.str.2008.10.019](https://doi.org/10.1016/j.str.2008.10.019)；[PMID 19141282](https://pubmed.ncbi.nlm.nih.gov/19141282/) |
| [4HSA](https://www.rcsb.org/structure/4HSA) | Crystal structures of interleukin 17A and its complex with IL-17 receptor A.；Nat Commun；2013 | [DOI 10.1038/ncomms2880](https://doi.org/10.1038/ncomms2880)；[PMID 23695682](https://pubmed.ncbi.nlm.nih.gov/23695682/) |
| [4ZXB](https://www.rcsb.org/structure/4ZXB) | Higher-Resolution Structure of the Human Insulin Receptor Ectodomain: Multi-Modal Inclusion of the Insert Domain.；Structure；2016 | [DOI 10.1016/j.str.2015.12.014](https://doi.org/10.1016/j.str.2015.12.014)；[PMID 26853939](https://pubmed.ncbi.nlm.nih.gov/26853939/) |
| [5O45](https://www.rcsb.org/structure/5O45) | Bioactive Macrocyclic Inhibitors of the PD-1/PD-L1 Immune Checkpoint.；Angew. Chem. Int. Ed. Engl.；2017 | [DOI 10.1002/anie.201707707](https://doi.org/10.1002/anie.201707707)；[PMID 28881104](https://pubmed.ncbi.nlm.nih.gov/28881104/) |
| [5VLI](https://www.rcsb.org/structure/5VLI) | Massively parallel de novo protein design for targeted therapeutics.；Nature；2017 | [DOI 10.1038/nature23912](https://doi.org/10.1038/nature23912)；[PMID 28953867](https://pubmed.ncbi.nlm.nih.gov/28953867/) |
| [6M0J](https://www.rcsb.org/structure/6M0J) | Structure of the SARS-CoV-2 spike receptor-binding domain bound to the ACE2 receptor.；Nature；2020 | [DOI 10.1038/s41586-020-2180-5](https://doi.org/10.1038/s41586-020-2180-5)；[PMID 32225176](https://pubmed.ncbi.nlm.nih.gov/32225176/) |
| [7ZBU](https://www.rcsb.org/structure/7ZBU) | A neutralizing epitope on the SD1 domain of SARS-CoV-2 spike targeted following infection and vaccination.；Cell Rep；2022 | [DOI 10.1016/j.celrep.2022.111276](https://doi.org/10.1016/j.celrep.2022.111276)；[PMID 35981534](https://pubmed.ncbi.nlm.nih.gov/35981534/) |

## 其他

### 数据范围和限制

公开论文内嵌表包已获得；完整研究获得未完成。25 条设计不是 861 个测试候选全库，未公开负例序列和完整逐候选结果，实验复合物 accession 仍无法验证。

### 完整性与验收

payload 共 1 文件、690,383 bytes；同样排序 inventory SHA-256 为 `2f07160576d506ceed8fa96e4aa66ac454803f89f580a2881c68edcdc81e3487`。独立审计要求 config 中目标文件集合与实际完全一致（允许 source README，保留上游自己的 README），拒绝 symlink、旁路 JSON/API/manifest、partial 文件或缺少任何可公开 PDB 层。PDF 页数/签名、XLSX 全部 worksheet、ZIP 全部 CRC 与安全成员均按文件类型核验；研究审计结果只保存本人 context，不发布为 raw sidecar。

上游 payload 文件身份；SHA-256 为获取后固定的本地值：

| payload 文件 | bytes | SHA-256 |
| --- | --- | --- |
| AlphaProteo_2024-09-12_arXiv-v1.html | 690383 | `cc76ffb3e89c08788c5ea1c06d6dcf367c384c73548829e76b54b703a9356d2b` |

### 许可和再分发边界

本版 arXiv 声明 CC BY-NC-SA 4.0；不把 RFdiffusion Figshare 或外部对照文章许可移植到 AlphaProteo。未公开 raw 需依作者数据可用性说明联系申请，本次未发送邮件或提交申请。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 861 个被测试候选 | 主 Table 1 聚合计数，非完整序列库 | 仅数量汇总 |
| 公开序列与亲和力 | S7：25 GDM 设计 + 7 对照；28 字面序列 | 已包含公开选定记录 |
| BLI/功能和结构验证 | 补充图、S4 EC50、S5/S6 采集统计 | 仅公开汇总/图；非统一原始仪器包 |
| 输入 PDB | 10 个 S1 输入加 7ZBU，共 11 对完整原生文件 | 已包含参考；非新 GDM 复合物 |
| Figshare 共享链接 | S4.1 指向 RFdiffusion 对照下载 | 拒绝误归属 |
| 完整候选/负例序列、实验结构 accession | 本文未提供可核验完整文件或 accession | 未获得完整研究范围 |
