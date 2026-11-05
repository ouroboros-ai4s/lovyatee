# merge

## 语义

把各 SRC 的 `pair` Parquet 合并成 modeling 的 `3A`，并产出运行旁表。所有查询在 DuckDB 里做，输出按 pyarrow 声明 schema 写出。

**输入契约** `PAIR_SCHEMA`（B 层 assemble 的输出，每个 SRC 一组 Parquet）：

| 列 | 类型 | 含义 |
| --- | --- | --- |
| `src` / `record_key` | str | 来源与源内记录键 |
| `AB_ID` / `AG_ID` / `3A_ID` | str | 已算好的 ID；链为空时可为 `None` |
| `vh` / `vl` | str | 清洗后可变域序列，可为 `None` |
| `ab_structure` / `ag_structure` | struct | `{structure_id, file_ref, chain_map}`，`chain_map` 是 JSON 字符串 |
| `ab_structure_rank` / `ag_structure_rank` | int32 | 小者优先；SRC 自带快照应赋比 RCSB 小的值，`None` 排最后 |
| `ab_lineage` / `ag_lineage` | list\<str\> | 实体清洗 lineage，每元素以 `step=` 开头 |
| `ag_sequence` | list\<str\> | 有序链序列，顺序参与 `AG_ID` |
| `obs` | list\<struct\> | `{label, assay, condition, replicate, lineage[]}` |

规则：

1. **有效性**：`vh`、`vl` 全空，或 `ag_sequence` 为空或含空串，或 `obs` 为空，或任一 `label` 为 `None` → 不进 `3a`，写 `reject_log(stage="merge", reason_code="invalid_3a")`，不中止运行。
2. **ID 校验**：SQL 校验同一 `AB_ID`/`AG_ID`/`3A_ID` 只对应一个 canonical；再对 distinct 行用 `ids.*` 重算与存储值比较。不一致抛 `IdCollision`，**在写 `out_dir` 之前中止**（不会留下半成品 `3a/`）。
3. **分组**：按 `3A_ID`。`affinity` 为各 pair 的 `obs` 按 `(src, record_key, obs 下标)` 排序后拼接，每条恰好一次。实体 `lineage` 取并集后按字典序排序。`structure` 取 `(rank, structure_id, src)` 最小者，其余进入 `structure_alt=<id>` lineage 元素。
4. **对账断言**：`Σ len(affinity)` 等于有效 pair 的 `obs` 总数；`pairs - 3a` 为相同 `3A_ID` 的合并数，写入 manifest。
5. **分片**：`int(3A_ID[:8], 16) % shards`，每片内按 `3A_ID` 排序。
6. **stats** 四张表：
   - `coverage(src, n_pairs, vh_null, vl_null, ab_structure_null, ag_structure_null)`
   - `rejects(src, stage, reason_code, n)`，含 `reject_glob` 读入的各阶段行与本阶段行
   - `label_types(src, col, rest, n)`：从 obs lineage 取 `col=` 片段，`rest` 为其后其余片段以 ` | ` 连接
   - `overlap(3A_ID, srcs)`：每个 `3A` 的 SRC 集合，取自 obs lineage 首片段
7. **qa_sample(3A_ID, stratum)**：分层取实体 lineage 中出现的 `step=` 名称，优先级 `structure_recover > mutation_rebuild > split > trim`，都没有为 `direct`；每层按 `md5(f"{seed}|{3A_ID}")` 升序取 `qa_per_stratum` 个。
8. **manifest.json**：键排序、无时间戳、无绝对路径。含 `id_version`、`rules_version`、`code_commit`、`tools`、`decision_files`（文件名 → sha256）、`row_counts`、`qa`。

输出布局：

```text
out_dir/
  3a/part-000.parquet ...         processed dataset 的唯一一项
  stats/{coverage,rejects,label_types,overlap}.parquet
  qa_sample.parquet
  reject_log.parquet
  manifest.json
```

对账公式（blueprint §8）：`Σ len(affinity[])` = 全部 pair 的成立 observation 总数，每条恰好一次；`pair 数 - 3A 数` = 相同 `3A_ID` 的合并数。

## 接口

```python
PAIR_SCHEMA: pa.Schema      # 见上
OUT_SCHEMA: pa.Schema       # 3A_ID, antibody{AB_ID, vh_sequence, vl_sequence, structure, lineage},
                            # antigen{AG_ID, sequence, structure, lineage}, affinity[{label, assay, condition, replicate, lineage}]
REJECT_SCHEMA: pa.Schema    # stage, reason_code, src, key, detail（detail 为 JSON 字符串）

@dataclass(frozen=True)
class MergeReport: n_pairs: int; n_3a: int; n_obs: int; n_rejected: int

def merge(pair_glob: str, out_dir: Path, *, reject_glob: str | None = None, shards: int = 16,
          qa_seed: int = 0, qa_per_stratum: int = 50,
          decision_files: Sequence[Path] = (), rules_version: str = "v1") -> MergeReport
```

`n_pairs` 为有效 pair 行数；`n_rejected` 为本阶段写入 `reject_log` 的行数（不含 `reject_glob` 读入的其他阶段行）。

## 示例

```python
from pathlib import Path
from etl.core.merge import merge

rep = merge("/data_new/ywy/runs/r1/assemble/*.parquet", Path("/data_new/ywy/runs/r1/merge"),
            reject_glob="/data_new/ywy/runs/r1/rejects/*.parquet",
            shards=16, qa_seed=0, qa_per_stratum=50,
            decision_files=sorted(Path("etl/decisions").glob("*.yaml")))
# MergeReport(n_pairs=..., n_3a=..., n_obs=..., n_rejected=...)
```

读回：

```python
import pyarrow.parquet as pq
t = pq.read_table("/data_new/ywy/runs/r1/merge/3a")
t.schema == OUT_SCHEMA           # True
```

重跑同一输入，`3a`、`stats`、`qa_sample`、`reject_log` 逐字节相同（manifest 因含 commit 与工具版本而不同）。
