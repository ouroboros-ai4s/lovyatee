---
- tags:
  - context
---

# Foldseek Interface Search

## time

2026-10-22

## source

- ../../context/2026-10-22-training-data-similarity-and-protein-complex-structure-prediction.md: section 7.2 and section 7.6.

## relation

- [[diversity_is_a_task_conditioned_coverage_claim]]: 具体化该问题定义中的 O/X 相似性层，并为 diversity coverage certificate 提供可复算的工具工作流。

## workflow

```text
object    = local cross-chain interface
extraction = Cα distance <= 10 Å, at least 4 valid residues per side
score     = interface score normalized by both interface lengths
```

The extraction boundary, code revision, chain mapping, coverage, and parent complex identifier are part of the measurement protocol.
