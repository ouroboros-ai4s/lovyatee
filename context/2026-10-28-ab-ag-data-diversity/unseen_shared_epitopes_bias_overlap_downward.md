---
tags:
  - context
---

# Unseen Shared Epitopes Bias Overlap Downward

## time

2026-10-21

## lineage

- ../bodn/2026-10-21-abag-sampling-coverage-theory-survey-s8.md: 第 8 条（Chao et al. 2006，丰度型相似性指数，以及校正未观测共有类别的估计量）。

## relation

- [[sampling_redundancy_and_biological_convergence_are_not_identifiable_from_database_frequencies]]: A ∥ B.

## description

比较两个数据源的表位重叠时，两边都没采到的共有表位使 incidence 型相似性指数系统性偏低，方向固定。这是统计量自带的抽样偏差，与「不可识别性」是两件事。

Chao et al. 2006 为对称、齐次的相似性指数给出概率推导，用 Laplace 型方法校正未观测到的共有类别；模拟显示缺失比例大时校正估计量的偏差显著下降。

方向可自证（我算的）：incidence 版 Jaccard 为 a/(a+b+c)，漏掉一个共有类使 a → a−1 而 b、c 不变，则 J′ − J = (a − (a+b+c)) / [(a+b+c)(a+b+c−1)] < 0。Sørensen 同理。所以「未采到的共有表位降低重叠」在 incidence 族上是恒成立的，不是有时高有时低。

决策方向：数据源显得比实际更不重叠 → 新颖度被高估 → 倾向「还要继续收」。所以 (b) 的默认偏差是**低估**冗余，而且偏的方向已知、偏量可算。

与不可识别性的区别：[[sampling_redundancy_and_biological_convergence_are_not_identifiable_from_database_frequencies]] 说观测集中度无法在「真实集中」与「收录偏差」之间归属；本条说的是重叠统计量本身的抽样偏差，有已知方向、有校正量。一个关于归因，一个关于量的偏差。两者互不细化。

迁移约束：校正要求两源使用同一套「物种」定义。τ 或 linkage 不同时共有类别不可对齐，校正无从计算 —— 这是硬约束的一种具体形态（跨抗原对应另见 [[cross_antigen_contact_overlap_requires_declared_correspondence]]）。

可操作要求：报重叠率时同时给两侧 coverage 与所用指数族；不同 τ 的两个源先重聚类到共同定义，否则该重叠率标为未决，不标为低。

可证伪内容：对同一抗原、同一 τ、同一 linkage 的两个独立分源 panel，用已知真值检验；若校正后的重叠率与真值之差大于未校正者，则校正对该指数失效。

竞争解释要排除的那一个是：观测到的低重叠率可能只是「两个数据源确实更不重叠」，而不是抽样偏差。这条排除它的方式不是引用，而是符号与量级 —— 偏差方向由代数固定为负，且大小随未观测共有类的比例单调增。若两个源的真实重叠结构相同，观测差异就只剩这一项；只有当两个源的真实重叠本身不同时，代数项才不足以解释全部差额，那时本条判为未决而非偏低。
