---
tags:
  - context
---

# Epitope Diversity Estimators Need Cross Antigen Validation

## time

2026-10-20

## lineage

- ../bodn/2026-10-20-abag-epitope-identity-survey-s1.md: 第 17、19、20 条（Ghanbarpour 2023 pLM paratope 相似性、Chomicz 2024 聚类基准、Waury 2025 模拟 repertoire 比较）。

## relation

- [[coverage_standardized_epitope_richness]]: A ⊑ B.

## description

表位多样性估计器的验证几乎都在**单抗原**的抗体集上做：一个 RBD 抗体 panel、一个 EGFR panel、一个 IL-6 体系。这类验证能证明「在该抗原内部能把已知分组分开」，但不能证明「在整个 repertoire 上的多样性估计可靠」。

原因是单抗原 panel 的多样性几乎全部由该抗原的少数显性模式构成 —— 估计器只需要区分几个模式就能在单抗原任务上表现良好，而跨抗原任务要求它在模式数、模式大小分布、以及噪声结构都不同的 panel 上都可靠。

要求：按**抗原家族**留出验证（held-out antigen family，不是 held-out antibody），并报告两个量：

1. 相对独立实验标注的丰富度误差（估计的表位簇数 vs 实验分箱/结构分类的簇数）；
2. 覆盖度估计误差（Good's coverage 的预测值 vs 外推验证值）。

第二个尤其重要，因为下游要的不是「有几个表位」而是「还差多少没覆盖」。只报丰富度误差会漏掉系统性偏差。

已知的具体缺口：Waury 2025 指出结构聚类方法此前只在单抗原抗体集上评估过，缺少在多样 repertoire 上的系统比较；Chomicz 2024 在 binder 检测与表位制图两个任务上横向比较五类方法，但仍是单抗原体系。

边界：若下游任务本身只在单抗原内做（例如某个靶点的抗体去冗余），这条不适用 —— 此时单抗原验证就是充分验证。

## spill

S2=0 且 S6=0，触发一票否决。全条无可证伪段，未点名任何竞争解释；S4=50 只折入了 Waury 的缺口陈述。

**复活条件**：给出一个具体的失败实例（某单抗原验证通过的估计量在跨抗原家族留出时误差有多大）；或把「须按抗原家族留出」这一要求写成可检验预测。
