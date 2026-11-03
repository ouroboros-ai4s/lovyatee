---
tags:
  - context
---

# IMGT Numbering

## time

2026-11-01

## source

- ../son/3a_src_data_etl_problem_ab.md: 方案 3–4，N/C 端候选边界。

## relation

- [[3a_src_data_etl_problem_ab]]: 第三套可变区编号体系，与 ANARCI、IgBLAST 互为校验。

## workflow

```text
input   = 单条链氨基酸序列
scheme  = IMGT unique numbering
output  = 位置 1 到位置 128 的编号、gap 位置
n_star  = 位置 1 的序列下标
c_star  = 位置 128 的序列下标
```

IMGT 唯一编号把可变区固定为位置 1–128，gap 只出现在编号层而不进入序列。用它取边界时，序列下标由非 gap 位置的累计计数换算。

三套编号在对齐正常时边界一致；不一致说明序列含插入、缺失或非抗体片段，按来源边界优先，冲突写入 lineage。
