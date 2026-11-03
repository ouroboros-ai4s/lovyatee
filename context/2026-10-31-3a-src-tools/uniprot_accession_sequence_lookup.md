---
- tags:
  - context
---

# UniProt Accession Sequence Lookup

## time

2026-11-01

## source

- ../son/3a_src_data_etl_problem_ag.md: 方案 1–2 与 6，UniProt accession 作为抗原序列来源，证据等级为第 5 级。

## relation

- [[3a_src_data_etl_problem_ag]]: 为抗原序列恢复提供显式 accession 对应的数据库序列，位于来源 FASTA、PDB/mmCIF 之后。

## workflow

```text
input   = 来源显式给出的 UniProt accession，或与 PDB 链明确关联的 accession
lookup  = 按 accession 读取条目序列
compare = 与更高优先级证据逐链比对
output  = accession、条目序列、数据库版本、比对结果、证据等级
```

UniProt 只在来源明确给出 accession，或来源指定的 PDB 链与该 accession 关联时使用。按抗原名称、语义相似度或普通搜索命中得到的条目不作为证据。

条目序列通常是数据库全长或成熟链，不等于实验使用的构建体。实验边界由第 3 项决定，本工具不做裁剪。与来源 FASTA、PDB SEQRES 或结构观察序列冲突时，取更高优先级的证据，并把冲突写入 lineage。
