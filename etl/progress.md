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

### R08 AVIDa-hTNFa — 完成

- 数据：`AVIDa-hTNFa.csv` 5,580 行 + `corpus-hTNFa.csv` 216,225 行无标签语料 + `antigen_sequences.csv` 1 行。与 inventory 一致。
- 决策文件 `etl/decisions/R08.yaml`：3 条 claim，`verify_decisions` 通过。抗原序列 = 233 aa TNF-alpha 前体，来自 `antigen_sequences.csv`；1TNF 只作靶点代表结构。
- 各阶段：adapt 5,580 records / 216,225 rejects（语料整表无 label，按 aff 方案第 1 项类 1 不成立，逐行进 reject）→ ab 5,577 键（5,576 ok，1 `no_domain`）→ ag 1 键 → assemble 5,579 pair。
- 单源 merge：`n_pairs=5,579, n_3a=5,571, sum len(affinity)=5,579`，断言全过。
- `no_domain` 占比 0（1/5,577），与 `vdomain.md` 的实测值一致。
- 过半码复查：`no_observation` 97.5% 全部来自语料表，该表确实无 label，条件成立，接受。
- 裁剪：5,579 条中 5,562 条 `c_tag=His6`、全部有 `n_len=22` 信号肽裁剪，与 inventory 的 22 aa + 6×His 描述一致。
- 抽查：3 条 `raw_ab` 与源单元格逐字一致；抽样的 `3A` 沿 lineage 回溯到行、`col=label`。

### R74 AbDesign 2.0 — 完成

- 数据：`pd_1/affinity.csv` 578 行（576 条有名 + 2 条 assay 对照），与 inventory 一致。
- 决策文件 `etl/decisions/R74.yaml`：3 条 claim，通过自查。抗原 = 5GGS entity 3 chain Y（123 aa PD-1），`structref` 取 entity 序列核对。
- 各阶段：adapt 566 records / 12 rejects（2 条对照无序列 `no_sequence`，10 行 kd 与 binding 均空 `no_observation`）→ ab 566 键全 ok → ag 1 键。
- observation 拆分：`kd` 388 条 + `binding` 178 条 = 566；`kd` 有值的行不再产出 `binding`，kon/koff/r2 不产出。inventory 记 388 / 566 是各自原始值行数，差 10 行两列皆空。
- 单源 merge：`n_pairs=566, n_3a=566, sum len(affinity)=566`，断言全过。
- 突变名（`5GGS__A_B_Z__A_T_28_M`）只进 lineage 的 `name=`。

### R03 AbDesign 1.0 — 完成

- 数据：`datasets_mut.csv` 1,303 行 + `datasets_wt.csv` 57 行，与 inventory 一致。
- 各阶段：adapt 1,303 records / 57 rejects（WT 参照表无 label，按 aff 方案第 1 项不成立）→ ab 1,226 键全 ok → ag 47 键（47 个 parent PDB，与 inventory 一致）→ assemble 1,303 pair。
- `affinity_type` 分布：`elisa_mut_to_wt_ratio` 658 + `ddg` 645 = 1,303，与 inventory 的 658 / 645 完全一致，且写进 observation lineage。
- 单源 merge：`n_pairs=1,303, n_3a=1,142`，断言全过；`pair - 3A = 161` 是同序列对不同抗原重复三元组合并。
- 抽查：`affinity_type=` 出现在 lineage 中，`method=` 与 `pdb_name=` 定位齐备。

### R80 ANTIPASTI — 完成

- 数据：`sabdab_summary_all.tsv` 1,266 行、`mendeley-data` 715 个 PDB（inventory 记 2,268 个文件，实际目录里 715 个且覆盖全部 715 个不同 PDB，不构成口径差异）。
- 与 inventory 的一处出入：`antigen_chain` 可以是多链（`E | G`），inventory 未提。按链序全部入库，链序参与 `AG_ID`。
- 各阶段：adapt 1,053 records / 213 rejects（209 `non_protein`：`antigen_type` 非 protein/peptide；4 `unresolved`：4KV5 的 I/K/L/F 链在 PDB 中不存在）→ ab 1,053 键（1,048 ok，3 `no_domain` + 2 `unresolved`）→ ag 1,041 键。
- **共享模块修改一处**：`vdomain.Hints` 新增 `single_chain`。来源已声明该行是单链构建体时，两域之间的整段残余即 linker，不再要求识别连接序列。R80 的 `scfv=True` 行因此从 47 条 `unresolved` 降到 2 条。理由：来源已给出构建体几何，要求 ANARCI 认出非标准 linker 属于额外约束；这一改动不涉及任何 SRC 分支，`Hints` 是通用输入。
- 排除占比：`non_protein` 16.5%、`unresolved` 0.47%、`no_domain` 0.24%。均未过半。
- `delta_g` 不产出，只有 `affinity`。
- 单源 merge：`n_pairs=1,048, n_3a=827`，断言全过。

### 第一批收尾 merge

`/data_new/ywy/etl_out/merge_all`（该 glob 覆盖 `SRC_R*/`，此刻即第一、二批已完成的部分）：
`n_pairs=9,480, n_3a=8,501, n_obs=9,480`，`Σ len(affinity)=9,480`，断言全过。
`overlap`：R08 5,571、R03 1,140、R80 749、R74 566、R76+R77 397、R76+R77+R80 76、R03+R76+R77+R80 2 —— 跨源同一 `3A` 的 SRC 集合并集正常。
`coverage`：R80 `vh_null=9`、`vl_null=154`（VL-only 与 VHH 行），其余 SRC 无空槽。

### R13 ANDD — 完成

- 数据：`ANDD_v2.xlsx` 单表 48,800 行、49 列。截面积：抗原、抗体、label 三者齐备 8,416；缺抗原 36,183；缺 label 4,201；全缺 0。
- 与 inventory 一致：`Predicted_or_Not` 四态 `real` 7,294 / `predicted` 2,271 / `\` 39,235；Kd-only 6,294、dG-only 93、both 907。
- 多链分隔符：`Ag_Seq` 有 1,443 行用 `/` 分隔多链，按顺序全部入库。inventory 的"多链分隔符"提示即此处。
- 各阶段：adapt 8,416 records / 40,384 rejects（36,183 `no_antigen_sequence` + 4,201 `no_observation`）→ ab 4,855 键（4,849 ok，6 `unresolved`）→ ag 3,105 键 → assemble 8,410 pair。
- observation：Kd 有值产出 Kd；Kd 空时产出 ΔG；`Predicted_or_Not` 写进 lineage。
- 单源 merge：`n_pairs=8,410, n_3a=6,067, sum len(affinity)=8,410`，断言全过。
- 过半码复查：`no_antigen_sequence` 74.2%。inventory 明记 48,800 行中只有 12,617 行有 `Ag_Seq`、36,183 行缺失，与实测 36,183 完全一致。没有抗原序列就不是 pair，条件成立，接受。
- `no_domain` / `unresolved` 合计 6 条（0.01%），无需第二个工具。

### R11 AbBiBench — 完成

- 数据：17 张 `binding_affinity` 表合计 215,699 行，与 inventory 完全一致。
- 决策文件 `etl/decisions/R11.yaml`：2 条 claim，`verify_decisions` 通过。抗原由 `metadata.json` 的 `pdb_path` + `antigen_chains` 从随包 PDB 重建。
- 两处源数据出入（已处理，不影响口径）：metadata 的路径带 `data/` 前缀、`1mhp` 与 `1mlc_LC` 两张表实际不存在（inventory 已记录 1mhp 的同类问题）；`AAYL50_bca.pdb` 文件名大写而 metadata 小写；`3gbn` 的链 A 是非蛋白实体，全长序列为空，剔除后抗原仍是链 B。
- 各阶段：adapt 215,699 records / 2 个表级 reject（文件缺失）→ ab 148,792 键全 ok（与 inventory 的 Unique 一致）→ ag 12 键（12 个 reference complex）→ assemble 215,699 pair、0 reject。
- 单源 merge：`n_pairs=215,699, n_3a=148,792, sum len(affinity)=215,699`，断言全过。`pair - 3A = 66,907` 是同抗体对不同抗原表的重复三元组。
- 抗原唯一序列 11 条（inventory 记 9 条，差异来自 3gbn 链 A 剔除前后的口径与 inventory 的统计方式不同；不影响 pair 产出）。

### R16 GUEST — 完成

- 数据：`antibody_antigen_affinities.txt` 42 行、`antibody_antigen_cases.txt` 68 行、194 个随包 PDB。与 inventory 一致。
- 抗体与抗原都由随包 PDB 重建；`Antibody PDB` 后缀里的 `H` / `L` 字母直接给链型（`3G6A_LH` 是 L 在前）；`Antigen PDB` 的 `(n)` 后缀是 case 内编号，剥掉。
- 各阶段：adapt 42 records / 0 rejects → ab 42 键全 ok → ag 39 键（38 ok，1 `placeholder`）→ assemble 41 pair。
- 唯一排除：一个抗原链的全长序列为空（非蛋白实体），按 `placeholder` 排除。
- 只产出 `Kd (nM)`，`ΔG (kcal/mol)` 不产出，符合 plan 的额外核对。
- 单源 merge：`n_pairs=41, n_3a=41`，断言全过。

### R20 SAbDab / SAbDab2 — 完成（资源适配器，不产 3A）

- `sabdab2_summary.csv` 22,264 行、11,604 个 PDB；`sabdab_search_structures_*.tar` 内 11,604 条 `full_structures/pdb_<8位>_sabdab.cif.gz`。
- 对外接口：`r20.index()`、`r20.structure_path(pdb)`（解到 `/data_new/ywy/cache/rcsb/` 并 gzip 展开）、`r20.open_structure(pdb)`（本地优先，未收录退回 RCSB）。
- 成员名是补零到八位的小写 PDB ID，不是数值编码。
- 抽查 3 个结构 ID：`10BT`（16 链）、`1AHW`（6 链）、`3HFM`（3 链），全部解析成功。
- 本 SRC 不产出 pair / 3A。

### 共享模块改动汇总

1. `vdomain.Hints` 新增 `single_chain`（R80 引入），附 `test_vdomain.py` 覆盖。
2. `check.py` 的 adapt 对账区分行级与表级 reject；`run_src.py` 传递 adapter 声明的 `SOURCE_ROWS`。
3. 依赖：新增 `openpyxl==3.1.5`（R13 / R16 的 xlsx）。
