---
- tags:
  - context
---

# zsasa Surface Area Measurement

## time

2026-10-22

## source

- ../../context/2026-10-22-training-data-similarity-and-protein-complex-structure-prediction.md: section 7.2 and section 7.8.

## relation

- [[diversity_is_a_task_conditioned_coverage_claim]]: 具体化该问题定义中的 O/X 相似性层，并为 diversity coverage certificate 提供可复算的工具工作流。

## workflow

```text
object = residue or surface patch
measure = SASA_single - SASA_complex
burial  = max(0, measure)
descriptor = buried-area-weighted amino-acid composition
```

The protocol fixes atom selection, ProtOr radii, a 1.4 Å probe, double precision, sampling density, and non-standard residue handling.
