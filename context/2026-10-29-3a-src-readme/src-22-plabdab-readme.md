---
tags:
  - context
---

# SRC_R22_PLABDAB 数据说明

## 数据集身份

- `source_id`：`SRC_R22_PLABDAB`
- `source_version`：`snapshot-2024-08-28`
- 原作者或发布机构：Oxford Protein Informatics Group；B. Abanades 等 PLAbDab 作者

## 实验设计和数据口径

PLAbDab 是 Patent and Literature Antibody Database，从专利与文献收集、整理抗体序列及来源/功能注释，并用 ABodyBuilder2 对部分配对抗体建模。它不是统一 phage-display 测定集。paired/unpaired 表和完整归档是同一来源的不同入口，不能相加成独立样本；专利家族、文献、序列重用和共同亲本可能造成泄漏。

来源文本、靶点描述和模型置信度不等于统一实验亲和力。没有可跨整库直接比较的逐行 KD 标签。预测模型不等于实验复合物，配对链的来源证据需保留。论文声称的规模不能代替本版本文件计数。 本次 paired CSV 实际176894行，精确 heavy_sequence/light_sequence 字符串对去重为78868对；3186行 model=FAILED，其余173708行复用77302个非FAILED模型名。unpaired CSV 有673959行，链枚举为{'L': 287636, 'H': 386323}，numbered 字符串去重300033条。这些精确字符串统计不做同源聚类，也不将配对和未配对表相加成独立抗体。论文说明 ABodyBuilder2 建模前会用 AbLang 补全部分 N端缺失；上游建模输入可能不同于原记录序列，必须保留这种差别，不能把预测补全当实验测得的完整构建体。

原始专利氨基酸序列示例含 B、Z 等模糊字符，不把它们当已确定的标准残基，也不在 raw 层删除或替换。后续模型输入须另行声明字符处理策略。

## 论文原文

- 标题：The Patent and Literature Antibody Database (PLAbDab): an evolving reference set of functionally diverse, literature-annotated antibody sequences and structures.
- 作者：Abanades B, Olsen TH, Raybould MIJ, Aguilar-Sanjuan B, Wong WK, Georges G, Bujotzek A, Deane CM.
- 载体与版本：Nucleic Acids Res
- 发布日期：2023-11-16
- DOI：10.1093/nar/gkad1056
- PMID / PMCID：37971316 / PMC10767817
- 本地文件：`articles/PLABDAB_2023-11-16_EuropePMC-published.xml`
- 文件大小：PLABDAB_2023-11-16_EuropePMC-published.xml：72925 bytes
- SHA-256：PLABDAB_2023-11-16_EuropePMC-published.xml：`27e568b47de11286eea07bcecf0308dea1e5cd99cd979fbd58fa93d7caa57725`
- 文本许可：CC BY 4.0
- 补充材料：无其他独立补充文件。

未取得的文件：primary PDF。已取得的 XML 是一手完整正文，不声称已取得 PDF。

## 仓库内容

- 一手入口：<https://opig.stats.ox.ac.uk/webapps/plabdab/>；HTTP object snapshot；上游日期 见对象 Last-Modified。

官方 paired/unpaired CSV.GZ 与完整 plabdab_data.tar.gz；HTTP 对象快照，无不可变 release。ETag / Last-Modified 和本地 SHA-256 固定本次取得的字节；同 URL 将来可能变化。

快照日期来自已归档 HTTP 对象的 Last-Modified（2024-08-28）；对象 SHA-256、ETag 另行固定。上游未提供不可变 release。原交付归档保持压缩格式，验收时读取所有成员，不在 raw 中重新生成数据表。

```text
snapshot-2024-08-28/
  PLAbDab/
    paired_sequences.csv.gz
    unpaired_sequences.csv.gz
    plabdab_data.tar.gz
```

| 对象 | Last-Modified | ETag |
| --- | --- | --- |
| PLAbDab/paired_sequences.csv.gz | Wed, 28 Aug 2024 23:20:12 GMT | "1724887212.0-11392439-1915491820" |
| PLAbDab/unpaired_sequences.csv.gz | Wed, 28 Aug 2024 15:06:36 GMT | "1724857596.0-43960421-2708412111" |
| PLAbDab/plabdab_data.tar.gz | Wed, 28 Aug 2024 23:42:35 GMT | "1724888555.337334-5045787915-418059270" |

ETag 用于身份条件请求，不把 multipart ETag 当文件 MD5；本地 SHA-256 见验收。

## 数据结构

### 原始交付与记录粒度

两个 gzip CSV 保存配对/非配对序列，完整 TAR.GZ 保存数据库交付的表与模型等原始成员。独立 models.tar.gz 与完整包角色重叠，不重复下载。保留原表列名、引用及来源 ID；实际完整归档内容以下面的成员和表核验为准。 完整归档的原始根目录名为 data-dev；models 中形如 PDB_H_L 的 .pdb 仍是 ABodyBuilder2 预测文件名，不因采用实验来源标识而变成原始实验坐标。整包79125个成员（含目录）、22337362349字节解压内容，79077个 .pdb 模型覆盖当前配对表的全部77302个成功模型名；其余1775个模型不由当前表引用，保留原包不删除。另有历史 unpaired_sequences_2024-05-20（666275行）、paired_sequences_2024-08-28（172907行），以及 failed_to_pair（402296行）、chunks、KaSearch NPZ/CSV 索引。当前未带日期的 paired/unpaired 归档表分别176894/673959行，与独立导出同口径；不将历史、chunks、索引及导出副本重复计入独立抗体。

| 原始表或 sheet | 非空数据行 | 列数 |
| --- | --- | --- |
| `PLAbDab/paired_sequences.csv` | 176894 | 15 |
| `PLAbDab/unpaired_sequences.csv` | 673959 | 17 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/unpaired_sequences_2024-05-20.csv` | 666275 | 17 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_14.csv` | 2 | 17 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_11.csv` | 3190 | 17 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_10.csv` | 56 | 17 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_7.csv` | 11 | 17 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_12.csv` | 4357 | 17 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_8.csv` | 16 | 17 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_13.csv` | 2 | 17 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_4.csv` | 331 | 17 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_0.csv` | 169 | 17 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/kasearch_db/extra_data/kasearch_paired_file.csv` | 176894 | 15 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/kasearch_db/extra_data/kasearch_unpaired_file.csv` | 673959 | 18 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/unpaired_sequences.csv` | 673959 | 17 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/paired_sequences.csv` | 176894 | 15 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/failed_to_pair.csv` | 402296 | 17 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/paired_sequences_2024-08-28.csv` | 172907 | 15 |

表行数包含重复条件、示例和派生副本，不求和作为独立生物对象。下表列名保持原始拼写；空表头以 `（空列名）` 标出，未修改文件。

### 字段说明

序列/链字段：上游序列字符串；publication/patent/source 类字段：出处与连接键；target/annotation：来源文本注释；结构模型和置信度：计算输出。无统一浓度单位/有利方向；缺失注释不能转换为阴性，文本未解析内容保留原样。 paired 字段 ID/heavy_ID/light_ID 保留来源记录标识；heavy_sequence/light_sequence 是来源可变域序列，含非标准残基或原始不确定字符；pairing 为配对策略，实际包括 Patent text/Same entry/Unique source/Ordered entries/Unique chain/Unique word/Xtal structure/TheraSAbDab，精度不能无条件当相同；targets_mentioned 只是原材料提及靶点，并非该抗体结合真值；model 为共享计算模型名或 FAILED，不是质量阈值或 KD。unpaired 的 numbered 是带间隙的编号序列，GBSeq_sequence 保留原数据库字符串（可能小写或范围更长）；GBSeq_*、GBReference_*、clone/isolate 为出处，不用大小写清洗改写原文件。 failed_to_pair 是配对算法未成功的来源记录，不是实验不结合；KaSearch CSV 第一行是 Species/Chain JSON 元数据，第二行才是真实列名，metadata 保留在审计证据中；其 unpaired 表另有 sequence 字段，是搜索用计算表示而非新增实验测量。NPZ 索引原样读取字节，不执行 object array 或模型反序列化。

| 原始表或 sheet | 字段（原始顺序） | 原始表示与特殊值 |
| --- | --- | --- |
| `PLAbDab/paired_sequences.csv` | `ID`, `heavy_sequence`, `light_sequence`, `heavy_ID`, `light_ID`, `heavy_definition`, `light_definition`, `organism`, `reference_authors`, `reference_title`, `update_date`, `cdr_lengths`, `model`, `pairing`, `targets_mentioned` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：targets_mentioned=23329, heavy_ID=1198, light_ID=1198, reference_authors=1, reference_title=1 |
| `PLAbDab/unpaired_sequences.csv` | `chain`, `numbered`, `cdr_lengths`, `GBSeq_locus`, `GBSeq_division`, `GBSeq_update-date`, `GBSeq_create-date`, `GBSeq_definition`, `GBSeq_accession-version`, `GBSeq_other-seqids`, `GBSeq_organism`, `GBSeq_sequence`, `GBSeq_project`, `GBReference_authors`, `GBReference_title`, `isolate`, `clone` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：GBSeq_project=663478, isolate=565811, clone=572858, GBReference_authors=3956, GBReference_title=3956 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/unpaired_sequences_2024-05-20.csv` | `chain`, `numbered`, `cdr_lengths`, `GBSeq_locus`, `GBSeq_division`, `GBSeq_update-date`, `GBSeq_create-date`, `GBSeq_definition`, `GBSeq_accession-version`, `GBSeq_other-seqids`, `GBSeq_organism`, `GBSeq_sequence`, `GBSeq_project`, `GBReference_authors`, `GBReference_title`, `isolate`, `clone` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：GBSeq_project=655928, isolate=558587, clone=565608, GBReference_authors=3823, GBReference_title=3823 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_14.csv` | `chain`, `numbered`, `cdr_lengths`, `GBSeq_locus`, `GBSeq_division`, `GBSeq_update-date`, `GBSeq_create-date`, `GBSeq_definition`, `GBSeq_accession-version`, `GBSeq_other-seqids`, `GBSeq_organism`, `GBSeq_sequence`, `GBSeq_project`, `GBReference_authors`, `GBReference_title`, `isolate`, `clone` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：clone=2 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_11.csv` | `chain`, `numbered`, `cdr_lengths`, `GBSeq_locus`, `GBSeq_division`, `GBSeq_update-date`, `GBSeq_create-date`, `GBSeq_definition`, `GBSeq_accession-version`, `GBSeq_other-seqids`, `GBSeq_organism`, `GBSeq_sequence`, `GBSeq_project`, `GBReference_authors`, `GBReference_title`, `isolate`, `clone` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：GBSeq_project=3149, isolate=3150, clone=3151, GBReference_authors=44, GBReference_title=44 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_10.csv` | `chain`, `numbered`, `cdr_lengths`, `GBSeq_locus`, `GBSeq_division`, `GBSeq_update-date`, `GBSeq_create-date`, `GBSeq_definition`, `GBSeq_accession-version`, `GBSeq_other-seqids`, `GBSeq_organism`, `GBSeq_sequence`, `GBSeq_project`, `GBReference_authors`, `GBReference_title`, `isolate`, `clone` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：GBSeq_project=56, isolate=56, clone=56, GBReference_authors=1, GBReference_title=1 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_7.csv` | `chain`, `numbered`, `cdr_lengths`, `GBSeq_locus`, `GBSeq_division`, `GBSeq_update-date`, `GBSeq_create-date`, `GBSeq_definition`, `GBSeq_accession-version`, `GBSeq_other-seqids`, `GBSeq_organism`, `GBSeq_sequence`, `GBSeq_project`, `GBReference_authors`, `GBReference_title`, `isolate`, `clone` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：GBSeq_project=5, isolate=5, clone=11, GBReference_authors=6, GBReference_title=6 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_12.csv` | `chain`, `numbered`, `cdr_lengths`, `GBSeq_locus`, `GBSeq_division`, `GBSeq_update-date`, `GBSeq_create-date`, `GBSeq_definition`, `GBSeq_accession-version`, `GBSeq_other-seqids`, `GBSeq_organism`, `GBSeq_sequence`, `GBSeq_project`, `GBReference_authors`, `GBReference_title`, `isolate`, `clone` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：GBReference_authors=35, GBReference_title=35, clone=4357, GBSeq_project=4322, isolate=4322 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_8.csv` | `chain`, `numbered`, `cdr_lengths`, `GBSeq_locus`, `GBSeq_division`, `GBSeq_update-date`, `GBSeq_create-date`, `GBSeq_definition`, `GBSeq_accession-version`, `GBSeq_other-seqids`, `GBSeq_organism`, `GBSeq_sequence`, `GBSeq_project`, `GBReference_authors`, `GBReference_title`, `isolate`, `clone` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：GBSeq_project=6, clone=14, GBReference_authors=10, GBReference_title=10, isolate=8 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_13.csv` | `chain`, `numbered`, `cdr_lengths`, `GBSeq_locus`, `GBSeq_division`, `GBSeq_update-date`, `GBSeq_create-date`, `GBSeq_definition`, `GBSeq_accession-version`, `GBSeq_other-seqids`, `GBSeq_organism`, `GBSeq_sequence`, `GBSeq_project`, `GBReference_authors`, `GBReference_title`, `isolate`, `clone` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：clone=2 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_4.csv` | `chain`, `numbered`, `cdr_lengths`, `GBSeq_locus`, `GBSeq_division`, `GBSeq_update-date`, `GBSeq_create-date`, `GBSeq_definition`, `GBSeq_accession-version`, `GBSeq_other-seqids`, `GBSeq_organism`, `GBSeq_sequence`, `GBSeq_project`, `GBReference_authors`, `GBReference_title`, `isolate`, `clone` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：GBReference_authors=2, GBReference_title=2, clone=3, GBSeq_project=330, isolate=2 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/chunks/data_split_0.csv` | `chain`, `numbered`, `cdr_lengths`, `GBSeq_locus`, `GBSeq_division`, `GBSeq_update-date`, `GBSeq_create-date`, `GBSeq_definition`, `GBSeq_accession-version`, `GBSeq_other-seqids`, `GBSeq_organism`, `GBSeq_sequence`, `GBSeq_project`, `GBReference_authors`, `GBReference_title`, `isolate`, `clone` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：GBSeq_project=111, isolate=111, GBReference_authors=58, GBReference_title=58, clone=80 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/kasearch_db/extra_data/kasearch_paired_file.csv` | `ID`, `heavy_sequence`, `light_sequence`, `heavy_ID`, `light_ID`, `heavy_definition`, `light_definition`, `organism`, `reference_authors`, `reference_title`, `update_date`, `cdr_lengths`, `model`, `pairing`, `targets_mentioned` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：targets_mentioned=23329, heavy_ID=1198, light_ID=1198, reference_authors=1, reference_title=1, model=3987 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/kasearch_db/extra_data/kasearch_unpaired_file.csv` | `chain`, `numbered`, `cdr_lengths`, `GBSeq_locus`, `GBSeq_division`, `GBSeq_update-date`, `GBSeq_create-date`, `GBSeq_definition`, `GBSeq_accession-version`, `GBSeq_other-seqids`, `GBSeq_organism`, `GBSeq_sequence`, `GBSeq_project`, `GBReference_authors`, `GBReference_title`, `isolate`, `clone`, `sequence` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：GBSeq_project=663478, isolate=565811, clone=572858, GBReference_authors=3956, GBReference_title=3956 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/unpaired_sequences.csv` | `chain`, `numbered`, `cdr_lengths`, `GBSeq_locus`, `GBSeq_division`, `GBSeq_update-date`, `GBSeq_create-date`, `GBSeq_definition`, `GBSeq_accession-version`, `GBSeq_other-seqids`, `GBSeq_organism`, `GBSeq_sequence`, `GBSeq_project`, `GBReference_authors`, `GBReference_title`, `isolate`, `clone` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：GBSeq_project=663478, isolate=565811, clone=572858, GBReference_authors=3956, GBReference_title=3956 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/paired_sequences.csv` | `ID`, `heavy_sequence`, `light_sequence`, `heavy_ID`, `light_ID`, `heavy_definition`, `light_definition`, `organism`, `reference_authors`, `reference_title`, `update_date`, `cdr_lengths`, `model`, `pairing`, `targets_mentioned` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：targets_mentioned=23329, heavy_ID=1198, light_ID=1198, reference_authors=1, reference_title=1 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/failed_to_pair.csv` | `chain`, `numbered`, `cdr_lengths`, `GBSeq_locus`, `GBSeq_division`, `GBSeq_update-date`, `GBSeq_create-date`, `GBSeq_definition`, `GBSeq_accession-version`, `GBSeq_other-seqids`, `GBSeq_organism`, `GBSeq_sequence`, `GBSeq_project`, `GBReference_authors`, `GBReference_title`, `isolate`, `clone` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：GBReference_authors=3956, GBReference_title=3956, clone=328073, GBSeq_project=394140, isolate=319349 |
| `PLAbDab/plabdab_data.tar.gz!data-dev/paired_sequences_2024-08-28.csv` | `ID`, `heavy_sequence`, `light_sequence`, `heavy_ID`, `light_ID`, `heavy_definition`, `light_definition`, `organism`, `reference_authors`, `reference_title`, `update_date`, `cdr_lengths`, `model`, `pairing`, `targets_mentioned` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：targets_mentioned=23137, heavy_ID=1046, light_ID=1046, reference_authors=1, reference_title=1 |

### 数据示例

来自 `PLAbDab/paired_sequences.csv` 的第一条真实非空数据行：

| 原始字段 | 原始值 |
| --- | --- |
| ID | 763134A |
| heavy_sequence | EVQLVESGGGVVQAGTSLRLSCTASAFNLSDYAMHWVRQAPGKGLZWVALISYGGSBTYYADSVRGRFTISRBISKBTLYLZMKTLRTEDTAVYYCAKLIAVAGTRBFWGQGTLVTVS |
| light_sequence | ESALTZPRSVSGSPGHSVTISCIGTSSNVGDYKYVSWYZZHPGKAPKLIIYEVSSRPSGVPDRFSGSKSGBTASLTISGLQAEDEABYYCCSYIGSYVFGTGTKVLVI |
| heavy_ID | 763134A_H |
| light_ID | 763134A_L |
| heavy_definition | Ig A1 Bur |
| light_definition | Ig A1 Bur |
| organism | Homo sapiens |
| reference_authors | Liu,Y.S.; Low,T.L.; Infante,A.; Putnam,F.W. |
| reference_title | Complete covalent structure of a human IgA1 immunoglobulin |
| update_date | 01-JAN-1900 |
| cdr_lengths | 8_8_12_9_3_8 |
| model | FAILED |
| pairing | Same entry |
| targets_mentioned | （空字符串） |

这是该原始表的一条记录；粒度按前述定义，不把结构表示、重复或归档成员当独立抗体。

## PDB 数据库

paired CSV 中 `pairing=Xtal structure` 的 12,778 条记录，以 `ID=PDB_authorH_authorL` 直接指向 6,834 个唯一条目；显式论文参考 7 条也在这组内。官方 current/removed holdings 确认 6,790 个仍有效、44 个已撤回，共影响 80 行。2026-10-14 从 wwPDB 历史快照恢复并验证其中 37 个撤回条目的原始 SEQRES FASTA 与 obsolete mmCIF，原 ID 和撤回状态保持不变；其余 7 个仍为 partial。TheraSAbDab 行的形如 `PDB_H_L` 模型名没有新增直接条目集合。完整 FASTA/mmCIF 不将可变区片段与整条链当完全相同，不根据模型名推断实验复合物或严格构建体匹配。配对 ID 提供原 author 链来源，全部 author/label 链和 entity 映射留在原文件。其余专利/文献行的 ABodyBuilder2 输出是预测模型，不是假定有实验 PDB 的逐行锚点。本次未配对表 `GBSeq_other-seqids` 中显式 `pdb|ID|` 链接为 0，未新增独立 PDB 锚点；专利/NCBI accession 不按形似 4 字符随意解释为 PDB。

本次审计接受 6,827 个唯一锚点，每个都有上游原始完整 entry FASTA 与完整 mmCIF（原样 `.cif.gz`），共 13,654 个文件、2.29 GiB（2,463,905,100 bytes）。逐对检查 entry ID、非空 `_atom_site` 及 canonical polymer 序列一致。FASTA 保留上游 entity ID、原始头和序列，没有从坐标重建序列；坐标保留完整原文件。author/label chain 与 entity 的原始映射在 FASTA 头及 mmCIF `_struct_asym`、`_entity_poly`、`_atom_site.auth_asym_id` 中，不臆造链角色。

文件路径为 `pdb/sequences/rcsb_pdb_<PDB>.fasta` 和 `pdb/structures/<PDB>.cif.gz`。确定性 inventory SHA-256：`1eb9b021c84bfdfb5e636589d19bd560459f8af394951a12ac679ce98a1a5533`；算法为按 source version 相对路径排序，逐文件组成 `path<TAB>bytes<TAB>sha256<LF>`（UTF-8）再计算 SHA-256。

PDB 子任务状态为 partial，尚缺 7 个已撤回条目的完整上游配对：`4OZ4` 的 PDBe FASTA 与历史 mmCIF canonical 序列首残基不一致；`5USI`、`6ERX`、`7CTU`、`7CU4`、`7CU7`、`7N01` 仅取得历史 mmCIF，尚无独立上游原始 FASTA。这 8 个候选文件保留在 follow-up staging，不进入 manifest；原 CSV 字段保留，不以相似或后继条目替换。撤回状态证据：<https://data.rcsb.org/rest/v1/holdings/removed/entry_ids>、<https://data.rcsb.org/rest/v1/holdings/current/entry_ids>（2026-09-18）。

## 使用方式

由调用者将 `dataset_root` 赋为该 source_version 目录。以下仅读原始入口，不清洗、换算或修补 raw。

```python
import gzip, csv
with gzip.open(dataset_root / "PLAbDab/paired_sequences.csv.gz", "rt", encoding="utf-8-sig", newline="") as stream:
    print(next(csv.DictReader(stream)))
```

## 采集过程记录

2026-09-18：按原始 HTTP 对象保存 paired/unpaired CSV.GZ 和完整模型 TAR.GZ。服务给 gzip 文件标注 Content-Encoding:gzip，采集时保留压缩原字节；大包按 Range 恢复，曾将并发从 16 降到 4。全量读取 79,125 个模型归档成员，核对 77,302 个当期成功模型名称覆盖；取得 6,790 对有效 PDB，44 个撤回条目明确 partial。KaSearch 表的首行 JSON metadata 与第二行真实表头分别保留。

2026-10-14：处理 44 个撤回 PDB 的 follow-up 结果。将 37 个具有 wwPDB 历史 SEQRES FASTA 与 obsolete mmCIF 且序列一致的配对发布到正式 `pdb/`，接入共享 reference 并更新 manifest 和迁移台账；正式文件均为 reference 硬链接。4OZ4 的序列不一致候选及 6 个 coordinate-only 条目继续保留在 staging，未伪装成完整锚点。

2026-09-18：全部正式 payload 按来源身份、大小和官方/本地 checksum 独立验收；原始表与附件已读取，FASTA 和完整 mmCIF 逐对核验。工作 README 同步共享版本，规定的 markdownlint 为零错误后发布。具体 API、原始下载日志、失败和重试记录保存在共享本批采集目录，未向任何作者发送消息或申请。

2026-09-18：复核 skill 版本规则，核实并保留 `snapshot-2024-08-28`，补充一手版本命名依据。同步来源配置、PDB 配置、工作与共享 README 及当前结构化验收/发布记录；旧文档和原验收记录保留在 runs 的 version-migration-history。修订前后按相对路径、字节数和 SHA-256 比对全部科学文件，内容保持原样；修订 README 使用规定的 markdownlint 配置验收。

2026-09-18：README 工作稿迁入由 developer.user 定位的个人 docs/readme。初版采集记录混用了跨来源的通用描述，本次按实际来源、下载与重试记录修订。论文及附件命名补齐平台和版本。以下名称变更均核对原文件字节数及 SHA-256，内容未改写；原始文件名与下载 URL 保留在采集记录中。

- `articles/PLABDAB_2023-11-16_EuropePMC.xml` → `articles/PLABDAB_2023-11-16_EuropePMC-published.xml`；72925 bytes，SHA-256 `27e568b47de11286eea07bcecf0308dea1e5cd99cd979fbd58fa93d7caa57725`。

旧文档和结构化报告保存在共享 runs/documentation-reorganization；修订后本地与共享 README 同步并执行规定的 Markdownlint。

- 上游原始名称 `fullTextXML`；入口 <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10767817/fullTextXML>。

## 参考文献

- [数据源固定版本/入口](https://opig.stats.ox.ac.uk/webapps/plabdab/)
- [归档主文 DOI](https://doi.org/10.1093/nar/gkad1056)
- [primary full-text XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10767817/fullTextXML)
- [RCSB PDB：按原表 PDB ID 引用条目及原始结构论文](https://www.rcsb.org/)

## 其他

### 完整性与验收

| payload | bytes | SHA-256 |
| --- | --- | --- |
| `PLAbDab/paired_sequences.csv.gz` | 11392439 | `10f0fb3b82ddee09209adaff51340380294e3782ba90034af16c9f1d56c458a5` |
| `PLAbDab/unpaired_sequences.csv.gz` | 43960421 | `fc1b726b6bad656021d32b7fb120f78e976f2fb1b908e3b3e61f26528715b448` |
| `PLAbDab/plabdab_data.tar.gz` | 5045787915 | `554359b11c8fcc18a4f8fce29e540e4212c1611fdf22478a97868ffbbc7d522a` |

原始 payload 合计 5101140775 bytes；inventory SHA-256 `a1183e5ebde5087dee1b9037c6372f2622fa1ec147d7eb3260bf80257d3b9802`（与 PDB 同一算法）。归档成员全部读取；统计与 API/验收报告保存于共享 runs，不作为 raw 附属 manifest 发布。每个文件与论文/PDB 身份均可重验，不执行交付包中的训练代码或模型反序列化。

### 许可和再分发边界

论文 CC BY 4.0 不自动授予整个数据库、专利序列或上游文献的商业/再分发权。公开下载入口不等于所有材料同一许可证，使用时保留文献与专利出处。

### 公开范围对照

| 范围 | 本次证据与状态 |
| --- | --- |
| 已取得的公开部分 | 官方 paired/unpaired CSV.GZ 与完整 plabdab_data.tar.gz；HTTP 对象快照，无不可变 release。ETag / Last-Modified 和本地 SHA-256 固定本次取得的字节；同 URL 将来可能变化。 |
| 论文/来源未公开或未取得部分 | 仅按本文具体缺口报告；未访问限制不冒称完成。 |
| processed / release | 未生成；本层仅上游原样输入。 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-14；partial）：7 个撤回 PDB ID 尚无可发布的完整上游 FASTA/mmCIF 配对。`4OZ4` 的候选 FASTA 与历史 mmCIF canonical 序列不一致；另外 6 个 ID 仅有历史坐标。相关 8 个文件保留在 follow-up staging；下一步仅在取得并验证独立上游原始 FASTA 后发布对应配对并关闭本项。
