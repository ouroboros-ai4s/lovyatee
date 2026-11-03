---
tags:
  - context
---

# 抗原—抗体亲和力数据：Stage 1 来源盘点

- 原始文件：docs/document.pdf
- 原始标题：抗原抗体亲和力数据：Stage 1 来源盘点
- 原始日期：2026-10-23
- PDF 页数：13
- Markdown 转存日期：2026-10-28

> 本文件是 PDF 的 UTF-8 中文 Markdown 转录。PDF 中的表格和图示已改写为文本；原 PDF 保留为视觉原始文件。

## 范围

本文盘点公开的抗体—抗原亲和力数据集、来源关系、下载位置、测量类型、结构信息和第一阶段 P1/P2 优先级。

PDF 共列出 20 个来源族：

| # | 来源 | PDF 中给出的规模或内容 |
| ---: | --- | --- |
| 1 | ASD / AgAb DB | 1,177,819 条记录；29 个来源 |
| 2 | ANDD | 48,683 条序列；9,557 个亲和力值；2,271 条预测记录 |
| 3 | AbBiBench | 超过 184,500 个测量值；HF 表 215,699 行 |
| 4 | FLAb / FLAb2 binding | 241 个数据集；132 个结合数据集 |
| 5 | AbRank | 超过 380,000 个 assay；其中 342,357 条与 FLAb 相关 |
| 6 | AB-Bind | 1,101 个突变体；32 个复合物 |
| 7 | SKEMPI 2.0 | 7,085 个突变 |
| 8 | SAbDab / SAbDab2 | 抗体—抗原结构和亲和力记录 |
| 9 | Guest antibody benchmark | 67 个结构案例；51 个亲和力案例 |
| 10 | AlphaBind public experiments | 约 750 万条公开实验记录 |
| 11 | MIT-LL AlphaSeq | 104,972 个抗体 |
| 12 | AbDesign 1.0 | 658 个突变体 + 14 个 WT 对照 = 672 个变体 |
| 13 | AbDesign 2.0 | 576 个单点突变；346 个产生的变体 |
| 14 | HER2-aff-large / Buzz | 超过 524,000 个变体 |
| 15 | AVIDa-hTNFa | 5,580 行有标签记录 |
| 16 | TDC AntibodyAff | 493 个 pair；431 个抗体；401 个抗原 |
| 17 | Akbar SAbDab Kd CSV | 500 个抗体 |
| 18 | MochiBind sampled data | CSV、pair 文件和 pairwise 标签 |
| 19 | Graphinity | 942,723 个 FoldX 值；20,829 个 Flex ddG 值 |
| 20 | ANTIPASTI | 数据记录和预测亲和力记录 |

## PDF 中的来源关系

- SAbDab → TDC → CSV。
- SAbDab → Akbar CSV。
- AB-Bind 和 SKEMPI 提供突变与亲和力记录。
- AbBiBench、AbRank 和 FLAb 属于汇编或基准层。
- AlphaBind、AlphaSeq、MochiBind、Graphinity 和 ANTIPASTI 通过公开实验、采样 pair、结构计算或预测层相互关联。
- AbDesign 和 Buzz 提供实验或计算标签不同的抗体变体数据。

## 测量与标签轴

PDF 中出现的字段类型包括：

- Kd、kon、koff；
- ΔΔG；
- ELISA ratio；
- enrichment；
- IC50；
- escape；
- bind / no-bind；
- assay 标签；
- FoldX 和 Rosetta 计算值；
- WT / mutant 状态。

这些字段含义并不相同，不能在未按来源和 assay 分层的情况下直接视为同一个训练目标。

## 来源卡片

### ASD / AgAb DB

- 版本：v2.0。
- 规模：1,177,819 条记录，来自 29 个来源。
- 标签：Kd、ΔΔG、IC50、ELISA、enrichment 和二元结合标签。
- 访问方式：Google Drive / Colab。
- 许可：CC BY-NC 4.0。
- 相关来源：AB-Bind、AbDesign、AbBiBench、AlphaSeq、Buzz、FLAb。

### ANDD

- 版本：Zenodo v2，2026-01-05。
- 规模：48,683 条序列、9,557 个亲和力值、2,271 个预测值。
- 主要字段：Kd、重链/轻链、PDB、Predicted_or_Not、provenance。
- 文件：XLSX、QC PDF、PDB ZIP。
- 许可：CC BY 4.0。
- 相关来源：SAbDab、AB-Bind、SKEMPI、PDBbind、ANTIPASTI。

### AbBiBench

- 来源：arXiv v2 和 Hugging Face。
- 规模：超过 184,500 个测量值；HF 表 215,699 行。
- 字段：log Kd、log enrichment、重链/轻链、binding_score。
- 相关来源：ASD。

### FLAb / FLAb2 binding

- 来源：GitHub main 和 README。
- 规模：241 个数据集、132 个 binding 数据集。
- 字段：Kd、IC50、escape、预测 Kd、重链/轻链序列、fitness。
- 相关来源：AbRank。

### AbRank

- 来源：arXiv v2、GitHub 和 Kaggle 材料。
- 规模：超过 380,000 个 assay；342,357 条 FLAb 相关记录。
- 字段：Kd、IC50、escape、抗体—抗原 pairwise ranking。
- 许可：CC BY-NC 4.0。

### AB-Bind

- 来源：GitHub master；CSV、XLSX、PDB。
- 规模：32 个复合物中的 1,101 个突变体。
- 主要标签：ΔΔG，带 WT / mutant 状态。
- 相关来源：SKEMPI、ASD。

### SKEMPI 2.0

- 版本：v2.0。
- 规模：7,085 个突变。
- 内容：WT / mutant 亲和力记录和 PPI 数据。
- 相关来源：AB-Bind。

### SAbDab / SAbDab2

- 抗体—抗原结构数据库，并包含亲和力相关记录。
- 相关来源：TDC、ANTIPASTI、ANDD、Graphinity 等。

### Guest antibody benchmark

- 来源：GitHub master。
- 规模：67 个结构案例、51 个亲和力案例。
- 内容：结合态/未结合态抗体结构、抗原 PDB 结构、Kd、ΔΔG。
- 相关来源：SAbDab。

### AlphaBind public experiments

- 来源：与 AlphaSeq 相关的公开实验。
- 规模：约 750 万条记录。
- 抗体格式：scFv、VHH。
- 相关来源：MochiBind、ASD、AlphaSeq。

### MIT-LL AlphaSeq

- 来源：Zenodo v1.0.0 和更新版本。
- 规模：104,972 个抗体。
- 格式：scFv 与肽靶标，带 binding score。
- 相关来源：FLAb、AbBiBench、A-Alpha、AlphaSeq。

### AbDesign 1.0

- 规模：658 个突变体 + 14 个 WT 对照 = 672 个变体。
- 标签：WT / mutant、ELISA binding ratio。
- 结构范围：7 个抗原上的 14 个复合物。
- 相关来源：AB-Bind、SKEMPI、ASD。

### AbDesign 2.0

- 规模：576 个单点突变、346 个产生的变体。
- 字段：Kd、kon、koff、developability profiles，以及结构关联系统。

### HER2-aff-large / Buzz

- 来源：Zenodo v2 和 GitHub 材料。
- 规模：超过 524,000 个变体。
- 标签：BLI 和 developability 相关值。
- 重点：CDR-H3 和特定靶标变体库。

### AVIDa-hTNFa

- 来源：Hugging Face 数据集。
- 规模：5,580 行有标签记录。
- 字段：VHH sequence、antigen label、bind/no-bind。
- 许可：CC BY-NC 4.0。

### TDC AntibodyAff

- 规模：493 个 pair、431 个抗体、401 个抗原。
- 来源关系：通过 TDC loader/SDK 访问 SAbDab affinity 数据。

### Akbar SAbDab Kd CSV

- 来源：Zenodo v1，2024-07-29。
- 规模：500 个抗体。
- 主要标签：Kd。
- 相关来源：SAbDab、TDC。

### MochiBind sampled data

- 来源：GitHub main。
- 内容：CSV、pair 文件、pairwise 标签和采样的抗体—抗原 pair。
- 相关来源：AlphaBind、MIT-LL AlphaSeq。

### Graphinity synthetic and experimental subsets

- 来源：GitHub、Zenodo 15384945、OPIG PDB。
- 主要标签：FoldX、Flex ddG、WT / mutant。
- 规模：942,723 个 FoldX 值、20,829 个 Flex ddG 值。
- 相关来源：AB-Bind、HER2 相关数据、SAbDab。

### ANTIPASTI

- 来源：Mendeley v1，2024-10-16。
- 内容：SAbDab 关联记录和预测亲和力值。
- 结构注释：Chothia 编号和 PDB 关联信息。
- 相关来源：ANDD、SAbDab。

## PDF 中的采集与复现计划

1. 记录 GitHub 或 Hugging Face URL 及 commit/revision。
2. 记录下载文件的 SHA-256。
3. 维护 source_inventory.csv / .json。
4. 维护 source_relationships.csv。
5. 使用 SVG/TikZ 生成图，并使用 Python 完成支持分析。
6. 使用 antibody、antigen、affinity、public dataset、database、benchmark、download、FLAb、AbDesign、AlphaBind、AlphaSeq 等关键词检索公开来源。

## PDF 中列出的参考链接

1. ASD / AgAb DB：<https://naturalantibody.com/asd/>
2. ANDD：<https://www.nature.com/articles/s41597-026-06878-0>
3. AbBiBench：<https://arxiv.org/html/2506.04235v2>
4. FLAb：<https://raw.githubusercontent.com/Graylab/FLAb/main/data/binding/README.md>
5. AbRank：<https://arxiv.org/html/2506.17857v2>
6. AB-Bind：<https://doi.org/10.1002/pro.2829>
7. SKEMPI 2.0：<https://life.bsc.es/pid/skempi2/>
8. SAbDab：<https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabdab>
9. Guest benchmark：<https://pmc.ncbi.nlm.nih.gov/articles/PMC8178184/>
10. AlphaBind：<https://pmc.ncbi.nlm.nih.gov/articles/PMC12296056/>
11. MIT-LL AlphaSeq：<https://zenodo.org/records/5095284>
12. AbDesign 1.0：<https://pmc.ncbi.nlm.nih.gov/articles/PMC12520099/>
13. AbDesign 2.0：<https://naturalantibody.com/ab-design2/>
14. HER2-aff-large / Buzz：<https://zenodo.org/records/10831512>
15. AVIDa-hTNFa：<https://huggingface.co/datasets/COGNANO/AVIDa-hTNFa>
16. TDC AntibodyAff：<https://tdcommons.ai/multi_pred_tasks/antibodyaff/>
17. Akbar SAbDab Kd CSV：<https://zenodo.org/records/13120765>
18. MochiBind sampled data：<https://raw.githubusercontent.com/amazon-science/ab-binding-eval/main/README.md>
19. Graphinity：<https://pmc.ncbi.nlm.nih.gov/articles/PMC12374841/>
20. ANTIPASTI：<https://data.mendeley.com/datasets/j4rt98xpy7/1>
