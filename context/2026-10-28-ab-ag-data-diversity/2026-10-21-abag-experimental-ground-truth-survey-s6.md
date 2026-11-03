---
- tags:
  - context
---

# Experimental Ground Truth: How Epitope Diversity Is Measured — ABAG Survey Section 6

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

#### Deep Mutational Scanning of SARS-CoV-2 Receptor Binding Domain Reveals Constraints on Folding and ACE2 Binding, (Starr et al., 2020, Cell, Fred Hutchinson Cancer Center)

用酵母展示的突变文库量化 RBD 替换对表达与 ACE2 结合的影响。把「与抗原功能相容的突变」与「破坏折叠或受体互作的突变」区分开。**为把抗体逃逸图谱解读为识别证据提供必要的对照**。

#### Complete Mapping of Mutations to the SARS-CoV-2 Spike Receptor-Binding Domain that Escape Antibody Recognition, (Greaney et al., 2021, Cell Host & Microbe, Fred Hutchinson Cancer Center)

用 DMS 制图 RBD 突变对单个抗体识别的影响，每个抗体获得一个功能逃逸谱，可跨位点与替换比较。**结构足迹相似的两个抗体可以有不同逃逸谱**，因此突变敏感性是表位多样性的又一个独立轴。

#### Comprehensive mapping of mutations in the SARS-CoV-2 receptor-binding domain that affect recognition by polyclonal human plasma antibodies, (Greaney et al., 2021, Cell Host & Microbe, Fred Hutchinson Cancer Center)

把逃逸制图推广到多克隆人血浆。结果是**不同个体在主导识别的抗原位点上存在变异**。血浆逃逸谱不唯一重构其组成抗体的特异性。

#### Deep mutational scans for ACE2 binding, RBD expression, and antibody escape in the SARS-CoV-2 Omicron BA.1 and BA.2 RBDs, (Starr et al., 2022, [待核])

对 BA.1 与 BA.2 的 RBD 做三套 DMS。**同一抗原的不同谱系版本，其表位多样性的度量分母不同**。

#### Deep mutational scanning to predict antibody escape in SARS-CoV-2 Omicron subvariants, ([待核], 2022, [待核])

用 DMS 预测亚变体的抗体逃逸。把逃逸谱用于前瞻预测。

#### Deep mutational scanning of rabies glycoprotein defines mutational constraint and antibody-escape mutations, ([待核], 2025, [待核])

狂犬病糖蛋白的 DMS，给出突变约束与逃逸突变。跨病原体的方法可迁移性证据。

#### Deep mutational scanning reveals functional constraints and antibody-escape potential of Lassa virus glycoprotein, ([待核], 2024, [待核])

拉沙病毒糖蛋白的 DMS。同上的另一病原体验证。

#### Deep mutational scanning comprehensively maps how Zika envelope protein mutations affect viral growth and antibody ..., (([待核], 2019, [待核]))

寨卡包膜蛋白的 DMS。

#### Epitope mapping via in vitro deep mutational scanning methods and its applications, ([待核], 2025, [待核])

体外 DMS 表位制图的方法与应用的综述。**是把 DMS 当作表位真值的入门参考**。

#### Deep Mutational Scanning in Immunology: Techniques and Applications, ([待核], 2025, [待核])

免疫学中的 DMS 技术与应用综述。

### 6.3 结构解析与结构驱动的表位识别

#### [Structures of Human Antibodies Bound to SARS-CoV-2 Spike Reveal Common Epitopes and Recurrent Features of Antibodies, (Barnes et al., 2020, Cell, Caltech)](https://doi.org/10.1016/j.cell.2020.06.025)

（见 1.1）cryo-EM 结构定义了一个阻断 ACE2 的表位，并识别出 VH3-53/VH3-66 来源的复发抗体类。

#### [Defining variant-resistant epitopes targeted by SARS-CoV-2 antibodies: A global consortium study, (Hastie et al., 2021, Science, Scripps Research)](https://doi.org/10.1126/science.abh2315)

（见 1.1）结构 + 竞争 + 中和三者结合，定义七个 RBD 抗体社区。

#### Structural basis for the recognition of SARS-CoV-2 by full-length human ACE2, (Yan et al., 2020, Science, Westlake University)

（见 1.4）ACE2-RBD 界面原子细节。

#### Structural insights of a highly potent pan-neutralizing SARS-CoV-2 human monoclonal antibody, ([待核], 2022, [待核])

一个泛中和抗体的结构基础。提供了「跨变体保守表位」的实例。

#### Alternative conformations of a major antigenic site on RSV F, (McLellan et al., 2019, [待核])

RSV F 蛋白上主要抗原位点存在替代构象。**同一序列的表位在构象上可以不同**——这是「结构固定、表位未定」的典型案例。

### 6.4 免疫原性与广度实验

#### Mosaic nanoparticles elicit cross-reactive immune responses to zoonotic coronaviruses in mice, (Cohen et al., 2021, Science, Caltech)

用展示多种冠状病毒 RBD 的免疫原，测量所引发应答的广度，把有意的抗原多样化与对抗原面板（含免疫原中没有的抗原）的交叉反应连接起来。**这支持用前瞻性广度试验而非仅计数不同抗原序列来评估收集多样性**。

#### Mosaic vaccines elicit CD8+ T lymphocyte responses that confer enhanced immune coverage of diverse HIV strains, (Ndhlovu?/Barouch?, 2010, [待核])

mosaic 疫苗引发覆盖多样 HIV 株的 T 细胞应答。**「覆盖度」作为设计目标**，与本仓库的多样性指标同构。

#### Increased Valency of Conserved-mosaic Vaccines Enhances the Breadth and Depth of Epitope Recognition, ([待核], 2016, [待核])

提高价数增强表位识别的广度与深度。**广度与深度是两个不同的量**，不能合并成一个多样性数字。

#### mRNA delivery of mosaic-8 pan-sarbecovirus RBD vaccines elicits distinct antibody epitope signatures, ([待核], 2026, [待核])

mosaic-8 疫苗引发不同的抗体表位签名。表位签名可作为免疫原多样性的读出。

#### Immunization with mosaic nanoparticles reveals that antigen avidity shapes the clonal hierarchy of the B cell ..., ([待核], 2026, [待核])

抗原亲合力塑造 B 细胞克隆层级。**多样性不只由免疫原种类决定，还由呈现方式决定**。

### 6.5 抗体谱系绘图与血清学

#### Comprehensive serological profiling of human populations using a synthetic human virome, (Xu et al., 2015, Science, Harvard University / HHMI)

提出 VirScan，用噬菌体展示的肽库与测序画像人群对多种人类病毒的抗体识别，量化跨肽靶的广度。**但该库呈现的是肽，无法完整捕捉不连续构象表位，因此不能单独验证三维表位多样性**。

#### [Computational epitope map of SARS-CoV-2 spike protein, (Sikora et al., 2021, PLoS Computational Biology, Max Planck Institute of Biophysics)](https://doi.org/10.1371/journal.pcbi.1008790)

对含四个全长、全糖基化 spike 的 410 万原子体系做多微秒分子动力学，通过映射空间可及性、结构刚性、序列保守性与通用抗体结合特征来恢复已知表位并发现候选。**关键发现：广泛且本征柔性的糖基外套遮蔽的表面积大于静态结构所提示的——结构动力学本身是表位多样性的一个维度**。

#### Linear epitope landscape of the SARS-CoV-2 Spike protein constructed from 1,051 COVID-19 patients, (Li et al., 2021, Cell Reports, [待核])

从 1,051 名患者构建线性表位图谱。**线性表位与构象表位是两套不同的多样性统计**，不可混算。

#### Linear B-Cell Epitope Prediction for In Silico Vaccine Design: A Performance Review of Methods Available via Command-Line ..., ([待核], 2021, [待核])

线性 B 细胞表位预测方法的性能综述。

#### Epitope-specific TCRbeta repertoire diversity imparts no functional advantage on the CD8+ T cell response ..., ([待核], 2008, [待核])

TCR 表位特异性 repertoire 多样性对功能**没有**带来优势。这是「多样性高不等于更好」的一条反向证据，值得在讨论多样性目标时并列引用。

#### Dynamics of the Magnitude, Breadth and Depth of the Antibody Response at Epitope Level Following Dengue Infection, ([待核], 2021, [待核])

登革热感染后抗体应答在表位层面的量级、广度与深度动态。**广度与深度分开测量**。

#### Quantifying influenza vaccine efficacy and antigenic distance, (Gupta et al., 2006, Vaccine, [待核])

（见 1.2）

#### Antigenic cartography of well-characterized human sera shows SARS-CoV-2 neutralization differences based on ..., ([待核], 2022, [待核])

用充分表征的人血清做抗原制图。显示血清面板的选择会改变推断出的抗原空间。

#### A computational framework for influenza antigenic cartography, ([待核], 2010, [待核])

抗原制图的计算框架。方法学参考。

---
