---
tags:
  - context
---

# SRC_R25_RFDIFFUSION 数据说明

## 数据集身份

- `source_id`：`SRC_R25_RFDIFFUSION`
- `source_version`：`snapshot-2025-06-25`
- 原作者或发布机构：Nathaniel R. Bennett、Joseph L. Watson 等；University of Washington / Institute for Protein Design

## 实验设计和数据口径

RFdiffusion 抗体研究先从已有复合物构造训练界面及配对负例，再计算设计 VHH/scFv，随后用 yeast display、SPR、竞争/功能实验和 cryo-EM 验证部分候选。Zenodo AntibodyTrainingDataset.csv 是训练样本索引与序列/聚类信息，不是全部设计候选的实验结合表。

CSV 有 11,777 行、6,205 个主 pdb；negative_example=true 5,857 行、false 5,920 行，validation_set=true 1,125 行、false 10,652 行。构造负例的链配对不是实验测得不结合，validation_set 是训练划分。原始 affinity 10,513 行为 None，其余沿用 SAbDab 的异质记录，不能视为统一 assay。cdr_seq 是拼接 CDR，不是完整抗体。结构/target/ab cluster 和负例关系必须成组检查泄漏。论文实验测得 SPR KD、EC50 与结构验证保留在补充 PDF，各自测量意义、单位和候选覆盖不同。

## 论文原文

- 标题：Atomically accurate de novo design of antibodies with RFdiffusion.
- 作者：Bennett NR, Watson JL, Ragotte RJ, Borst AJ, See DL, Weidle C, Biswas R, Yu Y, Shrock EL, Ault R, Leung PJY, Huang B, Goreshnik I, Tam J, Carr KD, Singer B, Criswell C, Wicky BIM, Vafeados D, Garcia Sanchez M, Kim HM, Vázquez Torres S, Chan S, Sun SM, Spear TT, Sun Y, O'Reilly K, Maris JM, Sgourakis NG, Melnyk RA, Liu CC, Baker D.
- 载体与版本：Nature
- 发布日期：2025-11-05
- DOI：10.1038/s41586-025-09721-5
- PMID / PMCID：41193805 / PMC12727541
- 本地文件：`articles/RFDIFFUSION_2025-11-05_EuropePMC-published.xml`
- 文件大小：RFDIFFUSION_2025-11-05_EuropePMC-published.xml：169840 bytes
- SHA-256：RFDIFFUSION_2025-11-05_EuropePMC-published.xml：`d7876bc73c47f2cb3fcb0fa1ef917c89c9b67750a22f6402bf515f978cd1564a`
- 文本许可：CC BY 4.0
- 补充材料：已归档 2 个文件。

| 本地文件 | 角色 | bytes | SHA-256 |
| --- | --- | --- | --- |
| `articles/RFDIFFUSION_2025-11-05_Nature-published-supplement-1.pdf` | Supplementary Information (download PDF ) | 100209859 | `f8bfe510c5f7b4c1910d41655709306832b3c563a97489f86a788094ea01e4ca` |
| `articles/RFDIFFUSION_2025-11-05_Nature-published-supplement-2.pdf` | Reporting Summary (download PDF ) | 1986435 | `269c1f7df84c46a1b793f1995dc7d6165c79d8322550363236eefe44400d7893` |

未取得的文件：primary PDF。已取得的 XML 是一手完整正文，不声称已取得 PDF。

## 仓库内容

- 一手入口：<https://zenodo.org/records/15741710>；record `15741710`；上游日期 2025-06-25。

公开训练 CSV、主文与两份公开 PDF 补充，以及可获得的直接训练 PDB/论文结构。此版本没有另一个全候选统一实验标签 CSV；不得声称每个训练样本均有新 SPR 测量。

上游未给整个数据交付包提供正式版本名；`snapshot-2025-06-25` 取自固定 Zenodo record 15741710 的 `created=2025-06-25T18:41:26.041230+00:00`，表示这条具体版本记录的创建日期。元数据 `publication_date=2025-06-25` 另行保留，不与该日期混用；不使用本次下载日期。原交付归档保持压缩格式，验收时读取所有成员，不在 raw 中重新生成数据表。

```text
snapshot-2025-06-25/
  rfdiffusion/
    AntibodyTrainingDataset.csv
```

## 数据结构

### 原始交付与记录粒度

主 CSV 40 列，将 SAbDab 风格元数据与作者 target_seq、cdr_seq、ab_cluster、target_cluster、negative_item、negative_example、validation_set 组合。negative_item 的条目集合是主 pdb 的子集。论文补充 PDF 中的验证候选和序列不重建为新 CSV；本层保留原始补充文件。

| 原始表或 sheet | 非空数据行 | 列数 |
| --- | --- | --- |
| `rfdiffusion/AntibodyTrainingDataset.csv` | 11777 | 40 |

表行数包含重复条件、示例和派生副本，不求和作为独立生物对象。下表列名保持原始拼写；空表头以 `（空列名）` 标出，未修改文件。

### 字段说明

pdb：训练条目；Hchain/Lchain/antigen_chain：原始 author 链；ab_chains/protein_target_chains：作者处理后的链角色，不能混用；model：结构模型编号；target_seq/cdr_seq：抗原与拼接 CDR 字符串；ab_cluster/target_cluster：派生聚类；negative_item：负配对关联条目；negative_example：构造标签；validation_set：训练划分；affinity/delta_g/affinity_method/temperature：上游异质记录，None 是缺失，单位按原记录；resolution：Å，method 为原始枚举。

| 原始表或 sheet | 字段（原始顺序） | 原始表示与特殊值 |
| --- | --- | --- |
| `rfdiffusion/AntibodyTrainingDataset.csv` | `pdb`, `Hchain`, `Lchain`, `model`, `antigen_chain`, `antigen_type`, `antigen_het_name`, `antigen_name`, `short_header`, `date`, `compound`, `organism`, `heavy_species`, `light_species`, `antigen_species`, `authors`, `resolution`, `method`, `r_free`, `r_factor`, `scfv`, `engineered`, `heavy_subclass`, `light_subclass`, `light_ctype`, `affinity`, `delta_g`, `affinity_method`, `temperature`, `pmid`, `ab_chains`, `protein_target_chains`, `cdr_seq`, `target_seq`, `ab_cluster`, `target_cluster`, `cdr_len`, `negative_item`, `negative_example`, `validation_set` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：antigen_het_name=10203, organism=22, affinity=10514, delta_g=10545, affinity_method=10513, temperature=11556, pmid=10513, Hchain=391, heavy_species=548, r_free=2517, r_factor=2517, heavy_subclass=377, Lchain=2085, light_species=2677, light_subclass=2027, light_ctype=2027, antigen_species=3124, short_header=58, antigen_chain=2813, antigen_type=2813, antigen_name=2813, protein_target_chains=3463, target_seq=3463, target_cluster=3463, negative_item=3463 |

### 数据示例

来自 `rfdiffusion/AntibodyTrainingDataset.csv` 的第一条真实非空数据行：

| 原始字段 | 原始值 |
| --- | --- |
| pdb | 7t82 |
| Hchain | D |
| Lchain | C |
| model | 0 |
| antigen_chain | A |
| antigen_type | protein |
| antigen_het_name | （空字符串） |
| antigen_name | leukocidin e |
| short_header | TOXIN |
| date | 01/11/23 |
| compound | Crystal Structure of LEUKOCIDIN E/CENTYRIN S26/FAB B438 |
| organism | （空字符串） |
| heavy_species | mus musculus |
| light_species | mus musculus |
| antigen_species | staphylococcaceae |
| authors | Luo, J., Malia, T.J., Buckley, P.T. |
| resolution | 3.5 |
| method | X-RAY DIFFRACTION |
| r_free | 0.279 |
| r_factor | 0.229 |
| scfv | False |
| engineered | True |
| heavy_subclass | IGHV1 |
| light_subclass | IGKV1 |
| light_ctype | Kappa |
| affinity | None |
| delta_g | None |
| affinity_method | None |
| temperature | None |
| pmid | None |
| ab_chains | HL |
| protein_target_chains | A |
| cdr_seq | GYKFSSYLPGSGSTISTATDWFAYRSSQTIVYSDGNTYLEKVSNRFSFQGSHVPYT |
| target_seq | SAGSNTNIENIGDGAEVIKRTEDVSSKKWGVTQNVQFDFVKDKKYNKDALIVKMQGFINSRTSFSDVKGSGYELTKRMIWPFQYNIGLTTKDPNVSLINYLPKNKIETTDVGQTLGYNIGGNFQSAPSIGGNGSFNYSKTISYTQKSYVSEVDKQNSKSVKWGVKANEFVTPDGKKSAHDRYLFVQSPNGPTGSAREYFAPDNQLPPLVQSGFNPSFITTLSHEKGSSDTSEFELSYGRNLDITYATLFPRTGIYAERKHNAFVNRNFVVRYKVNWKTHEIKVKGHN |
| ab_cluster | 7t82_H_L_B |
| target_cluster | 7t82_H_L_B |
| cdr_len | 56 |
| negative_item | 6x1u |
| negative_example | False |
| validation_set | False |

这是该原始表的一条记录；粒度按前述定义，不把结构表示、重复或归档成员当独立抗体。

## PDB 数据库

主 CSV 的 `pdb` 去重后是直接条目级训练锚点；`negative_item` 不增加唯一集合。作者链可能包含多字符，完整 FASTA/mmCIF 保留所有实体，不生成统一 H/L 对应或补链。论文新增 9NFU / 9NH7 是实验验证结构，7UHB / 9CM5 是竞争参考，其他明确列出的目标条目属于参考结构，不能与训练行混为新实验样本。撤回条目依据官方状态单独标记，不用相似结构替换。官方 current/removed 全量列表确认训练条目中 51 个已撤回、影响 98 行；直接有效训练条目 6,154 个，另有论文明确引用参考，原审计共接受 6,168 个锚点。2026-10-14 从 wwPDB 历史快照恢复并验证其中 41 个撤回条目的原始 SEQRES FASTA 与 obsolete mmCIF，原 ID 和撤回状态保持不变；其余 10 个仍为 partial。

本次审计接受 6,209 个唯一锚点，每个都有上游原始完整 entry FASTA 与完整 mmCIF（原样 `.cif.gz`），共 12,418 个文件、1.94 GiB（2,083,961,339 bytes）。逐对检查 entry ID、非空 `_atom_site` 及 canonical polymer 序列一致。FASTA 保留上游 entity ID、原始头和序列，没有从坐标重建序列；坐标保留完整原文件。author/label chain 与 entity 的原始映射在 FASTA 头及 mmCIF `_struct_asym`、`_entity_poly`、`_atom_site.auth_asym_id` 中，不臆造链角色。

文件路径为 `pdb/sequences/rcsb_pdb_<PDB>.fasta` 和 `pdb/structures/<PDB>.cif.gz`。确定性 inventory SHA-256：`fd76b59dfd2057003c2b737aa58a1c25f7e2180909fab480775dcc927f347ee2`；算法为按 source version 相对路径排序，逐文件组成 `path<TAB>bytes<TAB>sha256<LF>`（UTF-8）再计算 SHA-256。

PDB 子任务状态为 partial，尚缺 10 个已撤回条目的完整上游配对：`4OZ4` 的 PDBe FASTA 与历史 mmCIF canonical 序列首残基不一致；`5USI`、`6CSY`、`6ERX`、`7CTU`、`7CU4`、`7CU7`、`7KGL`、`7N01`、`7N0S` 仅取得历史 mmCIF，尚无独立上游原始 FASTA。这 11 个候选文件保留在 follow-up staging，不进入 manifest；原 CSV 字段保留，不以相似或后继条目替换。撤回状态证据：<https://data.rcsb.org/rest/v1/holdings/removed/entry_ids>、<https://data.rcsb.org/rest/v1/holdings/current/entry_ids>（2026-09-18）。7N01 的后继条目为 7RW2，但未静默替换。

## 使用方式

由调用者将 `dataset_root` 赋为该 source_version 目录。以下仅读原始入口，不清洗、换算或修补 raw。

```python
import csv
with (dataset_root / "rfdiffusion/AntibodyTrainingDataset.csv").open(encoding="utf-8-sig", newline="") as stream:
    print(next(csv.DictReader(stream)))
```

## 采集过程记录

2026-09-18：按 Zenodo record 15741710 保存训练 CSV，取得主文 XML、Supplementary Information 和 Reporting Summary。官方 current/removed 清单核对 51 个撤回训练 PDB；接受 6,168 个当前训练或论文参考锚点。首次未成功的 7T6B、7T25、7T4S、7TE9 在原进程结束后重试，最终均核验通过；旧失败记录保留在 runs。

2026-10-14：处理 51 个撤回 PDB 的 follow-up 结果。将 41 个具有 wwPDB 历史 SEQRES FASTA 与 obsolete mmCIF 且序列一致的配对发布到正式 `pdb/`，接入共享 reference 并更新 manifest 和迁移台账；正式文件均为 reference 硬链接。4OZ4 的序列不一致候选及 9 个 coordinate-only 条目继续保留在 staging，未伪装成完整锚点。

2026-09-18：全部正式 payload 按来源身份、大小和官方/本地 checksum 独立验收；原始表与附件已读取，FASTA 和完整 mmCIF 逐对核验。工作 README 同步共享版本，规定的 markdownlint 为零错误后发布。具体 API、原始下载日志、失败和重试记录保存在共享本批采集目录，未向任何作者发送消息或申请。

2026-09-18：复核 skill 版本规则，将不符合命名规则的 `zenodo-15741710` 原子重命名为 `snapshot-2025-06-25`。同步来源配置、PDB 配置、工作与共享 README 及当前结构化验收/发布记录；旧文档和原验收记录保留在 runs 的 version-migration-history。修订前后按相对路径、字节数和 SHA-256 比对全部科学文件，内容保持原样；修订 README 使用规定的 markdownlint 配置验收。

2026-09-18：README 工作稿迁入由 developer.user 定位的个人 docs/readme。初版采集记录混用了跨来源的通用描述，本次按实际来源、下载与重试记录修订。论文及附件命名补齐平台和版本。以下名称变更均核对原文件字节数及 SHA-256，内容未改写；原始文件名与下载 URL 保留在采集记录中。

- `articles/RFDIFFUSION_2025-11-05_EuropePMC.xml` → `articles/RFDIFFUSION_2025-11-05_EuropePMC-published.xml`；169840 bytes，SHA-256 `d7876bc73c47f2cb3fcb0fa1ef917c89c9b67750a22f6402bf515f978cd1564a`。
- `articles/RFDIFFUSION_2025-11-05_supplement-1.pdf` → `articles/RFDIFFUSION_2025-11-05_Nature-published-supplement-1.pdf`；100209859 bytes，SHA-256 `f8bfe510c5f7b4c1910d41655709306832b3c563a97489f86a788094ea01e4ca`。
- `articles/RFDIFFUSION_2025-11-05_supplement-2.pdf` → `articles/RFDIFFUSION_2025-11-05_Nature-published-supplement-2.pdf`；1986435 bytes，SHA-256 `269c1f7df84c46a1b793f1995dc7d6165c79d8322550363236eefe44400d7893`。

旧文档和结构化报告保存在共享 runs/documentation-reorganization；修订后本地与共享 README 同步并执行规定的 Markdownlint。

- 上游原始名称 `fullTextXML`；入口 <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12727541/fullTextXML>。
- 上游原始名称 `41586_2025_9721_MOESM1_ESM.pdf`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-025-09721-5/MediaObjects/41586_2025_9721_MOESM1_ESM.pdf>。
- 上游原始名称 `41586_2025_9721_MOESM2_ESM.pdf`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-025-09721-5/MediaObjects/41586_2025_9721_MOESM2_ESM.pdf>。

## 参考文献

- [数据源固定版本/入口](https://zenodo.org/records/15741710)
- [归档主文 DOI](https://doi.org/10.1038/s41586-025-09721-5)
- [primary full-text XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12727541/fullTextXML)
- [Supplementary Information (download PDF )](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-025-09721-5/MediaObjects/41586_2025_9721_MOESM1_ESM.pdf)
- [Reporting Summary (download PDF )](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-025-09721-5/MediaObjects/41586_2025_9721_MOESM2_ESM.pdf)
- [RCSB PDB：按原表 PDB ID 引用条目及原始结构论文](https://www.rcsb.org/)

## 其他

### 完整性与验收

| payload | bytes | SHA-256 |
| --- | --- | --- |
| `rfdiffusion/AntibodyTrainingDataset.csv` | 8516238 | `b55381ea4b843d6360bdc54282e29162de6809d685264397f9ff2f30c3679384` |

原始 payload 合计 8516238 bytes；inventory SHA-256 `62d78f0ba3551f1ad5589519849b04ec7e5960659238253418fd720c030ecc79`（与 PDB 同一算法）。归档成员全部读取；统计与 API/验收报告保存于共享 runs，不作为 raw 附属 manifest 发布。每个文件与论文/PDB 身份均可重验，不执行交付包中的训练代码或模型反序列化。

### 许可和再分发边界

Zenodo 训练数据 CC BY 4.0。Nature 主文现为 CC BY 4.0，官方修订记录注明 2026-09-15 从 CC BY-NC-ND 改为 CC BY；本次以实际版本为准。其他引用结构和关联资料保留其出处。

### 公开范围对照

| 范围 | 本次证据与状态 |
| --- | --- |
| 已取得的公开部分 | 公开训练 CSV、主文与两份公开 PDF 补充，以及可获得的直接训练 PDB/论文结构。此版本没有另一个全候选统一实验标签 CSV；不得声称每个训练样本均有新 SPR 测量。 |
| 论文/来源未公开或未取得部分 | 仅按本文具体缺口报告；未访问限制不冒称完成。 |
| processed / release | 未生成；本层仅上游原样输入。 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-14；partial）：10 个撤回 PDB ID 尚无可发布的完整上游 FASTA/mmCIF 配对。`4OZ4` 的候选 FASTA 与历史 mmCIF canonical 序列不一致；另外 9 个 ID 仅有历史坐标。相关 11 个文件保留在 follow-up staging；下一步仅在取得并验证独立上游原始 FASTA 后发布对应配对并关闭本项。
