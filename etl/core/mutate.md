# mutate

## 语义

两种编辑模式，都不改变链数、不做任何序列清洗之外的推断：

**`apply_point`（A/B/C 规则，ab 方案第 9 项）** — 结构型 SRC 只有亲本结构、逐行给突变。A 类（来源已给完整序列）**不经本函数**；本函数只处理 B 类（在 parent 序列上按编号落点）与 C 类（拒绝并给原因）。

- 每个 `edit` 的候选链为 `edit.chain`，为空则取全部 parent 链。
- 候选必须同时满足：编号方案存在、`(pos, ins)` 可映射、该位残基等于 `orig`。
- 全体候选**恰好一个**才接受。
- `new` 必须是单个 `A-Z` 字母。
- 长度不变，调用方可按位置继承可变域边界，不必重跑 ANARCI。
- 空 `edits` 返回 B 类、链原样。

`reason` 取值：`no_numbering`、`unmapped_position`、`orig_mismatch`、`ambiguous_chain`、`conflicting_edits`（同链同位两个不同 `new`）、`unsupported_edit`。

**`apply_region`（R75）** — 只有 CDR、需要从参考结构补全一条链。对指定链跑 `vdomain.parse`，取该域中 IMGT `(start,"")` 到 `(end,"")` 之间（按序列顺序，含插入码）的下标区间整体替换为 `replacement`；不校验被替换区间的原残基。替换后重新 `parse`，要求仍是同样数量的域、同一链型、且区间外残基逐位相同。返回 parent 的 VH 与 VL，被替换的一条换成新序列，另一条原样。区间 `(107, 116)` 为闭区间。

实测确认（2026-11-05，`1N8Z` 重链，IMGT）：107–116 共 10 个编号位全部存在，残基为 `WGGDGFYAMD`，落在 CDR-H3（IMGT 105–117）之内。blueprint 要求的区间可用，测试沿用 `(107, 116)`。

`reason`：`no_domain`、`region_boundary_missing`（start 或 end 缺位）、`bad_replacement`（`seqnorm` 不返回非空序列）、`region_mismatch`（替换后不再是同一链型的单域）。

## 接口

```python
SEQ_NUMBERING = "seq_1based"          # ParentChain 内置方案：1 起，无插入码

class Edit(NamedTuple):
    id: str; chain: str; orig: str; pos: int; new: str; numbering: str; ins: str = ""

@dataclass(frozen=True)
class ParentChain:
    seq: str
    numberings: Mapping[str, Mapping[tuple[int, str], int]] = field(default_factory=dict)

@dataclass(frozen=True)
class PointResult:
    cls: Literal["B", "C"]; chains: dict[str, str] | None; reason: str | None
    lineage: tuple[str, ...]; sites: tuple[tuple[str, str, int], ...]   # (edit.id, 链, 0 起下标)

@dataclass(frozen=True)
class RegionResult:
    vh: str | None; vl: str | None; reason: str | None; lineage: tuple[str, ...]

def apply_point(entity: Literal["ab","ag"], parent: Mapping[str, ParentChain],
                edits: Sequence[Edit]) -> PointResult
def apply_region(parent_h: str, parent_l: str | None, span: tuple[int, int], replacement: str,
                 chain: Literal["H","L"] = "H") -> RegionResult
```

`ParentChain` 的粘合方式：

```python
from etl.core.structref import open_structure
from etl.core.vdomain import parse

rec = open_structure("3BDY.pdb").chains["H"]
ParentChain(rec.full_seq, {"pdb_author": rec.index_of})           # 结构编号（SKEMPI / AB-Bind）

dom = parse(H).domains[0]
ParentChain(H, {"imgt": dom.residue_index})                       # IMGT 编号（region 模式）
```

`chain=""` 的搜索规则：在所有 parent 链上逐个试，命中多于一条即 `ambiguous_chain`；同源多聚体要由 adapter 展开成每链一个 `Edit`。

## 示例

```python
from etl.core.mutate import Edit, ParentChain, apply_point, apply_region

r = apply_point("ab", {"H": ParentChain("ACDE", {"pdb_author": {(52, ""): 1, (52, "A"): 2}})},
                [Edit("m", "H", "D", 52, "G", "pdb_author", "A")])
r.chains          # {'H': 'ACGE'}   插入码精确映射到 (52, A)
r.sites           # (('m', 'H', 2),)
r.lineage[0]      # 'step=mutation_rebuild | entity=ab | class=B | numbering=pdb_author | edits=H:D52A>G'

apply_point("ag", {"A": ParentChain("MKTAY")}, [Edit("m", "A", "T", 3, "S", "seq_1based")]).chains
# {'A': 'MKSAY'}

n = {"pdb_author": {(1, ""): 0}}
p = {"A": ParentChain("CD", n), "B": ParentChain("CD", n)}
apply_point("ag", p, [Edit("m", "", "C", 1, "G", "pdb_author")]).reason   # 'ambiguous_chain'
apply_point("ag", p, [Edit("m", "B", "C", 1, "G", "pdb_author")]).chains  # {'A': 'CD', 'B': 'GD'}

apply_region(H_1N8Z, L_1N8Z, (107, 116), "ARDYYGSSYF")
# RegionResult(vh=<含 ARDYYGSSYF 的重链 VH>, vl=<原 VL>, reason=None, lineage=(...))
apply_region(H_1N8Z, L_1N8Z, (107, 116), "ar1").reason     # 'bad_replacement'
apply_region("GGGG", L_1N8Z, (107, 116), "ARDYYGSSYF").reason   # 'no_domain'
```

## 与上游的衔接

- 突变位点落在 `vdomain` 裁掉的区段（信号肽、标签、恒定区）时，清洗后的序列与 parent 相同，按 hash 规则落入同一 `AB_ID`；位点仍写入 `sites`/lineage，证据不丢。
- `apply_point` 产出的是**整链**序列，不是 VH/VL；`vdomain` 的域边界按位点继承（长度不变）。
- `apply_region` 直接产出 VH/VL，因为它必须以 parent 的 IMGT 编号为定位基准，无法脱离 `vdomain` 使用。
