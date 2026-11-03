---
- tags:
  - context
---

# SRC_R29_RESP 数据说明

## 数据集身份

- `source_id`：`SRC_R29_RESP`
- `source_version`：`snapshot-2025-06-27`
- 原作者或发布机构：Jonathan Parkinson、Ryan Hard、Wei Wang；UC San Diego

## 实验设计和数据口径

以 atezolizumab scFv 的重链 error-prone PCR 构建约 78 million 文库，yeast display / 解离筛选并测序，再将读数整理为低/中/高序数结合类别，训练 autoencoder 和 ordinal 模型，选择少量候选验证。PD-L1 结合解离类别不是每条序列的精确 KD；论文 75,631 条处理后独特变体也不等于公开归档的所有训练/缓存/重复文件行数。

raw reads、encoded_data、模型、训练子集和再次使用的 Mason HER2 数据有层级/派生/跨资源重复关系。低中高类、off-rate 代理与 BLI KD 分开解释，保留选择规则、亲本和筛选批次；缺失不当不结合。cAbRep autoencoder 训练库来自外部数据库，未声称取得其完整数据库快照。 验证 Source Data 的 Figure 6B 工作表有75631条 Category/ordinal_regression_score，这是模型分数而非KD；Figure 8 和 Figure S7 为酵母表面解离/结合源数据，小规模 BLI 的 Mutant 4 因极慢解离无法拟合KD，不能填成精确零。

## 论文原文

- 标题：The RESP AI model accelerates the identification of tight-binding antibodies.
- 作者：Parkinson J, Hard R, Wang W.
- 载体与版本：Nat Commun
- 发布日期：2023-01-28
- DOI：10.1038/s41467-023-36028-8
- PMID / PMCID：36709319 / PMC9884274
- 本地文件：`articles/RESP_2023-01-28_EuropePMC-published.xml`；`articles/RESP_2023-01-28_NatureCommunications-published.pdf`
- 文件大小：RESP_2023-01-28_EuropePMC-published.xml：191818 bytes；RESP_2023-01-28_NatureCommunications-published.pdf：2347435 bytes
- SHA-256：RESP_2023-01-28_EuropePMC-published.xml：`6c292197de45bd1fe7e6093a75b2eef1ad6ba7b9a50f3b3dc9f53d590fc358a4`；RESP_2023-01-28_NatureCommunications-published.pdf：`f8afb703047570a4acb64cc751490abcc0de589f479af6ae0b334191ddbdf0e0`
- 文本许可：CC BY 4.0
- 补充材料：已归档 3 个文件。

| 本地文件 | 角色 | bytes | SHA-256 |
| --- | --- | --- | --- |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-1.pdf` | Supplementary Information | 5489337 | `ed4e3cccb7ac7243b8ce8613b4fbb7a2b513fc0983bcc304d5b57bf770e210bb` |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-2.pdf` | Reporting Summary | 375199 | `fbf700b0cf735a32ecee04bd04c70f701b5e9a152144cfbd96266d7ccc701bcc` |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip` | Source Data (download ZIP) | 7061439 | `267ed091c9b8593e859724f0bf3172c49975e4efcbb4873132e916b1b9f5632c` |

## 仓库内容

- 一手入口：<https://zenodo.org/records/15758312>；record `15758312`；上游日期 2023-01-28。
- 一手入口：<https://github.com/Wang-lab-UCSD/RESP>；commit `2621454a24804b131c6fa4979dc8dd46b7a8b942`，tree `aa2dc580f60e2198195b158cb30799269263054a`；上游日期 2025-06-27。

当前组合交付包括两个公开 Zenodo ZIP、固定作者 Git tree、公开论文/补充/Source Data、亲本结构，以及 ENA 对 PRJNA813220 提供的 6 个 FASTQ.GZ。ENA 文件覆盖 SRR18256858、SRR18256859、SRR18256860 的双端读数；未取得 NCBI `.sra` 容器。`RESP_data.zip` 内另含 RH01/02/03 各 R1/R2 的 6 个 FASTQ.GZ 和 1,899,342,445 bytes 的 `encoded_data.tar.gz`。逐条比较确认 ENA 与 ZIP 内对应读数的序列、质量值和顺序一致，但读名和 gzip 交付字节不同，因此保留为经过验证的另一份上游交付。上游 ZIP 另有仅 0 bytes 的 `/` 根目录成员，验收按原包只读检查，未按绝对路径解包。

上游未给整个数据交付包提供正式版本名；`snapshot-2025-06-27` 取自固定 Zenodo record 15758312 的 `created=2025-06-27T22:59:24.503643+00:00`，表示这条具体版本记录的创建日期。元数据 `publication_date=2023-01-28` 另行保留，不与该日期混用；不使用本次下载日期。 辅助 Git 包仍按下列独立 commit 固定。 `v0.0.1` 是交付中的 RESP 代码 release/tag，不覆盖本次同时保存的后续 Git commit 与整个组合数据包。原交付归档保持压缩格式，验收时读取所有成员，不在 raw 中重新生成数据表。

```text
snapshot-2025-06-27/
├── RESP/
│   ├── RESP-v0.0.1.zip
│   ├── RESP_data.zip
│   └── RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz
└── ENA_PRJNA813220/
    ├── SRR18256858_1.fastq.gz
    ├── SRR18256858_2.fastq.gz
    ├── SRR18256859_1.fastq.gz
    ├── SRR18256859_2.fastq.gz
    ├── SRR18256860_1.fastq.gz
    └── SRR18256860_2.fastq.gz
```

Git 快照全部 blob 与固定 commit tree 校验；2621454a24804b131c6fa4979dc8dd46b7a8b942：131 个 blob，LFS 0，submodule 0。

## 数据结构

### 原始交付与记录粒度

`RESP_data.zip` 原样保留原始读数与 nested `encoded_data.tar.gz` 等交付；`ENA_PRJNA813220/` 保存 ENA 独立交付的 3 个 run、6 个 mate 文件，共 835,653 对读数。SRR18256858、SRR18256859、SRR18256860 分别对应 RH03、RH02、RH01。Zenodo v0.0.1 ZIP 是正式代码版本，固定作者 Git tree 是后续代码快照，两者文件与派生数据存在重叠。论文 Source Data ZIP 包含验证图表源数据；编码数组/权重不以反序列化执行验收。代码包附带的 ProtVec 文件扩展名为 `.csv`、实际为 tab-delimited words + d1…d100（9,048 行），不是单字段实验表。`Mutation_scoring.csv` 原表头为 3 字段、19 条数据行均有 4 值；`cluster_marginal_distributions_source_data.csv` 为带标题的多段布局，不是单一规范字段表。原始行数包含标题/派生注释；两类不齐行文件不按位置报告列统计或修补成统一科学表。主要 ordinal 示例取论文 Source Data 的 Figure 6B 真实两字段记录。

| 原始表或 sheet | 非空数据行 | 列数 |
| --- | --- | --- |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/notebooks/decoy_scores.csv` | 24015 | 3 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/notebooks/decoys.csv` | 24014 | 182 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/notebooks/human-ness_scores.csv` | 143318 | 3 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/notebooks/orig.csv` | 23758 | 163 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/notebooks/orig_scores.csv` | 23759 | 3 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/results_and_resources/ProtVec/protVec_100d_3grams.csv` | 9048 | 101 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/results_and_resources/selected_sequences/Mutation_scoring.csv` | 19 | 3 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/results_and_resources/selected_sequences/Test_set_score_distribution.csv` | 75631 | 2 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/results_and_resources/selected_sequences/cluster_marginal_distributions_source_data.csv` | 43 | 1 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/results_and_resources/selected_sequences/dendrogram.csv` | 126 | 4 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/results_and_resources/simulated_annealing/markov_chain_scores.csv` | 7623 | 3 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/trastuzumab_data/raw_data/anarci_check2.csv_H.csv` | 1 | 133 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/trastuzumab_data/raw_data/mHER_H3_AgNeg.csv` | 27539 | 6 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/trastuzumab_data/raw_data/mHER_H3_AgPos.csv` | 11300 | 6 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/trastuzumab_data/raw_data/trastuzumab_anarci.txt_H.csv` | 1 | 133 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/trastuzumab_data/results_and_resources/model_exp_scores.csv` | 56 | 3 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/trastuzumab_data/results_and_resources/model_training_scores.csv` | 29999 | 2 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/trastuzumab_data/results_and_resources/uncertainty_vs_pred.csv` | 3158 | 2 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/notebooks/decoy_scores.csv` | 24015 | 3 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/notebooks/decoys.csv` | 24014 | 182 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/notebooks/human-ness_scores.csv` | 143318 | 3 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/notebooks/orig.csv` | 23758 | 163 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/notebooks/orig_scores.csv` | 23759 | 3 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/results_and_resources/ProtVec/protVec_100d_3grams.csv` | 9048 | 101 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/results_and_resources/selected_sequences/Mutation_scoring.csv` | 19 | 3 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/results_and_resources/selected_sequences/Test_set_score_distribution.csv` | 75631 | 2 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/results_and_resources/selected_sequences/cluster_marginal_distributions_source_data.csv` | 43 | 1 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/results_and_resources/selected_sequences/dendrogram.csv` | 126 | 4 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/results_and_resources/simulated_annealing/markov_chain_scores.csv` | 7623 | 3 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/trastuzumab_data/raw_data/anarci_check2.csv_H.csv` | 1 | 133 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/trastuzumab_data/raw_data/mHER_H3_AgNeg.csv` | 27539 | 6 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/trastuzumab_data/raw_data/mHER_H3_AgPos.csv` | 11300 | 6 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/trastuzumab_data/raw_data/trastuzumab_anarci.txt_H.csv` | 1 | 133 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/trastuzumab_data/results_and_resources/model_exp_scores.csv` | 56 | 3 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/trastuzumab_data/results_and_resources/model_training_scores.csv` | 29999 | 2 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/trastuzumab_data/results_and_resources/uncertainty_vs_pred.csv` | 3158 | 2 |

### 论文交付数据表

以下是实际归档补充数据的原始工作表/CSV；工作表计数包括表头、注释与多段布局，不是独立样本数。公式保留原字符串，未重算；展示第一条非空原始行便于识别入口，标题行不能误作科学表头。

| 补充数据工作表 | 非空行（含表头/注释） | 首条原始行 / 公式单元格 / 特殊码 |
| --- | --- | --- |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!Figure 5_source_data_file.xlsx#Figure 5A` | 47773 | Sequence_category, model, score / 0 / {} |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!Figure 5_source_data_file.xlsx#Figure 5B` | 47773 | Sequence_category, model, score / 0 / {} |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!Figure 5_source_data_file.xlsx#Figure 5C` | 47775 | Sequence_category, model, score / 0 / {} |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!Figure 6_source_data_file.xlsx#Figure 6A` | 46 | Source data for cluster 1 marginals plot / 0 / {} |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!Figure 6_source_data_file.xlsx#Figure 6B` | 75632 | Category, ordinal_regression_score / 0 / {} |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!Figure 6_source_data_file.xlsx#Figure 6C` | 7624 | Chain, iteration, score / 0 / {} |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!Figure 8_source_data_file.xlsx#Figure 8A` | 19 | Figure 6B Raw Data / 25 / {} |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!Figure 8_source_data_file.xlsx#Figure 8B` | 11 | Figure 6C Data, FB, FB, FB, FB / 0 / {} |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!SUPPLEMENTARY_Figure_S10_source_data_file.xlsx#Figure S10A` | 30000 | Label, Model assigned score / 0 / {} |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!SUPPLEMENTARY_Figure_S10_source_data_file.xlsx#Figure S10B` | 57 | Score / 0 / {} |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!SUPPLEMENTARY_Figure_S10_source_data_file.xlsx#Figure S10C` | 3159 | category, uncertainty / 0 / {} |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!SUPPLEMENTARY_Figure_S11_source_data_file.xlsx#Figure S11` | 127 | first_merged_id, second_merged_id, distances, num_obs_in_cluster / 0 / {} |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!SUPPLEMENTARY_Figure_S5_source_data_file.xlsx#Figure S5` | 1 | Figure S5 raw gels / 0 / {} |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!SUPPLEMENTARY_Figure_S7_source_data_file.xlsx#Figure S7` | 18 | Figure S7 raw data points / 69 / {} |

| 补充数据表 | parser 行数 | 首行原始内容（须按具体布局读） |
| --- | --- | --- |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!Figure 5_source_data_file.xlsx#Figure 5A` | 47772 | Sequence_category, model, score |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!Figure 5_source_data_file.xlsx#Figure 5B` | 47772 | Sequence_category, model, score |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!Figure 5_source_data_file.xlsx#Figure 5C` | 47774 | Sequence_category, model, score |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!Figure 6_source_data_file.xlsx#Figure 6A` | 45 | "Source data for cluster 1 marginals plot, , , , , , , , , " |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!Figure 6_source_data_file.xlsx#Figure 6B` | 75631 | Category, ordinal_regression_score |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!Figure 6_source_data_file.xlsx#Figure 6C` | 7623 | Chain, iteration, score |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!Figure 8_source_data_file.xlsx#Figure 8A` | 18 | "Figure 6B Raw Data, , , , , , , , , , , " |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!Figure 8_source_data_file.xlsx#Figure 8B` | 10 | "Figure 6C Data, , FB, , , FB, , , FB, , , FB, , " |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!SUPPLEMENTARY_Figure_S10_source_data_file.xlsx#Figure S10A` | 29999 | Label, Model assigned score |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!SUPPLEMENTARY_Figure_S10_source_data_file.xlsx#Figure S10B` | 56 | "Score, , " |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!SUPPLEMENTARY_Figure_S10_source_data_file.xlsx#Figure S10C` | 3158 | category, uncertainty |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!SUPPLEMENTARY_Figure_S11_source_data_file.xlsx#Figure S11` | 126 | first_merged_id, second_merged_id, distances, num_obs_in_cluster |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!SUPPLEMENTARY_Figure_S5_source_data_file.xlsx#Figure S5` | 0 | Figure S5 raw gels |
| `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!SUPPLEMENTARY_Figure_S7_source_data_file.xlsx#Figure S7` | 17 | "Figure S7 raw data points, , , , , , , , , , , , , , , , , , , , , , , , , " |

表行数包含重复条件、示例和派生副本，不求和作为独立生物对象。下表列名保持原始拼写；空表头以 `（空列名）` 标出，未修改文件。

### 字段说明

序列/样本名：变体和批次；reads/counts：测序读数/计数；binding category/ordinal label：排序类别，编码须以作者代码为准；off-rate：筛选/测定需分开，koff 小表示慢解离；KD：小规模验证浓度值、单位依实际表；encoded/embedding：模型输入；weight/checkpoint：计算模型，不作实验真值。 固定作者代码 encode_sequences.py 定义 y-tensor 四列：前两列为 >RH01、>RH02 指示，第三列类别 0=RH01、1=RH02、2=RH03，第四列为按类内/跨类读数频率计算的序列权重；这些不是 KD、kon 或 koff。未通过 torch.load/pickle 读取执行权重文件。 ProtVec d1…d100 为词向量维度，ANARCI Id/domain_no/编号位点字段为编号/物种比对计算结果；Sapiens score、human-ness、dendrogram 和模型/markov_chain 分数是计算输出，不能写为亲和力。带空列名或多段标题的辅助 CSV 保留原布局，不将自动第一行解析结果当已核实科学 schema。

| 原始表或 sheet | 字段（原始顺序） | 原始表示与特殊值 |
| --- | --- | --- |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/notebooks/decoy_scores.csv` | `id`, `chain`, `sapiens_score` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/notebooks/decoys.csv` | `Id`, `domain_no`, `hmm_species`, `chain_type`, `e-value`, `score`, `seqstart_index`, `seqend_index`, `identity_species`, `v_gene`, `v_identity`, `j_gene`, `j_identity`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `25`, `26`, `27`, `28`, `29`, `30`, `31`, `32`, `33`, `34`, `35`, `36`, `37`, `38`, `39`, `40`, `41`, `42`, `43`, `43A`, `43B`, `44`, `45`, `46`, `47`, `48`, `49`, `50`, `51`, `52`, `53`, `53A`, `53B`, `54`, `55`, `56`, `57`, `58`, `59`, `60`, `61`, `62`, `63`, `64`, `65`, `66`, `67`, `68`, `69`, `70`, `71`, `72`, `73`, `74`, `75`, `76`, `77`, `78`, `79`, `80`, `81`, `82`, `83`, `84`, `85`, `86`, `87`, `88`, `89`, `90`, `91`, `92`, `93`, `94`, `94A`, `95`, `96`, `97`, `98`, `99`, `100`, `101`, `102`, `103`, `103A`, `103B`, `103C`, `103D`, `103E`, `104`, `105`, `106`, `107`, `108`, `109`, `110`, `111`, `112`, `113`, `114`, `115`, `116`, `117`, `118`, `119`, `120`, `121`, `122`, `123`, `124`, `125`, `126`, `127`, `128`, `129`, `130`, `131`, `132`, `133`, `134`, `135`, `136`, `137`, `138`, `139`, `140`, `140A`, `140B`, `140C`, `140D`, `140E`, `141`, `141A`, `141B`, `141C`, `141D`, `141E`, `142`, `143`, `144`, `145`, `146`, `147`, `148`, `149` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：identity_species=24014, v_gene=24014, j_gene=24014 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/notebooks/human-ness_scores.csv` | `Sequence_category`, `model`, `score` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/notebooks/orig.csv` | `Id`, `domain_no`, `hmm_species`, `chain_type`, `e-value`, `score`, `seqstart_index`, `seqend_index`, `identity_species`, `v_gene`, `v_identity`, `j_gene`, `j_identity`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `25`, `26`, `27`, `28`, `29`, `30`, `31`, `32`, `33`, `34`, `35`, `36`, `37`, `38`, `39`, `40`, `41`, `42`, `43`, `43A`, `44`, `45`, `46`, `47`, `48`, `49`, `50`, `51`, `52`, `53`, `54`, `55`, `56`, `57`, `58`, `59`, `60`, `61`, `62`, `63`, `64`, `65`, `66`, `67`, `68`, `69`, `70`, `71`, `72`, `73`, `74`, `75`, `76`, `77`, `78`, `79`, `80`, `81`, `82`, `83`, `84`, `85`, `86`, `87`, `88`, `89`, `90`, `91`, `92`, `93`, `94`, `95`, `96`, `97`, `98`, `99`, `100`, `101`, `102`, `103`, `104`, `105`, `106`, `107`, `108`, `109`, `110`, `111`, `112`, `113`, `114`, `115`, `116`, `117`, `118`, `119`, `120`, `121`, `122`, `123`, `124`, `125`, `126`, `127`, `128`, `129`, `130`, `131`, `132`, `133`, `134`, `135`, `136`, `137`, `138`, `139`, `140`, `141`, `142`, `143`, `144`, `145`, `146`, `147`, `148`, `149` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：identity_species=23758, v_gene=23758, j_gene=23758 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/notebooks/orig_scores.csv` | `id`, `chain`, `sapiens_score` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/results_and_resources/ProtVec/protVec_100d_3grams.csv` | `words`, `d1`, `d2`, `d3`, `d4`, `d5`, `d6`, `d7`, `d8`, `d9`, `d10`, `d11`, `d12`, `d13`, `d14`, `d15`, `d16`, `d17`, `d18`, `d19`, `d20`, `d21`, `d22`, `d23`, `d24`, `d25`, `d26`, `d27`, `d28`, `d29`, `d30`, `d31`, `d32`, `d33`, `d34`, `d35`, `d36`, `d37`, `d38`, `d39`, `d40`, `d41`, `d42`, `d43`, `d44`, `d45`, `d46`, `d47`, `d48`, `d49`, `d50`, `d51`, `d52`, `d53`, `d54`, `d55`, `d56`, `d57`, `d58`, `d59`, `d60`, `d61`, `d62`, `d63`, `d64`, `d65`, `d66`, `d67`, `d68`, `d69`, `d70`, `d71`, `d72`, `d73`, `d74`, `d75`, `d76`, `d77`, `d78`, `d79`, `d80`, `d81`, `d82`, `d83`, `d84`, `d85`, `d86`, `d87`, `d88`, `d89`, `d90`, `d91`, `d92`, `d93`, `d94`, `d95`, `d96`, `d97`, `d98`, `d99`, `d100` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/results_and_resources/selected_sequences/Mutation_scoring.csv` | 原始首行/标题（未认可为科学表头）：`Mutation`, `forward_score`, `reverse_scores` | 19 行宽度与首行不齐；按原多段/不齐行布局阅读，不报告位置列统计。 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/results_and_resources/selected_sequences/Test_set_score_distribution.csv` | `Category`, `ordinal_regression_score` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/results_and_resources/selected_sequences/cluster_marginal_distributions_source_data.csv` | 原始首行/标题（未认可为科学表头）：`Source data for cluster 1 marginals plot` | 42 行宽度与首行不齐；按原多段/不齐行布局阅读，不报告位置列统计。 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/results_and_resources/selected_sequences/dendrogram.csv` | `first_merged_id`, `second_merged_id`, `distances`, `num_obs_in_cluster` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/results_and_resources/simulated_annealing/markov_chain_scores.csv` | `Chain`, `iteration`, `score` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/trastuzumab_data/raw_data/anarci_check2.csv_H.csv` | `Id`, `domain_no`, `hmm_species`, `chain_type`, `e-value`, `score`, `seqstart_index`, `seqend_index`, `identity_species`, `v_gene`, `v_identity`, `j_gene`, `j_identity`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `25`, `26`, `27`, `28`, `29`, `30`, `31`, `32`, `33`, `34`, `35`, `36`, `37`, `38`, `39`, `40`, `41`, `42`, `43`, `44`, `45`, `46`, `47`, `48`, `49`, `50`, `51`, `52`, `52A`, `53`, `54`, `55`, `56`, `57`, `58`, `59`, `60`, `61`, `62`, `63`, `64`, `65`, `66`, `67`, `68`, `69`, `70`, `71`, `72`, `73`, `74`, `75`, `76`, `77`, `78`, `79`, `80`, `81`, `82`, `82A`, `82B`, `82C`, `83`, `84`, `85`, `86`, `87`, `88`, `89`, `90`, `91`, `92`, `93`, `94`, `95`, `96`, `97`, `98`, `99`, `100`, `100A`, `100B`, `100C`, `101`, `102`, `103`, `104`, `105`, `106`, `107`, `108`, `109`, `110`, `111`, `112`, `113` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：identity_species=1, v_gene=1, j_gene=1 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/trastuzumab_data/raw_data/mHER_H3_AgNeg.csv` | `（空列名）`, `Count`, `Fraction`, `NucSeq`, `AASeq`, `AgClass` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/trastuzumab_data/raw_data/mHER_H3_AgPos.csv` | `（空列名）`, `Count`, `Fraction`, `NucSeq`, `AASeq`, `AgClass` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/trastuzumab_data/raw_data/trastuzumab_anarci.txt_H.csv` | `Id`, `domain_no`, `hmm_species`, `chain_type`, `e-value`, `score`, `seqstart_index`, `seqend_index`, `identity_species`, `v_gene`, `v_identity`, `j_gene`, `j_identity`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `25`, `26`, `27`, `28`, `29`, `30`, `31`, `32`, `33`, `34`, `35`, `36`, `37`, `38`, `39`, `40`, `41`, `42`, `43`, `44`, `45`, `46`, `47`, `48`, `49`, `50`, `51`, `52`, `52A`, `53`, `54`, `55`, `56`, `57`, `58`, `59`, `60`, `61`, `62`, `63`, `64`, `65`, `66`, `67`, `68`, `69`, `70`, `71`, `72`, `73`, `74`, `75`, `76`, `77`, `78`, `79`, `80`, `81`, `82`, `82A`, `82B`, `82C`, `83`, `84`, `85`, `86`, `87`, `88`, `89`, `90`, `91`, `92`, `93`, `94`, `95`, `96`, `97`, `98`, `99`, `100`, `100A`, `100B`, `100C`, `101`, `102`, `103`, `104`, `105`, `106`, `107`, `108`, `109`, `110`, `111`, `112`, `113` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：identity_species=1, v_gene=1, j_gene=1 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/trastuzumab_data/results_and_resources/model_exp_scores.csv` | `Score`, `（空列名）`, `（空列名）` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：（空列名）=110 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/trastuzumab_data/results_and_resources/model_training_scores.csv` | `Label`, `Model assigned score` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-v0.0.1.zip!jlparkI-RESP-52b818a/trastuzumab_data/results_and_resources/uncertainty_vs_pred.csv` | `category`, `uncertainty` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/notebooks/decoy_scores.csv` | `id`, `chain`, `sapiens_score` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/notebooks/decoys.csv` | `Id`, `domain_no`, `hmm_species`, `chain_type`, `e-value`, `score`, `seqstart_index`, `seqend_index`, `identity_species`, `v_gene`, `v_identity`, `j_gene`, `j_identity`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `25`, `26`, `27`, `28`, `29`, `30`, `31`, `32`, `33`, `34`, `35`, `36`, `37`, `38`, `39`, `40`, `41`, `42`, `43`, `43A`, `43B`, `44`, `45`, `46`, `47`, `48`, `49`, `50`, `51`, `52`, `53`, `53A`, `53B`, `54`, `55`, `56`, `57`, `58`, `59`, `60`, `61`, `62`, `63`, `64`, `65`, `66`, `67`, `68`, `69`, `70`, `71`, `72`, `73`, `74`, `75`, `76`, `77`, `78`, `79`, `80`, `81`, `82`, `83`, `84`, `85`, `86`, `87`, `88`, `89`, `90`, `91`, `92`, `93`, `94`, `94A`, `95`, `96`, `97`, `98`, `99`, `100`, `101`, `102`, `103`, `103A`, `103B`, `103C`, `103D`, `103E`, `104`, `105`, `106`, `107`, `108`, `109`, `110`, `111`, `112`, `113`, `114`, `115`, `116`, `117`, `118`, `119`, `120`, `121`, `122`, `123`, `124`, `125`, `126`, `127`, `128`, `129`, `130`, `131`, `132`, `133`, `134`, `135`, `136`, `137`, `138`, `139`, `140`, `140A`, `140B`, `140C`, `140D`, `140E`, `141`, `141A`, `141B`, `141C`, `141D`, `141E`, `142`, `143`, `144`, `145`, `146`, `147`, `148`, `149` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：identity_species=24014, v_gene=24014, j_gene=24014 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/notebooks/human-ness_scores.csv` | `Sequence_category`, `model`, `score` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/notebooks/orig.csv` | `Id`, `domain_no`, `hmm_species`, `chain_type`, `e-value`, `score`, `seqstart_index`, `seqend_index`, `identity_species`, `v_gene`, `v_identity`, `j_gene`, `j_identity`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `25`, `26`, `27`, `28`, `29`, `30`, `31`, `32`, `33`, `34`, `35`, `36`, `37`, `38`, `39`, `40`, `41`, `42`, `43`, `43A`, `44`, `45`, `46`, `47`, `48`, `49`, `50`, `51`, `52`, `53`, `54`, `55`, `56`, `57`, `58`, `59`, `60`, `61`, `62`, `63`, `64`, `65`, `66`, `67`, `68`, `69`, `70`, `71`, `72`, `73`, `74`, `75`, `76`, `77`, `78`, `79`, `80`, `81`, `82`, `83`, `84`, `85`, `86`, `87`, `88`, `89`, `90`, `91`, `92`, `93`, `94`, `95`, `96`, `97`, `98`, `99`, `100`, `101`, `102`, `103`, `104`, `105`, `106`, `107`, `108`, `109`, `110`, `111`, `112`, `113`, `114`, `115`, `116`, `117`, `118`, `119`, `120`, `121`, `122`, `123`, `124`, `125`, `126`, `127`, `128`, `129`, `130`, `131`, `132`, `133`, `134`, `135`, `136`, `137`, `138`, `139`, `140`, `141`, `142`, `143`, `144`, `145`, `146`, `147`, `148`, `149` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：identity_species=23758, v_gene=23758, j_gene=23758 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/notebooks/orig_scores.csv` | `id`, `chain`, `sapiens_score` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/results_and_resources/ProtVec/protVec_100d_3grams.csv` | `words`, `d1`, `d2`, `d3`, `d4`, `d5`, `d6`, `d7`, `d8`, `d9`, `d10`, `d11`, `d12`, `d13`, `d14`, `d15`, `d16`, `d17`, `d18`, `d19`, `d20`, `d21`, `d22`, `d23`, `d24`, `d25`, `d26`, `d27`, `d28`, `d29`, `d30`, `d31`, `d32`, `d33`, `d34`, `d35`, `d36`, `d37`, `d38`, `d39`, `d40`, `d41`, `d42`, `d43`, `d44`, `d45`, `d46`, `d47`, `d48`, `d49`, `d50`, `d51`, `d52`, `d53`, `d54`, `d55`, `d56`, `d57`, `d58`, `d59`, `d60`, `d61`, `d62`, `d63`, `d64`, `d65`, `d66`, `d67`, `d68`, `d69`, `d70`, `d71`, `d72`, `d73`, `d74`, `d75`, `d76`, `d77`, `d78`, `d79`, `d80`, `d81`, `d82`, `d83`, `d84`, `d85`, `d86`, `d87`, `d88`, `d89`, `d90`, `d91`, `d92`, `d93`, `d94`, `d95`, `d96`, `d97`, `d98`, `d99`, `d100` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/results_and_resources/selected_sequences/Mutation_scoring.csv` | 原始首行/标题（未认可为科学表头）：`Mutation`, `forward_score`, `reverse_scores` | 19 行宽度与首行不齐；按原多段/不齐行布局阅读，不报告位置列统计。 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/results_and_resources/selected_sequences/Test_set_score_distribution.csv` | `Category`, `ordinal_regression_score` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/results_and_resources/selected_sequences/cluster_marginal_distributions_source_data.csv` | 原始首行/标题（未认可为科学表头）：`Source data for cluster 1 marginals plot` | 42 行宽度与首行不齐；按原多段/不齐行布局阅读，不报告位置列统计。 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/results_and_resources/selected_sequences/dendrogram.csv` | `first_merged_id`, `second_merged_id`, `distances`, `num_obs_in_cluster` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/results_and_resources/simulated_annealing/markov_chain_scores.csv` | `Chain`, `iteration`, `score` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/trastuzumab_data/raw_data/anarci_check2.csv_H.csv` | `Id`, `domain_no`, `hmm_species`, `chain_type`, `e-value`, `score`, `seqstart_index`, `seqend_index`, `identity_species`, `v_gene`, `v_identity`, `j_gene`, `j_identity`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `25`, `26`, `27`, `28`, `29`, `30`, `31`, `32`, `33`, `34`, `35`, `36`, `37`, `38`, `39`, `40`, `41`, `42`, `43`, `44`, `45`, `46`, `47`, `48`, `49`, `50`, `51`, `52`, `52A`, `53`, `54`, `55`, `56`, `57`, `58`, `59`, `60`, `61`, `62`, `63`, `64`, `65`, `66`, `67`, `68`, `69`, `70`, `71`, `72`, `73`, `74`, `75`, `76`, `77`, `78`, `79`, `80`, `81`, `82`, `82A`, `82B`, `82C`, `83`, `84`, `85`, `86`, `87`, `88`, `89`, `90`, `91`, `92`, `93`, `94`, `95`, `96`, `97`, `98`, `99`, `100`, `100A`, `100B`, `100C`, `101`, `102`, `103`, `104`, `105`, `106`, `107`, `108`, `109`, `110`, `111`, `112`, `113` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：identity_species=1, v_gene=1, j_gene=1 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/trastuzumab_data/raw_data/mHER_H3_AgNeg.csv` | `（空列名）`, `Count`, `Fraction`, `NucSeq`, `AASeq`, `AgClass` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/trastuzumab_data/raw_data/mHER_H3_AgPos.csv` | `（空列名）`, `Count`, `Fraction`, `NucSeq`, `AASeq`, `AgClass` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/trastuzumab_data/raw_data/trastuzumab_anarci.txt_H.csv` | `Id`, `domain_no`, `hmm_species`, `chain_type`, `e-value`, `score`, `seqstart_index`, `seqend_index`, `identity_species`, `v_gene`, `v_identity`, `j_gene`, `j_identity`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `25`, `26`, `27`, `28`, `29`, `30`, `31`, `32`, `33`, `34`, `35`, `36`, `37`, `38`, `39`, `40`, `41`, `42`, `43`, `44`, `45`, `46`, `47`, `48`, `49`, `50`, `51`, `52`, `52A`, `53`, `54`, `55`, `56`, `57`, `58`, `59`, `60`, `61`, `62`, `63`, `64`, `65`, `66`, `67`, `68`, `69`, `70`, `71`, `72`, `73`, `74`, `75`, `76`, `77`, `78`, `79`, `80`, `81`, `82`, `82A`, `82B`, `82C`, `83`, `84`, `85`, `86`, `87`, `88`, `89`, `90`, `91`, `92`, `93`, `94`, `95`, `96`, `97`, `98`, `99`, `100`, `100A`, `100B`, `100C`, `101`, `102`, `103`, `104`, `105`, `106`, `107`, `108`, `109`, `110`, `111`, `112`, `113` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：identity_species=1, v_gene=1, j_gene=1 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/trastuzumab_data/results_and_resources/model_exp_scores.csv` | `Score`, `（空列名）`, `（空列名）` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：（空列名）=110 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/trastuzumab_data/results_and_resources/model_training_scores.csv` | `Label`, `Model assigned score` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz!RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942/trastuzumab_data/results_and_resources/uncertainty_vs_pred.csv` | `category`, `uncertainty` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |

### 数据示例

来自 `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip!Figure 6_source_data_file.xlsx#Figure 6B` 的第一条真实非空数据行：

| 原始字段 | 原始值 |
| --- | --- |
| Category | RH03 |
| ordinal_regression_score | 6.00886011123657 |

这是该原始表的一条记录；粒度按前述定义，不把结构表示、重复或归档成员当独立抗体。

## PDB 数据库

主文明确引用 5XXY 与 5X8L 作为 atezolizumab Fab / PD-L1 的亲本结构依据。它们是全库共享参考，不是这些重链变体的逐行结构。所有 polymer entity 和完整坐标保留，未把 Fab 与 scFv 构建体当完全相同。

本次审计接受 2 个唯一锚点，每个都有 RCSB 完整 entry FASTA 与完整 mmCIF（原样 .cif 或 .cif.gz），共 4 个文件 / 2204072 bytes。逐对检查 entry ID、非空 _atom_site 及 canonical polymer 序列一致。FASTA 保留 RCSB entity ID、原始头和序列，没有从坐标重建序列；坐标保留完整原文件。author/label chain 与 entity 的原始映射在 FASTA 头及 mmCIF `_struct_asym`、`_entity_poly`、`_atom_site.auth_asym_id` 中，不臆造链角色。

文件路径为 `pdb/sequences/rcsb_pdb_<PDB>.fasta`、`pdb/structures/<PDB>.cif.gz` 或 `<PDB>.cif`；复用已有完整未压缩 RCSB 原文件时不重新压缩。确定性 inventory SHA-256：`a98239dbec1188f67d39a20b3294673f1c0acd19d4afc1057794d10298f7be59`；算法为按相对路径排序，逐文件组成 `path<TAB>bytes<TAB>sha256<LF>`（UTF-8）再计算 SHA-256。

| PDB | FASTA bytes / SHA-256 | mmCIF bytes / SHA-256 |
| --- | --- | --- |
| 5X8L | 912 / `8ba3d30eb1fe1236dd3acab398a63dfab6ab3a9a65d726668ff271698134821a` | 1045081 / `e770699e0d51f9cfdbea3b9c859a6c0a5bc468039e002fc0fe5d282dde34d97a` |
| 5XXY | 810 / `f358849a7c174116db3c856da62bdb7e15784d6c5fce3238369d7b0f8bf05456` | 1157269 / `fcd49de058712ef7a88c4d4e5573b73d88b3750aade0aed9b51086b71ec3848f` |

## 使用方式

由调用者将 `dataset_root` 赋为该 source_version 目录。以下仅读原始入口，不清洗、换算或修补 raw。

```python
import zipfile
with zipfile.ZipFile(dataset_root / "RESP/RESP-v0.0.1.zip") as archive:
    print(archive.namelist()[:5])
```

## 采集过程记录

2026-09-18：取得固定 Zenodo 记录的 RESP_data.zip、v0.0.1 代码 ZIP 和后续固定 Git tree；2.11 GB 数据包恢复后核对官方 MD5。全量读取 nested TAR/GZIP 和六个 FASTQ.GZ，仅记录上游 ZIP 的零字节空根目录例外，不执行编码数组或权重。ProtVec 实为 tab，其他多段/不齐行 CSV 保留布局；验证例子来自 Figure 6B 原 Source Data。保留 All Rights Reserved 与元数据 other-open 的未消解边界。

2026-10-14：发布 2026-09-18 follow-up 已核验的 ENA PRJNA813220 交付。6 个 FASTQ.GZ 共 201.40 MiB（211,184,909 bytes），逐文件核对 SHA-256、gzip/FASTQ 结构和记录数；与 `RESP_data.zip` 内对应 reads 的序列、质量值及顺序一致，读名和 gzip 字节不同。目录以 `ENA_PRJNA813220/` 原子移入正式 source version，原 R29 follow-up staging 随后为空并已清理。

2026-09-18：全部正式 payload 按来源身份、大小和官方/本地 checksum 独立验收；原始表与附件已读取，FASTA 和完整 mmCIF 逐对核验。工作 README 同步共享版本，规定的 markdownlint 为零错误后发布。具体 API、原始下载日志、失败和重试记录保存在共享本批采集目录，未向任何作者发送消息或申请。

2026-09-18：复核 skill 版本规则，将不符合命名规则的 `zenodo-15758312` 原子重命名为 `snapshot-2025-06-27`。同步来源配置、PDB 配置、工作与共享 README 及当前结构化验收/发布记录；旧文档和原验收记录保留在 runs 的 version-migration-history。修订前后按相对路径、字节数和 SHA-256 比对全部科学文件，内容保持原样；修订 README 使用规定的 markdownlint 配置验收。

2026-09-18：README 工作稿迁入由 developer.user 定位的个人 docs/readme。初版采集记录混用了跨来源的通用描述，本次按实际来源、下载与重试记录修订。论文及附件命名补齐平台和版本。以下名称变更均核对原文件字节数及 SHA-256，内容未改写；原始文件名与下载 URL 保留在采集记录中。

- `articles/RESP_2023-01-28_EuropePMC.xml` → `articles/RESP_2023-01-28_EuropePMC-published.xml`；191818 bytes，SHA-256 `6c292197de45bd1fe7e6093a75b2eef1ad6ba7b9a50f3b3dc9f53d590fc358a4`。
- `articles/RESP_2023-01-28_publisher.pdf` → `articles/RESP_2023-01-28_NatureCommunications-published.pdf`；2347435 bytes，SHA-256 `f8afb703047570a4acb64cc751490abcc0de589f479af6ae0b334191ddbdf0e0`。
- `articles/RESP_2023-01-28_supplement-1.pdf` → `articles/RESP_2023-01-28_NatureCommunications-published-supplement-1.pdf`；5489337 bytes，SHA-256 `ed4e3cccb7ac7243b8ce8613b4fbb7a2b513fc0983bcc304d5b57bf770e210bb`。
- `articles/RESP_2023-01-28_supplement-2.pdf` → `articles/RESP_2023-01-28_NatureCommunications-published-supplement-2.pdf`；375199 bytes，SHA-256 `fbf700b0cf735a32ecee04bd04c70f701b5e9a152144cfbd96266d7ccc701bcc`。
- `articles/RESP_2023-01-28_supplement-3.zip` → `articles/RESP_2023-01-28_NatureCommunications-published-supplement-3.zip`；7061439 bytes，SHA-256 `267ed091c9b8593e859724f0bf3172c49975e4efcbb4873132e916b1b9f5632c`。

旧文档和结构化报告保存在共享 runs/documentation-reorganization；修订后本地与共享 README 同步并执行规定的 Markdownlint。

- 上游原始名称 `fullTextXML`；入口 <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9884274/fullTextXML>。
- 上游原始名称 `s41467-023-36028-8.pdf`；入口 <https://www.nature.com/articles/s41467-023-36028-8.pdf>。
- 上游原始名称 `41467_2023_36028_MOESM1_ESM.pdf`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-023-36028-8/MediaObjects/41467_2023_36028_MOESM1_ESM.pdf>。
- 上游原始名称 `41467_2023_36028_MOESM2_ESM.pdf`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-023-36028-8/MediaObjects/41467_2023_36028_MOESM2_ESM.pdf>。
- 上游原始名称 `41467_2023_36028_MOESM3_ESM.zip`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-023-36028-8/MediaObjects/41467_2023_36028_MOESM3_ESM.zip>。

## 参考文献

- [数据源固定版本/入口](https://zenodo.org/records/15758312)
- [数据源固定版本/入口](https://github.com/Wang-lab-UCSD/RESP)
- [归档主文 DOI](https://doi.org/10.1038/s41467-023-36028-8)
- [primary full-text XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9884274/fullTextXML)
- [primary PDF](https://www.nature.com/articles/s41467-023-36028-8.pdf)
- [Supplementary Information](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-023-36028-8/MediaObjects/41467_2023_36028_MOESM1_ESM.pdf)
- [Reporting Summary](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-023-36028-8/MediaObjects/41467_2023_36028_MOESM2_ESM.pdf)
- [Source Data (download ZIP)](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-023-36028-8/MediaObjects/41467_2023_36028_MOESM3_ESM.zip)
- [ENA PRJNA813220](https://www.ebi.ac.uk/ena/browser/view/PRJNA813220)
- [PDB 5XXY（条目含原始结构论文）](https://www.rcsb.org/structure/5XXY)
- [PDB 5X8L（条目含原始结构论文）](https://www.rcsb.org/structure/5X8L)

## 其他

### 完整性与验收

| payload | 大小 | SHA-256 |
| --- | --- | --- |
| `RESP/RESP-v0.0.1.zip` | 38.63 MiB（40,505,540 bytes） | `5ed01e18640c9109cbfe90ca4956890780214268c387e9b8c65617f47198aedc` |
| `RESP/RESP_data.zip` | 1.96 GiB（2,105,401,929 bytes） | `08f471490b74b79361097607f0de1a65f9ccfef9c65596d6cbe9cc42641e327c` |
| `RESP/RESP-2621454a24804b131c6fa4979dc8dd46b7a8b942.tar.gz` | 38.55 MiB（40,418,174 bytes） | `eb39eff0cb1d2ffd2de45ec2cb98dcb1abd3ec70115b0fc565a8fdd231e759d7` |
| `ENA_PRJNA813220/SRR18256858_1.fastq.gz` | 28.71 MiB（30,102,655 bytes） | `53c4e1da3980858601be6ebfc3664a528f3f7d762fc5dd2b0743d56ccdc8df7e` |
| `ENA_PRJNA813220/SRR18256858_2.fastq.gz` | 39.24 MiB（41,148,747 bytes） | `5b4e6e19e042929943e0b2a484153826dec11fa5eb44cf637d9159a76f62b4e4` |
| `ENA_PRJNA813220/SRR18256859_1.fastq.gz` | 28.31 MiB（29,680,560 bytes） | `e5ff9a05f1bf94df5ca9d7c0cc0d963fe1d2b344b4be2bc0edb7f38e1a88f88b` |
| `ENA_PRJNA813220/SRR18256859_2.fastq.gz` | 33.60 MiB（35,235,839 bytes） | `826292aa8b43697034374ff40391a2231053fda2d870eda2be972b53b3d28303` |
| `ENA_PRJNA813220/SRR18256860_1.fastq.gz` | 31.74 MiB（33,286,273 bytes） | `42dbebafce865da298ef9eb3e9a96c2ae8c91aca568c0db4f1cbe5fa9cc5f131` |
| `ENA_PRJNA813220/SRR18256860_2.fastq.gz` | 39.80 MiB（41,730,835 bytes） | `305e97e368dd85766e1a5ad14f66d690d08127d3d1a4e9804faf65a4be2ff63b` |

原始 payload 合计 2.23 GiB（2,397,510,552 bytes）；inventory SHA-256 `7800d9723dc3c981bef5b697d3948c735b099ca31544d2da1a52192267087117`（与 PDB 同一算法）。归档成员全部读取；统计与 API/验收报告保存于共享 runs，不作为 raw 附属 manifest 发布。每个文件与论文/PDB 身份均可重验，不执行交付包中的训练代码或模型反序列化。

### 许可和再分发边界

Zenodo 元数据 other-open 不等于明确的再分发授权；固定作者 Git tree 和正式 v0.0.1 ZIP 的 LICENSE 均仅写 Copyright 2021 The Regents of the University of California San Diego. All Rights Reserved.，未给出 MIT/BSD/Apache 等许可条款。数据 ZIP 没有另附 LICENSE/README，元数据 other-open 无法消解代码包的保留权利声明；不把公开下载解释为统一开放许可。论文 CC BY 4.0 只覆盖论文，其 Source Data 依原页面声明；捆绑 Mason/cAbRep 等上游权利与引用分别保留。

### 公开范围对照

| 范围 | 本次证据与状态 |
| --- | --- |
| 已取得的公开部分 | 两个公开 Zenodo ZIP、固定作者 Git tree、公开论文/补充/Source Data、亲本结构，以及 ENA PRJNA813220 的 3 个 run、6 个双端 FASTQ.GZ。ENA 与 ZIP 内对应 reads 内容一致，但交付字节不同；两份均按实际来源保留。未取得 NCBI `.sra` 容器。 |
| 论文/来源未公开或未取得部分 | 仅按本文具体缺口报告；未访问限制不冒称完成。 |
| processed / release | 未生成；本层仅上游原样输入。 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-14；许可边界待确认）：Zenodo 元数据的 `other-open` 与代码包中的 All Rights Reserved 声明没有给出覆盖整个数据交付的明确统一许可。当前按来源证据保留和核验文件，不将其解释为开放商用或任意再分发授权；下一步需由来源方或正式许可文本明确各对象的使用与再分发条件后关闭本项。
