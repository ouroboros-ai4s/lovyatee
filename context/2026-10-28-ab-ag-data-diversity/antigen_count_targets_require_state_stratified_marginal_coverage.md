---
tags:
  - context
---

# Antigen Count Targets Require State Stratified Marginal Coverage

## time

2026-10-22

## lineage

- [[diversity_is_a_task_conditioned_coverage_claim]]: 将收集规模解释为带声明的任务相关覆盖主张。
- [[annual_antigen_targets_require_marginal_interface_coverage_estimates]]: 提供抗原数量必须换算为跨抗原界面覆盖增量的预算问题。
- [[sufficient_sampling_returns_records_not_antigens]]: 说明采样理论返回的是记录数，不能直接换算为抗原数。
- [[antigen_state_ensemble_defines_the_epitope_denominator]]: 说明同一抗原名称下的表位分母由构象状态集合决定。
- [[sample_frequency_inflates_dominance_by_uncovered_mass]]: 说明样本频率会在未覆盖质量存在时夸大已见类别的优势。
- [[coverage_forecast_uncertainty_is_model_family_choice_not_sampling_error]]: 说明外推区间必须包含模型族选择造成的差异。
- ../bodn/2026-10-21-abag-sampling-coverage-theory-survey-s8.md: 第 1、5、6、7、10 条，提供丰富度、覆盖度和新增样本预测的估计框架。
- ../bodn/2026-10-21-abag-diversity-survey-appendix-three-axis-cross.md: 第 23 条，明确 90–100 抗原/年没有现成文献依据。

## relation

- [[diversity_is_a_task_conditioned_coverage_claim]]: A ⊑ B.
- [[annual_antigen_targets_require_marginal_interface_coverage_estimates]]: A ⊒ B.
- [[sufficient_sampling_returns_records_not_antigens]]: A ⊒ B.
- [[antigen_state_ensemble_defines_the_epitope_denominator]]: A ⊒ B.
- [[sample_frequency_inflates_dominance_by_uncovered_mass]]: A ⊒ B.
- [[coverage_forecast_uncertainty_is_model_family_choice_not_sampling_error]]: A ⊒ B.

## description

抗原数量目标只有在按抗原状态和界面单元分层后，才能解释为覆盖预算。需要估计加入候选抗原集合 A 相对于已有池 B 的边际收益 `Δμ(A|B)`，并同时声明每个抗原的构象状态集合、免疫背景、抗体采样深度、界面分类规则和参考版本。原始记录数、抗原数和已覆盖界面质量不是同一个抽样单位，不能用固定比例互换。

因此，“每年 90–100 个抗原”最多是预算占位。它只有在分层后的边际覆盖曲线、未见质量估计和模型族预测区间共同支持时，才可能升级为目标区间。把所有记录合并后再用丰富度或频率估计覆盖，会把状态多的抗原低估，把重复采样造成的频率集中误读成覆盖充分。

可操作形式是按抗原家族和状态集合建立增量表：每批新增抗原记录边际界面单元、独立抗体记录数、未见类别估计、下游留出性能和成本；内插与外推分开报告，外推同时报告合格模型族及其预测差。

可证伪内容：若在多个独立抗原家族中，固定记录数与固定抗原数给出的覆盖增量在预先容忍区间内一致，且构象状态、免疫背景和采样深度的分层不会改变目标排序，则本条在该数据族上退化为简单的抗原计数规划。

边界：单一固定抗原、固定构象状态和固定采样协议的内部比较可以直接报告记录数或类别数；跨抗原、跨状态或年度外推时，本条的分层要求重新生效。
