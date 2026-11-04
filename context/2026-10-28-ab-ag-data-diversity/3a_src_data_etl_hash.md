---
tags:
  - design
---

本设计文件针对的是 [[2026-11-01-20-src-data-etl-todo-list]] 中的 `## 1. Data ETL Specification`.

# AB_ID AG_ID 3A_ID Hash Scheme

## time

2026-11-01

## lineage

- 3a_src_data_etl_modeling.md: 3A model and ID definitions.
- 3a_src_data_etl_problem_ab.md: AB canonical serialization (`<SEP>`, `<NONE>`).
- 3a_src_data_etl_problem_ag.md: AG canonical serialization (`<SEP>`).

## relation

None.

## description

### 规则

- 哈希函数：SHA-256，输入为 UTF-8 字节，输出取前 128 位，小写 hex，共 32 字符。
- 输入只含清洗后的规范化序列。`structure`、`lineage`、来源、名称和 affinity 不参与。
- 每个输入带「类型/版本」前缀，使 AB、AG、3A 三个 ID 空间互不相交。
- `<SEP>` 和 `<NONE>` 是固定字面量。规范化后的序列只含氨基酸字符，不会与它们冲突。

### 定义

```python
def H(s: str) -> str:
    return sha256(s.encode("utf-8")).hexdigest()[:32]

AB_ID = H("ab/v1:" + (vh or "<NONE>") + "<SEP>" + (vl or "<NONE>"))
AG_ID = H("ag/v1:" + "<SEP>".join(chains))   # chains: 固定链顺序的有序序列列表
3A_ID = H("3a/v1:" + AB_ID + "|" + AG_ID)    # AB 在前，AG 在后
```

- `vh`、`vl`：空字符串先转为 `None`，再序列化为 `<NONE>`。VHH 和 heavy-only 的 `vl` 为 `None`，VL-only 的 `vh` 为 `None`。
- `chains`：单链和短肽是单元素列表；多链顺序按 problem_ag 第 4 项固定，不得排序后再 hash。
- 链顺序不同的同一组链是不同的 `AG_ID`。

### 版本

- 前缀中的 `v1` 是 ID 方案版本。清洗规则或序列化规则变化会改变 ID，此时升级版本号，不原地改写旧 ID。
- 每次运行把 ID 版本、清洗规则版本和代码 commit 写入全局 manifest。

### 校验

- 入库时对 ID 做碰撞检查：同一 ID 对应不同 canonical 字符串则中止，不静默合并。
- 每条 lineage 记录 canonical 字符串，便于由 ID 回溯输入。
- 单元测试固定一组 `(canonical 字符串, ID)` 向量，防止序列化被无意改动。
