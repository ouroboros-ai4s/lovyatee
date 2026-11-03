---
tags:
  - context
---

# SRC_R66_KYDAB 数据说明

## 数据集身份

- `source_id`：`SRC_R66_KYDAB`
- `source_version`：`snapshot-2026-03-23`
- 原作者或发布机构：Kymab Limited（KyDab 数据平台责任方；与 NaturalAntibody 作者团队共同发表数据说明）

### 来源方背景

[KyDab 门户条款](https://kydab.naturalantibody.com/terms-of-use)写明，Kymab Limited 是在英格兰注册的公司，注册办事处位于英国剑桥的 Babraham Research Campus。Kymab 开发了 KyDab 平台；平台获得盖茨基金会资助，所载数据来自 Kymab 独立或与其他受资助者共同开展的研究。

[赛诺菲 2021 年收购公告](https://www.sanofi.com/en/media-room/press-releases/2021/2021-01-11-07-30-00-2155914)将 Kymab 介绍为研发全人源单克隆抗体的临床阶段生物制药公司，研发领域包括免疫介导疾病与肿瘤免疫治疗；其 IntelliSelect 平台包含转基因抗体发现技术。赛诺菲于 [2021-04-09 宣布完成对 Kymab Group Ltd. 的收购](https://www.sanofi.com/en/media-room/press-releases/2021/2021-04-09-05-00-00-2207173)。

## 实验设计和数据口径

[KyDab v2 预印本](https://doi.org/10.64898/2026.03.25.713450)说明，来源为 Kymouse 人源化小鼠的 11 项免疫研究，覆盖 51 种免疫原。研究先进行免疫与血清反应筛查，再从选定动物的组织中分选 B 细胞并测定配对重链、轻链序列；部分 clone 经表达与体外结合实验。上游对序列进行了内部分析和 RIOT/IMGT 再注释。当前公开包包含处理后的表、FASTA、注释和部分实验汇总；它未提供仪器事件级原始文件。

11 个主要配对表的记录数合计为 123,527，和论文报告的 productive 配对记录总量相符。各 ZIP 同时包含原始表示、注释 CSV、AIRR 风格链表和 FASTA；这些是同一研究对象的多种表示。48 个表合计 503,249 条文件记录，不能当作独立抗体数。不同研究中只有部分 clone 进入结合实验；未测量行的空值不表示实验阴性。

公开实验测量包括 SPR、HTRF 与 ELISA。SPR 动力学/亲和力、HTRF 信号和 ELISA 荧光值具有不同实验口径，均保留来源列与条件；当前没有把它们换算为统一亲和力或跨实验排行。一个 ELISA 荧光字段出现字面 `NA`；部分条件性 `KD_M_PH*` 字段出现字面零值，其实验含义和检测边界尚待来源方说明。重复测量、多个分析物和 pH 条件可使同一 clone 对应多条文件记录。

## 论文原文

- 标题：KyDab - a comprehensive database of antibody discovery selection campaigns.
- 作者：Qingqing Zhou、Dawid Chomicz、David Melvin、Mark Griffiths、Sabrina Yahiya、Stephen Reece、Marguerite-Marie Le Pannérer、Konrad Krawczyk
- 发表来源：bioRxiv 预印本
- 归档文本版本：bioRxiv v2
- 发布日期：2026-04-15
- DOI：`10.64898/2026.03.25.713450`
- PMID / PMCID：无
- 本地文件：`articles/KyDab_2026-04-15_bioRxiv-v2.pdf`
- 文件大小：1.13 MiB（1189673 bytes）
- SHA-256：`ea113e45206df458fc70514692a6e1c7b6ecdf1db11fb093dc3bd097aaf89735`
- 文本许可：bioRxiv API 标记 `cc_by`
- 补充材料：未在本次归档中保存独立补充文件；相关研究的公开论文入口见门户各研究页

## 仓库内容

上游入口为 [KyDab 官方门户](https://kydab.naturalantibody.com/)，当前项目表列出 11 个 ZIP。门户没有给出统一的不可变 release 名或官方 SHA-256。`snapshot-2026-03-23` 的日期来自已收集官方 ZIP 中最新的 HTTP `Last-Modified`（2026-03-23）；每个原始 URL、ETag、字节数及本地哈希分别记录于采集研究材料。这是项目选择的文件集合快照名。交付目录 `KyDab/` 保存来源 ZIP 原样，不另行解包。

```text
snapshot-2026-03-23/
└── KyDab/
    ├── Influenza-KV7015.zip
    ├── KV7019.zip
    ├── KV7022.zip
    ├── KV7027.zip
    ├── KV7033.zip
    ├── KV7036.zip
    ├── Malaria-CSP-KV7018.zip
    ├── Malaria-CSP-KV7021.zip
    ├── RSV-KV7014.zip
    ├── Typhi-KV7003.zip
    └── pertussis-data.zip
```

11 个 ZIP 分别对应门户的一项研究交付包。各包中的主表、注释表、链表、FASTA 与元数据文件具有不同粒度；并非 11 个独立的平面 CSV。

## 数据结构

### 文件组与记录粒度

11 包共 73 个成员：48 个表、14 个 FASTA、9 个 JSON 和 2 个免疫原序列文本。普通表保存配对记录及实验上下文，`annotated.csv` 保存再注释列，`airr-heavy` 和 `airr-light` 分别保存链级计算注释，FASTA 保存来源序列表示，JSON 是研究级元数据。22 个扩展名为 `.tsv` 的 AIRR 风格文件在当前包中实际采用逗号分隔；读取器应按文件内容识别分隔符。

AIRR 链表的行数因链别和注释覆盖而与主要配对表不同。FASTA、普通表、注释表和 AIRR 链表中的一行所代表的对象也不同，不能把它们直接累加为独立样本。若无来源方连接说明，不能仅凭行序或相同的记录数作逐行对应。

### 实验值原始表示

SPR 相关列含来源给出的 `ka`、`k d`、`KD (M)` 及 pH 条件列；HTRF 表含 `Numerator`、`Denominator`、`Ratio`、`Percent Effect`、`DeltaF`；ELISA 表含 FI 汇总与重复编号。一个 ELISA 列出现 16 个 `NA`。原表的缺失、字面零和重复记录均保留；目前没有可靠依据把空值或零统一解释为无结合。

### 字段说明

对 48 个实际表的表头去重得到 179 个原始字段名。下表按字段族覆盖全部名称；普通/注释表与 AIRR 链表分别列出。所有字段均来自来源文件；除明确写出的 `KD (M)`、`KD_M_PH*` 和 FI 外，不从字段名补造单位或有利方向。AIRR 字段含义参考 [AIRR Rearrangement Schema](https://docs.airr-community.org/en/latest/datarep/rearrangements.html)，但本包实际分隔符以文件为准。

| 文件组与字段族 | 原始字段名 | 类型、单位、缺失和来源 |
| --- | --- | --- |
| 普通/注释表标识 | `ANIMAL`、`ANIMAL_ID`、`CLONE_ID`、`CLONE_NAME`、`ID`、`IDENTIFIER_ANIMAL`、`ID_1`、`STRAIN`、`TISSUE`、`animal_id` | 原样字符串；识别 clone、动物、组织或来源。空串表示原文件未填。不同表的 ID 命名空间尚未证明等价。 |
| 实验对象 | `ANALYTE`、`ANALYTE_NAME`、`ANTIGEN`、`ANTIGEN_NAME`、`Analyte`、`IMMUNOGEN`、`IMMUNOGEN_1`、`LABEL`、`antigen_name` | 原样类别或标签字符串；免疫原、检测分析物与标签列分别保留。`LABEL` 的编码含义尚待来源方说明。 |
| 配对链与片段 | `HEAVY_CHAIN_SEQ`、`LIGHT_CHAIN_SEQ`、`heavy_cdr3`、`heavy_seq`、`light_cdr3`、`light_seq` | 来源给出的序列字符串或局部 CDR3；空串保留。链序列、CDR3 与免疫原序列处于不同粒度。 |
| 链注释 | `heavy_complete_vdj`、`heavy_d_gene`、`heavy_j_gene`、`heavy_locus`、`heavy_productive`、`heavy_v_gene`、`light_complete_vdj`、`light_j_gene`、`light_locus`、`light_productive`、`light_v_gene` | RIOT/上游注释的基因名称、locus 或布尔表示；缺失按原文件空串保留，不作实验标签。 |
| SPR 与动力学 | `CAPTURE_LEVELS_PH5_5`、`CAPTURE_LEVELS_PH7_2`、`CAPTURE_LEVELS_PH7_6`、`Capture Levels`、`Comment`、`KA_PH5_5`、`KA_PH7_2`、`KA_PH7_6`、`KD (M)`、`KD_M_PH5_5`、`KD_M_PH7_2`、`KD_M_PH7_6`、`KD_PH5_5`、`KD_PH7_2`、`KD_PH7_6`、`has_kd_measurement`、`k d`、`ka` | 实验或注释数值、标记、备注；`KD (M)` 与 `KD_M_PH*` 字段名标示摩尔浓度，其他列的单位和零值解释需研究说明确认。空串、字面零均原样保留。 |
| HTRF | `DeltaF`、`Denominator`、`Numerator`、`Percent Effect`、`Ratio` | 实验汇总数值；原值不换算为亲和力，方向、计算公式和缺失口径按研究条件解释。 |
| ELISA | `ELISA MEAN (FI) Abaum all`、`ELISA MEAN (FI) Abaum mean`、`ELISA MEAN (FI) Abaum std`、`ELISA MEAN (FI) OMV all`、`ELISA MEAN (FI) OMV mean`、`ELISA MEAN (FI) OMV std`、`ELISA Mean (FI)`、`Replicate` | 荧光强度 FI 的重复、汇总或离散度表示；`Replicate` 是重复编号。一个 `ELISA Mean (FI)` 列有 16 个字面 `NA`。 |
| AIRR 输入与质控 | `additional_validation_flags`、`complete_vdj`、`exc`、`j_frameshift`、`locus`、`locus_species`、`numbering_scheme`、`productive`、`rev_comp`、`sequence`、`sequence_header`、`stop_codon`、`v_frameshift`、`vj_in_frame` | 原始链记录和 RIOT 质量/生产性标记；`sequence` 是核酸序列，空串为未填，布尔值保留原文本。 |
| AIRR 基因指派 | `c_call`、`d_call`、`j_call`、`j_frame`、`v_call`、`v_frame` | V/D/J/C 基因指派及阅读框注释；这些是计算注释，缺失不表示实验阴性。 |
| AIRR 坐标 | `c_germline_end`、`c_germline_start`、`c_sequence_end`、`c_sequence_start`、`cdr1_end`、`cdr1_start`、`cdr2_end`、`cdr2_start`、`cdr3_end`、`cdr3_start`、`d_alignment_end`、`d_alignment_start`、`d_germline_end`、`d_germline_start`、`d_sequence_end`、`d_sequence_start`、`fwr1_end`、`fwr1_start`、`fwr2_end`、`fwr2_start`、`fwr3_end`、`fwr3_start`、`fwr4_end`、`fwr4_start`、`j_alignment_end`、`j_alignment_start`、`j_germline_end`、`j_germline_start`、`j_sequence_end`、`j_sequence_start`、`v_alignment_end`、`v_alignment_start`、`v_germline_end`、`v_germline_start`、`v_sequence_end`、`v_sequence_start` | 序列、胚系或 CDR/FWR 的起止位置。AIRR 标准以 1 起始闭区间定义对应标准字段；本包的工具特有字段仍保留原值。 |
| AIRR 评分与 CIGAR | `c_cigar`、`c_identity`、`c_score`、`c_support`、`d_cigar`、`d_identity`、`d_score`、`d_support`、`j_cigar`、`j_identity`、`j_score`、`j_support`、`v_cigar`、`v_identity`、`v_score`、`v_support` | 基因比对的计算评分、支持度、同一性或 CIGAR 字符串；不作为结合实验标签。 |
| AIRR CDR/FWR | `cdr1`、`cdr1_aa`、`cdr2`、`cdr2_aa`、`cdr3`、`cdr3_aa`、`fwr1`、`fwr1_aa`、`fwr2`、`fwr2_aa`、`fwr3`、`fwr3_aa`、`fwr4`、`fwr4_aa` | 核酸片段及 `_aa` 氨基酸翻译，依论文所述 RIOT/IMGT 注释；序列范围只限相应区域。 |
| AIRR junction | `junction`、`junction_aa`、`junction_aa_length`、`junction_length` | 接合部的核酸/氨基酸字符串和长度；不与 CDR3 字段直接等同。 |
| AIRR 序列比对与编号映射 | `c_germline_alignment`、`c_germline_alignment_aa`、`c_sequence_alignment`、`c_sequence_alignment_aa`、`d_germline_alignment`、`d_sequence_alignment`、`germline_alignment`、`germline_alignment_aa`、`j_germline_alignment`、`j_germline_alignment_aa`、`j_sequence_alignment`、`j_sequence_alignment_aa`、`positional_scheme_mapping`、`scheme_residue_mapping`、`sequence_aa`、`sequence_aa_scheme_cigar`、`sequence_alignment`、`sequence_alignment_aa`、`v_germline_alignment`、`v_germline_alignment_aa`、`v_sequence_alignment`、`v_sequence_alignment_aa` | 核酸或 `_aa` 氨基酸的比对、胚系参照及编号映射；均为计算注释，不是实验测量。 |

### 数据示例

以下是实际文件首条记录的经核对摘录；为避免在说明文档中再传播逐条序列和测量值，clone 标识、分析物、序列与实验数值明确遮蔽。每行仍是各自原始文件的记录粒度。

| 原始成员 | 已核对字段摘录 | 记录粒度 |
| --- | --- | --- |
| `Influenza-KV7015.csv` | `TISSUE = Spleen / Lymph Node`；`CLONE_NAME`、`LIGHT_CHAIN_SEQ`、`HEAVY_CHAIN_SEQ`、`ANTIGEN_NAME` 已遮蔽 | 普通配对表的一条记录 |
| `INFLUENZA-KV7015-airr-heavy.tsv` | `numbering_scheme = imgt`；`locus = igh`；`productive = True`；`complete_vdj = True`；序列及记录标识已遮蔽 | 重链注释的一条记录 |
| `KV7019_ELISA_with_replicates.csv` | `Replicate = #1`；clone、分析物和 FI 数值已遮蔽 | 一条实验重复记录 |

## PDB 数据库

当前状态为 `partial`，没有发布 `pdb/` 文件。审计了 KyDab 主论文、门户 11 个研究页面、下载包的文件名与表头、NaturalAntibody 公开 GitHub 搜索，以及 RCSB 对 `KyDab`、全称和主论文 DOI 的全文检索。主论文的 PDB 提及用于比较既有数据库；目前没有证据将 KyDab 抗体记录或实验构建体连到具体 PDB 条目。RCSB 名称/DOI 检索无匹配，不能排除各免疫原在其他研究中存在结构。

当前没有可接受的条目级锚点，因此没有给出 PDB ID、分子角色、author/label 链号或逐条结构映射，也没有以空 FASTA/mmCIF 目录表示完成。若后续获得一手构建体到 PDB 的证据，每个被接受锚点均须同时取得 RCSB canonical FASTA 与完整 mmCIF，并分别验收链角色和编号对应。

## 采集过程记录

- 2026-09-22：核对项目配置、来源清单、KyDab 预印本 v2、门户与条款；从 bioRxiv 官方入口取得 v2 PDF，核对 14 页、标题、DOI、版本、文件大小和本地 SHA-256。
- 2026-09-22：用户从门户下载 11 个 ZIP 到共享存储源目录并提供原始 URL。本项目重新枚举门户项目表，确认当前 11 个 ZIP 链接与本地文件集合一致；逐项执行 HTTP HEAD，确认大小与 `Last-Modified`/URL `m` 对应。官方未给整包 SHA-256。
- 2026-09-22：独立遍历 ZIP CRC、成员路径与类型；全部通过。发现部分 `.tsv` 实际采用逗号分隔，随后改用表头检测分隔符并重新计数。表值表示审计记录 48 个表的行形状、空值和特殊编码，没有改写原文件。
- 2026-09-22：保存门户条款响应；把经哈希核对的 11 个 ZIP 和 v2 PDF 复制到同一存储根下的 staging，第二次运行逐项验证现有副本，清除 `.partial`。原始下载文件保留。
- 2026-09-22：审计论文、门户关联文献、公开 GitHub 和 RCSB 名称/DOI 索引；未接受 PDB 锚点。将通过验收的 staging 原子提升为 `snapshot-2026-03-23`，PDB 覆盖仍标记为 `partial`。
- 2026-09-22：逐项复核 source 根目录下载副本与正式版本中 11 个 ZIP 的字节数及 SHA-256 后，清理根目录重复副本；正式版本的 11 个 ZIP 保留并再次验收。
- 2026-09-22：根据 KyDab 门户条款及赛诺菲官方公告补充 Kymab 来源方背景，并更新 README 目录。

## 参考文献

- [KyDab 官方门户](https://kydab.naturalantibody.com/)及各研究落地页。
- [KyDab 条款](https://kydab.naturalantibody.com/terms-of-use)，核查于 2026-09-22。
- [Zhou 等，KyDab bioRxiv v2](https://doi.org/10.64898/2026.03.25.713450)，2026-04-15。
- [AIRR Community Rearrangement Schema](https://docs.airr-community.org/en/latest/datarep/rearrangements.html)，用于理解标准注释字段；本包实际分隔符已单独核验。
- [NaturalAntibody/riot_na](https://github.com/NaturalAntibody/riot_na)，论文所述序列注释工具的公开仓库；没有证据表明其保存 KyDab 的结构映射。
- [RCSB PDB Search API](https://search.rcsb.org/)，用于数据集名称和 DOI 检索。

## 其他

### 完整性与验收

11 个 ZIP 合计 161.24 MiB（169067643 bytes），共 73 个成员；全部通过 ZIP CRC、自检路径、重复成员、符号链接和加密成员审计。以下 SHA-256 均为本地计算值。HTTP `Content-Length` 对 11 包逐项相符，发布方未提供可直接比对的 SHA-256。

| 来源 ZIP | 大小 | 本地 SHA-256 |
| --- | --- | --- |
| `Influenza-KV7015.zip` | 6.11 MiB（6404600 bytes） | `9447e6e7ea4c0660e3fd12910c8076410f02b8d4dbee5cf384be3a90e2f1c900` |
| `KV7019.zip` | 7.34 MiB（7701212 bytes） | `fc6a423fc6d92338a4461c7ac367c75097e79fd7c9d336ad90b4607c3cbd5406` |
| `KV7022.zip` | 15.07 MiB（15806618 bytes） | `460130fa3f6b3859947998441db200851647611a0b90c4b2c191f12622cf296d` |
| `KV7027.zip` | 8.87 MiB（9301983 bytes） | `607f8630a68497da34158e99004c9f2edac5f1be0289f48dfe4c4a56bd35672f` |
| `KV7033.zip` | 8.59 MiB（9009934 bytes） | `231cb033d8ed547bd026bd16490cb4b1bec30275e7f4dfc83f3f5d6b18bd61f4` |
| `KV7036.zip` | 32.79 MiB（34380426 bytes） | `16d262c8cbc05737d3bb67fd30c2d1bcfb6370553936c045fabd65c27e2bd75b` |
| `Malaria-CSP-KV7018.zip` | 26.21 MiB（27481973 bytes） | `acda9cabfbdc6d98231a97c07da3c82d284bbbd7c0f28d76d8bd68daf4235396` |
| `Malaria-CSP-KV7021.zip` | 31.11 MiB（32619642 bytes） | `1ef3f94e58588eca1ef174a6609124367fedd0668a25ad1c37884543d68ec240` |
| `RSV-KV7014.zip` | 1.59 MiB（1669246 bytes） | `2baa25d41591f5cbf537cf580ad0f2dd10dbc9b3b73a80b28cd1d27e33a6187e` |
| `Typhi-KV7003.zip` | 6.12 MiB（6420871 bytes） | `6c198f75c1a81bbb8a30602f68423f143ea0f196d1c391b9f33e83d7e5024f43` |
| `pertussis-data.zip` | 17.42 MiB（18271138 bytes） | `43d1b21703e81ff6e987bd3592f742f676854de3f67ca372929b780214f22dd9` |

### 许可和再分发边界

[门户条款](https://kydab.naturalantibody.com/terms-of-use)规定用户及 Authorized Users 的有限使用许可、数据保管、访问与公开交流时的来源标注。条款由 Kymab 与使用者订立，并可由发布方更新；2026-09-22 的页面响应已保存在共享研究缓存。论文文本的 `cc_by` 许可适用于 bioRxiv 预印本，门户数据按门户条款处理。项目 raw/public 的版本落盘不改变门户条款对访问与再分发的约束。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 11 项研究、51 种免疫原 | 门户当前列出 11 个 ZIP；研究级 JSON 和表格保存免疫原字段，51 种口径尚未逐对象独立复算 | 研究包已包含；免疫原计数待复核 |
| 123,527 条 productive 配对记录 | 11 个普通主表的文件行数合计 123,527；链级 AIRR 行数另有不同 | 文件数量符合论文口径；跨表对象关系待核验 |
| 选定 clone 的体外结合测量 | 部分原表有 SPR、HTRF、ELISA 原始列，多个分析物与重复表示并存 | 部分包含，实验条件和异常值口径待核验 |
| 实验抗体—抗原复合物结构 | 11 包无 PDB/mmCIF 成员，也无已验逐行 PDB 连接键 | 当前公开包未发现结构文件；外部锚点审计为 `partial` |
| 仪器事件级原始读数 | 当前包以表格、FASTA、JSON 与文本交付 | 当前公开包未发现事件级文件 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-22；待来源证据）：SPR pH 条件列的单位、字面零、检测范围，以及 ELISA `NA` 和 HTRF 数值方向尚未从各研究实验说明逐项核实。原值已保留，当前不跨方法换算；下一步核对门户所引研究论文与方法材料。
- `Q02`（最近更新：2026-09-22；PDB `partial`）：主论文、门户和当前 schema 没有可接受的构建体/PDB 键；RCSB 名称/DOI 检索无匹配。当前不指定结构与链；下一步需要来源方或研究论文提供可辩护的构建体级证据。
- `Q03`（最近更新：2026-09-22；版本边界）：`snapshot-2026-03-23` 基于官方 ZIP 最新修改日期，门户没有统一不可变 release 或官方文件 SHA-256。已保存 11 个 URL、ETag、字节数和本地 SHA；未来复核应比较这些对象身份，并记录门户变更。
