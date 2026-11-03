---
tags:
  - context
---

# Split Plan Cannot Be Derived From Coverage Alone

## time

2026-10-22

## lineage

- [[similarity_split_score_drops_do_not_identify_leakage]]: 按相似性划分后掉分同时混入训练量、难度、近邻结构与标签组成变化。
- [[held_out_certificates_are_relative_to_a_declared_validator]]: 划分本身不是验证器，留出集 + 判定器 + 通过条件才是。
- <https://arxiv.org/abs/2610.23845>: SEER-Repro 用 agent 复现 77.4% 的原子主张，并对分析选择做稳健性重跑，说明"划分选择"本身是需要显式枚举的维度。

## relation

- [[four_claim_strengths_need_four_validators]]: A ⊑ B.

## description

原型把 `(1 - coverage)` 的缺口映射成 risk 等级，又把 covered/uncovered 直接当 split 的两侧。两者都是把覆盖结构当成任务结论。

划分的正确形式是：**给定 `(O, X, τ)`，枚举若干可辩护的划分方案，并对每个方案声明它检验什么假设。**

- 按相似性聚类划分检验"对未见族的外推"；
- 按时间或来源划分检验"对未来批次的迁移"；
- 随机划分不检验泄漏，只检验同分布拟合。

这三者不可互相替代，也不可由同一个 `τ` 派生。因此 split 产物应当是一张**方案表**，每行带它要证伪的假设与该方案的已知混淆项（例如按来源划分同时改变了样本量分布）。

**为什么不能只给一个划分**：划分后的性能差必须能被归因，而归因需要对照。只给一个划分，掉分既可以解释为泄漏也可以解释为难度，这是 [[similarity_split_score_drops_do_not_identify_leakage]] 已经说过的事。

**可操作要求**：split 产物输出 `plans: [{id, rule, hypothesis, confounds, realized_group_sizes}]`，并要求至少一个"不检验泄漏"的基线划分作为参照。

**可证伪内容**：若存在一个划分规则，其下的性能差可以只由覆盖统计预测（不需要对照划分），则该规则可以单独输出，本条的限制解除。
