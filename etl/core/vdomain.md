# vdomain

## 语义

用 ANARCI（IMGT 编号，`allow=["H","K","L"]`）把一条序列编号，得到可变域区间、每个位置的 IMGT 编号映射、区间之外的残余，再据此把序列落成 `vh`/`vl` 槽位。

派生规则（blueprint §3，不得改写）：

- **0 个域** → `reason="no_domain"`。空串、过短、非抗体蛋白都走这一支，不抛异常。非 `[A-Z]+` 的输入不送 ANARCI（hmmscan 会直接报错），同样按无域处理。
- **1 个域**：`H` → `vh`，`K`/`L` → `vl`，另一槽 `None`。VHH 与普通 VH-only 不区分，只写 lineage。TCR 链型不在 `allow` 中，按无域处理。
- **2 个域且恰为一条 H 加一条 K/L**：两域之间的残余必须含 linker（`hints.linker`、`LINKERS`、`(GGGGS)+`），否则 `unresolved`。VL-linker-VH 时按链型换入字段，lineage 写 `orientation=VL-VH`。相邻域的极少数未编号残基归给 linker 两侧后重新切分。
- **其他**（同类型两域、多于 2 域）→ `unresolved`。绝不把同型两域静默压成一对。
- `pair_slots(h, l)`：两槽不同且都不是完整 scFv 时逐槽 `to_fv`，H 槽要得 H、L 槽要得 K/L；恰好反过来则互换并写 `step=slot_swap`；两槽同为 H 或同为 K/L 为 `unresolved`。两槽规范化后相同：`to_fv` 得到 scFv 则按单链处理并写 `step=slot_single`（两个槽位保留），否则 `slot_collision`。只有一槽非空：`to_fv` 该槽。
- **`hints.spans`**（来源给出的构建体边界）：对每个 span 的子序列单独编号，找到域则该域边界取 span（来源边界优先）；ANARCI 自己的边界与之不同时 lineage 追加 `conflict=1` 与 `anarci_span`。找不到域的 span 视为无域。

lineage 元素：

| 元素 | 何时写 |
| --- | --- |
| `step=trim \| span=<s>-<e> \| n_len=<n> \| c_len=<n> \| c_tag=<名>` | 域外有残余或边界冲突；`c_tag` 只在匹配到 `TAGS` 时出现，多个按位置用 `+` 连接 |
| `step=split \| orientation=VH-VL\|VL-VH \| linker=<序列>` | 两域 scFv |
| `step=slot_swap` / `step=slot_single` | `pair_slots` 时置于 lineage 首位 |

`TAGS` 按序列长度降序匹配，已被较长标签覆盖的区段不再匹配。

## 接口

```python
LINKERS = ("GGGGSGGGGSGGGGS", "GGGGSGGGGSGGGGSGGGGS")      # 另匹配 (GGGGS)+
TAGS = {"His6": "HHHHHH", "FLAG": "DYKDDDDK", "HA": "YPYDVPDYA", "Myc": "EQKLISEEDL",
        "V5": "GKPIPNPLLGLDST", "StrepII": "WSHPQFEK", "AviTag": "GLNDIFEAQKIEWHE",
        "TwinStrep": "WSHPQFEKGGGSGGGSGGSAWSHPQFEK"}

@dataclass(frozen=True)
class Hints: linker: str | None = None; spans: tuple[tuple[int, int], ...] | None = None

@dataclass(frozen=True)
class Domain:
    start: int; end: int                          # 0 起，右开
    chain_type: str                               # "H" | "K" | "L"
    residue_index: Mapping[tuple[int, str], int]  # IMGT (编号, 插入码) -> 输入序列 0 起下标，不含 gap
    anarci_span: tuple[int, int] | None           # 仅在 hints.spans 与 ANARCI 不一致时非空

@dataclass(frozen=True)
class Parse: seq: str; domains: tuple[Domain, ...]      # 按 start 升序

@dataclass(frozen=True)
class Construct: vh: str | None; vl: str | None; reason: str | None; lineage: tuple[str, ...]

def parse(seq, hints=None) -> Parse                     # lru_cache(100_000)，同序列只跑一次 ANARCI
def parse_batch(seqs, hints=None) -> list[Parse]        # 一次 ANARCI 调用；含 spans 时退化为逐条
def derive(p, hints=None) -> Construct
def to_fv(seq, hints=None) -> Construct
def pair_slots(h, l, h_hints=None, l_hints=None) -> Construct
```

`reason` 取值：`None`（成功）、`no_domain`、`slot_collision`、`unresolved`。

`residue_index` 是下游 `mutate.apply_region` 的编号来源；`vdomain` 不产生突变。

## 示例

```python
from etl.core.lineage import get
from etl.core.vdomain import Hints, parse, pair_slots, to_fv

c = to_fv(R08_VHH)                       # 152 aa，22 aa 信号肽 + VHH + 6×His
c.vh, c.vl, c.reason                     # (112 aa 的 VHH, None, None)
c.lineage                                # ('step=trim | span=22-134 | n_len=22 | c_len=18 | c_tag=His6',)

to_fv(R76_SCFV)                          # 253 aa，VH-linker-VL
# Construct(vh=<116 aa>, vl=<110 aa>, reason=None,
#           lineage=(..., 'step=split | orientation=VH-VL | linker=GGGGSGGGGSGGGGS'))

to_fv(R76_VL + "GGGGSGGGGSGGGGS" + R76_VH)   # 反向 scFv
# lineage 末元素 'step=split | orientation=VL-VH | linker=GGGGSGGGGSGGGGS'

to_fv(R76_VH + "AAAAAAAAAAAA" + R76_VL).reason            # 'unresolved'
to_fv(R76_VH + "AAAAAAAAAAAA" + R76_VL, Hints(linker="AAAAAAAAAAAA")).reason   # None

pair_slots(R76_H, R76_L).reason          # None
pair_slots(R76_L, R76_H).lineage[0]      # 'step=slot_swap'
pair_slots(R76_H, R76_H).reason          # 'slot_collision'
pair_slots(R76_SCFV, R76_SCFV).lineage[0]# 'step=slot_single'
pair_slots(R76_H, R76_H2).reason         # 'unresolved'（另一条不同的 H）

to_fv("A" * 8).reason                    # 'no_domain'
```

Daft 里的用法（批大小 500，子进程执行，ANARCI 吞吐靠多批并行）：

```python
import daft
from etl.core.vdomain import parse_batch

@daft.func.batch(return_dtype=..., batch_size=500, use_process=True)
def parse_col(seqs: list[str]) -> list[str]:
    return [p.domains[0].chain_type if p.domains else "none" for p in parse_batch(seqs)]
```

## 实测覆盖

ANARCI 2026.2.13.2 + HMMER 3.4，IMGT 编号，2026-11-05，24 进程。序列取自 SRC 原始文件，均已去重。

| SRC | distinct 序列 | `no_domain` | `unresolved` | `to_fv` 成功率 |
| --- | --- | --- | --- | --- |
| R76 | 809 | 0 | 1 (0.1%) | 99.9% |
| R77 | 809 | 0 | 1 (0.1%) | 99.9% |
| R08 | 5577 | 1 (0.02%) | 0 | 99.98% |
| R74 | 576 | 0 | 0 | 100% |

结论：ANARCI 成功率 ≥ 99.9%，`no_domain` 占比可接受，不需要引入第二个工具（blueprint §3 的判据是"某 SRC 无来源边界且 `no_domain` 占比不可接受"）。

三个例外逐条看：

- R08 的 1 条 `no_domain` 是语料表里的非 VHH 残留行，正常排除。
- R76/R77 的 1 条 `unresolved` 是同一个序列（256 aa，VL + 22 aa 非 G4S linker + VH，中间为 `GSGGSTITSYNVYYTKLSSSGS`）。无来源边界，adapter 应从源文档给出 `Hints(linker=...)` 后转为正常 scFv；给不出 linker 时按未解析排除。
