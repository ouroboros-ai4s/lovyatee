---
tags:
  - context
---

# Validity Envelope Is Computed From Missingness And Exposure

## time

2026-10-22

## lineage

- [[four_claim_strengths_need_four_validators]]: 四类主张各有验证器；本条说明每类主张的适用边界如何算出来。
- [[missing_measurements_are_a_third_state_not_a_zero]]: 缺测比例是 envelope 的第一维。
- [[model_scores_add_a_fourth_undeclarable_field_class]]: `M` 的暴露状态不可完全审计，只能作为边界条件。
- [[pretraining_exposure_limits_model_based_diversity_validation]]: 预训练暴露限制了基于模型的验证能说什么。
- <https://doi.org/10.1101/2024.01.14.575565>: 图 fMRI 的 61 步 / 102 选项分析空间，说明边界必须按维度枚举而非一句话声明。

## relation

- [[four_claim_strengths_need_four_validators]]: A ⊑ B.

## description

原型的 `claims[].limits` 是静态字符串，等于什么都没说。适用边界必须**由证书里已有的量算出来**，至少四维：

| 维度 | 取值来源 | 越界时的后果 |
| --- | --- | --- |
| 缺测率 `unmeasured/declared` | S 的 missing 统计 | 超过阈值 → 只能出 partial |
| 输入档位 | O/X 要求的输入 vs D 实际具备 | 档位不足 → 该类主张不可提出 |
| `M` 暴露状态 | known / unknown / partial | 含 `unknown` → 模型相关主张不可 certified |
| `R` 的可观测程度 | 冻结版本 vs 动态来源 | 动态 → 结论带时间截点，不可跨截点比较 |

因此 envelope 是一个**结构体加一段计算规则**，不是一个字符串数组。报告时按主张逐项给出：`envelope.axes[*].value`、`within`、`reason`。

**关键的工程含义**：这使得"这份证书在什么情况下会失效"成为可机器检查的字段，而不是作者自述。它也直接支持下游：拿到证书的消费者可以问"在我要用的 R 上，这份证书还在 envelope 内吗"。

**可证伪内容**：若实测表明边界主要由未枚举的第五维（例如标签噪声）决定，而上述四维不能区分通过与失效的样本，则 envelope 需要重定义，本条的四维不完备。
