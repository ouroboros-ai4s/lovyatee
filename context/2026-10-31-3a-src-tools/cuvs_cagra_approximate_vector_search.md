---
- tags:
  - context
---

# cuVS CAGRA Approximate Vector Search

## time

2026-10-22

## source

- ../../context/2026-10-22-training-data-similarity-and-protein-complex-structure-prediction.md: section 7.2 and section 7.7.

## relation

- [[diversity_is_a_task_conditioned_coverage_claim]]: 具体化该问题定义中的 O/X 相似性层，并为 diversity coverage certificate 提供可复算的工具工作流。

## workflow

```text
index = graph-based approximate nearest-neighbor search
audit = compare recall and ranking against Faiss Flat
fallback = exact or expanded candidate search if recall fails
```

CAGRA is an acceleration workflow. Its speed does not replace an exact-recall audit or the fixed similarity protocol.
