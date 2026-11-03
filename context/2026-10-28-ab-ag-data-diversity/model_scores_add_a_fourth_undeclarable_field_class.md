---
tags:
  - context
---

# Model Scores Add A Fourth Undeclarable Field Class

## time

2026-10-21

## lineage

- [[diversity_reports_need_three_independent_field_classes]]: 提供三元组 (计数单位, 测量对象, 阶数权重) 与「不可补偿」的形式。
- [[pretraining_exposure_limits_model_based_diversity_validation]]: 提供模型继承暴露这一待声明项，以及「未见 ≠ 未知」的边界。
- [[protein_lm_scale_has_no_monotone_fitness_benefit]]: 提供「同一分数在不同规模下不对应同一 fitness 区间」的平移机制。

## relation

- [[diversity_reports_need_three_independent_field_classes]]: A ⊒ B.
- [[pretraining_exposure_limits_model_based_diversity_validation]]: A ⊒ B.
- [[protein_lm_scale_has_no_monotone_fitness_benefit]]: A ⊒ B.

## description

三元组把多样性报告拆成计数单位、测量对象、阶数权重三组必要条件，且三组不可补偿。只要报告里的数字来自模型打分而不是来自观测计数，就必须加第四组 —— 而第四组与前三种有一个性质上的区别，正是这个区别让它必须单列。

四组里前三组是**可执行的声明**：写「单位取克隆、τ=0.85、linkage 取单连锁」，读者就能复算。第四组不是。

**M 类，打分模型的状态**：模型身份、语料版本与时间截断、两侧对象在语料中的暴露状态、模型的规模档位。

第四组的关键差别在于：**它的取值常常是「未知」而不是「没有」。** 前三组里，缺失的字段可以补上、补上之后数字有定义；M 类里，「语料不可审计」是一个不可消除的取值。而 [[pretraining_exposure_limits_model_based_diversity_validation]] 已经证明「未见」不能由「没有记录」推出 —— 所以一个不可审计的模型，其暴露状态只能是未知，任何读数都不能被解释成「隔离干净」。

这不是精度问题，与 [[surface_metric_computability_and_claim_strength_run_opposite]] 同构但方向不同：那里是输入档位决定可算性，这里是输入档位**存在但不可验证**。

第二个必须单列的机制来自规模轴。[[protein_lm_scale_has_no_monotone_fitness_benefit]] 报告 p(sequence) 随规模同向平移、分数在越过某个规模后不再对应同一 fitness 区间。所以 M 类里模型规模不是一个可以「声明了就固定」的参数，它改变分数的**含义**。把 7B 模型给出的分数与 650M 模型给出的分数并表，等同把两个不同的测量单位混在一列 —— 而这一点在读数里完全看不出来。

**于是得到一条父记录都没有的操作判据：无法声明的字段，不能通过「已声明其余三组」来弥补，但可以强制降级结论的类型。** 具体地：

- 三组可执行声明齐全 + M 类完全可审计 → 可作跨数据集比较。
- M 类部分未知 → 只能在同一模型、同一语料版本**内部**比较；跨模型比较必须标为未校准。
- M 类完全未知 → 分数只能当**排序线索**，不能当计数或比例。

第三档是最常被越界的一档。一条「用模型分数筛出的高多样性子集」在这个档里，其实只说明「这个模型把这个子集排在前面」，不说明该子集更多样。

条件方向：**必要**是声明 M 类至少到「模型身份 + 语料是否可审计」这一层 —— 否则读数没有解释对象。**不充分**是即使 M 类完全可审计，规模轴仍使跨规模比较需要额外的校准对照（同家族、同语料的规模阶梯）；所以「语料审清了就能跨模型比」不成立。

可证伪内容：若存在两个不同规模、不同语料的模型，在同一批序列上给出的分数排序秩相关为 1 且差值恒定（即只是一个单调变换），则规模轴不引入独立自由度，M 类可退化为单一模型身份，本条对该对模型失效。

边界：报告完全不使用模型输出（纯观测计数）时，M 类为空集，本条不适用。用模型但只做内部排序、不跨模型不跨数据集时，本条退化为「声明模型身份」这一条。
