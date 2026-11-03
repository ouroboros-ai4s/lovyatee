---
- tags:
  - context
---

# SRC_R31_CAO_MINIBINDERS 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
  - [Cao 2022](#cao-2022)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [NGS 与计算输出](#ngs-与计算输出)
  - [设计模型与计算支架](#设计模型与计算支架)
  - [字段说明](#字段说明)
  - [数据示例](#数据示例)
- [PDB 数据库](#pdb-数据库)
- [采集过程记录](#采集过程记录)
- [参考文献](#参考文献)
- [其他](#其他)
  - [数据范围和限制](#数据范围和限制)
  - [完整性与验收](#完整性与验收)
  - [许可和再分发边界](#许可和再分发边界)
  - [公开范围对照](#公开范围对照)
- [待解决问题与处理进展](#待解决问题与处理进展)

## 数据集身份

- `source_id`：`SRC_R31_CAO_MINIBINDERS`
- `source_version`：`snapshot-2021-10-09`
- 原作者或发布机构：Longxing Cao、Brian Coventry、David Baker 等；University of Washington Institute for Protein Design 及合作机构

### 来源方背景

[华盛顿大学蛋白质设计研究所](https://www.ipd.uw.edu/about/)成立于 2012 年，汇集计算、生物和工程团队开展蛋白质设计。其负责人 David Baker 的团队开发了 Rosetta 等设计工具；Baker 获 [2024 年诺贝尔化学奖](https://www.ipd.uw.edu/2024/10/david-baker-wins-nobel-prize-for-protein-design/)。研究所介绍的成果还包括计算设计蛋白质疫苗与多项蛋白质设计方法。

本数据对应的工作由当时的 Baker 实验室研究人员 Longxing Cao、Brian Coventry 等牵头，团队用计算设计和实验筛选针对 12 个分子靶点获得结合蛋白，并公开了设计模型与筛选分析材料。该项目的[研究所介绍](https://www.ipd.uw.edu/2022/03/protein-drugs-designed-from-the-ground-up/)提供了研究背景和参与机构。

## 实验设计和数据口径

研究用靶点实验结构产生 50–65 aa 的 de novo miniprotein binder，经过计算设计/过滤，再以酵母表面展示、FACS 富集和深测序检验结合。主文报告 12 个 native protein 的 13 个位点（EGFR 选择两个位点）；后续 SSM、motif-grafting、优化设计和 SARS-CoV-2 RBD 分支另有相关数据。它是跨靶点蛋白 binder 数据，不能把这些短蛋白称为抗体。

pool 测序计数与 sort 浓度/收集比例共同用于估计 SC50，作为结合解离常数的 proxy。作者列名 kd_lb/kd_ub 是该估计的区间边界，不是所有设计的直接物理 KD。论文指出表达差异可造成拟合约五倍变化，并将低计数、疑似双转化细胞和 avidity 差异纳入质量判断；avid 与非 avid 的 SC50 不直接比较。inf、NaN、开放区间、low_conf 不能擅自归为有限值或统一阴性。少数优化设计有 BLI 验证，不能将其测量口径推广到全部 NGS 估计行。

包中混合原作者的序列/计数、sort 元数据、分析输出、计算 score、预测模型与图；项目 raw 层指保持这些上游字节，不意味着全是仪器原始数据。相同设计有不同分析表示、SSM 变体和共享 parent，模型 PDB/silent 表示也不是独立样本。训练切分应按设计亲本、真实序列和靶点考虑相关性。

## 论文原文

### Cao 2022

- 标题：Design of protein-binding proteins from the target structure alone
- 作者：Longxing Cao；Brian Coventry；Inna Goreshnik；Buwei Huang；William Sheffler；Joon Sung Park；Kevin M. Jude；Iva Marković；Rameshwar U. Kadam；Koen H. G. Verschueren；Kenneth Verstraete；Scott Thomas Russell Walsh；Nathaniel Bennett；Ashish Phal；Aerin Yang；Lisa Kozodoy；Michelle DeWitt；Lora Picton；Lauren Miller；Eva-Maria Strauch；Nicholas D. DeBouver；Allison Pires；Asim K. Bera；Samer Halabiya；Bradley Hammerson；Wei Yang；Steffen Bernard；Lance Stewart；Ian A. Wilson；Hannele Ruohola-Baker；Joseph Schlessinger；Sangwon Lee；Savvas N. Savvides；K. Christopher Garcia；David Baker
- 载体与版本：Nature；published PDF
- 发布日期：2022-03-24
- DOI：[10.1038/s41586-022-04654-9](https://doi.org/10.1038/s41586-022-04654-9)
- PMID / PMCID：35332283 / PMC9117152
- 本地文件：`articles/CaoMinibinders_2022-03-24_EuropePMC-published.xml`；`articles/CaoMinibinders_2022-03-24_Nature-published.pdf`
- 文件大小：CaoMinibinders_2022-03-24_EuropePMC-published.xml：280.63 KiB（287,362 bytes）；CaoMinibinders_2022-03-24_Nature-published.pdf：27.37 MiB（28,696,570 bytes）
- SHA-256：CaoMinibinders_2022-03-24_EuropePMC-published.xml：`7aef69b9917f1d9991dbd0210245c22d72a1aa6302ab1590d5095dba691e3825`；CaoMinibinders_2022-03-24_Nature-published.pdf：`dd48067c97ab4daed6e0a7115cb3f96209356cd7eea72c20bee92efb79903121`
- 文本许可：CC BY 4.0；第三方内容依其注明条件
- 补充材料：`articles/CaoMinibinders_2022-03-24_Nature-SupplementaryInformation.pdf`；`articles/CaoMinibinders_2022-03-24_Nature-ReportingSummary.pdf`

补充材料逐文件身份：

| 文件 | 大小 | SHA-256 |
| --- | --- | --- |
| `articles/CaoMinibinders_2022-03-24_Nature-SupplementaryInformation.pdf` | 4.22 MiB（4,425,016 bytes） | `22d42f6b8f53e454fc4a2a4c13db77385c278c41550f36a04998025a360c0840` |
| `articles/CaoMinibinders_2022-03-24_Nature-ReportingSummary.pdf` | 1.78 MiB（1,865,789 bytes） | `edd34d8b7ebea750ed9ef339d45f0025487c99eaef30bf249e29e4a7811283dd` |

## 仓库内容

一手入口为 Nature Data Availability 指向的 UW IPD supplemental_files。目录索引访问被拒绝，但原作者逐文件链接有效。没有正式 release/commit，snapshot-2021-10-09 取实验包 HTTP Last-Modified；两个全量模型对象为 2021-07-19，其他对象为 2021-10-09。这是混合对象快照的命名锚点，不能视为 2021-10-09 Git tree；每对象的 ETag/日期由下载配置保留，本次 SHA-256 固定实际字节身份。

```text
snapshot-2021-10-09/
└── robust_de_novo_design_minibinders_2021/
    ├── computational_protocol_analysis.tar.gz
    ├── experimental_data_and_analysis.tar.gz
    ├── scripts_and_main_pdbs.tar.gz
    ├── scaffolds.tar.gz
    ├── design_models_pdb.tar.gz
    └── design_models_silent.tar.gz
```

实验归档包含 sorting_ngs_data 与 ngs_analysis；计算归档包含图用计算 score；scripts_and_main_pdbs 是设计脚本、主要模型和分析代码；scaffolds 是计算支架库。六个声明归档均已取得并验收；两个 design_models 全量归档也列入实际 payload 树。

## 数据结构

### NGS 与计算输出

原实验 tar 有 27 个 sorts.csv，列数主要为 11；对应 pooled_counts.list 的列为 pool 加 description，实际列数取决于 sort 数。`sequences.list` 无表头，按空白分隔后依次为 AA、DNA、design name 三字段；亲和力 `.sc` 表也按空白分隔读取。本项目没有给 raw 文件添加列头。FGFR2 的计数/序列与主要亲和力 score 各有 59,999 行，可用 description/第三字段连接。

主 affinities 目录实际 27 张 score 表，通常 12 列，FGFR2_ssm/Tie2 为 11 列，H3_ssm_2 为 10 列。不能以一张 score 的 schema 概括全部。`affinities_no_doubly_transformed_thresold/` 是取消某过滤的另一分析表示，保留原拼写；不能叠加成新增实验。SSM validation/correlation、heatmap、grafting score 和计算图 score 是后验分析或计算输出。

| 实验 score 文件 | 数据行 | 列数 |
| --- | --- | --- |
| PDGFR.sc | 99992 | 12 |
| IL7Ra_graft.sc | 100000 | 12 |
| EGFR_ssm.sc | 14832 | 12 |
| Tie2_ssm.sc | 11124 | 12 |
| EGFR.sc | 99803 | 12 |
| H3.sc | 59941 | 12 |
| TGFb.sc | 15000 | 12 |
| FGFR2_ssm.sc | 30476 | 11 |
| TrkA.sc | 15000 | 12 |
| VirB8.sc | 15011 | 12 |
| InsulinR.sc | 59973 | 12 |
| CD3d_ssm.sc | 7492 | 12 |
| IGF1R.sc | 15000 | 12 |
| IGF1R_ssm.sc | 3556 | 12 |
| IL7Ra_ssm.sc | 7757 | 12 |
| FGFR2.sc | 59999 | 12 |
| SARS_CoV2_RBD_ssm.sc | 57392 | 12 |
| H3_ssm_2.sc | 12666 | 10 |
| TrkA_ssm.sc | 6303 | 12 |
| H3_ssm.sc | 16563 | 12 |
| Tie2.sc | 100000 | 11 |
| PDGFR_ssm.sc | 26717 | 12 |
| SARS_CoV2_RBD.sc | 99998 | 12 |
| VirB8_ssm.sc | 1217 | 12 |
| IL7Ra.sc | 14999 | 12 |
| InsulinR_ssm.sc | 40352 | 12 |
| TGFb_ssm.sc | 6180 | 12 |

### 设计模型与计算支架

| 归档 | 成员数（含目录） | PDB 文件数 |
| --- | --- | --- |
| computational_protocol_analysis.tar.gz | 17 | 0 |
| experimental_data_and_analysis.tar.gz | 778 | 53 |
| scripts_and_main_pdbs.tar.gz | 421 | 249 |
| scaffolds.tar.gz | 66837 | 66808 |
| design_models_pdb.tar.gz | 1056699 | 1056668 |
| design_models_silent.tar.gz | 31 | 0 |

已验收包中共 1,123,778 个 PDB 文件通过坐标读取，共 4,081,197,617 个原子记录。scaffolds 是上游计算支架库，scripts_and_main_pdbs 含设计/参考模型；这些文件数不是独立实验 binder 数，也不表示相同数量的晶体结构或唯一序列。RCSB 完整实验条目在后文单独验收，不以设计模型代替。上表已计入两个 design_models 全量包。

### 字段说明

| 文件 / 原始字段 | 表示、单位与来源 | 缺失与方向 |
| --- | --- | --- |
| sequences.list：三个无表头字段 | 设计 binder AA、含构建 flanks 的 DNA、设计名；原作者序列 | 不是抗体 VH/VL；第三字段连接 description，不自行翻译或裁剪 |
| pooled_counts.list：`bc1`–`bc38` 中该文件实际出现的列、`description` | 各测序 pool 的计数，原文件为浮点字符串；设计名 | 不同靶点文件含不同 `bc` 子集；零是计数零，不能直接作为不结合标签 |
| sorts.csv：pool_name、parent_pool、concentration | pool 关系及靶浓度（nM）；实验元数据 | 非普通 sort 的 concentration 可空；不能把 expression sort 当 binding sort |
| sorts.csv：avidity、special、collection_fraction | avid/空、expression/空等；收集比例 | avid 与非 avid 不同测量口径；non_standard_gate/notes 影响排除 |
| sorts.csv：collected_cells 或 num_cells | 收集细胞数，原始列名存在例外 | 按每文件列头处理，不强制一个 schema |
| sorts.csv：`special_num`、`frac_matching_seqs`、`non_standard_gate`、`notes` | 特殊 sort 编号、序列匹配比例、非标准 gate 标记和备注；实验元数据 | 空格/空值保留；非标准 gate 需要结合原始 sort 条件解释 |
| *.sc：kd_lb、kd_ub、avid_lb、avid_ub | NGS/FACS 派生 SC50 区间；nM | inf 是开放/不可估上界；0 和 NaN 保留；不是精确 KD |
| *.sc：low_conf、avid_doesnt_agree | 布尔字符串；低计数/avidity 不一致质量标志 | True 不应作为可靠数值标签；不能把此后验质量信息混入预测输入 |
| *.sc：binder_4000_nm、binder_400_nm | 上游按单次 sort 的阈值分类 | README 注释和列名阈值描述有差异；不自行改名或推断精确 KD |
| *.sc：`binder_800_nm` | 另一阈值分类列，仅在部分 score schema 出现 | 与上述两列同样需核对上游阈值定义 |
| *.sc：target、description | 实验目录/靶点标签与设计 ID | 部分 score 文件没有 target 字段，以原表和目录联接 |
| 计算 *.sc：ddg、contact_molecular_surface、score_per_res | Rosetta/几何派生值；单位按上游 README，非实验亲和力 | 不要当作实验 label；预测结构不是晶体结构 |

固定归档的原始列名覆盖清单如下。`pooled_counts.list` 的 `bc1`–`bc38` 是跨 27 个文件的并集，不表示每个文件都含全部列；`.sc` 的浓度前缀 `*_counts`、`*_enrich` 分别是对应 sort 的计数与富集派生值。`SCORE:` 是 Rosetta 表的行标记，不算字段。除上表已解释的实验主标签外，`delta_*`、`entropy_*`、`accuracy_*` 等属于后验分析或计算特征，单位与缺失编码仍需按各文件生成脚本核对。

- sorts.csv（12 种列名）：`avidity`、`collected_cells`、`collection_fraction`、`concentration`、`frac_matching_seqs`、`non_standard_gate`、`notes`、`num_cells`、`parent_pool`、`pool_name`、`special`、`special_num`。
- pooled_counts.list（39 种列名）：`bc1`、`bc10`、`bc11`、`bc12`、`bc13`、`bc14`、`bc15`、`bc16`、`bc17`、`bc18`、`bc19`、`bc2`、`bc20`、`bc21`、`bc22`、`bc23`、`bc24`、`bc25`、`bc26`、`bc27`、`bc28`、`bc29`、`bc3`、`bc30`、`bc31`、`bc32`、`bc33`、`bc34`、`bc35`、`bc36`、`bc37`、`bc38`、`bc4`、`bc5`、`bc6`、`bc7`、`bc8`、`bc9`、`description`。
- 实验与 SSM 的 .sc（118 种列名）：`0.100_counts`、`0.100_enrich`、`0.400_counts`、`0.400_enrich`、`0.500_counts`、`0.500_enrich`、`1.000_counts`、`1.000_enrich`、`1.500_counts`、`1.500_enrich`、`10.000_counts`、`10.000_enrich`、`100.000_counts`、`100.000_enrich`、`1000.000_counts`、`1000.000_enrich`、`2.000_counts`、`2.000_enrich`、`20.000_counts`、`20.000_enrich`、`200.000_counts`、`200.000_enrich`、`3000.000_counts`、`3000.000_enrich`、`40.000_counts`、`40.000_enrich`、`50.000_counts`、`50.000_enrich`、`70.000_counts`、`70.000_enrich`、`8.000_counts`、`8.000_enrich`、`accuracy_is_interface_boundary`、`accuracy_is_interface_core`、`accuracy_is_monomer_boundary`、`accuracy_is_monomer_core`、`accuracy_is_monomer_surface`、`avid_doesnt_agree`、`avid_lb`、`avid_ub`、`binder_4000_nm`、`binder_400_nm`、`binder_800_nm`、`by_vector`、`chosen_counts`、`chosen_enrich`、`chosen_ratio`、`contiguous_super_rmsd`、`cut_mode`、`ddg`、`ddg_no_repack`、`delta_chosen_enrich`、`delta_ddg_no_repack`、`delta_exp_ddg_center`、`delta_exp_ddg_lb`、`delta_exp_ddg_ub`、`delta_kd_center`、`delta_kd_lb`、`delta_kd_ub`、`delta_pfold_ddg_lb`、`delta_pfold_ddg_ub`、`delta_rosetta_lb`、`delta_rosetta_ub`、`delta_total_score`、`delta_total_score_monomer`、`delta_total_score_target`、`depth`、`depth_monomer`、`description`、`dg_fold`、`dg_fold_lb`、`dg_fold_ub`、`dock`、`entropy`、`entropy_is_interface_boundary`、`entropy_is_interface_core`、`entropy_is_monomer_boundary`、`entropy_is_monomer_core`、`entropy_is_monomer_surface`、`final_combined_score`、`final_entropy_score`、`final_rosetta_accuracy_score`、`highest_conc`、`index`、`is_interface_boundary`、`is_interface_core`、`is_loop`、`is_monomer_boundary`、`is_monomer_core`、`is_monomer_surface`、`kd_center`、`kd_lb`、`kd_ub`、`low_conf`、`lowest_conc`、`mut`、`native`、`p_entropy`、`p_letter`、`p_rosetta`、`p_total`、`parent_kd`、`parent_letter`、`rosetta_agrees`、`sc_neighbors`、`sc_sasa`、`scaff_type`、`score`、`special`、`ssm_letter`、`ssm_parent`、`ssm_seqpos`、`target`、`target_super_rmsd`、`time`、`total_score`、`total_score_monomer`、`total_score_target`。
- 计算分析 .sc（9 种列名）：`avg_all`、`contact_molecular_surface`、`ddg`、`ddg_norepack`、`description`、`mismatch_probability`、`protocol`、`score_per_res`、`upweight`。

### 数据示例

| target | description | kd_lb | kd_ub | low_conf |
| --- | --- | --- | --- | --- |
| FGFR2 | Motif0018_bcov_4helix_07809_0001_7670_0001 | 149707.3543091789 | inf | True |
| FGFR2 | mot_H_normal_HHH_eva_0047_000000004_0001_10_18_H_._EHEE_hb1_2317_0001_0002_0001_0001 | 61139.16385219888 | inf | True |

同一个 FGFR2 首行设计对应的真实 AA 是 `SKLLKLLQELTRKGDPSASFVLTLAFLLKEGNPEALKRVLEELEKELKDPELVERIRRILEELLK`。每行是设计在该实验/分析配置中的结果；首行 inf 上界和 True low_conf 不提供一个精确的 KD。CSV 首个 expression sort 是 pool 元数据，不是一个 binder 样本。

## PDB 数据库

审计主文 Methods、结构验证和 Data Availability，采用起始靶点及比较实验参考结构，并采用七个本研究结构。`target`、靶点目录和论文中的构建体名是连接键；同一靶点的多个设计共享参考条目，不能把这些条目视为逐设计实验结构。7RDH、7N3T、7OPB、7SH3 是相应设计复合物；7N1K、7S5B 是游离 binder；7N1J 包含 FGFR4，不能称为 FGFR2 复合物。

获取日期为 2026-09-18。一手入口为 RCSB 的 `https://www.rcsb.org/fasta/entry/<PDB_ID>/download` 与 `https://files.rcsb.org/download/<PDB_ID>.cif.gz`。复用共享缓存时保留其原始 `.cif` 或 `.cif.gz` 字节；缓存未通过身份检查时重新获取。保存完整条目的全部 polymer entities 和完整坐标，不筛链、不拼接变体序列。验证 entry ID、FASTA entity ID、canonical 序列与 mmCIF `_entity_poly.pdbx_seq_one_letter_code_can` 一致，并确认存在原子坐标。

接受 24 个唯一 ID，24 对通过配对检查，48 个已验收文件，共 9.19 MiB（9,631,840 bytes）。按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接的 inventory SHA-256：`f294760ff3e0e0e6b0d67b4a1ed6b3ddfa7081d33b103f9b513f7fa257659a69`。PDB 子任务状态为 `verified`。

2026-09-20 逐条复核 RCSB Data API：这 24 个 ID 的 entry 状态均为 `REL`；wwPDB/RCSB removed holdings 对每个 ID 均无撤回记录。因此当前没有证据表明这 24 个实验/参考锚点中存在 obsolete、superseded 或 withdrawn 条目，也没有可记录的官方撤回原因。这里所说的研究材料缺口，是 UW 作者包没有交付部分早期 docks、fragment-picker 输出和计算中间结构；它不等同于 PDB 数据库撤回。若后续条目状态改变，须记录官方 replacement、撤回日期和原因；官方未给原因时保持“原因未知”，不得推测。

外部条目中的链角色以 entity 描述和 `_entity_poly.pdbx_strand_id` 核对；这里保存全部链。上游表给出的角色链与具体实验序列仍须逐构建体验证，不能用相同 PDB ID 自动推定所有抗体序列或抗原构建体相同。

## 采集过程记录

1. 2026-09-18，阅读 Nature/Europe PMC 同 DOI 主文与 Supplementary Information，从正文解析六个 UW 原作者下载 URL；目录索引返回 403，改为逐对象获取 HEAD 的 bytes、ETag 和 Last-Modified。snapshot 日期来自实验对象，不来自本次日期。
2. 六包合计约 119 GB，其中 PDB 与 silent 全量模型两包约 117 GB。先验收四个较小包，再以 32 MiB 严格 HTTP range 断点续传两个大包；每块核对 ETag、Content-Range 和长度，最终对象核对官方字节数并计算 SHA-256。
3. 原高并发 Python 传输发生 TLS/读取超时，保留有效断点后改用 curl 持久重试。并发数按服务端实际吞吐调整；停止旧进程并确认退出后才切换，不同时写同一断点。
4. 使用 If-Match 和精确 Content-Range 校验恢复范围，保留 gzip 原始传输字节；取得文件独立检查字节数、SHA-256、全部 tar 成员路径/链接与 gzip trailer。按真实 schema 扫描 CSV、空白分隔计数/序列/score 和原生 README，不执行上游设计脚本。
5. 归档已发表 PDF、同 DOI XML、科学补充及报告；原始通用文件名按 2022-03-24 论文日期改为 CaoMinibinders 开头，改名 hash 不变。核对 24 个唯一 PDB 的完整 FASTA/mmCIF，不为每个设计生成参考序列。
6. 将科学口径、已取得字节和缺口写入本说明，工作稿每次修改立即同步 staging；执行固定 Markdownlint。只有全部声明目标通过验收才执行原子发布。
7. 2026-09-22 按最新版字段要求重新清点 27 份 `sorts.csv`、27 份 `pooled_counts.list` 与实验/计算归档中的 89 张 `.sc` 原始列名；补全来源级字段清单并将逐表派生字段语义列为待核问题。本轮重新核对六包文件大小、四个较小归档的 SHA-256 及 24 对 PDB 的完整 inventory SHA-256，均与前次验收一致。两个合计约 109 GiB 的模型归档本轮未重新计算全文件哈希，正文列示的 SHA-256 仍为 2026-09-20 首次完整验收结果。

## 参考文献

- [Nature 主文及数据/补充入口](https://www.nature.com/articles/s41586-022-04654-9)
- [原作者实验归档](https://files.ipd.uw.edu/pub/robust_de_novo_design_minibinders_2021/supplemental_files/experimental_data_and_analysis.tar.gz)
- [7RDH](https://www.rcsb.org/structure/7RDH)、[7N3T](https://www.rcsb.org/structure/7N3T)、[7N1K](https://www.rcsb.org/structure/7N1K)、[7N1J](https://www.rcsb.org/structure/7N1J)、[7S5B](https://www.rcsb.org/structure/7S5B)、[7OPB](https://www.rcsb.org/structure/7OPB)、[7SH3](https://www.rcsb.org/structure/7SH3)
- 其余起始/比较结构保留各 RCSB entry 对应的结构论文；设计与实验引用保留 Cao 2022。

## 其他

### 数据范围和限制

状态为 verified public-package onboarding：六个声明公开归档、论文材料和 24 个外部 PDB full-entry 配对均已验收。作者计算 README 明确省略部分早期 docks、fragment picker 及计算中间结构，因此仍不称为 complete-study acquisition。

### 完整性与验收

| payload | 大小 | SHA-256 |
| --- | --- | --- |
| `robust_de_novo_design_minibinders_2021/computational_protocol_analysis.tar.gz` | 68.74 MiB（72,074,840 bytes） | `7e1742b18018ab45e66bbb2956fa5cffe252a205237fba71fa269706e2074328` |
| `robust_de_novo_design_minibinders_2021/experimental_data_and_analysis.tar.gz` | 233.17 MiB（244,495,464 bytes） | `51f24e4525a3817ec2dfea1657f348a74bffd6366811147dff9c68c5055bb893` |
| `robust_de_novo_design_minibinders_2021/scripts_and_main_pdbs.tar.gz` | 62.45 MiB（65,485,326 bytes） | `207e31caabf1e78f9ef4bb74d2fce33fcaa661dfe8ad5e1699454b4c09fb56ab` |
| `robust_de_novo_design_minibinders_2021/scaffolds.tar.gz` | 1.21 GiB（1,294,241,263 bytes） | `68721a03c7a8ebfb8854495b58345a1208d189cefe2d18ddd8f2aeb66d1936bb` |
| `robust_de_novo_design_minibinders_2021/design_models_pdb.tar.gz` | 63.48 GiB（68,158,803,587 bytes） | `c66c1bbb80438a3af8d698128528fbf72b85479b395e1c18bafaf599a6ce49ce` |
| `robust_de_novo_design_minibinders_2021/design_models_silent.tar.gz` | 45.75 GiB（49,122,166,125 bytes） | `871e6557ccebb057ed11edd6758675179afba9b7a1b44eb83df96e4bae647bbd` |

已取得 payload 共 6 个、110.79 GiB（118,957,266,605 bytes）；排序拼接的 inventory SHA-256：`4862527922df43f3d022c53f2b32e2f709bc75b0bc3614cabf31899e8e6dd050`。上游未给出 checksum 的交付只将 SHA-256 作为本次字节身份，不能称为官方校验和。归档按成员检查重复/逃逸路径、链接和膨胀范围，逐个读取正规成员；ZIP 校验 CRC，gzip 校验尾部。表格按原始 encoding、header 和列宽检查，保留所有原值。

### 许可和再分发边界

主文文本及注明适用的出版方补充为 CC BY 4.0。该许可覆盖文章内容，不自动覆盖 UW 另行托管的六个下载归档。

2026-09-20 逐包复核许可证文件：六个声明归档没有提供一个覆盖整包的顶层 `LICENSE`、`LICENCE`、`COPYING` 或 `NOTICE`；四个包含分析、脚本和 scaffold 的归档只在 README 中说明用途与运行方法，没有给出统一数据或代码许可证。两个大型 PDB/silent 模型包同样没有可据以把模型重新标为 CC BY 4.0 的授权证据。因此这里存在明确的许可层级差异：论文为 CC BY 4.0，UW 数据包的整体再分发、修改和商用权限未由同一许可证统一授予。不得把论文许可扩展到整包，也不得把“公开可下载”解释为“可任意再许可”。

交付 README 和脚本直接调用 Rosetta `beta_nov16`。RosettaCommons 当前官方源码许可证名为 `Rosetta Software Non-Commercial License Agreement`：非商业用户仅可在其条件下使用，商业用途需要另行取得 University of Washington CoMotion 许可；Rosetta 官方同时声明其源码公开不等于 OSI 意义的开源。R31 包没有附带 `beta_nov16` 当时适用的 Rosetta 许可证文本，因此当前许可证只能证明现行 Rosetta 使用边界，不能反向断言历史构建所适用的条款版本完全相同。无论如何，下载 R31 数据不授予 Rosetta 软件本身的商用权。

UW 交付中的其他第三方代码和模型仍按各自权利说明处理；没有随包许可证时按权利未明确记录，不自行推定 MIT、BSD 或 CC BY。PDB 外部条目依 wwPDB/RCSB 数据政策。

### 公开范围对照

| 论文或来源声称的内容 | 实际公开文件证据 | 状态 |
| --- | --- | --- |
| NGS 筛选与 SC50 | 序列/计数/sort 元数据及区间 score | 核心公开处理材料已取得 |
| 全量模型 PDB/silent | 两个声明的大归档均完成逐成员验收 | 公开包已取得；不是实验晶体结构 |
| 全部早期计算中间结构 | 作者计算 README 明确部分省略 | 研究层不完整 |
| 大量设计都有直接 KD | 主要是 SC50 proxy；少数 BLI | 不能宣称 |
| 本研究及参考实验结构 | 24 个 full-entry 配对 | 已核验；非逐设计覆盖 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-22；待权利方说明）：六个 UW 数据归档没有覆盖整包的数据或代码许可证，历史 Rosetta `beta_nov16` 构建的适用条款也未随包保存。已逐包核对授权文件并区分论文 CC BY 4.0 与数据包、第三方软件；当前仅作可追溯内部核验。商业训练、再分发模型文件或运行旧版 Rosetta 前，下一步分别向 UW 数据权利方及 Rosetta 授权方确认范围与版本。
- `Q02`（最近更新：2026-09-22；待来源方说明）：`binder_4000_nm`、`binder_400_nm` 的列名与上游 README 的阈值描述存在差异。已保留原始列名和说明，不据此改写标签。下一步核对生成这些列的具体脚本及阈值参数；若仍无法消歧，再向作者确认实际浓度与判定规则。
- `Q03`（最近更新：2026-09-22；逐表字段核验未完成）：已从实验与计算归档清点 `sorts.csv`、`pooled_counts.list` 和 89 张 `.sc` 的原始列名，但 SSM、图用计算 score 的每个派生字段尚未逐文件追溯到生成脚本、单位与缺失编码。当前只将 `kd_lb`/`kd_ub` 等明确的区间标签用于来源级描述，其他计算列不能直接当实验亲和力。下一步对拟进入建模的数据表建立逐列来源对照，再决定是否将后验特征纳入 processed 层。
