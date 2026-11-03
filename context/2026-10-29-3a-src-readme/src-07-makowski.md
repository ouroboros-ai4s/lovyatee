# SRC_R07_MAKOWSKI 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [Library 二元标签](#library-二元标签)
  - [scFab 连续测量](#scfab-连续测量)
  - [IgG 连续测量](#igg-连续测量)
  - [模型输入和派生产物](#模型输入和派生产物)
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

- `source_id`：`SRC_R07_MAKOWSKI`
- `source_version`：`snapshot-2022-06-24`
- 原作者或发布机构：University of Michigan Tessier Lab（Emily K. Makowski 等）

### 来源方背景

[University of Michigan 的 Tessier Lab](https://tessier.lab.medicine.umich.edu/)研究治疗性抗体的发现、工程化、表征与递送，长期结合实验筛选和计算方法优化抗体性质。[课题组论文列表](https://tessier.lab.medicine.umich.edu/publications)包括抗体非特异性结合、自缔合、可开发性和机器学习设计方面的研究。负责人 Peter M. Tessier 的[官方履历](https://tessier.lab.medicine.umich.edu/tessier)记载，他于 2018 年当选美国医学与生物工程学会（AIMBE）会士，并曾获美国化学会 2015 年 Biochemical Technology Young Investigator Award；Emily K. Makowski 等人的 MET 抗体研究出自这一团队。

## 实验设计和数据口径

研究以临床阶段抗 MET/HGFR 抗体 emibetuzumab 为亲本，在重链 CDR 的 8 个位置构建酵母展示 single-chain Fab（scFab）文库。位置包括 HCDR1 的 Y33、HCDR2 的 R50/R54/R55/G56 和 HCDR3 的 A95/W97/Y102；每个位点采样野生型及 5 个旨在降低非特异性结合的替换，理论多样性约 170 万。

文库先经两轮 HGFR-Fc 磁珠筛选，再用流式分选获得高抗原结合、高或低非特异性结合群体。非特异性结合试剂为 ovalbumin（OVA）和 CHO soluble membrane proteins（SMP）。两次独立测序覆盖大量序列，作者最终选取 4,000 条高频序列用于模型：1,516 条为高 antigen-binding 标签，2,484 条为低标签；specificity 分层为 2,000 条高、2,000 条低。这里的 `ANT Binding` 和 `OVA Binding` 是二元筛选标签，不是 `K_D`、`EC50` 或连续流式强度。

另有两个连续测量层。`iso_binding.csv` 保存从分选库 Sanger 测序后挑出的 126 个 scFab，在酵母表面的 HGFR 与 OVA 单点结合信号；信号先除以 display signal、扣除 display-only control，再相对 emibetuzumab 归一化。`igg_binding.csv` 保存 96 个可溶 IgG 在 Protein A beads 上的 HGFR、OVA 和 SMP 单点结合信号及重复标准差，也使用 emibetuzumab/elotuzumab 对照归一化。它们是相对结合信号，不是全体候选的绝对亲和力。

三张核心表的序列不是三个独立集合简单相加：4,000-row library 与 96-row IgG 表重叠 24 条，library 与 126-row scFab 表无重叠，scFab 与 IgG 表重叠 16 条。候选形式、实验平台、标签类型和重叠关系必须保留。OVA/SMP 越低表示非特异性越弱，不能解释为 MET 亲和力；`pI_seq` 是序列计算值，不是结合测量。

## 论文原文

- 标题：Co-optimization of therapeutic antibody affinity and specificity using machine learning models that generalize to novel mutational space
- 作者：Emily K. Makowski、Patrick C. Kinnunen、Jie Huang、Lina Wu、Matthew D. Smith、Tiexin Wang、Alec A. Desai、Craig N. Streu、Yulei Zhang、Jennifer M. Zupancic、John S. Schardt、Jennifer J. Linderman、Peter M. Tessier
- 发表来源：Nature Communications 13, 3788
- 归档文本版本：正式发表版（Version of Record）
- 发布日期：2022-07-01
- DOI：10.1038/s41467-022-31457-3
- PMID / PMCID：PMID 35778381；PMCID PMC9249733
- 本地文件：`articles/Makowski_2022-07-01_NatureCommunications-published.pdf`
- 文件大小：2.17 MiB（2,279,644 bytes）
- SHA-256：`687c0cb987834b2a37513401c5b3812d583879f29bea3b04e9d83a7d89a4230e`
- 文本许可：CC BY 4.0
- 补充材料：`articles/Makowski_2022-07-01_NatureCommunications-SupplementaryInformation.pdf`，1.87 MiB（1,965,403 bytes），SHA-256 `e0e60fa20ee29ef8f942d051baa62af696f0e4680e7d5d18c5a9070b3a36189d`；`articles/Makowski_2022-07-01_NatureCommunications-PeerReviewFile.pdf`，339.15 KiB（347,290 bytes），SHA-256 `c7139df396e15e29280e7ff023778804664f0dbf69a349bf6171ec05a45706e0`；`articles/Makowski_2022-07-01_NatureCommunications-SourceData.xlsx`，110.00 KiB（112,639 bytes），SHA-256 `f82c52fcf7a24b2a620018a78f15806b3be487486654be9b12346164aa9f4b05`
- 引用数（查询快照）：167（[OpenAlex W4283744078](https://openalex.org/W4283744078)，查询于 2026-09-21）

Source Data XLSX 有 `Figure3A-B`、`Figure3C-D`、`Figures 4 and 5` 三个 sheet，分别对应 4,000-row library、126-row scFab 和 96-row IgG 的论文作图数据。作者仓库 CSV 在这些字段基础上增加 `pI_seq`、模型特征或分组标记。

## 仓库内容

上游为作者 GitHub 仓库 `Tessier-Lab-UMich/Emi_Pareto_Opt_ML`。固定 commit `0ed9ea241ad154de86acce0bdc63586ce66d99fa` 的日期为 2022-06-24，因此命名为 `snapshot-2022-06-24`。本项目用 `git archive` 保存该 commit 的完整 50-file worktree，不含不稳定 `.git` 内部数据；commit tree 为 6,059,742 blob bytes，无 submodule 或 Git LFS pointer。

```text
snapshot-2022-06-24/
└── Emi_Pareto_Opt_ML/
    ├── LICENSE.txt
    ├── readme.txt
    ├── emi_binding.csv
    ├── emi_reps.csv
    ├── iso_binding.csv
    ├── iso_reps.csv
    ├── igg_binding.csv
    ├── igg_reps.csv
    ├── *_pI.txt
    ├── deepNNWeights/
    ├── __pycache__/
    ├── *.py
    └── environment.yml
```

仓库还包含预训练神经网络权重、模型与特征生成脚本、热图输入和作者提交的 Python bytecode。`__pycache__/` 是固定上游 commit 自带内容，不是本项目运行脚本产生的缓存；为保持完整快照而保留。

## 数据结构

### Library 二元标签

`emi_binding.csv` 有 4,000 行、4 列，大小 488.01 KiB（499,720 bytes），SHA-256 为 `c70c64f9bf50400b0d5f1b3c8c0a42291b45e6b1f6caa859b3c1eb218f5eec01`。每条 `VH Sequence` 长 115 aa 且唯一。`ANT Binding` 和 `OVA Binding` 均只取 0/1；论文定义前者为 HGFR 筛选的低/高 antigen binding，后者用于低/高 OVA non-specific binding。`pI_seq` 为 4.78–9.26 的序列计算值。

`emi_reps.csv` 与上述 4,000 条序列逐行对应，后续 64 列是作者模型使用的 UniRep representation；`emi_pI.txt` 保存物化的 pI 特征。它们不是新的实验记录。

### scFab 连续测量

`iso_binding.csv` 有 126 行、126 条唯一 115-aa VH，大小 18.71 KiB（19,155 bytes），SHA-256 为 `8cf60a039688da7f580052e200928468f7caaa958ebd06681cb6247f9d8450f6`。`ANT Binding` 范围 -0.008428734–1.614862422，`OVA Binding` 范围 0.235812214–1.081845563。小于零的 antigen signal 来自背景扣除后的归一化结果，不能静默改为零，也不等同“不结合”。

`iso_reps.csv` 和 `iso_pI.txt` 分别提供同 126 条序列的 64 维 representation 与 pI 特征。表名中的 `iso` 指 isolated scFab clones，不表示抗体同种型。

### IgG 连续测量

`igg_binding.csv` 有 96 行、96 条唯一 115-aa VH，大小 14.76 KiB（15,117 bytes），SHA-256 为 `bf6bffc969eb1c13012640339e50c28c55f30f2c9e2d9d0f4ad8a116b839d5c5`。`ANT Binding` 范围 0.06–1.28，`OVA Binding` 为 0–1.0，`SMP Binding` 为 0–1.1；`ANT STDEV` 与 `OVA STDEV` 是生物重复的标准差。`Blosum62` 有 42 个空值，因为该标记只适用于部分新突变分组，空值不是 0。

`Sample` 是候选 ID，读取时保留文本表示，避免自动推断为数值测量。

`Scaffold`、`Interpolation` 和 `Blosum62` 是候选来源或保守性分组标记，不是测量值。`igg_reps.csv` 和 `igg_pI.txt` 提供相同 96 条序列的模型特征。

### 模型输入和派生产物

`residue_dict.csv` 保存氨基酸理化特征，`figure4_heatmap.csv` 与 `top_res_heatmap.csv` 保存论文图用汇总指标。Python 脚本以 one-hot、physicochemical 和 UniRep 特征训练 LDA 或神经网络；`deepNNWeights/` 保存已训练权重。模型 projection 是与结合性质相关的连续预测指标，不是实验 `K_D`。脚本、权重和重复特征不得计入实验样本量。

### 字段说明

| 文件 | 字段 | 原始表示 | 单位与有利方向 | 含义与缺失值 |
| --- | --- | --- | --- | --- |
| 三个 binding 表 | `VH Sequence` | 115-aa 字符串 | 无单位 | 各自实验层级中的 emibetuzumab VH 变体；无缺失 |
| `emi_binding.csv` | `ANT Binding` | 0/1 | 1 为高 | HGFR 筛选二元标签，不是定量亲和力 |
| `emi_binding.csv` | `OVA Binding` | 0/1 | 0 为低非特异性 | OVA 筛选二元标签 |
| 三个 binding 表 | `pI_seq` | 浮点数 | pH 尺度 | 从序列计算的等电点 |
| `iso_binding.csv` | `Sample` | 文本 ID | 无单位 | Sanger 分离的 scFab clone ID |
| `iso_binding.csv` | `ANT Binding` | 浮点数 | 相对信号，越大越强 | 酵母表面 scFab 的 HGFR 单点信号；可因扣背景略小于零 |
| `iso_binding.csv` | `OVA Binding` | 浮点数 | 相对信号，越小越特异 | 酵母表面 scFab 的 OVA 单点信号 |
| `igg_binding.csv` | `Sample` | 数值文本 | 无单位 | IgG 候选 ID，不应解析为测量值 |
| `igg_binding.csv` | `ANT Binding` | 浮点数 | 相对信号，越大越强 | IgG bead assay 的 HGFR 单点信号 |
| `igg_binding.csv` | `OVA Binding` | 浮点数 | 相对信号，越小越特异 | IgG bead assay 的 OVA 信号 |
| `igg_binding.csv` | `SMP Binding` | 浮点数 | 相对信号，越小越特异 | CHO soluble membrane protein 非特异性信号 |
| `igg_binding.csv` | `ANT STDEV` / `OVA STDEV` | 浮点数 | 同对应信号 | 生物重复标准差 |
| `igg_binding.csv` | `Blosum62` | 空、0 或 1 | 无单位 | 保守替换标记；42 个空值需原样保留 |
| `igg_binding.csv` | `Scaffold` / `Interpolation` | 0/1 | 无单位 | 候选分组标记，不是实验标签 |
| `emi_reps.csv`、`iso_reps.csv`、`igg_reps.csv` | `VH Sequence`、`0`–`63` | 115-aa 序列和 64 个浮点数 | 无实验单位 | UniRep representation，按序列连接对应 binding 表；模型派生 |
| `residue_dict.csv` | `Residue`、`Positive Charge`、`Negative Charge`、`Hydropathy Score`、`pI`、`Atoms (not hydrogen)`、`Hydrogen Bond D/A` | 氨基酸单字母和理化特征数值 | 电荷、疏水性、等电点及计数分别沿用原表定义 | 模型特征字典，不是样本测量 |
| `figure4_heatmap.csv` | 空表头列、`%HGFR`（2 列）、`rhoHGFR`（4 列）、`%OVA`（2 列）、`rhoOVA`（4 列） | 行名、比例/相关数值与带换行星号的图注文本 | 图形汇总尺度 | 原表有重复列名，须按列位置读取；不能当作样本级实验标签 |
| `top_res_heatmap.csv` | 空表头列、`None`、`33`、`50`、`54`、`55`、`56`、`95`、`97`、`98` | 行名和按位点汇总的数值 | 图形汇总尺度 | `None` 是原始列名，不是缺失值编码 |

### 数据示例

| 文件 | `VH Sequence` | `Sample` | `ANT Binding` | `OVA Binding` | 其他 |
| --- | --- | --- | --- | --- | --- |
| `emi_binding.csv` | `QVQLVQSGAEVKKPGASVKVSCKASGYTFTDYYMHWVRQAPGQGLEWMGRVNPNTADTTYNQKFEGRVTMTTDTSTSTAYMELRSLRSDDTAVYYCARVNGLDVWGQGTTVTVSS` | 无 | `0` | `1` | `pI_seq=8.64` |
| `iso_binding.csv` | `QVQLVQSGAEVKKPGASVKVSCKASGYTFTDYYMHWVRQAPGQGLEWMGRVNPNAEATTYNQKFEGRVTMTTDTSTSTAYMELRSLRSDDTAVYYCARSNGLDAWGQGTTVTVSS` | `E14-02` | `0.605333371` | `0.851331573` | `pI_seq=7.95` |
| `igg_binding.csv` | `QVQLVQSGAEVKKPGASVKVSCKASGYTFTDYYMHWVRQAPGQGLEWMGRVNPNKGGTTYNQKFEGRVTMTTDTSTSTAYMELRSLRSDDTAVYYCARANSLDDWGQGTTVTVSS` | `14.53` | `0.8` | `0` | `SMP Binding=0.05` |

三行分别代表 library 标签、isolated scFab 测量和 IgG 测量。即使序列相同，跨表记录也可能是不同分子形式和实验平台，不能当作简单重复。

## PDB 数据库

论文没有报告 emibetuzumab–MET 的实验复合物 PDB。Methods 明确记录了构建 emibetuzumab homology model 时使用的 4 个抗体模板，本 source 为每个模板保存 H/L canonical FASTA 与完整 deposited mmCIF。它们都不是 emibetuzumab，也不包含本实验的 MET 复合物。

| 模板角色 | PDB | 实际条目 | FASTA SHA-256 | mmCIF SHA-256 |
| --- | --- | --- | --- | --- |
| VH/VL framework | 4LIQ | RG7155 Fab–CSF-1R | `95d27d1b51edf3609ad8ec4e2cb74f6e325ce0386c9fec37e78dba5aea170b30` | `468317c0fc6d5bf193bcf71973ece866763c073936766f37470ebf91d2c0a48d` |
| light-chain CDRs | 3W2D | 3E2 Fab–enterotoxin B | `60f6b9f9815bd41f50fb00644e9990cd22a6fc497a33090c39d806f17487d9ab` | `9d250bbedaf22c571646b2cdf24c63fc883b70a95630af2f586a5942d102b94f` |
| HCDR1/HCDR2 | 4YHL | dabigatran reversal Fab | `92962a822b02b3c2d7cadac68cf6d8c4e76693ae59b3661dfaa6f0613424b76c` | `97752442f54c8699c7acae96ec1d08963c4cb4bbda59ddf6a4faf3584ba52abb` |
| HCDR3 | 5NHW | bimagrumab Fab | `02ae2b932d8c0a4e3279eb0874dfd35378bfae66fbac601e6aa91fbcc1c69713` | `7b6db6cc5df78e7bd1307846e18bc732b940b0e725dc4d88c322fab81820c985` |

另外，实验所用抗原为人 HGFR/MET-Fc；RCSB `6WVZ` 为另一抗体 amivantamab 的 Fab 与人 MET 胞外 Sema 区域实验复合物，其中 MET 是 polymer entity 3、label chain C / author chain M，canonical 序列 534 aa。它是靶点代表结构，不是 emibetuzumab 结合姿态；论文未给出 HGFR-Fc 的完整构建体序列，不能声称与实验抗原严格同构。另核对了 `6I04`，其为其他抗体与人 MET Sema 区域的复合物；本版本只保存 `6WVZ` 这个代表锚点，不把两个其他抗体复合物误作样本结构。

| 靶点代表 | PDB | FASTA | FASTA SHA-256 | mmCIF | mmCIF SHA-256 |
| --- | --- | --- | --- | --- | --- |
| 人 MET Sema 区域；非实验 Fab | 6WVZ | `pdb/sequences/rcsb_pdb_6WVZ.fasta`，1,231 bytes | `ca78e0a836fc57e2ef7523dad2fd3cb802e418894114cc38b872776bf4b0863a` | `pdb/structures/6WVZ.cif`，1.37 MiB（1,431,949 bytes） | `411fc609698e0390335a829650c0bd38d50bfc5db5a90c114f9546c40edc32f2` |

全部 FASTA 位于 `pdb/sequences/rcsb_pdb_<PDB>.fasta`，mmCIF 位于 `pdb/structures/<PDB>.cif`。4 个模板 FASTA 各含 H/L 两条项目选链记录；6WVZ FASTA 保留 RCSB 完整 entry 原始字节，含 MET 与其他抗体的三个 polymer entity，不以其中抗体链作为本数据集抗体。5 个锚点均有 FASTA 和完整 mmCIF。

## 采集过程记录

- 2026-09-18：从新版清单确认 R07，核验作者 GitHub、论文 DOI、PMC 全文、Nature source data 和 MIT/CC BY 4.0 许可。
- 2026-09-18：锁定作者仓库 commit `0ed9ea241ad154de86acce0bdc63586ce66d99fa`；核对 50 个 blob、5.78 MiB（6,059,742 bytes），无 submodule/LFS，使用 `git archive` 写入 staging。
- 2026-09-18：从 Nature 固定文章与 supplementary 端点下载主文、Supplementary Information、peer-review file 和 Source Data；PDF 魔数与 XLSX ZIP 容器均通过检查。
- 2026-09-18：论文没有 emibetuzumab–MET 实验 PDB。根据 Methods 的明确模板列表，从 RCSB 下载 4LIQ、3W2D、4YHL、5NHW 的 H/L FASTA 和完整 mmCIF，并核对 author/label chain、entity sequence 与坐标格式。
- 2026-09-18：核对 `emi_binding.csv`、`iso_binding.csv`、`igg_binding.csv` 的字段、行数、115-aa VH、唯一性、值域、空值和跨表重叠；并核对 `*_reps.csv`、pI、模型权重与 source-data sheet 的角色。
- 2026-09-18：README 同步到 staging 后执行 Python 验证、markdownlint、顶层残留检查和本地/远端 SHA-256 比对；全部通过后原子发布。
- 2026-09-22：按 Nature Communications 正式版发布日期 `2022-07-01` 规范主文、Supplementary Information、peer-review file 和 Source Data 四个归档名称；所有文件字节数与 SHA-256 保持不变，下载与验收脚本同步更新。
- 2026-10-08：以论文的人 HGFR-Fc 抗原描述核对 RCSB 6WVZ/6I04；接受 6WVZ 的人 MET entity 为靶点代表，补取完整 entry FASTA 和 mmCIF 并核对字节数、SHA-256 与坐标解析。因论文未给出实验 HGFR-Fc 精确序列，映射保持代表结构层级。

## 参考文献

- Makowski EK, et al. Co-optimization of therapeutic antibody affinity and specificity using machine learning models that generalize to novel mutational space. Nature Communications. 2022. <https://doi.org/10.1038/s41467-022-31457-3>
- 作者仓库固定 commit：<https://github.com/Tessier-Lab-UMich/Emi_Pareto_Opt_ML/tree/0ed9ea241ad154de86acce0bdc63586ce66d99fa>
- PMC 全文：<https://pmc.ncbi.nlm.nih.gov/articles/PMC9249733/>
- RCSB 模板：<https://www.rcsb.org/structure/4LIQ>；<https://www.rcsb.org/structure/3W2D>；<https://www.rcsb.org/structure/4YHL>；<https://www.rcsb.org/structure/5NHW>
- RCSB 人 MET 靶点代表：<https://www.rcsb.org/structure/6WVZ>；审计候选：<https://www.rcsb.org/structure/6I04>

## 其他

### 数据范围和限制

公开包保存模型使用的 4,000 条筛选标签、126 条 scFab 连续信号、96 条 IgG 连续信号、派生特征和分析代码。它不包含全部约 170 万理论 library、全部测序 reads、逐候选 `K_D`，也没有 emibetuzumab–MET 实验复合物结构。使用时至少按分子形式、实验平台、读出和序列重叠分组。

### 完整性与验收

- 顶层只含 `Emi_Pareto_Opt_ML/`、`pdb/`、`articles/`、`README.md`。
- 作者仓库完整 commit 快照为 50 个文件、5.78 MiB（6,059,742 bytes）。
- 三张核心表分别为 4,000、126、96 行；唯一序列、115-aa 长度、二元值域、连续值有限性、42 个 `Blosum62` 空值和跨表重叠均通过独立检查。
- 4 个论文建模模板与 1 个人 MET 靶点代表均同时具有 FASTA 与完整 mmCIF；4 个文章文件均通过格式检查。
- README 修改后必须经 markdownlint `0 error(s)`，并与远端 SHA-256 一致。

### 许可和再分发边界

作者仓库 `LICENSE.txt` 为 MIT License，要求保留版权和许可文本。Nature Communications 论文、Supplementary Information 和 Source Data 标为 CC BY 4.0。RCSB 文件需保留 PDB 条目与原始结构论文引用。模型依赖和第三方软件仍受各自条款约束，MIT 不替代其许可证。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 4,000 条用于模型的 library 序列 | `emi_binding.csv` 与 Source Data `Figure3A-B` | 已取得 |
| 125 个分选 scFab 加 parent/control 记录 | `iso_binding.csv` 与 Source Data `Figure3C-D` 共 126 行 | 已取得 |
| IgG 结合与非特异性测量 | `igg_binding.csv` 与 Source Data `Figures 4 and 5` 共 96 行 | 已取得 |
| 模型代码、特征与权重 | 完整作者 commit 快照 | 已取得 |
| emibetuzumab homology model | 论文给出模板和建模方法；仓库未提供最终结构文件 | 部分；4 个模板已补齐 |
| emibetuzumab–MET 实验复合物结构 | 论文未报告对应 PDB | 无可辩护锚点，不臆配 |
| 人 MET 靶点代表结构 | RCSB 6WVZ，MET entity 3 | 已取得；非实验 HGFR-Fc 严格构建体映射 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-08；结构映射部分完成）：论文只写人 HGFR-Fc，未给出完整实验抗原构建体序列。RCSB 6WVZ 的人 MET Sema 区域已作为靶点代表成对保存；4 个抗体模板亦已验收，但无法证明 6WVZ 与实验 HGFR-Fc 在非 MET 区域和构建体边界上严格一致，也不能由此得到 emibetuzumab–MET 结合姿态。若后续需要构建体级结构映射，应取得试剂货号/完整序列和相应结构证据；当前仅使用靶点代表层级。

本 source 已取得论文正文、补充材料、Source Data 和作者仓库中直接支撑当前三张表及模型复现的文件。未单独追索与当前数据解释无关的出版流程附件；正文未公开 emibetuzumab–MET 实验复合物，仍按上述结构边界使用。
