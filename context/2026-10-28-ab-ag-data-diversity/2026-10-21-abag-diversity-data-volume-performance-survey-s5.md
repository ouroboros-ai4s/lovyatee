---
tags:
  - context
---

# Diversity x Data Volume x Performance — ABAG Survey Section 5

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

#### HuCAL PLATINUM, a synthetic Fab library optimized for sequence diversity and superior performance in mammalian ... , (Prassler et al., 2011, [待核], MorphoSys)

一个以序列多样性为优化目标的合成 Fab 库。**工业界做法：多样性被当作库设计的显式目标函数**。

#### Construction of a large synthetic human scFv library with six diversified CDRs and high functional diversity, ([待核], 2009, [待核])

六个 CDR 全多样化的大规模合成 scFv 库。说明「功能多样性」与「序列多样性」被分别追求。

#### Next-generation sequencing enables the discovery of more diverse positive clones from a phage-displayed antibody ..., ([待核], 2017, [待核])

NGS 使能从噬菌体展示筛选中发现更多样的阳性克隆。**筛选深度本身决定了观测到的多样性**。

#### Diverse high-affinity DNA aptamers for wild-type and B.1.1.7 SARS-CoV-2 spike proteins from a pre-structured ..., ([待核], 2021, [待核])

预结构化文库产生多样高亲和力适配体。非抗体体系，但多样性来源可类比。

### 5.3 主动学习与信息量驱动采样

#### Active Learning for Convolutional Neural Networks: A Core-Set Approach, (Sener & Savarese, 2018, ICLR, California Institute of Technology)

把批量主动学习表述为选择能覆盖已学习表示空间的样本，用 core-set 形式化（与几何覆盖相关）。给出一个基于「距已表示样本的距离」的多样性操作定义。**用在抗原收集上，其效用取决于该表示是否捕捉到相关的表位变异，而非偶然的序列或结构差异**。

#### Submodularity in Data Subset Selection and Active Learning, (Wei et al., 2015, ICML, University of Washington)

研究奖励覆盖且具有收益递减性质的子集选择目标。这类目标可把「选择一个代表相似空间中未覆盖区域的抗原」形式化为可优化的价值。**为 90–100 个抗原/年的预算提供原则性分配策略，但在没有覆盖度与性能测量时不能确立该预算足够**。

#### Active learning-assisted directed evolution, (Qiu et al., 2025, [待核])

用主动学习辅助定向演化。是把「下一轮测什么」形式化的直接范例。

#### ALLM-Ab: Active Learning-Driven Antibody Optimization Using Fine-Tuned Protein Language Models, ([待核], 2025, [待核])

用微调蛋白语言模型的主动学习优化抗体。**主动学习正是「多样性 × 预算」问题的操作化**。

#### Using an FPLC to promote active learning... , ([待核], 2017, [待核])

（教学类，检索误命中，此处仅作噪声示例记录）

#### Choosing where to look next in a mutation sequence space: Active Learning of informative p53 cancer rescue mutations, (Danciu et al., 2007, [待核])

在前面的变异序列空间里主动学习。早期把「信息量」当作采样准则的工作。

### 5.4 冷启动与未见抗原评估

#### Mitigating cold-start problems in drug-target affinity prediction with interaction knowledge transferring, ([待核], 2022, [待核])

用相互作用知识迁移缓解药物-靶点亲和力预测的冷启动问题。**冷启动 = 未见实体**，与 ab-ag 的未见抗原同构。

#### CS-DTA: a language model-driven framework for robust drug-target affinity prediction under strict cold-start ..., ([待核], 2026, [待核])

在严格冷启动设定下的 DTA 预测。提供了「严格」如何定义的可参考模板。

#### LLMDTA: Improving Cold-Start Prediction in Drug-Target Affinity With Biological LLM, ([待核], 2025, [待核])

用生物 LLM 改善冷启动 DTA。

#### [Unconstrained generation of synthetic antibody-antigen structures..., (Robert et al., 2022, Nature Computational Science, University of Oslo)](https://doi.org/10.1038/s43588-022-00372-4)

（见 4.4）把特异性预测形式化为 ML 任务，并给出可复现的划分。

---
