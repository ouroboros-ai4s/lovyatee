# SRC_R32_VREVEN_AFFINITY 数据说明

## 数据集身份

- `source_id`：`SRC_R32_VREVEN_AFFINITY`
- `source_version`：`2.0`
- 原作者或发布机构：Vreven 等蛋白相互作用 benchmark 合作团队（University of Massachusetts Medical School、Francis Crick Institute、Barcelona Supercomputing Center、Utrecht University）

### 来源方背景

该来源由四个机构的计算结构生物学团队共同整理。论文作者单位包括 University of Massachusetts Medical School 的 Bioinformatics and Integrative Biology Program、Francis Crick Institute 的 Biomolecular Modelling Laboratory、Barcelona Supercomputing Center 的计算生物学联合项目，以及 Utrecht University 的 Bijvoet Center。当前 [Weng Lab benchmark 页面](https://zlab.wenglab.org/benchmark/) 继续维护 docking benchmark，并列出本研究及其后续 BM5.5 资源；2015 版本的责任主体和作者单位可由[论文 PubMed 记录](https://pubmed.ncbi.nlm.nih.gov/26231283/)核对。R32 固定的是论文对应的 docking v5 / affinity v2 历史交付，当前页面上的后续版本只用于确认维护沿革。

## 实验设计和数据口径

该来源没有对 179 个复合物重新执行一种统一的亲和力实验，而是把已有结构和已发表测量汇编为两个相互关联的 benchmark。作者先从 PDB 寻找同时具有结合态复合物和两个游离组分结构的候选，抗体–抗原候选还使用 SACS 补充；再按结构方法、分辨率、序列一致性、覆盖率、链长和非冗余规则筛选，并人工检查界面缺失、突变、辅因子和 biological assembly。`benchmark5.tgz` 是据此整理的 bound/unbound docking components，`Table_BM5.xlsx` 是 230 个 docking 案例的汇总表。

在 docking 案例中，作者继续检索已发表的实验亲和力。一个复合物存在多个报道值时，优先选择实验样品序列与结构 construct 相符的测量；仍有多个候选时再比较序列相似性和测量方法。公开的 `Kd (M)` 因而是每个结构案例选定的一条文献测量，不是本研究对全部案例统一复测的 replicate。SPR（表面等离子体共振）、ITC（等温滴定量热）、光谱法、BLI（生物层干涉）、热泳和 ELISA 等方法的温度、pH、缓冲液及构建体不同，跨案例比较必须保留这些条件。

两个 benchmark 的版本关系是：

```text
Docking v4：175 个案例 ──新增 55 个──> Docking v5：230 个案例
                                      └─其中 35 个找到实验亲和力──┐
Affinity v1：144 个案例 ────────────────────────────────────────┴─> Affinity v2：179 个案例
```

因此 35 条 v2 additions 是 55 个新 docking 案例中有可用亲和力的子集；它们与 affinity v1 的 144 条无重复，合并后构成 179 条 affinity v2。论文报告其中 33 个为抗体–抗原案例。`Table_BM5.xlsx` 的 230 行与 affinity 的 179 行不是两个独立实验队列，也不能相加为样本总数。

`Kd` 以 M 表示，越低结合越强；其中 3 条以 `<` 保存上界，表示真实 Kd 小于所列阈值。`dG` 不是另一项实验测量，而是作者按 `ΔG = RT ln(Kd)` 计算的 kcal/mol 派生值，温度未知时取 298.15 K；使用 `Kd` 预测时不能再把 `dG` 当作独立输入。`I-RMSD` 和 `DASA` 来自结合态/游离态结构比较，补充材料中的 affinity predictor 分数则是模型输出。这些结构派生量和预测分数分别适合结构分析与方法评估，不应改称实验亲和力。

## 论文原文

- 标题：Updates to the integrated protein-protein interaction benchmarks: Docking benchmark version 5 and affinity benchmark version 2
- 作者：Thom Vreven；Iain H. Moal；Anna Vangone；Brian G. Pierce；Panagiotis L. Kastritis；Mieczyslaw Torchala；Raphael Chaleil；Brian Jimenez-Garcia；Paul A. Bates；Juan Fernandez-Recio；Alexandre M.J.J. Bonvin；Zhiping Weng
- 发表来源：Journal of Molecular Biology，427(19)，3031–3041
- 归档文本版本：NCBI BioC 公共存档的作者稿全文 XML（NIHMS730749）
- 发布日期：2015-07-29
- DOI：[10.1016/j.jmb.2015.07.016](https://doi.org/10.1016/j.jmb.2015.07.016)
- PMID / PMCID：26231283 / PMC4677049
- 本地文件：`articles/VrevenAffinity_2015-07-29_NCBI-BioC-author-manuscript.xml`
- 文件大小：176.20 KiB（180,424 bytes）
- SHA-256：`991c4a5c75b3b1e0e1c4f33e032b6d9456f04eabaf13ac333939d94009854780`
- 文本许可：NCBI 仅标明可供文本挖掘及符合美国版权法 fair use 的使用，未标为 CC BY
- 补充材料：`protein_affinity_benchmark2/VrevenAffinity_2015-07-29_Elsevier-SupplementaryData.pdf`（6 页；152.99 KiB（156,657 bytes）；SHA-256 `1a99e13910c1ade4f851b73937844e55de668f7e14c6b3f902480ed8a1ee536c`），含 35 个新增案例、affinity predictor 评估和抗体 CDR 位点表
- 引用数（查询快照）：486（[OpenAlex](https://openalex.org/W1030883578)，查询于 2026-09-24）

本地归档的是同 DOI 论文的作者稿结构化全文，并非出版方排版 PDF；书目信息按正式期刊版本记录。方法、表格脚注和新增案例可由该作者稿与出版方补充材料共同核对。

## 仓库内容

一手结构入口现为 zlab.wenglab.org/benchmark；虽然首页展示最新 BM5.5，直接旧交付 Table_BM5.xlsx / benchmark5.tgz 仍可取得，HTTP 对象日期 2015-08-11。source_version=2.0 取目标 affinity benchmark 的正式版本，不把当前 BM5.5 抗体扩展或 R16 误作 R32 全量亲和力包。出版方 CDN 的 PII S0022283615004180 supplement 与主文补充 caption 相互对应。

```text
2.0/
├── protein_docking_benchmark5/
│   ├── Table_BM5.xlsx
│   └── benchmark5.tgz
└── protein_affinity_benchmark2/
    ├── VrevenAffinity_2015-07-29_Elsevier-SupplementaryData.pdf
    ├── affinity_benchmark1.tsv
    └── affinity_benchmark2_additions.tsv
```

两份 TSV 是 bmm.crick.ac.uk 原作者历史页面所列 CGI 响应的互联网档案原始捕获：v1 为 144 行，v2 响应为 35 行新增案例。文件原始 Content-Disposition 都叫 `affinity.tsv`，落盘时用范围明确的不同文件名避免碰撞，字节不变。

## 数据结构

### 结构表与亲和力表

Table_BM5.xlsx 只有 Sheet1，前两行是标题/空行，第三行才是九字段列头；后有 230 个真实案例及三个 category 分隔行。以 Complex 的 PDB/chain 编码识别案例，不把分隔行计为 233 个复合物。benchmark5.tgz 保存作者的 bound/unbound components，已逐成员读取检查，不能替代 PDB 完整 entity 的外部 canonical 验收。

坐标包的 920 个 PDB component 均读到原子，共 1,913,996 个原子记录。其中 34 个文件的尾部 charge 字段不是 Gemmi 可识别的标准格式；严格读取先记录失败，再仅针对该错误使用 max_line_length=78 读取坐标及 element 字段，保留全部原始字节。该兼容读取不验证列 79–80 的电荷含义，不把 component 当成完整 RCSB 条目。

三个分隔行分别是 `Rigid-body (151)`、`Medium Difficulty (45)` 和 `Difficult (34)`，括号数合计 230。作者以 I-RMSD 和非天然接触比例定义 docking 难度；这些行是工作表内的分组标题，不含九个字段的案例数据。

两份 affinity TSV 都是 Latin-1、两行表头、22 列。第一行是表名和 Extra Data 的单位注释，第二行才是字段名；两个 `Unbound PDB` 列名在 raw 中完全相同，必须按列位置区分。v1 有 144 行，v2 additions 有 35 行，179 个 `Complex PDB` 键均唯一。全部行有 `Kd (M)`，但其中 3 条是带 `<` 的删失字符串；v1 的名义 Kd 范围为 2.4e-14–6.35e-4 M，v2 新增表为 1.84e-11–2.21e-5 M。原始方法名、温度、pH、buffer、cofactor、评论和文献定位原样保留，缺失条件不补值。

出版方补充 PDF 有六页：Supporting Table 1 重列 35 个新 affinity 案例，Supporting Table 2 为计算 affinity 分数，Supporting Table 3 为 PARATOME 计算的抗体 CDR 位点（用于 HADDOCK docking restraints），末尾是原始实验引用。它为新增表提供独立交叉核对，不替代 144 行旧表。

### 字段说明

| 文件 / 原始字段 | 表示、单位与来源 | 缺失、方向与使用边界 |
| --- | --- | --- |
| BM5：`Complex` | 结合态复合物 PDB ID 加 author-chain 分组的字符串键 | 230 个值唯一；冒号两侧表示两个相互作用组分，不是 FASTA entity 顺序 |
| BM5：`Cat.` | 生物学类别代码；本版实际观察值见下表 | 分类注释，不是结合标签；`A` 与 `AB` 需按版本差异解释 |
| BM5：`PDB ID 1`、`Protein 1`、`PDB ID 2`、`Protein 2` | 两个游离组分的 PDB/author-chain 锚点及人工名称 | 括号内数字是所选 NMR model；组分可被多个案例复用 |
| BM5：`I-RMSD (Å)` | 游离组分叠合到结合态后界面 Cα 的 RMSD；界面残基按结合态中距另一组分任一原子 10 Å 内确定 | 单位 Å；较低表示构象变化较小；不代表亲和力 |
| BM5：`ΔASA(Å2)` | NACCESS 计算的复合形成前后溶剂可及表面积变化；Å² | 界面面积，不代表实验 Kd |
| BM5：`BM version introduced` | 案例首次进入 docking benchmark 的版本；实际为 2、3、4、5 | 版本号，不是测量年份或实验轮次 |
| Affinity：`Complex PDB` | 结合态复合物 PDB ID 加 author-chain 分组键 | 179 个值唯一；v1 与 v2 additions 之间无重复 |
| Affinity：`Type` | 生物学类别代码；本版实际观察值见下表 | 分类注释；`E` 与补充表存在一处来源差异 |
| Affinity：第 1 个 `Unbound PDB`、`Protein A` | 组分 A 的游离结构锚点和名称 | 原表有两个同名 `Unbound PDB`；按列位置区分 |
| Affinity：第 2 个 `Unbound PDB`、`Protein B` | 组分 B 的游离结构锚点和名称 | pandas 默认把第二个同名列显示为 `Unbound PDB.1`，raw 表头未改名 |
| Affinity：`Pubmed` | 所选亲和力测量的 PMID 字符串 | 6 行为空；同一 PMID 可支持多个案例 |
| Affinity：`Kd (M)` | 文献中选定的平衡解离常数；M | 179 行均有值；越低结合越强；3 行以 `<` 表示上界删失，不能直接当作精确浮点数 |
| Affinity：`dG` | 按 `ΔG = RT ln(Kd)` 计算的结合自由能；kcal/mol | 由 Kd 派生而非独立测量；温度未知时论文设 T=298.15 K；更负表示更强 |
| Affinity：`I-RMSD`、`DASA`（raw 列名末尾有一个 ASCII 空格） | 与 BM5 同源的界面 RMSD（Å）和面积变化（Å²） | 结构派生；读取时须保留或显式处理列名末尾空格 |
| Affinity：`Method` | 文献亲和力的实验方法原始字符串；本版全部观察值见下表 | 2 行为空；拼写和大小写变体保留，不能仅按字符串当作同一标准化 assay |
| Affinity：`Final Comments` | 结构与测量匹配、突变、离子依赖等人工备注 | 135 行为空；备注可改变该案例的适用边界 |
| Affinity：`Temperature (C)`、`pH` | 文献实验条件；温度单位为 °C，pH 无量纲 | 分别有 10 / 3 个空值；另含 `not stated`、`room temperature`、`ambient` 等原始文本 |
| Affinity：`Buffer/Ionic Strength` | 缓冲液、盐和离子强度的原始自由文本 | 5 行为空；未标准化为统一配方 |
| Affinity：`Cofactors (bound)`、`Cofactors (unbound)`、`Cofactors (binding)` | 结合态结构、游离结构与亲和力实验中的辅因子自由文本 | 分别有 153 / 155 / 155 个空值；三列角色不能互换 |
| Affinity：`Extra Data` | 补充热力学/动力学自由文本；表头注释给出 kon、koff、dH、dS、dCp 的单位约定 | 80 行为空；一个单元格可混合多个量和单位，不能直接作为单一数值列 |
| Affinity：`Corroborating Data` | 其他文献测量及比较说明的自由文本 | 105 行为空；不是被选为主标签的第二套统一测量 |
| Affinity：`Exact finding in:`（raw 列名末尾有一个 ASCII 空格） | 所选数值在原论文中的表、图、页或正文位置 | 179 行均填写；读取时须保留或显式处理列名末尾空格 |

**`Cat.` / `Type`（BM5 与两份 affinity TSV；取值范围依据：当前 2.0 文件扫描）**

| 原始取值 | BM5 `Cat.` 记录数 | Affinity `Type` 记录数 | 含义与证据边界 |
| --- | --- | --- | --- |
| `A` | 28 | 26 | 论文脚注明确定义为 antibody–antigen；本版新增案例使用该代码 |
| `AB` | 12 | 7 | 旧案例中的抗体–抗原代码；论文脚注未单列，但对象名称及 A+AB 与论文 40/33 个抗体案例总数一致 |
| `E` | 0 | 1 | 仅 affinity additions 的 3LVK_AC:B 使用；补充表将同一案例列为 ER，保留原 TSV 差异 |
| `EI` | 45 | 44 | enzyme–inhibitor |
| `ES` | 17 | 10 | enzyme–substrate |
| `ER` | 26 | 14 | enzyme complex with a regulatory or accessory chain |
| `OG` | 23 | 17 | other, G-protein containing |
| `OR` | 24 | 18 | other, receptor containing |
| `OX` | 55 | 42 | other, miscellaneous |

论文脚注只定义 `A`、`EI`、`ES`、`ER`、`OG`、`OR`、`OX`。当前文件还保留旧代码 `AB`，且 additions TSV 的 3LVK_AC:B 写作 `E`，而同论文 Supporting Table 1 写作 `ER`；raw 层不替换这些值。

**`BM version introduced`（Table_BM5.xlsx；取值范围依据：当前 BM5 文件扫描）**

| `BM version introduced` | BM5 记录数 |
| --- | --- |
| `2` | 84 |
| `5` | 55 |
| `4` | 52 |
| `3` | 39 |

**`Method`（两份 affinity TSV；取值范围依据：当前 2.0 文件扫描）**

| `Method` 原始取值 | 记录数 | 方法族及解释边界 |
| --- | --- | --- |
| `SPR` | 60 | 表面等离子体共振 |
| `ITC` | 32 | 等温滴定量热法 |
| `Inhibition assay` | 18 | 抑制实验；不同原始拼写不合并 |
| `Fluorescence inhibition assay` | 9 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `Spectroscopic inhibition assay` | 7 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `Spectrophotometric inhibition assay` | 6 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `Stopped-flow fluorescence` | 5 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `Fluorescence` | 4 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `Fluorescence titration` | 3 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `<empty>` | 2 | 原表空值；测量方法未记录 |
| `BLI` | 2 | 生物层干涉法 |
| `Fluorescence anisotropy` | 2 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `Fluorescence spectroscopy` | 2 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `Stopped-flow fluometry` | 2 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `Stopped-flow fluormetry` | 2 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `Thermophoresis` | 2 | 热泳法 |
| `Competitive Inhibition assay` | 1 | 抑制实验；不同原始拼写不合并 |
| `ELISA` | 1 | ELISA 或 ELISA 抑制法；保留原拼写 |
| `ELISA inhibiton assay` | 1 | ELISA 或 ELISA 抑制法；保留原拼写 |
| `Electrophoretic mobility shift assays` | 1 | 电泳迁移率变动实验 |
| `Flourescence` | 1 | 来源保留的实验方法标签 |
| `Fluorescence Spectroscopy` | 1 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `Fluorescence Titration` | 1 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `Fluorescence spectrophotometry` | 1 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `Fluorescence; stopped-flow` | 1 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `Inhibition assay (indirect-Upa Hydrolysis)` | 1 | 抑制实验；不同原始拼写不合并 |
| `Inhibitor assay` | 1 | 抑制实验；不同原始拼写不合并 |
| `Potentiometric` | 1 | 电位法 |
| `Radioligand binding` | 1 | 放射性配体结合或抑制实验 |
| `Radioligand inhibition assay` | 1 | 放射性配体结合或抑制实验 |
| `Reflectometric interference spectroscopy` | 1 | 反射干涉光谱法 |
| `Sedimentation equilibrium` | 1 | 沉降平衡法 |
| `Spectrophotometry` | 1 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `Spectroscopic assay` | 1 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `Spectroscopic inbition assay` | 1 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `Spectroscopy` | 1 | 荧光/光谱或其抑制、动力学变体；不同原始拼写不合并 |
| `Stopped-flow inhibition` | 1 | 抑制实验；不同原始拼写不合并 |

方法表按原始大小写和拼写逐项列出，因此 `Fluorescence Spectroscopy` 与 `Fluorescence spectroscopy` 等仍是不同字符串；方法族说明只帮助阅读，不在 raw 层合并类别。

### 数据示例

BM5 真正案例：Complex=1AHW_AB:C，Cat.=A，PDB ID 1=1FGN_LH，Protein 1=Fab 5g9，PDB ID 2=1TFH_A，Protein 2=Tissue factor，I-RMSD=0.69 Å，ΔASA=1899 Å²，BM version introduced=2。它在该表中没有 KD 字段。

Affinity v1 的真实首行：1A2K_C:AB，Type=OG，Kd=1.5e−7 M、dG=−9.31 kcal/mol、Temperature=25 °C、pH=7.5、Method=ITC、Pubmed=10681579。删失示例 1IQD_AB:C 的原始 Kd 是 `<1.4e-11` M，不能去掉 `<` 后当作精确值。v2 additions 的真实首行：1JTD_B:A，Type=EI，Kd=2.72e−11 M、dG=−14.41 kcal/mol、Temperature=25 °C、pH=7、Method=Inhibition assay、Pubmed=11573088。每行代表一个经人工选择测量值的结构复合物案例。

## PDB 数据库

逐项审计 `Table_BM5.xlsx` 与两份 affinity TSV 的 `Complex PDB`、两个 `Unbound PDB` 字段。并集产生 672 个唯一外部 ID，覆盖 230 个 BM5 docking 案例和 179 个 affinity 案例的结合态/游离态支持结构。原始 `AB:C` 等 author-chain 编码仍留在上游表中；坐标包是作者整理后的 docking components，外部完整 PDB 条目另行保存。

获取日期为 2026-09-18。一手入口为 RCSB 的 `https://www.rcsb.org/fasta/entry/<PDB_ID>/download` 与 `https://files.rcsb.org/download/<PDB_ID>.cif.gz`。复用共享缓存时保留其原始 `.cif` 或 `.cif.gz` 字节；缓存未通过身份检查时重新获取。保存完整条目的全部 polymer entities 和完整坐标，不筛链、不拼接变体序列。验证 entry ID、FASTA entity ID、canonical 序列与 mmCIF `_entity_poly.pdbx_seq_one_letter_code_can` 一致，并确认存在原子坐标。

接受 672 个唯一 ID，672 对通过配对检查，1,344 个已验收文件，共 200.23 MiB（209,958,907 bytes）。按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接的 inventory SHA-256：`92a70c8b018099c150639b20bd0c8a453979603b839d47ac4b1fc0523198cce6`。PDB 子任务状态为 `verified`。

撤销条目 `1A2K`, `1ERK`, `2DTQ`, `3RVW` 使用撤销前的 RCSB 官方 `pdb_seqres` 快照 FASTA 与 wwPDB obsolete mmCIF。保存批量对象身份及逐条原始记录哈希，并要求完整 author-chain 集合和 canonical 序列逐项相等；未用 successor 覆盖原始键，也未从 mmCIF 生成 FASTA。

外部条目中的链角色以 entity 描述和 `_entity_poly.pdbx_strand_id` 核对；这里保存全部链。上游表给出的角色链与具体实验序列仍须逐构建体验证，不能用相同 PDB ID 自动推定所有抗体序列或抗原构建体相同。

## 使用方式

```python
import pandas as pd

support = pd.read_excel(dataset_root / "protein_docking_benchmark5/Table_BM5.xlsx", header=2)
cases = support[support["Complex"].str.match(r"^[1-9][A-Za-z0-9]{3}_", na=False)]
old = pd.read_csv(dataset_root / "protein_affinity_benchmark2/affinity_benchmark1.tsv", sep=chr(9), header=1, encoding="latin-1")
new = pd.read_csv(dataset_root / "protein_affinity_benchmark2/affinity_benchmark2_additions.tsv", sep=chr(9), header=1, encoding="latin-1")
affinity = pd.concat([old, new], ignore_index=True)
```

dataset_root 由调用者指定；两表保留各自表头，拼接前不要把 v2 additions 误当成完整 2.0 表。

## 采集过程记录

1. 2026-09-18，核对 PMC/BioC 主文 DOI 与版本，对照 179 affinity 和 230 docking 的区别。历史 affinity 主机当前不可达，先保存诊断，没有关闭 TLS 验证或把第三方扩展称为原始包。
2. 恢复迁移后官方站点的旧 Table_BM5.xlsx、benchmark5.tgz，记录 2015-08-11 对象日期、大小和 ETag，下载到 staging，逐成员与表格独立检查。读取 XLSX 的 extension warning 未改写 raw 文件。
3. PMC/Europe PMC 主文及 supplement PDF 路径返回拒绝访问。NCBI BioC 的同 DOI author-manuscript 全文可获取，核对 PMID/DOI 后归档；仍未取得出版 PDF。随后用主文对应 PII 找到出版方 CDN 的原始 mmc1.pdf，取得 156,657 bytes 六页补充，Supporting Table 1 与主文 35 新案例吻合。
4. 将原始 1-s2.0-S0022283615004180-mmc1.pdf 按 2015-07-29 电子发表日期改名为 VrevenAffinity_2015-07-29_Elsevier-SupplementaryData.pdf，重命名前后 hash 保持一致。未将 PDF 内容重写成新的 raw CSV。
5. 对坐标包逐成员读取并解析全部 920 个 PDB；34 个原始文件尾部 charge 格式触发严格 reader 失败，记录具体位置后，以只读到第 78 列的兼容 reader 验证原子坐标，未改写 raw。
6. 2026-09-19，从互联网档案恢复原 affinity 页面及两个官方 CGI 原始响应。逐字节固定 v1 144 行和 v2 additions 35 行，核对字段宽度、179 个唯一 Complex PDB 键、全部 Kd 与论文的总数；不从 PDF OCR 重建表格。
7. 审计 BM5 与完整 affinity 表内三类结构键，得到 672 个唯一外部 ID。668 个现行条目使用 RCSB FASTA/mmCIF；1A2K、1ERK、2DTQ、3RVW 使用撤销前的 RCSB 官方 `pdb_seqres` 快照记录与 wwPDB obsolete mmCIF，完整 author-chain 集合和 canonical 序列逐项相等。没有用 successor 替换原始键，也没有从坐标生成 FASTA。
8. 重新执行 payload、论文、PDB inventory 与 README 验收，工作稿立即同步 staging README，并执行固定 Markdownlint；全部声明目标通过后原子发布 2.0。
9. 2026-09-24，按最新 README 合同复核全部九个 BM5 字段和 22 个 affinity 字段，逐项统计类别、方法、缺失值及重复键。确认 3 条 Kd 为 `<` 删失值、其余 176 条 dG 与论文公式一致；同时记录 `E` / `ER` 的上游表间差异。重新核验 672 对 PDB，四个 obsolete 条目仍使用原始历史配对，没有受到早期 PDB 拉取脚本问题影响；同步更新迁移后的正式路径、README hash 和发布验收总字节。

## 参考文献

- [2015 主文公共存档](https://pmc.ncbi.nlm.nih.gov/articles/PMC4677049/)
- [PubMed 论文记录与作者单位](https://pubmed.ncbi.nlm.nih.gov/26231283/)
- [官方结构基准入口](https://zlab.wenglab.org/benchmark/)
- [当前结构基准页所链接的 CC BY 4.0 文本](https://zlab.wenglab.org/benchmark/LICENSE)
- [出版方补充 PDF](https://ars.els-cdn.com/content/image/1-s2.0-S0022283615004180-mmc1.pdf)
- [原 affinity v2 页面历史快照](https://web.archive.org/web/20160222210338id_/http://bmm.crick.ac.uk/~bmmadmin/Affinity/affinity2.html)
- [官方 affinity v1 TSV 历史响应](https://web.archive.org/web/20160222210442id_/http://bmm.crick.ac.uk/~bmmadmin/Affinity/getcsv.cgi)
- [官方 affinity v2 additions TSV 历史响应](https://web.archive.org/web/20160222210442id_/http://bmm.crick.ac.uk/~bmmadmin/Affinity/getcsv2.cgi)
- [NCBI author-manuscript BioC 全文](https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC4677049/ascii)
- [RCSB 官方历史快照说明](https://www.wwpdb.org/ftp/pdb-ftp-sites)
- [3RVW 的 RCSB obsolete 记录](https://www.rcsb.org/structure/removed/3RVW)

## 其他

### 数据范围和限制

状态为 verified public-package onboarding。完整保存 affinity v1 的 144 行与 v2 新增的 35 行，合计 179 个亲和力案例；另保存 BM5 的 230 个 docking 案例及作者整理坐标。该状态覆盖论文所述公开 benchmark 交付、解释论文和外部 PDB 配对，不覆盖 179 篇原始测量文献的仪器曲线、逐次拟合或全部候选测量。

### 完整性与验收

| payload | 大小 | SHA-256 |
| --- | --- | --- |
| `protein_docking_benchmark5/Table_BM5.xlsx` | 46.31 KiB（47,426 bytes） | `5397368d44dd36c71079274cf4521b29c410bc8473aef884e68262484211f151` |
| `protein_docking_benchmark5/benchmark5.tgz` | 37.07 MiB（38,867,186 bytes） | `2288678ea1595207aab8893b0aa19ecc74ea534a065803ea7ee5623d574cc591` |
| `protein_affinity_benchmark2/VrevenAffinity_2015-07-29_Elsevier-SupplementaryData.pdf` | 152.99 KiB（156,657 bytes） | `1a99e13910c1ade4f851b73937844e55de668f7e14c6b3f902480ed8a1ee536c` |
| `protein_affinity_benchmark2/affinity_benchmark1.tsv` | 45.06 KiB（46,142 bytes） | `3c1b2cbfb6fc8c2f0f19873b739509865bfb34f8ec3d4f5c47ed09cde8f87602` |
| `protein_affinity_benchmark2/affinity_benchmark2_additions.tsv` | 10.21 KiB（10,457 bytes） | `be91f833b33dfef4fc2956b6ab5991fe0dd24d5a493d3e3ccf3758a8ed7a83c0` |

已取得 payload 共 5 个、37.32 MiB（39,127,868 bytes）；排序拼接的 inventory SHA-256：`c3789684971f0920d5e4209baf8e1dbc3851fb68e74d4f29dc4e4a8c5fca8112`。上游未给出 checksum 的交付只将 SHA-256 作为本次字节身份，不能称为官方校验和。归档按成员检查重复/逃逸路径、链接和膨胀范围，逐个读取正规成员；ZIP 校验 CRC，gzip 校验尾部。表格按原始 encoding、header 和列宽检查，保留所有原值。

### 许可和再分发边界

当前 Weng Lab benchmark 页面写有 “This work is licensed under a Creative Commons Attribution 4.0 International License” 并链接 CC BY 4.0 全文，但该滚动页面现在展示 BM5.5，没有明确说明这项许可是否追溯覆盖仍可直接下载的 BM5.0 历史对象。历史 affinity 页面和两份 CGI TSV 也未找到覆盖数据的独立许可。因此上游未特别说明覆盖整套 R32 payload 的统一数据许可，使用与再分发范围仍不明确；公开入口允许本项目完成当前接入，但不能据此宣称已获商用或任意再分发授权。NCBI 作者稿只标明文本挖掘/fair use，出版方补充材料不自动继承数据页面许可。PDB 原始记录依 wwPDB/RCSB 数据政策，与作者加工的 BM5 component 坐标分开。

### 公开范围对照

| 论文或来源声称的内容 | 实际公开文件证据 | 状态 |
| --- | --- | --- |
| Docking benchmark v5 的 230 个案例 | Table_BM5.xlsx 230 个案例；benchmark5.tgz 920 个 component | 完整取得 |
| Affinity benchmark v2 的 179 个案例 / 33 个抗体案例 | v1 144 行 + v2 additions 35 行；A+AB 共 33 行 | 完整取得 |
| 55 个新增 docking 案例中的 35 个 affinity 子集 | additions TSV 35 行，并与 Supporting Table 1 交叉核对 | 已包含；不是独立于 230 的第三套队列 |
| 实验 Kd 及其条件 | 179 个 Kd，含 3 个 `<` 删失值；条件和来源定位按行保留 | 公开汇总值；非底层曲线 |
| 预测 affinity 分数 | Supporting Table 2 | 计算值；非新增实验 |
| 672 个原始外部结构锚点 | 672 对 FASTA/mmCIF；4 个为官方历史配对 | PDB verified |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-24；不阻塞本次接入发布）：整套历史 payload 的数据许可范围仍不明确。已核对当前 Weng Lab 页面及其 CC BY 4.0 链接、历史 affinity 页面、CGI 响应、论文 Data Availability 和本地文件，尚未找到明确同时覆盖 BM5.0、affinity v1/v2 TSV 与作者加工坐标的统一条款；当前保留来源、版本和分层许可说明。商用、衍生和对外再分发前仍需向维护方确认；取得能明确覆盖各对象及版本的许可声明后关闭。
- `Q02`（最近更新：2026-09-24；不阻塞本次接入发布）：出版方排版主文 PDF 尚未本地归档。已固定同 DOI、PMID/PMCID 的 NCBI 作者稿全文 XML，并取得出版方六页补充 PDF，现有证据足以复核方法和表格；Publisher PDF 的缺失只影响版式级逐页复核。后续若出现可合法公开下载且 DOI/页码可验证的稳定入口，再核对字节与哈希后归档；若出版方确认仅可在线受限访问，则以当前作者稿归档作为关闭依据。
- `Q03`（最近更新：2026-09-24；不阻塞本次接入发布，但影响类别标准化）：论文脚注未定义 raw 中的 `AB` 和 `E`。`A + AB` 与论文公布的 docking/affinity 抗体案例总数完全一致，支持把 `AB` 视为旧抗体代码；唯一的 `E` 行 3LVK_AC:B 在 Supporting Table 1 中写作 `ER`，显示 TSV 与补充表存在来源差异。raw 值保持不变，processed 层在未取得作者说明前不得静默把 `E` 改为 `ER`；获得维护方数据字典或更正说明后关闭。
