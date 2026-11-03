---
tags:
  - context
---

# Declaration Library Is The Reusable Asset

## time

2026-10-22

## lineage

- [[reference_domain_is_the_research_output_not_a_slot]]: `R` 与 `V` 是研究产出，应作为独立、可复用的对象。
- [[core_is_two_functions_and_one_document_type]]: 内核只有测量、派生、证书三项；复用发生在声明层。
- <https://www.biorxiv.org/content/10.1101/2025.05.30.656746v1>: Biomni 的 Know-How Library 是按需检索的最佳实践与协议集合，而不是固化在代码里。
- <https://arxiv.org/abs/2512.16676>: DataFlow 的约 200 个可复用算子构成可组合基底，agent 只负责编排。

## relation

- [[reference_domain_is_the_research_output_not_a_slot]]: A ⊑ B.

## description

如果每次任务都让 AI 从自然语言重新构造 `O/X/R/V`，系统退回到"每次重造 diversity 定义"——这正是要避免的形态。可复用的资产不是代码，是**声明**：

- `R` 的构造（哪些抗原族、什么权重、怎样分层）一次做对，多份证书复用；
- `V` 的构造（留出集、判定器、通过条件）同样；
- `X` 的协议（字段、规范化、比对方法、阈值依据）按对象类型沉淀。

因此架构中应当有一个显式库：声明按类型、版本、适用条件存档，可被检索、引用、分叉。AI 的工作从"发明"变成"选择或最小修改"。

这与 Biomni 的 Know-How Library、DataFlow 的算子库同构，但对象不同：它们存的是**做法**，这里存的是**量什么、怎么算通过**。后者的复用率决定了整个系统是否真的比一次性脚本强。

**代价**：库需要治理（谁改、何时失效、如何分叉），否则会积累互相矛盾的 `R`。治理规则至少要求：每次被引用时记录，冲突时不覆盖而分叉。

**可证伪内容**：若实测表明在一个任务族内，`R`/`V` 的复用率接近零（每次都重写），则库只是目录，本节的主张退化为文档组织问题。
