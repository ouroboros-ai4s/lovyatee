---
- tags:
  - context
---

# ANARCI Antibody Numbering

## time

2026-11-01

## source

- ../son/3a_src_data_etl_problem_ab.md: 方案 3–4，N 端与 C 端候选边界。

## relation

- [[3a_src_data_etl_problem_ab]]: 同时给出可变区的起点和终点，作为 N/C 两端的主候选边界来源。

## workflow

```text
input     = 单条链氨基酸序列
scheme    = Kabat, Chothia, IMGT, AHo, Martin
output    = 编号后的残基、链类型、位置 1 与位置 128 的边界
n_star    = 编号位置 1 对应序列下标
c_star    = 编号位置 128 对应序列下标
```

ANARCI 判链类型（VH、VK、VL、VHH 等）并输出逐残基编号。位置 1 和最后一个可变区编号位置之间的序列区间就是成熟可变区；位置 1 之前是信号肽、标签或前导序列，之后是恒定区或融合标签。

链类型判定同时是 VHH 与 heavy-only 区分的工具侧证据，须与来源标签一并记录。编号用到的 HMM 集合与 scheme 版本写进 lineage。
