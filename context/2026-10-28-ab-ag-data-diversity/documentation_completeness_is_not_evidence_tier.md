---
tags:
  - context
---

# Documentation Completeness Is Not Evidence Tier

## time

2026-10-22

## lineage

- [[approval_cannot_strengthen_a_claim]]: 该条区分证据等级与人工批准；本条区分证据等级与文档完备度。
- <https://arxiv.org/abs/2606.09809>: EvalCards 把复现性、文档完备度、provenance 风险、分数可比性做成四个独立信号，正是因为它们不能互相补偿。
- <https://arxiv.org/abs/1805.03677>: Dataset Nutrition Label 的模块化设计——诊断量与文档描述分开。

## relation

- [[approval_cannot_strengthen_a_claim]]: A ⊑ B.

## description

数据文档框架（datasheets、nutrition labels、model cards、EvalCards）共同的失败模式是：**填得全的卡片看起来比填得少的更可信**，但填写完备度只反映作者投入，不反映测量是否成立。EvalCards 的四个信号必须分列，正是为了阻断这种补偿。

对本项目直接的含义：声明槽全部填满（七槽都有对象、没有一个 `unknown`）**不构成任何证据**。一个把 `R` 写成 `{"domain": "production"}` 的声明，字面上合法，信息量为零。

三条规则：

1. 每个槽的"已填"必须可区分为**结构化**（可被 schema 检查、可被下游消费）与**占位**（自由文本）。只有结构化才算填了。
2. 证书不得以"声明完整度"作为强度依据；强度只由 `V` 决定。
3. 文档层的价值在**可发现与可复用**，不在认证。因此它应当与证书分离，不要合并成一个总分。

**可证伪内容**：若实测表明结构化声明完整度与证书在独立留出集上的通过率高度相关，则完整度可以作为预筛信号；但只要出现完整度高而通过率不高的样本，本条成立（大概率会出现）。
