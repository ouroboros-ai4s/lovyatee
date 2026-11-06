# ETL B 层进度

起始 2026-11-06。base commit `5997064`（`origin/etl-a-layer`）。

## 开工状态

- **偏离一处，已记录：** plan 要求 A 层先合入 `origin/main` 再开工。实测 `origin/main` 无任何 `etl/` 文件，`etl-a-layer` 分支完整且 `pytest etl` 59 项全过。`etl-b-layer` 因此从 `origin/etl-a-layer@5997064` 切出。Pthahnix 合并时先合 `etl-a-layer`，`etl-b-layer` 可 fast-forward 接上。
- `pytest etl`：59 passed（2026-11-06，host）。
- 输出根：`/data_new/ywy/etl_out/`；结构缓存 `/data_new/ywy/cache/rcsb/`。
- A 层 `vdomain.md` 记录的 `no_domain` 实测：R76 809 distinct 中 0，R77 同，R08 5577 中 1（0.02%），R74 576 中 0。

## 沉淀的做法（后续 SRC 复用）

**目录**
```text
etl/b/
  pipeline.py   驱动：Record、缓存键、ab/ag 分阶段、assemble、reconcile.json
  entities.py   共享 resolver：evidence -> ab_entity / ag_entity
  run_src.py    python -m etl.b.run_src R76 --workers 32
  check.py      python -m etl.b.check SRC_R76（判据 1-5）
etl/adapters/<src>.py   SRC 专属 adapt() -> (records, rejects)
```
产物：`/data_new/ywy/etl_out/<SRC>/{raw_ab,raw_ag,raw_obs,ab_entity,ag_entity,pair,reject_log}.parquet`、`reconcile.json`、`<stage>.parquet.key`、`merge_check/`。

**adapter 契约**
- `adapt()` 返回 `(list[Record], list[reject dict])`。raw 值（`h_raw` / `l_raw` / `ag_raw` / `label`）与源单元格逐字一致，除 `.strip()` 外不改动。
- `Record.ab_evidence` / `ag_evidence` 只放影响清洗的小字符串字段，进 `ab_key` / `ag_key`。
- 大对象（例如 parent 的编号表）放 `Record.ab_ctx` / `ag_ctx`，不进键。
- observation 的 `lineage` 由 adapter 用 `lineage.locator` 加 `kv("col", 列名)` 拼，不拼 ID。

**共享 resolver**
- `ab_entity`：`seqnorm.normalize` -> 可选 `mutate.apply_point` -> `vdomain.pair_slots` -> `ids.ab_id`。
- `ag_entity`：`seqnorm.normalize` -> `antigen_bound.bound` -> `ids.ag_id`。
- 排除码直接来自 core 模块：`no_domain`、`slot_collision`、`unresolved`、`no_sequence`、`non_protein`、`sequence_conflict`、`boundary_*`、`order_ambiguous`；adapter 侧另有 `bad_slot_list`、`missing_sequence`、`no_observation`。

**缓存键**
`stage_key = H(RULES_VERSION, etl/core 的 git commit, src, 阶段名, 决策文件 hash, 排序后的全部输入键)`。命中即跳过该阶段，产物旁 `.key`。`RULES_VERSION` 在 `pipeline.py`。

**对账**
`reconcile.json` 每次运行写：records / adapt_rejects / ab_keys / ag_keys / pairs / assemble_rejects / observations / distinct_3a / reasons。`check.py` 逐条比对 plan 判据 1-5 并跑单源 merge 断言。

**共享模块改动**：无。

## SRC 进度

### R76 TDC AntibodyAff — 完成

- 数据：`protein_sabdab.csv` 493 行，与 inventory 一致。476 唯一 `(X1, X2)` pair；21 行两槽位相同（其中 15 行含 `GGGGSGGGGSGGGGS`）；Y 无空值；14 对重复 2 次、1 对重复 4 次。
- 各阶段：adapt 493 / 0 rejects → ab 493 键（492 ok，1 `slot_collision`）→ ag 401 键（401 ok）→ assemble 492 pair、1 reject。
- 单源 merge：`n_pairs=492, n_3a=475, n_obs=492, sum len(affinity)=492`，断言全过。`pair - 3A = 17`，等于重复对多出的观测数（14×1 + 1×3）。
- 排除占比：`slot_collision` 1/493 = 0.2%。
- `no_domain` 占比：0，与 `vdomain.md` 一致。
- 476 差额闭合：476 唯一 pair → 475 个 `3A`，差 1 是 `slot_collision` 那条（`3ux9`，同一 256 aa 序列写入两槽，VL + 22 aa 非 G4S linker + VH，无来源边界可给 `Hints.linker`；与 `vdomain.md` 记录的 R76/R77 那 1 条 `unresolved` 是同一条）。
- 抽查：3 条 `raw_ab` 与源单元格逐字一致；3 条 `3A` 的 `col=Y` 与行号回溯正确。
- `qa_per_stratum` 建议 50。R76 的实体 lineage 分布：trim 956、split 20、slot_single 20、seqnorm 1；trim 层取 50 条足够。`structure_recover` 与 `mutation_rebuild` 两层要到 R74 / R14 才有样本。

### R77 Akbar SAbDab Kd — 完成

- 数据：`antibody_affinity_protein_sabdab.csv` 493 行，列名 `Antibody_ID / Antibody / Antigen_ID / Antigen / Y`，与 inventory 一致，与 R76 同源。
- 各阶段：与 R76 同 —— adapt 493 / 0 rejects → ab 493 键（492 ok，1 `slot_collision`）→ ag 401 键 → assemble 492 pair。
- `3A_ID` 集合与 R76 完全相同（各 475，交集 475，两侧独有 0），与 inventory 的同源快照判断一致。
- R76 + R77 merge（`/data_new/ywy/etl_out/R76_R77_check`）：`n_pairs=984, n_3a=475, n_obs=984`，`sum len(affinity)=984`。共有 `3A_ID` 的 `affinity[]` 同时含两个 SRC 的 tuple，各自保留定位（例：`SRC_R76 | protein_sabdab.csv | row=331 | ID1=5c0s | col=Y` 与 `SRC_R77 | antibody_affinity_protein_sabdab.csv | row=331 | Antibody_ID=5c0s | col=Y`）。
- `affinity` 长度分布：460 条 2、14 条 4、1 条 8，与 R76 内重复结构跨源叠加一致。
- 集合差异：0 条。
