---
tags:
  - context
---

# Recipe Plan Is A Mixture Optimization Not A Ranking

## time

2026-10-22

## lineage

- <https://arxiv.org/abs/2607.24516>: DecoupleMix 把配方拆成类间比例与类内组成两个正交子问题，类内用带多样性目标的约束凸优化。
- <https://arxiv.org/abs/2511.20643>: CABS 证明在线批采样可以按声明目标分布构造，而非离线静态过滤。
- [[four_claim_strengths_need_four_validators]]: 配方收益是独立的主张类别，需要对照训练验证器。
- [[antigen_count_targets_require_state_stratified_marginal_coverage]]: 增量覆盖是集合覆盖的差分，不是逐项相加。

## relation

- [[four_claim_strengths_need_four_validators]]: A ⊑ B.

## description

原型的 `recipe` 用例把已覆盖对象排在前面、未覆盖排在后面，再按预算截断——结果是预算紧时第一个丢掉未覆盖样本，与多样性目标反向。

配方不是排序。它在数学上是**在约束下选择子集，使目标覆盖增量最大**：

```text
maximize   Σ_{r∈R} w(r) · 1[∃ d∈D_sel : sim(d,r) ≥ τ]      （边际覆盖）
subject to |D_sel| ≤ B,  exposure 约束（每种策略的重复次数）
```

即加权集合覆盖的预算版本。落到实现上，三条与原型不同：

1. **截断必须保住未被覆盖的层**，不能按相似度降序一刀切。
2. **采样策略是声明的一部分**：`rep_only` / `cluster→member` / `none` 改变的是模型看到什么、看几次，不是 diversity 的定义；它们进入配方而不是进入 `X`。
3. **类间与类内分开**：跨数据源比例与源内选择是两个子问题，混在一起调会互相抵消（DecoupleMix 的核心论点）。

**代价与边界**：加权集合覆盖是 NP-hard，预算大时需近似（贪心给 1−1/e 保证）。在小预算对照实验中，近似误差可能大于策略差异，此时配方结论只能作为方向而非判决。

**可证伪内容**：若目标覆盖权重 `w` 无法独立于配方结果给出（即权重是从结果反推的），则整个优化是循环的，只能作为 ranker 使用，不能称为优化。
