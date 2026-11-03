---
tags:
  - context
---

# Residue Score Field Does Not Determine Patch Count

## time

2026-10-21

## lineage

- ../bodn/2026-10-21-abag-computational-epitope-prediction-survey-s7.md: 第 1–6 条（六个预测器的输出形式）、第 18 条（Greenbaum 2007，数据集与评价指标缺乏共识）、第 26 条（AFilter，承认预测界面需后验过滤）。

## relation

- [[interface_diversity_metrics_require_metric_specific_observability]]: A ⊑ B.

## description

从逐残基分数到「表位 patch 划分」缺两个量：**邻接图**与**阈值**。而所有已报告的评估指标对这两者都不施加约束。

邻接图是独立输入。patch 定义为超阈残基在表面邻接图上的连通分量。BepiPred-2.0/3.0 的输入是序列，没有空间邻接，只能给线性片段；序列位置到表面邻接的映射不是单射，同一分数串对应多种空间排布。DiscoTope-3.0/PEPITO/CEP/SEMA 有坐标才有图，但图的构造与截断半径仍是外部参数。

阈值没有价格。AUC 与逐残基 precision-recall 对分数的严格单调变换不变，因此对任何阈值索引量 —— patch 数、超阈覆盖率 —— 零约束。

数值构造（我构造）：20 残基表面，正例为残基 5–10。两个分数场排序完全相同（AUC 相同）。若残基 5–10 落在三段互不接触的沟槽壁上，τ 处连通分量为 3 而非 1。**指标不动，patch 数差 3 倍。**

第 18 条再压一层：标签规则与数据集本身无共识，连 AUC 的分母都不唯一。所以「哪个预测器更准」在指标未统一时不是可回答问题。

τ 这一半与 [[richness_ranking_is_threshold_ranking]] 同构（那條讲丰富度排序随 τ 变），邻接图这一半是对上条「所需输入」清单的补充 —— 那条说不同指标需要不同输入，本条点名缺的具体是邻接图与 τ 两个自由参数。

可接受做法：连同 τ 扫描曲线与邻接图来源一起报告 patch 数；两者缺一时 patch 数记为**未定义**，不记零。

可证伪内容：若存在一个以 patch 划分为评价单元的已发表基准，并给出某预测器在该单元上的误差界，则「指标不约束 patch 数」在该预测器上失效。
