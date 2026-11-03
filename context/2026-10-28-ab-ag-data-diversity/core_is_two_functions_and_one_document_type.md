---
tags:
  - context
---

# Core Is Two Functions And One Document Type

## time

2026-10-22

## lineage

- [[similarity_structure_is_not_a_certificate]]: 该条把测量与派生分成两层。
- [[certificate_must_be_verifiable_offline]]: 该条要求证书可脱离进程复核。
- [[agent_compiles_declarations_the_core_executes]]: 该条要求非确定性的 agent 输出止步于声明。
- [[reference_domain_is_the_research_output_not_a_slot]]: 该条把 R/V 提升为独立对象。

## relation

- [[similarity_structure_is_not_a_certificate]]: A ⊑ B.

## description

把各部分去重后，与宿主无关、与具体算法无关的部分只有三项：

```text
Measure : (D, O, X) -> S            # 一个接口，实现可替换
F       : (S, R, V, T, M) -> C      # 纯函数，语义固定
C       : certificate               # 一种文档类型，可离线校验
```

其余全部是**实现或外壳**，不是内核：

- 相似性算法 → `Measure` 的 adapter，各自带 provenance；
- 状态机与人工批准 → 证书上的字段与流程，不参与 `F`；
- MCP / skill / CLI → 宿主适配层，只搬运声明与证书；
- 三个下游用例 → 对 `C` 的查询或优化，不扩展内核。

这条推论的价值在于划界：**任何不能写成这三项之一的功能，都是在外壳上生长，应当被质疑。** 原型的 335 行里，属于内核的不足 80 行；剩下的状态机、门禁、in-memory 记账都不是科学，而是可以两周写完、也可以两周重写的工程。真正的研究产出是 `R` 的构造与 `V` 的独立性。

**边界**：`Measure` 的 adapter 协议（输入契约、provenance 字段、缺失语义）虽然属于外壳，但它一旦错，内核的结论就不可信。所以它是"外壳中必须有标准的部分"，不能各自发挥。

**可证伪内容**：若某个下游用例确实需要扩展 `F` 的语义（例如需要知道中间结构而不只是最终覆盖），则内核不止一项，本条应修订为三项加该用例的额外函数。
