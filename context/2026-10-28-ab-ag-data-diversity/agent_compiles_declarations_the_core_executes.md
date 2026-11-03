---
tags:
  - context
---

# Agent Compiles Declarations The Core Executes

## time

2026-10-22

## lineage

- <https://doi.org/10.3390/ijgi15060238>: ICDL-Agent 用 schema 约束的工作流生成 + 有界修复，在领域工具注册表上把自然语言映射为可执行流水线，并强调可复现。
- <https://arxiv.org/abs/2512.16676>: DataFlow 用约 200 个可复用算子与 PyTorch 风格 API 构建流水线，再由 agent 把自然语言规格翻译为可执行流水线。
- <https://arxiv.org/abs/2512.07785>: HEP 案例把 LLM agent 与 Snakemake 组合——工作流管理器强制确定性，agent 只生成与修复代码；但即便 temperature=0，最终输出仍有随机变化。
- [[tool_inventory_is_not_a_measurement_protocol]]: 工具清单不等于协议；本条规定 agent 的产物是协议声明而非直接执行。

## relation

- [[tool_inventory_is_not_a_measurement_protocol]]: A ⊑ B.

## description

已有系统的共同结构与我们的方案同构：**agent 负责把自然语言意图编译成受约束的规格，确定性执行器负责跑规格。** 差别在于编译产物是什么：

| 系统 | 编译产物 | 确定性由谁保证 |
| --- | --- | --- |
| ICDL-Agent | 工具调用工作流 | 工作流 schema |
| DataFlow | 算子图 | 框架 |
| HEP+Snakemake | CWL/Snakefile | 工作流管理器 |
| 本项目 | `(D,O,X,R,V,T,M)` 声明 + 证书 | 声明哈希与纯函数 `F` |

第三种与其他三者的关键差异：**工作流保证"步骤按序执行"，不保证"结论是输入的纯函数"**。Snakemake 能让同一条命令重跑，但不会告诉你同一个 coverage 数字是否由同一份证据推出。所以我们的确定性对象不是执行计划，是声明与证书。

一条来自 HEP 的实证约束：即使 temperature=0，采样参数默认值仍使 agent 输出不完全确定。因此**不能把 agent 的自由文本当作可复算输入**；只有结构化声明可以进入证书。agent 的对话是过程，不是产物。

**可证伪内容**：若存在一种 agent 输出形式，其非确定性不影响结论复算（例如输出已被完全规范化且校验和稳定），则可不要求结构化声明，本条放宽。
