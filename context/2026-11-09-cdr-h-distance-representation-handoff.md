---
tags:
  - context
---

# CDR-H 距离原料表示方案 —— Handoff

## 当前结论

三个 CDR-H pairwise distance matrix 不应作为唯一的数据源。

原始信息是每个 unique VH 在 CDR-H1、CDR-H2、CDR-H3 的 IMGT 对齐结果。距离矩阵只是把这些结果两两比较后物化出来的派生结果。可以保存对齐后的 CDR 表示，在需要时按原规则计算距离，从而保持每个 pairwise 距离不变，同时避免提前落盘三份超大矩阵。

这不是把矩阵的一行聚合成一个值，也不是保存 k 近邻或阈值边。每条 VH 的每个 CDR 位点仍然完整保留。

## 必须保持的原始定义

| 项 | 约束 |
|---|---|
| 对象 | IMGT unique numbering 下的 CDR-H1 / H2 / H3 |
| 对齐 | 按 IMGT position/key 对齐 |
| 插入位点 | 保留在编号层，用于对齐；不把它们混成普通序列位置 |
| 距离 | 按共同 IMGT 位点逐位比较，非 Levenshtein |
| 缺失 | 任一方 CDR 或位点为 null 时，该位点不计入该 pair 的距离 |
| 输出 | H1、H2、H3 三个距离分别保留 |

距离计算的人话版本：

1. 取两条 VH 的同一个 IMGT 位点。
2. 如果任一方没有这个位点，跳过。
3. 如果两边都有氨基酸且不同，距离加一。
4. 对 H1、H2、H3 分别累计。

## 现有产物

远程主机 `3x5090` 的 `/data_new/ywy/analysis/l1/`：

- `vh_distinct.parquet`
  - 1,172,563 条 unique VH
  - 列：`vh, n_rows, n_ab, ag_ids`
- `cdr_all.parquet`
  - 单次 ANARCI pass 的结果
  - 列：`vh, n_rows, n_ab, {h1,h2,h3}_{seq,n,key,err}`
  - `key` 保存 IMGT 位置串
- `cdr_all.py`
  - CDR 提取与 IMGT key 生成
- `cmp_lev_ham.py`
  - 原距离与 Levenshtein 的对比脚本

`cdr_all.parquet` 已经基本是距离计算的直接原料。新方案不需要重新对 1,172,563 条 VH 做 ANARCI；重点是把现有 `{seq, key}` 规范化成可批量读取的固定位置表示。

## 目标数据流

```text
unique VH
  -> ANARCI IMGT numbering（现有结果）
  -> CDR-H1/H2/H3 的 key + residue
  -> 固定的 IMGT position 表
  -> 每条 VH 的 CDR 编码
  -> 精确 pairwise distance provider
  -> clustering
```

## 实施计划

### 1. 冻结现有距离契约

远端连通后先读取 `cdr_all.py` 和 `cmp_lev_ham.py`，确认以下细节：

- IMGT key 的具体排序；
- 插入位点的排序和表示；
- 空 CDR、无 ANARCI domain、全 null 的处理；
- 两条序列的共同位点规则；
- 距离是否为原始 mismatch count，是否存在归一化；
- H1/H2/H3 的边界和输出类型。

保存现有 400×400 结果作为 golden reference。

### 2. 生成规范化 CDR 表示

以现有 `cdr_all.parquet` 为输入，分别为 H1、H2、H3 建立全局 IMGT position 表。

每条 VH 在每个固定位置保存：

- 氨基酸编码；
- null 标记；
- 必要时保留原始 key 映射和错误状态。

编码可以使用紧凑的 `uint8` 或 bit-packed 表示。预计总规模为几十到百 MB，具体大小取决于实际 IMGT key 数量。

同时保存：

- VH 到整数 row index 的映射；
- 每个 CDR 的 position 表；
- 氨基酸编码表；
- 距离规则版本；
- 输入文件与代码版本信息。

### 3. 实现精确距离计算器

实现按 block 读取的距离计算器：

- 输入两组 VH row；
- 只比较相同 IMGT position；
- null 按现有规则跳过；
- 对 H1/H2/H3 分别返回整数距离；
- 不计算 Levenshtein；
- 不改变距离定义。

先实现一个直接、可审计的参考版本，再考虑 GPU 或 SIMD 优化。全量计算仍然是 pairwise 规模，改变的是存储方式，不是计算复杂度。

### 4. 接入 clustering

优先让 clustering 读取：

- 固定 CDR 表示；或
- 能按 block 返回精确距离的 distance provider。

禁止用以下结果替代完整距离关系：

- k 近邻图；
- 阈值边；
- 随机 pair；
- 低维近似 embedding。

如果当前聚类程序硬性要求完整预计算矩阵，则需要先确认具体算法：

- 支持距离函数或 block 输入：直接改输入接口；
- 只支持矩阵随机读取：使用外部存储/分块读取；
- 无法改接口：bit-pack 作为兜底方案，而不是主方案。

### 5. 验证

必须完成：

- 新旧实现对 400×400 的 H1/H2/H3 距离逐项相等；
- 覆盖全 null、空 CDR、无 domain、插入位点、长度差异、相同序列和最大长度；
- 抽样比较距离分布、行统计和距离排序；
- 在小数据集上比较新旧 clustering 结果；
- 对 1 万、10 万条做 block 速度、内存和显存测试；
- 通过后再跑 1,172,563 条全量。

## 兜底方案

如果下游最终确实要求三份完整矩阵文件，可以利用距离上限做 bit-packing：

- H1：5 bit；
- H2：5 bit；
- H3：6 bit。

三份矩阵约从 2.06 TB 降到 1.38 TB。这个方案保持完整 pairwise 矩阵，但仍然保留了矩阵的存储和随机访问成本，只作为接口无法改动时的兜底。

## 当前阻碍

本地仓库没有 `analysis/l1` 下的实际脚本；这些脚本位于 `3x5090`。当前 SSH 连接被拒绝，因此尚未核对 `cdr_all.py` 和 `cmp_lev_ham.py` 的具体实现。

远端恢复后，第一步不是写新代码，而是读取这两个脚本并用 400×400 golden reference 锁定全部距离语义。
