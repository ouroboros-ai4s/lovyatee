---
tags:
  - context
---

# Chao1 Lower Bound Moves With The Threshold

## time

2026-10-21

## lineage

- ../bodn/2026-10-21-abag-sampling-coverage-theory-survey-s8.md: 第 6 条（Chiu et al. 2014，修改的 Good-Turing 下界，用 tripleton / quadrupleton 校正一阶偏差）。

## relation

- [[epitope_community_count_is_assay_resolution_limited]]: A ⊑ B.

## description

结论：Chao1 型下界在表位数据上不是保守下界。τ 收紧会把「至少还有多少个未观测类别」推高，且推高是二阶的。

经典 Chao1 为 S_obs + f1²/(2f2)，f1、f2 分别是 singleton 与 doubleton 类数。**这是经典结果，不归给某篇摘要。** τ 收紧把一个 doubleton 簇拆成两个 singleton：f1 +2、f2 −1、S_obs +1，分子按平方抬高、分母同时压低。

数值（我构造）：起始 f1=20、f2=10、S_obs=100，下界 = 100 + 400/20 = 120。把 5 个 doubleton 拆成 10 个 singleton 后 f1=30、f2=5、S_obs=105，下界 = 105 + 900/10 = 195。**没有新数据进入，下界上升 62.5%。**

本条挣得的压缩：把一个看似属于「误差无固定符号」家族的估计量，单独挑出来证明它在 τ 这个轴上的方向是固定的 —— 这是把一条更一般的不可判断言细化成一个可操作的方向性结论，原文献没有这一层。

与「无固定符号」的关系：[[epitope_community_count_is_assay_resolution_limited]] 说观测社区数是联合函数、误差无固定符号 —— 那是对**观测计数**说的。对**下界**，τ 这一个轴的方向是固定的（收紧 → 上升），不能拿「无固定符号」为这个报数开脱。

Chiu et al. 2014 用修改的 Good-Turing 公式、借 tripleton / quadrupleton 校正一阶偏差，得到更紧的下界。更紧不改变它对 f1、f2 的依赖，只换系数 —— 放大机制仍在，常数不同。原文「对任何丰度分布成立」只覆盖丰度分布，不含物种身份固定与独立抽样两条前提。

可操作要求：报 Chao1 下界必须同时给 τ、linkage、f1 与 f2 的原始计数，并在 τ ±20% 上给区间。单一的「至少还有 K 个表位未采到」不可用。

可证伪内容：在已知真实簇组成的面板上，以真 τ 与 ±20% τ 分别计算，若三个下界的 95% 区间完全重叠，则放大效应该面板不成立。

必要与充分要分开说：**τ 固定**是「下界可用于跨数据集比较」的必要条件（上段给出的单调性就是必要性论证）；但它不是充分条件 —— 固定 τ 之后，f2 = 0 时经典 Chao1 退化（分母为零，需换 Chao1-bc 一类修正），且抽样不独立时 f1 本身是覆盖率的偏估计。所以「报了 τ 就能比」这个读法不成立。
