---
tags:
  - design
---

# Data ETL Pipeline Blueprint

- [Data ETL Pipeline Blueprint](#data-etl-pipeline-blueprint)
  - [lineage](#lineage)
  - [1. 总体结构](#1-总体结构)
    - [1.1 分工](#11-分工)
    - [1.2 原则与数据流](#12-原则与数据流)
  - [2. 台账](#2-台账)
    - [2.1 重叠，合并为共享模块](#21-重叠合并为共享模块)
    - [2.2 冲突，裁决](#22-冲突裁决)
    - [2.3 缺口，默认处理](#23-缺口默认处理)
  - [3. 模块](#3-模块)
    - [AI 接缝](#ai-接缝)
  - [4. 中间表与运行输出](#4-中间表与运行输出)
  - [5. 运行环境与执行模型](#5-运行环境与执行模型)
    - [5.1 运行环境](#51-运行环境)
    - [5.2 技术栈](#52-技术栈)
    - [5.3 执行模型](#53-执行模型)
  - [6. SRC 映射与实施顺序](#6-src-映射与实施顺序)
  - [7. 交付物与交接](#7-交付物与交接)
    - [7.1 etl 目录](#71-etl-目录)
    - [7.2 handoff.md](#72-handoffmd)
    - [7.3 A 层开发顺序](#73-a-层开发顺序)
  - [8. 验收](#8-验收)

## lineage

- [[3a_src_data_etl_modeling]]: 3A model that the pipeline outputs.
- [[3a_src_data_etl_problem_ab]]: antibody-side algorithms, items 1-12.
- [[3a_src_data_etl_problem_ag]]: antigen-side algorithms, items 1-8.
- [[3a_src_data_etl_hash]]: ID scheme, authoritative for serialization.
- [[3a_src_data_etl_problem_aff]]: affinity observation rules, items 1-7.
- [[agent_compiles_declarations_the_core_executes]]: agent output enters a run only as structured declarations.

本设计文件针对的是 [[2026-11-01-20-src-data-etl-todo-list]] 中的 `## 2. Data ETL SRC-by-SRC` 和 `## 3. Data ETL Merge`，把 `## 1. Data ETL Specification` 的各项方案整合为可以直接实现的模块化流水线，并给出它在 3x5090 上的技术栈与交接方式。

## 1. 总体结构

### 1.1 分工

流水线由执行者 cc 在 3x5090 上完成。cc 像接手任务的工程师：读 `handoff.md` 与本文，逐个 SRC 查看原始数据，自己写该 SRC 的 adapter 和跑数脚本，调用共享模块，自己决定怎么试跑、怎么核对、遇到问题怎么处理。本文与 `etl/` 只交付定义「做对」所需的部分。

| 层 | 内容 | 谁来做 |
| --- | --- | --- |
| A | 业务语义（3A 模型、ID、affinity 规则、清洗规则）；8 个共享模块；`3a` 的输出形状与 `merge`；技术选型与运行环境；`handoff.md` | 本文与 `etl/` 交付 |
| B | 每个 SRC 的 adapter、跑数脚本与编排；中间表怎么落盘；缓存与续跑；对账与试跑；决策文件的写法与取证 | cc 按实际 SRC 现场完成 |

共享模块按功能划分，不按 SRC 划分，不含任何 SRC 的名称或特例，也没有「适配 20 个 SRC 的通用脚本」；SRC 之间的差异全部落在 adapter 里，adapter 属于 B 层。第 4、5 节中的表结构、缓存键、阶段划分是推荐形态，cc 可以按实际调整；`3a` 的形状、affinity 五元组、ID 公式和 lineage 语法不可改动。

### 1.2 原则与数据流

五条原则：

1. adapter 薄：只把源行搬成统一的 record，不清洗序列，不推断生物学含义。
2. 清洗只实现一次：序列、结构、突变的处理只在共享模块里出现。
3. 按 distinct 键计算：同一个清洗输入只处理一次，再 join 回 record。
4. 运行期确定性：AI 只产出带证据的决策文件，运行期不调用 AI。
5. 以产出为目标：能得到有效 3A 就产出，排除只用于确实无法产出的记录。本文各处的排除码是默认处置，不是必须照做的拒绝规则。某个排除条件命中一个 SRC 的大部分记录时，说明该条件与这个 SRC 的实际数据不符，由 cc 现场调整处理方式并记入 lineage，不让条件把整个 SRC 挡掉。

```text
SRC 原始数据 -> adapter(SRC) -> raw_ab / raw_ag / raw_obs   (以 record_key 对齐)
                                 |            |
              AB 支 (distinct ab_key)   AG 支 (distinct ag_key)         AFF 支
              pair_slots + seqnorm      bind (adapter + 决策文件)       已在 adapter 内完成
              -> structref              -> structref
              -> mutate (-> vdomain)    -> mutate
              -> vdomain                -> antigen_bound
              -> ids -> ab_entity       -> ids -> ag_entity
                                 |
              assemble: 按 record_key 汇合，校验 3A 有效性与突变归属，算 3A_ID
                                 |
              merge: 跨 SRC 按 3A_ID 分组，追加 affinity[]，校验，统计，输出
```

一条 record 是一个 `(抗体输入, 抗原输入, observation 列表)`。一个源行可以产出多条 record，`record_key = (src, file, row, role)`，`role` 由 adapter 给出，例如 R15 的 `mut` 与 `wt`，R75 流感集的各个抗原。

AFF 支没有跨行逻辑：占位词过滤、一行多值拆分、`col=` 与类型列写入 lineage、`None` 与 `unknown` 处理（problem_aff 第 1–7 项）都是单行内的操作，不去重，不聚合，因此全部放在 adapter 中，只共享 `lineage` 的字符串构造函数。

## 2. 台账

### 2.1 重叠，合并为共享模块

| 重叠内容 | 出处 | 合并为 |
| --- | --- | --- |
| 在序列中定位可变域：N 端信号肽、C 端标签、恒定区、scFv linker、链身份、非抗体判定、H/L 槽位处理 | ab#3、4、5、6、7、8、12 | `vdomain` |
| WT/parent/突变重建，A/B/C 分类，唯一映射才接受 | ab#9、ag#5 | `mutate`，参数 `entity ∈ {ab, ag}` |
| CDR-only 的母本补全是 parent 上的区间替换（R75：IMGT 107–116） | ab#11 | `mutate` 的 `region` 模式 |
| PDB/mmCIF/FASTA 解析、entity 与 chain 选择、序列按来源优先级恢复、覆盖检查 | ab#10、ag#2、ag#3 的结构覆盖部分 | `structref` |
| "来源 > 结构 > 工具 > fallback，冲突全部写入 lineage" | ab#3–4、5、6、10，ag#6 | `resolve(candidates, order, on_tie)` |
| 字符归一化 | ab#2、ag#7 | `seqnorm` |
| ID 公式与 canonical 序列化 | modeling、ab 方案开头、ag#7、hash | `ids` |
| lineage 字段清单 | 各项均重复列出 | `lineage` |
| 跨源合并与 lineage 追加 | ag#8、todo §3、hash 校验 | `merge` |

### 2.2 冲突，裁决

| 冲突 | 裁决 |
| --- | --- |
| ab#3–4 要求 scFv 先拆，ab#6 要求拆后再做 3–5，ab#5 要求 3–4 先做 | `vdomain` 一次调用输出全部可变域区间，N 端残余、C 端残余、恒定区、linker 都是区间之外的部分，不存在先后顺序 |
| ID 公式：modeling 与 ab、ag 写作无前缀的 `hash(...)`，hash 文档带 `ab/v1:`、`ag/v1:`、`3a/v1:` 前缀 | 以 hash 文档为准 |
| reject/audit：modeling 写"进入 reject/audit"，ab、ag、aff 写"不建 audit 目录"，todo §3 要求输出 reject reason 统计 | 运行输出中的 `reject_log`，见第 4 节。它不是数据集，不进入 processed dataset |
| todo §3 第 60 行要求输出"重复判定原因"；aff#7 规定不判定不去重 | 以 aff#7 为准：merge 只按 `3A_ID` 分组追加，来源差异由各 tuple 的 lineage 承担，没有"重复判定"这一步，因此没有对应产出。第 58 行的跨源 pair 去重等价于按 `3A_ID` 分组，保留 |
| ab#11 母本搜索第二档（其余 20 个 SRC）使 R75 依赖其他 SRC 的 processed 输出 | 首版只用同 SRC 和来源明确引用的 PDB（`1N8Z`）。第二档的跨 SRC 搜索不实现；各 SRC 不依赖其他 SRC 的处理结果，保持独立可重跑 |

### 2.3 缺口，默认处理

| 缺口 | 默认 |
| --- | --- |
| ag#7 没有列出抗原的字符规则 | 沿用 `seqnorm`（ab#2） |
| 清洗不仅依赖序列，还依赖来源边界、构建体标签、结构 | `evidence` 进入缓存键；只写 lineage 的字段放入 `notes`，不进入缓存键 |
| 突变属于抗体还是抗原侧，ab#9 与 ag#5 都要求先判定，但没有模块负责 | adapter 按源的 partner 或链字段判定并分发到所属侧；无法判定记 C 类。assemble 断言每个声明的突变恰被 AB 或 AG 一侧消费一次，否则 reject `mutation_unassigned` |
| 模型的 `structure` 是单值，ag#8 允许同一 `AG_ID` 有多个结构 | `structure` 取来源优先级最高者，同级按 `SRC_ID`、结构 ID 字典序；其余只写 lineage |
| `structure` 对象没有具体表示 | 指针对象 `{structure_id, file_ref, chain_map}`，不复制坐标；缺失为 `None` |
| 结构快照来源 | 优先使用 SRC 自带归档，RCSB 为后备。R50 的作者归档是重编号快照，突变编号按它映射 |
| R15 的 WT pair 没有完整序列，不属于 A 类 | WT record = 结构恢复的 parent + 空突变表，走 `mutate` 的 `point` 模式 |
| R76 的 `3RVV`、`3RVW` 已撤销并入 `5VPL`、`5VPG` | `structref` 解析为替代条目，替代关系写入 lineage |
| 突变位点落在被裁掉的区段 | 清洗后的序列与 parent 相同，按 hash 规则落入同一 `AB_ID`，位点写入 lineage |

## 3. 模块

共享模块 8 个，每个是 `etl/core/` 下的一个 Python 文件加一份同名 md（语义、接口、示例），文件内不含 SRC 名称和特例。`resolve`、`ids`、`lineage` 是小函数。

| 模块 | 输入 → 输出 | 吸收的条目 | 工具 |
| --- | --- | --- | --- |
| `seqnorm` | 原始字符串 → 规范序列或 `None`，附 gap、未知残基、非法字符标记 | ab#2、ag#7 | 无 |
| `structref` | 结构 ID 与 chain/entity 查询 → 链记录（entity、按优先级取得的序列、观察到的残基、编号）和覆盖信息 | ab#10、ag#2、ag#3 的结构部分 | gemmi 0.7.5；SRC 自带快照，RCSB 经 mihomo 代理只读拉取并缓存 |
| `mutate` | `point`：`(entity, parent 链, 突变元组, 编号方案)` → 突变序列，或 C 类与原因；`region`：`(parent 两链, 方案, 区间, 替换序列)` → 替换后的链，另一条链原样保留 | ab#9、ab#11、ag#5 | 无；`region` 调用 `vdomain` 取 parent 编号 |
| `vdomain` | `(序列, hints)` → 可变域区间列表 `[(start, end, 链类型, 编号)]` 与区间之外的残余；`hints` 来自 `evidence` 中的来源边界与结构边界 | ab#3、4、5、6、7、8、12 | ANARCI 2026.2.13.2 经 HMMER 3.4 的 `hmmscan`（首版唯一工具） |
| `antigen_bound` | 抗原链候选与构建体证据 → 实验片段的有序链列表 | ag#3、ag#4、ag#6 | 无 |
| `resolve` | `(候选列表, 优先级顺序, on_tie)` → `(选中项, 全部候选, 冲突标记)`；`on_tie ∈ {pick_top, reject}`，可挂 tie-break 函数 | 见 2.1 | 无 |
| `ids` | 规范序列 → `AB_ID`、`AG_ID`、`3A_ID`，碰撞检查，golden vector | hash、ag#7 | hashlib |
| `lineage` | 键值 → lineage 字符串；语法固定为用竖线分隔的 `key=value` 片段（定位、`col=`、类型列、`step=`、各步骤描述） | 各项的 lineage 清单 | 无 |

各调用点的冲突策略在 `resolve` 的参数里配置：ab#3–5 取最高优先级并记录冲突（`pick_top`）；ab#6 同级时取两侧域有效且未解释片段最短的候选（`pick_top` 加 tie-break）；ag#6 同级冲突排除（`reject`）。首版只有 ANARCI 一个工具，ab#3–4 的"多工具一致"一层不可达，跳过。

`vdomain` 的派生规则：

- 区间数为 0：非抗体或无法定位，记 `no_domain`，排除。
- 区间数为 1：该区间是 VH/VHH 或 VL，由链类型决定；区间之外的 N 端残余按信号肽或标签、C 端残余按标签或恒定区在 lineage 中归类。
- 区间数为 2：只有一条 H 加一条 K/L 才是 scFv。两区间之间的残余按 ab#6 校验为 linker：来源给出的 linker、已知 linker 库、G4S 重复，且 linker 完全位于两域之间、没有第三个域、不残留在 VH 或 VL 中。方向为 VL-linker-VH 时互换后写入字段。
- 其他情形（同类型两区间、区间数大于 2）：不静默压缩为一对，按未解析排除。
- 槽位处理 `pair_slots(h, l)`（ab#7）：两槽不同且都不是完整 scFv，直接进入逐链处理；两槽相同且无 linker，排除为 `slot_collision`；两槽相同且含 linker，或只有一槽且是完整 scFv，按单链处理，并保留两个槽位的原始定位；两槽不同但标签存疑，仅当一条为 H、另一条为 K/L 时互换，否则按未解析排除。
- heavy-only 一律写为 `vh_sequence`，`vl_sequence = None`；VHH、普通 VH-only 的区别只写 lineage（ab#8）。

`mutate` 的 `point` 模式只接受唯一映射且原残基一致的编辑（A/B/C 规则同 ab#9）。`region` 模式用于 R75：先对 parent 跑 `vdomain` 得到 IMGT 编号，替换指定区间，校验框架两侧与总长度，不校验被替换区间的原残基；输出 parent 的 VH 与 VL，被替换的链换成新序列，另一条链原样保留。区间边界需用 `1N8Z` 实测确认。

首版只接 ANARCI。ab 方案列出的 SignalP 6.0、Phobius、IgBLAST、HMMER3、InterProScan、DIAMOND 在以下情形才引入：某 SRC 的记录没有来源边界，且 ANARCI 失败（`no_domain`）占比不可接受。ANARCI 对 VHH、非人源、截断域和 scFv 两域的覆盖需要用 R08、R74、R76 的真实序列实测。ANARCI 单次调用的 `ncpu` 参数没有加速作用，吞吐靠多批并行取得，见 5.3。

### AI 接缝

AI 只用于把非结构化证据（README、metadata、表说明、文献语境）转成结构化论断，范围限于：

- ag#1 固定目标 SRC 的抗原身份与来源。
- ag#2 没有随包序列时的序列来源指针。
- ab#11 的 parent 来源（VH 与 VL 一并给出）。

产物是 `decisions/<SRC>.yaml`：

```yaml
src: R23
claims:
  - id: ag-mit-target
    kind: ag_context            # ag_context | sequence_source | parent_source
    applies_to: {file: ..., column: Target, value: MIT_Target}
    value: {name: ..., branch: fixed, sequence_ref: ...}
    evidence:
      - {file: ..., locator: ..., quote: ...}
```

- `applies_to` 限定论断适用的文件、列和取值，不适用的行不继承。R23 有 4 个 Target（MIT_Target 与 AlphaNeg1~3，各 314,925 行），AlphaNeg 是不同的抗原对象，需要各自的 claim；没有来源序列的 Target，其行按 `no_antigen_binding` 排除。R09、R11、R75、R79 这类多表多靶 SRC 同理，按表、列、值分别给 claim。
- 证据可以是快照中的文件，包括其他 SRC 的原始文件；也可以是工作者 AI 经 mihomo 代理联网取得的页面，页面文本存为决策文件旁的快照文件，证据写 `{url, snapshot_file, quote}`。决策文件不引用任何 SRC 的处理结果。
- 跨 SRC 的对应关系（例如 R78 是 R79 各 campaign 的采样）由工作者 AI 联网核验，核验依据以原文引用写入证据。
- 论断写入决策文件前由 cc 自查：`file` 或 `snapshot_file` 存在，`quote` 在其中逐字出现，`value` 中的序列在引用的 FASTA 或结构 entity 中逐字出现。自查的方式由 cc 决定，不交付校验工具；自查不过的论断不进入决策文件。
- 决策文件入库（含网页快照），内容 hash 进入缓存键。运行期只读决策文件，不联网，不调用 AI。

## 4. 中间表与运行输出

Parquet，每个 SRC 一组。以下是推荐的数据形态，cc 可以按实际调整；`3a` 的形状由 modeling 固定。

```text
raw_ab     record_key, src, h_raw, l_raw, evidence, notes             ab_key = H(h_raw, l_raw, evidence)
raw_ag     record_key, src, branch, seq_raw[], evidence, notes        ag_key = H(branch, seq_raw[], evidence)
raw_obs    record_key, label, assay, condition, replicate, lineage[]
ab_entity  ab_key -> AB_ID, vh, vl, structure, lineage[], applied_edits[]  | reason_code
ag_entity  ag_key -> AG_ID, sequence[], structure, lineage[], applied_edits[]  | reason_code
pair       record_key, AB_ID, AG_ID, 3A_ID, obs[]                     (assemble 输出)
3a         3A_ID, antibody, antigen, affinity[]                       (merge 输出，即 modeling 的 3A)
```

- `evidence` 是 JSON 字符串，由 adapter 填，只含影响清洗的内容：源的构建体标签、结构引用与链号、来源给出的边界、待应用的编辑（解析成 `(id, chain, orig, pos, new, numbering)` 的元组，A 类序列不含）、所用决策文件的 claim ID。`notes` 只含写入 lineage 的内容（A 类序列的突变原文、名称、来源描述），不进入缓存键。
- adapter 输出契约：`raw_*` 中的值保持源的原样；`None` 只用于源为空或占位的字段；`raw_obs` 的 `label` 不为 `None`，其余三个字段各自可为 `None`。
- `ab_entity.lineage` 与 `ag_entity.lineage` 只含清洗步骤，每条以 `step=<名称>` 开头。assemble 把 record 的源定位与 `notes` 追加到实体副本，merge 对相同 ID 的 lineage 取并集。
- `reason_code` 非空的实体对应的 record 不生成 `3A`。
- 一个源行的 observation 全部不成立（problem_aff 第 1 项）时，adapter 不输出 record，并写入 `reject_log`。

**运行输出**：processed dataset 只有 `3a` 的 Parquet shards。其余都是运行输出，随运行目录保存，不进入 processed dataset：

- `reject_log`：`(stage, reason_code, src, key, detail)`。`detail` 是 JSON，保存候选、证据等级、未通过的检查，足以由原始定位重新处理（ab、ag 方案对排除记录的要求）。adapter、ab、ag、assemble、merge 各阶段都写。
- `stats`：由 merge 生成的旁路表，不改动 `affinity[]` 的五元组。内容为 sequence/structure 覆盖（按 SRC 统计 `structure` 与各链为 `None` 的数量）、reject reason 计数、label type（对 observation lineage 解析 `col=` 与类型列取值，按 `(src, col, 类型列取值)` 计数）、source overlap（每个 `3A_ID` 的 SRC 集合，来自 lineage 的 `SRC_Rxx` 定位）。
- `qa_sample`：按固定随机种子分层抽样的 `3A` 列表，分层依据是实体 lineage 的 `step=`（直接、裁剪、拆分、突变重建、结构恢复），种子与每层数量写入 manifest。

## 5. 运行环境与执行模型

### 5.1 运行环境

流水线在 3x5090 上运行。下表是 2026-11-04 的实测情况。

| 项 | 实测 |
| --- | --- |
| 主机 | `ssh 3x5090`，Ubuntu 24.04，Python 3.12.3，128 核，251 GB 内存，3 × RTX 5090 |
| GPU | 显存已被其他用户大量占用。流水线是 CPU 任务，不使用 GPU |
| 共享 | 33 个登录用户，负载约 8。并行 worker 以 32 为上限 |
| 磁盘 | 根分区已满，只剩 3.7 GB，`~` 在根分区上。工作区、临时文件和各类缓存（`TMPDIR`、`UV_CACHE_DIR`、`XDG_CACHE_HOME`）全部放在 `/data_new/ywy/`，该盘剩 1.8 TB |
| 权限 | 无 sudo。系统包用 `apt-get download` 加 `dpkg -x` 解到用户目录，HMMER 即此法安装在 `/data_new/ywy/tools/hmmer/usr/bin` |
| 数据 | `/data_new/ywy/dataset-abag/SRC_Rxx_*`；仓库在 host 上位于 `/data_new/ywy/LOVYATEE/`，`etl/` 在其根目录下 |
| 网络 | 直连可达：PyPI 清华镜像、`archive.ubuntu.com`、`rcsb.org`。直连不通：`github.com`、`pypi.org`、`huggingface.co`、`files.rcsb.org`、`www.ebi.ac.uk`，这些只能经 mihomo 代理，已逐个测通，`files.rcsb.org` 下载 `1N8Z.cif` 约 1 秒。DNS 只有 `1.1.1.1` 能用，`8.8.8.8` 和国内公共 DNS 的 UDP 53 都超时 |

mihomo v1.19.33 装在 `/data_new/ywy/tools/mihomo/`，监听 `127.0.0.1:17890`（http 与 socks 混合端口），控制接口在 `127.0.0.1:19090`，策略组 `PROXY` 为 url-test，节点来自用户的订阅，共 65 个，实测 32 个存活。订阅链接只存在于 host 上权限为 600 的 `config.yaml`，不入库。需要外网的命令显式带 `https_proxy=http://127.0.0.1:17890`，其余流量不经代理。mihomo 的 DNS 固定为 `1.1.1.1`。mihomo 必须带 `GODEBUG=tlsmlkem=0` 启动：Go 默认的 ML-KEM 密钥交换会让 TLS ClientHello 变大，在这个网络上握手超时，订阅拉取失败。启动命令为 `GODEBUG=tlsmlkem=0 setsid nohup ./mihomo -d . -f config.yaml`，主机重启后需要重新启动。下载失败时先查 `PROXY` 组当前选中的节点和存活数。

到 host 的 SSH 经本机端口转发，偶发断开。长任务用 `setsid nohup` 启动并把日志写入文件，断线不中断运行。

### 5.2 技术栈

| 角色 | 选择 | 用法 |
| --- | --- | --- |
| 流水线引擎 | Daft 0.7.26 | 各 SRC 的阶段：读取、distinct、批量 UDF（调用 ANARCI、gemmi）、join 回 record、写 Parquet |
| 查询与 merge | DuckDB 2.0.0 | 直接对 Parquet 写 SQL：全局 merge 的分组追加、对账、`stats`、`qa_sample` |
| 存储格式 | pyarrow 25.0.1，Parquet | schema 用 pyarrow 声明 |
| 结构解析 | gemmi 0.7.5 | `structref` 解析 PDB 与 mmCIF。已在 R14 的 `3BDY.pdb` 上验证：entity 全长序列（H 链 230）与已观察残基（216）可分别取得，覆盖检查可行。RCSB 的 `1N8Z.cif` 同样验证：轻链 214、重链 220，HER2 的 entity 全长 607，已观察 581 |
| 可变域编号 | ANARCI 2026.2.13.2 与 HMMER 3.4 | `vdomain` |
| 环境 | uv 0.13.7，venv 在 `/data_new/ywy/envs/etl` | 版本记录在 `etl/` 的依赖文件中 |
| 测试 | pytest | 模块自检 |

Daft 与 DuckDB 读写同一份 Parquet，分工按场景而不是按阶段，两者都能做的事 cc 任选其一。已验证 `affinity[]` 可以作为 `list<struct>` 存取：Daft 写出，DuckDB 用 `list()` 按 `3A_ID` 分组追加，Daft 和 pyarrow 都能读回，`None` 保留。全为 `None` 的列会被推断成 `null` 类型，所以每张表的 schema 必须用 pyarrow 显式声明。

Ray 不采用。Ray 解决的是跨机调度和 actor 编排，这里是单机 CPU 密集的 distinct 序列并行。Daft 在本机直接并行，并带 Ray 后端（`daft.set_runner_ray`，已确认存在），需要跨机时切换，业务代码不变。

### 5.3 执行模型

逻辑阶段为五个：`adapt → ab → ag → assemble → merge`。前四个按 SRC 独立运行，`merge` 全局运行。编排方式由 cc 决定，这五个阶段不引入 Snakemake 或 Airflow，需要跨机调度时再引入。

- **缓存键**：键应覆盖输入内容 hash、模块版本、规则版本、决策文件 hash、外部结构快照 hash，键不变则跳过。每个阶段、每个 SRC 的产物旁写 `.key`。
- **distinct 键**：`ab`、`ag` 阶段按 `ab_key`、`ag_key` 去重后处理。没有逐行序列的结构型 SRC（R14、R15、R50）再分两层：parent 恢复与 `vdomain` 以 `(结构引用, 链)` 为键只做一次，随后按编号映射应用点突变并校验原残基，长度不变，可变域边界按位置继承，不重跑 ANARCI；含插入或缺失的编辑才重跑 `vdomain`。R50 的 942,723 行 FoldX 来自 1,409 个 PDB，只有这样才能省算。
- **并行**：SRC 之间并行；distinct 键之间并行，ANARCI 按批调用。规模参照：R09 约 460 万行（其中 li2023 两张表 1,259,700 与 1,903,927 行），R23 1,259,700 行，R50 963,552 行（FoldX 942,723，Flex 20,829）。ANARCI 在 host 上的实测（IMGT 编号，重链序列，每批 500 条）：单进程 69 条/秒，8 进程 557，32 进程 1,967，随进程数线性增长；单次调用的 `ncpu` 取 8 与 16 没有差别，并行靠多批多进程。100 万条 distinct 序列在 32 进程下约 9 分钟。Daft 原生执行器下，批量 UDF 调用 ANARCI 的实测（16,000 条，`batch_size=500`）：默认在线程里运行，156 条/秒；`use_process=True` 为 1,397 条/秒，接近纯多进程的水平。`into_partitions` 在原生执行器上不起作用，批大小用 `batch_size` 控制；`max_concurrency` 只适用于 `@daft.cls`。
- **外部输入**：结构优先取 SRC 自带的文件（R14 的 `AB-Bind-Database/*.pdb` 可直接解析）；SRC 里没有的，经 mihomo 代理从 RCSB 只读拉取，按 PDB ID 缓存到 `/data_new/ywy/cache/rcsb/`，缓存文件 hash 进入缓存键。
- **merge 的断言**：同一 `AB_ID`、`AG_ID`、`3A_ID` 只对应一个 canonical 字符串，否则中止（hash 文档）；每个 `3A` 满足 modeling 的有效性。
- **manifest**：ID 方案版本、清洗规则版本、代码 commit、工具版本（Daft、DuckDB、gemmi、ANARCI、HMMER）、决策文件 hash、各阶段行数、`qa_sample` 的种子。

## 6. SRC 映射与实施顺序

抗体侧和抗原侧入口取自 problem_ab、problem_ag 对各 SRC 的列举，序列形态取自各 SRC 的 inventory。表中是给 cc 的业务提示，具体怎么处理由 cc 对照实际数据决定。

| SRC | 抗原入口 | 需要的非平凡处理 |
| --- | --- | --- |
| R76、R77 | 逐行序列 | 列表字符串解析；21 行 H/L 槽位相同（15 行含 linker）；恒定区 |
| R08 | 固定目标 TNF-alpha，有直接序列 | 22 aa 信号肽、`6×His`、VHH；`corpus-hTNFa.csv` 无 label，不产生 observation |
| R74 | 固定目标 PD-1，由参考结构 5GGS 的 entity 3 重建 | 576 条完整突变重链（A 类，突变名只入 lineage），末尾 `HHHHHH`，恒定区 |
| R03 | 逐行序列，附参考 PDB | 完整重/轻链（A 类，突变字段只入 lineage）；WT 与突变体两张表；`affinity_type` 长表 |
| R80 | PDB 链恢复 | 结构恢复、VL-linker-VH 反向 scFv、VL-only、NA 与非蛋白抗原排除 |
| R20 | 无 affinity | 不是流水线 SRC，作为 `structref` 的资源适配器，不产生 `3A` |
| R14 | 亲本 PDB 实体，无逐行序列 | 首个 B 类 SRC：突变落在抗体或抗原侧；Fc-only 排除（1T83、3WJJ）；结构恢复与编号映射 |
| R15 | 参考结构的非抗体伙伴 | `mut`/`wt` 两条 record；突变在任一侧；非抗体复合物排除；多链伙伴 |
| R50 | 结构关联 FASTA | 4 张表：FoldX 942,723、Flex 20,829 产出（每个 Flex 行 2 条 observation）；AB-Bind 645、SKEMPI 608 不产出，实验 ΔΔG 的原始值由 R14、R15 提供；作者归档的重编号快照；名称编码突变；VL-only；scFv；计算 ddG |
| R75 | 固定目标 HER2 | CDR-only，经 `mutate` 的 `region` 模式从 `1N8Z` 补全 VH 并保留 parent VL；流感集一行多抗原 |
| R13 | 逐行序列 | 多链分隔符与缺失值；H/L 槽位内的 scFv；恒定区 |
| R11 | 固定目标，由结构重建 | 恒定区 |
| R16 | PDB/FASTA 重建 | 5C2B 单链 scFv；4NKI、5I30 的来源标签与结构实体不一致 |
| R79 | 活动级固定构建体，无随包序列 | 抗原序列取自 R78 的原始文件（R78 是 R79 各 campaign 的 5k 采样，每张表的 `antigen` 列带直接序列）；对应关系由工作者 AI 联网核验并写入决策文件，对不上的 campaign（如 HER2-OPT 与 R78 的 HER2 120 aa 片段）其行按 `no_antigen_binding` 排除 |
| R23、R78 | 固定构建体，直接序列 | scFv（VH-GGGGSGGGGSGGGGS-VL）；R23 的 4 个 Target |
| R10 | 逐行序列，PDB 锚点 | 突变主要描述抗原逃逸；`IC50`、`Affinity_Kd`、`escape` 三个亲和力列，部分行多列并存 |
| R09 | 固定目标与 AbRank 序列混合 | 86 张表；scFv；突变；kothiwal 的两个独立读数 |
| R12 | 逐行序列 | 长表 `affinity_type`；`scfv.csv` 中完整单链与 754 条独立 H/L 混合；非抗体链 |

建议按垂直切片推进，批次沿用 todo，批内先后按引入新模块的顺序，cc 可按实际情况调整：

1. **R76**：贯穿 adapter、`pair_slots`、`seqnorm`、`vdomain`、`ids`、`lineage`、assemble、merge，`structure` 先只记录 PDB 指针。
2. **R77**：预期与 R76 产出相同的 `3A_ID` 集合（inventory 标 R77 为 R76 的同源快照）。差异逐条查，这一步同时验证 merge 的跨源追加。
3. **R08**：信号肽、标签、固定目标与决策文件。
4. **R74**：A 类突变序列的 lineage 处理、`structref` 从参考结构重建抗原。
5. **R03**：WT 与突变体两表，长表 lineage。
6. **R80**：结构恢复，`vdomain` 的两区间与反向 scFv。
7. 第二批依次为 R20 资源适配器、R14、R15、R50、R75、R13、R11、R16：R14 首次验证 `mutate` 的 `point` 模式与编号映射，R15 加入 WT record 与双侧突变，R50 验证结构型 SRC 的两层键，R75 验证 `region` 模式。第三批按 todo 的顺序。
8. 每个 SRC 只补它引入的 adapter 和特例。共享模块出现 SRC 特例即视为划分错误：cc 修正模块本身，不在模块里加按 SRC 的分支。

## 7. 交付物与交接

### 7.1 etl 目录

```text
etl/
  handoff.md        交接文档，cc 的入口
  env.sh            激活环境：venv、PATH 中的 hmmscan、TMPDIR 与各缓存目录
  <依赖文件>         uv 导出的版本记录
  core/
    seqnorm.py  structref.py  mutate.py  vdomain.py
    antigen_bound.py  resolve.py  ids.py  lineage.py
    merge.py
    <模块名>.md      每个模块一份：语义、接口、示例
```

B 层的产物（`adapters/`、`decisions/`、`runs/` 等）由 cc 在 `etl/` 下按需创建，目录结构由 cc 决定。

### 7.2 handoff.md

`handoff.md` 保持短，内容限于：

- 目标与成功标准：产出有效的 `3a` shards。成功的标准是有产出，不是处处合规（原则 5）。
- 硬约束：affinity 五元组不改，额外信息只进 lineage；不写根分区，临时文件与缓存放 `/data_new/ywy/`；刻意保持压缩的数据集不解包；只在 main 工作。
- 环境入口：`env.sh`、代理用法、数据路径（5.1）。
- 工作对象：20 个 SRC 的清单与建议顺序（第 6 节），每个 SRC 指向它的 inventory、README 与相关设计文档。
- 共享模块的用法。发现模块缺陷可以直接修，不加按 SRC 的分支，修改记一行并重跑受影响的 SRC。
- 决策文件的原则：论断带可追溯的证据，运行期不联网不调用 AI。写法与取证方式由 cc 决定。
- cc 自己维护进度记录，用于跨上下文续作。

### 7.3 A 层开发顺序

1. `ids`、`lineage`、`seqnorm`：无外部依赖。`ids` 用 hash 文档的 golden vector 自检。
2. `vdomain`：用 R08、R74、R76 的真实序列实测 ANARCI 对 VHH、scFv、截断域的覆盖，得到 `no_domain` 比例，作为是否引入第二个工具的依据。
3. `structref`、`mutate`、`resolve`。
4. `antigen_bound`：设计中最粗的一个，写它的 md 时把 ag#3、4、6 落成可编码的规则。
5. `merge`，含 `stats` 与 `qa_sample`。
6. `env.sh`、依赖文件、`handoff.md`。

每个带判断逻辑的模块留一个最小自检（`__main__` 里的断言或一个 `test_*.py`），用真实序列。

## 8. 验收

- **ID**：golden vector 单元测试（hash 文档已要求）；同一输入重跑，ID 与 manifest hash 逐字节一致。
- **对账**，每个阶段按自己的单位分别核对：
  - `adapt`：源行数 = 产出 record 的行数 + `reject_log` 中该 SRC 的 adapt 行数；产出的 record 数可大于行数（R15 的 `mut`/`wt`）。
  - `ab`、`ag`：distinct 键数 = ok 实体数 + reject 实体数。
  - `assemble`：record 数 = pair 数 + reject 数。
  - `merge`：`Σ len(affinity[])` = 全部 pair 的成立 observation 总数，每条恰好出现一次（aff#7）；pair 数与 `3A` 数的差额 = 相同 `3A_ID` 的合并数。
- **排除占比**：按 `reason_code` 统计每个 SRC 的排除占比。某个原因码命中过半记录时，先复查该排除条件是否适用于这个 SRC（原则 5），再决定是否接受。
- **R76**：493 行对应 476 个源内唯一 `(X1, X2)` pair；最终 `3A` 数与 476 的差额必须能被 `reject_log` 与 ID 合并解释。
- **跨源**：R77 对 R76 的 `3A_ID` 集合（见第 6 节）。
- **工具覆盖**：在 R08、R74、R76 上统计 `vdomain` 的 `no_domain` 比例，作为是否引入第二个工具的依据。
- **抽样**：todo §3 的人工检查使用 `qa_sample`；每层数量在第一个切片完成后确定。
