---
tags:
  - design
---

# Affinity Label Cleaning Problem Inventory

本设计文件针对的是 [[2026-11-01-20-src-data-etl-todo-list]] 中的 `## 1. Data ETL Specification`.

## time

2026-11-04

## lineage

- [[3a_src_data_etl_modeling]]: current MVP model for the processed Ab-Ag pair dataset.
- [[3a_src_data_etl_problem_ab]]: mutation classes A/B/C on the antibody side.
- [[3a_src_data_etl_problem_ag]]: mutation classes A/B/C on the antigen side.
- [[src-03-abdesign-1-0-inventory]]: ELISA mutant/WT ratio and ddG blocks merged from SKEMPIv2 and AB-Bind.
- [[src-08-avida-htnfa-inventory]]: binary binding label plus an unlabeled VHH corpus.
- [[src-09-flab-inventory]]: 86 binding tables with mixed label types, units and embedded AbRank rows.
- [[src-10-abrank-inventory]]: Kd, IC50 and escape columns with `Aff_op` censoring and 8 upstream sources.
- [[src-11-abbibench-inventory]]: per-file normalized `binding_score` without units or assay.
- [[src-12-asd-agab-db-inventory]]: largest compilation with log Kd, binary, ordinal and computed ΔG labels.
- [[src-13-andd-inventory]]: real Kd and ΔG, predicted Kd and unlabeled rows from 27 sub-sources.
- [[src-14-ab-bind-inventory]]: ddG only, 9 assay names, no WT baseline rows.
- [[src-15-skempi-2-0-inventory]]: mutant and WT Kd with 20 methods, relational values and `n.b`.
- [[src-16-guest-inventory]]: 42 cases with paired Kd and ΔG.
- [[src-20-sabdab-sabdab2-inventory]]: structure only, no affinity labels.
- [[src-23-mit-ll-alphaseq-inventory]]: predicted log nM with assay and replicate fields, plus empty labels.
- [[src-50-graphinity-inventory]]: computed FoldX and Flex ddG only.
- [[src-74-abdesign-2-0-inventory]]: Kd with kon/koff on the same row, plus a binary binding label.
- [[src-75-her2-aff-large-buzz-inventory]]: ordinal sort classes, binary labels and small external continuous sets.
- [[src-76-tdc-antibodyaff-inventory]]: single `Y` value without unit or assay.
- [[src-77-akbar-sabdab-kd-csv-inventory]]: same 493 `Y` values as R76.
- [[src-78-mochibind-sampled-data-inventory]]: sampled AlphaSeq log10 Kd with model predictions on the same row.
- [[src-79-alphabind-inventory]]: campaign-level AlphaSeq log10 Kd with model predictions on the same row.
- [[src-80-antipasti-inventory]]: Kd and ΔG on the same row with an unreliable method field.

## relation

None.

## description

### 问题

这份记录只列出 20 个 SRC 暴露出的 affinity 清洗问题，暂不决定具体方案。下游用途未知，[processed Ab-Ag pair dataset model](3a_src_data_etl_modeling.md) 规定 `affinity[]` 直接保存来源的原始观测，不换算、不聚合。因此这里只保留"原始值要装进统一 schema 就必须统一"的问题。modeling 当前的 `(label, assay, condition, replicate, lineage[])` 没有单位和截断符号的位置，方案阶段补齐。

1. **无值或占位的记录是否构成 observation**：modeling 要求每个有效 `3A` 至少有一条"有效 affinity label"，"有效"尚未定义。
    - **有记录无值**：R08 `corpus-hTNFa.csv` 216,225 行、R10 的 1,059 行、R13 的 39,235 行、R23 的 907,561 行空 `Pred_affinity`、R15 的 228 行 `n.b`。空值不是 negative。
    - **整源无 label**：R20 只有结构元数据，不产生 observation。
    - **最低条件**：可解析的数值、来源明确的定性判定，哪些算有效。

2. **一条源记录含多个值时如何拆成 observation**：schema 里一条 observation 只有一个 label。
    - **同行多值**：R16 的 Kd 与 ΔG、R80 的 `affinity` 与 `delta_g`、R13 的 907 行 Kd 与 ΔG、R74 的 `kd`、`binding` 与 `kon/koff`、R09 kothiwal 表的 SPR KD 与 EC50、R10 的三个互斥亲和力列。
    - **跨 pair 的同行双值**：R15 每行同时给 `Affinity_mut` 与 `Affinity_wt`，分属突变体和 WT 两个 pair。
    - **粒度**：一条 observation 对应一行还是一列，lineage 需要定位到哪一级。

3. **`label_type` 和单位如何统一**：同一个名字指不同的量，不同的名字指同一个量。
    - **同名异义**：`log_Kd` 实际包含 `-ln(KD nM)`（R09 koenig2017）、`-log Kd`（R12）、`log10(Kd nM)`（R78/R79）、逐文件归一化的 `binding_score`（R11）和 `log(Kd_ratio)`（R10）。`ddG` 同时指突变差 ΔΔG（R14、R03、R50）和绝对 ΔG（R13、R16、R80、R12 `biomap`）。
    - **异名同义**：`Kd (nM)`、`KD (M)`、`kd`、`Y`、`Affinity_Kd [nM]` 指同一个量。
    - **非定量标签**：二元（R08、R12 `bool`、R75）、序数（R12 buzz、R75 `class`）、比值和富集（R03、R12）只能归类，不能当作 Kd。
    - **单位**：M、nM、µM、pM、µg/mL、ng/mL、kJ/mol、kcal/mol 和 log 变换并存。R76/R77 的 `Y`、R12 `osh` 的 `kd`、R75 shanehsazzadeh 的 `affinity` 没有单位，缺失如何表示，不能凭量级补写。

4. **实验值、预测值和计算值如何标记**：多个来源把非实验值与实验值放在同一类字段里。
    - **计算**：R50 的 963,552 条 FoldX/Flex ddG；R12 `biomap` 的 2,725 条计算 ΔG。
    - **预测**：R13 的 2,271 行 predicted Kd；R23 的 352,139 条 `Pred_affinity`；R09 li2023/engelhart2022；R78/R79 的 `predicted_affinity` 与实验 `alphaseq_affinity` 同行并存。
    - **两条轴混写**：量的种类（Kd、ΔΔG）和值的来源（实验、预测、计算）是两个维度，现有词表用 `predicted`、`ddG` + `computational` 混写。todo 已要求 R50、R23 单独处理，需要定义这条线落在哪个字段。

5. **截断符号如何保存**：检测限处的值不是精确值。
    - **已有标记**：inventory 只在 R10 和 R15 发现。R10 的 `Aff_op` 为 `=` 307,797 / `>` 34,062 / `<` 497；R15 的 `Affinity_wt` 有 41 个关系式（`<1E-11`、`<1.4E-10`），写在值字符串内部，需要先解析。
    - **无标记来源**：其余来源没有截断信息，精确值与检测限值无法区分。

6. **assay、condition、replicate 的缺失和边界**：多数来源没有这三个字段，已有字段也混入了别的内容。
    - **缺失表示**：R10、R11、R76、R77 等没有 assay，几乎所有来源没有 replicate，inventory 记 `unknown`，schema 里用 `null` 还是 `unknown`。
    - **assay 混入 label 名**：R09 的 IC50 行 assay 写作 `IC50`，二元行写作 `bind/no bind`，R12 的计算行写作 `computational`。
    - **condition 混入 provenance**：R12 的 `abbd`、`scmc`，R78/R79 的 `fine-tuning`、`validation`，R23 的 `assay 1` 是来源子集或数据切分，不是实验条件。R23 的 AlphaNeg1~3 是不同的抗原对象，R09 phillips 的 `genotype` 已由 problem_ab 第 9 项写入序列。

7. **重复测量如何判定**：affinity 不参与 `3A_ID`，同一测量在多个来源出现时没有现成的去重键。
    - **汇编关系**：R76 与 R77 的 `Y` 逐行相同；R78 是 R79 的采样，两者与 R23、R09 li2023 同属 AlphaSeq；R10 内含 SKEMPIv2、AbSci、SabDab、AlphaSeq、AbCoV；R09 内嵌 AbRank 与 AVIDa-hTNFa；R12 内含 flab、skempiv2、ab-bind、buzz、alphaseq；R13 内含 AB-Bind、SabDab，与 R80 同源；R03 的 ddG 来自 R15 与 R14；R74 与 R75 的 Buzz 同源。
    - **源内重复**：R76/R77 的 493 行只有 476 个唯一 pair（14 对出现 2 次，1 对出现 4 次）；R10 同一 (heavy, light, Ag) 三元组最多出现 88 次；R15 每行都带 `Affinity_wt`，拆出 WT observation 后需要折叠。
    - **判定标准**：同一测量在不同来源以 nM、M、`-log` 表示且舍入不同，如何认定相等。真实重复测量（R23 有 Assay 1/2、Replicate 1~3，其余没有）与重复登记如何区分。
    - **口径冲突**：todo 对 R76/R77 写"只保留一个 canonical measurement"，modeling 写"逐条追加"，需要统一。

相关 20 个 inventory：

- [R03 AbDesign 1.0](../2026-10-30-3a-src-inventory/src-03-abdesign-1-0-inventory.md)
- [R08 AVIDa-hTNFa](../2026-10-30-3a-src-inventory/src-08-avida-htnfa-inventory.md)
- [R09 FLAb](../2026-10-30-3a-src-inventory/src-09-flab-inventory.md)
- [R10 AbRank](../2026-10-30-3a-src-inventory/src-10-abrank-inventory.md)
- [R11 AbBiBench](../2026-10-30-3a-src-inventory/src-11-abbibench-inventory.md)
- [R12 ASD / AgAb DB](../2026-10-30-3a-src-inventory/src-12-asd-agab-db-inventory.md)
- [R13 ANDD](../2026-10-30-3a-src-inventory/src-13-andd-inventory.md)
- [R14 AB-Bind](../2026-10-30-3a-src-inventory/src-14-ab-bind-inventory.md)
- [R15 SKEMPI 2.0](../2026-10-30-3a-src-inventory/src-15-skempi-2-0-inventory.md)
- [R16 Guest antibody benchmark](../2026-10-30-3a-src-inventory/src-16-guest-inventory.md)
- [R20 SAbDab / SAbDab2](../2026-10-30-3a-src-inventory/src-20-sabdab-sabdab2-inventory.md)
- [R23 MIT-LL AlphaSeq](../2026-10-30-3a-src-inventory/src-23-mit-ll-alphaseq-inventory.md)
- [R50 Graphinity](../2026-10-30-3a-src-inventory/src-50-graphinity-inventory.md)
- [R74 AbDesign 2.0](../2026-10-30-3a-src-inventory/src-74-abdesign-2-0-inventory.md)
- [R75 HER2-aff-large / Buzz](../2026-10-30-3a-src-inventory/src-75-her2-aff-large-buzz-inventory.md)
- [R76 TDC AntibodyAff](../2026-10-30-3a-src-inventory/src-76-tdc-antibodyaff-inventory.md)
- [R77 Akbar SAbDab Kd CSV](../2026-10-30-3a-src-inventory/src-77-akbar-sabdab-kd-csv-inventory.md)
- [R78 MochiBind sampled data](../2026-10-30-3a-src-inventory/src-78-mochibind-sampled-data-inventory.md)
- [R79 AlphaBind public experiments](../2026-10-30-3a-src-inventory/src-79-alphabind-inventory.md)
- [R80 ANTIPASTI](../2026-10-30-3a-src-inventory/src-80-antipasti-inventory.md)
