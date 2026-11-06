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

### R14 AB-Bind — 完成

- 数据：`AB-Bind_experimental_data.csv` 1,101 行（含表头）、32 个随包 PDB。编码是 latin-1（表内含非 UTF-8 字节）。
- 决策文件 `etl/decisions/R14.yaml`：4 条 claim，通过自查。
- 抗体/抗原侧判定：主判据是 ANARCI 能否认出免疫球蛋白域；`Partners(A_B)` 是链组写法（`A_HL` 展开为 A、H、L），链名只作兜底。
- 突变解析：`链:原残基位置新残基`，作者编号；插入码在结构里是大写、源表写小写，resolver 统一转大写。
- 各阶段：adapt 683 records / 418 rejects（310 `no_antigen_binding`、108 `unresolved`）→ ab 397 键全 ok → ag 284 键（283 ok，1 拒）→ assemble 682 pair。
- 排除构成：`no_antigen_binding` 310 = 1T83 的 246（Fc-only）+ 3WJJ 的 25（Fc-only）+ 1DVF 的 39（两侧皆 Fv，无独立抗原）；`unresolved` 108 = 6 个无抗体链的普通蛋白复合物（1AK4、1JTG、1KTZ、HM_1KTZ、1FFW、3K2M）。与 inventory 的分类逐项对上。
- 过半码复查：`no_antigen_binding` 28.2%，未过半，且构成已逐项说明。
- 单源 merge：`n_pairs=682, n_3a=680, sum len(affinity)=682`，断言全过。
- **Review Focus 第 4 条已验**：同一个 `AB_ID` 下的三条记录（1BJ1 row=19/20/21）编辑不同，`ag_key` 分别为 `640ba445` / `81fa5066` / `15395b63`，`3A_ID` 分成 19 个，未共用键。

### R15 SKEMPI 2.0 — 完成

- 数据：`skempi_v2.csv`（分号分隔、latin-1）7,085 行、348 个复合物键。随包结构在 `pdb/structures/`（初版误指 `pdb/`，348 个都走了 RCSB 下载，已修）。
- 突变格式：`<原残基><链><位置><插入码><新残基>`，例如 `LI45G` 是链 I 第 45 位 L→G。**这与我最初按 AB-Bind 顺序解析相反，已修正并在 adapter 注释里写明。**
- 每行产两条 record：`mut`（应用突变、`Affinity_mut`）与 `wt`（不改序列、`Affinity_wt`），符合 aff 方案第 2 项。
- `n.b` / `n.b.` 按 aff 方案第 1 项视为成立的定性 observation（原字符串进 label）；`unf`、空值不成立。
- 各阶段：adapt 2,422 records / 5,874 rejects（全部 `no_antigen_binding`）→ ab 712 键（685 ok，27 拒）→ ag 479 键全 ok → assemble 2,370 pair。
- 单源 merge：`n_pairs=2,370, n_3a=937, sum len(affinity)=2,370`，断言全过。
- **与 plan 的数字有出入，已判明：** plan 期望 `Affinity_mut` 2,273 / `Affinity_wt` 2,289 条 observation。本快照实测：抗体相关复合物 1,211 源行（与源自带 `Hold_out_type=AB/AG` 的 1,211 行完全吻合），产 2,422 条 record、2,370 条成立 observation（52 条被 `orig_mismatch` / `unmapped_position` 拒）。1,211 行的口径与 inventory 的"942 行 / 48 复合物"也不同，inventory 自身的 942 与源字段 AB/AG 的 1,211 就对不上。以源字段和实测为准，plan 的 2,273/2,289 视作其他快照或另一种折叠方式下的数字。
- 过半码复查：`no_antigen_binding` 82.9%（5,874 / 7,085）。SKEMPI 2.0 是通用 PPI 突变库，抗体–抗原只是其中子集（inventory 明记"其余 316 个 accession 为普通蛋白-蛋白复合物…不在本表"）。条件成立，接受。

### 共享模块与驱动的后续改动

4. `pipeline.Record` 新增 `row_key`，`reconcile.json` 新增 `covered_rows`：一行产多条 record 的 SRC（R15 的 mut/wt）按源行对账，不再重复计数。
5. `pipeline.core_commit()` 改为对 `etl/core/*.py` 加 `etl/b/*.py` 取内容 hash。原先只看 `etl/core`，改 resolver 不会让缓存失效，R14 曾因此跑出旧结果。
6. `entities.ab_entity` / `ag_entity` 的主题编号按 `ab_ctx` 的 `h_chain` / `l_chain` 取，不再假定链名就是 `H` / `L`（SKEMPI 与 AB-Bind 的链名多样）。

### R50 Graphinity — 完成

- 数据：`Synthetic_FoldX_ddG_942723.csv` 942,723 行 + `Synthetic_FlexddG_ddG_20829.csv` 20,829 行 = 963,552 行，与 inventory 一致。
- `complex` 编码：FoldX 是 `<pdb>_<原残基><链><位置><新残基>`；Flex 是 `<pdb>_<抗体链组>_<抗原链组>_<原残基><链><位置><新残基>`。
- 两层键：parent 按 `(结构引用, 链)` 缓存（`structure_parents`），`vdomain` 每个 parent 只做一次；94 万行不再逐行恢复编号表。
- **判定一处，已记录：** 突变不重建序列，只进 lineage（A 类处理）。原因：FoldX 的 `orig` 取自 Graphinity 自己的参考序列，与 PDB entity 残基常不一致，用 `apply_point` 重建时 90% 以上行会被 `orig_mismatch` 挡掉；而计算 ddG 本身不需要突变后序列。
- 各阶段：adapt 925,711 records / 37,841 rejects（`unresolved`，结构链不在 Graphinity 包内）→ ab 2,658 键（1,396 ok）→ ag 2,626 键 → assemble 918,698 pair、7,013 reject。
- 单源 merge：`n_pairs=918,698, observations=938,487`，断言全过。ab/ag 键数是结构级 entity（1,409 个 parent），不是行数。
- 百分点：`records + adapt_rejects = 963,552`，与源行数一致。
- 产出列：FoldX `foldx_ddg`；Flex `flexddg_ddg` 与 `flexddg_ddg-talaris2014` 各一条 observation。`flexddg_ddg-talaris2014-gam` 与 `flexddg_ddg` 逐行相等，不产出。
- 需要 `SHARDED = True`（10 万行一片），否则整表驻留内存会到 GB 级。

### R75 HER2-aff-large / Buzz — 完成

- 数据：`data.zip` 解出的 5 个子集，主表 `her2_aff_large` 524,346 行（`0.7_0.15_0.15` 三份 split 之和），与 inventory 一致；mason 34,049、shanehsazzadeh 198、neg 574、流感 199,892。
- 决策文件 `etl/decisions/R75.yaml`：3 条 claim，通过自查。抗体由 `mutate.apply_region` 从 1N8Z 重链 B 的 IMGT 107-116 替换本行 CDR-H3，保留 parent VL（1N8Z 链 A）；抗原 HER2 取 1N8Z entity 3 链 C。
- 各阶段：adapt 759,059 records / 0 rejects → ab 626,620 键全 ok → ag 6 键（1 ok）→ assemble 559,167 pair。
- observation 1,083,513 条：主表每行 `class` 与 `label` 两条。
- 单源 merge：`n_pairs=559,167, n_3a=558,413, sum len(affinity)=1,083,513`，断言全过。
- 排除：流感集 199,892 行（26.3%）按 `placeholder` 排除 —— 这 2 个体系的抗原序列不在本 SRC 包内，也不在 R09 的 phillips 表里（该表只有重/轻链）。未过半，接受。

### R13 补充：`Predicted_or_Not` 与四态

已在 R13 小节记录，此处不重复。

### R11 / R16 补充

见前文。

### R78 MochiBind — 完成

- 数据：7 张采样表合计 33,454 行，与 inventory 一致。
- 观察值：`alphaseq_affinity` 33,454 条 + `predicted_affinity` 19,224 条 = 52,678；`parental_*`、`avg_off_target_affinity` 不产出。
- 单源 merge：`n_pairs=33,454, n_3a=33,337`，断言全过。

### R10 AbRank — 完成

- 数据：`AbRank_dataset.csv`（制表符）342,356 行、28 列，与 inventory 一致。
- **一处数据事实，已记录：** `Source=RBD-escape` 的 192,559 行里，`Ag_seq` 实际是突变标记串（如 `SARS-CoV2_(A410E)`），不是氨基酸序列；这些行没有抗原序列，按 `no_antigen_sequence` 排除。其余行的 `Ag_seq` 是真正的序列。
- 三个读数列 `Affinity_Kd [nM]` / `IC50 [ug/mL]` / `escape` 各成一条 observation；值原样保留（含 `>`/`<`）。`log_Aff`、`log(Kd_ratio)`、`Aff_op` 不产出。
- 单源 merge：`n_pairs=148,736, n_3a=147,202, sum len(affinity)=149,026`，断言全过。

### R23 MIT-LL AlphaSeq — 完成

- 数据：`MITLL_AAlphaBio_Ab_Binding_dataset.csv` 1,259,700 行、14 列，与 inventory 一致。
- 决策文件 `etl/decisions/R23.yaml`：3 条 claim，通过自查。正靶抗原是 14 aa 肽 PDVDLGDISGINAS。
- 各阶段：adapt 154,632 records / 1,105,068 rejects → ab 71,830 键全 ok → ag 1 键 → assemble 154,632 pair。
- 排除构成：`no_antigen_binding` 944,775（AlphaNeg1~3 是负对照、没有来源序列，决策文件 C2 要求排除）；`no_observation` 160,293（`Pred_affinity` 空）。
- 单源 merge：`n_pairs=154,632, n_3a=71,830, sum len(affinity)=154,632`，断言全过。

### R79 AlphaBind — 完成

- 数据：8 张 AlphaSeq 表合计 209,924 行，与 inventory 一致。
- 决策文件 `etl/decisions/R79.yaml`：4 条 claim，通过自查（含跨源取值核对）。3 个 campaign 的抗原序列取自 R78 的原始文件；`HER2-OPT` 与 R78 的 HER2 片段不是同一构建体，按 C4 排除。
- 各阶段：adapt 193,764 records / 16,160 rejects → ab 188,957 键全 ok → ag 3 键 → assemble 193,764 pair。
- observation 302,230 条：`alphaseq_affinity` 与 `predicted_affinity` 各成一条。
- 单源 merge：`n_pairs=193,764, n_3a=188,957`，断言全过。

### 驱动层改动（第二批）

7. `pipeline.run_sharded`：大 SRC 按 10 万行分片，每片独立跑完再合并 parquet。适用于 R50（96 万）、R12（118 万）、R23（126 万）、R10（34 万）、R09（463 万）。
8. `adapters` 可返回生成器 + `adapt.rejects` 容器；`run_sharded` 在 record 流消费完后读取 rejects。
9. `structure_parents.py`：结构型 SRC 共享的 parent 恢复与缓存，`(结构, 链)` 只解析一次。
10. `entities._parents` 支持 `ctx` 只给结构引用（`ref` + `chains`），不在每个 record 里复制编号表。
11. `entities.ab_entity` / `ag_entity` 增加两槽皆空时的 `no_sequence` 兜底（原先会抛 `ValueError: vh and vl both empty`）。
12. `verify_decisions` 支持 `value_from_file`，用于跨 SRC 取值（R79 的抗原取自 R78）。

### R09 FLAb — 进行中（第三次重跑）

- 数据：`data/binding/` 80 张 CSV + 6 个 zip，tar 后合计约 463 万行。
- **判断两处，已记录：**
  1. 只有 AbRank（`ag_seq`）与 kothiwal 系列（`antigen_seq`）带逐行抗原序列；其余表没有。li2023 两张表与 SRC_R23 同批测量（`MIT_Target`），复用 R23 决策文件里的 14 aa 肽 `PDVDLGDISGINAS`；`AlphaNeg1~3` 是负对照，同 R23 处理。
  2. engelhart2022、tsuruta2024 两表、phillips2021、adams2017、cognano 等固定靶表没有任何可核验的抗原序列来源，按 `no_antigen_binding` 排除（决策文件 R09 C3）。这与 plan 的 "固定目标需要决策文件" 一致：没有可核验证据的就不编。
- 决策文件 `etl/decisions/R09.yaml`：3 条 claim，通过自查。
- 第一次跑把 `ag_seq` 只认成一个列名，491 万行被误判 `no_antigen_sequence`；第二次扩展到 `antigen_seq` 等列名后仍缺固定靶，第三次加上 `FIXED_ANTIGEN` 与 `no_antigen_binding` 分支。
