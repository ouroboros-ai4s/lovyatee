---
- tags:
  - context
---

# Sampling and Coverage Theory — ABAG Survey Section 8

## 8. 采样与覆盖度理论

**这是原稿缺失的一层。** 「90–100 个抗原/年够不够」本质是**未见物种估计**问题：在已采集的抗原/表位里，还有多少类别未被采到。生态学为此发展了一整套非参数方法，且都只依赖「稀有类别的计数」（singleton/doubleton），与抗体数据的结构高度契合。

### 8.1 有效类别数与稀疏化

#### A guide to the application of Hill numbers to DNA-based diversity analyses, (Alberdi & Gilbert, 2019, Molecular Ecology Resources, University of Copenhagen)

系统说明 Hill numbers（有效类别数）如何用于多样性分析。**Hill number 的核心优势是尺度参数 q 可调**：q=0 是纯丰富度（不理会频次），q=1 是 Shannon 有效数，q=2 偏重常见类。同一数据集在不同 q 下给出的多样性排序可以不同——这意味着**报告单一数字是不完整的**。

#### [Distance-based functional diversity measures and their decomposition: a framework based on Hill numbers, (Chiu & Chao, 2014, PLoS ONE, National Tsing Hua University)](https://doi.org/10.1371/journal.pone.0100014)

把 Hill numbers 扩展到考虑类别之间的两两功能距离，导出功能 Hill numbers（「等丰度且功能等距的类别数」）、平均功能多样性与总功能多样性。**这几乎是为表位多样性量身定做的框架**：类别 = 表位簇，距离 = 界面距离，且能分解成「有多少类」×「类之间差多远」两个因子。

#### Measuring metagenome diversity and similarity with Hill numbers, (Kang et al., 2018, [待核])

用 Hill numbers 度量宏基因组的多样性与相似性。

#### Diversity indices for ecological networks: a unifying framework using Hill numbers, (Ohlmann et al., 2019, Ecology Letters, [待核])

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
