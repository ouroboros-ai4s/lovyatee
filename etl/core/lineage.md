# lineage

## 语义

lineage 是一行字符串，由若干片段用 ` | ` 连接。片段分两类：

- **定位片段**：`SRC_Rxx`（必须匹配 `^SRC_R\d+$`）、文件名、`row=N`、`col=<列名>`，由 `locator` 生成，固定在最前。
- **键值片段**：`key=value`，由 `kv` 或 `step` 生成。

同一片段内，值里的 `|` 与 `\` 用反斜杠转义，换行与回车换成空格。`split` 按未转义的 ` | ` 切分，`get` 取第一个同名 key 并反转义，缺失返回 `None`。片段数不固定，`split` 不做结构校验。

## 接口

| 函数 | 返回 | 说明 |
| --- | --- | --- |
| `kv(key, value)` | `"key=value"` | 值转 `str`，转义后拼接 |
| `locator(src, file, *frags)` | `"SRC_Rxx \| file \| ..."` | `src` 不合正则抛 `ValueError` |
| `step(name, *frags)` | `"step=name \| ..."` | 步骤描述片段，第一个片段是 `step=` |
| `join(*frags)` | 用 `SEP` 连接 | 空参数返回 `""` |
| `split(s)` | `list[str]` | 按未转义的 `SEP` 切分 |
| `get(s, key)` | `str \| None` | 第一个同名 key 的反转义值 |
| `SEP` | `" | "` | 分隔符常量 |

## step= 名称约定

- `trim`、`split`、`mutation_rebuild`、`structure_recover`：`merge` 的 `qa_sample` 按这四个名称分层，取最高者；都没有为 `direct`。
- `seqnorm`、`resolve`、`slot_swap`、`slot_single`、`structure_open`、`structure_check`：自由使用，不参与分层。

实体 lineage 的每个元素以 `step=<名称>` 开头；记录级 lineage（observation、locator）不以 `step=` 开头。

## 示例

```python
from etl.core.lineage import get, join, kv, locator, split, step

locator("SRC_R76", "protein_sabdab.csv", "row=123", "ID1=1ABC")
# 'SRC_R76 | protein_sabdab.csv | row=123 | ID1=1ABC'

s = join(locator("SRC_R09", "kothiwal2025htp_DCC_spr.csv", "row=4"),
         kv("col", "SPR kinetics - KD (nM)"))
get(s, "col")            # 'SPR kinetics - KD (nM)'
split(s)                 # ['SRC_R09', 'kothiwal2025htp_DCC_spr.csv', 'row=4', 'col=SPR kinetics - KD (nM)']

t = join(kv("col", "a | b"), kv("x", "1"))
get(t, "col"), len(split(t))     # ('a | b', 2)

step("trim", "n_len=22")                 # 'step=trim | n_len=22'
get(step("trim"), "step")                # 'trim'
get(step("trim"), "nope")                # None
kv("k", "a\nb")                          # 'k=a b'
```
