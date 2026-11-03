---
tags:
  - context
---

# Similarity Artifact Must Be Sparse And Threshold Indexed

## time

2026-10-22

## lineage

- [[similarity_structure_is_not_a_certificate]]: 该条规定 S 是可复用对象；本条规定该对象在 600 GiB 量级上的可计算表示。
- [[surface_metric_computability_and_claim_strength_run_opposite]]: 该条说明输入档位决定可算的量；本条说明数据结构档位决定可算的统计量。
- <https://modelcontextprotocol.io/specification/2025-06-18/server/tools.md>: 结构化结果契约，用于判断稀疏产物需要携带哪些自描述字段。

## relation

- [[similarity_structure_is_not_a_certificate]]: A ⊑ B.

## description

在 64 个数据源、约 609 GiB 的规模上，`N × N` 相似度矩阵不可能物化。因此 `S` 的表示不是矩阵，而是**稀疏且按阈值索引的结构**：每个查询对象的 top-k 近邻、在若干预设阈值上的成员关系、以及显式的未测量标记。三条表示要求：

1. **稀疏**：只保留超过声明下限 `τ₀` 的近邻；`τ₀` 以下不存，但要记"已搜索且低于下限"，与"未搜索"区分。
2. **阈值索引**：coverage 只需要"每个参考对象是否存在一个相似度 ≥ τ 的 D 成员"，这是对稀疏行的取最大值，不是全矩阵统计。多个 τ 对应多条读路径，不能靠重算。
3. **未测量与低相似度分列**：稀疏结构里必须能区分"测了但低于阈值"与"根本没有可比对记录"，否则三值状态在表示层就丢失了。

**哪类结论因此不可算**：任何需要精确全矩阵统计量的结论——两两平均距离、距离分布的分位数、全局谱——在稀疏表示下只能近似，且近似误差不随 N 稳定。证书不得声明这类量，除非另做全量计算并把代价写进声明。

**可操作要求**：`S` 的 schema 里放 `search_rule`（k、下限、召回策略）、`measured_pairs_estimate`、`unmeasured_units`。coverage 的分母从 `unmeasured_units` 直接取，而不是从对象总数推。

**可证伪内容**：若某个必需结论确实依赖稀疏结构不能给出的统计量（例如它只由平均距离决定），则要么放弃该结论，要么改表示；只要存在一个这样的结论，本条对"用稀疏结构承载全部结论"的主张就被推翻。

**边界**：本条约束的是数据集级覆盖。单个抗原或单个抗体的逐对比较不受影响，可以直接全量计算。
