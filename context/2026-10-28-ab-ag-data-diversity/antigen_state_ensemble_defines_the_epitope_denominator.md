---
tags:
  - context
---

# Antigen State Ensemble Defines The Epitope Denominator

## time

2026-10-21

## lineage

- ../bodn/2026-10-21-abag-experimental-ground-truth-survey-s6.md: 第 3 条（Abdiche 2012，同一抗原制备物内部存在多种表位状态）、第 25 条（McLellan 2019，RSV F 主要抗原位点的替代构象）、第 32 条（Sikora 2021，糖基外套遮蔽面积大于静态结构所示）。

## relation

- [[epitope_diversity_is_a_joint_antigen_immune_background_property]]: A ⊑ B.

## description

「某个抗原有几个表位」的分母不是抗原名称，而是一组被声明的构象状态。

三条证据各自来自不同协议。Abdiche 2012 用无标记生物传感器分箱，发现同一抗原制备物内部存在多种表位状态 —— 这是**分母**问题：同一个 name 下可以有多个可区分的结合面。McLellan 2019 报告 RSV F 主要抗原位点存在替代构象，同一序列、不同构象给出不同位点几何。Sikora 2021 对含四个全长全糖基化 spike 的 410 万原子体系做多微秒分子动力学，报告本征柔性的糖基外套遮蔽面积大于静态结构所提示 —— **这是模拟结论，不是实验测量**，不得当实验事实引用。

三条合起来：固定抗原序列、固定免疫背景之后，每抗原的表位数仍不是单值。这是 [[epitope_diversity_is_a_joint_antigen_immune_background_property]] 的特例 —— 那条说抗原项参与决定，本条说抗原项本身是集合而非点。

后果落在分母上。跨研究比较「每抗原 N 个表位」之前，必须声明状态集合或取样协议（用哪个构象的代表结构、还是构象系综加权）。「每年 90–100 个抗原」若把一个制备物当作一个分母单位，构象状态多的抗原被系统性低估，而状态少的被高估 —— 误差随抗原而异，不能用一个常数修正。

可操作要求：报告表位数时同时给 (a) 所用结构或构象集合的来源，(b) 是否跨构象求和，(c) 若跨构象，用的是什么加权。

可证伪内容：对同一抗原的全部已解析构象，用同一 τ 与 linkage 聚类得到完全相同的表位簇集合，则本条对该抗原不适用。
