---
tags:
  - conclusion
---

# Diversity Is A Task Conditioned Coverage Claim

## time

2026-10-22

## lineage

- [[diversity_reports_need_three_independent_field_classes]]: 将计数单位、测量对象和阶数/权重确定为三个不可互补的声明类。
- [[model_scores_add_a_fourth_undeclarable_field_class]]: 补出模型身份、语料暴露和规模状态这一类不可完全审计的字段。
- [[redundancy_reference_sets_are_declarations_not_parameters]]: 说明参考集合是声明而非可扫描参数。
- [[held_out_certificates_are_relative_to_a_declared_validator]]: 说明留出证书必须绑定留出集、验证器和通过条件。
- [[epitope_object_choice_can_flip_panel_rankings]]: 说明测量对象改变可以直接翻转面板排序。
- [[coverage_forecast_uncertainty_is_model_family_choice_not_sampling_error]]: 说明覆盖外推必须声明模型族及其族间差异。
- ../bodn/2026-10-21-abag-diversity-as-evaluation-tool-survey-s4.md: 提供按任务评价多样性和严格留出划分的原始材料。
- ../bodn/2026-10-21-abag-general-ppi-surface-comparison-survey-s3.md: 提供跨抗原界面比较需要对应关系和观测协议的原始材料。
- ../bodn/2026-10-21-abag-diversity-data-volume-performance-survey-s5.md: 提供数据量、模型规模和性能关系尚未形成稳定规律的原始材料。

## relation

- [[model_scores_add_a_fourth_undeclarable_field_class]]: A ⊒ B.
- [[redundancy_reference_sets_are_declarations_not_parameters]]: A ⊒ B.
- [[epitope_object_choice_can_flip_panel_rankings]]: A ⊒ B.

## description

- [Diversity Is A Task Conditioned Coverage Claim](#diversity-is-a-task-conditioned-coverage-claim)
  - [time](#time)
  - [lineage](#lineage)
  - [relation](#relation)
  - [description](#description)
    - [Dataset merge](#dataset-merge)
    - [Similarity layer](#similarity-layer)
    - [The seven declaration slots](#the-seven-declaration-slots)
    - [Diversity as a coverage functional](#diversity-as-a-coverage-functional)

本条定义本项目要研究的问题：**多样性不是数据集自身的一个固定数值，而是在声明对象、观测协议、参考域、验证器、下游任务以及模型状态之后，对任务相关覆盖能力提出的可验证主张。**

一份 diversity 报告不是单一分数，而是一份带适用条件的覆盖证书：

```lean
Certificate = (D, O, X, R, V, T, M, result)
```

任一索引改变，原主张都不能自动迁移。数字可能仍然可计算，但不再自动具有跨数据集、跨对象、跨参考域或跨任务的解释。

### Dataset merge

数据集并集不是普通集合的 `union`。定义带有固定合并策略 `π` 的二元运算：

```lean
D_1 ∧_{dataset}^{π} D_2
  := merge(D_1, D_2;
           provenance, version, deduplication,
           quality_filter, sampling_rule)
```

结果必须保留来源、版本、去重规则、质量过滤规则和采样规则。于是：

```lean
D = Avidbase ∧_{dataset}^{π} OpenAlphaSeq
```

表示一个有明确生成历史的数据集对象，而不是两个记录表的无损拼接。若 `π` 固定且去重与采样具有确定性，该运算可在忽略记录顺序后进行链式组合；否则不同的合并顺序可能产生不同的 `D`。

### Similarity layer

`O` 指定比较对象的单位，`X` 指定如何观测和测量该对象。对数据集中的对象集合：

```lean
O(D) = {o_1, o_2, ..., o_n}

sim_{D,O,X}(o_i, o_j)
  := similarity measured under the declared X protocol

S(D, O, X)
  := [sim_{D,O,X}(o_i, o_j)]_{i,j}
```

例如：

```lean
O_ab = CDR-H3 object
X_ab = fixed numbering + amino-acid sequence + edit distance

O_ag = antigen surface patch
X_ag = patch residues + coordinates + contact graph + geometry
```

`S(D,O,X)` 是与下游任务无关的相似性结构，但不是完全脱离上下文的常数：`O` 决定比较单位，`X` 决定可观测字段与测量协议，`D` 决定对象集合、质量边界和可能的归一化方式。若 `X` 使用训练得到的表示，还必须声明该表示的训练来源和暴露状态。

相似性是 diversity 的基础，但 diversity 不是自动等于 `1 - similarity`。只有在相似度已规范化并且只讨论两个对象时，才可以定义 pairwise dissimilarity：

```lean
dissimilarity(o_i, o_j) = 1 - sim(o_i, o_j)
```

数据集层面的 diversity 还需要规定如何聚合相似性结构，以及相对于什么参考域判断 coverage。

### The seven declaration slots

```lean
D = observed dataset assembled under declared merge rules
O = comparison object and its unit of analysis
X = observable fields and measurement protocol
R = declared reference or target domain
V = held-out set + independent validator + pass condition
T = downstream task definition
M = model identity + exposure + scale/state
```

`O` 不是笼统的 `ab` 或 `ag`。如果抗体按 CDR 聚类、抗原按表面 patch 聚类，则应分别声明：

```lean
O_ab = CDR-defined antibody object
O_ag = surface-patch-defined antigen object
O_int = antibody-antigen interface object
```

`X` 不是字段名称的罗列，而是字段如何被规范化、表示、比较和转化为距离或相似度的完整协议。

`R` 不能从 coverage claim 中删除。它可以有两个角色：

```lean
R_ref    = defines the denominator or reference space for coverage
R_target = tests whether a rule transfers beyond D
```

例如：

```lean
D        = Avidbase ∧_{dataset}^{π} OpenAlphaSeq
R_target = D ∧_{dataset}^{π} other_db
```

当 `R` 尚不可完全观测时，只能声明一个冻结版本、来源范围、时间截点或任务代理域；不能把未知的真实全局空间当作已经被证明的 `R`。没有 `R` 时仍可报告 D 内部的 richness、cluster dispersion 或 relative diversity，但不能把它解释为对外部空间的 coverage。

`V` 不是 `cluster + split` 本身。`cluster rule` 规定如何分组，`split design` 规定如何生成 train/val/test，`V` 则规定用什么独立证据判断从 `D` 到 `R` 的覆盖主张是否成立：

```lean
V = (held_out R, independent measurement, pass condition)
```

下游模型在 `(T,M)` 上的表现是验证路径之一，主要支持任务条件下的迁移结论；它不能单独证明 cluster 在生物学上就是正确的。对象层差异、任务层泛化和数据或预训练泄漏需要分别审计。

`T` 与 `M` 保持分离：

```lean
T = what behavior is evaluated
M = which model, checkpoint, exposure, and scale/state are evaluated
E = (T, M)  # optional evaluation context
```

同一任务可以比较多个模型，同一模型也可以执行多个任务；因此可以在执行层使用 `E`，但问题定义仍保留 `T` 与 `M` 两个字段。

### Coverage and generalization

`coverage` 与 `generalization` 都可以写成从 `D` 指向 `R`，但二者不是同一件事：

```text
coverage:
  D 覆盖了 R 多少对象空间

generalization:
  在 D 上训练的模型能否在 R 上完成 T
```

coverage 是对象空间关系。对 `R` 中的对象，检查 `D` 中是否存在达到阈值 `τ` 的代表：

```text
covered(r; D, O, X, τ)
  := ∃ d ∈ D : sim_{O,X}(d, r) ≥ τ

Coverage(D → R | O, X, τ)
  := Σ_{r ∈ R} w(r) · 1[covered(r)]
     / Σ_{r ∈ R} w(r)
```

generalization 是模型迁移关系：

```text
f_D = Train(M, D, T)

Generalization(D → R | T, M)
  := Performance(f_D, R, T)
```

因此，`R` 不是对 `D` 执行 generalize 的主体；模型在 `D` 上形成规则，再到 `R` 上接受检验。coverage 可能是 generalization 的结构性前提或解释变量，但二者不等价：高 coverage 可能因标签噪声、模型容量或未观测因素而产生低 generalization，低 coverage 也可能在任务足够简单时产生高 generalization。

当 `R` 同时承担参考域和外部迁移测试域时，应在验证协议中声明其角色：

```text
R_ref    = defines the coverage denominator
R_target = tests transfer beyond D
```

更细的证书可以显式区分二者：

```text
DiversityCertificate
  = (D, O, X, R_ref, R_target, V, T, M, result)
```

当前七槽位表示仍可保留 `R`，由 `V` 说明该 `R` 是 coverage 参考域、留出目标域，或二者兼有。

### Diversity as a coverage functional

相似性层先产生结构，再由参考域和验证条件把它转化为 coverage claim：

```lean
S(D, O, X) = similarity structure

Diversity(D, O, X, R, V, T, M)
  = F(S(D, O, X), R, V, T, M)
```

因此本项目要研究的不是一个脱离条件的“最佳 diversity 分数”，而是：哪些 `O/X` 相似性结构、参考域 `R`、验证器 `V`、任务 `T` 和模型状态 `M` 的组合，能够稳定预测目标空间中的任务泛化与覆盖；哪些只改变报告口径；哪些会翻转排序或 coverage 判决。

最小研究对象仍然是可复算的覆盖证书：

```lean
(D, O, X, R, V, T, M, result)
```

证书必须能复算、能指出未测区域，并能在改变一个索引时重新检验。年度抗原数量只能作为该证书给出的覆盖增量和预测区间的预算结果，不能预先当作多样性的定义。

可证伪内容：若在预先声明的多个对象、观测协议、参考域、验证器和模型状态下，所有合格数据集的排序与覆盖结论均保持不变，且差异小于预设容忍度，则本条的“索引化主张”在该任务族上退化为单一可迁移指标。

边界：只描述一个固定数据集内部、固定测量协议下的原始计数时，本条不要求展开全部索引；一旦比较数据集、预测未见对象、外推 coverage 或报告模型分数，七类声明重新成为问题定义的一部分。
