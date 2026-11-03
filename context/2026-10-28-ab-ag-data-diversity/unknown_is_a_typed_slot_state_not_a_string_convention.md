---
tags:
  - context
---

# Unknown Is A Typed Slot State Not A String Convention

## time

2026-10-22

## lineage

- [[diversity_is_a_task_conditioned_coverage_claim]]: 该条允许 `M` 在规划阶段缺席，但要求最终模型结论不能没有它。
- [[approval_cannot_strengthen_a_claim]]: 证据等级必须由结构决定；未知状态同样必须由结构决定。
- [[documentation_completeness_is_not_evidence_tier]]: 声明"已填"必须能与占位区分。
- <https://modelcontextprotocol.io/specification/2025-06-18/server/tools.md>: 工具契约要求输入在服务端再次校验，字符串约定无法承担校验。

## relation

- [[approval_cannot_strengthen_a_claim]]: A ⊑ B.

## description

原型允许 `{"status": "unknown"}`，但 schema 只是 `additionalProperties: true`。这意味着"未知"是一个**约定**，不是状态：任何自由文本、任何缺字段、任何拼错的 status 都能通过校验，而且下游无法机械判断"这个槽到底知不知道"。

未知必须是枚举状态，且与另外两类区分：

```text
known           有结构化取值
unknown         声明为不适用或当前不可获得，附理由
unfilled        还没处理
```

三者的下游含义不同：`unfilled` 阻止锁定；`unknown` 允许锁定但强制所有相关主张降级；`known` 才参与计算。把 `unknown` 与 `unfilled` 合并会在两个方向上出错——把没做的当成有意不做（过早锁定），或把有意不做的当成没做（永远锁不上）。

进一步，`unknown` 不是全有全无。`M` 可以知道模型族而不知道 checkpoint 与暴露状态；`V` 可以知道留出集而不知道判定器。因此每个槽内部需要**字段级的未知标记**，而非槽级。

**可证伪内容**：若存在一类槽，其取值空间无法预先枚举、只能自由文本（例如未来的任务类型），则该槽必须作为 `open` 类型单独处理，并在使用它的主张上强制标记为临时性；不能让整个 schema 退化为自由对象来容纳它。
