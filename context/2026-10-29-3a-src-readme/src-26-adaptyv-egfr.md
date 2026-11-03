---
- tags:
  - context
---

# SRC_R26_ADAPTYV_EGFR 数据说明

## 数据集身份

- `source_id`：`SRC_R26_ADAPTYV_EGFR`
- `source_version`：`snapshot-2025-03-18`
- 原作者或发布机构：Adaptyv Bio；Round 2 联合 Polaris / Dimension

## 实验设计和数据口径

两轮竞赛接受针对 EGFR 的设计（含抗体及其他结合蛋白），反向翻译/优化 DNA，cell-free 表达，随后 BLI 多浓度测量和 1:1 全局拟合，汇总重复与候选。Round 1 在 25°C、PBS-T/0.02% BSA 中使用约 316.2–10 nM 抗原；Round 2 在 25°C、HBS-T/0.5% BSA 中使用 1000–10 nM 抗原；这些条件以各自原 README 为准。预测 PAE、pLDDT、ipTM、ESM PLL 和相似度不属于实验结合标签。

Round 1 summary 202 行、replicate 461 行，summary 194 个 KD 缺失；Round 2 summary 402 行、replicate 953 行，summary 347 个 KD 缺失。这些包含对照和重复，不能当 202+402 个独立抗体。Round 2 binding=true/false/unknown 为 55/325/22，缺失与 unknown 不改写为不结合。KD 表保留原数字（如对照为 6.6e-9）；summary 的 kd/kon/koff 列名未写单位，官方 README 仅明确抗原浓度为 nM，故不将 summary 自动换算成 nM 或声称其单位已由明确字段核验。kon/koff 保留拟合来源和失败/置信度信息。neutralisation coefficient 是竞争抑制比例，不等于 KD。两轮共享对照、提交人和重复必须分组。

## 论文原文

### Round 1 官方实验方法

- 标题：EGFR Protein Design Competition Round 1: official README methods
- 作者：Adaptyv Bio
- 载体与版本：GitHub 官方方法文档，commit 37a164244ca6822d73db87bb2135af062b40f9d5
- 发布日期：2024-12-12
- DOI：无；官方方法文档未给出关联 DOI
- PMID / PMCID：无 / 无
- 本地文件：`articles/EGFR-R1_2024-12-12_GitHub-37a164244ca6.md`
- 文件大小：EGFR-R1_2024-12-12_GitHub-37a164244ca6.md：6964 bytes
- SHA-256：EGFR-R1_2024-12-12_GitHub-37a164244ca6.md：`daa5132a9603ddbe5161c1dc83a14c24e67e5451b999217019ca7f54f86be738`
- 文本许可：Apache 2.0 code / ODbL data per repository LICENSE.md
- 补充材料：无其他独立补充文件。

### Round 2 官方实验方法

- 标题：EGFR Protein Design Competition Round 2: official README methods
- 作者：Adaptyv Bio
- 载体与版本：GitHub 官方方法文档，commit fc91b91ddc367830b755b215dbc69669675ad6a0
- 发布日期：2025-03-18
- DOI：无；官方方法文档未给出关联 DOI
- PMID / PMCID：无 / 无
- 本地文件：`articles/EGFR-R2_2025-03-18_GitHub-fc91b91ddc36.md`
- 文件大小：EGFR-R2_2025-03-18_GitHub-fc91b91ddc36.md：9807 bytes
- SHA-256：EGFR-R2_2025-03-18_GitHub-fc91b91ddc36.md：`5db5081846f8c60d2c9273e597a7272b6856a84311f5dc727198e8e67a0e3aa4`
- 文本许可：Apache 2.0 code / ODbL data per repository LICENSE.md
- 补充材料：无其他独立补充文件。

未识别到关联期刊主文；本节保存官方方法文档，不将其称为论文。

## 仓库内容

- 一手入口：<https://github.com/adaptyvbio/egfr_competition_1>；commit `37a164244ca6822d73db87bb2135af062b40f9d5`，tree `2d74638ec9f775f0309d563a3ac1b8534414b1f4`；上游日期 2024-12-12。
- 一手入口：<https://github.com/adaptyvbio/egfr_competition_2>；commit `fc91b91ddc367830b755b215dbc69669675ad6a0`，tree `65bbf9df1f6de5647b28f59597ed9420633ae0f3`；上游日期 2025-03-18。

两个固定 Git tree 和 README 给出的公开交付对象；两轮取样、对照、汇总和预测模型分别保留。source_version 取组合快照中最新 commit 日期 2025-03-18，而非下载日期。

快照日期来自已固定 commit `fc91b91ddc367830b755b215dbc69669675ad6a0` 的 committer 日期 2025-03-18；不是下载日期。原交付归档保持压缩格式，验收时读取所有成员，不在 raw 中重新生成数据表。

```text
snapshot-2025-03-18/
  egfr_competition_1/
    egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5.tar.gz
    docking_predictions.zip
    package.zip
  egfr_competition_2/
    egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0.tar.gz
    package.zip
    package_neutralisation.zip
    embeddings.zip
    structure_predictions.zip
```

Git 快照全部 blob 与固定 commit tree 校验；37a164244ca6822d73db87bb2135af062b40f9d5：11 个 blob，LFS 0，submodule 0；fc91b91ddc367830b755b215dbc69669675ad6a0：9 个 blob，LFS 0，submodule 0。

| 对象 | Last-Modified | ETag |
| --- | --- | --- |
| egfr_competition_2/package.zip | Fri, 13 Dec 2024 19:07:34 GMT | "7ac411fcca6afd4e1e271a5033ed422f-11" |
| egfr_competition_2/package_neutralisation.zip | Tue, 18 Mar 2025 10:57:59 GMT | "dce71bdac6d9f38cafd64889d0883b5a-2" |
| egfr_competition_1/docking_predictions.zip | Tue, 01 Oct 2024 10:14:54 GMT | "af1bc7d753ffb05d6e91af75f1cd7e1f-5" |
| egfr_competition_2/embeddings.zip | Thu, 12 Dec 2024 17:04:13 GMT | "cd82593fdfdaee34342b02dadf7dd64e" |
| egfr_competition_2/structure_predictions.zip | Fri, 13 Dec 2024 00:29:00 GMT | "7ce1cf9ffe6bc0db3f6675ae9c4492b9-5" |
| egfr_competition_1/package.zip | Wed, 25 Sep 2024 18:34:50 GMT | "9726369d681bd410b43fe1360caa672d-11" |

ETag 用于身份条件请求，不把 multipart ETag 当文件 MD5；本地 SHA-256 见验收。

## 数据结构

### 原始交付与记录粒度

两个固定 Git 包保存 results 汇总、replicate 及计算指标；README 指向的 package.zip、neutralisation、embeddings 和 predicted structures 等外部对象单独按原名保存。多表用原始 name/replicate 等键连接，不按同名跨轮盲目合并。FoldSeek 结果中的 PDB ID 是相似性命中，不能当该候选的实际结构。 独立验收读取 6001 个原始表、13710063 个非空数据行，其中 Round 1 package 为 2107 条曲线、4360469 个采样点，Round 2 package 为 3815 条曲线、9218891 个采样点，neutralisation package 为 57 条曲线、119497 个采样点及 57 行 reading_data 元数据。这些采样点不是独立设计，预测指标与 embeddings 的多表也不能和 summary 相加。README 对同一归档内同字段表汇总行数并显示首表路径，原包未合并或改写；不同预测状态仍用原成员名区分。

| 原始表或 sheet | 非空数据行 | 列数 |
| --- | --- | --- |
| `egfr_competition_1/egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5.tar.gz!egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5/results/docking_predictions/predicted_binding_metrics.xlsx#Experiments` | 212 | 37 |
| `egfr_competition_1/egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5.tar.gz!egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5/results/docking_predictions/predicted_binding_metrics.xlsx#Candidates` | 200 | 8 |
| `egfr_competition_1/egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5.tar.gz!egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5/results/docking_predictions/predicted_binding_metrics.xlsx#Targets` | 1 | 4 |
| `egfr_competition_1/egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5.tar.gz!egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5/results/replicate_summary.csv` | 461 | 9 |
| `egfr_competition_1/egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5.tar.gz!egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5/results/result_summary.csv` | 202 | 11 |
| `egfr_competition_1/egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5.tar.gz!egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5/results/sequence_similarity.csv` | 74 | 9 |
| `egfr_competition_2/egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0.tar.gz!2 个同字段表；首表 egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0/results/destress_binder_only.csv` | 800 | 70 |
| `egfr_competition_2/egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0.tar.gz!egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0/results/foldseek_results.tsv` | 393 | 37 |
| `egfr_competition_2/egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0.tar.gz!egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0/results/replicate_summary.csv` | 953 | 8 |
| `egfr_competition_2/egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0.tar.gz!egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0/results/result_summary.csv` | 402 | 14 |
| `egfr_competition_2/egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0.tar.gz!egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0/results/sequence_similarity.csv` | 252 | 11 |
| `egfr_competition_2/package.zip!3815 个同字段表；首表 package/raw_data/ccalia.Paesani_Lab_design1_2_1000.0.csv` | 9218891 | 2 |
| `egfr_competition_2/package_neutralisation.zip!57 个同字段表；首表 package/raw_data/aureliabustos.wwt_noised_I_scaffold_shorted_var6640_1_100.0.csv` | 119497 | 2 |
| `egfr_competition_2/package_neutralisation.zip!package/raw_data/reading_data.csv` | 57 | 5 |
| `egfr_competition_1/docking_predictions.zip!docking_predictions/predicted_binding_metrics.xlsx#Experiments` | 212 | 37 |
| `egfr_competition_1/docking_predictions.zip!docking_predictions/predicted_binding_metrics.xlsx#Candidates` | 200 | 8 |
| `egfr_competition_1/docking_predictions.zip!docking_predictions/predicted_binding_metrics.xlsx#Targets` | 1 | 4 |
| `egfr_competition_2/embeddings.zip!esm2_650m.csv` | 1131 | 1281 |
| `egfr_competition_2/embeddings.zip!esmc_600m.csv` | 1131 | 1153 |
| `egfr_competition_2/embeddings.zip!saprot.csv` | 1131 | 481 |
| `egfr_competition_2/embeddings.zip!protrek.csv` | 1131 | 2049 |
| `egfr_competition_2/embeddings.zip!esm2_15b.csv` | 1131 | 5121 |
| `egfr_competition_2/embeddings.zip!esm2_3b.csv` | 1131 | 2561 |
| `egfr_competition_1/package.zip!2107 个同字段表；首表 package/raw_data/adrian.tripp-egfr_cetuxi_0133_0002_A_4_31.6.csv` | 4360469 | 2 |

表行数包含重复条件、示例和派生副本，不求和作为独立生物对象。下表列名保持原始拼写；空表头以 `（空列名）` 标出，未修改文件。

### 字段说明

name/sequence_name：候选/样本标识；username：提交者；sequence/dna：设计与优化 DNA；replicate：重复编号；kd/kon/koff：BLI 拟合数值或缺失，KD/koff 较小常有利、kon 需结合模型；binding/binding_strength/confidence/expression/nc_adjusted_expression：实验分类与表达/置信度，unknown 保留；pae_interaction/plddt/iptm/esm_pll/similarity_check：预测或检索指标；neutralisation 系数：独立竞争 readout。 Round 1 原始曲线字段 Time (s)/Shift (nm) 明确表示秒和 nm；Round 2 / neutralisation 原始曲线 t/y 的列名本身没有时间/响应单位；文件名包含样本、重复和浓度编码，按各轮官方方法解释浓度 nM，不把一条曲线的采样点当独立结合蛋白。

| 原始表或 sheet | 字段（原始顺序） | 原始表示与特殊值 |
| --- | --- | --- |
| `egfr_competition_1/egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5.tar.gz!egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5/results/docking_predictions/predicted_binding_metrics.xlsx#Experiments` | `experiment_id`, `candidate_id`, `target_id`, `experiment_type`, `submitted`, `complete`, `best_model_path`, `bsa_best`, `bsa_max`, `bsa_mean`, `bsa_min`, `bsa_std`, `desolv_best`, `desolv_max`, `desolv_mean`, `desolv_min`, `desolv_std`, `elec_best`, `elec_max`, `elec_mean`, `elec_min`, `elec_std`, `composite_score_best`, `composite_score_max`, `composite_score_mean`, `composite_score_min`, `composite_score_std`, `total_best`, `total_max`, `total_mean`, `total_min`, `total_std`, `vdw_best`, `vdw_max`, `vdw_mean`, `vdw_min`, `vdw_std` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：best_model_path=8, bsa_best=8, bsa_max=8, bsa_mean=8, bsa_min=8, bsa_std=8, desolv_best=8, desolv_max=8, desolv_mean=8, desolv_min=8, desolv_std=8, elec_best=8, elec_max=8, elec_mean=8, elec_min=8, elec_std=8, composite_score_best=8, composite_score_max=8, composite_score_mean=8, composite_score_min=8, composite_score_std=8, total_best=8, total_max=8, total_mean=8, total_min=8, total_std=8, vdw_best=8, vdw_max=8, vdw_mean=8, vdw_min=8, vdw_std=8 |
| `egfr_competition_1/egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5.tar.gz!egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5/results/docking_predictions/predicted_binding_metrics.xlsx#Candidates` | `candidate_id`, `candidate_seq_len`, `candidate_sequence`, `candidate_fasta_line`, `candidate_folded`, `candidate_pdb_path`, `candidate_active_residues`, `candidate_active_residue_selection` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `egfr_competition_1/egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5.tar.gz!egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5/results/docking_predictions/predicted_binding_metrics.xlsx#Targets` | `target_id`, `target_pdb_path`, `target_active_residues`, `target_active_residue_selection` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `egfr_competition_1/egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5.tar.gz!egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5/results/replicate_summary.csv` | `name`, `replicate`, `kd`, `kon`, `koff`, `binding`, `confidence`, `expression`, `nc_adjusted_expression` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：kd=443, kon=452, koff=452 |
| `egfr_competition_1/egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5.tar.gz!egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5/results/result_summary.csv` | `name`, `username`, `sequence_name`, `kd`, `sequence`, `dna`, `plddt`, `pae_interaction`, `similarity_check`, `model_names`, `methods` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：username=1, sequence_name=1, plddt=1, pae_interaction=1, similarity_check=128, model_names=1, methods=1, kd=194 |
| `egfr_competition_1/egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5.tar.gz!egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5/results/sequence_similarity.csv` | `id`, `db_id`, `identity`, `alignment_length`, `num_mismatches`, `query_coverage`, `target_coverage`, `db`, `similarity_check` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `egfr_competition_2/egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0.tar.gz!2 个同字段表；首表 egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0/results/destress_binder_only.csv` | `design_name`, `file_name`, `full_sequence`, `dssp_assignment`, `composition_ALA`, `composition_CYS`, `composition_ASP`, `composition_GLU`, `composition_PHE`, `composition_GLY`, `composition_HIS`, `composition_ILE`, `composition_LYS`, `composition_LEU`, `composition_MET`, `composition_ASN`, `composition_PRO`, `composition_GLN`, `composition_ARG`, `composition_SER`, `composition_THR`, `composition_VAL`, `composition_TRP`, `composition_UNK`, `composition_TYR`, `ss_prop_alpha_helix`, `ss_prop_beta_bridge`, `ss_prop_beta_strand`, `ss_prop_3_10_helix`, `ss_prop_pi_helix`, `ss_prop_hbonded_turn`, `ss_prop_bend`, `ss_prop_loop`, `isoelectric_point`, `charge`, `mass`, `num_residues`, `packing_density`, `aggrescan3d_avg_value`, `aggrescan3d_min_value`, `aggrescan3d_max_value`, `hydrophobic_fitness_per_aa`, `budeff_total_per_aa`, `budeff_steric_per_aa`, `budeff_desolvation_per_aa`, `budeff_charge_per_aa`, `evoef2_total_per_aa`, `evoef2_ref_total_per_aa`, `evoef2_intraR_total_per_aa`, `evoef2_interS_total_per_aa`, `evoef2_interD_total_per_aa`, `rosetta_total_per_aa`, `rosetta_fa_atr_per_aa`, `rosetta_fa_rep_per_aa`, `rosetta_fa_intra_rep_per_aa`, `rosetta_fa_elec_per_aa`, `rosetta_fa_sol_per_aa`, `rosetta_lk_ball_wtd_per_aa`, `rosetta_fa_intra_sol_xover4_per_aa`, `rosetta_hbond_lr_bb_per_aa`, `rosetta_hbond_sr_bb_per_aa`, `rosetta_hbond_bb_sc_per_aa`, `rosetta_hbond_sc_per_aa`, `rosetta_dslf_fa13_per_aa`, `rosetta_rama_prepro_per_aa`, `rosetta_p_aa_pp_per_aa`, `rosetta_fa_dun_per_aa`, `rosetta_omega_per_aa`, `rosetta_pro_close_per_aa`, `rosetta_yhh_planarity_per_aa` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：aggrescan3d_avg_value=1, aggrescan3d_min_value=1, aggrescan3d_max_value=1, evoef2_total_per_aa=1, rosetta_total_per_aa=1, rosetta_fa_atr_per_aa=1, rosetta_fa_rep_per_aa=1, rosetta_fa_intra_rep_per_aa=1, rosetta_fa_elec_per_aa=1, rosetta_fa_sol_per_aa=1, rosetta_lk_ball_wtd_per_aa=1, rosetta_fa_intra_sol_xover4_per_aa=1, rosetta_hbond_lr_bb_per_aa=1, rosetta_hbond_sr_bb_per_aa=1, rosetta_hbond_bb_sc_per_aa=1, rosetta_hbond_sc_per_aa=1, rosetta_dslf_fa13_per_aa=1, rosetta_rama_prepro_per_aa=1, rosetta_p_aa_pp_per_aa=1, rosetta_fa_dun_per_aa=1, rosetta_omega_per_aa=1, rosetta_pro_close_per_aa=1, rosetta_yhh_planarity_per_aa=1 |
| `egfr_competition_2/egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0.tar.gz!egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0/results/foldseek_results.tsv` | `common_id`, `query_swissprot`, `target_swissprot`, `fident_swissprot`, `alnlen_swissprot`, `mismatch_swissprot`, `gapopen_swissprot`, `qstart_swissprot`, `qend_swissprot`, `tstart_swissprot`, `tend_swissprot`, `evalue_swissprot`, `bits_swissprot`, `alntmscore_swissprot`, `qtmscore_swissprot`, `ttmscore_swissprot`, `lddt_swissprot`, `lddtfull_swissprot`, `prob_swissprot`, `query_pdb`, `target_pdb`, `fident_pdb`, `alnlen_pdb`, `mismatch_pdb`, `gapopen_pdb`, `qstart_pdb`, `qend_pdb`, `tstart_pdb`, `tend_pdb`, `evalue_pdb`, `bits_pdb`, `alntmscore_pdb`, `qtmscore_pdb`, `ttmscore_pdb`, `lddt_pdb`, `lddtfull_pdb`, `prob_pdb` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `egfr_competition_2/egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0.tar.gz!egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0/results/replicate_summary.csv` | `name`, `replicate`, `kd`, `kon`, `koff`, `binding_strength`, `binding`, `expression` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：kon=843, koff=843, kd=823 |
| `egfr_competition_2/egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0.tar.gz!egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0/results/result_summary.csv` | `username`, `name`, `kd`, `binding_strength`, `binding`, `expression`, `sequence`, `dna`, `pae_interaction`, `esm_pll`, `iptm`, `plddt`, `similarity_check`, `design_models` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：username=2, pae_interaction=2, esm_pll=2, iptm=2, plddt=2, similarity_check=150, design_models=15, kd=347 |
| `egfr_competition_2/egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0.tar.gz!egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0/results/sequence_similarity.csv` | `id`, `db_id`, `identity`, `alignment_length`, `query_length`, `num_mismatches`, `query_coverage`, `target_coverage`, `db`, `similarity_check`, `distance` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `egfr_competition_2/package.zip!3815 个同字段表；首表 package/raw_data/ccalia.Paesani_Lab_design1_2_1000.0.csv` | `t`, `y` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `egfr_competition_2/package_neutralisation.zip!57 个同字段表；首表 package/raw_data/aureliabustos.wwt_noised_I_scaffold_shorted_var6640_1_100.0.csv` | `t`, `y` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `egfr_competition_2/package_neutralisation.zip!package/raw_data/reading_data.csv` | `sample`, `replicate`, `concentration`, `run_id`, `loading` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `egfr_competition_1/docking_predictions.zip!docking_predictions/predicted_binding_metrics.xlsx#Experiments` | `experiment_id`, `candidate_id`, `target_id`, `experiment_type`, `submitted`, `complete`, `best_model_path`, `bsa_best`, `bsa_max`, `bsa_mean`, `bsa_min`, `bsa_std`, `desolv_best`, `desolv_max`, `desolv_mean`, `desolv_min`, `desolv_std`, `elec_best`, `elec_max`, `elec_mean`, `elec_min`, `elec_std`, `composite_score_best`, `composite_score_max`, `composite_score_mean`, `composite_score_min`, `composite_score_std`, `total_best`, `total_max`, `total_mean`, `total_min`, `total_std`, `vdw_best`, `vdw_max`, `vdw_mean`, `vdw_min`, `vdw_std` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：best_model_path=8, bsa_best=8, bsa_max=8, bsa_mean=8, bsa_min=8, bsa_std=8, desolv_best=8, desolv_max=8, desolv_mean=8, desolv_min=8, desolv_std=8, elec_best=8, elec_max=8, elec_mean=8, elec_min=8, elec_std=8, composite_score_best=8, composite_score_max=8, composite_score_mean=8, composite_score_min=8, composite_score_std=8, total_best=8, total_max=8, total_mean=8, total_min=8, total_std=8, vdw_best=8, vdw_max=8, vdw_mean=8, vdw_min=8, vdw_std=8 |
| `egfr_competition_1/docking_predictions.zip!docking_predictions/predicted_binding_metrics.xlsx#Candidates` | `candidate_id`, `candidate_seq_len`, `candidate_sequence`, `candidate_fasta_line`, `candidate_folded`, `candidate_pdb_path`, `candidate_active_residues`, `candidate_active_residue_selection` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `egfr_competition_1/docking_predictions.zip!docking_predictions/predicted_binding_metrics.xlsx#Targets` | `target_id`, `target_pdb_path`, `target_active_residues`, `target_active_residue_selection` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `egfr_competition_2/embeddings.zip!esm2_650m.csv` | `sequence`, `esm2_650m_dim_1`, `esm2_650m_dim_2`, `esm2_650m_dim_3`, `esm2_650m_dim_4`, `esm2_650m_dim_5`, `esm2_650m_dim_6`, `esm2_650m_dim_7`, `esm2_650m_dim_8`, `esm2_650m_dim_9`, `esm2_650m_dim_10`, `esm2_650m_dim_11`, `esm2_650m_dim_12`, `esm2_650m_dim_13`, `esm2_650m_dim_14`, `esm2_650m_dim_15`, `esm2_650m_dim_16`, `esm2_650m_dim_17`, `esm2_650m_dim_18`, `esm2_650m_dim_19`, `esm2_650m_dim_20`, `esm2_650m_dim_21`, `esm2_650m_dim_22`, `es …（本行余下约 26654 字符是逐维度列名枚举，汇总文件中省略；完整内容见原 README）|
| `egfr_competition_2/embeddings.zip!esmc_600m.csv` | `sequence`, `esmc_600m_dim_1`, `esmc_600m_dim_2`, `esmc_600m_dim_3`, `esmc_600m_dim_4`, `esmc_600m_dim_5`, `esmc_600m_dim_6`, `esmc_600m_dim_7`, `esmc_600m_dim_8`, `esmc_600m_dim_9`, `esmc_600m_dim_10`, `esmc_600m_dim_11`, `esmc_600m_dim_12`, `esmc_600m_dim_13`, `esmc_600m_dim_14`, `esmc_600m_dim_15`, `esmc_600m_dim_16`, `esmc_600m_dim_17`, `esmc_600m_dim_18`, `esmc_600m_dim_19`, `esmc_600m_dim_20`, `esmc_600m_dim_21`, `esmc_600m_dim_22`, `es …（本行余下约 23838 字符是逐维度列名枚举，汇总文件中省略；完整内容见原 README）|
| `egfr_competition_2/embeddings.zip!saprot.csv` | `sequence`, `saprot_dim_1`, `saprot_dim_2`, `saprot_dim_3`, `saprot_dim_4`, `saprot_dim_5`, `saprot_dim_6`, `saprot_dim_7`, `saprot_dim_8`, `saprot_dim_9`, `saprot_dim_10`, `saprot_dim_11`, `saprot_dim_12`, `saprot_dim_13`, `saprot_dim_14`, `saprot_dim_15`, `saprot_dim_16`, `saprot_dim_17`, `saprot_dim_18`, `saprot_dim_19`, `saprot_dim_20`, `saprot_dim_21`, `saprot_dim_22`, `saprot_dim_23`, `saprot_dim_24`, `saprot_dim_25`, `saprot_dim_26`, `sap …（本行余下约 8130 字符是逐维度列名枚举，汇总文件中省略；完整内容见原 README）|
| `egfr_competition_2/embeddings.zip!protrek.csv` | `sequence`, `protrek_dim_1`, `protrek_dim_2`, `protrek_dim_3`, `protrek_dim_4`, `protrek_dim_5`, `protrek_dim_6`, `protrek_dim_7`, `protrek_dim_8`, `protrek_dim_9`, `protrek_dim_10`, `protrek_dim_11`, `protrek_dim_12`, `protrek_dim_13`, `protrek_dim_14`, `protrek_dim_15`, `protrek_dim_16`, `protrek_dim_17`, `protrek_dim_18`, `protrek_dim_19`, `protrek_dim_20`, `protrek_dim_21`, `protrek_dim_22`, `protrek_dim_23`, `protrek_dim_24`, `protrek_dim_ …（本行余下约 39452 字符是逐维度列名枚举，汇总文件中省略；完整内容见原 README）|
| `egfr_competition_2/embeddings.zip!esm2_15b.csv` | `sequence`, `esm2_15b_dim_1`, `esm2_15b_dim_2`, `esm2_15b_dim_3`, `esm2_15b_dim_4`, `esm2_15b_dim_5`, `esm2_15b_dim_6`, `esm2_15b_dim_7`, `esm2_15b_dim_8`, `esm2_15b_dim_9`, `esm2_15b_dim_10`, `esm2_15b_dim_11`, `esm2_15b_dim_12`, `esm2_15b_dim_13`, `esm2_15b_dim_14`, `esm2_15b_dim_15`, `esm2_15b_dim_16`, `esm2_15b_dim_17`, `esm2_15b_dim_18`, `esm2_15b_dim_19`, `esm2_15b_dim_20`, `esm2_15b_dim_21`, `esm2_15b_dim_22`, `esm2_15b_dim_23`, `esm2_1 …（本行余下约 106013 字符是逐维度列名枚举，汇总文件中省略；完整内容见原 README）|
| `egfr_competition_2/embeddings.zip!esm2_3b.csv` | `sequence`, `esm2_3b_dim_1`, `esm2_3b_dim_2`, `esm2_3b_dim_3`, `esm2_3b_dim_4`, `esm2_3b_dim_5`, `esm2_3b_dim_6`, `esm2_3b_dim_7`, `esm2_3b_dim_8`, `esm2_3b_dim_9`, `esm2_3b_dim_10`, `esm2_3b_dim_11`, `esm2_3b_dim_12`, `esm2_3b_dim_13`, `esm2_3b_dim_14`, `esm2_3b_dim_15`, `esm2_3b_dim_16`, `esm2_3b_dim_17`, `esm2_3b_dim_18`, `esm2_3b_dim_19`, `esm2_3b_dim_20`, `esm2_3b_dim_21`, `esm2_3b_dim_22`, `esm2_3b_dim_23`, `esm2_3b_dim_24`, `esm2_3b_dim_ …（本行余下约 49692 字符是逐维度列名枚举，汇总文件中省略；完整内容见原 README）|
| `egfr_competition_1/package.zip!2107 个同字段表；首表 package/raw_data/adrian.tripp-egfr_cetuxi_0133_0002_A_4_31.6.csv` | `Time (s)`, `Shift (nm)` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |

### 数据示例

来自 `egfr_competition_1/egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5.tar.gz!egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5/results/result_summary.csv` 的第一条真实非空数据行：

| 原始字段 | 原始值 |
| --- | --- |
| name | Cetuximab_scFv |
| username | （空字符串） |
| sequence_name | （空字符串） |
| kd | 6.63834535035629e-09 |
| sequence | QVQLKQSGPGLVQPSQSLSITCTVSGFSLTNYGVHWVRQSPGKGLEWLGVIWSGGNTDYNTPFTSRLSINKDNSKSQVFFKMNSLQSNDTAIYYCARALTYYDYEFAYWGQGTLVTVSAGGGGSGGGGSGGGGSDILLTQSPVILSVSPGERVSFSCRASQSIGTNIHWYQQRTNGSPRLLIKYASESISGIPSRFSGSGSGTDFTLSINSVESEDIADYYCQQNNNWPTTFGAGTKLELK |
| dna | ATGCAGGTGCAGCTGAAACAGAGCGGCCCGGGCCTGGTGCAGCCATCTCAATCTCTGTCTATTACTTGCACTGTTTCTGGCTTTAGCCTGACCAACTATGGCGTGCATTGGGTGCGCCAGAGCCCGGGCAAAGGTCTGGAATGGTTAGGCGTGATTTGGAGCGGCGGCAACACCGATTATAACACCCCGTTTACCAGCCGCCTGAGCATTAACAAAGACAACAGCAAAAGCCAGGTGTTCTTCAAAATGAACAGCCTGCAGAGCAACGATACCGCGATTTATTATTGCGCGCGCGCGCTGACCTATTATGATTATGAATTTGCGTATTGGGGCCAGGGCACCCTGGTGACCGTGAGCGCGGGGGGAGGCGGTTCGGGTGGTGGCGGCTCAGGCGGCGGCGGTAGTGATATTCTGTTAACGCAAAGTCCGGTGATTCTGAGCGTTAGTCCAGGCGAACGCGTGTCTTTTAGCTGCCGCGCATCTCAGTCTATTGGCACCAACATTCATTGGTATCAGCAGCGCACCAACGGCAGCCCGCGCCTGCTGATTAAATATGCGAGCGAAAGCATTAGCGGCATTCCGAGCCGCTTCAGTGGTAGCGGCAGCGGTACCGATTTTACGTTAAGTATCAACAGCGTGGAAAGCGAAGATATTGCGGACTACTACTGCCAGCAGAACAACAACTGGCCGACCACCTTTGGCGCGGGCACCAAACTGGAACTGAAAGGCTCCGCTTGGAGTCATCCACAATTCGAAAAAGGTGGAGGTTCCGGAGGTGGATCGGGAGGTTCTGCCTGGTCTCATCCACAATTTGAGAAGTAACTAGCATCTAGCATAACCCCTCTCTAAACGGAGGGGTTT |
| plddt | （空字符串） |
| pae_interaction | （空字符串） |
| similarity_check | （空字符串） |
| model_names | （空字符串） |
| methods | （空字符串） |

这是该原始表的一条记录；粒度按前述定义，不把结构表示、重复或归档成员当独立抗体。

## PDB 数据库

1YY9 为 EGFR ectodomain / cetuximab Fab 的共享靶点与对照参考复合物；1IVO 为 human EGF / EGFR 对照参考复合物。Round 2 result_summary 的 Human_EGF 对照序列与 1IVO entity 2 canonical sequence 完全相同（53 aa，author chains C/D），EGFR 为 entity 1、author chains A/B。该序列一致不证明测量构建体的全部修饰、状态及靶点都与该结构相同。保留完整 entry，而非每个竞赛设计的实验结构。拒绝将 FoldSeek 最近命中或 AlphaFold 模型当候选的实验 PDB；未发现逐设计已测定坐标。

本次审计接受 2 个唯一锚点，每个都有 RCSB 完整 entry FASTA 与完整 mmCIF（原样 .cif 或 .cif.gz），共 4 个文件 / 467077 bytes。逐对检查 entry ID、非空 _atom_site 及 canonical polymer 序列一致。FASTA 保留 RCSB entity ID、原始头和序列，没有从坐标重建序列；坐标保留完整原文件。author/label chain 与 entity 的原始映射在 FASTA 头及 mmCIF `_struct_asym`、`_entity_poly`、`_atom_site.auth_asym_id` 中，不臆造链角色。

文件路径为 `pdb/sequences/rcsb_pdb_<PDB>.fasta`、`pdb/structures/<PDB>.cif.gz` 或 `<PDB>.cif`；复用已有完整未压缩 RCSB 原文件时不重新压缩。确定性 inventory SHA-256：`bbae0fe61edf5473452920ebd315d4db9bc93fc836c9a2a3a3778d49579312a4`；算法为按相对路径排序，逐文件组成 `path<TAB>bytes<TAB>sha256<LF>`（UTF-8）再计算 SHA-256。

| PDB | FASTA bytes / SHA-256 | mmCIF.gz bytes / SHA-256 |
| --- | --- | --- |
| 1IVO | 814 / `d83dc71e621570f01d4652db1d39abbeda63c73ce0befe68140e7b3ce8894aed` | 242336 / `01ae9b0d1d000f1e444e6fc8f190d746fa9716fb75fe511a60a2025b7396fd11` |
| 1YY9 | 1272 / `a5725ad46c8c2123cec864dcfa2369abd87403dc24bc316a604ace0d7a5dfe7f` | 222655 / `9a12e1b29235697c0035ad072ab6b9497c97f23fed97973870eccbae32da01ee` |

## 使用方式

由调用者将 `dataset_root` 赋为该 source_version 目录。以下仅读原始入口，不清洗、换算或修补 raw。

```python
import tarfile
with tarfile.open(dataset_root / "egfr_competition_1/egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5.tar.gz") as archive:
    print(archive.getnames()[:5])
```

## 采集过程记录

2026-09-18：固定两轮各自的 Git commit，并取得 README 指向的六个外部对象，合计八个 payload。初次批量执行遇到 staging 写锁冲突；确认原进程结束后恢复，外部包继续保留有效范围。独立读取 6,001 个表，区分设计 summary、replicate 和曲线采样点。官方 Git README 原字节另归档为 methods；没有捏造关联期刊论文。1IVO、1YY9 只作为对照/靶点参考。

2026-09-18：全部正式 payload 按来源身份、大小和官方/本地 checksum 独立验收；原始表与附件已读取，FASTA 和完整 mmCIF 逐对核验。工作 README 同步共享版本，规定的 markdownlint 为零错误后发布。具体 API、原始下载日志、失败和重试记录保存在共享本批采集目录，未向任何作者发送消息或申请。

2026-09-18：复核 skill 版本规则，核实并保留 `snapshot-2025-03-18`，补充一手版本命名依据。同步来源配置、PDB 配置、工作与共享 README 及当前结构化验收/发布记录；旧文档和原验收记录保留在 runs 的 version-migration-history。修订前后按相对路径、字节数和 SHA-256 比对全部科学文件，内容保持原样；修订 README 使用规定的 markdownlint 配置验收。

2026-09-18：README 工作稿迁入由 developer.user 定位的个人 docs/readme。初版采集记录混用了跨来源的通用描述，本次按实际来源、下载与重试记录修订。论文及附件命名补齐平台和版本。以下名称变更均核对原文件字节数及 SHA-256，内容未改写；原始文件名与下载 URL 保留在采集记录中。

- `articles/egfr_competition_1_official_methods.md` → `articles/EGFR-R1_2024-12-12_GitHub-37a164244ca6.md`；6964 bytes，SHA-256 `daa5132a9603ddbe5161c1dc83a14c24e67e5451b999217019ca7f54f86be738`。
- `articles/egfr_competition_2_official_methods.md` → `articles/EGFR-R2_2025-03-18_GitHub-fc91b91ddc36.md`；9807 bytes，SHA-256 `5db5081846f8c60d2c9273e597a7272b6856a84311f5dc727198e8e67a0e3aa4`。

旧文档和结构化报告保存在共享 runs/documentation-reorganization；修订后本地与共享 README 同步并执行规定的 Markdownlint。

- 上游原始名称 `README.md (fixed Git tree)`；入口 <https://codeload.github.com/adaptyvbio/egfr_competition_1/tar.gz/37a164244ca6822d73db87bb2135af062b40f9d5>。
- 上游原始名称 `README.md (fixed Git tree)`；入口 <https://codeload.github.com/adaptyvbio/egfr_competition_2/tar.gz/fc91b91ddc367830b755b215dbc69669675ad6a0>。

## 参考文献

- [数据源固定版本/入口](https://github.com/adaptyvbio/egfr_competition_1)
- [数据源固定版本/入口](https://github.com/adaptyvbio/egfr_competition_2)
- [primary official methods documentation](https://codeload.github.com/adaptyvbio/egfr_competition_1/tar.gz/37a164244ca6822d73db87bb2135af062b40f9d5)
- [primary official methods documentation](https://codeload.github.com/adaptyvbio/egfr_competition_2/tar.gz/fc91b91ddc367830b755b215dbc69669675ad6a0)
- [PDB 1IVO（条目含原始结构论文）](https://www.rcsb.org/structure/1IVO)
- [PDB 1YY9（条目含原始结构论文）](https://www.rcsb.org/structure/1YY9)

## 其他

### 完整性与验收

| payload | bytes | SHA-256 |
| --- | --- | --- |
| `egfr_competition_1/egfr_competition_1-37a164244ca6822d73db87bb2135af062b40f9d5.tar.gz` | 5588674 | `a8a7f3ea52cb0228d480ab0665cc2b7da88999ce8bc5b18d1cf1e23ba09fc5a1` |
| `egfr_competition_2/egfr_competition_2-fc91b91ddc367830b755b215dbc69669675ad6a0.tar.gz` | 1237450 | `7bd50f1d2111373e4e939f2dd4ad202e9a47f5d467061f18ea3f1e3aa3bfd960` |
| `egfr_competition_2/package.zip` | 405521893 | `cf88a6548eeafd4a3c5b4d095b46a6ab0343c90eda3f961b2d1ac7851070630a` |
| `egfr_competition_2/package_neutralisation.zip` | 10919209 | `1c87dc13f7b423e65dd1d30eae9d2179c65b4d8f7555539bef64eaad2b4ecd2f` |
| `egfr_competition_1/docking_predictions.zip` | 30154461 | `407e1d8ff17c2fccde44b21ffe7b2bca63542b1f8ca2aa6962a67e1409761443` |
| `egfr_competition_2/embeddings.zip` | 69654339 | `0ed257b3493c6b1f205277367a2f01ef501af42a5f0b7374f574f8e2d96f8824` |
| `egfr_competition_2/structure_predictions.zip` | 38272709 | `02d1728f972a0474db29ea5c96bd917fa7a1e3689e6644fcf3c514b518586491` |
| `egfr_competition_1/package.zip` | 130832841 | `21a869c1bc9d1477394f2c82b4cb46a46bded43bc370f7558c2eecd41930700d` |

原始 payload 合计 692181576 bytes；inventory SHA-256 `191164f681385a2e1ccad4754d939b0fbb45cd1d86bc45b1700ad1771c8706be`（与 PDB 同一算法）。归档成员全部读取；统计与 API/验收报告保存于共享 runs，不作为 raw 附属 manifest 发布。每个文件与论文/PDB 身份均可重验，不执行交付包中的训练代码或模型反序列化。

### 许可和再分发边界

两个仓库 LICENSE.md：数据 ODbL，代码 Apache 2.0。外部包按同一竞赛来源保留上游说明；普通公开下载不需申请。未代用户请求免除 ODbL 的商业许可。

### 公开范围对照

| 范围 | 本次证据与状态 |
| --- | --- |
| 已取得的公开部分 | 两个固定 Git tree 和 README 给出的公开交付对象；两轮取样、对照、汇总和预测模型分别保留。source_version 取组合快照中最新 commit 日期 2025-03-18，而非下载日期。 |
| 论文/来源未公开或未取得部分 | 仅按本文具体缺口报告；未访问限制不冒称完成。 |
| processed / release | 未生成；本层仅上游原样输入。 |
