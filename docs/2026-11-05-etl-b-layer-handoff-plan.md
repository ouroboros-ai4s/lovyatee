# ETL B 层 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 3x5090 的 `etl-b-layer` 分支上，对 20 个 SRC 逐个写 adapter 与跑数脚本，用 A 层共享模块得到各 SRC 的 `pair` 表，最后跑 `merge` 产出 `3a` shards。

**Architecture:** 每个 SRC 一条垂直切片：`adapt → ab → ag → assemble`，输出符合 `merge.PAIR_SCHEMA` 的 Parquet；`merge` 在最后全局运行一次。本计划只定边界、顺序、完成判据和需要停下来问的情形，其余（目录结构、缓存、编排、对账工具、决策文件的取证方式）由执行者对照实际数据决定。这份文件按 handoff 的形式写：给出现状、已验证与未验证的事实、引用路径，不复制设计文档。

**Tech Stack:** 与 A 层相同：Python 3.12.3、Daft 0.7.26、DuckDB 2.0.0、pyarrow 25.0.1、gemmi 0.7.5、ANARCI 2026.2.13.2 + HMMER 3.4、uv 0.13.7、pytest 9.2.0。

**Spec:** `context/2026-11-04-3a-src-data-etl-blueprint.md`（§1 分工与原则、§3 AI 接缝、§4 中间表、§6 SRC 映射、§8 验收）；A 层 plan `docs/2026-11-05-etl-a-layer-dev-plan.md`；A 层合入 main 之后的 `etl/handoff.md` 与 `etl/core/*.md`；各 SRC 的 inventory 在 `context/2026-10-30-3a-src-inventory/`；设计文档在 `context/2026-10-28-ab-ag-data-diversity/`。

## 交接说明

- **现状（2026-11-05）：** A 层 plan 已写好，尚未执行；`etl/` 目前不在 `main`。B 层必须等 A 层分支 `etl-a-layer` 由 Pthahnix 合入 `origin/main` 后才能开工。
- **已验证（来自 blueprint §5 与 A 层 plan 编写时的实测）：** host 环境与路径；Daft 批量 UDF 调 ANARCI 在 `use_process=True`、`batch_size=500` 下约 1,397 条/秒；ANARCI 32 进程约 1,967 条/秒；`files.rcsb.org` 与 `data.rcsb.org` 经 mihomo 可达，`3RVV` 撤销后对应 `5VPL`；`/data_new/ywy/dataset-abag/` 下 20 个 SRC 目录均存在（名称见各任务表）。
- **未验证，开工后自行核对：**
  - A 层代码的实际签名，以 `etl/core/*.md` 为准，与 A 层 plan 不一致时以代码为准。
  - 各 SRC 的实际列名、行数与 inventory 是否一致，不一致处记入 `etl/progress.md`。
  - `vdomain` 在 R08、R74、R76 上的 `no_domain` 占比，A 层 Task 5 会把实测值写进 `etl/core/vdomain.md`。
  - R23、R79 等需要决策文件的 SRC 能否找到可核验的来源。
- **建议的 skill：** `superpowers:executing-plans`（或 `superpowers:subagent-driven-development`）；对账不平时用 `superpowers:systematic-debugging`；每个切片收尾前用 `superpowers:verification-before-completion`。
- **不含任何密钥。** mihomo 订阅链接与 GitHub token 只在 host 的 600 权限文件里，不入库，不要写进任何提交。

## Global Constraints

- **前提检查：** `ssh 3x5090 'cd /data_new/ywy/LOVYATEE && git fetch origin && git log --oneline origin/main -- etl/core/merge.py'` 有输出，并且 `source etl/env.sh && pytest etl` 全过；否则停下，告知 Pthahnix。
- **只在远程做。** 全部工作在 `ssh 3x5090` 的 `/data_new/ywy/LOVYATEE`，分支 `etl-b-layer`（从 `origin/main` 切出）。本地 `D:\LOVYATEE` 不做任何写操作；文件用 `ssh 3x5090 'cat > path' <<'EOF'` 写入。只在 `etl-b-layer` 提交，不动 `main`，全部完成后 push 该分支，由 Pthahnix 亲自 merge。每个 SRC 一次提交，信息形如 `feat(etl-b): <SRC> adapter and run`，末尾加当前会话规定的署名行。
- **命令简写：** `[host] <cmd>` 表示 `ssh 3x5090 'cd /data_new/ywy/LOVYATEE && source etl/env.sh && <cmd>'`。
- **范围：** 20 个 SRC：R03 R08 R09 R10 R11 R12 R13 R14 R15 R16 R20 R23 R50 R74 R75 R76 R77 R78 R79 R80。R20 不产生 `3A`，只作为 `structref` 的资源适配器。
- **输出位置：** 代码、`decisions/<SRC>.yaml`（含网页快照）、`etl/progress.md` 进仓库；所有 Parquet、日志、缓存都在仓库之外，各 SRC 的中间产物放 `/data_new/ywy/etl_out/<SRC>/`，最终结果放 `/data_new/ywy/etl_out/final/`，外部结构缓存 `/data_new/ywy/cache/rcsb/`。不提交 Parquet。不写根分区；`/data_new/ywy/abag_final` 与 `/data_new/ywy/_tmp_paircalc` 不是本任务的，不碰；刻意保持压缩的数据集不解包。
- **adapter 薄：** 只把源行搬成 record，值保持源的原样，`None` 只用于源为空或占位的字段；不清洗序列，不推断生物学含义。清洗只在 `etl/core/` 的共享模块里出现一次。
- **共享模块无 SRC 特例。** 发现 A 层模块缺陷可以直接修，不加按 SRC 的分支，在 `etl/progress.md` 记一行并重跑受影响的 SRC。
- **不写一个适配 20 个 SRC 的通用脚本，不建重型 RULE 表。**
- **以产出为目标：** 排除码（`no_domain`、`slot_collision`、`mutation_unassigned`、`no_antigen_binding` 等）是默认处置。某个原因码命中一个 SRC 过半记录时，视为该条件与此 SRC 的实际数据不符：现场调整处理方式，把调整写进 lineage 与 `etl/progress.md`，不让条件把整个 SRC 挡掉。
- **affinity 五元组不改：** `(label, assay, condition, replicate, lineage[])`；`label` 不为 `None`；额外信息只进 lineage。observation 的取舍按 `3a_src_data_etl_problem_aff.md` 第 1–7 项，全部在 adapter 内的单行范围完成，不去重。
- **ID 与 lineage：** 公式与语法见 A 层 plan Global Constraints，直接调用 `etl.core.ids` 与 `etl.core.lineage`，不自己拼。
- **AI 接缝：** AI 只产出带证据的 `decisions/<SRC>.yaml`；论断写入前自查：引用的 `file` 或 `snapshot_file` 存在，`quote` 逐字出现，`value` 中的序列在引用的 FASTA 或结构 entity 中逐字出现；自查不过的论断不入库。运行期只读决策文件，不联网，不调用 AI。网页证据存快照文件，经 mihomo（`ETL_PROXY`）取得。
- **缓存键：** 覆盖输入内容 hash、`etl/core` 的 git commit、规则版本、决策文件 hash、外部结构快照 hash，键不变则跳过，键写在产物旁的 `.key`。`evidence` 进键，只写 lineage 的 `notes` 不进键。
- **资源：** 并行 worker 以 32 为上限；超过一分钟的任务用 `setsid nohup <cmd> > <log> 2>&1 &` 启动并读日志；SSH 偶发断开时先重试。
- **自己维护 `etl/progress.md`：** 每个 SRC 一段，记状态、关键数字、与 inventory 不符之处、对共享模块的修改、遗留问题，供跨上下文续作。
- **停下来问 Pthahnix 的情形：** 共享模块无法表达某个 SRC 的需求；需要改 affinity 五元组或 ID 公式；源数据与 inventory 的出入改变了 SRC 的范围；打算整体放弃一个 SRC。其余自行判断。

## Review Focus

1. 某个排除原因码命中一个 SRC 过半记录。（每个切片的完成判据都含"按原因码统计排除占比"）
2. adapter 在搬运时已经改动了值（去空白、改大小写、吞占位符），使 `seqnorm` 和 `ids` 看不到源的原样。（每个切片抽 3 条 record，`raw_ab` 与 `raw_ag` 的值须与源单元格逐字一致）
3. 一行多个读数的 SRC 把派生值或不属于本 pair 的量当成 observation，或漏掉独立读数。（R09、R10、R15、R50、R75、R79 的 observation 数须与 aff 方案第 2 项的产出表一致）
4. `evidence` 漏掉影响清洗的字段（来源边界、待应用的编辑、决策文件 claim ID），使两条不同记录共用同一个 `ab_key` 或 `ag_key`。（R14、R15、R50 的切片检查：编辑不同的两条 record 的键不同）
5. 长任务被 SSH 断线打断后，重跑得到不同的结果或半成品。（至少在一个大 SRC 上验证：杀掉进程后重跑，`.key` 命中的阶段被跳过，最终 ID 集合不变）

---

## 切片完成判据（每个 SRC 都适用）

以下是每个切片收尾时必须成立的事，做法由执行者决定：

1. **adapt 对账：** 源行数 = 产出 record 数 + `reject_log` 中该 SRC 的 adapt 行数；record 数可以大于行数（R15 的 `mut`/`wt`）。
2. **ab、ag 对账：** distinct 键数 = ok 实体数 + reject 实体数。
3. **assemble 对账：** record 数 = pair 数 + reject 数。
4. **单源 `merge`：** 对该 SRC 的 `pair` 表跑一次 `merge` 到 `/data_new/ywy/etl_out/<SRC>/merge_check/`，其断言全过，`Σ len(affinity)` 等于成立 observation 总数。
5. **排除占比：** 按 `reason_code` 列出占比；过半的原因码先复查条件（Global Constraints 的"以产出为目标"），结论写入 `etl/progress.md`。
6. **抽查：** 随机抽 3 条 `3A`，沿 lineage 回到源文件的行，核对序列、裁剪边界和 observation 的 `col=`；同时抽 3 条 record 核对 Review Focus 第 2 条。
7. **提交：** adapter、run 脚本、决策文件（含快照）、`etl/progress.md` 一次提交。

---

### Task 1: 开工准备

**Files:**
- Create: `etl/progress.md`

**Interfaces:**
- Consumes: A 层的全部产物（`etl/handoff.md`、`etl/core/*.md`、`merge.PAIR_SCHEMA`、`merge.REJECT_SCHEMA`）。
- Produces: 分支 `etl-b-layer`；`/data_new/ywy/etl_out/`；记录了 base commit 的 `etl/progress.md`。

- [ ] **Step 1: 前提检查**：见 Global Constraints 第一条。失败则停下并回报，不要自行修 A 层。
- [ ] **Step 2: 建分支**：`ssh 3x5090 'cd /data_new/ywy/LOVYATEE && git switch -c etl-b-layer origin/main'`。
- [ ] **Step 3: 通读** `etl/handoff.md`、blueprint §4、§6、§8，以及每个 `etl/core/<模块>.md` 的"接口"和"示例"。
- [ ] **Step 4: 建输出根目录并写 `etl/progress.md` 的开头**：日期、base commit、`pytest etl` 通过数、A 层 `vdomain.md` 中记录的 `no_domain` 实测占比。
- [ ] **Step 5: Commit**：`[host] git add etl/progress.md && git commit -m "feat(etl-b): start B layer"`。

---

### Task 2: 切片 R76（贯穿全部阶段的第一个 SRC）

**SRC：** `SRC_R76_TDC_ANTIBODYAFF` | inventory：`src-76-tdc-antibodyaff-inventory.md`

**Files:**
- Create: R76 的 adapter、run 脚本（位置自定，建议 `etl/adapters/`）

**Interfaces:**
- Consumes: `seqnorm.normalize`、`vdomain.pair_slots`、`antigen_bound.bound`、`structref.open_structure`、`ids.ab_id/ag_id/three_a_id`、`lineage.locator/kv/step`、`merge.merge`。
- Produces: `/data_new/ywy/etl_out/R76/` 下符合 `merge.PAIR_SCHEMA` 的 `pair` Parquet、`reject_log`。

这一步定下后面所有 SRC 沿用的做法（目录结构、阶段脚本形态、缓存键、对账方式），按你的判断来，但要在 `etl/progress.md` 写清楚，后面的切片复用。

业务提示（blueprint §6）：`X1` 是列表字符串（重、轻链），`X2` 是抗原序列，`Y` 无单位描述，lineage 写 `col=Y`；21 行 H/L 槽规范化后相同（其中 15 行含 `GGGGSGGGGSGGGGS`），走 `pair_slots`；恒定区由 `vdomain` 处理；`structure` 先只记录 PDB 指针，`3RVV`、`3RVW` 由 `structref` 解析为 `5VPL`、`5VPG` 并写入 lineage。

- [ ] **Step 1: 读** R76 的 inventory、README、抽样行，把与 inventory 的出入记入 `etl/progress.md`。
- [ ] **Step 2: 写 adapter 并跑通** `adapt → ab → ag → assemble`，在 distinct 键上计算。
- [ ] **Step 3: 完成判据 1–7。** 另须满足：493 行对应 476 个源内唯一 `(X1, X2)` pair；最终 `3A` 数与 476 的差额能被 `reject_log` 与 ID 合并解释；记录本 SRC 的 `no_domain` 占比，与 `vdomain.md` 的实测值比较。
- [ ] **Step 4: 回报 Pthahnix 并继续**：给出各阶段行数、排除原因码占比、`no_domain` 占比，以及对 `qa_sample` 每层数量的建议（blueprint §8：每层数量在第一个切片完成后确定）。除非 Pthahnix 叫停，不等回复，继续 Task 3。
- [ ] **Step 5: Commit。**

---

### Task 3: 切片 R77（验证跨源追加）

**SRC：** `SRC_R77_AKBAR_SABDAB_KD` | inventory：`src-77-akbar-sabdab-kd-csv-inventory.md`

**Interfaces:**
- Consumes: Task 2 沉淀的做法和 adapter 里可复用的部分（adapter 是 SRC 专属的，复用的是写法，不是共享模块）。
- Produces: R77 的 `pair` Parquet。

- [ ] **Step 1: 做 R77 切片**，完成判据 1–7。inventory 标 R77 为 R76 的同源快照，预期产出与 R76 相同的 `3A_ID` 集合。
- [ ] **Step 2: 对 R76 与 R77 一起跑 `merge`**（输出到 `/data_new/ywy/etl_out/R76_R77_check/`），核对：共有的 `3A_ID` 的 `affinity[]` 同时含两个 SRC 的 tuple，各 tuple 的 lineage 保留各自的定位；两边 `3A_ID` 集合的差异逐条查明原因并写入 `etl/progress.md`。
- [ ] **Step 3: Commit。**

---

### Task 4: 第一批其余切片（R08、R74、R03、R80）

每个 SRC 一次提交，完成判据 1–7 适用。表中"业务提示"取自 blueprint §6，具体怎么处理由执行者对照实际数据决定。

| SRC（目录） | inventory | 业务提示 | 额外核对 |
| --- | --- | --- | --- |
| R08 `SRC_R08_AVIDA_HTNFA` | `src-08-avida-htnfa-inventory.md` | 固定目标 TNF-alpha，有直接序列，需要一份决策文件说明抗原身份与来源；22 aa 信号肽、`6×His`、VHH；`corpus-hTNFa.csv` 无 label，不产生 observation | 抽样记录的 lineage 含信号肽与标签的裁剪记录；无 label 的行进 adapt 的 `reject_log` 而不是静默丢弃 |
| R74 `SRC_R74_ABDESIGN2` | `src-74-abdesign-2-0-inventory.md` | 576 条完整突变重链（A 类，突变名只入 lineage），末尾 `HHHHHH`，带恒定区；PD-1 由参考结构 5GGS 的 entity 3 重建，需要决策文件指明序列来源 | `kd` 缺失的行以 `binding` 为唯一 observation，有 `kd` 的行不再产出 `binding`；kon、koff、r2 不产出 |
| R03 `SRC_R03_ABDESIGN_DB` | `src-03-abdesign-1-0-inventory.md` | 逐行序列，附参考 PDB；完整重轻链（A 类，突变字段只入 lineage）；WT 与突变体两张表；`affinity_type` 长表 | `affinity_type=<取值>` 出现在 observation 的 lineage 里（`ddg`、`elisa_mut_to_wt_ratio`） |
| R80 `SRC_R80_ANTIPASTI` | `src-80-antipasti-inventory.md` | PDB 链恢复；VL-linker-VH 反向 scFv；VL-only；NA 与非蛋白抗原排除；linker 为结构里观察到的非标准 linker 时经 `Hints.linker` 传给 `vdomain` | 记录 `non_protein` 与 `unresolved` 的占比；`delta_g` 不产出 |

- [ ] **Step 1: 按表逐个完成 R08、R74、R03、R80 的切片。**
- [ ] **Step 2: 第一批收尾**：对已完成的 6 个 SRC（R76、R77、R08、R74、R03、R80）一起跑一次 `merge` 到 `/data_new/ywy/etl_out/batch1_check/`，更新 `etl/progress.md`，并回报 Pthahnix 各 SRC 的产出数与排除占比。

---

### Task 5: 第二批切片（R20、R14、R15、R50、R75、R13、R11、R16）

顺序按 blueprint §6：R14 首次用 `mutate.apply_point` 与编号映射；R15 加入 WT record 与双侧突变；R50 验证结构型 SRC 的两层键；R75 验证 `mutate.apply_region`。完成判据 1–7 适用，R20 例外。

| SRC（目录） | inventory | 业务提示 | 额外核对 |
| --- | --- | --- | --- |
| R20 `SRC_R20_SABDAB` | `src-20-sabdab-sabdab2-inventory.md` | 无 affinity，不是流水线 SRC；作为 `structref` 的资源适配器，不产生 `3A` | 在 progress.md 写明其他 SRC 如何通过它取得结构，抽 3 个结构 ID 能解析 |
| R14 `SRC_R14_ABBIND` | `src-14-ab-bind-inventory.md` | 亲本 PDB 实体，无逐行序列；突变落在抗体或抗原侧，先判所属；Fc-only 排除（`1T83`、`3WJJ`）；结构自带 `AB-Bind-Database/*.pdb` | Review Focus 第 4 条：两条编辑不同的 record 的 `ab_key` 不同；`mutation_unassigned` 的占比 |
| R15 `SRC_R15_SKEMPI2` | `src-15-skempi-2-0-inventory.md` | 每个源行产出 `mut` 与 `wt` 两条 record（`wt` 为空编辑表的 `point` 模式）；突变在任一侧；非抗体复合物排除；多链伙伴 | `Affinity_mut` 突变体侧 2,273 条、`Affinity_wt` WT 侧 2,289 条 observation 的数量与 aff 方案一致；WT 序列无法重建时只丢 WT observation |
| R50 `SRC_R50_GRAPHINITY` | `src-50-graphinity-inventory.md` | 4 张表：FoldX 942,723 行、Flex 20,829 行产出（每个 Flex 行 2 条 observation）；AB-Bind 645、SKEMPI 608 不产出；两层键：`(结构引用, 链)` 恢复 parent 与 `vdomain` 只做一次，再按编号映射应用点突变；作者归档是重编号快照；名称编码突变；VL-only；scFv；计算 ddG | 942,723 行来自 1,409 个 PDB，parent 恢复次数应与之同量级，不是行数；`flexddg_ddg-talaris2014-gam` 不产出；Review Focus 第 4 条 |
| R75 `SRC_R75_BUZZ` | `src-75-her2-aff-large-buzz-inventory.md` | HER2 固定目标，需要决策文件；CDR-only，经 `apply_region` 从 `1N8Z` 补全 VH 并保留 parent VL；流感集一行多抗原（CR6261 为 h1、h9，CR9114 为 h1、h3、fluB），每个抗原的 `*_mean` 一条 observation，分属不同 pair | 区间 IMGT 107–116 与 A 层 `mutate.md` 的实测一致；流感集 `*_label` 不产出 |
| R13 `SRC_R13_ANDD` | `src-13-andd-inventory.md` | 多链分隔符与缺失值；H/L 槽内的 scFv；恒定区 | `Predicted_or_Not` 取值写入 observation 的 lineage；有 Kd 的行不再产出 ΔG |
| R11 `SRC_R11_ABBIBENCH` | `src-11-abbibench-inventory.md` | 固定目标，由结构重建，需要决策文件；恒定区 | 重建出的抗原序列与决策文件引用的结构 entity 逐字一致 |
| R16 `SRC_R16_GUEST` | `src-16-guest-inventory.md` | PDB/FASTA 重建；`5C2B` 单链 scFv；`4NKI`、`5I30` 的来源标签与结构实体不一致，按 `antigen_bound` 的"来源优先、结构只记录不一致"处理 | 只产出 Kd，ΔG 不产出 |

- [ ] **Step 1: 按表完成 8 个 SRC。**
- [ ] **Step 2: 在 R50 或 R15 上验证 Review Focus 第 5 条**：杀掉运行中的进程后重跑，已命中 `.key` 的阶段被跳过，最终 `3A_ID` 集合与不中断的一次相同。
- [ ] **Step 3: 第二批收尾**：对前两批的 SRC 一起跑一次 `merge` 到 `/data_new/ywy/etl_out/batch2_check/`，更新 `etl/progress.md`，回报 Pthahnix。

---

### Task 6: 第三批切片（R79、R23、R78、R10、R09、R12）

顺序按 todo。这一批规模大，`ab`、`ag` 阶段必须按 distinct 键处理，不对逐行序列整体跑 `vdomain`。规模参照：R09 约 460 万行（li2023 两张表 1,259,700 与 1,903,927 行），R23 1,259,700 行。

| SRC（目录） | inventory | 业务提示 | 额外核对 |
| --- | --- | --- | --- |
| R79 `SRC_R79_ALPHABIND` | `src-79-alphabind-inventory.md` | 活动级固定构建体，无随包序列；抗原序列取自 R78 的原始文件（R78 是 R79 各 campaign 的 5k 采样，`antigen` 列带直接序列）；对应关系由执行者联网核验并写进决策文件，对不上的 campaign（如 HER2-OPT 与 R78 的 HER2 120 aa 片段）的行按 `no_antigen_binding` 排除 | `alphaseq_affinity` 与 `predicted_affinity` 各成 observation；`parental_*`、`avg_off_target_affinity` 不产出；决策文件不引用任何 SRC 的处理结果 |
| R23 `SRC_R23_ALPHASEQ` | `src-23-mit-ll-alphaseq-inventory.md` | 固定 14 aa 肽靶；4 个 Target（`MIT_Target`、`AlphaNeg1~3`，各 314,925 行），按 `applies_to` 各给 claim；没有来源序列的 Target，其行按 `no_antigen_binding` 排除；scFv（VH-GGGGSGGGGSGGGGS-VL）；唯一读数是 `Pred_affinity` | 每个 Target 一条 claim 的证据可逐字核验；`no_antigen_binding` 的占比 |
| R78 `SRC_R78_MOCHIBIND` | `src-78-mochibind-sampled-data-inventory.md` | 4 个固定抗原构建体，有直接序列；scFv | 抗原序列与 R79 决策文件中引用的 R78 原始序列逐字一致 |
| R10 `SRC_R10_ABRANK` | `src-10-abrank-inventory.md` | 逐行序列，PDB 锚点；突变主要描述抗原逃逸；`IC50`、`Affinity_Kd`、`escape` 三个读数列，部分行多列并存，值保持字符串原样（含 `>`） | AbCoV 的 293 行 IC50 与 Kd 并存各成 observation；RBD-escape 的 20,500 行 Kd 与 `escape` 并存各成 observation；`Aff_op`、`log_Aff` 等不产出 |
| R09 `SRC_R09_FLAB` | `src-09-flab-inventory.md` | 86 张表；固定目标与 AbRank 序列混合，固定目标需要决策文件；scFv；突变；kothiwal 的 SPR KD 与 Cell Display EC50 是两个独立读数 | `Pred_affinity` 列（li2023、engelhart2022）写入 lineage；`fitness`、取对数与单位换算列不产出 |
| R12 `SRC_R12_ASD` | `src-12-asd-agab-db-inventory.md` | 逐行序列；长表 `affinity_type`（16 种取值）；`scfv.csv` 中完整单链与 754 条独立 H/L 混合；非抗体链 | `affinity_type=<取值>` 进 lineage；`delta_g`（2,725 条计算 ΔG）保留并以 lineage 标明；`processed_measurement` 不产出 |

- [ ] **Step 1: 按表完成 6 个 SRC。** 需要决策文件的，先取证、自查、入库，再跑。
- [ ] **Step 2: 第三批收尾**：更新 `etl/progress.md`，回报 Pthahnix 各 SRC 的产出数、排除占比和决策文件清单。

---

### Task 7: 全局 merge、验收、提交

**Files:**
- Modify: `etl/progress.md`

**Interfaces:**
- Consumes: 全部 SRC 的 `pair` Parquet 与 `reject_log`。
- Produces: `/data_new/ywy/etl_out/final/` 下的 `3a/`、`stats/`、`qa_sample.parquet`、`reject_log.parquet`、`manifest.json`。

- [ ] **Step 1: 全局 merge**：`merge(pair_glob=<全部 SRC>, out_dir=/data_new/ywy/etl_out/final, reject_glob=<全部 SRC 的 reject_log>, qa_per_stratum=<Task 2 回报时建议的数量>, decision_files=<全部决策文件>)`。
- [ ] **Step 2: 验收（blueprint §8）**：
  - 对账：`Σ len(affinity[])` 等于全部 pair 的成立 observation 总数；pair 数与 `3A` 数的差额等于相同 `3A_ID` 的合并数。
  - 同一 `AB_ID`、`AG_ID`、`3A_ID` 只对应一个 canonical 字符串（`merge` 已断言，确认它没有被绕过）。
  - 排除占比：按原因码逐个 SRC 列表；过半者已按 Global Constraints 复查并有结论。
  - 工具覆盖：R08、R74、R76 的 `no_domain` 占比，并写出是否需要引入第二个工具的结论（blueprint §3 的判据：某 SRC 无来源边界且 `no_domain` 占比不可接受）。
  - R76 的 476 差额、R77 对 R76 的差异已在 `etl/progress.md` 有解释。
- [ ] **Step 3: 复现**：对同一输入再跑一次 `merge` 到 `/data_new/ywy/etl_out/final_rerun/`，`3a/*.parquet` 与 `manifest.json` 逐字节相同。
- [ ] **Step 4: 人工抽查**：从 `qa_sample` 的每层各取若干条，核对 `3A_ID`、VH/VL/VHH、抗原片段和结构链映射；结果与取样数量写入 `etl/progress.md`。
- [ ] **Step 5: Commit 并 push 分支**：

```bash
[host] git add etl && git commit -m "feat(etl-b): final merge and acceptance"
ssh 3x5090 'cd /data_new/ywy/LOVYATEE && git push -u origin etl-b-layer'
```
Expected: push 输出含 `etl-b-layer -> etl-b-layer`。

- [ ] **Step 6: 回报**：分支名、`3A` 总数、各 SRC 的产出与排除占比、最终结果的路径 `/data_new/ywy/etl_out/final/`、对共享模块做过的修改、遗留问题；然后等待 Pthahnix 亲自 merge。
