# ids

## 语义

`AB_ID`、`AG_ID`、`3A_ID` 是清洗后规范序列的 SHA-256 前 128 位（32 位小写 hex），输入带类型前缀，三个 ID 空间互不相交：

```
H(s)        = sha256(s.encode("utf-8")).hexdigest()[:32]
AB_ID       = H("ab/v1:" + (vh or "<NONE>") + "<SEP>" + (vl or "<NONE>"))
AG_ID       = H("ag/v1:" + "<SEP>".join(chains))
3A_ID       = H("3a/v1:" + AB_ID + "|" + AG_ID)
```

`ab_canonical`、`ag_canonical` 返回的字符串就是传给 `H` 的完整输入，含前缀；lineage 记录它，ID 可回溯输入。`structure`、`lineage`、来源名称与 affinity 不参与。

约束：

- 序列只接受 `^[A-Z]+$`（清洗后的序列），违反抛 `ValueError`。
- 空字符串先转 `None`。`vh` 与 `vl` 都为 `None` 抛 `ValueError`。
- `chains` 非空、元素非空、顺序即给定顺序，**不得排序后再 hash**；链序不同则 `AG_ID` 不同。
- VHH 与 heavy-only 的 `vl` 为 `None`，VL-only 的 `vh` 为 `None`。

**版本升级**：清洗规则或序列化规则变化时把 `ID_VERSION` 升到 `v2`，不原地改写旧 ID。每次运行的 ID 版本与规则版本写入 `manifest.json`。

## 接口

| 函数 | 返回 | 说明 |
| --- | --- | --- |
| `H(s)` | 32 位 hex | 直接哈希，不做校验 |
| `ab_canonical(vh, vl)` | `"ab/v1:..."` | |
| `ag_canonical(chains)` | `"ag/v1:..."` | |
| `ab_id(vh, vl)` | `AB_ID` | |
| `ag_id(chains)` | `AG_ID` | |
| `three_a_id(ab, ag)` | `3A_ID` | 参数是已算好的两个 ID |
| `check_collisions(pairs)` | `None` | `(id, canonical)`，同 id 不同 canonical 抛 `IdCollision` |
| `IdCollision` | `Exception` | |
| `ID_VERSION` | `"v1"` | |

## 示例

```python
from etl.core.ids import ab_id, ag_id, three_a_id

VH, VL = "EVQLVESGGGLVQPGGSLRLSCAAS", "DIQMTQSPSSLSASVGDRVTITC"
ab_id(VH, VL)                     # 'e3530acaf90a5cf523a8b903e5372108'
ab_id(VH, None)                   # '59f042dd1616144d9f65b9a11841453f'
ab_id(None, VL)                   # 'de2aae6e62343da45bae33b3a8a080eb'
ab_id(VH, "")                     # 同 ab_id(VH, None)
ag_id(["MKTAYIAKQR"])             # '55ed5a94b7b3b6807cce2bb54e47868e'
ag_id(["MKTAYIAKQR", "GSHMLE"])   # '68fc1ebba8e066070e2faaca2d29e264'
ag_id(["GSHMLE", "MKTAYIAKQR"])   # 'ce1862b24e9e2302a97209f63b878a97'  链序参与 hash
three_a_id(ab_id(VH, VL), ag_id(["MKTAYIAKQR"]))
# '3aa15df2f9fb69f637d53f45e9843941'
```

这些向量也由 host 上的 `sha256sum` 独立算过，见 `test_ids.py`。

规模上 `merge` 不逐行调 `check_collisions`：它在 DuckDB 里按 ID 分组数 distinct canonical，等价检查（见 `merge.md`）。
