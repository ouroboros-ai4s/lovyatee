---
tags:
  - context
---

# Interface Filters Certify Reference Likeness Not Novelty

## time

2026-10-21

## lineage

- ../bodn/2026-10-21-abag-computational-epitope-prediction-survey-s7.md: 第 26 条（AFilter，用机器学习优化的界面能量过滤改进 AlphaFold 派生表位预测）；第 25 条（AbAdapt）作上下文。

## relation

- [[predicted_structures_add_no_classes_beyond_the_reference]]: A ⊑ B.

## description

用判别器过滤预测界面之后保留下来的样本，其共同点是「像实验界面」—— 而这正是参考集的性质。所以过滤后的预测批次不能用来主张新增了表位覆盖。

AFilter 的立场（从标题与综述转述读出）：AlphaFold 派生的表位预测需要机器学习优化的界面能量过滤才可用，即承认原始预测界面不能直接用。机制是（我推的，非原文）：这类过滤器是二分类器或能量打分，参数在实验复合物与诱饵上拟合，接受域因此被定义为参考分布附近。

与支撑集判据合起来看：过滤本身把 P 推向 E，所以「P ⊆ E」是过滤器构造的结果，不是「模型没有新东西」的经验发现。[[predicted_structures_add_no_classes_beyond_the_reference]] 的判据没有错，但不能用在过滤后的批次上 —— 那样测的会是过滤器，不是模型。

数值构造（我构造）：设参考集 patch 支撑 |E| = 10，预测批次原有 13 个 patch，其中 3 个在 E 外。过滤器按「与已知界面能量分布的距离」保留 60%；若 E 外样本在这个尺子上更远，E 外的 3 个被优先剔除，保留集支撑恰为 E 的子集。报告的保留率与后续表位计数都不会显示这一步。

边界：这不是说过滤无用。没有它，预测界面确实不可用。本条只说它不能同时充当「新增覆盖」的证书 —— 同一个组件不能既做筛选又做验收。

可证伪内容：在过滤器训练分布之外（未参与拟合的新抗原家族）测保留率；若 E 外预测界面的保留率与 E 内相当，则「过滤偏向参考相似性」被推翻，本条对该过滤器失效。
