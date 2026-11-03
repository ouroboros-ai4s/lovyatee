---
tags:
  - context
---

# abag bucket 序列类型普查

## 第一轮：数据集序列类别普查（2026-10-21）

覆盖 **28 个分组 / 4,624,675 行**。完整数字见同名 `.json`（`ab` / `ag` 字段）。

R12 ASD 拆成两行：它的 CSV 导出与 20 个 parquet 分片装的是同一批相互作用的两种格式，合并会把同一批行数算两遍。

| 源 | 表数 | 行数 | 主要 AB 类型 |
| --- | ---: | ---: | --- |
| SRC_R01_IGDESIGN | 18 | 330 | CDR peptide only 320, VH+VL pair 10 |
| SRC_R02_ABSCI_HER2 | 3 | 93 | CDR peptide only 93 |
| SRC_R03_ABDESIGN_DB | 2 | 1,360 | IgG (HC+LC) 537, VH + VL-CL 438, VH+VL pair 130 |
| SRC_R04_IPI | 88 | 3,338 | CDR peptide only 1,920, VH+VL pair 1,418 |
| SRC_R05_TITESEQ | 4 | 160 | CDR peptide only 160 |
| SRC_R06_KOENIG | 2 | 8,550 | VH+VL pair 8,082 |
| SRC_R07_MAKOWSKI | 6 | 8,444 | VH only 8,444 |
| SRC_R08_AVIDA_HTNFA | 3 | 221,806 | VHH 122,341, unclassified-V 59,187, VH only 40,144 |
| SRC_R11_ABBIBENCH | 17 | 215,699 | VH+VL pair 150,599, IgG (HC+LC) 30,925 |
| SRC_R12_ASD（CSV 导出） | 3 | 643,252 | VH + VL-CL 368,133, VHH 84,125, scFv 67,386 |
| SRC_R12_ASD（parquet 分片） | 9 | 530,025 | VH + VL-CL 298,190, VH only 56,490, VHH 39,533 |
| SRC_R13_ANDD | 1 | 48,800 | VHH 16,859, unclassified-V 9,530, VH+VL pair 6,682 |
| SRC_R20_SABDAB | 1 | 22,264 | VH+VL pair 13,749, VHH 2,522 |
| SRC_R21_AVIDBASE | 1 | 1,048 | VHH 579, VH only 104 |
| SRC_R22_PLABDAB | 2 | 576,894 | VH only 158,326, VH+VL pair 133,913, VL only 87,008 |
| SRC_R25_RFDIFFUSION | 1 | 11,777 | domain fragment 10,011, CDR peptide only 1,745 |
| SRC_R34_ABLIFT | 1 | 2,048 | VH+VL pair 1,978 |
| SRC_R40_AVIDA_HIL6 | 1 | 400,000 | VHH 201,553, unclassified-V 132,139, VH only 65,791 |
| SRC_R41_AVIDA_SARS_COV2 | 4 | 154,023 | VHH 95,040, unclassified-V 37,408, VH only 21,494 |
| SRC_R46_SHANKER | 10 | 262 | VL 132, VH+VL pair 127 |
| SRC_R47_ROSACE | 8 | 76 | VH+VL pair 76 |
| SRC_R48_ZIMMERMANN | 1 | 21 | VL 14, VH+VL pair 7 |
| SRC_R49_GARBINSKI_GSK | 3 | 261 | VH 126, VH+VL pair 63 |
| SRC_R59_BINDCRAFT | 1 | 212 | unclassified-V 163, domain fragment 48 |
| SRC_R61_COV_ABDAB | 1 | 40 | CDR peptide only 40 |
| SRC_R62_COV_UNIBIND | 6 | 75,459 | VH+VL+multi-domain 65,992, IgG (HC+LC) 820 |
| SRC_R67_OPEN_ALPHASEQ | 9 | 1,698,105 | scFv 583,874, VHH+multi-domain 378,608, multi-domain 266,184 |
| SRC_R70_CR9114_DMS | 2 | 328 | VH only 160, VH+VL pair 134 |

### 全库合计（按行，R12 两种格式分开计）

| 类型 | 行数 |
| --- | ---: |
| VHH / 纳米抗体 | 733,543 |
| scFv 单链 | 692,630 |
| VH + VL-CL（Fab 缺 CH1） | 667,781 |
| VH only | 360,097 |
| VH+VL pair (Fv) | 351,431 |
| IgG (HC+LC) | 37,079 |
| IgG 仅重链 | 25,600 |
| Fab light only (CL) | 23,819 |
| Fab (CH1+CL) | 5,257 |
| CDR 肽段 | 4,278 |
| VL only | 111,629 |

另有 1,611,406 行无法归入单一分子类型（占 34.8%），单列如下。集合之间有重叠，三项不可相加：

- 含 `multi-domain(large)` 的行 1,056,235——多为 DMS 表「参考抗体 + 突变体」并排，或抗体与抗原序列同列，行本身不描述单一分子。
- 含 `unclassified-V` 的行 698,462——IMGT 编号只有 FR3 片段，或框架基序变异，不足以定族。
- 两者兼有 204,407（已含在上面两个数里）。
- 结构域碎片与小类 61,116：`VH+domain-fragment` 35,292、`domain fragment` 18,349、`Fab 仅重链(CH1)` 6,640 等。

上表 11 类合计 3,013,144 行。

**AB 的 type 不止主人列的五种。** 实际观测到的完整清单：
`IgG (HC+LC)`、`IgG 仅重链`、`Fab (CH1+CL)`、`Fab 仅重链(CH1)`、`Fab 仅轻链(CL)`、`VH + VL-CL（Fab 缺 CH1）`、`VH+VL pair (Fv)`、`VH only`、`VL only`、`VHH`、`scFv`、`CDR 肽段`、`Fc 片段`、`结构域碎片`、`多结构域大链`、`unclassified-V`。

`VH + VL-CL` 这一类值得单独留意：R12 ASD 的 66.6 万行是「VH + 带 CL 的轻链」，即 Fab 但缺 CH1。既不能算 IgG，也不能算裸 Fv，按 IgG/Fab/Fv 三分会全部错分。

### 抗原侧

抗原**没有** AB 那样的恒定区分类体系，不存在 IgG/Fab/VHH 层面的划分。可测的只有三件事：

1. **是否存有抗原序列**。28 个分组里只有 11 个表内有抗原序列列，其余只给靶点名称。
2. **抗原序列的尺寸类**（`peptide <30aa` / `single domain 80-160aa` / `domain pair 160-260aa` / `large 260-460aa` / `very large >460aa` / `huge >800aa`）。差异极大：R12 的 37.9 万行是 >460aa 的胞外域，R62 的 5.3 万行是 160-260aa 的 RBD。
3. **靶点名称**，用于判断单一抗原还是抗原面板。R04 是 10 个细胞表面靶点的面板（PDL1/PDL2/IL23R/LOX1/ROBO1/ROBO2N/DCC/TIGIT/Syncytin2/DKK），R40 是 IL-6 单点突变系列，R41 是 SARS-CoV-2 变异株面板。

---

## 第二轮：抗体完整可变区可用性普查（2026-10-27）

### 判定结果总览

73 份 readme，其中 `R24`、`R39`、`R52`、`R55` 只有 readme、bucket 内无数据，故实际核验 **69 个源**。

| 判定 | 源数 | 含义 |
| --- | ---: | --- |
| **可用** | **46** | 满足 A/B/C 之一，抗体侧可落到完整 VH+VL 或完整 VHH |
| **有条件** | 10 | 有序列，但母本不在 bucket 内、或只有片段/CDR 串、或序列混有非抗体骨架 |
| **不可用** | 13 | 抗体侧没有序列，或变体在抗原侧，或只有突变效应数值 |
| 无数据 | 4 | `R24`、`R39`、`R52`、`R55`，只有 readme |
| 合计 | 73 | |

### 可用（46）

| 源 | 路径 | 抗体形态 | 序列列 / 证据 | 规模 |
| --- | --- | --- | --- | ---: |
| R01 IgDesign | C | Fab（母本 Fv） | 只有 `HCDR1/2/3`；母本在 `sabdab/summaries/pdb_0000*.csv` 的 `VH`/`VL` 列（10 个文件覆盖 8 个实验体系 + 2 个无抗原沉积）。已核验长度：5i5k 122/107、5j13 122/108、5ngv 115/111、5nhw 115/111、6a3w 116/108、6hhc 120/107、6pe7 116/113、6pe8 116/113、6ppg 123/108、6u6u 119/108 | 1,243 可拼（CD40 的 201 行 HCDR 被 X 遮蔽，仅阳性对照可还原） |
| R02 Absci HER2 | C | Fab/IgG（曲妥珠单抗母本） | `spr-controls.csv` 有 `HCDR1/2/3`；母本 VH/VL 在 `pdb/sequences/rcsb_pdb_1N8Z.fasta`（重 220 aa 含 CH1、轻 214 aa 含 CL）。`zero-shot-binders.csv` 只有 `HCDR3` + 编辑距离，落位需自行比对 | 1,855（HCDR123 可拼）+ 422（仅 HCDR3） |
| R03 AbDesign DB | A | IgG/Fab | `heavy_sequence`、`light_sequence`、`heavy_sequence_variable`、`light_sequence_variable` 并列；变区列直接可用 | 1,303 + 57 |
| R04 IPI | A | Fv | `heavy`（124 aa）、`light`（107 aa），已核验为纯变区；另有 `antigen_seq`。`0Library_keys.xlsx` 给种系框架 `VH1-69`/`VK1-39` 全长，佐证这是共享框架上的 CDR3 多样性库 | 3,338（两个 Zenodo 版本重复，去重后约 1,669） |
| R05 Tite-Seq | C | scFv（4-4-20 母本） | 只有 `CDR1H`、`CDR3H` 的核酸与氨基酸；母本在 `pdb/sequences/rcsb_pdb_1FLR.fasta`（4-4-20 Fab，重链 227 aa）。表里只给 CDR1H/CDR3H，CDR2 与框架须取自母本 | 11,038 条拟合记录 |
| R06 Koenig VEGF | A | Fv | `heavy`/`light` 全长变区 | 4,275 |
| R07 Makowski MET | A | VH only | `VH Sequence` 为完整 VH；轻链未随表发布，bucket 内也没有 Emibetuzumab 轻链序列，按主人口径以 VH-only 计入 | 4,222 |
| R08 AVIDa-hTNFa | A | VHH | `VHH_sequence` | 5,580 配对 / 216,225 语料 |
| R09 FLAb | A | 混合（IgG/Fab/scFv/VHH） | 165 张表，`heavy` 出现 161 张、`light` 157 张，绝大多数为变区全长；异质 schema（112 种表头）需逐表核对 | 4,627,533 |
| R10 AbRank | A | IgG/Fab | `Ab_heavy_chain_seq`、`Ab_light_chain_seq`，实测含 CH1/CL 全长约 400 aa，可直接切变区；另有 `Ag_seq` | 381,713 |
| R11 AbBiBench | A | 混合 | `heavy_chain_seq`、`light_chain_seq` | ~216,000 |
| R12 ASD | A | 混合（VH+VL-CL 为主） | `antibodies.csv` 的 `Antibody heavy`/`Antibody light`；parquet 分片为嵌套 `chains` 字典 | 1,097,946 交互 / 716,650 完整配对 |
| R13 ANDD | A | 混合 | `Ab/Nano H_Chain AA`、`Ab/Nano L_Chain AA` | 48,800 |
| R20 SAbDab2 | A | Fab/Fv/VHH | `VH`、`VL` 列直接给变区 | 22,264 |
| R21 AVIDbase | A | VHH | `vhh_sequence`（52 列，含 `ag_sequence`、界面残基） | 1,048 |
| R22 PLAbDab | A | Fab/scFv/VHH | `paired_sequences.csv.gz` 的 `heavy_sequence`/`light_sequence`；另有未配对表 | 176,894 配对 |
| R23 AlphaSeq | A | scFv | `POI`、`Sequence`（scFv 全长）、`HC`、`LC`、`CDRH1-3`、`CDRL1-3` 全给 | 1,259,700 行 / 104,972 POI |
| R28 Mason HER2 | C | IgG（曲妥珠单抗母本 scFv/Fab） | DMS_opt 包内 `data/` 有 42 个 NGS 汇总表：`mHER_H3_*_Ab.txt`（含 `Clonal sequence(s)`、IMGT FR1–FR4 与 CDR1–3 分列）、`mHER_H3_AgPos.csv`/`AgNeg.csv`（`AASeq` + `AgClass`）。母本在 `pdb/sequences/rcsb_pdb_1N8Z.fasta`（Herceptin Fab 轻重链全长） | 约 10^4 变体 |
| R16 Guest | B | Fab/Fv | `antibody_antigen_cases.txt` 67 行，列含 `Complex PDB`/`Antibody PDB`/`Antibody`/`Antigen`/`I-RMSD`/`ΔASA`/`Category`；**67 个 Antibody PDB 全部在 `pdb/sequences/` 有 fasta**（已逐个比对，缺失 0）。抽查 1L7I = pertuzumab Fab 重/轻链、3MJ8 = HL4E10 Fab 重/轻链 | 67 个复合物 |
| R32 Vreven PPI v2 | B | Fab | `affinity_benchmark1.tsv` + `affinity_benchmark2_additions.tsv` 共 179 行，复合物键自带链角色（`1BJ1_HL:VW`、`3EOA_LH:I`）；**其中 20 行为抗体—抗原**，20 个 PDB 的 fasta 全在 bucket 内（缺失 0） | 20 个抗体复合物，每例一个 Kd |
| R29 RESP | C | scFv（Atezolizumab 母本） | 表里只有 counts/类别；母本可从 `pdb/sequences/rcsb_pdb_5XXY/5X8L.fasta` 取 | 75,631 独特序列 |
| R30 HIE | A/C | Fab/IgG | `supplement-3.xlsx` 给 Kd + `Design` 位点码；`supplement-6.csv` 直接给 `Variable Sequence` 全长 + `Recommended Mutation` | 122 变体 / 7 条进化线 |
| R33 IEDB BCR | A | BCR（重轻链/单链） | `bcr_full_v3.csv` 两条 `Protein Sequence`；6,914 行同时含 calculated V domain。长度异质，须按 Chain 1/2 判形态 | 10,461 行 |
| R34 AbLIFT | A | Fv | `heavy`/`light` 全长变区 | 2,048 |
| R35 Li AlphaSeq | A | scFv | 与 R23 同 schema（`POI`/`Sequence`/`HC`/`LC`/CDR）；v2.0 另含 dataset_2 | 1,259,701 + 1,903,928 |
| R36 Hutchinson NIP228 | A | Fab + IgG | `heavy`/`light`；同一候选有两种价态 | 362（重叠，非独特数） |
| R37 Jain | A | Fab/IgG | `heavy`/`light` | 31 单价 + 2 多价 |
| R40 AVIDa-hIL6 | A | VHH | `VHH_sequence` + `Ag_sequence`（30 个 IL-6 突变体） | 573,891 配对 |
| R41 AVIDa-SARS-CoV-2 | A | VHH | `VHH_sequence` + `Ag_sequence`（17 个抗原） | 77,003 |
| R42 MAGMA-seq | C | Fab | 表里是 `Variant` 突变串（`4A8>VH:M59I-ATC\|4A8>VL:S7T-ACT`）；母本在 `WT/wt.csv`，给 4A8/CC121 等亲本的 VH/VL 全长 DNA + 编码位点区间 | 1,040 + 1,071 |
| R43 Phillips bnab | C | Fab（CR6261/CR9114） | `variant` 为 16 位二进制基因型（16 个选定位点 × 2 等位）；母本可从 `pdb/sequences/` 取：4FQY = CR9114 轻链（已核验 `Antibody CR9114 light chain`），3GBN = CR6261 Fab | 67,033 |
| R44 Kirby | C | Fab | `Variant` 突变串 + `map_rep1/2.csv` 给每 barcode 的 VH/VL DNA（含 `Gene_H`/`Gene_L`） | 869 + 1,407 |
| R45 Ab-CoV | A | Fab/VHH | `VHorVHH`、`VL` 列；抽样 878 行中 49 行重轻链齐、810 行仅 VH/VHH、19 行全缺 | 1,780 条目 |
| R46 Shanker | A | Fab | `heavy`/`light` | 223 |
| R47 Rosace | A | Fv | `heavy`/`light`（含 Adalimumab/Golimumab 全长示例） | 76 |
| R48 Zimmermann | A | Fv | `heavy`/`light` | 21 |
| R49 Garbinski GSK | A | Fv | `heavy`/`light` | 261 |
| R54 AIntibody | A | Fab | `sequence_aa_light`、`sequence_aa_heavy` 全长 + CDR 分列；Challenge 2/3 还带 `affinity`/`on_rate`/`off_rate` | 3 个挑战 |
| R61 CoV-AbDab | A | Fab/VHH | `VHorVHH`、`VL`；形态分布同 R45 | 动态库 |
| R62 CoV-UniBind | A | IgG/Fab | `antibody_heavy_chain_sequence`、`antibody_light_chain_sequence`、`antibody_vh_sequence`、`antibody_vl_sequence` 四列并列 + `spike_sequence` | 75,459 |
| R66 KyDab | A | Fab/VHH | `KV7019.csv` 的 `HEAVY_CHAIN_SEQ`/`LIGHT_CHAIN_SEQ`（DNA）+ `*-airr-heavy.tsv`（`sequence_aa`、`germline_alignment_aa`）+ `*.fasta`（AA）。11 个研究包各自封装 | 123,527 配对 |
| R67 Open AlphaSeq | A（需切） | VHH / scFv | `mata_sequence`/`matalpha_sequence` 是**含酵母展示融合的全长蛋白**，抗体域嵌在其中——上一轮 1,056,235 行落 `multi-domain(large)` 即由此。需按融合边界切出，融合蛋白身份由 `*_description` 给出 | 1,698,105 |
| R69 CH65 comblib | C | scFv | `geno` 为 16 位基因型；母本 CH65 可从 `pdb/sequences/rcsb_pdb_5UGY.fasta` 取 | 65,536 基因型 × 3 抗原 |
| R70 CR9114 DMS | A | Fv | `doc/IGHV1-69_HAstem_Abs.xlsx` 给 `VH_AA`/`VL_AA` 全文 + `VH_nuc`/`VL_nuc` | 328 |
| R71 CGGnaive DMS | C | scFv | `wildtype_sequence.fasta` 给母本 scFv（VH-linker-VL，1,045 nt）；表里 `aa_substitutions` 是 scFv 线性编号替换串，可直接回填 | 8,192 设计 |
| R74 Omi32 BioPhy-Seq | C | IgG（Omi32 谱系） | `protein_Omi-32.fasta` 给母本全长重链（VH-CH1-Fc-TM）+ 轻链；表里 `geno` 为 13 位二元位点码，可回填 | 8,192 基因型 |

### 有条件（10）

序列存在，但不满足「完整 VH/VL 在 bucket 内闭合」。

| 源 | 缺口 |
| --- | --- |
| R14 AB-Bind | 表只有 `#PDB` + `Mutation` + `ddG`，无序列列。32 个复合物里 21 个是抗体—抗原，27 个 fasta 中 20 个是抗体结构。编号规则已抽样验证：1MLC 的 9 个位点在 H/L 链 SEQRES 上全中；12 个复合物的 239 个位点里 178 命中、39 不中、22 超界——**不是每个复合物都能靠位号直接回填**，需逐复合物校准 |
| R15 SKEMPI 2.0 | `Mutation(s)_PDB` 用「角色字母 + SEQRES 位号」（`LI38G` = 轻链第 38 位 I→G），已核验该位号对应 fasta 的 SEQRES 序号（1MLC 的 H57/H58/H28/H35/H99/H98/H100 与 L32/L92 共 9 点全中）。345 个 fasta 中 **57 个是抗体复合物**；缺口只是「哪条链是抗体」需按 fasta 描述判定 |
| R17 PDBbind PP | 只有结构与数值，无归一的序列表。2,852 个 fasta 中有 **636 个是 SAbDab 收录的抗体结构**（与 SAbDab2 的 6,028 个抗体 PDB 取交集所得）。缺的一步是：`INDEX_general_PP` 没有 antibody/antigen 链角色字段，2,852 行里哪 636 行属抗体—抗原、哪条链是抗体，需按 fasta 的链描述自行判定 |
| R19 DIPS-Plus | 表是界面特征；12,601 fasta 可切，其中 **70 个是抗体结构**。比例过低（0.6%），且无链角色字段，不划算 |
| R25 RFdiffusion | `cdr_seq` 是 HCDR+LCDR 的无分隔拼接串，`Hchain`/`Lchain` 只是 PDB 链字母。**它本身就是母本 CDR 的拼接**：抽查 7T82 的 56 aa 可完整切成 6 段、全部逐字命中该 PDB 的 Fab 链，未覆盖 0；7T86 的 51 aa 有 39 aa 无对应（该结构的抗体链不在 bucket 内）。所以能拼的只是「母本已归档」的那部分，而 `ab_cluster` 又表明行间共享同一母本——可用于回填，但必须先按 pdb 逐条确认母本存在 |
| R26 Adaptyv EGFR | Round 2 `result_summary.csv` 402 行，有 `sequence`/`dna`/`kd`/`binding`。设计混合抗体与非抗体骨架：按 `(GGGGS)₃` linker 或 FR4 基序判定，402 条里只有 **51 条（12.7%）是抗体形态**，长度 13–250 aa（中位 89）。`package.zip` 的 4,716 个 CSV 是 BLI 曲线，不是提交数。缺的一步是按序列分型后再取抗体子集 |
| R27 Porebski | `read 1/2/3` 是翻译后的**局部片段**（含 `*` 终止符），非全长；HEL Nb / IL-7 scFv / HER2 scFv 的完整母本未随包发布 |
| R50 Graphinity | 主体是 FoldX/Flex-ddG 计算值，但结构侧完整：`pdb`/`complex`/`ab_chain`/`ag_chain` 四列直接给链角色（如 `1adq` / `1adq_DH31A` / `ab_chain=HL` / `ag_chain=A`），1,406 个 fasta 中 1,342 个是抗体结构。缺的是序列列本身与实验标签（实验子集仅 645/608 条，来自 AB-Bind/SKEMPI） |
| R57 DACUM | SKEMPI 1.1 清理版，无序列列，处理同 R15；147 个 fasta 中 18 个是抗体复合物 |
| R58 dbMPIKT | 只有 `Mutation(s)_PDB` + 突变名 + 标题，无序列列；229 fasta 可作母本但表与链的对应关系未给 |

### 不可用（13，另有 4 个源无数据：R24 / R39 / R52 / R55）

| 源 | 原因 |
| --- | --- |
| R18 BIORAD | 只审计 PDBbind 数值能否由原文支持，无序列 |
| R31 Cao minibinders | 非抗体，长度 <65 aa 的小结合蛋白 |
| R38 IntAct | MITAB 相互作用表，无序列列，只有 interactor ID |
| R51 MaveDB | 只有 `hgvs_pro`，研究主体为一般蛋白；无抗体变区 |
| R53 Saka | 只有 html/docx/xlsx 说明，无可解析表 |
| R56 ASEdb | 只有 `asedb.mysql` 转储 + PDB，未导出可比对表；32 个 fasta 中仅 6 个是抗体结构 |
| R59 BindCraft | `Sequence` 是设计的小结合蛋白，非抗体 |
| R60 AlphaProteo | 非抗体，只有论文 html + 结构 |
| R63 CovEpiAb | 汇总库，只有网页快照与补充表；无逐抗体序列表 |
| R64 COVIC-DB | 各实验室 xlsx，抗体以 `COVIC-1` 类盲化编号标识，序列映射未公开 |
| R65 BID | 历史库，只有 html 快照 |
| **R72 Omicron landscape** | **变体在抗原侧**：`geno` 是 RBD 的 15 位等位码；抗体是 5 个固定参考（REGN10987/CB6/S309/CoV555/ACE2），逐行无抗体序列 |
| **R73 Background dependence** | 同上：`aa_geno` 是 175 aa RBD，抗体为 REGN10987/AZD1061/AZD8895 固定骨架；三个库的变异都在抗原 |
