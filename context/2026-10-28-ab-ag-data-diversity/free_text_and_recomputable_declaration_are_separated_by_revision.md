---
tags:
  - context
---

# Free Text And Recomputable Declaration Are Separated By Revision

## time

2026-10-22

## lineage

- [[unknown_is_a_typed_slot_state_not_a_string_convention]]: 未知必须结构化；这条与"让 AI 自由表达"直接冲突。
- [[agent_compiles_declarations_the_core_executes]]: agent 输出不能作为可复算输入。
- [[declaration_library_is_the_reusable_asset]]: 复用发生在声明层，要求声明可比对。
- <https://arxiv.org/abs/2512.07785>: 即便 temperature=0，agent 输出仍不确定，故自由文本不能进入证书。

## relation

- [[agent_compiles_declarations_the_core_executes]]: A ⊑ B.
- [[unknown_is_a_typed_slot_state_not_a_string_convention]]: A ⊒ B.

## description

矛盾的两侧：

- **改善的一侧**：`R` 与 `V` 是研究判断，需要自由表达（"我想覆盖生产域里那些有结构、有 KD、但没被反复研究的抗原"）。强制结构化会把研究者压成填表员，也会漏掉尚未命名的维度。
- **恶化的一侧**：证书要可复算。自由文本不能比较、不能校验、不能复算，一旦进入证书，`F` 就不再是纯函数。

**这不是取舍可以解决的**——两边都是硬要求。分离条件在**时间轴**上：

```text
exploration  自由文本            → 不进入证书，只进入对话与笔记
proposal     结构化 + 附 rationale（自由文本作为注释字段，不参与计算）
locked       结构化，rationale 冻结为不可变注释
revision     rationale 变化 → 不一定改结构化；结构化变化 → 新 revision
```

关键点：**自由文本不是被删除，而是被降级为不可参与计算的注释**。它保留在 `rationale` 字段里，可读、可审计、可作为下一版声明的来源，但 `F` 不读它。

第二条分离在**对象上**：`R` 的"意图描述"与"可观测定义"是两个字段。前者自由文本，后者必须是可枚举的（哪些族的名单、权重公式、时间截点）。意图可以模糊，观测定义不可以。

**残余冲突**：有些研究判断暂时无法结构化（新的表位分类法）。此时不能靠放宽 schema 解决，只能把该用例标为 `exploratory`，输出 report 而非 certificate——即降级结论类型，而不是降级结构约束。

**可证伪内容**：若实测表明研究者从不需要保留 rationale（结构化字段一旦填好就不再回看自由文本），则注释字段可以去掉，分离退化为"先写后结构化"的一次性流程。
