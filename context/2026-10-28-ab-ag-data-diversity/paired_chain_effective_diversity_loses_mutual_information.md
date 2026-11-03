---
tags:
  - context
---

# Paired Chain Effective Diversity Loses Mutual Information

## time

2026-10-20

## lineage

- ../bodn/2026-10-20-abag-antibody-side-diversity-survey-s2.md: 第 26 条（Jayaram 2012，VH/VL germline 配对偏好）的定量化。

## relation

- [[antibody_diversity_counting_unit_is_declared_not_derived]]: A ⊑ B.

## description

VH/VL 配对不是随机的（Jayaram 2012），但后果不是「组合上界不可达」，而是「有效多样性减少，减少量恰好等于互信息」。

对离散配对分布，恒等式是

H(VH, VL) = H(VH) + H(VL) − I(VH; VL)

在 exp(H) 意义下的有效多样性上：D_joint = D_VH · D_VL / exp(I)。

两个必须分开的量：

1. **组合计数上界仍然可达。** 非独立不排除任何组合存在。反例：`P = [[0.4, 0.1], [0.1, 0.4]]`，两边际都是 (0.5, 0.5)，偏离乘积明显，但四种组合全部存在，计数等于 2×2 = 4。只有当某个联合概率为 0、且该组合在边际独立假设下被计入时，计数才真的下降。
2. **被压低的是有效多样性**，压低量 = exp(I)。按边际熵相加（即假设独立配对）高估的部分有精确表达式，可直接测量。

实践后果：按单链统计 repertoire 多样性而不报 I，得到的是「若配对独立时的有效多样性」，这是一个上界，偏差方向固定且可算。这与 [[sequence_diversity_bias_has_no_fixed_sign]] 不同 —— 那条的方向不固定，这条有恒等式。

可证伪内容：在配对 repertoire 上估计 I，若 I 在各数据集上统计不可区分于零，则这条退化为「配对可忽略」，偏差量为零。

边界：只在 VH 与 VL 都测到的配对数据上定义。单链数据无法估计 I，只能声明未知。
