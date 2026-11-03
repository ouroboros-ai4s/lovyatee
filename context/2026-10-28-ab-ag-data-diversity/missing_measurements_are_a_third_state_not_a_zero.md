---
tags:
  - context
---

# Missing Measurements Are A Third State Not A Zero

## time

2026-10-22

## lineage

- [[surface_metric_computability_and_claim_strength_run_opposite]]: 该条要求分列"可算记录数"与"可支撑结论的记录数"；本条把该要求落成覆盖率的分母规则。
- [[similarity_artifact_must_be_sparse_and_threshold_indexed]]: 稀疏结构里必须能区分"低于阈值"与"未搜索"，本条规定这两者进入统计的方式。
- [[redundancy_undecidability_splits_into_computational_and_observational]]: 未决分为加算力可解与需加观测两类；本条说明覆盖统计面对前者时的正确写法。

## relation

- [[similarity_artifact_must_be_sparse_and_threshold_indexed]]: A ⊑ B.

## description

原型的 coverage 统计里，一对分数都没有的对象取最大值 0，于是被计入 `uncovered`。这不是精度损失，是**把一个三值状态压成二值**：

```text
covered      ≥ τ
uncovered    measured, max < τ
unmeasured   没有任何一条可比对的记录
```

`query_coverage_fraction` 的分母因此错误。若 90% 的比对没有测，覆盖率被压到真实值的十分之一，而这个数字照样能被 certified。更糟的是它的方向不确定：缺失偏向难测对象时覆盖率被低估，偏向易测对象时被高估——所以不能靠"保守估计"辩解。

三条规则：

1. **分母分列**：`measured_denominator` 与 `declared_denominator` 同时报告。前者是具备该输入档的记录数，后者是声明域的全部对象。
2. **覆盖率是一个区间，不是数**：在 `measured_denominator` 上算出的覆盖率是**上界**（未测的可能全不覆盖）与**下界**（未测的可能全覆盖）之间的一个值。报告必须给区间，或明确声明"缺失按零处理"这一额外假设。
3. **不许静默填零**：任何把 `unmeasured` 当 `uncovered` 的路径必须在输出里带 `imputed_missing: true` 与理由。

这同时给出了"缺失可接受"的门槛：当 `unmeasured / declared` 超过声明阈值时，证书只能出 `partial`，不能出 coverage 结论。门槛本身是 `V` 的一部分，不是实现里的常量。

**可证伪内容**：若在目标数据集上实测表明 `unmeasured` 的分布与 `covered` 判决完全独立（即随机缺失），则区间退化为一个无偏估计，三值状态可以按缺失机制合并；只要实测显示缺失与判决相关，填零就是有偏的，本条成立。

**边界**：本条针对"对象级覆盖"。对于"同一对象上不同指标的缺失"，处理相同，但分母是"具备该指标输入"的对象数，不是总对象数。
