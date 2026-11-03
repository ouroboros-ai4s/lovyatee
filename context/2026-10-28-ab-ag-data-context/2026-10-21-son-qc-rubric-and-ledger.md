---
tags:
  - context
---

# Son Pool QC — Rubric, Protocol, and Ledger

日期：2026-10-21。对象：`odrerir/son/` 全部记录。

## 一、使用的 skill

本文件之外的打分口径全部由下列 skill 的强制条款推导，不引入未经 skill 背书的维度。

| skill | 在本工作中的角色 | 被采用的强制条款 |
| --- | --- | --- |
| `rank-candidates` | 主框架（mode：`full-ranking` + `non-compensatory-screening`） | 判据方向与缺失值策略须先声明；硬约束不得当作可补偿分数；排名须报稳定性 |
| `define-criteria` | 维度推导 | 3–12 个判据；每个须有 name / definition / unit / 方向；不得重叠到重复计数 |
| `normalize-comparison-scale` | 分维换到 0–100 同尺度 | 方向在变换前后一致；缺失不得静默插补 |
| `score-object` | 逐条逐维打分 | 每维须带证据引用与一句话理由；rubric 由调用方提供，不由 skill 提供 |
| `aggregate-ranking` | 加权合成 | 权重和为 1（±0.001）；并列按预先声明的 tie-break |
| `assess-sensitivity` | 权重扰动 | 每维 ±20% 扰动，≥4 场景，报 Kendall τ；stable ≥0.8 / sensitive 0.5–0.8 / unstable <0.5 |
| `derive-consequences` | S1 判据来源 | 任何终点不得在没有中间推导步的情况下发出 |
| `generate-counterexample` | S2 判据来源 | 反例须满足声明作用域再违反结论；域外个例不算反例 |
| `evaluate-necessity-sufficiency` | S3 判据来源 | 必要性需缺席/移除对照，充分性需存在/干预对照，两者分开报告 |
| `audit-explanatory-compression` / `classify-simplicity-evidence` | S4 判据来源 | earned 须压缩至少一个独立事实并排除至少一个替代；禁止按篇幅判分 |
| `assess-construct-validity` / `audit-validator-independence` | S5 判据来源 | 每条有效性判断须引用具体条目；验证器与被验对象共享假设即为 pass-by-construction |
| `test-risky-prediction` | S6 判据来源 | 预测须能与至少一个替代解释区分；事后解释不算前瞻约束 |
| `odrerir` | 只负责结构合法与非侵入 | 明确声明 `No scoring or ranking of ideas`；QC 只写 frontmatter，不改章节、不改 slug |

未被采用：`pairwise-ranking`（63 条两两为 1953 对，成本不成比例）、`portfolio-optimization`（此处不需要子集）、`check-dominance`（12 维下几乎不存在严格支配）。

## 二、分层与权重

结构合法（原 F1）不计分，改为前置机械修复——结构错误是缺陷不是质量差异，进入分数会污染排序。

| 层 | 维度 | 权重 | 100 | 50 | 0 |
| --- | --- | ---: | --- | --- | --- |
| F | F2 单命题 | 8 | 一句话概括不失真 | 需两个从句 | 承载两个独立断言 |
| F | F3 边界显式 | 7 | 有作用域且有失效条件 | 只有其一 | 无 |
| F | F4 可证伪段 | 8 | 有，且指明观测量 | 有，但不可观测 | 无 |
| F | F5 可操作要求 | 6 | 指明下游须报告什么 | 泛泛要求 | 无 |
| F | F6 原子非冗余 | 3 | 与池内无实质重叠 | 与一条部分重叠 | 是另一条的改写 |
| S | S1 推理有效 | 14 | 每步可回指前一步 | 一处跳步 | 结论不由前提得出 |
| S | S2 反例具体 | 14 | 域内、可构造、给出数值或结构 | 存在但未构造 | 未给 |
| S | S3 必要/充分分判 | 12 | 两个方向都判 | 只判一个 | 混用 |
| S | S4 压缩挣得 | 12 | 压缩独立事实 + 排除具名替代 | 只排除替代 | 换名重述 |
| S | S5 构造效度 | 13 | 被引条目确证该断言 | 引用部分支持 | 循环或无关 |
| S | S6 区分力 | 3 | 排除了一个具名替代 | 原则上可排除 | 与替代同真 |

合计 100；形式 32，内容 68。允许两档之间取值，但须在理由中说明为何不落任一档。

`QC = Σ wᵢ·sᵢ / 100`，sᵢ ∈ [0,100]。


## 二之二、v2 锚点（批 1 校准后修订）

批 1 的两名评分员在 11 维上给出总分 ρ = 0.54–0.92，但分维一致率很低：F6 ρ=0.18、F2 ρ=0.36、S2 ρ=0.36、S1 ρ=0.46、S6 ρ=0.50。原因不是评分员不严，而是锚点本身可两读。以下 6 维换成可机械判定的定义，仍是同一批 skill 的判据，只是把「怎样算」写死。

**F2 单命题**
删去所有「唯一作用是支撑主命题」的句子后若仅剩一个命题 → 100；若仍剩一个自带证伪条件的独立断言 → 0；主命题需两个从句才能说完、但两个从句不可分别证伪 → 50。

**F6 原子非冗余**（改为近机械）
看 `relation` 字段：有任一 `⊑/⊒/≺/≻/∥` 边 → 50（构造上即为部分重叠）；无边且正文无实质重述 → 100；本条主张已完全由另一条正文蕴涵 → 0。

**S1 推理有效**
逐段检查相邻两段：后段结论可否只凭前段已陈述的内容得到。另加一条 scope 检查：被引证据与标题断言必须是同一类量（计数对计数、比例对比例）。任一处不同类 → 至多 50。全段可回指且 scope 相符 → 100；一处归纳性跃迁（从个案推全称）→ 75；标题结论不由正文证据得出 → 0。

**S2 反例具体**（五档，取消中间值）
- 100：给出数值或完整指定的结构，无需新信息即可复算
- 75：给出文献中的具名实测实例且带数字
- 50：只给可能性陈述（「可以为零」「存在这样的划分」），无实例
- 25：只给误差方向，无实例
- 0：无

**S4 压缩挣得**（两条件合取）
压缩 ≥1 个独立经验事实 **且** 排除 ≥1 个具名替代 → 100；只满足其一 → 50；两者皆无（换名重述）→ 0。

**S6 区分力**
- 100：点名一个**对同一观察的竞争解释**，并给出排除它的论证
- 50：点名替代，但只以断言排除
- 0：未点名任何替代

「对同一证据的过强读法」不作为替代解释计入；替代必须是机制或路径层面另作解释者。

S3、S5、F3、F4、F5 的 ρ ≥ 0.88，锚点保留不变。


## 二之三、v3 锚点（批 1 二次校准后定稿）

v2 把 F2/F6/S2 收紧了，但 S1（ρ=0.42）与 S4（ρ=−0.12）仍未收敛，F2/F6/S6 也只到 0.6。根因是两个判据词没有定义：S1 的「量类相符」被逐条施加到全部引用，S4 的「独立经验事实」把方法学依赖也算进去了。v3 定死这两点，其余沿用 v2。

**S1 推理有效**——只检查两件事：
(a) 每一段结论是否只用前文已陈述的内容推出；
(b) **主证据**（即在 lineage 中被当作该断言直接支撑的那一条）与标题断言的量类是否一致。背景性引用不参与 (b)。
- 100：(a)(b) 皆成立
- 75：一处归纳性跃迁（从个案推全称），或主证据来自不同的受控条件（如不同结构集、不同协议）而正文未加限定
- 50：主证据与标题断言的量类不同（面积对计数、比例对类别数、工具对算子）
- 0：结论不由正文证据得出

**S4 压缩挣得**——(a) 是否把 ≥1 个**文献报告的**结果折进一个该文献未陈述的结论；(b) 是否点名一个替代读法/解释并有论证地排除。
- 定义性事实、方法学参数依赖、自推导公式 **不** 计为 (a)。
- 过强读法（对同一证据的夸大）**不** 计为 (b)，与 S6 一致。
- 100：(a)(b) 皆是；50：恰有一项；0：皆无（换名重述）。

**F2、F6 沿用 v2；S6 沿用 v2（过强读法不计）；S2 沿用 v2 五档。**


## 二之四、v4 锚点（S3 收口）

批 2 的 S3 分维 ρ=0.69、平均差 31.7，是最后一处未收口的判据。分歧来自「提到两个方向」与「对两个方向分别判定」被混为一谈。v4 只钉 S3，其余沿用 v3。

**S3 必要/充分分判**——只看正文有没有把「A 是 B 的必要条件」与「A 是 B 的充分条件」当成两件事分别给出判据：
- 100：两个方向各自给出判据或对照（例：证明合并不可能、拆分可能）
- 50：只判其中一个方向，或两个方向都提到但没有任何判据
- 0：全文不涉及条件方向

「提到两个方向但没有判据」算 50，不算 100。这一条是 v2/v3 未写死、导致 55 分分歧的那一处。

批 1–3 的 S3 按此规则由主控从两名评分员的理由文本重新判定，使三批可比；批 4 起直接在 prompt 中施加。


## 二之五、聚合规则（定稿）

**不做两评分员均值合成。** 三批的对比显示：均值会把 S2/S4 的 0–50 分歧折成 25–50，把该降的条目抬回 revise。改为：

1. 两个评分员独立打 11 维，互不可见。
2. 逐维算 Spearman ρ。ρ ≥ 0.8 的维度取均值；ρ < 0.8 的维度不由均值决定——主控阅读两份理由，按 v2–v4 锚点裁决，裁决值即为该维分数（分歧本身作为缺陷记录）。
3. 复核阈值：ρ ≥ 0.8 视为两评分员一致；0.5 ≤ ρ < 0.8 一律裁决；ρ < 0.5 视为该维度在本批未收敛，裁决并在 ledger 记名。
4. 总分按 11 维固定权重 100 分合成，再做否决与分档。
5. `QS3 的稳定化`：v4 后 S3 不再重打，由主控按规则直接判定（100 / 50 / 0），只判一次。

保留的已知缺陷：S3 与 F2 的分歧来自锚点解释而非测量噪声，裁决值带有主控偏好；所有裁决条目在附录逐个记录两名评分员的原始分与主控理由。


## 二之六、v6 修正（F6 锚点错误，批后复核）

v2 给 F6 写的规则是「`relation` 有任一 `⊑/⊒/≺/≻/∥` 边 → 50」。这条是错的，且与 §八 最初的设计口径直接冲突（原文：「与池内已有记录是否实质重复（relation 已表达的不算重复）」）。

理由：`⊑` 的含义是「A 是 B 的特例」，`∥` 是「互不细化」——两者都不是「重复」。relation 字段正是池子用来记录关系的手段，拿它当重复的证据，等于把「已经声明清楚的关系」当成缺陷。按 v2 规则，63 条里有 46 条被机械扣分，其中多数只是正常地声明了父子关系。

**修正后 F6**：只有正文对另一条构成实质重述（同一主张、无新增内容）才计 50。声明了 relation 边且正文有新增内容 → 100。

16 条保留 F6=50（正文确有重述），其余 47 条改为 100。总分变化 +1.5，两条跨档（`canonical_class_count_is_not_a_dynamical_state_count` 79.7→81.2，`unseen_shared_epitopes_bias_overlap_downward` 78.7→80.2），均升入 keep。

**这是一次批后改规则，且改动方向使分数上升。** 记录在此以便复核：若认为 F6 应保持 v2 的机械判法，则上述 13 条总分回到原值，drop/revise 分档不变（无一条跨档下降）。


## 二之七、v7 修正（S2 分两轨，采纳方口径）

本池的用途是记录洞见与推论，不是记录实验结果。v2 的 S2 锚点只承认「数值或完整指定的结构」，把自推导的推论一律压到 25–50，这与池子的用途不符 —— 一条正确且可读的推导，其价值不取决于有没有人做过对应实验。

v7 把 S2 拆成两轨，先判记录的**类型**，再按对应轨道给分：

| 类型 | 判据 | 100 | 75 | 50 | 25 | 0 |
| --- | --- | --- | --- | --- | --- | --- |
| **推论型** | 主张由定义、代数或逻辑推出，本身不依赖新观测 | 推导链完整、每步可复核，读毕能自行重算或复述 | 推导成立但有一步靠断言补桥 | 只有结论，推导缺失 | 只能给出方向 | 无 |
| **经验型** | 主张关于实测事实（某个量多大、某现象是否存在） | 给出数值或完整指定的结构，可复算 | 具名实测实例且带数字 | 只有可能性陈述 | 只给误差方向 | 无 |

类型由主控判定并写进 ledger；判错的记录按错轨打分，不得混用。写作时应当在正文自报类型（「我构造的」「待检验假设」「原文报告」），这一句本身不进分数，但它决定走哪一轨。

**这是一次放宽，且改动方向使分数上升。** 依据是用户 2026-10-21 的指令：不要求实验验证，推论亦可采纳，只需文本描述清楚。若日后要按实验标准重评，把推论型记录改回 v2 轨道即可，14 条中 9 条的分数会回落到 revise。

## 三、一票否决（non-compensatory）

任一触发，总分封顶 40，不参与加权：

1. lineage 指向的 bodn 路径不存在，或被引条目在正文中不支持该断言；
2. 正文没有任何可证伪内容，也无法从正文推出；
3. S2 与 S4 同时为 0（既无具体反例，又只是换名重述）。

## 四、分档

- ≥ 80：保留。
- 65–79：需要一次定向修订（通常是补 S2 或 S3）。
- < 65：降 `dregs`，`spill` 写明触发的维度。

## 五、执行协议

- Pass 0：`odrerir check` + frontmatter 检查，ERR 原地机械修复，不计入分数。
- Pass 1–2：63 条分 7 批（每批 9 条），每批起 2 个独立 scorer，互不可见，各打 11 维。
- Pass 3：逐维算两 scorer 的 Spearman ρ。ρ ≥ 0.8 取均值；0.5–0.8 由主控裁决并记录分歧；< 0.5 该维不进入总分，只报分项。
- Pass 4：否决 → 加权 → 分档 → 权重 ±20% 扰动（每维一次，其余按比例缩放保持和为 1），报总分排序的 Kendall τ。
- Pass 5：写回 `qc: <int>` 到 frontmatter；本文件追加结果。

## 六、写入格式

```yaml
---
tags:
  - 2026-10-20-diversity-literature-survey
qc: 82
---
```

只写总分，不写分项与分档 tag。分项矩阵只留在本文件的附录。

## 七、已知限制

- 除结构检查外全部维度都是判断型，分数只在同一批次与同一 rubric 版本内可比。
- 内容分由两个主体独立给出，仍不构成外部验证；绝对分值不应跨 rubic 版本比较。
- 锚定集（10 条，见附录）用于检测日后重评的漂移。

## 八、结果

打分日期 2026-10-21。63 条：**keep 42 / revise 5 / drop 16**，得分区间 40–95。

分数经过三个版本：

| 版本 | keep | revise | drop | 说明 |
| --- | ---: | ---: | ---: | --- |
| 首轮（v1–v6） | 13 | 34 | 16 | 依实验标准打分，S2 只认数值或完整结构 |
| 修订后（v6） | 33 | 14 | 16 | 34 条按缺陷逐维修订 |
| 采纳方口径（v7） | 42 | 5 | 16 | S2 分推论型/经验型两轨，见 §二之七 |

v7 的依据是池子的用途：记录洞见与推论，不是记录实验结果。一条推导只要文本写清楚，其价值不取决于有没有对应的实验。**这是口径变更，不是修订** —— 14 条在 v7 下升到 keep 的 9 条，正文一字未改，只是 S2 的判据换成了「推导链是否可复核」。

### 8.1 修订做了什么

34 条按打分指出的具体维度改，不重写。典型修法：

- **S3 = 0/50**：补「必要」与「不充分」两个方向各自的判据，各给一个可判的理由。
- **S2 = 12/25/50**：补可复算的构造或具名实测数值。
- **S4 = 0/50**：补「本条挣得的压缩」句，说明折入了哪个文献结果、排除了哪个具名替代。「自推导公式」与「方法学参数依赖」不算压缩。
- **F5 = 25**：补下游报告要求的具体字段。
- **lineage 编号错位与列出未用**：逐条回核并改正。

### 8.2 修订的可信度

修订由主控完成，有自我确认的风险。处置是两轮独立验证：

1. 第一轮两个 verifier 各复核 17 条，报「1 固定 / 11 部分 / 5 未固定」（另一组「2 / 11 / 4」）。
2. 第二轮 verifier 复核主控自行给出的 6 个分数，推翻 4 个，全部下调。
3. 两轮指出三处事实性错误（一处不可实现的集合、一处错位的编号移位、一处循环构造），已修正并重算。

### 8.3 剩余的 5 条 revise

| QC | 记录 | 缺什么 |
| ---: | --- | --- |
| 76.4 | `novel_sequence_count_bounds_novel_binding_mode_count` | F4=62、F5=58：这条是纯代数定理，「可证伪内容」与「可操作要求」两栏本来就不太适用，写成了硬凑 |
| 74.2 | `predicted_epitope_field_is_a_reference_panel_marginal` | S3=50、S4=50、S5=52：缺条件方向分判与具名替代的排除 |
| 70.6 | `epitope_partitions_are_not_axiomatically_nested` | F4=62、S3=50：只有否定性结论，没有正面判据 |
| 75.0 | `epitope_diversity_rankings_depend_on_weighting` | F3=60、F4=72、S4=58：边界与证伪段偏弱 |
| 70.0 | `predicted_structures_add_no_classes_beyond_the_reference` | S5=45：lineage 三条均未在正文直接使用 |

### 8.4 降级

16 条在 `dregs/`，slug 不变，`relation` 边照旧解析。每条 `spill` 写了降级理由与复活条件。

## 九、数字与引语回核（主控逐条）
# 数字与引语回核（主控，2026-10-21）

| 记录 | 主张 | 回核结果 |
| --- | --- | --- |
| epitope_community_count_is_assay_resolution_limited | lineage「第 5、6、7 条的分组数（7 / 6 / 五类）」 | s1 #5 Hastie=七个社区 ✓；#6 Cao=六个表位组 ✓；#7 Smith 2004 抗原制图**无任何分组数**，「五类」无出处 ✗ |
| contact_matching_bounds_can_leave_redundancy_undecided | 引 Caprara 2004「原则上难以优化，但在相关蛋白上可以高精度计算」 | s3 #9 摘要为「把结构对齐形式化为最大接触图重叠问题并用整数规划精确求解…理论最优基准」，**无此引语**。可能出自原文而非 bodn 摘要，属不可核验的归属，非矛盾 |
| fixed_coverage_enables_guaranteed_representative_selection | 引 Holm & Sander「在多项式时间内最好（在某些假设下）」 | s4 #3 摘要为「从大规模蛋白序列集合中去除近邻冗余…冗余阈值的选择在此已被显式讨论」，**无此引语**。同属不可核验归属 |
| differential_task_advantage_needs_an_interaction_test | 构造「两个任务上 A−B 的效应量都为正、都在各自置信区间内与零不可区分…此时逐任务看是一个显著一个不显著」 | **自相矛盾**：CI 覆盖零即两侧都不显著，推不出「一个显著一个不显著」。S2 判 25 |

结论：三类问题中只有第一类构成 lineage 内容错误（可判 V1 级）；第二、三类是不可从池内核验的原文归属，不是矛盾。三处都应在下一轮修订时回原文确认。

## V1 否决（确认）

`pair_novelty_requires_four_role_specific_exposure_states`：正文写「Park & Marcotte 在 PPI 上量出了…三类分别占 19.2%、49.2%、31.6%，而随机交叉验证的测试集有超过 99% 落在第一类」。回核：

- s4 第 10 条（Park & Marcotte 2012）摘要只有「都未出现、出现一个、都出现，对应难度截然不同的任务」，**无任何百分比**。
- 全仓库 `bodn/` 与 `context/` 检索 `19.2` / `49.2` / `31.6`，无一处是该三分比例的来源（命中项均为文件大小与 CSV 字段）。
- 数字以事实语气写出，非标注为推断。

判定 V1 成立，总分封顶 40。

## 第二批回核（主控）

| 记录 | 主张 | 回核结果 |
| --- | --- | --- |
| richness_bounds_do_not_transfer_to_coverage | lineage「第 7 条（Chao 2009…其目标比例由同一批稀有类估出）」 | s8 #7 写「估计为检测到渐近丰富度的**任意比例**（含 100%）所需的最小额外个体…它需要的是稀有类别的频次」。目标比例是使用者选定的，不是从稀有类估出的；从稀有类估出的是渐近丰富度本身。**措辞错误，循环性论点本身仍成立**，需改写该句 |
| richness_bounds_do_not_transfer_to_coverage | 「第 10 条（Orlitsky 2016）的最优性范围」 | s8 #10 只写「对所有 t 都有效的估计量类…该范围是最优的、其均方误差接近最优」。记录补入的「已知物种集」「i.i.d. 样本」「平方误差」三项前提**不在条目内**，属外加 |
| richness_bounds_do_not_transfer_to_coverage | 可证伪段「Chao1 型下界…不低于真实覆盖比例（以质量计）」 | 该检验把计数与质量直接相比，正是本条正文自己判为量类错误的比较。**可证伪段自身失效**，须重写 |


## 十、可复现记录

本轮评分的全部数据已内联到本文件，`.qc/` 工作目录已清理，不再需要外部文件。

### 10.1 聚合算法

1. 两名评分员独立打 11 维（互不可见），整数 0–100。
2. 逐格比较：`|A − B| < 30` 取均值；`|A − B| ≥ 30` 由主控按 §二之二–二之四 的锚点裁决，裁决值取代均值。分歧格共 79 个，逐格列出在 10.3。
3. 加权：F2=8, F3=7, F4=8, F5=6, F6=3, S1=14, S2=14, S3=12, S4=12, S5=13, S6=3，和为 100。
4. 总分 = Σ w·s / 100；一票否决触发则封顶 40。
5. 分档：≥80 keep，65–79 revise，<65 drop。

复现只需 10.2 的矩阵与 10.3 的裁决表，无需脚本。10.2 已是修订轮后的最终值；首轮值见 8.2 的说明。

### 10.2 每条的 11 维最终值

（v7 轨道修正后；S2 分推论型/经验型两轨，见 §二之七。总分保留一位小数，`qc:` 字段取四舍五入到整数。）

| 记录 | 总分 | 分档 | F2 | F3 | F4 | F5 | F6 | S1 | S2 | S3 | S4 | S5 | S6 |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `polyclonal_escape_profiles_are_mixture_measurements` | 94.6 | keep | 95 | 65 | 100 | 100 | 100 | 95 | 100 | 100 | 95 | 92 | 92 |
| `joint_pair_redundancy_requires_one_reference_witness` | 91.7 | keep | 100 | 100 | 100 | 100 | 98 | 100 | 100 | 95 | 50 | 90 | 90 |
| `chao1_lower_bound_moves_with_the_threshold` | 90.4 | keep | 95 | 98 | 98 | 98 | 100 | 95 | 100 | 100 | 50 | 92 | 65 |
| `interface_redundancy_verdicts_require_declared_and_calibrated_search_scope` | 89.5 | keep | 92 | 92 | 95 | 98 | 100 | 90 | 100 | 100 | 50 | 92 | 88 |
| `peptide_library_data_cannot_be_pooled_into_conformational_coverage` | 89.4 | keep | 95 | 100 | 100 | 100 | 100 | 90 | 50 | 100 | 95 | 92 | 95 |
| `sample_frequency_inflates_dominance_by_uncovered_mass` | 87.6 | keep | 88 | 100 | 98 | 100 | 100 | 88 | 100 | 100 | 50 | 78 | 75 |
| `paired_chain_effective_diversity_loses_mutual_information` | 87.0 | keep | 50 | 100 | 100 | 75 | 100 | 98 | 100 | 100 | 50 | 92 | 95 |
| `bio_foundation_model_data_scaling_has_no_established_law` | 86.7 | keep | 100 | 100 | 100 | 100 | 100 | 95 | 75 | 100 | 50 | 88 | 50 |
| `blocking_certifies_difference_not_identity` | 86.6 | keep | 100 | 100 | 100 | 100 | 50 | 88 | 50 | 100 | 100 | 75 | 100 |
| `canonical_class_count_is_not_a_dynamical_state_count` | 86.6 | keep | 100 | 100 | 100 | 75 | 50 | 90 | 50 | 100 | 88 | 100 | 80 |
| `quality_filtering_has_metric_dependent_diversity_effects` | 86.0 | keep | 75 | 92 | 90 | 100 | 92 | 88 | 100 | 100 | 50 | 88 | 62 |
| `design_pipeline_success_does_not_establish_fingerprint_sufficiency` | 85.8 | keep | 32 | 90 | 98 | 98 | 95 | 85 | 100 | 100 | 72 | 86 | 88 |
| `interpolation_is_free_extrapolation_is_not` | 85.7 | keep | 80 | 88 | 95 | 98 | 50 | 88 | 100 | 100 | 50 | 90 | 72 |
| `contact_overlap_is_a_tolerance_not_an_equivalence` | 85.4 | keep | 98 | 70 | 90 | 95 | 100 | 98 | 100 | 100 | 50 | 70 | 65 |
| `residue_score_field_does_not_determine_patch_count` | 85.2 | keep | 80 | 98 | 98 | 100 | 100 | 82 | 100 | 100 | 50 | 72 | 75 |
| `antibody_diversity_counting_unit_is_declared_not_derived` | 84.9 | keep | 100 | 88 | 100 | 100 | 100 | 95 | 100 | 50 | 50 | 88 | 100 |
| `escape_spectra_are_indexed_by_the_mutation_library` | 84.9 | keep | 95 | 90 | 92 | 92 | 100 | 80 | 50 | 100 | 88 | 92 | 80 |
| `interface_diversity_metrics_require_metric_specific_observability` | 84.9 | keep | 92 | 88 | 65 | 98 | 100 | 85 | 100 | 100 | 50 | 88 | 65 |
| `accuracy_based_redundancy_estimates_require_independent_calibration` | 84.5 | keep | 50 | 100 | 100 | 62 | 50 | 88 | 100 | 100 | 62 | 100 | 50 |
| `clonotype_threshold_is_not_a_specificity_threshold` | 84.3 | keep | 92 | 92 | 95 | 95 | 100 | 82 | 75 | 100 | 50 | 98 | 50 |
| `contact_matching_bounds_can_leave_redundancy_undecided` | 83.9 | keep | 88 | 95 | 92 | 95 | 95 | 95 | 50 | 100 | 50 | 100 | 100 |
| `germline_motif_predicts_public_clone_recurrence` | 83.8 | keep | 88 | 92 | 95 | 92 | 50 | 70 | 100 | 100 | 50 | 95 | 50 |
| `protein_lm_scale_has_no_monotone_fitness_benefit` | 83.5 | keep | 88 | 100 | 98 | 98 | 90 | 95 | 55 | 100 | 50 | 90 | 78 |
| `vhh_is_out_of_domain_for_fab_calibrated_instruments` | 83.4 | keep | 100 | 100 | 95 | 88 | 100 | 82 | 75 | 50 | 90 | 85 | 90 |
| `cross_reactivity_breadth_is_not_a_function_of_the_antibody_alone` | 83.4 | keep | 100 | 82 | 88 | 92 | 100 | 80 | 50 | 100 | 88 | 82 | 88 |
| `pretraining_exposure_limits_model_based_diversity_validation` | 83.3 | keep | 85 | 100 | 98 | 100 | 90 | 95 | 50 | 100 | 50 | 92 | 90 |
| `interface_filters_certify_reference_likeness_not_novelty` | 83.2 | keep | 95 | 92 | 95 | 82 | 100 | 62 | 88 | 75 | 88 | 80 | 88 |
| `cross_antigen_contact_overlap_requires_declared_correspondence` | 83.1 | keep | 50 | 88 | 98 | 98 | 98 | 78 | 100 | 100 | 62 | 80 | 50 |
| `antigen_state_ensemble_defines_the_epitope_denominator` | 82.5 | keep | 100 | 100 | 100 | 100 | 50 | 100 | 50 | 50 | 100 | 100 | 0 |
| `scaling_exponents_are_not_transportable_across_data_regimes` | 82.4 | keep | 60 | 98 | 100 | 52 | 100 | 88 | 100 | 100 | 50 | 80 | 62 |
| `sequence_diversity_bias_has_no_fixed_sign` | 82.1 | keep | 88 | 100 | 100 | 88 | 50 | 78 | 100 | 50 | 88 | 71 | 85 |
| `collection_breadth_requires_a_held_out_antigen_assay` | 82.0 | keep | 95 | 98 | 95 | 95 | 100 | 80 | 50 | 100 | 50 | 98 | 75 |
| `sufficient_sampling_returns_records_not_antigens` | 81.9 | keep | 80 | 98 | 98 | 100 | 50 | 88 | 100 | 65 | 50 | 81 | 88 |
| `specificity_labels_partition_the_panel_not_the_epitope_surface` | 81.9 | keep | 92 | 98 | 95 | 60 | 100 | 88 | 92 | 100 | 50 | 58 | 90 |
| `differential_task_advantage_needs_an_interaction_test` | 81.9 | keep | 50 | 85 | 98 | 98 | 50 | 78 | 100 | 100 | 50 | 92 | 60 |
| `footprint_overlap_does_not_predict_escape_spectrum` | 81.7 | keep | 95 | 88 | 95 | 88 | 100 | 88 | 75 | 75 | 50 | 90 | 85 |
| `single_linkage_bridges_distinct_clones` | 81.7 | keep | 98 | 92 | 65 | 55 | 100 | 95 | 98 | 100 | 50 | 64 | 85 |
| `richness_ranking_is_threshold_ranking` | 81.5 | keep | 90 | 100 | 98 | 100 | 100 | 80 | 100 | 62 | 50 | 72 | 82 |
| `sampling_redundancy_and_biological_convergence_are_not_identifiable_from_database_frequencies` | 80.9 | keep | 80 | 100 | 100 | 78 | 100 | 85 | 95 | 52 | 60 | 85 | 72 |
| `clone_and_epitope_partitions_require_independent_witnesses` | 80.7 | keep | 50 | 95 | 95 | 80 | 50 | 80 | 100 | 100 | 50 | 88 | 50 |
| `similarity_split_score_drops_do_not_identify_leakage` | 80.3 | keep | 92 | 98 | 95 | 92 | 100 | 88 | 52 | 100 | 50 | 82 | 55 |
| `unseen_shared_epitopes_bias_overlap_downward` | 80.2 | keep | 95 | 98 | 95 | 100 | 100 | 90 | 70 | 62 | 50 | 91 | 50 |
| `novel_sequence_count_bounds_novel_binding_mode_count` | 76.4 | revise | 100 | 100 | 62 | 58 | 50 | 100 | 100 | 50 | 50 | 65 | 100 |
| `epitope_diversity_rankings_depend_on_weighting` | 75.0 | revise | 72 | 60 | 72 | 92 | 50 | 78 | 75 | 100 | 58 | 75 | 72 |
| `predicted_epitope_field_is_a_reference_panel_marginal` | 74.2 | revise | 88 | 98 | 100 | 100 | 50 | 70 | 100 | 50 | 50 | 52 | 75 |
| `epitope_partitions_are_not_axiomatically_nested` | 70.6 | revise | 95 | 92 | 62 | 70 | 100 | 80 | 75 | 50 | 50 | 68 | 62 |
| `predicted_structures_add_no_classes_beyond_the_reference` | 70.0 | revise | 98 | 75 | 50 | 75 | 50 | 80 | 100 | 62 | 50 | 45 | 80 |
| `pair_novelty_requires_four_role_specific_exposure_states` | 65.4 | drop | 92 | 100 | 100 | 100 | 88 | 80 | 25 | 50 | 50 | 45 | 62 |
| `paratope_diversity_requires_antibody_format_calibration` | 64.9 | drop | 92 | 80 | 50 | 100 | 50 | 75 | 25 | 50 | 92 | 58 | 62 |
| `epitope_community_count_is_assay_resolution_limited` | 64.8 | drop | 50 | 50 | 50 | 88 | 50 | 68 | 88 | 50 | 78 | 58 | 58 |
| `canonical_class_criterion_has_two_readings` | 63.9 | drop | 100 | 38 | 25 | 100 | 50 | 100 | 100 | 0 | 50 | 75 | 0 |
| `epitope_diversity_estimators_need_cross_antigen_validation` | 63.5 | drop | 72 | 60 | 50 | 95 | 100 | 75 | 25 | 100 | 50 | 68 | 0 |
| `clustering_method_ranking_is_task_dependent` | 63.4 | drop | 50 | 98 | 95 | 95 | 50 | 78 | 52 | 50 | 50 | 45 | 55 |
| `lm_representations_compress_off_germline_variation` | 63.3 | drop | 50 | 78 | 88 | 100 | 100 | 80 | 12 | 50 | 50 | 88 | 50 |
| `cdr_class_map_is_not_a_function_in_either_direction` | 62.5 | drop | 12 | 95 | 78 | 95 | 50 | 95 | 62 | 0 | 50 | 92 | 50 |
| `paratope_prediction_is_antigen_agnostic` | 62.4 | drop | 100 | 88 | 92 | 38 | 100 | 85 | 12 | 50 | 50 | 60 | 75 |
| `annual_antigen_targets_require_marginal_interface_coverage_estimates` | 61.2 | drop | 0 | 100 | 100 | 100 | 50 | 50 | 50 | 50 | 62 | 75 | 50 |
| `epitope_diversity_needs_a_stability_profile` | 60.6 | drop | 50 | 88 | 58 | 98 | 100 | 78 | 45 | 50 | 50 | 48 | 50 |
| `epitope_diversity_is_a_joint_antigen_immune_background_property` | 60.1 | drop | 80 | 60 | 45 | 90 | 98 | 72 | 52 | 50 | 25 | 79 | 32 |
| `fixed_coverage_enables_guaranteed_representative_selection` | 59.9 | drop | 92 | 98 | 98 | 70 | 100 | 78 | 38 | 50 | 0 | 50 | 62 |
| `richness_bounds_do_not_transfer_to_coverage` | 57.9 | drop | 35 | 78 | 50 | 100 | 100 | 70 | 50 | 50 | 50 | 50 | 45 |
| `cdr_class_count_is_procedure_dependent` | 49.7 | drop | 50 | 50 | 25 | 100 | 50 | 62 | 50 | 0 | 75 | 62 | 0 |
| `coverage_standardized_epitope_richness` | 48.5 | drop | 90 | 70 | 50 | 72 | 100 | 58 | 28 | 50 | 8 | 45 | 8 |

### 10.3 分歧格与裁决（|A−B| ≥ 30）

| 记录 | 维 | A | B | 裁决 |
| --- | --- | ---: | ---: | ---: |
| `accuracy_based_redundancy_estimates_require_` | F2 | 100 | 50 | 50 |
| `accuracy_based_redundancy_estimates_require_` | F6 | 100 | 50 | 50 |
| `annual_antigen_targets_require_marginal_inte` | F2 | 0 | 50 | 0 |
| `annual_antigen_targets_require_marginal_inte` | F6 | 100 | 50 | 50 |
| `annual_antigen_targets_require_marginal_inte` | S1 | 100 | 50 | 50 |
| `antibody_diversity_counting_unit_is_declared` | F2 | 100 | 50 | 100 |
| `antibody_diversity_counting_unit_is_declared` | S4 | 100 | 50 | 50 |
| `antigen_state_ensemble_defines_the_epitope_d` | S1 | 100 | 50 | 100 |
| `antigen_state_ensemble_defines_the_epitope_d` | S6 | 0 | 50 | 0 |
| `bio_foundation_model_data_scaling_has_no_est` | S4 | 100 | 50 | 50 |
| `canonical_class_count_is_not_a_dynamical_sta` | S6 | 100 | 50 | 50 |
| `canonical_class_criterion_has_two_readings` | S4 | 50 | 100 | 50 |
| `canonical_class_criterion_has_two_readings` | S6 | 0 | 50 | 0 |
| `cdr_class_count_is_procedure_dependent` | S6 | 0 | 50 | 0 |
| `cdr_class_map_is_not_a_function_in_either_di` | S6 | 45 | 75 | 50 |
| `clone_and_epitope_partitions_require_indepen` | S6 | 20 | 50 | 50 |
| `clonotype_threshold_is_not_a_specificity_thr` | S4 | 15 | 50 | 50 |
| `clonotype_threshold_is_not_a_specificity_thr` | S6 | 15 | 50 | 50 |
| `clustering_method_ranking_is_task_dependent` | F2 | 90 | 50 | 50 |
| `collection_breadth_requires_a_held_out_antig` | S4 | 85 | 50 | 50 |
| `contact_matching_bounds_can_leave_redundancy` | S6 | 60 | 100 | 100 |
| `contact_overlap_is_a_tolerance_not_an_equiva` | S5 | 70 | 100 | 70 |
| `coverage_standardized_epitope_richness` | F3 | 70 | 100 | 70 |
| `coverage_standardized_epitope_richness` | F4 | 30 | 75 | 50 |
| `cross_antigen_contact_overlap_requires_decla` | F2 | 90 | 60 | 50 |
| `cross_antigen_contact_overlap_requires_decla` | S6 | 0 | 70 | 50 |
| `differential_task_advantage_needs_an_interac` | S2 | 40 | 70 | 25 |
| `epitope_community_count_is_assay_resolution_` | F2 | 90 | 55 | 50 |
| `epitope_community_count_is_assay_resolution_` | F4 | 85 | 55 | 50 |
| `epitope_diversity_estimators_need_cross_anti` | F3 | 85 | 55 | 60 |
| `epitope_diversity_estimators_need_cross_anti` | S2 | 0 | 50 | 25 |
| `epitope_diversity_estimators_need_cross_anti` | S6 | 50 | 0 | 0 |
| `epitope_diversity_is_a_joint_antigen_immune_` | F3 | 90 | 55 | 60 |
| `epitope_diversity_is_a_joint_antigen_immune_` | S4 | 60 | 25 | 25 |
| `epitope_diversity_needs_a_stability_profile` | F2 | 90 | 45 | 50 |
| `epitope_diversity_needs_a_stability_profile` | S4 | 0 | 50 | 50 |
| `epitope_diversity_needs_a_stability_profile` | S6 | 80 | 50 | 50 |
| `epitope_diversity_rankings_depend_on_weighti` | F3 | 85 | 55 | 60 |
| `epitope_partitions_are_not_axiomatically_nes` | S4 | 50 | 85 | 50 |
| `fixed_coverage_enables_guaranteed_representa` | S4 | 50 | 0 | 0 |
| `fixed_coverage_enables_guaranteed_representa` | S5 | 85 | 50 | 50 |
| `footprint_overlap_does_not_predict_escape_sp` | S4 | 50 | 90 | 50 |
| `germline_motif_predicts_public_clone_recurre` | S6 | 95 | 50 | 50 |
| `interface_diversity_metrics_require_metric_s` | S4 | 50 | 85 | 50 |
| `joint_pair_redundancy_requires_one_reference` | S4 | 50 | 90 | 50 |
| `lm_representations_compress_off_germline_var` | F2 | 50 | 100 | 50 |
| `pair_novelty_requires_four_role_specific_exp` | S3 | 50 | 90 | 50 |
| `pair_novelty_requires_four_role_specific_exp` | S4 | 50 | 90 | 50 |
| `paired_chain_effective_diversity_loses_mutua` | F2 | 70 | 100 | 50 |
| `paired_chain_effective_diversity_loses_mutua` | F5 | 60 | 90 | 75 |
| `paired_chain_effective_diversity_loses_mutua` | S3 | 50 | 90 | 100 |
| `paratope_prediction_is_antigen_agnostic` | S5 | 60 | 90 | 60 |
| `predicted_epitope_field_is_a_reference_panel` | F5 | 65 | 25 | 25 |
| `predicted_epitope_field_is_a_reference_panel` | S6 | 50 | 90 | 75 |
| `predicted_structures_add_no_classes_beyond_t` | F3 | 50 | 90 | 75 |
| `pretraining_exposure_limits_model_based_dive` | S2 | 0 | 40 | 0 |
| `pretraining_exposure_limits_model_based_dive` | S4 | 50 | 100 | 50 |
| `residue_score_field_does_not_determine_patch` | S3 | 100 | 50 | 100 |
| `residue_score_field_does_not_determine_patch` | S6 | 50 | 80 | 75 |
| `richness_bounds_do_not_transfer_to_coverage` | F2 | 35 | 65 | 35 |
| `richness_bounds_do_not_transfer_to_coverage` | F4 | 90 | 50 | 50 |
| `sample_frequency_inflates_dominance_by_uncov` | S3 | 100 | 50 | 100 |
| `sampling_redundancy_and_biological_convergen` | F3 | 85 | 55 | 55 |
| `sampling_redundancy_and_biological_convergen` | S5 | 40 | 70 | 40 |
| `scaling_exponents_are_not_transportable_acro` | F2 | 90 | 60 | 60 |
| `scaling_exponents_are_not_transportable_acro` | S3 | 20 | 50 | 20 |
| `sequence_diversity_bias_has_no_fixed_sign` | S2 | 50 | 80 | 50 |
| `sequence_diversity_bias_has_no_fixed_sign` | S3 | 30 | 0 | 0 |
| `similarity_split_score_drops_do_not_identify` | S3 | 50 | 90 | 50 |
| `similarity_split_score_drops_do_not_identify` | S4 | 50 | 90 | 50 |
| `similarity_split_score_drops_do_not_identify` | S6 | 55 | 90 | 55 |
| `single_linkage_bridges_distinct_clones` | F5 | 85 | 55 | 55 |
| `single_linkage_bridges_distinct_clones` | S3 | 100 | 70 | 100 |
| `sufficient_sampling_returns_records_not_anti` | S4 | 90 | 50 | 50 |
| `unseen_shared_epitopes_bias_overlap_downward` | S4 | 50 | 85 | 50 |
| `unseen_shared_epitopes_bias_overlap_downward` | S6 | 50 | 80 | 50 |
| `vhh_is_out_of_domain_for_fab_calibrated_inst` | S3 | 25 | 65 | 25 |
| `vhh_is_out_of_domain_for_fab_calibrated_inst` | S4 | 90 | 50 | 90 |
| `vhh_is_out_of_domain_for_fab_calibrated_inst` | S6 | 90 | 45 | 90 |

## 十一、本轮的偏差与未做

- **未移动任何文件到 `dregs/`。** 17 条 drop 档仍留在 `son/`，`qc:` 字段已标出。移动会改变 `relation` 边的可达性（多条 drop 档是池内的中间节点，例如 `coverage_standardized_epitope_richness`），需先确认替代的父节点。
- **未修订任何条目。** 34 条 revise 档的缺陷已定位到维度，但正文未改。
- **62 条的正向结论未做外部验证。** 两名评分员都是同一模型族，S5 的「被引条目是否支持该断言」只核到 bodn 摘要层，未回原文。三处引语（Caprara、Holm & Sander、AFilter）在池内无法核验归属，已记为待办。
- **F2 的锚点在批次间仍有解释空间**（主控裁决 8 格），是最大的单维裁决量。若要进一步提高可比性，需把 F2 也改写成机械判据。
