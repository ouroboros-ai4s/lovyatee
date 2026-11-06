# antigen_bound

## 语义

抗原侧最粗的一层：把 adapter 给出的每条候选链（序列候选、来源边界、结构观察片段）折成**一条有序、裁剪后的链序列列表**，供 `ids.ag_id` 使用。它不判断某条链是否属于实验抗原——那由 adapter 与决策文件决定，本模块只回答"给定这些链，它们的绑定形态是什么"。

规则（ag 方案第 3、4、6 项的代码化）：

1. **链集合**：空 → `no_sequence`。任一链 `is_protein=False` → `non_protein`（DNA/RNA、配体、离子整体排除）。
2. **每链取序列**：对 `candidates` 跑 `resolve(order=LEVELS, on_tie="reject")`。同级不同序列 → `sequence_conflict`；无候选 → `no_sequence`。上级与下级取值不同时，上级优先采纳，但 lineage 追加 `step=resolve | chain=<key> | ... | conflict=1`（证据保留）。
3. **每链取边界**：`boundaries` 同样按 `LEVELS` 做 `resolve(on_tie="reject")`。同级不同 `(start, end)` → `boundary_ambiguous`；`0 <= start < end <= len(序列)` 不成立 → `boundary_out_of_range`。按选中边界裁剪，写 `step=trim | chain=<key> | span=<s>-<e> | label=<label> | removed_n=<n> | removed_c=<n>`。无边界则整条保留。
4. **结构核对**：`observed_segments` 给出时，每个片段都出现在选中序列中为 `structure=consistent`，否则 `structure=mismatch`，写 `step=structure_check | chain=<key> | structure=...`。**不一致只记录，不排除**，序列以来源为准。
5. **链序**：所有链都有 `order` 时按 `order` 排；`order` 重复或部分有部分无 → `order_ambiguous`；都没有时按 `(entity, key)` 字典序。**相同序列的链不去重**：同源多聚体保留为列表中的多个元素，顺序参与 `AG_ID`。
6. 成功时 `chains` 为按链序排列的裁剪后序列，`keys` 为对应链 key。

排除码是**默认处置**，不是判决。某个码命中一个 SRC 的大部分记录时，说明该条件与该 SRC 不符，由执行者在 adapter 侧调整并记入 lineage。

## 接口

```python
@dataclass(frozen=True)
class SeqCandidate: level: str; seq: str                 # level ∈ resolve.LEVELS

@dataclass(frozen=True)
class Boundary: level: str; start: int; end: int; label: str   # 0 起右开，坐标在选中的序列上

@dataclass(frozen=True)
class Chain:
    key: str
    is_protein: bool = True
    order: int | None = None
    entity: str | None = None
    candidates: tuple[SeqCandidate, ...] = ()
    boundaries: tuple[Boundary, ...] = ()
    observed_segments: tuple[str, ...] | None = None       # 来自 ChainRecord.observed_segments()

@dataclass(frozen=True)
class Bound:
    chains: tuple[str, ...] | None
    keys: tuple[str, ...]
    reason: str | None
    lineage: tuple[str, ...]

def bound(chains: Sequence[Chain]) -> Bound
```

`reason`：`None`、`no_sequence`、`non_protein`、`sequence_conflict`、`boundary_ambiguous`、`boundary_out_of_range`、`order_ambiguous`。

## 示例

```python
from etl.core.antigen_bound import Boundary, Chain, SeqCandidate, bound

c = Chain("A", candidates=(SeqCandidate("source_native", "MKYLLPTAAAGLLLLAAQPAMA" + "DKTHTCPPCP"),),
          boundaries=(Boundary("source_native", 22, 32, "mature_chain"),))
b = bound([c])
b.chains    # ('DKTHTCPPCP',)
b.lineage[0]  # 'step=trim | chain=A | span=22-32 | label=mature_chain | removed_n=22 | removed_c=0'

bound([Chain("B", candidates=(SeqCandidate("source_native", "MKTAYIAKQR"),), entity="1"),
       Chain("A", candidates=(SeqCandidate("source_native", "MKTAYIAKQR"),), entity="1")])
# Bound(chains=('MKTAYIAKQR', 'MKTAYIAKQR'), keys=('A', 'B'), ...)   同源二聚体不去重

c = Chain("A", candidates=(SeqCandidate("source_native", "AAAA"),
                           SeqCandidate("structure_canonical", "AAAB")),
          observed_segments=("BB",))
b = bound([c])
b.chains          # ('AAAA',)      来源优先
"structure=mismatch" in " ".join(b.lineage)     # True   只记录
"conflict=1" in " ".join(b.lineage)             # True

bound([Chain("D", is_protein=False)]).reason        # 'non_protein'
bound([]).reason                                    # 'no_sequence'
```

典型 adapter 粘合：

```python
from etl.core.structref import open_structure

rec = open_structure("1N8Z").chains["C"]
Chain(rec.chain_id, entity=rec.entity_id,
      candidates=(SeqCandidate("structure_canonical", rec.full_seq),),
      observed_segments=rec.observed_segments())
```
