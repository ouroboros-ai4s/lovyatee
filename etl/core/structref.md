# structref

## 语义

把一条结构引用变成按链拆开的记录：entity 全长序列、已观察残基、作者编号到 `full_seq` 下标的映射、覆盖信息。

- `ref` 是**现有文件路径**（SRC 自带快照，优先）则直接解析；否则当 **PDB ID** 处理：先查缓存目录下的 `<ID>.cif`，未命中经 `ETL_PROXY` 从 `files.rcsb.org` 下载并原子写入缓存。
- **撤销条目**：RCSB 至今仍对已撤销 ID 返回 200，所以缓存未命中时先查 `data.rcsb.org/rest/v1/holdings/removed/<ID>`。`id_codes_replaced_by` 恰好一个则改取替代条目，令 `replaced_from=<原 ID>`，lineage 写 `step=structure_open | replaced_from=3RVV | structure_id=5VPL`；其余情形抛 `StructureNotFound`。
- 代理只用于 RCSB，不设全局代理。
- `full_seq` 是 entity 的 SEQRES 单字母序列，非标准残基为 `X`；无 SEQRES 时等于 `observed_seq`。
- `index_of` 把**作者编号 `(残基号, 插入码)`** 映射到 `full_seq` 下标。SKEMPI、AB-Bind 的突变用它；R50 的作者重编号快照也按它映射。映射由 `gemmi.align_sequence_to_polymer` 得到，`match_string` 中 `|` 的位置即 entity 下标。
- `observed_segments()` 把已观察残基按 `full_seq` 下标切成连续片段，缺口处断开；`consistent_with(seq)` 要求每个片段都在 `seq` 中出现。**只核对，不补残基**：结构缺口不产生新序列。
- `sha256` 是结构文件的 hash，调用方用它组成缓存键；覆盖信息为 `len(observed_seq)` 对 `len(full_seq)`。

`pick_sequence` 按 `resolve.LEVELS` 前四级择优（`source_native` ← `source`、`source_fasta_or_rebuilt` ← `fasta`、`structure_canonical` ← `full_seq`、`structure_observed` ← `observed_seq`），`on_tie="pick_top"`。结果来自后两级时 lineage 含 `step=structure_recover`。空串候选忽略。

## 接口

```python
class StructureNotFound(Exception): ...

@dataclass(frozen=True)
class ChainRecord:
    chain_id: str
    entity_id: str
    is_protein: bool
    full_seq: str
    observed_seq: str
    index_of: Mapping[tuple[int, str], int]
    def observed_segments(self) -> tuple[str, ...]
    def consistent_with(self, seq: str) -> bool

@dataclass(frozen=True)
class Structure:
    structure_id: str
    requested_id: str
    file: Path
    sha256: str
    chains: Mapping[str, ChainRecord]
    lineage: tuple[str, ...]
    replaced_from: str | None = None

def open_structure(ref: str | Path, cache_dir: Path | None = None) -> Structure
def pick_sequence(rec, source=None, fasta=None) -> tuple[str | None, tuple[str, ...]]
```

`cache_dir` 默认 `$RCSB_CACHE`。

## 示例

```python
from etl.core.structref import open_structure, pick_sequence

s = open_structure("/data_new/ywy/dataset-abag/SRC_R14_ABBIND/snapshot-2019-04-10/AB-Bind-Database/3BDY.pdb")
h = s.chains["H"]
len(h.full_seq), len(h.observed_seq), len(h.index_of)    # (230, 216, 216)
sum(map(len, h.observed_segments()))                     # 216
h.consistent_with(h.full_seq)                            # True

s = open_structure("1N8Z")                               # 先查 $RCSB_CACHE，再经 ETL_PROXY 下载
sorted(len(c.full_seq) for c in s.chains.values())       # [214, 220, 607]  (A 轻链, B 重链, C HER2)
her2 = next(c for c in s.chains.values() if len(c.full_seq) == 607)
len(her2.observed_seq)                                   # 581

s = open_structure("3RVV")
s.structure_id, s.replaced_from, s.lineage[0]
# ('5VPL', '3RVV', 'step=structure_open | replaced_from=3RVV | structure_id=5VPL')

seq, lin = pick_sequence(h)                              # 只有结构证据时
lin[0].startswith("step=structure_recover")              # True

# 粘合到 mutate
from etl.core.mutate import ParentChain
ParentChain(h.full_seq, {"pdb_author": h.index_of})
```

`1BNA` 是 DNA 双链，`is_protein` 全为 `False`；`0ZZZ` 抛 `StructureNotFound`。
