---
tags:
  - context
---

# Specification Curve Is The Reporting Form

## time

2026-10-22

## lineage

- [[diversity_is_a_task_conditioned_coverage_claim]]: 该条说索引一变结论不自动迁移；本条给出在索引空间上如何报告。
- <https://doi.org/10.31234/osf.io/nhrwq>: multiverse / specification curve 用全部可辩护分析路径的分布代替单一结果。
- <https://doi.org/10.1101/2024.01.14.575565>: 图 fMRI 分析有 61 个步骤、102 个选项，其中 17 步存在争议，作者用决策支持工具枚举路径。
- <https://arxiv.org/abs/2610.23845>: SEER-Repro 的 agent 对已复现结论重跑分析选择，9.5% 的复现结论被认为对选择敏感。

## relation

- [[diversity_is_a_task_conditioned_coverage_claim]]: A ⊑ B.

## description

七槽不是要一次性填对的参数，而是一棵**可枚举的选择树**：`X` 的表示与阈值、`R` 的构成、`V` 的留出方案、`φ` 的权重。每一组选择都是一条合法的分析路径。

因此正确的报告形式不是"我们的 diversity 是 0.62"，而是**规格曲线**：横轴是路径，纵轴是结论量，标出通过/不通过的判决，再按选择维度分组看哪一维主导变化。

三条由此推出：

1. **单一数字不可发布**，除非同时给出它在选择空间中的位置与邻域。
2. **"哪个选择最影响结论"本身是主要产出**，且它与"哪个选择最正确"是不同问题——前者可测，后者往往不可判定。
3. 模型比较必须落在同一路径上，跨路径比较的是路径差异而非模型差异（与 [[differential_task_advantage_needs_an_interaction_test]] 同源）。

**代价**：路径数指数增长。必须用分层抽样或逐维扰动控制预算，并在报告里声明枚举了哪些、跳过了哪些——跳过区域是未测区域。

**可证伪内容**：若实测表明在目标任务上结论对全部已枚举维度都不敏感（判决在 95% 路径上一致），则规格曲线退化为单点报告，本条只增加成本。
