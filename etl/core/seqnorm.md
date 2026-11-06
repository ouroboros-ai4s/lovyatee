# seqnorm

## 语义

把源里的原始序列字符串（可能带 FASTA 标题、换行、空白、大小写混排）变成清洗后的序列，或返回 `None` 并附排除标记。它只做与业务无关的规范化，不猜任何源特有的占位写法。

规则按顺序：

1. 以 `>` 开头的行视为标题并丢弃；标题行多于一个 → `multi_record`。
2. 转大写，删除全部空白。
3. 结果为空 → `placeholder`。
4. 与 `placeholders` 中任一项（忽略大小写与首尾空白）相等 → `placeholder`。文本占位符（`NA`、`None`、`N/A`）由 adapter 通过该参数传入，模块自己不猜。
5. 含 `-`、`.`、`*` 中任一 → `gap`。**不截断尾部的 `*`，也不填 gap**：返回 `None` 并打标记，由 adapter 按源的语义自行预处理（截断、拆链或排除）。FASTA 的尾部 `*` 与内部对齐 gap 是两件事，模块不区分。
6. 含非 ASCII 字母字符（数字、符号、全角字符）→ `illegal_char`。
7. 含 `X B Z J U O` → 保留序列，标记 `unknown_residue`。

`placeholder`、`gap`、`illegal_char`、`multi_record` 时 `seq=None`；`unknown_residue` 时 `seq` 非空。

## 接口

```python
class SeqNorm(NamedTuple):
    seq: str | None
    flags: tuple[str, ...]      # 取值：placeholder, gap, unknown_residue, illegal_char, multi_record
    @property
    def lineage(self) -> tuple[str, ...]

def normalize(raw: str | None, placeholders: Collection[str] = ()) -> SeqNorm
```

`lineage`：无 flags 返回 `()`；否则返回单元素 `("step=seqnorm | flags=gap,unknown_residue",)`，flags 按上表顺序排列。

## 示例

```python
from etl.core.seqnorm import normalize

normalize(" evq lve\n")                              # ('EVQLVE', ())
normalize(">1ABC_H mol:protein\nEVQL\nVESG\n")       # ('EVQLVESG', ())
normalize("EVQLV*")                                  # (None, ('gap',))
normalize("EVQ-LV")                                  # (None, ('gap',))
normalize("EVQLV*").lineage                          # ('step=seqnorm | flags=gap',)
normalize("EVQXLVB")                                 # ('EVQXLVB', ('unknown_residue',))
normalize("EVQ1LV")                                  # (None, ('illegal_char',))
normalize(">a\nEVQ\n>b\nLVE")                        # (None, ('multi_record',))
normalize(None)                                      # (None, ('placeholder',))
normalize("NA")                                      # ('NA', ())            默认不认占位符
normalize("na", placeholders={"NA"})                 # (None, ('placeholder',))
```

adapter 侧的典型用法：先按源文档把 `NA`、`-` 等占位写进 `placeholders`，再对尾部 `*` 自己截断。
