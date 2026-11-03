---
tags:
  - context
---

# Four Claim Strengths Need Four Validators

## time

2026-10-22

## lineage

- [[diversity_is_a_task_conditioned_coverage_claim]]: 该条区分 coverage 与 generalization，并说明后者需要模型。
- [[task_relevant_diversity_requires_controlled_interaction_and_independent_validation]]: 该条要求任务相关优势由交互项与独立验证支持。
- [[held_out_certificates_are_relative_to_a_declared_validator]]: 每种主张的强度上界由各自的留出集与判定器决定。
- [[similarity_split_score_drops_do_not_identify_leakage]]: 划分后掉分同时混入训练量、难度、近邻结构与标签组成变化。
- <https://arxiv.org/abs/2606.09809>: EvalCards 显示报告层若不区分"测得全"与"测得对"，读者无法比较结论。

## relation

- [[task_relevant_diversity_requires_controlled_interaction_and_independent_validation]]: A ⊑ B.

## description

四类主张共用一份证书语义，但不共用验证器，也不共用强度上界：

| 主张 | 回答什么 | 必需输入 | 失败时最可能的误读 |
| --- | --- | --- | --- |
| 对象覆盖 | R 中多少对象在 D 中有 ≥τ 的代表 | D, O, X, R, τ | 把覆盖率读成泛化率 |
| 任务迁移 | 在 D 上训练的 M 能否在 R 上完成 T | + T, M（含暴露状态） | 把掉分读成泄漏 |
| 配方收益 | 改变采样/聚类策略造成多少覆盖与性能差异 | + 对照训练预算 | 把一次训练的差异读成策略效果 |
| 推理风险 | 当前输入相对预训练集的风险与 confidence 如何组合 | + 校准集、独立 V | 把相似度当失败概率 |

因此 `validated` 不是一个全局状态。证书必须逐主张记录：用了哪个验证器、该验证器独立于什么、通过条件是什么。一份证书可以同时持有"对象覆盖已认证"与"任务迁移未验证"。

**结构性推论**：`materialize_plan` 的三种用例不是同一证书的三个视图，而是三种不同的证据要求。`recipe` 与 `risk` 若引用未经各自验证器的证书，只能输出 `provisional`，即使对象覆盖已 certified。

**可证伪内容**：若实测表明四类主张在同一份证据下的判决总是同向且同幅（例如覆盖率高的数据集在所有任务上都更好），则可退化为单一验证器；只要出现一个反例，本条成立。

**边界**：本条不要求为每类主张实现独立流水线，只要求独立的验证器与独立的强度字段。
