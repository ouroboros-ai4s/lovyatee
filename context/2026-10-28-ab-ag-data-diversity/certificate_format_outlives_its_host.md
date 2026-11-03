---
tags:
  - context
---

# Certificate Format Outlives Its Host

## time

2026-10-22

## lineage

- [[certificate_must_be_verifiable_offline]]: 证书必须能在没有产生它的进程时复核。
- [[core_is_two_functions_and_one_document_type]]: 内核是函数与文档类型，不是插件。
- [[agent_compiles_declarations_the_core_executes]]: 宿主只搬运声明与证书，不定义语义。
- <https://arxiv.org/abs/2312.07852>: RO-Crate 被六种工作流系统实现，说明格式可跨宿主存活的先例。

## relation

- [[certificate_must_be_verifiable_offline]]: A ⊑ B.

## description

MCP、skill、plugin manifest 都是**投递通道**，生命周期以年计；证书格式的生命周期以项目计。把格式绑在通道上，等于让结论随宿主版本失效。

因此分层应当是：

```text
format + verifier   —— 无宿主依赖，纯文本 + 一个校验函数
core (Measure / F)  —— 可用任意语言实现，只要通过 conformance suite
adapters            —— 工具包装，各自带 provenance
host bindings       —— MCP server / skill / CLI / notebook，随时可换
```

判据很简单：**删掉所有 host binding，证书还能被验证吗？** 能，则格式独立；不能，则格式在通道里。

这也决定了实现顺序：先有 format 与 conformance suite（一组固定的输入与期望证书），再有任意一个宿主绑定。反过来做（先写 MCP server）会让 format 被传输层的便利性塑形——原型的 `RUNS` 字典就是这种情况。

**可证伪内容**：若项目最终只在一个宿主上使用、且不打算归档证书，则格式独立性没有收益，可以合并进宿主实现。
