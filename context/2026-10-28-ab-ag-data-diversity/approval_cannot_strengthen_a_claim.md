---
tags:
  - context
---

# Approval Cannot Strengthen A Claim

## time

2026-10-22

## lineage

- [[held_out_certificates_are_relative_to_a_declared_validator]]: 该条给出证书强度上界 = 留出集独立性；本条把该上界落实为状态机内的不可越级规则。
- [[validator_fit_on_the_reference_certifies_membership_not_departure]]: 说明判定器在参考集上拟合时只能证明归属，不能证明偏离。
- <https://arxiv.org/abs/2606.09809>: EvalCards 的经验——报告完备度与结论可信度被混在同一分数里时，读者无法区分"写得全"与"测得对"。

## relation

- [[held_out_certificates_are_relative_to_a_declared_validator]]: A ⊑ B.

## description

原型里 `status == "certified"` 由 `human_decisions` 里的 `certificate: approved` 推出，而 `claims[].strength` 又由 `status` 推出。结果：**点一次批准，主张强度就上升一档。** 这与留出证书的定义相反——强度上界由独立证据给定，人工只能决定"放不放行"，不能决定"证不成立"。

拆分必须发生在数据模型里，不是措辞里：

```text
evidence_tier  ∈ {unmeasured, measured_internal, validated_independent}
                —— 只能由 V 的实际构成与独立性审计决定，不可人工提升
review_state   ∈ {pending, approved, rejected}
                —— 只能由人工决定，不改变 evidence_tier
publishable    = (evidence_tier ≥ 声明的门槛) ∧ (review_state == approved)
```

由此得到三条规则：

1. **批准不写进主张。** 证书可以带 `approved_by` 与时间，但 `claims[].strength` 只能引用 `evidence_tier` 与 `V` 的独立性判决。同一份证据被批准或被拒绝，强度字段逐字节相同。
2. **拒绝不可撤销地降级证据？不。** 拒绝只降 `review_state`；若人工认为证据本身不足，必须通过修改 `V`（产生新 revision）来表达，而不是改一个布尔。
3. **AI 无权设 `evidence_tier`。** 它只能提案 `V`；tier 由 schema 对 `V` 的结构检查与独立性审计共同决定。这是 AI 停止处的可执行形式。

**这也解决了一个原型没暴露的问题**：`evidence_tier` 是对 AI 输出的约束。若无此字段，模型只要把 `V` 写得像模像样，证书就是 certified，而语义上什么也没变。

**可证伪内容**：若存在一类主张，其强度只能由人工专家判断给出、无法由 `V` 的结构与独立性检验映射，则该类主张必须单列，不得复用本状态机。
