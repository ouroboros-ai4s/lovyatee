---
- tags:
  - context
---

# IgBLAST Antibody Alignment

## time

2026-11-01

## source

- ../son/3a_src_data_etl_problem_ab.md: 方案 3–4，N/C 端候选边界。

## relation

- [[3a_src_data_etl_problem_ab]]: 与 ANARCI 并列的可变区边界来源，用于多工具一致判定。

## workflow

```text
input   = 单条链氨基酸序列
db      = germline V、D、J 数据库
output  = V(D)J 比对区间、CDR/FWR 注释、FR1 起点与 FR4 终点
n_star  = FR1 第一个残基的序列下标
c_star  = FR4 最后一个残基的序列下标
```

IgBLAST 通过胚系比对给出 FR1–FR4 的边界，N 端取 FR1 起点、C 端取 FR4 终点。它同时报告链类型与胚系 V 基因，后者可作为来源未标注 VHH 时的旁证。

胚系库版本与 organism 参数改写边界结果，需写进 lineage。
