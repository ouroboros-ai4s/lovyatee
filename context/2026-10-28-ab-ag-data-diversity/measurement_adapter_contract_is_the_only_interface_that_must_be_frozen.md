---
tags:
  - context
---

# Measurement Adapter Contract Is The Only Interface That Must Be Frozen

## time

2026-10-22

## lineage

- [[core_is_two_functions_and_one_document_type]]: 内核三项；adapter 属于外壳，但错误会污染内核。
- [[missing_measurements_are_a_third_state_not_a_zero]]: adapter 必须能表达"测了但低"与"没测"。
- [[similarity_artifact_must_be_sparse_and_threshold_indexed]]: adapter 的输出是稀疏结构，不是矩阵。
- [[tool_inventory_is_not_a_measurement_protocol]]: 工具产生证据，不产生结论。

## relation

- [[core_is_two_functions_and_one_document_type]]: A ⊑ B.
- [[missing_measurements_are_a_third_state_not_a_zero]]: A ⊒ B.

## description

内核只有三项，其中 `Measure` 是可替换实现。既然可替换，就必须有一个**冻结的接口**，否则每个 adapter 用不同语义，内核的结论不可信。接口最小为：

```text
measure(request) -> artifact

request  = { items: [(id, payload_locator)], x_protocol: {...}, search_rule: {...} }
artifact = { s_digest, pairs: [{q, r, sim, method}], missing: [...],
             search_rule, provenance: {tool, version, params, invocation_id} }
```

四条硬约束：

1. **provenance 由 adapter 填，server 不得代填。** 原型的硬编码 `adapter: "local-declared-measurement"` 会让所有下游误以为来源已知。
2. **缺测显式化**：每个 `(q, r)` 要么有条目，要么在 `missing` 里带原因（`no_structure` / `below_floor` / `tool_failed`）。不允许省略。
3. **相似度归一到 [0,1] 且方向一致**（1 = 更相似）。不同工具的原始分数（E-value、TM-score、RMSD）在 adapter 内转换，并记录转换规则。
4. **`s_digest` 由 `(D,O,X,adapter_version)` 决定**，不是由调用者给。

**第四条是防伪的关键**：若 adapter 允许自报 digest，两个不同实现可以声称产出同一个 S。

**可证伪内容**：若目标用例只需要一个 adapter（例如只做序列相似性），冻结接口是过度设计，可直接写死；一旦需要第二种测量（结构、界面、表面），本条成立。
