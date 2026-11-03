---
tags:
  - context
---

# BLASTp Profile Boundary

## time

2026-11-01

## source

- ../son/3a_src_data_etl_problem_ab.md: 方案 5，恒定区与融合结构域的序列边界。

## relation

- [[3a_src_data_etl_problem_ab]]: 为恒定区裁剪提供 profile 边界证据，位于来源、结构与编号边界之后。

## workflow

```text
input    = 待判定单条链氨基酸序列
db       = 恒定区、融合标签参考序列
run      = blastp
output   = 比对区间、identity、coverage、E-value、比对起点与终点
boundary = 比对区间的起点或终点换算为序列下标
```

BLASTp 在方案 5 的边界优先序里属于 profile 边界一级，排在来源边界、结构边界、ANARCI/IgBLAST/IMGT 编号边界之后。

它与 DIAMOND 覆盖同一类长片段。两者差异在速度与敏感度：DIAMOND 更快，BLASTp 在短恒定区段上的比对更保守。比对区间落在序列尾部且 coverage 足够时，区间起点即恒定区切割位置。

参考库版本、E-value 阈值与 coverage 下限写入 lineage。
