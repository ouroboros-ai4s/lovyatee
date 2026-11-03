---
tags:
  - conclusion
---

# MVP Is An Agent Driven Data Design Loop

## time

2026-10-22

## lineage

- [[agent_compiles_declarations_the_core_executes]]: 将 agent 编译与确定性执行收缩为一条可运行的 MVP 数据设计闭环。
- [[tool_inventory_is_not_a_measurement_protocol]]: `O` 与 `X` 仍由工具协议规定；本条把它们接入 Agent 生成的下游数据处理程序。
- [[diversity_is_a_task_conditioned_coverage_claim]]: 在保留 `D/O/X/R/T/M` 条件化的同时，本条把 coverage 从 MVP 核心降为可选的事后分析。

## relation

- [[agent_compiles_declarations_the_core_executes]]: A refines B.

## description

本项目的 MVP 是一个**由 Agent 驱动的数据设计闭环**，不是预先定义 coverage 或 universal diversity score。核心目标是：根据相似性结构、目标场景、下游任务、模型和评估定义，生成可执行的数据处理程序，并用真实模型实验验证其结果。

七个直接定义的输入为：

```text
D(.)       dataset
O(.)       protein 上被观测的对象，由工具协议规定
X(.)       相似性计算工具或工具组合，以 MCP 形式提供
R(.|prompt) 具体的外部 dataset，或自然语言描述的目标场景
T(.|prompt) 下游任务；进入 P 前转化为可执行任务要求
M(.)       待训练的 model
E(.)       evaluation definition
```

`E` 是确定性的评估程序定义，可包含：

```text
E = (eval_logic, metrics, baseline?)
```

实际评价数据单独记为：

```text
D_e       test split 或生产环境中的 evaluation data
```

相似性结果由固定输入计算：

```text
S = similarity(D, O, X)
```

Agent skill 根据相似性结果和任务要求生成可执行的数据处理程序：

```text
P = agent(S, R, T, M, E)
```

程序执行后得到用于训练或下游任务的数据：

```text
D_p = process(P, D)
M_t = train(M, D_p)
V   = evaluate(M_t, D_e, T, E)
```

其中 `V` 是最终实验结果，例如论文主结果表中的指标、基线比较和不同数据方案的表现。`P` 已经内含对 `S` 的使用逻辑，因此 `D_p = process(P, D)` 不再把 `S` 作为单独的运行输入。

本次实验的定义证书为：

```text
C = (D, O, X, R, T, M, E)
```

`C` 描述一次实验要处理什么数据、观测什么对象、使用什么相似性工具、面向什么场景和任务，以及如何评价。`P`、`D_p`、`M_t` 和 `V` 是根据这份定义执行得到的产物；`C` 本身不预先声称模型成功。

`coverage` 不属于 MVP 的基础概念。若后续需要，它只能从 `S`、`R`、`D_p` 或 `V` 中作为事后分析量派生，不能成为生成 `D_p` 之前必须成立的前置目标。
