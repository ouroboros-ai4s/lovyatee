---
tags:
  - context
---

# SRC_R01_IGDESIGN 数据说明

- [SRC\_R01\_IGDESIGN 数据说明](#src_r01_igdesign-数据说明)
  - [数据集身份](#数据集身份)
    - [来源方背景](#来源方背景)
  - [实验设计和数据口径](#实验设计和数据口径)
    - [设计问题、候选与对照](#设计问题候选与对照)
    - [从计划文库到公开记录](#从计划文库到公开记录)
    - [高通量 SPR 的样品与测量流程](#高通量-spr-的样品与测量流程)
    - [SPR 标签与解释边界](#spr-标签与解释边界)
    - [IL17A 外部序列参考](#il17a-外部序列参考)
  - [论文原文](#论文原文)
  - [仓库内容](#仓库内容)
  - [数据结构](#数据结构)
    - [CSV 文件与记录口径](#csv-文件与记录口径)
    - [序列与盲化范围](#序列与盲化范围)
    - [SPR 标签](#spr-标签)
    - [scRMSD 派生字段](#scrmsd-派生字段)
    - [字段说明](#字段说明)
    - [数据示例](#数据示例)
  - [PDB 数据库](#pdb-数据库)
    - [SAbDab2 抗体实例注释](#sabdab2-抗体实例注释)
  - [采集过程记录](#采集过程记录)
  - [参考文献](#参考文献)
  - [其他](#其他)
    - [数据范围和限制](#数据范围和限制)
    - [完整性与验收](#完整性与验收)
    - [许可和再分发边界](#许可和再分发边界)
    - [公开范围对照](#公开范围对照)
  - [待解决问题与处理进展](#待解决问题与处理进展)

## 数据集身份

- `source_id`：`SRC_R01_IGDESIGN`
- `source_version`：`snapshot-2025-01-10`
- 原作者或发布机构：Absci Corporation（Amir Shanehsazzadeh 等研究者）

### 来源方背景

Absci Corporation 于 2011 年以 AbSci, LLC 的形式创立，总部位于美国华盛顿州温哥华；截至 2026-09-21，其普通股在纳斯达克全球精选市场以 `ABSI` 交易，见[投资者常见问题](https://investors.absci.com/resources/investor-faqs)。[纳斯达克行情摘要](https://api.nasdaq.com/api/quote/ABSI/summary?assetclass=stocks)显示，Absci 于 2026-09-21 收盘后的市值约为 16.85 亿美元。公司目前以生成式 AI 设计生物药，处于临床研发阶段。其[2025 年全年业绩公告](https://investors.absci.com/news-releases/news-release-details/absci-reports-business-updates-and-fourth-quarter-and-full-1)列示合作项目收入 280 万美元、研发费用 8,140 万美元和净亏损 1.152 亿美元（均为截至 2025-12-31 的财年口径），说明其经营仍以研发投入和合作项目为主。

在抗体设计方面，Absci 的[技术介绍](https://www.absci.com/technology/)描述了生成式模型与高通量实验相衔接的平台。[官方论文列表](https://www.absci.com/publications/)收录 IgDesign；[IgDesign 原论文](https://www.absci.com/wp-content/uploads/2024/05/IgDesign-Antibody-inverse-folding-with-in-vitro-validation-1.pdf)由 Amir Shanehsazzadeh 等人报告抗体逆折叠设计及体外验证。除自有研究外，Absci 于 2024 年宣布与[纪念斯隆凯特琳癌症中心合作](https://investors.absci.com/news-releases/news-release-details/absci-collaborates-global-cancer-center-discover-novel)，运用生成式 AI 探索新的治疗性抗体。

## 实验设计和数据口径

### 设计问题、候选与对照

这项研究以 8 个已有实验复合物结构的参考抗体-抗原系统为起点，研究的是已知复合物背景下的重链 CDR 序列重设计，而不是从单独的抗原出发设计完整抗体。IgDesign 以复合物骨架、抗原序列和参考抗体 framework 序列为条件，为各系统生成重链 CDR 候选。8 组评估采用相同方法，但分别训练一套 IgMPNN 和 IgDesign 模型：每次从训练集中留出与当前靶点相关的抗原条目，再在该靶点上评估设计表现。

论文对每个抗原生成 100 万条模型输出，再按最低 cross-entropy loss 选择 100 条 HCDR3 设计和 100 条 HCDR123 设计用于体外评估。HCDR3 设计只替换当前系统参考抗体的 HCDR3；HCDR123 设计同时替换 HCDR1、HCDR2 和 HCDR3；未替换的重链 framework、轻链和相应 CDR 沿用参考抗体。这里的 100 万条是每个靶点的模型生成规模，不是 SPR 实测记录数。

作为比较基线，作者还为每个靶点抽取 100 条 SAbDab HCDR3：先从对应模型的训练集选取与参考抗体 HCDR3 等长的片段；数量不足时，依次补入验证集的等长片段、训练集中长度相差一个残基的片段（论文附录 C）。这些片段同样被置入当前参考抗体背景，只替换 HCDR3。SAbDab 组不是 IgDesign 生成的设计，也不是预先认定的 non-binder；它是用来检验结构和靶点条件化设计是否优于自然抗体片段的比较组，其结合标签仍由后续 SPR 测量产生。

因此，每个靶点的名义实验文库由 100 条 IgDesign HCDR3、100 条 IgDesign HCDR123 和 100 条 SAbDab HCDR3 组成，8 个靶点合计 2,400 条候选文库条目，不包含 assay control。公开 CSV 中每个系统另有 1 条 `Positive Control`，即保留参考抗体 HCDR 的已知 binder，不属于模型设计或 SAbDab 基线。论文附录 C 说明各文库设置 mAb 阳性对照、Fab 阳性对照和 Fab 阴性对照（CD40 不含 mAb 阳性对照）；但公开 CSV 每个系统只有 1 条未注明形式的 `Positive Control`，没有可映射的 Fab 阴性对照记录。

### 从计划文库到公开记录

作者把 HCDR1 至 HCDR3 区域的 DNA 变体克隆为 Fab，在 *E. coli* 中表达并进行高通量 SPR，随后对配套样本测序以确定实际氨基酸序列。论文附录 D.4 说明，测序后会根据主要与次要序列的丰度及序列差异判断样本是否可视为克隆群体；若样本的主导氨基酸序列无法匹配任何预期设计，则丢弃该样本。因此，“每个系统计划 300 条、合计 2,400 条”描述的是名义候选文库规模，论文表 3 和公开 CSV 统计的则是经过实验与测序处理后保留下来的结果记录。

从 2,400 条名义候选到公开记录的计数关系如下：

```text
名义候选文库（不含 assay controls）
8 个靶点 ×（100 IgDesign HCDR3 + 100 IgDesign HCDR123 + 100 SAbDab HCDR3）
= 2,400 条候选文库条目
    │
    └─ DNA 克隆为 Fab → E. coli 表达 → 高通量 SPR → 配套样本测序与序列质控
       各阶段留存数未公开；附录 D.4 明确记录的排除情形之一是
       “主导氨基酸序列无法匹配任何预期设计”
        │
        ├─ 论文表 3：1,437 条候选记录（278 binder）
        │
        └─ 公开 CSV：1,436 条候选记录（278 binder + 1,158 non-binder）
           ├─ IgDesign HCDR3：495（165 binder）
           ├─ IgDesign HCDR123：488（110 binder）
           └─ SAbDab HCDR3：453（3 binder）
                │
                └─ 再加入 8 条参考阳性对照（均为 binder；不属于上述 2,400 条）
                    = 公开 CSV 共 1,444 行（286 binder + 1,158 non-binder）
```

论文表 3 与公开 CSV 的对应关系如下；括号内为其中的 binder 数：

| 统计口径 | IgDesign HCDR3 | IgDesign HCDR123 | SAbDab HCDR3 | 三类候选合计 | 阳性对照 | 全部记录 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 论文表 3 | 495（165） | 489（110） | 453（3） | 1,437（278） | 未列入 | 1,437（278） |
| 公开 CSV | 495（165） | 488（110） | 453（3） | 1,436（278） | 8（8） | 1,444（286） |

两种口径唯一的分组数量差异在 C5 的 HCDR123 组：论文为 7/68，公开 CSV 为 7/67。这解释了为什么论文三类候选合计 1,437 条，而 CSV 只有 1,436 条非对照记录；CSV 再加入 8 条阳性对照后才得到 1,444 行，因此“CSV 比论文多 7 行”不表示多公开了 7 条候选。

**从名义文库的 2,400 条到公开候选的 1,436 条，数值上相差 964 条；公开材料没有给出这 964 条的逐条去向或克隆、表达、SPR、测序与质控各阶段的损耗数量。** 已知的序列不匹配过滤只能解释其中一种排除情形，不能据此把全部差额归因于该步骤，也不能把这 964 条统称为实验 non-binder。事实上，公开 CSV 已经保留了 1,158 条候选 non-binder；这里缺少的是可发布、可分析记录，而不是一个额外的阴性类别。论文也没有提供 2,400 条名义候选与 1,436 条公开记录的逐条映射，因此公开 binder rate 的实测分母应按当前可分析的候选记录定义，不能直接使用 2,400 条名义文库条目或每靶点 100 万条模型输出。论文表 4 中 ACVR2B 的 HCDR123 显著性数值也无法从表 3 所列计数复现，详见文末 Q04。

### 高通量 SPR 的样品与测量流程

本来源的候选筛选采用从细菌裂解液捕获 Fab 的高通量 SPR（high-throughput surface plasmon resonance，HT-SPR）。SPR 通过芯片表面的实时光学响应观察分子的结合与解离。归档 bioRxiv v2 附录 D.1—D.3（第 15—16 页）描述了候选以 Fab 形式在大肠杆菌中表达，随后裂解、离心去除不溶物、加入 SPR 缓冲液并过滤，再将裂解样品转入 384 孔板供 Carterra LSA 测量；该候选流程在裂解后直接进入芯片捕获，没有逐个候选先纯化 Fab 的独立步骤。

Carterra LSA SAD200M 芯片先用生物素化抗体捕获试剂处理，再从裂解样品中捕获 Fab 并进行洗涤与基线稳定。随后注入 ACRO Biosystems 提供的对应靶抗原胞外结构域，使用 5 个浓度：从 500 nM 配制 3 倍系列稀释，记录 300 秒结合和 900 秒解离阶段的响应。此时 Fab 位于芯片表面，设定浓度的抗原是流过表面的分析物。论文没有给出这些抗原试剂的逐系统 catalog、批次、实际序列、标签、纯度或寡聚状态。[Carterra 平台说明](https://carterra-bio.com/lsa/)表明，LSA 通过芯片上不同位置的阵列和成像读出并行监测相互作用；平台容量不能用来反推本数据每次运行的样本数或批次对应关系。论文只给出捕获试剂的类别，具体试剂身份及逐候选捕获量未在公开材料中明确。

论文将该测量称为 non-regeneration kinetics（非再生动力学）。这种滴定方式在同一浓度系列的各次注射之间不安排再生步骤，分析需考虑残余结合状态；相关方法解释见 [TitrationAnalysis 方法论文](https://pmc.ncbi.nlm.nih.gov/articles/PMC10667272/)。R01 的完整测量周期仍包含芯片再生，附录 D.3 明列“配体固定、空白注射、抗原注射、芯片再生”及跨运行重复设计。因此，非再生描述的是浓度系列内的安排。该通用方法文献用于解释术语，不证明 R01 使用了其中的软件或拟合模型。

HT-SPR 属于 SPR；裂解液捕获和非再生操作本身不能作为判定数据低质量的依据。在遵守适当实验设计与分析要求时，LSA 可以获得动力学和亲和力参数，已有 [LSA 与 Biacore 8K 的直接比较研究](https://doi.org/10.1177/2472555220934814)提供方法层面的验证。R01 每条结果的可靠性仍需结合本批测量的捕获水平、参考扣除、曲线及拟合质量评估；其他平台验证研究不能替代本批逐条验收。

### SPR 标签与解释边界

上述 HT-SPR 流程直接产生随时间变化的响应曲线，即 sensorgram。“某个重复观察到结合”是作者对该次曲线给出的实验判定，`KD` 则是作者从浓度系列响应中拟合并汇总报告的亲和力参数。当前 CSV 的 KD 应理解为该表面捕获实验体系下的作者报告值；公开包没有逐候选纯化后独立复测的对应证据，不能据此认定已获得与实验体系无关的本征亲和力，也不能仅因采用 HT-SPR 就统一改称表观 KD。

论文和公开包没有给出逐曲线的阳性阈值、`KD` 拟合模型、残差、置信区间或质量验收标准，也没有可逐候选对应的表达量、活性评估和芯片捕获水平。测量温度与 pH 未明确报告；培养或裂解温度不能替代 SPR 温度。因此，当前公开表支持使用作者发布的重复级判定及其汇总结果，但不足以独立复核每条曲线和拟合。相关证据缺口及后续核实事项集中跟踪于文末 Q07。

从该样品制备与捕获流程作方法学判断，表达、折叠、捕获不足以及结合本身较弱都可能影响可观察信号；这些是需要区分的可能因素，不是已经证实发生于某条记录的失败原因。缺少上述逐候选质控资料时，不能把所有阴性都归为序列本身不结合，也不能反过来擅自标为表达失败。

公开 CSV 同时包含三类候选记录和参考阳性对照，两类记录的 `Binder` 采用不同口径。对三类候选，只有全部 SPR replicate 都观察到结合时，`Binder` 才为 `True`；公开 CSV 的候选行与这条规则一致。因此，`Binder=False` 不一定表示“所有重复均未结合”：公开表有 73 条 `Binder=False` 候选仍给出 KD，说明其中至少部分重复产生了可定量的结合结果。`KD (nM)` 是观察到结合的重复实验所得 KD 的平均值，空 KD 表示没有定量值，不是 0。

参考阳性对照用于确认 assay 能识别已知 binder，其 `Binder` 保留预先设定的阳性对照身份，不再按候选的“全部重复均结合”规则重新判定。因此，ACVR2B 的参考阳性对照虽然只有 14/16 个重复观察到结合，仍标为 `Binder=True`；这里的 `True` 表示该行属于已知阳性对照，并不表示 16 个重复全部观察到结合。在候选记录中，`Binding Replicates`、`Replicates` 和 `Ratio Binding Replicates` 直接参与 `Binder` 判定；更一般地，这些字段本身是下游实验结果，不能作为预测 `Binder` 或 `KD` 的输入特征。

公开 CSV 还有 3 条 IgDesign HCDR3 记录报告 1/1 次结合并标为 `Binder=True`，分别来自 ACVR2B、CD40 和 TNFRSF9；论文附录 D.3 说明少数样本使用单个 replicate。其中 ACVR2B 和 TNFRSF9 的两条记录，公开的 HCDR1、HCDR2、HCDR3 与各自系统的阳性对照相同。相关重复性与分组问题分别保留在文末 Q05、Q06。

公开数据中的“盲化”发生在序列发布环节：CD40–Ravagalimab 系统的设计 HCDR 按实际替换区域写为 `X`，阳性对照和未被设计的参考 HCDR 仍保留原序列，SPR 测量结果与结合标签继续公开。这样可以比较该系统的实验结果，但无法根据公开表分析被遮蔽的设计序列。作者仓库未说明选择这一系统遮蔽序列的具体原因，也未描述 SPR 测试时采用实验人员盲法；逐行遮蔽范围见下文“序列与盲化范围”。

`scRMSD` 是作者用预测 Fv 相对参考实验结构计算的派生结构偏差，不是 SPR 实验值，也不是结构模型直接输出的置信度。8 个参考复合物有实验坐标，但 1,444 条公开记录并不各自对应一份实验结构。

当前 source 保存固定 Git 仓库及其中的处理后实验汇总，项目口径为 `processed-public` raw input。8 个代表性 sensorgram PDF 仅覆盖部分测量；逐行、逐 replicate 的 SPR 仪器原始导出未公开。

### IL17A 外部序列参考

IgDesign 论文和 `Afasevikumab-IL17A.csv` 将该系统靶点报告为 IL17A，而论文引用的 `6PPG`
抗原实体是 IL17F；两侧冲突及实验材料缺口继续由 Q01 跟踪。为固定可复核的人 IL17A 序列参考，
项目于 2026-10-15 从 UniProtKB REST API 取得 reviewed 条目 `Q16552` 的完整 JSON 与 canonical
FASTA。该条目的 `entryVersion=209`、`sequenceVersion=1`，canonical sequence 为 155 aa；官方
feature 将 1—23 标为 signal peptide，将 `PRO_0000015423` 的 24—155 标为 mature chain。

| 文件 | 大小 / SHA-256 | 作用 |
| --- | --- | --- |
| `uniprot/records/Q16552.json` | 57.67 KiB（59,050 bytes） / `318600fd1e50a7968ed8a7c4fd94cbdb5048b1875f0c884b6d21525718f23c63` | 固定条目身份、版本、完整序列及 feature 区间 |
| `uniprot/sequences/Q16552.fasta` | 239 bytes / `adba67673d8cbcb6c28a7b6d73dbb45482949b8b58f8d1aa36d084968f4fec78` | 固定 UniProt canonical FASTA 原始字节 |
| `uniprot/manifest.json` | 1.46 KiB（1,491 bytes） | 固定 UniProt release、选择区间、公共内容寻址路径和两份原始响应的哈希 |

JSON 与 FASTA 均来自 UniProt release `2026_03`，来源目录通过硬链接引用
`data/raw/reference/uniprot/Q16552/` 中的内容寻址对象。按官方 feature 从完整序列取 24—155
得到 132 aa mature sequence；其无换行序列 SHA-256 为
`05feac071264f46588ee51cffcfd74552cc224bbdb3e3490fe36680428444110`。这项外部证据为后续处理
提供固定参考，不表示 IgDesign 作者交付了该序列，也不证明实际 SPR 抗原试剂与 `Q16552`
mature chain 逐残基一致。

## 论文原文

- 标题：*IgDesign: In vitro validated antibody design against multiple therapeutic antigens using inverse folding*
- 作者：Amir Shanehsazzadeh et al.
- 发表来源：bioRxiv
- 归档文本版本：预印本 v2
- 发布日期：2024-12-14
- DOI：`10.1101/2023.12.08.570889`
- PMID / PMCID：无
- 本地文件：`articles/IgDesign_2024-12-14_bioRxiv-v2.pdf`
- 文件大小：39.60 MiB（41,525,940 bytes）
- SHA-256：`7ce3a3a6c96b2459d0247b1f9a04a7a17739068c69d1df1c28b86b8abc4d57c1`
- 文本许可：CC BY-NC-ND 4.0
- 补充材料：无独立补充包；主 PDF 的附录 A—E 涵盖建模方法、数据整理与划分、抗体文库设计、湿实验流程及结果分析
- 引用数（查询快照）：27（[OpenAlex W4389515053](https://openalex.org/W4389515053)，查询于 2026-09-21）

归档文件名采用 bioRxiv v2 的发布日期 `2024-12-14`；DOI 中的 `2023.12.08` 保留为论文标识的一部分。文件由 bioRxiv 原始下载名 `2023.12.08.570889v2.full.pdf` 改名，字节和哈希未变。

## 仓库内容

上游来源为 `AbSciBio/igdesign`。本 source 固定 commit `70431eef0afaf0496d7d84e22dfdc1980ec9e70e`；commit 日期为 2025-01-10，因此命名为 `snapshot-2025-01-10`。`igdesign/` 保留完整固定 Git 快照，无 LFS pointer 或 submodule；模型 checkpoint 下载脚本未执行。

```text
snapshot-2025-01-10/
└── igdesign/
    ├── data/
    │   ├── *.csv                         7 个未盲化系统
    │   ├── Blinded/
    │   │   └── Ravagalimab-CD40.csv     1 个设计 HCDR 盲化系统
    │   └── Sensorgrams/
    │       └── *.pdf                    8 个代表性 sensorgram
    ├── configs/
    ├── examples/
    ├── igdesign/
    ├── README.md
    └── LICENSE
```

固定 tree 有 47 个 tracked 文件。`igdesign/data/` 的 8 个 CSV 与 8 个 sensorgram PDF 共 16 个文件、2.24 MiB（2,345,336 bytes）。`examples/` 的两个 PDB 是推理示例，不是 8 个参考复合物或全部公开记录所对应抗体的结构集合。

## 数据结构

### CSV 文件与记录口径

| 文件 | 行数 | 实验系统 |
| --- | ---: | --- |
| `igdesign/data/Afasevikumab-IL17A.csv` | 179 | IL17A |
| `igdesign/data/Bimagrumab-ACVR2B.csv` | 212 | ACVR2B |
| `igdesign/data/Blinded/Ravagalimab-CD40.csv` | 201 | CD40，设计 HCDR 盲化 |
| `igdesign/data/Eculizumab-C5.csv` | 198 | C5 |
| `igdesign/data/Osocimab-FXI.csv` | 116 | FXI |
| `igdesign/data/Spesolimab-IL36R.csv` | 177 | IL36R |
| `igdesign/data/Tezepelumab-TSLP.csv` | 176 | TSLP |
| `igdesign/data/Utomilumab-TNFRSF9.csv` | 185 | TNFRSF9 |

8 张表 schema 相同，均为 47 列：12 个实验、序列和 SPR 字段，加 35 个 scRMSD 派生字段。每行是一条“参考抗体背景 + 已发布 HCDR + 该系统实验结果”的记录，不是完整抗体序列，也不是独立结构样本。每张表对应一个靶点，SPR 结果只记录候选与该靶点的结合情况；公开文件未提供这些候选对其余靶点的测量。

### 序列与盲化范围

公开 CSV 只给 `HCDR1`、`HCDR2`、`HCDR3`，不含完整重链可变区、完整轻链可变区、framework、LCDR 或全长抗体。数据范围不表示 IgDesign 模型只能处理 HCDR；它只反映本次体外构建和公开文件的范围。

`Blinded/Ravagalimab-CD40.csv` 并非把所有序列统一写成 `X`。阳性对照保留三条 HCDR；136 条 HCDR3 设计保留参考 HCDR1/2，只把 HCDR3 写成 `XXXXXXXXX`；64 条 HCDR123 设计分别写成 `XXXXXXXX`、`XXXXXXXX`、`XXXXXXXXX`。未设计的参考 HCDR 仍可见。

### SPR 标签

| 字段 | 实验含义 |
| --- | --- |
| `KD (nM)` | 作者报告的本 HT-SPR 体系下的 KD，由 sensorgram 拟合并在有定量值的重复间取平均，单位 nM；越小通常表示亲和力越强，逐条拟合质量尚不能独立复核 |
| `Binding Replicates` | 作者判为观察到结合的 SPR 重复数 |
| `Replicates` | 重复总数 |
| `Ratio Binding Replicates` | 结合重复数占总重复数的比例 |
| `Binder` | 实验二元标签；非对照必须全部重复结合才为 `True` |

### scRMSD 派生字段

`scRMSD` 全称为 self-consistency RMSD（自洽均方根偏差）。35 个字段由 5 个区域与 7 个模型或汇总策略组合：区域为 `HCDR1`、`HCDR2`、`HCDR3`、`HCDR123`、`Fv`；模型为 `ABB2`、`ABB3`、`ABB3-LM`、`ESMFold`，汇总策略为 `Mean Ensemble`、`Min Ensemble`、`Max Ensemble`。

作者先从各抗体变体的重链、轻链可变区序列预测 Fv，再以 C-alpha 原子 Kabsch 对齐到参考抗体实验结构，并计算各区域 RMSD。参考 PDB 中缺失的 FWR 残基不参与。三个 Ensemble 字段是同一行、同一区域四个模型值的均值、最小值和最大值，不是三个额外模型；该关系已对 6,795 个数值完整的行-区域组合复核。

### 字段说明

以下字段适用于上列 8 张同构 CSV，共 47 列。前 12 列逐项列出；后 35 列遵循原始列名规则 `{区域} scRMSD ({后缀})`：`{区域}` 取 `HCDR1`、`HCDR2`、`HCDR3`、`HCDR123`、`Fv`，`{后缀}` 取 `ABB2`、`ABB3`、`ABB3-LM`、`ESMFold`、`Mean Ensemble`、`Min Ensemble`、`Max Ensemble`。这 5 × 7 个组合与实际表头逐一对应。

| 原始字段或字段组 | 原始表示、单位与含义 | 缺失、特殊编码与来源 |
| --- | --- | --- |
| `Target` | 文本；该行接受 SPR 测试的抗原靶点 | 无空值；作者提供的实验系统标识 |
| `Reference Ab` | 文本；提供当前系统抗体背景的参考抗体名称 | 无空值；作者提供的实验系统标识 |
| `Method` | 文本枚举：`Positive Control`、`SAbDab`、`Inverse Folding`；标记对照或候选序列来源 | 无空值；作者提供的分组标识 |
| `HCDRs Designed` | 文本枚举：`HCDR3`、`HCDR123`；标记替换的重链 CDR 范围 | 8 条阳性对照为空；作者提供的设计范围标识 |
| `HCDR1` | 氨基酸序列文本；重链第一 CDR | 无空值；CD40 系统被设计的位置可用 `X` 遮蔽，来源为作者公开的序列列 |
| `HCDR2` | 氨基酸序列文本；重链第二 CDR | 无空值；CD40 系统被设计的位置可用 `X` 遮蔽，来源为作者公开的序列列 |
| `HCDR3` | 氨基酸序列文本；重链第三 CDR | 无空值；CD40 系统被设计的位置可用 `X` 遮蔽，来源为作者公开的序列列 |
| `KD (nM)` | 数值；作者报告的本 HT-SPR 体系下的 KD，由 sensorgram 拟合并在有定量值的重复间取平均，单位 nM；越小通常表示亲和力越强 | 1,085 行为空，表示未给出定量值；另有 73 行 `Binder=False` 仍有数值；来源为 HT-SPR 测量汇总，曲线级拟合、捕获水平与验收细节未公开 |
| `Binding Replicates` | 数值，语义为次数；作者判为观察到结合的 SPR 重复数 | 无空值，CSV 中可写作 `2.0`；来源为 SPR 测量汇总 |
| `Replicates` | 数值，语义为次数；SPR 重复总数 | 无空值，CSV 中可写作 `2.0`；来源为 SPR 测量汇总 |
| `Ratio Binding Replicates` | 0 至 1 的数值；结合重复数除以重复总数，无单位 | 无空值；由前两列重复数派生 |
| `Binder` | `True` 或 `False`；结合结果的二元标签 | 无空值；作者依据 SPR 重复结果判定，非对照需全部重复观察到结合 |
| `{区域} scRMSD ({模型})`（20 列） | `{模型}` 依次取 `ABB2`、`ABB3`、`ABB3-LM`、`ESMFold`；各模型预测结构相对参考实验结构的区域偏差，数值单位 Å，越小表示结构越接近 | 35 个 scRMSD 列在相同的 85 条 SAbDab 基线记录中为空；来源为结构预测后的计算值 |
| `{区域} scRMSD ({汇总策略})`（15 列） | `{汇总策略}` 依次取 `Mean Ensemble`、`Min Ensemble`、`Max Ensemble`；同一区域四个模型 scRMSD 的均值、最小值和最大值，数值单位 Å | 与上组在相同 85 行为空；来源为四个计算值的统计汇总 |

### 数据示例

以下真实记录取自 `igdesign/data/Afasevikumab-IL17A.csv`，只展示核心字段：

| 角色 | `Method` | `HCDRs Designed` | `HCDR3` | `KD (nM)` | 结合/总重复 | `Binder` |
| --- | --- | --- | --- | ---: | --- | --- |
| 参考阳性对照 | `Positive Control` | 空 | `ARDIGGFGEFYWNFGL` | 1.2625 | 16 / 16 | `True` |
| IgDesign binder | `Inverse Folding` | `HCDR3` | `ARDVGADGLYYFVFDL` | 244.0 | 2 / 2 | `True` |
| IgDesign non-binder | `Inverse Folding` | `HCDR3` | `ARDVGGSGLYYFVFDL` | 空 | 0 / 2 | `False` |
| SAbDab baseline | `SAbDab` | `HCDR3` | `ARKGSDRLSDNDPFDA` | 空 | 0 / 2 | `False` |

四行的 `HCDR1=GFTFDDYA`、`HCDR2=INWSSGGI`。它们共享 IL17A/Afasevikumab 实验系统，但序列来源和结合结果不同；空 KD 不得转成 0。

## PDB 数据库

论文 Table 2 给出 8 个共享参考复合物及各自的重链、轻链、抗原 author chain。映射强度为“一张数据 CSV 对应一个参考复合物”，不是 1,444 条记录各自有一个结构。2026-09-16 从 RCSB 取得这 8 个条目的 canonical entity 序列和完整 mmCIF。2026-10-15 的结构覆盖复核另确认 5NHW、6PE7 是分别与 Bimagrumab、Ravagalimab 参考抗体序列相符、且没有抗原共同沉积的独立 Fab 条目；这两项是结构补充证据，不改变论文的 8 个系统映射。

| 系统 | PDB | author chains H/L/Ag | FASTA 大小 / SHA-256 | mmCIF 大小 / SHA-256 |
| --- | --- | --- | --- | --- |
| Ravagalimab-CD40 | `6PE8` | `A/B/U` | 864 bytes / `8b23fd39953f083230d87c1eb476d39bbb6b2333939f79247b73dddd55a974f3` | 958.11 KiB（981,102 bytes） / `d7537daa97e775aa5f680de64e164004f44f45041ac12508fbb58da0d44d45b7` |
| Spesolimab-IL36R | `6U6U` | `H/L/R` | 881 bytes / `8fd7f7c596f5522ebd0edfdaedb328fb863c4e5dbf2f56ebea7388d542a8c62e` | 1012.17 KiB（1,036,466 bytes） / `9eec3a5baee92e769460d870b4ac0df424d6f69880c4b742eddb6048a9959137` |
| Eculizumab-C5 | `5I5K` | `H/L/B` | 2.32 KiB（2,377 bytes） / `07d8d17e33d3581cd78bbf0587e0a9c18e42e3e4e5de6d3fa6dcbf972777dd97` | 5.98 MiB（6,269,989 bytes） / `0052dcff8e3ddad5ca3e5ec26e6e5eab451bc26769c7862b5affe35909e7c5df` |
| Tezepelumab-TSLP | `5J13` | `C/B/A` | 867 bytes / `45d4071b39d33580b147ab36844c4af484e2b2882db56affd237356ac8947923` | 827.04 KiB（846,893 bytes） / `438291af87290feaf94ed02c76401eeb14dea352cec680f268bcb9161f587827` |
| Afasevikumab-IL17A | `6PPG` | `B/A/G` | 828 bytes / `1f363b1f6f0fb7d6201602fa1199279e943fb19c47d52beae1a1c9ab8325730f` | 943.24 KiB（965,875 bytes） / `3248c1dc463038e3260106a6b906c305509fdffc908a6d5c8047baa96ca66261` |
| Osocimab-FXI | `6HHC` | `H/L/A` | 917 bytes / `d1b79517586d2dcea9af17865ba128d784a05cf095f08c39d6b1fdf6b264c74e` | 977.75 KiB（1,001,214 bytes） / `6f36fea5c373cb6d861eb02a8e85091e2da45e152cfad3716275aa26b438273f` |
| Bimagrumab-ACVR2B | `5NGV` | `H/L/A` | 587 bytes / `5c5bad7506fe69f827c2a38553f5edcab2f450278d6e4b27100ff5f93961d6eb` | 536.29 KiB（549,158 bytes） / `2d293aeba02152ea0b0ea72ecec7f4af3af77096854628d649ef4bbeffed4ae3` |
| Utomilumab-TNFRSF9 | `6A3W` | `A/B/C` | 640 bytes / `bd9183890d91950083d2794199cc30cdfcc3ab3e46372a9a8b5647f5454982bb` | 2.06 MiB（2,157,512 bytes） / `bcceba354205a9f6c05cc619971a26ab9ae25c5b0f8c53734a8c27bc2b551a96` |
| Bimagrumab 独立 Fab | `5NHW` | `H/L/—` | 632 bytes / `097602376ff926b29c260d7d6c44db0fa48f7560477441160b12b6bc9b8bca75` | 425.03 KiB（435,229 bytes） / `7b6db6cc5df78e7bd1307846e18bc732b940b0e725dc4d88c322fab81820c985` |
| Ravagalimab 独立 Fab | `6PE7` | `H/L/—` | 565 bytes / `d128895a97a5e3c97aa742e26e2c118df418252fbf0cce1a7c0182b72df6b8ac` | 426.20 KiB（436,429 bytes） / `c3944663ec70537a1fa7acf32e5dc48ef23fe4d89ef0fec6c5766c3446063801` |

10 份 FASTA 与 10 份 mmCIF 的解压内容合计 14.01 MiB（14,689,025 bytes）。FASTA 位于 `pdb/sequences/rcsb_pdb_<PDB ID>.fasta`，压缩 mmCIF 位于 `pdb/structures/<PDB ID>.cif.gz`。除 5J13、5NHW、6PE7 外，FASTA 是项目从 RCSB canonical entity 序列生成的选链视图，header 记录 role、complex、author chain 和 label asym；5J13、5NHW、6PE7 保存 RCSB entry FASTA。5J13 header 只有 `Chain A/B/C`，没有显式 author→label 字段，其 Table 2 author chain 到实际 `label_asym_id` 的对应来自 mmCIF `_atom_site` 核验。`5I5K` 的抗原 author chain `B` 对应 mmCIF label asym `A`，同样以 mmCIF 记录为准。

这些 canonical 序列表示参考结构构建体的 deposited sequence，可包含恒定区片段或坐标未解析残基；临床抗体全长序列需另行取得与核验。`6PPG` 的 RCSB antigen entity 描述为 Interleukin-17F，而 IgDesign `Target` 为 IL17A；两侧原文及待核问题见 Q01。10 个条目均同时具备 FASTA 和 mmCIF；`pdb/manifest.json` 记录数据集路径、公共内容寻址路径和内容 SHA-256。

### SAbDab2 抗体实例注释

2026-10-15 从 SAbDab2 按 Table 2 的 H/L author chain 和两份独立 Fab 的 H/L chain 固定 10 个
antibody instance。这里的 SAbDab2 外部注释与 CSV `Method=SAbDab` 的基线设计不是同一个
对象：前者用于核验参考结构中的重轻链配对、可变域和 IMGT 注释，后者是 IgDesign 实验文库的
一类候选。5I5K、6PE8、6PPG 和 6A3W 各含多个抗体坐标副本，因此选择同时固定 PDB ID 与
instance ID，不能只靠 PDB ID 还原。

| PDB | antibody instance | SAbDab2 ID | 实例类型 | annotation JSON 大小 / SHA-256 | summary CSV 大小 / SHA-256 |
| --- | --- | --- | --- | --- | --- |
| `5I5K` | `pdb_00005i5k-H-L` | `sabdab2_H0171L0117` | `FAB` | 35,068 bytes / `38e5db44be9a43785b77889765a4334939432553550dc9cd33928c288cbf2026` | 1,417 bytes / `36f7f1f2e876f6b7d2bf33b3b3f6def3e5e5607482f962d773d676f88510d8d8` |
| `5J13` | `pdb_00005j13-C-B` | `sabdab2_H01J9L019F` | `FAB` | 12,432 bytes / `c49f2e191b44b88188410de8ff2c16719dcc9eeb2dd48a5c6fe039d13379426d` | 1,505 bytes / `2b106caf1645bc13681557e9e780d4a06436bb9bf4f8ee0a213d27b87124beda` |
| `5NGV` | `pdb_00005ngv-H-L` | `sabdab2_H01EWL0177` | `FV` | 13,204 bytes / `f156870683e73c1a481b077ad40faf81fe8e1404c70a429a010cb433daaa5172` | 1,545 bytes / `16ab2133c1be0e9b8c7dc292b55d1f9ae9ca8dfb29d56cfc9297c8a7b6d3f85f` |
| `5NHW` | `pdb_00005nhw-H-L` | `sabdab2_H01EWL0177` | `FAB` | 11,395 bytes / `d6fbfcc0913f4d41dc4971086df37185da78c383f0beb44897ee368ef2ce8c2f` | 1,362 bytes / `6c1343f899b86117eb1e1586c03e4f656a40892a44f933397d4dfc08102aff09` |
| `6A3W` | `pdb_00006a3w-A-B` | `sabdab2_H01W8L01GX` | `FV` | 44,896 bytes / `1f19a5a01b3418b157239ab1b68edb80274e466f5bf56cb24bbe04ec046fcafd` | 1,555 bytes / `96207967404f8d85b7992cb5377628c5323ebdf025134a6fc00bafab7efe5c21` |
| `6HHC` | `pdb_00006hhc-H-L` | `sabdab2_H01YHL01JS` | `FAB` | 15,028 bytes / `b4d07e0724472a7181c1d52372e69840167d3467a3191243b03b69bdb53c5990` | 1,579 bytes / `b594e42cc03fd65ad23d3f94a0795ac923f71c444cc373eee6d890e1aa9dd463` |
| `6PE7` | `pdb_00006pe7-H-L` | `sabdab2_H027QL01SF` | `FAB` | 12,201 bytes / `303e48aa85cbe45223c02f15f6a6d2179383bb21fdd8ee2fdbd4c7562dced83e` | 1,357 bytes / `e1997a0c0959855054e953405ce629df4d0e7db0b8c839d77848725ea0b40f1c` |
| `6PE8` | `pdb_00006pe8-A-B` | `sabdab2_H027QL01SF` | `FAB` | 23,526 bytes / `5b26eb4532be4d61d3a37535491b27aa7ef8b1ea09003d177ade26add75aa771` | 1,465 bytes / `a73947a09d5a291158db7cc86fd127c0ba29203421931b67e4c477ef97c368f5` |
| `6PPG` | `pdb_00006ppg-B-A` | `sabdab2_H0290L01TE` | `FAB` | 33,854 bytes / `cbb79bcb2663dc60214f8b0f1e01a236495284f1dfc57bc26567f9f2b238792a` | 1,478 bytes / `d3129608f8acb79aee3fd4972f00b99d90405a58e3798e8fec639595dfc61ed5` |
| `6U6U` | `pdb_00006u6u-H-L` | `sabdab2_H0286L01SV` | `FAB` | 12,124 bytes / `95e0fe96c20bf27ef14f11b6d1c81b638054fff5b2f990ef0fb059ffdc136510` | 1,452 bytes / `ca84238b37999e17103546d604247c5ce01a564ba7543884fcd365d3c7c35998` |

10 份 annotation JSON 与 10 份 summary CSV 共 223.09 KiB（228,443 bytes）；summary 的
`SABDABupdate_date` 均为 `20261008`，本次获取时间为 `2026-10-15T10:56:29+00:00`。
逐项核对时，10 个实例的 VH 和 VL 都分别在所选 RCSB canonical H/L record 中恰好连续出现一次。
文件位于 `sabdab/annotations/` 和 `sabdab/summaries/`，均为项目级
`data/raw/reference/sabdab/` 内容寻址对象的硬链接；`sabdab/manifest.json` 固定选择、公共路径、
字节数和哈希。此次只需要实例注释，因此没有重复保存 SAbDab2 的 IMGT 重编号 mmCIF；结构坐标
仍采用上文固定的 RCSB mmCIF。

RCSB canonical FASTA 提供 PDB polymer entity 的序列字节，SAbDab2 提供公开的 H/L 实例配对、
可变域序列和 IMGT 编号。两类 raw 证据本身不包含 1,444 条记录的候选 VH；把 CSV HCDR 放回
参考可变域属于后续 processed 重建，不写入本 source README 的事实层。

## 采集过程记录

- 2026-09-16 用 `download_r01_igdesign.sh` 在 ab02 完整 clone 上游仓库并 detach 到 commit `70431eef0afaf0496d7d84e22dfdc1980ec9e70e`。核对 47 个 tracked 文件、16 个 data 文件、字节数、`git fsck --full` 和工作树状态后原子发布；交付目录后来从通用名 `github/` 改为上游原名 `igdesign/`，脚本路径同步更新。
- 同日下载 bioRxiv v2 PDF，最初保存为 `2023.12.08.570889v2.full.pdf`，随后按项目规则改为 `IgDesign_2023-12-08_bioRxiv-v2.pdf`；重命名前后字节与 SHA-256 一致。
- PDB 第一次尝试从 8 个参考复合物取得链序列后，将每条数据记录的 HCDR 替换进参考重链，生成 1,244 条重建序列和 1,444 行 manifest。这属于推断性序列重建，超出 raw 外部补充范围，整份输出已删除。
- 第二次尝试只保留 8 个外部锚点的 24 条 RCSB canonical 链序列选取结果，但仍只有 FASTA，并生成 manifest。脚本为 ab02 Python 3.6.9 改写兼容语法，远端 `py_compile` 通过后经代理执行。
- 第三次补齐 8 个完整 mmCIF，并保证 FASTA 与 mmCIF 在一次原子发布中成对出现。随后把 R01 专用实现抽成通用 `fetch_pdb_reference_data.py`，用 `r01_igdesign_pdb_config.json` 描述 8 个复合物。
- 曾短暂维护 sequence/structure 两份 manifest，再合并为单一 manifest。确认与 README 逐项表重复后，删除所有 manifest，最终 `pdb/` 只保留 `sequences/` 和 `structures/`，完整性事实统一写入 README。
- 探测 RCSB `Content-Disposition` 后确认完整 entry FASTA 的默认下载名为 `rcsb_pdb_<ID>.fasta`，mmCIF 为 `<ID>.cif`。中途为选链视图使用过纯 `<ID>.fasta`，最终改用与 RCSB 默认 FASTA 相同的文件名；该选链视图的序列取自 canonical entity，角色 header 由项目生成，仅调整文件名时内容哈希不变。
- 发布前清理 `.README.md.partial`、旧 PDB 输出、`structures_manifest.csv` 和单独 `manifest.csv`。README、下载脚本和远端目录路径同步到最终状态。
- 2026-09-22：复核 RCSB 逐链实例与已存 mmCIF 的 `_atom_site` 记录，修正 `5I5K` 抗原 FASTA header 中的 label asym `D` 为 `A`。三条 canonical 序列正文与 8 份 mmCIF 均保持原样；更新 FASTA SHA-256，并验证 16 个 PDB 文件的完整性摘要。
- 2026-09-22：按更新后的 README 格式复核 R01 的上游仓库、CSV 统计、论文与 RCSB 条目，并在文末登记仍待确认的实验口径、结构靶点和数据授权问题 `Q01`—`Q03`；上游数据及 PDB 文件未改动。
- 2026-09-22：对照归档的 bioRxiv v2 附录 C，补全 SAbDab 基线 HCDR3 抽样不足时的递补规则；并按附录 A—E 的实际内容修正论文归档说明。原始数据与论文 PDF 均未改动。
- 2026-09-22：复核归档论文表 3/4、附录 D 和 8 张 CSV，补全 `Q02` 的候选去向疑问，新增 `Q04`—`Q06` 跟踪统计检验、单重复阳性与设计记录同对照 HCDR 的待确认事项；公开原始文件未改动。
- 2026-09-22：依据 bioRxiv v2 的发布日，将归档 PDF 从 `IgDesign_2023-12-08_bioRxiv-v2.pdf` 改名为 `IgDesign_2024-12-14_bioRxiv-v2.pdf`，字节数和 SHA-256 不变；同步澄清 PDB FASTA 为项目生成的选链视图，补全 RCSB 条目、原始结构论文引用及 PDB 文件总大小。
- 2026-09-23：重新按数据形成主线核对模型生成、候选选择、实验处理、论文统计与公开表之间的关系；区分 SAbDab 基线、参考阳性对照和 IgDesign 设计，明确 2,400 条名义文库、论文 1,437 条比较组记录、CSV 1,436 条非对照记录及 1,444 条总记录的计数边界，并补充部分重复结合与标签的关系。原始数据、论文和 PDB 文件均未改动。
- 2026-09-24：补充 2,400 条名义候选到论文 1,437 条、公开 CSV 1,436 条候选及加入阳性对照后 1,444 行的计数流程图；明确 964 条差额没有逐条去向和分阶段损耗数据，不能解释为实验 non-binder。随后按“直接观测—拟合或判定—公开字段”的顺序补充 SPR sensorgram、重复级结合判定、`KD` 拟合与汇总标签之间的关系，并标明未公开的曲线级阈值和拟合质量信息。原始数据、论文和 PDB 文件均未改动。

- 2026-10-14：复核归档 bioRxiv v2 附录 D.1—D.3，并以 Carterra 平台说明、非再生滴定方法论文和 LSA/Biacore 对比研究解释技术背景；补充裂解液 Fab 捕获、阵列式 HT-SPR、浓度系列内非再生与完整周期再生的区别，修订 KD 字段及阴性解释边界，将捕获和曲线质控资料缺失作为已知使用限制保留在正文。初稿曾将该限制单列为 Q07；复核后撤回该待办，不表示资料缺口已经解决，后续确有具体处理决策受阻时再登记针对性问题。本轮仅更新文档，上游数据、归档论文、PDB 文件及 Q01—Q06 均保持原样。

- 2026-10-14：为集中提示后续处理者，恢复 Q07，聚焦逐候选捕获、表达/活性与曲线拟合证据缺口；正文继续保留已确认的 HT-SPR 方法和解释边界，不将方法本身列为质量问题。Q07 不阻塞现有公开包接入，尚未获得的证据仍标为待补充。

- 2026-10-15：复核统一 PDB 内容寻址存储和 R01 结构覆盖。确认 5NHW、6PE7 的 canonical FASTA 与完整 mmCIF 已通过全局验收，选择当前 RCSB entry FASTA 后在 R01 建立 4 个硬链接并更新 `pdb/manifest.json`；同时按现有文件修正 5J13 FASTA 的大小、SHA-256 和 author→label 证据说明。早期“删除单项 manifest”的记录描述当时状态；当前 manifest 是后续统一 PDB 存储迁移引入的引用台账。
- 2026-10-15：按已核实的 H/L author chain 从 SAbDab2 固定 10 个 antibody instance，归档 10 份 entry annotation JSON 和 10 份实例 summary CSV；对象进入项目级内容寻址目录，R01 通过硬链接与 `sabdab/manifest.json` 引用。逐项核对 instance、SAbDab2 ID、类型、字节数和 SHA-256；未下载本次处理不需要的 SAbDab2 重编号坐标。
- 2026-10-15：从 UniProtKB REST API 固定人 IL17A reviewed 条目 `Q16552` 的 JSON 与 canonical FASTA，核对 release `2026_03`、entry version 209、sequence version 1、物种 9606、signal peptide 1—23 和 mature chain `PRO_0000015423` 24—155。两份官方响应进入项目级内容寻址目录，R01 通过硬链接与 `uniprot/manifest.json` 引用；复算 mature sequence 为 132 aa，SHA-256 为 `05feac071264f46588ee51cffcfd74552cc224bbdb3e3490fe36680428444110`，并清理下载 staging。本次补证不关闭 Q01。

## 参考文献

- 固定快照：<https://github.com/AbSciBio/igdesign/commit/70431eef0afaf0496d7d84e22dfdc1980ec9e70e>
- 上游 README：<https://raw.githubusercontent.com/AbSciBio/igdesign/70431eef0afaf0496d7d84e22dfdc1980ec9e70e/README.md>
- bioRxiv v2：<https://www.biorxiv.org/content/10.1101/2023.12.08.570889v2>
- IgDesign DOI：<https://doi.org/10.1101/2023.12.08.570889>
- Carterra LSA 平台说明（阵列与成像读出技术背景）：<https://carterra-bio.com/lsa/>
- TitrationAnalysis 方法论文（非再生滴定术语及分析背景）：<https://pmc.ncbi.nlm.nih.gov/articles/PMC10667272/>
- LSA 与 Biacore 8K 直接比较研究（平台方法验证，不替代 R01 质控）：<https://doi.org/10.1177/2472555220934814>
- `6PE8`：[RCSB 条目](https://www.rcsb.org/structure/6PE8)；[原始结构论文（Argiriadi et al.）](https://doi.org/10.1186/s12860-019-0213-4)
- `6U6U`：[RCSB 条目](https://www.rcsb.org/structure/6U6U)；[原始结构论文（Larson et al.）](https://doi.org/10.1002/pro.3862)
- `5I5K`：[RCSB 条目](https://www.rcsb.org/structure/5I5K)；[原始结构论文（Schatz-Jakobsen et al.）](https://doi.org/10.4049/jimmunol.1600280)
- `5J13`：[RCSB 条目](https://www.rcsb.org/structure/5J13)；[原始结构论文（Verstraete et al.）](https://doi.org/10.1038/ncomms14937)
- `6PPG`：[RCSB 条目](https://www.rcsb.org/structure/6PPG)；[原始结构论文（Tilegenova et al.）](https://doi.org/10.1080/19420862.2019.1692764)
- `6HHC`：[RCSB 条目](https://www.rcsb.org/structure/6HHC)；[原始结构论文（Schaefer et al.）](https://doi.org/10.1016/j.jmb.2019.09.008)
- `5NGV`：[RCSB 条目](https://www.rcsb.org/structure/5NGV)；[原始结构论文（Morvan et al.）](https://doi.org/10.1073/pnas.1707925114)
- `6A3W`：[RCSB 条目](https://www.rcsb.org/structure/6A3W)；[原始结构论文（Li et al.）](https://doi.org/10.1016/j.celrep.2018.09.073)
- `5NHW`：[RCSB 条目](https://www.rcsb.org/structure/5NHW)
- `6PE7`：[RCSB 条目](https://www.rcsb.org/structure/6PE7)
- SAbDab2：[数据库与下载格式说明](https://sabdab.opig.stats.ox.ac.uk/about)
- UniProtKB `Q16552`：[条目](https://www.uniprot.org/uniprotkb/Q16552/entry)；[JSON](https://rest.uniprot.org/uniprotkb/Q16552.json)；[canonical FASTA](https://rest.uniprot.org/uniprotkb/Q16552.fasta)

## 其他

### 数据范围和限制

- 每个靶点 100 万条模型生成输出、逐记录对应抗体的完整 VH/VL、预测结构，以及 IgDesign 模型训练所用的固定 General PDB/SAbDab 快照和完整 split manifest 均未随仓库发布。
- CD40-Ravagalimab 的实验标签公开，但实际设计 HCDR 被按设计范围遮蔽，不能用于真实序列建模或重新计算 scRMSD。
- 8 个代表性 sensorgram PDF 不是逐行、逐 replicate 的仪器原始输出。`download_ckpts.sh` 指向外部模型权重，未执行且不属于 SPR 数据。
- RCSB 补充覆盖论文的 8 个参考复合物和后续确认的 2 个独立 Fab；补充目录中没有为 1,444 条公开记录逐条提供完整序列或坐标，临床抗体全长结构也需另行核验。
- SAbDab2 补充只覆盖上述 10 个参考结构中的已选 antibody instance；它不提供公开 CSV 逐行候选的完整 VH/VL，也不把 RCSB 参考结构自动等同于实际 SPR 制剂。
- UniProtKB `Q16552` 补充固定人 IL17A canonical 与 mature-chain 注释，供后续构建体处理引用；它不消除 6PPG IL17F 与来源报告 IL17A 的冲突，也不确认实际 SPR 抗原的逐残基构造。

### 完整性与验收

- `igdesign/` 固定 commit 的 47 个 tracked 文件与 tree 一致，`git fsck --full` 通过，工作树干净，无 LFS pointer 或 submodule。
- `igdesign/data/` 有 8 个 CSV 和 8 个 PDF，共 2.24 MiB（2,345,336 bytes）；CSV 合计 1,444 行，schema、标签值域和盲化范围逐表通过。
- 8 个论文参考复合物和 2 个独立 Fab 的 FASTA/mmCIF 均已取得；PDB ID、映射强度、author chain、字节数和 SHA-256 见“PDB 数据库”。
- 10 个 SAbDab2 annotation JSON 和对应实例 summary CSV 均已取得；PDB/instance 组合、SAbDab2 ID、类型、字节数和 SHA-256 见“PDB 数据库”。
- UniProtKB `Q16552` JSON 与 canonical FASTA 均已取得；条目版本、feature 区间、文件字节数、哈希及 132 aa mature sequence 哈希见“IL17A 外部序列参考”。
- bioRxiv v2 PDF 的字节数和 SHA-256 见“论文原文”。
- 上游 payload 没有混入验证输出；`pdb/manifest.json`、`sabdab/manifest.json` 和 `uniprot/manifest.json` 只固定项目统一外部参考对象及其来源选择。SAbDab2 annotation JSON、summary CSV 以及 UniProt JSON、FASTA 是本次处理实际依赖的公开数据库原始响应，不是验证日志。

### 许可和再分发边界

- `igdesign/LICENSE` 是代码仓库的 MIT 软件许可证；快照没有独立数据许可证，不能据此自动推定 CSV 和 sensorgram PDF 获得同样的再分发授权。
- bioRxiv v2 文本许可为 CC BY-NC-ND 4.0，不能替代仓库数据许可。
- RCSB 来源的 canonical 序列选链 FASTA 与原始 mmCIF 按对应 PDB 条目和 RCSB 使用政策引用，不属于 igdesign 仓库许可证覆盖范围。
- SAbDab2 annotation JSON 与 summary CSV 按 SAbDab2 的 CC BY 4.0 数据条款引用，不属于 igdesign 仓库许可证覆盖范围。
- UniProtKB `Q16552` JSON 与 FASTA 按 UniProt 的 CC BY 4.0 数据许可引用，不属于 igdesign 仓库许可证覆盖范围。
- 商业使用、公开再分发或对盲化数据外推前，应向上游作者确认权限，并保留固定 commit 与校验记录。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 8 个系统的 SPR 筛选结果 | 8 个 CSV，共 1,444 行 | 已包含处理结果表 |
| 278 个非对照 binder | 286 个 `Binder=True` 减 8 个阳性对照 | 已包含，与论文一致 |
| CD40-Ravagalimab 设计序列 | 设计 HCDR 为 `X` 掩码 | 部分包含；标签在，设计序列未公开 |
| 8 个参考实验复合物 | 8 对 FASTA 与 RCSB mmCIF | 已包含外部参考 |
| 两个可复用的独立 Fab 条目 | 5NHW、6PE7 的 RCSB FASTA 与 mmCIF | 已包含结构补充证据 |
| 10 个参考抗体实例的公开可变域注释 | SAbDab2 annotation JSON 与实例 summary CSV | 已包含外部注释证据 |
| 人 IL17A canonical 与 mature-chain 注释 | UniProtKB `Q16552` JSON、FASTA 与选择 manifest | 已包含外部序列证据；不代表实验试剂逐残基身份已确认 |
| 逐记录对应抗体的完整 VH/VL 与结构 | 固定 tree 与 PDB 补充中均无 | 未包含 |
| 百万级候选库和固定训练快照 | 固定 tree 中无 | 未包含 |
| 完整逐 replicate SPR 输出 | 仅 8 个代表性 sensorgram PDF | 未包含 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-22；已发询证邮件、待回复）：IgDesign [论文 Table 2](https://www.biorxiv.org/content/10.1101/2023.12.08.570889v2)将 Afasevikumab–IL17A 系统关联到 `6PPG`，公开 CSV 的 `Target` 也写为 IL17A；[RCSB 6PPG](https://www.rcsb.org/structure/6PPG)将其抗原实体和 author chain `G` 标为 IL-17F。已核对两侧条目与本地参考文件；实验所用抗原、模型输入结构与这一条目的确切对应关系仍待确认，影响该系统的靶点与结构解释。据用户确认，相关询证邮件已发出。下一步等待回复，核对答复是否明确实验抗原材料及结构输入依据；取得可核对的一手说明后更新相关章节。
- `Q02`（最近更新：2026-09-24；待逐项口径说明）：[论文](https://www.biorxiv.org/content/10.1101/2023.12.08.570889v2)描述的 8 组实验文库共含 2,400 条候选；论文表 3 的三类比较组合计 1,437 条，不含公开表中的参考阳性对照。附录 D.4 说明会过滤未匹配预期设计序列的样本，但没有给出逐阶段数量或逐候选去向。固定快照的 8 张 CSV 合计 1,444 行，其中 8 行为阳性对照、1,436 行为非对照候选；名义候选与公开候选相差 964 条，公开候选本身包含 1,158 条 non-binder。C5 的 HCDR123 设计在论文表 3 为 7/68、CSV 为 7/67。已核对论文方法与各 CSV 分组，并在正文用流程图明确当前可证实的计数关系；仍需厘清各阶段候选损耗、论文筛选总数与公开行的逐条对应，影响实验入选率和逐行复现。下一步向作者索取各阶段计数、过滤原因及 C5 的逐行映射。
- `Q03`（最近更新：2026-09-22；待权利方说明）：固定快照的 [MIT LICENSE](https://github.com/AbSciBio/igdesign/blob/70431eef0afaf0496d7d84e22dfdc1980ec9e70e/LICENSE)以软件为授权对象；[bioRxiv 页面](https://www.biorxiv.org/content/10.1101/2023.12.08.570889v2)标明的是预印本文本许可。已检查仓库说明与许可文件，尚未找到单独明确覆盖 CSV 和 sensorgram PDF 的商业训练及再分发条款，影响公司使用决策。下一步向 Absci 确认这些文件的权利范围及拟议用途所需授权，取得可核验答复后更新“许可和再分发边界”。
- `Q04`（最近更新：2026-09-22；待作者核对统计检验）：[论文 v2 表 3/4](https://www.biorxiv.org/content/10.1101/2023.12.08.570889v2)将 ACVR2B 的 HCDR123 设计列为 4/68、SAbDab 基线列为 0/66，却报告 Fisher 检验 `p=2.6e-3`，据此将该靶点计入显著结果。按表列计数独立复算，双侧 `p≈0.11955`、单侧 `p≈0.06342`，均高于论文的 `0.003125` 阈值；C5 的 HCDR123 表列 p 值也未能从所列计数复现。已核对归档 PDF 并用 Fisher 精确检验复算，尚需确认作者使用的统计输入、检验方向或是否存在勘误；在此之前，论文所称 HCDR123 在 4/8 靶点显著的结论缺少可复现依据。下一步向作者索取统计脚本、逐组输入及修订说明。
- `Q05`（最近更新：2026-10-15；待单重复阳性证据）：公开 CSV 在 ACVR2B、CD40、TNFRSF9 各有一条 IgDesign HCDR3 记录为 `Binding Replicates/Replicates=1/1` 且 `Binder=True`；论文附录 D.3 明确说明少数样本使用单个 replicate。已逐行核对作者的标签规则，公开包未给出与这 3 条记录对应的独立复测结果，影响其阳性标签的重复性评估。raw 层按来源原样保存这些标签；本 source README 不决定下游是否纳入。下一步向作者确认有无额外测量证据，或安排独立复测。
- `Q06`（最近更新：2026-10-15；待设计与对照身份核对）：ACVR2B、TNFRSF9 各有一条 `Inverse Folding` HCDR3 记录，其公开的三条 HCDR 与本系统 `Positive Control` 完全相同；这两条也属于 Q05 的单重复阳性。已逐行对照固定快照，公开包没有逐候选完整 Fab 序列与设计来源映射，尚无法确认构建体身份及其被计入设计组的依据。它们会影响新设计成功数；按公开 ACVR2B HCDR3 计数做排除该条的敏感性复算，Fisher 双侧 p 值从约 `0.00183` 变为约 `0.00359`，跨过论文的 `0.003125` 阈值。raw 层保留来源原始分组，是否建立 processed 对象由处理文档规定；下一步向作者核实完整构建体、候选来源和分组口径。
- `Q07`（最近更新：2026-10-14；待补充逐候选质控与拟合证据）：**裂解液 Fab 捕获 HT-SPR 的逐条质量复核与阴性解释仍受资料缺口限制。** 已核对归档 bioRxiv v2 附录 D.1—D.3：候选采用 Carterra LSA 上的裂解液 Fab 捕获和非再生动力学测量，仍属于 SPR；当前公开包只有汇总表和代表性 sensorgram PDF，缺少逐候选表达/活性、芯片捕获水平、完整逐重复曲线及明确的拟合模型、阳性判定和质量验收标准。现有证据不足以逐条复核 KD 拟合质量，或区分未观察到结合与表达、活性、捕获不足等可能因素；这不表示已证实某条记录质量失败。公开 CSV 原样给出作者报告的 KD、Binder 与重复数；source 事实不足以把阴性归因为表达失败，也不足以判断全部 KD 是否属于 apparent_KD。此项不阻塞现有公开包接入，但限制独立定量复核及跨实验体系比较。下一步拟向作者确认上述质控与分析流程、取得可对应候选及重复的记录，并核实是否有纯化后独立复测证据；当前未就本项发出询证。获得足以支持相应用途的一手说明或数据并完成核验后，更新正文并关闭已解决部分，剩余缺口继续跟踪。
