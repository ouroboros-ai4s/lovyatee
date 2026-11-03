---
- tags:
  - context
---

# General PPI and Protein-Surface Comparison Methods — ABAG Survey Section 3

## 3. 广义 PPI 与蛋白表面比较方法

这一节是工具库。核心分歧在于**比较的粒度**：整链折叠、局部表面 patch、界面残基集合、还是接触图。四者回答不同问题，且都不能直接等同于「表位是同一个」。

### 3.1 界面残基集合比较与对接质量度量

#### DockQ: A Quality Measure for Protein-Protein Docking Models, (Basu & Wallner, 2016, PLoS ONE, RWTH Aachen University)

把 native contact 恢复率、界面 RMSD、配体 RMSD 组合成一个连续的对接质量分数。其分量在伙伴与残基对应关系确定后，可直接用于比较界面。**但 DockQ 是参照式的模型评估，不是无关联表位之间的一般距离**。

#### iAlign: a method for the structural comparison of protein–protein interfaces, (Gao & Skolnick, 2010, Bioinformatics, Georgia Institute of Technology)

用界面几何与界面接触对齐蛋白界面，包括不需要常规序列对应关系的比较。可识别序列相似性很弱但相互作用架构相似的蛋白。**对抗体-抗原对，比较完整界面同时捕捉两个伙伴的排布，这与只比较抗原 patch 不同**。

#### [Predicting protein-protein interface residues using local surface structural similarity, (Jordan et al., 2012, BMC Bioinformatics, University of Nebraska-Lincoln)](https://doi.org/10.1186/1471-2105-13-41)

用局部表面结构相似性预测界面残基。说明**局部表面相似性本身携带界面信息**，可作为表位区域的几何签名。

#### [A Novel Geometry-Based Approach to Infer Protein Interface Similarity, (Budowski-Tal et al., 2018, Scientific Reports, Tel Aviv University)](https://doi.org/10.1038/s41598-018-26497-z)

提出基于几何的方法推断蛋白界面相似性。直接对标会上「蛋白表面究竟怎么比较」这一遗留问题。

#### [Quantitative comparison of protein-protein interaction interface using physicochemical feature-based descriptors of surface patches, (Shin et al., 2023, Frontiers in Molecular Biosciences, [待核])](https://doi.org/10.3389/fmolb.2023.1110567)

提出 PPI-Surfer，用局部表面区域的理化描述子比较并量化 PPI 界面的相似性，能找到**不共享序列与结构相似性**的相似潜在结合区域。这是「界面相似性可以脱离序列/折叠相似性独立存在」的明确证据，对本仓库的多样性定义影响最大。

#### [Protein docking by the interface structure similarity: how much structure is needed?, (Sinha et al., 2012, PLoS ONE, University of Kansas)](https://doi.org/10.1371/journal.pone.0031349)

量化「需要多少结构信息才能判定界面相似」。给出界面比较的**分辨率下限**，是设定结构聚类阈值时的直接依据。

#### [Combining pairwise structural similarity and deep learning interface contact prediction to estimate protein complex model accuracy in CASP15, (Roy et al., 2023, Proteins, University of Missouri)](https://doi.org/10.1002/prot.26542)

把成对结构相似性与深度学习接触预测结合来估计复合物模型精度。说明界面相似性可以作为一个连续的、可组合的度量使用。

#### Optimal contact map alignment of protein-protein interfaces, (Pulim et al., 2008, [待核])

用接触图对齐比较蛋白-蛋白界面。接触图把界面抽象成图结构，天然适合「残基在序列上不连续但空间相邻」的情形。

#### 1001 optimal PDB structure alignments: integer programming methods for finding the maximum contact map overlap, (Caprara et al., 2004, [待核])

把结构对齐形式化为最大接触图重叠问题并用整数规划精确求解。提供接触图相似的**理论最优基准**，可用于检验启发式方法的损失。

#### Evolution and similarity evaluation of protein structures in contact map space, (Ding et al., 2005, [待核])

在接触图空间评价蛋白结构的演化与相似性。接触图距离的演化含义是可解释的，这在解释多样性指标时有用。

### 3.2 表面 patch 几何描述子

#### Fast protein tertiary structure retrieval based on global surface shape similarity, (Sael et al., 2008, Proteins, Purdue University)

用紧凑的三维 Zernike 描述子表示蛋白表面形状，支持旋转不变的比较。展示了无需逐残基序列对齐即可量化几何相似性。**其描述子描述的是全局形状，用于表位须另行验证局部 patch 表示**。

#### [Protein-protein docking using region-based 3D Zernike descriptors, (Venkatraman et al., 2009, BMC Bioinformatics, Purdue University)](https://doi.org/10.1186/1471-2105-10-407)

把 3D Zernike 描述子用在基于区域的对接上。区域级描述子的成功说明**局部几何签名足以支撑识别**。

#### Molecular surface representation using 3D Zernike descriptors for protein shape comparison and docking, (Kihara et al., 2011, [待核])

综述并扩展用 3D Zernike 描述子做分子表面表示、形状比较与对接。是表面几何描述子的方法学参考。

#### [Exploring the potential of 3D Zernike descriptors and SVM for protein-protein interface prediction, (Daberdaku & Ferrari, 2018, BMC Bioinformatics, University of Padova)](https://doi.org/10.1186/s12859-018-2084-7)

把 3D Zernike 描述子与 SVM 结合做界面预测。说明几何描述子携带的界面信息足以训练分类器。

#### [Rapid automated superposition of shapes and macromolecular models using spherical harmonics, (Konarev et al., 2016, Journal of Applied Crystallography, EMBL Hamburg)](https://doi.org/10.1107/s1600576716005793)

用球谐函数在傅里叶空间做快速形状叠合，比实空间算法快一个数量级，适合低分辨率形状模型。**对只有低分辨率或预测结构的数据集，这是可用的表面比较路径**。

#### Travel depth, a new shape descriptor for macromolecules: application to ligand binding, (Coleman & Sharp, 2006, Journal of Molecular Biology, [待核])

提出 travel depth 作为大分子形状描述子。凹度/深度是表位描述中常被忽略但直接影响抗体可及性的一维。

#### Surface-histogram: a new shape descriptor for protein-protein docking, (Axenopoulos et al., 2012, [待核])

提出表面直方图描述子用于对接。提供了与 Zernike 互补的另一种旋转不变表示。

#### FTIP: an accurate and efficient method for global protein surface comparison, (Lee et al., 2020, [待核])

提出全局蛋白表面比较方法。是对比「全局表面相似 vs 局部 patch 相似」两种粒度的现成工具。

#### Matching protein surface structural patches for high-resolution blind peptide docking, (Khashan et al., 2022, [待核])

用表面结构 patch 匹配做高分辨率盲肽对接。patch 匹配在肽-蛋白场景可行，说明**短表位（线性肽）与构象表位可以用同一套 patch 语言描述**。

#### Conformational epitope matching and prediction based on protein surface spiral features, (Sun et al., 2021, [待核])

用表面螺旋特征做构象表位匹配与预测。是少数**把表面特征直接用于表位（而非一般结合位点）**的工作。

#### 3D-SURFER: software for high-throughput protein surface comparison and analysis, (Sael et al., 2009, Bioinformatics, Purdue University)

高通量蛋白表面比较软件。工程上可直接用于 `data/raw/public/` 的大规模表面素描。

#### Protein surface similarities: a survey of methods to describe and compare protein surfaces, (Via et al., 2000, [待核])

综述描述与比较蛋白表面的方法。是入门的分类学参考，也是判断「哪些描述子够用」的历史基线。

### 3.3 局部结构比对与结合位点相似

#### ProBiS algorithm for detection of structurally similar protein binding sites by local structural alignment, (Konc & Janežič, 2010, Bioinformatics, University of Ljubljana)

用局部结构比对检测结构相似的蛋白结合位点，包括无同源关系的蛋白。**ProBiS 的核心主张——局部结合位点相似性可以跨越全局折叠差异——正是「表面 patch 聚类」的理论支撑**。

#### ProBiS-database: precalculated binding site similarities and local pairwise alignments of PDB structures, (Konc & Janežič, 2012, [待核])

把 ProBiS 的局部比对结果预计算成数据库。可作为「已有局部位点相似性」的现成资源。

#### Detecting local ligand-binding site similarity in nonhomologous proteins by surface patch comparison, (Xiong et al., 2012, [待核])

用表面 patch 比较在非同源蛋白间检测局部结合位点相似性。直接对标「表位相似但不共享序列/折叠」的情形。

#### Supersites within superfolds. Binding site similarity in the absence of homology, (Russell, 1998, Journal of Molecular Biology, [待核])

在无同源性的超折叠内部识别相似的结合位点（supersites）。这是「结合位点相似性独立于折叠相似性」的早期关键证据。

#### SiteMine: Large-scale binding site similarity searching in protein structure databases, (Schmidt et al., 2024, [待核])

在蛋白结构数据库上做大规模结合位点相似性搜索。工程上对应「在全库尺度上做界面聚类」的可行性验证。

#### Structural motif search across the protein universe with Folddisco, (2026, [待核])

把结构模体搜索推广到全蛋白宇宙。对表位这类局部模体的检索是直接可用的方法论。

#### Identifying protein biochemical functions by similarity search using the molecular surface database eF-site, (Kinoshita et al., 2003, [待核])

用分子表面数据库做相似性搜索以识别生化功能。表面相似性可用于功能注释，说明其捕捉的是功能相关特征而非偶然几何。

#### Protein functional surfaces: global shape matching and local spatial alignments of ligand binding sites, (Tseng et al., 2008, [待核])

结合全局形状匹配与局部空间对齐全。

#### Binding site similarity analysis for the functional classification of the protein kinase family, (Bryant et al., 2009, [待核])

用结合位点相似性做蛋白激酶家族的功能分类。**用结合位点相似性做分类**是「以界面为多样性空间」的直接先例。

### 3.4 接触图谱与图相似

#### TM-align: a protein structure alignment algorithm based on the TM-score, (Zhang & Skolnick, 2005, Nucleic Acids Research, University of Michigan)

用 TM-score 优化结构对齐，提供整体折叠相似性的标准度量。可用于识别抗原的折叠冗余，并在比较映射的表位残基前建立结构对应关系。**全局折叠相似性本身不能确立两个抗体识别等价的表面 patch**。

#### US-align: universal structure alignments of proteins, nucleic acids, and macromolecular complexes, (Zhang et al., 2022, Nature Methods, University of Missouri)

把结构对齐推广到蛋白、核酸与复合物。**对 ab-ag 复合物，可整复合物对齐**，这是比较「结合模式」而非「单侧结构」的现成手段。

#### MM-align: a quick algorithm for aligning multiple-chain protein complex structures using iterative dynamic programming, (Mukherjee & Zhang, 2009, Nucleic Acids Research, University of Michigan)

用迭代动态规划做多链复合物结构对齐。复合物对齐是判断「两个抗体-抗原对是否同构」的直接方法。

#### [Rapid automated superposition of shapes and macromolecular models using spherical harmonics, (Konarev et al., 2016, J Appl Cryst, EMBL Hamburg)](https://doi.org/10.1107/s1600576716005793)

（见 3.2）低分辨率形状叠合。

#### CMView: interactive contact map visualization and analysis, (Vejnar et al., 2011, [待核])

接触图可视化与分析工具。工程上便于人工审查候选表位簇。

#### Fast and accurate protein structure search with Foldseek, (van Kempen et al., 2024, Nature Biotechnology, Seoul National University / ETH Zurich)

用结构字母表编码三级残基环境，实现大规模结构相似性搜索。提供发现抗原结构近邻并把大数据集组织成结构组的现成机制。**整链相似性与表位相似性是不同的量，须辅以局部界面比较**。

### 3.5 表面指纹作为设计目标

#### [Deciphering interaction fingerprints from protein molecular surfaces using geometric deep learning, (Gainza et al., 2020, Nature Methods, EPFL)](https://doi.org/10.1038/s41592-019-0666-6)

提出 MaSIF，从几何与化学特征中学习局部分子表面 patch 的描述子。描述子比较支持表面识别与相互作用兼容性评估。**这些 embedding 是表位聚类的候选，但其训练目标与对构象的敏感性须先检查，才能把 embedding 距离当作生物多样性**。

#### [De novo design of protein interactions with learned surface fingerprints, (Gainza et al., 2023, Nature, EPFL / University of Washington)](https://doi.org/10.1038/s41586-023-05993-x)

在 MaSIF 基础上设计针对 SARS-CoV-2 spike、PD-1、PD-L1、CTLA-4 的 de novo binder，多个设计获得实验验证。**这是「表面指纹足以编码识别特异性」的最强反向证明**：如果学习到的表面描述子不能区分不同 patch，就不可能用它设计出特异性 binder。

#### Decoding Protein-Membrane Binding Interfaces from Surface-Fingerprint-Based Geometric Deep Learning, ([待核], 2025, [待核])

把表面指纹用于蛋白-膜界面。说明该表示不限于可溶性蛋白结合。

#### An explainable language model for antibody specificity prediction using curated influenza hemagglutinin antibody data, (Xu et al., 2024, [待核])

用策展的流感 HA 抗体数据训练可解释语言模型预测抗体特异性。特异性预测本身可看作表位多样性的下游检验。

#### A Pharmacophore-Based Method for Rapid and Accurate Virtual Screening of Antibody Libraries against Antigens, ([待核], 2025, [待核])

用药效团方法做抗体库对映抗原的虚拟筛选。提供了「以化学特征而非几何比较界面」的补充视角。
