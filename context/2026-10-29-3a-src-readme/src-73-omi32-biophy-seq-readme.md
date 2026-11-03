---
- tags:
  - context
---

# SRC_R73_OMI32_BIOPHY_SEQ 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [作者仓库的测量和模型产物](#作者仓库的测量和模型产物)
  - [交互浏览器和辅助分析](#交互浏览器和辅助分析)
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

- `source_id`：`SRC_R73_OMI32_BIOPHY_SEQ`
- `source_version`：`snapshot-2026-05-30`
- 原作者或发布机构：Cole R. Tharp、Angela M. Phillips 等论文作者团队

### 来源方背景

这批数据的主要作者来自美国加州大学旧金山分校（UCSF）微生物与免疫学系的 Phillips Lab；论文另列 NanoImaging Services（圣迭戈）的共同作者，Angela M. Phillips 同时署名 Howard Hughes Medical Institute。[预印本全文](https://europepmc.org/articles/PMC13015495)列有各作者单位。[实验室成员页](https://aphillipslab.ucsf.edu/lab-members)列 Phillips 为负责人、Cole Tharp 为研究生；[实验室动态](https://aphillipslab.ucsf.edu/news)记载 2025 年 9 月为实验室建组三周年。

该实验室研究病毒蛋白和抗体演化的分子约束，并开发高通量表型测定，见[实验室研究介绍](https://aphillipslab.ucsf.edu/research)。其[发表清单](https://aphillipslab.ucsf.edu/publications)列出 Phillips 参与的 2021 年和 2023 年抗体亲和力景观研究，也列出本次 Omi32 预印本。以上背景说明作者团队此前的相关研究经历。

## 实验设计和数据口径

研究对象是 Omi32 抗体谱系的 13 个二元突变位点，共有 `2^13 = 8,192` 种设计基因型。作者对武汉株、BA.1、BA.4 的 RBD 结合，以及抗体表达和多反应性分别形成测量表。同一 `geno` 可在不同表中出现；各表行数表示该指标保留下来的基因型数量，不能相加为独立抗体数。

高通量测量链从条码与基因型的关联表、分选计数和流式荧光记录出发。作者根据各浓度与分选区间的计数和荧光值估计每个基因型的平均信号，再拟合浓度响应曲线，得到结合的 `K_D` 或多反应性的 `EC50`。`K_D` 越低代表结合越强；作者的 cleaned affinity CSV 将 `-log10(K_D/M)` 以 `log10Kd` 名称存储，数值越大表示结合越强。拟合范围的边界、信号质量及两个生物重复的筛选会删去部分基因型；`7.0` 等边界值可表示检测边界钉扎，使用时应保留这一删失信息。表达值来自荧光信号的对数值，经批次中位数校正后对可用重复求均值和标准误；它是相对测量尺度。多反应性表的 `mean_EC50_3p` 实际由两个 `PSR_log10EC50` 重复值求均值，按作者原字段保留；其试剂浓度来源以 mg/mL 表示。不同指标的数值与方向须按各自字段解释。

公开的五张 cleaned 表分别有武汉株亲和力 6,740、BA.1 亲和力 7,037、BA.4 亲和力 7,416、表达 8,150、多反应性 5,510 个唯一 `geno`。条码清理表有 126,684 个唯一条码，对应 8,192 种 `binary_genotypes`；条码行是测序读段关联记录的汇总，并非 126,684 个独立抗体。作者仓库还保留原始流程输出、流式事件 CSV、低通量验证表和分析脚本。

作者把 cleaned 测量用于非线性变换、线性交互模型及交叉验证，再为五个表型分别生成覆盖全部 8,192 个基因型的 `predicted_phenotype` 和 `prediction_se`。这些字段是模型估计及其不确定度，覆盖没有通过测量筛选的基因型。浏览器数据又把预测值、荧光曲线和二维布局组合成可视化文件；浏览器的数值方向与仓库中相应模型输出有额外符号或归一化处理，不能按同名列直接拼接。模型评估应按基因型和数据形成路径安排训练、验证和测试，避免把预测产物或同一基因型的派生视图当成独立实测标签。

低通量验证表只有 10 行，其中 `geno` 的 `100010100110`、`111111001111` 和 `0` 少于标准 13 位。来源 README 明确提醒电子表格可能删除前导零；这些原值仍按原样保留，逐行连接到主表前须核实编码。

## 论文原文

- 标题：Biophysical trade-offs in antibody evolution are resolved by conformation-mediated epistasis
- 作者：Cole R. Tharp、Claudio Catalano、Anthony Khalifeh、Sam Ghaffari-Kashani、Ruimin Huang、Gyunghoon Kang、Giovanna Scapin、Angela M. Phillips
- 发表来源：bioRxiv 预印本；截至 2026-09-24 未核实到期刊正式版
- 归档文本版本：2026-03-16 的预印本 v2；另存 Europe PMC 的对应全文 XML
- 发布日期：2026-03-16
- DOI：`10.64898/2026.03.12.711465`
- PMID / PMCID：`41889954` / `PMC13015495`
- 本地文件：`articles/2026.03.12.711465v2.full.pdf`
- 文件大小：22.95 MiB（24,063,372 bytes）
- SHA-256：`e2a17d21562cad3dcba3cb335cad945f1e704a5e0859dc2e7a2edc0175dd151f`
- 文本许可：Europe PMC 全文 XML 标明 CC BY 4.0
- 补充材料：`articles/Omi32_2026-03-16_PMC-v2-supplement.zip`，9.41 MiB（9,871,239 bytes），SHA-256 `96ecc4c6fab475e2d456b44083b081b7b9209b851ed8b3e2c8f09657c939c21e`；外层 31 个成员，其中 `media-1.zip` 有 29 个成员，均通过 ZIP CRC 检查

全文 XML 位于 `articles/Omi32_2026-03-16_PMC-v2.xml`，277.57 KiB（284,231 bytes），SHA-256 `a31bd5fa6183ebe13617f94ef6c87c9e89094834352e22e7e672cb219de2d44a`。PDF 可解析为 57 页，嵌入标题与论文一致，创建日期为 2026-03-16。PDF 来自用户手动归档；其官方逐字节身份仍按文末问题跟踪。

## 仓库内容

作者仓库：<https://github.com/Ctharp17/Omi32_BioPhy-Seq>。固定 Git commit 为 `9a57903a8c77b691998f84a95b2764653a4b0279`，tree 为 `16011ccdd072b71edc71a3cf3cf017d22a961e67`；commit 日期是 2026-05-30，因此采用 `snapshot-2026-05-30`。仓库包含 2,048 个跟踪文件，payload 共 1.44 GiB（1,548,810,881 bytes）；没有 Git submodule 或未解析的 LFS 指针。`.git` 历史随仓库留存，不计入上述 payload 字节数。

交互浏览器由作者 README 和论文链接到 <https://amphilli.github.io/Omi32_browser_git/>。2026-09-24 获取其页面代码、站点 MIT 许可证和 5 个本地数据对象。该网页没有可访问的 Git commit 锚点，因此以各文件 SHA-256 固定本次字节；HTTP `Last-Modified` 为 2026-02-24，不能作为科学数据版本号。浏览器 `data/Omi32.csv` 与作者 Git 仓库 `force-directed-layouts/data/Omi32.csv` 的 SHA-256 不同，两个交付副本在本目录中分别保留。`source_version` 的日期只标记作者 Git commit，其余组件另按论文版本、数据库 accession 或文件哈希识别。

```text
snapshot-2026-05-30/
├── Omi32_BioPhy-Seq/
│   ├── BioPhy-Seq_measurements/
│   ├── barcode-variant-table_generation/
│   ├── epistasis_inference/
│   ├── force-directed-layouts/
│   ├── pathway_analysis/
│   ├── Figures/
│   ├── LICENSE
│   └── README.md
└── Omi32_browser_git/
    ├── LICENSE
    ├── index.html
    ├── yoda.js
    ├── yoda.css
    └── data/
        ├── Omi32.csv
        ├── BA1.arrow
        ├── BA4.arrow
        ├── PSR.arrow
        └── WUHAN.arrow
```

`BioPhy-Seq_measurements/` 保存高、低通量结果；`barcode-variant-table_generation/` 保存条码连接材料；`epistasis_inference/` 保存建模输入、系数、交叉验证和预测；`pathway_analysis/` 与 `Figures/` 是下游分析与图表产物。站点 `index.html` 和 `yoda.js` 引用的本地数据对象正是上列 5 个文件；第三方 CDN 依赖按 URL 引用，未复制进此数据快照。

## 数据结构

### 作者仓库的测量和模型产物

作者 Git payload 包含 1,051 个 CSV 和 60 个 TSV，解析出的表头共有 86 种形态；许多流式事件文件共享同一表头，模型协方差矩阵则有由位点组合构成的宽表头。五张主要 cleaned 表位于 `BioPhy-Seq_measurements/high-throughput_measurements/results_Omi-32/cleaned_datasets/`。`geno` 是文本形式的 13 位二元键；导入电子表格时必须保持文本类型。`epistasis_inference/datasets_for_inference/` 在对应测量表后增加 `pos1` 至 `pos13` 与 `num_mutations`。模型目录中的五张 `reference-based/predicted_phenotypes/*_predictions.csv` 均有 `geno`、`predicted_phenotype`、`prediction_se` 三列和 8,192 行。

`results_Omi-32/raw_outputs/` 保存各重复的计数、荧光摘要、拟合结果及统计；`Flow-data/` 和低通量 `flow_data/` 保存事件级仪器导出 CSV。`barcode-variant-table_generation/clean_geno-barcode_table/variants_barcodes_binary-genos.csv` 是条码到设计基因型的多对一映射。图表、路径分析和模型系数文件属于派生分析结果，各自的行粒度可为基因型、折次、模型参数、路径、边或仪器事件。当前 Git BA.1 输出的重复代号是 `d/i`，与另存的网页 Arrow 快照不同。

### 交互浏览器和辅助分析

站点 `data/Omi32.csv` 有 8,192 行、66 列，以 `variant` 保存基因型，并包含四种结合或多反应性浏览器数值、表达、标准误、布局坐标及 13 个位置的邻居差值。4 个 Arrow IPC 文件均能解析为 8,192 行：`BA1.arrow`、`BA4.arrow`、`WUHAN.arrow` 各 30 列，`PSR.arrow` 有 38 列。各文件含 `variant`、对应显示数值和按重复与浓度编号展开的荧光摘要；没有测量时可为空。站点 CSV 为 7.09 MiB（7,437,298 bytes）；五个数据对象合计 15.54 MiB（16,294,618 bytes）。

### 字段说明

以下按来源文件家族及可还原原始字段名的规则覆盖实际 CSV、TSV 和 Arrow 字段。`i` 表示位点或浓度编号时均注明范围；`r1`、`r2` 与 `rep1`、`rep2` 保留各文件原拼写。空字符串、`null`、`NaN` 等按原文件保留；某些 CSV 的空表头 `''` 是作者导出的行索引，不作为测量特征。数值字段未注明绝对单位时保留来源尺度，不进行项目侧换算。

| 适用文件或家族 | 原始字段或命名规则 | 类型、含义与解释边界 |
| --- | --- | --- |
| 基因型、条码和派生表 | `geno`、`binary_genotypes`、`variant`、`from_binary`、`to_binary`、`from_genotype`、`to_genotype` | 字符串基因型或路径端点；主库使用 13 位二元编码。低通量表的 3 个短值保留原样。 |
| 基因型与模型输入 | `pos1`…`pos13`、`pos345`、`num_mutations`、`som_mut`、`mutation_index`、`nb_mutations_from` | 位点二元编码、突变数量或路径边的位点索引；`pos345` 是图表中多个位点的派生组合标记。无物理单位。 |
| 条码映射及设计参考 | `index`、`target`、`library`、`barcode`、`barcode_length`、`variant_call_support`、`codon_substitutions`、`aa_substitutions`、`n_codon_substitutions`、`n_aa_substitutions`、`substitutions`、`sequential_site`、`reference_site`、`amino_acid`、`mutation_type`、`region`、`dummy_site`、`run`、`fastq`、`name` | 上游条码、变体注释、位点对应与输入文件标识；支持计数和替换数为非负计数，序列或注释为文本。`fastq` 是上游文件名字段，当前 source 未归档 FASTQ 字节。 |
| 样本与仪器元数据 | `sample`、`sample_id`、`sample_name`、`construct`、`solute`、`replicate`、`antigen`、`concentration`、`concentration_float`、`bin`、`P5`、`P7`、`col_i`、`row_i`、`cell count`、`collection_date`、`sequencing_data_subdir`、`cytometry_data_subdir`、`directory`、`row`、`well`、`well column`、`shortname` | 样本、分选区间、重复、试剂浓度和板位或输入目录的来源标签；浓度单位依具体 assay 的上游表与论文，`P5`/`P7` 为测序索引字段。`antigen` 在部分分析文件也用作表达或 PSR 指标键。 |
| 事件级流式 CSV | `FSC-A`、`FSC-H`、`FSC-W`、`SSC-A`、`SSC-H`、`SSC-W`、`Time`，以及 `530_30 Blue B-A`、`530_30 Blue C-A`、`530/30 Blue B-A`、`582_15 YG D-A`、`585_15 YG E-A`、`585/15 YG E-A`、`586_15 YG D-A` | 单个事件的散射、检测通道与采集时间；数值为仪器原始尺度，通道拼写依批次变化。这些事件行不代表独立抗体基因型。 |
| 计数与流程统计 TSV | `Omi32_{a,b,d,e,f,g,h,i}_{编号或F}_{编号}`、`num_reads`、`num_unique_UMIs`、`num_reads_dropped`、`frac_reads_dropped`、`num_genos_seen`、`fastq_file`、`total_reads_considered`、`reads_matching_pattern`、`fraction_of_fastq_accepted`、`reads_with_incorrect_barcode`、`reads_with_no_err_in_barcode`、`reads_with_one_sub_in_barcode`、`reads_with_two_or_more_subs_in_barcode`、`reads_with_indels_in_barcode`、`total_accepted`、`fraction_accepted`、`reads_with_corrected_index_err`、`reads_with_no_index_err`、`reads_thrown_out`、`fraction_of_index_accepted` | 各样本分选计数、UMI/读段和接受比例；`Omi32_i_*` 属于 BA.1 的另一个重复代号。计数为非负整数，比例在来源尺度，不能直接当成亲和力标签。 |
| 流式汇总与逐浓度拟合 | `mean_log10_PEs`、`std_log10_PEs`、`mean_log10_FITCs`、`std_log10_FITCs`、`mean_log10PE0`…`mean_log10PE8`、`std_log10PE0`…`std_log10PE8`、`variant_frac_conc0`…`variant_frac_conc8`，后者也有 `_r1`/`_r2` 后缀 | 荧光对数均值、标准差与变体频率；浓度序号 0–6 用于亲和力，0–8 用于 PSR。荧光值是仪器相对尺度，比例无单位；缺失浓度点须保持缺失。 |
| 拟合诊断与过滤 | `A`、`B`、`r2`、`sigma`、`median_variant_fraction`、`log10Kd`、`log10Kd_rep1`、`log10Kd_rep2`、`PSR_log10EC50`，以及相应 `_rep1`/`_rep2` 或 `_r1`/`_r2` 形式；`z_score_log_A_over_expr_rep1`、`z_score_log_A_over_expr_rep2`、`z_used` | 浓度响应拟合的幅度、背景、拟合优度、残差尺度、变体频率、重复表型及过滤统计；`z_used` 在当前三个 affinity cleaned 表分别为 1.8、3.4、1.9。`log10Kd` 在测量表沿用作者的正向亲和力尺度，边界值可能是钉扎值。 |
| cleaned 亲和力与表达 | `wuhan_log10Kd_mean`、`ba1_log10Kd_mean`、`ba4_log10Kd_mean` 及各自 `_sem`；`expr_mednorm_mean`、`expr_mednorm_sem`、`ba4_expr_r1`、`ba4_expr_r2`、`wuhan_expr_r1`、`wuhan_expr_r2`、`psr_expr_r1`、`psr_expr_r2` | 每基因型的重复均值、标准误与各实验重复的校正后表达；亲和力按作者存储的 `-log10(K_D/M)` 数值，表达为相对 `log10` 荧光尺度。标准误缺失或零须按原值解释。 |
| cleaned 多反应性 | `PSR_log10EC50_r1`、`PSR_log10EC50_r2`、`A_r1/r2`、`B_r1/r2`、`r2_r1/r2`、`sigma_r1/r2`、`median_variant_fraction_r1/r2`、`Mean fluorescence expression_r1`、`Mean fluorescence expression_r2`、`Std fluorescence expression_r1`、`Std fluorescence expression_r2`、`mean_EC50_3p`、`SEM_EC50_3p` | 两重复的拟合与诊断；最后两列是作者代码对两个 `PSR_log10EC50` 值求得的均值与标准误，字段名未说明这一变换。试剂输入浓度为 mg/mL，表中汇总值使用来源拟合后的对数尺度。 |
| 低通量验证和其他摘要 | `antibody`、`wuhan_lt_mean/sem`、`ba1_lt_mean/sem`、`ba4_lt_mean/sem`、`replicate_1_expression`、`replicate_2_expression`、`replicate_1_sem`、`replicate_2_sem`、`log_EC50`、`log_EC50_err`、`mean_log_EC50`、`sem_log_EC50`、`hill_coefficient`、`hill_coefficient_err`、`mean_hill_coefficient`、`sem_hill_coefficient`、`amplitude_A`、`baseline_B`、`mean_amplitude_A`、`mean_baseline_B`、`fit_quality_rmse`、`mean_fit_rmse`、`n_replicates`、`expression`、`expression_sem` | 单构建体的验证拟合、荧光或稳定性摘要；`*_mean`、`*_sem` 是同指标均值与标准误，`n_replicates` 为重复数，`rmse` 为拟合误差。低通量表有空值，未测指标不可补为零。 |
| 预测与模型输入 | `predicted_phenotype`、`prediction_se`、`wuhan_predicted_phenotype`、`ba1_predicted_phenotype`、`ba4_predicted_phenotype`、`expression_predicted_phenotype`、`psr_predicted_phenotype` 及相应 `_prediction_se`；`version`、`is_pinned` | 模型对基因型的预测及标准误，或线性化文件的版本与边界钉扎标识。预测覆盖 8,192 个设计点；缺失实测标签仍有预测值。 |
| 模型选择和交叉验证 | `scope`、`phenotype`、`phenotype_name`、`order`、`predict_phenotypes`、`fold`、`r2_train`、`r2_test` 及 `_mean`/`_std` 形式、`n_samples`、`n_train_used`、`n_test_used`、`n_params`、`alpha_bonf`、`num_sig` 及 `_mean`/`_std` 形式 | 模型范围、变换、阶数、折次及训练/测试拟合统计；`r2` 越高拟合越好，但同基因型派生文件不可组成独立测试样本。`n_*` 是模型样本或参数计数。 |
| 模型协方差矩阵 | 空表头 `''` 与由 1–13 位点编号组成的 `1`、`1 2`、`1 2 3` 等单、双、三阶列名；来源表头可能重复 `1` | 行列是模型参数或其组合的矩阵坐标，单元格为系数协方差；单位随所拟合表型尺度平方变化。重复列名按原样保留，读取时应以列位置和作者模型配置定位。 |
| 浏览器 CSV | 空表头 `''`、`variant`、`BA1_log10Kd`、`BA4_log10Kd`、`WUHAN_log10Kd`、`PSR_log10Kd`、对应 `*_stelog10Kd`、`Expression_log10Kd`、`Expression_stelog10Kd`、`fdl_x`、`fdl_y`、`{BA1,BA4,WUHAN,PSR}_{0..12}_deltaKd` | 行索引、13 位基因型、展示用预测值与误差、二维布局坐标、单步邻居的展示数值差。作者生成 notebook 对亲和力显示值做负号转换，对表达另作归一化；`Expression_log10Kd` 的名称沿用网页代码，不表示表达有 `K_D` 单位。 |
| 浏览器 Arrow | `variant`、对应 `{BA1,BA4,WUHAN,PSR}_log10Kd`、`c{0..6}_{a,b,c,d,e,f}`、`e{0..6}_{a,b,c,d,e,f}`；PSR 另有 `c{0..8}_{g,h}`、`e{0..8}_{g,h}` | 浏览器逐基因型显示值和不同重复/浓度的荧光对数均值 `c`、标准差 `e`；实际存在的重复字母由每个 Arrow schema 限定：BA4 `a/b`、BA1 `c/d`、WUHAN `e/f`、PSR `g/h`。缺少实验曲线的位置可为空。 |
| 路径分析 | `step_0`…`step_13`、`bootstrap_0`…`bootstrap_10`、`path_rank`、`path`、`from_genotype`、`to_genotype`、`from_binary`、`to_binary`、`mutation_index`、`nb_mutations_from`、`is_uphill`、`Mutation`、`Order 1`…`Order 13` | 路径、边、重复抽样概率和突变顺序的模型派生结果；`is_uphill` 为模型定义的方向标志。数值是对应模拟或模型尺度，不是新的实验亲和力测量。 |
| 图表与辅助统计 | `Dataset`、`Mean_log10_paths`、`SEM_log10_paths`、`Mean_paths`、`Percent_of_total`、`BLI_r1`、`BLI_r2`、`tm_1`…`tm_3`、`PC1`、`PC2`、`comparison`、`pearson_r`、`pearson_p`、`spearman_rho`、`spearman_p`、`n`、`slope`、`intercept` | 图表分组、路径汇总、正交验证、稳定性重复、降维坐标和相关/回归统计；`p` 为显著性数值，`n` 为比较样本数。来源图表的验证量纲按原文件保留。 |
| 结构与交互图表衍生 | `pair`、`distance`、`epistasis`、`i`、`j`、`site`、`chain`、`resi`、`buried_area`、`total_effect`、`abs_effect`、`hex_color`、`mean_expr_e/p`、`sem_expr_e/p`、`w_kd_mean_e/p`、`w_kd_sem_e/p`、`ba1_kd_mean_e/p`、`ba1_kd_sem_e/p`、`ba4_kd_mean_e/p`、`ba4_kd_sem_e/p`、`delta_ab_{抗体编号或GERMLINE或OMI32}_{rep1/rep2/expr/pred}` 及其 `mean_`/`sem_` 前缀 | 位点对、结构编号、表面积、效果与颜色编码，以及图表连接的测量/预测/差值统计；`e` 与 `p` 分别标记实验和预测来源。单位与符号随图表来源文件，不能与 cleaned 标签直接合并。 |
| 其他来源计数 | `category`、`count`、`total_effect`、`abs_effect`、`site`、`chain`、`resi` | PacBio 处理类别和计数，或结构图表的位点效果。重复出现的字段按所在文件家族解释。 |

当前 source version 中观察到的可简洁列全的分类取值如下；这些是文件扫描结果，不保证未来版本只允许这些值。

| 字段及适用家族 | 当前原始取值与含义 |
| --- | --- |
| `is_pinned`（线性化文件） | `0` 未钉扎；`1` 被来源模型标记为边界钉扎。 |
| `predict_phenotypes`（模型配置表） | `FALSE` 不在该配置输出预测；`TRUE` 输出预测。 |
| `is_uphill`（路径边表） | `0` 非来源模型定义的上升边；`1` 是上升边。 |
| `mutation_type`（设计表） | `designed mutation`：设计位点突变。 |
| `target`、`library`（条码表） | `target=gene` 为来源目标标签；`library=Omi-32-1` 为该库 ID。 |
| `category`（PacBio readstats） | `filtered PacBio_amplicon` 过滤后读段；`aligned PacBio_amplicon` 已比对读段；`unmapped` 未映射读段。 |
| `scope`（模型文件） | `all` 全部来源输入；`pos4_binders` 特定正向结合子集；`full` 全位点模型；`pos4` 来源定义的位点子集，具体筛选以相应脚本为准。 |
| `phenotype`、`phenotype_name`（模型文件） | `raw` 原测量尺度输入；`latent_hill`、`latent_logistic` 及 `latent_hill_v1`、`latent_hill_v2`、`latent_logistic_v1` 为来源代码定义的非线性变换版本。 |
| `region`（位点表） | `CH`、`VH`、`VL`、`CK`、`TM`、`SP1`、`P2A`、`SP2`、`Myc`、`Other`：来源的构建体区域代码，精确区域边界以原位点表为准。 |
| `solute`（样本表） | `BA1`、`BA4`、`WH`、`PSR` 为试剂/指标代码；空字符串表示来源表未填。 |
| `antigen`（低通量/模型表） | `BA1`、`BA4`、`WUHAN`、`Wuhan`、`PSR` 及小写 `ba1`、`ba4`、`wuhan`、`psr`、`expression`，另有空字符串；大小写与来源文件保持一致，`expression` 和 `psr` 在模型表中是指标键。 |
| `replicate`（元数据与低通量表） | `a/b` 对应 BA.4、`d/i` 对应 BA.1、`e/f` 对应武汉株、`g/h` 对应 PSR；`1/2` 为低通量重复编号；空字符串为来源缺失。 |

### 数据示例

- `ba1_affinity_cleaned.csv` 的 `geno=0000000000000` 一行记录 `ba1_log10Kd_mean=7.0`、`ba1_log10Kd_sem=0.0`、`z_used=3.4`。该行是一个基因型在 BA.1 指标下的清理后汇总，`7.0` 位于论文所述亲和力检测边界。
- `ba1_raw_3order_full_biochem_predictions.csv` 的相同 `geno` 记录 `predicted_phenotype=7.398105259990238`、`prediction_se=0.06978912188547425`。这是一项模型预测，与上一行关联同一基因型。
- 浏览器站点 `data/Omi32.csv` 的相同 `variant` 记录 `BA1_log10Kd=-7.398105259990238`、`fdl_x=8.701248168945312`、`fdl_y=-2.3225789070129395`。数值方向与预测表不同，布局坐标仅用于网页展示。

## PDB 数据库

论文的 Data Availability 明确列出五个 PDB entry 与对应 EMDB entry。项目按 entry 粒度保存 RCSB 原始完整 FASTA 和 mmCIF；论文支持 entry 与参考复合物的对应，尚无逐基因型结构键。未生成带推定链角色的选链 FASTA。以下文件均于 2026-09-24 从 RCSB 取得，10 个文件合计 2.65 MiB（2,775,860 bytes）；每对的 CIF 内也记录相应 EMDB accession。

| 参考复合物 | PDB / EMDB | FASTA 大小与 SHA-256 | mmCIF 大小与 SHA-256 |
| --- | --- | --- | --- |
| germline + LCκ | `11OU` / `EMD-75893` | 753 bytes；`741deed43826d15905bf66a40a6ff350d797a74a9efb87faad4b3305b91732c0` | 449.38 KiB（460,160 bytes）；`ce7eea1b6cb78b236060275c58b1cdfdae881af3e59e184556f79757628673d6` |
| Omi32 + LCκ | `11OR` / `EMD-75892` | 730 bytes；`c7c4d1344b948845d5a62f47b7f9a99a6120d99a322ef29eafd602b30b5d346b` | 446.86 KiB（457,581 bytes）；`2912dab8daa2e68f109b901a1180daca1f4c9646ffffa5bbda5b61f3ec46efd6` |
| germline + BA.1 + LCκ | `11OQ` / `EMD-75891` | 1.02 KiB（1,048 bytes）；`587ff4f27e3625ae724dbbcbad59a0eb116f2b924554dbc03e3644935a2058eb` | 588.72 KiB（602,851 bytes）；`bcddb59371c8b5d44214d47585f110e3393d15cbaf401ff0897ce3a9962356e8` |
| germline + BA.4 + LCκ | `11OO` / `EMD-75889` | 1.01 KiB（1,035 bytes）；`1f68e63b7ce4d70064e0341785133f61882c870a6e66654117a37fc4a1b09880` | 609.19 KiB（623,815 bytes）；`aba0acb147dd5bda800d115ad343796d75e67bbb21f5a3e86162ccf56eb71188` |
| Omi32 + BA.4 + LCκ | `11OL` / `EMD-75887` | 1.02 KiB（1,043 bytes）；`26bd1a07147f4aef5de0f21ccd3bae192c56b5983fb7bc1519243a72ec14f166` | 612.15 KiB（626,844 bytes）；`5982618996817bd0dfd7a9fa30c7bcbb4be35e1ec690b07eca8712ae5df5d29c` |

`pdb/sequences/` 中的 FASTA 是 RCSB 全 entry 的原始文件，`pdb/structures/` 中是完整坐标。复合物层级的连接依据为论文 Data Availability 与 CIF 的数据库交叉引用；链副本与作者编号的具体选择未作为确定映射发布。五个结构是 germline/Omi32 等参考构建体，8,192 个基因型并无逐条对应结构。

五个 EMDB primary map 归入 `emdb/maps/`，与上述五个 CIF 一一对应。2026-09-24 从 EMDB 官方镜像取得，合计 1.30 GiB（1,392,197,015 bytes）；全部压缩文件均通过 gzip 完整性检查。

| EMDB 图 | 文件大小 | SHA-256 |
| --- | --- | --- |
| `EMD-75893` / `emd_75893.map.gz` | 203.43 MiB（213,312,571 bytes） | `4da35acba00a3e0428c7298dcbb08fe0648f19352fad8465f5e6db0043583559` |
| `EMD-75892` / `emd_75892.map.gz` | 203.48 MiB（213,360,798 bytes） | `8a48178474f848c469ab0b55adf076e26ca7c25e780a06004e119f06f44134d1` |
| `EMD-75891` / `emd_75891.map.gz` | 306.79 MiB（321,697,572 bytes） | `166f7994fc6e3809e6f880d07145139f97282990150001f7c8c17100b65f42ef` |
| `EMD-75889` / `emd_75889.map.gz` | 307.11 MiB（322,032,525 bytes） | `95432fde1cf6c5e89869980f46a908ef55c9c752bd8b2c913efb3f130a874a6a` |
| `EMD-75887` / `emd_75887.map.gz` | 306.89 MiB（321,793,549 bytes） | `bc455d0f375799586aa0cf2908967df474c86e6536eaaab3ea61e34f6dd57f81` |

## 采集过程记录

- 2026-09-24：用户指定直接处理 R73，覆盖原批次串行启动顺序；R69 保持研究中，R70–R72 未动。读取项目配置、资源清单、skill 与 README 格式合同，在共享 raw staging 建立 `snapshot-2026-05-30.partial`。
- 2026-09-24：从作者 Git 仓库固定 commit/tree，核对 2,048 个跟踪文件、干净工作树、`git fsck`、LFS 与 submodule 状态。作者仓库含 cleaned 测量、原始流程输出、建模预测和浏览器生成代码。
- 2026-09-24：Europe PMC 全文 XML 和 supplementaryFiles 可直接取得；早期 PMC PDF 请求返回 HTML 挑战，bioRxiv PDF 请求返回 429。用户随后把预印本 PDF 放进 `articles/`；验证文件签名、标题、57 页可读性及 SHA-256。ZIP 外层及内层 CRC 均通过。
- 2026-09-24：按论文列出的五个 PDB ID 从 RCSB 成对获取 FASTA/mmCIF，核对 entry ID、字节数与 SHA-256；本次只保存完整 entry，未推定具体链副本。
- 2026-09-24：用户把站点 1 个 CSV 和 4 个 Arrow 文件放在 staging 根；逐文件与站点现取字节 SHA-256 比对一致，CSV 8,192 行，Arrow 逐个解析为 8,192 行。随后移入 `Omi32_browser_git/data/`，归档页面代码和站点 MIT 许可证。发现站点 CSV 与作者 Git 中同名展示 CSV 有不同哈希，两个原文件均保留。
- 2026-09-24：Arrow 逐列校验发现站点 BA.1 文件使用 `c/d` 重复代号，当前 Git 的 BA.1 高通量输出使用 `d/i`；按两个交付快照分别记录，不做无证据的重复映射。
- 2026-09-24：扩大论文结构资料审计，发现与 PDB 对应的五个 EMDB primary map，官方 HEAD 合计 1.30 GiB（1,392,197,015 bytes）。初次串行下载速度过低，停止并清理仅有的未完成片段；改用官方镜像的可恢复分段脚本，遇到 TLS 中断后加入重试和另一官方镜像回退。五图最终均通过官方字节数、gzip 和 SHA-256 复核，`Q05` 关闭。
- 2026-09-24：用户明确暂缓约 200 GB 的测序 FASTQ；NCBI/ENA 当前未提供可验证的完整 run 文件清单。本次只接入公开处理结果及已核实的非 FASTQ 附件，并在问题清单保留 accession 与后续验收条件。
- 2026-09-24：独立脚本在 staging 核对 Git、22 个固定附件、五个 EMDB 图、五对 PDB、cleaned/预测表和 1,197 个原始表格字段；浏览器 Arrow 逐列解析通过，README 的 markdownlint 为 0 错误。确认正式目标不存在后，在同一文件系统原子重命名为正式目录；正式目录的完整脚本和 Arrow 复验再次通过。已同步本地 README、状态台账与验证记录。

- 2026-09-24：核对 README 格式合同后补充来源方背景；依论文作者单位及 UCSF 实验室官网核实团队、地点、研究方向和相关发表记录，本地工作文件与共享正式 README 同步。

## 参考文献

- [Tharp 等，bioRxiv 预印本，DOI 10.64898/2026.03.12.711465](https://doi.org/10.64898/2026.03.12.711465)。
- [Europe PMC 全文记录 PMC13015495](https://europepmc.org/articles/PMC13015495)。
- [作者 Git 数据与代码仓库](https://github.com/Ctharp17/Omi32_BioPhy-Seq)，本 source 固定 commit `9a57903a8c77b691998f84a95b2764653a4b0279`。
- [作者链接的交互浏览器](https://amphilli.github.io/Omi32_browser_git/)。
- [NCBI BioProject PRJNA1469908](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1469908) 与 [PacBio run SRR38904967](https://www.ncbi.nlm.nih.gov/sra/SRR38904967)。
- RCSB 条目：[11OU](https://www.rcsb.org/structure/11OU)、[11OR](https://www.rcsb.org/structure/11OR)、[11OQ](https://www.rcsb.org/structure/11OQ)、[11OO](https://www.rcsb.org/structure/11OO)、[11OL](https://www.rcsb.org/structure/11OL)；对应 EMDB accession 见上表。
- [EMDB 官方地图获取与使用说明](https://www.ebi.ac.uk/emdb/faq)；各图 accession、文件和哈希见上表。

## 其他

### 数据范围和限制

本 source 公开包包括作者仓库、浏览器站点、预印本及其补充材料、五组参考结构与对应电镜图。作者仓库的 `raw_outputs/` 指分析流程产物；最底层仪器 FASTQ 未纳入本次归档。模型预测、可视化 CSV/Arrow、图表汇总均与 cleaned 测量有关联，训练/测试划分必须考虑共同的 `geno` 与派生关系。网页与作者 Git 的同名浏览器 CSV 属不同发布字节快照。

### 完整性与验收

截至 2026-09-24，作者 Git commit/tree、2,048 个跟踪文件及 1,548,810,881 payload bytes 已验证；论文 PDF、XML、补充 ZIP、10 个 RCSB 文件、五个 EMDB primary map 和浏览器页面及数据文件均有固定 SHA-256。五个 Arrow 均可解析；主 CSV 与低通量 `geno` 异常已按原样记录。`workspace/users/yangwuyu/scripts/validate_r74_omi32_biophy_seq.py` 在 staging 和正式目录均通过，README 的固定 markdownlint 为 0 错误。公开包已发布到 `SRC_R73_OMI32_BIOPHY_SEQ/snapshot-2026-05-30/`；完整研究数据获得保持 partial，原因和后续条件见文末问题。

### 许可和再分发边界

作者 Git 快照含 MIT `LICENSE`；浏览器站点根目录也提供 MIT `LICENSE`，版权声明为 Angela Phillips。论文 XML 标明 CC BY 4.0。EMDB 官方说明地图数据自由使用并需署名原作者及 accession。各组件的许可按其来源分别记录；使用时保留作者、论文、PDB/EMDB accession 和原始许可证文本。本项目的共享 raw 目录是内部数据存储，后续公开再分发需沿各来源条款核对。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 作者分析与 cleaned 测量 | 固定 Git tree 与 5 张 cleaned 表、流程输出 | 已取得并通过基础验收 |
| 覆盖 8,192 基因型的模型预测 | 5 张 `predicted_phenotypes` CSV | 已取得；标为预测 |
| 交互浏览器数据 | 1 个 CSV、4 个 Arrow、HTML/JS/CSS 与 MIT 许可证 | 已取得；按站点文件哈希固定 |
| 预印本及补充材料 | 57 页 PDF、Europe PMC XML、补充 ZIP | 已取得；PDF 官方字节身份待复核 |
| 五个参考复合物及 EM 图 | 5 对 FASTA/mmCIF；5 个 EMDB primary map | 已取得并通过文件完整性验收 |
| PacBio 与 Illumina 原始 FASTQ | 仅有 `SRR38904967` 与 `PRJNA1469908` accession 线索，无完整 run 文件清单 | 本次按用户要求暂缓 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-24；暂缓）：作者 README 估计完整压缩 FASTQ 约 200 GB，指向 `SRR38904967` 和 `PRJNA1469908`；当前 ENA 文件报告未给出可核验的 run 文件清单。用户要求暂不下载。此缺口限制从测序原始读段重新运行分析；现有 cleaned 表和模型产物可按本 README 的层级使用。待用户恢复该分支且官方给出 run、URL、bytes、MD5 后，先核算容量，再逐文件获取和验收。
- `Q02`（最近更新：2026-09-24；映射待核实）：低通量 `Omi32_low-throughput_affinities.csv` 的 10 行中有 `100010100110`、`111111001111`、`0` 三个短 `geno`。原值已保留；在未对照作者构建体标识核实时，不把它们自动补零后与 13 位主表做确定性连接。关闭条件是得到同一版本中逐行编码依据。
- `Q03`（最近更新：2026-09-24；结构链粒度待核实）：论文与 CIF 支持五个 entry 及 EMDB 的复合物级关联；本次保留完整 entry FASTA/mmCIF，未发布推定的 author/label chain 角色映射。若后续任务需要链级特征，需以论文或作者输入文件和 CIF 实例表逐项核实链角色、编号与副本。
- `Q04`（最近更新：2026-09-24；论文字节身份待复核）：PDF 由用户手动放入 `articles/`，可解析为 57 页且标题、创建日期与预印本记录相符；官方 PDF 端点先前返回访问挑战或 429，尚无官方 PDF checksum。当前以固定本地 SHA-256 和 Europe PMC XML 交叉核对文本；若一手入口可用，需比对 PDF 字节或版本元数据后关闭。
- `Q06`（最近更新：2026-09-24；版本映射待核实）：站点 `BA1.arrow` 中重复后缀为 `c/d`，作者 Git 当前 BA.1 原始输出为 `d/i`；两个快照各自已按原字节保存。跨快照使用荧光曲线时，应先从作者生成 notebook 或正式版本说明取得 `c` 与 `i` 的关系；目前不把它们视作同一重复。
