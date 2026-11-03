---
tags:
  - context
---

# Diversity As An Evaluation Tool: Redundancy, Leakage, Partition — ABAG Survey Section 4

## 4. 多样性作为评估工具：冗余、泄漏、划分

这一节是仓库 3.2 节「按相似性聚类 → 划分 → 看指标是否下降 ⇒ 该维度承载真实泄漏」的方法学前身。**核心发现：这一步单独做不成立**——指标下降也可以由训练集变小、分布偏移来解释，必须有对照。

### 4.1 冗余去除与代表集选择

#### [Choosing non-redundant representative subsets of protein sequence data sets using submodular optimization, (Libbrecht et al., 2018, Proteins, University of Washington)](https://doi.org/10.1002/prot.25461)

指出 CD-HIT、PISCES、UCLUST 等启发式阈值算法没有理论保证，提出用次模优化选代表集。以 SCOPe 结构库为金标准，**次模优化在同样规模下覆盖更多的 SCOPe 域家族**。这是「多样性可以用覆盖目标形式化」的直接证据，也是回答「90–100 个抗原够不够」的可用工具。

#### Identifying representative sequences of protein families using submodular optimization, ([待核], 2025, [待核])

把次模优化用在蛋白家族的代表序列选择上。方法学延续。

#### Removing near-neighbour redundancy from large protein sequence collections, (Holm & Sander, 1998, Bioinformatics, EMBL-EBI)

从大规模蛋白序列集合中去除近邻冗余。这是 PDB/SCOP 层面冗余控制的原始工作，**冗余阈值的选择在此已被显式讨论**。

#### Protein sequence redundancy reduction: comparison of various method, ([待核], 2010, [待核])

比较不同的序列冗余削减方法。给出方法间差异的量化，可用于论证阈值敏感度。

#### Redundancy-weighting the PDB for detailed secondary structure prediction using deep-learning models, ([待核], 2020, [待核])

用冗余加权处理 PDB 用于深度学习。**冗余加权 vs 硬去重**是两种不同的处理哲学，前者保留频次信息，后者丢弃。多样性统计须明确用哪一种。

#### The influence of dataset homology and a rigorous evaluation strategy on protein secondary structure prediction, ([待核], 2021, [待核])

显示数据集同源性对二级结构预测评估的影响。跨任务证据：**同源性控制不严会系统性高估性能**。

#### Dataset size and composition impact the reliability of performance benchmarks for peptide-MHC binding prediction, (Kim et al., 2014, [待核])

数据集规模与组成影响 pMHC 结合预测基准的可靠性。**「数据集组成」即多样性**，此处被显式当作影响结论的变量。

#### PLINDER: The protein-ligand interactions dataset and evaluation resource, (Durairaj et al., 2024, [待核])

提出一个带有多轴质量与相似性标注的蛋白-配体交互数据集与评估资源。其组织方式（每条记录带最近邻与相似性分层）**可直接借鉴为 ab-ag 数据集的 schema**。

#### PiNUI: A Dataset of Protein–Protein Interactions for Machine Learning, (Bushuiev et al., 2023, [待核])

面向机器学习的 PPI 数据集，强调数据划分与质量控制。是与 ab-ag 最接近的一般 PPI 类比。

### 4.2 泄漏感知划分与基准

#### Flaws in evaluation schemes for pair-input computational predictions, (Park & Marcotte, 2012, Nature Methods, University of Texas at Austin)

证明 pair-input 预测器的评估关键取决于测试对中的两个实体是否在训练中出现过：都未出现、出现一个、都出现，对应难度截然不同的任务。**随机的对划分测的是比泛化容易得多的任务**。对抗体-抗原数据，这直接要求分开报告「未见抗体 / 未见抗原 / 两者皆未见」三种评估。**这是仓库 3.2 节判别法必须补上的三分**。

#### [Cracking the black box of deep sequence-based protein-protein interaction prediction, (Bernett et al., 2024, Briefings in Bioinformatics, Technical University of Munich)](https://doi.org/10.1093/bib/bbae076)

系统考察深度学习 PPI 预测器对数据泄漏、序列相似性与节点度信息的依赖，并与基础机器学习模型对比。**随机划分造成的训练-测试重叠导致性能被严重高估；当通过最小化序列相似性来避免泄漏后，性能变成随机**。而且直接利用序列相似性与网络拓扑的基线模型以极低计算成本达到相近水平。**这是本仓库最该直接引用的反面证据**。

#### [Component puzzle protein-protein interaction prediction, (Hosseini et al., 2025, Briefings in Bioinformatics, University of Waterloo)](https://doi.org/10.1093/bib/bbaf685)

承接 Bernett 的结论（现有方法只学到序列相似性与节点度，去泄漏后性能随机），提出 C3PI，声称是首个在去泄漏设置下仍显著优于竞争方法的工作。无论其结论是否成立，**它定义了「去泄漏后仍有效」这一评价门槛**。

#### [Beware of Data Leakage from Protein LLM Pretraining, (Hermann et al., 2024, [预印本], Technical University of Munich)](https://doi.org/10.1101/2024.07.23.604678)

在蛋白热稳定性预测中测量 PLM 预训练泄漏的影响，比较「预训练感知划分」与「朴素划分」。**预训练泄漏对结果有一致的影响**。对 ab-ag 的意涵：即使训练/测试按结构去泄漏，PLM 预训练集仍可能已含该抗体/抗原。**这是第二层泄漏，仓库目前的划分方法没有覆盖**。

#### [A structural antibody benchmark for leakage-aware deep-learning evaluation, (Cohen et al., 2026, [预印本], IBM Research)](https://doi.org/10.64898/2026.09.06.749672)

提出 SABLE：16,511 条实验训练条目 + 327 条人工复核测试条目 + 3,274 个专利来源的高置信 AlphaFold3 模型（覆盖 476 个抗原）。**仅靠时间截断无法防止训练-测试泄漏**，须用抗体与抗原序列相似性双重过滤，且每条测试条目记录最近的训练集邻居，从而可以按相似性分层报告性能。**这是仓库要建的基准的直接原型**。

#### [A Structural Antibody Benchmark of AlphaFold3 reveals Hallucinated Epitopes and a Bias for Orderness, (Solanki et al., 2026, [预印本], University of Delaware)](https://doi.org/10.64898/2026.07.30.741792)

用 SAbDab 的 3,401 个实验验证复合物与 23,798 个阴性对照基准 AF3。100 个推理种子下最大召回 53%；存在对 X 射线来源抗体的偏置、对 EM 来源的劣势，且阳性预测率随靶蛋白尺寸与表面积增大而下降。**有意思的是：CDR 氨基酸组成与长度、以及训练数据泄漏，均未发现引入显著偏置**——这与 Bernett 的结论方向相反，值得并列记录。

#### What does AlphaFold3 learn about antibody and nanobody docking, and what remains unsolved?, ([待核], 2025, [待核])

专门分析 AF3 在抗体与纳米抗体对接上学到了什么。是评估「用预测结构补表位维度」是否可靠的关键文献。

#### Benchmarking Boltz-2 for Screening of Therapeutic Antibody-Antigen Interactions, ([待核], 2026, [待核])

基准 Boltz-2 在治疗性抗体-抗原相互作用筛选上的表现。可作为 co-folding 路线的可用性证据。

#### [Evaluating Protein Transfer Learning with TAPE, (Rao et al., 2019, NeurIPS, Stanford University)](https://arxiv.org/abs/1906.08230)

提出一套蛋白学习基准，含针对「超越训练近邻」的泛化测试。说明**明确指定训练与测试之间生物关系的重要性**。类比地，抗体基准应显式说明其划分测试的是新序列、新谱系、新抗原家族，还是新结合面。

#### ATOM3D: Tasks on Molecules in Three Dimensions, (Townshend et al., 2021, NeurIPS Datasets and Benchmarks, Stanford University)

提供标准化的三维分子学习任务（含蛋白界面预测），并带任务特定的数据集构造与划分。对本仓库的用处：**「聚类再划分，看性能下降」这一实验，性能下降只证明模型对该分布偏移敏感；要主张泄漏，必须控制训练规模与其他划分差异**。

#### A new framework for evaluating model out-of-distribution generalisation for the biochemical domain, ([待核], 2024, [待核])

提出生化领域 OOD 泛化评估框架。可提供「分布偏移」与「泄漏」的区分标准。

#### Out-of-distribution generalization enhances protein function annotation for low-homology sequences, ([待核], 2026, [待核])

低同源序列上的 OOD 泛化。与 ab-ag 的未见抗原情形同构。

#### Strict OOD Antigen-to-Antibody Retrieval with CDR-Aware Slot Late Interaction, ([待核], 2026, [待核])

在严格 OOD 设定下做抗原到抗体的检索。**检索任务比预测任务更适合做多样性评估**，因为不需要亲和力标签。

### 4.3 数据集的多样性 / 偏置诊断

#### MHChron: diversity-balanced dataset design for robust peptide–MHC binding prediction across MHC class I and II, ([待核], 2026, [待核])

用多样性均衡的数据集设计提升 pMHC 结合预测的稳健性。**「多样性均衡」作为数据设计目标，而非事后度量**，这是仓库可以直接借用的框架。

#### A curated structural dataset of peptide-protein complexes reveals biases in existing datasets and principles of ..., ([待核], 2026, [待核])

策展肽-蛋白复合物数据集，并由此揭示既有数据集的偏置。方法论上与本仓库的「数据现状摸底」任务同构。

#### Benchmark Bias and Conformational Dynamics in Allosteric Site Prediction, ([待核], 2026, [待核])

揭示变构位点预测中的基准偏置与构象动力学问题。跨任务的偏置诊断范例。

#### The importance of residue-level filtering and the Top2018 best-parts dataset of high-quality protein residues, ([待核], 2022, [待核])

强调残基级过滤的重要性并给出高质量数据集。**质量过滤会改变多样性**：过滤越严，残余多样性越低。

#### Graphinity 实验派生/计算 ΔΔG, (R50)

（本仓库已接入的数据源）合并实验派生与计算的 ΔΔG，**计算标签与实验标签混在同一表里**，是多样性统计须先分层的典型例子。

#### A unified peptide array platform for antibody epitope binning, mapping, specificity and predictive off-target ..., ([待核], 2022, [待核])

统一的肽阵列平台同时做分箱、制图、特异性与脱靶预测。工程上把多种表位测量压到一条流水线。

### 4.4 合成数据与可控多样性

#### [Unconstrained generation of synthetic antibody-antigen structures to guide machine learning methodology for antibody specificity prediction, (Robert et al., 2022, Nature Computational Science, University of Oslo)](https://doi.org/10.1038/s43588-022-00372-4)

提出 Absolut!，可参数化无约束生成基于晶格的 3D 抗体-抗原结合结构，且**对构象 paratope、epitope 与亲和力有真值**。把常见免疫学特异性预测问题形式化为 ML 任务，并确认在实验数据上训练的方法排序与在 Absolut! 数据上一致。**这是验证「哪种相似性维度承载真实泄漏」最干净的沙盒：多样性可调，真值已知**。

#### [Machine learning optimization of candidate antibody yields highly diverse sub-nanomolar affinity antibody libraries, (Li et al., 2023, Nature Communications, MIT)](https://doi.org/10.1038/s41467-023-39022-2)

端到端贝叶斯、语言模型驱动的方法，设计大且多样的高亲和力 scFv 库并经实验测量。**显式比较库的预测成功率与实际测量，展示「库成功率」与「多样性」之间的权衡**。这是少数真正把多样性当作可调参数而非事后统计的工作。

#### Insight into the libraries: Precise determination of the diversity of a combinatorial antibody library..., (Glanville et al., 2009, PNAS, [待核])

（与 2.2 同篇）组合库多样性的精确测定。
