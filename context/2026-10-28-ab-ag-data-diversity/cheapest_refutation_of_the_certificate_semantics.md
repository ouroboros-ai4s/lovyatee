---
tags:
  - context
---

# Cheapest Refutation Of The Certificate Semantics

## time

2026-10-22

## lineage

- [[core_is_two_functions_and_one_document_type]]: 待检验主张——三项内核足以支撑四类下游用途。
- [[four_claim_strengths_need_four_validators]]: 若四类主张需要不同的 F，内核就多于一项。
- [[specification_curve_is_the_reporting_form]]: 结论对索引敏感的程度，是判断"索引化主张"是否退化的直接观测。

## relation

- [[four_claim_strengths_need_four_validators]]: A ⊑ B.

## description

**锐化后的主张**：对任意一个下游用例（recipe / split / risk），存在一组 `(D,O,X,R,V,T,M)`，使得 `F` 的输出足以回答该用例的核心问题，且不需要 `F` 之外的、与该用例绑定的额外语义。

**最便宜的推翻观测**：在抗体侧取一个已有明确功能标签的小数据集（例如同一抗原、已知结合与否的几个抗体族），做三件事：

1. 只变 `X`（CDR-H3 编辑距离 vs ESM 嵌入余弦），算 coverage；
2. 只变 `τ`（0.5 / 0.6 / 0.7 / 0.8）；
3. 看 coverage 排序与"已知结合族是否被覆盖"这个外部标签是否给出**相反**的判决。

成本：一个抗原、几十条抗体、两种相似度、四档阈值 = 8 次计算，无需训练。

**为什么这是最便宜且决定性**：

- 若排序在合理索引变化下翻转，则单一证书不能同时服务"配方选择"与"风险判断"——因为前者需要稳定排序，后者需要稳定绝对覆盖。
- 若排序稳定且与外部标签一致，则索引化主张在该任务族上退化，内核可以简化为单一指标，架构可以大幅缩减。

**判决形式**（只有三种）：

- BROKEN：排序在 8 个格点中翻转 ≥ 1 次，且翻转不伴随外部标签变化。
- CORROBORATED：8 个格点排序一致，且与已知结合族判断一致。
- UNFALSIFIABLE：数据集缺少可用的外部标签（此时必须承认该项目当前无法自证）。

**当前状态**：未执行。本机无数据，环境在 ab 机；这是一个需要在 ab 机跑的最小实验，约 1 小时。

**这条记录的价值**：它把"架构是否成立"变成了一个周末可完成的实验，而不是一个设计辩论。
