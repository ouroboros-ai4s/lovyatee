---
- tags:
  - context
---

# Phobius Signal Peptide Prediction

## time

2026-11-01

## source

- ../son/3a_src_data_etl_problem_ab.md: 方案 3–4，N 端候选边界。

## relation

- [[3a_src_data_etl_problem_ab]]: 与 SignalP 并行产生 N 端候选边界，参与多工具一致判定。

## workflow

```text
input  = 原始氨基酸序列
output = 信号肽区间、跨膜螺旋区间、拓扑模型
check  = N 端疏水段是信号肽还是跨膜螺旋
n_star = 信号肽区间终点对应的序列下标
```

Phobius 用联合隐马尔可夫模型同时预测信号肽与跨膜拓扑。它的作用是区分 N 端疏水段属于可切除的信号肽还是跨膜螺旋，防止把 VH 的真实 N 端残基当作信号肽切掉。

SignalP 与 Phobius 都给信号肽时取一致切割位点。只有 Phobius 给出时按多工具一致级别处理，优先级低于来源边界。
