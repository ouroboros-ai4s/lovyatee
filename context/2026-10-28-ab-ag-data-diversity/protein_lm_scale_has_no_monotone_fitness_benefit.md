---
tags:
  - context
---

# Protein LM Scale Has No Monotone Fitness Benefit

## time

2026-10-21

## lineage

- ../bodn/2026-10-21-abag-diversity-data-volume-performance-survey-s5.md: 第 1 条（Hou 2026，fitness 预测在中等 p(sequence) 区间最好，超过某个规模后下降；本池该节第 22 条是同一篇的重复条目，不另计证据）。

## relation

None.

## description

「用最大的蛋白语言模型给数据打分」没有依据。Hou 2026 报告：fitness 预测能力在**中等** p(sequence) 区间最好，模型越大越倾向给出偏高的 p(sequence)，超过某个规模后性能下降；机制落在 p(sequence) 是否匹配同源序列的演化模式。

三处措辞要收紧。第一，原文说的是越过某个规模之后下降，**不是单调反向**；把 U 形读成「越大越差」会推出「一律用小模型」，那是原文不支持的。第二，指标是零样本突变效应的排序，不是表征质量，也不是嵌入空间的距离统计。第三，已有信息不足以判断该 U 形对 ab-ag 配对打分是否成立 —— 这是待检验假设。

可构造的说明（我构造，非原文数据）：设真实 fitness 对 log p 单峰、峰值在 0，两个模型分别给出 0 与 +1 的 log p，后者在峰值左侧序列上的排序会反转。规模带来的不是精度提升，而是同向平移。

所以若用 pLM 分数判断某批配对值不值得收，规模是必须校准的自由度：同一家族、同一语料做规模阶梯，固定测试项，同时报预测 p(sequence) 的分布位置。这条不推出「小模型更好」，只推出单调性不成立。

两个条件方向分开说。**必要**：在把 pLM 分数当跨批次可比的量之前，必须先报出该规模在 p(sequence) 分布上的位置 —— 位置不同，同一个分数不对应同一个 fitness 区间。**不充分**：报出位置之后，分数仍不能直接跨规模比较，因为平移量本身依赖序列家族；所以「同位置就可比」不成立，要同家族内比。

与 [[pretraining_exposure_limits_model_based_diversity_validation]] 不冲突：那条管模型是否见过测试对象，这条管同一暴露状态下规模与分数的关系。与 [[lm_representations_compress_off_germline_variation]] 不构成细化关系，两条各管一个失效环节：那条说嵌入几何压缩了 off-germline 功能差异，这条说似然分数随规模平移。

可证伪内容：在同一家族、同一语料的规模阶梯上，若最大模型相对中等模型的 fitness 预测优势在 95% 置信区间内显著为正，则「超中等规模后下降」在该任务上被推翻。
