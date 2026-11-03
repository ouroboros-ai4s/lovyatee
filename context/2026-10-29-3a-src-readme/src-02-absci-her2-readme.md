---
tags:
  - context
---

# SRC_R02_ABSCI_HER2 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
  - [实验对象与设计边界](#实验对象与设计边界)
  - [从模型设计到公开表](#从模型设计到公开表)
  - [ACE 标签与 SPR controls](#ace-标签与-spr-controls)
  - [top-k 评测支线](#top-k-评测支线)
  - [公开表口径与连接关系](#公开表口径与连接关系)
  - [数值解释与数据限制](#数值解释与数据限制)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [零样本 binder 表](#零样本-binder-表)
  - [SPR control 表](#spr-control-表)
  - [候选多属性表](#候选多属性表)
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

- `source_id`：`SRC_R02_ABSCI_HER2`
- `source_version`：`snapshot-2024-08-08`
- 原作者或发布机构：Absci Corporation（Amir Shanehsazzadeh 等研究者）

### 来源方背景

Absci Corporation 于 2011 年以 AbSci, LLC 的形式创立，总部位于美国华盛顿州温哥华；截至 2026-09-21，其普通股在纳斯达克全球精选市场以 `ABSI` 交易，见[投资者常见问题](https://investors.absci.com/resources/investor-faqs)。公司目前以生成式 AI 设计生物药，处于临床研发阶段。其[2025 年全年业绩公告](https://investors.absci.com/news-releases/news-release-details/absci-reports-business-updates-and-fourth-quarter-and-full-1)列示合作项目收入 280 万美元、研发费用 8,140 万美元和净亏损 1.152 亿美元（均为截至 2025-12-31 的财年口径），说明其经营仍以研发投入和合作项目为主。

Absci 将模型设计与实验筛选、候选物表征相连接；[公司技术页面](https://www.absci.com/de-novo-design/)将 HER2 工作列为其 de novo 抗体设计实例。[2024 年研究海报](https://www.absci.com/wp-content/uploads/2024/08/Design-of-Functional-Developable-and-Potent-Antibodies-Using-Generative-AI.pdf)列出 Amir Shanehsazzadeh 等作者，展示该团队在抗体设计与实验验证之间的协作。同年，公司还宣布与 [Twist Bioscience 合作](https://investors.absci.com/news-releases/news-release-details/absci-and-twist-bioscience-collaborate-design-novel-antibody)，结合生成式设计和 DNA 合成开发新的治疗性抗体。

## 实验设计和数据口径

### 实验对象与设计边界

**核心实验对象是曲妥珠单抗参考体系中的 anti-HER2 抗体与人 HER2 胞外结构域的结合。** 主抗原是 human HER2（ERBB2）extracellular domain；抗体侧包括阳性对照 trastuzumab（Herceptin）以及生成式模型设计的重链 CDR 变体。因此，公开数据的主要亲和力任务是比较这些设计抗体对 human HER2 的结合，而不是在多个互不相关的抗原之间做通用抗体排序。

| 实验角色 | 对象和在研究中的作用 |
| --- | --- |
| 主抗原 | Human HER2 extracellular domain。SPR 中以最高 500 nM、3 倍梯度的 5 个浓度注入，用于判定结合并拟合 `KD`。 |
| 参考抗体 | Trastuzumab。它提供参考 framework、HCDR 序列、已知 HER2 表位和阳性对照；trastuzumab–HER2 复合物 PDB `1N8Z` 是共享结构输入。 |
| 设计抗体 | 论文设置了 HCDR3-only 和 HCDR123 两种重链设计模式，并将相应 DNA 变体置于 trastuzumab Fab 构建体中：前者只替换 HCDR3，后者允许 HCDR1、HCDR2 和 HCDR3 共同变化。 |
| 交叉反应抗原 | 深度表征阶段另测 cynomolgus、canine、mouse HER2，以及 human HER1、HER3、HER4，用于评价物种交叉反应和 HER 家族选择性；这些不是主设计靶点。 |
| 错误抗原结构输入 | Rat HER2、human HER3 和 VEGF 分别以 PDB `1N8Y`、`7MN8`、`1CZ8` 用作模型的错误抗原输入对照，不构成公开 CSV 中新增的主抗体–抗原任务。 |

上述参考体系也限定了“zero-shot”的准确含义：训练中排除了 HER2 及其同源体复合物，但设计阶段仍向模型提供 `1N8Z` 的 HER2 结构、trastuzumab framework 和已知结合表位。因此，这里验证的是在已有靶点结构和参考表位条件下，对未在训练集中出现的 HER2 体系生成抗体 CDR，而不是完全不使用 HER2 或参考抗体信息的盲设计。

### 从模型设计到公开表

研究采用两步生成流程：MaskedDesign 根据 human HER2 结构、目标表位和 trastuzumab framework 预测抗体–抗原复合物骨架，IgMPNN 再根据该预测结构生成 HCDR3-only 或 HCDR123 序列，并用 sequence loss（model log-likelihood）对候选排序。论文 v4 没有公开计算阶段一共生成了多少条候选，也没有公开模型代码、权重或完整分数；能够确认的实验筛选规模是约 100 万个 HCDR 变体。这些 ACE library 除模型设计外，还包含 controls、用于比较的 biological baselines 和未报告结果的内部 ablation 子集，因此这一数量表示整项实验的 library 规模，不是公开表的行数，也不是一个单独的纯模型设计集合。

进入实验的 HCDR 变体被置于 trastuzumab Fab 构建体中，并在 *E. coli* 中胞内表达。细胞经固定和通透后，ACE（Activity-specific Cell-Enrichment）以 FACS 同时检测 Fab 表达和 human HER2 结合，再以 NGS 读取各序列在分选 gate 中的富集情况，由此产生高通量的预期 binder/non-binder 标签。论文 v4 将整体实验流程描述为 ACE 筛选后再用 SPR 验证，公开的 421 个 HCDR3-only design 是这条流程下游的 SPR-confirmed binder 结果。但公开材料没有说明候选入选 SPR 的规则、全库 ACE binder 数、SPR 送测总数或 SPR 失败数，也没有公开 ACE 结果与这 421 条记录的逐项映射。因此不能把 421 解释为全部 ACE binder，也不能用 `421 / 1,000,000` 计算整体成功率。

公开包将 SPR 结果整理成两个相互重叠的表。`zero-shot-binders.csv` 由这 421 个设计 binder 和 trastuzumab 阳性对照组成，共 422 行；`spr-controls.csv` 则是更广的 SPR 标签汇总，共 1,855 个唯一 HCDR1/HCDR2/HCDR3 组合，包含 758 个 binder 和 1,097 个 non-binder。前表 422 条记录均能在后表中按 trastuzumab HCDR1/HCDR2 背景、相同 HCDR3 和相同 `KD` 找到；后表另有 1,433 条其他 SPR controls，包括 336 个 binder 和 1,097 个 non-binder。因此，`zero-shot-binders.csv` 是公开包单独汇总的设计 binder 子集，而不是与 `spr-controls.csv` 彼此独立的另一批抗体。

421 个设计 binder 中有 71 个 `KD < 10 nM`；作者从高亲和力设计中结合序列多样性和生物物理性质选取少量候选继续表征。公开多属性表保留 trastuzumab 和 Candidate 1–12 共 13 行，其中 Candidate 12 因 NR-CGE main peak purity 低于 95% 而未进入正文对 11 个设计的并列比较。实验流程与公开文件的关系可概括为：

```text
实验流程
human HER2 结构 + 目标表位 + trastuzumab framework
    └─ MaskedDesign 预测抗体–抗原复合物骨架
       └─ IgMPNN 生成 HCDR3-only / HCDR123 候选并按 sequence loss 排序
          └─ 多个实验 library 接受 ACE 筛选
             （论文 v4 报告规模约为 100 万个 HCDR 变体，其中还有 controls、baselines 和 ablations）
             └─ 产生预期 binder / non-binder 标签
                └─ 候选入选 SPR 的规则和送测数量未公开
                   └─ 逐一表达并用 SPR 复核结合、测量 KD
                      └─ 421 个 HCDR3-only SPR-confirmed design

公开文件关系
spr-controls.csv（1,855 条：758 binder + 1,097 non-binder）
    ├─ 其中 422 条与 zero-shot-binders.csv 完全对应
    │  ├─ 421 个设计 binder
    │  └─ 1 个 trastuzumab 阳性对照
    └─ 其他 1,433 条 SPR controls
       ├─ 336 binder
       └─ 1,097 non-binder

421 个设计 binder
    └─ 71 个 KD < 10 nM
       └─ 其中 12 个设计 + trastuzumab → 深度表征表（13 行）
          └─ 正文并列比较 11 个设计；Candidate 12 因质量门槛未纳入
```

这条主线说明公开表中的设计抗体如何形成以及三张表如何重叠，但不表示每个中间集合均已完整发布。公开包只保留作者整理后的 SPR 标签、binder `KD` 和少量候选的后续表征；百万级候选、逐条 ACE 结果以及完整的 ACE→SPR 选择记录均未公开。

### ACE 标签与 SPR controls

**`spr-controls.csv` 中的 `Binder` 是作者给出的 SPR 判定，不是 ACE 分类结果。** `Binder=True` 表示在论文所述 SPR 条件下确认与 human HER2 结合；`Binder=False` 表示在该条件下未确认结合。

理解这一标签口径，需要区分 SPR 的直接观测与最终写入表中的结果。SPR（表面等离子共振）在这里先将 Fab 捕获到芯片表面，再按 5 个浓度注入 human HER2，记录 300 秒结合和 900 秒解离期间随时间变化的响应曲线，即 sensorgram。曲线响应是仪器直接观测；是否观察到结合是作者对曲线作出的实验判定，`KD` 则是从同一组 SPR 浓度系列响应中拟合出的亲和力参数。

论文对后续亲和力与交叉反应面板明确写明使用单结合位点模型进行非线性回归，但没有说明这一模型是否逐条用于公开的全部高通量 SPR controls，也没有给出这些 controls 的曲线级阳性 cutoff、拟合质量或验收标准。因此，公开 CSV 支持使用作者给出的最终 `Binder` 和 `KD`，但不足以还原每条曲线的判定过程。

这里的 `control` 表示实验角色，不是与“设计抗体”互斥的序列来源类别；一条设计序列经 SPR 确认后，也可以在后续实验或公开汇总中作为已知标签的 control。研究者把这些已有 SPR 结论的序列与待筛选设计一起放入 ACE library，用 SPR 标签选择 ACE 判定阈值并评估 ACE 能否区分 binder 和 non-binder。因此，公开 `spr-controls.csv` 既包含 421 个设计 binder 和 trastuzumab，也包含其他 SPR binder/non-binder controls。论文未公开每轮 library 中具体使用了哪些 controls，不能由文件重叠反推每条序列被用作 control 的时间顺序。

ACE 实验中，AF647 标记的 human HER2 用于检测抗原结合，BV421 标记的 anti-kappa light chain 用于检测 Fab 表达。FACS 排除聚集体、杂质及未进入表达 gate 的细胞后，把 HER2 阳性信号分入 `P1`、`P2` collection gates，并另收集无结合信号的 negative gate；这里的直接仪器观测是单细胞荧光及相应分选事件。

完成分选后，NGS 统计每条序列在各 gate 和未分选 library 中的相对丰度。某个 gate 的 enrichment score 是该序列在该 gate 中的占比除以它在未分选 library 中的占比。因此，enrichment 不是单个细胞的荧光强度，而是从分选后序列计数派生的相对富集比；ACE binder/non-binder 又是在三个重复的 enrichment 上应用下述阈值得到的汇总标签。

`P1_R1`、`P1_R2`、`P1_R3` 表示同一序列在三个独立处理的 FACS 技术重复 `R1`–`R3` 中的 P1 enrichment，`P2_R1`–`P2_R3` 同理。论文没有把 P1/P2 分别命名为“高亲和力”和“低亲和力”gate，因此本 source 保留原 gate 名称。给定阈值 `t1`、`t2`，ACE 的筛选规则是：

```text
median(P1_R1, P1_R2, P1_R3) >= t1
OR
min(P2_R1, P2_R2, P2_R3) >= t2
```

满足任一条件即标为 ACE binder，否则标为 ACE non-binder。作者以同一 library 中 controls 的 SPR 标签为参照，用 grid search 选择使 F1-score 最大的阈值：HCDR3 library 使用 `t1=3.51`、`t2=8.89`，HCDR123 library 使用 `t1=6.87`、`t2=3.05`。其中 `median(P1)` 允许一个重复偏离，`min(P2)` 则要求三个重复的 P2 都达到阈值。

Supplementary Tables 2–3 显示，HCDR3 controls 中 2,203 个 SPR binder 有 114 个被 ACE 判为 non-binder，recall 为 94.83%；HCDR123 controls 中 2,270 个 SPR binder 有 161 个被判为 non-binder，recall 为 92.91%。两组 precision 分别为 95.39% 和 95.65%。因此 ACE 是扩大筛选规模的代理实验，仍存在假阳性和假阴性；ACE non-binder 的准确含义是在该次 ACE 条件与阈值下未达到筛选阳性。阈值调定和性能计算使用同一批 library controls，论文没有公开独立留出 controls，报告的性能不是独立外部验证。

上述标签来源并不意味着 `Binder=False` 是脱离检测范围和实验条件的绝对不结合。SPR 在研究中承担参考验证角色，但公开包没有逐条 sensorgram、拟合质量、重复一致性或明确的曲线级阳性 cutoff；因此，这些记录应准确表述为“在论文所述 SPR 条件下未确认结合”。论文 ACE 性能表统计 4,795 个 HCDR3 control entries 和 5,468 个 HCDR123 control entries，公开 `spr-controls.csv` 则包含 1,855 个唯一 HCDR1/HCDR2/HCDR3 组合；两种统计层级之间没有公开逐项映射，见 `Q07`。

### top-k 评测支线

论文的 top-k 分析用于评价模型排序是否把更可能结合的序列排在前面，不是生成三张公开表的连续筛选步骤。top-k 也不是把所有长度的候选混在一起后直接全局取前 `k` 条：Methods 说明，作者先在各个固定 HCDR3 长度组内按 sequence loss（model log-likelihood）排序，再根据 OAS-J 的 HCDR3 长度分布为各长度分配合计 `k` 个名额。HCDR3 和 HCDR123 两种设计模式的 top 1,000 子集再用 ACE 标签计算 binding rate：HCDR3 为 106/1,000（10.6%），HCDR123 为 18/1,000（1.8%）。同一分析还把模型设计与 OAS、SAbDab、错误抗原输入等 populations 比较。

这两个 1,000 是模型评测的分母；论文没有把它们报告为约 100 万条实验库的全部 ACE 阳性，也没有公开它们与 421 个 SPR-confirmed HCDR3 design 之间的逐条集合关系。因此，1,000 不能解释为“通过 ACE 的数量”，421 也不能作为约 100 万条实验库的总体成功率分子。top-k 统计比较中的其他方法问题见 `Q03`，相关集合与送测分母缺口见 `Q07`。

### 公开表口径与连接关系

对应上述实验主线和 ACE 校准支路，三张公开表分别保留 SPR 确认的设计 binder、更广的 SPR 标签 controls，以及少数候选的深度表征；它们存在重叠而非三个独立样本集合。记录口径如下：

- `zero-shot-binders.csv`：422 行，包括 421 个设计 HCDR3 binder 和 1 个 trastuzumab HCDR3 阳性对照；每行都有对 human HER2 的 SPR `KD`。
- `spr-controls.csv`：1,855 个唯一 HCDR1/HCDR2/HCDR3 组合，包括 758 个 `Binder=True` 和 1,097 个 `Binder=False`。758 个 binder 有 `KD`，non-binder 的 `KD` 为空；空值表示公开包只给二元判定，没有可用的定量亲和力。其中 422 条与 `zero-shot-binders.csv` 一一对应，即 421 个 HCDR3-only 设计 binder 和 1 个 trastuzumab 阳性对照；另外 1,433 条是其他抗体变体的 SPR controls。因此，在记录关系上，`zero-shot-binders.csv` 是单独汇总的 HCDR3-only binder 子集，而 `spr-controls.csv` 保留了更广的 SPR 标签范围。论文 ACE 性能表使用的 control entries 数量更大，与这 1,855 个唯一氨基酸组合没有公开的逐项映射，因而不把该文件等同于每轮 ACE library 使用的全部 controls。
- `functionality-developability-cross_reactivity-data.csv`：trastuzumab 阳性对照与 Candidate 1–12 共 13 行，其中 12 个 Candidate 均来自前两张表已有的 HCDR3-only 设计 binder。这张表是对同一批抗体中少数候选进行深入表征的扩展表，并不是新增的一组抗体；除初始 human HER2 SPR `KD` 外，还汇总了 Fab/mAb SPR、细胞表面结合、ADCC、不同物种 HER2 及 HER 家族蛋白交叉反应、产品质量和可开发性等后续实验结果。

这三张表并非彼此独立的样本集合，而是存在明确的记录连接。首先，`zero-shot-binders.csv` 的 422 个 HCDR3 均能在 `spr-controls.csv` 找到一条相同 HCDR3、trastuzumab 参考 HCDR1/HCDR2 和完全相同 `KD` 的记录，因此两表中的这些行是同一批测量的不同表示。

再看 `spr-controls.csv` 内部，1,855 条记录对应 1,855 个互不重复的 HCDR1/HCDR2/HCDR3 组合，但只包含 1,829 个不同的 HCDR3。这是因为其中 17 个 HCDR3 分别出现在多个不同的 HCDR1/HCDR2 背景中，共形成 43 条记录；这里的“重复”只表示 HCDR3 被复用，并不存在三段 HCDR 完全相同的重复组合。其中两个 HCDR3 在不同 HCDR1/HCDR2 背景下分别出现 binder 和 non-binder 标签，说明每个 control 需要由 HCDR1、HCDR2、HCDR3 的完整组合定义。

在此基础上，多属性表进一步从 HCDR3-only binder 中选取少数候选开展深度表征。表内 13 个 HCDR3 均能在前两表中找到对应记录：其中 1 个是 trastuzumab，另外 12 个是 Candidate 1–12；12 个设计候选的初始 SPR `KD` 均小于 10 nM。不过，421 个设计 binder 中共有 71 个满足 `KD < 10 nM`，因此亲和力阈值只界定了候选范围，并不能单独解释这 12 个序列为何入选。论文说明，正文最终并列分析的 11 个高亲和力设计还结合了序列多样性和生物物理性质进行选择，但公开材料没有给出从这 71 个候选到最终表征集合的完整排序或筛选规则。

论文正文之所以写 11 个设计，而公开表保留 12 个，是因为 Candidate 12 的 NR-CGE main peak purity 为 94.4%，低于 95% 的质量门槛；其功能性、可开发性和表位分群数据仍被公开，但未纳入正文的并列比较，以免生产质量问题干扰解释。候选确定后，这些设计被制备为全长 mAb，并进一步接受上述功能性、交叉反应和可开发性实验。因此，从记录关系看，这张表确实是前两表中 13 个相同抗体的扩展表；从实验内容看，它增加的是新的后续测量，而不只是为原有 SPR 记录补充说明字段。其中一位小数的初始 `KD (nM)` 是前两表对应两位小数值的四舍五入结果。由此，合并数据或划分训练、验证和测试集时，应按这些连接关系联动分组并保留各表原始精度。

### 数值解释与数据限制

在明确表间连接关系后，数值字段还需要按实验条件解释。SPR `KD` 的单位为 nM，值越小表示亲和力越强。论文的 HER2 SPR 依次注入从 500 nM 开始、按 3 倍梯度稀释的 5 个抗原浓度，记录 300 秒结合和 900 秒解离，完成该组抗原注射后再生芯片。500 nM 因此是这项实验实际覆盖的最高抗原浓度，不是 SPR 仪器本身的固定检测上限。

若作者报告的 `KD` 高于 500 nM，表示这一数值高于实验的最高测试浓度；这不能单独证明该记录没有结合或作者的判定错误，但精确亲和力数值会更依赖曲线质量和拟合条件。论文为后续亲和力与交叉反应面板给出了单结合位点非线性回归模型，却没有把公开高通量 controls 的每条记录与具体拟合模型、参数或质量标准对应起来。

公开 controls 的 758 条定量记录中，有 40 条 `KD` 高于 500 nM。由于公开包没有这些记录可逐条对应的 sensorgram、拟合参数、残差、逐重复结果或置信区间，目前无法判断其精细数值和排序是否稳定。使用时保留作者报告的原始 `KD` 和 `Binder` 标签；精确亲和力回归或排序则需标记这些记录超出最高测试浓度，并通过排除、降权或按边界外数据处理进行敏感性分析。相关证据缺口及后续处理列于 `Q05`。

除上述测量边界外，建模前还需区分可由序列预先计算的字段与实验完成后才产生的结果字段。`-log(KD (M))` 由 `KD` 换算，编辑距离由候选序列与指定参考序列或数据库比较得到；各类 `Score`、`Product Quality Observation` 和 `Developability Observation` 则是作者对相应实验读数所作的分级或汇总。这些字段并非一概不能作为模型输入，而应根据预测目标和实际预测时点判断：某字段若本身就是预测目标、由目标值直接换算，或参与生成目标标签，就必须从输入中排除，以免发生标签泄漏。例如，亲和力回归不能把 `KD` 或 `-log(KD (M))` 同时作为答案和输入，binder 分类也不能使用据以确定该标签的 SPR 结果；若任务是在实验前仅凭序列进行预测，实验后获得的各类 score 和 observation 同样不可作为输入。编辑距离可以在实验前由序列计算，因此在参考集合及其版本明确、且任务设定允许使用该信息时可以作为特征，否则只宜用于结果分析。

确定可用输入字段后，还要避免把不同实验用途的结果合并为同一测量。多属性表中的 `mAb KD (nM) (hHER2)` 对应 Fab/mAb 亲和力比较，`mAb Binding - Human HER2` 对应跨物种和 HER 家族交叉反应面板。两者都是 human HER2 mAb SPR 摘要，但来自不同实验用途；例如 trastuzumab 分别为 1.61 nM 和 6.2 ± 4.9 nM。公开材料未给出两组数值逐条对应的实验批次、曲线和拟合条件，使用时应分别保留，待解决关系见 `Q06`。

最后，上述解释仍受公开范围限制。当前 source 是作者整理后的 `processed-public` 结果包，三张 CSV 按行只记录 HCDR 片段；不过，同一上游快照的 `unlocking-de-novo-antibody-design/README.md` 另行给出了 trastuzumab Fab 的 227 aa 重链、214 aa 轻链及三个 HCDR 的 IMGT 定义。结合论文 Methods 所述的共同 trastuzumab Fab 载体，421 个 HCDR3-only design 可以通过替换参考重链中的 HCDR3，重建其 Fab 重链氨基酸序列，并与公开的共同轻链配对；`spr-controls.csv` 中的 HCDR123 变体则可按同一规则替换 HCDR1、HCDR2 和 HCDR3。由此得到的是依据公开参考序列生成的派生 Fab 序列，不是 CSV 直接提供的逐行原始字段。

上述信息仍不足以恢复每个变体实际使用的同义密码子、完整质粒、信号肽或标签，也没有给出深度表征候选转成 full-length mAb 后的确切 Fc 和表达构建体。公开包同样缺少 ACE enrichment、FACS gate/count、NGS read、SPR sensorgram、逐 replicate 曲线、完整候选库、生成模型代码和权重。PDB `1N8Z` 提供的是 trastuzumab–HER2 共享参考坐标，不能通过替换 HCDR 序列直接得到各设计抗体的三维结构。

## 论文原文

- 标题：*Unlocking de novo antibody design with generative artificial intelligence*
- 作者：Amir Shanehsazzadeh et al.
- 发表来源：bioRxiv
- 归档文本版本：预印本 v4
- 发布日期：2024-01-07
- DOI：`10.1101/2023.01.08.523187`
- PMID / PMCID：无
- 本地文件：`articles/AbsciHER2_2024-01-07_bioRxiv-v4.pdf`
- 文件大小：6.32 MiB（6,631,108 bytes）
- SHA-256：`478a9c5842e1a95ce63ce03aa5b551bdd623a9509b1c10715649c99147ac80eb`
- 文本许可：CC BY-NC-ND 4.0
- 补充材料：Supplementary figures 与 tables 已内嵌在 64 页主 PDF，无独立补充文件
- 引用数（查询快照）：86（[OpenAlex W4313892628](https://openalex.org/W4313892628)，查询于 2026-09-23）

## 仓库内容

上游来源为 `AbSciBio/unlocking-de-novo-antibody-design`。仓库没有 tag 或 GitHub Release，本 source 固定 commit `cd2bd4b6932b5301d435555dc22084d407e4b92b`；commit 日期为 2024-08-08，因此版本名为 `snapshot-2024-08-08`，不是下载日期。交付目录保存完整 `.git` 快照。

```text
snapshot-2024-08-08/
└── unlocking-de-novo-antibody-design/
    ├── .git/
    ├── LICENSE
    ├── README.md
    ├── zero-shot-binders.csv
    ├── spr-controls.csv
    └── functionality-developability-cross_reactivity-data.csv
```

上游 README 第一段将零样本文件写为不存在的 `zero-shot-designs.csv`，但固定 Git tree 和 README 后文的真实文件名均为 `zero-shot-binders.csv`。raw 层保留 tree 中的真实原名，不为掩盖上游文档错误而改名。

## 数据结构

### 零样本 binder 表

`zero-shot-binders.csv` 有 422 行、7 列：`HCDR3`、`KD (nM)`、`-log(KD (M))`、`HCDR3 Edit Distance to Trastuzumab`、`Minimum HCDR3 Edit Distance to SAbDab`、`Minimum HCDR3 Edit Distance to OAS`、`Minimum HCDR123 Edit Distance to OAS`。HCDR3 均为氨基酸字符串，KD 无空值。

`-log(KD (M))` 是文件内已发布的派生值，当前 tree 没有独立 `KD (M)` 列。OAS/SAbDab 距离也是上游计算字段；本 source 不包含对应外部数据库快照或最近邻记录。

### SPR control 表

`spr-controls.csv` 有 1,855 行、5 列：`HCDR1`、`HCDR2`、`HCDR3`、`KD (nM)`、`Binder`。三个序列字段共同表示重链 CDR 片段，不是完整抗体序列；标签的记录键为三个 CDR 的组合。`Binder` 只有 `True` 和 `False`；KD 只在 758 条 binder 记录中存在。

### 候选多属性表

`functionality-developability-cross_reactivity-data.csv` 有 13 行、48 列。字段覆盖 HCDR3、HER2 KD、Fab/mAb KD 与 SD、cELISA EC50、ADCC EC50、多物种 HER2 与 HER1/3/4 结合、DLS、DSF、SEC、NR-CGE、Red-CGE、完整质量、AC-SINS、anti-DNA/anti-insulin、HIC、developability observation 和 FcRn chromatography。`HCDR3` 可与另外两表连接；本表 `KD (nM)` 仅保留一位小数，另外两表保留两位。

原始字符串包含 `NB`、`ND`、空 score、`+`/`++`/`+++`、`mean ± SD`、non-breaking space 和零宽字符。raw 层保持原字节，不清洗或重新序列化。上游没有公开所有 score 的阈值字典，不能按列名自行补齐。论文 v4 第 60 页 Supplementary Table 8 的 12 行 `NR-CGE Main (%)` 逐项重复同表熔解温度；CSV 相应值为 94.8%–99.4%，与 LMW/HMW 分量逐行合计约 100%。此字段按作者 CSV 原值读取，论文表格差异仍待来源方澄清。`FcRn chromatography` 记录体外相对保留/峰宽信息；该字段未提供体内半衰期。

### 字段说明

以下逐组覆盖三张 CSV 的 7、5、48 个原始字段。数值在 CSV 中均为文本表示；多属性表含不间断空格和零宽字符，空字符串、`NB`、`ND` 与只含零宽字符的单元格需按原样区分。

| 文件 | 原始字段 | 表示、单位与来源 | 缺失及特殊编码 |
| --- | --- | --- | --- |
| `zero-shot-binders.csv` | `HCDR3` | 重链 CDR3 氨基酸片段；作者设计序列 | 无空值 |
| `zero-shot-binders.csv` | `KD (nM)`、`-log(KD (M))` | 前者为由 SPR sensorgram 拟合的解离常数摘要，nM、越小亲和力通常越强；后者为上游从 KD 派生的负对数、越大通常越强 | 两列均无空值；文件没有独立 `KD (M)` 列，逐条曲线和拟合质量未公开 |
| `zero-shot-binders.csv` | `HCDR3 Edit Distance to Trastuzumab`、`Minimum HCDR3 Edit Distance to SAbDab`、`Minimum HCDR3 Edit Distance to OAS`、`Minimum HCDR123 Edit Distance to OAS` | 整数字符串；作者计算的序列编辑距离，越小越相近 | 四列均无空值；最近邻序列和数据库快照未随包发布 |
| `spr-controls.csv` | `HCDR1`、`HCDR2`、`HCDR3` | 重链三个 CDR 的氨基酸片段；作者提供的候选序列 | 均无空值，不构成完整 VH |
| `spr-controls.csv` | `KD (nM)`、`Binder` | 由 SPR sensorgram 得到的解离常数摘要（nM，越小亲和力通常越强）及作者发布的 SPR 二元判定（`True`/`False`），不是 ACE 分类结果 | 1,097 条 `Binder=False` 记录的 KD 为空，表示在论文所述 SPR 条件下未确认结合；不代表任何条件下绝对不结合；`Binder` 无空值，逐条判定 cutoff 与拟合质量未公开 |
| 多属性表 | `Candidate`、`HCDR3`、`Length`、`Edit distance to trastuzumab` | 候选 ID、重链 CDR3、长度和相对参考序列的编辑距离；后两列为上游派生数值 | 13 行均有值；`Candidate` 为 `Trastuzumab` 或 `1`–`12` |
| 多属性表 | `KD (nM)`、`Fab KD (nM) (hHER2)`、`Fab KD SD`、`mAb KD (nM) (hHER2)`、`mAb KD SD` | 作者发布的亲和力汇总，KD 与 SD 单位 nM；数值越小通常表示更强结合 | 13 行均有数值；首个 KD 字段为对应 zero-shot/controls KD 的一位小数表示，Fab 与 mAb 为不同分子形式 |
| 多属性表 | `cELISA EC50 (pM)`、`cELISA EC50 SD`、`ADCC EC50 (pM)`、`ADCC EC50 SD` | 前者来自固定细胞的表面结合测定，后者来自 Jurkat NFAT-luciferase 报告信号拟合；均为 EC50 与 SD，单位 pM，同一 assay 内较小 EC50 通常表示较强效应 | 13 行均有数值；ADCC 字段未提供直接靶细胞裂解率，两种 EC50 不可混作同一测量 |
| 多属性表 | `mAb Binding - Human HER2`、`mAb Binding - Mouse HER2`、`mAb Binding - Cynomolgus HER2`、`mAb Binding - Canine HER2`、`mAb Binding - Human HER1`、`mAb Binding - Human HER3`、`mAb Binding - Human HER4` | 各物种 HER2 或人 HER 家族交叉反应 SPR 汇总；字段名未写单位，论文 Supplementary Table 10 指定结合者的 KD 均值和 SD 单位为 nM | 可出现 `NB`，表示原表未报告结合；不可当作数值零，也不可与单列 mAb KD 当作同一次测量 |
| 多属性表 | `DLS - Cumulant PDI`、`DSF - IP #1 (oC)`、`DSF - IP #2 (oC)` | 动态光散射多分散指数（无单位）与差示扫描荧光两个转变温度（原表标作 `oC`）；产品质量实验汇总 | 字符串可带零宽字符；转变温度较高通常表示较高热稳定性 |
| 多属性表 | `SEC - HMW (%)`、`SEC - Main (%)`、`SEC - LMW (%)`、`NR-CGE - LMW (%)`、`NR-CGE - Main (%)`、`NR-CGE - HMW (%)`、`Red-CGE - Purity (%)`、`Red-CGE - Impurities (%)` | SEC、非还原/还原 CGE 的高分子、主峰、低分子、纯度或杂质比例；实验汇总，单位 % | `SEC - HMW (%)` 有 6 个 `ND`，Candidate 12 的 `SEC - LMW (%)` 也为 `ND`；保留各列原始数值和 `ND` |
| 多属性表 | `Deglycosylated intact mass - Identity`、`Deglycosylated intact mass - Additional species observed`、`Product Quality Observation (SEC, NR-CGE, Red-CGE, Deglycosylated intact mass)` | 完整质量身份判定、附加物种及产品质量文字观察；作者实验汇总 | 原样保留列表文本、不间断空格和零宽字符 |
| 多属性表 | `AC-SINS - Shift (nm)`、`AC-SINS - Score` | AC-SINS 位移（nm）及上游分级；聚集倾向实验汇总 | score 有空字符串、零宽字符及 `+`/`++`；分级阈值未完整公开 |
| 多属性表 | `Polyspecificity - Anti-DNA (AU)`、`Polyspecificity - Anti-DNA score`、`Polyspecificity - Anti-insulin (AU)`、`Polyspecificity - Anti-insulin score` | 多反应性 assay 读数（AU）及上游分级 | score 可只含零宽字符或 `+`/`++`；不能据此自行补数值阈值 |
| 多属性表 | `HIC - RRT`、`HIC - # Main`、`HIC - Score` | 疏水相互作用色谱的相对保留时间、主峰数及上游分级；前两者无单位 | score 可只含零宽字符或 `+`/`++`/`+++` |
| 多属性表 | `Developability Observation (Based on AC-SINS, Polyspecificity, HIC)` | 综合可开发性文字观察；作者汇总 | `No red flags`、`Medium`、`Low`、`High` 等原文可带零宽字符 |
| 多属性表 | `FcRn chromatography - Retention time (min)`、`FcRn chromatography - RRT`、`FcRn chromatography - Peak width (min)`、`FcRn chromatography - Score` | FcRn 色谱保留时间和峰宽（min）、相对保留时间（无单位）及上游分级；体外测量 | score 可为空或 `+`/`++`/`+++`；不能直接换算体内半衰期 |

### 数据示例

`zero-shot-binders.csv` 的首条真实记录为：

```text
TRYFFNGWYYFDV,0.94,9.03,9,5,3,7
```

它表示一条 HCDR3 记录，SPR KD 为 0.94 nM，并附带一个对数派生值和四个编辑距离。

`spr-controls.csv` 的首条真实记录为：

```text
GFNIKDTY,IYPTNGYT,ARWGGYGFYAMDY,0.56,True
```

它表示三个 HCDR 片段及其 SPR binder 标签，不代表完整抗体序列。多属性表的 trastuzumab 行含 `NB`、`mean ± SD`、non-breaking space 与零宽字符，读取后不得在 raw 文件中覆盖这些原始表示。

## PDB 数据库

论文 v4 第 3、23、25 页和作者仓库将 trastuzumab–human HER2 的 `1N8Z` 作为设计及后续结构建模的参考；第 23 页 Methods 的 “Model Structural Inputs” 还明确列出三个错误抗原输入对照：rat HER2 `1N8Y`、human HER3 `7MN8` 和 VEGF `1CZ8`。四项均为论文级结构锚点。三张公开 CSV 没有逐行 PDB 键，也没有将三个错误抗原对照逐条连接至公开测量行的键；这些结构均不能当作各设计变体的实验复合物坐标。

论文写出的链 ID 与 RCSB mmCIF 中的 polymer `label_asym_id` 一致。下表的 author 编号另由各条目 `_atom_site` 的 polymer entity、`auth_asym_id`、`label_asym_id` 交叉核对；对照链只表示论文指定的抗原输入范围，完整 mmCIF 仍保存整个沉积 entry。

| 用途与 PDB | 论文链 / RCSB label 链 | RCSB author 链 | 选链 canonical 序列 |
| --- | --- | --- | --- |
| trastuzumab–human HER2 共享参考 `1N8Z` | 重链 B、轻链 A、HER2 C | B、A、C | 220、214、607 aa |
| rat HER2 错误抗原对照 `1N8Y` | A | C | 608 aa |
| human HER3 错误抗原对照 `7MN8` | A | A | 1,066 aa |
| VEGF 错误抗原对照 `1CZ8` | A、B | V、W | 两份同一 94 aa entity 序列 |

`1N8Z` 的三条选链序列与作者仓库 README 的参考序列比较：轻链 214 aa 完全一致；沉积重链 220 aa 是仓库所列 227 aa 序列的前缀，沉积 HER2 607 aa 是仓库所列 630 aa 序列的前缀。差出的末端分别为 7 和 23 aa。因此，重建设计 Fab 的氨基酸序列时，应以作者快照中的 `unlocking-de-novo-antibody-design/README.md` 所列 227 aa 重链和 214 aa 轻链为共同 scaffold；项目补充的 `pdb/sequences/rcsb_pdb_1N8Z.fasta` 保存 RCSB 沉积构建体的选链 canonical 序列，主要用于核对参考结构。raw source 没有额外生成逐设计的拼接序列，这类派生结果应在后续 processed 层产生。`1N8Z` 仍只是共享参考结构，不能视为各设计变体的实验坐标；`7MN8.cif` 包含 HER2/HER3/NRG1b–trastuzumab Fab 完整 entry，所选 FASTA 只摘录论文指向的 HER3 entity。

四份 FASTA 均由项目通用脚本从 RCSB canonical polymer entity 序列生成选链视图，role 与链号 header 属于项目标注；四份 mmCIF 保留 RCSB 下载字节。`1N8Z` 文件时间戳为 2026-09-16；三个对照于 2026-09-22 从 RCSB 获取。2026-09-22 复核共 4 份 FASTA（7 条记录）和 4 份完整 mmCIF，合计 3.63 MiB（3,810,067 bytes），均可解析，selected sequence 与 mmCIF entity canonical sequence 一致。来源入口为 RCSB `https://data.rcsb.org/rest/v1/core/` 的 entry、polymer entity、polymer entity instance API，以及 `https://files.rcsb.org/download/<PDB_ID>.cif`。

| PDB | FASTA 大小 | FASTA SHA-256 | mmCIF 大小 | mmCIF SHA-256 |
| --- | ---: | --- | ---: | --- |
| `1N8Z` | 1.26 KiB（1,294 bytes） | `3833c4d29b9f15306f3eb580b49f82d944324d80d7b42fbace507676ce3c36f7` | 825.79 KiB（845,613 bytes） | `9f22f02b6e514de56dab8a48bc31a16302a51397779e64c398ad3a7f05cb19a2` |
| `1N8Y` | 697 bytes | `1713b711cd46f4dea8b28a9b8198807b1ff9c3b1a2e75dbfe99c64a532b65599` | 516.73 KiB（529,130 bytes） | `a03414a43de54cafbb80c93a97d2b915ab3060c1daf326411003371d67fe0eee` |
| `7MN8` | 1.14 KiB（1,165 bytes） | `ca5338413a14d4a9a10fcd247207ed5fd034019b5824d2c4106261f8b1600daa` | 1.45 MiB（1,524,278 bytes） | `da047fa40d3db49c0630a5f4aa38a11c177ccfda55c909e834879a13ffe5b925` |
| `1CZ8` | 376 bytes | `02e2c03c25c75b781570a573f74dd7261c9265b1ce84f69b88ac778f478d28cc` | 886.24 KiB（907,514 bytes） | `f309271f7e8c12b2cacd7ac0912d07488d3f2730d753834906bcd772b181cac1` |

## 采集过程记录

- 2026-09-16 核验上游 commit、文件清单、字节数、CSV schema、仓库许可证和论文 Data/Code Availability。
- 首次落盘把交付目录命名为 `github_snapshot_2026-09-16/`，且将 README 与 `articles/` 放在 source 根目录。后续按项目规范原地重组为 `snapshot-2024-08-08/unlocking-de-novo-antibody-design/`，日期改取固定 commit 时间；移动前后核对 HEAD 与全部文件 SHA-256，未改文件内容。
- 2026-09-16 从 bioRxiv v4 页面取得论文 PDF；发布方文件原名 `2023.01.08.523187v4.full.pdf`，按项目约定改为 `AbsciHER2_2024-01-07_bioRxiv-v4.pdf`；重命名前后字节数和 SHA-256 一致。
- 初次调研已识别 1N8Z，但当时将其记录为 source 外部步骤而未下载。项目确立 PDB 硬性要求后，使用通用脚本和 `r02_absci_her2_pdb_config.json` 补齐一份 FASTA 与一份 mmCIF。
- PDB 补充明确采用三张表共享一个 HER2 参考锚点的一对多关系，没有生成逐行副本、变体序列或旁路 manifest。
- 2026-09-22 复核论文 v4 Methods 第 23 页，补齐原先遗漏的 `1N8Y`、`7MN8`、`1CZ8` 三项错误抗原输入对照。先在 source 目录旁的 `.pdb-controls-2026-09-22.partial/` 暂存；RCSB API/完整 mmCIF 下载、FASTA/entity 对照、polymer author↔label 链映射、文件数和 SHA-256 验收通过后移入正式 `pdb/`，清除 staging。三对照补齐配置、同步脚本及过程记录现归档于 `workspace/users/yangwuyu/scripts/r02_absci_her2/` 和 `workspace/users/yangwuyu/context/2026-09-22-r02-control-pdb-completion.md`；上游 Git 快照和原有 1N8Z 文件保持原字节。
- 2026-09-22 针对旧版 PDB 脚本曾按 entity 链列表位置配对 author/label 编号的问题，使用已改为逐个 polymer instance 核对的新版本 `fetch_pdb_reference_data.py` 和四锚点完整配置，对正式 `pdb/` 执行现存目录只读在线复验。脚本重新获取 RCSB entry、entity、instance、FASTA 和 mmCIF，四份选链 FASTA 与四份完整 mmCIF 均同当前 RCSB 字节、大小及 SHA-256 一致；再以独立 mmCIF/FASTA 解析器复核 7 条选链 canonical 序列及 author↔label 对应。无覆盖写入、无 staging 残留，八份已发布文件无需修复；完整命令与验收结果见 `workspace/users/yangwuyu/context/2026-09-22-r02-pdb-revalidation.md`。
- 2026-09-22 逐项比对两张 SPR 表，确认 422 条 zero-shot HCDR3 在 controls 中各有一条同 HCDR3、参考 HCDR1/2 和完全相同的 KD；据此补充训练/测试分组说明。随后复核多属性表的 13 个 HCDR3：均在另外两表中出现；其一位小数 KD 均等于对应两位小数 KD 按十进制常规四舍五入的结果。修订 README 中的跨表连接与精度说明，三张原始 CSV 保持原字节。
- 2026-09-22 全面复核 bioRxiv v4、Supplementary Tables 2–10 与三张 CSV，发现论文中的 NR-CGE 列、部分正文方向和 Fisher p 值存在可复现冲突；结果与计算见 `workspace/users/yangwuyu/context/2026-09-22-r02-full-scientific-audit.md`。使用固定 CSV 原值，不修改来源文件。再次从 bioRxiv 取得的 v4 PDF 与已归档 PDF 均为 64 页、6,631,108 bytes，64 页文本逐页相同；两份字节只在 59 个动态 PDF metadata/ID 字节上不同，归档 SHA-256 只标识当时取得的文件。作者仓库公开问题 #2 记载旧版 `KD (M)` 幂次已由作者修正；当前固定 tree 无该字段，nM KD 与 pKD 已复核。
- 2026-09-22 将论文 ADCC 方法中的效应细胞接种量矛盾登记为 `Q04`；核对其与已列出的公开范围缺口，未把确认未公开的底层材料重复登记为待作者解释的数据错误。保留原论文和 CSV 数值。
- 2026-09-22 对照全面审计记录，将高于最高 HER2 注射浓度的 SPR KD 拟合值的定量可靠性列为 `Q05`；继续保留两表共 45 行原始记录（对应 40 条唯一 controls 测量），使用时标记测试浓度边界，未推算替代 KD。
- 2026-09-22 再次按论文 Table 1、Supplementary Tables 4–5 的公开计数重算 12 与 30 项 Fisher 比较，发现 Supplementary Table 5 星号和例外说明另有两处漏报；可复算脚本见 `workspace/users/yangwuyu/scripts/r02_absci_her2/audit_paper_fisher.py`，据此扩充 `Q03`。逐列核对多属性 CSV 发现 Candidate 12 的 `SEC - LMW (%)` 也为 `ND`，修正字段说明；区分两组 human HER2 mAb KD 摘要，并将其逐实验对应关系列为 `Q06`。来源 CSV 和 PDF 均保持原字节。
- 2026-09-22 将先前由 wuhuawei 执行的三对照补齐、论文/公开包审计、skill 合规核验和复算脚本归档至 R02 发布者的工作区；旧审计的时间点事实与当前发布状态分开记录，原始 CSV、论文及 PDB 文件保持原字节。
- 2026-09-23 重写“实验设计和数据口径”，将 human HER2 胞外结构域、trastuzumab 参考体系、设计 HCDR 变体、交叉反应抗原和错误抗原结构输入分开说明，并按实验流程和三张公开表重新组织记录口径；未修改上游 CSV、论文或 PDB 文件。
- 2026-09-23 补充解释 `KD > 500 nM` 与最高测试浓度的关系，区分结合判定、动力学外推和精确亲和力排序，并扩充 `Q05` 的当前处理方式与关闭条件；未修改作者报告的原始数值。
- 2026-09-23 根据论文 v4 第 27–30、38、53–54 页补充 ACE 的 FACS/NGS enrichment、P1/P2、三个技术重复、F1 阈值校准和混淆矩阵口径；新增校准与筛选双支路流程图，区分 ACE 筛选标签、作者报告的 SPR 标签和公开的 421 个 SPR-confirmed binder 子集，并将公开 controls 与论文 ACE performance control entries 的映射缺口登记为 `Q07`。上游文件保持原字节。
- 2026-09-23 复核论文 Table 1、Inference、Wet-lab validation 与“Generative models produce diverse binders”段落，明确百万级 library、各设计模式 top-1,000 ACE 报告子集和 421 个 SPR-confirmed HCDR3 binder 的分母及集合关系；重画流程图并扩充 `Q07`，未修改上游实验文件。
- 2026-09-23 按“模型设计—ACE 筛选—SPR 确认—公开表”的主实验链重组数据口径，将 SPR controls 的校准作用和 top-k 模型评测分别移至独立小节；明确模型生成总数未公开、论文 v4 报告的约 100 万个 HCDR 变体是实验 library 规模，并将 421 条 SPR-confirmed design 放回 ACE→SPR 主链。同时明确 `zero-shot-binders.csv` 的 422 条记录全部包含于 `spr-controls.csv` 的 1,855 条记录中，并区分序列来源与 control 实验角色。上游实验文件保持原字节。
- 2026-09-23 重写派生与汇总字段的建模说明，按预测目标和预测时点区分标签泄漏、实验后不可用字段与可预先计算的编辑距离；同时补充两个 human HER2 SPR 字段之间的过渡说明。未修改上游实验文件。
- 2026-09-23 修正设计序列的可重建范围：作者仓库 README 已给出 trastuzumab Fab 的 227 aa 重链和 214 aa 轻链，结合各行 HCDR 可在 processed 层重建 Fab 氨基酸序列；仍缺失的是逐变体 DNA、完整表达构建体及设计变体三维坐标。上游文件保持原字节。
- 2026-09-23 复核作者仓库 README、论文正文和 Supplementary Tables 2–3，明确 `spr-controls.csv` 的 `Binder` 为作者发布的 SPR 判定而非 ACE 分类；将 `Binder=False` 限定为在论文所述 SPR 条件下未确认结合，并在 ACE 关系和字段说明中同步标注。上游文件保持原字节。
- 2026-09-23 完成系统复核后，将主流程的方法信息限定为归档的论文 v4：修正 ACE 为 *E. coli* 胞内表达后固定、通透和 FACS 检测，按 MaskedDesign→IgMPNN 重写模型流程，将实验 library 规模改为约 100 万个 HCDR 变体，并补充 top-k 的 OAS-J 长度分层取样口径。同时按 Methods 精简 SPR 注射说明，将 `KD > 500 nM` 限定为需要拟合证据才能判断精细数值稳定性的量程边界问题，并更新 OpenAlex 引用快照。上游 CSV、论文和 PDB 文件保持原字节。
- 2026-09-24 按“直接观测—派生或拟合—阈值判定—公开字段”的顺序复核实验口径：明确 ACE 从单细胞荧光和 FACS 分选事件，经 NGS 计数与 enrichment 计算得到阈值标签；明确 SPR 从 sensorgram 得到曲线级结合判定和 `KD`。同时区分论文对后续亲和力/交叉反应面板明确给出的单结合位点拟合模型，与高通量 controls 未逐条公开的拟合和阳性判定细节。上游 CSV、论文和 PDB 文件保持原字节。
- 本地 README 工作文件从早期 context 路径迁移到 `docs/readme/`，并同步到 source version。已废弃目录名、临时 metadata 和验证文件未留在正式目录。

## 参考文献

- 数据仓库：<https://github.com/AbSciBio/unlocking-de-novo-antibody-design>
- 固定 commit：<https://github.com/AbSciBio/unlocking-de-novo-antibody-design/commit/cd2bd4b6932b5301d435555dc22084d407e4b92b>
- bioRxiv v4：<https://www.biorxiv.org/content/10.1101/2023.01.08.523187v4>
- 1N8Z 结构论文：Cho, H.-S. et al. (2003), *Nature* 421:756-760, DOI `10.1038/nature01392`
- RCSB 1N8Z：<https://www.rcsb.org/structure/1N8Z>
- RCSB 抗原输入对照：[1N8Y](https://www.rcsb.org/structure/1N8Y)、[7MN8](https://www.rcsb.org/structure/7MN8)、[1CZ8](https://www.rcsb.org/structure/1CZ8)
- 7MN8 结构论文：Diwanji et al. (2021), *Nature* 600:339–343, DOI `10.1038/s41586-021-04084-z`
- 1CZ8 结构论文：Chen et al. (1999), *Journal of Molecular Biology* 293:865–881, DOI `10.1006/jmbi.1999.3192`

## 其他

### 数据范围和限制

当前快照只公开三张处理后表。ACE assay 数据在论文 Data Availability 中标为 withheld，代码在 Code Availability 中标为 withheld；固定 Git tree 也没有 ACE/FACS/NGS 原始记录、sensorgram、逐重复曲线、完整候选库、模型代码或权重。

三张 CSV 没有逐行存放完整抗体序列，但上游仓库 README 已公开共同的 trastuzumab Fab 重链和轻链；结合各行 HCDR 可以派生完整 VH/VL 及 Fab 两条氨基酸链。当前材料不足以唯一确定的是逐变体 DNA、质粒及标签等表达构建信息、深度表征阶段的 full-length mAb 全长构建体，以及各设计变体的三维结构。OAS/SAbDab 字段只保存距离，不含外部输入快照和最近邻 identity。

### 完整性与验收

本 source 的固定公开包及论文明确引用的四个 PDB 锚点已按现有一手证据验收；研究使用的 ACE/FACS/NGS 底层数据和模型代码仍未公开，因此完整研究数据获取未完成。

- 仓库 HEAD 为 `cd2bd4b6932b5301d435555dc22084d407e4b92b`；重组前后 Git HEAD 和全部文件 SHA-256 一致。
- 三张 CSV 可解析，分别为 422、1,855 和 13 行；真实 schema、空值、复合字符串和不可见 Unicode 已核对。
- 1N8Z、1N8Y、7MN8 和 1CZ8 各有 FASTA 与 mmCIF；链角色、polymer author/label 编号、文件大小和 SHA-256 已核对。
- bioRxiv v4 PDF 为 64 页，字节数和 SHA-256 见“论文原文”。
- source version 内未发布 manifest、metadata、API response 或验证报告。

### 许可和再分发边界

- 仓库数据按根目录 `LICENSE` 使用 Clear BSD License（允许商业使用，但不授予任何专利权；本仓库文本还增加了数据归因条款）。引用或发表数据时应归因 `Absci Corporation (2023)`；再分发时应保留版权声明、许可条件和免责声明，且未经书面许可不得使用 Absci 或贡献者名称为衍生产品背书。
- bioRxiv v4 论文文本许可为 CC BY-NC-ND 4.0，不能替代仓库数据许可。
- 四项 PDB 文件按 RCSB 使用政策和各自原始结构论文引用，不属于 Absci 仓库许可证覆盖范围。
- OAS、SAbDab 距离字段不表示相关数据库快照已经随本 source 再分发。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| anti-HER2 binder/non-binder 与 binder affinity | `zero-shot-binders.csv`、`spr-controls.csv` | 已包含处理表 |
| 候选功能性、可开发性、质量与交叉反应 | 13 行、48 列 characterization CSV | 部分包含，仅汇总表 |
| ACE assay 数据 | 固定 tree 无相关文件；论文称 withheld | 未公开 |
| 原始 SPR sensorgram 与逐重复值 | 固定 tree 无相应文件 | 未公开 |
| 生成库、模型代码、权重与完整分数 | 固定 tree 无相应文件；论文称代码 withheld | 未公开 |
| trastuzumab Fab 参考轻重链 | 上游 `unlocking-de-novo-antibody-design/README.md` 提供 227 aa 重链和 214 aa 轻链；`pdb/sequences/rcsb_pdb_1N8Z.fasta` 提供 RCSB 参考选链序列 | 已包含；前者用于设计序列重建，后者用于参考结构核对 |
| 各公开变体的 Fab 氨基酸序列 | CSV 提供 HCDR；论文说明变体使用共同 trastuzumab Fab 载体 | 可在 processed 层派生，raw 包未逐行存放 |
| 逐变体 DNA、完整表达构建体与 full-length mAb 序列 | 固定 tree 无相应文件 | 未公开，不能由同义密码子或 Fab 序列唯一确定 |
| 八个设计 binder 的计算结构模型 | 论文第 5 页报告建模；固定 tree 无坐标文件 | 未公开，PDB 补充仅为参考/对照结构 |
| ACE 阈值优化和性能评估逐条记录 | 论文仅给汇总混淆矩阵；固定 tree 无分数、独立留出集或逐条 ACE 标签 | 未公开，无法独立复核泛化性能 |
| trastuzumab–HER2 参考结构 | RCSB 1N8Z FASTA 与 mmCIF | 已包含外部共享参考 |
| 错误抗原结构输入对照 | RCSB 1N8Y、7MN8、1CZ8 的 FASTA 与 mmCIF | 已包含外部论文级对照；公开 CSV 无逐行连接键 |
| OAS/SAbDab 输入快照与最近邻 identity | CSV 只有距离字段 | 未包含 |

## 待解决问题与处理进展

已确认未随公开包发布的底层实验数据、模型材料和结构坐标列在上文“公开范围对照”；这些缺口使完整研究数据获取保持未完成。本节跟踪需要来源方进一步确认、且会改变数据解释或使用判断的具体问题。

- `Q01`（最近更新：2026-09-22；待来源方说明）：多属性表的 AC-SINS、anti-DNA、anti-insulin、HIC 和 FcRn `Score` 使用空值或 `+`/`++`/`+++` 等原始分级；已逐列核对固定 CSV，仓库说明没有给出完整阈值字典。当前保留原始分级，不将其换算为连续数值或跨 assay 的统一等级。若后续需要以这些分级训练或比较模型，向来源方索取各 assay 的判定阈值及空值含义，再更新字段口径。
- `Q02`（最近更新：2026-09-22；待来源方澄清）：论文 v4 第 60 页 Supplementary Table 8 的 12 个 `NR-CGE Main (%)` 与同表 Tm 逐项相同，而固定 CSV 给出另一组逐行合计约 100% 的 CGE 数值；当前保留 CSV 原值并将论文该列视为不可靠。第 6 页 Candidate 2 的 cELISA EC50 方向及跨物种最优候选编号也与 Table 2、Supplementary Table 10 和第 7 页冲突；同页的“所有候选 Tm 低于 trastuzumab”与 Candidate 4 的 80.2°C 对对照 79.5°C 不符。第 3 页称 ACE recall 高于 95%，而 Supplementary Tables 2/3 分别为 94.83% 和 92.91%。请求作者确认表 8 的真实主峰值及相应正文勘误；此前不从论文该列转录数值。
- `Q03`（最近更新：2026-09-22；待来源方澄清）：论文 Methods 第 25 页把单个 2×2 表的超几何概率写作 Fisher p 值；第 17 页 `18/1000` 对 `6/1000` 报 `p=0.0078`，按双侧 Fisher 检验重算约为 `0.0219`，再按论文声称的 12 次 Bonferroni 校正约为 `0.2624`。Supplementary Table 5 还把 HCDR123 top 100 对 OAS-J、HCDR3 top 100 对 VEGF 标作达到图注阈值；重算的双侧 p 分别为 `0.00513`、`0.00545`，按论文声明的 30 次校正分别为 `0.154`、`0.164`。图注将 HCDR3 top 100 对 HER3 的单表概率写为 `0.0025`，而 HER3 与 rat HER2 同为 3/100，单表概率均约 `0.0068`；约 `0.0024` 对应 VEGF 的 2/100。当前保留论文原报告；后续模型比较须由公开计数重算，请求作者提供实际统计代码或勘误，避免沿用有争议的显著性标记。
- `Q04`（最近更新：2026-09-22；待来源方核实）：论文 v4 第 32 页的 ADCC 方法同时记载每孔 `5×10^4` 个靶细胞、效应细胞:靶细胞为 `2:1`，以及每孔 `1×10^10` 个效应细胞；前两项对应每孔 `1×10^5` 个效应细胞，与第三项相差五个数量级。当前保留论文原报告，不据此推定实际接种量；公开 `ADCC EC50` 仅作为作者报告的 Jurkat NFAT-luciferase 摘要使用，不能据这段方法复现实验接种量。需来源方提供实际接种量或方法勘误，再更新复现说明。
- `Q05`（最近更新：2026-09-24；待来源方提供拟合证据）：论文 v4 第 30 页记 HER2 最高注射浓度为 500 nM；公开 controls 中有 40 条唯一记录的 `KD` 高于 500 nM。论文对后续亲和力和交叉反应面板说明使用单结合位点非线性回归，但没有明确这些高通量 control 记录是否采用同一模型；公开包也没有可逐条对应的 sensorgram、拟合参数、残差、逐重复结果或置信区间，因而无法确认超出最高测试浓度的精确数值是否稳定，也无法复核其细粒度排序。当前保留作者报告的原始 `KD` 和二元标签，同时在亲和力回归与排序中标记这些记录，并以排除、降权或边界外处理进行敏感性分析。取得上述曲线、拟合参数及质量信息并完成逐条复核后，才能关闭本问题。
- `Q06`（最近更新：2026-09-22；待来源方提供实验对应关系）：同一候选的 human HER2 mAb SPR 亲和力在 Supplementary Tables 9 和 10 分别报告，公开 CSV 的 `mAb KD (nM) (hHER2)` 与 `mAb Binding - Human HER2` 对应值也不同；trastuzumab 为 1.61 nM 与 6.2 ± 4.9 nM。两组属于分别报告的亲和力比较和交叉反应面板，不能合并为重复测量或据此判定一列错误。当前按实验用途分别使用；若要跨面板汇总或解释差异，需来源方提供对应实验批次、曲线与拟合条件。
- `Q07`（最近更新：2026-09-23；待来源方提供映射和逐条 ACE 数据）：论文 Supplementary Tables 2–3 的 ACE 性能评估分别统计 4,795 个 HCDR3 control entries 和 5,468 个 HCDR123 control entries，公开 `spr-controls.csv` 则包含 1,855 个唯一 HCDR1/HCDR2/HCDR3 组合。论文 v4 还分别报告约 100 万个 HCDR 变体的实验 library 规模、Table 1 中 HCDR3 与 HCDR123 各自的 top-1,000 ACE binding rate，以及经 SPR 确认的 421 个 HCDR3 designs，但没有单列模型在计算阶段生成的候选总数，也没有公开全库 ACE binder 数、421 条与两个 top-1,000 子集的逐项集合关系、SPR 送测总数或失败数。论文与仓库也没有提供 control entry、氨基酸变体、DNA/codon 表示、ACE replicate 及公开 CSV 行之间的逐项映射或 P1/P2 enrichment。当前不把上述计数视为连续漏斗或逐行一一对应，不从 421/1,000,000 推算总体成功率，也不把汇总混淆矩阵结果回填到公开记录；下游只使用 `spr-controls.csv` 中作者报告的 SPR 标签，并把未公开或仅由 ACE 判阴性的设计排除在硬负样本之外。取得上述映射、逐重复 enrichment、完整送测分母和独立验证划分后，才能复算阈值、性能并关闭本问题。
