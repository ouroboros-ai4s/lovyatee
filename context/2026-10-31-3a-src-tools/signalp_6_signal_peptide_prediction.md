---
tags:
  - context
---

# SignalP 6 Signal Peptide Prediction

## time

2026-11-01

## source

- ../son/3a_src_data_etl_problem_ab.md: 方案 3–4，N 端候选边界与 fallback。

## relation

- [[3a_src_data_etl_problem_ab]]: 为 N 端裁剪提供无来源边界时的默认候选边界。

## workflow

```text
input    = 原始氨基酸序列
output   = 信号肽类别概率、切割位点位置
class    = Sec/SPI, Sec/SPII, Tat/SPI, Tat/SPII, 无信号肽
n_star   = 切割位点对应的序列下标
fallback = 无来源边界时取 n_star
```

SignalP 6 用蛋白语言模型输出五类信号肽的概率与切割位点，切割位点直接给出 `n*`。类别判为无信号肽时不产生 N 端证据，序列原样进入后续裁剪。

抗体记录多数不含信号肽。该工具主要覆盖 R08 这类带 22 aa 前缀的来源，其余记录的 N 端边界由 ANARCI 或 IgBLAST 的可变区起点给出。
