---
tags:
  - context
---

# SRC_R04_IPI 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
  - [抗体库和筛选主线](#抗体库和筛选主线)
  - [常规筛选如何形成 424 条表征记录](#常规筛选如何形成-424-条表征记录)
  - [机器学习支路如何补入 62 条记录](#机器学习支路如何补入-62-条记录)
  - [公开产物、标签与解释边界](#公开产物标签与解释边界)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [NGS 选择表](#ngs-选择表)
  - [机器学习输入表](#机器学习输入表)
  - [486 抗体表征表](#486-抗体表征表)
  - [FLAb 派生副本](#flab-派生副本)
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

- `source_id`：`SRC_R04_IPI`
- `source_version`：`zenodo-15707494`
- 原作者或发布机构：Institute for Protein Innovation 的 Deepash Kothiwal 团队及论文合作者

### 来源方背景

[Institute for Protein Innovation](https://proteininnovation.org/) 是位于美国波士顿的独立非营利研究机构，由哈佛医学院的 Timothy A. Springer 和 Andrew Kruse 于 2017 年共同创办，见[机构历史](https://proteininnovation.org/history/)。两位创办人希望把可再生的合成抗体作为共享研究工具，特别面向细胞表面和分泌蛋白靶点；IPI 因此建立酵母展示抗体发现平台，并开展资源共享、研究合作及培训。

其[2023 年报](https://proteininnovation.org/resources/annual-reports/)记录了面向整合素蛋白家族推出首批抗体资源；[2025 年成果报告](https://proteininnovation.org/wp-content/uploads/2025/12/2025-IPI-Accomplishments_FINAL.pdf)称当年完成 10,000 个抗体的验证。Deepash Kothiwal 领导的本项研究与 Harvard Medical School 合作，机构[专题报道](https://proteininnovation.org/2025/05/machining-antibodies-at-ipi/)介绍了其面向细胞表面抗原的高通量抗体发现工作。

## 实验设计和数据口径

### 抗体库和筛选主线

研究先建立一个以 VH1-69 为固定重链骨架、主要改变 CDRH3 的合成 Fab 酵母展示库。四个亚库分别搭配 `VK1-39`、`VK3-15`、`VK3-20` 和 `VK4-1` 轻链；前三种形成相对平坦的抗原识别面，`VK4-1` 因较长的 CDRL1 形成相对凹陷的识别面。CDRH3 长度和位点氨基酸频率参考 OAS 的人 naïve B-cell repertoire，同时在寡核苷酸设计中尽量排除若干已知序列风险。论文估计完整库接近十亿个不同 Fab；这个库规模不是本 source 的公开记录数。

作者用同一库并行筛选 10 个抗原系统：DCC、鼠 DKK1、IL23R、LOX1、PD-L1、PD-L2、ROBO1、ROBO2 的 N 端结构域、Syncytin-2 和 TIGIT。每个抗原分别进行 flat pool 和 concave `VK4-1` 两条选择支路：先以 100 nM 生物素化抗原做一轮 MACS，再依次以 100、20 和 4 nM 抗原做三轮 FACS，并在各轮扩增后测序 ARM。ARM 包含 CDRH3 和标识所配轻链的条形码，因此公开的 `CDR3 + heavy + light` 能标识库内设计，而不是完整测序 read 或完整 IgG 构建体。

22 张 NGS CSV 是这一步的选择结果汇总。20 张主表对应“10 个抗原 × flat/concave 两种几何”，保存 FACS1–3 的 read count 和作者给出的相似序列 cluster；另两张 `humanROBO1_flatMACS1.csv`、`humanROBO2N_flatMACS1.csv` 补充 ROBO1/ROBO2N flat 支路的 MACS–FACS1–3 计数。它们不是 22 次彼此独立的抗体实验，也不是 binder/non-binder 真值表。

新版 Zenodo record 另补入 PD-L1、PD-L2、ROBO1 和 ROBO2N 四张机器学习输入表。它们按 `CDR3 + heavy + light` 汇总 MACS1 和三轮 affinity sort 的计数，供作者公开的 logistic-regression 代码训练、评分和验证；它们与上述 22 张选择汇总表有重叠，但 CDRH3 边界、轻链拼写和处理层级不同，不能把两组行数直接相加成独立抗体数。

### 常规筛选如何形成 424 条表征记录

作者先按抗原和选择支路汇总各轮 NGS 结果，再把等长且 BLOSUM62 相似度超过作者阈值的 CDRH3 归为 cluster。随后主要依据 FACS3 丰度，从每个选中 cluster 取最丰富的 CDRH3 代表，订购 429 条重链基因；其中 424 条获得足够产量，并与测序所指示的固定轻链共同表达为人 IgG1。这里的 424 条是经过多轮富集、聚类和代表序列挑选的候选，不是从 NGS 表随机抽取的正负样本。

这 424 条抗体随后接受两类质量检查和两类结合表征：PSR ELISA 检查对 avidin、DNA、insulin 和 Sf9 membrane preparation 的多反应性，SEC 检查聚集或降解；SPR 测量抗体对筛选所用可溶性截短抗原的动力学，cell display 则测量抗体对 ExpiCHO-S 细胞表面完整或较完整抗原构建体的滴定响应。

这里有一处需要按论文版本区分的数字。bioRxiv v1 正文写 302 条满足 SEC benchmark，但其表 S3 已列为 301/123；正式发表版正文把该数修正为 301。正式版表 S3 的 20 个分组逐行相加同样是 301/123，不过表底总计误印为 301/121。当前 CSV 与逐行合计一致：424 条常规候选中，PSR 为 `Pass` 350、`Medium` 4、`Fail` 70，SEC 为 `Pass` 301、`Fail` 123。论文还报告 285 条同时通过两项质量检查，但 CSV 中严格 `Pass/Pass` 只有 265 条，即 285 不能由公开字段直接复算。表 S3 进一步列出的 103 条 SPR 和 118 条 cell-display 结果叠加了质量及效力判据，不能把这两个数字理解为“424 条中只有 103/118 条结合”。

### 机器学习支路如何补入 62 条记录

末轮富集会损失早期选择中的一部分序列多样性，因此论文又从早期轮次开出一条独立的补充支路。作者针对目标的 MACS1 与 FACS1 序列训练正则化 logistic-regression 模型：以归一化丰度从 MACS1 到 FACS1 增加的序列为正例，输入为 CDRH3 的 1–3-mer 计数及轻链 identity。这里的正负例是早期选择富集标签，不是 SPR 或 cell display 证实的 binder/non-binder 标签。

模型对早期候选打分后，作者再结合 FACS1 丰度、与已订购候选及候选之间的 Levenshtein 距离，选出 29 条在后续轮次中耗减或丢失的 ROBO2N 序列；PD-L2 采用同类方法另选 33 条。新版数据和代码为 PD-L1、PD-L2、ROBO1、ROBO2N 四个 campaign 提供输入表与预训练参数，但论文中实际补入 486 抗体表的仍只有 ROBO2N 和 PD-L2 这 62 条候选。

这 29 + 33 = 62 条机器学习补充候选也被实际表达和测试；它们在公开表中分别以 `ROBO2N_ML_Ab_*` 和 `PDL2_ML_Ab_*` 命名。主表的 486 条因此可明确拆成 424 条常规末轮筛选候选和 62 条早期轮次机器学习补充候选，而不是 486 条都由同一条 FACS3 选样规则产生。

```text
近十亿规模的合成 Fab 酵母展示库
        │
        ├── 10 个抗原 × flat/concave ── MACS + 3 轮 FACS + NGS
        │                                └── 聚类并选代表：429 条重链订购
        │                                    └── 424 条产量充足的常规候选
        │
        └── ROBO2N / PD-L2 早期轮次 ── logistic regression 补选
                                             └── 29 + 33 = 62 条 ML 候选

424 条常规候选 + 62 条 ML 候选
        └── PSR、SEC、SPR、cell display 汇总为 486 条表征记录
```

### 公开产物、标签与解释边界

22 张选择汇总表合计 94,274 行，其中 20 张 FACS1–3 主表为 86,666 行，两张额外 MACS 表为 7,608 行；跨全部文件有 82,359 个唯一 `CDR3` 文本和 91,808 个唯一 `CDR3 + heavy + light` 组合。论文所称“超过 68,000 个至少有两个 ARM counts 的唯一 ARM 序列”、CSV 行数以及上述跨文件去重数采用不同分母和去重范围，不能相互替代。部分 ARM 会跨抗原或选择支路出现，20 张主表内部还有 138 个重复 `CDR3 + heavy + light` 行实例且计数不同；分析时必须保留来源文件、抗原和 paratope geometry，不能把一行直接解释为一个全局唯一抗体。

四张机器学习输入表另有 383,341 行；每张表内 `CDR3 + heavy + light` 唯一，跨四表去重后为 382,399 个组合和 356,601 个 `CDR3` 文本。这组表覆盖更早、更大的候选池，并与 22 张汇总表存在 22,957 个经 CDRH3 前导 `C` 归一化后相同的组合，因此 383,341 与 94,274 不能相加解释为互不重叠的样本总数。

486 抗体表是作者整理后的结果汇总：364 条有数值 SPR 参数，345 条有数值 cell-display EC50，324 条两者都有，385 条至少有一种数值，101 条两种均为 `Fail`。PSR 为 394 `Pass`、88 `Fail`、4 `Medium`，SEC 为 355 `Pass`、131 `Fail`。SPR 使用 Carterra LSA 的多浓度动力学数据做 1:1 Langmuir 全局拟合，以 `KD = kdis / ka` 得到亲和力；cell display 则用细胞表面抗原的抗体滴定曲线拟合 EC50。两者的抗原呈现形式、观测量和拟合过程不同，不能视为可互换标签；在各自单位正确且结果可拟合时，数值越小通常表示结合越强。

**NGS count/cluster、PSR、SEC 和结果字段中的 `Fail` 都不是统一的 binder/non-binder 金标准。** NGS 富集还受展示效率、重轻链配对、克隆生长和交叉污染影响；PSR/SEC 是多反应性与样品完整性检查；SPR 或 cell display 的 `Fail` 只说明作者没有报告可用的相应数值。由于公开包没有 sensorgram、滴定点、拟合 `R²`、重复实验或失败原因，不能进一步把所有 `Fail` 严格区分为“确实不结合”和“样品、测量或拟合未通过”。486 条又是经过筛选的候选集合，不代表完整库中的总体正负分布。

FLAb 固定 commit 把 486 表中有数值的结果按抗原和 assay 拆成 10 张 EC50 表与 10 张 SPR 表。709 行等于 345 条 EC50 assay rows 加 364 条 SPR assay rows，并不表示 709 个抗体；两类表的并集只有 385 个唯一抗体，其中 324 个同时出现于两类表。EC50 的 `fitness` 原样等于 nM 数值，越小越有利，但 FLAb inventory 把 favorable direction 标成向上；SPR 的 `fitness = 9 - log10(KD 数值)`，意在把 nM 转为 pKD。

这层派生还有两个必须在 processed 层处理的风险。其一，PD-L2 与 ROBO2N 的 29 条 ML-derived 数值与 `kdis/ka` 一致地处于 M 量级，却仍放在主表和 FLAb 统一标作 `KD (nM)` 的列中；FLAb 又按 nM 换算，令 pKD 类 `fitness` 偏高 9。其二，FLAb 为 385 个唯一抗体构造的 `heavy` 全部呈 `...YYCARCAR...`：Zenodo 的表征表 `CDRH3` 已以 `CAR` 开头，而拼接所用 VH 模板也在插入点前保留 `CAR`，因此很可能重复了边界 motif。raw 层保留上游原值；下游不得在未核实和显式记录规则时直接把这些 `fitness` 或 `heavy` 当作可信标准字段。

正式版公开的代码归档补齐了四个 campaign 的输入读取、特征构建、预训练参数、评分与部分候选选择逻辑，但没有锁定 Python 依赖环境，也没有保存运行后生成的 `scores/` 和 `selected_abs/` 结果。当前选择循环只输出 ROBO1/ROBO2N，不能不加修改地重现论文所述 33 条 PD-L2 补选候选；这不影响已公开 486 表的内容，但限制了从原始输入端到最终候选的端到端复算。

## 论文原文

### 预印本

- 标题：*High-Throughput Machine Learning-Aided Antibody Discovery for Cell Surface Antigens*
- 作者：Deepash Kothiwal et al.
- 发表来源：bioRxiv v1
- 发布日期：2025-05-15
- DOI：`10.1101/2025.05.15.650607`
- PMID / PMCID：无
- 文本许可：CC BY-NC 4.0
- 主文：`articles/Kothiwal_2025-05-15_bioRxiv-v1.pdf`，12 页，5,867,156 bytes，SHA-256 `e01e07dba7f5bedcabcdbfd5c2ef049ad7269da4501f71ab0bea3caaeb958aa0`
- 补充材料：`articles/Kothiwal_2025-05-15_bioRxiv-v1-supplement.pdf`，23 页，6,145,124 bytes，SHA-256 `6209c6393002763389139795bf07f31e1c85ab598cdeb3ee82db89a5a3488755`

### 正式发表版

- 标题：*High-throughput machine learning-aided antibody discovery for cell surface antigens*
- 作者：Deepash Kothiwal et al.
- 期刊：*Cell Systems* 17(8), 101645
- 在线发表：2026-06-23；卷期日期：2026-08-19
- DOI：`10.1016/j.cels.2026.101645`
- PMID：`42335897`；PMCID：截至 2026-09-24 未见
- 文本许可：CC BY-NC-ND 4.0
- 正式版 PDF：`articles/Kothiwal_2026_Cell-Systems_version-of-record.pdf`，44 页，31,539,422 bytes，SHA-256 `61c11d014c181db707941c2bb2b8e098e724a51224a6313abcb8689830d69b03`。该官方文件把 22 页补充信息附在正文之后。
- 独立补充材料：`articles/Kothiwal_2026_Cell-Systems_supplemental-information.pdf`，22 页，9,993,327 bytes，SHA-256 `631fb562a7419f705b6e255dce87a854173aa58bcc22ba2ac88d141747ee43b1`
- 透明同行评审记录：`articles/Kothiwal_2026_Cell-Systems_transparent-peer-review.pdf`，28 页，3,419,488 bytes，SHA-256 `c1a1850ebab2b6e3c85905056999cd90277480406da9f69ae707f640905dd66c`

预印本和正式版属于同一项研究，但不是同一文本版本。正式版补充了修订后的方法、分析和同行评审所促成的实验内容，并把正文中的 SEC 通过数从 302 修正为 301；解释论文结论时以正式版为准。数据文件本身仍按 Zenodo record 独立定版，本 source 采用正式论文 key resources table 指向的较新 record `15707494`，不会用论文措辞去改写原始 CSV。

OpenAlex 把预印本 DOI 和正式论文 DOI 合并在同一 work [W4410395662](https://openalex.org/W4410395662) 下；截至 2026-09-24 的 `cited_by_count` 为 1，因此这里只记录一次，不把两个出版版本的数字相加。

## 仓库内容

主数据来自不可变 Zenodo record `15707494`，DOI 为 `10.5281/zenodo.15707494`，concept DOI 为 `10.5281/zenodo.15367596`，发布日期为 2025-06-20。它是较早 record `15367597` 的后续版本：原有 24 个文件的字节与 MD5 均未改变，新增四张机器学习输入 CSV。正式 record 编号直接构成 `source_version=zenodo-15707494`；较早版本仍作为同级历史快照保留，不被覆盖。

论文列出的代码归档是 Zenodo record `20060875`（DOI `10.5281/zenodo.20060875`，版本 `v1.0.0`，MIT License），其中 ZIP 对应 GitHub commit `cb07330a89a1c3338ef4cb86e9855646e503c535`。`Kothiwal2025/FLAb/` 则是 FLAb commit `e05e3f0135783ffb7de412df6a1467e7a0031911` 的选择性快照，只保留解释 R04 所需的说明、许可和 20 张目标 CSV，不是完整 FLAb 仓库。

```text
zenodo-15707494/
└── Kothiwal2025/
    ├── Zenodo-15707494/
    │   ├── 00Library_Biophysics_486Abs(1).csv
    │   ├── 0Library_keys.xlsx
    │   ├── *_Test1_Lib31.csv             4 张机器学习输入表
    │   └── 其余 *.csv                    22 张 NGS 选择汇总表
    ├── Code-Zenodo-20060875/
    │   └── ML-antibody-discovery-v1.0.0.zip
    └── FLAb/
        ├── README.md
        ├── LICENSE
        └── data/
            ├── README.md
            └── binding/                  20 张 EC50/SPR 派生表
```

Zenodo API 列出 28 个对象，总计 28.50 MiB（29,885,226 bytes），包括 27 个 CSV 和一个 XLSX。`Zenodo-15707494/` 是论文作者的一手公开数据包；`Code-Zenodo-20060875/` 是作者定版的软件归档；`FLAb/` 是后来从 486 表筛选数值结果、补入完整序列字段并构造 `fitness` 的训练友好型派生副本；`articles/` 和 `pdb/` 是本项目为解释与检索另行归档的材料。各层来源和生成关系不能互相冒充。

## 数据结构

### NGS 选择表

20 张常规 FACS 表使用 9 列：`CDR3`、`heavy`、`light`，以及三轮各自的 count 和 cluster。`humanROBO1_flatMACS1.csv` 与 `humanROBO2N_flatMACS1.csv` 使用 7 列：`CDR3`、`heavy`、`light`、`MACS`、`FACS1`、`FACS2`、`FACS3`。

一行表示某一来源文件中一个 ARM 文本及其跨轮次汇总，不保证 `CDR3 + heavy + light` 在文件内唯一。20 张主表的 86,666 行中有 138 个额外的重复键实例，它们保留了不同的 round count；若要聚合，必须先定义按轮次求和、取最大值或保留实例等规则，不能静默去重。

`heavy` 和 `light` 是 `VH1-69`、`VK3-15` 等链模板标识，不是完整氨基酸序列。`0Library_keys.xlsx` 的 `0Library_keys` sheet 占 23 行、5 个实际使用列，其中空行用于分段；内容包括重链/轻链模板、CDRH3 插入说明、一个计数示例和 10 个抗原构建体序列。模板中的 `X` 或小写 `x` 是上游占位符，raw 层保持原样；工作簿将论文和 CSV 所称的 `VK4-1` 写成 `VK14-1`，应视为待上游确认的命名差异，不要据此新增第五种轻链。

NGS 表与 486 表的 CDRH3 边界约定不同，不能按字符串直接连接。486 表的全部 `CDRH3` 都以 `C` 开头；对 424 条常规候选去掉这一位后，再结合抗原、HC 和 LC，可在 20 张主表中找到 423 条，余下的 `PDL1_Concave_Ab_011` 在 486 表的三轮 NGS 字段本身均为 `Fail`。这项连接结果说明应显式记录边界变换和多重匹配，而不是把两个同名“CDR3”字段直接等同。

### 机器学习输入表

四张 `*_Test1_Lib31.csv` 采用同一组 8 列：`CDR3`、`heavy`、`light`、`key`、`Macs1`、`Aff1`、`Aff2`、`Aff3`。其中 `key` 逐行等于 `CDR3:heavy:light`；四个计数列分别保存 MACS1 和三轮 affinity sort 的 read count，空白表示该序列在相应轮次没有公开计数。作者代码在计算归一化丰度时把这些空白填为 0，但 raw 层保持空白原值。

| 文件 | 行数 | `Macs1` 非空 | `Aff1` 非空 | `Aff2` 非空 | `Aff3` 非空 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `PD1-L1_Test1_Lib31.csv` | 109,857 | 90,095 | 20,104 | 1,396 | 313 |
| `hPD-L2_chase_Test1_Lib31.csv` | 83,785 | 72,357 | 9,886 | 1,076 | 263 |
| `hROBO1_Test1_Lib31.csv` | 104,289 | 94,006 | 8,059 | 2,002 | 525 |
| `hROBO2N_Test1_Lib31.csv` | 85,410 | 77,820 | 6,186 | 1,385 | 70 |

这四张表中的 `CDR3` 已包含前导 `C`，轻链值写作 `VK4-01`；22 张选择汇总表中的 `CDR3` 不含这一个前导字符，轻链则写作 `VK4-1`。两种差异均来自上游文件，做跨表连接时需要显式归一化，不能在 raw 层改名或改序列。

### 486 抗体表征表

`00Library_Biophysics_486Abs(1).csv` 使用两行组合表头。按普通单行表头读取会把第二行误算成数据并得到 487 行；正确读取后为 486 条唯一 `Antibody_Name` 记录。

按名称可将它们分成 424 条常规候选与 62 条 `_ML_` 候选。`Antigen` 有 11 个原始文本值，但这并不表示 11 个生物靶点：`hROBO2N` 的 6 条常规 flat 候选与 `ROBO2N` 的 7 条常规 concave 候选及 29 条 ML 候选都属于同一个 ROBO2N 抗原系统。下表按原始文本计数，因此保留两种拼写。

| `Antigen` | 记录数 |
| --- | ---: |
| IL23R | 75 |
| Syncytin2 | 61 |
| DCC | 57 |
| LOX1 | 55 |
| PDL2 | 54 |
| ROBO1 | 48 |
| PDL1 | 38 |
| ROBO2N | 36 |
| TIGIT | 34 |
| DKK1 | 22 |
| hROBO2N | 6 |

### FLAb 派生副本

FLAb 的 10 张 EC50 表合计 345 行，10 张 SPR 表合计 364 行；两类文件并集为 385 个唯一抗体名称，其中 324 个名称同时出现于两类表。EC50 行集合恰好对应 486 表中 EC50 为数值的记录，SPR 行集合恰好对应 KD 为数值的记录，因此这 709 行是 assay-specific 派生记录而不是独立抗体。

FLAb `data/binding/README.md` 声称 20 张表合计 697 行，并将 `DCC_spr` 写成 23 行；固定 commit 的实际文件合计 709 行，`DCC_spr` 为 35 行。多出的 12 行不是重复名称或重复序列，本 source 保留真实 Git tree。FLAb 的 `heavy` 虽提供完整可变区文本，但 385 个唯一序列全部含疑似重复的 `YYCARCAR` 边界；在问题澄清前，应优先从 Zenodo 的模板和 CDRH3 重新建立有版本记录的重建规则，而不是直接采用该字段。

### 字段说明

22 张选择汇总 CSV 有两种表头，四张机器学习输入 CSV 另有一组统一表头。486 抗体 CSV 的上层组名与第二行子列名合并后形成 14 个实际字段；FLAb 的 20 张派生 CSV 另有 18/19 列。`0Library_keys.xlsx` 是多个小表和注释段拼在同一 sheet 中，按段落说明其原始列头。下表的 `␠` 表示原始字段名中的一个尾随 ASCII 空格，便于准确还原实际拼写。

| 文件或表 | 原始字段 | 表示、单位与来源 | 缺失及特殊编码 |
| --- | --- | --- | --- |
| 常规 NGS CSV | `CDR3`、`heavy`、`light` | CDRH3 可变片段及重/轻链模板 ID；作者处理后的 ARM 记录 | 无空值；模板 ID 不是完整链序列；与 486 表 `CDRH3` 的边界相差一个前导 `C` |
| 常规 NGS CSV | `FACS1_count`、`FACS1_cluster`、`FACS2_count`、`FACS2_cluster`、`FACS3_count`、`FACS3_cluster` | 三轮选择的汇总 read count 与每轮 cluster 编号；整数文本，无物理单位 | 同一 ARM 可有多个行实例或跨文件出现；0 是上游计数/聚类编码，不等同 non-binder |
| 两张 MACS CSV | `CDR3`、`heavy`、`light`、`MACS`、`FACS1`、`FACS2`、`FACS3` | 序列与模板字段同上；后四列为磁性/荧光选择计数或汇总值 | 不与常规表的 `FACS*_cluster` 混作同一字段 |
| 四张机器学习输入 CSV | `CDR3`、`heavy`、`light`、`key`、`Macs1`、`Aff1`、`Aff2`、`Aff3` | 含前导 `C` 的 CDRH3、模板 ID、三字段拼接键，以及 MACS1/三轮 affinity sort count | 计数空白是上游缺失编码；作者代码计算时填 0；`VK4-01` 与其他表的 `VK4-1` 是同一轻链的拼写差异 |
| 486 抗体 CSV | 上层 `Antibody_Name`、`Antigen`、`Antigen Recognition Module (ARM)`；后者下层为 `HC`、`LC`、`CDRH3` | 抗体 ID、靶点、重/轻链模板和 CDRH3；原文件用两行表头表示 | 486 个抗体名唯一；上层表头在合并组内留空 |
| 486 抗体 CSV | 上层 `Deep Sequencing Counts (NGS)`；下层 `FACS1`、`FACS2`、`FACS3` | 三轮 NGS 选择计数；实验汇总，无物理单位 | 与逐事件 FASTQ 或流式事件不同 |
| 486 抗体 CSV | 上层 `Quality control`；下层 `PSR␠`、`SEC` | 两项质量控制分类；上游实验汇总 | `Pass`、`Fail`、`Medium` 等原值；`PSR␠` 含尾随空格 |
| 486 抗体 CSV | 上层 `SPR kinetics`；下层 `KD (nM)`、`ka (1/Ms)`、`kdis (1/s)` | 1:1 全局拟合的平衡解离常数、缔合和解离速率；标称单位分别为 nM、M⁻¹s⁻¹、s⁻¹ | 122 条记录统一写 `Fail`；29 条 ML 数值实为 M 量级，不能按表头直接混用 |
| 486 抗体 CSV | 上层 `Cell Display␠␠`；下层 `EC50 (nM)` | 细胞表面抗原呈现 assay 的 EC50，单位 nM；越小通常结合越强 | 141 条记录为 `Fail`；不公开失败原因；上层标题中有两个尾随空格 |
| `0Library_keys.xlsx` 模板段 | `Antibody chain`、`Sequence` | 重/轻链模板名称与含 CDRH3 占位符的氨基酸序列 | `X`/`x` 是原始占位符；`VK14-1` 与论文/CSV 的 `VK4-1` 不一致；空行分隔段落 |
| `0Library_keys.xlsx` 示例段 | `CDR3`、`heavy`、`light`、`MACS`、`FACS1` | 一条示例 CDRH3、模板及选择计数；无物理单位 | 示例段不构成第二份独立筛选表 |
| `0Library_keys.xlsx` 抗原段 | `Antigen sequences:`、`Species`、`C-terminal tags` 及无列名的序列列 | 靶点名称、物种、标签与抗原氨基酸序列；上游构建体说明 | 10 个抗原条目；该段第四列在原表中没有表头 |
| FLAb EC50/SPR CSV | `Antibody_Name`、`Antigen`、`Antigen Recognition Module (ARM)`、`LC`、`CDRH3` | 原 486 表对应的抗体 ID、靶点、模板和 CDRH3；FLAb 再整理字段 | 只保留有相应数值标签的候选；跨 EC50/SPR 表可重复 |
| FLAb EC50/SPR CSV | `Deep Sequencing Counts (NGS) - FACS1`、`Deep Sequencing Counts (NGS) - FACS2`、`Deep Sequencing Counts (NGS) - FACS3`、`Quality control - PSR␠`、`Quality control - SEC` | 上游选择计数与 QC 分类的派生副本 | 保留原始 `Pass`/`Fail`/`Medium` 等文本 |
| FLAb EC50/SPR CSV | `SPR kinetics - KD (nM)`、`SPR Kinetics - ka (1/Ms)`、`SPR Kinetics - kdis (1/s)`、`Cell Display␠␠ - EC50 (nM)` | 两种 assay 的汇总值；单位以原始列名为准，大小写与两行表头不同 | SPR 有 29 行 ML-derived 值呈 M 量级，需单独标记 |
| FLAb EC50/SPR CSV | `antigen_seq`、`light`、`heavy` | FLAb 发布的抗原、轻链和重链氨基酸序列字段；由 Zenodo key/template 派生 | 385 个唯一 `heavy` 均含疑似重复的 `YYCARCAR` 边界，未经核实不得直接作为标准 VH |
| FLAb SPR CSV | `neg log SPR Kd (M)`、`fitness` | FLAb 对 KD 的负对数变换及训练标签，数值越大通常表示较强结合 | 两列均受 29 行单位异常影响，不作原地修正 |
| FLAb EC50 CSV | `fitness` | 原表 EC50 的 nM 数值副本，数值越小通常结合越强 | inventory 标注的 favorable direction 与数值方向不一致 |

下列字段的取值集合较小，适合作为枚举理解；记录数均来自当前版本，不把缺失值并入类别。

| 文件或字段 | 全部公开取值 | 含义与记录数 |
| --- | --- | --- |
| 22 张选择汇总表 `heavy` | `VH1-69` | 固定重链模板；94,274 行均为该值 |
| 22 张选择汇总表 `light` | `VK1-39`、`VK3-15`、`VK3-20`、`VK4-1` | 四种轻链模板；分别为 21,274、21,874、18,922、32,204 行 |
| 四张机器学习输入表 `heavy` | `VH1-69` | 固定重链模板；383,341 行均为该值 |
| 四张机器学习输入表 `light` | `VK1-39`、`VK3-15`、`VK3-20`、`VK4-01` | 四种轻链模板；分别为 103,080、99,158、87,666、93,437 行；`VK4-01` 对应其他文件的 `VK4-1` |
| 486 表 `HC` | `VH1-69` | 486 条均使用同一重链骨架 |
| 486 表 `LC` | `VK1-39`、`VK3-15`、`VK3-20`、`VK4-1` | 分别为 100、141、74、171 条 |
| 486 表 `PSR␠` | `Pass`、`Medium`、`Fail` | 分别为 394、4、88 条；反映多反应性筛查结果，不是结合标签 |
| 486 表 `SEC` | `Pass`、`Fail` | 分别为 355、131 条；反映样品聚集、降解或保留时间检查，不是结合标签 |

`Antigen` 的 11 个原始文本值及各自记录数已在“486 抗体表征表”中完整列出，不在此重复。

### 数据示例

NGS 文件 `hDCC-fn4fn6L_concave.csv` 的首条真实记录为：

```text
ARSVQPLYPWPFDY,VH1-69,VK4-1,21,3,644,1,10190,1
```

字段依次对应 `CDR3`、`heavy`、`light` 和三轮 count/cluster。该行是在 DCC concave 文件中的一个 ARM 汇总行实例，同时包含三个 FACS 轮次；序列信息限于 CDR3 和 heavy/light 模板标识。

486 表中的真实记录 `DCC_Ab_001` 为：

```text
DCC_Ab_001,DCC,VH1-69,VK3-15,CARSWRAVDYTLFDY,32,1082,21114,Pass,Fail,29.73,1.84E+06,5.25E-02,37.3
```

它包含 ARM、三轮 NGS 计数、PSR/SEC、SPR 和 cell-display 汇总。其 NGS 对应片段是去掉前导 `C` 后的 `ARSWRAVDYTLFDY`；对应的 FLAb DCC EC50 行以同一抗体名连接，`fitness=37.3`，即原始 EC50 nM 数值。该 FLAb 行的 `heavy` 则被拼为 `...YYCARCARSWRAVDYTLFDYWG...`，展示了不能忽略的 `CAR` 重复问题。

## PDB 数据库

论文与公开表没有为 486 个新筛选抗体提供抗体-抗原复合物 PDB，也没有逐行 PDB 键。`pdb/` 是本项目补充的十个靶点代表结构，只用于提供目标蛋白的外部结构参照；它们不是这 486 个抗体的结合姿态，也不能作为实验抗体-抗原复合物使用。

| 实验抗原 | 代表 PDB | 选取链（author / label） | 与实验构建体的关系 |
| --- | --- | --- | --- |
| DCC（人） | `5X83` | A / A（Fn4），B / B（Fn5–Fn6） | 两条链分别覆盖实验构建体中的相应片段；不是同一条完整 construct |
| DKK1（鼠） | `3S2K` | C / C | **PDB 链是人 DKK1，同实验所用鼠 DKK1 不是同一物种或同一序列，只能作同源代表结构** |
| IL23R（人） | `5MZV` | C / C | 覆盖人 IL23R 构建体片段；实验 construct 另含 Fc 和标签 |
| LOX1（人） | `6TLA` | A / A | 覆盖人 LOX1 构建体片段 |
| PD-L1（人） | `3BIK` | A / A | 覆盖人 PD-L1 构建体片段 |
| PD-L2（人） | `6UMT` | B / B | 近同源的人 PD-L2 片段，并非实验 construct 的字节级同序列副本 |
| ROBO1（人） | `5O5G` | A / A | 覆盖实验构建体中的 ROBO1 片段 |
| ROBO2N（人） | `6IAA` | A / A | 完整 PDB 链含实验 N 端片段；不是同一截短 construct |
| Syncytin-2（人） | `7OIX` | A / A | 近同源的人 Syncytin-2 结构片段，并非实验 construct 的严格副本 |
| TIGIT（人） | `3Q0H` | A / A | 覆盖人 TIGIT 构建体片段 |

每个条目均保存所选 target chain 的 RCSB canonical FASTA 和完整 mmCIF，分别位于 `pdb/sequences/` 与 `pdb/structures/`。DCC 使用两条目标链，因此十个结构共有 11 条 FASTA 记录。`0Library_keys.xlsx` 中的抗原构建体序列只用于核对靶点身份及覆盖关系；标签、信号肽、Fc、截短边界和物种差异均可能使它与 PDB canonical sequence 不完全相同。

此前通用 PDB 脚本曾错误地按位置配对 entity-level `auth_asym_ids` 与 `asym_ids`。本批 R04 文件现已用修正后的逐 chain-instance 逻辑重新验收：11 条 FASTA 记录的 author chain、label chain 和 entity canonical sequence 均与对应 mmCIF 一致；2026-09-24 重新获取的十个 RCSB mmCIF 也与本地字节逐一相同。因此旧脚本缺陷没有造成 R04 的链错配，现存问题是上述“代表结构不等于实验 construct”的解释边界，而不是文件取错链。

| PDB | FASTA SHA-256 | mmCIF SHA-256 |
| --- | --- | --- |
| `3BIK` | `fef4588a21f5f508e02f219b4438cc669b42340d72e703e37f215299e33357e3` | `5f12ce3d7dfa98175c0084bc8ea0e298c04003bd9ba6eff54c12fb621d3a23c5` |
| `3Q0H` | `f5c4287c32f4faef0c79102b911d4136e426be2600ea3910ba8fe9c99b52d3bb` | `67f8e0cd1d32e32ac46f2423c844857e5a3790c9aee5920e953c3fccb2672042` |
| `3S2K` | `cbceb5a4ea214e2d048c5e2b63ef33290635a2488a93f1f914476c542c610c04` | `1f9632f01be9ac96191ea0e191f5e44821b55cfa1ae147267cb936933d2ec8fc` |
| `5MZV` | `17bef35c5be8ea815c79b028d072f18d1eb89b250a65f6a0e8897a880af3007a` | `7e1e98ae715e1e0e98aaef3f5140db3287f12264d8a724d9cd0b2d6be880def2` |
| `5O5G` | `203dc6c3c15d35fcc78479802e7bf5b3dafdbd31d85299698d6552a9091998dd` | `aa0ffec3e2c96e2b8be2ca5e48c947bc927bb78cdd1f7ce5c5bdcd09805dc879` |
| `5X83` | `788bb878c481b6b8aa078302f3916d9129394dadbb748847001e894c5db5ae74` | `379690a8ffa754e023cefdd7bba6fb0cf6ece018ea13ad48829639aaa05f0d5c` |
| `6IAA` | `a22740e91777638fb985875a8921b5ea9dd4c9bbe599f7fe213e82580d14f1e8` | `aff8af466d4f5e63d7b006520d8a2b9f65a8dd1346fa3aedfd8e10f2e0db2ef1` |
| `6TLA` | `3d9aa45f6a43c3bac03faeb561ec13c6b146ab11f66187a100e39540bbb51351` | `383105823fa370f70159fc1997f4b776c33b6c6458b90de3d1aeebb4a481f21e` |
| `6UMT` | `948cd4ed3a44bf40f8942196fdc0e1afb0c58b4ce46f19fef365b1689ea0222e` | `59e870b3704265d0d81bab6ee2c223ce5d3b24088c6d237ecf2c74b038cc2518` |
| `7OIX` | `e17e5f31c69e5eb677252b08b619b208c0f2644dee24266616bb6c0ba3c806a4` | `90c4a1ed48210867fb6722bcdd23ce2e4884c707c82f7233c1ca2b43e7bebe76` |

`pdb/` 共 20 个文件、9.83 MiB（10,308,636 bytes）。按相对路径排序，将每个文件序列化为 `relative_path<TAB>bytes<TAB>sha256<LF>` 后拼接，inventory SHA-256 为 `07017d98a964a50566a6e3a0a9becf39ec7759655bc11b990cf68bb5a1f2021e`。文件于 2026-09-17 从 RCSB 取得；未发布独立 manifest。

## 采集过程记录

- 2026-09-17 首次发布 `zenodo-15367597`：从 Zenodo 下载 24 个对象；从 FLAb 固定 commit 保存 20 张目标 CSV 和 4 个说明/许可文件；归档 bioRxiv v1 主文与补充材料，并补取十个靶点的 RCSB FASTA/mmCIF。Zenodo 对象按官方 MD5 和字节数、FLAb 文件按 Git blob SHA-1、PDF 按 SHA-256 验收。
- 2026-09-24 发现正式论文 key resources table 指向同一 concept DOI 下的后续数据 record `15707494`。核对确认旧 24 个对象未改变，新 record 只增加四张机器学习输入表；因此新建 `zenodo-15707494`，保留旧版本不覆盖。
- 同日归档正式发表版、独立补充信息和透明同行评审记录，并按正式论文列出的 Zenodo record `20060875` 归档代码 `v1.0.0`。代码 ZIP 的顶层目录对应 GitHub commit `cb07330a89a1c3338ef4cb86e9855646e503c535`。
- 重新审计 PDB 时使用已修正的逐 chain-instance 映射方法，并进一步核对 FASTA sequence 与 mmCIF entity canonical sequence；十个 mmCIF 也与 2026-09-24 的当前 RCSB 下载逐字节一致。审计确认没有旧脚本造成的错链，同时补记 DKK1 的人/鼠跨物种边界。
- 验收仍保留上游异常而不改 raw 字节，包括 FLAb inventory 行数漂移、EC50 favorable direction、29 条 ML-derived SPR 单位、重链 `CAR` 重复、论文质量控制汇总数和代码端到端复现缺口；处理状态集中列在正文和“待解决问题与处理进展”。

## 参考文献

- Zenodo 数据 record：<https://zenodo.org/records/15707494>
- Zenodo 数据历史 record：<https://zenodo.org/records/15367597>
- Zenodo 代码 record：<https://zenodo.org/records/20060875>
- bioRxiv v1：<https://www.biorxiv.org/content/10.1101/2025.05.15.650607v1>
- *Cell Systems* 正式论文：<https://doi.org/10.1016/j.cels.2026.101645>
- 作者代码仓库：<https://github.com/debbiemarkslab/ML-antibody-discovery>
- 作者代码固定 commit：<https://github.com/debbiemarkslab/ML-antibody-discovery/commit/cb07330a89a1c3338ef4cb86e9855646e503c535>
- FLAb 仓库：<https://github.com/Graylab/FLAb>
- FLAb 固定 commit：<https://github.com/Graylab/FLAb/commit/e05e3f0135783ffb7de412df6a1467e7a0031911>
- RCSB 条目：`5X83`、`3S2K`、`5MZV`、`6TLA`、`3BIK`、`6UMT`、`5O5G`、`6IAA`、`7OIX`、`3Q0H`

## 其他

### 数据范围和限制

- 可直接使用的核心实验层是 486 条候选的 PSR、SEC、SPR 和 cell-display 汇总；22 张选择汇总表与四张机器学习输入表提供这些候选之前的选择轨迹，但没有对全部库做逐条结合验证。训练/测试切分至少应按抗原、相似序列 cluster 和候选支路检查泄漏，不能把同一抗体在 EC50/SPR 两张 FLAb 表中的两行当成两个独立样本。
- 公开文件没有作者定义的统一 binder/non-binder 列。若项目需要二元任务，必须另行声明采用哪一种 assay、如何处理 `Fail`、单位异常和 QC，以及阈值如何确定；这种下游标签是项目构造，不是论文原生金标准。
- NGS 文件是作者从测序 reads 处理得到的氨基酸、模板、计数和 cluster 汇总；486 表又是选样、表达、测量和拟合后的汇总。两层都属于 `processed-public`，不能从当前文件重跑原始 read processing、FACS gating、SPR fitting 或 EC50 curve fitting。代码归档可以重跑公开表之上的特征和评分逻辑，但不能补回缺失的原始实验层。
- 论文指出低丰度序列可能受 PCR/测序错误及不同抗原池裂解时交叉污染影响。跨抗原共享的低计数 ARM 不能在不审计背景的情况下直接解释为交叉反应抗体。

### 完整性与验收

- Zenodo 28 个对象共 28.50 MiB（29,885,226 bytes），全部匹配 API 官方 MD5 和字节数；其中较早版本的 24 个对象字节不变。
- 代码 Zenodo ZIP 为 1,489,828 bytes，匹配官方 MD5，ZIP 无损坏成员；内含 13 个文件、4 个预训练模型参数和 MIT License。
- FLAb 20 个目标 CSV 与 4 个说明/许可文件全部匹配固定 commit tree。
- 27 个 Zenodo CSV、20 个 FLAb CSV 均可解析；XLSX ZIP 和工作簿内容可读取。
- bioRxiv 主文/补充材料为 12/23 页；正式版主文件、独立补充材料、透明同行评审记录为 44/22/28 页，所有页面均可提取文本。
- `pdb/` 的 20 个文件全部匹配固定哈希；11 条选定链通过 FASTA header、mmCIF author/label chain 和 canonical entity sequence 三方核对。
- 当前版本目录共有 79 个文件，其中 `pdb/` 下 20 个；所有相对路径唯一。临时 API 响应和验证输出未作为 source 文件发布。

### 许可和再分发边界

- 数据 Zenodo record 将 28 个对象标为 CC BY 4.0。
- bioRxiv 主文和补充材料标注 CC BY-NC 4.0。
- *Cell Systems* 正式论文及其补充材料标注 CC BY-NC-ND 4.0。
- 代码 Zenodo record 标注 MIT License，允许使用、修改和商用，但需保留版权及许可声明；这不改变输入数据和论文各自的许可。
- FLAb `data/README.md` 将该研究条目标为 CC BY-NC 4.0；顶层 `LICENSE` 只是指向逐数据集许可表，不是统一仓库许可。
- 各层声明不可互相替代。使用 Zenodo 原始数据对象时遵守 CC BY 4.0；商业使用或再分发 FLAb 派生 CSV 前按 FLAb 标注执行；论文 PDF 的非商业、禁止演绎限制不自动覆盖数据或 MIT 代码。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| NGS 轮次汇总计数 | 22 个 Zenodo CSV | 已包含 |
| 四个 campaign 的 ML 输入计数 | 4 个 `*_Test1_Lib31.csv` | 已包含；与 22 张汇总表有重叠，不是额外独立样本 |
| library chain/antigen keys | `0Library_keys.xlsx` | 已包含 |
| 486 个实验抗体的汇总表征 | `00Library_Biophysics_486Abs(1).csv` | 已包含 |
| logistic-regression 代码和预训练参数 | Zenodo `v1.0.0` ZIP | 已包含；缺依赖锁和部分物化输出，不能直接端到端复现 PD-L2 选样 |
| FLAb 的 EC50/SPR 训练表 | 20 个固定 commit CSV | 已包含，存在行数、方向、单位和重链拼接风险 |
| 原始 FASTQ | 当前 28 个 Zenodo 对象中未发现 | 未包含 |
| SPR sensorgram/拟合工程 | 当前公开包中未发现 | 未包含 |
| flow cytometry event、FACS gate 和完整滴定曲线 | 当前公开包中未发现 | 未包含 |
| assay replicate、误差和逐条失败原因 | 当前公开包中未发现 | 未包含 |
| 作者运行后生成的 `scores/`、`selected_abs/` 和完整选样审计轨迹 | 代码 ZIP 只保留空目录占位符；486 表只给最终候选 | 未包含 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-24；待上游口径确认）：Zenodo 主表与 FLAb 固定快照中，PD-L2 与 ROBO2N 的 29 条 ML-derived SPR 数值呈 M 量级；按 `kdis/ka` 复算也得到同一量级，但字段统一标为 nM，FLAb 继续按 nM 计算 `fitness`。当前保留上游原值，在下游将这些行单独标记，不与其余 SPR `fitness` 直接比较。下一步向原作者或 FLAb 维护者确认原始单位、换算意图与更正版本。
- `Q02`（最近更新：2026-09-24；待上游序列确认）：FLAb 的 385 个唯一 `heavy` 全部由“末端已含 `CAR` 的 VH 模板 + 以 `CAR` 起始的 `CDRH3` + J 区后缀”拼成，因而出现 `YYCARCAR`；Zenodo 工作簿还把论文/CSV 的 `VK4-1` 写作 `VK14-1`。当前不原地修正，processed 层若需完整 VH 应显式采用单一边界约定并记录版本。下一步向 FLAb 维护者确认重链拼接规则，并向原作者确认工作簿轻链名称。
- `Q03`（最近更新：2026-09-24；代码复现缺口）：代码 `v1.0.0` 已成功归档，不再是“下载不到”。但归档没有依赖锁或运行后评分/选样文件，且当前候选选择循环只处理 ROBO1 和 ROBO2N，没有直接输出论文中的 33 条 PD-L2 补选候选；`Aff3_Macs1` 的实现还调用 `calc_enrichment(..., "Macs1", "Aff2")` 而非 `Aff3`。当前将代码用于核对公开方法和输入输出边界，不把它宣称为无需修改即可完整复现。下一步向作者确认 PD-L2 选样脚本及 `Aff3_Macs1` 行是否为笔误。
