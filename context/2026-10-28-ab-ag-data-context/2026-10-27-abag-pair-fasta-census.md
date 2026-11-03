---
tags:
  - context
---

# abag pair 双侧 FASTA 可达性逐 R 摸底（2026-10-27）

## 目的

为构建 **ab–ag pair 序列数据集** 做逐 R 摸底。产物是一份「每个 R 里哪些 ab/ag 能落到完整 FASTA」的扫描记录，为下一轮生成 index/dataset 提供依据。

**判定口径（与上一轮「抗体可用性普查」不同，本轮双侧重）**：
- **ab 侧**：完整 FASTA 到 **Fv 级**——VH+VL、或 VHH、或可切/可拼到该级别。获取路径分四等：`直接可用`（表内字段即序列）、`需切`（IgG→VH/VL、scFv→VH/VL、融合蛋白→域）、`需拼`（CDR 串 + 母本）、`需第三方`（母本/序列在 bucket 外，需人工上网）。
- **ag 侧**：完整 FASTA 到 **实验所用构建体**（b 口径，可带 Fc/AviTag/His 等标签，不一定等于天然全长蛋白）。路径同四等。
- 两侧都到 Fv/构建体级、且序列可逐字取得，才算**可闭合**。逐字取不到但有具体外部目标（UniProt/PDB/专利号）的记为 `blocked_*` 待人工；连外部目标都没有的记为 `无序列`。
- **不要求** affinity label、结构。

> 注（主人 Q3）：PLM 训练用序列是**天然可变域/全长蛋白**（AbLang/IgLM 用 OAS/SAbDab 的 VH/VL，ESM 用 UniProt 全长），不是实验构建体。b 口径的构建体与 PLM 训练分布并不等同，跨两者时需显式归一化。已记录，下一轮定。

## 全库概览

73 个源中 69 个 bucket 内有数据（R24/R39/R52/R55 仅 readme）。按「ab 与 ag 是否都可达 Fv/构建体级 FASTA」分档：

### A 档：ab+ag 双侧表内即可闭合（列内即序列，无外部依赖）

| R | ab | ag | 规模 | 说明 |
| --- | --- | --- | ---: | --- |
| R03 AbDesign DB | `heavy_sequence_variable`+`light_sequence_variable` | `antigen_sequence`（逐行，33 个唯一值） | 1,303 行 | 7 抗原，PDB 来源序列 |
| R08 AVIDa-hTNFa | `VHH_sequence` 5,580/5,580 | `Ag_sequence`（`antigen_sequences.csv`，1 条 TNFa-WT-beads，233 aa） | 5,580 配对 | VHH 串含信号肽/His 标签，需切 |
| R12 ASD | parquet `chains.antibody_chains`{heavy,light} + `target_chains`{full} | 同表 `target_chains` | 1,177,819 行，**全部 heavy+light+ag 三槽非空**（实测） | 去重后配对数待算 |
| R13 ANDD | `Ab/Nano H_Chain AA`+`L_Chain AA` | `Ag_Seq` | 48,800 行，四列实测全非空 | 需复核 PDB 链角色 |
| R21 AVIDbase | `vhh_sequence` | `ag_sequence` | 1,048 行，双侧全非空 | 纯 VHH |
| R23 AlphaSeq v1 | `HC`+`LC`（`Sequence` 为 scFv） | 无列——靶肽 `PDVDLGDISGINAS`（README 正文逐字给，6LXT 含） | 1,259,700 行 | 3 个阴性对照肽无序列 |
| R35 Li AlphaSeq v2 | 同 R23 | 同 R23 | 1,259,701 + 1,903,928 行 | 同 R23 |
| R40 AVIDa-hIL6 | `VHH_sequence` | `Ag_sequence`（31 个构建体键，218 aa 含前缀+His） | 573,891 配对 | 双侧都需切 |
| R41 AVIDa-SARS-CoV-2 | `VHH_sequence` | `Ag_sequence`（`antigen_sequences.csv` 17 条构建体） | 77,003 配对 | 同上 |
| R67 Open AlphaSeq | `mata_sequence`/`matalpha_sequence`（按实验区分 ab/ag） | 同表另一列 | 9 表共 1,705,908 行 | scFv 需切、VHH 可直接 |
| R74 Omi32 BioPhy-Seq | 需拼：`geno` 13 位 + `aa_substitutions` + PDB 母本（11OR/11OU 已随包） | `WUHAN` 无序列；`BA1`/`BA4` RBD 在 PDB 11OQ/11OO/11OL（已随包） | 8,192 基因型 | 武汉株 ag 缺 → 部分闭合 |

```bash
┌───────────────┬───────────┬─────────┬─────────┬────────────┐
│       R       │   行数    │ ab 唯一 │ ag 唯一 │ pairs 唯一 │
├───────────────┼───────────┼─────────┼─────────┼────────────┤
│ R03           │        57 │      46 │      33 │         47 │
├───────────────┼───────────┼─────────┼─────────┼────────────┤
│ R08           │     5,580 │   5,577 │       1 │      5,577 │
├───────────────┼───────────┼─────────┼─────────┼────────────┤
│ R13           │    48,800 │  34,450 │   3,866 │     38,014 │
├───────────────┼───────────┼─────────┼─────────┼────────────┤
│ R21           │       690 │     673 │     443 │        690 │
├───────────────┼───────────┼─────────┼─────────┼────────────┤
│ R40           │   573,891 │  38,599 │      31 │    573,891 │
├───────────────┼───────────┼─────────┼─────────┼────────────┤
│ R41           │    77,003 │  36,100 │      17 │     76,800 │
├───────────────┼───────────┼─────────┼─────────┼────────────┤
│ R12           │ 1,177,819 │ 868,194 │   9,985 │  1,075,481 │
├───────────────┼───────────┼─────────┼─────────┼────────────┤
│ R23           │ 1,259,700 │ 104,968 │       4 │    419,872 │
├───────────────┼───────────┼─────────┼─────────┼────────────┤
│ R35 d1        │ 1,259,700 │ 104,968 │       4 │    419,872 │
├───────────────┼───────────┼─────────┼─────────┼────────────┤
│ R35 d2        │ 1,903,921 │  78,872 │       4 │    315,485 │
├───────────────┼───────────┼─────────┼─────────┼────────────┤
│ AlphaSeq 合并 │ 4,423,321 │ 183,081 │       1 │    183,081 │
├───────────────┼───────────┼─────────┼─────────┼────────────┤
│ R67           │ 1,705,908 │ 251,418 │   2,441 │  1,155,023 │
├───────────────┼───────────┼─────────┼─────────┼────────────┤
│ 合计          │           │         │         │  3,108,604 │
└───────────────┴───────────┴─────────┴─────────┴────────────┘
```

### B 档：ab 表内即可，ag 需随包 PDB/外部

| R | ab | ag | 规模 | 说明 |
| --- | --- | --- | ---: | --- |
| R01 IgDesign | 需拼：`HCDR1/2/3` + 母本（sabdab summaries 随包） | 无列；8 靶点 PDB 随包；SPR 抗原试剂（ACRO 货号）未知 | 1,444 行 | 1,243 行可拼（CD40 盲化除外） |
| R02 Absci HER2 | 需拼：`HCDR1/2/3` + trastuzumab Fab（README 随包） | 无列；HER2 ECD，1N8Z/630 aa 随包；交叉反应 5 抗原无序列 | 1,855 行 | 单抗原可闭合 |
| R04 IPI | 需拼：`CDR3`/`CDRH3` + `0Library_keys.xlsx` 模板（随包） | 10 个抗原构建体序列在 `0Library_keys.xlsx`（随包） | 22 NGS 表 94,274 行 + 486 表 486 行 | 抗原序列随包，含标签 |
| R05 Tite-Seq | 需拼：`CDR1H_AA`+`CDR3H_AA` + 母本 1FLR（随包） | fluorescein 小分子——**无蛋白 FASTA** | 11,039 行 | ag 永久不可闭合 |
| R06 Koenig | `heavy`+`light` 直接可用 | 无列；VEGF-A 2FJG 随包；实验生物素化构建体未知 | 4,275 行 | 单抗原近似闭合 |
| R07 Makowski MET | `VH Sequence` 直接可用，**无轻链**（emibetuzumab VL 不在包内） | 无列；MET Sema 6WVZ 随包；HGFR-Fc 构建体未知 | 4,222 行 | ab 缺 VL → 不能闭合 |
| R09 FLAb | 165 表 `heavy`/`light`（缺 4 表）；AbRank 子表齐全 | 仅 20 表带 `antigen_seq`（709 行）；其余无 | 4,627,533 行 | 大而杂，见 R09 详表 |
| R10 AbRank | `Ab_heavy_chain_seq`+`Ab_light_chain_seq` 342,356/342,356 实测 | `Ag_seq` 342,356/342,356 实测 | 342,356 行 | 双侧直接闭合 |
| R11 AbBiBench | `heavy_chain_seq`+`light_chain_seq` 直接可用 | 无列；13 个 case PDB 随包 | 215,699 行 | ag 需按 case 从 PDB 切链 |
| R20 SAbDab2 | `VH` 22,169/22,264、`VL` 17,559/22,264 | 无列；`antigen_chain`+11,604 个 PDB entry FASTA 随包 | 22,264 行 | 缺 VL 4,705 行；ag 需切链 |
| R22 PLAbDab | `heavy_sequence`+`light_sequence` 176,894/176,894 实测 | 无列；`targets_mentioned` 自由文本，23,329 行缺 | 176,894 行 | ag 侧专利/文献行无法闭合 |
| R25 RFdiffusion | 需切：`cdr_seq` 是 CDR 拼接，母本 PDB 需逐条确认 | `target_seq` 8,314/11,777 实测 | 11,777 行 | 两侧都部分 |
| R28 Mason HER2 | 需第三方：只有 `AASeq` CDRH3，README 明确禁止用 1N8Z 拼 | HER2，1N8Z 随包 | 36,391 唯一 CDR3 | ab 不可闭合 |
| R29 RESP | 需第三方：75,631 变体 scFv 序列未在包内；亲本 atezolizumab 未给 | PD-L1，5XXY/5X8L 随包 | 75,631 行 | ab 不可闭合 |
| R34 AbLIFT | `heavy`+`light` 直接可用（2,048 行） | 无列；HEL 1MLC / VEGF 2FJG / QSOX1 4IJ3 随包 | 2,048 行 | 三靶点近似闭合 |
| R36 Hutchinson | `heavy`+`light` 直接可用 | 无列；HEL 1MLC 随包（生物素化构建体未给） | 362 行 / 207 唯一对 | 近似闭合 |
| R37 Jain | `heavy`+`light` 直接可用 | 无列；HEL 1AKI / 鼠溶菌酶 1IVM 随包；mouse-Lysozyme-Fc 融合构建体无 | 31+2 行 | 2 行 Fc 融合不可闭合 |
| R45 Ab-CoV | `VH or VHH`+`VL`（5,033 行，VL 缺 548） | `Ab-CoV_viral_protein.csv` `Protein Sequence` 24 条病毒蛋白（随包）；但行级 `Binds to` 是名称 | 5,033 行 | 需名→序列映射 |
| R46 Shanker | `heavy`+`light` 直接可用 | 无列；Wuhan/BA.1 RBD 在 7MMO/7Y0W 随包；**BQ.1.1/XBB.1.5 无** | 223 行 | 2/4 抗原不可闭合 |
| R47 Rosace | `heavy`+`light`（仅 Adalimumab 14+Golimumab 5 行有） | 无列；HSA 5VNW / TNF 3WD5 / RBD 6W41 随包 | 76 行 | 19 行闭合 |
| R48 Zimmermann | `heavy`+`light` 直接可用（注意：**FLAb 把 heavy/light 语义写反**） | fluorescein 小分子——无蛋白 FASTA | 21 行 | ag 永久不可闭合 |
| R49 Garbinski | `heavy`+`light` 直接可用 | 无列；RSV F 推断（4ZYP/4JHW/6W52 随包），构建体未确认 | 94 对 | ag 构建体未确认 |
| R50 Graphinity | 需切：`ab_chain` 指向 PDB entry 链 | 同表 `ag_chain` | 942,723 + 20,829 行 | 纯计算 ddG |
| R61 CoV-AbDab | `VHorVHH`+`VL` 12,918 行，VL 缺 806 | 无列；`Binds to` 258 种名称 token | 12,918 行 | ag 需外部 |
| R62 CoV-UniBind | `antibody_vh_sequence`+`vl_sequence` 75,459/75,459 实测 | `antigen_sequence` 75,459/75,459、trimmed 22,543 | 75,459 行 | 双侧直接闭合 |
| R66 KyDab | `HEAVY_CHAIN_SEQ`+`LIGHT_CHAIN_SEQ`（zip 内） | `ANTIGEN_NAME` 名称列；部分抗原 FASTA（14 个随包） | 123,527 行 | ab 直接；ag 部分 |
| R69 CH65 | 需拼：`geno` 16 位 + mutation_list + 母本 5UGY（随包） | `MA90`/`SI06`/`MA90-G189E` 3 抗原——**无序列、无对应文件** | 65,536 基因型 | ag 不可闭合 |
| R70 CR9114 DMS | 需拼：VH 120 aa peptide（随包）+ VL 取自 4FQI（随包） | H1/H3/B HA 三抗原——无序列 | 2,521×4 | ag 不可闭合 |
| R71 CGGnaive | 需拼：母本 codon（`CGGnaive_sites.csv` 随包） | IgY CH2（`IgY-CH2.pdb` + 9ODB 随包） | 4,158 设计 | linker 15 位 NA，VH/VL 可拼 |
| R72 Omicron landscape | 4 固定抗体，PDB 随包（7C01/7KMG/6XDG/6WPT） | `geno` 15 位 + `config.yaml.RBD` 两参考 RBD 核苷酸（随包） | 32,768×4 | 双侧可闭合 |
| R73 Background dep | 8 固定抗体：3 个 PDB 随包（7L7E/7MMO/7WHH），**5 个缺失** | `aa_geno` 175 aa RBD 序列（表内直接给） | 51 表 4,795,558 行 | 5 抗体需外部 |

### C 档：需从 PDB/结构切链的角色判定类
| R | 说明 |
| --- | --- |
| R14 AB-Bind | 无序列列，`#PDB`+`Partners(A_B)` 切；5 个 `HM_` 同源模型无真实分子序列 |
| R15 SKEMPI 2.0 | 无序列列，`#Pdb` 切；345 PDB 随包；需判哪侧是抗体（`Hold_out_type` 部分标注） |
| R16 Guest | 无序列列，`pdbs/*_r_b.pdb`（r=抗体）；67 案例，194 PDB 随包 |
| R17 PDBbind PP | 无序列列，2,852 PDB 随包；**无抗体/抗原角色字段**，636 抗体结构需自行判定 |
| R19 DIPS-Plus | `.dill` 序列化，12,601 锚点随包；0.6% 抗体结构，无角色字段 |
| R32 Vreven PPI | `Unbound PDB`/`Complex PDB` 切链；672 PDB 随包；33 抗体案例 |
| R43 Phillips | 需拼：`variant` 16 位基因型 + 论文位点定义；母本 3GBN/4FQI/4FQY 随包；**ag 4 靶点无序列** |
| R57 DACUM | 无序列列，147 PDB 随包；`Hold_out_type` AB/PI,AB 301 条 |
| R58 dbMPIKT | 无序列列，229 PDB 随包；无行级配对键 |

### D 档：不可用/无序列（保留理由）
| R | 原因 |
| --- | --- |
| R18 BIORAD | 数值审计，无序列 |
| R24/R39/R52/R55 | bucket 无数据 |
| R26 Adaptyv EGFR | 混合抗体/非抗体，无类型列，仅 51/402 是抗体形态 |
| R27 Porebski | read 片段非全长，3 个亲本序列均不在包内 |
| R30 Hie | 5 亲本 + UCA 均需第三方；`Design` 只有名称 |
| R31 Cao minibinders | 非抗体 |
| R33 IEDB | 主表无序列；仅 `bcr_full_v3.csv` 6,745/10,461 双链 + `bcr_3d_assays.csv` 5,947 行有 |
| R38 IntAct | MITAB，无序列 |
| R42 MAGMA-seq | `Variant` 突变串编号基准未给；ag S1/HA 无序列 |
| R44 Kirby | `Variant` 需 UCA 母本（GenBank 外部）；ag S1/RBD 无序列 |
| R51 MaveDB | ab 无序列（2D7/12G5），ag 参考序列不随包 |
| R53 Saka | ag 是小分子（犬尿氨酸）；VL 需专利 |
| R56 ASEdb | 无序列列，仅 PDB 参考 |
| R59 BindCraft | 非抗体（de novo binder） |
| R60 AlphaProteo | 非抗体；861 候选仅 25 条有序列 |
| R63 CovEpiAb | ab 无序列，详情页未存档 |
| R64 COVIC-DB | 抗体盲化，无 sequence 映射 |
| R65 BID | 非抗体（一般 PPI 丙氨酸扫描） |

## 关键实测数据（3x5090 上，2026-10-27 断连前测得）

> 这些是直接读下载中的文件得到的，不是 README 转述；供下一轮写代码时引用。断连后本机无法再复核，如需复验请恢复通道。

- R10 AbRank 主表 342,356 行：`Ab_heavy_chain_seq`/`Ab_light_chain_seq`/`Ag_seq` **三列 342,356/342,356 全非空**。
- R12 ASD parquet（20 片，1,177,819 行）：`chains` 槽位统一为 `heavy`/`light`/`full`，**全部行三槽非空**；ag len 14–3011（中位 607）。列：`dataset,affinity,affinity_type,chains,metadata,confidence,nanobody,scfv,processed_measurement`。
- R40 AVIDa-hIL6 57.4 万行：`VHH_sequence` 全非空，`Ag_sequence` 全非空，len 恒 218（27 aa 前缀+185 mature+6 His）。
- R62 CoV-UniBind 6 表 75,459 行：`antibody_vh_sequence`/`vl`/`antigen_sequence` 全非空；`antigen_sequence_trimmed` 22,543（52,749 行只有全长）。
- R03 突变表 1,303 行：`heavy_sequence_variable`/`light_sequence_variable`/`antigen_sequence` 全非空；`antigen_sequence` 33 个唯一值。
- R08/R41：`antigen_sequences.csv` 分别 1/17 条。
- R20 SAbDab2：VH 22,169/22,264，VL 17,559/22,264。
- R22 PLAbDab：heavy/light 176,894/176,894。
- R25 RFdiffusion：`target_seq` 8,314/11,777（缺 3,463）。
- R06/R34/R36/R37/R47/R48/R49：`heavy`+`light` 全非空（规模见各表）。
- R13 ANDD xlsx `Sheet3` 48,800 行：H/L/Ag/Ab_or_Nano/PDB_ID 五列全非空（需复核空字符串 vs NA 编码）。
- R21 AVIDbase xlsx：`vhh_sequence`/`ag_sequence` 1,048/1,048；`ag_uniprot_accession_code` 1,031/1,048。
- R45 `Ab-CoV_viral_protein.csv`：24 条病毒蛋白序列（`Accesssion`+`Protein Sequence`）。
- R70：`Fasta/CR9114_HC_WT.pep`/`GL.pep` 存在（120 aa VH）；VL 需 4FQI。
- R71：`data/wildtype_sequence.fasta` 存在（1,045 nt scFv 母本）；IgY-CH2 PDB 随包。
- R72：`config.yaml.RBD` 存在（含 ancestral/evolved 核苷酸 + `sequence_begins_with_residue: 331`）；5 个 PDB fasta 随包。
- R74：PDB 11OR/11OU/11OQ/11OO/11OL fasta 随包；**Wuhan RBD 无**。
- 服务器 python 环境：`/data_new/ywy/_pyenv`（venv，pyarrow 26.0 + openpyxl 3.1.5 已装，tsinghua 镜像）。

---

## A 档逐 R 详表（ab+ag 双侧表内即可闭合）

### R03 AbDesign DB
- **bucket**：`SRC_R03_ABDESIGN_DB/snapshot-2025-08-26`
- **文件**：`AbDesign/datasets_mut.csv`（1,303 行）+ `datasets_wt.csv`（57 行）
- **ab 列**：`heavy_sequence_variable` / `light_sequence_variable`（VH/VL 可变区，直接可用；另给全长 `heavy_sequence`/`light_sequence` 与 6 个 CDR 列）
- **ag 列**：`antigen_sequence`（逐行，实测 33 个唯一值；README 注明是「PDB 结构条目中的抗原序列」，即晶体构建体；ELISA 包被抗原试剂身份未给）
- **pair 键**：`dataset + index`（index 跨子集重复）；跨来源去重键 = `pdb_name+heavy_sequence_variable+light_sequence_variable+antigen_sequence+mutation_chain_id+mutation_pos_imgt_wt+orig_residue+new_residue`
- **人工多级跳转清单**：无（`antigen_sequence`、VH/VL 均逐行；47 个亲本 PDB 的 FASTA/mmCIF 随包）
- **风险**：`antigen_sequence` 是结构序列而非实验包被抗原；SKEMPIv2/AB-Bind 子集是汇编的异质实验（ELISA/SPR/ITC/KinExA），不同子集的 `affinity` 量纲不同（本轮不需要）；147 个同键跨来源重复不能按键删行；`original_id` 非全局主键。

### R08 AVIDa-hTNFa
- **bucket**：`SRC_R08_AVIDA_HTNFA/snapshot-2025-06-26`
- **文件**：`AVIDa-hTNFa.csv`（5,580 行）+ `antigen_sequences.csv`（1 条）
- **ab 列**：`VHH_sequence`（5,580/5,580 实测非空；106–172 aa，含 N 端信号肽样前缀与末端 6 His，需切——README 未给确切边界）
- **ag 列**：`Ag_sequence`（`antigen_sequences.csv`，`Ag_label=TNFa-WT-beads`，233 aa 人 TNFα 前体；实验用 bead 偶联形式边界未说明）
- **pair 键**：`VHH_sequence + Ag_label`
- **人工多级跳转清单**：无（双侧随包）
- **风险**：`VHH_sequence` 非纯可变域（需切但无规则）；`Ag_sequence` 是前体 233 aa，成熟 157 aa 在 PDB 1TNF（随包，第 143 位 D vs L 与数据不一致）；正例 3 条序列跨两只羊驼，按行切分会泄漏；label 仅二分类。

### R10 AbRank
- **bucket**：`SRC_R10_ABRANK/snapshot-2025-07-08`
- **文件**：`AbRank/abrank-kaggle-v4.zip` → `AbRank_dataset.csv`（342,356 行，**tab 分隔**）
- **ab 列**：`Ab_heavy_chain_seq` / `Ab_light_chain_seq`（**342,356/342,356 实测全非空**；README 未说明 VH/VL 还是全长，需切变区）
- **ag 列**：`Ag_seq`（**342,356/342,356 实测全非空**）；另 `Ag_name`/`Ag_name_details`
- **pair 键**：`Ab_name + Ag_name`（README：每行代表一次配对测量）；缺失值统一为字面 `NA`
- **人工多级跳转清单**：无（`Ab_Hseqs.fasta`/`Ab_Lseqs.fasta`/`Ag_seqs.fasta` 随包）
- **规模**：8 来源 342,356 行（RBD-escape 192,559、CATNAP 74,540、AlphaSeq 71,834、AbCoV 1,392、SKEMPIv2 935、AbSci 758、SabDab 249、OVA-binders 89）；论文称「>380,000」口径不一致
- **风险**：DMS 来源（RBD-escape/AlphaSeq）的突变体行 `Ab_PDB_ID` 指向参考复合物而非逐行；`Ag_seq` 是否等于实际测量构建体未说明；`Ab_name` 在 DMS 下是否逐变体唯一未说明；跨来源 `Ag_name` 命名体系不统一。

### R12 ASD
- **bucket**：`SRC_R12_ASD/2.0`
- **文件**：`asd_2.0/` 20 个 parquet 分片 + `antibodies.csv`/`nanobodies.csv`/`scfv.csv`（3 个 CSV 是同一批数据的子集格式）
- **ab 列**：parquet `chains` 结构内 `antibody_chains`（`heavy`/`light` 槽位；**实测全部行 heavy+light 非空**，1,177,819 行；槽位键名实测为 `heavy`/`light`）
- **ag 列**：同结构 `target_chains`（`full` 槽位，**实测全部行非空**；len 14–3011，中位 607）；`metadata.target_pdb`/`target_uniprot` 伴随
- **pair 键**：`dataset + metadata.source_url + chains` 组合；`affinity_type` 区分端点；无逐行唯一键
- **人工多级跳转清单**：无（2,227 个 `target_pdb` 的 FASTA 随包）
- **规模**：1,177,819 行；论文旧口径 1,097,946 相互作用 / 865,153 独特抗体 / 716,650 完整重轻链 / 9,575 抗原实体（不可相加）
- **风险**：`nanobody`/`scfv` 布尔 127 个 null；9,159 抗体 map 值、2,536 靶点 map 值含 `X`；`affinity_type` 混合 `-log Kd (M)`/`ic_50`/fuzzy h-m-l/bool；CSV 与 parquet 装同一批数据（第一轮普查已确认），合并会重复计数。

### R13 ANDD
- **bucket**：`SRC_R13_ANDD/snapshot-2026-01-05`
- **文件**：`ANDD/Antibody and Nanobody Design Dataset (ANDD)_v2.xlsx`（`Sheet3` 48,800 行 × 49 列，实测）
- **ab 列**：`Ab/Nano H_Chain AA` / `Ab/Nano L_Chain AA`（**实测全非空**；另有 `Ab_or_Nano` 区分抗体/纳米抗体、`Ab/Nano_CDR *` 6 列）
- **ag 列**：`Ag_Seq`（**实测全非空**）+ `Ag_Name`/`Ag_Entity ID`/`Ag_Accession Code(s)`/`Ag_Database Name`
- **pair 键**：`PDB_ID + H_Chain Auth Asym ID + L_Chain Auth Asym ID + Ag_Auth Asym ID`（`PDB_ID` 缺 27,952 行，不可单独作键）
- **人工多级跳转清单**：6 个 obsolete 原条目（`5USI`/`6CSY`/`6ERX`/`7KGL`/`7N01`/`7N0S`）原生 FASTA 不可恢复，**现有来源无法闭合**；其余 8,421 锚点随包
- **规模**：48,800 行（398 个精确重复行）；论文口径 48,683 条序列 / 9,557 亲和力；`Affinity_Kd` 非 NA 8,042 行
- **风险**：README 的缺失统计（H 360、L 31,435、Ag 36,183）与实测全非空矛盾——README 可能按 NA 编码计缺而 xlsx 空字符串；`Predicted_or_Not` 2,271 条是 ANTIPASTI 预测（非实验）；PDB 连接为 entry 级，链角色需复核。

### R21 AVIDbase
- **bucket**：`SRC_R21_AVIDBASE/snapshot-2026-07-29`
- **文件**：`AVIDbase/AVIDbase.xlsx`（4 sheet：nr 691 / prot 592 / low 100 / r 1,049 行）
- **ab 列**：`vhh_sequence`（**1,048/1,048 实测非空**；纯 VHH 单域）
- **ag 列**：`ag_sequence`（**1,048/1,048 实测非空**；逗号分隔多抗原链；`ag_uniprot_accession_code` 1,031/1,048）
- **pair 键**：`unique_id`（形如 `1g6v_0`，= `PDB + interface_index`）
- **人工多级跳转清单**：无（836 个 PDB FASTA/mmCIF 随包）
- **规模**：1,048 行（r 档）；nr 690 行（README 称 689，保留原文件）
- **风险**：`ag_sequence` 含 X 残留；一条记录多抗原链时 `ag_sequence` 逗号分段与 `ag_auth_chain_id` 顺序对应未说明；仅 VHH，无常规 VH+VL。

### R23 AlphaSeq v1 / R35 Li AlphaSeq v2
- **bucket**：`SRC_R23_ALPHASEQ/v1.0.0` / `SRC_R35_LI_ALPHASEQ/v2.0.0`（同一 schema 体系）
- **文件**：`AlphaSeq_Antibody_Dataset-v1.0.0.zip` → `MITLL_AAlphaBio_Ab_Binding_dataset.csv`（1,259,700 行，实测表头 `POI,Sequence,Target,Assay,Replicate,Pred_affinity,HC,LC,CDRH1,CDRH2,CDRH3,CDRL1,CDRL2,CDRL3`）；v2.0 含 `antibody_dataset_1` + `dataset_2`
- **ab 列**：`HC`+`LC`（可变区，直接可用）；`Sequence` 为 scFv 全长（v1 实测含 GGGGS linker；README 注明 v1 有 990,000 行 HC-LC 顺序 + 269,700 行 LC-HC 顺序，不能用 `Sequence` 顺序概括）
- **ag 列**：无序列列。靶点 1 个：SARS-CoV-2 HR2 13 aa 肽 `PDVDLGDISGINAS`（README 正文逐字给，`6LXT` entity 1 含该肽，已随包）；3 个阴性对照 `AlphaNeg1/2/3` **无序列**
- **pair 键**：`POI + Target + Assay + Replicate`（实测无重复键）
- **人工多级跳转清单**：`AlphaNeg1/2/3` 三条阴性对照肽序列——README 未说明在包内任何文件
- **规模**：v1 1,259,700 行 / 104,972 POI / 104,968 唯一 scFv / 352,139 有限 `Pred_affinity`；v2 dataset_1 1,259,701 + dataset_2 1,903,928；共享 759 条相同全 scFv
- **风险**：`Pred_affinity` 是 AlphaSeq 校准估计而非 BLI/SPR；`POI` 与 `Sequence` 不一一对应；阴性对照无法闭合；v1 两种链顺序并存。

### R40 AVIDa-hIL6
- **bucket**：`SRC_R40_AVIDA_HIL6/1.0.0`
- **文件**：`AVIDa-hIL6-Zenodo/il6_aai_dataset.csv`（573,891 行，实测）
- **ab 列**：`VHH_sequence`（**573,891/573,891 实测非空**；38,599 唯一；含 N 端信号肽前缀 `MKYLLPTAAAGLLLLAAQPAMA` 与末端 `HHHHHH`，需切无规则）
- **ag 列**：`Ag_sequence`（**573,891/573,891 实测非空，len 恒 218** = 27 aa 前缀 + 185 aa mature IL-6 + 6 His；README 明确构建体边界）；31 个抗原键（30 突变体 + `IL-6_WTs` 三组 WT 合并键）
- **pair 键**：`(VHH_sequence, Ag_label)` 573,891 唯一，无孤立 join
- **人工多级跳转清单**：无
- **规模**：573,891 配对（正 20,980 / 负 552,911）；420 个 FASTA 库 24,036,149 条；论文 1,998,127 non-significant 配对不在包内
- **风险**：VHH 串非纯域；`Ag_label` 的 `IL-6_WTs` 是三组 WT 合并；`#ONU ID` 不跨表唯一，跨表只能靠序列串。

### R41 AVIDa-SARS-CoV-2
- **bucket**：`SRC_R41_AVIDA_SARS_COV2/snapshot-2024-10-17`
- **文件**：`AVIDa-SARS-CoV-2/AVIDa-SARS-CoV-2.csv`（77,003 行）+ `train.csv`（49,685）+ `test.csv`（27,318）+ `antigen_sequences.csv`（17 条）
- **ab 列**：`VHH_sequence`（77,003/77,003 实测非空；36,100 唯一；94–166 aa，部分含信号前缀）
- **ag 列**：`Ag_sequence`（`antigen_sequences.csv`，17 条，521–1,328 aa；`Ag_label` 必须带 `_bead`/`_cell` 后缀，同变体名两种 construct 长度不同）
- **pair 键**：`VHH_sequence + Ag_label`（train/test 并集=总表，264 条 VHH 跨 train/test）
- **人工多级跳转清单**：无
- **风险**：VHH 串含前缀需切；`_bead`/`_cell` 后缀删掉即错配；17 条件键 vs 论文 12 抗原口径不同。

### R67 Open AlphaSeq
- **bucket**：`SRC_R67_OPEN_ALPHASEQ/snapshot-2025-12-04`
- **文件**：`open-alphaseq/data/YM_XXXX/data.parquet`（9 张，实测表头 `mata_description,matalpha_description,mata_sequence,matalpha_sequence,alphaseq_affinity,affinity_lower_bound,affinity_upper_bound,normalized_affinity,above_background,sufficient_replicate_observations`）
- **ab 列**：`mata_sequence`（按实验区分：YM_0549/1068 VHH72 变体；YM_0693/0988 PP489/ABC001 scFv；YM_0852/0985 Pembrolizumab scFv；YM_0989/0990 Trastuzumab scFv；YM_0005 抗冠状病毒面板，`m396_scFv_LH_Mod` 用 `&` 连接轻重两段）。scFv 需按 linker 切 VH+VL；VHH 单域直接可用（VHH72 125 aa 与沉积完全匹配）
- **ag 列**：`matalpha_sequence`（完整构建体 AA 串：122 aa PD-1、209 aa RBD、120 aa HER2、TIGIT、S1/S2 等；README 逐条给出与沉积的连续相同片段关系）
- **pair 键**：`(mata_description, matalpha_description)` 按文件限定
- **人工多级跳转清单**：无（亲本 Pembrolizumab/Trastuzumab/VHH72/CR3022 以 WT 行出现在 `mata_sequence` 内；6 个 PDB 锚点随包）
- **规模**：9 表共 1,705,908 行（163,882/299,910/407,803/134,580/186,745/120,208/148,128/94,604/150,048）；有限 affinity 1,378,079 行
- **风险**：YM_0985/0988/0990 数据卡与实际文件不一致；`&` 分隔规则上游未说明；HL/LH 两种 scFv 方向并存去重时不能当两个抗体。

### R74 Omi32 BioPhy-Seq（部分闭合）
- **bucket**：`SRC_R74_OMI32_BIOPHY_SEQ/snapshot-2026-05-30`
- **ab 列**：`geno`（13 位二元位点码，2^13=8,192）+ `aa_substitutions`/`codon_substitutions` + 母本 Omi32 Fab（`pdb/sequences/rcsb_pdb_11OR.fasta`）与 germline（`11OU.fasta`），**均随包**。需拼：13 位点替换叠加到母本
- **ag 列**：`solute`/`antigen` 取值 `BA1`/`BA4`/`WUHAN`/`WH`/`PSR`；BA.1 RBD 在 `11OQ.fasta`、BA.4 在 `11OO`/`11OL.fasta`（随包）；**Wuhan RBD 无对应 PDB，需外部**
- **pair 键**：`geno`（文本二元键）+ 表型表（`wuhan_log10Kd_mean`/`ba1_log10Kd_mean`/`ba4_log10Kd_mean`/`expr_mednorm_mean`/`PSR_log10EC50`）
- **人工多级跳转清单**：`WUHAN` RBD 序列（5 个 PDB entry 均无武汉株抗原）
- **规模**：5 张 cleaned 表 6,740/7,037/7,416/8,150/5,510 个唯一 `geno`；预测表 5×8,192
- **风险**：`region` 表含 `CH/CK/TM/SP1/P2A/Myc` 等构建体区域，实验构建体比 Fab 长，Fv 级切分需自行判定；低通量表 3 个短 `geno` 与 13 位主表不可确定性连接。

---

## B 档逐 R 详表（ab 直接可用，ag 需随包 PDB/外部）

### R01 IgDesign
- **bucket**：`SRC_R01_IGDESIGN/snapshot-2025-01-10`
- **ab 列**：`HCDR1`/`HCDR2`/`HCDR3`（8 张 `igdesign/data/*.csv` + `Blinded/Ravagalimab-CD40.csv`）。**需拼**：三段 HCDR 替换回参考抗体可变域；母本在 `pdb/sequences/rcsb_pdb_<PDB>.fasta`（10 个参考/独立 Fab，随包）与 `sabdab/summaries/pdb_0000*.csv` 的 `VH`/`VL` 列（10 实例随包）
- **ag 列**：无序列列。`Target` 8 个文本：IL17A/ACVR2B/CD40/C5/FXI/IL36R/TSLP/TNFRSF9。参考复合物 PDB 随包（6PPG/5NGV/6PE8/5I5K/6HHC/6U6U/5J13/6A3W + 5NHW/6PE7）。SPR 抗原试剂（ACRO Biosystems）货号/序列未给
- **pair 键**：`Target + Reference Ab + HCDR1 + HCDR2 + HCDR3`（README 未定义主键）
- **人工多级跳转清单**：8 系统的 SPR 抗原试剂（ACRO 货号，需向作者索取）；CD40 盲化设计（136 条 HCDR3 + 64 条 HCDR123 为 `X`，包外无来源）
- **规模**：1,444 行（8 表 179/212/201/198/116/177/176/185；1,436 非对照 + 8 阳性对照）；1,243 行可拼（7 系统未盲化）；标签 286 binder/1,158 non-binder
- **风险**：CD40 的 200 条设计 HCDR 掩码无法闭合；`6PPG` 抗原是 IL-17F 与 `Target`=IL17A 冲突（Q01）；HCDR 的 CDR 定义/编号方案未说明，替换回母本的具体位置无定论。

### R02 Absci HER2
- **bucket**：`SRC_R02_ABSCI_HER2/snapshot-2024-08-08`
- **ab 列**：`spr-controls.csv` 的 `HCDR1`/`HCDR2`/`HCDR3`（1,855 行）；`zero-shot-binders.csv` 只有 `HCDR3`（422 行）。**需拼**：HCDR 替换进 trastuzumab Fab 227 aa 重链 + 214 aa 轻链（`unlocking-de-novo-antibody-design/README.md` 随包）
- **ag 列**：无序列列。human HER2 ECD；参考 1N8Z（沉积 607 aa）+ 作者仓库 630 aa（随包）；交叉反应 cyno/canine/mouse HER2 + HER1/3/4 **无序列**
- **pair 键**：`HCDR1+HCDR2+HCDR3`（1,855 唯一）；zero-shot 以 `HCDR3` 键可逐条回连 controls（同 HCDR3 + trastuzumab 背景 + 相同 KD）
- **人工多级跳转清单**：4 个交叉反应抗原（cyno/canine/mouse HER2、HER1/3/4）无序列无货号；421 条设计的 full-length mAb 构建体未公开
- **规模**：1,855 行（758 binder/1,097 non-binder）；唯一 ab–ag 配对 = 1,855（单抗原）
- **风险**：controls 无字段区分 HCDR3-only 与 HCDR123；17 个 HCDR3 出现在多个 HCDR1/2 背景且 2 个 HCDR3 在不同背景下 binder/non-binder 各一——必须用完整三元组；ag 构建体边界与交叉反应序列缺失。

### R04 IPI
- **bucket**：`SRC_R04_IPI/zenodo-15367597`（旧）+ `zenodo-15707494`（新）
- **ab 列**：NGS 表 `CDR3`+`heavy`+`light`；486 表 `Antibody_Name`+`Antigen`+`Antigen Recognition Module (ARM)`+`CDRH3`；FLAb `heavy`+`light`。`heavy`/`light` 是模板 ID（VH1-69/VK1-39/VK3-15/VK3-20/VK4-1）。**需拼**：CDR3 换入 `0Library_keys.xlsx` 模板段（随包，含 X 占位符）
- **ag 列**：CSV 无序列列；`0Library_keys.xlsx` 抗原段含 **10 个抗原构建体序列**（含 C 端标签；SPR 用可溶性截短，cell display 用较完整构建体），**随包**；FLAb `antigen_seq` 另给
- **pair 键**：`Antigen + CDR3 + heavy + light`；486 表 `Antibody_Name`；NGS `CDR3` 与 486 `CDRH3` 差一个前导 `C`，连接前须归一化
- **人工多级跳转清单**：无（10 个抗原构建体 + 5 个种系模板随包；10 个代表 PDB 随包但不等于实验构建体）
- **规模**：旧版 22 NGS 表 94,274 行 + 486 表 486 行 + FLAb 709 行（385 唯一抗体）；新版 4 张 ML 输入表 383,341 行
- **风险**：模板含 X 占位符，CDRH3 插入边界需自定；FLAb 重链 `YYCARCAR` 重复（Q02）；PD-L2/ROBO2N 29 条 ML 派生 SPR 值标 `KD (nM)` 但 M 量级；DKK1 实验用鼠但代表结构是人。

### R05 Tite-Seq
- **bucket**：`SRC_R05_TITESEQ/snapshot-2017-09-24`
- **ab 列**：`CDR1H_AA`/`CDR3H_AA`（各 10 aa）+ 核酸 `CDR1H`/`CDR3H`。**需拼**：两段 CDR 放回 WT 4-4-20（`pdb/sequences/rcsb_pdb_1FLR.fasta` 随包，H/L 各 219 aa）；scFv linker 未给
- **ag 列**：fluorescein **小分子**——无蛋白 FASTA（`1FLR` mmCIF 含配体坐标随包，无 SMILES）
- **pair 键**：无列名 index + 来源文件；序列级键 `CDR1H+CDR3H`
- **人工多级跳转清单**：OPT 超高亲和力对照（含 1H/3H 外突变）与 Δ 无功能对照（大段缺失）**需外部**，不能由公开字段重建；scFv linker 序列 README 未说明
- **规模**：3 replicate 11,039 行；唯一核酸对并集 3,682、AA 对并集 2,807
- **风险**：**ag 侧永久不可闭合（小分子）**；CDR 边界/编号定义未说明；7,411 行 `fit_KD` 在检测边界（标签非本轮必需）。

### R06 Koenig
- **bucket**：`SRC_R06_KOENIG/snapshot-2026-08-17`
- **ab 列**：`heavy`（120 aa）+`light`（108 aa），**直接可用**（G6.31 Fv 变体）
- **ag 列**：无序列列。VEGF-A（人）；PDB 2FJG（chain V，102 aa）+ 游离 Fab 2FJF 随包；实验生物素化 VEGF 构建体未给
- **pair 键**：`heavy + light`（4,275 唯一对，binding/expression 两表同集合）
- **人工多级跳转清单**：实验用生物素化 VEGF 试剂完整序列（README 未说明）
- **规模**：binding 4,275 + expression 4,275 行
- **风险**：2FJG 抗体是 G6 而数据是 G6.31（CDR-L3 4 处替换）；2FJG 的 102 aa VEGF 是否等于实验抗原未定；binding 表 KD 是 FLAb 全量派生值，论文只对少量候选做 SPR。

### R07 Makowski MET
- **bucket**：`SRC_R07_MAKOWSKI/snapshot-2022-06-24`
- **ab 列**：`VH Sequence`（115 aa，**直接可用**）——但 **VL 缺失**（emibetuzumab 轻链可变区不在包内），**需第三方**
- **ag 列**：无序列列。人 HGFR/MET（MET-Fc）；`6WVZ` MET Sema（534 aa）随包，README 明确「论文未给出 HGFR-Fc 完整构建体序列」
- **pair 键**：各表内 `VH Sequence`（iso 表另 `Sample`）
- **人工多级跳转清单**：emibetuzumab 轻链可变区（不在包内）；人 HGFR-Fc 实验抗原构建体；OVA/CHO SMP 序列（非特异性对照）
- **规模**：emi 4,000 + iso 126 + igg 96 行（跨表重叠 24/0/16）
- **风险**：**ab 缺 VL 不能闭合**；4 个 PDB 只是 homology model 模板（非 emibetuzumab）；三表分子形式不同（scFab 酵母/IgG beads），同序列跨表非重复测量。

### R09 FLAb / FLAb2（大而杂，单列）
- **bucket**：`SRC_R09_FLAB/snapshot-2026-08-17`
- **文件**：`FLAb/data/binding/` 80 张 CSV（97,749 行）+ 6 个 zip（AbRank 子表 342,356、engelhart 94 MB、li2023 两份 736 MB/1.1 GB、tsuruta 两份）+ `score/` 派生目录（esmif 等，非实验）
- **ab 列**：`heavy`（161 表）/`light`（157 表）；AbRank 子表 `Ab_heavy_chain_seq`/`Ab_light_chain_seq`；部分表只给 CDR 列（11 表，母本不在包内）
- **ag 列**：仅 **20 表**带 `antigen_seq`（实测：19 张 kothiwal2025htp_* 709 行 + 1 张 hie2023？）；另有 29 张表 `Antigen` 只是名称列；其余 50+ 表无抗原列
- **人工多级跳转清单**：无 `Ag_seq`/`antigen_seq` 的表需回各自原研究取靶点序列（README **未列出表名与靶点名**）
- **规模**：165 表 4,627,533 行（binding 86 表 4,606,788）；30 个 study；11 张表 581,237 个精确重复行
- **风险**：无跨表统一 pair 键；`heavy` 构型不明（VHH/重链/其他）；`li2023machine_affinity2` 前六行为说明文本（非表头）；跨 assay 单位方向不统一。**FLAb 与 R06/R34/R36/R37/R46/R47/R48/R49/R04 的原表重复**——第一轮普查已确认 R09 是汇编层，用 FLAb 表时须按 study 去重。

### R11 AbBiBench
- **bucket**：`SRC_R11_ABBIBENCH/snapshot-2026-05-02`
- **ab 列**：`heavy_chain_seq`+`light_chain_seq`（17 张 CSV，**直接可用**；长度 117–121/211/215 aa，非全 IgG 也非全可变区——混合）
- **ag 列**：无序列列。13 个 case 由文件名与 `complex_structure/*.pdb`（随包）+ `pdb/sequences/` 8 个接受锚点 FASTA 决定
- **pair 键**：无逐行键；抗原由所属 CSV 文件（case）决定；行级内容 `heavy_chain_seq+light_chain_seq`
- **人工多级跳转清单**：`1mlc_LC`、`1mhp` 两表的 metadata affinity_data 路径在固定 tree 中不存在；`5a12_vegf` epitope/paratope 与 `antigen_chain` 冲突需人工重判链角色
- **规模**：17 CSV 215,699 行；论文「>184,500」与「14/16/17 assays」三口径并存
- **风险**：ag 完全依赖 PDB 条目 + 链选择，metadata 链映射部分缺失/冲突；附录表（5a12_ang2/5a12_vegf/g6_LC/aayl50_LC/aayl52_LC）无 `complex_structure` 同名文件；无抗体标识无法判跨表重复。

### R20 SAbDab / SAbDab2
- **bucket**：`SRC_R20_SABDAB/snapshot-2026-09-11`
- **ab 列**：`VH`+`VL`+6 个 CDR 列（`sabdab2_summary.csv`，22,264 行；**实测 VH 22,169/22,264、VL 17,559/22,264**）；`type` 区分 FAB 10,470/FV 6,954/SD-H 4,614/SD-L 95/FAB+FC 40/VNAR 91
- **ag 列**：无序列列；`antigen_chain`/`antigen_name`/`antigen_species`；11,604 个 PDB entry FASTA/mmCIF 随包（`SAbDab2/sabdab_search_structures_20260918T143233.tar` 尚未下载完成，entry 级 FASTA 已随包）
- **pair 键**：`INSTANCE + antigen_chain`（`|` 分隔分量同位置对应）
- **人工多级跳转清单**：无（entry 级 FASTA/mmCIF 随包）
- **规模**：22,264 行 / 11,604 PDB / 6,897 唯一 SABDAB_ID
- **风险**：README Q01 明确「尚未建立 INSTANCE → author/label 链的可核验映射」，ag 切链可能错；hapten/ion 类行无 polymer 序列；缺 VL 4,705 行；同 PDB 多 instance 共用一套坐标。

### R22 PLAbDab
- **bucket**：`SRC_R22_PLABDAB/snapshot-2024-08-28`
- **ab 列**：`heavy_sequence`+`light_sequence`（`paired_sequences.csv.gz`，**实测 176,894/176,894 非空**；含 B/Z 等模糊字符）
- **ag 列**：无序列列。`targets_mentioned` 自由文本（23,329 行缺）；仅 `pairing=Xtal structure` 12,778 行可回 PDB entry（随包）
- **pair 键**：`ID` 唯一标识抗体；ab–ag 无唯一配对键
- **人工多级跳转清单**：7 个 PDB（4OZ4/5USI/6ERX/7CTU/7CU4/7CU7/7N01）缺完整上游 FASTA 配对；全部专利/文献行需回原专利取抗原序列（无专利号列）；`TheraSAbDab` 行模型名
- **规模**：paired 176,894 行（去重 78,868 对）；unpaired 673,959 行（L 287,636 + H 386,323）
- **风险**：**专利/文献行 ag 无法闭合**；`targets_mentioned` 只是「原材料提及」，非结合真值；`model` 是 ABodyBuilder2 预测非实验坐标。

### R25 RFdiffusion（部分闭合）
- **bucket**：`SRC_R25_RFDIFFUSION/snapshot-2025-06-25`
- **ab 列**：`cdr_seq`（CDR 拼接，非完整抗体）；`ab_chains` 给链角色。**需切**：从 `pdb/sequences/rcsb_pdb_<PDB>.fasta` 按 `ab_chains`/`Hchain`/`Lchain` 切母本链；**须逐条确认母本存在**（抽查 7T82 可拼、7T86 的 39 aa 无对应）
- **ag 列**：`target_seq`（**实测 8,314/11,777 非空**，len 4–1075）；`protein_target_chains`/`antigen_chain`
- **pair 键**：`pdb + ab_chains + protein_target_chains`（`model` 区分同一 entry 的模型）
- **人工多级跳转清单**：10 个撤回条目（4OZ4/5USI/6CSY/6ERX/7CTU/7CU4/7CU7/7KGL/7N01/7N0S）缺完整上游 FASTA/mmCIF；论文验证候选序列只在 supplement PDF，CSV 无这些设计序列
- **规模**：11,777 行（negative_example 5,857/5,920；validation_set 1,125/10,652）；6,205 主 pdb；6,209 锚点接受
- **风险**：`cdr_seq` 只有 CDR；`Hchain` 缺 391、`Lchain` 缺 2,085；`target_seq` 缺 3,463（与 `negative_item` 同数）；`negative_example` 是构造负例非实验不结合；论文实验候选与 CSV 不同源。

### R28 Mason HER2
- **bucket**：`SRC_R28_MASON/snapshot-2020-09-02`
- **ab 列**：`AASeq`（CDRH3）+`NucSeq`；**无 VH/VL**。README 明确「不能拼接亲本生成未发布的完整抗体」，**禁止用 1N8Z 拼出** → **需第三方（作者申请）**
- **ag 列**：HER2；1N8Z 随包（共享亲本 Fab/HER2 复合物）
- **pair 键**：`AASeq + AgClass`
- **人工多级跳转清单**：完整 IgG 变体序列（未公开，需向作者申请）
- **规模**：AgNeg 27,539 + AgPos 11,300 行；合并 36,391 唯一 CDR3
- **风险**：ab 不可闭合；`AgClass` 是分选类别非 KD。

### R29 RESP
- **bucket**：`SRC_R29_RESP/snapshot-2025-06-27`
- **ab 列**：无完整变体序列列。`orig.csv`/`decoys.csv` 是 ANARCI 编号表；`Test_set_score_distribution.csv` 只有 `Category`+`ordinal_regression_score`。**75,631 变体 scFv 序列未在包内；亲本 atezolizumab 未给** → **需第三方**
- **ag 列**：PD-L1；5XXY/5X8L 随包（atezolizumab Fab / PD-L1 亲本结构）
- **pair 键**：README 未说明——`Category` 类序数与变体序列之间无共同键
- **人工多级跳转清单**：atezolizumab scFv 重轻链序列；75,631 变体抗体 FASTA；`encoded_data.tar.gz` 内编码数组
- **规模**：75,631 行（Figure 6B）；Figure 5A/B/C 各 47,773/47,773/47,775
- **风险**：**ab 不可闭合**；变体序列与类别标签无法 join；5XXY/5X8L 是 Fab 与 scFv 构建体不等同；许可 All Rights Reserved。

### R34 AbLIFT
- **bucket**：`SRC_R34_ABLIFT/snapshot-2019-08-23`
- **ab 列**：`heavy`（114 aa）+`light`（108 aa），**直接可用**（2,048 行 D44.1 单点变体）
- **ag 列**：无序列列。HEL（1MLC 随包，entity 3 chains E/F）、VEGF（2FJG 随包）、QSOX1（4IJ3 随包）
- **pair 键**：`heavy+light` 组合（无 ID 列）
- **人工多级跳转清单**：无（3 靶点 PDB 随包）
- **规模**：FLAb 2,048 行；S4 115 位置 2,209 单元格；论文 2,294 单点突变
- **风险**：`KD (nM)` 是 `exp(−round(S4 单元格,2))` 的数学变换非独立测量；3 个靶点共享 2,048 行变体（README 未给抗原分配键？需按实验区分）；construct 一致性未验证。

### R36 Hutchinson NIP228/HEL
- **bucket**：`SRC_R36_HUTCHINSON/snapshot-2026-08-17`
- **ab 列**：`heavy`+`light`（12 张 CSV，**直接可用**；VH/VL 可变区）
- **ag 列**：无序列列。HEL（鸡卵清溶菌酶，生物素化）；1MLC 随包（entity 3，chains E/F）
- **pair 键**：`heavy+light` + 来源文件名（multikd/singlekd/top200/top27 实验组）
- **人工多级跳转清单**：无（HEL 1MLC 随包）
- **规模**：8 binding 表 362 行 / 197 唯一对 + 4 Tm 表 258 行；207 唯一对合计
- **风险**：生物素化 HEL 构建体边界未给；IgG 恒定区未给（完整 IgG 无法重建）；4,602 候选仅 207 公开。

### R37 Jain 2024
- **bucket**：`SRC_R37_JAIN/snapshot-2026-08-17`
- **ab 列**：`heavy`+`light`（2 张 CSV，**直接可用**）
- **ag 列**：无序列列。HEL（1AKI 随包，129 aa）；mouse lysozyme-**Fc 融合**（1IVM 随包但 README 明确「不能把 1IVM 当成 mouse-lysozyme-Fc 结构」）
- **pair 键**：`heavy+light` + 文件名
- **人工多级跳转清单**：mouse-Lysozyme-Fc 融合构建体序列（CSV 与 XLSX 均未给）
- **规模**：HEL 31 行 + mouse 2 行；并集 31 个 VH/VL；原 XLSX 43 个 ADI 抗体
- **风险**：**mouse-Fc 2 行不可闭合**；HEL 与 1AKI 一致性未验证；53 个 `N.B.` 阴性只在 XLSX。

### R45 Ab-CoV
- **bucket**：`SRC_R45_ABCOV/figshare-5661658-v1`
- **ab 列**：`CoV-AbDab_220222.csv` 的 `VH or VHH`+`VL`（5,033 行，VL 缺 548）；`Ab-CoV_interface_detail.csv` 的 `vh_or_vhh`+`vl`（133 行）；FLAb 两表 `heavy`+`light`（KD 141、IC50 427 行）
- **ag 列**：`Ab-CoV_viral_protein.csv` 有 **24 条病毒蛋白序列**（`Accesssion`+`Protein Sequence`，**实测随包**）；但行级抗原只给 `Binds to` 名称（多值分号分隔）
- **pair 键**：`Name + Binds to`（CoV-AbDab）；`pdb_id+ab+binds_to`（interface）；FLAb 两表**无名称/株/方法/文献/PDB 键**
- **人工多级跳转清单**：`Binds to` 258 种 token → 24 条病毒蛋白或外部库的映射；FLAb 141/427 行的原始抗体名/株/方法；81 个仅来源级连接的 PDB 与抗体行的对应；552 个治疗性抗体序列（identity 矩阵只有百分比）
- **规模**：5,033 + 133 + 141 + 427 行；24 病毒蛋白；214 PDB
- **风险**：无统一严格配对键；`Binds to` 多值名称；FLAb 两表完全无抗原标识；缺 light 的 32/25 行不能与 VHH 自动区分。

### R46 Shanker
- **bucket**：`SRC_R46_SHANKER/zenodo-11260318`
- **ab 列**：`heavy`+`light`（7 张 FLAb CSV，**直接可用**；Ly1404 119/109 aa、SA58 120/109 aa）
- **ag 列**：无序列列。SARS-CoV-2 Wuhan/BA.1/BQ.1.1/XBB.1.5；Wuhan RBD 在 7MMO 随包（205 aa S1）、BA.1 在 7Y0W 随包（193 aa）；**BQ.1.1 与 XBB.1.5 无序列**
- **pair 键**：文件名（亲本+抗原株+端点）+ `Design` + `heavy`+`light`
- **人工多级跳转清单**：BQ.1.1 RBD、XBB.1.5 RBD（2 个抗原完全无序列）
- **规模**：7 表 223 行（IC50 150 + KD 73）；唯一 VH/VL 45/32/32/19/46/7/26
- **风险**：**2/4 抗原不可闭合**；7MMO/7Y0W 是共享亲本复合物非逐行结构；KD 是 bivalent IgG apparent KD 而 FLAb 只给 VH/VL。

### R47 Rosace
- **bucket**：`SRC_R47_ROSACE/snapshot-2023-04-06`
- **ab 列**：`heavy`+`light`（仅 Adalimumab 14 行 + Golimumab 5 行有完整序列，**实测**）；其余 4 亲本（Nb.B201/CR3022/H11-D4/H11-H4）FLAb 表内无序列行（需从 5VNW/6W41/6YZ5/6ZBP 取，随包）
- **ag 列**：无序列列。HSA（5VNW 随包 585 aa）、TNFα（3WD5/5YOY 随包）、SARS-CoV-2 RBD（6W41/6YZ5/6ZBP 随包）
- **pair 键**：`Ab + Mutations`（FLAb binding，单抗原由文件名区分）
- **人工多级跳转清单**：4 个亲本在 Fig S9 48 个 KD 单元格的逐行抗体名（表内只有位置无 `Ab` 列）；5 个亲本的抗原 construct 序列（PDB 参考随包，实验构建体未知）
- **规模**：FLAb 8 CSV 共 76 行（19 种设计 × binding/CIC/Tm 复本）
- **风险**：FLAb 只覆盖 2 亲本 19 设计，其余 4 亲本只有论文图 48 个 KD 单元格；`KD (nM)` 表头与 M 尺度数值冲突；补充 Table S1 construct 含连接肽/标签而 FLAb 是分离可变区。

### R48 Zimmermann
- **bucket**：`SRC_R48_ZIMMERMANN/snapshot-2026-08-17`
- **ab 列**：`heavy`+`light`（21 行，**实测全非空**）——**注意 FLAb 把字段语义写反**：`heavy` 是 112-aa 轻链可变区，`light` 才是 118-aa 重链可变区，需显式反转
- **ag 列**：fluorescein **小分子**——无蛋白 FASTA
- **pair 键**：`heavy+light`（反转后）
- **人工多级跳转清单**：无（1FLR 随包，仅成熟 4-4-20 参考）
- **规模**：21 行 / 20 唯一 VL/VH 组合；唯一 VL 2 种、VH 18 种
- **风险**：**ag 永久不可闭合（小分子）**；README 记录 12 条 mature-VL 的 VH 第 37 位为 S 而论文/1FLR 为 V，序列本身存疑。

### R49 Garbinski/GSK
- **bucket**：`SRC_R49_GARBINSKI_GSK/snapshot-2026-08-17`
- **ab 列**：`heavy`+`light`（3 张 CSV，**实测 81 行全非空**；120–126/106–114 aa；4 个参考对 AM14/D25/Motavizumab/RSB1 有样本名，其余 90 对无标识）
- **ag 列**：无序列列。RSV F（推断；4ZYP/4JHW/6W52 随包，**构建体/株系/方向未确认**——README Q02）
- **pair 键**：`heavy+light`（三表以 (heavy,light) 连接）
- **人工多级跳转清单**：GSK KD assay 实际抗原 construct（构建体、株系、方向）；81 个 KD 对的上游候选名称/设计谱系
- **规模**：94 唯一对（KD 81 / Tm1 86 / expression 94；交集 74）
- **风险**：**ag 构建体未确认**；其余 90 对无样本名只能按 Levenshtein 最近参考分组；三表无 replicate ID。

### R50 Graphinity
- **bucket**：`SRC_R50_GRAPHINITY/v1`
- **ab 列**：`pdb`+`complex`+`ab_chain`+`ag_chain`（`Synthetic_FoldX_ddG_942723.csv`、`Synthetic_FlexddG_ddG_20829.csv`）；`Experimental_ddG_645/608` 另给 `chain_prot1`/`chain_prot2`。**需切**：从 `pdb/sequences/rcsb_pdb_<ID>.fasta`（1,406 个随包）取 `ab_chain` 对应 entity 切可变区；README 未给切分边界
- **ag 列**：`ag_chain` 指向同一 entry 的抗原链（FASTA/mmCIF 随包）
- **pair 键**：`pdb + complex + ab_chain + ag_chain`（`(pdb,complex)` 有 76 组重复键，必须加链角色）
- **人工多级跳转清单**：`7CU4`（RCSB REMOVED 不可取得）；4 个 synthetic mutated/wt PDB 归档 **bucket 未包含**
- **规模**：942,723 + 20,829 行（纯 FoldX/Flex 计算 ddG）；Experimental 645/608 单点突变
- **风险**：突变体序列需应用 `complex` 中的单点突变而 WT/mutant 结构包不在 bucket；`ab_chain` 是否完整 Fv 及切分边界未说明；标签为计算值非实验测量；645 中 5 个复合物不是抗体–抗原。

### R61 CoV-AbDab
- **bucket**：`SRC_R61_COV_ABDAB/snapshot-2024-02-08`
- **ab 列**：`VHorVHH`+`VL`+`CDRH3`+`CDRL3`（`CoV-AbDab_080224.csv` 12,918 行，**实测 VHorVHH 12,918/12,918、VL 12,112/12,918**）；`Nb` 801 行 VL 全空（VHH 完整）；`ND` 572 行不可用
- **ag 列**：无序列列。`Binds to` 258 种 token（`SARS-CoV2_WT`/`SARS-CoV1` 等）+ `Protein + Epitope` 43 种写法；无抗原 FASTA、无构建体边界
- **pair 键**：`Name + Binds to`（`Name` 12,916 个值，`R15-F7`/`ADI-62113` 各两行不能当严格主键）
- **人工多级跳转清单**：258 个 `Binds to` token 的抗原序列；`Protein + Epitope` 43 种靶蛋白写法；5 个 PDB（7B11 unreleased/7KGL/7N01/7NY5/7SIX removed）不可取得
- **规模**：12,918 行；Ab 12,117 + Nb 801；`Neutralising Vs` 6,373
- **风险**：**ag 侧完全无序列无法闭合**；`Binds to` 定性文本无 assay 条件；CSV 与 ANARCI JSON（24,442 键）有 239+1,815 个键不一致。

### R62 CoV-UniBind
- **bucket**：`SRC_R62_COV_UNIBIND/snapshot-2025-12-02`
- **ab 列**：`antibody_vh_sequence`+`antibody_vl_sequence`（6 张 parquet，**实测 75,459/75,459 非空**）；另有 `antibody_heavy_chain_sequence`/`light_chain_sequence` 全长
- **ag 列**：`antigen_sequence`（**75,459/75,459 非空**）+ `antigen_sequence_trimmed`（22,543）+ `antigen_domain`/`antigen_residue_indices` + `spike_sequence`；作者按实际接触把复合物拆成 ab–ag 对，抗原裁到 RBD/NTD
- **pair 键**：`antibody_name + antigen_lineage + mutations + pdb_id`
- **人工多级跳转清单**：无（920 个 PDB FASTA/mmCIF 随包）
- **规模**：6 表 632/61,661/9,691/2,472/164/839 = 75,459；抗体 183 个；`pdb_id` 并集 176
- **风险**：52,749 行缺 trimmed（只有全长）；`log10_kd` 无统一单位字段；processed zip 920 个 PDB 与论文 177 unique 口径不一致；仅 176 个 PDB 有实验行级连接。

### R66 KyDab
- **bucket**：`SRC_R66_KYDAB/snapshot-2026-03-23`
- **ab 列**：`KV7019.zip` 内 `KV7019.csv` 表头 `CLONE_NAME,ANIMAL,TISSUE,LIGHT_CHAIN_SEQ,HEAVY_CHAIN_SEQ,ANTIGEN_NAME,...`（**实测**）；另有 `*-airr-heavy/light.tsv`（`sequence_aa`）与 `*.fasta`。11 个研究包 zip。README 未说明是否达 Fv 级（是否含恒定区未声明）
- **ag 列**：`ANTIGEN_NAME`/`ANALYTE_NAME` 等名称列（非序列）；每包 JSON 有 `Antigen Sequence` 字段但多为空串（KV7019 实测为空）；14 个 FASTA 随包，README 未列哪个对应哪个抗原
- **pair 键**：`CLONE_ID/CLONE_NAME + ANALYTE_NAME + 研究包 + Replicate`
- **人工多级跳转清单**：百日咳毒素/疟疾 CSP/SARS-CoV-2/伤寒毒素/OMV 构建体序列（README 明示部分 FASTA 有、部分不完整）；各免疫原名称与序列
- **规模**：11 主表 123,527 行（productive 配对）；约 960 抗体有数值 KD、约 910 有完整 H/L+KD
- **风险**：**ag 侧只有名称，部分 FASTA 有但对应关系未列**；ab 序列是否含恒定区未说明；ELISA 表字面 `NA` 与字面零值并存。

### R69 CH65 comblib（部分闭合）
- **bucket**：`SRC_R69_CH65_COMBLIB/snapshot-2023-02-01`
- **ab 列**：`geno`（16 位二进制，2^16=65,536）+ `mutation_list.tsv`（`mut_name/nt_pos/codon_0/codon_1/aa_0/aa_1/aa_pos/synonymous`，**实测存在**）+ 母本 CH65 scFv（`pdb/sequences/rcsb_pdb_5UGY.fasta` 随包）。**需拼**
- **ag 列**：无序列列。`MA90`/`SI06`/`MA90-G189E` 3 个抗原名；README 未把 5UGY 的 HA entity 与这三个抗原建立对应
- **pair 键**：`geno + 抗原`（`MA90_mean`/`SI06_mean`/`G189E_mean` 三列）
- **人工多级跳转清单**：MA90 / MA90-G189E / SI06 三个 HA 抗原序列（README 无对应文件）
- **规模**：65,536 基因型 × 3 抗原；QCfilt 65,536、REPfilt 65,535
- **风险**：**ag 完全无序列**；`V98I` 行 mutation_list 内部冲突（aa_0=R aa_1=R synonymous=True）未解析；`log10Kd` 按 `-log10(K_D [M])` 解释符号方向须显式。

### R70 CR9114 DMS
- **bucket**：`SRC_R70_CR9114_DMS/v1.0.0`
- **ab 列**：`Fasta/CR9114_HC_WT.pep`+`GL.pep`（120 aa VH，**实测存在**）+ VL 从 `pdb/sequences/rcsb_pdb_4FQI.fasta` light chain 取（216 aa，随包；README 未声明该链与实验构建体同源，只声明 VH 前 120 aa 一致）。**需拼**
- **ag 列**：无序列列。`Brisbane/59/2007 H1 stem #4900` / `Singapore/INFIMH-16-0019/2016 H3` / `B/Lee/1940 HA` 3 个病毒株/HA 名——**无序列**；4FQI 是 H5 复合物非本研究抗原
- **pair 键**：`mut_kabat` + assay（germline-H1/somatic-H1/somatic-H3/somatic-BHA 四表）
- **人工多级跳转清单**：3 个 HA 抗原序列（外部）；`Fasta/CR9114_original_seq.fa`（`compile_TiteSeq.py` 引用，**不在固定 tree**）
- **规模**：2,521×4 表（120 位置 × 21 aa）；有限 Kd 2,421/2,476/2,498/2,503
- **风险**：**ag 完全无序列**；VL 来源链与实验构建体同源未声明；`Kd` 列名是拟合内部参数名非摩尔单位。

### R71 CGGnaive DMS
- **bucket**：`SRC_R71_CGGNAIVE_DMS/snapshot-2025-02-03`
- **ab 列**：`mutation`（`final_variant_scores.csv`，chain-local 如 `N108(L)R`）+ `CGGnaive_sites.csv`（235 个 construct-linear 位置：112 H + 15 linker + 108 L，`KI_codon` 母本）+ `codon_variant_table.csv`（`aa_substitutions`）。**需拼**：235 位切分成 VH/VL；**linker 15 位 `KI_codon` 为 NA**，完整 scFv 单链不可组装（VH/VL 两级可用）
- **ag 列**：无序列列。`target=CGG_naive`（chicken IgY CH2 domain）；`data/IgY-CH2_EH2_final_real_space_refined_021.pdb`（随包）+ `pdb/sequences/rcsb_pdb_9ODB.fasta`（随包）
- **pair 键**：`mutation + target`（跨表须经 `site_scFv`↔`site` 转换，不能按数字直接 join）
- **人工多级跳转清单**：无（IgY CH2 两侧随包；母本 codon 随包）
- **规模**：4,158 构建设计；论文 4,161 可能替换；`final_variant_scores.csv` 4,800 行；`variant_counts.csv` 17,703,468 行（非独立抗体）
- **风险**：linker 15 位 NA → 完整单链不可组装；`9ODB` 是 `2.1hi` 而非 naive clone 2.1（含 8 替换）；current-main 与 paper-linked 两张 final_variant_scores 数值不同。

### R72 Omicron landscape
- **bucket**：`SRC_R72_OMICRON_AB_LANDSCAPE/snapshot-2023-11-10`
- **ab 列**：无表内序列；4 个固定抗体由文件名区分：`CB6`(LY-CoV016)、`CoV555`(LY-CoV555)、`REGN10987`、`S309`；PDB FASTA 随包（**实测**：`7C01.fasta`/`7KMG.fasta`/`6XDG.fasta`/`6WPT.fasta`）；另有 `ACE2`（受体 7WPB）
- **ag 列**：无序列列；`geno`（15 位，2^15=32,768）+ `config.yaml.RBD`（**实测存在**，含 ancestral/evolved 核苷酸 + `sequence_begins_with_residue: 331`）。**需拼**：`geno` 位替换施加到参考 RBD
- **pair 键**：`geno`（五表集合完全相同，可横向连接）
- **人工多级跳转清单**：无（4 抗体 PDB + 参考 RBD 核苷酸随包）；`GISAID EPI_SET` 只用于系统发生，与序列无关
- **规模**：4 抗体表 × 32,768 = 131,072 基因型×抗体；S309 有限值 32,768 全
- **风险**：抗体是 PDB 沉积的 Fab/VH-VL，README 未说明实验构建体与沉积逐残基一致；`6WPT` 的 S309 只 127/107 aa；全零基因型=武汉 Hu-1 RBD，与 PDB 锚点 S1 构建不同源；`<k>` 浓度/bin 对应不在表内。

### R73 Background dependence（部分闭合）
- **bucket**：`SRC_R73_BACKGROUND_DEPENDENCE_SARS_COV2/snapshot-2026-02-13`
- **ab 列**：无表内序列；`File_Details.csv` 的 `Ligand` 列给抗体名。8 个抗体中 3 个 PDB 随包（**实测**：`AZD1061`/`AZD8895` 在 `7L7E.fasta`、`LY-CoV1404` 在 `7MMO.fasta`、`ACE2` 在 `7WHH.fasta`）；**5 个缺失**（REGN10987/S309/002-S21F2/Iv0221/Iv0262）
- **ag 列**：`aa_geno`（**175 aa RBD 序列，表内直接给**，起点 331，可含 `-` 占位符）；`pos_<n>` 位点列 + `pos_background`/`background_strain`
- **pair 键**：Library B 无单列键（9 个 `pos_<n>` + `aa_geno`）；Library C `xaba_geno`（稳定键）；Library M 仅 `aa_geno`+位点列
- **人工多级跳转清单**：5 个抗体（REGN10987/S309/002-S21F2/Iv0221/Iv0262）序列——REGN10987/S309 在 R72 bucket 有（6XDG/6WPT）但属另一 source；002-S21F2/Iv0221/Iv0262 本项目任何 source 都无锚点
- **规模**：51 表 4,795,558 行（Library B 1,152 设计、C 16,800、M 约 30 万）
- **风险**：5 个抗体不可闭合（其中 3 个任何 source 无锚点）；`7L7E` 含 4 抗体实体各有 4 同序列副本且 README 不指定副本；Library M 的 `ab_1`–`ab_8` 与抗体编号对应未给出。

---

## C 档逐 R 详表（结构切链 + 角色判定类）

### R14 AB-Bind
- **bucket**：`SRC_R14_ABBIND/snapshot-2019-04-10`
- **ab 侧**：**无序列列**。`#PDB`+`Partners(A_B)`+`Protein-1/2`+`Mutation`。**需切**：32 个自带 PDB（随包）按 `Partners(A_B)` 链组切；27 个晶体体系另有 RCSB FASTA/mmCIF（随包）
- **ag 侧**：同键的另一侧链组；32 体系（27 晶体 + 5 `HM_` 同源模型）；`HM_1YY9/3BN9/2NYY/2NZ9/1KTZ` 无自身 accession，实际测量分子序列需回原文献
- **pair 键**：`#PDB + Partners(A_B) + Mutation`（1,101 行 → 1,096 唯一键，5 个键重复且 ddG 不同）
- **人工多级跳转清单**：5 个 HM 体系的真实实验分子序列（README 未给原文献条目）；8 个条目的 H/L 链名与 RCSB author 链不一致需人工映射（但自带 PDB 含相应链）
- **规模**：1,101 行 × 16 列；645 单成分 + 456 多成分突变
- **风险**：`Partners(A_B)` 字母不是固定抗体/抗原角色（AB_C/A_BC/AB_CD 等）；81 行突变同时涉及两侧；5 个 HM 无真实分子序列。

### R15 SKEMPI 2.0
- **bucket**：`SRC_R15_SKEMPI2/2.0`
- **ab 侧**：**无序列列**。`#Pdb`（如 `1CSE_E_I`）+`Mutation(s)_PDB`+`Protein 1/2`。**需切**：345 个 PDB（随包）取链；`Hold_out_type` 含 AB/PI,AB 标记 301 条（R57 DACUM 复用了这个）
- **ag 侧**：同键另一侧链组
- **pair 键**：`#Pdb + Mutation(s)_PDB`；345 个 accession
- **人工多级跳转清单**：无（345 锚点两层文件随包）；但**哪条链是抗体**需按 fasta 描述判定
- **规模**：7,085 行 × 29 字段（11 个精确重复行）；抗体子集 57 个复合物（第一轮普查核验）
- **风险**：无 antibody/antigen 角色字段；`Mutation(s)_cleaned` 与 `Mutation(s)_PDB` 两套编号体系；一般 PPI 占多数。

### R16 Guest
- **bucket**：`SRC_R16_GUEST/snapshot-2020-11-17`
- **ab 侧**：**无序列列**。`Complex PDB`/`Antibody PDB`/`Antibody`/`Antigen PDB`/`Antigen`。**需切**：`pdbs/<Case>_r_b.pdb`/`_r_u.pdb`（r=抗体、l=抗原、b/u=结合/游离，**实测文件存在**）；194 个 PDB FASTA/mmCIF 随包
- **ag 侧**：`Antigen PDB` + `<Case>_l_{b,u}.pdb`
- **pair 键**：`Case`（67 行唯一）
- **人工多级跳转清单**：无（3RVW→5VPG、4ZAI→7JNY 已用 2020 归档补）；`2I25`（IgNAR）无 CDR2 等价环
- **规模**：67 案例；affinity 42 行、ΔG 51 行
- **风险**：两端都靠结构切链；unbound 可来自另一 PDB；r/l 与抗体/抗原对应仅 README 一句说明。

### R17 PDBbind PP
- **bucket**：`SRC_R17_PDBBIND_PP/2020`
- **ab 侧**：**无序列列、无角色字段**。`INDEX_general_PP.2020` 只给 `PDB code/resolution/year/binding/reference/ligand name`。**需切**：2,852 个 entry FASTA（随包）按链切
- **ag 侧**：同 entry 的伙伴链组；`ligand name` 非受控文本
- **pair 键**：`PDB code`（2,852 唯一）
- **人工多级跳转清单**：**636 个抗体结构的判定**（第一轮普查：与 SAbDab2 6,028 个抗体 PDB 交集）；`reference` 列 765 行 token 与本行 PDB 不同
- **规模**：2,852 行；Kd 2,618/Ki 171/IC50 63
- **风险**：无法确定哪一侧是抗体；一个 entry 多链/对称副本；README 明言「直接把 2,852 行全当抗体样本会改变数据含义」。

### R19 DIPS-Plus
- **bucket**：`SRC_R19_DIPS_PLUS/1.1.0`
- **ab 侧**：`final_raw_dips.tar.gz` 的 Pair namedtuple（`sequences`/`df0`/`df1`/`complex`/`id`）；`.dill` 序列化对象。**无抗体身份**，需另行筛抗体–抗原链对
- **ag 侧**：同 `sequences` 字段；无角色区分
- **pair 键**：`complex`（如 `5cxc.pdb1`）
- **人工多级跳转清单**：无（12,601 锚点 FASTA/mmCIF 随包；8 个撤回 ID 已用历史 SEQRES 补齐）
- **规模**：42,112 Pair（train 33,159 + val 8,290）+ DB5 230（train 140/val 35/test 55）
- **风险**：**只有 70 个是抗体结构（0.6%）**，无链角色字段，不划算；`sequences` 字段语义（每条链长度/是否含信号肽标签）README 未说明。

### R32 Vreven PPI v2
- **bucket**：`SRC_R32_VREVEN_AFFINITY/2.0`
- **ab 侧**：`affinity_benchmark1.tsv`+`affinity_benchmark2_additions.tsv` 共 179 行；`Protein A/B`+`Unbound PDB`+`Complex PDB`（如 `1JTD_B:A`）。**需切**：672 个 PDB FASTA/mmCIF（随包）按 author chain 取链；链角色需按 entity 描述判定
- **ag 侧**：同键另一侧链组
- **pair 键**：`Complex PDB`（179 个值唯一）
- **人工多级跳转清单**：无（672 个 PDB 全随包，含 4 个 obsolete 用撤销前官方 pdbsnapshots）
- **规模**：179 案例；抗体–抗原 33（A 26 + AB 7，README 注明与论文 40/33 一致）；BM5 docking 230 案例另一口径
- **风险**：两侧序列都需人工按链切分；`Complex` 冒号两侧是分组非 FASTA entity 顺序；一个 PDB 被多案例复用，抗原 construct 未必同一。

### R43 Phillips（部分闭合）
- **bucket**：`SRC_R43_PHILLIPS/snapshot-2021-09-22`
- **ab 侧**：`variant`（CR6261 11 位）/`sequence`（CR9114 16 位）二进制 genotype（FLAb 4 文件 67,033 行）。**需拼**：genotype 位点定义与 alignment 只在论文；母本 3GBN（CR6261）/4FQI/4FQY（CR9114）FASTA 随包
- **ag 侧**：无序列列。`h1_mean`/`h9_mean`/`h3_mean`/`fluB_mean` 列名前缀；4 个 HA 靶点（H1/H9/H3/fluB）**无序列**；3GBN HA1/HA2 随包（4FQI 是 H5 代理非 H1）
- **pair 键**：genotype + 抗原列 + replicate + inference method
- **人工多级跳转清单**：CR6261 11 位/CR9114 16 位的位点定义与 alignment（论文正文）；4 个 HA 实验 construct 序列
- **规模**：CR6261 2^11=2,048 genotype；CR9114 2^16=65,536；FLAb 4 文件 67,033 行（未覆盖 fluB）
- **风险**：**ag 完全无序列**；genotype 无位点定义无法转 AA；4FQI 是 H5 而非 H1；pKD 边界值与 ML 表 `h*_mean` 量纲不同。

### R57 DACUM
- **bucket**：`SRC_R57_DACUM/snapshot-2019-03-08`
- **ab 侧**：**无序列列**。`SKEMPI_ID`（`1CSE_E_I_LI45G`）+`Protein`+`Mutation_PDB`。147 个 PDB FASTA（随包）；`Hold_out_type` 为 AB 222 条 + PI,AB 79 条 = 301 条
- **ag 侧**：同键另一侧链组
- **pair 键**：`SKEMPI_ID`（1,872 唯一；1.1 与 1.0 同集合不能相加）
- **人工多级跳转清单**：无（147 PDB 随包）
- **规模**：1,872 行；147 个 Protein 编码
- **风险**：每行只有突变编码，抗体/抗原角色未标注；PDB entry 与实验构建体未对齐；非抗体体系（酶-抑制剂）占多数。

### R58 dbMPIKT
- **bucket**：`SRC_R58_DBMPIKT/snapshot-2018-11-27`
- **ab 侧**：**无序列列、无行级配对键**。File 1 `Protein`/`Mutation(s)_PDB`/`Mutations name`/`Title`；File 2 `PDB ID`/`Chain ID`；File 3 聚合计数
- **ag 侧**：无序列列；230 个候选 PDB 中 229 个 FASTA 随包（`1TPQ` UNRELEASED 404）
- **pair 键**：**无**（README：「工作簿没有给出把四组清单恢复为逐记录数据库表的主键或行级映射」）
- **人工多级跳转清单**：`1TPQ`（RCSB UNRELEASED，无法取得）；5,291 条逐记录导出（无公开路径，需联系维护方）
- **规模**：File 1 379 非空行；File 2 500 非空行；论文 5,291 突变 / 233 PDB / 245 复合物
- **风险**：无法还原为逐记录表；无任何数值字段；README 自述仍在 staging。

---

## D 档逐 R 详表（不可用/无序列）

### R26 Adaptyv EGFR
- **bucket**：`SRC_R26_ADAPTYV_EGFR/snapshot-2025-03-18`
- `Round 2 result_summary.csv` 402 行，`sequence` 列是提交全长设计——**混合抗体与非抗体骨架**，README 未给类型列；按 linker/FR4 判定 51 条（12.7%）抗体形态，len 13–250（中位 89）。EGFR 靶点 `1IVO` entity 1 随包；Round 1 202 行。
- 用与不用：只取抗体形态子集才可能成对，且测量构建体与 1IVO 等同未核验。

### R27 Porebski
- `read 1/2/3` 是翻译后局部片段（含 `*` 终止符），非全长；**HEL Nb / IL-7 scFv / HER2 scFv 三个亲本完整序列都不在包内**。`1LYZ`/`1N8Z`/`3DI2` 只是共享参考。五表 8,796,184 行规模虽大但 ab 侧无法闭合。

### R30 Hie
- **5 个亲本（MEDI8852/mAb114/S309/REGN10987/C143）+ UCA 的 VH/VL 都不在包内**；`Design` 只有名称，突变位点编码规则未说明；ag 7 条路线/5 抗原构建体全缺。`TheraSAbDab_SeqStruc_OnlineDownload` 是否覆盖这些抗体 README 未说明。122 变体 / 7 路线。
- 可用性：ab 需第三方且 `Design` 无法解析 → 本轮不可闭合。

### R33 IEDB BCR
- 主 `bcell_full_v3.csv` 无序列列；仅 `bcr_full_v3.csv` 6,745/10,461 行双链 + 7,844 行至少一链 + 6,914 行有 calculated V domain；`bcr_3d_assays.csv` 5,947 行有 `Antigen Sequence`+`Chain 1/2 Sequence`。ag 侧 epitope 可以是线性肽/不连续残基/非蛋白对象，不能统一当全长抗原。
- 用与不用：3D 子集（5,947 行）双侧有序列，可作小规模可用；主表 1,692,185 assay 无序列。

### R38 IntAct
- MITAB 相互作用表，`interactor` ID 无序列；无抗体变区。跳过。

### R42 MAGMA-seq
- `Variant` 是 `4A8>VH:M59I-ATC|4A8>VL:S7T-ACT` 复合突变串，**编号基准（母本/密码子规则）README 未说明**；母本 5 个 PDB 随包但抗原 S1/H1 实验 construct 无序列；`COV2-2489` 亲本无锚点。1,040+1,071 行。ab 无法确定性重建 AA。

### R44 Kirby
- 同 R42 结构：`Variant` 含密码子/同义变化，母本为 **inferred UCA**（SI Table S6 GenBank accession，外部）；8 亲本仅 6 个有 PDB 锚点；ag S1/RBD 无序列。1,356+1,878 行。不可闭合。

### R51 MaveDB
- ab 无序列（2D7/12G5）；ag 参考序列（CCR5 P51681/CXCR4 P61073/INSR P06213/GB1）需 URN 回查不随包；每行是突变体。588,717 行。不可闭合。

### R53 Saka
- ag 是小分子犬尿氨酸——无蛋白 FASTA；VL 需专利 WO2015083764 SEQ ID NO:97（映射未确认）；仅 21 条逐行公开。不可闭合。

### R56 ASEdb
- 无序列列，只有 `system.PDB`（101 系统/32 唯一 PDB）+ 丙氨酸扫描记录；README 明言「不通过 RCSB FASTA 擅自生成变体序列」。不可闭合。

### R59 BindCraft
- `Sequence` 是 de novo 设计小蛋白（212 条），**非抗体**；13 个靶点（4 个只有计算模型链 A）。不可闭合。

### R60 AlphaProteo
- 非抗体 de novo binder；861 个测试候选仅 25 条有公开序列；抗原只给链与区间不给构建体。不可闭合。

### R63 CovEpiAb
- ab 无序列（结果页 12,604 行只有 `ID/Name/Type/Protein/Bind/Neutralizing/Structure`）；详情页未存档（/covepiab/help 404）；`Structure` 829 个 PDB 无链角色。不可闭合。

### R64 COVIC-DB
- `Antibody label` 413 个盲化编号，**无 COVIC-ID→sequence 映射**；14 工作簿 14,859 行；ag `Tested antigen` 名称形式。两侧都不可闭合。

### R65 BID
- 一般 PPI 丙氨酸扫描（9 复合物/41 突变），无抗体维度。跳过。

---

## 遗留：人工多级跳转总清单（需主人或我上网逐条找）

> 规则：凡「README 明确在 bucket 内某文件」不算；凡「无序列列、无随包文件、只有名称/货号/专利号/PDB」的条目，逐条列出。

### 抗原侧（ag 缺 FASTA 的）
1. R01：8 个系统的 SPR 抗原试剂（ACRO Biosystems 货号，需向作者索取）——ACVR2B、CD40、C5、FXI、IL36R、TSLP、TNFRSF9、IL17A
2. R02：4 个交叉反应抗原（cynomolgus HER2、canine HER2、mouse HER2、human HER1/3/4）
3. R05：fluorescein（小分子，无蛋白序列可言）——**判定为不可闭合**
4. R06：实验用生物素化 VEGF（2FJG 102 aa 是否为实验构建体未定）
5. R07：人 HGFR-Fc 完整构建体；OVA；CHO SMP
6. R13：`PDB_ID` 缺失的 27,952 行的抗原身份
7. R17：PDBbind 636 抗体结构的链角色判定（非序列缺失，是角色判定）
8. R22：PLAbDab 专利/文献行的抗原序列（README 无专利号列，仅 `ID`=如 `763134A`）
9. R23/R35：`AlphaNeg1/2/3` 三条阴性对照肽序列
10. R25：10 个撤回 PDB 的完整 FASTA（4OZ4/5USI/6CSY/6ERX/7CTU/7CU4/7CU7/7KGL/7N01/7N0S）；论文验证候选序列（只在 supplement PDF）
11. R28：无（HER2 1N8Z 随包）
12. R37：mouse-lysozyme-Fc 融合构建体序列
13. R43：4 个 HA 实验 construct（H1/H9/H3/fluB）
14. R45：`Binds to` 258 种 token 中未匹配 24 条病毒蛋白的；FLAb 141/427 行的抗原归属
15. R46：BQ.1.1 RBD、XBB.1.5 RBD
16. R49：GSK RSV F 构建体/株系/方向
17. R61：`Binds to` 258 种 token 的抗原序列（SARS-CoV2_WT/SARS-CoV1 等）
18. R66：百日咳毒素 / 疟疾 CSP×2 / SARS-CoV-2 / 伤寒毒素 / OMV 构建体序列 + 11 包免疫原对应
19. R69：MA90、MA90-G189E、SI06 三个 HA 抗原序列
20. R70：Brisbane/59/2007 H1 stem、Singapore/2016 H3、B/Lee/1940 HA
21. R74：Wuhan RBD 序列

### 抗体侧（ab 缺 FASTA/缺 VL 的）
1. R05：OPT / Δ 两个对照的完整 scFv；scFv linker 序列
2. R07：emibetuzumab 轻链可变区
3. R28：Mason 完整 IgG 变体序列（作者申请）
4. R29：atezolizumab scFv 重/轻链；75,631 变体抗体 FASTA
5. R30：5 亲本 + UCA（MEDI8852/mAb114/S309/REGN10987/C143）VH/VL
6. R33：`Group IRI` 无法唯一化整抗体；4UD3/4UDZ 撤销条目 FASTA
7. R42：亲本 COV2-2489 完整 VH/VL；4A8/CC12.1/CR6261/222-1C06/2-7 的变体编号基准
8. R43：CR6261 11 位/CR9114 16 位位点定义与 alignment
9. R44：8 亲本的 inferred UCA（SI Table S6 GenBank）；亲本 1-20 / CC6.31
10. R51：2D7、12G5（无序列）
11. R53：VL（专利 WO2015083764 SEQ ID NO:97）
12. R63：12,602 个 `Name`（除 Roberts_201、2B04 外）的完整重轻链序列——详情页
13. R64：413 个 COVIC 编号的 identity/sequence 映射
14. R73：002-S21F2、Iv0221、Iv0262（本项目任何 source 都无锚点）
15. R14：5 个 HM 体系（HM_1YY9/3BN9/2NYY/2NZ9/1KTZ）的真实实验分子序列

### 角色判定类（序列都在，但需人工确认哪侧是抗体）
- R15 SKEMPI2（345 PDB 中 57 抗体复合物）
- R17 PDBbind（636 抗体结构）
- R19 DIPS-Plus（70 抗体结构）
- R20 SAbDab2（INSTANCE→链的可核验映射，README Q01）
- R50 Graphinity（`chain_prot1/2` 与 `ab_chain/ag_chain` 映射）
- R57 DACUM（`Protein 1/2` 哪侧抗体）
- R58 dbMPIKT（四清单无法恢复逐记录表）

---

## 下一轮工作（数据落地后）

1. **修 pyarrow 依赖**：服务器已有 `/data_new/ywy/_pyenv`（pyarrow 26 + openpyxl 已装，tsinghua 镜像）。恢复通道后在 3x5090 上建表。
2. **生成 index**：按 A/B/C/D 档分派，首选双侧表内即闭合的 A 档（R03/R08/R10/R12/R13/R21/R23/R35/R40/R41/R62/R67）与部分 B 档（R20/R22/R34/R36/R47/R48/R49 等）。
3. **手工多级跳转**：按上方清单，我亲自上网逐条找 FASTA（主人已确认不走全自动 pipeline）。
4. **去重**：R09 与 R06/R34/R36/R37/R46/R47/R48/R49/R04 原表重复；R45 与 R61 重复；R12 的 CSV 与 parquet 同一批；R73 的 REGN10987/S309 与 R72 重复。
5. **ag 归一化**：A 档里 R40/R41/R08 的构建体串（信号肽+标签）需切到可变域/成熟区；b 口径（构建体）与 PLM 训练分布（天然序列）的关系需单独定。

