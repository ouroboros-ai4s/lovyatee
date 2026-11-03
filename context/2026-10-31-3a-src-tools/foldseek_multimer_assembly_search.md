---
- tags:
  - context
---

# Foldseek Multimer Assembly Search

## time

2026-10-22

## source

- ../../context/2026-10-22-training-data-similarity-and-protein-complex-structure-prediction.md: section 7.2 and section 7.6.

## relation

- [[diversity_is_a_task_conditioned_coverage_claim]]: 具体化该问题定义中的 O/X 相似性层，并为 diversity coverage certificate 提供可复算的工具工作流。

## workflow

```text
object = two-chain assembly in one common spatial frame
score  = s_assembly = min(TM_target, TM_reference)
fields = chain mapping, both coverages, complexqtmscore, complexttmscore
```

This workflow preserves relative chain geometry. Separate single-chain scores cannot be substituted for it.
