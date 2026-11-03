---
tags:
  - context
---

# Reference Domain Is The Research Output Not A Slot

## time

2026-10-22

## lineage

- [[diversity_is_a_task_conditioned_coverage_claim]]: 该条把 `R` 分为 `R_ref` 与 `R_target` 两个角色；本条说明这两个角色的取值是本项目的主要科学产出。
- [[redundancy_reference_sets_are_declarations_not_parameters]]: 参考集换一个，判决可以从 3/3 变成 0/3。
- [[antigen_count_targets_require_state_stratified_marginal_coverage]]: 年度抗原目标只有作为覆盖增量才有意义。
- <https://arxiv.org/abs/1805.03677>: Dataset Nutrition Label 把诊断模块与数据集文档分开，说明"量什么"本身是可独立产出的对象。

## relation

- [[diversity_is_a_task_conditioned_coverage_claim]]: A ⊑ B.

## description

`R` 与 `V` 在 schema 里各占一个字段，看起来是配置。实际上它们是本研究的**答案**：

- `R` 定义 coverage 的分母。生产域由哪些抗原族、哪些状态、什么权重组成，没有任何文献给出现成定义；确定它需要一个可辩护的构造过程，而这个过程本身就是产出。
- `V` 定义"通过"是什么意思。留出集的选择、验证器的独立性、通过阈值，三者共同决定证书强度上界。
- `F` 在 `R`、`V` 固定后只是算术。

推论：**产物应该把 `R` 和 `V` 作为可命名、可复用、可版本化的独立对象，而不是证书里的内联字段。** 一个 `R` 定义可以被多份证书引用；一个 `V` 也可以。证书引用它们的摘要，就像引用 `S` 一样。这样"同一个 S 在哪些 R 下被检验过"和"同一个 R 支撑了哪些主张"都成为可查询的关系，而这正是两个下游决策需要的形式。

同时这也给出工作量配比：schema 与状态机是几天到两周的工程，`R` 的构造与 `V` 的独立性是数月的研究。若最终代码里 `R`/`V` 仍只是 `additionalProperties` 允许的自由对象，而状态机占了大部分行数，产物就是漂亮但没有回答问题。

**可证伪内容**：若 `R` 与 `V` 在实践中每次都随任务重新手写、从不复用，则把它们提升为独立对象只增加间接层，本条退回内联字段即可。
