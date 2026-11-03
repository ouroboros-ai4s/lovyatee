# SRC_R30_HIE 数据说明

## 数据集身份

- `source_id`：`SRC_R30_HIE`
- `source_version`：`snapshot-2022-08-05`
- 原作者或发布机构：Brian L. Hie、Peter S. Kim 等；Stanford University / 合作者

## 实验设计和数据口径

一般蛋白语言模型提出少量氨基酸替换，研究先测第一轮单点变体，再组合替换开展第二轮，表达/纯化并用 BLI、neutralisation 与热稳定性测量验证。七条路线为 MEDI8852、MEDI8852 UCA、mAb114、mAb114 UCA、S309、REGN10987、C143，抗原株/构建体各异。论文共 122 个变体，除一个外可表达；不能把推荐的 742 个治疗抗体突变、DMS benchmark 或所有工作表行当这些测量对象。

成熟抗体多以 Fab KD 测量；UCA 和 C143 等表含 IgG apparent KD，进一步 Fab 验证是另一层。实际 XLSX 的 REGN10987/C143 标注 CoV2 Beta S2P，S309 标注 CoV-2 WT S6P；按原表区分，不用笼统 spike 标签合并。KD 单位 nM、小值有利；IC50 和 Tm 是其他 readout。NB / NB* 与无测量保留原义，不能设成零。工作表包含空白格式行、公式、合并单元格、重复对照与多抗原条件；max_row 不是样本数，缓存公式值可能缺失/过期。parent/UCA、轮次、HC/LC 和重复共享需分组。

## 论文原文

- 标题：Efficient evolution of human antibodies from general protein language models.
- 作者：Hie BL, Shanker VR, Xu D, Bruun TUJ, Weidenbacher PA, Tang S, Wu W, Pak JE, Kim PS.
- 载体与版本：Nat Biotechnol
- 发布日期：2023-04-24
- DOI：10.1038/s41587-023-01763-2
- PMID / PMCID：37095349 / PMC10869273
- 本地文件：`articles/HIE_2023-04-24_EuropePMC-published.xml`；`articles/HIE_2023-04-24_NatureBiotechnology-published.pdf`
- 文件大小：HIE_2023-04-24_EuropePMC-published.xml：241829 bytes；HIE_2023-04-24_NatureBiotechnology-published.pdf：13647540 bytes
- SHA-256：HIE_2023-04-24_EuropePMC-published.xml：`8bfc288361f4266ccd07e6dfe4a102cfa9f7047f121d4f7082461595cdfbb90d`；HIE_2023-04-24_NatureBiotechnology-published.pdf：`3ab0764eae92c20690f30694920b9833d115eba025803c036ed3ae84c6f02670`
- 文本许可：CC BY 4.0
- 补充材料：已归档 9 个文件。

| 本地文件 | 角色 | bytes | SHA-256 |
| --- | --- | --- | --- |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-1.pdf` | Supplementary Information Supplementary Tables 1–13 and Supplementary Information. | 511071 | `6ca32c5567b8b7c85111978547a0c31a45bde05105a74522f62c1bb5fdfc8861` |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-2.pdf` | Reporting Summary | 2168229 | `23712cd28b27c1a242241cd516d6a22b59830b36623e4b70215c776ebf265bc6` |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx` | Supplementary Data 1 Experimental  K d , IC 50  and  T m  values across seven antibody-directed evolution campaigns. | 303220 | `444d2c43333c5c545620e258ff15f8ca8d751d7116cf6e013e8b9db021966ca3` |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-4.xlsx` | Supplementary Data 2 MFI values for polyspecificity experiments and predicted MHC-binding peptides for immunogenicity experiments. | 29704 | `3335292d4346eb8b3cf558cbb855e12a2e674a9a075ce45e464a9d254a3a1cfe` |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-5.xlsx` | Supplementary Data 3 Benchmark results for comparison to other sequence-based methods. | 100110 | `de9b51faedcc6c5b06a753b50cc4d5e3e2b5550fb7ee6c65dc4eece621e4a8a9` |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-6.csv` | Supplementary Data 4 Language-model-recommended amino acid substitutions for 742 therapeutic antibodies. | 2324840 | `aa29a7e1d1ba1c0b80c2fb91af1d0cc14532ffb0ae45f4234bb7a44ac77b734f` |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-7.csv` | Supplementary Data 5 Mean rank values of 48 methods across DMS benchmarking experiments. | 879 | `7f7a1bfbd0d376ca2f13dd55fded9f2d72d924359e31c72fd194556096deee66` |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-8.xlsx` | Supplementary Data 6 List of oligonucleotide sequences used in this paper. | 18918 | `b48d68674a7652aa97f6905f91e9e8179b43330cea9470dbbbf5bd7f1b674016` |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-9.zip` | Supplementary Code Relevant code and scripts described in this paper. | 44784 | `a850bf7eb5075269b3e7497d5d792954a77b949ee7f10c3f3276aaa70bb4c493` |

## 仓库内容

- 一手入口：<https://zenodo.org/records/6968342>；record `6968342`；上游日期 2022-03-11。
- 一手入口：<https://github.com/brianhie/efficient-evolution>；commit `e9e8f610a5b4b3f48515741323209232faaf5039`，tree `70b5bd7934cf07c325c66a0d68fa6d481ced7028`；上游日期 2023-08-26。

Zenodo 全部公开数据 TAR、固定代码 tree、主文和全部可取得论文补充、可辩护亲本/靶点结构；按具体文件报告仍缺少的补充，不把未取得项写成完成。

上游未给整个数据交付包提供正式版本名；`snapshot-2022-08-05` 取自固定 Zenodo record 6968342 的 `created=2022-08-05T20:39:05.455219+00:00`，表示这条具体版本记录的创建日期。元数据 `publication_date=2022-03-11` 另行保留，不与该日期混用；不使用本次下载日期。 辅助 Git 包仍按下列独立 commit 固定。原交付归档保持压缩格式，验收时读取所有成员，不在 raw 中重新生成数据表。

```text
snapshot-2022-08-05/
  efficient-evolution/
    data.tar.gz
    efficient-evolution-e9e8f610a5b4b3f48515741323209232faaf5039.tar.gz
```

Git 快照全部 blob 与固定 commit tree 校验；e9e8f610a5b4b3f48515741323209232faaf5039：43 个 blob，LFS 0，submodule 0。

## 数据结构

### 原始交付与记录粒度

Zenodo data.tar.gz 为作者公共输入数据；固定 efficient-evolution Git 包为代码快照。Supplementary Data 1 XLSX 含七条路线的两轮测量和 thermal melt；另外有 polyspecificity、benchmark、742 抗体模型推荐、48 方法 mean rank、oligo 和代码。Supplementary Data 1 的 MEDI parent 文本拼为 MEDI8825，而 HC 等为 MEDI8852，原样保留并提示可能上游拼写错误，不自行改 raw。 实测 Zenodo 内 kd_binding.xlsx 与 publisher Supplementary Data 1 不同：C143 Round beta 分别 30/31 条非空行（含表头），不能盲目把两个交付当完全相同副本。data.tar 内还含 DMS benchmark、Thera-SAbDab 的742个条目、IMGT VDJ 无表头 TSV、Abysis 统计和 UniRef 派生的局部序列/MSA；不等于完整 UniRef 库。无表头 VDJ 的审计列名仅作 parser 说明。

| 原始表或 sheet | 非空数据行 | 列数 |
| --- | --- | --- |
| `efficient-evolution/data.tar.gz!data/dms/dms_pafa.csv` | 10013 | 4 |
| `efficient-evolution/data.tar.gz!data/dms/dms_p53.csv` | 7467 | 50 |
| `efficient-evolution/data.tar.gz!data/dms/dms_bla.csv` | 5434 | 27 |
| `efficient-evolution/data.tar.gz!data/dms/dms_mapk1.csv` | 6840 | 50 |
| `efficient-evolution/data.tar.gz!data/dms/dms_ha_h1.csv` | 10735 | 17 |
| `efficient-evolution/data.tar.gz!data/dms/dms_adrb2.csv` | 7847 | 51 |
| `efficient-evolution/data.tar.gz!data/dms/dms_env.csv` | 16359 | 17 |
| `efficient-evolution/data.tar.gz!data/dms/dms_infa.csv` | 1368 | 18 |
| `efficient-evolution/data.tar.gz!data/dms/dms_ha_h3.csv` | 10754 | 17 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#Contents` | 16 | 2 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#MEDI Round alpha` | 49 | 15 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#MEDI Round beta` | 19 | 26 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#MEDI UCA Round alpha` | 9 | 26 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#MEDI UCA Round beta` | 41 | 17 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#S309 Round alpha` | 11 | 19 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#S309 Round beta` | 30 | 17 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#mAb114 Round alpha` | 14 | 19 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#mAb114 Round beta` | 15 | 18 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#mAb114-UCA Round alpha` | 11 | 10 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#mAb114-UCA Round beta` | 14 | 9 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#REGN10987 Round alpha` | 17 | 11 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#REGN10987 Round beta` | 34 | 11 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#C143 Round alpha` | 16 | 9 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#C143 Round beta` | 29 | 11 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#Thermal melt data` | 38 | 9 |
| `efficient-evolution/data.tar.gz!data/pafa/abf8761_markin_data-s1.csv` | 1042 | 35 |
| `efficient-evolution/data.tar.gz!data/imgt/vdj_information.tsv` | 112657 | 4 |
| `efficient-evolution/data.tar.gz!data/thera-sabdab/TheraSAbDab_SeqStruc_OnlineDownload_2022-02-26.csv` | 742 | 23 |

### 论文交付数据表

以下是实际归档补充数据的原始工作表/CSV；工作表计数包括表头、注释与多段布局，不是独立样本数。公式保留原字符串，未重算；展示第一条非空原始行便于识别入口，标题行不能误作科学表头。

| 补充数据工作表 | 非空行（含表头/注释） | 首条原始行 / 公式单元格 / 特殊码 |
| --- | --- | --- |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx#Contents` | 17 | Supplementary Data 1: Experimental Kd, IC50, and Tm values across seven antibody evolution directed evolution campaigns. / 0 / {} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx#MEDI Round alpha` | 50 | Antigen, Chain mutated, Design, Kd rep1 (nM), Kd rep2 (nM), Kd avg (nM), Kd stdev (nM), Fold change, 1-sided t-test P / 114 / {'NB': 2} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx#MEDI Round beta` | 20 | Antigen, Chain mutated, Design, Kd rep1 (nM), Kd rep 2 (nM), Kd avg (nM), Kd stdev (nM), Fold change, 1-sided t-test P / 41 / {} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx#MEDI UCA Round alpha` | 10 | Antigen, Chain mutated, Design, IgG Kd rep1 (nM), IgG Kd rep2 (nM), IgG Kd avg (nM), IgG Kd stdev (nM), Fold change, 1-sided t-test P / 35 / {} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx#MEDI UCA Round beta` | 42 | Antigen, Chain mutated, Design, IgG Kd rep1 (nM), IgG Kd rep2 (nM), IgG Kd avg (nM), IgG Kd stdev (nM), Fold change, 1-sided t-test P / 143 / {} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx#S309 Round alpha` | 12 | Antigen, Chain mutated, Design, Kd rep1 (nM), Kd rep2 (nM), Kd rep3 (nM), Kd avg (nM), Kd stdev (nM), Fold Change, 1-sided t-test P / 39 / {'ND': 1} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx#S309 Round beta` | 31 | Antigen, Chain mutated, Design, Kd rep1 (nM), Kd rep2 (nM), Kd avg (nM), Kd stdev (nM), Fold Change, 1-sided t-test P / 91 / {} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx#mAb114 Round alpha` | 15 | Antigen, Chain mutated, Design, Kd rep1 (nM), Kd rep2 (nM), Kd rep3 (nM), Kd avg (nM), Kd stdev (nM), Fold Change, 1-sided t-test P / 55 / {} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx#mAb114 Round beta` | 16 | Antigen, Chain mutated, Design, Kd rep1 (nM), Kd rep2 (nM), Kd avg (nM), Kd stdev (nM), Fold Change, 1-sided t-test P / 54 / {'NA': 1} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx#mAb114-UCA Round alpha` | 12 | Antigen, Chain mutated, Design, IgG Kd rep1 (nM), IgG Kd rep2 (nM), IgG Kd avg (nM), IgG Kd stdev (nM), Fold Change, 1-sided t-test P / 31 / {'NB': 2, 'NB\*': 2} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx#mAb114-UCA Round beta` | 15 | Antigen, Chain mutated, Design, IgG Kd rep1 (nM), IgG Kd rep2 (nM), IgG Kd avg (nM), IgG Kd stdev (nM), Fold Change, 1-sided t-test P / 38 / {} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx#REGN10987 Round alpha` | 18 | Antigen, Chain mutated, Design, Kd rep1 (nM), Kd rep2 (nM), Kd rep3 (nM), Kd avg (nM), Kd stdev (nM), Fold Change, 1-sided t-test P / 36 / {} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx#REGN10987 Round beta` | 35 | Antigen, Chain mutated, Design, Kd rep1 (nM), Kd rep2 (nM), Kd rep3 (nM), Kd avg (nM), Kd stdev (nM), Fold Change, 1-sided t-test P / 104 / {'NA': 2} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx#C143 Round alpha` | 17 | Antigen, Chain mutated, Design, IgG Kd rep1 (nM), IgG Kd rep2 (nM), IgG Kd avg (nM), IgG Kd stdev (nM), Fold Change, 1-sided t-test P / 47 / {'NB\*': 6} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx#C143 Round beta` | 31 | Antigen, Chain mutated, Design, IgG Kd rep1 (nM), IgG Kd rep2 (nM), IgG Kd avg (nM), IgG Kd stdev (nM), Fold Change, 1-sided t-test P / 68 / {'NB\*': 4, 'NA': 2} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx#Thermal melt data` | 39 | Antibody, HC, LC, Design, Tm rep1, Tm rep 2, Tm rep3, Avg Tm, Error Tm / 76 / {} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-4.xlsx#Contents` | 4 | Supplementary Data 2: Median fluorescence intensity values for polyspecificity experiments and predicted MHC-binding peptides for immunogenicity experiments. / 0 / {} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-4.xlsx#Polyspecifity` | 97 | sample_name, Median APC-A / 0 / {} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-4.xlsx#Immunogenicity (MHC I)` | 39 | Antibody, MHC, Binding strength\*, Position, Peptide, Count, WT Binomial P / 0 / {} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-4.xlsx#Immunogenicity (MHC II)` | 39 | Antibody, MHC, Binding strength\*, Position, Peptide, Count, WT Binomial P / 0 / {} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-5.xlsx#Contents` | 7 | Supplementary Data 3: Benchmark results for comparison to other sequence-based methods. / 0 / {} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-5.xlsx#MEDI8852 UCA` | 45 | Method, Chain, Variant, IgG Kd rep 1 (nM), IgG Kd rep 2 (nM), IgG Kd mean (nM), IgG Kd error (nM), CV (%), Fold change, 1-sided t-test P / 139 / {'NB': 6, 'NB\*': 4} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-5.xlsx#mAb114 UCA` | 50 | Method, Chain, Variant, IgG Kd rep1 (nM), IgG Kd rep2 (nM), IgG Kd mean (nM), IgG Kd stdev (nM), CV (%), Fold change, 1-sided t-test P / 94 / {'NB\*': 6, 'NB': 4} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-5.xlsx#C143` | 76 | Method, Chain, Variant, IgG Kd rep1 (nM), IgG Kd rep2 (nM), IgG Kd mean (nM), IgG Kd stdev (nM), CV (%), Fold change, 1-sided t-test P / 132 / {'NB\*': 5, 'NB': 12} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-5.xlsx#UniRef90 sweep` | 64 | Antibody, Alignment depth, Number of known improvements, Mutations / 0 / {} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-5.xlsx#ESM-1b, UniRef50 alone` | 103 | MEDI8852 VH / 0 / {} |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-8.xlsx#Sheet1` | 178 | Supplementary Data 6: Oligonucleotides used in this study / 0 / {} |

| 补充数据表 | parser 行数 | 首行原始内容（须按具体布局读） |
| --- | --- | --- |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-6.csv` | 17168 | Therapeutic, Variable Sequence, Recommended Mutation, Number of Language Models |
| `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-7.csv` | 48 | model, mean_rank |

表行数包含重复条件、示例和派生副本，不求和作为独立生物对象。下表列名保持原始拼写；空表头以 `（空列名）` 标出，未修改文件。

### 字段说明

Antigen/Chain mutated/Design：实验组和突变名称（不总为全长序列）；`Kd rep1 (nM)` 等 / `IgG Kd rep1 (nM)` 等：重复浓度值，后者含 avidity；Kd avg/stdev/Fold change/P：作者公式/统计派生；`NB`/`NB*`：无结合/作者脚注特殊码，不可当数值；IC50：功能抑制值；Tm：°C；模型推荐 substitution/mean rank：预测或评测，不是实测 KD；空 Antigen/Chain mutated 单元格可能是排版，不自动视为未知靶点或独立样本。

| 原始表或 sheet | 字段（原始顺序） | 原始表示与特殊值 |
| --- | --- | --- |
| `efficient-evolution/data.tar.gz!data/dms/dms_pafa.csv` | `variant`, `DMS_kcat`, `DMS_km`, `DMS_kcat_km` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：DMS_kcat=8997, DMS_km=8997, DMS_kcat_km=8973 |
| `efficient-evolution/data.tar.gz!data/dms/dms_p53.csv` | `variant`, `PROVEAN`, `PPH2_HumVar`, `PPH2_HumDiv`, `Grantham`, `BLOSUM62`, `PhD_SNP`, `PANTHER`, `SNPs&GO`, `FATHMM`, `PonP2`, `SNAP2`, `PonPS`, `NetDiseaseSNP`, `M-CAP`, `PAPI`, `GERP++`, `SiPhy`, `VEST4`, `FathmmXF`, `DEOGEN2`, `CONDEL`, `DeepSequence`, `REVEL`, `S3D-PROF 6GGC B`, `SNP&GOs3D 6GGC B`, `SuSPect`, `SIFT`, `Envision`, `SIFT4G`, `LRT`, `MutationTaster`, `MetaSVM`, `MetaLR`, `MutPred`, `MVP`, `MPC`, `PrimateAI`, `MutationAssessor`, `CADD`, `DANN`, `fathmm-MKL`, `Eigen-pred`, `GenoCanyon`, `fitCons`, `phyloP`, `phastCons`, `DMS_WT_Nutlin`, `DMS_null_Nutlin`, `DMS_null_etoposide` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：PANTHER=2185, M-CAP=5149, PAPI=6147, GERP++=6147, SiPhy=6160, FathmmXF=5147, CONDEL=5147, REVEL=5147, S3D-PROF 6GGC B=3800, SNP&GOs3D 6GGC B=3800, SIFT=1, SIFT4G=5147, LRT=5165, MutationTaster=6321, MetaSVM=5147, MetaLR=5147, MutPred=5193, MVP=5148, MPC=5153, PrimateAI=5381, MutationAssessor=5156, CADD=5147, DANN=5147, fathmm-MKL=5147, Eigen-pred=5147, GenoCanyon=5147, fitCons=5147, phyloP=5147, phastCons=5147, PonPS=41, DMS_WT_Nutlin=19, DMS_null_Nutlin=19, DMS_null_etoposide=19 |
| `efficient-evolution/data.tar.gz!data/dms/dms_bla.csv` | `variant`, `PROVEAN`, `PPH2_HumDiv`, `Grantham`, `BLOSUM62`, `PhD_SNP`, `SNPs&GO`, `DeepSequence`, `SNAP2`, `NetDiseaseSNP`, `SuSPect`, `S3D-PROF 1M40 A`, `SNP&GOs3D 1M40 A`, `SIFT`, `PANTHER`, `Envision`, `DMS_(a)`, `DMS_amp_0_(b)`, `DMS_amp_10_(b)`, `DMS_amp_39_(b)`, `DMS_amp_156_(b)`, `DMS_amp_625_(b)`, `DMS_amp_2500_(b)`, `DMS_cefo_0.2_(b)`, `DMS_M182T_(c)`, `DMS_WT_(c)`, `DMS_(d)` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：S3D-PROF 1M40 A=456, SNP&GOs3D 1M40 A=456, SIFT=1, PANTHER=5434, Envision=5434, DMS_amp_0_(b)=456, DMS_amp_10_(b)=570, DMS_amp_39_(b)=456, DMS_amp_156_(b)=456, DMS_amp_625_(b)=456, DMS_amp_2500_(b)=456, DMS_cefo_0.2_(b)=456, DMS_M182T_(c)=5237, DMS_WT_(c)=4444, DMS_(d)=437, DMS_(a)=5367 |
| `efficient-evolution/data.tar.gz!data/dms/dms_mapk1.csv` | `variant`, `PROVEAN`, `PPH2_HumVar`, `PPH2_HumDiv`, `Grantham`, `BLOSUM62`, `PhD_SNP`, `PANTHER`, `SNPs&GO`, `FATHMM`, `PonP2`, `SNAP2`, `VEST4`, `FathmmXF`, `PonPS`, `NetDiseaseSNP`, `M-CAP`, `PAPI`, `GERP++`, `SiPhy`, `DEOGEN2`, `CONDEL`, `DeepSequence`, `REVEL`, `S3D-PROF 4ZZN A`, `SNP&GOs3D 4ZZN A`, `SuSPect`, `SIFT`, `Envision`, `SIFT4G`, `LRT`, `MutationTaster`, `MetaSVM`, `MetaLR`, `MutPred`, `MVP`, `MPC`, `PrimateAI`, `MutationAssessor`, `CADD`, `DANN`, `fathmm-MKL`, `Eigen-pred`, `GenoCanyon`, `fitCons`, `phyloP`, `phastCons`, `DMS_DOX`, `DMS_SCH`, `DMS_VRT` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：FathmmXF=4679, M-CAP=4679, PAPI=4678, GERP++=4678, SiPhy=4678, CONDEL=4677, REVEL=4678, S3D-PROF 4ZZN A=437, SNP&GOs3D 4ZZN A=437, SIFT=1, SIFT4G=4677, LRT=4677, MutationTaster=4677, MetaSVM=4677, MetaLR=4677, MutPred=4688, MVP=4677, MPC=4683, PrimateAI=4683, MutationAssessor=4683, CADD=4677, DANN=4677, fathmm-MKL=4677, Eigen-pred=4677, GenoCanyon=4677, fitCons=4677, phyloP=4677, phastCons=4677, DMS_DOX=30, DMS_SCH=30, DMS_VRT=30, PonP2=114, PonPS=114, PANTHER=2299 |
| `efficient-evolution/data.tar.gz!data/dms/dms_ha_h1.csv` | `variant`, `PROVEAN`, `PPH2_HumDiv`, `Grantham`, `BLOSUM62`, `PhD_SNP`, `PANTHER`, `SNPs&GO`, `SNAP2`, `NetDiseaseSNP`, `SuSPect`, `DeepSequence`, `SIFT`, `S3D-PROF`, `SNP&GOs3D`, `Envision`, `DMS` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：PANTHER=10735, SIFT=1, S3D-PROF=10735, SNP&GOs3D=10735, Envision=10735, DMS=19, DeepSequence=152 |
| `efficient-evolution/data.tar.gz!data/dms/dms_adrb2.csv` | `variant`, `PROVEAN`, `PPH2_HumVar`, `PPH2_HumDiv`, `Grantham`, `BLOSUM62`, `PhD_SNP`, `PANTHER`, `SNPs&GO`, `FATHMM`, `PonP2`, `SNAP2`, `VEST4`, `FathmmXF`, `SuSPect`, `PonPS`, `NetDiseaseSNP`, `M-CAP`, `DEOGEN2`, `CONDEL`, `PAPI`, `GERP++`, `SiPhy`, `DeepSequence`, `REVEL`, `S3D-PROF 2RH1 A`, `SNP&GOs3D 2RH1 A`, `SIFT`, `Envision`, `SIFT4G`, `LRT`, `MutationTaster`, `MetaSVM`, `MetaLR`, `MutPred`, `MVP`, `MPC`, `PrimateAI`, `MutationAssessor`, `CADD`, `DANN`, `fathmm-MKL`, `Eigen-pred`, `GenoCanyon`, `fitCons`, `phyloP`, `phastCons`, `DMS_0`, `DMS_0.15`, `DMS_0.625`, `DMS_5` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：PANTHER=1007, FathmmXF=5388, M-CAP=5392, CONDEL=5388, PAPI=5388, GERP++=5388, SiPhy=5388, REVEL=5388, S3D-PROF 2RH1 A=2527, SNP&GOs3D 2RH1 A=2527, SIFT=1, SIFT4G=5388, LRT=5388, MutationTaster=5388, MetaSVM=5388, MetaLR=5388, MutPred=5428, MVP=5390, MPC=5394, PrimateAI=5394, MutationAssessor=5394, CADD=5388, DANN=5388, fathmm-MKL=5388, Eigen-pred=5388, GenoCanyon=5388, fitCons=5388, phyloP=5388, phastCons=5388, DMS_0=47, DMS_0.15=47, DMS_0.625=47, DMS_5=35, PonPS=2 |
| `efficient-evolution/data.tar.gz!data/dms/dms_env.csv` | `variant`, `PROVEAN`, `PPH2_HumDiv`, `Grantham`, `BLOSUM62`, `PhD_SNP`, `PANTHER`, `SNPs&GO`, `SNAP2`, `NetDiseaseSNP`, `SuSPect`, `DeepSequence`, `S3D-PROF 3VTP C`, `SNP&GOs3D 3VTP C`, `SIFT`, `Envision`, `DMS` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：PANTHER=16359, S3D-PROF 3VTP C=15580, SNP&GOs3D 3VTP C=15580, SIFT=1, Envision=16359, DMS=3496 |
| `efficient-evolution/data.tar.gz!data/dms/dms_infa.csv` | `variant`, `PROVEAN`, `PPH2_HumDiv`, `Grantham`, `BLOSUM62`, `PhD_SNP`, `PANTHER`, `SNPs&GO`, `SNAP2`, `NetDiseaseSNP`, `SuSPect`, `DeepSequence`, `SIFT`, `Envision`, `S3D-PROF`, `SNP&GOs3D`, `DMS_min`, `DMS_rich` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：PANTHER=1368, SIFT=1, Envision=1368, S3D-PROF=1368, SNP&GOs3D=1368 |
| `efficient-evolution/data.tar.gz!data/dms/dms_ha_h3.csv` | `variant`, `PROVEAN`, `PPH2_HumDiv`, `Grantham`, `BLOSUM62`, `PhD_SNP`, `PANTHER`, `SNPs&GO`, `SNAP2`, `SuSPect`, `NetDiseaseSNP`, `DeepSequence`, `SIFT`, `S3D-PROF`, `SNP&GOs3D`, `Envision`, `DMS` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：PPH2_HumDiv=10754, PANTHER=10754, SIFT=1, S3D-PROF=10754, SNP&GOs3D=10754, Envision=10754 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#Contents` | `Supplementary Data 1: Experimental Kd, IC50, and Tm values across seven antibody evolution directed evolution campaigns.`, `（空列名）` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#MEDI Round alpha` | `Antigen`, `Chain mutated`, `Design`, `Kd rep1 (nM)`, `Kd rep2 (nM)`, `Kd avg (nM)`, `Kd stdev (nM)`, `Fold change`, `t-test P`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：Chain mutated=26, t-test P=22, （空列名）=294, Antigen=37, Kd rep1 (nM)=20, Kd rep2 (nM)=20, Kd avg (nM)=1, Kd stdev (nM)=10, Fold change=20 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#MEDI Round beta` | `Antigen`, `Chain mutated`, `Design`, `Kd rep1 (nM)`, `Kd rep 2 (nM)`, `Kd avg (nM)`, `Kd stdev (nM)`, `Fold change`, `t-test P`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：Chain mutated=3, t-test P=16, （空列名）=323, Antigen=13, Kd avg (nM)=13, Kd stdev (nM)=13, Fold change=13, Kd rep 2 (nM)=2 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#MEDI UCA Round alpha` | `Antigen`, `Chain mutated`, `Design`, `IgG Kd rep1 (nM)`, `IgG Kd rep2 (nM)`, `IgG Kd avg (nM)`, `IgG Kd stdev (nM)`, `Fold change`, `t-test P`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：Chain mutated=7, t-test P=1, （空列名）=153, Antigen=8 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#MEDI UCA Round beta` | `Antigen`, `Chain mutated`, `Design`, `IgG Kd rep1 (nM)`, `IgG Kd rep2 (nM)`, `IgG Kd avg (nM)`, `IgG Kd stdev (nM)`, `Fold change`, `t-test P`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：Chain mutated=28, t-test P=18, （空列名）=328, Antigen=34 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#S309 Round alpha` | `Antigen`, `Chain mutated`, `Design`, `Kd rep1 (nM)`, `Kd rep2 (nM)`, `Kd rep3 (nM)`, `Kd avg (nM)`, `Kd stdev (nM)`, `Fold Change`, `t-test P`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：Chain mutated=9, t-test P=2, （空列名）=99, Antigen=10, Kd rep1 (nM)=1 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#S309 Round beta` | `Antigen`, `Chain mutated`, `Design`, `Kd rep1 (nM)`, `Kd rep2 (nM)`, `Kd avg (nM)`, `Kd stdev (nM)`, `Fold Change`, `t-test P`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：Chain mutated=7, t-test P=21, （空列名）=240, Antigen=21, Kd avg (nM)=8, Kd stdev (nM)=8, Fold Change=8, Kd rep2 (nM)=1 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#mAb114 Round alpha` | `Antigen`, `Chain mutated`, `Design`, `Kd rep1 (nM)`, `Kd rep2 (nM)`, `Kd rep3 (nM)`, `Kd avg (nM)`, `Kd stdev (nM)`, `Fold Change`, `t-test P`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：Chain mutated=12, t-test P=1, （空列名）=126, Antigen=13 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#mAb114 Round beta` | `Antigen`, `Chain mutated`, `Design`, `Kd rep1 (nM)`, `Kd rep2 (nM)`, `Kd avg (nM)`, `Kd stdev (nM)`, `Fold Change`, `t-test P`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）`, `（空列名）` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：Chain mutated=10, t-test P=1, （空列名）=120, Antigen=12 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#mAb114-UCA Round alpha` | `Antigen`, `Chain mutated`, `Design`, `IgG Kd rep1 (nM)`, `IgG Kd rep2 (nM)`, `IgG Kd avg (nM)`, `IgG Kd stdev (nM)`, `Fold Change`, `t-test P`, `（空列名）` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：Chain mutated=9, t-test P=4, （空列名）=11, Antigen=9, IgG Kd avg (nM)=3, IgG Kd stdev (nM)=3, Fold Change=3, Design=1, IgG Kd rep1 (nM)=1, IgG Kd rep2 (nM)=1 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#mAb114-UCA Round beta` | `Antigen`, `Chain mutated`, `Design`, `IgG Kd rep1 (nM)`, `IgG Kd rep2 (nM)`, `IgG Kd avg (nM)`, `IgG Kd stdev (nM)`, `Fold Change`, `t-test P` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：Chain mutated=7, t-test P=7, Antigen=10, Design=1, IgG Kd rep1 (nM)=1, IgG Kd rep2 (nM)=2, IgG Kd avg (nM)=6, IgG Kd stdev (nM)=6, Fold Change=6 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#REGN10987 Round alpha` | `Antigen`, `Chain mutated`, `Design`, `Kd rep1 (nM)`, `Kd rep2 (nM)`, `Kd rep3 (nM)`, `Kd avg (nM)`, `Kd stdev (nM)`, `Fold Change`, `t-test P`, `（空列名）` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：Chain mutated=12, t-test P=11, （空列名）=17, Antigen=14, Kd rep3 (nM)=10, Kd avg (nM)=10, Kd stdev (nM)=10, Fold Change=10 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#REGN10987 Round beta` | `Antigen`, `Chain mutated`, `Design`, `Kd rep1 (nM)`, `Kd rep2 (nM)`, `Kd rep3 (nM)`, `Kd avg (nM)`, `Kd stdev (nM)`, `Fold Change`, `t-test P`, `（空列名）` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：Chain mutated=13, t-test P=16, （空列名）=24, Antigen=25, Fold Change=7, Kd rep3 (nM)=6, Kd avg (nM)=6, Kd stdev (nM)=6, Kd rep2 (nM)=1 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#C143 Round alpha` | `Antigen`, `Chain mutated`, `Design`, `IgG Kd rep1 (nM)`, `IgG Kd rep2 (nM)`, `IgG Kd avg (nM)`, `IgG Kd stdev (nM)`, `Fold Change`, `t-test P` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：Chain mutated=14, t-test P=5, Antigen=14, IgG Kd avg (nM)=4, IgG Kd stdev (nM)=4, Fold Change=4, Design=1, IgG Kd rep1 (nM)=1, IgG Kd rep2 (nM)=1 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#C143 Round beta` | `Antigen`, `Chain mutated`, `Design`, `IgG Kd rep1 (nM)`, `IgG Kd rep2 (nM)`, `IgG Kd avg (nM)`, `IgG Kd stdev (nM)`, `Fold Change`, `t-test P`, `（空列名）`, `（空列名）` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：Chain mutated=11, t-test P=15, （空列名）=40, Antigen=19, IgG Kd avg (nM)=14, IgG Kd stdev (nM)=14, Fold Change=14, Design=1, IgG Kd rep1 (nM)=1, IgG Kd rep2 (nM)=3 |
| `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#Thermal melt data` | `Antibody`, `HC`, `LC`, `Design`, `Tm rep1`, `Tm rep 2`, `Tm rep3`, `Avg Tm`, `Error Tm` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `efficient-evolution/data.tar.gz!data/pafa/abf8761_markin_data-s1.csv` | `variant`, `library`, `kcat_cMUP_s-1`, `kcat_cMUP_limit`, `kcat_cMUP_p-value`, `KM_cMUP_uM`, `KM_cMUP_limit`, `KM_cMUP_p-value`, `kcatOverKM_cMUP_M-1s-1`, `kcatOverKM_cMUP_limit`, `kcatOverKM_cMUP_p-value`, `kcatOverKM_MeP_M-1s-1`, `kcatOverKM_MeP_limit`, `kcatOverKM_MeP_p-value`, `kcatOverKM_MecMUP_M-1s-1`, `kcatOverKM_MecMUP_limit`, `kcatOverKM_MecMUP_p-value`, `Ki_Pi_uM`, `Ki_Pi_limit`, `Ki_Pi_p-value`, `fa`, `fa_limit`, `fa_p-value`, `kcatOverKM_MePkchem_M-1s-1`, `kcatOverKM_MePkchem_limit`, `kcatOverKM_MePkchem_p-value`, `FC1`, `FC1_limit`, `FC1_p-value`, `FC2/3`, `FC2/3_limit`, `FC2/3_p-value`, `FC4_s-1`, `FC4_limit`, `FC4_p-value` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：FC1=182, FC1_limit=186, FC1_p-value=181, Ki_Pi_uM=40, Ki_Pi_limit=41, Ki_Pi_p-value=40, FC2/3=40, FC2/3_limit=41, FC2/3_p-value=40, FC4_s-1=46, FC4_limit=45, FC4_p-value=43, kcat_cMUP_s-1=24, kcat_cMUP_limit=24, kcat_cMUP_p-value=24, KM_cMUP_uM=24, KM_cMUP_limit=24, KM_cMUP_p-value=24, fa=25, fa_limit=25, fa_p-value=25, kcatOverKM_MePkchem_M-1s-1=25, kcatOverKM_MePkchem_limit=25, kcatOverKM_MePkchem_p-value=25, kcatOverKM_MeP_M-1s-1=1, kcatOverKM_MeP_limit=1, kcatOverKM_MeP_p-value=1, kcatOverKM_MecMUP_M-1s-1=1, kcatOverKM_MecMUP_limit=1, kcatOverKM_MecMUP_p-value=1 |
| `efficient-evolution/data.tar.gz!data/imgt/vdj_information.tsv` | `segment_type`, `gene`, `allele`, `sequence` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：sequence=4 |
| `efficient-evolution/data.tar.gz!data/thera-sabdab/TheraSAbDab_SeqStruc_OnlineDownload_2022-02-26.csv` | `Therapeutic`, `Format`, `CH1 Isotype`, `VD LC`, `Highest_Clin_Trial (Oct '21)`, `Est. Status`, `Heavy Sequence`, `Light Sequence`, `Heavy Sequence (if bispec)`, `Light Sequence (if bispec)`, `100% SI Structure`, `99% SI Structure`, `95-98% SI Structure`, `Year Proposed`, `Year Recommended`, `Target`, `Companies`, `Conditions Approved`, `Conditions Active`, `Conditions Discontinued`, `Development Tech`, `Notes`, `（空列名）` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：100% SI Structure=535, 99% SI Structure=611, 95-98% SI Structure=619, Notes=676, （空列名）=742, Conditions Discontinued=2, CH1 Isotype=1 |

### 数据示例

来自 `efficient-evolution/data.tar.gz!data/binding/kd_binding.xlsx#MEDI Round alpha` 的第一条真实非空数据行：

| 原始字段 | 原始值 |
| --- | --- |
| Antigen | H4 Hubei |
| Chain mutated | （空单元格） |
| Design | MEDI8825 |
| Kd rep1 (nM) | 0.5371 |
| Kd rep2 (nM) | 0.7225 |
| Kd avg (nM) | =AVERAGE(D2:E2) |
| Kd stdev (nM) | =_xlfn.STDEV.P(D2:E2) |
| Fold change | =$D$2/D2 |
| t-test P | （空单元格） |
| （空列名） | （空单元格） |
| （空列名） | （空单元格） |
| （空列名） | （空单元格） |
| （空列名） | （空单元格） |
| （空列名） | （空单元格） |
| （空列名） | （空单元格） |

这是该原始表的一条记录；粒度按前述定义，不把结构表示、重复或归档成员当独立抗体。

## PDB 数据库

接受 5FHC（mAb114/100 与 Ebola GP）、5JW3/5JW4（MEDI8852 与 H7/H5 HA）、5JW5（MEDI8852 Fab）、6WPS（S309/spike）、6XDG（REGN10933/10987 与 RBD）为共享亲本/靶点参考。HA 和 spike 的参考株/构建体不等于所有测量条件，UCA 不等于成熟亲本；没有确认 C143 专属 PDB。先前候选 5HYI 实为 hole-hole Fc、7K8W 为 C119、7K8X 为 C121，官方身份核对后拒绝并清除本次 staging 副本。无逐新变体实验结构映射。

本次审计接受 6 个唯一锚点，每个都有 RCSB 完整 entry FASTA 与完整 mmCIF（原样 .cif 或 .cif.gz），共 12 个文件 / 4329250 bytes。逐对检查 entry ID、非空 _atom_site 及 canonical polymer 序列一致。FASTA 保留 RCSB entity ID、原始头和序列，没有从坐标重建序列；坐标保留完整原文件。author/label chain 与 entity 的原始映射在 FASTA 头及 mmCIF `_struct_asym`、`_entity_poly`、`_atom_site.auth_asym_id` 中，不臆造链角色。

文件路径为 `pdb/sequences/rcsb_pdb_<PDB>.fasta`、`pdb/structures/<PDB>.cif.gz` 或 `<PDB>.cif`；复用已有完整未压缩 RCSB 原文件时不重新压缩。确定性 inventory SHA-256：`caac27e1eb9a5614e1fe789cdbcde87fb8447faa077140c1efde7ec599914ccb`；算法为按相对路径排序，逐文件组成 `path<TAB>bytes<TAB>sha256<LF>`（UTF-8）再计算 SHA-256。

| PDB | FASTA bytes / SHA-256 | mmCIF.gz bytes / SHA-256 |
| --- | --- | --- |
| 5FHC | 1770 / `b66c5a03bd2a55c40fe9e83821d8acdecae37d1b21378cd54216485fe0b16763` | 491807 / `efe30a2f2cd8c3d195131db657543b9f05a292151ccec00e61840b72e95b7ad9` |
| 5JW3 | 1238 / `c895a7b714154a5b59c9ec1e997868498d3b00821860cb5431cacbcbd595a6cf` | 384486 / `8c1e6dfd04c0e53a03ba7e863f3d8230a9e4c72a4a60811dfdd8f7754895ad04` |
| 5JW4 | 1763 / `2ef5fba8903a475e3fb7987859408d6de602dc5b25ff7a3ac5a1727933c6ecdb` | 2137251 / `dd0b4dd91d8e856b86b6db29d1d73eb143ae4b8aaf9fac3eaf2374a7b609e875` |
| 5JW5 | 577 / `2ecf353df02accebdc49132f9ad2efa4b7f4ea6e389bcad696552e6b4869d5ba` | 365529 / `d7d401ffc6aeab980f24914aff78011d6944ccd2229b16f991717bab70330a96` |
| 6WPS | 1838 / `39148780a7f94d740dbd0d2456d6a4f75256f6f7f4974fda9f93f0bd1c8b4859` | 728037 / `c7e1ddd5e5d6b5f06e8e927d1735dabe16b125d787717f1293ab0da7b3e191a2` |
| 6XDG | 1588 / `c87eac3f50480b7943376eb2aa3d53e4230d07ab8485bbfda693ef0c02d279fc` | 213366 / `c8351f47f31c3bbcf0731a0219da0452d2ed86d9593e50a6e3ae525d95409734` |

## 使用方式

由调用者将 `dataset_root` 赋为该 source_version 目录。以下仅读原始入口，不清洗、换算或修补 raw。

```python
import tarfile
with tarfile.open(dataset_root / "efficient-evolution/data.tar.gz") as archive:
    print(archive.getnames()[:5])
```

## 采集过程记录

2026-09-18：取得 data.tar.gz、固定 efficient-evolution Git tree、主文 XML/PDF 与九份公开附件。核对两个来源 kd_binding 工作表不同、无表头 VDJ 首行与公式/特殊值；没有把 DMS/742 治疗抗体推荐当新实验变体。初选 5HYI、7K8W、7K8X 被官方分子身份否定，清除本次 staging 误选副本后保留六个有证据的亲本/靶点参考。

2026-09-18：全部正式 payload 按来源身份、大小和官方/本地 checksum 独立验收；原始表与附件已读取，FASTA 和完整 mmCIF 逐对核验。工作 README 同步共享版本，规定的 markdownlint 为零错误后发布。具体 API、原始下载日志、失败和重试记录保存在共享本批采集目录，未向任何作者发送消息或申请。

2026-09-18：复核 skill 版本规则，将不符合命名规则的 `zenodo-6968342` 原子重命名为 `snapshot-2022-08-05`。同步来源配置、PDB 配置、工作与共享 README 及当前结构化验收/发布记录；旧文档和原验收记录保留在 runs 的 version-migration-history。修订前后按相对路径、字节数和 SHA-256 比对全部科学文件，内容保持原样；修订 README 使用规定的 markdownlint 配置验收。

2026-09-18：README 工作稿迁入由 developer.user 定位的个人 docs/readme。初版采集记录混用了跨来源的通用描述，本次按实际来源、下载与重试记录修订。论文及附件命名补齐平台和版本。以下名称变更均核对原文件字节数及 SHA-256，内容未改写；原始文件名与下载 URL 保留在采集记录中。

- `articles/HIE_2023-04-24_EuropePMC.xml` → `articles/HIE_2023-04-24_EuropePMC-published.xml`；241829 bytes，SHA-256 `8bfc288361f4266ccd07e6dfe4a102cfa9f7047f121d4f7082461595cdfbb90d`。
- `articles/HIE_2023-04-24_publisher.pdf` → `articles/HIE_2023-04-24_NatureBiotechnology-published.pdf`；13647540 bytes，SHA-256 `3ab0764eae92c20690f30694920b9833d115eba025803c036ed3ae84c6f02670`。
- `articles/HIE_2023-04-24_supplement-1.pdf` → `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-1.pdf`；511071 bytes，SHA-256 `6ca32c5567b8b7c85111978547a0c31a45bde05105a74522f62c1bb5fdfc8861`。
- `articles/HIE_2023-04-24_supplement-2.pdf` → `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-2.pdf`；2168229 bytes，SHA-256 `23712cd28b27c1a242241cd516d6a22b59830b36623e4b70215c776ebf265bc6`。
- `articles/HIE_2023-04-24_supplement-3.xlsx` → `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-3.xlsx`；303220 bytes，SHA-256 `444d2c43333c5c545620e258ff15f8ca8d751d7116cf6e013e8b9db021966ca3`。
- `articles/HIE_2023-04-24_supplement-4.xlsx` → `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-4.xlsx`；29704 bytes，SHA-256 `3335292d4346eb8b3cf558cbb855e12a2e674a9a075ce45e464a9d254a3a1cfe`。
- `articles/HIE_2023-04-24_supplement-5.xlsx` → `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-5.xlsx`；100110 bytes，SHA-256 `de9b51faedcc6c5b06a753b50cc4d5e3e2b5550fb7ee6c65dc4eece621e4a8a9`。
- `articles/HIE_2023-04-24_supplement-6.csv` → `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-6.csv`；2324840 bytes，SHA-256 `aa29a7e1d1ba1c0b80c2fb91af1d0cc14532ffb0ae45f4234bb7a44ac77b734f`。
- `articles/HIE_2023-04-24_supplement-7.csv` → `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-7.csv`；879 bytes，SHA-256 `7f7a1bfbd0d376ca2f13dd55fded9f2d72d924359e31c72fd194556096deee66`。
- `articles/HIE_2023-04-24_supplement-8.xlsx` → `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-8.xlsx`；18918 bytes，SHA-256 `b48d68674a7652aa97f6905f91e9e8179b43330cea9470dbbbf5bd7f1b674016`。
- `articles/HIE_2023-04-24_supplement-9.zip` → `articles/HIE_2023-04-24_NatureBiotechnology-published-supplement-9.zip`；44784 bytes，SHA-256 `a850bf7eb5075269b3e7497d5d792954a77b949ee7f10c3f3276aaa70bb4c493`。

旧文档和结构化报告保存在共享 runs/documentation-reorganization；修订后本地与共享 README 同步并执行规定的 Markdownlint。

- 上游原始名称 `fullTextXML`；入口 <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10869273/fullTextXML>。
- 上游原始名称 `s41587-023-01763-2.pdf`；入口 <https://www.nature.com/articles/s41587-023-01763-2.pdf>。
- 上游原始名称 `41587_2023_1763_MOESM1_ESM.pdf`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM1_ESM.pdf>。
- 上游原始名称 `41587_2023_1763_MOESM2_ESM.pdf`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM2_ESM.pdf>。
- 上游原始名称 `41587_2023_1763_MOESM3_ESM.xlsx`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM3_ESM.xlsx>。
- 上游原始名称 `41587_2023_1763_MOESM4_ESM.xlsx`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM4_ESM.xlsx>。
- 上游原始名称 `41587_2023_1763_MOESM5_ESM.xlsx`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM5_ESM.xlsx>。
- 上游原始名称 `41587_2023_1763_MOESM6_ESM.csv`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM6_ESM.csv>。
- 上游原始名称 `41587_2023_1763_MOESM7_ESM.csv`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM7_ESM.csv>。
- 上游原始名称 `41587_2023_1763_MOESM8_ESM.xlsx`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM8_ESM.xlsx>。
- 上游原始名称 `41587_2023_1763_MOESM9_ESM.zip`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM9_ESM.zip>。

## 参考文献

- [数据源固定版本/入口](https://zenodo.org/records/6968342)
- [数据源固定版本/入口](https://github.com/brianhie/efficient-evolution)
- [归档主文 DOI](https://doi.org/10.1038/s41587-023-01763-2)
- [primary full-text XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10869273/fullTextXML)
- [primary PDF](https://www.nature.com/articles/s41587-023-01763-2.pdf)
- [Supplementary Information Supplementary Tables 1–13 and Supplementary Information.](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM1_ESM.pdf)
- [Reporting Summary](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM2_ESM.pdf)
- [Supplementary Data 1 Experimental  K d , IC 50  and  T m  values across seven antibody-directed evolution campaigns.](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM3_ESM.xlsx)
- [Supplementary Data 2 MFI values for polyspecificity experiments and predicted MHC-binding peptides for immunogenicity experiments.](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM4_ESM.xlsx)
- [Supplementary Data 3 Benchmark results for comparison to other sequence-based methods.](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM5_ESM.xlsx)
- [Supplementary Data 4 Language-model-recommended amino acid substitutions for 742 therapeutic antibodies.](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM6_ESM.csv)
- [Supplementary Data 5 Mean rank values of 48 methods across DMS benchmarking experiments.](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM7_ESM.csv)
- [Supplementary Data 6 List of oligonucleotide sequences used in this paper.](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM8_ESM.xlsx)
- [Supplementary Code Relevant code and scripts described in this paper.](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41587-023-01763-2/MediaObjects/41587_2023_1763_MOESM9_ESM.zip)
- [PDB 5FHC（条目含原始结构论文）](https://www.rcsb.org/structure/5FHC)
- [PDB 5JW3（条目含原始结构论文）](https://www.rcsb.org/structure/5JW3)
- [PDB 5JW4（条目含原始结构论文）](https://www.rcsb.org/structure/5JW4)
- [PDB 5JW5（条目含原始结构论文）](https://www.rcsb.org/structure/5JW5)
- [PDB 6WPS（条目含原始结构论文）](https://www.rcsb.org/structure/6WPS)
- [PDB 6XDG（条目含原始结构论文）](https://www.rcsb.org/structure/6XDG)

## 其他

### 完整性与验收

| payload | bytes | SHA-256 |
| --- | --- | --- |
| `efficient-evolution/data.tar.gz` | 12247531 | `eee886b07064474d39ac072152997734b60ffbdb0e9644cb1ccf74abac20f6c7` |
| `efficient-evolution/efficient-evolution-e9e8f610a5b4b3f48515741323209232faaf5039.tar.gz` | 25068 | `69553363155df1c39c7fa6f7eba038c52fa8112408449eb7a757855554fbc6ce` |

原始 payload 合计 12272599 bytes；inventory SHA-256 `54c85e9d2777c98ce15f4d8314e2a3e09dcbebeab2c5d231bf450ffc7b0ed56e`（与 PDB 同一算法）。归档成员全部读取；统计与 API/验收报告保存于共享 runs，不作为 raw 附属 manifest 发布。每个文件与论文/PDB 身份均可重验，不执行交付包中的训练代码或模型反序列化。

### 许可和再分发边界

Zenodo 元数据 cc-nc（非商业），代码 Git MIT，论文/其公开补充 CC BY 4.0；不同层不能互相覆盖。Zenodo 说明不包含 UniRef 数据，未声称取得完整语言模型预训练数据。

### 公开范围对照

| 范围 | 本次证据与状态 |
| --- | --- |
| 已取得的公开部分 | Zenodo 全部公开数据 TAR、固定代码 tree、主文和全部可取得论文补充、可辩护亲本/靶点结构；按具体文件报告仍缺少的补充，不把未取得项写成完成。 |
| 论文/来源未公开或未取得部分 | 仅按本文具体缺口报告；未访问限制不冒称完成。 |
| processed / release | 未生成；本层仅上游原样输入。 |
