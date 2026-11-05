# resolve

## 语义

多个来源给出同一个量（序列、边界、结构指针）时，按给定的优先级顺序择优，并把全部候选与冲突标记留给 lineage。

- 取 `order` 中最高且非空的一级。
- 该级只有一种 `value`：选中它（按该级输入顺序取第一个）。
- 该级有多种 `value`：同级 tie。`on_tie="reject"` 返回 `selected=None`；`on_tie="pick_top"` 用 `tie_break` 选，没有 `tie_break` 取该级输入顺序第一个。
- `conflict` 为全部候选中 `value` 的种类多于一种，与是否 tie 无关：低级别与选中值不同也算冲突（上层值优先采纳，冲突保留证据）。
- 空候选返回 `Resolved(None, (), False)`。`source` 不在 `order` 中抛 `ValueError`（调用方契约错误）。

`LEVELS` 是抗原与结构序列证据的统一词表（ag 方案第 6 项的优先级）：

```
source_native > source_fasta_or_rebuilt > structure_canonical > structure_observed > external_accession
```

## 接口

```python
LEVELS = ("source_native", "source_fasta_or_rebuilt", "structure_canonical", "structure_observed", "external_accession")

@dataclass(frozen=True)
class Candidate: source: str; value: object

@dataclass(frozen=True)
class Resolved:
    selected: Candidate | None
    candidates: tuple[Candidate, ...]          # 按 order 的优先级，同级保持输入顺序
    conflict: bool
    def lineage_frags(self) -> list[str]       # ["resolved=<source>|none", "candidates=<src>:<val>;...", "conflict=1"（仅冲突时）]

def resolve(candidates, order, on_tie, tie_break=None) -> Resolved
```

## 各调用点的配置

| 调用点 | order | on_tie | 说明 |
| --- | --- | --- | --- |
| ab 方案第 3–5 项（VH/VL 序列择优） | `LEVELS` | `pick_top` | 取最高优先级，冲突写入 lineage |
| ab 方案第 6 项（scFv 域边界） | `LEVELS` | `pick_top` + `tie_break` | tie 时取两侧域都有效且未解释片段最短者 |
| ag 方案第 6 项（抗原序列） | `LEVELS` | `reject` | 同级冲突整条排除为 `sequence_conflict` |
| `structref.pick_sequence` | `LEVELS[:4]` | `pick_top` | 空串候选先由调用方忽略 |

首版只有 ANARCI 一个可变域工具，ab 方案第 3–4 项的"多工具一致"一层不可达，`LEVELS` 中不设工具轴；引入第二个工具时新增一级而不是改变已有级别的含义。

## 示例

```python
from etl.core.resolve import Candidate, resolve

ORDER = ["source", "structure"]
r = resolve([Candidate("structure", "AAA"), Candidate("source", "AAB")], ORDER, "reject")
r.selected          # Candidate(source='AAB', value='AAB')
r.conflict          # True
r.lineage_frags()   # ['resolved=source', 'candidates=source:AAB;structure:AAA', 'conflict=1']

resolve([Candidate("source", "AAA"), Candidate("structure", "AAA")], ORDER, "reject").conflict   # False

cs = [Candidate("source", "AAAA"), Candidate("source", "AA")]
resolve(cs, ORDER, "reject").selected                                     # None
resolve(cs, ORDER, "pick_top").selected.value                             # 'AAAA'
resolve(cs, ORDER, "pick_top", tie_break=lambda c: min(c, key=lambda x: len(x.value))).selected.value  # 'AA'

resolve([], ORDER, "reject")       # Resolved(selected=None, candidates=(), conflict=False)
```
