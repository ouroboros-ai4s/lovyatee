---
tags:
  - context
---

# Diversity Reports Need Three Independent Field Classes

## time

2026-10-21

## lineage

- [[antibody_diversity_counting_unit_is_declared_not_derived]]: 计数单位与其参数、采样深度这一组待声明字段。
- [[epitope_partitions_are_not_axiomatically_nested]]: 测量对象（接触集 / 几何 / 竞争 / 逃逸谱 / 可及性）这一组。
- [[richness_ranking_is_threshold_ranking]]: 阶数 q、阈值 τ、连锁方式这一组。

## relation

- [[antibody_diversity_counting_unit_is_declared_not_derived]]: A ⊒ B.
- [[richness_ranking_is_threshold_ranking]]: A ⊒ B.

## description

三条父记录各自要求声明一组字段，但它们从未被放在一起比较过。放在一起会得到一个更强的结论：**这三是三个独立的自由度，任一组缺失，数字不是「不够精确」，是无定义。**

三组字段：

- **A 类，计数单位**：序列 / 克隆 / 谱系 / 结构类，以及该单位的参数（τ、距离定义、连锁方式）与采样深度。
- **B 类，测量对象**：接触残基集合、结合几何、竞争关系、逃逸谱、跨构象可及性。
- **C 类，加权与阶数**：Hill 阶数 q、按频率还是按功能加权。

对 [[epitope_partitions_are_not_axiomatically_nested]] 的 ⊒ 由 richness → community_count → coverage_standardized → contact_overlap → epitope_partitions 这条已有的链蕴含，按 cover-only 未重复写边；它在 lineage 里仍是父记录。

独立性是构造性的，每组固定另两组、只变本组即可：A 变（同一批序列，克隆阈值 τ 从 0.8 到 0.9）数字变；B 变（同一 panel，接触集划分改逃逸谱划分）数字变；C 变（同一划分，q=0 改 q=2）数字变。三组之间没有换算。

**不可补偿，这是本条真正新增的部分。** 三组的失效不是同一量纲上的精度损失，所以「我多声明了两组」不构成对第三组的任何弥补。可以构造一个两组全声明、第三组缺失而结论反向的实例：

- 设 dataset-1 有 3 个克隆，分布于 3 个逃逸组，各组等量；
- dataset-2 有 3 个克隆，全部属于同一逃逸组。
- A、B 都声明清楚：单位取克隆、对象取逃逸谱。此时 q=0（簇数）给两者都是 3，判「一样多样」；q=2 给 dataset-1 为 3、dataset-2 为 1，判「差 3 倍」。
- 结论的方向由未声明的 C 类决定，而 A、B 声明得再完整也不影响这一点。

反过来同样成立：C 类声明得再完整，若 B 类对象未定，两个不同的划分给出两个不同的 q 值，C 类无从作用。所以三组是三个正交的必要条件，不是一条有待补全的清单。

由此得到可操作形式：一份多样性报告的最小证书是三元组 (A, B, C)，**且证书按三元组签发，不按字段累加计分**。「报了单位、报了对象、没报 q」不是 2/3 完成度，是不可用。

条件方向：**必要**是三组全在 —— 上面的实例给出「缺 C 时方向由 C 决定」。**不充分**是三元组齐全后仍不唯一：同一组内部还有自由参数（A 内的连锁方式、B 内的表位分箱协议、C 内的权重来源），三元组给的是可复现的边界，不是唯一值。

可证伪内容：若存在一组固定了 A、B 却对 C 不敏感的数据集对（在 q ∈ {0,1,2} 上排序与差距完全不变），且该情形不是退化（如全部记录同类），则 C 类可与另两组分离，本条的「三组独立」在该数据集族上失效。

边界：只报单数据集内部一个数、不做跨数据集比较时，B 类退化为该数据集的实测对象、C 类退化为所报的那一个值，三组塌缩为对实测协议的一段描述，本条的证书要求不必展开。
