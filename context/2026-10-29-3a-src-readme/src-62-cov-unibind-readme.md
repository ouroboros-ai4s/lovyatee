---
tags:
  - context
---

# SRC_R62_COV_UNIBIND 数据说明

## 数据集身份

- `source_id`：`SRC_R62_COV_UNIBIND`
- `source_version`：`snapshot-2025-12-02`
- 原作者或发布机构：InstaDeep Ltd Applied AI 团队与 BioNTech US Systems Immunology 团队（通讯作者 Yunguan Fu）

### 来源方背景

正式论文的七位作者中，Aryan Bhasin、Francesco Saccon、Callum Canavan、Andrew Robson、Joao Euko 和通讯作者 Yunguan Fu 隶属 InstaDeep Ltd，Alexandra C. Walls 隶属 BioNTech US；论文还注明全部工作由 InstaDeep Ltd 资助。数据由 Hugging Face 的 `InstaDeepAI` 账号发布。

[InstaDeep 官方介绍](https://www.instadeep.com/about-us/)记载公司于 2014 年创立，在伦敦等城市设有办公室，业务集中于人工智能和机器学习。[BioNTech 2023-07-31 公告](https://www.biontech.com/content/dam/biontech-corporate/global/pdf/home/media/en/news/attachments/2023/07/15371.pdf)确认已完成对 InstaDeep Ltd 的收购；InstaDeep 此后作为 BioNTech 的伦敦／英国子公司运营，母公司 BioNTech SE 在 Nasdaq 以 `BNTX` 交易。该合作把 InstaDeep 的 AI/ML 能力用于药物发现、免疫疗法与疫苗研发。

## 实验设计和数据口径

CoV-UniBind 是多来源汇编和模型基准，不是一次统一实验。作者从 SAbDab/PDB 整理 SARS-CoV-2 spike—抗体结构，从 CoV-AbDab、COVID-19 Drug Resistance Database（DRDB）、两组 deep mutational scanning（DMS）、Jian 等人的 ELISA 以及五组 SPR 研究汇集标签；再用标准化抗体名称或六条 CDR 序列把实验记录与结构信息连接。DMS 通过大规模单突变筛选给出逃逸量，ELISA 的 IC50 表示达到半最大结合响应所需的抗体浓度，SPR 的 KD 表示平衡解离常数，DRDB 则汇集中和效价变化。六类标签的单位、参照和有利方向并不统一。

当前文件的形成关系为：

```text
CoV-AbDab / DRDB / DMS / ELISA / SPR
                    │
                    ▼
      6 张标准化数据表（75,459 行）
                    │
        ┌───────────┴────────────┐
        ▼                        ▼
SAbDab/PDB 结构处理       模型与基线打分
processed / trimmed ZIP   6 张 scores 表（75,374 行）
        │
        ▼
抗体同义词、CDR、表位与结构连接
```

六张数据表实查如下。“抗原谱系数”是 `antigen_lineage` 的不同取值数；DMS 的单点突变主要写在 `mutations`，因此该列为 1 不代表只有一个抗原变体。

| 文件 | 行数 | 抗体数 | 抗原谱系数 | PDB ID 数 | `target_type` |
| --- | ---: | ---: | ---: | ---: | --- |
| `covabdab_binding.parquet` | 632 | 55 | 40 | 55 | `binding` |
| `dms_bloom_ab_escape.parquet` | 61,661 | 89 | 1 | 84 | `escape` |
| `dms_cao_ab_escape.parquet` | 9,691 | 85 | 1 | 80 | `escape` |
| `drdb_binding_potency.parquet` | 2,472 | 88 | 36 | 84 | IC50/80/90/100 `_log10_fold` |
| `jian_elisa_ab_ic50.parquet` | 164 | 9 | 40 | 8 | `IC50_log10_fold` |
| `spr_ab_affinity.parquet` | 839 | 80 | 12 | 77 | `log10_kd` |

每行表示某个来源中一个标准化抗体名称、抗原谱系／突变组合和标签的组合记录。同一抗体可跨谱系、突变、来源和结构重复出现；同一 `pdb_id` 也服务多行。六表合计 75,459 行，而论文 Table 1 报告 75,460 条；raw 层保留固定 commit 的实际文件，不补造缺少的一行。

`binding` 是布尔标签，当前有 353 个 `True` 和 279 个 `False`。`escape` 是来源 DMS 的连续逃逸值；DRDB/ELISA 的 `*_log10_fold` 与 SPR 的 `log10_kd` 是来源整理后的对数表示。论文评测时按任务需要翻转指标符号，使更高评测分数统一对应更强结合；原始 Parquet 没有统一成同一物理量，训练前须按 `source_name`、`source_doi`、`assay_name` 和 `target_type` 追溯参照、单位与方向。

结构来自 SAbDab 的 Chothia 编号条目。作者去除水和 heteroatom，把含多个抗体的复合物按实际接触拆成抗体—抗原对；抗体保留 VH/VL，抗原另裁剪到 RBD 或 NTD，并以任意原子距离不超过 5 Å 定义 CDR—抗原接触。公开 `processed.zip` 和 `trimmed.zip` 是这套实验 PDB 的处理版本。

模型分数来自折叠、逆折叠、抗体语言模型和两个 DMS 基线。AF2-Monomer、AF2-Multimer、Boltz-1 与 Chai-1 的公开部分只包含模型指标；这些模型产生的预测坐标由论文注明“available upon request”，未包含在本 source version。预测坐标不是新增实验解析结构，其缺失不阻塞公开包接入。

## 论文原文

- 标题：CoV-UniBind: a unified antibody binding database for SARS-CoV-2
- 作者：Aryan Bhasin、Francesco Saccon、Callum Canavan、Andrew Robson、Joao Euko、Alexandra C. Walls、Yunguan Fu
- 发表来源：*Bioinformatics Advances* 6(1):vbaf328
- 归档文本版本：正式发表版的 Europe PMC JATS XML
- 发布日期：2026-01-08
- DOI：[10.1093/bioadv/vbaf328](https://doi.org/10.1093/bioadv/vbaf328)
- PMID / PMCID：[41542366](https://pubmed.ncbi.nlm.nih.gov/41542366/) / [PMC12800777](https://pmc.ncbi.nlm.nih.gov/articles/PMC12800777/)
- 本地文件：`articles/CoV-UniBind_2026-01-08_BioinformaticsAdvances-FullText.xml`
- 文件大小：87.90 KiB（90,007 bytes）
- SHA-256：`4d6e3b160d1a5f24d4feab608bc785de6fc6038da4ce62c9770b2bc51f7a6fd6`
- 文本许可：[Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)
- 补充材料：`articles/CoV-UniBind_2026-01-08_BioinformaticsAdvances-Supplementary.pdf`，6 页，1.01 MiB（1,060,339 bytes），SHA-256 `2653860f3bb80ce273fd1abfe90227b004356b3d7356c66f7b151edbbe18481d`

正式论文的书目日期、标题、DOI、作者、Data Availability 和正文许可已与 [OUP 正式页](https://academic.oup.com/bioinformaticsadvances/article/6/1/vbaf328/8417618)交叉核对。

## 仓库内容

上游入口为 [InstaDeepAI/CoVUniBind](https://huggingface.co/datasets/InstaDeepAI/CoVUniBind)。本 source version 固定不可变 commit [`1a3d3a135c21e2a07bf75c9eb7015585b168bf65`](https://huggingface.co/datasets/InstaDeepAI/CoVUniBind/tree/1a3d3a135c21e2a07bf75c9eb7015585b168bf65)，Hugging Face metadata 时间为 2025-12-02 14:21:53 UTC，因此版本名为 `snapshot-2025-12-02`。payload 是该 commit 的全部 18 个 repository objects，LFS 对象已解析为实际文件。

```text
snapshot-2025-12-02/
└── CoVUniBind/
    ├── .gitattributes
    ├── README.md
    ├── cov-unibind.py
    ├── antibody_info/
    │   └── antibody_synonyms.parquet
    ├── data/
    │   ├── covabdab_binding.parquet
    │   ├── dms_bloom_ab_escape.parquet
    │   ├── dms_cao_ab_escape.parquet
    │   ├── drdb_binding_potency.parquet
    │   ├── jian_elisa_ab_ic50.parquet
    │   ├── spr_ab_affinity.parquet
    │   └── structures/
    │       ├── processed.zip
    │       └── trimmed.zip
    └── scores/
        ├── covabdab_binding_scores.parquet
        ├── dms_bloom_ab_escape_scores.parquet
        ├── dms_cao_ab_escape_scores.parquet
        ├── drdb_binding_potency_scores.parquet
        ├── jian_elisa_ab_ic50_scores.parquet
        └── spr_ab_affinity_scores.parquet
```

六张 `data/` 表保存标准化实验或汇编标签，六张 `scores/` 表保存对应记录的基线与模型分数，`antibody_info/` 保存 183 个标准化抗体及其 CDR/表位信息，两套 ZIP 保存上游加工后的 PDB 坐标。上游 README 的目录树把同义词文件写成 CSV，加载脚本又引用不存在的 `antibody_synonyms_with_epitopes.parquet`；固定 commit 中实际文件名以上述树为准。

## 数据结构

### 六张实验与汇编数据表

六表均有 33 个同名字段。除 `covabdab_binding.parquet` 的布尔 `target_value` 外，其余五表为浮点 `target_value`。裁剪相关字段只在存在相应结构域裁剪时有值：六表共有 52,749 行缺少裁剪序列／范围；`epitope_alteration_count` 在六张数据表中全部为空，它只在 scores 表中计算后填充。

DRDB 表有 2,387 行 IC50、54 行 IC90、30 行 IC80 和 1 行 IC100；对应 scores 表只保留 2,387 个 IC50 行。因此六张 scores 表合计 75,374 行，比六张数据表少 85 行。

### 模型分数表

六张 scores 表保留连接键、原标签、表位变更计数、Cao/Bloom DMS 基线和可用模型输出。各模型并未覆盖全部任务：

| 分数组 | 至少有一个该组指标的行数 | 覆盖表 |
| --- | ---: | --- |
| DMS 与表位基线 | 75,374 | 全部六表 |
| 逆折叠模型 | 75,374 | 全部六表 |
| AF2-Monomer | 13,713 | 除 DMS-Bloom 外的五表 |
| AF2-Multimer | 4,022 | CoV-AbDab、DRDB、ELISA、SPR |
| Boltz-1 | 4,022 | CoV-AbDab、DRDB、ELISA、SPR |
| Chai-1 | 1,635 | CoV-AbDab、ELISA、SPR |
| AbLang2 / IgBERT | 1,463 | CoV-AbDab 与 SPR |

逆折叠分数根据给定抗体—抗原结构评估突变序列。补充方法说明 FAMPNN 使用 negative likelihood ratio，ProteinMPNN、MPNNsol 与 AbMPNN 使用 negative log-likelihood；每个输入的采样数和聚合方式由模型而异。表位变更计数只统计落入结构表位的抗原变更，Cao/Bloom 基线把相应 DMS 的单点逃逸均值对多突变求和；这些分数高时表示更大逃逸倾向。折叠指标是模型置信度或误差指标，不能解释为实验亲和力。

### 抗体同义词表

`antibody_synonyms.parquet` 有 183 行、10 列，`antibody_name` 在当前表中唯一。每行保留一个分号分隔的同义词字符串、一个或多个分号分隔 PDB ID、六条 CDR 序列、结构接触得到的表位残基和表位域。全表可解析 325 个不同 PDB token；`epitope_domain` 为 176 个 `RBD`、6 个 `NTD` 和 1 个 `RBD/S1_CTD1/S1_CTD2`。

论文把六条 CDR 相同的抗体视为抗原相互作用意义上的功能等价项。这个整理规则有助于跨来源匹配，但不证明完整 VH/VL 序列、抗体格式、糖基化或实验构建体完全相同。

### 上游结构归档

`processed.zip` 为 244.82 MiB（256,717,383 bytes），SHA-256 `8c361bd05bc6e29bbc1d6c6754015fc0f8805e4c8ba077749ee926e8b018df00`。安全扫描得到 3,902 个 members，其中 1,950 个符合 `processed/<PDB>_chothia_<chains>.pdb`，覆盖 920 个文件名 PDB ID；另有 1,951 个 `__MACOSX/` metadata members 和一个目录项。解压成员总大小为 1.03 GiB（1,105,350,367 bytes）。

`trimmed.zip` 为 60.09 MiB（63,004,759 bytes），SHA-256 `64144e4ad11648a7db1812f1577c2db96deb96973d754402edddce145b57671e`。安全扫描得到 1,982 个 members，其中 990 个有效 PDB 文件覆盖 362 个 PDB ID，另有 991 个 `__MACOSX/` metadata members 和一个目录项；有效 ID 是 processed 集合的子集。解压成员总大小为 261.54 MiB（274,240,198 bytes）。

六张数据表的 `pdb_id` 并集为 176 个，加入同义词表后并集为 327 个；processed 归档还有 593 个 ID 没有出现在这两类表中。论文正文写 1,950 个处理复合物来自 177 个 unique PDB structures，与固定 commit 的 ZIP 文件名统计不一致。当前不把归档中的额外结构自动映射到实验行。

### 字段说明

六张 `data/` 表的全部 33 个字段按语义分组如下：

| 字段 | 原始表示与含义 |
| --- | --- |
| `antibody_name`、`antigen_lineage` | 标准化抗体同义词字符串与抗原谱系。DMS 的具体变体主要由 `mutations` 表示。 |
| `target_value`、`target_type` | 来源标签及类型；类型和当前行数见下表。布尔 binding、DMS escape、对数 fold 与对数 KD 不能直接混为同一量纲。 |
| `source_name`、`source_doi`、`assay_name` | 上游研究／数据库、论文 DOI 或 URL及 assay 名称；DRDB 的 `assay_name` 有多种 pseudovirus、virus isolate 和其他中和体系。 |
| `pdb_id`、`structure_release_date`、`structure_resolution` | 连接到结构条目的 ID、发布日期和 Å 分辨率。多个数据行可共享同一 PDB。 |
| `mutations` | 谱系共识变更或单点突变的来源字符串；删除和插入沿用上游写法。 |
| `antigen_chain_ids`、`antibody_heavy_chain_id`、`antibody_light_chain_id` | 上游处理结构中的抗原、重链和轻链 author-chain 标识；一个字段可含多个 chain ID。 |
| `antigen_domain`、`antigen_residue_indices`、`antigen_residue_indices_trimmed`、`antigen_host` | 抗原域、完整／裁剪范围和宿主注释。裁剪范围缺失时相应裁剪序列也缺失。 |
| `epitope_residues`、`epitope_mutations`、`epitope_domain` | 结构接触表位、落入表位的变更和表位域。 |
| `epitope_alteration_count` | `data/` 六表全部为空；`scores/` 中为根据结构表位计算的整数变更数。 |
| `spike_sequence` | 完整 spike 氨基酸序列。 |
| `antibody_heavy_chain_sequence`、`antibody_light_chain_sequence` | 上游结构中的完整抗体重／轻链序列。 |
| `antibody_vh_sequence`、`antibody_vl_sequence` | 裁剪到可变域的重／轻链序列。 |
| `antigen_sequence`、`antigen_sequence_trimmed` | 带来源 indel 表示的完整／裁剪抗原序列。 |
| `antigen_sequence_without_indels`、`antigen_sequence_trimmed_without_indels` | 去除插入／删除符号后的完整／裁剪抗原序列。 |
| `antigen_pdb_sequence`、`antigen_pdb_sequence_trimmed` | PDB 坐标对应的完整／裁剪抗原序列。 |

**`target_type`（六张 `data/` 表；取值范围依据：当前 source version 扫描）**

| 原始取值 | 当前记录数 | 含义 |
| --- | ---: | --- |
| `binding` | 632 | CoV-AbDab 的定性结合布尔标签。 |
| `escape` | 71,352 | Bloom/Cao DMS 的连续逃逸标签。 |
| `IC50_log10_fold` | 2,551 | DRDB 中和或 Jian ELISA 结合的 IC50 对数 fold 表示。 |
| `IC80_log10_fold` | 30 | DRDB IC80 对数 fold 表示。 |
| `IC90_log10_fold` | 54 | DRDB IC90 对数 fold 表示。 |
| `IC100_log10_fold` | 1 | DRDB IC100 对数 fold 表示。 |
| `log10_kd` | 839 | SPR KD 的对数表示；文件未附统一单位字段。 |

六张 `scores/` 表的全部分数字段按模型族分组如下；某列只在有相应计算的表中出现，不能把缺列补零：

| 字段组 | 原始字段名与含义 |
| --- | --- |
| 连接与标签 | `antibody_name`、`antigen_lineage`、`pdb_id`、`mutations`、`target_value`；`epitope_domain` 仅见于 CoV-AbDab scores。 |
| 基线 | `epitope_alteration_count`、`cao_dms_global_score`、`bloom_dms_global_score`。 |
| AF2-Monomer | `interchain_pae_monomer`、`interface_pae_monomer`、`overall_pae_monomer`、`interface_plddt_monomer`、`average_plddt_monomer`、`ptm_monomer`、`iptm_monomer`、`interface_ptm_monomer`。 |
| AF2-Multimer | `interchain_pae_multimer`、`interface_pae_multimer`、`overall_pae_multimer`、`interface_plddt_multimer`、`average_plddt_multimer`、`ptm_multimer`、`iptm_multimer`、`interface_ptm_multimer`。 |
| Boltz-1 | `confidence_score_boltz`、`ptm_boltz`、`iptm_boltz`、`protein_iptm_boltz`、`complex_plddt_boltz`、`complex_iplddt_boltz`、`complex_pde_boltz`、`complex_ipde_boltz`。 |
| Chai-1 | `ptm_chai`、`iptm_chai`、`complex_plddt_chai`、`complex_iplddt_chai`、`complex_pae_chai`、`complex_ipae_chai`、`complex_pde_chai`、`complex_ipde_chai`、`rmsd_chai`。 |
| 逆折叠 | `proteinmpnn_scores`、`mpnnsol_scores`、`abmpnn_scores`、`fampnn_0_3_cath_scores`、`fampnn_0_3_scores`、`fampnn_0_0_scores`、`antifold_score`、`interface_antifold_score`、`esmif1_score`、`interface_esmif1_score`。 |
| 抗体语言模型 | `ablang2_score`、`igbert_score`。 |

同义词表的全部 10 个字段为 `antibody_name`、`pdb_id`、`antibody_heavy_chain_cdr1`、`antibody_heavy_chain_cdr2`、`antibody_heavy_chain_cdr3`、`antibody_light_chain_cdr1`、`antibody_light_chain_cdr2`、`antibody_light_chain_cdr3`、`epitope_residues` 和 `epitope_domain`。CDR 与表位字段都是氨基酸或带残基编号的字符串；`pdb_id` 可含分号分隔的多个 ID。

### 数据示例

下面是 `jian_elisa_ab_ic50.parquet` 的一条真实记录摘录：

```text
antibody_name=bd30_515;bd_515
antigen_lineage=BA.1
target_value=-2.3279021420642825
target_type=IC50_log10_fold
source_name=jian_2024_nature
source_doi=10.1038/s41586-024-08315-x
assay_name=elisa
pdb_id=7e88
epitope_domain=RBD
```

对应 `jian_elisa_ab_ic50_scores.parquet` 中存在同一实验连接键的模型行；其中一条真实摘录为：

```text
antibody_name=bd30_515;bd_515
antigen_lineage=B
pdb_id=7e88
mutations=D614G
target_value=-1.4329736338409396
epitope_alteration_count=0
cao_dms_global_score=0.0
bloom_dms_global_score=0.0
```

第一段是一条 ELISA 汇编标签，第二段是同一抗体/PDB 下另一个抗原背景的 score 记录；它们不是重复实验行，也不能仅凭抗体名和 PDB ID 合并。

## PDB 数据库

PDB 审计联合扫描 `processed.zip` 的有效文件名以及六张数据表的 `pdb_id` 字段。processed 归档提供 920 个可解析 PDB ID，已经覆盖数据表中的 176 个 ID；这 920 个 ID 全部在 2026-09-25 从 RCSB 取得一对当前 entry 文件：

- `pdb/sequences/rcsb_pdb_<PDB_ID>.fasta`：920 个 RCSB 完整 entry FASTA。
- `pdb/structures/<PDB_ID>.cif`：920 个 RCSB 完整原始 mmCIF。

两类合计 1,840 个文件、1.84 GiB（1,978,417,332 bytes），按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接得到的 inventory SHA-256 为 `81217569ca4a1aee4873cc832b96d31af203b0bbbb8a980a980e2d265123da1a`。独立验收逐项确认 FASTA header、PDB ID、mmCIF `atom_site` 和 canonical polymer entity sequence。

这些 RCSB 文件与上游 ZIP 的连接强度是 entry 级直接映射；它们保留完整 entry 的全部 polymer 与坐标，没有根据 `<chains>` 文件名裁剪，也没有给链增加推断性角色。只有数据表明确引用的 176 个 ID 具有实验记录级连接；其余 ID 只由上游 processed 归档成员名支持。上游 ZIP 中的 Chothia PDB 是加工坐标，RCSB mmCIF/FASTA 是外部数据库原始 entry 补充，二者不能互相替代。

## 采集过程记录

- 2026-09-19：批次工作流建立 `SRC_R62_COV_UNIBIND/.staging/snapshot-2025-12-02`，按 Hugging Face 固定 commit 获取 18 个公开 repository objects，并归档正式论文全文 XML和 6 页补充 PDF。
- 2026-09-19 至 2026-09-25：校验普通 Git blob 与 LFS SHA-256，解析六张数据表、六张 score 表和同义词表；对两套 ZIP 执行成员遍历、路径穿越、重复项、链接与展开大小安全检查。实际数据表为 75,459 行，论文汇总为 75,460 条，保留差异而未改写 raw 文件。
- 2026-09-25：从 processed ZIP 和 Parquet 字段审计出 920 个唯一 PDB 锚点，补齐 920 对 RCSB FASTA/mmCIF；确认六张数据表只直接引用其中 176 个 ID，并记录论文 177 个 unique PDB 与公开归档 920 个文件名 ID 的差异。
- 2026-09-25：核对正式论文 Data Availability 与补充方法，确认申请制 folded structures 是 AF2-Monomer、AF2-Multimer、Boltz-1 和 Chai-1 的预测坐标；公开 score 指标已落盘，预测坐标缺失按非阻塞事项记录。
- 2026-09-25：OUP 正式页和 Europe PMC XML 均标明 2026-01-08 发布；将原先误用 `2026-01-09` 的全文 XML与补充 PDF 文件名更正为 `2026-01-08`，更名前后大小和 SHA-256 不变。
- 2026-09-25：独立预发布审计确认固定版本、精确文件集、哈希、Parquet schema、ZIP 安全性、论文身份、PDB 配对、无 symlink 和无残留 partial；本地与 staging source README 保持 byte-identical。
- 2026-09-25：发布脚本在移动前后各完成一次全量审计，将暂存目录原子发布为 `SRC_R62_COV_UNIBIND/snapshot-2025-12-02`；前后均为 18 个 payload、920 对 RCSB FASTA/mmCIF。

## 参考文献

- [CoV-UniBind Hugging Face 固定 commit](https://huggingface.co/datasets/InstaDeepAI/CoVUniBind/tree/1a3d3a135c21e2a07bf75c9eb7015585b168bf65)
- [Bhasin, Saccon et al. (2026), CoV-UniBind](https://doi.org/10.1093/bioadv/vbaf328)
- [OUP 正式论文页](https://academic.oup.com/bioinformaticsadvances/article/6/1/vbaf328/8417618)
- [CoV-AbDab](https://doi.org/10.1093/bioinformatics/btaa739)
- [COVID-19 Drug Resistance Database](https://doi.org/10.1371/journal.pone.0261045)
- [Cao et al. DMS](https://doi.org/10.1038/s41586-022-05644-7)
- [Jian et al. ELISA](https://doi.org/10.1038/s41586-024-08315-x)
- [SAbDab](https://doi.org/10.1093/nar/gkt1043)
- [RCSB PDB 文件下载服务](https://www.rcsb.org/docs/programmatic-access/file-download-services)
- [RCSB PDB 使用政策](https://www.rcsb.org/pages/usage-policy)

## 其他

### 数据范围和限制

本 source version 保存上游已经汇编、标准化和计算后的公开对象，不包含各来源实验的底层仪器曲线、plate/FACS/NGS 原始数据或统一 replicate。75,459 行横跨定性 binding、DMS escape、ELISA/中和 IC50 fold 和 SPR KD，测量条件与尺度异质；监督任务应在同一来源和标签口径内构造，并按抗体、谱系、PDB、上游研究和近缘序列控制泄漏。

结构表示也高度非独立：同一 PDB entry 可拆出多个链组合，processed 和 trimmed 可保存同一复合物的不同加工层，RCSB 外部补充又是同一 entry 的完整表示。计数结构文件不能代替计数独立实验或抗体。

### 完整性与验收

Hugging Face payload 为 18 个文件、321.50 MiB（337,119,197 bytes），inventory SHA-256 为 `aad5c3c11e23b479517115d6a563530d1f8751c1ab3edef4ef4fcccd531cfe5a`。论文归档为 87.90 KiB 全文 XML与 1.01 MiB、6 页补充 PDF。外部 PDB 补充为 1,840 个文件、1.84 GiB（1,978,417,332 bytes），inventory SHA-256 为 `81217569ca4a1aee4873cc832b96d31af203b0bbbb8a980a980e2d265123da1a`。

验收覆盖固定 commit、18 个对象的 Git blob/LFS identity、字节数与 SHA-256、全部 Parquet schema 和行数、ZIP 完整遍历及安全性、XML/PDF 身份、920 对 FASTA/mmCIF 的可解析性和 canonical entity sequence。source version 没有 symlink、旁路 manifest、metadata 响应或 `.partial` 文件。

### 许可和再分发边界

正式论文正文明确采用 CC BY 4.0；该许可覆盖论文文本，不自动覆盖 Hugging Face 中汇集自多项研究和数据库的全部数据。固定 Hugging Face card 没有 `license` metadata，仓库也没有独立 LICENSE；上游未特别说明覆盖该数据包的统一许可，使用、商用、衍生和再分发范围仍需逐来源确认。

公开 payload 由上游在 non-gated Hugging Face 入口主动提供，当前未发现与本项目 raw 接入明确冲突的条款，因此统一数据许可缺失不阻塞本 source package 发布。CoV-AbDab、DRDB、DMS、ELISA、SPR、SAbDab/PDB 和各论文的原始权利与引用要求仍分别适用。RCSB 补充遵循 [RCSB PDB 使用政策](https://www.rcsb.org/pages/usage-policy)。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 六类统一实验／汇编数据 | 六张 `data/*.parquet`，实际 75,459 行 | 已包含；与论文 75,460 条差 1 行 |
| 模型和基线分数 | 六张 `scores/*.parquet`，75,374 行 | 已包含；DRDB 只为 2,387 个 IC50 行提供 scores |
| 183 个抗体同义词 | `antibody_synonyms.parquet` 183 行 | 已包含 |
| 1,950 个处理后复合物 | `processed.zip` 1,950 个有效 PDB members | 已包含 |
| 裁剪后的结构表示 | `trimmed.zip` 990 个有效 PDB members | 已包含 |
| 模型 folded structures | Data Availability 说明需申请；公开包只含相关模型指标 | 未包含；不阻塞公开包发布 |
| 统一数据许可 | card 无 license metadata，仓库无独立 LICENSE | 未明确；不阻塞本次接入发布 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-25；非阻塞）：论文只说明 folded structures 可申请，补充方法确认它们是 AF2-Monomer、AF2-Multimer、Boltz-1 和 Chai-1 的预测坐标，但没有公布文件数、逐文件身份、版本或交付许可。公开 score 表已完整验收；当前不提交申请，也不把该缺口解释为实验结构缺失。只有后续任务需要坐标级模型姿态复核时才联系作者，并在取得清单、版本、许可和文件后独立验收关闭。
- `Q02`（最近更新：2026-09-25；非阻塞）：Hugging Face card 和仓库没有覆盖 18 个 payload 对象的统一数据许可。已核对论文 CC BY 4.0、公开 non-gated 入口和多来源组成，未发现阻止本项目 raw 接入的明确条款；商用、衍生和对外再分发仍不得据此推定获准。逐上游来源确认覆盖范围或发布方补充统一许可后关闭。
- `Q03`（最近更新：2026-09-25；非阻塞）：固定文件与论文/card/loader 存在三类公开口径漂移：六表为 75,459 行而论文写 75,460；processed ZIP 覆盖 920 个文件名 PDB ID而论文写 177 个 unique PDB structures；card 把同义词写成 CSV，loader 引用不存在的 `antibody_synonyms_with_epitopes.parquet`。当前以固定 commit 的实际字节和 schema 为准，直接读取 Parquet，并只把六张数据表中的 176 个 PDB ID视为实验行级连接。发布方解释计数口径或修正仓库后重新固定版本并关闭。
