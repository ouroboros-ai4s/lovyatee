---
- tags:
  - context
---

# Four Tiers of Epitope Identity — ABAG Survey Section 1

## 1. ABAG 表位多样性：什么算「不同的表位」

这一类的核心问题不是「怎么算距离」，而是**距离算在什么对象上**：接触残基集合、结合几何、竞争关系、还是逃逸谱。四者在文献里被分别使用，且不等价。

### 1.1 表位分类体系与社区划分

#### Structural analysis of B-cell epitopes in antibody:protein complexes, (Kringelum et al., 2013, Molecular Immunology, University of Copenhagen)

系统分析实验解析的抗体-蛋白复合物，刻画表位的几何与理化性质。表位由三维接触定义，因此序列上相距很远的残基可以属于同一个结合面。这支持在空间残基邻域上而非抗原序列窗口上度量多样性。

#### Computational characterization of B-cell epitopes, (Rubinstein et al., 2008, Molecular Immunology, Weizmann Institute of Science)

比较表位与抗原其他表面区域的结构与理化性质。其基于接触的定义为比较表位组成、可及性与几何提供了基础。这类描述子刻画了表位差异，但**不能确立两个表位在功能上不同**。

#### The Immune Epitope Database (IEDB): 2018 update, (Vita et al., 2019, Nucleic Acids Research, La Jolla Institute for Immunology)

描述一个将表位连接到来源抗原、物种、宿主与实验测定的策展资源，包含不连续表位。这些注释提供了若干互补的分类轴，而非统一的表位距离度量。做多样性统计时须区分「唯一表位记录」与「独立抗原家族、表面区域、测定情境」。

#### [Structures of Human Antibodies Bound to SARS-CoV-2 Spike Reveal Common Epitopes and Recurrent Features of Antibodies, (Barnes et al., 2020, Cell, California Institute of Technology)](https://doi.org/10.1016/j.cell.2020.06.025)

提出一个影响广泛的 SARS-CoV-2 RBD 抗体分类，依据结合位置、ACE2 竞争关系、以及在不同 spike 构象下的可及性。识别重叠区域的抗体可以在接近角度与构象可及性上不同。因此表位多样性包含**结合几何与抗原状态**，不只是接触残基身份。

#### [Defining variant-resistant epitopes targeted by SARS-CoV-2 antibodies: A global consortium study, (Hastie et al., 2021, Science, Scripps Research)](https://doi.org/10.1126/science.abh2315)

整合竞争测定、结构信息与功能表征，把抗体组织成若干表位社区（七个 RBD 定向抗体社区）。社区捕捉相关的识别模式，而变体敏感性在社区内与社区间提供功能区分。这是同时在配对数据集上报告结构覆盖与抗性谱覆盖的可用模型。

#### [Omicron escapes the majority of existing SARS-CoV-2 neutralizing antibodies, (Cao et al., 2022, Nature, Peking University)](https://doi.org/10.1038/s41586-021-04385-3)

用高通量酵母展示测定 247 个抗 RBD 中和抗体的逃逸突变谱，并对中和抗体做无监督聚类，得到六个表位组（A–F），作者报告该分组与知识驱动的结构分类高度一致。这是**「功能分组 = 结构分组」这一等价命题最直接的经验证据**，也是本仓库最该先锚定的事实之一。注意分组依据是逃逸谱而非接触残基。

#### Mapping the antigenic and genetic evolution of influenza virus, (Smith et al., 2004, Science, University of Cambridge)

引入抗原制图，用血清学测定把病毒与血清定位到低维抗原空间。距离总结的是识别上的功能差异，揭示了仅凭遗传距离看不到的关系。这是度量抗原多样性的基础方法，但推断出的几何依赖于血清面板与测定。

#### A neutralizing antibody selected from plasma cells that binds to group 1 and group 2 influenza A hemagglutinins, (Corti et al., 2011, Science, Humabs BioMed / Institute for Research in Biomedicine)

表征一个识别流感 A 两个主要组别共有的血凝素茎部表位的抗体。说明**抗原序列多样性可以与保守的抗体识别并存**。交叉反应广度必须在抗原面板上直接测量，并与序列多样性分开报告。

### 1.2 表位距离与抗原图谱

#### Quantifying influenza vaccine efficacy and antigenic distance, (Gupta et al., 2006, Vaccine, [待核])

把抗原距离与疫苗有效性联系起来，是「抗原距离」作为可计算量的早期系统化工作。距离定义在血凝素序列差异上，仅部分反映功能差异。对本仓库的意义：**这正是会上「抗原多样性是否可用序列刻画」的否命题方**。

#### [Influenza hemagglutinin antigenic distance measures capture trends in HAI differences and infection outcomes, but are not suitable predictive tools, (Skarlupka et al., 2020, Vaccine, University of Georgia)](https://doi.org/10.1016/j.vaccine.2020.06.042)

评估多种基于氨基酸替换的抗原距离度量作为 HAI 滴度差与临床结局的预测工具。距离度量确实描述了趋势，但结果变量的变异导致预测区间极宽。**结论是这类序列抗原距离不能当作预测工具**——对「用序列近似表位多样性」是一个明确的负面证据。

#### Antigenic cartography of SARS-CoV-2 reveals that Omicron BA.1 and BA.2 are antigenically distinct, (van der Straten et al., 2022, [待核])

把抗原制图方法用在 SARS-CoV-2 变体上，显示 BA.1 与 BA.2 在抗原空间上可分。说明即使在同谱系内部，功能层面的多样性也未必由遗传距离反映。

#### CE-BLAST makes it possible to compute antigenic similarity for newly emerging pathogens, (Qiu et al., 2018, Nature Communications, [待核])

提出对新兴病原体可在无血清面板时计算抗原相似性的方法。这类方法的价值在于**覆盖度盲区**：没有实验血清时，抗原多样性只能靠计算代理。

#### The geometry of shape space: application to influenza, (Smith et al., 2001, Journal of Theoretical Biology, [待核])

把免疫学的 shape space 形式化为可计算的几何结构，并用流感数据检验。提供了把「抗原-抗体距离」当作度量空间的公理化基础。注意：shape space 的维度与度量并不由数据唯一确定。

#### Rethinking "shape space": evidence from simulated docking suggests that steric shape complementarity is not limited to dissimilar shapes, (Perelson & Oster?, 1994, [待核])

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

#### Structural diversity in a human antibody germline library, (Kovaltsuk et al., 2016, mAbs, University of Oxford)

分析人类抗体 germline 库的结构多样性，说明 germline 层面的结构覆盖是有限的。这为「抗体侧多样性的天花板」提供了一个可引用的经验数字。

#### The repertoire of human germline VH sequences reveals about fifty groups of VH segments with different hypervariable loops, (Chothia et al., 1992, Journal of Molecular Biology, MRC Laboratory of Molecular Biology)

把人类 germline VH 序列归纳为约五十组，各组超变环不同。这是「抗体多样性可从有限 germline 结构类出发」这一论点的原始来源。

#### Most marginal zone B cells in rat express germline encoded Ig VH genes and are ligand selected, (Dammers et al., [待核])

显示部分 B 细胞群的 VH 几乎完全 germline 编码。对多样性统计的提醒：**序列多样性低不等于功能多样性低**，选择压力可以维持窄序列谱。

#### Structural basis for the recognition of SARS-CoV-2 by full-length human ACE2, (Yan et al., 2020, Science, Westlake University)

给出 ACE2-RBD 界面的原子细节，是判断「某个 RBD 表位是否与受体位点重叠」的参照。表位多样性若按「是否阻断受体结合」二分，这个结构就是判定基准。

#### A highly conserved cryptic epitope in the receptor binding domains of SARS-CoV-2 and SARS-CoV, (Yuan et al., 2020, Science, [待核])

描述一个在 SARS-CoV 与 SARS-CoV-2 RBD 间保守的隐蔽表位。说明**表面可及性**（跨变体保守但平时被遮蔽）是表位多样性的一个独立维度，仅看结构差异会漏掉。

#### Cross-Neutralization of a SARS-CoV-2 Antibody to a Functionally Conserved Site Is Mediated by Avidity, (Liu et al., 2020, [待核])

一个对功能保守位点的交叉中和是由亲合力（avidity）而非表位相似性介导的。对多样性统计的警告：**交叉反应广度不等于表位同一性**，亲合力可以制造假的「同一表位」信号。

#### Broad cross-reactivity across sarbecoviruses exhibited by a subset of COVID-19 donor-derived neutralizing antibodies, (Robbiani et al., 2021, [待核])

部分 COVID-19 供体来源的中和抗体对沙贝病毒呈广谱交叉反应。这类抗体的存在说明「一个抗原上的表位数量」本身依赖于所考察的抗体谱系范围。

#### Neutralization potency of monoclonal antibodies recognizing dominant and subdominant epitopes on SARS-CoV-2 Spike, ([待核], 2021, [待核])

区分显性（dominant）与次显性（subdominant）表位上的抗体及其中和效力。**免疫显性层级**意味着按抗体数量加权的表位分布与按功能重要性加权的分布不同，多样性指标须声明用哪一种权重。

#### A SARS-CoV-2 variant elicits an antibody response with a shifted immunodominance hierarchy, (Greaney et al., 2022, [待核])

变体可以改变免疫显性层级。因此「某抗原的表位多样性」不是抗原的固有属性，而是抗原 × 免疫背景的联合属性。

#### A computational method for immune repertoire mining that identifies novel binders from different clonotypes, ([待核], 2021, [待核])

用计算方法在 repertoire 中挖掘来自不同克隆型的新 binder。支持「克隆型多样性 ≠ binder 多样性」这一区分。

#### Public Baseline and shared response structures support the theory of antibody repertoire functional commonality, ([待核], 2021, [待核])

提出「公共基线」概念，说明不同个体的 repertoire 在功能层面共享结构。对多样性统计的意涵：跨个体的重复不是数据冗余，而是功能收敛的证据。

#### Convergent evolution and B-cell recirculation in germinal centers in a human lymph node, ([待核], 2023, [待核])

在人生发中心观察到收敛演化。收敛意味着**序列距离会系统性高估功能多样性**。
