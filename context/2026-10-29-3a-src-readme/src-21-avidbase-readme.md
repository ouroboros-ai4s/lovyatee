---
tags:
  - context
---

# SRC_R21_AVIDBASE 数据说明

## 数据集身份

- `source_id`：`SRC_R21_AVIDBASE`
- `source_version`：`snapshot-2026-07-29`
- 原作者或发布机构：Tadej Medved、Jurij Lah、Goran Miličić、San Hadži；Novartis / AVIDbase

## 实验设计和数据口径

AVIDbase 从 SAbDab / PDB 的 VHH–抗原晶体结构开始，自动提出界面，再人工复核生物学组装、错误注释和非蛋白接触。作者提取界面、去表达标签、统一 IMGT 编号和链名、处理 MSE，最后计算冗余、完整性与结构描述符；Rosetta 重打包/最小化是计算精修，不是新的实验观测。数据截至 2026-02-09，Zenodo 发布日期与截断日期不同。每行是一个界面，不能按每行一个独立抗体或每个结构表示一个独立样本计数。

实测最终工作簿：nr 690 行，prot 591 行，low 99 行，r 1048 行；prot/low 是 nr 的分区，r 是冗余集合。上游 README 的 nr=689 与文件=690 不同，保留原文件。nr/r 合并含 836 个 PDB。Git 内嵌工作簿、示例和 Zenodo 表不是新独立数据。没有逐界面亲和力测量；ΔASA、B-factor、分辨率和计算能量不能当 KD 标签。按共享 PDB、VHH、抗原和 epitope_cluster 检查泄漏。

## 论文原文

- 标题：AVIDbase: A biologically accurate structural dataset of nanobody-antigen complexes.
- 作者：Medved T, Lah J, Miličić G, Hadži S.
- 载体与版本：Protein Sci
- 发布日期：2026-08-24
- DOI：10.1002/pro.70773
- PMID / PMCID：42635303 / PMC13501898
- 本地文件：`articles/AVIDBASE_2026-08-24_EuropePMC-published.xml`
- 文件大小：AVIDBASE_2026-08-24_EuropePMC-published.xml：101077 bytes
- SHA-256：AVIDBASE_2026-08-24_EuropePMC-published.xml：`c72f2cd9fa9b1cda50574fdbd4e7cadcb44e401d23c1c7bc0dff542b8cc94e7b`
- 文本许可：CC BY 4.0
- 补充材料：已归档 1 个文件。

| 本地文件 | 角色 | bytes | SHA-256 |
| --- | --- | --- | --- |
| `articles/AVIDBASE_2026-08-24_ProteinScience-published-supplement-1.docx` | Table S1/S2 and supplementary figures (official EuropePMC supplementary ZIP member) | 746960 | `39080a90a1fff66e2a5bda1e188b25ef74d7f04db7d4f9030c70b738e061dc99` |

未取得的文件：primary PDF。已取得的 XML 是一手完整正文，不声称已取得 PDF。

## 仓库内容

- 一手入口：<https://zenodo.org/records/21675248>；record `21675248`；上游日期 2026-07-29。
- 一手入口：<https://github.com/Novartis/AVIDbase>；commit `69a13d0ddd8adac810c0cf7964927e1f89d8a200`，tree `99a20aa1dcd089778c7e6666b2d9463dad31d8f0`；上游日期 2026-07-29。

正式 Zenodo 三个文件、固定 Git tree、最终界面的外部 PDB 原始序列与坐标。nr/r 不是全部输入候选；辅助 SAbDab 输入中的其他条目不计入最终界面 PDB 覆盖。

上游未给整个数据交付包提供正式版本名；`snapshot-2026-07-29` 取自固定 Zenodo record 21675248 的 `created=2026-07-29T12:20:40.772961+00:00`，表示这条具体版本记录的创建日期。元数据 `publication_date=2026-07-29` 另行保留，不与该日期混用；不使用本次下载日期。 辅助 Git 包仍按下列独立 commit 固定。原交付归档保持压缩格式，验收时读取所有成员，不在 raw 中重新生成数据表。

```text
snapshot-2026-07-29/
  AVIDbase/
    AVIDbase.xlsx
    AVIDbase.zip
    annotation_input_table_MANUAL.xlsx
    AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz
```

Git 快照全部 blob 与固定 commit tree 校验；69a13d0ddd8adac810c0cf7964927e1f89d8a200：52 个 blob，LFS 0，submodule 0。

## 数据结构

### 原始交付与记录粒度

AVIDbase.xlsx 四个 sheet 用 unique_id、PDB 和 interface_index 描述界面；annotation_input_table_MANUAL.xlsx 是人工注释输入。AVIDbase.zip 保留作者整理和计算精修的结构树。Git 包保留全部代码、输入表和示例。原始 author chain 的组装副本后缀（如 `_0`）与最终标准化 H/A 链名属于不同命名体系。

| 原始表或 sheet | 非空数据行 | 列数 |
| --- | --- | --- |
| `AVIDbase/AVIDbase.xlsx#AVIDbase-nr` | 690 | 52 |
| `AVIDbase/AVIDbase.xlsx#AVIDbase-prot` | 591 | 52 |
| `AVIDbase/AVIDbase.xlsx#AVIDbase-low` | 99 | 52 |
| `AVIDbase/AVIDbase.xlsx#AVIDbase-r` | 1048 | 52 |
| `AVIDbase/annotation_input_table_MANUAL.xlsx#Sheet1` | 1909 | 23 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/AVIDbase.xlsx#AVIDbase-nr` | 690 | 52 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/AVIDbase.xlsx#AVIDbase-prot` | 591 | 52 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/AVIDbase.xlsx#AVIDbase-low` | 99 | 52 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/AVIDbase.xlsx#AVIDbase-r` | 1048 | 52 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/annotation_input_table_MANUAL.xlsx#Sheet1` | 1909 | 23 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/example/cluster_plots/ag_name_lysozyme_ag_source_organism_gallus-gallus.tsv` | 9 | 52 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/example/intermediary_tables/annotation_input_table_UNMODIFIED.xlsx#Sheet1` | 1909 | 23 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/example/intermediary_tables/assembly_generation_UNMODIFIED.xlsx#Sheet1` | 1738 | 52 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/input_files/sabdab/20260209_peptide_summary.tsv` | 98 | 30 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/input_files/sabdab/20260209_protein_summary.tsv` | 3185 | 30 |

表行数包含重复条件、示例和派生副本，不求和作为独立生物对象。下表列名保持原始拼写；空表头以 `（空列名）` 标出，未修改文件。

### 字段说明

unique_id：界面字符串标识；PDB：原始条目小写四字符ID；interface_index：从0起的界面编号；variant：从B起的冗余副本，代表记录为空；intra_redundancy / inter_redundancy：指向代表unique_id的关系，非布尔结合标签；epitope_cluster：结构对齐派生簇；interface_integrity：high/medium/low质量分类；bio_assembly_id / assembly_strategy：提取或对称操作得到组装的依据，0不代表官方assembly 0；vhh_pdbx_entity_id：原PDB实体；vhh_auth_chain_id / ag_auth_chain_id：带作者组装副本后缀的链表；vhh_chain_id / ag_chain_id：对应作者整理结构链；resolution：Å。vhh_sequence / ag_sequence：作者从源mmCIF取得并去标签，后者为逗号分隔各抗原链且非规范残基可为X；CDR1/2/3：作者按IMGT编号的VHH片段。missing_density、glycan、cofactor和noncanonical字段为注释/距离，不是亲和力；距离沿用结构坐标Å，缺失/不适用留空。title/date/PMID/DOI/UniProt/edit_comment/selector字段是来源和编辑信息。完整52列原始定义在articles补充DOCX Table S1，原样保留。

| 原始表或 sheet | 字段（原始顺序） | 原始表示与特殊值 |
| --- | --- | --- |
| `AVIDbase/AVIDbase.xlsx#AVIDbase-nr` | `unique_id`, `PDB`, `interface_index`, `variant`, `intra_redundancy`, `inter_redundancy`, `interface_integrity`, `epitope_cluster`, `bio_assembly_id`, `assembly_strategy`, `vhh_pdbx_entity_id`, `vhh_auth_chain_id`, `ag_auth_chain_id`, `vhh_chain_id`, `ag_chain_id`, `vhh_source_organism`, `ag_name`, `ag_protein`, `ag_domain`, `ag_source_organism`, `ag_source_organism_subtype`, `ag_quaternary_structure`, `resolution`, `contains_missing_density`, `vhh_missing_density_spans`, `ag_missing_density_spans`, `closest_missing_density_span`, `closest_missing_density_distance`, `closest_glycan_residue`, `closest_glycan_distance`, `expected_cofactors`, `closest_cofactor`, `closest_cofactor_distance`, `noncanonical_residues`, `interface_noncanonical_residues`, `contains_crystal_waters`, `CDR1`, `CDR2`, `CDR3`, `vhh_sequence`, `ag_sequence`, `interface_residues`, `vhh_pdb_title`, `ag_pdb_title`, `pdb_structure_title`, `release_date`, `pmid`, `publication_doi`, `ag_uniprot_name`, `ag_uniprot_accession_code`, `edit_comment`, `pymol_interface_selector` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：variant=690, intra_redundancy=690, inter_redundancy=690, ag_domain=358, ag_source_organism_subtype=573, vhh_missing_density_spans=615, ag_missing_density_spans=405, closest_missing_density_span=372, closest_missing_density_distance=372, closest_glycan_residue=535, closest_glycan_distance=535, noncanonical_residues=674, interface_noncanonical_residues=687, edit_comment=631, expected_cofactors=577, closest_cofactor=608, closest_cofactor_distance=608, pmid=86, publication_doi=74, ag_uniprot_name=17, ag_uniprot_accession_code=17 |
| `AVIDbase/AVIDbase.xlsx#AVIDbase-prot` | `unique_id`, `PDB`, `interface_index`, `variant`, `intra_redundancy`, `inter_redundancy`, `interface_integrity`, `epitope_cluster`, `bio_assembly_id`, `assembly_strategy`, `vhh_pdbx_entity_id`, `vhh_auth_chain_id`, `ag_auth_chain_id`, `vhh_chain_id`, `ag_chain_id`, `vhh_source_organism`, `ag_name`, `ag_protein`, `ag_domain`, `ag_source_organism`, `ag_source_organism_subtype`, `ag_quaternary_structure`, `resolution`, `contains_missing_density`, `vhh_missing_density_spans`, `ag_missing_density_spans`, `closest_missing_density_span`, `closest_missing_density_distance`, `closest_glycan_residue`, `closest_glycan_distance`, `expected_cofactors`, `closest_cofactor`, `closest_cofactor_distance`, `noncanonical_residues`, `interface_noncanonical_residues`, `contains_crystal_waters`, `CDR1`, `CDR2`, `CDR3`, `vhh_sequence`, `ag_sequence`, `interface_residues`, `vhh_pdb_title`, `ag_pdb_title`, `pdb_structure_title`, `release_date`, `pmid`, `publication_doi`, `ag_uniprot_name`, `ag_uniprot_accession_code`, `edit_comment`, `pymol_interface_selector` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：variant=591, intra_redundancy=591, inter_redundancy=591, ag_domain=297, ag_source_organism_subtype=500, vhh_missing_density_spans=539, ag_missing_density_spans=375, closest_missing_density_span=347, closest_missing_density_distance=347, closest_glycan_residue=476, closest_glycan_distance=476, noncanonical_residues=580, interface_noncanonical_residues=591, edit_comment=539, expected_cofactors=492, closest_cofactor=514, closest_cofactor_distance=514, pmid=78, publication_doi=66, ag_uniprot_name=15, ag_uniprot_accession_code=15 |
| `AVIDbase/AVIDbase.xlsx#AVIDbase-low` | `unique_id`, `PDB`, `interface_index`, `variant`, `intra_redundancy`, `inter_redundancy`, `interface_integrity`, `epitope_cluster`, `bio_assembly_id`, `assembly_strategy`, `vhh_pdbx_entity_id`, `vhh_auth_chain_id`, `ag_auth_chain_id`, `vhh_chain_id`, `ag_chain_id`, `vhh_source_organism`, `ag_name`, `ag_protein`, `ag_domain`, `ag_source_organism`, `ag_source_organism_subtype`, `ag_quaternary_structure`, `resolution`, `contains_missing_density`, `vhh_missing_density_spans`, `ag_missing_density_spans`, `closest_missing_density_span`, `closest_missing_density_distance`, `closest_glycan_residue`, `closest_glycan_distance`, `expected_cofactors`, `closest_cofactor`, `closest_cofactor_distance`, `noncanonical_residues`, `interface_noncanonical_residues`, `contains_crystal_waters`, `CDR1`, `CDR2`, `CDR3`, `vhh_sequence`, `ag_sequence`, `interface_residues`, `vhh_pdb_title`, `ag_pdb_title`, `pdb_structure_title`, `release_date`, `pmid`, `publication_doi`, `ag_uniprot_name`, `ag_uniprot_accession_code`, `edit_comment`, `pymol_interface_selector` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：variant=99, intra_redundancy=99, inter_redundancy=99, ag_domain=61, ag_source_organism_subtype=73, vhh_missing_density_spans=76, closest_glycan_residue=59, closest_glycan_distance=59, expected_cofactors=85, closest_cofactor=94, closest_cofactor_distance=94, noncanonical_residues=94, interface_noncanonical_residues=96, edit_comment=92, ag_missing_density_spans=30, closest_missing_density_span=25, closest_missing_density_distance=25, ag_uniprot_name=2, ag_uniprot_accession_code=2, pmid=8, publication_doi=8 |
| `AVIDbase/AVIDbase.xlsx#AVIDbase-r` | `unique_id`, `PDB`, `interface_index`, `variant`, `intra_redundancy`, `inter_redundancy`, `interface_integrity`, `epitope_cluster`, `bio_assembly_id`, `assembly_strategy`, `vhh_pdbx_entity_id`, `vhh_auth_chain_id`, `ag_auth_chain_id`, `vhh_chain_id`, `ag_chain_id`, `vhh_source_organism`, `ag_name`, `ag_protein`, `ag_domain`, `ag_source_organism`, `ag_source_organism_subtype`, `ag_quaternary_structure`, `resolution`, `contains_missing_density`, `vhh_missing_density_spans`, `ag_missing_density_spans`, `closest_missing_density_span`, `closest_missing_density_distance`, `closest_glycan_residue`, `closest_glycan_distance`, `expected_cofactors`, `closest_cofactor`, `closest_cofactor_distance`, `noncanonical_residues`, `interface_noncanonical_residues`, `contains_crystal_waters`, `CDR1`, `CDR2`, `CDR3`, `vhh_sequence`, `ag_sequence`, `interface_residues`, `vhh_pdb_title`, `ag_pdb_title`, `pdb_structure_title`, `release_date`, `pmid`, `publication_doi`, `ag_uniprot_name`, `ag_uniprot_accession_code`, `edit_comment`, `pymol_interface_selector` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：variant=233, intra_redundancy=233, ag_domain=670, ag_source_organism_subtype=888, vhh_missing_density_spans=940, ag_missing_density_spans=552, closest_missing_density_span=498, closest_missing_density_distance=498, closest_glycan_residue=866, closest_glycan_distance=866, expected_cofactors=862, closest_cofactor=911, closest_cofactor_distance=911, noncanonical_residues=1033, interface_noncanonical_residues=1045, edit_comment=866, inter_redundancy=598, pmid=111, publication_doi=103, ag_uniprot_name=17, ag_uniprot_accession_code=17 |
| `AVIDbase/annotation_input_table_MANUAL.xlsx#Sheet1` | `（空列名）`, `PDB`, `interface_index`, `is_edited`, `edit_comment`, `keep`, `vhh_pdbx_entity_id`, `bio_assembly_id`, `assembly_strategy`, `vhh_auth_chain_id`, `ag_auth_chain_id`, `small_molecules`, `expected_cofactors`, `ag_name`, `vhh_anarcii_score`, `vhh_pdb_title`, `ag_pdb_title`, `resolution`, `pdb_structure_title`, `pmid`, `publication_doi`, `ag_uniprot_name`, `ag_uniprot_accession_code` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：edit_comment=1502, expected_cofactors=1576, small_molecules=883, ag_auth_chain_id=6, pmid=240, publication_doi=214, ag_uniprot_name=53, ag_uniprot_accession_code=53 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/AVIDbase.xlsx#AVIDbase-nr` | `unique_id`, `PDB`, `interface_index`, `variant`, `intra_redundancy`, `inter_redundancy`, `interface_integrity`, `epitope_cluster`, `bio_assembly_id`, `assembly_strategy`, `vhh_pdbx_entity_id`, `vhh_auth_chain_id`, `ag_auth_chain_id`, `vhh_chain_id`, `ag_chain_id`, `vhh_source_organism`, `ag_name`, `ag_protein`, `ag_domain`, `ag_source_organism`, `ag_source_organism_subtype`, `ag_quaternary_structure`, `resolution`, `contains_missing_density`, `vhh_missing_density_spans`, `ag_missing_density_spans`, `closest_missing_density_span`, `closest_missing_density_distance`, `closest_glycan_residue`, `closest_glycan_distance`, `expected_cofactors`, `closest_cofactor`, `closest_cofactor_distance`, `noncanonical_residues`, `interface_noncanonical_residues`, `contains_crystal_waters`, `CDR1`, `CDR2`, `CDR3`, `vhh_sequence`, `ag_sequence`, `interface_residues`, `vhh_pdb_title`, `ag_pdb_title`, `pdb_structure_title`, `release_date`, `pmid`, `publication_doi`, `ag_uniprot_name`, `ag_uniprot_accession_code`, `edit_comment`, `pymol_interface_selector` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：variant=690, intra_redundancy=690, inter_redundancy=690, ag_domain=358, ag_source_organism_subtype=573, vhh_missing_density_spans=615, ag_missing_density_spans=405, closest_missing_density_span=372, closest_missing_density_distance=372, closest_glycan_residue=535, closest_glycan_distance=535, noncanonical_residues=674, interface_noncanonical_residues=687, edit_comment=631, expected_cofactors=577, closest_cofactor=608, closest_cofactor_distance=608, pmid=86, publication_doi=74, ag_uniprot_name=17, ag_uniprot_accession_code=17 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/AVIDbase.xlsx#AVIDbase-prot` | `unique_id`, `PDB`, `interface_index`, `variant`, `intra_redundancy`, `inter_redundancy`, `interface_integrity`, `epitope_cluster`, `bio_assembly_id`, `assembly_strategy`, `vhh_pdbx_entity_id`, `vhh_auth_chain_id`, `ag_auth_chain_id`, `vhh_chain_id`, `ag_chain_id`, `vhh_source_organism`, `ag_name`, `ag_protein`, `ag_domain`, `ag_source_organism`, `ag_source_organism_subtype`, `ag_quaternary_structure`, `resolution`, `contains_missing_density`, `vhh_missing_density_spans`, `ag_missing_density_spans`, `closest_missing_density_span`, `closest_missing_density_distance`, `closest_glycan_residue`, `closest_glycan_distance`, `expected_cofactors`, `closest_cofactor`, `closest_cofactor_distance`, `noncanonical_residues`, `interface_noncanonical_residues`, `contains_crystal_waters`, `CDR1`, `CDR2`, `CDR3`, `vhh_sequence`, `ag_sequence`, `interface_residues`, `vhh_pdb_title`, `ag_pdb_title`, `pdb_structure_title`, `release_date`, `pmid`, `publication_doi`, `ag_uniprot_name`, `ag_uniprot_accession_code`, `edit_comment`, `pymol_interface_selector` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：variant=591, intra_redundancy=591, inter_redundancy=591, ag_domain=297, ag_source_organism_subtype=500, vhh_missing_density_spans=539, ag_missing_density_spans=375, closest_missing_density_span=347, closest_missing_density_distance=347, closest_glycan_residue=476, closest_glycan_distance=476, noncanonical_residues=580, interface_noncanonical_residues=591, edit_comment=539, expected_cofactors=492, closest_cofactor=514, closest_cofactor_distance=514, pmid=78, publication_doi=66, ag_uniprot_name=15, ag_uniprot_accession_code=15 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/AVIDbase.xlsx#AVIDbase-low` | `unique_id`, `PDB`, `interface_index`, `variant`, `intra_redundancy`, `inter_redundancy`, `interface_integrity`, `epitope_cluster`, `bio_assembly_id`, `assembly_strategy`, `vhh_pdbx_entity_id`, `vhh_auth_chain_id`, `ag_auth_chain_id`, `vhh_chain_id`, `ag_chain_id`, `vhh_source_organism`, `ag_name`, `ag_protein`, `ag_domain`, `ag_source_organism`, `ag_source_organism_subtype`, `ag_quaternary_structure`, `resolution`, `contains_missing_density`, `vhh_missing_density_spans`, `ag_missing_density_spans`, `closest_missing_density_span`, `closest_missing_density_distance`, `closest_glycan_residue`, `closest_glycan_distance`, `expected_cofactors`, `closest_cofactor`, `closest_cofactor_distance`, `noncanonical_residues`, `interface_noncanonical_residues`, `contains_crystal_waters`, `CDR1`, `CDR2`, `CDR3`, `vhh_sequence`, `ag_sequence`, `interface_residues`, `vhh_pdb_title`, `ag_pdb_title`, `pdb_structure_title`, `release_date`, `pmid`, `publication_doi`, `ag_uniprot_name`, `ag_uniprot_accession_code`, `edit_comment`, `pymol_interface_selector` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：variant=99, intra_redundancy=99, inter_redundancy=99, ag_domain=61, ag_source_organism_subtype=73, vhh_missing_density_spans=76, closest_glycan_residue=59, closest_glycan_distance=59, expected_cofactors=85, closest_cofactor=94, closest_cofactor_distance=94, noncanonical_residues=94, interface_noncanonical_residues=96, edit_comment=92, ag_missing_density_spans=30, closest_missing_density_span=25, closest_missing_density_distance=25, ag_uniprot_name=2, ag_uniprot_accession_code=2, pmid=8, publication_doi=8 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/AVIDbase.xlsx#AVIDbase-r` | `unique_id`, `PDB`, `interface_index`, `variant`, `intra_redundancy`, `inter_redundancy`, `interface_integrity`, `epitope_cluster`, `bio_assembly_id`, `assembly_strategy`, `vhh_pdbx_entity_id`, `vhh_auth_chain_id`, `ag_auth_chain_id`, `vhh_chain_id`, `ag_chain_id`, `vhh_source_organism`, `ag_name`, `ag_protein`, `ag_domain`, `ag_source_organism`, `ag_source_organism_subtype`, `ag_quaternary_structure`, `resolution`, `contains_missing_density`, `vhh_missing_density_spans`, `ag_missing_density_spans`, `closest_missing_density_span`, `closest_missing_density_distance`, `closest_glycan_residue`, `closest_glycan_distance`, `expected_cofactors`, `closest_cofactor`, `closest_cofactor_distance`, `noncanonical_residues`, `interface_noncanonical_residues`, `contains_crystal_waters`, `CDR1`, `CDR2`, `CDR3`, `vhh_sequence`, `ag_sequence`, `interface_residues`, `vhh_pdb_title`, `ag_pdb_title`, `pdb_structure_title`, `release_date`, `pmid`, `publication_doi`, `ag_uniprot_name`, `ag_uniprot_accession_code`, `edit_comment`, `pymol_interface_selector` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：variant=233, intra_redundancy=233, ag_domain=670, ag_source_organism_subtype=888, vhh_missing_density_spans=940, ag_missing_density_spans=552, closest_missing_density_span=498, closest_missing_density_distance=498, closest_glycan_residue=866, closest_glycan_distance=866, expected_cofactors=862, closest_cofactor=911, closest_cofactor_distance=911, noncanonical_residues=1033, interface_noncanonical_residues=1045, edit_comment=866, inter_redundancy=598, pmid=111, publication_doi=103, ag_uniprot_name=17, ag_uniprot_accession_code=17 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/annotation_input_table_MANUAL.xlsx#Sheet1` | `（空列名）`, `PDB`, `interface_index`, `is_edited`, `edit_comment`, `keep`, `vhh_pdbx_entity_id`, `bio_assembly_id`, `assembly_strategy`, `vhh_auth_chain_id`, `ag_auth_chain_id`, `small_molecules`, `expected_cofactors`, `ag_name`, `vhh_anarcii_score`, `vhh_pdb_title`, `ag_pdb_title`, `resolution`, `pdb_structure_title`, `pmid`, `publication_doi`, `ag_uniprot_name`, `ag_uniprot_accession_code` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：edit_comment=1502, expected_cofactors=1576, small_molecules=883, ag_auth_chain_id=6, pmid=240, publication_doi=214, ag_uniprot_name=53, ag_uniprot_accession_code=53 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/example/cluster_plots/ag_name_lysozyme_ag_source_organism_gallus-gallus.tsv` | `unique_id`, `PDB`, `interface_index`, `variant`, `intra_redundancy`, `inter_redundancy`, `interface_integrity`, `epitope_cluster`, `bio_assembly_id`, `assembly_strategy`, `vhh_pdbx_entity_id`, `vhh_auth_chain_id`, `ag_auth_chain_id`, `vhh_chain_id`, `ag_chain_id`, `vhh_source_organism`, `ag_name`, `ag_protein`, `ag_domain`, `ag_source_organism`, `ag_source_organism_subtype`, `ag_quaternary_structure`, `resolution`, `contains_missing_density`, `vhh_missing_density_spans`, `ag_missing_density_spans`, `closest_missing_density_span`, `closest_missing_density_distance`, `closest_glycan_residue`, `closest_glycan_distance`, `expected_cofactors`, `closest_cofactor`, `closest_cofactor_distance`, `noncanonical_residues`, `interface_noncanonical_residues`, `contains_crystal_waters`, `CDR1`, `CDR2`, `CDR3`, `vhh_sequence`, `ag_sequence`, `interface_residues`, `vhh_pdb_title`, `ag_pdb_title`, `pdb_structure_title`, `release_date`, `pmid`, `publication_doi`, `ag_uniprot_name`, `ag_uniprot_accession_code`, `edit_comment`, `pymol_interface_selector` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：variant=9, intra_redundancy=9, inter_redundancy=9, ag_domain=9, ag_source_organism_subtype=9, vhh_missing_density_spans=8, ag_missing_density_spans=8, closest_missing_density_span=7, closest_missing_density_distance=7, closest_glycan_residue=9, closest_glycan_distance=9, expected_cofactors=9, closest_cofactor=9, closest_cofactor_distance=9, noncanonical_residues=9, interface_noncanonical_residues=9, edit_comment=9 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/example/intermediary_tables/annotation_input_table_UNMODIFIED.xlsx#Sheet1` | `（空列名）`, `PDB`, `interface_index`, `is_edited`, `edit_comment`, `keep`, `vhh_pdbx_entity_id`, `bio_assembly_id`, `assembly_strategy`, `vhh_auth_chain_id`, `ag_auth_chain_id`, `small_molecules`, `expected_cofactors`, `ag_name`, `vhh_anarcii_score`, `vhh_pdb_title`, `ag_pdb_title`, `resolution`, `pdb_structure_title`, `pmid`, `publication_doi`, `ag_uniprot_name`, `ag_uniprot_accession_code` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：edit_comment=1909, expected_cofactors=1909, ag_name=1909, small_molecules=883, pmid=217, publication_doi=191, ag_uniprot_name=53, ag_uniprot_accession_code=53 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/example/intermediary_tables/assembly_generation_UNMODIFIED.xlsx#Sheet1` | `unique_id`, `PDB`, `interface_index`, `variant`, `intra_redundancy`, `inter_redundancy`, `interface_integrity`, `epitope_cluster`, `bio_assembly_id`, `assembly_strategy`, `vhh_pdbx_entity_id`, `vhh_auth_chain_id`, `ag_auth_chain_id`, `vhh_chain_id`, `ag_chain_id`, `vhh_source_organism`, `ag_name`, `ag_protein`, `ag_domain`, `ag_source_organism`, `ag_source_organism_subtype`, `ag_quaternary_structure`, `resolution`, `contains_missing_density`, `vhh_missing_density_spans`, `ag_missing_density_spans`, `closest_missing_density_span`, `closest_missing_density_distance`, `closest_glycan_residue`, `closest_glycan_distance`, `expected_cofactors`, `closest_cofactor`, `closest_cofactor_distance`, `noncanonical_residues`, `interface_noncanonical_residues`, `contains_crystal_waters`, `CDR1`, `CDR2`, `CDR3`, `vhh_sequence`, `ag_sequence`, `interface_residues`, `vhh_pdb_title`, `ag_pdb_title`, `pdb_structure_title`, `release_date`, `pmid`, `publication_doi`, `ag_uniprot_name`, `ag_uniprot_accession_code`, `edit_comment`, `pymol_interface_selector` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：variant=923, intra_redundancy=923, inter_redundancy=1738, epitope_cluster=1738, ag_domain=1028, ag_source_organism_subtype=1461, vhh_missing_density_spans=1555, ag_missing_density_spans=957, closest_missing_density_span=870, closest_missing_density_distance=870, closest_glycan_residue=1401, closest_glycan_distance=1401, expected_cofactors=1439, closest_cofactor=1519, closest_cofactor_distance=1519, noncanonical_residues=1707, interface_noncanonical_residues=1732, edit_comment=1497, pmid=197, publication_doi=177, ag_uniprot_name=34, ag_uniprot_accession_code=34 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/input_files/sabdab/20260209_peptide_summary.tsv` | `pdb`, `Hchain`, `Lchain`, `model`, `antigen_chain`, `antigen_type`, `antigen_het_name`, `antigen_name`, `short_header`, `date`, `compound`, `organism`, `heavy_species`, `light_species`, `antigen_species`, `authors`, `resolution`, `method`, `r_free`, `r_factor`, `scfv`, `engineered`, `heavy_subclass`, `light_subclass`, `light_ctype`, `affinity`, `delta_g`, `affinity_method`, `temperature`, `pmid` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：Lchain=97, antigen_het_name=95, light_species=97, light_subclass=84, light_ctype=84, affinity=98, delta_g=98, affinity_method=98, temperature=98, pmid=98, r_free=12, r_factor=12, antigen_chain=3, antigen_type=3, antigen_name=3, antigen_species=4, heavy_species=1 |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz!AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200/input_files/sabdab/20260209_protein_summary.tsv` | `pdb`, `Hchain`, `Lchain`, `model`, `antigen_chain`, `antigen_type`, `antigen_het_name`, `antigen_name`, `short_header`, `date`, `compound`, `organism`, `heavy_species`, `light_species`, `antigen_species`, `authors`, `resolution`, `method`, `r_free`, `r_factor`, `scfv`, `engineered`, `heavy_subclass`, `light_subclass`, `light_ctype`, `affinity`, `delta_g`, `affinity_method`, `temperature`, `pmid` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：Lchain=3157, antigen_het_name=2632, light_species=3161, light_subclass=3000, light_ctype=3000, affinity=3141, delta_g=3141, affinity_method=3141, temperature=3133, pmid=3118, antigen_chain=36, antigen_type=36, antigen_name=36, antigen_species=67, r_free=1366, r_factor=1366, heavy_species=64, short_header=2, Hchain=3, heavy_subclass=3 |

### 数据示例

来自 `AVIDbase/AVIDbase.xlsx#AVIDbase-nr` 的第一条真实非空数据行：

| 原始字段 | 原始值 |
| --- | --- |
| unique_id | 1g6v_0 |
| PDB | 1g6v |
| interface_index | 0 |
| variant | （空单元格） |
| intra_redundancy | （空单元格） |
| inter_redundancy | （空单元格） |
| interface_integrity | high |
| epitope_cluster | bos-taurus/carbonic-anhydrase/cluster1 |
| bio_assembly_id | 0 |
| assembly_strategy | asym |
| vhh_pdbx_entity_id | 2 |
| vhh_auth_chain_id | K_0 |
| ag_auth_chain_id | A_0 |
| vhh_chain_id | H |
| ag_chain_id | A |
| vhh_source_organism | camelus-dromedarius |
| ag_name | carbonic-anhydrase |
| ag_protein | carbonic-anhydrase |
| ag_domain | （空单元格） |
| ag_source_organism | bos-taurus |
| ag_source_organism_subtype | （空单元格） |
| ag_quaternary_structure | monomer |
| resolution | 3.5 |
| contains_missing_density | 0 |
| vhh_missing_density_spans | （空单元格） |
| ag_missing_density_spans | （空单元格） |
| closest_missing_density_span | （空单元格） |
| closest_missing_density_distance | （空单元格） |
| closest_glycan_residue | （空单元格） |
| closest_glycan_distance | （空单元格） |
| expected_cofactors | ZN |
| closest_cofactor | X.1-ZN |
| closest_cofactor_distance | 19.54000091552734 |
| noncanonical_residues | （空单元格） |
| interface_noncanonical_residues | （空单元格） |
| contains_crystal_waters | 0 |
| CDR1 | GYTVSTYC |
| CDR2 | ILGGSTYY |
| CDR3 | AGSTVASTGWCSRLRPYDYHY |
| vhh_sequence | QVQLVESGGGSVQAGGSLRLSCAASGYTVSTYCMGWFRQAPGKEREGVATILGGSTYYGDSVKGRFTISQDNAKNTVYLQMNSLKPEDTAIYYCAGSTVASTGWCSRLRPYDYHYRGQGTQVTVSS |
| ag_sequence | MSHHWGYGKHNGPEHWHKDFPIAKGERQSPVDIDTHTAKYDPSLKPLSVSYDQATSLRILNNGHAFNVEFDDSQDKAVLKGGPLDGTYRLIQFHFHWGSLDGQGSEHTVDKKKYAAELHLVHWNTKYGDFGKAVQQPDGLAVLGIFLKVGSAKPGLQKVVDVLDSIKTKGKSADFTNFDPRGLLPESLDYWTYPGSLTTPPLLECVTWIVLKEPISVSSEQVLKFRKLNFNGEGEPEELMVDNWRPAQPLKNRQIKASFK |
| interface_residues | H.37,H.108,H.109,H.110,H.111A,H.111C,H.112C,H.112A,H.114,H.116,H.117,A.80,A.46,A.189,A.182,A.52,A.180,A.187,A.188 |
| vhh_pdb_title | ANTIBODY HEAVY CHAIN |
| ag_pdb_title | CARBONIC ANHYDRASE |
| pdb_structure_title | Complex of the camelid heavy-chain antibody fragment CAB-CA05 with bovine carbonic anhydrase |
| release_date | 2000-11-22 |
| pmid | 11342547.0 |
| publication_doi | 10.1074/jbc.M102107200 |
| ag_uniprot_name | CAH2_BOVIN |
| ag_uniprot_accession_code | P00921 |
| edit_comment | （空单元格） |
| pymol_interface_selector | select 1g6v_0_interface, (chain H & resi 108,109,110,111A,111C,112A,112C,114,116,117,37) \| (chain A & resi 180,182,187,188,189,46,52,80) |

这是该原始表的一条记录；粒度按前述定义，不把结构表示、重复或归档成员当独立抗体。

## PDB 数据库

以最终 nr/r 的 PDB 字段去重，836 个条目是直接条目级映射。完整 entry 包含所有 polymer entity 和链，不把原始条目的 chain ID 当作标准化界面的 H/A；未选择某条链、重建组装或补接缺失序列。原始 SEQRES/canonical 序列可长于有坐标的残基。官方 current/removed 列表确认 834 个当前有效条目；9H01、9RIT 已撤回，共影响 3 条 nr/r 界面记录。2026-10-14 从 wwPDB 历史快照恢复并逐对核验这两个撤回条目的原始 SEQRES FASTA 与 obsolete mmCIF，保留原始 ID 和撤回状态，不以当前条目或后继条目替换。

本次审计接受 836 个唯一锚点，每个都有上游原始完整 entry FASTA 与完整 mmCIF（原样 `.cif.gz`），共 1,672 个文件、265.60 MiB（278,501,396 bytes）。逐对检查 entry ID、非空 `_atom_site` 及 canonical polymer 序列一致。FASTA 保留上游 entity ID、原始头和序列，没有从坐标重建序列；坐标保留完整原文件。author/label chain 与 entity 的原始映射在 FASTA 头及 mmCIF `_struct_asym`、`_entity_poly`、`_atom_site.auth_asym_id` 中，不臆造链角色。

文件路径为 `pdb/sequences/rcsb_pdb_<PDB>.fasta` 和 `pdb/structures/<PDB>.cif.gz`。确定性 inventory SHA-256：`b6cb4ab35dc89339149d2828d04c9357144f208a06f9c5e11b647f6aa7705956`；算法为按 source version 相对路径排序，逐文件组成 `path<TAB>bytes<TAB>sha256<LF>`（UTF-8）再计算 SHA-256。

PDB 子任务状态为 completed：834 个当前条目和 2 个历史撤回条目均有已验证的原始 FASTA/mmCIF 配对。撤回状态证据：<https://data.rcsb.org/rest/v1/holdings/removed/entry_ids>、<https://data.rcsb.org/rest/v1/holdings/current/entry_ids>（2026-09-18）；历史文件恢复与正式发布复核于 2026-10-14 完成。

## 使用方式

由调用者将 `dataset_root` 赋为该 source_version 目录。以下仅读原始入口，不清洗、换算或修补 raw。

```python
import openpyxl
book = openpyxl.load_workbook(dataset_root / "AVIDbase/AVIDbase.xlsx", read_only=True, data_only=False)
print(next(book["AVIDbase-nr"].iter_rows(values_only=True)))
```

## 采集过程记录

2026-09-18：按 Zenodo record 21675248 保存三个正式数据文件，另保存作者固定 Git commit。核对 nr/r 的 836 个唯一 PDB，接受 834 个；9H01、9RIT 已撤回，canonical FASTA 缺失，保留原表和 partial 边界。主文 PDF 未取得，归档一手完整 XML 与 DOCX 补充。

2026-10-14：结案原 PDB 缺口。根据 2026-09-18 follow-up 验证记录，将 9H01、9RIT 的 wwPDB 历史 SEQRES FASTA 与 obsolete mmCIF 发布到正式 `pdb/`，接入共享 reference 并更新 manifest 和迁移台账；正式文件均为 reference 硬链接，逐对复核无异常。迁出后 R21 follow-up staging 为空并已清理。

2026-09-18：全部正式 payload 按来源身份、大小和官方/本地 checksum 独立验收；原始表与附件已读取，FASTA 和完整 mmCIF 逐对核验。工作 README 同步共享版本，规定的 markdownlint 为零错误后发布。具体 API、原始下载日志、失败和重试记录保存在共享本批采集目录，未向任何作者发送消息或申请。

2026-09-18：复核 skill 版本规则，将不符合命名规则的 `zenodo-21675248` 原子重命名为 `snapshot-2026-07-29`。同步来源配置、PDB 配置、工作与共享 README 及当前结构化验收/发布记录；旧文档和原验收记录保留在 runs 的 version-migration-history。修订前后按相对路径、字节数和 SHA-256 比对全部科学文件，内容保持原样；修订 README 使用规定的 markdownlint 配置验收。

2026-09-18：README 工作稿迁入由 developer.user 定位的个人 docs/readme。初版采集记录混用了跨来源的通用描述，本次按实际来源、下载与重试记录修订。论文及附件命名补齐平台和版本。以下名称变更均核对原文件字节数及 SHA-256，内容未改写；原始文件名与下载 URL 保留在采集记录中。

- `articles/AVIDBASE_2026-08-24_EuropePMC.xml` → `articles/AVIDBASE_2026-08-24_EuropePMC-published.xml`；101077 bytes，SHA-256 `c72f2cd9fa9b1cda50574fdbd4e7cadcb44e401d23c1c7bc0dff542b8cc94e7b`。
- `articles/AVIDBASE_2026-08-24_supplement-1.docx` → `articles/AVIDBASE_2026-08-24_ProteinScience-published-supplement-1.docx`；746960 bytes，SHA-256 `39080a90a1fff66e2a5bda1e188b25ef74d7f04db7d4f9030c70b738e061dc99`。

旧文档和结构化报告保存在共享 runs/documentation-reorganization；修订后本地与共享 README 同步并执行规定的 Markdownlint。

- 上游原始名称 `fullTextXML`；入口 <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13501898/fullTextXML>。
- 上游原始名称 `PRO-35-e70773-s001.docx`；入口 <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13501898/supplementaryFiles>。

## 参考文献

- [数据源固定版本/入口](https://zenodo.org/records/21675248)
- [数据源固定版本/入口](https://github.com/Novartis/AVIDbase)
- [归档主文 DOI](https://doi.org/10.1002/pro.70773)
- [primary full-text XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13501898/fullTextXML)
- [Table S1/S2 and supplementary figures (official EuropePMC supplementary ZIP member)](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13501898/supplementaryFiles)
- [RCSB PDB：按原表 PDB ID 引用条目及原始结构论文](https://www.rcsb.org/)

## 其他

### 完整性与验收

| payload | bytes | SHA-256 |
| --- | --- | --- |
| `AVIDbase/AVIDbase.xlsx` | 894176 | `c258e7874dd16f21dbc18ed246fdf1edff62338456ef2fc37c2889b40c321ed8` |
| `AVIDbase/AVIDbase.zip` | 372675657 | `f98939854bdf0f84940bfa597bb993a4a64b478668a013e8daa333d8d4e3a97d` |
| `AVIDbase/annotation_input_table_MANUAL.xlsx` | 258117 | `62c885f904fb5630fbb8f8a2e1a687b43e0408599a15d173634bbc357824b3c3` |
| `AVIDbase/AVIDbase-69a13d0ddd8adac810c0cf7964927e1f89d8a200.tar.gz` | 5148654 | `486a1ce9076821afcc7773242ed1eca456e8e9936e3ee0e45e4593f359155dbe` |

原始 payload 合计 378976604 bytes；inventory SHA-256 `ee12b5ccf11647dd46f4305bbdb464d25270d8493a3e103e85d507f68e7fdf6b`（与 PDB 同一算法）。归档成员全部读取；统计与 API/验收报告保存于共享 runs，不作为 raw 附属 manifest 发布。每个文件与论文/PDB 身份均可重验，不执行交付包中的训练代码或模型反序列化。

### 许可和再分发边界

Zenodo 数据 CC BY 4.0；Git 代码 GPL-3.0；论文 CC BY 4.0。PDB 的引用和各层来源应保留。

### 公开范围对照

| 范围 | 本次证据与状态 |
| --- | --- |
| 已取得的公开部分 | 正式 Zenodo 三个文件、固定 Git tree、最终界面的外部 PDB 原始序列与坐标。nr/r 不是全部输入候选；辅助 SAbDab 输入中的其他条目不计入最终界面 PDB 覆盖。 |
| 论文/来源未公开或未取得部分 | 仅按本文具体缺口报告；未访问限制不冒称完成。 |
| processed / release | 未生成；本层仅上游原样输入。 |

## 待解决问题与处理进展

截至 2026-10-14，本次接入与 PDB 锚点核验范围内暂无待解决问题。
