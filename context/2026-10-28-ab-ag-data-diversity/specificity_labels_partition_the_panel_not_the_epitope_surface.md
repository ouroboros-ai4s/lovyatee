---
tags:
  - context
---

# Specificity Labels Partition The Panel Not The Epitope Surface

## time

2026-10-21

## lineage

- ../bodn/2026-10-21-abag-computational-epitope-prediction-survey-s7.md: 第 13 条（Xu 2024，流感 HA 抗体特异性的可解释语言模型）、第 14 条（Yu 2025，监督微调提升特异性预测）、第 15 条（对比学习做序列到特异性预测）。

## relation

- [[epitope_partitions_are_not_axiomatically_nested]]: A ⊑ B.

## description

抗体特异性标签是对**抗原面板**的划分，与表位划分互不细化，因此不能当表位观测的验证目标。

标签来源：三条都用结合测定产生的标签 —— 「该抗体结合面板中的哪个抗原/亚型」—— 作用在一个离散面板上。综述说「特异性是可观测的表位代理」，这条不成立：代理至少要单向细化，而下面两个构造反驳显示两个方向都不细化。

反例一，同面板不同表位：抗体 a 与 b 都只结合 Ag1，但分别落在 Ag1 的两个不相邻 patch。同一特异性类，不同表位。

反例二，同表位不同类：抗体 c 结合 Ag1 与 Ag2 上的同一保守位点。特异性按唯一抗原定义时，c 落入「交叉反应」或单独一类，而其表位可与 a 相同。

数值（我构造的基础率论证）：面板 K=2、90% 抗体只结合 Ag1 时，常数预测器准确率 0.9。所报准确率由面板组成与正类比例决定，与表位分辨率无关。

所以特异性基准最多验证「抗原身份可再识别」，不能当表位覆盖的验收标准。这与 [[epitope_partitions_are_not_axiomatically_nested]] 的关系：那条说五类测量对象之间无必然映射；本条指出特异性标签是**第六类对象**，并且它连单向蕴含都不成立 —— 比「无必然映射」更强。

阈值与价态对标签可靠性的影响另见 [[cross_reactivity_breadth_is_not_a_function_of_the_antibody_alone]]，本条只谈划分结构。

可证伪内容：若在同一抗原面板上，特异性预测器对已知结合不同表位的两组抗体给出可复现的不同输出（留出验证），则特异性标签携带表位信息，本条被推翻。
