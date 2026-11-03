---
- tags:
  - context
---

# PDB/mmCIF Structure Cross-Validation

## time

2026-11-01

## source

- ../son/3a_src_data_etl_problem_ab.md: 方案 5，结构作为变量区边界的交叉验证证据。

## relation

- [[3a_src_data_etl_problem_ab]]: 为变量区边界提供结构侧证据，优先于编号边界与 profile 边界。

## workflow

```text
input   = PDB 或 mmCIF 结构、原始记录的结构 ID
parse   = chain、entity、residue numbering、observed residues
select  = 按来源 chain ID、entity 注释、序列比对选出 H/L 链
align   = 结构派生序列 对齐 规范化后的来源序列
map     = 变量区与恒定区的转换点 映射回来源序列下标
output  = chain ID、entity ID、编号体系、残基范围、比对 identity、缺失残基、结构边界
```

结构只承担链选择、序列提取、编号映射和边界核验。坐标不参与改造，缺失残基不补齐，也不对结构做建模。

结构边界在优先序里只低于来源边界，高于编号边界和 profile 边界。与序列侧边界一致时标记为 cross-validated；冲突时取高优先级者，全部候选与冲突状态写入 lineage。

编号体系（auth 或 label）、观察到的残基范围与缺失残基改写边界结果，需随边界一起记录。
