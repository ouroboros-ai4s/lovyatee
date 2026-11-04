---
tags:
  - design
---

# Processed Ab Ag Pair Dataset Model

本设计文件针对的是 [[2026-11-01-20-src-data-etl-todo-list]] 中的 `## 1. Data ETL Specification`.

## time

2026-10-31

## lineage

- ../../docs/2026-11-01-20-src-data-etl-todo-list.md: 20-source ETL TODO and processing order.
- ../3a-src-inventory/src-03-abdesign-1-0.md: source inventory evidence.
- ../3a-src-inventory/src-08-avida-htnfa.md: source inventory evidence.
- ../3a-src-inventory/src-09-flab.md: source inventory evidence.
- ../3a-src-inventory/src-10-abrank.md: source inventory evidence.
- ../3a-src-inventory/src-11-abbibench.md: source inventory evidence.
- ../3a-src-inventory/src-12-asd-agab-db.md: source inventory evidence.
- ../3a-src-inventory/src-13-andd.md: source inventory evidence.
- ../3a-src-inventory/src-14-ab-bind.md: source inventory evidence.
- ../3a-src-inventory/src-15-skempi-2-0.md: source inventory evidence.
- ../3a-src-inventory/src-16-guest.md: source inventory evidence.
- ../3a-src-inventory/src-20-sabdab-sabdab2.md: source inventory evidence.
- ../3a-src-inventory/src-23-mit-ll-alphaseq.md: source inventory evidence.
- ../3a-src-inventory/src-50-graphinity.md: source inventory evidence.
- ../3a-src-inventory/src-74-abdesign-2-0.md: source inventory evidence.
- ../3a-src-inventory/src-75-her2-aff-large-buzz.md: source inventory evidence.
- ../3a-src-inventory/src-76-tdc-antibodyaff.md: source inventory evidence.
- ../3a-src-inventory/src-77-akbar-sabdab-kd-csv.md: source inventory evidence.
- ../3a-src-inventory/src-78-mochibind-sampled-data.md: source inventory evidence.
- ../3a-src-inventory/src-79-alphabind.md: source inventory evidence.
- ../3a-src-inventory/src-80-antipasti.md: source inventory evidence.

## relation

None.

## description

`abag-data-etl` 的 MVP 产物是按全局清洗结果去重后的 Ab–Ag pair 数据集。每个唯一 pair 对应一条 `3A`：

```python
3A = (3A_ID, antibody, antigen, affinity[])
```

其中 `3A_ID`、`AB_ID` 和 `AG_ID` 都在清洗后生成。结构和 lineage 不参与去重。

`antibody` 的全局去重键是清洗后的 H/L 二元组；`antigen` 的全局去重键是清洗后的有序抗原链序列列表；`3A` 的全局去重键是 `(AB_ID, AG_ID)`。因此，同一 pair 的多个 affinity observations 只挂在同一个 `3A_ID` 下。

```python
AB_ID  = hash(vh_sequence, vl_sequence)
AG_ID  = hash(canonical_sequence_list)
3A_ID  = hash(AB_ID, AG_ID)
```

hash 输入使用清洗后的规范化字符串、固定字段顺序和明确的空值表示。`structure`、`lineage`、affinity 内容和来源不进入上述 hash。`AG_ID` 的输入是固定链顺序下的 `canonical_sequence_list`；同一列表序列化后再计算 hash。链顺序优先采用来源明确顺序，其次是结构 entity/chain 顺序，最后才使用稳定的 chain ID 排序；无法唯一确定顺序时排除。

数据结构为：

```python
antibody = {
  AB_ID,
  vh_sequence,     # VL-only 时为 null
  vl_sequence,     # VHH/heavy-only 时为 null
  structure,       # 当前没有结构时为 null
  lineage[]
}

antigen = {
  AG_ID,
  sequence: list[FASTA],  # 单链为单元素列表，多链按固定顺序保存
  structure,       # 整体抗原/复合物结构；当前没有结构时为 null
  lineage[]
}

affinity = [
  (label, assay, condition, replicate, lineage[]),
  ...
]
```

不再保存 `format` 字段。`vl_sequence = null` 表示没有轻链，通常对应 VHH；有 VH 和 VL 时按 Fv 粒度保存。抗体 `structure` 保存整体 Fv/VHH 结构对象，并在对象内部保留链 ID 和残基映射；它可以是共享参考结构，也可以为 `null`。

抗原的 `sequence` 和 `structure` 统一到 affinity 实验实际使用的片段。有效 `3A` 必须至少有一个清洗后的 `vh_sequence` 或 `vl_sequence`，实验对应的抗原 `sequence: list[FASTA]` 和至少一条 affinity observation；两者不能同时为 `null`。`vh_sequence` 或 `vl_sequence` 可以为 `null`。无法可靠对应到实验片段、无法得到任何有效抗体 variable-region sequence 或没有有效 affinity label 的记录进入 reject/audit，不进入有效 3A dataset。`antigen.sequence` 始终是有序 `list[FASTA]`：单链和短肽是单元素列表，多链抗原按固定顺序保存多个链；`antigen.structure` 保存对应的整体结构或复合物结构。

`affinity` 保留 inventory 探测到的原始 `(label, assay, condition, replicate)`，并增加该 observation 的 `lineage`。本轮不强行统一 label 类型、单位、截断符号或 assay 数值表达；同一 pair 涉及多条观测时逐条追加到 `affinity[]`。

`lineage[]` 是 MVP 的来源定位列表，使用字符串记录 `SRC_ID`、文件或表名、原始行号、原始记录 ID 或必要的 description。例如：

```text
SRC_R76 | protein_sabdab.csv | row=123 | ID1=1ABC
```

同一个 AB 或 AG 被多个来源复用时，在对应实体的 `lineage[]` 中追加定位；同一个 pair 的不同测量在各自 affinity observation 中保留各自的 `lineage[]`。

20 个 inventory 文档：

- [R03 AbDesign 1.0](../2026-10-30-3a-src-inventory/src-03-abdesign-1-0-inventory.md)
- [R08 AVIDa-hTNFa](../2026-10-30-3a-src-inventory/src-08-avida-htnfa-inventory.md)
- [R09 FLAb](../2026-10-30-3a-src-inventory/src-09-flab-inventory.md)
- [R10 AbRank](../2026-10-30-3a-src-inventory/src-10-abrank-inventory.md)
- [R11 AbBiBench](../2026-10-30-3a-src-inventory/src-11-abbibench-inventory.md)
- [R12 ASD / AgAb DB](../2026-10-30-3a-src-inventory/src-12-asd-agab-db-inventory.md)
- [R13 ANDD](../2026-10-30-3a-src-inventory/src-13-andd-inventory.md)
- [R14 AB-Bind](../2026-10-30-3a-src-inventory/src-14-ab-bind-inventory.md)
- [R15 SKEMPI 2.0](../2026-10-30-3a-src-inventory/src-15-skempi-2-0-inventory.md)
- [R16 Guest antibody benchmark](../2026-10-30-3a-src-inventory/src-16-guest-inventory.md)
- [R20 SAbDab / SAbDab2](../2026-10-30-3a-src-inventory/src-20-sabdab-sabdab2-inventory.md)
- [R23 MIT-LL AlphaSeq](../2026-10-30-3a-src-inventory/src-23-mit-ll-alphaseq-inventory.md)
- [R50 Graphinity](../2026-10-30-3a-src-inventory/src-50-graphinity-inventory.md)
- [R74 AbDesign 2.0](../2026-10-30-3a-src-inventory/src-74-abdesign-2-0-inventory.md)
- [R75 HER2-aff-large / Buzz](../2026-10-30-3a-src-inventory/src-75-her2-aff-large-buzz-inventory.md)
- [R76 TDC AntibodyAff](../2026-10-30-3a-src-inventory/src-76-tdc-antibodyaff-inventory.md)
- [R77 Akbar SAbDab Kd CSV](../2026-10-30-3a-src-inventory/src-77-akbar-sabdab-kd-csv-inventory.md)
- [R78 MochiBind sampled data](../2026-10-30-3a-src-inventory/src-78-mochibind-sampled-data-inventory.md)
- [R79 AlphaBind public experiments](../2026-10-30-3a-src-inventory/src-79-alphabind-inventory.md)
- [R80 ANTIPASTI](../2026-10-30-3a-src-inventory/src-80-antipasti-inventory.md)

ETL 只负责序列、结构、pair 和 affinity 的清洗、对齐、去重与保存，不执行 CDR-focused、surface-focused 或 diversity 分析。
