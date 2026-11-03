---
- tags:
  - context
---

# InterProScan Pfam Domain Annotation

## time

2026-10-22

## source

- ../../context/2026-10-22-training-data-similarity-and-protein-complex-structure-prediction.md: section 7.2 and section 7.5.

## relation

- [[diversity_is_a_task_conditioned_coverage_claim]]: 具体化该问题定义中的 O/X 相似性层，并为 diversity coverage certificate 提供可复算的工具工作流。

## workflow

```text
object = domain occurrence and ordered domain architecture
tool   = InterProScan 6, Pfam only
output = accession, type, coordinates, representative flag, fragments
```

The resulting domain label sequence supports separate composition and order measures. Repeated domains remain repeated; discontinuous fragments do not become extra occurrences.
