---
tags:
  - context
---

# SRC_R46_SHANKER 数据说明

## 数据集身份

- `source_id`：`SRC_R46_SHANKER`
- `source_version`：`zenodo-11260318`
- 原作者或发布机构：Varun R. Shanker、Theodora U. J. Bruun、Brian L. Hie、Peter S. Kim；Stanford Peter Kim Lab 发布论文材料，Zenodo 发布原始研究归档，Graylab/FLAb 提供后续标准化表

### 来源方背景

Peter Kim Lab 是 Stanford University School of Medicine 的学术研究团队，研究结合结构生物学、蛋白质工程、免疫学和机器学习，当前公开方向包括以蛋白语言模型理解并引导蛋白进化。Peter S. Kim 现为 Stanford 生物化学教授、Sarafan ChEM-H Institute Scholar，并任 Chan Zuckerberg Biohub San Francisco investigator。该来源方不是独立商业公司，因此公司成立时间、融资、运营收入和上市状态不适用；本数据的发布关系应理解为“Stanford 学术团队—Science/bioRxiv 论文—Zenodo/PMC 研究附件—FLAb 后续汇编”。

## 实验设计和数据口径

这项研究先用已有蛋白和抗体突变实验检验结构条件语言模型，再把方法用于两个抗 SARS-CoV-2 临床抗体亲本 LY-CoV1404（bebtelovimab）和 SA58。R46 同时保存了这两部分：Zenodo 原始归档主要包含模型评估所用的 DMS/抗体基准和计算输出；Data S1、S2、S4 及 FLAb 表则承载两个亲本的新实验结果。它们不是同一批样本，也不能合并成一个统一的 binder/non-binder 标签表。

主实验链可概括为：

```text
亲本抗体及共享复合物结构（LY-CoV1404: 7MMO；SA58: 7Y0W）
  └─ 结构条件语言模型给候选单点替换打分
       └─ Round 1：每个亲本选 20 个单点变体，共 40 个
            └─ 表达 IgG；以假病毒中和实验测 IC50
                 └─ 将 IC50 相对 WT 改善超过 1.1 倍的替换组合为 Round 2 设计
                      ├─ 再测不同病毒株的 IC50
                      ├─ 用 BLI 测 RBD 结合的 apparent KD
                      └─ 对部分设计测多特异性 APC MFI
```

WT 是同一亲本的实验参照；Elotuzumab 和 ixekizumab 是多特异性实验中用于锚定低、高信号范围的临床抗体对照，都不是模型新设计的候选。论文还用只依赖序列的语言模型重复两轮设计作为方法对照，Data S1 因而同时包含 `SILM Variants` 和 `LM Variants` 四个 sheets。

IC50 和 KD 回答的问题不同。IC50 来自 ACE2/TMPRSS2/HeLa 细胞的 SARS-CoV-2 假病毒中和实验：发光信号经细胞-only 和病毒-only 对照归一化，再以三参数抑制曲线求使感染信号降低 50% 的抗体浓度；数值越低通常表示功能性中和越强。实验使用 biological duplicates 和 technical duplicates。KD 来自 Octet RED96 的 BLI：生物素化 RBD 固定在 streptavidin sensor 上，IgG 以 100 nM 结合，曲线按 1:2 bivalent model 拟合；因此这是双价 IgG 的 apparent KD，不是单价内禀亲和力。Data S2 保存两个 replicate、平均值、误差和 fold-change，FLAb KD 表只保留平均值及序列。

本次取得的一手表把 FLAb 的处理边界解释清楚了：

| 一手附件 | 一手范围 | FLAb 对应处理 |
| --- | --- | --- |
| Data S1 | 4 sheets、115 条非空 WT/设计记录；每行可同时有两个病毒株端点，并保留 SD、`n` 和 `>LOQ` | 拆成 4 张按亲本/病毒株命名的 IC50 CSV，只保留可写成标量的 150 条端点并添加 VH/VL；不是 150 个独立设计 |
| Data S2 | LY-CoV1404 36 条 BQ.1.1 记录；SA58 30 条 BQ.1.1 和 30 条 XBB.1.5 记录 | 3 张 KD CSV 共 73 行；SA58-BQ.1.1 中 23 条 `<1.0E-12` 字符串未进入 FLAb，数值行被保留 |
| Data S4 | 39 条 APC MFI replicate，涉及 13 个 control/WT/设计组合 | 3 张 polyreactivity CSV 仍为 39 行，增加序列，`fitness` 复制端点值 |
| Data S3 / S5 | 30 条模型相关性汇总 / 19 条机器学习定向进化研究比较 | 当前所选 FLAb 表没有对应拆分文件；它们是研究背景和模型评价，不是新抗体结合标签 |

**上游数值边界：** Data S2 证明 FLAb 中 SA58-BQ.1.1 的 `0.0` 来自原工作簿对两个 `<1.0E-12` replicate 写入的平均值；SA58-XBB.1.5 的 `7.642e+19` 和 `1.804e+12` M 也来自一手表的字面拟合结果。前者是检测下限/删失信息被压平后的值，后两者明显不能当可靠定量亲和力。三类值均按原样保留，不解释为无限强或真实超弱结合，不取对数，也不用于无审查的排序。

**单位边界：** Data S1 自身在不同病毒株列中交替使用 `ng/µL` 和 `µg/µL`，而正文只称 IC50 达到 nanomolar range；因此新取得的一手表没有消除、反而确认了上游单位标注不一致。FLAb 的统一表头 `Avg Neutralization IC50 (ng/µL)` 只能按原字段保存，未经作者确认不得据此做跨表绝对浓度换算。

## 论文原文

### 正式发表版

- 标题：Unsupervised evolution of protein and antibody complexes with a structure-informed language model
- 作者：Varun R. Shanker、Theodora U. J. Bruun、Brian L. Hie、Peter S. Kim
- 发表来源：*Science* 385, 46–53 (2024)，Version of Record
- 归档文本版本：作者课题组公开的正式发表版 PDF；与 DOI、题名和页码一致
- 发布日期：2024-07-04
- DOI：[10.1126/science.adk8946](https://doi.org/10.1126/science.adk8946)
- PMID / PMCID：38963838 / PMC11616794
- OpenAlex：work `W4400313991`，截至 2026-09-24 引用数 146；该计数随时间变化
- 本地主文：`articles/Shanker_2024-07-04_Science-AuthorHosted.pdf`
- 文件大小：1.23 MiB（1,292,947 bytes）；8 页
- SHA-256：`cd207004fb1421eb2fcc3709a82af838113471de5426a3d581f441e2f9246704`
- 文本许可：© 2024 authors, exclusive licensee AAAS；没有把数据仓库的 CC BY 4.0 延伸到论文 PDF
- 补充材料：当前 PMC 正式关联清单中的 Supplementary Material 与 Data S1–S5 已全部取得；作者站另有一份页数不同的 Science supplementary information，两个 PDF 均按原字节保留

| 对象 | 本地文件 | 大小 | SHA-256 |
| --- | --- | --- | --- |
| Science supplementary information | `articles/Shanker_2024-07-04_Science-SupplementaryInformation.pdf` | 2.93 MiB（3,076,988 bytes）；32 页 | `09bbefb7af4e20dfe80a276ffde44d8ae05a5cb6625c557ef6f86aa8fa6d4ef8` |
| PMC author-manuscript supplement | `articles/Shanker_2024-07-04_PMC-SupplementaryMaterial.pdf` | 4.38 MiB（4,594,623 bytes）；23 页 | `f888090e7c672296c9ecc91897d255a6332856a565865080b135ccab8de0d99d` |
| Data S1 | `Shanker-supplementary-data/Shanker_2024-07-04_Data-S1.xlsx` | 21.17 KiB（21,682 bytes） | `c25926bc1caa63ed5597dd04c6bfc5334b8c39f51b1d0b8dfa0833c6b2c95e76` |
| Data S2 | `Shanker-supplementary-data/Shanker_2024-07-04_Data-S2.xlsx` | 21.40 KiB（21,912 bytes） | `30a26684801a9cd56fc3f46c9177d4fec6a08108c8e04365d20c98b30a9a1c02` |
| Data S3 | `Shanker-supplementary-data/Shanker_2024-07-04_Data-S3.csv` | 892 B（892 bytes） | `9726d13f5e0df4db23db47e69559ac0897156d349583a6712e30797901508a83` |
| Data S4 | `Shanker-supplementary-data/Shanker_2024-07-04_Data-S4.xlsx` | 11.38 KiB（11,657 bytes） | `7c0d694f2b5f0be0435babffa919e853761b59d34cf55bfe24f8b7ce51e7d065` |
| Data S5 | `Shanker-supplementary-data/Shanker_2024-07-04_Data-S5.xlsx` | 13.61 KiB（13,941 bytes） | `4c76fae17c824c9a8bb12049fce8e75112e953b222f3dd792c150f59e0e89222` |

### 预印本

- 标题：Inverse folding of protein complexes with a structure-informed language model enables unsupervised antibody evolution
- 作者：Varun R. Shanker、Theodora U. J. Bruun、Brian L. Hie、Peter S. Kim
- 发表来源：bioRxiv，v2
- 归档文本版本：作者课题组公开的 bioRxiv v2 PDF；PDF 标注本版本发表于 2023-12-21
- DOI：[10.1101/2023.12.19.572475](https://doi.org/10.1101/2023.12.19.572475)
- OpenAlex：work `W4390023653`，截至 2026-09-24 引用数 20；不与正式版相加
- 本地文件：`articles/Shanker_2023-12-21_bioRxiv-v2-AuthorHosted.pdf`
- 文件大小：5.33 MiB（5,588,840 bytes）；56 页
- SHA-256：`85f6133934d91158a50990c9868b468022cc02e53dc57f28c887cc393a5b1885`
- 文本许可：CC BY-NC-ND 4.0
- 与正式版关系：正式发表版改题并经过同行评议；解释当前数据时以正式版 Methods、Data S1–S5 和 Zenodo 记录为主，预印本保留用于追踪版本演变

## 仓库内容

`source_version` 使用一手 Zenodo record 11260318 的正式记录号，不使用下载日伪造版本。它是一个可追溯的组合快照：Zenodo 原始归档发布于 2024-07-04；Data S1–S5 来自当前 PMC 关联文件；FLAb 10 张标准化 CSV 固定在 commit `e05e3f0135783ffb7de412df6a1467e7a0031911`（2026-08-17）。作者代码仓库只作为来源连接核验，没有把完整代码 tree 混入数据 payload。

```text
zenodo-11260318/
  FLAb/data/binding/                 # 7 CSV：IC50 4 张、KD 3 张
  FLAb/data/polyreactivity/          # 3 CSV：APC MFI
  Shanker-supplementary-data/        # Data S1–S5
  structural-evolution-data/         # Zenodo data.tar.gz
```

目录树只列上游数据 payload。`articles/`、`pdb/` 与 README 另作为论文归档、结构核验和版本说明材料保存，不混入上表。全部文件保持原字节或按 RCSB `.cif.gz` 无损解压；没有把表格清洗、去重、换单位或覆盖原文件。

## 数据结构

### 文件和记录关系

FLAb 的 7 张 binding CSV 共 223 行，其中 IC50 150 行、KD 73 行；3 张 polyreactivity CSV 共 39 行。行数表示“某序列在某亲本、抗原株、端点或 replicate 下的一条记录”，不等于独立抗体数。同一 WT/设计会跨病毒株、端点和文件重复出现，训练/测试划分必须按亲本与实际 VH/VL 序列检查泄漏。

| FLAb 文件 | 数据行 | 唯一 VH/VL | 额外整行副本 | 序列长度 aa | 空值 |
| --- | --- | --- | --- | --- | --- |
| `FLAb/data/binding/shanker2024unsupervised_Ly1404-BQ.1.1_IC50.csv` | 50 | 45 | 0 | heavy=[119], light=[109] | chain=2 |
| `FLAb/data/binding/shanker2024unsupervised_Ly1404-BQ.1.1_Kd.csv` | 36 | 32 | 0 | heavy=[119], light=[109] | Chain Mutated=5 |
| `FLAb/data/binding/shanker2024unsupervised_Ly1404_Wuhan_IC50.csv` | 32 | 32 | 0 | heavy=[119], light=[109] | chain=1 |
| `FLAb/data/binding/shanker2024unsupervised_SA58-BA.1_IC50.csv` | 19 | 19 | 0 | heavy=[120], light=[109] | chain=1 |
| `FLAb/data/binding/shanker2024unsupervised_SA58-BQ.1.1_IC50.csv` | 49 | 46 | 0 | heavy=[120], light=[109] | chain=2 |
| `FLAb/data/binding/shanker2024unsupervised_SA58-BQ.1.1_Kd.csv` | 7 | 7 | 0 | heavy=[120], light=[109] | 0 |
| `FLAb/data/binding/shanker2024unsupervised_SA58-XBB.1.5_Kd.csv` | 30 | 26 | 0 | heavy=[120], light=[109] | Chain Mutated=5 |
| `FLAb/data/polyreactivity/shanker2024unsupervised_APC-MFI_Elotuzumab-Ixekuzimab.csv` | 6 | 2 | 0 | heavy=[119], light=[107, 112] | 0 |
| `FLAb/data/polyreactivity/shanker2024unsupervised_APC-MFI_Ly1404.csv` | 18 | 6 | 0 | heavy=[119], light=[109] | chain=3 |
| `FLAb/data/polyreactivity/shanker2024unsupervised_APC-MFI_SA58.csv` | 15 | 5 | 1 | heavy=[120], light=[109] | chain=3 |

Data S1–S5 是正式论文附件，保留比 FLAb 更完整的重复、误差、删失和方法比较信息。Zenodo `data.tar.gz` 则是另一层完整原始研究归档：99 个普通成员，含 45 CSV、19 FASTA、23 PDB、8 JSON、1 XLSX、1 TXT 和 2 个辅助文件；展开体积 140,765,212 bytes。本项目不在 raw 目录展开它，审计时逐成员读取。

### 字段说明

| 文件/表组 | 原字段 | 类型、枚举、单位与方向 | 含义/限制 |
| --- | --- | --- | --- |
| FLAb 全部 CSV | `heavy`, `light` | 氨基酸字符串；LY 119/109 aa，SA58 120/109 aa；对照轻链另有 107/112 aa | 抗体可变区，不是完整 IgG construct；FLAb 后加字段 |
| FLAb IC50 | `chain` | 枚举：空值、`HC`、`LC`、`both` | 突变所在链；空值对应 WT 或未填，不表示缺少序列 |
| FLAb IC50 | `design` | WT 或突变组合标识 | 亲本内设计名，不是全局样本键 |
| FLAb IC50 | `Avg Neutralization IC50 (ng/µL)` | 浮点；越低通常中和越强；上游 Data S1 单位标签内部不一致 | 假病毒中和端点；FLAb 已去掉 SD、n、fold-change 和 >LOQ 行 |
| FLAb IC50 | `fitness` | 与 IC50 标量相同 | 派生副本；预测同一端点时不得作为输入 |
| FLAb KD | `Chain Mutated` | 枚举：空值、`HC`、`LC`、`both` | 与 Data S2 同义字段 |
| FLAb KD | `Design` | WT 或突变组合标识 | 大小写保留上游风格 |
| FLAb KD | `Kd avg (M)` | 浮点，M；越低通常结合越强；含 0 和两个极端值 | BLI 1:2 bivalent fit 的 apparent KD；不是 SPR 或单价 KD |
| FLAb KD | `fitness` | 与 `Kd avg (M)` 相同 | 派生副本；不是独立标签 |
| FLAb APC-MFI | `chain` | 枚举：空值、`HC`、`LC`、`both`；control 文件无此列 | 突变所在链 |
| FLAb APC-MFI | `Design` / `design` | WT、突变组合或 control 名称 | 同一设计有多个 replicate；大小写随原文件 |
| FLAb APC-MFI | `APC MFI` | 非负整数；越高表示更强 PSR 信号 | 多特异性/非特异相互作用端点，不是抗原亲和力 |
| FLAb APC-MFI | `fitness` | 与 APC MFI 相同；control 文件只保留此列 | 派生副本 |
| Data S1 | `Round`, `n_mut`, `Chain Mutated`, `Design` | `Round` 枚举 1/2；链枚举空、HC、LC、both | 四个 sheets 分别为两个亲本的 SILM/LM 设计 |
| Data S1 | `Avg Neutralization IC50 ± SD (...)`, `n`, `Avg IC50 Fold-Change ± SD` | 数值±SD、整数或 NA/n.d./>LOQ；单位标签依列为 ng/µL 或 µg/µL | 每个病毒株一组三列；保留重复数和删失信息 |
| Data S2 | `Antigen`, `Round`, `Chain Mutated`, `Design` | Antigen 枚举 BQ.1.1、XBB.1.5；Round 1/2；链为 HC/LC/both | 合并单元格需向下填充 Antigen/Round 才能逐行解释 |
| Data S2 | `Kd rep1 (M)`, `Kd rep2 (M)`, `Kd avg (M)`, `Kd Std Dev/error (nM)`, `Kd FC` | 数值或 `<1.0E-12`/Undefined；单位按原表 | 完整 BLI 汇总；注意 error 表头为 nM、实际数值尺度需结合原表审查 |
| Data S3 | `Input`, `Method`, `Antibody`, `Target`, `Correlation` | Input/Method/抗体/靶点枚举与 Spearman 相关系数 | `Input` 包括 Ab-Ag、Ab only、Ab VH only/Ab VH/VL only、ESM-1v、AbLang、abYsis |
| Data S4 | `Antibody`, `Design`, `APC MFI`, `MFI FC`, `Kd FC`, `Antigen` | Antibody 枚举 Control、Ly-1404、SA58；其余为数值或空值 | 39 条多特异性 replicate；FC/Antigen 仅部分行有值 |
| Data S5 | `study`, `title`, `link`, `phenotype` | 研究元数据字符串 | 机器学习定向进化研究比较，不是 R46 新实验样本 |
| Data S5 | `labeled data points used for training`, `hit rate (frac improved)`, `log10(search space)` | 整数/浮点/NA | 跨研究比较指标 |
| Data S5 | `interpolative_extrapolative`, `ML_requires_structure`, `original study link` | 枚举 interpolative/extrapolative、yes/no 或空值 | 方法分类与链接 |
| Zenodo `dms/if_results` | `seqid`, `log_likelihood`, `log_likelihood_target` 或 `log_likelihood_exclude` | 标识和模型分数；无统一实验单位 | 12 个 DMS 模型输出表 |
| Zenodo `dms/dms_files` 与 `dms_esm1vScored` | `variant`、各预测器列、各 `DMS*` 实验列、5 个 `esm1v*` 列 | 宽表；字段因蛋白而异 | 已有 DMS benchmark 及模型分数，不并入新抗体 IC50/KD |
| Zenodo CR6261/CR9114 | `genotype`, 各病毒株 replicate/mean/sem, `pos*`, `som_mut`, `mutant` | 组合基因型、实验读数和位点 | 既有抗流感抗体突变基准 |
| Zenodo G6 | `id`, `norm_binding`, `expr_enrich`, `mutant`；两个无表头文件为 sequence/value | 序列、结合/表达读数 | 无表头文件必须显式指定两列，不能把首行当表头 |
| Zenodo abYsis JSON | `scheme_name`, `frequencies` | 字符串和嵌套频数结构 | 抗体残基频率背景 |

### 数据示例

| 真实文件/位置 | 实际值摘录 | 解释范围 |
| --- | --- | --- |
| `shanker2024unsupervised_Ly1404-BQ.1.1_IC50.csv` 第 2 行 | chain=空, design=WT, Avg Neutralization IC50 (ng/µL)=110.0, fitness=110.0 | heavy 119 aa / light 109 aa |
| `shanker2024unsupervised_Ly1404-BQ.1.1_Kd.csv` 第 2 行 | Chain Mutated=空, Design=WT, Kd avg (M)=1.7e-06, fitness=1.7e-06 | heavy 119 aa / light 109 aa |
| `shanker2024unsupervised_Ly1404_Wuhan_IC50.csv` 第 2 行 | chain=空, design=WT, Avg Neutralization IC50 (ng/µL)=2.7, fitness=2.7 | heavy 119 aa / light 109 aa |
| `shanker2024unsupervised_SA58-BA.1_IC50.csv` 第 2 行 | chain=空, design=WT, Avg Neutralization IC50 (ng/µL)=22.0, fitness=22.0 | heavy 120 aa / light 109 aa |
| `shanker2024unsupervised_SA58-BQ.1.1_IC50.csv` 第 2 行 | chain=空, design=WT, Avg Neutralization IC50 (ng/µL)=6.4, fitness=6.4 | heavy 120 aa / light 109 aa |
| `shanker2024unsupervised_SA58-BQ.1.1_Kd.csv` 第 2 行 | Chain Mutated=HC, Design=T55N, Kd avg (M)=4.59e-09, fitness=4.59e-09 | heavy 120 aa / light 109 aa |
| `shanker2024unsupervised_SA58-XBB.1.5_Kd.csv` 第 2 行 | Chain Mutated=空, Design=WT, Kd avg (M)=2.38e-06, fitness=2.38e-06 | heavy 120 aa / light 109 aa |
| `shanker2024unsupervised_APC-MFI_Elotuzumab-Ixekuzimab.csv` 第 2 行 | Design=Ixekuzimab, fitness=81038 | heavy 119 aa / light 112 aa |
| `shanker2024unsupervised_APC-MFI_Ly1404.csv` 第 2 行 | chain=空, design=WT, APC MFI=9944, fitness=9944 | heavy 119 aa / light 109 aa |
| `shanker2024unsupervised_APC-MFI_SA58.csv` 第 2 行 | chain=空, design=WT, APC MFI=2065, fitness=2065 | heavy 120 aa / light 109 aa |
| Data S1 / `Ly1404 SILM Variants` 第 3 行 | Design=WT；Wuhan IC50=2.7 ± 1.1，n=3；BQ.1.1 IC50=110 ± 32，n=7 | 展示同一行包含两个病毒株端点；单位按原表列头 |
| Data S2 / `SA58` 第 2 行 | Antigen=BQ.1.1；Design=WT；rep1/rep2/avg=<1.0E-12；error=Undefined | FLAb 没有保留这类字符串删失记录 |
| Data S3 第 2 行 | Input=Ab-Ag；Method=SILM；Antibody=CR9114；Target=H1；Correlation=0.65 | 模型相关性汇总，不是 KD |
| Data S4 第 2 行 | Antibody=Control；Design=Elotuzumab；APC MFI=1963 | control replicate，不是模型设计 |
| Data S5 第 2 行 | study=Biswas (2021)；phenotype=fluorescence；training points=24；hit rate=0.1 | 跨研究方法比较 |

示例只用于说明真实布局；序列不在文档重复展开。所有预测任务都应从原文件读取，并把 `fitness`、fold-change、模型 score 等与目标同源的派生字段排除在输入之外。

## PDB 数据库

接受 19 个有一手连接证据的结构锚点，但用途分两层。`7MMO` 和 `7Y0W` 是两个新实验亲本的共享参考复合物：7MMO 的 A/D、B/E、C/F 分别是 LY-CoV1404 重链、轻链和原始株 RBD；7Y0W 的 H、L、R 是 SA58（BD55-5840）重链、轻链和 BA.1 RBD，A/B 属于同一条目中的另一抗体。它们不能冒充 BQ.1.1/XBB.1.5 或每条设计变体的实验结构。

其余 17 个 entry 来自 Zenodo 捆绑 benchmark：`3GBN`、`4FQI`、`2FJG` 对应 CR6261、CR9114、G6 抗体基准，另外 14 个是蛋白 DMS 输入或背景。它们用于复现模型评估，不代表新增的 LY-CoV1404/SA58 结合实验。

| RCSB entry | 一手连接证据 | 完整条目的 polymer entities |
| --- | --- | --- |
| [1M40](https://www.rcsb.org/structure/1M40) | Zenodo archive:data/dms/dms_libs/bla_1m40_dmsLib.fasta; Zenodo archive:data/dms/dms_libs/bla_1m40_a_dmsLib.fasta; Zenodo archive:data/dms/structures/bla_1m40_a.pdb | entity 1: author A, 263 aa, BETA-LACTAMASE TEM |
| [1USU](https://www.rcsb.org/structure/1USU) | Zenodo archive:data/dms/dms_libs/hsp82_1usu_a_dmsLib.fasta; Zenodo archive:data/dms/structures/hsp82_1usu_a.pdb | entity 1: author A, 260 aa, HEAT SHOCK PROTEIN HSP82; entity 2: author B, 170 aa, AHA1 |
| [2BZG](https://www.rcsb.org/structure/2BZG) | Zenodo archive:data/dms/dms_libs/tpmt_2bzg_a_dmsLib.fasta; Zenodo archive:data/dms/structures/tpmt_2bzg_a.pdb | entity 1: author A, 232 aa, THIOPURINE S-METHYLTRANSFERASE |
| [2CE2](https://www.rcsb.org/structure/2CE2) | Zenodo archive:data/dms/dms_libs/hras_2ce2_x_dmsLib.fasta; Zenodo archive:data/dms/structures/hras_2ce2_x.pdb | entity 1: author X, 166 aa, GTPASE HRAS |
| [2FJG](https://www.rcsb.org/structure/2FJG) | Zenodo archive:data/ab_mutagenesis_expts/g6/g6_2fjg_lc_lib.fasta; Zenodo archive:data/ab_mutagenesis_expts/g6/2fjg_lh_fvar.pdb; Zenodo archive:data/ab_mutagenesis_expts/g6/2fjg_l_fvar.pdb; Zenodo archive:data/ab_mutagenesis_expts/g6/g6_2fjg_hc_lib.fasta; Zenodo archive:data/ab_mutagenesis_expts/g6/2fjg_h_fvar.pdb; Zenodo archive:data/ab_mutagenesis_expts/g6/2fjg_vlh_fvar.pdb | entity 1: author V,W, 102 aa, Vascular endothelial growth factor A; entity 2: author L,A, 214 aa, Fab light chain; entity 3: author H,B, 227 aa, Fab heavy chain |
| [2RH1](https://www.rcsb.org/structure/2RH1) | Zenodo archive:data/dms/dms_libs/adrb2_2rh1_dmsLib.fasta | entity 1: author A, 500 aa, beta-2-adrenergic receptor/T4-lysozyme chimera |
| [3COQ](https://www.rcsb.org/structure/3COQ) | Zenodo archive:data/dms/dms_libs/gal4_3coq_b_dmsLib.fasta; Zenodo archive:data/dms/structures/gal4_3coq_b.pdb | entity 1: author D, 20 aa, DNA (5'-D(*DAP*DCP*DCP*DGP*DGP*DAP*DGP*DGP*DAP*DCP*DAP*DGP*DTP*DCP*DCP*DTP*DCP*DCP*DGP*DG)-3'); entity 2: author E, 20 aa, DNA (5'-D(*DTP*DCP*DCP*DGP*DGP*DAP*DGP*DGP*DAP*DCP*DTP*DGP*DTP*DCP*DCP*DTP*DCP*DCP*DGP*DG)-3'); entity 3: author A,B, 89 aa, Regulatory protein GAL4 |
| [3GBN](https://www.rcsb.org/structure/3GBN) | Zenodo archive:data/ab_mutagenesis_expts/cr6261/cr6261_3gbn_hc_lib.fasta; Zenodo archive:data/ab_mutagenesis_expts/cr6261/3gbn_h_fvar.pdb; Zenodo archive:data/ab_mutagenesis_expts/cr6261/3gbn_lh_fvar.pdb; Zenodo archive:data/ab_mutagenesis_expts/cr6261/3gbn_ablh_fvar.pdb | entity 1: author A, 331 aa, Hemagglutinin; entity 2: author B, 179 aa, Hemagglutinin; entity 3: author H, 226 aa, Fab Heavy Chain; entity 4: author L, 221 aa, Fab Lambda Light Chain |
| [3S4Y](https://www.rcsb.org/structure/3S4Y) | Zenodo archive:data/dms/dms_libs/tpk1_3s4y_a_dmsLib.fasta; Zenodo archive:data/dms/structures/tpk1_3s4y_a.pdb | entity 1: author A,B, 247 aa, Thiamin pyrophosphokinase 1 |
| [3UBT](https://www.rcsb.org/structure/3UBT) | Zenodo archive:data/dms/dms_libs/haeiiim_3ubt_b_dmsLib.fasta; Zenodo archive:data/dms/structures/haeiiim_3ubt_b.pdb | entity 1: author Y,A,B, 331 aa, Modification methylase HaeIII; entity 2: author D,E,F,G,H,C, 6 aa, 5'-D(*TP*GP*GP*CP*CP*A)-3' |
| [3VUB](https://www.rcsb.org/structure/3VUB) | Zenodo archive:data/dms/dms_libs/ccdb_3vub_a_dmsLib.fasta; Zenodo archive:data/dms/structures/ccdb_3vub_a.pdb | entity 1: author A, 101 aa, CCDB |
| [4FQI](https://www.rcsb.org/structure/4FQI) | Zenodo archive:data/ab_mutagenesis_expts/cr9114/4fqi_h_fvar.pdb; Zenodo archive:data/ab_mutagenesis_expts/cr9114/4fqi_lh_fvar.pdb; Zenodo archive:data/ab_mutagenesis_expts/cr9114/cr9114_4fqi_hc_lib.fasta; Zenodo archive:data/ab_mutagenesis_expts/cr9114/4fqi_ablh_fvar.pdb | entity 1: author A, 334 aa, Hemagglutinin HA1; entity 2: author B, 177 aa, Hemagglutinin HA2; entity 3: author H, 230 aa, antibody CR9114 heavy chain; entity 4: author L, 216 aa, antibody CR9114 light chain |
| [4Q5E](https://www.rcsb.org/structure/4Q5E) | Zenodo archive:data/dms/dms_libs/ubi4_4q5e_b_dmsLib.fasta; Zenodo archive:data/dms/structures/ubi4_4q5e_b.pdb | entity 1: author A, 174 aa, Protein kinase OspG; entity 2: author B, 76 aa, Polyubiquitin; entity 3: author C, 156 aa, Ubiquitin-conjugating enzyme E2 L3 |
| [4ZZN](https://www.rcsb.org/structure/4ZZN) | Zenodo archive:data/dms/dms_libs/mapk1_4zzn_a_dmsLib.fasta; Zenodo archive:data/dms/structures/mapk1_4zzn_a.pdb | entity 1: author A, 350 aa, MITOGEN-ACTIVATED PROTEIN KINASE 1 |
| [5B2R](https://www.rcsb.org/structure/5B2R) | Zenodo archive:data/dms/dms_libs/cas9_5b2r_b_dmsLib.fasta; Zenodo archive:data/dms/structures/cas9_5b2r_b.pdb | entity 1: author A, 81 aa, Guide RNA; entity 2: author B, 1372 aa, CRISPR-associated endonuclease Cas9; entity 3: author C, 28 aa, Target DNA; entity 4: author D, 8 aa, Non-target DNA, DNA (5'-D(*TP*GP*AP*GP*AP*TP*TP*G)-3') |
| [5F6E](https://www.rcsb.org/structure/5F6E) | Zenodo archive:data/dms/dms_libs/ube2i_5f6e_a_dmsLib.fasta; Zenodo archive:data/dms/structures/ube2i_5f6e_a.pdb | entity 1: author A, 157 aa, SUMO-conjugating enzyme UBC9 |
| [5V03](https://www.rcsb.org/structure/5V03) | Zenodo archive:data/dms/dms_libs/calm1_5v03_r_dmsLib.fasta; Zenodo archive:data/dms/structures/calm1_5v03_r.pdb | entity 1: author B, 102 aa, Small conductance calcium-activated potassium channel protein 2; entity 2: author R, 149 aa, Calmodulin |
| [7MMO](https://www.rcsb.org/structure/7MMO) | main-paper/shared-binding reference | entity 1: author A,D, 223 aa, LY-CoV1404 Fab heavy chain; entity 2: author B,E, 215 aa, LY-CoV1404 Fab light chain; entity 3: author C,F, 205 aa, Spike protein S1 |
| [7Y0W](https://www.rcsb.org/structure/7Y0W) | main-paper/shared-binding reference | entity 1: author A, 123 aa, BD55-5514H; entity 2: author B, 107 aa, BD55-5514L; entity 3: author H, 119 aa, BD55-5840H; entity 4: author L, 109 aa, BD55-5840L; entity 5: author R, 193 aa, Spike protein S1 |

每个 entry 保存一个 RCSB full-entry FASTA 和一个完整 mmCIF，共 13.50 MiB（14,159,546 bytes）。FASTA 路径为 `pdb/sequences/rcsb_pdb_<ID>.fasta`，坐标路径为 `pdb/structures/<ID>.cif`；逐 polymer canonical sequence、entry identity、坐标和 chain reference 已重新配对核验。PDB 子集 inventory SHA-256 为 `f115c41081d893ed3db1eb0acc7073576e685a94ac8d7fdcd9451726214519f0`。没有补环、CDR graft、变体重建、按数据行复制或把作者裁剪 PDB 冒充 RCSB 原件。

## 使用方式

优先按问题选择一手层级：需要重复、误差、删失或明确 assay 设计时读 Data S1/S2/S4；只需统一 VH/VL 加单个标量端点时才读 FLAb。不要把 IC50、apparent KD 和 APC MFI 拼成同一数值标签。

```python
import csv
from pathlib import Path

dataset_root = Path("/path/to/zenodo-11260318")
path = dataset_root / "FLAb/data/binding/shanker2024unsupervised_Ly1404-BQ.1.1_Kd.csv"
with path.open(encoding="utf-8-sig", newline="") as stream:
    rows = list(csv.DictReader(stream))
```

使用 KD 表时，应先把 `0.0`、超大值和上游删失规则单独建模；使用 IC50 表时，不要在单位未澄清前跨病毒株做绝对浓度换算。

## 采集过程记录

- 2026-09-18：固定 FLAb commit `e05e3f0135783ffb7de412df6a1467e7a0031911`，按 Git blob 和 SHA-256 复用 R09 已核验的 10 张 CSV；下载 Zenodo 11260318 的 `data.tar.gz`，官方 MD5 `9bbf0d261f6518449ac5b1813559876a` 匹配，全部 99 个普通成员通过安全路径、长度和格式审计。
- 2026-09-18：从作者课题组 publications 页取得正式主文和 Science supplementary information；从作者页取得 bioRxiv v2。所有 PDF 均核对题名/DOI/页数并冻结原字节。
- 2026-09-18：从论文正文、归档文件名和结构引文建立 19 个 PDB 锚点，取得 RCSB full-entry FASTA/mmCIF。早期验收曾把 `verify_pair` 参数顺序传错；修正后对 19 对文件全量重跑并通过，本次又在最终审计中再次逐 entry 验证，因此错误调用没有影响交付文件或结论。
- 2026-09-24：确认 PMC 当前列出 Supplementary Material 与 Data S1–S5。旧下载端点因新增浏览器 proof-of-work 曾被误判为不可访问；归档器实现 PMC 页面公开的 SHA-256 challenge 后，六个对象全部取得并通过 PDF/XLSX/CSV 格式及 SHA-256 验证。
- 2026-09-24：逐 sheet 对照 Data S1/S2/S4 与 FLAb，确认数值筛选、删失丢失、IC50 单位冲突和 KD 异常值均来自上游处理/原表；没有在 raw 快照中修复。完成 README、PDB 双层核验、全文件 inventory、验收预览后，将 staging 原子晋升为本地正式版本目录。

| 归档本地路径 | 上游原名 | 大小 | 原字节 SHA-256 |
| --- | --- | --- | --- |
| `FLAb/data/binding/shanker2024unsupervised_Ly1404-BQ.1.1_IC50.csv` | shanker2024unsupervised_Ly1404-BQ.1.1_IC50.csv | 12.49 KiB（12,792 bytes） | `91853f8b9eea20ed3b0659aa41b718e3f8a172e4bb6c4edd8f9c9cc8dbb44bae` |
| `FLAb/data/binding/shanker2024unsupervised_Ly1404-BQ.1.1_Kd.csv` | shanker2024unsupervised_Ly1404-BQ.1.1_Kd.csv | 9.28 KiB（9,501 bytes） | `adcece1c357d52a5da3c297e77295477b28c7122a85c41234872c413f769bfad` |
| `FLAb/data/binding/shanker2024unsupervised_Ly1404_Wuhan_IC50.csv` | shanker2024unsupervised_Ly1404_Wuhan_IC50.csv | 8.01 KiB（8,199 bytes） | `641c8c6950cca8fc7e0cfec0ee6e3c023522153527d315a91bbc6a6aa5d42fa2` |
| `FLAb/data/binding/shanker2024unsupervised_SA58-BA.1_IC50.csv` | shanker2024unsupervised_SA58-BA.1_IC50.csv | 4.71 KiB（4,828 bytes） | `724d814e6ba7a796fbcd6596142d986271bb515230ba8961a48caa827f5f761e` |
| `FLAb/data/binding/shanker2024unsupervised_SA58-BQ.1.1_IC50.csv` | shanker2024unsupervised_SA58-BQ.1.1_IC50.csv | 12.12 KiB（12,415 bytes） | `a6c62235a8826775f8b2f9a36725a3f62b58e1435b49dce072e1ff1b9737f96a` |
| `FLAb/data/binding/shanker2024unsupervised_SA58-BQ.1.1_Kd.csv` | shanker2024unsupervised_SA58-BQ.1.1_Kd.csv | 1.81 KiB（1,855 bytes） | `15b2095afd64be421f2148e2c878e4b3affa013e46dd5f4b593e8201f0a88d1e` |
| `FLAb/data/binding/shanker2024unsupervised_SA58-XBB.1.5_Kd.csv` | shanker2024unsupervised_SA58-XBB.1.5_Kd.csv | 7.61 KiB（7,789 bytes） | `40c8f336925429fb2c349b883c2997d328cc1a5ad36431a0aa30a78fa2b0869a` |
| `FLAb/data/polyreactivity/shanker2024unsupervised_APC-MFI_Elotuzumab-Ixekuzimab.csv` | shanker2024unsupervised_APC-MFI_Elotuzumab-Ixekuzimab.csv | 1.47 KiB（1,509 bytes） | `375516ab38a7ac0064baa148cb4a88d6af34b9e691e393f8e0dc916e2aa8837f` |
| `FLAb/data/polyreactivity/shanker2024unsupervised_APC-MFI_Ly1404.csv` | shanker2024unsupervised_APC-MFI_Ly1404.csv | 4.86 KiB（4,980 bytes） | `baf07b9679840563cf0cbce1ab93d45346f05151072313a6e60d80d9c95f5c48` |
| `FLAb/data/polyreactivity/shanker2024unsupervised_APC-MFI_SA58.csv` | shanker2024unsupervised_APC-MFI_SA58.csv | 3.75 KiB（3,836 bytes） | `e371a4a310981b69367c5f0c8a7f918ea23038d4e0544b14398771e160d2102d` |
| `Shanker-supplementary-data/Shanker_2024-07-04_Data-S1.xlsx` | NIHMS2034687-supplement-Data_s1.xlsx | 21.17 KiB（21,682 bytes） | `c25926bc1caa63ed5597dd04c6bfc5334b8c39f51b1d0b8dfa0833c6b2c95e76` |
| `Shanker-supplementary-data/Shanker_2024-07-04_Data-S2.xlsx` | NIHMS2034687-supplement-Data_s2.xlsx | 21.40 KiB（21,912 bytes） | `30a26684801a9cd56fc3f46c9177d4fec6a08108c8e04365d20c98b30a9a1c02` |
| `Shanker-supplementary-data/Shanker_2024-07-04_Data-S3.csv` | NIHMS2034687-supplement-Data_s3.csv | 892 B（892 bytes） | `9726d13f5e0df4db23db47e69559ac0897156d349583a6712e30797901508a83` |
| `Shanker-supplementary-data/Shanker_2024-07-04_Data-S4.xlsx` | NIHMS2034687-supplement-Data_s4.xlsx | 11.38 KiB（11,657 bytes） | `7c0d694f2b5f0be0435babffa919e853761b59d34cf55bfe24f8b7ce51e7d065` |
| `Shanker-supplementary-data/Shanker_2024-07-04_Data-S5.xlsx` | NIHMS2034687-supplement-Data_s5.xlsx | 13.61 KiB（13,941 bytes） | `4c76fae17c824c9a8bb12049fce8e75112e953b222f3dd792c150f59e0e89222` |
| `articles/Shanker_2023-12-21_bioRxiv-v2-AuthorHosted.pdf` | 20231219572475v2full-1.pdf | 5.33 MiB（5,588,840 bytes） | `85f6133934d91158a50990c9868b468022cc02e53dc57f28c887cc393a5b1885` |
| `articles/Shanker_2024-07-04_PMC-SupplementaryMaterial.pdf` | NIHMS2034687-supplement-Supplementary_Material.pdf | 4.38 MiB（4,594,623 bytes） | `f888090e7c672296c9ecc91897d255a6332856a565865080b135ccab8de0d99d` |
| `articles/Shanker_2024-07-04_Science-AuthorHosted.pdf` | science.adk8946.pdf | 1.23 MiB（1,292,947 bytes） | `cd207004fb1421eb2fcc3709a82af838113471de5426a3d581f441e2f9246704` |
| `articles/Shanker_2024-07-04_Science-SupplementaryInformation.pdf` | Shanker 2024 SI.pdf | 2.93 MiB（3,076,988 bytes） | `09bbefb7af4e20dfe80a276ffde44d8ae05a5cb6625c557ef6f86aa8fa6d4ef8` |
| `structural-evolution-data/Shanker_2024-07-04_Zenodo-11260318.tar.gz` | data.tar.gz | 49.24 MiB（51,634,008 bytes） | `218ab6fa2ee3f8b5d649ebfbf485f545e402a80327a7c08ee92ee62a7ede0687` |

Zenodo 原名 `data.tar.gz` 仅做描述性改名，字节未变；Data S1–S5 和 PMC supplement 也保留上游原名及下载连接。这里的“发布”只指从项目 `.staging` 晋升到共享存储的正式本地版本路径，不代表向互联网重新分发。

## 参考文献

- [正式论文](https://doi.org/10.1126/science.adk8946)。
- [bioRxiv v2](https://doi.org/10.1101/2023.12.19.572475)。
- [PMC 正文与关联文件](https://pmc.ncbi.nlm.nih.gov/articles/PMC11616794/)。
- [Zenodo 原始数据](https://doi.org/10.5281/zenodo.11260318)。
- [Zenodo 代码与脚本](https://doi.org/10.5281/zenodo.11260509)。
- [作者固定代码仓库](https://github.com/varun-shanker/structural-evolution/tree/b79576a524729cb9ef5fac4795bfa2dfee462f50)。
- [FLAb 固定版本](https://github.com/Graylab/FLAb/tree/e05e3f0135783ffb7de412df6a1467e7a0031911)。
- [Peter Kim Lab 研究方向](https://peterkimlab.stanford.edu/research-4)。
- [Peter Kim Stanford profile](https://profiles.stanford.edu/peterkim)。
- [Peter Kim Lab 论文目录](https://peterkimlab.stanford.edu/publications)。
- [OpenAlex 正式版 work](https://openalex.org/W4400313991)。
- [OpenAlex 预印本 work](https://openalex.org/W4390023653)。
- [1M40 原始结构论文（RCSB citation DOI）](https://doi.org/10.1021/ja0259640)。
- [1USU 原始结构论文（RCSB citation DOI）](https://doi.org/10.1038/SJ.EMBOJ.7600141)。
- [2BZG 原始结构论文（RCSB citation DOI）](https://doi.org/10.1002/PROT.21272)。
- [2CE2 原始结构论文（RCSB citation DOI）](https://doi.org/10.1529/BIOPHYSJ.105.078931)。
- [2FJG 原始结构论文（RCSB citation DOI）](https://doi.org/10.1074/jbc.M507783200)。
- [2RH1 原始结构论文（RCSB citation DOI）](https://doi.org/10.1126/science.1150577)。
- [3COQ 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/j.str.2008.03.015)。
- [3GBN 原始结构论文（RCSB citation DOI）](https://doi.org/10.1126/science.1171491)。
- [3UBT 原始结构论文（RCSB citation DOI）](https://doi.org/10.1074/jbc.M112.413054)。
- [3VUB 原始结构论文（RCSB citation DOI）](https://doi.org/10.1006/jmbi.1998.2395)。
- [4FQI 原始结构论文（RCSB citation DOI）](https://doi.org/10.1126/science.1222908)。
- [4Q5E 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/j.str.2014.04.010)。
- [4ZZN 原始结构论文（RCSB citation DOI）](https://doi.org/10.1021/ACS.JMEDCHEM.5B00466)。
- [5B2R 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/j.molcel.2016.02.018)。
- [5F6E 原始结构论文（RCSB citation DOI）](https://doi.org/10.1002/anie.201511351)。
- [5V03 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/j.str.2018.02.017)。
- [7MMO 原始结构论文（RCSB citation DOI）](https://doi.org/10.1101/2021.04.30.442182)。
- [7Y0W 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/j.celrep.2022.111845)。

使用某个捆绑 benchmark 或结构时，还应引用其原论文；不能只引用 Science、Zenodo 或 FLAb 汇编。

## 其他

### 数据范围和限制

当前版本是 `processed-public` 多来源组合：完整取得 Zenodo 11260318 原始归档、PMC 当前列出的 Data S1–S5 与 supplement、作者公开正式版/SI/预印本、所选 FLAb 标准化表及 19 个可辩护 RCSB 锚点。这里的“完整”仅针对上述明确定义的公开快照，不声称包含仪器原始 BLI traces、逐孔发光值、FlowJo event、所有构建/纯化批次、作者私有模型权重或未公开材料。

### 完整性与验收

独立验收 58 个文件（不含 README），共 76.76 MiB（80,484,740 bytes）；inventory SHA-256 `eaf012af072bd81166ef913316ff50ef71031f7ff8f9837aab3c0b2d14852fa7`。inventory 规则为按路径排序的 `relative_path<TAB>bytes<TAB>sha256<LF>`。所有配置 payload 均核对 frozen identity；CSV 全行解析，XLSX 校验 ZIP CRC 并遍历全部 sheets，PDF 逐页读取，TAR 逐成员安全审计，PDB 两层配对验证；目录无意外文件或符号链接。

### 许可和再分发边界

- Zenodo 11260318 原始数据标注 CC BY 4.0。
- 作者 `structural-evolution` 仓库标注 MIT；FLAb 的 study index 也把本研究对应表标为该 MIT license。该说明适用于其相应仓库对象，不自动覆盖 Science/PMC PDF 或第三方 benchmark 的原始权利。
- bioRxiv v2 标注 CC BY-NC-ND 4.0；Science 正式主文和补充 PDF 标注 © 2024 authors, exclusive licensee AAAS，未发现 CC 许可。
- RCSB 文件按 RCSB 数据库条款使用；Zenodo 归档中捆绑的既有 DMS/抗体 benchmark 还应保留各原论文引用和原条款。

本项目将文件保存到内部共享存储的正式版本目录，不把“本地发布”解释为已获得对全部对象的互联网再分发授权。

### 公开范围对照

| 来源对象 | 当前证据 | 状态 |
| --- | --- | --- |
| Zenodo 11260318 `data.tar.gz` | 官方 MD5 匹配；99 个成员逐一读取 | 完成 |
| 正式主文、作者 SI、PMC supplement、bioRxiv v2 | DOI/题名/页数/SHA-256 核验 | 完成 |
| PMC 当前列出的 Data S1–S5 | 4 XLSX + 1 CSV；全部 sheets/行/CRC 核验 | 完成 |
| FLAb 10 CSV | 固定 commit、Git blob、SHA-256、表结构和一手附件关系核验 | 完成所选子集 |
| 19 个结构锚点 | 19 FASTA + 19 full mmCIF；canonical entity 配对通过 | 完成定义范围 |
| 仪器底层文件与未公开研究材料 | 正式公开包未提供 | 不在本快照承诺范围 |

## 待解决问题与处理进展

| 编号 | 问题 | 当前判断与影响 | 后续处理 |
| --- | --- | --- | --- |
| Q01 | 作者站 32 页 SI 首页笼统写 `Data S1 to S6` 和 `MDAR Checklist`，但同 PDF 的详细清单、PMC 23 页 supplement 及 PMC 关联文件都只列 Data S1–S5 | 当前公开交付只能确认 S1–S5；不把未识别对象写成已取得。该差异不阻止按“PMC 当前清单 + Zenodo + FLAb”定义的本地版本发布 | 若 Science/作者后续给出 Data S6 或 MDAR 的独立稳定入口，按新文件身份补建版本，不覆盖本版本 |
| Q02 | Data S1 的 IC50 列在不同病毒株间分别标 `ng/µL` 与 `µg/µL`，FLAb 又统一成 `ng/µL` | 单位仍不明确；保留字面表头，禁止未经确认的绝对浓度换算。相对 WT fold-change 可按一手表定义解释 | 需要作者或 publisher 更正说明；在此之前下游 schema 应带 `unit_unresolved=true` |
| Q03 | Science 图注称 55 个设计变体均可表达，而 Data S1 两个 SILM sheets 字面共有 56 条非 WT 设计记录（Round 1 为 40、Round 2 为 16） | 公开材料没有解释 1 条差异；行级分析以 Data S1 明示记录为准，不用正文总数覆盖表格 | 若需要复现论文“55”统计，需作者说明排除哪条设计及原因 |
