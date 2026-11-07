# ETL B 层产物交接

[[2026-11-05-etl-a-layer-dev-plan]] 和 [[2026-11-05-etl-b-layer-handoff-plan]] 的产物交接.

## 位置

全部产物在远程主机 `ssh 3x5090`，仓库之外：

```text
/data_new/ywy/etl_out/
├── final/            最终结果（下称根）
├── final_rerun/      同一输入的第二遍，用于复现核对
└── SRC_R03 … SRC_R80/   各源中间产物，20 个目录
```

`etl_out/` 合计约 13 GB，其中 `final/` 411 MB、`final_rerun/` 411 MB。

## 最终结果 `final/`

```text
final/
├── 3a/                  16 个 Parquet 分片，part-000.parquet … part-015.parquet，共 326 MB
├── stats/
│   ├── coverage.parquet     各 SRC 的 pair 数、空槽计数
│   ├── overlap.parquet      每个 3A_ID 覆盖了哪些 SRC
│   ├── label_types.parquet  各 SRC 的读数来源列
│   └── rejects.parquet      排除码按 SRC / 阶段计数
├── qa_sample.parquet    200 条抽样，4 个层各 50 条
├── reject_log.parquet   merge 阶段的排除记录，38 MB
└── manifest.json        行数、代码 commit、工具版本、决策文件 sha256
```

`manifest.json` 记录的计数：

| 项 | 值 |
| --- | ---: |
| `pairs` | 3,785,871 |
| `3a` | 1,901,774 |
| `obs` | 4,459,976 |
| `rejected` | 0 |

`code_commit` 为 `8d221796be97f83c30dcb0646467be4d987741bb`，已合入 `main`（合并点 `860fe4d`）。

## 3a 的表结构

一行一个 `3A`：

- `3A_ID` string
- `antibody` struct：`AB_ID`、`vh_sequence`、`vl_sequence`、`structure`（`structure_id` / `file_ref` / `chain_map`）、`lineage[]`
- `antigen` struct：`AG_ID`、`sequence[]`、`structure`、`lineage[]`
- `affinity[]` struct：`label`、`assay`、`condition`、`replicate`、`lineage[]`

## 各 SRC 中间产物

`SRC_R*/` 下固定这几个文件：

```text
raw_ab.parquet          清洗前的原始槽位值
raw_ag.parquet
raw_obs.parquet
ab_entity.parquet       distinct 抗体键的解析结果（含排除码）
ag_entity.parquet
pair.parquet            符合 etl.core.merge.PAIR_SCHEMA
reject_log.parquet      adapt + assemble 阶段排除
reconcile.json          各阶段计数
check.json              判据 1–5 结果
merge_check/            单源 merge 的 3a
run.log
*.parquet.key           阶段缓存键
```

`SRC_R20/` 为空目录：它是结构资源适配器，不产 pair / 3A。

各目录体积（大者）：`SRC_R75` 3.8 GB、`SRC_R10` 3.7 GB、`SRC_R09` 2.4 GB（其中 `SRC_R09/data/` 2.2 GB 是从压缩包解出的源 CSV）、`SRC_R23` 761 MB、`SRC_R12` 402 MB。

## 读法

全部是 Parquet，pyarrow 与 duckdb 都可直接读：

```python
import duckdb
con = duckdb.connect()
con.sql("select count(*) from read_parquet('/data_new/ywy/etl_out/final/3a/*.parquet')")
```

## 相关代码

`/data_new/ywy/LOVYATEE`，`main` @ `860fe4d`。

```text
etl/adapters/r03.py … r80.py   20 个 SRC 适配器
etl/b/pipeline.py              驱动
etl/b/entities.py              共享 resolver
etl/b/run_src.py               python -m etl.b.run_src SRC_R76
etl/b/check.py                 python -m etl.b.check SRC_R76
etl/b/final_merge.py           全局 merge
etl/decisions/*.yaml           8 个 SRC 的决策文件
etl/progress.md                逐 SRC 记录与验收结果
```

## 源数据

`/data_new/ywy/dataset-abag/SRC_Rxx_*`。

## 环境

```bash
ssh 3x5090
cd /data_new/ywy/LOVYATEE && source etl/env.sh
```

`env.sh` 给出 venv `/data_new/ywy/envs/etl`、HMMER、`TMPDIR`、RCSB 缓存与 `ETL_PROXY=http://127.0.0.1:17890`。
