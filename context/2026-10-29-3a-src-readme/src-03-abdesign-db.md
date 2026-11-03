---
- tags:
  - context
---

# SRC_R03_ABDESIGN_DB 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
  - [AbDesign 新实验如何形成](#abdesign-新实验如何形成)
  - [外部突变子集如何并入](#外部突变子集如何并入)
  - [公开产物、标签与解释边界](#公开产物标签与解释边界)
- [论文原文](#论文原文)
  - [bioRxiv 预印本 v1](#biorxiv-预印本-v1)
  - [mAbs 正式发表版](#mabs-正式发表版)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [突变与野生型数据表](#突变与野生型数据表)
  - [结构归档](#结构归档)
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

- `source_id`：`SRC_R03_ABDESIGN_DB`
- `source_version`：`snapshot-2025-08-26`
- 原作者或发布机构：NaturalAntibody / NATURALANTIBODY S.A.（Bartosz Janusz 等研究者）

### 来源方背景

NaturalAntibody 是由计算抗体研究者 Konrad Krawczyk 创办的波兰公司。[波兰国家法院登记册当前摘录](https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/0000887528?rejestr=P&format=json)（摘录生成于 2026-09-24，登记状态截至 2026-09-03）显示，现有法律主体 `NATURALANTIBODY SPÓŁKA AKCYJNA` 于 2021-03-08 登记，KRS 编号为 `0000887528`，注册地在什切青，并设克拉科夫分支；[公司联系页面](https://naturalantibody.com/contact-us/)同样列出什切青总部和克拉科夫研发部门。[公司介绍](https://naturalantibody.com/about-us/)列明创始人及其计算抗体研究背景。`S.A.`（股份公司）是法律形式，不能据此判断是否上市；截至本次核验，尚未取得能够确认其上市状态的公司或交易所一手披露，因此此处不将其表述为上市或未上市公司。

公司业务围绕抗体数据的收集、生成和分析展开。[平台介绍](https://www.naturalantibody.com/research/)将其工作分为抗体数据资源、机器学习模型和分析平台，平台提供数据库检索、序列工程与结构建模等功能。公司还建设了整合抗体—抗原相互作用的 [ASD DB](https://www.naturalantibody.com/asd/)，官方 2.0 版说明其汇集 29 个公开来源。截至 2026-09-24，[数据资源目录](https://www.naturalantibody.com/antibody-data/)把 AbDesign DB 与后续 AbDesign 2.0 分别列为两个资源；本 source 对应 Janusz 等人论文关联的原始 AbDesign DB，不包含 AbDesign 2.0。

## 实验设计和数据口径

### AbDesign 新实验如何形成

AbDesign 新实验以 7 个抗原为对象；每个抗原分别选择 2 种具有公开复合物结构的不同亲本抗体，共形成 14 个亲本抗体—抗原体系。研究对象是在这些已知抗体背景中做 CDR-H3 单点突变，不是从抗原出发重新设计完整抗体。作者先根据每个亲本抗体—抗原 PDB 复合物的原子坐标，逐一计算 CDR-H3 与抗原的重原子（即非氢原子）间距离。只要某个 CDR-H3 残基的任一重原子与抗原任一重原子的距离小于 4.5 Å，就将该残基列为候选突变位点。随后，作者按每个抗原最多安排 96 个抗体构建体的实验容量选择样本：在该抗原对应的两个亲本抗体中选择 94 个单点突变，并保留 2 个 WT 亲本对照；选择突变时尽量均匀覆盖候选位点和替换氨基酸。7 个抗原合计为 658 个单点突变和 14 个 WT 对照，即论文所说的 672 个 variants。

论文方法把 cysteine 列为采样时要排除或避免的替换，但这不是公开文件中的绝对过滤条件：658 条 AbDesign 记录中仍有 5 条 `new_residue=C`。因此应把论文表述理解为总体设计偏好，逐条分析以发布表为准。

作者把各亲本抗体的 VH/VL 插入双顺反子表达载体；该载体同时用于表达重链和轻链，并分别补上人 IgG1 重链恒定区和人 κ 轻链恒定区。载体转入 CHO 细胞后，细胞在 96 孔深孔板中培养并产生完整抗体，作者再从培养上清中将其纯化。

结合测量采用统一的 ELISA（酶联免疫吸附测定）流程，并使用另一类 96 孔测量板。作者先以 1 µg/mL 抗原包被板孔，使抗原固定在孔内表面；完成封闭后，加入从 1 µg/mL 起始的四倍系列稀释抗体，即后一档浓度为前一档的四分之一。孵育并洗去未结合的抗体后，加入识别人 IgG Fc 的二抗和 TMB 显色底物，最后读取 450 nm 吸光度。留在孔内的抗体越多，通常产生的吸光信号越强，因此该读数可以反映当前实验条件下保留的相对结合信号。前述每个抗原安排的 96 个是抗体构建体数量；进入 ELISA 后，每个构建体还会按浓度梯度占用多个测量孔。

作者以同板相应 WT 作为参照，将某一浓度下突变体的 ELISA 读数除以 WT 读数，形成公开的 binding-retainment ratio。数值越大，表示突变体相对 WT 保留的 ELISA 结合信号越多。在同一比较浓度、包被和检测条件一致且信号未饱和时，较大的 ratio 通常提示突变体的结合表现更好，并可能对应更小的 `KD`（即更高的亲和力）。不过，ELISA 吸光度还会受到抗体有效浓度、抗原包被状态和最大结合信号等因素影响，因此不能用 ratio 直接换算 `KD` 或确定亲和力改变幅度。公开材料也没有说明 CSV 中单个标量具体采用哪个浓度。

| 抗原 | 亲本 PDB | AbDesign 突变数 |
| --- | --- | ---: |
| PD-1 | `5GGS` / `6XKR` | 51 / 43 |
| CTLA-4 | `6RP8` / `5GGV` | 28 / 66 |
| SIRPα | `6NMS` / `6NMU` | 48 / 46 |
| VEGF | `7KF0` / `1BJ1` | 36 / 58 |
| gp120 | `6MFP` / `5F9W` | 36 / 58 |
| lysozyme | `1BVK` / `2YSS` | 38 / 56 |
| SARS-CoV-2 RBD | `7BEJ` / `7JMO` | 34 / 60 |

### 外部突变子集如何并入

SKEMPIv2 和 AB-Bind 是对既有文献实验的汇编。由于原始研究的目的各不相同，上游数据既有每个变体只改一个氨基酸的单点突变，也有同一变体同时改变多个位点的多点突变。多点突变记录的 `ΔΔG` 对应整个突变组合相对 WT 的结合变化，不能直接拆成各个位点的独立效应。

这些外部记录不是上述 672 个统一 ELISA 实验的后续阶段，也没有由 NaturalAntibody 重新测量。为与 AbDesign 新实验的单点突变记录保持相同粒度，作者从两个汇编中筛出同时具有完整重链、轻链和抗原的抗体—抗原复合物，再保留抗体侧单点突变，并在各来源内部去重。论文说明，重复记录优先保留信息更完整、测量方法更精细或温度更低的条目。最终发布的 `datasets_mut.csv` 中，SKEMPIv2 为 377 条、AB-Bind 为 268 条，全部是单点突变；它们的实验方法来自不同研究，包括 SPR、ELISA、ITC、KinExA 等。

正式论文表 4 同时报告了外部数据库在“已限定为抗体侧变体、但尚未排除多点突变”时的更大统计口径。它与当前 CSV 的关系如下，其中多点突变数由论文的全部变体数减去单点突变数得到：

| 外部来源 | 论文表 4 的全部抗体侧变体 | 进入当前 CSV 的单点突变 | 未进入当前 CSV 的多点突变 |
| --- | ---: | ---: | ---: |
| SKEMPIv2 | 571 | 377 | 194 |
| AB-Bind | 351 | 268 | 83 |

因此，571 和 351 用于描述论文曾比较的上游范围，不是 `datasets_mut.csv` 的应有行数；当前 CSV 没有多点突变记录。相应地，论文按全部抗体侧变体统计的 SKEMPIv2 34 个和 AB-Bind 13 个 PDB，与当前单点突变表对应的 31 个和 12 个 PDB 不是同一统计口径。

### 公开产物、标签与解释边界

三条数据支路及其公开产物可概括为：

```text
AbDesign 新实验
14 个 WT 亲本 ── 接触位点选取 ──> 658 个 CDR-H3 单点突变
      └── 7 个抗原 ×（94 个突变 + 2 个 WT 对照）──> 672 个实验对象
          └── 公开 658 个 mutant/WT ELISA ratio；WT 原始读数未单独发布

SKEMPIv2 上游汇编 ── 筛选、来源内去重 ──> 377 个单点突变 ΔΔG
AB-Bind 上游汇编 ── 筛选、来源内去重 ──> 268 个单点突变 ΔΔG

三类记录 ── 统一序列、编号和结构处理
          ├── datasets_mut.csv：1,303 条突变结果记录
          ├── datasets_wt.csv：57 条来源内亲本参照记录（47 个唯一 PDB）
          └── abdesign.tar.gz：每条突变和 WT 各 7 套结构表示
```

`datasets_wt.csv` 的 14 条 AbDesign 记录只能标识 14 个亲本的序列和结构参照；该表没有 `affinity`，不能据此恢复论文所说的 14 个 WT ELISA 测量。公开数值是 `datasets_mut.csv` 中 658 个已经归一化的 ratio。

AbDesign 的 `affinity` 是连续的 binding-retainment ratio，当前范围为 0.01420615062 至 1.368466153：接近 1 表示相对 WT 的 ELISA 表现相近，趋近 0 表示结合信号明显降低，`>1` 表示相对信号更强。它不是 KD、Ka、绝对结合自由能或严格的亲和力常数。发布包没有给出固定的 binder/non-binder 标签或金标准阈值；论文也指出多数系统没有清楚的二类分界，只在不同分析中考察 `1`、`0.9` 等阈值，并把趋近 0 的值视为可能不结合。因此，`ratio < 1` 只表示弱于 WT，不能自动标为 non-binder，跨抗原或亲本体系比较也需要额外校准。

SKEMPIv2 和 AB-Bind 的 `affinity_type=ddg`，论文口径为 `ΔΔG = ΔG_mutant - ΔG_wild-type`，正值表示突变后结合变弱，负值表示结合增强。它同样是连续的相对变化量，不是二元 binder 标签；而且这些值汇编自异质实验。其方向、单位和生成过程都不同于 AbDesign ELISA ratio，建模时必须按 `dataset` 与 `affinity_type` 分层，不能直接拼成一个统一回归标签。

虽然实验采用四倍系列稀释，当前 CSV 为每个突变只保留一个 ratio，没有公开各浓度的逐点吸光度、选取哪个浓度形成该标量、是否由整条稀释曲线汇总，以及实验重复数、误差或不确定度。当前 source 因而只能作为作者整理后的 `processed-public` 结果包使用，不能由公开文件重算或独立审计这些 ratio。

## 论文原文

### bioRxiv 预印本 v1

- 标题：*AbDesign: database of point mutants of antibodies with associated structures reveals poor generalization of binding predictions from machine learning models*
- 作者：Bartosz Janusz et al.
- 发表来源：bioRxiv
- 归档文本版本：预印本 v1
- 发布日期：2025-06-13
- DOI：`10.1101/2025.06.09.658639`
- PMID / PMCID：无
- 本地文件：`articles/AbDesign_2025-06-13_bioRxiv-v1.pdf`
- 文件大小：5.36 MiB（5,622,690 bytes）
- SHA-256：`10d29fbb9a0f17722be679118541dc206ebc08a6df4febf0a7bf70630e7a9934`
- 文本许可：CC BY 4.0
- 补充材料：无独立 bioRxiv 补充文件

归档文件名采用 bioRxiv v1 的发布日期 `2025-06-13`；DOI 中的 `2025.06.09` 保留为论文标识的一部分。

### mAbs 正式发表版

- 标题：*AbDesign: database of point mutants of antibodies with associated structures reveals poor generalization of binding predictions from machine learning models*
- 作者：Bartosz Janusz et al.
- 发表来源：mAbs 17(1):2567319
- 归档文本版本：正式发表版（Version of Record；PMC 开放存档）
- 发布日期：2025-10-08
- DOI：`10.1080/19420862.2025.2567319`
- PMID / PMCID：`41058476` / `PMC12520099`
- 本地文件：`articles/AbDesign_2025-10-08_mAbs-Version-of-Record.pdf`
- 文件大小：7.44 MiB（7,805,490 bytes）
- SHA-256：`960327c199428ff8b30b2310d76858a394d3eff51ad6c51406e466a4b2007b5c`
- 文本许可：CC BY-NC 4.0
- 补充材料：`articles/AbDesign_2025-10-08_mAbs-supplement.pdf`，336.81 KiB（344,896 bytes），SHA-256 `f7eadb1c29bd23b0a9ff75cf52fc78b879f37b12ad55d97d21b8fa23617aa697`；同时保留 Europe PMC `supplementaryFiles` 接口返回的 `articles/AbDesign_2025-10-08_mAbs-supplementaryFiles.zip`，3.44 MiB（3,605,465 bytes），SHA-256 `d533f4442502811dcf561b2be47556f66ea921e460d689feb23bed1d3f8fa94e`
- 引用数（查询快照）：8（[OpenAlex W4414948154](https://openalex.org/W4414948154)，查询于 2026-09-24）

这份 ZIP 的 51 个成员并不代表 51 份补充材料。真正独立的补充文档只有 11 页的 `KMAB_A_2567319_SM1820.pdf`，内容包括 Supplementary Figures 1–3 和 Supplementary Tables 1–5；项目将其原样改名为上述补充 PDF。其余 50 个成员是正式论文的网页渲染资源：12 个正文图号各有 `_OC`、`_PB` 两个 JPG 和同名 GIF 版本，共 48 个文件，另有 2 个公式 JPG。保留 ZIP 是为了保存 Europe PMC 接口的原始返回包，而不是把这些渲染图片计作额外补充数据。

当前 `snapshot-2025-08-26` 记录的是上游文件在 2025-08-26 的状态；mAbs 正式论文则于 2025-10-08 发表。为完整解释这批数据，本地 `articles/` 同时归档了 bioRxiv v1 主文、后来发表的 mAbs 正式主文及其补充 PDF。正式论文用于补充解释并核对方法和统计口径；预印本与正式版表述不同时，以正式版为准，但数据版本仍保持为 `snapshot-2025-08-26`。OpenAlex 将预印本和正式版记录为不同 work；上述引用快照只取正式发表版，不与预印本相加。

## 仓库内容

上游通过 NaturalAntibody 官方页面和 Google Drive 文件夹发布六个对象，没有 release、不可变 record version 或版本号。`snapshot-2025-08-26` 取自主归档 `abdesign.tar.gz` 下载响应的 `Last-Modified: 2025-08-26`，不是本项目下载日期。Drive 对象仍可能被原位替换，因此当前 README 记录字节数与 SHA-256，快照名不应解释为上游正式版本。

```text
snapshot-2025-08-26/
└── AbDesign/
    ├── README.md
    ├── LICENSE.txt
    ├── abdesign.tar.gz
    ├── datasets_mut.csv
    ├── datasets_wt.csv
    └── datasets_wt.xlsx
```

`AbDesign/` 保留官方 Drive 文件夹的真实名称，六个对象保持原始文件名。主归档未在 raw 层展开，避免同时保存 807 MB 压缩包和约 3.71 GB 解包副本；下游应解包到工作目录或按需流式读取。

## 数据结构

### 突变与野生型数据表

| `dataset` | `datasets_mut.csv` | `datasets_wt.csv` | 标签类型 |
| --- | ---: | ---: | --- |
| `AbDesign` | 658 | 14 | `elisa_mut_to_wt_ratio` |
| `SKEMPIv2` | 377 | 31 | `ddg` |
| `AB-Bind` | 268 | 12 | `ddg` |
| 合计 | 1,303 | 57 | 不可混为同一数值口径 |

`datasets_mut.csv` 的 1,303 行是按 `dataset` 保留的来源记录；同一个突变可能被多个来源收录，因此不能把这些行直接视为 1,303 个彼此独立的突变。为识别跨来源重合，本文用亲本 PDB、重/轻链可变区序列、抗原序列、突变链、WT IMGT 位点以及突变前后氨基酸共同定义“处理后突变键”，对应的原始字段为 `pdb_name`、`heavy_sequence_variable`、`light_sequence_variable`、`antigen_sequence`、`mutation_chain_id`、`mutation_pos_imgt_wt`、`orig_residue` 和 `new_residue`。

按这一口径，1,303 行对应 1,156 个不同的键，其中有 147 个键跨来源重复：146 个同时出现在 SKEMPIv2 和 AB-Bind，1 个同时出现在 AbDesign 和 SKEMPIv2。这里的“重复”只表示公开字段指向相同的亲本序列背景和单点突变，不代表两个来源一定分别进行了独立实验。不同来源中的相同键仍可能具有不同的 `method`、`affinity` 和 `original_id`，因此不能仅凭键相同就删除其中一行。

正式补充材料报告 SKEMPIv2 与 AB-Bind 共有 46 个 single-point mutants，少于上述 146 个处理后键；公开材料没有给出其 overlap 匹配代码，可能涉及原始链编号、原始突变字符串或其他定义差异。因此，1,156 只作为当前表字段下的去重审计数，不替代论文口径，也不应当作新的官方样本数。

三个子集的 57 条 WT 行覆盖 47 个唯一 PDB ID；WT 行同样按 `dataset` 分开保留，所以同一个 PDB 可以出现于多个来源。每条突变记录的 `pdb_name` 都能在相应来源的 WT 表中找到。两张 CSV 第一列列名为空，是上游序列化 index。突变表另有 `index`，它只在各 `dataset` 子集内唯一并会跨子集重复；定位记录至少使用 `dataset + index`，连接结构时再带 `pdb_name` 和突变字段。`original_id` 也不是全局主键：AbDesign 的 658 行为空，AB-Bind 还有 2 个 `original_id` 各自对应两条不同的处理后突变记录。

`datasets_wt.xlsx` 有两个 sheet。`datasets_wt` 为 57 行、25 列，与 `datasets_wt.csv` 逐单元格一致；`Sheet1` 为 14 行、24 列，等于 WT 表中的 AbDesign 14 行去掉首个序列化 index 列。未发现公式。

所有 1,303 条突变记录都提供结构条目中的抗原、重链、轻链序列，以及重/轻链可变区和六个 CDR 字段。这些序列与作者处理的 PDB 结构相对应；它们不是实验表达载体的完整序列，也不能自动解释为天然蛋白、临床抗体或完整 IgG1/κ 构建体。特别是，论文所述表达载体中的完整恒定区和质粒序列没有在两张表中逐构建体发布。

### 结构归档

`abdesign.tar.gz` 有 9,591 个成员，其中 9,524 个文件、67 个目录和 9,520 个 PDB；解包文件总计 3.45 GiB（3,705,989,265 bytes）。归档没有绝对路径、`..` 路径或重复成员名。归档内 `abdesign/datasets_mut.csv`、`abdesign/datasets_wt.csv` 和 `abdesign/README.md` 分别和外置同名文件逐字节一致。

结构层包括 `wt/pdbs_cleaned/` 的亲本晶体结构清理副本，以及 ABodyBuilder2 建模、framework 对齐、OpenMM 精修、可变区裁剪和侧链构象替换等派生表示。清理结构已统一链 ID、去除 altloc 和氢原子，不是未经处理的 PDB 原始下载；所有突变体结构都是计算模型或侧链替换产物，不是实验解析结构。

| 子集 | 突变记录 | 每条突变的结构表示 | WT 复合物 | 每个 WT 的结构表示 | PDB 总数 |
| --- | ---: | ---: | ---: | ---: | ---: |
| AbDesign | 658 | 7 | 14 | 7 | 4,704 |
| SKEMPIv2 | 377 | 7 | 31 | 7 | 2,856 |
| AB-Bind | 268 | 7 | 12 | 7 | 1,960 |
| 合计 | 1,303 | - | 57 | - | 9,520 |

每个子集的七套突变结构使用两种文件名连接方式。以下相对目录均位于 `abdesign/<dataset>/` 下，三类 `dataset` 的规则相同：

| CSV 连接字段 | 对应的突变结构目录 |
| --- | --- |
| `mutated_pdb_name` | `abb2/mutated/pdbs_aligned/`、`abb2/mutated/pdbs_aligned_refined/`、`conformation/mutated/pdbs_mutated/`、`conformation/mutated/pdbs_mutated_refined/` |
| `mutated_pdb_name_imgt` | `abb2/mutated/pdbs_modelled/`、`abb2/mutated/pdbs_aligned_refined_variable/`、`conformation/mutated/pdbs_mutated_refined_variable/` |

上述 21 个突变结构目录均已逐目录核对，文件名集合分别与相应 CSV 字段完全一致；另外 21 个 WT 结构目录以 `pdb_name + ".pdb"` 命名。这样，三类子集共形成 42 个 PDB 目录。

同一突变的七个结构表示高度相关，不是七个独立样本。训练、验证和测试至少应跨 `dataset` 先检查处理后突变键，再按亲本 `pdb_name` 或抗原系统分组，避免同一突变、亲本或近重复结构跨 split。

### 字段说明

以下覆盖突变表 38 列及 WT 表 25 列；两表第一列表头都是空字符串。CSV 中的数字、字典和序列均以文本存储；突变表仅 `original_id` 在 658 条 AbDesign 行为空，其他字段没有空单元格。

| 文件 | 原始字段 | 表示、单位与来源 | 缺失及特殊编码 |
| --- | --- | --- | --- |
| 两表 | 空表头列、`dataset`、`pdb_name` | 上游序列化索引、子集名称和亲本 PDB ID；作者整理的记录与结构连接键 | 无空值；空表头是原始列名，不应删除 |
| 突变表 | `index`、`original_id` | 子集内整数索引及原始来源标识；作者整理的字段 | `index` 跨子集重复；`original_id` 在 AbDesign 的 658 行为空，AB-Bind 有 2 个值各重复两次，均不能单独作全局主键 |
| 突变表 | `method`、`affinity`、`affinity_type` | 测定方法、数值文本及标签类型；AbDesign 为无单位 ELISA WT 归一化比值，SKEMPIv2/AB-Bind 为 kcal/mol 的 ΔΔG | 均无空值；两种标签的方向和量纲不能混用 |
| 突变表 | `mutation_chain_id`、`orig_residue`、`mutation_pos`、`new_residue` | 突变链、原/新氨基酸及原始结构位置；作者提供的单点突变定位 | 均无空值；位置为编号文本，需连同 PDB/链解释 |
| 突变表 | `mutation_pos_imgt`、`mutation_pos_imgt_wt` | 突变体及 WT 的 IMGT 编号文本；项目不将其改写为 PDB 位置 | 均无空值；普通位点为整数文本，插入位点可带字母后缀 |
| 突变表 | `mutated_pdb_name`、`mutated_pdb_name_imgt` | 普通编号和 IMGT 编号的归档内突变结构文件名；模型/处理产物连接键 | 均无空值；结构表示不是新增独立实验 |
| 两表 | `orig_antigen_chain_id`、`orig_heavy_chain_id`、`orig_light_chain_id` | 亲本结构的抗原、重链、轻链 ID；作者整理的结构映射 | 均无空值；链编号须与相应 PDB 条目及清理结构核对 |
| 两表 | `antigen_sequence`、`heavy_sequence`、`light_sequence` | PDB 结构条目中的抗原、重链、轻链氨基酸序列；作者处理后的表格字段 | 均无空值；不等于实验载体的完整 IgG1/κ 构建体序列 |
| 两表 | `heavy_sequence_variable`、`light_sequence_variable` | 重/轻链可变区氨基酸序列；从构建体序列截取的上游字段 | 均无空值 |
| 两表 | `heavy_cdr1`、`heavy_cdr2`、`heavy_cdr3`、`light_cdr1`、`light_cdr2`、`light_cdr3` | 六个 CDR 氨基酸片段；上游划分 | 均无空值；编号依其 IMGT 映射理解 |
| 两表 | `heavy_variable_start`、`heavy_variable_end`、`light_variable_start`、`light_variable_end` | 可变区在对应完整链序列中的零基边界；上游结构处理字段 | 均无空值；除 3 条 WT 轻链记录外，可用 Python 左闭右开切片 `[start:end]` 还原可变区，例外见 `Q04` |
| 突变表 | `heavy_imgt_to_residue_mapping`、`light_imgt_to_residue_mapping` | 字符串化 IMGT 到残基映射；作者处理的突变体字段 | 均无空值；与 WT 表的列名不同 |
| WT 表 | `heavy_imgt_residue_mapping`、`light_imgt_residue_mapping` | 字符串化 IMGT 到残基映射；作者处理的亲本字段 | 均无空值；与突变表的列名不同 |
| 两表 | `heavy_positional_imgt_mapping`、`light_positional_imgt_mapping` | 字符串化“完整链零基位置 → IMGT 编号”映射；字典键从相应 `variable_start` 开始，不是在可变区内重新从 0 编号 | 均无空值；解析时保留原字符串；突变表和 WT 表的插入位点写法不同，见下文 |

IMGT 插入位点在两类表中采用等价但不同的文本约定。突变表的 `mutation_pos_imgt`、`mutation_pos_imgt_wt` 和 positional mapping 使用字母后缀，例如 `112A`、`112B`；WT positional mapping 使用小数后缀，例如 `112.1`、`112.2`。当前有 91 条突变记录的 `mutation_pos_imgt_wt` 使用字母后缀；连接 WT 映射时应先按 `112A ↔ 112.1`、`112B ↔ 112.2` 的规则统一表示，不能直接比较原始字符串。两张表中的原始值均保持不变。

低基数分类字段的原始取值按字段分组列在下面，避免在同一张表中反复显示相同的文件名和字段名。`dataset`、`method`、`affinity_type`、`mutation_chain_id` 及氨基酸字段的取值范围均由上游 `AbDesign/README.md` 定义；记录数来自当前 `snapshot-2025-08-26` 两张 CSV 的实际扫描，不代表未来版本一定保持相同分布。

**`dataset`（两张 CSV）**

| 原始取值 | 当前记录数 | 含义 |
| --- | ---: | --- |
| `AbDesign` | 突变 658；WT 14 | 本研究新测的统一 ELISA 子集 |
| `SKEMPIv2` | 突变 377；WT 31 | 从 SKEMPIv2 筛出的抗体侧单点突变子集 |
| `AB-Bind` | 突变 268；WT 12 | 从 AB-Bind 筛出的抗体侧单点突变子集 |

**`method`（突变表）**

| 原始取值 | 当前记录数 | 含义 |
| --- | ---: | --- |
| `ELISA` | 772 | 酶联免疫吸附测定；同时出现于 AbDesign 和外部汇编记录 |
| `SPR` | 273 | 表面等离子体共振 |
| `FL` | 40 | 荧光法（fluorescence） |
| `ITC` | 35 | 等温滴定量热法 |
| `SP` | 17 | 光谱法（spectroscopy） |
| `KinExA` | 38 | kinetic exclusion assay |
| `Yeast Disp. Flow Cyt` | 35 | 酵母表面展示结合流式细胞术分析 |
| `Phage ELISA` | 68 | 噬菌体展示 ELISA |
| `Enzymatic 1` | 17 | AB-Bind 保留的酶学测定子类别 1；当前包未展开 1/2 的具体划分规则 |
| `Enzymatic 2` | 8 | AB-Bind 保留的酶学测定子类别 2；当前包未展开 1/2 的具体划分规则 |

**`affinity_type`（突变表）**

| 原始取值 | 当前记录数 | 含义 |
| --- | ---: | --- |
| `elisa_mut_to_wt_ratio` | 658 | AbDesign 突变体相对同板 WT 的 ELISA 归一化比值，无单位 |
| `ddg` | 645 | 外部子集的 `ΔΔG = ΔG_mutant - ΔG_wild-type`，单位为 kcal/mol |

**`mutation_chain_id`（突变表）**

| 原始取值 | 当前记录数 | 含义 |
| --- | ---: | --- |
| `H` | 1,070 | 突变位于抗体重链 |
| `L` | 233 | 突变位于抗体轻链 |

**`orig_residue`、`new_residue`（突变表）**

| 当前观察到的原始取值 | 当前记录数 | 含义 |
| --- | ---: | --- |
| `A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y` | 两字段各 1,303 个非空值，均覆盖 20 种 | 标准氨基酸一字母代码，分别表示突变前和突变后残基 |

`pdb_name`、三个 `orig_*_chain_id`、`original_id`、结构文件名和序列不是枚举字段，而是结构、记录或内容标识；即使某些字段在当前快照中的唯一值不多，也应按连接键或标识符解释，不把当前集合外推为封闭的全部可能值。

WT 表没有 `affinity`，它保存各突变的亲本结构与序列参照；`datasets_wt.xlsx` 的两个 sheet 与 `datasets_wt.csv` 是同一批记录的不同交付表示，字段由上述 WT 表说明覆盖。

### 数据示例

`datasets_mut.csv` 首条真实记录的核心字段为：

```text
dataset=AbDesign,pdb_name=1BJ1,method=ELISA,affinity=0.8856053098,affinity_type=elisa_mut_to_wt_ratio
mutation_chain_id=H,orig_residue=H,mutation_pos=101,mutation_pos_imgt=109,new_residue=Y
mutated_pdb_name=0__1BJ1__H_101_H_Y.pdb,heavy_cdr3=AKYPYYYGSSHWYFDV
```

它是一条相对 WT 的单点突变 ELISA 记录，并通过两个 PDB 文件名字段连接归档内派生结构。

`datasets_wt.csv` 首条真实记录的核心字段为：

```text
dataset=AbDesign,pdb_name=5GGS,orig_antigen_chain_id=Z,orig_heavy_chain_id=A,orig_light_chain_id=B
heavy_cdr3=ARRDYRFDMGFDY,light_cdr3=QHSRDLPLT
```

它是一条 WT 亲本记录，不含 `affinity`，也不是突变样本。

## PDB 数据库

`datasets_wt.csv` 的 57 条 WT 记录覆盖 47 个唯一 `pdb_name`。这是亲本复合物级的直接映射：WT 行通过 `dataset + pdb_name` 连接来源和结构，1,303 条突变记录再通过同一来源内的 `pdb_name` 连接相应亲本；突变记录没有逐条实验结构。项目于 2026-09-17 从 RCSB 获取 47 份完整 mmCIF，并生成以 RCSB canonical polymer entity 序列为正文的选链 FASTA；2026-09-22 又逐链复核并纠正 header，mmCIF 字节未变。RCSB 条目 URL 使用 `https://www.rcsb.org/structure/<PDB ID>`，例如 [1BJ1](https://www.rcsb.org/structure/1BJ1)。

每个 FASTA 恰有抗体重链、轻链和抗原 3 条记录，47 个条目合计 141 条。header 记录项目角色、author chain 和 mmCIF label asym；141 个 label asym 均能在相应 mmCIF 中唯一落到一个 polymer entity。下表汇总这些选链的序列覆盖；polymer entity ID 是各 PDB entry 内的局部编号，精确 entity、author/label chain 和坐标范围以对应 FASTA header 与 mmCIF 为准。

| 角色 | FASTA 记录 | entry 内 entity ID 取值 | canonical 序列长度 | 首个有坐标 `label_seq_id` | 最后一个有坐标 `label_seq_id` | 有坐标残基数 |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| 抗体重链 | 47 | `1` / `2` / `3` | 113–257 aa | 1–4 | 113–231 | 113–227 |
| 抗体轻链 | 47 | `1` / `2` / `3` / `4` | 107–220 aa | 1–4 | 107–220 | 104–220 |
| 抗原 | 47 | `1` / `3` | 76–1,295 aa | 1–83 | 71–1,294 | 68–1,267 |

链角色首先采用 `orig_antigen_chain_id`、`orig_heavy_chain_id` 和 `orig_light_chain_id`。其中 AB-Bind 的 7 个清理结构把抗体统一编号为 `H/L`，项目以 Cα 坐标逐残基匹配到 RCSB author chain；其余选择均由表中 author chain 唯一解析到一个 RCSB polymer entity。7 个跨编号映射为：

| PDB | 清理结构重/轻链 | RCSB author 重/轻链 | Cα 匹配数（重/轻） |
| --- | --- | --- | ---: |
| `1DQJ` | `H/L` | `B/A` | 210 / 214 |
| `1MLC` | `H/L` | `B/A` | 218 / 214 |
| `1N8Z` | `H/L` | `B/A` | 220 / 214 |
| `1VFB` | `H/L` | `B/A` | 116 / 107 |
| `1YY9` | `H/L` | `D/C` | 220 / 211 |
| `2NYY` | `H/L` | `D/C` | 217 / 216 |
| `3BN9` | `H/L` | `F/E` | 224 / 211 |

47 个 PDB ID 为：`1BJ1, 1BVK, 1CZ8, 1DQJ, 1JRH, 1KIP, 1KIQ, 1KIR, 1MHP, 1MLC, 1N8Z, 1NCA, 1NMB, 1VFB, 1XGP, 1XGQ, 1XGR, 1XGT, 1XGU, 1YY9, 2B2X, 2BDN, 2NYY, 2YSS, 3BDY, 3BE1, 3BN9, 3G6D, 3HFM, 3L5X, 3N85, 3NGB, 3SE8, 3SE9, 4I77, 5C6T, 5F9W, 5GGS, 5GGV, 6MFP, 6NMS, 6NMU, 6RP8, 6XKR, 7BEJ, 7JMO, 7KF0`。

这些文件是 47 个亲本条目的外部原始沉积，不是 1,303 个突变体的实验结构。`pdb/` 共 94 个文件、44.06 MiB（46,201,862 bytes）。按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接后的 inventory SHA-256 为 `747060e1293ac36365f4a0d4b5f84a93dacf62c80b21e907975ec43776aa5c99`。未发布独立 PDB manifest。

## 采集过程记录

- 2026-09-17 在 ab02 通过 mihomo `127.0.0.1:17890` 下载。工具、Python 依赖和工作文件均位于 `/data/ab02/yangwuyu`，未把安装内容或数据写入 `/home/yangwuyu`。
- 先按 Drive 文件夹实时 metadata 枚举六个对象。执行时发现研究记录把上游 `README.md` file ID 中的 `KJjB` 误抄为 `KJbB`，已按实时一手 metadata 更正；文件夹真实名称也核实为 `AbDesign`。
- `datasets_wt.xlsx` 是 Google Spreadsheet，使用官方 XLSX export 端点；其余普通对象使用 Drive 下载接口。主归档采用断点续传并在 staging 完成。
- bioRxiv 从 ab02 返回 403，改为本地下载后用 tar over SSH 上传；本地与远端 SHA-256 一致。正式补充 ZIP 从 Europe PMC 取得，并提取、改名补充 PDF。
- CSV、XLSX、tar.gz、ZIP 和 PDF 均做独立解析；六个 Drive 对象的字节数与 SHA-256、归档安全、表格 schema 和结构计数均验收通过。
- staging 验收后原子发布到正式目录，并清理下载 partial、临时 inventory、验证报告和废弃 metadata；需长期保留的身份与完整性事实写入本 README。
- 后续按项目 PDB 硬性要求，以 WT 表的 47 个唯一 PDB ID 补齐 RCSB FASTA 与 mmCIF，并把完整性摘要合入 README。
- 2026-09-22：对 57 份 WT 清理结构与 47 个原始 mmCIF 逐链核对，发现旧配置在同一 polymer entity 有多个同序列副本时默认取排序靠前的 author chain，导致 `3BN9` 的旧 FASTA 将重/轻链指向 `D/C`；Cα 坐标逐残基匹配证实清理结构实际对应 `F/E`。旧下载器还曾把 entity 级 `auth_asym_ids` 与 `asym_ids` 按列表位置配对，这两个集合没有逐位置对应保证，因而另有 8 份 FASTA 的 author/label header 需要纠正。修正后改用 RCSB 逐链 instance API 确认编号，并为 7 个跨编号条目的 14 条抗体链保存坐标证据；canonical 序列正文和 47 份 mmCIF 字节未改变。
- 2026-09-22：对照 bioRxiv v1 的发布日期，将归档 PDF 从 `AbDesign_2025-06-09_bioRxiv-v1.pdf` 改为 `AbDesign_2025-06-13_bioRxiv-v1.pdf`；字节数与 SHA-256 未变。复核两张 CSV 的 38/25 个原始列名和空值表示，补全字段说明。
- 2026-09-24：按数据形成主线重新核对 bioRxiv v1、mAbs 正式主文、补充材料和公开文件；区分 AbDesign 新测 ELISA 与两个外部汇编子集，澄清 658/672、单点/多点突变、WT 参照行、连续标签和七套结构表示的计数关系，并补充 cysteine 实际记录、跨来源处理后突变键及 ELISA 标量复现边界。同日按最新版 README 规范补充来源方版本区分、PDB 映射强度、polymer entity 和序列覆盖摘要，并将重复的数据语义移回对应正文。原始数据、论文和 PDB 文件均未改动。
- 2026-09-24：按波兰国家法院登记册、公司官网及证券市场一手入口补核来源方背景，确认现有法律主体的登记日期、注册地、研发分支和当前产品方向；因没有取得可确认上市状态的一手披露，未从 `S.A.` 法律形式或检索无结果推断上市或未上市。数据文件未改动。
- 2026-09-24：将“论文原文”改为以 bioRxiv v1 和 mAbs 正式发表版为条目主体；正式主文记录 Europe PMC 在线入口和未归档状态，正式版补充 PDF 与原始 ZIP 归入该版本的“补充材料”，不再把补充文件作为独立论文条目。论文与数据文件均未改动。
- 2026-09-24：补齐 mAbs 正式发表版 PDF。收到的发布方原名文件 `KMAB_17_2567319.pdf` 为 22 页、7,805,490 bytes，文件内题名和 DOI 与正式论文一致；其 MD5 `f199b0a117b8a94e3a96e8f4c9f5b62a` 与 PMC AWS 开放数据元数据完全一致。项目在不改变字节的前提下将其改名为 `AbDesign_2025-10-08_mAbs-Version-of-Record.pdf` 并移入 `articles/`，本地 SHA-256 为 `960327c199428ff8b30b2310d76858a394d3eff51ad6c51406e466a4b2007b5c`。同日重新清点 Europe PMC ZIP，确认只有 1 份补充 PDF，其余 50 个成员为正文图和公式的网页渲染资源，并据此修正文档表述。
- 2026-09-24：查询 OpenAlex 正式发表版 work `W4414948154`，记录其引用数快照为 8；预印本为独立 work，未与正式版数字相加。数据文件未改动。
- 2026-09-24：按最新版字段说明规则扫描两张 CSV，逐项补充低基数分类字段和氨基酸字段的来源定义、当前取值及记录数，并明确结构 ID、链 ID 和文件名等标识符不按枚举处理。正式主文和补充材料均已归档并通过完整性验证，本次未发现需要新增跟踪的文件获取缺口。数据文件未改动。
- 2026-09-24：系统复核全部表格、论文、补充材料、结构归档和 PDB 补充。新增固定文件 SHA-256、归档内 WT 表、42 个结构目录文件名映射、IMGT 编号表示、可变区边界、94 个 PDB 文件语义与 inventory，以及 14 条 chain override 的坐标级回归检查；同时重新从 RCSB 获取 47 个条目的当前来源内容并逐文件比对。复核确认现有 PDB FASTA/mmCIF 与当前 RCSB 一致，`3BN9` 仍唯一对应 `F/E`。数据文件未改动；3 条 WT 轻链边界异常转入 `Q04` 跟踪。

## 参考文献

- AbDesign 官方页面：<https://naturalantibody.com/ab-design/>
- 官方 Drive：<https://drive.google.com/drive/folders/1vF568s3Ge-fCQ-8-oAJIEH3BLr3O3k6H>
- 波兰国家法院登记册当前摘录：<https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/0000887528?rejestr=P&format=json>
- mAbs 正式论文：<https://doi.org/10.1080/19420862.2025.2567319>
- bioRxiv v1：<https://www.biorxiv.org/content/10.1101/2025.06.09.658639v1>
- Europe PMC：<https://europepmc.org/article/PMC/12520099>
- SKEMPI 2.0：Jankauskaitė et al., *Bioinformatics* 2019, DOI `10.1093/bioinformatics/bty635`
- AB-Bind：Sirin et al., *Protein Science* 2016, DOI `10.1002/pro.2829`
- RCSB PDB 条目：以 [1BJ1](https://www.rcsb.org/structure/1BJ1) 为 URL 格式，其余 46 个 ID 见“PDB 数据库”；各条目页的 Primary Citation 给出原始结构论文

## 其他

### 完整性与验收

| 文件 | 大小 | SHA-256 |
| --- | ---: | --- |
| `AbDesign/abdesign.tar.gz` | 769.91 MiB（807,308,003 bytes） | `988ef0c28b92efe5c36fa620cb4aa48164bf3d1c78c5752e4159709dba468e32` |
| `AbDesign/datasets_mut.csv` | 8.45 MiB（8,857,834 bytes） | `a7f0c8b8284f5f16d14ab75096c1bd25b2e4eac6a55bcc964bcc5424fbde5f6e` |
| `AbDesign/datasets_wt.csv` | 322.73 KiB（330,478 bytes） | `cad4d7843722f63d911c4fff525c0c3b062c24455577497b8f6ddfcc10de3c51` |
| `AbDesign/datasets_wt.xlsx` | 42.46 KiB（43,475 bytes） | `33c44174fd01efed1d11e3acc40931bc7c70e763bfbd50372b99a7b26db1ed65` |
| `AbDesign/LICENSE.txt` | 18.89 KiB（19,346 bytes） | `3711f963c05d0be80d53e5923308a6dee31b203da23435c9cfb7c7b6e4dd5e19` |
| `AbDesign/README.md` | 6.54 KiB（6,692 bytes） | `49d5fc11bdd078f5430c3aa60259042053f31a8e7530c2b5ec4e849dd0b558be` |

六个 Drive 对象、文章文件、归档成员安全、CSV/XLSX 内容与 94 个 RCSB 文件均已独立验收。`workspace/users/yangwuyu/scripts/validate_r03_abdesign_db.py` 负责固定文件身份、表格、归档、PDB 本地语义和坐标证据检查，并可通过 `--verify-current-rcsb` 调用通用 PDB 工具重新核对当前 RCSB 来源字节；详细执行证据位于 `workspace/users/yangwuyu/context/2026-09-17-r03-abdesign-db-validation.md`。

### 许可和再分发边界

- `AbDesign/LICENSE.txt` 为 CC BY-NC 4.0。官方页面说明非商业实体可作非商业使用；商业实体应联系 NaturalAntibody。
- 包中捆绑的 SKEMPI 和 AB-Bind 数据不由 NaturalAntibody 主张权利，必须分别遵守原始来源条款。当前包未为二者分别附独立许可证；AB-Bind 的公开仓库也没有标准 SPDX 许可证。
- `wt/pdbs_cleaned` 源自 PDB 条目，使用时应保留相应 PDB 引用。模型结构是派生物，不能抹去上游结构出处。
- 文章文本许可与数据包许可分开；bioRxiv 的 CC BY 4.0 不能反向覆盖数据包、SKEMPIv2 或 AB-Bind。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 7 个抗原、14 个亲本复合物 | WT 表 AbDesign 14 行；论文 Table 1 | 已包含 |
| 658 个 CDR-H3 单点突变 | 突变表 AbDesign 658 行 | 已包含 |
| 14 个 WT 对照，与突变合计 672 个实验对象 | WT 表有 14 条亲本参照行，但无 WT `affinity` | 对照身份已包含；WT 原始测量值未发布 |
| 658 个 ELISA WT 归一化 ratio | `affinity_type=elisa_mut_to_wt_ratio` | 已包含作者汇总标量；无二元 binder 标签 |
| 原始逐孔读数、完整曲线、标量生成规则、replicate 和图像 | 六个 Drive 对象和主归档中未发现 | 未包含 |
| 亲本实验结构 | 上游清理副本和 47 个 RCSB 补充条目 | 已包含 |
| 每个突变的实验晶体结构 | 论文说明突变结构由建模或构象替换生成 | 未包含 |
| SKEMPIv2 / AB-Bind 抗体侧单点突变子集 | 377 / 268 条 `ddg` 记录和对应结构层 | 已包含处理子集；不含论文统计的多点突变，权利另行追溯 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-24；待权利方说明）：AbDesign 包的 `LICENSE.txt` 使用 CC BY-NC 4.0，并说明商业实体需联系 NaturalAntibody；捆绑的 SKEMPIv2、AB-Bind 子集还需分别追溯原来源权利。已核对本地许可证、上游包构成和当前官方页面，当前仅按公开材料保留内部审阅范围，未将整个混合包视为统一可商用数据。若拟用于公司模型训练或对外分发，下一步取得 NaturalAntibody 及相关原始来源对具体用途的书面许可或明确条款，再更新使用边界。
- `Q02`（最近更新：2026-09-24；待方法细节）：正式论文说明抗体做四倍系列稀释、每个测量以同板 WT 吸光度归一化，结果段又称 binding-retainment ratio 来自某一浓度下的 WT 与 mutant 读数；公开 CSV 每个突变只给一个 ratio，未说明对应浓度、曲线汇总方式、replicate 数或不确定度。该缺口影响 ratio 的独立复算、噪声评估和阈值选择。当前保留作者连续值，不自行补二元 binder 标签；下一步向作者索取标量计算规则及重复实验信息。
- `Q03`（最近更新：2026-09-24；待 overlap 定义）：正式补充材料报告 SKEMPIv2 与 AB-Bind 共享 46 个 single-point mutants；按当前 CSV 的 PDB、三条链序列、WT IMGT 位点和氨基酸替换组成处理后键，可得到 146 个跨两来源重复键。已确认这些键的结构序列相同，但两来源的原始编号、方法和数值可不同。差异影响跨来源去重和数据划分；当前保留 `dataset` 维度，并在 split 前按处理后键排查泄漏。下一步核对作者 overlap 脚本或取得其匹配字段定义，再决定是否能建立一一映射。
- `Q04`（最近更新：2026-09-24；待上游字段定义）：绝大多数可变区可由完整链序列按 Python 左闭右开切片 `[start:end]` 还原，但 `datasets_wt.csv` 中 SKEMPIv2 `3NGB`、SKEMPIv2 `3SE8` 和 AB-Bind `3NGB` 的 `light_variable_end` 分别为 98、101、98；这三行只有使用包含终点的 `[start:end+1]` 才与长度为 99、102、99 的 `light_sequence_variable` 一致。相应突变记录使用 99、102、99，符合左闭右开口径。当前保留上游原值，并在验证脚本中固定检测这三条例外；在作者说明其为包含式边界还是行级 off-by-one 之前，下游应优先使用已发布的 `light_sequence_variable`，不要仅靠这三行的 end 字段重新截取。
