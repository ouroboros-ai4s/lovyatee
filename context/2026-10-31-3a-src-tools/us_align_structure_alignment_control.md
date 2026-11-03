---
tags:
  - context
---

# US-align Structure Alignment Control

## time

2026-10-22

## source

- ../../context/2026-10-22-training-data-similarity-and-protein-complex-structure-prediction.md: section 7.2, section 7.6, and section 10.1.

## relation

- [[diversity_is_a_task_conditioned_coverage_claim]]: 具体化该问题定义中的 O/X 相似性层，并为 diversity coverage certificate 提供可复算的工具工作流。

## workflow

```text
object = paired protein complex or assembly
input  = two structures with chain correspondence
score  = lower of target- and reference-normalized TM-scores
purpose = small-scale structural audit and controlled selection matrix
```

US-align is a comparison implementation and audit control. Its heuristic alignment is not an exact global-optimum certificate.
