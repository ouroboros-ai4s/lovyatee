---
tags:
  - context
---

<!-- markdownlint-disable -->
# 2026-10-20 抗原抗体多样性的建模与度量：文献调研目录

> 范围：蛋白 / 抗原-抗体（ab-ag）多样性如何被定义、量化、验证。服务于本仓库的两个下游决策——数据要收集到什么规模、现有开源数据是否已高度重复。
>
> 检索：Europe PMC 105 组结构化查询，去重后 1,193 条记录；另以独立模型（GPT-6 Astra）做无网络的知识召回，用于发现检索词覆盖不到的经典文献。两路结果交叉比对后保留本文条目。
>
> 元数据说明：标题、作者、年份、期刊来自 Europe PMC 返回；**机构一栏为作者单位或通讯单位的最佳判断，未经原始 PDF 核对，标 `[待核]` 者尤须复核**。已撤回或仅预印本的条目标注 `[预印本]`。

---

## 目录

| H2 | 分类 | 条目 | H3 数 |
| --- | --- | ---: | ---: |
| 1 | ABAG 表位多样性：什么算「不同的表位」 | 33 | 4 |
| 2 | 抗体侧多样性：CDR 与谱系 | 32 | 5 |
| 3 | 广义 PPI 与蛋白表面比较方法 | 42 | 5 |
| 4 | 多样性作为评估工具：冗余、泄漏、划分 | 31 | 4 |
| 5 | 多样性 × 数据量 × 性能 | 22 | 4 |
| 6 | 实验真值：表位多样性怎么测出来 | 39 | 5 |
| 7 | 计算表位 / paratope 预测 | 26 | 4 |
| 8 | 采样与覆盖度理论 | 10 | 2 |
| — | 三轴交叉（不占篇数，为结构说明） | — | — |
| | **条目合计** | **235** | **33** |
| | **去重后独立文献** | **222** | |

> 13 条重复出现是**跨节交叉引用**（标注「见 X.X」），例如 Cao 2022 同时属于 1.1（表位组划分）与 4.2（逃逸谱）；Robert 2022 同时属于 4.4（合成数据）与 5.4（冷启动）。同一篇在不同小节承担不同论证角色。

---

## 1. ABAG 表位多样性：什么算「不同的表位」

这一类的核心问题不是「怎么算距离」，而是**距离算在什么对象上**：接触残基集合、结合几何、竞争关系、还是逃逸谱。四者在文献里被分别使用，且不等价。

### 1.1 表位分类体系与社区划分

#### [Structural analysis of B-cell epitopes in antibody:protein complexes, (Kringelum et al., 2013, Molecular Immunology, University of Copenhagen)]([no-url])

系统分析实验解析的抗体-蛋白复合物，刻画表位的几何与理化性质。表位由三维接触定义，因此序列上相距很远的残基可以属于同一个结合面。这支持在空间残基邻域上而非抗原序列窗口上度量多样性。

#### [Computational characterization of B-cell epitopes, (Rubinstein et al., 2008, Molecular Immunology, Weizmann Institute of Science)]([no-url])

比较表位与抗原其他表面区域的结构与理化性质。其基于接触的定义为比较表位组成、可及性与几何提供了基础。这类描述子刻画了表位差异，但**不能确立两个表位在功能上不同**。

#### [The Immune Epitope Database (IEDB): 2018 update, (Vita et al., 2019, Nucleic Acids Research, La Jolla Institute for Immunology)]([no-url])

描述一个将表位连接到来源抗原、物种、宿主与实验测定的策展资源，包含不连续表位。这些注释提供了若干互补的分类轴，而非统一的表位距离度量。做多样性统计时须区分「唯一表位记录」与「独立抗原家族、表面区域、测定情境」。

#### [Structures of Human Antibodies Bound to SARS-CoV-2 Spike Reveal Common Epitopes and Recurrent Features of Antibodies, (Barnes et al., 2020, Cell, California Institute of Technology)](https://doi.org/10.1016/j.cell.2020.06.025)

提出一个影响广泛的 SARS-CoV-2 RBD 抗体分类，依据结合位置、ACE2 竞争关系、以及在不同 spike 构象下的可及性。识别重叠区域的抗体可以在接近角度与构象可及性上不同。因此表位多样性包含**结合几何与抗原状态**，不只是接触残基身份。

#### [Defining variant-resistant epitopes targeted by SARS-CoV-2 antibodies: A global consortium study, (Hastie et al., 2021, Science, Scripps Research)](https://doi.org/10.1126/science.abh2315)

整合竞争测定、结构信息与功能表征，把抗体组织成若干表位社区（七个 RBD 定向抗体社区）。社区捕捉相关的识别模式，而变体敏感性在社区内与社区间提供功能区分。这是同时在配对数据集上报告结构覆盖与抗性谱覆盖的可用模型。

#### [Omicron escapes the majority of existing SARS-CoV-2 neutralizing antibodies, (Cao et al., 2022, Nature, Peking University)](https://doi.org/10.1038/s41586-021-04385-3)

用高通量酵母展示测定 247 个抗 RBD 中和抗体的逃逸突变谱，并对中和抗体做无监督聚类，得到六个表位组（A–F），作者报告该分组与知识驱动的结构分类高度一致。这是**「功能分组 = 结构分组」这一等价命题最直接的经验证据**，也是本仓库最该先锚定的事实之一。注意分组依据是逃逸谱而非接触残基。

#### [Mapping the antigenic and genetic evolution of influenza virus, (Smith et al., 2004, Science, University of Cambridge)]([no-url])

引入抗原制图，用血清学测定把病毒与血清定位到低维抗原空间。距离总结的是识别上的功能差异，揭示了仅凭遗传距离看不到的关系。这是度量抗原多样性的基础方法，但推断出的几何依赖于血清面板与测定。

#### [A neutralizing antibody selected from plasma cells that binds to group 1 and group 2 influenza A hemagglutinins, (Corti et al., 2011, Science, Humabs BioMed / Institute for Research in Biomedicine)]([no-url])

表征一个识别流感 A 两个主要组别共有的血凝素茎部表位的抗体。说明**抗原序列多样性可以与保守的抗体识别并存**。交叉反应广度必须在抗原面板上直接测量，并与序列多样性分开报告。

### 1.2 表位距离与抗原图谱

#### [Quantifying influenza vaccine efficacy and antigenic distance, (Gupta et al., 2006, Vaccine, [待核])]([no-url])

把抗原距离与疫苗有效性联系起来，是「抗原距离」作为可计算量的早期系统化工作。距离定义在血凝素序列差异上，仅部分反映功能差异。对本仓库的意义：**这正是会上「抗原多样性是否可用序列刻画」的否命题方**。

#### [Influenza hemagglutinin antigenic distance measures capture trends in HAI differences and infection outcomes, but are not suitable predictive tools, (Skarlupka et al., 2020, Vaccine, University of Georgia)](https://doi.org/10.1016/j.vaccine.2020.06.042)

评估多种基于氨基酸替换的抗原距离度量作为 HAI 滴度差与临床结局的预测工具。距离度量确实描述了趋势，但结果变量的变异导致预测区间极宽。**结论是这类序列抗原距离不能当作预测工具**——对「用序列近似表位多样性」是一个明确的负面证据。

#### [Antigenic cartography of SARS-CoV-2 reveals that Omicron BA.1 and BA.2 are antigenically distinct, (van der Straten et al., 2022, [待核])]([no-url])

把抗原制图方法用在 SARS-CoV-2 变体上，显示 BA.1 与 BA.2 在抗原空间上可分。说明即使在同谱系内部，功能层面的多样性也未必由遗传距离反映。

#### [CE-BLAST makes it possible to compute antigenic similarity for newly emerging pathogens, (Qiu et al., 2018, Nature Communications, [待核])]([no-url])

提出对新兴病原体可在无血清面板时计算抗原相似性的方法。这类方法的价值在于**覆盖度盲区**：没有实验血清时，抗原多样性只能靠计算代理。

#### [The geometry of shape space: application to influenza, (Smith et al., 2001, Journal of Theoretical Biology, [待核])]([no-url])

把免疫学的 shape space 形式化为可计算的几何结构，并用流感数据检验。提供了把「抗原-抗体距离」当作度量空间的公理化基础。注意：shape space 的维度与度量并不由数据唯一确定。

#### [Rethinking "shape space": evidence from simulated docking suggests that steric shape complementarity is not limited to dissimilar shapes, (Perelson & Oster?, 1994, [待核])]([no-url])

用模拟对接质疑「形状互补意味着形状相异」的直觉假设。对本仓库的直接意涵：**界面互补性不能简化为单一形状距离**，这支持把界面比较做成多描述子而非单标量。

### 1.3 Paratope / Epitope 的对应关系

#### [Ab-Ligity: identifying sequence-dissimilar antibodies that bind to the same epitope, (Wong et al., 2021, mAbs, University of Oxford)](https://doi.org/10.1080/19420862.2021.1873478)

提出一个专门针对抗体-抗原界面的结构相似性度量，在预测 paratope 的模型结构上评估其识别「靶向高度相似表位的抗体」的能力。多数采用相似结合模式的抗体可仅凭序列相似性（如克隆分型）识别；**在困难子集上才需要结构度量**。这个「序列够用的比例」是设计筛选策略的关键数字。

#### [Epitope profiling using computational structural modelling demonstrated on coronavirus-binding antibodies, (Robinson et al., 2021, PLoS Computational Biology, University of Oxford)](https://doi.org/10.1371/journal.pcbi.1009675)

基于结构建模与聚类做表位画像。在 Coronavirus Antibody Database 上，多占据结构簇中 **92% 的抗体结合一致的域**。作者结论是免疫应答的收敛程度高于序列方法所提示的——**序列多样性会高估真实表位多样性**。

#### [Structure-free antibody paratope similarity prediction for in silico epitope binning via protein language models, (Ghanbarpour et al., 2023, iScience, [待核])](https://doi.org/10.1016/j.isci.2023.106036)

用蛋白语言模型预测 paratope，再以 pLM 表示度量抗体间相似性，从而在无结构时做表位分箱。在 SARS-CoV-2 RBD 与 EGFR 两个案例上验证。这是「无结构数据能否进入表位维度」的代表性尝试。

#### [Computational epitope binning reveals functional equivalence of sequence-divergent paratopes, (Mahita et al., 2022, Computational and Structural Biotechnology Journal, Dartmouth College)](https://doi.org/10.1016/j.csbj.2022.04.036)

系统比较基于序列、基于建模结构、基于建模相互作用三种信息做 binder 分箱的效果，用重复体（repebody）抗 IL-6 体系作为多样性来源。结论支持**在建模相互作用层面比较能识别序列差异大的功能等价 paratope**。

#### [Benchmarking antibody clustering methods using sequence, structural, and machine learning similarity measures for antibody discovery applications, (Chomicz et al., 2024, Frontiers in Molecular Biosciences, NaturalAntibody)](https://doi.org/10.3389/fmolb.2024.1352508)

横向比较克隆型、序列、paratope 预测、结构预测、embedding 五类抗体分组方法，在 binder 检测与表位制图两个任务上评估。**这是与本仓库 3.2 节「按哪种相似性聚类才任务相关」最接近的已发表基准**，应作为方法学基线精读。

#### [Comparison of sequence- and structure-based antibody clustering approaches on simulated repertoire sequencing data, (Waury et al., 2025, PLoS Computational Biology, Vrije Universiteit Amsterdam)](https://doi.org/10.1371/journal.pcbi.1013057)

在模拟的 repertoire 测序数据上比较序列聚类与结构聚类，重点看后者能否识别低序列相似但功能收敛的抗体。指出此前结构方法只在单抗原抗体集上评估过，**缺少在多样 repertoire 上的系统比较**。

### 1.4 表位多样性缺口与上限

#### [Analysis of nanobody paratopes reveals greater diversity than classical antibodies, (Mitchell & Colwell, 2018, Protein Engineering Design & Selection, University of Cambridge)](https://doi.org/10.1093/protein/gzy017)

用 156 个 VHH-抗原复合物结构与 156 个常规抗体-抗原结构对比。VHH 的 paratope 在**参与结合的骨架片段、接触残基、接触类型**上都更多样，且接触倾向与序列变异的关系不同于 VH。对多样性的意涵：把 VHH 与常规抗体放进同一个 paratope 多样性统计会低估 VHH 一侧。

#### [Structural diversity in a human antibody germline library, (Kovaltsuk et al., 2016, mAbs, University of Oxford)]([no-url])

分析人类抗体 germline 库的结构多样性，说明 germline 层面的结构覆盖是有限的。这为「抗体侧多样性的天花板」提供了一个可引用的经验数字。

#### [The repertoire of human germline VH sequences reveals about fifty groups of VH segments with different hypervariable loops, (Chothia et al., 1992, Journal of Molecular Biology, MRC Laboratory of Molecular Biology)]([no-url])

把人类 germline VH 序列归纳为约五十组，各组超变环不同。这是「抗体多样性可从有限 germline 结构类出发」这一论点的原始来源。

#### [Most marginal zone B cells in rat express germline encoded Ig VH genes and are ligand selected, (Dammers et al., [待核])]([no-url])

显示部分 B 细胞群的 VH 几乎完全 germline 编码。对多样性统计的提醒：**序列多样性低不等于功能多样性低**，选择压力可以维持窄序列谱。

#### [Structural basis for the recognition of SARS-CoV-2 by full-length human ACE2, (Yan et al., 2020, Science, Westlake University)]([no-url])

给出 ACE2-RBD 界面的原子细节，是判断「某个 RBD 表位是否与受体位点重叠」的参照。表位多样性若按「是否阻断受体结合」二分，这个结构就是判定基准。

#### [A highly conserved cryptic epitope in the receptor binding domains of SARS-CoV-2 and SARS-CoV, (Yuan et al., 2020, Science, [待核])]([no-url])

描述一个在 SARS-CoV 与 SARS-CoV-2 RBD 间保守的隐蔽表位。说明**表面可及性**（跨变体保守但平时被遮蔽）是表位多样性的一个独立维度，仅看结构差异会漏掉。

#### [Cross-Neutralization of a SARS-CoV-2 Antibody to a Functionally Conserved Site Is Mediated by Avidity, (Liu et al., 2020, [待核])]([no-url])

一个对功能保守位点的交叉中和是由亲合力（avidity）而非表位相似性介导的。对多样性统计的警告：**交叉反应广度不等于表位同一性**，亲合力可以制造假的「同一表位」信号。

#### [Broad cross-reactivity across sarbecoviruses exhibited by a subset of COVID-19 donor-derived neutralizing antibodies, (Robbiani et al., 2021, [待核])]([no-url])

部分 COVID-19 供体来源的中和抗体对沙贝病毒呈广谱交叉反应。这类抗体的存在说明「一个抗原上的表位数量」本身依赖于所考察的抗体谱系范围。

#### [Neutralization potency of monoclonal antibodies recognizing dominant and subdominant epitopes on SARS-CoV-2 Spike, ([待核], 2021, [待核])]([no-url])

区分显性（dominant）与次显性（subdominant）表位上的抗体及其中和效力。**免疫显性层级**意味着按抗体数量加权的表位分布与按功能重要性加权的分布不同，多样性指标须声明用哪一种权重。

#### [A SARS-CoV-2 variant elicits an antibody response with a shifted immunodominance hierarchy, (Greaney et al., 2022, [待核])]([no-url])

变体可以改变免疫显性层级。因此「某抗原的表位多样性」不是抗原的固有属性，而是抗原 × 免疫背景的联合属性。

#### [A computational method for immune repertoire mining that identifies novel binders from different clonotypes, ([待核], 2021, [待核])]([no-url])

用计算方法在 repertoire 中挖掘来自不同克隆型的新 binder。支持「克隆型多样性 ≠ binder 多样性」这一区分。

#### [Public Baseline and shared response structures support the theory of antibody repertoire functional commonality, ([待核], 2021, [待核])]([no-url])

提出「公共基线」概念，说明不同个体的 repertoire 在功能层面共享结构。对多样性统计的意涵：跨个体的重复不是数据冗余，而是功能收敛的证据。

#### [Convergent evolution and B-cell recirculation in germinal centers in a human lymph node, ([待核], 2023, [待核])]([no-url])

在人生发中心观察到收敛演化。收敛意味着**序列距离会系统性高估功能多样性**。

---

## 2. 抗体侧多样性：CDR 与谱系

抗体侧是会上认为「相对直观」的一侧。但文献显示这一侧的阈值同样不稳：规范类在溶液中会互相跃迁，克隆型阈值依赖连锁方式，而序列聚类与结构聚类给出的划分可以完全不同。

### 2.1 CDR 规范类与结构聚类

#### [Canonical structures for the hypervariable regions of immunoglobulins, (Chothia et al., 1987, Journal of Molecular Biology, MRC Laboratory of Molecular Biology)]([no-url])

确立许多抗体超变环只采用有限几种复发的主链构象，且与环长和特定残基相关。规范类提供了一种不同于序列一致性的结构多样性度量。但它们不构成对 CDR-H3 的完备分类，也不能单独决定结合特异性。

#### [A new clustering of antibody CDR loop conformations, (North et al., 2011, Journal of Molecular Biology, Fox Chase Cancer Center)](https://doi.org/10.1016/j.jmb.2010.10.030)

用基于方向统计的距离函数与亲和传播聚类，在 300 多个非冗余抗体结构上重建六个 CDR 环的构象分类，覆盖 28 种 CDR 长度组合（Chothia 只覆盖 20 种）。提供了「结构类数量」这一可操作计数。**两条序列不相近的 CDR 可以落在同一个构象簇**，因此序列多样性与结构多样性必须分开报告。

#### [Length-independent structural similarities enrich the antibody CDR canonical class model, (Nowak et al., 2016, mAbs, University of Oxford)](https://doi.org/10.1080/19420862.2016.1158370)

证明各 CDR 类型都存在跨长度的结构相似环，据此建立长度无关的规范类。在三个 NGS repertoire 数据集（逾百万序列）上，长度无关簇比标准方法多分类约 13.5 万条序列（约 20% 提升）。**说明聚类阈值的选取直接改变被测多样性的大小**。

#### [A penultimate classification of canonical antibody CDR conformations, (Kelow et al., 2022, [预印本], Fox Chase Cancer Center)](https://doi.org/10.1101/2022.10.12.511988)

修订 2011 年的分类，指出许多簇并非「规范」（未随结构增长而扩大），且部分簇实际代表多种构象。这是**对既有分类体系可靠性的自我修正**，引用时必须说明用的是哪一版。

#### [PyIgClassify: a database of antibody CDR structural classifications, (Adolf-Bryfogle et al., 2015, Nucleic Acids Research, Fox Chase Cancer Center)]([no-url])

把 CDR 结构分类与序列、结构注释一起公开，支持把观测到的环分配到既有构象簇。对数据集审计而言，**类覆盖度与类频次不平衡比抗体结构总数更有信息量**。

#### [Antibody CDR loops as ensembles in solution vs. canonical clusters from X-ray structures, (Fernández-Quintero et al., 2020, mAbs, University of Innsbruck)](https://doi.org/10.1080/19420862.2020.1744328)

用分子动力学结合实验结构信息，在微秒到毫秒尺度上观察到所有 CDR 环在规范簇之间存在构象跃迁，且与长度、序列组成无关。还发现**若干规范簇的中位数实际属于同一动力学极小**。这是对「CDR 结构多样性 = 规范类计数」最直接的质疑。

#### [Transitions of CDR-L3 Loop Canonical Cluster Conformations on the Micro-to-Millisecond Timescale, (Fernández-Quintero et al., 2019, [待核])]([no-url])

聚焦 CDR-L3，量化其在规范簇之间的跃迁速率。单一晶体结构给出的类归属是快照，不是该序列的固有类。

#### [Canonical structures of short CDR-L3 in antibodies, (North et al., 2014, [待核])]([no-url])

专门处理短 CDR-L3 的规范结构。短环的行为与长环不同，且样本量小；这提示**在类计数里，小样本类的存在与否对总数影响很大**。

#### [Antibody CDR loops as ensembles... / Investigating the ability of deep learning-based structure prediction to extrapolate and/or enrich the set of canonical CDR conformations, ([待核], 2024, [待核])]([no-url])

检验结构预测模型能否外推或丰富已有的规范 CDR 构象集合。若预测模型只能复现训练中见过的类，则用它补结构不会增加结构多样性——**这是用预测结构补数据前必须做的检验**。

### 2.2 序列聚类阈值与克隆型

#### [Cd-hit: a fast program for clustering and comparing large sets of protein or nucleotide sequences, (Li & Godzik, 2006, Bioinformatics, Burnham Institute for Medical Research)](https://doi.org/10.1093/bioinformatics/btl158)

引入被广泛用于冗余去除的高效序列聚类。一致性阈值定义了操作性的序列分组，但覆盖度要求与所选序列区域强烈影响这些分组的含义。**在抗体数据上，聚完整可变域与聚 CDR 回答的是不同问题，可能给出差别极大的划分**。

#### [MMseqs2 enables sensitive protein sequence searching for the analysis of massive data sets, (Steinegger & Söding, 2017, Nature Biotechnology, Seoul National University / Max Planck Institute)](https://doi.org/10.1038/nbt.3988)

提供可扩展且灵敏的蛋白序列搜索，支持同源检测与冗余控制。它能发现朴素去重漏掉的关系。做抗原划分时，基于序列的分离**仍须审计共享折叠、保守表位与交叉反应家族**。

#### [Hierarchical clustering can identify B cell clones with high confidence in Ig repertoire sequencing data, (Gupta et al., 2017, The Journal of Immunology, Yale University)]([no-url])

在兼容的 V/J 与连接长度组内，用连接序列距离评估层次聚类的克隆指派。距离定义、连锁方式与聚类阈值都会影响推断出的克隆结构。**相关阈值是一个经过验证的克隆推断参数，而不是适用于结合特异性的通用 CDR 一致性截断**。

#### [Change-O: a toolkit for analyzing large-scale B cell immunoglobulin repertoire sequencing data, (Gupta et al., 2015, Bioinformatics, Yale University)]([no-url])

提供 repertoire 处理、克隆分组、germline 重建与谱系分析工具。其框架区分单个序列与同一 B 细胞克隆的相关成员。用在配对数据集上，可避免把单一谱系的密集采样误当作宽抗体多样性。

#### [A bioinformatic framework for immune repertoire diversity profiling enables detection of immunological status, (Greiff et al., 2015, Genome Medicine, University of Oslo)]([no-url])

用多样性剖面（diversity profiles）刻画 repertoire 分布，而非压成单一丰富度或熵值。对本仓库的用法：**同样的剖面可用来描述序列簇、谱系或结构类的频次分布**，但须声明采样深度与计数单位。

#### [Precise determination of the diversity of a combinatorial antibody library gives insight into the human immunoglobulin repertoire, (Glanville et al., 2009, PNAS, [待核])]([no-url])

对组合抗体库的多样性做精确测定，并据此推断人类免疫球蛋白 repertoire。是把测序深度与多样性估计耦合起来的经典范例。

#### [Diversity and clonal selection in the human T-cell repertoire, (Qi et al., 2014, PNAS, [待核])]([no-url])

用测序估计人类 T 细胞 repertoire 的多样性与克隆选择。方法上与本仓库的可迁移点：**如何把「未观测到的克隆」纳入总量估计**。

#### [Commonality despite exceptional diversity in the baseline human antibody repertoire, (Briney et al., 2019, Nature, [待核])](https://doi.org/10.1038/s41586-018-0879-5)

在极高的基线多样性中仍发现公共性（commonality）。对数据收集的直接意涵：**「没见过的抗体」不等于「没见过的结合模式」**，公共性使得按序列去重会高估新颖度。

### 2.3 结构 / 表面聚类用于抗体

#### [Surface ID: a geometry-aware system for protein molecular surface comparison, (Riahi et al., 2023, Bioinformatics, Sanofi)](https://doi.org/10.1093/bioinformatics/btad196)

基于几何与化学特征的几何深度学习系统，做高通量表面比较，并提供一种新的分组与对齐算法，可用于按功能聚类蛋白。文中报告其在表面相似性评估上表现最好。这是**「界面/表面作为独立比较空间」最现成的工具**。

#### [Benchmarking antibody clustering methods using sequence, structural, and machine learning similarity measures for antibody discovery applications, (Chomicz et al., 2024, Frontiers in Molecular Biosciences, NaturalAntibody)](https://doi.org/10.3389/fmolb.2024.1352508)

（与 1.3 同篇，此处作为结构侧证据引用）在 binder 检测任务上，各方法差异不显著；**在表位制图任务上结构类方法才有优势**。这一「任务依赖」结论正是仓库 3.2 节要验证的东西。

#### [Tokenizing loops of antibodies, (Fang et al., 2026, mAbs, Genentech)](https://doi.org/10.1080/19420862.2026.2645271)

提出 Igloo，一个同时编码主链二面角与序列的多模态抗体环 tokenizer，用对比学习把主链二面角相近的环拉近。对所有环都能给出 token，**解决了规范簇覆盖面有限的问题**，同时仍能恢复规范构象。在检索最相似 H3 环上比现有方法高 6.1%。

#### [Structural Analysis and Epitope Prediction of S2 Domain of SARS-CoV-2 ..., ([待核], 2023, [待核])]([no-url])

对 SARS-CoV-2 S2 域做结构分析与表位预测，并在主要变体间比较保守性。提供了一个「同一抗原因变体而异」的具体表位覆盖案例。

#### [Structural comparison of somatically related PG9 and PG16 in complex with their epitope reveals differences in ..., ([待核], 2012, [待核])]([no-url])

两个体细胞相关的抗体结合同一类表位却有不同的识别细节。**体细胞相关性（序列近）不保证表位同一性**。

### 2.4 谱系与 germline 多样性

#### [Addressing the antibody germline bias and its effect on language models for improved antibody design, (Olsen et al., 2024, Bioinformatics, University of Oxford)](https://doi.org/10.1093/bioinformatics/btae618)

指出天然抗体序列的可变域大部分保持 germline，这在抗体语言模型预训练中引入对 germline 残基的强偏置，而离开 germline 的突变往往是获得功能的关键。**对本仓库的意涵：用 LM 表示做多样性统计时，germline 偏置会压缩真实差异**。

#### [The repertoire of human germline VH sequences reveals about fifty groups of VH segments with different hypervariable loops, (Chothia et al., 1992, Journal of Molecular Biology, MRC Laboratory of Molecular Biology)]([no-url])

（与 1.4 同篇，此处作为谱系侧基础引用）约五十组 VH，每组超变环不同——这是抗体结构多样性的 germline 底数。

#### [Germline-encoded amino acid-binding motifs drive immunodominant public antibody responses, (Sangesland et al., 2023, [待核])]([no-url])

germline 编码的氨基酸结合基序驱动免疫显性的公共抗体应答。解释了为什么跨个体出现相同结合模式：**公共性源自 germline，而非数据重复**。

#### [Germline VH/VL pairing in antibodies, (Jayaram et al., 2012, [待核])]([no-url])

分析 VH/VL 的 germline 配对偏好。配对不是随机的，因此**按单链统计多样性会高估组合多样性**。

#### [Antibody Heavy Chain Variable Domains of Different Germline Gene Origins Diversify through Different Paths, (Sheng et al., 2017, [待核])]([no-url])

不同 germline 来源的 VH 通过不同路径多样化。单一多样性指标在不同 germline 子群上含义不同。

#### [The mouse antibody heavy chain repertoire is germline-focused and highly variable between inbred strains, (Collins et al., 2015, [待核])]([no-url])

不同近交系间重链 repertoire 差异很大。**多样性的「基线」是物种/品系属性**，跨物种汇总前必须分层。

### 2.5 VHH / 单域抗体的特殊性

#### [Analysis of nanobody paratopes reveals greater diversity than classical antibodies, (Mitchell & Colwell, 2018, PEDS, University of Cambridge)](https://doi.org/10.1093/protein/gzy017)

（见 1.4）VHH 的 paratope 多样性高于常规抗体，接触类型也不同。

#### [Comparative analysis of nanobody sequence and structure data, (Mitchell & Colwell, 2018, Proteins, University of Cambridge)]([no-url])

系统比较纳米抗体的序列与结构数据特征。为「VHH 能否与 Fab 放进同一个聚类空间」提供了经验边界。

#### [Analysis and modeling of the variable region of camelid single-domain antibodies, (Sircar et al., 2011, [待核])]([no-url])

对骆驼科单域抗体可变区做分析与建模。框架区的补偿性接触在 VHH 中更常见，呼应会上「CDR 之外的接触位点」。

#### [Camel heavy-chain antibodies: diverse germline V(H)H and specific mechanisms enlarge the antigen-binding repertoire, (Nguyen et al., 2000, EMBO Journal, [待核])]([no-url])

VHH 通过多样的 germline 与特定机制扩大抗原结合 repertoire。说明**VHH 的多样性来源与常规抗体不同**，不能套用 CDR 规范类框架。

---

## 3. 广义 PPI 与蛋白表面比较方法

这一节是工具库。核心分歧在于**比较的粒度**：整链折叠、局部表面 patch、界面残基集合、还是接触图。四者回答不同问题，且都不能直接等同于「表位是同一个」。

### 3.1 界面残基集合比较与对接质量度量

#### [DockQ: A Quality Measure for Protein-Protein Docking Models, (Basu & Wallner, 2016, PLoS ONE, RWTH Aachen University)]([no-url])

把 native contact 恢复率、界面 RMSD、配体 RMSD 组合成一个连续的对接质量分数。其分量在伙伴与残基对应关系确定后，可直接用于比较界面。**但 DockQ 是参照式的模型评估，不是无关联表位之间的一般距离**。

#### [iAlign: a method for the structural comparison of protein–protein interfaces, (Gao & Skolnick, 2010, Bioinformatics, Georgia Institute of Technology)]([no-url])

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

#### [Optimal contact map alignment of protein-protein interfaces, (Pulim et al., 2008, [待核])]([no-url])

用接触图对齐比较蛋白-蛋白界面。接触图把界面抽象成图结构，天然适合「残基在序列上不连续但空间相邻」的情形。

#### [1001 optimal PDB structure alignments: integer programming methods for finding the maximum contact map overlap, (Caprara et al., 2004, [待核])]([no-url])

把结构对齐形式化为最大接触图重叠问题并用整数规划精确求解。提供接触图相似的**理论最优基准**，可用于检验启发式方法的损失。

#### [Evolution and similarity evaluation of protein structures in contact map space, (Ding et al., 2005, [待核])]([no-url])

在接触图空间评价蛋白结构的演化与相似性。接触图距离的演化含义是可解释的，这在解释多样性指标时有用。

### 3.2 表面 patch 几何描述子

#### [Fast protein tertiary structure retrieval based on global surface shape similarity, (Sael et al., 2008, Proteins, Purdue University)]([no-url])

用紧凑的三维 Zernike 描述子表示蛋白表面形状，支持旋转不变的比较。展示了无需逐残基序列对齐即可量化几何相似性。**其描述子描述的是全局形状，用于表位须另行验证局部 patch 表示**。

#### [Protein-protein docking using region-based 3D Zernike descriptors, (Venkatraman et al., 2009, BMC Bioinformatics, Purdue University)](https://doi.org/10.1186/1471-2105-10-407)

把 3D Zernike 描述子用在基于区域的对接上。区域级描述子的成功说明**局部几何签名足以支撑识别**。

#### [Molecular surface representation using 3D Zernike descriptors for protein shape comparison and docking, (Kihara et al., 2011, [待核])]([no-url])

综述并扩展用 3D Zernike 描述子做分子表面表示、形状比较与对接。是表面几何描述子的方法学参考。

#### [Exploring the potential of 3D Zernike descriptors and SVM for protein-protein interface prediction, (Daberdaku & Ferrari, 2018, BMC Bioinformatics, University of Padova)](https://doi.org/10.1186/s12859-018-2084-7)

把 3D Zernike 描述子与 SVM 结合做界面预测。说明几何描述子携带的界面信息足以训练分类器。

#### [Rapid automated superposition of shapes and macromolecular models using spherical harmonics, (Konarev et al., 2016, Journal of Applied Crystallography, EMBL Hamburg)](https://doi.org/10.1107/s1600576716005793)

用球谐函数在傅里叶空间做快速形状叠合，比实空间算法快一个数量级，适合低分辨率形状模型。**对只有低分辨率或预测结构的数据集，这是可用的表面比较路径**。

#### [Travel depth, a new shape descriptor for macromolecules: application to ligand binding, (Coleman & Sharp, 2006, Journal of Molecular Biology, [待核])]([no-url])

提出 travel depth 作为大分子形状描述子。凹度/深度是表位描述中常被忽略但直接影响抗体可及性的一维。

#### [Surface-histogram: a new shape descriptor for protein-protein docking, (Axenopoulos et al., 2012, [待核])]([no-url])

提出表面直方图描述子用于对接。提供了与 Zernike 互补的另一种旋转不变表示。

#### [FTIP: an accurate and efficient method for global protein surface comparison, (Lee et al., 2020, [待核])]([no-url])

提出全局蛋白表面比较方法。是对比「全局表面相似 vs 局部 patch 相似」两种粒度的现成工具。

#### [Matching protein surface structural patches for high-resolution blind peptide docking, (Khashan et al., 2022, [待核])]([no-url])

用表面结构 patch 匹配做高分辨率盲肽对接。patch 匹配在肽-蛋白场景可行，说明**短表位（线性肽）与构象表位可以用同一套 patch 语言描述**。

#### [Conformational epitope matching and prediction based on protein surface spiral features, (Sun et al., 2021, [待核])]([no-url])

用表面螺旋特征做构象表位匹配与预测。是少数**把表面特征直接用于表位（而非一般结合位点）**的工作。

#### [3D-SURFER: software for high-throughput protein surface comparison and analysis, (Sael et al., 2009, Bioinformatics, Purdue University)]([no-url])

高通量蛋白表面比较软件。工程上可直接用于 `data/raw/public/` 的大规模表面素描。

#### [Protein surface similarities: a survey of methods to describe and compare protein surfaces, (Via et al., 2000, [待核])]([no-url])

综述描述与比较蛋白表面的方法。是入门的分类学参考，也是判断「哪些描述子够用」的历史基线。

### 3.3 局部结构比对与结合位点相似

#### [ProBiS algorithm for detection of structurally similar protein binding sites by local structural alignment, (Konc & Janežič, 2010, Bioinformatics, University of Ljubljana)]([no-url])

用局部结构比对检测结构相似的蛋白结合位点，包括无同源关系的蛋白。**ProBiS 的核心主张——局部结合位点相似性可以跨越全局折叠差异——正是「表面 patch 聚类」的理论支撑**。

#### [ProBiS-database: precalculated binding site similarities and local pairwise alignments of PDB structures, (Konc & Janežič, 2012, [待核])]([no-url])

把 ProBiS 的局部比对结果预计算成数据库。可作为「已有局部位点相似性」的现成资源。

#### [Detecting local ligand-binding site similarity in nonhomologous proteins by surface patch comparison, (Xiong et al., 2012, [待核])]([no-url])

用表面 patch 比较在非同源蛋白间检测局部结合位点相似性。直接对标「表位相似但不共享序列/折叠」的情形。

#### [Supersites within superfolds. Binding site similarity in the absence of homology, (Russell, 1998, Journal of Molecular Biology, [待核])]([no-url])

在无同源性的超折叠内部识别相似的结合位点（supersites）。这是「结合位点相似性独立于折叠相似性」的早期关键证据。

#### [SiteMine: Large-scale binding site similarity searching in protein structure databases, (Schmidt et al., 2024, [待核])]([no-url])

在蛋白结构数据库上做大规模结合位点相似性搜索。工程上对应「在全库尺度上做界面聚类」的可行性验证。

#### [Structural motif search across the protein universe with Folddisco, (2026, [待核])]([no-url])

把结构模体搜索推广到全蛋白宇宙。对表位这类局部模体的检索是直接可用的方法论。

#### [Identifying protein biochemical functions by similarity search using the molecular surface database eF-site, (Kinoshita et al., 2003, [待核])]([no-url])

用分子表面数据库做相似性搜索以识别生化功能。表面相似性可用于功能注释，说明其捕捉的是功能相关特征而非偶然几何。

#### [Protein functional surfaces: global shape matching and local spatial alignments of ligand binding sites, (Tseng et al., 2008, [待核])]([no-url])

结合全局形状匹配与局部空间对齐全。

#### [Binding site similarity analysis for the functional classification of the protein kinase family, (Bryant et al., 2009, [待核])]([no-url])

用结合位点相似性做蛋白激酶家族的功能分类。**用结合位点相似性做分类**是「以界面为多样性空间」的直接先例。

### 3.4 接触图谱与图相似

#### [TM-align: a protein structure alignment algorithm based on the TM-score, (Zhang & Skolnick, 2005, Nucleic Acids Research, University of Michigan)]([no-url])

用 TM-score 优化结构对齐，提供整体折叠相似性的标准度量。可用于识别抗原的折叠冗余，并在比较映射的表位残基前建立结构对应关系。**全局折叠相似性本身不能确立两个抗体识别等价的表面 patch**。

#### [US-align: universal structure alignments of proteins, nucleic acids, and macromolecular complexes, (Zhang et al., 2022, Nature Methods, University of Missouri)]([no-url])

把结构对齐推广到蛋白、核酸与复合物。**对 ab-ag 复合物，可整复合物对齐**，这是比较「结合模式」而非「单侧结构」的现成手段。

#### [MM-align: a quick algorithm for aligning multiple-chain protein complex structures using iterative dynamic programming, (Mukherjee & Zhang, 2009, Nucleic Acids Research, University of Michigan)]([no-url])

用迭代动态规划做多链复合物结构对齐。复合物对齐是判断「两个抗体-抗原对是否同构」的直接方法。

#### [Rapid automated superposition of shapes and macromolecular models using spherical harmonics, (Konarev et al., 2016, J Appl Cryst, EMBL Hamburg)](https://doi.org/10.1107/s1600576716005793)

（见 3.2）低分辨率形状叠合。

#### [CMView: interactive contact map visualization and analysis, (Vejnar et al., 2011, [待核])]([no-url])

接触图可视化与分析工具。工程上便于人工审查候选表位簇。

#### [Fast and accurate protein structure search with Foldseek, (van Kempen et al., 2024, Nature Biotechnology, Seoul National University / ETH Zurich)]([no-url])

用结构字母表编码三级残基环境，实现大规模结构相似性搜索。提供发现抗原结构近邻并把大数据集组织成结构组的现成机制。**整链相似性与表位相似性是不同的量，须辅以局部界面比较**。

### 3.5 表面指纹作为设计目标

#### [Deciphering interaction fingerprints from protein molecular surfaces using geometric deep learning, (Gainza et al., 2020, Nature Methods, EPFL)](https://doi.org/10.1038/s41592-019-0666-6)

提出 MaSIF，从几何与化学特征中学习局部分子表面 patch 的描述子。描述子比较支持表面识别与相互作用兼容性评估。**这些 embedding 是表位聚类的候选，但其训练目标与对构象的敏感性须先检查，才能把 embedding 距离当作生物多样性**。

#### [De novo design of protein interactions with learned surface fingerprints, (Gainza et al., 2023, Nature, EPFL / University of Washington)](https://doi.org/10.1038/s41586-023-05993-x)

在 MaSIF 基础上设计针对 SARS-CoV-2 spike、PD-1、PD-L1、CTLA-4 的 de novo binder，多个设计获得实验验证。**这是「表面指纹足以编码识别特异性」的最强反向证明**：如果学习到的表面描述子不能区分不同 patch，就不可能用它设计出特异性 binder。

#### [Decoding Protein-Membrane Binding Interfaces from Surface-Fingerprint-Based Geometric Deep Learning, ([待核], 2025, [待核])]([no-url])

把表面指纹用于蛋白-膜界面。说明该表示不限于可溶性蛋白结合。

#### [An explainable language model for antibody specificity prediction using curated influenza hemagglutinin antibody data, (Xu et al., 2024, [待核])]([no-url])

用策展的流感 HA 抗体数据训练可解释语言模型预测抗体特异性。特异性预测本身可看作表位多样性的下游检验。

#### [A Pharmacophore-Based Method for Rapid and Accurate Virtual Screening of Antibody Libraries against Antigens, ([待核], 2025, [待核])]([no-url])

用药效团方法做抗体库对映抗原的虚拟筛选。提供了「以化学特征而非几何比较界面」的补充视角。

---

## 4. 多样性作为评估工具：冗余、泄漏、划分

这一节是仓库 3.2 节「按相似性聚类 → 划分 → 看指标是否下降 ⇒ 该维度承载真实泄漏」的方法学前身。**核心发现：这一步单独做不成立**——指标下降也可以由训练集变小、分布偏移来解释，必须有对照。

### 4.1 冗余去除与代表集选择

#### [Choosing non-redundant representative subsets of protein sequence data sets using submodular optimization, (Libbrecht et al., 2018, Proteins, University of Washington)](https://doi.org/10.1002/prot.25461)

指出 CD-HIT、PISCES、UCLUST 等启发式阈值算法没有理论保证，提出用次模优化选代表集。以 SCOPe 结构库为金标准，**次模优化在同样规模下覆盖更多的 SCOPe 域家族**。这是「多样性可以用覆盖目标形式化」的直接证据，也是回答「90–100 个抗原够不够」的可用工具。

#### [Identifying representative sequences of protein families using submodular optimization, ([待核], 2025, [待核])]([no-url])

把次模优化用在蛋白家族的代表序列选择上。方法学延续。

#### [Removing near-neighbour redundancy from large protein sequence collections, (Holm & Sander, 1998, Bioinformatics, EMBL-EBI)]([no-url])

从大规模蛋白序列集合中去除近邻冗余。这是 PDB/SCOP 层面冗余控制的原始工作，**冗余阈值的选择在此已被显式讨论**。

#### [Protein sequence redundancy reduction: comparison of various method, ([待核], 2010, [待核])]([no-url])

比较不同的序列冗余削减方法。给出方法间差异的量化，可用于论证阈值敏感度。

#### [Redundancy-weighting the PDB for detailed secondary structure prediction using deep-learning models, ([待核], 2020, [待核])]([no-url])

用冗余加权处理 PDB 用于深度学习。**冗余加权 vs 硬去重**是两种不同的处理哲学，前者保留频次信息，后者丢弃。多样性统计须明确用哪一种。

#### [The influence of dataset homology and a rigorous evaluation strategy on protein secondary structure prediction, ([待核], 2021, [待核])]([no-url])

显示数据集同源性对二级结构预测评估的影响。跨任务证据：**同源性控制不严会系统性高估性能**。

#### [Dataset size and composition impact the reliability of performance benchmarks for peptide-MHC binding prediction, (Kim et al., 2014, [待核])]([no-url])

数据集规模与组成影响 pMHC 结合预测基准的可靠性。**「数据集组成」即多样性**，此处被显式当作影响结论的变量。

#### [PLINDER: The protein-ligand interactions dataset and evaluation resource, (Durairaj et al., 2024, [待核])]([no-url])

提出一个带有多轴质量与相似性标注的蛋白-配体交互数据集与评估资源。其组织方式（每条记录带最近邻与相似性分层）**可直接借鉴为 ab-ag 数据集的 schema**。

#### [PiNUI: A Dataset of Protein–Protein Interactions for Machine Learning, (Bushuiev et al., 2023, [待核])]([no-url])

面向机器学习的 PPI 数据集，强调数据划分与质量控制。是与 ab-ag 最接近的一般 PPI 类比。

### 4.2 泄漏感知划分与基准

#### [Flaws in evaluation schemes for pair-input computational predictions, (Park & Marcotte, 2012, Nature Methods, University of Texas at Austin)]([no-url])

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

#### [What does AlphaFold3 learn about antibody and nanobody docking, and what remains unsolved?, ([待核], 2025, [待核])]([no-url])

专门分析 AF3 在抗体与纳米抗体对接上学到了什么。是评估「用预测结构补表位维度」是否可靠的关键文献。

#### [Benchmarking Boltz-2 for Screening of Therapeutic Antibody-Antigen Interactions, ([待核], 2026, [待核])]([no-url])

基准 Boltz-2 在治疗性抗体-抗原相互作用筛选上的表现。可作为 co-folding 路线的可用性证据。

#### [Evaluating Protein Transfer Learning with TAPE, (Rao et al., 2019, NeurIPS, Stanford University)](https://arxiv.org/abs/1906.08230)

提出一套蛋白学习基准，含针对「超越训练近邻」的泛化测试。说明**明确指定训练与测试之间生物关系的重要性**。类比地，抗体基准应显式说明其划分测试的是新序列、新谱系、新抗原家族，还是新结合面。

#### [ATOM3D: Tasks on Molecules in Three Dimensions, (Townshend et al., 2021, NeurIPS Datasets and Benchmarks, Stanford University)]([no-url])

提供标准化的三维分子学习任务（含蛋白界面预测），并带任务特定的数据集构造与划分。对本仓库的用处：**「聚类再划分，看性能下降」这一实验，性能下降只证明模型对该分布偏移敏感；要主张泄漏，必须控制训练规模与其他划分差异**。

#### [A new framework for evaluating model out-of-distribution generalisation for the biochemical domain, ([待核], 2024, [待核])]([no-url])

提出生化领域 OOD 泛化评估框架。可提供「分布偏移」与「泄漏」的区分标准。

#### [Out-of-distribution generalization enhances protein function annotation for low-homology sequences, ([待核], 2026, [待核])]([no-url])

低同源序列上的 OOD 泛化。与 ab-ag 的未见抗原情形同构。

#### [Strict OOD Antigen-to-Antibody Retrieval with CDR-Aware Slot Late Interaction, ([待核], 2026, [待核])]([no-url])

在严格 OOD 设定下做抗原到抗体的检索。**检索任务比预测任务更适合做多样性评估**，因为不需要亲和力标签。

### 4.3 数据集的多样性 / 偏置诊断

#### [MHChron: diversity-balanced dataset design for robust peptide–MHC binding prediction across MHC class I and II, ([待核], 2026, [待核])]([no-url])

用多样性均衡的数据集设计提升 pMHC 结合预测的稳健性。**「多样性均衡」作为数据设计目标，而非事后度量**，这是仓库可以直接借用的框架。

#### [A curated structural dataset of peptide-protein complexes reveals biases in existing datasets and principles of ..., ([待核], 2026, [待核])]([no-url])

策展肽-蛋白复合物数据集，并由此揭示既有数据集的偏置。方法论上与本仓库的「数据现状摸底」任务同构。

#### [Benchmark Bias and Conformational Dynamics in Allosteric Site Prediction, ([待核], 2026, [待核])]([no-url])

揭示变构位点预测中的基准偏置与构象动力学问题。跨任务的偏置诊断范例。

#### [The importance of residue-level filtering and the Top2018 best-parts dataset of high-quality protein residues, ([待核], 2022, [待核])]([no-url])

强调残基级过滤的重要性并给出高质量数据集。**质量过滤会改变多样性**：过滤越严，残余多样性越低。

#### [Graphinity 实验派生/计算 ΔΔG, (R50)]([no-url])

（本仓库已接入的数据源）合并实验派生与计算的 ΔΔG，**计算标签与实验标签混在同一表里**，是多样性统计须先分层的典型例子。

#### [A unified peptide array platform for antibody epitope binning, mapping, specificity and predictive off-target ..., ([待核], 2022, [待核])]([no-url])

统一的肽阵列平台同时做分箱、制图、特异性与脱靶预测。工程上把多种表位测量压到一条流水线。

### 4.4 合成数据与可控多样性

#### [Unconstrained generation of synthetic antibody-antigen structures to guide machine learning methodology for antibody specificity prediction, (Robert et al., 2022, Nature Computational Science, University of Oslo)](https://doi.org/10.1038/s43588-022-00372-4)

提出 Absolut!，可参数化无约束生成基于晶格的 3D 抗体-抗原结合结构，且**对构象 paratope、epitope 与亲和力有真值**。把常见免疫学特异性预测问题形式化为 ML 任务，并确认在实验数据上训练的方法排序与在 Absolut! 数据上一致。**这是验证「哪种相似性维度承载真实泄漏」最干净的沙盒：多样性可调，真值已知**。

#### [Machine learning optimization of candidate antibody yields highly diverse sub-nanomolar affinity antibody libraries, (Li et al., 2023, Nature Communications, MIT)](https://doi.org/10.1038/s41467-023-39022-2)

端到端贝叶斯、语言模型驱动的方法，设计大且多样的高亲和力 scFv 库并经实验测量。**显式比较库的预测成功率与实际测量，展示「库成功率」与「多样性」之间的权衡**。这是少数真正把多样性当作可调参数而非事后统计的工作。

#### [Insight into the libraries: Precise determination of the diversity of a combinatorial antibody library..., (Glanville et al., 2009, PNAS, [待核])]([no-url])

（与 2.2 同篇）组合库多样性的精确测定。

---

## 5. 多样性 × 数据量 × 性能

**这一节的文献支持弱于预想，且有多条方向相反的结论。** 直接做「多样性 × 数据量 × 参数」三方联合的工作极少；通用的缩放律文献（Kaplan、Hoffmann）针对语言模型，其指数不可移植。更值得注意的是 Hou 2026 的结论——**蛋白语言模型越大，fitness 预测反而越差**——与会上「参数量须随数据量同步调整」的假设方向相反。

### 5.1 缩放律与饱和

#### [Understanding language model scaling for protein fitness prediction, (Hou et al., 2026, Nature Computational Science, UCSF)](https://doi.org/10.1038/s43588-026-01010-z)

指出模型规模、训练数据与随机因素都会使预测的 p(sequence) 偏离真实 fitness。**性能取决于 p(sequence) 是否匹配同源序列的演化模式，而对多数蛋白这在中等的 p(sequence) 水平上最优；超过某个规模后性能下降**。大模型倾向于预测更高的 p(sequence)，可能超出这个中等区间。**这是「参数量越大越好」的直接反例。**

#### [Evaluating the role of pretraining dataset size and diversity on single-cell foundation model performance, (DenAdel et al., 2026, Nature Methods, Harvard University)](https://doi.org/10.1038/s41592-026-03120-y)

用 2,220 万细胞预训练 400 个模型、做 6,400 次实验。**当前方法在远小于现有语料的数据规模上就性能饱和；与 LLM 不同，单细胞基础模型没有清晰的数据缩放律**，开发者应平衡模型容量、数据集规模与算力，而非无差别地同时扩大三者。**这是「数据量 × 多样性 × 参数量」三元关系在生物领域的直接经验证据，且结论是三者不存在简单缩放。**

#### [Deep Learning Scaling is Predictable, Empirically, (Hestness et al., 2017, [预印本], Baidu Silicon Valley AI Lab)](https://arxiv.org/abs/1712.00409)

跨多个领域研究经验学习曲线，识别出预测误差随训练集规模近似幂律变化的区间。它支持在多种数据规模上先测性能再外推。**但其结果不确立原始 ab-ag 配对数或抗原数是正确的缩放变量**。

#### [Scaling Laws for Neural Language Models, (Kaplan et al., 2020, [预印本], OpenAI)](https://arxiv.org/abs/2001.08361)

把语言模型 loss 建模为参数量、数据量、算力的函数。提供区分「数据受限」与「模型受限」的框架。对 ab-ag，类比实验必须同时变模型容量与数据量，并**单独追踪生物覆盖度**；已发表的指数不可直接搬运。

#### [Training Compute-Optimal Large Language Models, (Hoffmann et al., 2022, NeurIPS, DeepMind)](https://arxiv.org/abs/2203.15556)

研究训练算力应如何在模型规模与数据量之间分配，证明在数据不足时单纯增加参数量是低效的。对配对生物数据的意涵：**应评估多个模型规模，而非假定更大的模型能补偿狭窄的抗原覆盖**。

#### [Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences, (Rives et al., 2021, PNAS, Facebook AI Research)](https://doi.org/10.1073/pnas.2016239118)

研究大规模蛋白语言建模如何产生包含结构与功能信息的表示，提供「预训练规模提升表示质量」的蛋白侧证据。**但它不确立需要多少实验表征的 ab-ag 对**，因此预训练与未预训练模型须分别做下游学习曲线。

### 5.2 多样性—性能权衡的实证

#### [Machine learning optimization of candidate antibody yields highly diverse sub-nanomolar affinity antibody libraries, (Li et al., 2023, Nature Communications, MIT)](https://doi.org/10.1038/s41467-023-39022-2)

（见 4.4）显式展示库成功率与多样性之间的权衡曲线。

#### [HuCAL PLATINUM, a synthetic Fab library optimized for sequence diversity and superior performance in mammalian ... , (Prassler et al., 2011, [待核], MorphoSys)]([no-url])

一个以序列多样性为优化目标的合成 Fab 库。**工业界做法：多样性被当作库设计的显式目标函数**。

#### [Construction of a large synthetic human scFv library with six diversified CDRs and high functional diversity, ([待核], 2009, [待核])]([no-url])

六个 CDR 全多样化的大规模合成 scFv 库。说明「功能多样性」与「序列多样性」被分别追求。

#### [Next-generation sequencing enables the discovery of more diverse positive clones from a phage-displayed antibody ..., ([待核], 2017, [待核])]([no-url])

NGS 使能从噬菌体展示筛选中发现更多样的阳性克隆。**筛选深度本身决定了观测到的多样性**。

#### [Diverse high-affinity DNA aptamers for wild-type and B.1.1.7 SARS-CoV-2 spike proteins from a pre-structured ..., ([待核], 2021, [待核])]([no-url])

预结构化文库产生多样高亲和力适配体。非抗体体系，但多样性来源可类比。

### 5.3 主动学习与信息量驱动采样

#### [Active Learning for Convolutional Neural Networks: A Core-Set Approach, (Sener & Savarese, 2018, ICLR, California Institute of Technology)]([no-url])

把批量主动学习表述为选择能覆盖已学习表示空间的样本，用 core-set 形式化（与几何覆盖相关）。给出一个基于「距已表示样本的距离」的多样性操作定义。**用在抗原收集上，其效用取决于该表示是否捕捉到相关的表位变异，而非偶然的序列或结构差异**。

#### [Submodularity in Data Subset Selection and Active Learning, (Wei et al., 2015, ICML, University of Washington)]([no-url])

研究奖励覆盖且具有收益递减性质的子集选择目标。这类目标可把「选择一个代表相似空间中未覆盖区域的抗原」形式化为可优化的价值。**为 90–100 个抗原/年的预算提供原则性分配策略，但在没有覆盖度与性能测量时不能确立该预算足够**。

#### [Active learning-assisted directed evolution, (Qiu et al., 2025, [待核])]([no-url])

用主动学习辅助定向演化。是把「下一轮测什么」形式化的直接范例。

#### [ALLM-Ab: Active Learning-Driven Antibody Optimization Using Fine-Tuned Protein Language Models, ([待核], 2025, [待核])]([no-url])

用微调蛋白语言模型的主动学习优化抗体。**主动学习正是「多样性 × 预算」问题的操作化**。

#### [Using an FPLC to promote active learning... , ([待核], 2017, [待核])]([no-url])

（教学类，检索误命中，此处仅作噪声示例记录）

#### [Choosing where to look next in a mutation sequence space: Active Learning of informative p53 cancer rescue mutations, (Danciu et al., 2007, [待核])]([no-url])

在前面的变异序列空间里主动学习。早期把「信息量」当作采样准则的工作。

### 5.4 冷启动与未见抗原评估

#### [Mitigating cold-start problems in drug-target affinity prediction with interaction knowledge transferring, ([待核], 2022, [待核])]([no-url])

用相互作用知识迁移缓解药物-靶点亲和力预测的冷启动问题。**冷启动 = 未见实体**，与 ab-ag 的未见抗原同构。

#### [CS-DTA: a language model-driven framework for robust drug-target affinity prediction under strict cold-start ..., ([待核], 2026, [待核])]([no-url])

在严格冷启动设定下的 DTA 预测。提供了「严格」如何定义的可参考模板。

#### [LLMDTA: Improving Cold-Start Prediction in Drug-Target Affinity With Biological LLM, ([待核], 2025, [待核])]([no-url])

用生物 LLM 改善冷启动 DTA。

#### [Unconstrained generation of synthetic antibody-antigen structures..., (Robert et al., 2022, Nature Computational Science, University of Oslo)](https://doi.org/10.1038/s43588-022-00372-4)

（见 4.4）把特异性预测形式化为 ML 任务，并给出可复现的划分。

#### [Understanding language model scaling for protein fitness prediction, (Hou et al., 2026, Nature Computational Science, UCSF)](https://doi.org/10.1038/s43588-026-01010-z)

（见 5.1）性能并非随规模单调。

---

## 6. 实验真值：表位多样性怎么测出来

没有这一节，前面的所有计算指标都没有校准。三类实验给出三种「不同」：**竞争分箱**（是否互相阻断）、**逃逸谱**（哪些突变使识别失效）、**结构**（哪些残基接触）。它们不等价。

### 6.1 表位分箱

#### [High-throughput epitope binning assays on label-free array-based biosensors can yield exquisite epitope discrimination that facilitates the selection of monoclonal antibodies with functional activity, (Abdiche et al., 2014, PLoS ONE, Novartis Institutes for BioMedical Research)](https://doi.org/10.1371/journal.pone.0092451)

用阵列式无标记生物传感器对大量单抗做交叉阻断分析。分析的抗体对数越多，区分表位的概率越高。**关键限定：两个抗体交叉阻断是「结合同一表位」的必要非充分条件**，因此高分辨分箱能识别出「相似但独特」的表位。文中还显示表位与功能活性相关。

#### [High throughput solution-based measurement of antibody-antigen affinity and epitope binning, (Estep et al., 2013, mAbs, [待核])](https://doi.org/10.4161/mabs.23049)

基于溶液的亲和力与表位分箱高通量测量。补充了固相分箱之外的测量模式。

#### [Label-free epitope binning assays of monoclonal antibodies enable the identification of antigen heterogeneity, (Abdiche et al., 2012, Journal of Immunological Methods, Novartis)](https://doi.org/10.1016/j.jim.2012.05.010)

用分箱识别抗原的异质性。**同一个抗原制备物内部可以有多种表位状态**，这直接影响多样性分母的定义。

#### [High-throughput epitope binning of therapeutic monoclonal antibodies: why you need to bin the fridge, (Brooks et al., 2014, Drug Discovery Today, [待核])](https://doi.org/10.1016/j.drudis.2014.05.011)

主张治疗性抗体必须做分箱的立场性综述。提供了工业界为什么需要表位多样性度量的直接论述。

#### [The emerging role of biosensor-based epitope binning and mapping in antibody-based drug discovery, (Ditto & Brooks, 2016, Expert Opinion on Drug Discovery, [待核])](https://doi.org/10.1080/17460441.2016.1229295)

综述生物传感器分箱与制图在药物发现中的作用，**明确提出在早期筛选中使用分箱以确保候选具有表位多样性**。

#### [Flow Cytometry-Based Epitope Binning Using Competitive Binding Profiles for the Characterization of Monoclonal Antibodies, (Chan et al., 2018, SLAS Discovery, [待核])](https://doi.org/10.1177/2472555218774334)

用流式细胞术基于竞争结合谱做表位分箱，覆盖细胞与可溶靶点。把分箱推广到细胞表面抗原。

#### [Epitope Binning of Monoclonal and Polyclonal Antibodies by Biolayer Interferometry, (Nagashima & Mousa, 2023, Methods in Molecular Biology, [待核])](https://doi.org/10.1007/978-1-0716-3239-0_2)

BLI 分箱的实验方案。可操作性参考。

#### [Competitive Epitope Binning Using HT-SPR, (Bedinger et al., 2025, Methods in Molecular Biology, [待核])](https://doi.org/10.1007/978-1-0716-4591-8_19)

高通量 SPR 竞争分箱方案。

#### [Epitope Binning for multiple antibodies simultaneously using mammalian cell display and DNA sequencing, (Lin et al., 2024, Communications Biology, Tokyo Institute of Technology)](https://doi.org/10.1038/s42003-024-06363-7)

用哺乳动物细胞展示与 DNA 测序同时做多个抗体的表位分箱。**把分箱规模化到「同时多抗体」**，这对构造两两阻断矩阵的完整度很关键。

#### [Combining deep mutational scanning and SPR binning approaches for large-scale epitope identification of anti-ricin antibodies, (Kot et al., 2025, mAbs, [待核])](https://doi.org/10.1080/19420862.2025.2544922)

把 DMS 与 SPR 分箱结合做大规模表位识别。**两种测量互相校准**，是解决「分箱只给必要非充分条件」这一弱点的方式。

### 6.2 深度突变扫描与逃逸图谱

#### [Deep Mutational Scanning of SARS-CoV-2 Receptor Binding Domain Reveals Constraints on Folding and ACE2 Binding, (Starr et al., 2020, Cell, Fred Hutchinson Cancer Center)]([no-url])

用酵母展示的突变文库量化 RBD 替换对表达与 ACE2 结合的影响。把「与抗原功能相容的突变」与「破坏折叠或受体互作的突变」区分开。**为把抗体逃逸图谱解读为识别证据提供必要的对照**。

#### [Complete Mapping of Mutations to the SARS-CoV-2 Spike Receptor-Binding Domain that Escape Antibody Recognition, (Greaney et al., 2021, Cell Host & Microbe, Fred Hutchinson Cancer Center)]([no-url])

用 DMS 制图 RBD 突变对单个抗体识别的影响，每个抗体获得一个功能逃逸谱，可跨位点与替换比较。**结构足迹相似的两个抗体可以有不同逃逸谱**，因此突变敏感性是表位多样性的又一个独立轴。

#### [Comprehensive mapping of mutations in the SARS-CoV-2 receptor-binding domain that affect recognition by polyclonal human plasma antibodies, (Greaney et al., 2021, Cell Host & Microbe, Fred Hutchinson Cancer Center)]([no-url])

把逃逸制图推广到多克隆人血浆。结果是**不同个体在主导识别的抗原位点上存在变异**。血浆逃逸谱不唯一重构其组成抗体的特异性。

#### [Deep mutational scans for ACE2 binding, RBD expression, and antibody escape in the SARS-CoV-2 Omicron BA.1 and BA.2 RBDs, (Starr et al., 2022, [待核])]([no-url])

对 BA.1 与 BA.2 的 RBD 做三套 DMS。**同一抗原的不同谱系版本，其表位多样性的度量分母不同**。

#### [Deep mutational scanning to predict antibody escape in SARS-CoV-2 Omicron subvariants, ([待核], 2022, [待核])]([no-url])

用 DMS 预测亚变体的抗体逃逸。把逃逸谱用于前瞻预测。

#### [Deep mutational scanning of rabies glycoprotein defines mutational constraint and antibody-escape mutations, ([待核], 2025, [待核])]([no-url])

狂犬病糖蛋白的 DMS，给出突变约束与逃逸突变。跨病原体的方法可迁移性证据。

#### [Deep mutational scanning reveals functional constraints and antibody-escape potential of Lassa virus glycoprotein, ([待核], 2024, [待核])]([no-url])

拉沙病毒糖蛋白的 DMS。同上的另一病原体验证。

#### [Deep mutational scanning comprehensively maps how Zika envelope protein mutations affect viral growth and antibody ..., (([待核], 2019, [待核]))]([no-url])

寨卡包膜蛋白的 DMS。

#### [Epitope mapping via in vitro deep mutational scanning methods and its applications, ([待核], 2025, [待核])]([no-url])

体外 DMS 表位制图的方法与应用的综述。**是把 DMS 当作表位真值的入门参考**。

#### [Deep Mutational Scanning in Immunology: Techniques and Applications, ([待核], 2025, [待核])]([no-url])

免疫学中的 DMS 技术与应用综述。

### 6.3 结构解析与结构驱动的表位识别

#### [Structures of Human Antibodies Bound to SARS-CoV-2 Spike Reveal Common Epitopes and Recurrent Features of Antibodies, (Barnes et al., 2020, Cell, Caltech)](https://doi.org/10.1016/j.cell.2020.06.025)

（见 1.1）cryo-EM 结构定义了一个阻断 ACE2 的表位，并识别出 VH3-53/VH3-66 来源的复发抗体类。

#### [Defining variant-resistant epitopes targeted by SARS-CoV-2 antibodies: A global consortium study, (Hastie et al., 2021, Science, Scripps Research)](https://doi.org/10.1126/science.abh2315)

（见 1.1）结构 + 竞争 + 中和三者结合，定义七个 RBD 抗体社区。

#### [Structural basis for the recognition of SARS-CoV-2 by full-length human ACE2, (Yan et al., 2020, Science, Westlake University)]([no-url])

（见 1.4）ACE2-RBD 界面原子细节。

#### [Structural insights of a highly potent pan-neutralizing SARS-CoV-2 human monoclonal antibody, ([待核], 2022, [待核])]([no-url])

一个泛中和抗体的结构基础。提供了「跨变体保守表位」的实例。

#### [Alternative conformations of a major antigenic site on RSV F, (McLellan et al., 2019, [待核])]([no-url])

RSV F 蛋白上主要抗原位点存在替代构象。**同一序列的表位在构象上可以不同**——这是「结构固定、表位未定」的典型案例。

### 6.4 免疫原性与广度实验

#### [Mosaic nanoparticles elicit cross-reactive immune responses to zoonotic coronaviruses in mice, (Cohen et al., 2021, Science, Caltech)]([no-url])

用展示多种冠状病毒 RBD 的免疫原，测量所引发应答的广度，把有意的抗原多样化与对抗原面板（含免疫原中没有的抗原）的交叉反应连接起来。**这支持用前瞻性广度试验而非仅计数不同抗原序列来评估收集多样性**。

#### [Mosaic vaccines elicit CD8+ T lymphocyte responses that confer enhanced immune coverage of diverse HIV strains, (Ndhlovu?/Barouch?, 2010, [待核])]([no-url])

mosaic 疫苗引发覆盖多样 HIV 株的 T 细胞应答。**「覆盖度」作为设计目标**，与本仓库的多样性指标同构。

#### [Increased Valency of Conserved-mosaic Vaccines Enhances the Breadth and Depth of Epitope Recognition, ([待核], 2016, [待核])]([no-url])

提高价数增强表位识别的广度与深度。**广度与深度是两个不同的量**，不能合并成一个多样性数字。

#### [mRNA delivery of mosaic-8 pan-sarbecovirus RBD vaccines elicits distinct antibody epitope signatures, ([待核], 2026, [待核])]([no-url])

mosaic-8 疫苗引发不同的抗体表位签名。表位签名可作为免疫原多样性的读出。

#### [Immunization with mosaic nanoparticles reveals that antigen avidity shapes the clonal hierarchy of the B cell ..., ([待核], 2026, [待核])]([no-url])

抗原亲合力塑造 B 细胞克隆层级。**多样性不只由免疫原种类决定，还由呈现方式决定**。

### 6.5 抗体谱系绘图与血清学

#### [Comprehensive serological profiling of human populations using a synthetic human virome, (Xu et al., 2015, Science, Harvard University / HHMI)]([no-url])

提出 VirScan，用噬菌体展示的肽库与测序画像人群对多种人类病毒的抗体识别，量化跨肽靶的广度。**但该库呈现的是肽，无法完整捕捉不连续构象表位，因此不能单独验证三维表位多样性**。

#### [Computational epitope map of SARS-CoV-2 spike protein, (Sikora et al., 2021, PLoS Computational Biology, Max Planck Institute of Biophysics)](https://doi.org/10.1371/journal.pcbi.1008790)

对含四个全长、全糖基化 spike 的 410 万原子体系做多微秒分子动力学，通过映射空间可及性、结构刚性、序列保守性与通用抗体结合特征来恢复已知表位并发现候选。**关键发现：广泛且本征柔性的糖基外套遮蔽的表面积大于静态结构所提示的——结构动力学本身是表位多样性的一个维度**。

#### [Linear epitope landscape of the SARS-CoV-2 Spike protein constructed from 1,051 COVID-19 patients, (Li et al., 2021, Cell Reports, [待核])]([no-url])

从 1,051 名患者构建线性表位图谱。**线性表位与构象表位是两套不同的多样性统计**，不可混算。

#### [Linear B-Cell Epitope Prediction for In Silico Vaccine Design: A Performance Review of Methods Available via Command-Line ..., ([待核], 2021, [待核])]([no-url])

线性 B 细胞表位预测方法的性能综述。

#### [Epitope-specific TCRbeta repertoire diversity imparts no functional advantage on the CD8+ T cell response ..., ([待核], 2008, [待核])]([no-url])

TCR 表位特异性 repertoire 多样性对功能**没有**带来优势。这是「多样性高不等于更好」的一条反向证据，值得在讨论多样性目标时并列引用。

#### [Dynamics of the Magnitude, Breadth and Depth of the Antibody Response at Epitope Level Following Dengue Infection, ([待核], 2021, [待核])]([no-url])

登革热感染后抗体应答在表位层面的量级、广度与深度动态。**广度与深度分开测量**。

#### [Quantifying influenza vaccine efficacy and antigenic distance, (Gupta et al., 2006, Vaccine, [待核])]([no-url])

（见 1.2）

#### [Antigenic cartography of well-characterized human sera shows SARS-CoV-2 neutralization differences based on ..., ([待核], 2022, [待核])]([no-url])

用充分表征的人血清做抗原制图。显示血清面板的选择会改变推断出的抗原空间。

#### [A computational framework for influenza antigenic cartography, ([待核], 2010, [待核])]([no-url])

抗原制图的计算框架。方法学参考。

---

## 7. 计算表位 / paratope 预测

**定位：这一类不是多样性理论，而是「无结构数据时的退路」**。`data/raw/public/` 中相当比例只有序列，这一节决定了它们能否进入表位维度。

### 7.1 B 细胞表位预测

#### [BepiPred-2.0: improving sequence-based B-cell epitope prediction using conformational epitopes, (Jespersen et al., 2017, Nucleic Acids Research, Technical University of Denmark)]([no-url])

用构象表位训练数据改进基于序列的 B 细胞表位预测。是序列-only 路线的基线。

#### [BepiPred-3.0: Improved B-cell epitope prediction using protein language models, (Clifford et al., 2022, Protein Science, Technical University of Denmark)]([no-url])

用蛋白语言模型改进 B 细胞表位预测。**pLM 表示已能在序列层面捕捉部分表位信息**，这对无结构数据的可用性影响最大。

#### [DiscoTope-3.0: improved B-cell epitope prediction using inverse folding latent representations, (Høie et al., 2024, Frontiers in Immunology, Technical University of Denmark)](https://doi.org/10.3389/fimmu.2024.1322712)

用逆折叠潜表示改进表位预测。逆折叠表示对「什么序列能放在这个表面位置」编码充分，天然适合表位。

#### [PEPITO: improved discontinuous B-cell epitope prediction using multiple distance thresholds and half sphere exposure, (Sweredoski & Baldi, 2008, Bioinformatics, UC Irvine)]([no-url])

用多距离阈值与半球暴露改进不连续表位预测。早期结构基方法的代表。

#### [CEP: a conformational epitope prediction server, (Kringelum et al., 2006, [待核])]([no-url])

构象表位预测服务器。

#### [SEMA: Antigen B-cell conformational epitope prediction using deep transfer learning, (Collatz et al., 2022, [待核])]([no-url])

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

#### [An explainable language model for antibody specificity prediction using curated influenza hemagglutinin antibody data, (Xu et al., 2024, [待核])]([no-url])

可解释语言模型预测抗体特异性。

#### [Supervised fine-tuning of pre-trained antibody language models improves antigen specificity prediction, (Yu et al., 2025, [待核])]([no-url])

监督微调提升抗原特异性预测。**特异性是可观测的表位代理**，可作为多样性方法的验证目标。

#### [Contrastive learning for antibody-antigen sequence-to-specificity prediction, ([待核], 2026, [待核])]([no-url])

对比学习做序列到特异性的预测。

#### [Unconstrained generation of synthetic antibody-antigen structures..., (Robert et al., 2022, Nature Computational Science, University of Oslo)](https://doi.org/10.1038/s43588-022-00372-4)

（见 4.4）

#### [Structure-free antibody paratope similarity prediction for in silico epitope binning via protein language models, (Ghanbarpour et al., 2023, iScience, [待核])](https://doi.org/10.1016/j.isci.2023.106036)

（见 1.3）

### 7.4 表位预测的评估争议

#### [Towards a consensus on datasets and evaluation metrics for developing B-cell epitope prediction tools, (Greenbaum et al., 2007, Journal of Molecular Recognition, [待核])]([no-url])

指出 B 细胞表位预测在数据集与评价指标上缺乏共识。**指标定义不统一时，「哪个方法预测得更准」这个问题本身没有意义**。

#### [Understanding the Significance and Implications of Antibody Numbering and Antigen-Binding Surface/Residue Definition, (Dondelinger et al., 2018, Frontiers in Immunology, University of Liège)](https://doi.org/10.3389/fimmu.2018.02278)

系统比较不同编号体系与 CDR 定义。**不同数据库使用不同编号约定与 CDR 定义，因此「CDR 多样性」的数值依赖于所采用的体系**。这是 CDR 聚类前必须先固定的口径。

#### [ANARCI: antigen receptor numbering and receptor classification, (Dunbar & Deane, 2016, Bioinformatics, University of Oxford)](https://doi.org/10.1093/bioinformatics/btv552)

抗体编号与受体分类工具。工程上是把各数据集统一到同一 CDR 口径的必要环节。

#### [IMGT unique numbering for immunoglobulin and T cell receptor variable domains and Ig superfamily V-like domains, (Lefranc et al., 2003, Developmental & Comparative Immunology, University of Montpellier)]([no-url])

IMGT 唯一编号。是事实上的接口标准。

#### [50 years of antibody numbering schemes: a statistical and structural evaluation reveals key differences and limitations, (Dondelinger et al., 2024, [待核])]([no-url])

对五十年的抗体编号方案做统计与结构评估，**揭示关键差异与局限**。直接文献化「编号口径会影响结论」这件事。

#### [AbRSA: A robust tool for antibody numbering, (Yu et al., 2019, [待核])]([no-url])

鲁棒的抗体编号工具。

#### [EpiScan: accurate high-throughput mapping of antibody-specific epitopes using sequence information, (Wang et al., 2024, npj Systems Biology and Applications, [待核])](https://doi.org/10.1038/s41540-024-00432-7)

纯用抗体序列信息（VH、VL、CDR、FR 分别建块再加权）预测特定抗体在抗原上的表位。**「抗体特异性表位」而非「抗原通用表位」的定位方式，与本仓库的配对数据观点一致**。

#### [Improved Antibody-Specific Epitope Prediction Using AlphaFold and AbAdapt, ([待核], 2022, [待核])]([no-url])

用 AF 与 AbAdapt 改进抗体特异性表位预测。

#### [AFilter: Improved Antibody Epitope Prediction by Machine Learning-Optimized Interface Energy Filtering of AlphaFold ..., ([待核], 2026, [待核])]([no-url])

用机器学习优化的界面能量过滤改进 AF 派生表位预测。承认了 AF 预测的界面需要额外过滤——呼应 AF3 幻觉表位的问题。

---

## 8. 采样与覆盖度理论

**这是原稿缺失的一层。** 「90–100 个抗原/年够不够」本质是**未见物种估计**问题：在已采集的抗原/表位里，还有多少类别未被采到。生态学为此发展了一整套非参数方法，且都只依赖「稀有类别的计数」（singleton/doubleton），与抗体数据的结构高度契合。

### 8.1 有效类别数与稀疏化

#### [A guide to the application of Hill numbers to DNA-based diversity analyses, (Alberdi & Gilbert, 2019, Molecular Ecology Resources, University of Copenhagen)]([no-url])

系统说明 Hill numbers（有效类别数）如何用于多样性分析。**Hill number 的核心优势是尺度参数 q 可调**：q=0 是纯丰富度（不理会频次），q=1 是 Shannon 有效数，q=2 偏重常见类。同一数据集在不同 q 下给出的多样性排序可以不同——这意味着**报告单一数字是不完整的**。

#### [Distance-based functional diversity measures and their decomposition: a framework based on Hill numbers, (Chiu & Chao, 2014, PLoS ONE, National Tsing Hua University)](https://doi.org/10.1371/journal.pone.0100014)

把 Hill numbers 扩展到考虑类别之间的两两功能距离，导出功能 Hill numbers（「等丰度且功能等距的类别数」）、平均功能多样性与总功能多样性。**这几乎是为表位多样性量身定做的框架**：类别 = 表位簇，距离 = 界面距离，且能分解成「有多少类」×「类之间差多远」两个因子。

#### [Measuring metagenome diversity and similarity with Hill numbers, (Kang et al., 2018, [待核])]([no-url])

用 Hill numbers 度量宏基因组的多样性与相似性。

#### [Diversity indices for ecological networks: a unifying framework using Hill numbers, (Ohlmann et al., 2019, Ecology Letters, [待核])]([no-url])

把 Hill numbers 统一到网络多样性。**抗原-抗体对本身就是二部图**，这个框架可直接套用。

#### [Interpolating, extrapolating, and comparing incidence-based species accumulation curves, (Colwell et al., 2004, Ecology, University of Connecticut)](https://doi.org/10.1890/03-0557)

针对基于出现/缺失（incidence）的物种累积函数提出一般二项混合模型，覆盖观测样本数以内的内插与超出观测集的外推，并给出闭式期望丰富度及其置信区间。**这正是「收集到 N 个抗原之后还会发现多少新表位」这一问题的标准答案形式**，而且它区分内插与外推——前者不完全依赖模型假设。

### 8.2 未见类别估计

#### [An improved nonparametric lower bound of species richness via a modified good-turing frequency formula, (Chiu et al., 2014, Biometrics, National Tsing Hua University)](https://doi.org/10.1111/biom.12200)

指出在超高多样群落里，准确的丰富度下界比不准确的点估计更有用。传统 Chao1 下界只用最稀有类别的信息（singleton 与 doubleton 数）；本文用修改的 Good-Turing 公式估计其一阶偏差，并借助 tripleton/quadrupleton 的信息校正，得到一个改进的非参数下界，对任何丰度分布都成立。**对应到抗原数据：只数「只出现一次的表位簇」和「只出现两次的」，就能给出「至少还有多少个表位类别未被采到」的下界**。

#### [Sufficient sampling for asymptotic minimum species richness estimators, (Chao et al., 2009, Ecology, National Tsing Hua University / University of Connecticut)](https://doi.org/10.1890/07-2147.1)

给出第一个统计严格的非参数方法，估计为检测到渐近丰富度的任意比例（含 100%）所需的最小额外个体、样本或采样面积。**这是唯一能直接回答「还要再收集多少个抗原才够」的文献**；它需要的是稀有类别的频次，而这些频次恰好可以从已有的表位分箱/聚类结果中得到。

#### [Abundance-based similarity indices and their estimation when there are unseen species in samples, (Chao et al., 2006, Biometrics, University of Connecticut / Academia Sinica)](https://doi.org/10.1111/j.1541-0420.2005.00489.x)

为任意对称、齐次的基于出现与否的相似性指数给出概率推导，并扩展出丰度型指数；应用 Laplace 近似提出**校正「未观测到的共有类别」效应的估计量**。模拟显示当相当比例的类别缺失时，校正估计量显著降低未校正估计的偏差。**对应到本仓库：比较两个数据源的表位重叠时，两边都未采到的表位会让重叠率被系统性低估；这个估计量正是修法**。

#### [Unveiling the species-rank abundance distribution by generalizing the Good-Turing sample coverage theory, (Chao et al., 2015, Ecology, National Tsing Hua University)](https://doi.org/10.1890/14-0550.1)

指出对样本中已检测到的类别，其样本相对丰度是真实相对丰度的**正偏**估计，且偏差随该类别越稀有而增大；提出分别调整已检测类别的相对丰度、并为「未检测到但推断存在」的类别估计相对丰度。**这解释了为什么直接用样本频次画表位分布会高估常见表位、低估稀有表位**。

#### [Optimal prediction of the number of unseen species, (Orlitsky et al., 2016, PNAS, UC San Diego)](https://doi.org/10.1073/pnas.1607774113)

研究 Fisher 等人提出的问题：用 n 个样本预测再取 t·n 个新样本时会出现多少个此前未见过的类别，并给出可证明对所有 t 都有效的估计量类，且证明该范围是最优的、其均方误差接近最优。**这是「外推多样性—收集量曲线」的严格数学基础**。

---

## 附：三轴交叉（结构说明，不占篇数）

上述八类作为阅读清单可用，但**混合了四种不同性质的东西**：生物对象、计算工具、实验测量、评估目标。若要用于决策，更清晰的框架是三个轴交叉：

| 轴 | 取值 |
| --- | --- |
| **对象** | 抗体（序列 / 结构 / paratope）· 抗原表面 patch · 完整界面（双侧排布）· 配对记录 |
| **测量** | 序列一致性 · 几何相似 · 竞争阻断 · 逃逸谱 · 交叉反应广度 · 结构解析 |
| **用途** | 覆盖度估计 · 收集设计 · 泛化检验 |

几个交叉点已有成熟文献（例如「界面 × 几何 × 覆盖度」= 3.1/3.2；「配对记录 × 逃逸谱 × 泛化检验」= 6.2 + 4.2），而**「抗原表面 patch × 几何 × 收集设计」几乎是空的**——这恰好是本仓库要填的位置。

### 三条必须带走的限定

1. **更硬的聚类划分本身不能证明泄漏。** 它可能只是引入了合法的分布偏移。要主张泄漏，须：控制训练集大小（用等规模子集对照）、审计跨划分的实际相似度、并在多个阈值上重复。这一点在 Park 2012、Bernett 2024、ATOM3D 三处被分别以不同方式强调。

2. **「结构不同」与「功能不同」不是同一件事，且方向不稳定。** Hastie 2021 与 Cao 2022 都报告结构分类与功能分类高度一致，但 Robinson 2021 发现序列方法会低估收敛（序列多样性 → 高估表位多样性），而 Greaney 2021 发现结构足迹相似的两个抗体可以有不同逃逸谱（结构相似 → 低估功能差异）。**两个方向的偏差都存在，取决于测量的是哪一层。**

3. **没有任何文献确立 90–100 抗原/年足够。** 判断依据只能是：增量表位覆盖（§8.2 的 Chao/Good-Turing 估计量）、新功能组的发现率（§8.1 的累积曲线外推）、以及固定未见抗原测试集上的学习曲线（§4.2 的 SABLE 式划分，§5.1 的多规模对照）。
