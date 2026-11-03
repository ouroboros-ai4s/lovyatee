---
- tags:
  - context
---

# PyHMMER Profile Query

## time

2026-10-22

## source

- ../../context/2026-10-22-training-data-similarity-and-protein-complex-structure-prediction.md: section 7.2 and section 7.4.

## relation

- [[diversity_is_a_task_conditioned_coverage_claim]]: 具体化该问题定义中的 O/X 相似性层，并为 diversity coverage certificate 提供可复算的工具工作流。

## workflow

```text
query  = target sequence
reference = preloaded profile-HMM collection
raw    = Domain.score and local match coordinates
score  = s_evo(q,r) = Domain.score / max(L_q, L_profile)
```

Reported and included states, profile length, coverage, database size, and filter settings remain attached to the score.
