---
tags:
  - context
---

# Provenance Document Is Not A Certificate

## time

2026-10-22

## lineage

- <https://arxiv.org/abs/2312.07852>: Workflow Run RO-Crate 按 W3C PROV 对齐，打包工作流运行的全部输入、输出、代码，已被六种工作流系统实现。
- <https://arxiv.org/abs/2508.02866>: PROV-AGENT 把 agent 的 prompt、response、decision 也纳入 provenance，用 MCP 采集。
- <https://doi.org/10.7717/peerj-cs.2985>: DLProv 证明深度学习工作流的端到端溯源可行，开销上限 1.4%。
- [[certificate_must_be_verifiable_offline]]: 本条区分"记录发生过什么"与"结论能被重算"。

## relation

- [[certificate_must_be_verifiable_offline]]: A ⊑ B.

## description

溯源已有成熟标准与实现：PROV-O、RO-Crate、PROV-AGENT、DLProv。它们解决的问题是**"这次运行用了什么、谁触发的、产出是什么"**，并且已经被证明可以在真实工作流里低开销部署。

但溯源文档不保证结论可复算。它可以完整记录：输入文件哈希、工具版本、参数、环境、时间戳、执行者——然后仍然无法告诉你"这个 coverage 数字在同样输入下是否唯一"。缺的是那条纯函数约束：`F(S,R,V,T,M)` 必须确定。

两者的分野可以精确写成：

```text
provenance:  ∃ 一条记录，描述 (输入, 过程, 输出)
certificate: ∀ 相同输入，F 给出相同输出，且 verify(blob) 可离线判定
```

前者是存在量词，后者是全称量词。这不是实现细节的差别，而是可审计性的门槛。

因此本项目的产物应当**复用**已有的 provenance 标准作为记录层，而把"可重算"作为额外的一层要求；不要重新发明溯源格式，也不要以为有了溯源就有了证书。

**可证伪内容**：若存在一个 PROV 扩展能表达"结论是输入的纯函数"并强制校验，则本条的区分退化为命名差异。
