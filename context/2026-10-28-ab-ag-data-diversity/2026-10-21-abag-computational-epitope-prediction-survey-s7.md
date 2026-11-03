---
tags:
  - context
---

# Computational Epitope and Paratope Prediction — ABAG Survey Section 7

## 7. 计算表位 / paratope 预测

**定位：这一类不是多样性理论，而是「无结构数据时的退路」**。`data/raw/public/` 中相当比例只有序列，这一节决定了它们能否进入表位维度。

### 7.1 B 细胞表位预测

#### BepiPred-2.0: improving sequence-based B-cell epitope prediction using conformational epitopes, (Jespersen et al., 2017, Nucleic Acids Research, Technical University of Denmark)

用构象表位训练数据改进基于序列的 B 细胞表位预测。是序列-only 路线的基线。

#### BepiPred-3.0: Improved B-cell epitope prediction using protein language models, (Clifford et al., 2022, Protein Science, Technical University of Denmark)

用蛋白语言模型改进 B 细胞表位预测。**pLM 表示已能在序列层面捕捉部分表位信息**，这对无结构数据的可用性影响最大。

#### [DiscoTope-3.0: improved B-cell epitope prediction using inverse folding latent representations, (Høie et al., 2024, Frontiers in Immunology, Technical University of Denmark)](https://doi.org/10.3389/fimmu.2024.1322712)

用逆折叠潜表示改进表位预测。逆折叠表示对「什么序列能放在这个表面位置」编码充分，天然适合表位。

#### PEPITO: improved discontinuous B-cell epitope prediction using multiple distance thresholds and half sphere exposure, (Sweredoski & Baldi, 2008, Bioinformatics, UC Irvine)

用多距离阈值与半球暴露改进不连续表位预测。早期结构基方法的代表。

#### CEP: a conformational epitope prediction server, (Kringelum et al., 2006, [待核])

构象表位预测服务器。

#### SEMA: Antigen B-cell conformational epitope prediction using deep transfer learning, (Collatz et al., 2022, [待核])

用深度迁移学习做抗原 B 细胞构象表位预测。

### 7.2 Paratope 预测

#### [Parapred: antibody paratope prediction using convolutional and recurrent neural networks, (Liberis et al., 2018, Bioinformatics, University of Cambridge)](https://doi.org/10.1093/bioinformatics/bty305)

用卷积与循环神经网络从序列预测 paratope。paratope 预测是把抗体侧投射到表位空间的桥梁。

#### [Paragraph-antibody paratope prediction using graph neural networks with minimal feature vectors, (Chinery et al., 2023, Bioinformatics, University of Oxford)](https://doi.org/10.1093/bioinformatics/btac732)

用图神经网络与最小特征向量做 paratope 预测。**feature 越少越说明结构本身携带信息**。

#### [Attentive Cross-Modal Paratope Prediction, (Deac et al., 2019, Journal of Computational Biology, [待核])](https://doi.org/10.1089/cmb.2018.0175)

跨模态注意力做 paratope 预测，同时利用抗体与抗原两侧。

#### [ParaSurf: a surface-based deep learning approach for paratope-antigen interaction prediction, (Papadopoulos et al., 2025, Bioinformatics, [待核])](https://doi.org/10.1093/bioinformatics/btaf062)

基于表面的深度学习方法预测 paratope-抗原相互作用。**把 paratope 预测搬到表面表示上，与本仓库的界面维度直接衔接**。

#### [Geometric epitope and paratope prediction, (Pegoraro et al., 2024, Bioinformatics, [待核])](https://doi.org/10.1093/bioinformatics/btae405)

几何方法同时预测表位与 paratope。两侧联合预测比单侧更能约束界面定义。

#### [ParaAntiProt provides paratope prediction using antibody and protein language models, (Kalemati et al., 2024, Scientific Reports, [待核])](https://doi.org/10.1038/s41598-024-80940-y)

同时用抗体与通用蛋白语言模型做 paratope 预测。

### 7.3 抗体特异性预测

#### An explainable language model for antibody specificity prediction using curated influenza hemagglutinin antibody data, (Xu et al., 2024, [待核])

可解释语言模型预测抗体特异性。

#### Supervised fine-tuning of pre-trained antibody language models improves antigen specificity prediction, (Yu et al., 2025, [待核])

监督微调提升抗原特异性预测。**特异性是可观测的表位代理**，可作为多样性方法的验证目标。

#### Contrastive learning for antibody-antigen sequence-to-specificity prediction, ([待核], 2026, [待核])

对比学习做序列到特异性的预测。

#### [Unconstrained generation of synthetic antibody-antigen structures..., (Robert et al., 2022, Nature Computational Science, University of Oslo)](https://doi.org/10.1038/s43588-022-00372-4)

（见 4.4）

#### [Structure-free antibody paratope similarity prediction for in silico epitope binning via protein language models, (Ghanbarpour et al., 2023, iScience, [待核])](https://doi.org/10.1016/j.isci.2023.106036)

（见 1.3）

### 7.4 表位预测的评估争议

#### Towards a consensus on datasets and evaluation metrics for developing B-cell epitope prediction tools, (Greenbaum et al., 2007, Journal of Molecular Recognition, [待核])

指出 B 细胞表位预测在数据集与评价指标上缺乏共识。**指标定义不统一时，「哪个方法预测得更准」这个问题本身没有意义**。

#### [Understanding the Significance and Implications of Antibody Numbering and Antigen-Binding Surface/Residue Definition, (Dondelinger et al., 2018, Frontiers in Immunology, University of Liège)](https://doi.org/10.3389/fimmu.2018.02278)

系统比较不同编号体系与 CDR 定义。**不同数据库使用不同编号约定与 CDR 定义，因此「CDR 多样性」的数值依赖于所采用的体系**。这是 CDR 聚类前必须先固定的口径。

#### [ANARCI: antigen receptor numbering and receptor classification, (Dunbar & Deane, 2016, Bioinformatics, University of Oxford)](https://doi.org/10.1093/bioinformatics/btv552)

抗体编号与受体分类工具。工程上是把各数据集统一到同一 CDR 口径的必要环节。

#### IMGT unique numbering for immunoglobulin and T cell receptor variable domains and Ig superfamily V-like domains, (Lefranc et al., 2003, Developmental & Comparative Immunology, University of Montpellier)

IMGT 唯一编号。是事实上的接口标准。

#### 50 years of antibody numbering schemes: a statistical and structural evaluation reveals key differences and limitations, (Dondelinger et al., 2024, [待核])

对五十年的抗体编号方案做统计与结构评估，**揭示关键差异与局限**。直接文献化「编号口径会影响结论」这件事。

#### AbRSA: A robust tool for antibody numbering, (Yu et al., 2019, [待核])

鲁棒的抗体编号工具。

#### [EpiScan: accurate high-throughput mapping of antibody-specific epitopes using sequence information, (Wang et al., 2024, npj Systems Biology and Applications, [待核])](https://doi.org/10.1038/s41540-024-00432-7)

纯用抗体序列信息（VH、VL、CDR、FR 分别建块再加权）预测特定抗体在抗原上的表位。**「抗体特异性表位」而非「抗原通用表位」的定位方式，与本仓库的配对数据观点一致**。

#### Improved Antibody-Specific Epitope Prediction Using AlphaFold and AbAdapt, ([待核], 2022, [待核])

用 AF 与 AbAdapt 改进抗体特异性表位预测。

#### AFilter: Improved Antibody Epitope Prediction by Machine Learning-Optimized Interface Energy Filtering of AlphaFold ..., ([待核], 2026, [待核])

用机器学习优化的界面能量过滤改进 AF 派生表位预测。承认了 AF 预测的界面需要额外过滤——呼应 AF3 幻觉表位的问题。

---
