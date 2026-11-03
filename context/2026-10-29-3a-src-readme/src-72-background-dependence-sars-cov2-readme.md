---
- tags:
  - context
---

# SRC_R72_BACKGROUND_DEPENDENCE_SARS_COV2 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [三个变异文库和表型类型](#三个变异文库和表型类型)
  - [表型表的分组和粒度](#表型表的分组和粒度)
  - [处理目录中的中间表](#处理目录中的中间表)
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

- `source_id`：`SRC_R72_BACKGROUND_DEPENDENCE_SARS_COV2`
- `source_version`：`snapshot-2026-02-13`
- 原作者或发布机构：哈佛大学组织与进化生物学系 Desai 实验室（Alief Moulana、Thomas Dupic、Michael M. Desai）

### 来源方背景

本 source 的研究与数据由 Michael M. Desai 在哈佛大学组织与进化生物学系（Department of Organismic and Evolutionary Biology, Harvard University）领导的实验室完成，论文署名作者为 Alief Moulana、Thomas Dupic 与 Michael M. Desai；Thomas Dupic 同时隶属 Aix-Marseille 大学马赛免疫学中心（Centre d'Immunologie de Marseille-Luminy）。作者贡献声明记录：概念化由 A. M. 与 M. M. D. 完成，文库设计与构建由 A. M. 完成，实验由 A. M. 与 T. D. 完成，数据分析由 A. M. 完成，M. M. D. 负责指导与经费。以上取自论文本身的署名与贡献声明。

该实验室围绕实验演化、适应度景观与深度突变扫描方法开展工作，与本次数据直接相关的前作包括 *Compensatory epistasis maintains ACE2 affinity in SARS-CoV-2 Omicron BA.1*（Nature Communications，2022）与 *The landscape of antibody binding affinity in SARS-CoV-2 Omicron BA.1 evolution*（eLife，2023）。本数据源是该系列在多个 Omicron 遗传背景上的延续，其 Library B 的测量流程沿用前两篇建立的 Tite-Seq 与酵母展示体系。

`https://github.com/desai-lab` 是发布本次数据的 GitHub 组织；正文核验时组织页可达。核验过程中尝试的机构与团队主页入口及结果记在调研记录：哈佛 OEB 人员页与 `projects.iq.harvard.edu` 返回 HTTP 403（WAF 拦截），`desai.harvard.edu` 与 `mdesai.oeb.harvard.edu` 无法建立连接，`desailab.org` 可达但属于另一个同名实验室（研究补体系统），与本来源无关。因此本节只写论文署名、贡献声明与该组织页可以支持的内容，未核实成立时间、人员规模或荣誉信息。

来源方对数据可靠性的判断不进入本节；方法、口径与公开缺口分别见“实验设计和数据口径”和“其他/完整性与验收”。

## 实验设计和数据口径

本 source 的公开对象是三类**已清洗的表型测量表**，来自酵母表面展示系统上对 SARS-CoV-2 受体结合域（RBD）组合突变文库的高通量结合测定。数据不是测序原始计数：原始 FASTQ 存放在 NCBI BioProject `PRJNA1433816`，仓库只发布经比对、计数与拟合后的基因型级表型值，以及部分中间推断表。

论文构建了四个组合突变文库。其中第一个是武汉 Hu-1 背景上 ACE2 相关 Omicron BA.1 突变的全部组合，来自前作已发表数据，不在本仓库内。本 source 覆盖其余三个，仓库的 `File_Details.csv` 用 `B`、`C`、`M` 标注：

| 文库 | 遗传背景 | 设计变体数 | ACE2 测定 | 抗体测定 | 抗体清单 |
| --- | --- | ---: | --- | --- | --- |
| B | Omicron ancestor | 1,152 | Tite-Seq | Tite-Seq | AZD1061、AZD8895、REGN10987 |
| C | 七个背景 | 16,800 | Tite-Seq | Sort-Seq（两个浓度） | AZD1061、AZD8895、REGN10987、LY-CoV1404、S309 |
| M | 四个背景 | 约 30 万（实测） | Sort-Seq（单浓度） | Enrichment | AZD1061、AZD8895、REGN10987、LY-CoV1404、S309、002-S21F2、Iv0221、Iv0262 |

Library B 的设计量按 2⁷ × 3² = 1,152 计算，对应七个双等位与两个三等位位点。Library C 按 7 个背景 × 2³ × 3¹ × 4¹ × 5² = 16,800 计算。

三个文库的位点集合不同，且同一文库内不同测定也未必一致：

- Library B 的九个位点固定为 371、376、405、408、446、452、486、493、496。论文 Figure 2 把它们的等位归属标为 BA.1 突变（S371L、G446S、G496S）、BA.2 与 BA.5 共有突变（T376A、D405N、R408S）、BA.5 特有突变（L452R、F486V、R493Q），以及另两个突变（S371F、L452Q）。L452Q 是 BA.2.12.1 谱系在 RBD 上的特征替换，BA.4 与 BA.5 的 RBD 突变集合在本次测定的九个位点上不可区分，因此仓库 README 写作 BA.5／BA.2.12.1、论文正文写作 BA.4／BA.5 指的是同一组观测等位。
- Library C 的七个库位点固定为 346、444、452、460、486、490、493，另有一个 `pos_background` 背景编号。背景由 17 个位点（339、371、373、375、376、405、408、417、440、446、477、478、484、496、498、501、505）组成的序列决定。
- Library M 的位点集合按表变化：a 组抗体表 39 个位点，b 组抗体表 33 个位点，`MABAa_ACE2` 与 `MABAa_Exp` 36 个，`MABAb_ACE2` 与 `MABAb_Exp` 38 个。

三类表型的定义与数值来源：

- **KDs**：经 Tite-Seq 滴定的表观解离常数。酵母在 10⁻¹² 至 10⁻⁶ M、0.5 log 间隔的一系列配体浓度下孵育，按结合荧光分选到四个门（一个 PE⁻ 非结合门与三个等群体的 PE⁺ 门），测序得到每个基因型在各浓度下的平均对数荧光，再对每个基因型拟合 Hill 函数的对数形式，得到 `K_D,app`。拟合的 `A` 参数限制在 10²–10⁶，`B` 限制在 1–10⁵，`K_D` 限制在 10⁻¹⁴–10⁻⁵ M。发布表中的 `kd` 即该拟合值。
- **Fluor**：指定配体浓度下的平均对数荧光。Sort-Seq 在少数浓度上测量（Library C 的抗体用 10⁻⁶ M 与 10⁻⁸ M，Library M 的 ACE2 用 10⁻⁷ M），表达表型则是表达标签自身的荧光值。表中列名以 `_mean` 结尾的是该量，`_sd` 是其不确定度。
- **Enrichment**：单分箱富集分数，用于 Library M 的抗体。分选时只收一个门——非结合与结合两侧中细胞数较少的那一侧——按该侧是否代表结合表型取 `p_s,f` 或其补数 `1 − p_s,f`。因此该分数可以为负，也可以大于 1，方向随所选群体变化，跨抗体的绝对值不可直接比较。

测量链上可核验的边界：Tite-Seq 的 `K_D,app` 是拟合参数而非直接观察量，依赖 Hill 模型假设；不同测定之间的位点集合差异来自各表实际观察到的突变位点，不是设计差异；Library M 的富集表在合并前对 ACE2 结合群体做过一次分选富集。

仓库 README.txt 还说明 Library M 的理论组合数为 4 × 2¹⁶ × 3⁵。按该式实算为 63,700,992，与 README.txt 写的 63,700,920 相差 72；实际测定的约 30 万个变体是随机抽取的，不由该式直接决定。

## 论文原文

- 标题：Epistasis and background dependence in the evolution of Omicron variants of the SARS-CoV-2 spike protein
- 作者：Alief Moulana、Thomas Dupic、Michael M. Desai
- 发表来源：Molecular Biology and Evolution，第 43 卷第 5 期，文章号 msag100
- 归档文本版本：正式发表版（version of record），经 Europe PMC 的 PMC13179739 全文 XML 核对
- 发布日期：2026-05-01
- DOI：`10.1093/molbev/msag100`
- PMID / PMCID：`42142336` / `PMC13179739`
- 本地文件：`articles/BackgroundDependenceSARSCoV2_2026-05-01_MBE-msag100.xml`
- 文件大小：151.64 KiB（155,276 bytes）
- SHA-256：`3cb751522d6249a36cff2cd142430c541df65d75bdef52082b96bd7d50351f82`
- 文本许可：CC BY 4.0
- 补充材料：`articles/BackgroundDependenceSARSCoV2_2026-05-01_MBE-msag100-supplement-1-library-construction.xlsx`（107.79 KiB（110,372 bytes），建库用 gblock 与引物表，论文 Methods 记为 File S1）、`articles/BackgroundDependenceSARSCoV2_2026-05-01_MBE-msag100-supplement-2-sequencing-primers.xlsx`（12.97 KiB（13,278 bytes），测序引物，记为 File S2）、`articles/BackgroundDependenceSARSCoV2_2026-05-01_MBE-msag100-supplement-3-supplementary-figures.pdf`（1.87 MiB（1,956,833 bytes），补充图 S1–S3）

出版方的正文 PDF 未归档：`academic.oup.com` 的 article-pdf 端点在本项目出口返回 Cloudflare 拦截页，带浏览器 User-Agent 重试仍为 HTTP 403，Europe PMC 的 PDF 渲染端点返回 403、PMC 网页版 PDF 路径返回挑战页而非 PDF。正文改用同一 PMCID 的 Europe PMC 全文 XML 核对，书目字段与 DOI 元数据另行交叉核对。PDF 缺口记入“待解决问题与处理进展”的 `Q02`。

## 仓库内容

上游一手入口为 GitHub 仓库 `desai-lab/background_dependence_SARS-CoV-2` 的固定 commit。版本锚点：

| 项目 | 值 |
| --- | --- |
| 仓库 | `https://github.com/desai-lab/background_dependence_SARS-CoV-2.git` |
| commit | `a73c17836975a8e3f5ad093c7b423ddee5fb17e8` |
| commit tree | `335172dc13ab0f707db0e9570d480744fc2c2655` |
| commit 时间 | 2026-02-13T19:50:46+00:00 |
| commit 标题 | `Initial commit` |
| 远端 refs | 仅 `refs/heads/main`，无 tag、无 release |

`source_version` 取名 `snapshot-2026-02-13`，日期取自该固定 commit 自身的提交时间，不是本次下载日期。仓库只有一个 commit，不存在论文发表后继续更新的版本漂移问题。

快照为完整快照：固定 tree 共 69 个 blob、252,686,386 bytes，全部以原始字节保存。`.gitignore` 内容为 `*.csv`，因此上游以 `.csv.zip` 形式提交表型表。

```text
snapshot-2026-02-13/
└── background_dependence_SARS-CoV-2/
    ├── README.txt
    ├── File_Details.csv.zip
    ├── File_Details.xlsx
    ├── File_Details.xlsx.zip
    ├── ABBA_a_phenotype_data.csv.zip … ABBA_h_phenotype_data.csv.zip
    ├── XABA_ACE2_rep_d_phenotype_data.csv.zip
    ├── XABA_AZD1061_6_rep_a_phenotype_data.csv.zip … XABA_S309_8_rep_b_phenotype_data.csv.zip
    ├── MABAa_ACE2_phenotype_data.csv.zip
    ├── MABAa_002-S21F2_phenotype_data.csv.zip … MABAa_S309_phenotype_data.csv.zip
    ├── MABAb_ACE2_phenotype_data.csv.zip
    ├── MABAb_002-S21F2_phenotype_data.csv.zip … MABAb_S309_phenotype_data.csv.zip
    ├── LibraryB_raw_data_processing/
    │   ├── 20241222_ABBA_old_Kd-reloaded.R
    │   └── 20250127_ABBA_exp_loaded.R
    ├── LibraryC_raw_data_processing/
    │   ├── 20241224_XABA_reloaded.R
    │   ├── XAB_inferred_phenos_ab_20250216.csv.zip
    │   └── XAB_inferred_phenos_ace2_c_20250216.csv.zip
    └── LibraryM_raw_data_processing/
        ├── 20251016_MABA_ab_loaded.R
        ├── 20251016_MABA_ace2_loaded.R
        ├── MABA_inferred_ab_enrichment_20251016.csv.zip
        └── MABA_inferred_phenos_fluor_20251016.csv.zip
```

根目录的 33 个 `*_phenotype_data.csv.zip` 是发布表，前三个字母标识文库（`ABBA` = B、`XABA` = C、`MABA` = M）。`File_Details.csv` 是这批表的索引，逐文件给出所属文库、配体、重复号、表型类别以及表型列名与标准差列名。三个 `*_raw_data_processing/` 目录存放作者的清洗脚本和两张中间推断表，是发布表的上游产物。

`.DS_Store` 与 `LibraryC_raw_data_processing/.DS_Store`、`LibraryM_raw_data_processing/.DS_Store` 是上游提交的 macOS 元数据文件，原样保留。

## 数据结构

### 三个变异文库和表型类型

33 张发布表按 `File_Details.csv` 的 `Library` 列分为三组，字段结构各不相同。

**Library B（`ABBA_*`，8 张表）** 每张 15 列：一个无名行号列、`ph_mean`、`ph_sd`、九个 `pos_<n>` 位点列、`sort`、`dataset`、`aa_geno`。`dataset` 恒为 `ABBA`，`sort` 取 `a` 至 `h`，与文件名后缀一致。`File_Details.csv` 给出配体与重复号的对应：a/b 为 ACE2，c/d 为 REGN10987，e/f 为 AZD1061，g/h 为 AZD8895。

行数在 1,152（a、b、h）与 1,520（d）之间。设计量为 1,152；超过设计量的表在九个位点上出现设计外等位，例如 `pos_452` 出现 `H`、`pos_446` 出现 `E`、`pos_371` 出现 `R`、`pos_376` 出现 `P`、`pos_496` 出现 `A`。这些行按上游发布原样保留。

**Library C（`XABA_*`，23 张表）** 每张 15 列：`ph_mean`、`ph_sd`、`pos_background`、七个库位点列、`xaba_geno`、`sort`、`dataset`、`aa_geno`、`background_strain`。`sort` 取 `a`、`b` 或 `d`，`dataset` 取 `XABA_ab` 或 `XABA_ace2`。

表型列名与测定的对应来自作者脚本 `20241224_XABA_reloaded.R`：`X16`/`X18` 为 AZD1061 在 1 µM 与 10 nM，`X26`/`X28` 为 AZD8895，`X36`/`X38` 为 LY-CoV1404，`X46`/`X48` 为 REGN10987，`X56`/`X58` 为 S309，`F` 为表达荧光，`ace2` 为 ACE2。文件名中的 `_6_` 与 `_8_` 即对应 10⁻⁶ M 与 10⁻⁸ M 两个浓度。行数从 2,393（`XABA_Exp_rep_b`）到 57,829，全部大于 16,800 的设计量。

`pos_background` 的取值由同一脚本按 17 位背景序列匹配得到，脚本内定义了七个模板并把它们命名为 W、Q498R、N501Y、DBL、OM、BA1、BA2：

**`pos_background`（`XABA_*`；取值范围依据：来源脚本 `20241224_XABA_reloaded.R` 的模板定义）**

| 原始取值 | 脚本内名称 | 17 位背景序列 |
| --- | --- | --- |
| `1` | W | `GSSSTDRKNGSTEGQNY` |
| `2` | Q498R | `GSSSTDRKNGSTEGRNY` |
| `3` | N501Y | `GSSSTDRKNGSTEGQYY` |
| `4` | DBL | `GSSSTDRKNGSTEGRYY` |
| `5` | OM | `DSPFTDRNKGNKAGRYH` |
| `6` | BA1 | `DLPFTDRNKSNKASRYH` |
| `7` | BA2 | `DFPFANSNKGNKAGRYH` |
| `9` | 未命名 | 不匹配上述任一模板、且七个库位点全为武汉等位 |

取值 `8` 从未出现。脚本对不匹配任何模板且七个库位点不等于武汉等位的行赋 `0` 并在写表前过滤掉，因此 `0` 不出现在发布表中。该脚本还按 `pos_background` 分组保留行数不少于 64 的组。

**Library M（`MABA_*`，20 张表）** 分两类。ACE2 与表达各两张（`MABAa_ACE2`、`MABAb_ACE2`、`MABAa_Exp`、`MABAb_Exp`），带 `ph_mean` 与 `ph_sd` 成对；八个抗体各两张（`MABAa_<抗体>`、`MABAb_<抗体>`），只有 `ph_mean`。所有表共有一个无名行号列、`sort`、`dataset`、`aa_geno`，位点列数按前述四组不同。抗体表的 `sort` 列取值为 `a` 或 `NA`，`dataset` 列取值为 `MABA` 或 `NA`，与文件名前缀并不一一对应。

行数：a 组抗体表 171,228，b 组抗体表 156,562，`MABAa_Exp` 与 `MABAa_ACE2` 298,120，`MABAb_ACE2` 与 `MABAb_Exp` 187,237。Library M 的两个处理脚本把背景筛选注释掉，因此这些表保留全部背景而不做参考背景过滤。

`aa_geno` 是 RBD 的氨基酸序列，起点为残基 331，长度 175。当上游基因型长度不等于 525 时，脚本分别翻译前后两段再用 `-` 连接，此时 `aa_geno` 中会出现一个 `-` 占位符，占据该 3 nt 缺失对应的残基位置。全部 51 张表满足：对任意 `pos_<n>` 列，`aa_geno` 的第 `n − 331` 个字符（从 0 计）与该列取值相同，`-` 位置除外。

### 表型表的分组和粒度

每张表的一行是一个基因型在该次测定下的表型读数。同一基因型会在不同表、不同重复号下多次出现，行与行之间不构成独立样本：Library B 的 a 与 b 是同一配体的两次独立实验，Library C 同一抗体在 1 µM 与 10 nM 的两次测定共享同一批基因型但表型不同，Library M 的 a 组与 b 组关系未由随附脚本说明。

不同表之间的键不统一。Library B 用九个 `pos_<n>` 列加 `aa_geno` 标识基因型，没有单列主键。Library C 用 `xaba_geno`，其值等于 `pos_background` 直接拼接七个库位点列的取值，可作稳定键。Library M 只有 `aa_geno` 与位点列，没有拼接键。

### 处理目录中的中间表

四个中间表是发布表的上游产物，未做基因型展开，也不是测序计数：

| 文件 | 行数 | 列数 | 内容 |
| --- | ---: | ---: | --- |
| `LibraryC_raw_data_processing/XAB_inferred_phenos_ab_20250216.csv.zip` | 157,357 | 26 | 五个抗体在两个浓度上的分箱推断荧光与表达 |
| `LibraryC_raw_data_processing/XAB_inferred_phenos_ace2_c_20250216.csv.zip` | 57,211 | 51 | ACE2 的 Hill 拟合值、`cov` 与 11 个分箱的占用比与荧光统计 |
| `LibraryM_raw_data_processing/MABA_inferred_ab_enrichment_20251016.csv.zip` | 156,561 | 27 | 八个抗体的富集分数与分箱计数 |
| `LibraryM_raw_data_processing/MABA_inferred_phenos_fluor_20251016.csv.zip` | 187,237 | 6 | ACE2 与表达的均值与标准差 |

四者都额外带一个 `__MACOSX/._<同名>` 成员，是打包时写入的 macOS 资源分叉，不含数据。

### 字段说明

**`File_Details.csv` / `File_Details.xlsx`**（索引表，48 行）

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `Filename` | 字符串 | 发布表文件名，不含 `.zip` 后缀 |
| `Library` | 枚举 | 所属文库，取值 `B`、`C`、`M` |
| `Ligand` | 字符串 | 测定的配体名；表达测定为 `-` |
| `Replicate` | 整数 | 重复编号；Library M 的抗体表统一写 `1` |
| `Phenotype` | 字符串 | 表型类别与条件，取值见下 |
| `Pheno_col` | 字符串 | 对应表中的表型列名，恒为 `ph_mean` |
| `Std_col` | 字符串 | 对应表中的标准差列名，`ph_sd` 或 `-` |

**`Phenotype`（`File_Details.csv`；取值范围依据：当前 source version 观察）**

| 原始取值 | 含义 |
| --- | --- |
| `KD` | Tite-Seq 拟合的表观解离常数 |
| `Fluor at 1uM` | 1 µM 配体浓度下的对数荧光 |
| `Fluor at 10nM` | 10 nM 配体浓度下的对数荧光 |
| `Fluor at 100nM` | 100 nM 配体浓度下的对数荧光 |
| `Fluor RBD` | 表达标签自身的荧光 |
| `Enrichment at 100nM` | 100 nM 配体浓度下的单分箱富集分数 |

**Library B 表（`ABBA_*`，15 列）**

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| （无名首列） | 整数 | 行号，从 1 起 |
| `ph_mean` | 浮点 | 该次测定的表型值；`KD` 表为 `kd`，其余为对数荧光 |
| `ph_sd` | 浮点 | `ph_mean` 的标准差 |
| `pos_371`、`pos_376`、`pos_405`、`pos_408`、`pos_446`、`pos_452`、`pos_486`、`pos_493`、`pos_496` | 单字符 | 该位点的氨基酸，按武汉 Hu-1 参考编号 |
| `sort` | 枚举 | 重复号，取值 `a` 至 `h` |
| `dataset` | 字符串 | 恒为 `ABBA` |
| `aa_geno` | 字符串 | 175 个字符的 RBD 氨基酸序列，起点残基 331 |

**Library C 表（`XABA_*`，15 列）**

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `ph_mean` | 浮点 | 表型值 |
| `ph_sd` | 浮点 | 标准差；ACE2 表的该列在来源脚本中写作 `cov` |
| `pos_background` | 枚举 | 背景编号，取值见上表 |
| `pos_346`、`pos_444`、`pos_452`、`pos_460`、`pos_486`、`pos_490`、`pos_493` | 单字符 | 七个库位点的氨基酸 |
| `xaba_geno` | 字符串 | `pos_background` 与七个位点取值的直接拼接 |
| `sort` | 枚举 | 重复号，取值 `a`、`b`、`d` |
| `dataset` | 枚举 | `XABA_ab` 或 `XABA_ace2` |
| `aa_geno` | 字符串 | 175 个字符的 RBD 氨基酸序列 |
| `background_strain` | 字符串 | 17 个字符的背景序列，取值与 `pos_background` 一一对应 |

**Library M 表（`MABA_*`，38 至 44 列）**

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| （无名首列） | 整数 | 行号，从 1 起 |
| `ph_mean` | 浮点 | 表型值；ACE2 与表达为对数荧光，抗体表为富集分数 |
| `ph_sd` | 浮点 | 标准差；仅 ACE2 与表达表存在，抗体表没有该列 |
| `pos_<n>` | 单字符 | 该位点的氨基酸；位点集合按表的四组不同，见前文 |
| `sort` | 枚举 | 取值 `a`、`b` 或 `NA` |
| `dataset` | 枚举 | 取值 `MABA` 或 `NA` |
| `aa_geno` | 字符串 | 175 个字符的 RBD 氨基酸序列，可能含一个 `-` 占位符 |

**`XAB_inferred_phenos_ab_20250216.csv`（26 列）**

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `sort` | 枚举 | 重复号，取值 `a` 或 `b` |
| `genotype` | 字符串 | RBD 核苷酸序列 |
| `16_mean`、`18_mean`、`26_mean`、`28_mean`、`36_mean`、`38_mean`、`46_mean`、`48_mean`、`56_mean`、`58_mean`、`0_mean` | 浮点 | 各分箱推断的对数荧光；十位数字标识抗体（1 = AZD1061、2 = AZD8895、3 = LY-CoV1404、4 = REGN10987、5 = S309），个位数字标识浓度，`0` 为另一分箱 |
| 同名前缀的 `_sd` 列 | 浮点 | 对应 `_mean` 列的标准差 |
| `F_mean`、`F_sd` | 浮点 | 表达荧光及其标准差 |

**`XAB_inferred_phenos_ace2_c_20250216.csv`（51 列）**

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `sort` | 字符串 | 恒为 `c` |
| `genotype` | 字符串 | RBD 核苷酸序列 |
| `kd` | 浮点 | Hill 拟合的表观解离常数 |
| `A`、`B` | 浮点 | Hill 拟合的饱和荧光与背景荧光参数 |
| `error` | 浮点 | 拟合误差 |
| `cov` | 浮点 | 拟合协方差类指标，发布表的 `ph_sd` 取自此列 |
| `6_occupancy_mean`、`65_occupancy_mean`、`7_occupancy_mean`、`75_occupancy_mean`、`8_occupancy_mean`、`9_occupancy_mean`、`10_occupancy_mean`、`11_occupancy_mean`、`12_occupancy_mean`、`125_occupancy_mean`、`0_occupancy_mean` | 浮点 | 各分箱的推断占用比；列名前缀为浓度编号的紧凑写法 |
| 同名前缀的 `_occupancy_sd` 列 | 浮点 | 对应占用比的标准差 |
| `6_mean`、…、`0_mean` | 浮点 | 各分箱的对数荧光均值 |
| 同名前缀的 `_sd` 列 | 浮点 | 对应均值的标准差 |

缺失值在 `_mean`／`_occupancy_mean` 一类列中以空字段表示，读取时不能当作 0。

**`MABA_inferred_ab_enrichment_20251016.csv`（27 列）**

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `seq_consensus` | 字符串 | 该变体的 RBD 核苷酸共有序列 |
| `uns`、`uns_0` | 浮点 | 未分选群体的读数估计 |
| `ACE2_1`、`ACE2_2`、`ACE2_3`、`ACE2_4` | 浮点 | ACE2 四次测定的分箱读数 |
| `Exp_1`、`Exp_2`、`Exp_3`、`Exp_4` | 浮点 | 表达四次测定的分箱读数 |
| `ab_1`、…、`ab_8` | 浮点 | 八个抗体的分箱读数；编号与抗体的对应关系未在本文件中给出 |
| `enrichment_1`、…、`enrichment_8` | 浮点 | 八个抗体的富集分数，可为负或大于 1 |

这些计数列大量以空字段表示缺失，与 0 有别。

**`MABA_inferred_phenos_fluor_20251016.csv`（6 列）**

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `sort` | 枚举 | 重复号，取值 `a`、`b` 或 `NA` |
| `genotype` | 字符串 | RBD 核苷酸序列 |
| `ACE2_mean`、`ACE2_sd` | 浮点 | ACE2 对数荧光的均值与标准差 |
| `Exp_mean`、`Exp_sd` | 浮点 | 表达荧光的均值与标准差 |

`ACE2_mean`、`Exp_mean` 在缺少对应测定的行上为空字段。

### 数据示例

`ABBA_a_phenotype_data.csv` 的第一条记录（15 列，此处按可读顺序摘录）：

```text
1, 9.64563867067554, 0.337355286724439, S, T, D, S, S, L, F, R, G, a, ABBA,
NITNLCPFDEVFNATRFASVYAWNRKRISNCVADYSVLYNSAPFFTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVSQIAPGQTG
NIADYNYKLPDDFTGCVIAWNSNKLDSKVSGNYNYLYRLFRKSNLKPFERDISTEIYQAGNKPCNGVAGFNCYFPLRSYGFRPT
YGVGH
```

首列为行号 1；`ph_mean` 为 9.6456、`ph_sd` 为 0.3374；`pos_371` 到 `pos_496` 依次为 `S T D S S L F R G`；`sort` 为 `a`；`dataset` 为 `ABBA`；`aa_geno` 是 175 个字符的 RBD 序列，起点残基 331。该行表示 ABBA 文库中一个基因型在 ACE2 重复 a 下的表观亲和力读数，不是独立样本——同一基因型在 `ABBA_b` 中另有一行。

`XABA_ACE2_rep_d_phenotype_data.csv` 的第一条记录：

```text
7.82312203547735, 0.828139724122806, 2, I, R, M, K, V, S, R, 2IRMKVSR, d,
XABA_ace2, NITNLCPFGEVFNATIFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEV
RQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSRVGGNYNYMYRLFRKSKLKPFERDISTEIYQAGSTPCNGVEGVNCYSP
LRSYGFRPTNGVGY, GSSSTDRKNGSTEGRNY
```

该行表型为 7.8231，标准差 0.8281；`pos_background` 为 `2`，七个库位点为 `I R M K V S R`；`xaba_geno` 为背景号与七个位点的直接拼接 `2IRMKVSR`；`sort` 为 `d`；`dataset` 为 `XABA_ace2`；`background_strain` 为 `GSSSTDRKNGSTEGRNY`，与 `pos_background = 2` 的模板一致。

`MABAa_ACE2_phenotype_data.csv` 的第一条记录（42 列，`pos_` 列按位点顺序摘录）：

```text
1, 3.24957273771927, 0.665400791331667, V, G, R, K, L, F, P, F, T, K, D, S, K, N, N, L, K, P,
G, D, L, F, L, K, N, K, K, -, K, V, S, R, S, R, Y, H, a, MABA,
NVTNLCPFGEVFNATRFASVYAWNRKRISNCVADYSVLYNFAPFFTFKCYGVSPTKLNDLCFTNVYADSFVIKGDEVSQIAPGQ
TGKIADYNYKLPDDFTGCVIAWNSNNLDSKPGGNYDYLYRFLRKSKLKPFERDISTEIYQAGNKPCKG-KGVNCYSPLRSYSFR
PTYGVGH
```

该行 `ph_mean` 为 3.2496、`ph_sd` 为 0.6654，随后是按位点顺序排列的 36 个氨基酸取值；其中 `pos_456` 位置为空缺对应的残基记为 `-`，与 `aa_geno` 中的占位符位置一致。`sort` 为 `a`，`dataset` 为 `MABA`。

## PDB 数据库

论文在三处点名结构，全部用作展示突变位点在 RBD 表面空间分布的参考结构。数据集本身不含逐行 PDB 键，也没有把某条记录绑定到某个结构的字段，因此映射强度为“论文制图所用的参考结构”，不是逐行或逐构建体映射。

| 论文位置 | PDB | 论文中的用途 |
| --- | --- | --- |
| Figure 1c | `7WHH` | 展示 Figure 1a 所列位点的空间分布 |
| Figure 2d、Figure 3f | `7L7E` | 展示 Library B 与 Library C 的突变效应与上位效应 |
| Figure 3f | `7MMO` | 展示 Library C 的上位效应位点 |

RCSB 实体核验结果：

| PDB | 实体 | 描述 | author chains | label chains | 长度 |
| --- | ---: | --- | --- | --- | ---: |
| `7WHH` | 1 | Processed angiotensin-converting enzyme 2 | A | A | 598 |
| `7WHH` | 2 | Spike glycoprotein | E | B | 194 |
| `7L7E` | 1 | AZD8895 重链 | A, H, I, T | A, G, H, O | 225 |
| `7L7E` | 2 | AZD8895 轻链 | B, J, L, U | B, I, J, P | 216 |
| `7L7E` | 3 | AZD1061 重链 | C, E, M, O | C, E, K, M | 236 |
| `7L7E` | 4 | AZD1061 轻链 | D, F, N, P | D, F, L, N | 219 |
| `7L7E` | 5 | Spike protein S1 | G, K, S, b | Q, R, S, T | 215 |
| `7MMO` | 1 | LY-CoV1404 Fab 重链 | A, D | A, D | 223 |
| `7MMO` | 2 | LY-CoV1404 Fab 轻链 | B, E | B, E | 215 |
| `7MMO` | 3 | Spike protein S1 | C, F | C, F | 205 |

chain 选择证据与边界：`7WHH` 的两个实体各只有一个副本，实体与链的对应无歧义。`7L7E` 的四个抗体实体各有 4 个同序列副本，且该条目同时含 AZD8895 与 AZD1061 两套 Fab；`7MMO` 的三个实体各有 2 个同序列副本。同序列副本无法仅凭序列区分，论文也没有指定副本，因此本次不指定任何具体副本，也不生成带角色标签的选链 FASTA。本 skill 的通用脚本 `fetch_pdb_reference_data.py` 要求填入选链映射，本次未使用它。

数据集测定的其余抗体（REG10987 之外还包括 002-S21F2、Iv0221、Iv0262 等）论文未点名任何结构，本次不自行选择锚点。上游 payload 内不含结构文件，仓库的分析 notebook 也不加载坐标。

取回的文件为 RCSB 原始完整 entry FASTA 与完整 mmCIF，共 6 个对象、8.14 MiB（8,538,369 bytes）。FASTA 是 RCSB 按条目发布的完整 entry 序列，保留来源字节，不是项目生成的选链视图。

| 文件 | 大小 | SHA-256 |
| --- | ---: | --- |
| `pdb/sequences/rcsb_pdb_7WHH.fasta` | 973 bytes | `2974d4166da9f0f7ae9bb930258e80cb410cff4b40ef6f04fd2783b403035faf` |
| `pdb/sequences/rcsb_pdb_7L7E.fasta` | 1,713 bytes | `14db0c80360c52ca97470df0c7b4cc32ab69c26e482d3db4f7f0c6896fbbfb81` |
| `pdb/sequences/rcsb_pdb_7MMO.fasta` | 875 bytes | `cde8f27a736ca2fa8932a9b0936d4bfeac7e8e184a2e1aaab2ed56ca281c3bb3` |
| `pdb/structures/7WHH.cif` | 1.25 MiB（1,310,469 bytes） | `d28d5ad354f857f3f4382e5d50ffeeb8961afc04388ab412d45ac1db916ecc9e` |
| `pdb/structures/7L7E.cif` | 5.94 MiB（6,232,609 bytes） | `e0459e9fac3cb1b8e36ed7526941922627e792a53b57b59e1381305790f19c78` |
| `pdb/structures/7MMO.cif` | 968.49 KiB（991,730 bytes） | `c10bbc839a0b964544d916c0f11fb559de4158528419c776c8f4c24dfa00d73f` |

FASTA 记录数与 RCSB 实体数逐条目一致：`7WHH` 2 条、`7L7E` 5 条、`7MMO` 3 条。

## 采集过程记录

- 2026-09-25：另一开发者 `wuhuawei` 以其自有工具链记录本 source 的仓库锚点与逐文件字节数，状态止于 `payload-acquired`，其记录中的 `independent_audit_passed` 为 `false`。本次接入按 `dataset-source-onboarding` 重新执行独立验收。
- 2026-09-28：核对 GitHub 远端 refs。`git ls-remote --symref` 显示 `HEAD` 指向 `refs/heads/main`，`--refs` 只返回 `refs/heads/main` 一个 ref，无 tag。固定 commit `a73c17836975a8e3f5ad093c7b423ddee5fb17e8`，tree `335172dc13ab0f707db0e9570d480744fc2c2655`，提交时间 2026-02-13T19:50:46+00:00，标题 `Initial commit`。
- 2026-09-28：编写并执行 `scripts/download_r73_background_dependence.sh`，从固定 commit 取 Git 对象、`git archive` 展开固定 tree，再逐文件按 Git blob 编码重算 SHA-1。得 69 个 blob、252,686,386 bytes，内容 inventory SHA-256 为 `dbab1030b70d5af576951ac5366654b067176c6f55976c84f6c733c2d1b761ef`。staging 内无临时残留。该结果与 `wuhuawei` 记录的逐文件清单一致。
- 2026-09-28：`academic.oup.com` 的正文 PDF 端点返回 Cloudflare 拦截页。带浏览器 User-Agent 重试仍为 HTTP 403；Europe PMC 的 `?pdf=render` 返回 403，`fullTextPDF` 返回 404，PMC 网页版 PDF 路径返回 1,817 bytes 的挑战页而非 PDF。改从 Europe PMC 取同一 PMCID 的全文 XML 与补充包，`hasPDF`、`hasSuppl` 均为 `Y`。
- 2026-09-28：补充包 `msag100_supplementary_data.zip` 内含三个对象，上游文件名为 `Supplemenatry_Figures.pdf`（原拼写如此）、`Supplementary_File_1_Library_construction.xlsx`、`Supplementary_File_2_Sequencing_Primersxlsx.xlsx`（原文件名缺少分隔点）。按项目命名约定改写为 `BackgroundDependenceSARSCoV2_2026-05-01_MBE-msag100-supplement-<n>-<描述>.<ext>`，改写前后核对字节数与 SHA-256 一致。
- 2026-09-28：从 RCSB 取 `7WHH`、`7L7E`、`7MMO` 的完整 entry FASTA 与完整 mmCIF。首次下载的 `7L7E.cif` 与 `7MMO.cif` 在原子坐标循环中途截断（文件末尾停在半行 `ATOM` 记录，`curl --max-time` 到期），改用 `.cif.gz` 端点重新取得并解压，以“文件以 `#` 收尾”为准复核后替换。`7MMO.cif` 的完整大小为 991,730 bytes，截断版本为 933,888 bytes；`7L7E.cif` 的完整大小为 6,232,609 bytes，截断版本为 2,514,944 bytes。
- 2026-09-28：解析 51 张发布表与 4 张中间表。逐一验算并通过的恒等式：`xaba_geno` 等于 `pos_background` 与七个库位点取值的直接拼接（23 张表全部行）；`pos_background` 取 1 至 7 时 `background_strain` 等于对应模板（23 张表全部行）；全部 51 张表满足 `aa_geno` 第 `n − 331` 个字符等于 `pos_<n>` 列取值，`-` 位置除外（合计 4,795,558 行）。`pos_background` 的实际取值为 1 至 7 与 9，8 未出现。
- 2026-09-28：普查压缩包成员结构。58 个 zip 每个恰有一个数据成员，其中 4 个中间表另带一个 `__MACOSX/._<同名>` 资源分叉成员；未发现绝对路径、`..` 穿越或符号链接成员。
- 2026-09-28：从 ENA portal 取 `PRJNA1433816` 的 run 级 filereport：613 runs、1,226 个 FASTQ 对象、243,537,670,832 bytes（226.81 GiB），全部为 Illumina NovaSeq 6000 的 `AMPLICON`／`SYNTHETIC`／`PCR`。直连 `ftp.sra.ebi.ac.uk` 超时，经节点代理访问。测得上限约单流 0.74 MB/s、两流并行合计 1.56 MB/s。
- 2026-09-28：启动 `scripts/download_r73_background_dependence_reads.sh` 下载 reads，逐对象校验官方字节数与 MD5，已完成对象写入状态文件可断点续跑。与 R71 的 reads 下载并行执行。
- 2026-09-28：核验责任主体背景。论文署名与贡献声明确认责任方为哈佛大学组织与进化生物学系 Desai 实验室。`https://github.com/desai-lab` 可达；哈佛 OEB 人员页与 `projects.iq.harvard.edu/desailab` 返回 HTTP 403，`desai.harvard.edu` 与 `mdesai.oeb.harvard.edu` 无法连接，`desailab.org` 可达但属于研究补体系统的另一实验室。据此只写论文署名、贡献声明与组织页支持的内容。
- 2026-09-28：核验许可。固定 tree 内无 `LICENSE`、`LICENCE` 或 `COPYING`。GitHub 仓库元数据的 license 字段因共享代理出口 IP 触发 API 限流（HTTP 403）未能读取，`/license` 端点同样 403。论文文本为 CC BY 4.0。
- 2026-09-28：编写 `scripts/validate_r73_background_dependence.py`，对 staging 目录执行独立验收，结果为 `VALIDATION OK`。
- 2026-09-30：reads 下载改由本机 Clash 隧道出口（ab02 `127.0.0.1:27897` 反向代理至本机 7892，比 ab02 上 yangwuyu 的 mihomo 17890 快 2–3 倍），使用自建并发下载器 `scripts/r73_concurrent_download.py`（4 路并发，父进程唯一写状态文件，逐对象校验官方字节数与 MD5）。下载器对 ENA 目录占位符缺陷对象不再自动重试，改以 `verified.txt.skipped` 记录并跳过。
- 2026-10-01：reads 下载完成。1,222 个 FASTQ 对象（243,080,357,268 bytes，226.39 GiB）逐对象通过官方字节数与 MD5 校验并落盘 staging，无 `.partial` 残留。inventory 全量 1,226 个对象（243,537,670,832 bytes）；4 个对象（`SRR37521082_2`、`SRR37521286_2`、`SRR37521546_2`、`SRR37521649_2`）因 ENA 缺失无法取得，见 `Q07`。
- 2026-10-01：将 `sra/` 从 staging 原子装配进正式 source version 目录，补丁 validator 支持 `--require-sra` 与 `R73_SRA_SKIPPED` 跳过清单，以 `--require-sra` 全量复验通过后发布。发布前后核对目录属主与模式为同组可读。

## 参考文献

- 数据仓库：`desai-lab/background_dependence_SARS-CoV-2`，固定 commit `a73c17836975a8e3f5ad093c7b423ddee5fb17e8`，<https://github.com/desai-lab/background_dependence_SARS-CoV-2>
- 原始测序：NCBI BioProject `PRJNA1433816`，<https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1433816>
- 主论文：Moulana A, Dupic T, Desai MM. Epistasis and background dependence in the evolution of Omicron variants of the SARS-CoV-2 spike protein. Molecular Biology and Evolution. 2026;43(5):msag100. doi:10.1093/molbev/msag100
- 前作（Library B 的方法来源）：Moulana A, et al. Compensatory epistasis maintains ACE2 affinity in SARS-CoV-2 Omicron BA.1. Nature Communications. 2022;13:7011. doi:10.1038/s41467-022-34506-z
- 前作（同为 Omicron RBD 抗体结合景观）：Moulana A, et al. The landscape of antibody binding affinity in SARS-CoV-2 Omicron BA.1 evolution. eLife. 2023;12:e83442. doi:10.7554/eLife.83442
- Tite-Seq 方法：Adams RM, Mora T, Walczak AM, Kinney JB. Measuring the sequence-affinity landscape of antibodies with massively parallel titration curves. eLife. 2016;5:e23156. doi:10.7554/eLife.23156
- 深度突变扫描背景：Starr TN, et al. Deep mutational scanning of SARS-CoV-2 receptor binding domain reveals constraints on folding and ACE2 binding. Cell. 2020;182:1295–1310.e20. doi:10.1016/j.cell.2020.08.012
- 上位效应拟合软件：Faure AJ, Lehner B. MoCHI: neural networks to fit interpretable models and quantify energies, energetic couplings, epistasis, and allostery from deep mutational scanning data. Genome Biology. 2024;25:303. doi:10.1186/s13059-024-03444-y
- PDB 条目（ACE2／RBD）：Lan J, et al. Structural insights into the SARS-CoV-2 Omicron RBD-ACE2 interaction. Cell Research. 2022;32:593–595. doi:10.1038/s41422-022-00644-8；结构 `7WHH`
- PDB 条目（AZD1061）：Dong J, et al. Genetic and structural basis for SARS-CoV-2 variant neutralization by a two-antibody cocktail. Nature Microbiology. 2021;6:1233–2477. doi:10.1038/s41564-021-00972-2；结构 `7L7E`
- PDB 条目（LY-CoV1404）：Westendorf K, et al. LY-CoV1404 (bebtelovimab) potently neutralizes SARS-CoV-2 variants. Cell Reports. 2022;39:110812. doi:10.1101/2021.04.30.442182；结构 `7MMO`
- 酵母展示体系：Wentz AE, Shusta EV. A novel high-throughput screen reveals yeast genes that increase secretion of heterologous proteins. Applied and Environmental Microbiology. 2007;73:1189–1198. doi:10.1128/AEM.02427-06

## 其他

### 数据范围和限制

本 source 的公开包是基因型级清洗表型表与部分中间推断表，不是测序原始计数。原始 FASTQ 已从 BioProject `PRJNA1433816` 对应的 ENA 条目取得并随本 source version 发布在 `sra/`，详见“完整性与验收”与 `Q01`。

三类表型不可合并为统一的亲和力标度：`KDs` 是 Hill 拟合的表观解离常数，`Fluor` 是单一浓度下的对数荧光，`Enrichment` 是单分箱富集分数且方向随所选群体变化。跨文库、跨表型的数值不可直接比较。

同一基因型在多次测定中重复出现。Library B 的重复对、Library C 的两个浓度与重复号、Library M 的 a/b 两组都指向同一批基因型，按行随机切分会让同一基因型同时出现在训练与测试侧。

格式细节：`aa_geno` 在部分行含 `-` 占位符；`XAB_inferred_phenos_*` 的 `_mean` 与 `_occupancy_mean` 列、`MABA_inferred_ab_enrichment` 的计数列以空字段表示缺失，与 0 有别。这些是不可见的原始表示，读取时须显式处理。

### 完整性与验收

| 验收项 | 结果 |
| --- | --- |
| 固定 commit 与 tree | `a73c1783…` / `335172dc…`，与冻结常量一致 |
| payload 文件集合 | 与固定 Git tree 完全一致，69 blob、252,686,386 bytes |
| 逐文件 Git blob SHA-1 | 全部与 tree 条目一致 |
| payload inventory SHA-256 | `dbab1030b70d5af576951ac5366654b067176c6f55976c84f6c733c2d1b761ef` |
| 论文与补充材料 | 4 个对象，字节数与 SHA-256 全部匹配 |
| PDB 锚点 | 3 个，FASTA 3 + mmCIF 3，逐文件字节数与 SHA-256 匹配；mmCIF 均以 `#` 收尾 |
| PDB FASTA 记录数 | 2 / 5 / 3，与 RCSB 实体数一致 |
| 表型表行数 | 51 张表逐表匹配冻结值 |
| `xaba_geno` 恒等式 | 23 张 Library C 表全部行成立 |
| `background_strain` 与背景模板 | 23 张 Library C 表全部行成立 |
| `aa_geno` 位点一致性 | 51 张表、合计 4,795,558 行全部成立 |
| 压缩包成员 | 58 个 zip 各含一个数据成员，无绝对路径、`..` 或符号链接 |
| 原始测序 reads | `sra/` 1,222 个对象、243,080,357,268 bytes（226.39 GiB），逐对象通过官方字节数与 MD5 校验；4 个 ENA 缺失对象已记录并按跳过口径核减（见 `Q07`） |
| staging 与发布后验证 | `validate_r73_background_dependence.py` 以 `--require-sra` 复验均通过 |

### 许可和再分发边界

- **仓库数据**：固定 tree 内没有 `LICENSE`、`LICENCE` 或 `COPYING`，仓库任何位置均无许可声明。GitHub 仓库元数据的 license 字段本次未能读取（API 限流，HTTP 403），`/license` 端点同样返回 403。因此结论是：**上游未特别说明覆盖该数据的许可，使用与再分发范围不明确**。既不推定允许，也不推定禁止。该事项记入 `Q03`。
- **论文文本**：CC BY 4.0，覆盖论文正文与随文补充材料。
- **代码**：三个 `*_raw_data_processing/` 目录下的 R 脚本随仓库发布，未附独立许可声明；仓库无顶层代码许可。
- **原始测序数据**：适用 NCBI／ENA 条目的条款，与前两类分开。
- **PDB 文件**：适用 RCSB PDB 的数据使用条款，与上述各类分开。

论文文本许可、代码许可与外部数据库条款都不能替代仓库数据的许可。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| Library B 的 Tite-Seq 亲和力（ACE2、AZD1061、AZD8895、REGN10987） | `ABBA_a`–`ABBA_h` 八张表 | 已包含 |
| Library C 的 ACE2 亲和力与五个抗体两浓度的 Sort-Seq | `XABA_*` 二十三张表 | 已包含 |
| Library M 的 ACE2／表达荧光与八个抗体富集 | `MABA_*` 二十张表 | 已包含 |
| Library B 的表达表 | `20250127_ABBA_exp_loaded.R` 输出 `ABBA_i` 与 `ABBA_j`，两者不在固定 tree 内 | 未公开 |
| Library C ACE2 的第二个重复中间表 | `20241224_XABA_reloaded.R` 读入 `XAB_inferred_phenos_ace2_d_20250216.csv`，该文件不在固定 tree 内 | 未公开 |
| 原始测序 reads | BioProject `PRJNA1433816`，613 runs、1,226 个 FASTQ、226.81 GiB；已发布 `sra/` 1,222 个对象（226.39 GiB），4 个 ENA 缺失对象见 `Q07` | 已包含（4 个对象缺失，见 `Q07`） |
| Library A（武汉背景上的 BA.1 突变组合） | 本仓库固定 tree 内无对应文件 | 不在本 source 范围 |
| 论文正式版 PDF | 出版方端点返回 Cloudflare 拦截页 | 未取得（`Q02`） |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-01；已关闭）：原始测序 reads 已发布。已从 BioProject `PRJNA1433816` 的 ENA run 级 inventory（613 runs、1,226 个 FASTQ、243,537,670,832 bytes）取得 1,222 个 FASTQ 对象（243,080,357,268 bytes，226.39 GiB），逐对象校验官方字节数与 MD5 通过，装配进 `sra/` 并随 source version 发布；以 `--require-sra` 复验通过。4 个对象因 ENA 缺失无法取得，见 `Q07`。
- `Q07`（最近更新：2026-10-01；未决，不阻塞发布）：ENA 缺失 4 个 FASTQ 对象。`SRR37521082_2`、`SRR37521286_2`、`SRR37521546_2`、`SRR37521649_2` 在 ENA inventory 中列出（含官方字节数与 MD5），但官方 FTP/HTTP URL 返回 802 字节的 `Index of` 目录占位符页面而非文件，断点续传收到 416 且无法取得；与 R71 的 `SRR21428958_2` 同款缺陷。当前 `sra/` 落盘口径按“inventory 全量减缺失对象”如实记录，4 个对象合计 457,383,196 bytes。下一步：向 ENA 报告并等待上游修复或补发。关闭条件：ENA 恢复对象后补取并通过字节数与 MD5 校验。该事项不阻塞已发布部分的验收结论，`--require-sra` 按跳过口径通过。
- `Q02`（最近更新：2026-09-28；未取得）：论文正式发表版 PDF 未归档。已核实 `academic.oup.com` 的 article-pdf 端点在本次出口返回 Cloudflare 拦截页（带浏览器 User-Agent 仍为 HTTP 403），Europe PMC 的 PDF 端点返回 403／404，PMC 网页版 PDF 路径返回挑战页。当前以同一 PMCID 的 Europe PMC 全文 XML 作为解释基准，书目字段与 DOI 元数据已交叉核对。下一步：待出口可达或取得作者／机构托管副本时归档并与 XML 版本比对。关闭条件：归档一份身份可核验的正式版 PDF。
- `Q03`（最近更新：2026-09-28；未决，不阻塞发布）：上游未特别说明覆盖仓库数据的许可。已核实固定 tree 内无任何许可文件，GitHub 元数据接口本次因限流未能读取。当前按“使用与再分发范围不明确”处理，正文分层说明各对象许可。下一步：向作者或出版方确认仓库数据许可。关闭条件：取得覆盖数据的明确许可声明，或来源方书面说明。对本次接入发布不构成阻塞，但商用、衍生和再分发授权仍不明确。
- `Q04`（最近更新：2026-09-28；未决）：`File_Details.csv` 与实际文件不一致。索引表把 ACE2 的表列为 `XABA_ACE2_rep_c_phenotype_data.csv`，而固定 tree 内的实际文件是 `XABA_ACE2_rep_d_phenotype_data.csv`；`rep_c` 不在 tree 内，`rep_d` 未被索引表列出。影响：以 `File_Details.csv` 为索引的程序会找不到文件。当前保留原始文件名与原始索引内容，未做改写。下一步：向作者确认是索引笔误还是 `rep_c` 未发布。关闭条件：来源方澄清，或在取得 `rep_c` 后补入。
- `Q05`（最近更新：2026-09-28；未决）：处理脚本引用但未随仓库发布的中间产物。`20250127_ABBA_exp_loaded.R` 输出 `ABBA_i` 与 `ABBA_j` 表达表，`20241224_XABA_reloaded.R` 读入 `XAB_inferred_phenos_ace2_d_20250216.csv`，两者都不在固定 tree 内。影响：Library B 的表达表与 Library C ACE2 的第二个重复无法在本地复算。当前以已发布的 `ABBA_a`–`ABBA_h` 与 `XABA_ACE2_rep_d` 为准。下一步：确认这些文件是否属于公开范围。关闭条件：文件发布，或来源方确认不在公开范围并说明理由。
- `Q06`（最近更新：2026-09-28；未决）：Library M 抗体表 a 组与 b 组的关系未被随附脚本说明。两个处理脚本分别把 `sort` 置为 `a` 与 `b`，却都写出 `MABAb_` 前缀的文件；发布表中 a 组与 b 组并存，两组的位点列数不同（39 与 33），组内 `sort` 列取值为 `a` 或 `NA`，`File_Details.csv` 又把两组都记为 `Replicate = 1`。影响：不能确定两组是同一测定的两次重复、还是两种不同分选方向的独立结果，进而影响重复性与可合并性的判断。当前按两组分别保留，不合并、不互为重复。下一步：向作者确认 a/b 的分组依据。关闭条件：来源方给出两组的定义。
