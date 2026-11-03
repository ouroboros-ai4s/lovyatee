---
- tags:
  - context
---

# Paratope Prediction Is Antigen Agnostic

## time

2026-10-21

## lineage

- ../bodn/2026-10-21-abag-computational-epitope-prediction-survey-s7.md: 第 7 条（Parapred）、第 8 条（Paragraph）、第 12 条（ParaAntiProt）；第 9、10、11 条（Attentive Cross-Modal、ParaSurf、Geometric）作边界。

## relation

- [[paratope_diversity_requires_antibody_format_calibration]]: A ∥ B.

## description

抗体单侧输入的 paratope 预测器输出的是对参考抗原集合的边缘量，不能当作某抗体在某抗原上的表位观测。

Parapred 输入抗体序列，Paragraph 输入抗体结构与最小特征向量，ParaAntiProt 同时用抗体与通用蛋白语言模型 —— 三者都**不含抗原输入**。标签形式：抗体残基 r 为正，当且仅当参考复合物集中**存在某个**抗原使 d(r, a) < cutoff。同样是 ∃，这次对参考抗原集取。所以输出近似 P(r 是 paratope | 抗体)，与「该 paratope 落在哪个表位」无关。

Paragraph 的「feature 越少越说明结构本身携带信息」是表示论证，在此设定下不可证伪：抗原不在输入里，削减特征只检验抗体侧各描述子之间的冗余，不检验「结构是否携带 paratope 与抗原的对应」。要检验后者需固定 paratope、变动抗原 —— 而该任务的设计恰好排除了这个变动。不是该结论假，是它没有可观测的否定条件。

跨模态条目（第 9 条 Attentive Cross-Modal、第 10 条 ParaSurf、第 11 条 Geometric）含抗原输入，是本节唯一可能给配对量的类别；它们仍受「分数场 → patch」那一关的阈值与邻接图约束（见 [[residue_score_field_does_not_determine_patch_count]]）。

后果（推论，标为待检验假设）：把预测 paratope 聚类当作表位聚类，会把对接不同表面的抗体并到一起。合并方向固定，不能靠提高精度修正。与 [[paratope_diversity_requires_antibody_format_calibration]] 不互相细化：固定 format 不解决抗原边缘化，反之亦然。

可证伪内容：对同一抗体在 ≥2 个不同抗原上的实验结构，若 paratope 残基集合的差异可忽略，则抗原边缘化不损失配对信息，本条被推翻。

## spill

S2=12 无任何实例，F5=38 无操作要求。S5=60：「标签形式：抗体残基 r 为正，当且仅当存在某个参考抗体 a 使 d(r,a) < cutoff」这一并集标签设定在六条被引条目中均无出处，以事实语气写出。

**复活条件**：核实六个预测器的训练标签构造（README 或原文方法节），把并集标签这一步写成有出处的观察而非推断；补一个「同一抗体在两个抗原上的预测 paratope 差异」实例。
