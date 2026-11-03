---
tags:
  - context
---

# Antibody-Side Diversity: CDR and Lineage — ABAG Survey Section 2

抗体侧是会上认为「相对直观」的一侧。但文献显示这一侧的阈值同样不稳：规范类在溶液中会互相跃迁，克隆型阈值依赖连锁方式，而序列聚类与结构聚类给出的划分可以完全不同。

## 2.1 CDR 规范类与结构聚类

### Canonical structures for the hypervariable regions of immunoglobulins, (Chothia et al., 1987, Journal of Molecular Biology, MRC Laboratory of Molecular Biology)

确立许多抗体超变环只采用有限几种复发的主链构象，且与环长和特定残基相关。规范类提供了一种不同于序列一致性的结构多样性度量。但它们不构成对 CDR-H3 的完备分类，也不能单独决定结合特异性。

### [A new clustering of antibody CDR loop conformations, (North et al., 2011, Journal of Molecular Biology, Fox Chase Cancer Center)](https://doi.org/10.1016/j.jmb.2010.10.030)

用基于方向统计的距离函数与亲和传播聚类，在 300 多个非冗余抗体结构上重建六个 CDR 环的构象分类，覆盖 28 种 CDR 长度组合（Chothia 只覆盖 20 种）。提供了「结构类数量」这一可操作计数。**两条序列不相近的 CDR 可以落在同一个构象簇**，因此序列多样性与结构多样性必须分开报告。

### [Length-independent structural similarities enrich the antibody CDR canonical class model, (Nowak et al., 2016, mAbs, University of Oxford)](https://doi.org/10.1080/19420862.2016.1158370)

证明各 CDR 类型都存在跨长度的结构相似环，据此建立长度无关的规范类。在三个 NGS repertoire 数据集（逾百万序列）上，长度无关簇比标准方法多分类约 13.5 万条序列（约 20% 提升）。**说明聚类阈值的选取直接改变被测多样性的大小**。

### [A penultimate classification of canonical antibody CDR conformations, (Kelow et al., 2022, [预印本], Fox Chase Cancer Center)](https://doi.org/10.1101/2022.10.12.511988)

修订 2011 年的分类，指出许多簇并非「规范」（未随结构增长而扩大），且部分簇实际代表多种构象。这是**对既有分类体系可靠性的自我修正**，引用时必须说明用的是哪一版。

### PyIgClassify: a database of antibody CDR structural classifications, (Adolf-Bryfogle et al., 2015, Nucleic Acids Research, Fox Chase Cancer Center)

把 CDR 结构分类与序列、结构注释一起公开，支持把观测到的环分配到既有构象簇。对数据集审计而言，**类覆盖度与类频次不平衡比抗体结构总数更有信息量**。

### [Antibody CDR loops as ensembles in solution vs. canonical clusters from X-ray structures, (Fernández-Quintero et al., 2020, mAbs, University of Innsbruck)](https://doi.org/10.1080/19420862.2020.1744328)

用分子动力学结合实验结构信息，在微秒到毫秒尺度上观察到所有 CDR 环在规范簇之间存在构象跃迁，且与长度、序列组成无关。还发现**若干规范簇的中位数实际属于同一动力学极小**。这是对「CDR 结构多样性 = 规范类计数」最直接的质疑。

### Transitions of CDR-L3 Loop Canonical Cluster Conformations on the Micro-to-Millisecond Timescale, (Fernández-Quintero et al., 2019, [待核])

聚焦 CDR-L3，量化其在规范簇之间的跃迁速率。单一晶体结构给出的类归属是快照，不是该序列的固有类。

### Canonical structures of short CDR-L3 in antibodies, (North et al., 2014, [待核])

专门处理短 CDR-L3 的规范结构。短环的行为与长环不同，且样本量小；这提示**在类计数里，小样本类的存在与否对总数影响很大**。

### Antibody CDR loops as ensembles... / Investigating the ability of deep learning-based structure prediction to extrapolate and/or enrich the set of canonical CDR conformations, ([待核], 2024, [待核])

检验结构预测模型能否外推或丰富已有的规范 CDR 构象集合。若预测模型只能复现训练中见过的类，则用它补结构不会增加结构多样性——**这是用预测结构补数据前必须做的检验**。

## 2.2 序列聚类阈值与克隆型

### [Cd-hit: a fast program for clustering and comparing large sets of protein or nucleotide sequences, (Li & Godzik, 2006, Bioinformatics, Burnham Institute for Medical Research)](https://doi.org/10.1093/bioinformatics/btl158)

引入被广泛用于冗余去除的高效序列聚类。一致性阈值定义了操作性的序列分组，但覆盖度要求与所选序列区域强烈影响这些分组的含义。**在抗体数据上，聚完整可变域与聚 CDR 回答的是不同问题，可能给出差别极大的划分**。

### [MMseqs2 enables sensitive protein sequence searching for the analysis of massive data sets, (Steinegger & Söding, 2017, Nature Biotechnology, Seoul National University / Max Planck Institute)](https://doi.org/10.1038/nbt.3988)

提供可扩展且灵敏的蛋白序列搜索，支持同源检测与冗余控制。它能发现朴素去重漏掉的关系。做抗原划分时，基于序列的分离**仍须审计共享折叠、保守表位与交叉反应家族**。

### Hierarchical clustering can identify B cell clones with high confidence in Ig repertoire sequencing data, (Gupta et al., 2017, The Journal of Immunology, Yale University)

在兼容的 V/J 与连接长度组内，用连接序列距离评估层次聚类的克隆指派。距离定义、连锁方式与聚类阈值都会影响推断出的克隆结构。**相关阈值是一个经过验证的克隆推断参数，而不是适用于结合特异性的通用 CDR 一致性截断**。

### Change-O: a toolkit for analyzing large-scale B cell immunoglobulin repertoire sequencing data, (Gupta et al., 2015, Bioinformatics, Yale University)

提供 repertoire 处理、克隆分组、germline 重建与谱系分析工具。其框架区分单个序列与同一 B 细胞克隆的相关成员。用在配对数据集上，可避免把单一谱系的密集采样误当作宽抗体多样性。

### A bioinformatic framework for immune repertoire diversity profiling enables detection of immunological status, (Greiff et al., 2015, Genome Medicine, University of Oslo)

用多样性剖面（diversity profiles）刻画 repertoire 分布，而非压成单一丰富度或熵值。对本仓库的用法：**同样的剖面可用来描述序列簇、谱系或结构类的频次分布**，但须声明采样深度与计数单位。

### Precise determination of the diversity of a combinatorial antibody library gives insight into the human immunoglobulin repertoire, (Glanville et al., 2009, PNAS, [待核])

对组合抗体库的多样性做精确测定，并据此推断人类免疫球蛋白 repertoire。是把测序深度与多样性估计耦合起来的经典范例。

### Diversity and clonal selection in the human T-cell repertoire, (Qi et al., 2014, PNAS, [待核])

用测序估计人类 T 细胞 repertoire 的多样性与克隆选择。方法上与本仓库的可迁移点：**如何把「未观测到的克隆」纳入总量估计**。

### [Commonality despite exceptional diversity in the baseline human antibody repertoire, (Briney et al., 2019, Nature, [待核])](https://doi.org/10.1038/s41586-018-0879-5)

在极高的基线多样性中仍发现公共性（commonality）。对数据收集的直接意涵：**「没见过的抗体」不等于「没见过的结合模式」**，公共性使得按序列去重会高估新颖度。

## 2.3 结构 / 表面聚类用于抗体

### [Surface ID: a geometry-aware system for protein molecular surface comparison, (Riahi et al., 2023, Bioinformatics, Sanofi)](https://doi.org/10.1093/bioinformatics/btad196)

基于几何与化学特征的几何深度学习系统，做高通量表面比较，并提供一种新的分组与对齐算法，可用于按功能聚类蛋白。文中报告其在表面相似性评估上表现最好。这是**「界面/表面作为独立比较空间」最现成的工具**。

### [Benchmarking antibody clustering methods using sequence, structural, and machine learning similarity measures for antibody discovery applications, (Chomicz et al., 2024, Frontiers in Molecular Biosciences, NaturalAntibody)](https://doi.org/10.3389/fmolb.2024.1352508)

（与 1.3 同篇，此处作为结构侧证据引用）在 binder 检测任务上，各方法差异不显著；**在表位制图任务上结构类方法才有优势**。这一「任务依赖」结论正是仓库 3.2 节要验证的东西。

### [Tokenizing loops of antibodies, (Fang et al., 2026, mAbs, Genentech)](https://doi.org/10.1080/19420862.2026.2645271)

提出 Igloo，一个同时编码主链二面角与序列的多模态抗体环 tokenizer，用对比学习把主链二面角相近的环拉近。对所有环都能给出 token，**解决了规范簇覆盖面有限的问题**，同时仍能恢复规范构象。在检索最相似 H3 环上比现有方法高 6.1%。

### Structural Analysis and Epitope Prediction of S2 Domain of SARS-CoV-2 ..., ([待核], 2023, [待核])

对 SARS-CoV-2 S2 域做结构分析与表位预测，并在主要变体间比较保守性。提供了一个「同一抗原因变体而异」的具体表位覆盖案例。

### Structural comparison of somatically related PG9 and PG16 in complex with their epitope reveals differences in ..., ([待核], 2012, [待核])

两个体细胞相关的抗体结合同一类表位却有不同的识别细节。**体细胞相关性（序列近）不保证表位同一性**。

## 2.4 谱系与 germline 多样性

### [Addressing the antibody germline bias and its effect on language models for improved antibody design, (Olsen et al., 2024, Bioinformatics, University of Oxford)](https://doi.org/10.1093/bioinformatics/btae618)

指出天然抗体序列的可变域大部分保持 germline，这在抗体语言模型预训练中引入对 germline 残基的强偏置，而离开 germline 的突变往往是获得功能的关键。**对本仓库的意涵：用 LM 表示做多样性统计时，germline 偏置会压缩真实差异**。

### The repertoire of human germline VH sequences reveals about fifty groups of VH segments with different hypervariable loops, (Chothia et al., 1992, Journal of Molecular Biology, MRC Laboratory of Molecular Biology)

（与 1.4 同篇，此处作为谱系侧基础引用）约五十组 VH，每组超变环不同——这是抗体结构多样性的 germline 底数。

### Germline-encoded amino acid-binding motifs drive immunodominant public antibody responses, (Sangesland et al., 2023, [待核])

germline 编码的氨基酸结合基序驱动免疫显性的公共抗体应答。解释了为什么跨个体出现相同结合模式：**公共性源自 germline，而非数据重复**。

### Germline VH/VL pairing in antibodies, (Jayaram et al., 2012, [待核])

分析 VH/VL 的 germline 配对偏好。配对不是随机的，因此**按单链统计多样性会高估组合多样性**。

### Antibody Heavy Chain Variable Domains of Different Germline Gene Origins Diversify through Different Paths, (Sheng et al., 2017, [待核])

不同 germline 来源的 VH 通过不同路径多样化。单一多样性指标在不同 germline 子群上含义不同。

### The mouse antibody heavy chain repertoire is germline-focused and highly variable between inbred strains, (Collins et al., 2015, [待核])

不同近交系间重链 repertoire 差异很大。**多样性的「基线」是物种/品系属性**，跨物种汇总前必须分层。

## 2.5 VHH / 单域抗体的特殊性

### [Analysis of nanobody paratopes reveals greater diversity than classical antibodies, (Mitchell & Colwell, 2018, PEDS, University of Cambridge)](https://doi.org/10.1093/protein/gzy017)

（见 1.4）VHH 的 paratope 多样性高于常规抗体，接触类型也不同。

### Comparative analysis of nanobody sequence and structure data, (Mitchell & Colwell, 2018, Proteins, University of Cambridge)

系统比较纳米抗体的序列与结构数据特征。为「VHH 能否与 Fab 放进同一个聚类空间」提供了经验边界。

### Analysis and modeling of the variable region of camelid single-domain antibodies, (Sircar et al., 2011, [待核])

对骆驼科单域抗体可变区做分析与建模。框架区的补偿性接触在 VHH 中更常见，呼应会上「CDR 之外的接触位点」。

### Camel heavy-chain antibodies: diverse germline V(H)H and specific mechanisms enlarge the antigen-binding repertoire, (Nguyen et al., 2000, EMBO Journal, [待核])

VHH 通过多样的 germline 与特定机制扩大抗原结合 repertoire。说明**VHH 的多样性来源与常规抗体不同**，不能套用 CDR 规范类框架。
