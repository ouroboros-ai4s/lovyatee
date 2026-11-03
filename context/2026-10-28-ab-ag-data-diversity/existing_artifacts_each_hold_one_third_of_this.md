---
tags:
  - context
---

# Existing Artifacts Each Hold One Third Of This

## time

2026-10-22

## lineage

- <https://www.biorxiv.org/content/10.1101/2025.05.30.656746v1>: Biomni——统一 action space + 通用 agent，强于编排，弱于声明。
- <https://arxiv.org/abs/2312.07852>: Workflow Run RO-Crate——强于运行溯源，弱于结论复算。
- <https://arxiv.org/abs/2606.09809>: EvalCards——强于报告结构，弱于测量语义。
- <https://doi.org/10.31234/osf.io/nhrwq>: multiverse / specification curve——强于选择空间报告，弱于计算实现。
- [[core_is_two_functions_and_one_document_type]]: 本项目内核为测量、派生、证书三项。
- [[tool_inventory_is_not_a_measurement_protocol]]: 工具清单不等于协议。

## relation

- [[core_is_two_functions_and_one_document_type]]: A ⊒ B.

## description

把公开产物按"是否提供测量语义 / 冲突消解 / 结论复算 / 选择空间报告"四项打分（有 = 1，无 = 0）：

| 产物 | 测量语义 | 选择空间 | 结论复算 | agent 编排 |
| --- | --- | --- | --- | --- |
| Biomni / STELLA | 0 | 0 | 0 | 1 |
| DataFlow / ICDL-Agent | 部分（算子固定） | 0 | 0 | 1 |
| RO-Crate / PROV-AGENT / DLProv | 0 | 0 | 0 | 部分 |
| Datasheets / Nutrition Label / EvalCards | 0 | 0 | 0 | 0 |
| multiverse / Comet 工具箱 | 0 | 1 | 部分 | 0 |
| DecoupleMix / CABS | 部分（配方语义） | 部分 | 0 | 0 |

没有任何一项在"测量协议 + 选择空间报告 + 结论可复算"三项上同时为 1。**空白不在算法，在组合**：把已有标准当作构件（PROV 做记录层、specification curve 做报告层、工具做测量层），中间缺的是把它们缝起来并强制"结论 = 输入的纯函数"的那一层。

这也限定了新颖性主张的写法：不能声称新的相似性度量，也不能声称新的 agent 框架；能声称的是**证书语义 + 复算校验 + 选择空间**的三元组，以及它在抗原-抗体覆盖问题上的落地。若主张写大了，评审会拿上面任一行指出已有工作。

**可证伪内容**：若检索到任一公开系统已同时具备三项（例如某个带 executable certificate 的科研平台），本条失效，产物应改为在其上扩展而非自建。

**边界**：本条只覆盖截至 2026-10 已检索到的公开工作；专利与未公开内部系统不在范围内。
