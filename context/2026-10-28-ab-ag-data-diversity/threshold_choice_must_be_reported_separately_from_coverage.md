---
tags:
  - context
---

# Threshold Choice Must Be Reported Separately From Coverage

## time

2026-10-22

## lineage

- [[richness_ranking_is_threshold_ranking]]: 富集度排序本质是阈值排序。
- [[chao1_lower_bound_moves_with_the_threshold]]: 阈值一动，Chao1 下界随之动。
- [[specification_curve_is_the_reporting_form]]: 阈值是可枚举选择维度之一，应在规格曲线上呈现。

## relation

- [[specification_curve_is_the_reporting_form]]: A ⊑ B.

## description

`τ` 不是覆盖率的精度旋钮，它**改变被测量的对象**。τ=0.8 的"覆盖"与 τ=0.5 的"覆盖"回答的是两个不同问题（前者近乎同一物，后者近乎同类）。

因此：

1. 覆盖率必须与 τ 一起报告，不能只报数。
2. 在 τ 上的曲线（coverage vs τ）比单点更有信息量，且其形状可区分"真的没有"与"差一点"。
3. `τ` 的选择依据必须写在 `V` 里（为什么这个阈值对本任务有意义），不能是默认值。
4. **不同数据集的 τ 不可各自调优后比较**——那是把测量工具也当成待优化的对象。

对下游决策的含义：年度抗原预算对应的不是一个覆盖率目标，而是"在某个 τ 下达到某覆盖率"，两者必须同时给出。同一预算在 τ 放宽后所需抗原数可能低一个数量级，这不是好消息，是任务定义变了。

**可证伪内容**：若目标任务的失败模式对 τ 在一个宽区间内不敏感（模型性能随 τ 变化平坦），则 τ 可固定为约定值，本条只要求记录。
