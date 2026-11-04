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

这份记录只列出 20 个 SRC 暴露出的 affinity 清洗问题，暂不决定具体方案。下游用途未知，[processed Ab-Ag pair dataset model](3a_src_data_etl_modeling.md) 规定 `affinity[]` 直接保存来源的原始观测，不换算、不聚合。因此这里只保留"原始值要装进统一 schema 就必须统一"的问题。modeling 的 `(label, assay, condition, replicate, lineage[])` 不改结构，类型、单位、截断符号等额外信息只能写进 `lineage`。

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

### 方案

#### 1. 无值或占位的记录是否构成 observation

扫描 `G:\abag-datasets` 后，"无值"有五种含义，只有第一种是"没有做实验"：

| 类 | 含义 | 例子 | 处理 |
| --- | --- | --- | --- |
| 1. 没有测量 | 来源是序列或结构库，从未带亲和力 | R13 的 39,235 行（`Reason_Code=not_reported`）、R08 `corpus-hTNFa.csv` 的 216,225 行、R20 整源 | 不成立 |
| 2. 测了另一种量 | 表里只有 IC50 和 KD 两列，该行测的是别的量 | R10 的 CATNAP 1,032 行（只有 IC80）、AbCoV 27 行（只有 EC50） | 不成立 |
| 3. 测了，失败 | 占位符表示 assay 没有出结果，同行其他列常有值 | R09 kothiwal 的 `Fail`、R15 的 `unf`、R12 的 `I.C.` | 不成立 |
| 4. 检测不到结合 | 有信息：弱于检测限，但没有数值 | R15 的 `n.b`/`n.b.`（278 行）、R74 的 `binding=0`、R08 与 R75 的 `label=0` | 成立，为定性 observation |
| 5. 空位，原因未记录 | 来源不说明为什么为空 | R23 的空 `Pred_affinity`、R79 的空 `alphaseq_affinity`、R74 的空 `binding`、R12 的字符串 `nan` | 不成立 |

一条 observation 成立，需满足以下任一项：

- 可解析的精确数值。
- 带 `>` 或 `<` 的边界值，例如 R12 的 `>8.8`、R15 的 `>1E-04`。
- 来源明确的定性判定：binary（含 0）、ordinal、`n.b`。

三者都不满足则不成立。R74 中 `binding=1` 但无 KD 的 80 行按 binary 成立。

规则：

- 空不是 negative。空值、`Fail`、`nan` 不转换为 0 或 `n.b`。
- 一行多列时逐列判断。R09 kothiwal 的 EC50 为 `Fail` 而 SPR KD 有值时，EC50 不成立，KD 成立。
- R10 空行的 `Aff_op` 恒为 `=`，是填充值，不作为有值的证据。
- 占位词由 SRC 适配器列出，不做全局映射。同一个符号含义随来源变化：`nan` 在 R12 是缺失，`n.b` 在 R15 是信息，`Fail` 在 R09 是失败。适配器未列出的非数值字符串按不成立处理。
- 一个 pair 的 observation 全部不成立时，不生成 `3A`。
- 不成立的记录留在原始数据集，不进入 processed dataset，也不新建 audit 目录。成立的 observation 在 `lineage` 中记录原始列名和原始字符串，例如 `n.b.`。

初始占位词表：

| SRC | 不成立 | 成立（边界或定性） |
| --- | --- | --- |
| R08 | `corpus-hTNFa.csv`（无 label 列） | `label` 0/1 |
| R09 | `Fail` | |
| R10 | 空串、`NA` | |
| R12 | `nan`、`I.C.` | `>8.8` |
| R13 | `\`、`Reason_Code=not_reported` | |
| R15 | `unf` | `n.b`、`n.b.`、`>`/`<` 值 |
| R23、R79 | 空值 | |
| R74 | `binding` 空 | `binding` 0/1 |
| R75 | | `label` 0/1 |

相关 inventory：

- [R08 AVIDa-hTNFa](../2026-10-30-3a-src-inventory/src-08-avida-htnfa-inventory.md)
- [R09 FLAb](../2026-10-30-3a-src-inventory/src-09-flab-inventory.md)
- [R10 AbRank](../2026-10-30-3a-src-inventory/src-10-abrank-inventory.md)
- [R12 ASD / AgAb DB](../2026-10-30-3a-src-inventory/src-12-asd-agab-db-inventory.md)
- [R13 ANDD](../2026-10-30-3a-src-inventory/src-13-andd-inventory.md)
- [R15 SKEMPI 2.0](../2026-10-30-3a-src-inventory/src-15-skempi-2-0-inventory.md)
- [R20 SAbDab / SAbDab2](../2026-10-30-3a-src-inventory/src-20-sabdab-sabdab2-inventory.md)
- [R23 MIT-LL AlphaSeq](../2026-10-30-3a-src-inventory/src-23-mit-ll-alphaseq-inventory.md)
- [R74 AbDesign 2.0](../2026-10-30-3a-src-inventory/src-74-abdesign-2-0-inventory.md)
- [R75 HER2-aff-large / Buzz](../2026-10-30-3a-src-inventory/src-75-her2-aff-large-buzz-inventory.md)
- [R79 AlphaBind public experiments](../2026-10-30-3a-src-inventory/src-79-alphabind-inventory.md)

相关设计：[processed Ab-Ag pair dataset model](3a_src_data_etl_modeling.md)。

#### 2. 一条源记录含多个值时如何拆成 observation

扫描 20 个 SRC 后，一行里的多个值分为三种，只有第二种各自成为 observation。R03、R08、R11、R14、R23、R76、R77 每行只有一个读数（R03、R12 为 `affinity` + `affinity_type` 的长表），R20 没有 affinity。

**粒度**：一条 observation 对应一个原始读数，即一行中的一列。同一行的多条 observation 共享行号，靠列名区分，`lineage` 定位到文件、表、行、列，例如 `SRC_R09 | kothiwal2025htp_DCC_spr.csv | row=4 | col=SPR kinetics - KD (nM)`。

**1. 同一次测量的不同写法：派生值，不单列**

派生值是同一行里可以由另一列用固定算法算出的值：单位换算、取对数、ΔG = RT·ln Kd、按阈值判 0/1、整列拷贝。只存产生它们的独立读数。

例外：派生标签是该条目的唯一读数时保留。R74 中 KD 缺失的 179 行里 `binding` 是唯一读数；R75 的 mason_et_al 只有 `label`；R13 只有 ΔG 的行里 ΔG 是唯一读数。

不是本 pair 的读数也不产出：R79 的 `parental_mean_aff` 是亲本的均值，`avg_off_target_affinity` 的聚合对象来源未定义。

**2. 同一行的独立读数：各成一条 observation**

- R09 kothiwal：SPR KD 与 Cell Display EC50，assay 不同，各一条。
- R10：AbCoV 有 293 行 IC50 与 Kd 并存；RBD-escape 有 20,500 行 Kd 与 `escape` 并存。
- R75 流感集：一条重链对应多个抗原（CR6261 为 h1、h9，CR9114 为 h1、h3、fluB），每个抗原的 `*_mean` 各一条，分属不同 pair。
- R15：每行的 `Affinity_mut` 属于突变体 pair，`Affinity_wt` 属于 WT pair，见下。

**R15 的突变体与 WT 拆分**

- `Affinity_mut` 产出到突变体 pair，突变位于抗体侧还是抗原侧、序列如何重建，按 problem_ab 第 9 项和 problem_ag 第 5 项；`Affinity_wt` 产出到 WT pair，每个来源行各产出一条。
- WT 序列无法重建（C 类）时不产出 WT observation，突变体 observation 不受影响。

**R50 的 Flex 表**

`flexddg_ddg-talaris2014-gam` 与 `flexddg_ddg` 逐行相等，属整列拷贝，不产出。`flexddg_ddg` 与 `flexddg_ddg-talaris2014` 是不同打分函数的读数，各成一条 observation。

**3. 不是亲和力的量**

kon、koff、ka、kdis、dH、dS、r2，以及 QC、NGS 计数、表达量，不单列。通则：这些动力学和热力学量仅当该条目没有任何其他可用 label 时才作为 observation 保留。

核对结果：R74（389 行）、R15（突变体侧 2,273 行，WT 侧 2,289 行）、R09 kothiwal（688 行）去掉后都还有 Kd 或 EC50，不丢条目。唯一例外是 R12 `htm` 的 3 行 `ka (1/Ms)`（515000、25000、411000），它们所在的 pair 在 R12 里没有别的行，按通则保留。`ka` 的类型描述见第 3 项。

**各 SRC 的产出**

| SRC | 产出的读数列 | 不产出 |
| --- | --- | --- |
| R09 | 每张表的原始 label 列；kothiwal 另有 EC50 | `fitness`、取对数和单位换算列、ka/kdis、QC、NGS 计数 |
| R10 | `IC50`、`Affinity_Kd`、`escape`（保留原始值字符串，含 `>`） | `log_Aff`、`log(Kd_ratio)`、`Aff_op` |
| R12 | `affinity`（按 `affinity_type`） | `processed_measurement` |
| R13 | Kd；无 Kd 时的 ΔG | 与 Kd 同行的 ΔG |
| R15 | `Affinity_mut`、`Affinity_wt` | `*_parsed`、kon/koff/dH/dS |
| R16 | Kd | ΔG |
| R50 | `foldx_ddg`、`flexddg_ddg`、`flexddg_ddg-talaris2014` | 绝对 dG 列、`flexddg_ddg-talaris2014-gam` |
| R74 | `kd`；`kd` 缺失时 `binding` | 有 `kd` 时的 `binding`、kon/koff/r2 |
| R75 | 流感集各抗原 `*_mean`；主表 `class`；外部集 `affinity`，缺失时 `label` | 流感集 `*_label`；主表 `label` |
| R78、R79 | `alphaseq_affinity` | `parental_*`、`avg_off_target_affinity`；`predicted_affinity` 见第 4 项 |
| R80 | `affinity` | `delta_g` |

#### 3. `label_type` 和单位如何统一

不统一，只搬运。`affinity` 的元组 `(label, assay, condition, replicate, lineage[])` 不增减字段。`label` 保存源值原样，源对这个值的类型和单位所做的描述只写进该 observation 的 `lineage`。

**lineage 的写法**

在原有定位后追加源的原始描述，字符串照抄，不映射词表，不换算：

1. `col=<列名>`：值所在的列，列名里的类型和单位随之保留，如 `col=Affinity_Kd [nM]`。
2. 行内带类型列的源，再追加 `<类型列>=<该行取值>`。R12 的 `affinity_type` 有 16 种取值（`Kd (nM)`、`-log Kd (M)`、`ddg`、`fuzzy`、`bool`、`ka (1/Ms)` 等），R03 `datasets_mut.csv` 的 `affinity_type` 有 `ddg`、`elisa_mut_to_wt_ratio` 两种。
3. 源没有描述的，只写 `col=`，不补单位，不按量级推断。涉及 R76/R77 的 `Y`、R12 `osh` 的 `kd`、R75 shanehsazzadeh 的 `affinity`。

```text
SRC_R12 | <文件> | row=123 | col=affinity | affinity_type=ka (1/Ms)
SRC_R09 | kothiwal2025htp_DCC_spr.csv | row=4 | col=SPR kinetics - KD (nM)
```

二元、序数和比值标签（R08、R12 `bool`/`fuzzy`、R75 `class`、R03 `elisa_mut_to_wt_ratio`）同样处理：`label` 照抄，类型靠列名或类型列区分。第 2 项留下的 R12 `ka (1/Ms)` 3 行也由此解决，不需要为它另设位置。

#### 4. 实验值、预测值和计算值如何标记

预测值和计算值与实验值一样成为 observation，不设过滤。标记只靠 `lineage`，沿用第 3 项的 `col=` 与 `<类型列>=<取值>`，不新增写法，不区分"预测"和"计算"，用源自己的名字。

| SRC | 源的标记 | lineage 里的内容 |
| --- | --- | --- |
| R09 li2023、engelhart2022 | 列名 `Pred_affinity` | `col=Pred_affinity` |
| R12 | `affinity_type=delta_g`（2,725 条计算 ΔG） | `affinity_type=delta_g` |
| R13 | 行内列 `Predicted_or_Not`：`predicted` 2,271（其中 841 行有 Kd）、`real` 7,294、`\` 39,235 | 追加 `Predicted_or_Not=<取值>` |
| R23 | 列名 `Pred_affinity`，352,139 条，是该源唯一的 affinity 列 | `col=Pred_affinity` |
| R50 | 列名 `foldx_ddg`、`flexddg_ddg` | `col=foldx_ddg`、`col=flexddg_ddg` |
| R78、R79 | 列名 `predicted_affinity`，与实验 `alphaseq_affinity` 同行并存 | `col=predicted_affinity` |

R78、R79 的 `predicted_affinity` 是模型输出，不能由同行其他列用固定算法算出，不属于第 2 项的派生值，按独立读数各成一条 observation。

R23 和 R50 的 affinity 全部是非实验值，产出的 `3A` 只含这类 observation。是否进入最终数据集由下游靠 `lineage` 过滤，这两个 SRC 的单独处理见 todo。

#### 5. 截断符号如何保存

不单独保存。`label` 保存源的值字符串原样，`>`、`<` 留在字符串里，`lineage` 不再追加。

- R10：`Aff_op` 为 `>` 或 `<` 的 34,559 行，`IC50` 或 `Affinity_Kd` 字符串都已带符号，`Aff_op` 冗余，不产出（与第 2 项一致）。另有 2 行 `Aff_op` 为 `=` 而 `IC50` 字符串含 `<>`，以字符串为准。
- R12 的 `>8.8`、R15 的 `<1E-11` 等同理，`*_parsed` 不产出。
- 无标记的来源不补。R09 phillips 的 7.0 和 6.0 疑似检测下限，源没有标记，不推断，只在 inventory 记录。

#### 6. assay、condition、replicate 的缺失和边界

三个字段与 `label` 一样只暂存源的原始记录，原样转存，不统一，不清洗。

- 缺失为 `None`。`label` 不允许为 `None`，`assay`、`condition`、`replicate` 各自可以为 `None`，互不影响。
- inventory 记为 `unknown` 的，字段为 `None`，`lineage` 追加 `assay=unknown`、`condition=unknown` 或 `replicate=unknown`。
- 其余内容原样保存，包括 inventory 已有的取值。

#### 7. 重复测量如何判定

不判定，不去重。`affinity[]` 是列表，同一 `3A_ID` 下每条成立的 observation 各追加一个 `(label, assay, condition, replicate, lineage[])`，各带自己的 `lineage`。

- 源内重复：R76/R77 的 493 行对应 476 个 pair，重复的 pair 得到多条 tuple。R15 的 WT 同理。
- 跨源重复：同一测量出现在多个来源时，各自一条 tuple。
- 不比较 `label` 的数值，不做单位或舍入的相等判断，不区分真实重复与重复登记。

相关 inventory：

- [R03 AbDesign 1.0](../2026-10-30-3a-src-inventory/src-03-abdesign-1-0-inventory.md)
- [R09 FLAb](../2026-10-30-3a-src-inventory/src-09-flab-inventory.md)
- [R10 AbRank](../2026-10-30-3a-src-inventory/src-10-abrank-inventory.md)
- [R12 ASD / AgAb DB](../2026-10-30-3a-src-inventory/src-12-asd-agab-db-inventory.md)
- [R13 ANDD](../2026-10-30-3a-src-inventory/src-13-andd-inventory.md)
- [R15 SKEMPI 2.0](../2026-10-30-3a-src-inventory/src-15-skempi-2-0-inventory.md)
- [R16 Guest antibody benchmark](../2026-10-30-3a-src-inventory/src-16-guest-inventory.md)
- [R50 Graphinity](../2026-10-30-3a-src-inventory/src-50-graphinity-inventory.md)
- [R74 AbDesign 2.0](../2026-10-30-3a-src-inventory/src-74-abdesign-2-0-inventory.md)
- [R75 HER2-aff-large / Buzz](../2026-10-30-3a-src-inventory/src-75-her2-aff-large-buzz-inventory.md)
- [R78 MochiBind sampled data](../2026-10-30-3a-src-inventory/src-78-mochibind-sampled-data-inventory.md)
- [R79 AlphaBind public experiments](../2026-10-30-3a-src-inventory/src-79-alphabind-inventory.md)
- [R80 ANTIPASTI](../2026-10-30-3a-src-inventory/src-80-antipasti-inventory.md)

相关设计：[processed Ab-Ag pair dataset model](3a_src_data_etl_modeling.md)。
