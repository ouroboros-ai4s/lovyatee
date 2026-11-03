---
tags:
  - context
---

# Paratope Diversity Requires Antibody Format Calibration

## time

2026-10-20

## lineage

- ../bodn/2026-10-20-abag-epitope-identity-survey-s1.md: 第 21 条（Mitchell & Colwell 2018，VHH 与常规抗体对比）为主，辅以第 22、23、24 条（germline 结构多样性、VH 分组、germline 编码 B 细胞）。

## relation

- [[epitope_partitions_are_not_axiomatically_nested]]: A ⊑ B.

## description

VHH（单域）与常规 VH-VL 的 paratope 不是同一类对象，把它们放进同一个多样性统计会得到依赖于混合比例的结论，且偏差方向不能预设。

Mitchell & Colwell 2018 在 156 对 VHH-抗原与 156 对常规抗体-抗原结构上比较：VHH 的 paratope 在**参与结合的骨架片段、接触残基、接触类型**三方面都更多样，且接触倾向与序列变异的关系不同于 VH。原因是可以补偿 VL 缺失的那部分接触被转移到原本不参与结合的骨架区域 —— 所以按「CDR 接触残基」定义的 paratope 对 VHH 是系统性不完整的。

这条与 [[sequence_diversity_bias_has_no_fixed_sign]] 是同一现象的两面：R 的符号不稳定，一部分正来自 format 混合。所以在计算 R 或任何 paratope 多样性指标之前，必须先固定 format，再变动抗原侧。

可操作的两步：

1. paratope 描述子集必须按 format 分别定义 —— VHH 要包含骨架接触，常规抗体可以只用 CDR 环；
2. 若必须合并统计，报告混合比例，并单独给出两层的指标，不能只给池化值。

与会议 §二.3 的关系：会上说「CDR 之外也存在少量接触位点（例如极短 CDR3 时由 Framework 补偿结合），目前没有统一理论，暂按小概率事件处理」。对 VHH 这不是小概率事件，而是常态。所以那条临时约定只适用于常规抗体，VHH 必须单独处理。

边界：VHH 的结论基于 156 个结构，其中 camelid 免疫来源占多数；人类重链抗体（VH-only）是否同构，目前证据不足。

## spill

S2=25 无构造反例，F4=50 无可证伪段。另有两处与被引条目相抵：正文写「可以补偿 VL 缺失的那部分接触被转移到原本不参与结合的骨架区域」，该机制在 s2 第 21 条（Mitchell & Colwell）中无对应；正文又说「偏差方向不能预设」，而被引条目本身写的是「会低估 VHH 一侧」。lineage 中第 22、23、24 条列出未用。

**复活条件**：把机制归因改为被引条目支持的表述（VHH 的 paratope 在骨架片段、接触残基、接触类型三方面都更多样，这一点条目里有）；删掉或标注「偏差方向不能预设」与被引条目的张力；补一个可证伪设计（按 format 分层重算某多样性指标，看混合比例与偏差的关系）。结论本身（paratope 统计须先固定 format）与 `vhh_is_out_of_domain_for_fab_calibrated_instruments` 一致，两条应合并考虑。
