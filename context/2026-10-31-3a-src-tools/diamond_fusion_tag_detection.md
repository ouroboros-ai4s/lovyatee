---
- tags:
  - context
---

# DIAMOND Long Fusion Tag Detection

## time

2026-11-01

## source

- ../son/3a_src_data_etl_problem_ab.md: 方案 3–4，C 端候选边界。

## relation

- [[3a_src_data_etl_problem_ab]]: 为长融合标签与恒定区提供 C 端候选边界。

## workflow

```text
input    = 单条链氨基酸序列尾部窗口
db       = IgG constant domain、GST、MBP、SUMO、Fc 参考序列
run      = blastx 或 blastp，敏感度高于默认
output   = 比对区间、identity、coverage、比对起点
c_star   = 比对起点之前的最后一个抗体残基下标
```

DIAMOND 在保持速度的前提下做蛋白比对，覆盖 ANARCI 编号范围之外的恒定区长片段。比对区间落在序列尾部且 coverage 足够时，区间起点即为 C 端切割位置。

标签短于约 30 aa 时比对信号不足，交给标签模式匹配；DIAMOND 只承担长融合结构与恒定区的边界。
