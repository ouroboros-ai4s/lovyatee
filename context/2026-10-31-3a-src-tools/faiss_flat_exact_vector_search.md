---
- tags:
  - context
---

# Faiss Flat Exact Vector Search

## time

2026-10-22

## source

- ../../context/2026-10-22-training-data-similarity-and-protein-complex-structure-prediction.md: section 7.2 and section 7.7.

## relation

- [[diversity_is_a_task_conditioned_coverage_claim]]: 具体化该问题定义中的 O/X 相似性层，并为 diversity coverage certificate 提供可复算的工具工作流。

## workflow

```text
object = fixed-length representation vector
index  = Flat, exhaustive distance computation
score  = cosine distance after fixed standardization and normalization
```

Faiss Flat is the exact baseline for validating approximate vector retrieval. It does not define the representation or its standardization.
