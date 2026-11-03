---
tags:
  - context
---

# Handoff — diversity-coverage 产物架构（2026-10-22）

> 本文件是给后续 agent 的 background prompt。读完应当能直接接着工作，不需要重读对话历史。
> 写于 2026-10-22，对应 commit `cd90662`。

---

## 1. 仓库与当前状态

- 仓库：`G:\OUROBOROS-AI4S\abag-diversity`，分支 `main`，已推送 `origin/main`（`cd90662`）。
- 池根：`G:\OUROBOROS-AI4S\abag-diversity\odrerir`。
- 池现状（实测）：son **89**、dregs 16、mead **0**、bodn 9、tools 14。
- 有序子图：101 节点 / 106 边 / 高度 7 / 58 根。
- `odrerir check` 全绿（同批同日的 `check-relation-causality` WARN 是良性的，不要为消 WARN 改日期）。

### 本机没有数据

`data/` 不在本机。全部原始数据源在 ab 机的 `/data/shared/CX029_binding_ranking/data/raw/public/<source_id>/<version>/`，另有一份在 HF 私有 bucket `Pthahnix/dataset-abag`（64 个源，约 609 GiB）。本机无 HF 凭据（`hf buckets ls` 返回 401）。2026-10-22 起 `ssh ab01/ab02/ab03` 均返回 `Permission denied (publickey)`。

**推论：在本机做出的任何关于数据内容的断言，只能停在「文档声称」这一档，必须显式标注。任何实际读取 CSV、跑实验、核算行数的工作都要等 ab 机恢复。**

---

## 2. 这个项目在解什么

一句话：**抗原-抗体数据的多样性如何定义、量化、并验证其有效性。**

服务两个下游决策：

1. 数据要收集到什么规模（当前目标每年 90–100 个抗原，够不够未知）；
2. 现有开源数据在表位层面是否已高度重复。

核心约束（2026-10-19 会议）：

- 抗原侧表位多样性**不能用序列刻画**（表位在三维相邻，序列上可相距很远）；
- 抗体侧可在 CDR 序列/结构上聚类，但阈值主观；
- 几何/接触信息是不可忽略的一维；
- 度量对象是**配对抗原-抗体**，不是单侧；
- 有效性判据：按某相似性聚类后若模型指标显著下降，说明该维度承载真实泄漏。

书面定义在 `odrerir/son/diversity_is_a_task_conditioned_coverage_claim.md`：

```text
Certificate = (D, O, X, R, V, T, M, result)
S(D,O,X)    = similarity structure
Diversity   = F(S, R, V, T, M)
```

---

## 3. 本次会话做了什么

### 3.1 评估了 Codex 给的 demo

对象：`context/2026-10-22-diversity-coverage-demo/`（`server/server.py` 335 行、`server/schema.json`、`skills/diversity-coverage/SKILL.md`、5 个测试），设计文档 `context/2026-10-22-diversity-coverage-plugin-research.md`。

**结论：分层接缝对了（skill 负责对话、MCP 负责确定性记账、证书是对象），但内核是空的，且把测量与编排塞进了 server，把 `R`/`V` 降级成两个标量。**

### 3.2 找到的六处实质缺陷（含行号，可复核）

1. **缺测被当成「不覆盖」**（`server.py:178-189`）。一对分数都没有的对象取 max=0，计入 `uncovered`，`query_coverage_fraction` 分母包含全部对象。若 90% 的比对没测，覆盖率被压低 90%，而该数字照样能被 certified。这直接违反研究文档第 65 行自己写的「不把缺失值填成零相似度」。
2. **`S` 的缓存键错了**（`server.py:134`、`:157`）。用整份七槽 declaration 的哈希绑相似性产物，但 `S` 只应依赖 `(D,O,X)`。后果：换一个 `R` 就要整张矩阵重算，而「同一 S 在不同 R 下是否给出不同结论」正是本项目最需要问的问题，在该寻址规则下无法提出。
3. **`V` 塌缩成一个阈值，且人工批准在提升主张强度**（`server.py:211`）。`strength = certified if status==certified`，而 status 由 `human_decisions` 推出。点一次批准就把主张升档，与留出证书的定义相反：强度上界由独立证据给定，人工只能决定放不放行。
4. **证书活不过进程**（`server.py:20` 的模块级 `RUNS`）。重启/换机/三个月后复查都不可能。而「可复算、可审计」是这件产物的全部理由。
5. **`recipe` 在预算受限时优先丢掉未覆盖样本**（`server.py:257`：`selected = (covered + uncovered)[:limit]`）。方向与多样性目标相反；且完全没有 `rep_only` / `cluster→member` / `none` 三种采样策略。
6. **`provenance` 硬编码**（`server.py:141`：`{"adapter": "local-declared-measurement"}`）。接上 MMseqs2/Foldseek 后会持续声明虚假来源。

次要：`covered_query_ids`（D 侧）与 `covered_reference_ids`（R 侧）同权重呈现，但 coverage 是 `D→R`；`risk` adapter 的 0.2/0.5 阈值硬编码。

### 3.3 落入池子：26 条 son 记录

全部 `tags: 2026-10-22-architecture-design`，且**只有这一个 tag**。已按语义挂成树（每条一个 `⊑` 边），`check` 全绿。

| slug | 一句话 |
| --- | --- |
| `core_is_two_functions_and_one_document_type` | 内核只有 `Measure`、`F`、证书三项，其余全是外壳 |
| `similarity_structure_is_not_a_certificate` | S 的键是 `(D,O,X)` 不是七槽；分离落成产物边界 |
| `similarity_artifact_must_be_sparse_and_threshold_indexed` | 609 GiB 下不能物化矩阵，稀疏到顶-k + 显式未测 |
| `certificate_must_be_verifiable_offline` | 证书必须是自校验字节，`verify(blob)` 不需要服务端 |
| `certificate_format_outlives_its_host` | 删掉所有 host binding 后证书还能验证，格式才算独立 |
| `provenance_document_is_not_a_certificate` | provenance 是存在量词，certificate 是全称量词 |
| `measurement_adapter_contract_is_the_only_interface_that_must_be_frozen` | 唯一必须冻结的接口；adapter 自报 provenance，server 不得代填 |
| `approval_cannot_strengthen_a_claim` | `evidence_tier` 与 `review_state` 必须分开 |
| `four_claim_strengths_need_four_validators` | 对象覆盖 / 任务迁移 / 配方收益 / 推理风险，四套验证器 |
| `validity_envelope_is_computed_from_missingness_and_exposure` | 边界由缺测率、输入档位、`M` 暴露、`R` 可观测性算出 |
| `missing_measurements_are_a_third_state_not_a_zero` | 覆盖率是区间不是数，分母分列 |
| `coverage_number_can_travel_but_its_meaning_cannot` | 覆盖率可比条件最苛刻：需同一 O/X/R/τ/w/插补策略 |
| `threshold_choice_must_be_reported_separately_from_coverage` | τ 改变被测量的对象，不是精度旋钮 |
| `specification_curve_is_the_reporting_form` | 报告形式是规格曲线，不是单一数字 |
| `merge_coverage_is_bounded_not_additive` | `max ≤ Cov(A∪B) ≤ min(1, 和)`，增量必须实测 |
| `recipe_plan_is_a_mixture_optimization_not_a_ranking` | 加权集合覆盖的预算版本，不是排序后截断 |
| `split_plan_cannot_be_derived_from_coverage_alone` | 输出方案表（规则 / 假设 / 混淆项），至少一个基线划分 |
| `reference_domain_is_the_research_output_not_a_slot` | `R`/`V` 是可命名、可版本化、可复用的对象，不是配置 |
| `declaration_library_is_the_reusable_asset` | 可复用资产是声明，不是代码 |
| `unknown_is_a_typed_slot_state_not_a_string_convention` | `known` / `unknown` / `unfilled` 三态，字段级而非槽级 |
| `documentation_completeness_is_not_evidence_tier` | 七槽填满不构成任何证据 |
| `tool_inventory_is_not_a_measurement_protocol` | 工具清单回答能做什么，协议回答数是什么意思 |
| `agent_compiles_declarations_the_core_executes` | agent 编译声明，核心执行；HEP 实测 temperature=0 仍不确定 |
| `free_text_and_recomputable_declaration_are_separated_by_revision` | 用时间轴分离自由表达与可复算，rationale 降级为注释 |
| `existing_artifacts_each_hold_one_third_of_this` | 公开产物无一同时具备三项，空白在组合不在算法 |
| `cheapest_refutation_of_the_certificate_semantics` | 一个抗原、8 个格点，一小时可判架构成立与否 |

---

## 4. 调研结论（作为 background prompt 的事实依据）

横向比对结果（详见 `existing_artifacts_each_hold_one_third_of_this`）：

| 产物 | 测量语义 | 选择空间 | 结论复算 | agent 编排 |
| --- | --- | --- | --- | --- |
| Biomni / STELLA | 0 | 0 | 0 | 1 |
| DataFlow / ICDL-Agent | 部分 | 0 | 0 | 1 |
| RO-Crate / PROV-AGENT / DLProv | 0 | 0 | 0 | 部分 |
| Datasheets / Nutrition Label / EvalCards | 0 | 0 | 0 | 0 |
| multiverse / Comet | 0 | 1 | 部分 | 0 |
| DecoupleMix / CABS | 部分 | 部分 | 0 | 0 |

**没有任何公开系统在「测量协议 + 选择空间报告 + 结论可复算」三项上同时成立。** 新颖性只能主张这三元组的缝合，写大了会立刻被指认已有工作。

关键实证约束：

- ScienceAgentBench：102 个任务、最强 agent 三次尝试独立解决 32.4%；
- BioDataLab：100 个上游整理任务、最强模型 40%，瓶颈在多步编排与格式遵循；
- HEP + Snakemake：即便 temperature=0，采样参数默认值仍使输出不确定 → **agent 自由文本不能作为可复算输入**；
- SEER-Repro：9.5% 的已复现结论对分析选择敏感 → 规格曲线是必要的报告形式。

---

## 5. 架构结论（后续工作的基准）

### 5.1 内核

```text
Measure : (D, O, X) -> S            # 一个冻结接口，实现可替换
F       : (S, R, V, T, M) -> C      # 纯函数，语义固定
C       : certificate               # 一种文档类型，可离线校验
```

判据：**任何不能写成这三项之一的功能，都是在外壳上生长，应当被质疑。**

### 5.2 分层（按寿命从长到短）

```text
format + verifier   —— 无宿主依赖，纯文本 + 一个校验函数
core (Measure / F)  —— 任意语言实现，通过 conformance suite
adapters            —— 工具包装，各自带 provenance
host bindings       —— MCP server / skill / CLI / notebook，随时可换
```

### 5.3 工作量的真实配比

schema 与状态机是几天到两周的工程；`R` 的构造与 `V` 的独立性是数月的研究。demo 现在把 100% 的复杂度花在前者、0% 在后者。架构定稿时若代码里的权重还是这样，产物会漂亮、可运行，但不回答任何一个原始问题。

---

## 6. 未完成 / 下一步

按优先级：

1. **跑 `cheapest_refutation_of_the_certificate_semantics`**。一个抗原、几十条抗体、两种 `X`（CDR-H3 编辑距离 / ESM 余弦）、四档 `τ` = 8 次计算，无需训练。判 BROKEN（排序翻转）/ CORROBORATED（稳定且与外部标签一致）/ UNFALSIFIABLE（缺外部标签）。**这个实验决定架构是否需要收缩，应排在写代码之前。**
2. `build-domain-ontology`：冻结七槽的 JSON 类型、必填字段、三态（known/unknown/unfilled）。当前每槽都是 `additionalProperties: true`。
3. `audit-validator-independence`：把 `V` 从 `{coverage_threshold}` 扩成三元组，并给出证据强度降级规则。
4. `structural-transformation`：验证三个 adapter 是否真从同一内核推出，还是三个各自硬编码。
5. mead 层仍为空。89 条 son/dregs 没有一条结晶成提案；`context/2026-10-19-...-requirements.md` 第四节的任务清单（表征方式、指标定义、有效性检验、数据摸底、90–100 复核）**尚无一项被池子结论回应**。

---

## 7. 硬约束（违反会出错）

- **池根必须显式传**：`PYTHONIOENCODING=utf-8 python .claude/skills/odrerir/scripts/odrerir.py --root odrerir <new|index|check|stats>`。Windows 下不设 `PYTHONIOENCODING=utf-8` 会因 GBK 在 `⊑` 上抛 `UnicodeEncodeError`。
- **`relation` 只写 cover-only 边**（Hasse 图）。能被链推出的边会被 `check-transitivity` 拒绝。
- **`relation` 段不允许任何非 `- [[slug]]: A <op> B.` 的行**，包括括注。
- **`lineage` 里的 URL 必须写成 `<https://...>`**（markdownlint MD034）。检查器已支持剥尖括号；`.claude/` 不提交，换机后需重新打补丁。
- **slug 是 id**：改标题 = 重命名，必须在同一次编辑里改掉所有指向它的 `[[slug]]`。
- **不要为了消传递冗余去改既有记录的边**。本轮试过，会让既有断言的语义被链式推导替代；全部回退，改为新记录挂自身最近父节点。
- **`.claude/` 不 commit**（`.gitignore` 已排除）。
- **`odrerir/.obsidian/graph.json` 被 Obsidian 运行时从内存覆盖**。改前先确认 Obsidian 已退出。
- **`core.autocrlf=true`** 会让部分 `.md` 显示 modified 而内容逐字节未变。用 `git diff --exit-code` 或 md5 证伪，不要当真实改动提交。
- **推送、删除、改外部状态前先确认**。用户此前拒绝过 `taskkill` / `tasklist` 一类进程操作。
- **markdownlint**：`odrerir/` 已清到只剩两条（都在 `bodn/`，原始材料按池规则不校验）。MD013 行长度全池 474 处、全仓 1086 处，用户明确表示「这样就行」，**不要主动去折行**。`context/` 里还有 MD009/MD012/MD032 等，本轮未动，也不在范围内。

---

## 8. 可用资源

- `odrerir/` 池：89 son / 16 dregs / 9 bodn / 14 tools。
- `odrerir/tools/`：MMseqs2、Foldseek、US-align、HMMER、HHsearch、InterProScan、zsasa、FreeSASA、Faiss、cuVS 等 14 份测量工具记录 —— 是 `X` 的实现来源，但工具名不构成相似性定义。
- `context/`：会议转写、8 节文献调研（235 条目 / 222 独立文献）、数据集索引、Codex 对话、插件设计、demo。
- Skills：`odrerir`（容器规则）、`research-catalog`（51 tactics）、`ponytail`（本会话全程 full，控制实现规模）。

---

## 9. 一句话交接

方向已定：证书语义成立，demo 的接缝正确但内核空、分层错。**下一步不是写更多代码，是跑那个一小时的 8 格点实验**——它决定架构是需要收缩还是需要展开。
