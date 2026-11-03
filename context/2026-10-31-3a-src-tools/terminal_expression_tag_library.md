---
tags:
  - context
---

# Terminal Expression Tag Library

## time

2026-11-01

## source

- ../son/3a_src_data_etl_problem_ab.md: 方案 3–4，C 端候选边界与标签库。

## relation

- [[3a_src_data_etl_problem_ab]]: 为 C 端裁剪提供模式匹配的标签集合。

## workflow

```text
短标签  = FLAG, HA, Myc, V5, Strep-tag II, Twin-Strep, AviTag
长融合  = GST, MBP, SUMO, Fc
match   = 序列末端精确或近精确匹配，允许编码残基导致的 1–2 aa 偏差
c_star  = 匹配区间之前的最后一个抗体残基下标
```

短标签按序列模式匹配，长度 8–30 aa，位于序列末端，切割边界明确。长融合与恒定区超出模式匹配的可靠范围，由 DIAMOND 或 InterProScan 给出区间。

末端连续组氨酸单独处理：天然 CDR-H3 与 FR4 尾部可出现 1–3 个组氨酸，只在连续 ≥5 个 H 且与来源声明一致时判定为 His-tag。

匹配所用的标签序列、允许偏差、命中的位置与来源证据写入 lineage。
