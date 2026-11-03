---
tags:
  - context
---

# Merge Coverage Is Bounded Not Additive

## time

2026-10-22

## lineage

- [[diversity_is_a_task_conditioned_coverage_claim]]: 该条把数据集并集写成带固定策略的 `∧_π`，不是集合 union。
- [[antigen_count_targets_require_state_stratified_marginal_coverage]]: 该条给出增量覆盖 `Δμ(A|B)`，并指出批次间重叠必须扣除。
- [[reference_domain_is_the_research_output_not_a_slot]]: 覆盖分母由 `R` 决定，故并集的覆盖必须在同一 `R` 下比较。

## relation

- [[reference_domain_is_the_research_output_not_a_slot]]: A ⊑ B.

## description

在固定 `(O, X, R, τ, w)` 下，覆盖函数 `Cov(D)` 对并集满足：

```text
max(Cov(A), Cov(B)) ≤ Cov(A ∪ B) ≤ min(1, Cov(A) + Cov(B))
```

上界不紧，且当 A、B 覆盖同一批对象时趋近于 max。因此**"两个各覆盖 60% 的数据集合并后覆盖 100%"是错的**，正确说法是合并后仍在 60%–100% 之间，具体值取决于重叠。

两条操作推论：

1. **增量必须实测，不能由单源覆盖率推算。** 这正是年度抗原预算不能写成"抗原数 × 每抗原表位数"的原因。
2. **并集运算不满足消去律**：`Cov(A ∪ B) = Cov(A ∪ C)` 不能推出 `Cov(B) = Cov(C)`。因此"两个配方覆盖相同"不意味着可互换——它们在未覆盖区域的形状上不同。

对架构的含义：`S` 的合并必须是**结构合并**（近邻表的并集），然后重新算 coverage，而不是把两份 coverage 数字相加。这也是为什么 `S` 必须与 `C` 分离——只有保留结构，合并后的结论才可算。

**可证伪内容**：若在目标数据集上实测表明两个源的覆盖重叠度始终接近 0（互不覆盖），则并集覆盖近似可加，本条的上界约束在实务中可省。
