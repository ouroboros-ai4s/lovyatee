---
tags:
  - context
---

# MMseqs2 Sequence Search

## time

2026-10-22

## source

- ../../context/2026-10-22-training-data-similarity-and-protein-complex-structure-prediction.md: section 7.2 and section 7.3.

## relation

- [[diversity_is_a_task_conditioned_coverage_claim]]: 具体化该问题定义中的 O/X 相似性层，并为 diversity coverage certificate 提供可复算的工具工作流。

## workflow

```text
input  = query and reference protein sequences
output = identity I, bidirectional coverage cq/cr, traceback
score  = s_seq(q,r) = I * sqrt(cq * cr)
```

MMseqs2 supplies sequence candidates and alignment evidence. The project score must be recomputed from the saved traceback; the tool name is not the similarity definition.
