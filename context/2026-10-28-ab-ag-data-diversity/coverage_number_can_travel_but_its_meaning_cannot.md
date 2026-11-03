---
tags:
  - context
---

# Coverage Number Can Travel But Its Meaning Cannot

## time

2026-10-22

## lineage

- [[diversity_is_a_task_conditioned_coverage_claim]]: 该条说索引改变时数字可算但解释不迁移。
- [[reference_domain_is_the_research_output_not_a_slot]]: 参考域是研究产出，因此跨参考域的覆盖率不是同一个量。
- [[missing_measurements_are_a_third_state_not_a_zero]]: 分母构成不同时，同一百分数不可比。

## relation

- [[reference_domain_is_the_research_output_not_a_slot]]: A ⊑ B.

## description

覆盖率的定义是 `covered / declared`，两个数都依赖声明。因此：

```text
Coverage(D → R₁ | O,X,τ) 与 Coverage(D → R₂ | O,X,τ)
```

即使都是 0.7，也不是同一个量；它们的差不能解释为"对 R₂ 更好"。更隐蔽的是**同一 R 下不同 D 的可比性**：若 D₁ 的 `unmeasured` 比例高于 D₂，两者的分母含义不同，直接比较会系统偏向测量更全的一方。

可比的充分条件是：同一 `O`、同一 `X`（含版本与参数）、同一 `R`、同一 `τ`、同一权重 `w`、且 `unmeasured` 比例相同或已显式建模。缺任一项，报告里必须标注"异口径"。

**这是本项目最容易被误用的一处**：覆盖率数字在报告表里看起来最有横向可比性，实际上它的可比条件最苛刻。

**可操作要求**：每个 coverage 值携带一个 `comparability_key = H(O, X, R, τ, w, imputation_policy)`；不同 key 的值放在不同表中，或在同一表中分组。

**可证伪内容**：若实测表明在若干 `R` 与 `X` 的合理变化下，覆盖率排序稳定（Spearman ρ 接近 1）且差异小于预设容忍度，则数字可跨口径近似迁移，本条只要求记录 key 即可。
