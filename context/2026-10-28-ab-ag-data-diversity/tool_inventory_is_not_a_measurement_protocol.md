---
tags:
  - context
---

# Tool Inventory Is Not A Measurement Protocol

## time

2026-10-22

## lineage

- <https://www.biorxiv.org/content/10.1101/2025.05.30.656746v1>: Biomni 用 150 个分析工具、25 个生物领域构成统一 action space，由 action discovery agent 从文献中挖掘。
- <https://arxiv.org/abs/2410.05080>: ScienceAgentBench 在 102 个来自 44 篇论文的数据驱动任务上，最强 agent 三次尝试仅独立解决 32.4%。
- <https://doi.org/10.1145/3770855.3817556>: BioDataLab 在 100 个上游数据库整理任务上，最强模型成功率 40%，瓶颈在多步工具编排与格式遵循。
- [[diversity_is_a_task_conditioned_coverage_claim]]: 该条要求 `X` 是"字段如何被规范化、表示、比较"的完整协议，而不是字段名罗列。

## relation

- [[diversity_is_a_task_conditioned_coverage_claim]]: A ⊑ B.

## description

当代 agent 环境的主流做法是把工具集合成 action space（Biomni：150 工具、25 领域），让模型在运行时自行组合。这对探索性分析有效，但它与"测量协议"是两件不同的东西：

- **工具清单**回答"能做什么"；**协议**回答"做出来的数是什么意思"。
- 同一组工具、不同参数，可以给出判决相反的相似性结构；Biomni 的环境里没有一个对象记录这层声明。
- 能力基准给出了上界：在上游整理类任务上，最好的模型也只有 32–40% 成功率，且失败集中在多步编排与格式遵循——恰好是声明槽最容易失守的地方。

因此架构上必须把两者分开：**工具侧只产出带 provenance 的原始测量；协议侧是独立的、可校验的声明对象；结论侧是纯函数。** 这也解释了为什么"把 O/X 包装成 MCP 就能用"不成立——包装解决调用，不解决语义。

反过来说，agent 的价值不在替代协议，而在**提出协议候选**并把人类从不熟悉的领域词汇里带出来。

**可证伪内容**：若实测表明由模型在工具空间内自选流程、不写显式 `X` 协议，产出的覆盖判决在重复运行间与跨数据集比较中保持一致，则声明层可省，本条失效。

**边界**：单个数据集的探索性画像（richness、聚类分布）不需要完整协议；一旦跨数据集比较或外推，本条成立。
