---
tags:
  - context
---

# FreeSASA Surface Area Control

## time

2026-10-22

## source

- ../../context/2026-10-22-training-data-similarity-and-protein-complex-structure-prediction.md: section 7.2 and section 7.8.

## relation

- [[diversity_is_a_task_conditioned_coverage_claim]]: 具体化该问题定义中的 O/X 相似性层，并为 diversity coverage certificate 提供可复算的工具工作流。

## workflow

```text
purpose = independent SASA implementation control or fallback
compare = per-residue burial, interface area, and final surface descriptor
constraint = match atom, radius, probe, and sampling settings
```

FreeSASA checks the numerical stability of zsasa-derived surface measurements; implementation agreement does not establish biological validity.
