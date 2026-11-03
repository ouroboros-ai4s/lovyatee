---
tags:
  - context
---

# HHsearch Profile Profile Comparison

## time

2026-10-22

## source

- ../../context/2026-10-22-training-data-similarity-and-protein-complex-structure-prediction.md: section 7.2 and section 7.4.

## relation

- [[diversity_is_a_task_conditioned_coverage_claim]]: 具体化该问题定义中的 O/X 相似性层，并为 diversity coverage certificate 提供可复算的工具工作流。

## workflow

```text
input  = two profiles generated from retained alignments
tool   = HH-suite 3 / HHsearch
score  = s_HH = Score / max(L_Q, L_R)
```

HHsearch has its own profile format and score space. Its score is not interchangeable with an HMMER or PyHMMER score.
