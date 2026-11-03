---
- tags:
  - context
---

# One Surface Descriptor Can Define Cross Antigen Coverage

## time

2026-10-22

## lineage

- ../bodn/2026-10-21-abag-general-ppi-surface-comparison-survey-s3.md: 汇总多种界面粒度和几何/理化描述子，未给出跨任务通用的单一距离。
- [[cross_antigen_contact_overlap_requires_declared_correspondence]]: 说明跨抗原比较的对应关系必须单独声明。
- [[interface_diversity_metrics_require_metric_specific_observability]]: 说明不同指标对可观测输入的要求不同。
- [[antigen_surface_patch_geometry_is_the_unfilled_collection_axis]]: 将界面几何与收集设计的交叉区域标为研究缺口，而非现成标准。

## relation

- [[cross_antigen_contact_overlap_requires_declared_correspondence]]: A ⊥ B.
- [[interface_diversity_metrics_require_metric_specific_observability]]: A ⊥ B.

## description

这是一个被调研材料诱发、但不能保留为 son 的快捷主张：只要选定一个表面几何描述子，就可以直接得到跨抗原的表位覆盖率和收集优先级。

它把描述子相似度、表位对应、覆盖质量和任务效用压成一个量。现有材料支持的是“某些描述子在特定输入和任务上可用”，不支持“一个描述子对所有抗原、状态集合和下游任务都提供同一覆盖语义”。不同粒度的界面对象需要不同输入，跨抗原对应关系也不能由描述子名称自动补出。

## spill

缺少跨抗原校准、独立留出验证和任务条件；把几何排序误读成覆盖证书。复活条件是：在多个抗原家族和明确状态集合上，预先比较至少两种描述子，声明对应规则和可观测输入，并证明某一描述子在独立任务上的覆盖增量与性能增量稳定优于替代方案。
