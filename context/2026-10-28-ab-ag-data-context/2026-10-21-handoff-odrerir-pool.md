---
tags:
  - context
---

# Handoff — odrerir 池：状态与下一步

写于 2026-10-21。给接手的 agent：读完这一份即可继续，不需要重读对话历史。

- 仓库：`G:\OUROBOROS-AI4S\abag-diversity`，`origin` = <https://github.com/ouroboros-ai4s/abag-diversity.git>（private），分支 `main`，HEAD `c474e96`
- 池根：`G:\OUROBOROS-AI4S\abag-diversity\odrerir`

---

## 1. 这个仓库在做什么

大项目里的一个小问题：**抗原-抗体数据的多样性如何定义、量化、并验证其有效性。**

它服务两个下游决策（完整版见 `context/2026-10-19-abag-diversity-problems-tasks-requirements.md`）：

1. 数据要收集到什么规模（阶段性目标是每年约 90–100 个抗原，够不够未知）；
2. 现有开源数据在多样性上是否已经高度重复（若重复，收集计划要调整）。

`odrerir/` 是这件事的**原料池**：把文献与推导得到的原子命题按固定 schema 存成记录，带 `[[slug]]` 因果边，组成一张可校验的有向图。它不是论文，不是知识库，是**待加工的判断集合**。

---

## 2. 目录与文件职责

| 路径 | 是什么 |
| --- | --- |
| `odrerir/bodn/` | 原始材料，9 个文件。只要求首行 `# <Title>`，不校验、不索引 |
| `odrerir/son/` | 原子命题，59 条，`<slug>.md` |
| `odrerir/dregs/` | 被降级的命题，15 条，schema = son + `spill` |
| `odrerir/mead/` | 成品 / 提案，**0 条，至今为空** |
| `odrerir/INDEX.md` | 生成物，只由 `odrerir.py index` 写，不要手改 |
| `context/2026-10-20-diversity-literature-survey.md` | 8 节文献调研，235 条目 / 222 独立文献。`son/` 的 48 条 survey 记录全部源自它 |
| `context/2026-10-19-ai-meeting-notes-weekly-algorithm-research-discussion.md` | 会议转写 |
| `context/2026-10-19-abag-diversity-problems-tasks-requirements.md` | 从会议里抽出的问题 / 任务 / 需求，是 North Star 的书面形式 |
| `context/2026-10-21-son-qc-rubric-and-ledger.md` | 评分 rubric 的完整版本史 + 逐条分数矩阵 |
| `assets/synthwave84-palette.csv` | Obsidian 主题调色板，取色用 |

---

## 3. 池的当前数字（已实测，非记忆）

```
记录      74  = son 59 + dregs 15 + mead 0
relation  73 行 = 63 条有序边（⊑ 42 / ⊒ 21）+ 10 条 ∥（kind: compatibility）
有序子图   68 节点 / 63 边 / 高度 6 / 41 根 / 11 叶 / 1 个弱连通分量
孤立节点   0
```

**6 条记录只出现在 ∥ 边上，不在有序子图里**：`pair_novelty_requires_four_role_specific_exposure_states`、`paratope_prediction_is_antigen_agnostic`、`sample_frequency_inflates_dominance_by_uncovered_mass`、`similarity_split_score_drops_do_not_identify_leakage`、`sufficient_sampling_returns_records_not_antigens`、`unseen_shared_epitopes_bias_overlap_downward`。schema 允许（∥ 不闭合传递），但意味着 `stats` 的高度 6 只描述有序子图。

`odrerir check` 12 项全 ok。唯一输出是 `check-relation-causality` 的 WARN —— 同批记录 `time` 相同（2026-10-20 / 2026-10-21），`A.time >= B.time` 成立但先后未定义。**这些 WARN 是良性的**，不要为消 WARN 改日期。

---

## 4. 两条 tag，互斥

```
48 条 son   → 2026-10-20-diversity-literature-survey   （文献调研产出）
11 条 son   → 2026-10-21-corollary                     （从已有记录推导出的推论）
15 条 dregs → 2026-10-20-diversity-literature-survey
```

tag 不相交是用户明确要求的，不要给 corollary 补上 survey tag。

corollary 的 11 条**没有 `qc:` 字段** —— 评分那一轮只覆盖 survey 的 63 条，corollary 是之后写的。若要做 QC，需先决定它们是否入同一 rubric。

Obsidian 图配色（`odrerir/.obsidian/graph.json`，四组 query 互斥，因此不依赖匹配优先级）：

| query | 色 | 数量 |
| --- | --- | --- |
| `path:dregs/` | `#614E83` | 15 |
| `path:INDEX.md` | `#3A3646` | 1 |
| `tag:#2026-10-21-corollary` | `#E88477` | 11 |
| `tag:#2026-10-20-diversity-literature-survey` | `#745D9E` | 48 |

**坑一：Obsidian 运行时会把 `graph.json` 从内存覆盖回去。** 改这个文件前先确认 Obsidian 已退出，否则改动会被吃掉（已踩过一次）。
**坑二：`core.autocrlf=true` 会让部分 `.md` 显示为 modified 而内容逐字节未变。** 用 `git diff --exit-code` 或 md5 证伪，不要当成真改动提交。

---

## 5. 11 条 corollary 是什么

推导方式统一为「在已有约束上做合取 / 归谬 / 实例化 / 提升」，不是头脑风暴。每条都写了 `lineage`（指向父记录的 `[[slug]]`）与 `relation`（逻辑算子）。

| slug | 一句话 |
| --- | --- |
| `redundancy_undecidability_splits_into_computational_and_observational` | 「未决」要拆成计算性（加算力可解）与观测性（只能加标注），两者误差方向相反，混算得出的数无意义 |
| `redundancy_reference_sets_are_declarations_not_parameters` | 同一批查询、同一阈值，换参考库可使冗余率从 3/3 变 0/3；冗余率是声明不是参数 |
| `duplicate_is_not_a_property_of_the_dataset` | 对非单射的测量，「重复」没有取值。未决因此有第三种：表征性，不可归约 |
| `held_out_certificates_are_relative_to_a_declared_validator` | 留出集判决是三元组（留出集, 判定器, 通过条件）；证书强度 ≤ 留出集独立性 |
| `validator_fit_on_the_reference_certifies_membership_not_departure` | 在参考集上拟合的判定器只能证明「属于」，不能证明「偏离」 |
| `diversity_reports_need_three_independent_field_classes` | 计数单位 / 测量对象 / (q, 权重) 三等分且**不可互相补偿**，缺一报告即不可解释 |
| `model_scores_add_a_fourth_undeclarable_field_class` | 模型分数引入第四类字段（模型身份、语料版本、暴露状态、规模档），可取「未知」，只能用来降级结论类型 |
| `surface_metric_computability_and_claim_strength_run_opposite` | 指标的输入要求与它能支撑的结论强度成反比；「全部记录都打了分」是假覆盖，分母必须是具备该输入档的记录 |
| `epitope_object_choice_can_flip_panel_rankings` | 表位对象（contact / escape / …）这个轴在 (q, w) 之外；同一组 q 下两个对象给出相反的面板排名 |
| `overlap_identity_fails_on_two_independent_axes` | 重叠同一性在命名空间（可用映射修复）与有效支撑（不可修复，只能量化）两个轴上各自失败 |
| `coverage_forecast_uncertainty_is_model_family_choice_not_sampling_error` | 覆盖外推的不确定性由模型族选择决定，不是采样误差；更多数据收窄两条带但不会让它们合并 |

另有 1 条从 dregs 复活：`pair_novelty_requires_four_role_specific_exposure_states`（qc 65）。复活时删掉了原文三个无出处的百分比（19.2% / 49.2% / 31.6% / 99%），改成 s4 §10 实际支持的定性表述，并删掉了 `## spill`。

---

## 6. 评分那一轮做了什么（survey 的 63 条）

完整口径见 `context/2026-10-21-son-qc-rubric-and-ledger.md`，这里只记结论与**实测到的偏差**。

- rubric：11 维，F 层 6 维（形式）+ S 层 5 维（内容），加权，非补偿式一票否决，`qc:` 只写总分。
- 版本史 v1→v7。v7 是关键口径变更：**S2（反例）分「推论型 / 经验型」两轨**。理由是池子记录洞见与推论，不记录实验结果；一条推导只要链可复核即有价值。9 条因此升到 keep，正文一字未改。
- 实测分档：**keep 42 / revise 6 / drop 15**（`son` 中 qc ≥ 80 有 42 条，65–79 有 6 条；`dregs` 15 条全部 ≤ 65）。

**ledger 里有两处数字已经过期，接手时不要照抄：**

1. §八 表头写 `revise 5 / drop 16`，实际是 `revise 6 / drop 15`。差的第 6 条 revise 是 `pair_novelty_...`（qc 65），它在 ledger 定稿后才从 dregs 复活，§8.3 的 5 行表没有更新。
2. §十一 写「17 条 drop 档仍留在 son」，实际 `son/` 中 qc < 65 已为 0 条，全部已移入 `dregs/`。

这 5 条 revise 档（qc 65–79）仍有已知缺陷，正文未改：

| QC | 记录 | 缺什么 |
| ---: | --- | --- |
| 76 | `novel_sequence_count_bounds_novel_binding_mode_count` | F4 / F5 是纯代数定理硬凑的两栏 |
| 74 | `predicted_epitope_field_is_a_reference_panel_marginal` | S3 / S4 / S5：缺条件方向分判与具名替代的排除 |
| 71 | `epitope_partitions_are_not_axiomatically_nested` | F4 / S3：只有否定结论，无正面判据 |
| 75 | `epitope_diversity_rankings_depend_on_weighting` | F3 / F4 / S4：边界与证伪段偏弱 |
| 70 | `predicted_structures_add_no_classes_beyond_the_reference` | S5：lineage 三条均未在正文直接使用 |

以及 `pair_novelty_...`（65）在 v7 口径下仍是最低分，是否再修未定。

---

## 7. 本轮改过的 skill（重要，会影响后续记录）

`odrerir` skill 原来只允许 `mead` 用 `[[slug]]` 作为 lineage 来源，`son` / `dregs` 只能指向 `../bodn/*.md` 或 URL。推论记录必须能指父记录，所以按用户指令（选项 B）修了 skill 本身。

**改动**：lineage 的任意一行若匹配 `[[slug]]`，即解析为父记录引用，不再看目录。同时补上两个洞 —— 自指报错；`mead` 不得指向另一个 `mead`。

**三处同步**：`scripts/odrerir.py` 的 `cmd_check_lineage`、`references/schema.json` 的 lineage 契约、`SKILL.md:57` 的散文。语义明确为：**lineage 记 provenance，连接多个父记录的逻辑算子写在 `relation`，不写在 lineage。**

落点两个：

- `G:\OUROBOROS-AI4S\abag-diversity\.claude\skills\odrerir\` —— **`.claude/` 被 gitignore，这份改动只存在于工作区，未 commit，也不会被 push。** 换机器或重开会话若 skill 不在，行为会回退。
- `G:\BABELIUM\odrerir\skills\odrerir\` —— 已同步并推送到 <https://github.com/babelium/odrerir.git>（commit `c9ee842`）。**那份才是上游。**

---

## 8. 下一次会话的方向（供参考，均未开工）

用户上一轮的意图是「63 条不足以支撑 diversity 研究，要从池子里继续长东西」。已长出 11 条并闭合成单一连通分量。自然的候选：

1. **mead 层仍是空的。** 74 条 son/dregs 没有一个结晶成提案；`requirements.md` 第四节的任务清单（表征方式、指标定义、有效性检验流程、数据摸底、「90–100 抗原/年」复核）没有任何一项被池子的结论回应过。
2. **第三批推论。** 现有 11 条集中在「冗余 / 重复」与「报告字段」两条线；`epitope_object_choice_can_flip_panel_rankings` 与 `surface_metric_computability_...` 打开的「对象轴 vs 指标轴」还没被推到底。
3. **对 5 条 revise 档做定向修订**（第 6 节表），这是唯一有明确缺陷清单的活。
4. **corollary 的 QC。** 11 条没有 `qc:`，是否并入同一 rubric 未定。

---

## 9. 不变的约束（违反会出错）

- **池根必须显式传。** `--root` 从不推断，没有配置文件、没有环境变量。命令形态（在仓库根执行）：
  ```
  PYTHONIOENCODING=utf-8 python .claude/skills/odrerir/scripts/odrerir.py --root odrerir <new|index|check|stats>
  ```
  Windows 下不设 `PYTHONIOENCODING=utf-8` 会因 GBK 编码在 `⊑` 上抛 `UnicodeEncodeError`。
- **`relation` 只写 cover-only 边**（Hasse 图）。任何能被链推出的边都会被 `check-transitivity` 拒绝 —— 本轮被这条拒了四次。
- **`relation` 段不允许任何非 `- [[slug]]: A <op> B.` 的行**，包括括注。要解释边为什么被删，写进 `## description`。
- **slug 是 id。** 改标题 = 重命名，必须在同一次编辑里改掉所有指向它的 `[[slug]]`。
- **`.claude/` 不 commit**（用户明确要求，且已在 `.gitignore`）。
- **推送、删除、改外部状态前先确认。** 用户此前拒绝过 `taskkill` / `tasklist` 一类进程操作，不要未经要求重试。
- 对外部仓库的推送已授权过一次（`ouroboros-ai4s/abag-diversity` 已推送完成）。不要再推，除非被要求。

---

## 10. 建议下一位使用的 skills

按顺序，前两个是必需的：

1. **`odrerir`** —— 容器规则。存记录、跑 check、看 schema 都靠它。池根要显式给。
2. **`ponytail`** —— 本会话全程生效（full）。控制实现规模，别加没被要求的东西。
3. **`research-catalog`** —— 若下一步是继续推推论或做方案，用它选 tactic，再加载选中的 tactic body。本轮用过的：`synthesize-literature-evidence`、`audit-benchmark-validity`、`map-validity-envelope`、`audit-convergence-independence`。
4. **`construct-argument-map`** / **`derive-consequences`** —— 若要把 11 条推论串成一条论证线而非散点。
5. **`write-research-spec`** —— 若要把池子转成 mead 层的可执行提案。
6. **`rank-candidates`** + `define-criteria` + `aggregate-ranking` + `assess-sensitivity` —— 仅在要重跑 QC 时需要；rubric 已在 ledger 定稿，重复劳动没有意义。
