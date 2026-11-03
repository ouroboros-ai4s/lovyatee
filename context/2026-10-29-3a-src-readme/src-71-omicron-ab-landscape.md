# SRC_R71_OMICRON_AB_LANDSCAPE 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
  - [兄弟交付 Tite-Seq 流程仓库](#兄弟交付-tite-seq-流程仓库)
- [数据结构](#数据结构)
  - [原始测序 reads（sra/）](#原始测序-readssra)
  - [亲和力表的列结构与记录关系](#亲和力表的列结构与记录关系)
  - [分析产物](#分析产物)
  - [兄弟交付的元数据表](#兄弟交付的元数据表)
  - [字段说明](#字段说明)
  - [数据示例](#数据示例)
- [PDB 数据库](#pdb-数据库)
- [采集过程记录](#采集过程记录)
- [参考文献](#参考文献)
- [其他](#其他)
  - [数据范围和限制](#数据范围和限制)
  - [完整性与验收](#完整性与验收)
  - [许可和再分发边界](#许可和再分发边界)
  - [公开范围对照](#公开范围对照)
- [待解决问题与处理进展](#待解决问题与处理进展)

## 数据集身份

- `source_id`：`SRC_R71_OMICRON_AB_LANDSCAPE`
- `source_version`：`snapshot-2023-11-10`
- 原作者或发布机构：哈佛大学有机体与进化生物学系 Desai 实验室（第一作者 Alief Moulana；通讯作者 Angela M. Phillips、Michael M. Desai）

### 来源方背景

Michael M. Desai 在[实验室成员页](https://www.desai-lab.com/people/)上的职务为“Professor of Organismic and Evolutionary Biology and of Physics”，隶属哈佛大学有机体与进化生物学系与物理系，同时关联 FAS Center for Systems Biology；论文作者单位另列出 NSF-Simons Center for Mathematical and Statistical Analysis of Biology 与 Quantitative Biology Initiative。实验室[研究方向页](https://www.desai-lab.com/research/) 把“Binding landscapes for immune-pathogen coevolutionary dynamics”列为独立方向，说明其研究抗体与 T 细胞受体同相关抗原的结合亲和力表型，并自述开发了“methods such as Tite-Seq to dramatically increase the throughput of phenotypic measurements”，与本 source 所用的测量方法直接对应。

本论文九位作者中，Alief Moulana 与 Alex Poret 等同组成员在成员页上列为哈佛大学有机体与进化生物学系研究生（Moulana 为本 source 第一作者）；Angela M. Phillips 与 Thomas Dupic 已分别转任 University of California, San Francisco 助理教授与 Centre d'Immunologie de Marseille-Luminy 团队负责人。论文另一部分作者（Allison J. Greaney、Tyler N. Starr、Jesse D. Bloom）隶属 Fred Hutchinson Cancer Center 基础科学与计算生物学部、华盛顿大学基因组科学系与 Howard Hughes Medical Institute，作者单位以论文自身所列机构为准。仓库由 GitHub 组织 `desai-lab` 维护。

## 实验设计和数据口径

本 source 测量的是**抗原变体侧**的景观：把 SARS-CoV-2 Omicron BA.1 相对武汉 Hu-1 的 15 个 RBD 氨基酸替换做全组合，得到 `2^15 = 32,768` 个基因型，再用 Tite-Seq 测每个基因型对四个治疗性抗体的表观解离常数。四个抗体为 LY-CoV016（CB6）、LY-CoV555、 REGN10987 与 S309，另有受体 ACE2。抗体侧固定，不是在同一抗原下比较不同抗体序列的排序数据。

实验对象是展示 RBD 的酵母库。论文 Methods 记录：每个抗体在两个不同日期各做一次 biological replicate，共八个 assay；每个浓度分选约 1.2 百万个细胞，按前向/侧向散射、表达荧光（FITC，anti-cMyc）与结合荧光（PE，anti-human IgG）门选，随后建库并在 Illumina NovaSeq SP 上测序（加 10% PhiX）。各抗体的抗体浓度区间不同：

| assay | 抗体浓度区间（论文 Methods） |
| --- | --- |
| LY-CoV016（CB6） | 10⁻⁶ 至 10⁻¹² M，0.75-log 递增 |
| LY-CoV555 | 10⁻⁶ 至 10⁻¹² M，0.75-log 递增 |
| REGN10987 | 10⁻⁶ 至 10⁻¹²·⁷ M，0.75-log 递增 |
| S309 | 10⁻⁷ 至 10⁻¹² M，0.5-log 递增 |

**基因型编码**：`geno` 是 15 位二进制字符串，第 k 位对应词典中的第 k 个位点， `'0'` 为该位点的武汉 Hu-1 等位，`'1'` 为 Omicron BA.1 等位。位置与替换的对应为

```text
1 G339D   2 S371L   3 S373P   4 S375F   5 K417N   6 N440K   7 G446S   8 S477N
9 T478K  10 E484A  11 Q493R  12 G496S  13 Q498R  14 N501Y  15 Y505H
```

全零基因型 `000000000000000` 即武汉 Hu-1 RBD，全一基因型 `111111111111111` 即 BA.1 RBD。

**数值来源**：公开数值不是逐事件流式数据，也不是原始测序计数，而是拟合结果。论文 Methods 描述的处理链为：由各 bin 的读数比例与分选细胞数估计某基因型在某浓度的平均对数荧光，再以 Hill 函数拟合 `log10` 形式的浓度依赖曲线，得到 `A`（饱和时荧光增量）、 `B`（背景荧光）与 `K_D,app`；拟合的 `curve_fit` 边界为 `A` 10²–10⁶、`B` 1–10⁵、 `K_D` 10⁻¹⁴–10⁻⁵ M。两个 replicate 的拟合在剔除 `r² < 0.8` 或 `SE > 1` 的值后取平均。 **非结合型**由荧光判据定义：某基因型在全部浓度上的最大与最小估计对数荧光之差小于 1（对数荧光单位）即判为非结合型，该阈值由已知非结合型的分布确定。

公开的 `cleaned_Kds_RBD_*` 表是上述拟合的**逐基因型汇总**，每个抗体一张，各含全部 32,768 个基因型（唯一基因型数与行数一致）。表中的 `log10Kd` 按 `-log10(K_D,app [M])` 解读，数值越大亲和力越强；本次发布的表中该列与 `log10Kd_pinned` 逐行完全相同。非结合型在论文作图时被设定为 5.0 以便绘图，这一替换发生在 `Omicron_ab_Landscape.Rmd` 内，不写回发布表：发布表保留上游原值（非结合型多为空值，但也有带值的行），不把缺失写成零或边界值。

复制号的字母后缀按 assay 区分（CB6 为 `i`/`j`，LY-CoV555 为 `e`/`v`，REGN10987 为 `g`/`h`，S309 为 `c`/`d`，ACE2 为 `a`/`b`/`x`）。这一对应由兄弟交付中的 `Titeseq/metadata/replicate_info_RBD.tsv` 直接给出（四个抗体各两次实验，ACE2 三次）， ENA 的实验标题（如 `omicron-ab replicate e concentration 6 bin 2`）与之相互印证。

本 source 的产物不止亲和力表。仓库用 `Omicron_ab_Landscape.Rmd` 从五张表生成论文图；`Analyze/` 下的 notebook 与 `data/` 下的系数文件承载上位性（Tobit / lasso）推断、结构注释与系统发生分析。这些是**派生结果**：`*_prediction_*` 文件给出模型对每个基因型的预测值，`*_version_*` 与 `Analyze/Structure/*` 给出模型系数，两者都用于论文的图，不是新的实验测量。`data/CV_rsquared.csv` 是各抗体、各阶数模型的交叉验证 `R²`；`data/fig4_phylogeny.csv` 是 15 个替换的效应与 GISAID 系统发生频率的对照表。

ACE2 表与其他四张不同：文件名带 `low_filter`，含三个复制号区块而非两个，且没有 `is_non_binder` / `is_clean` 等 QC 列。`Omicron_ab_Landscape.Rmd` 对 ACE2 直接赋值 `is_non_binder = FALSE`、`is_clean = TRUE`，即不施加该 QC 判据。三者都是 **三次实验**（`a` 2022-02-22、`b` 2022-03-03、`x` 2022-04-14），`low_filter` 指合并前不剔除 `SE > 1` 的拟合，逐 replicate 的核对证据见“数据结构/兄弟交付的元数据表”。

## 论文原文

- 标题：*The landscape of antibody binding affinity in SARS-CoV-2 Omicron BA.1 evolution*
- 作者：Alief Moulana、Thomas Dupic、Angela M. Phillips、Jeffrey Chang、Anne A. Roffler、Allison J. Greaney、Tyler N. Starr、Jesse D. Bloom、Michael M. Desai
- 发表来源：eLife（2023；12:e83442）
- 归档文本版本：Version of Record v2（eLife 记录的 v2 `versionDate` 为 2023-02-23）
- 发布日期：2023-02-23
- DOI：`10.7554/eLife.83442`
- PMID / PMCID：`36803543` / `PMC9949795`
- 本地文件：`articles/OmicronAbLandscape_2023-02-23_eLife-v2.pdf`
- 文件大小：2.58 MiB（2,707,623 bytes）
- SHA-256：`6ab237312d0a1ca5c79b3458c88b10fa95659b47453ef1c4060f90f51fdf0f5b`
- 文本许可：CC BY 4.0（eLife 版权声明写作“Moulana, Dupic et al.”）
- 补充材料：`articles/` 共四个对象，见下表

| 文件 | 大小 | SHA-256 |
| --- | ---: | --- |
| `OmicronAbLandscape_2023-02-23_eLife-v2.pdf` | 2.58 MiB（2,707,623 bytes） | `6ab237312d0a1ca5c79b3458c88b10fa95659b47453ef1c4060f90f51fdf0f5b` |
| `OmicronAbLandscape_2023-02-23_eLife-v2.xml` | 190.79 KiB（195,366 bytes） | `3de00ecbf360da140fbabd3165fe0469c0b800b06e0d69cb90d3628f0dab59e5` |
| `OmicronAbLandscape_2023-02-23_eLife-v2-supplement-1-isogenic-validation.docx` | 5.34 KiB（5,467 bytes） | `5340f3a51f5a671705dd38a94c3de94ae292b6b760486dc9bb133cc882737a06` |
| `OmicronAbLandscape_2023-02-23_eLife-v2-supplement-2-mdar-checklist.docx` | 100.17 KiB（102,579 bytes） | `5729d5b0762b94f271d3959c06f3e8325e306c5328b2a5366ec164454ae63248` |

正文 XML 与 PDF 来自 eLife 官方 CDN 的同一 v2 路径；PDF 为 19 页，起始字节为 `%PDF-1.4`。Supplementary file 1 是论文 Figure 1—figure supplement 1A 引用的 isogenic 验证表，Supplementary file 2 是 MDAR 报告清单。eLife 同时提供单独的 figures PDF，本次未归档：它是同一批图的再排版，不增加正文之外的数据。

## 仓库内容

一手入口是作者公开仓库 <https://github.com/desai-lab/omicron_ab_landscape>。上游没有 tag 也没有 release，因此本项目把完整 commit SHA 作为不可变版本锚点：

| 项目 | 固定值 |
| --- | --- |
| commit | `78a479925134820e8c2cc296108e79b65fa22ef6` |
| commit tree | `2aec2e9ebaa2a459372068f31d8d9f5e7c0580f9` |
| commit 时间 | 2023-11-10T16:58:28Z |
| 默认分支 | `main` |
| `source_version` | `snapshot-2023-11-10`（日期取自固定 commit 的 UTC 日期） |
| tree entries | 88（81 blob、7 tree） |
| blob 数 | 81 |
| blob 字节合计 | 262.34 MiB（275,083,357 bytes） |
| 内容 inventory SHA-256 | `d96ed528f6ea30beb6eff2736f90388c7d68b6965e75ce0775218d674d3121f2` |

固定 tree 是完整上游快照，没有 submodule（无 mode `160000` 条目）、没有 `.gitmodules`、没有 `.gitattributes`，对全部不超过 1,024 bytes 的 blob 检查标准 Git LFS pointer 头也未发现 LFS 指针。inventory SHA-256 的序列化方式为：按相对路径排序，对每个文件写入 `relative_path<TAB>bytes<TAB>content_sha256<LF>`，再计算整体 SHA-256。

```text
snapshot-2023-11-10/
└── omicron_ab_landscape/
    ├── Analyze/
    │   ├── Epistasis/
    │   │   ├── Tobit_model.ipynb
    │   │   ├── model_coefs_tobit/
    │   │   └── tobit.py
    │   ├── Landscape/
    │   │   ├── Phylogeny.ipynb
    │   │   └── force-directed-layout.ipynb
    │   ├── QC/
    │   │   ├── QC-antibodies.ipynb
    │   │   └── Analysis-antibodies.ipynb
    │   └── Structure/
    │       ├── Antibodies.ipynb
    │       └── <4 个 *_aic_*order_biochem.txt 效应表>
    ├── data/
    │   ├── cleaned_Kds_RBD_ACE2_low_filter.tsv
    │   ├── cleaned_Kds_RBD_{CB6,CoV555,REGN10987,S309}_proper.csv
    │   ├── lasso_prediction_*_aic_opt_order_biochem.txt
    │   ├── lasso_version_*_aic_*_order_biochem.txt
    │   ├── ACE2_5order_biochem.txt
    │   ├── thomas_version_S309_aic_4_order_biochem.txt
    │   ├── CV_rsquared.csv
    │   └── fig4_phylogeny.csv
    ├── Omicron_ab_Landscape.Rmd
    ├── omicron_ab_landscape.Rproj
    ├── README.md（上游自述）
    ├── .gitignore
    └── .DS_Store
└── sra/   （ENA PRJNA877045 原始测序 reads，1,472 个 FASTQ）
```

`data/` 是全部图的输入，17 个文件合计 207.26 MiB（217,327,294 bytes）：五张亲和力表、四个 `lasso_prediction_*` 逐基因型预测、四个 `lasso_version_*` 系数表、`ACE2_5order_biochem.txt` 与 `thomas_version_S309_aic_4_order_biochem.txt` 两个额外效应表、`CV_rsquared.csv` 与 `fig4_phylogeny.csv`。

`Analyze/` 是分析代码，59 个文件合计 54.98 MiB（57,649,557 bytes）。 `Analyze/Epistasis/model_coefs_tobit/` 单独占 48 个文件、52.35 MiB （54,888,164 bytes），为四个抗体在 1–4 阶下的系数与预测输出，S309 另有 `_c`、`_d` 两组并列文件。`Analyze/QC/`、`Analyze/Landscape/`、`Analyze/Structure/` 分别承载测序质控、系统发生与力导向布局、结构注释的 notebook。

上游 `README.md` 仅 513 bytes，自述仓库含 `TiteSeq/`、`Analysis/`、`data/` 与 `Additional_data/` 四个目录。固定 tree 中实际只有 `Analyze/` 与 `data/`，前两者不存在， `Additional_data/` 也不存在。上游 README 的目录名与实际 tree 不一致，本 source 保留上游原文不改写，差异记在“公开范围对照”。

论文 Data Availability 给出的 Software Heritage 归档为 `swh:1:rev:9ab630decfa835b2551430ed693796ef366b1aff`，与项目固定的 commit `78a4799…` 不同：归档对应论文发表时的仓库状态，项目固定的是此后（2023-11-10）的上传版本。两者不是同一快照，引用时不要混用。

### 兄弟交付 Tite-Seq 流程仓库

论文的 Code Availability 把 **Tite-Seq 处理流程**指向本仓库，但 `desai-lab/omicron_ab_landscape` 的全部 9 个 commit 都不含 `TiteSeq/` 目录（核对记录见“采集过程记录”）。流程、其运行元数据与 GISAID 补充表实际位于同一实验室的兄弟仓库 `desai-lab/compensatory_epistasis_omicron`，即前一篇论文 *Compensatory epistasis maintains ACE2 affinity during evolution of Omicron BA.1 SARS-CoV-2* 的配套仓库。本项目把该仓库的相关部分作为**兄弟交付**纳入同一 source version，使公开包能够自证本 README 中关于位点词典、复制号与 QC 判据的说明。

| 项目 | 固定值 |
| --- | --- |
| 仓库 | `https://github.com/desai-lab/compensatory_epistasis_omicron` |
| tag | `v0` |
| commit | `08be590a7a4ad8976a82caf9c736b9763d2aae33` |
| commit tree | `d80a38cfba1edc3fc5c4bb70b57048b3e66dd427` |
| commit 时间 | 2022-10-06T10:50:44-04:00 |
| commit 标题 | `Fix the fluorescence bug Jeffrey found` |
| 完整 tree | 636 blob、660.00 MiB（691,910,254 bytes） |
| 本次纳入 | 47 blob、63.35 MiB（66,423,763 bytes） |
| 纳入内容 inventory SHA-256 | `e333dcc4f9eced922417e667de6d3216003bc39335b7545c6cea48fc377b1c7e` |

纳入范围是**选择性快照**，规则为：只保留本论文直接引用的部分——`Titeseq/` （Snakefile 流程、脚本、notebook、运行配置与元数据表、流程自身产出的 RBD Kd 与表达表）、`Supplementary_Files/`（建库 gblock、引物与测序引物表、GISAID 补充表 PDF）、`LICENSE` 与 `README.md`。完整 tree 中另有 `Analyze/`（166 文件、169.5 MiB）、 `Additional_data/`（271 文件、191.0 MiB）与 `Final_Figures/`（150 文件、235.9 MiB），它们是前一篇论文的分析、验证与制图产物，不属于本 source 的解释范围，未纳入。纳入的每个文件都按其 Git blob 编码逐字节与固定 tree 核对。

```text
snapshot-2023-11-10/
└── compensatory_epistasis_omicron/
    ├── Titeseq/
    │   ├── Snakefile
    │   ├── cluster.yaml
    │   ├── environment.yaml
    │   ├── run_snake.sbatch
    │   ├── generate_simulated_fastq.ipynb
    │   ├── metadata/
    │   ├── notebooks/
    │   ├── scripts/
    │   └── results/Kds/
    ├── Supplementary_Files/
    ├── LICENSE
    └── README.md
```

`Titeseq/scripts/` 保存流程各步骤的实现（`parse_fastqs.py`、`count_UMIs.py`、 `parse_genotype.py`、`flow.py`、`kd_inference.py`、`merge_replicates.py` 等）， `Titeseq/metadata/` 保存运行配置与逐样本表，`Titeseq/results/Kds/` 保存该流程对 RBD 实验自身产出的 Kd 与表达表。该仓库的 `LICENSE` 为 MIT（Copyright (c) 2022 Thomas Dupic），覆盖其代码；它的 `README.md` 带有与 R71 仓库相同的目录描述，说明 R71 仓库那份自述是照抄自这里且两边都与实际 tree 不符。

## 数据结构

### 原始测序 reads（sra/）

`sra/` 保存 ENA BioProject `PRJNA877045` 的 736 个 run 的原始双端测序 FASTQ。每个 run 两个文件（`_1.fastq.gz` / `_2.fastq.gz`），共 **1,472 个对象**、67.72 GiB（72,717,382,225 bytes）。全部对象为 Illumina NovaSeq 6000 的 AMPLICON/SYNTHETIC/PCR 文库。文件按 ENA 官方 inventory 逐对象校验 bytes 与 MD5 落盘，未改名、未解压、未重组。

### 亲和力表的列结构与记录关系

五张表都是宽表，**一行对应一个基因型**，不是一条测序读数、一次分选事件或一次拟合。五张表的 `geno` 集合完全相同，都是全 `2^15` 设计空间，因此可以逐基因型横向连接。四张抗体 CSV 首列是一个无名导出索引列，其值等于把 `geno` 按二进制读出的整数（逐行成立），不携带额外信息。ACE2 的 TSV 没有该列。列名由固定命名规则构成：

| 列组 | 命名 | 数量与含义 |
| --- | --- | --- |
| 基因型 | `geno` | 1 列，15 位二进制字符串 |
| 单次 experiment 区块 | `log10Kd_<r>`、`A_<r>`、`B_<r>`、`r2_<r>`、`sigma_<r>`、`mean_log10PE<k>_<r>`、`std_log10PE<k>_<r>` | 每个复制号 `<r>` 一组；`<r>` 见下表 |
| 表达区块（部分） | `Mean fluorescence expression_<r>`、`Std fluorescence expression_<r>` | 仅 REGN10987 的 `g` 与 ACE2 的 `a`、`b` |
| 汇总 | `log10Kd`、`err_log10Kd`、`mean_sigma`、`log10Kd_pinned` | 4 列，四张抗体表与 ACE2 表都有 |
| QC（仅四张抗体表） | `max_fluo`、`min_fluo`、`difference`、`is_non_binder`、`is_clean` | 5 列 |

`<k>` 从 0 连续编号，列数与 assay 有关；本次发布版本各区块的实际范围与字段总数：

| 文件 | 复制号 | `mean_log10PE`/`std_log10PE` 的 `<k>` 范围 | 表达列 | 字段总数 |
| --- | --- | --- | --- | ---: |
| `cleaned_Kds_RBD_CB6_proper.csv` | `i`、`j` | 各 0–10 | 无 | 65 |
| `cleaned_Kds_RBD_CoV555_proper.csv` | `e`、`v` | 各 0–9 | 无 | 61 |
| `cleaned_Kds_RBD_REGN10987_proper.csv` | `g`、`h` | 各 0–10 | 仅 `g` | 67 |
| `cleaned_Kds_RBD_S309_proper.csv` | `c`、`d` | 各 0–11 | 无 | 69 |
| `cleaned_Kds_RBD_ACE2_low_filter.tsv` | `a`、`b` | 各 0–12 | `a`、`b` | 98 |
| 同上 | `x` | 0–10 | 无 | （并入上行） |

论文报告了各抗体的抗体浓度区间（见“实验设计和数据口径”）。`<k>` 与具体浓度、bin 的对应关系不在本 source 的公开表内，只存在于兄弟交付的 Tite-Seq 流程输入中： `Titeseq/metadata/sample_info_RBD.tsv` 按样本同时记录 `bin` 与 `concentration`， `config.yaml.RBD` 给出流程的序列与位点定义；该表与公开列的逐列换算仍须按流程脚本复核，本 source 不代为推断。

五张表之间没有公开的映射表，逐基因型连接键就是 `geno` 本身。跨抗体比较时要注意：同一个 `geno` 在不同抗体下是**不同的实验记录**，`is_non_binder`、`log10Kd` 与误差都按抗体各自成立；把五个抗体的值并成一条多标签记录会丢掉这个区别。

### 分析产物

`data/` 与 `Analyze/` 中的系数、预测文件是派生结果，分两类：

- `*_prediction_*.txt`（32,769 行）是制表符分隔的四列文本，表头为 `Genotype`、`Actual Kd`、`Predicted Kd`、`Predicted Kd linear`，逐基因型给出观测值与模型预测值。`data/lasso_prediction_<ab>_aic_opt_order_biochem.txt` 用该抗体的最优阶数；`Analyze/Epistasis/model_coefs_tobit/` 下另有 1–4 阶各自的预测。
- `*_version_*.txt` 与 `data/ACE2_5order_biochem.txt`、 `data/thomas_version_S309_aic_4_order_biochem.txt`、`Analyze/Structure/*.txt` 是系数表：首行形如 `Params: <n>`，随后是 `Term`、`Coefficient`、`Standard Error` 列（部分文件另有 `Coefficient_Lin`、`Standard Error_Lin`，ACE2 的文件另有 `p-value`、`95% CI lower`、`95% CI upper`）。`Term` 取 `Intercept` 或位点编号（单一位点如 `1`，组合如 `1,2`），编号即“实验设计和数据口径”中的位点词典。 `Analyze/Structure/Antibodies.ipynb` 读取 `Analyze/Structure/` 下的效应表并把位点编号替换为残基号（339、371、…、505）后作图。

`Analyze/QC/QC-antibodies.ipynb` 与 `Analyze/QC/Analysis-antibodies.ipynb` 处理测序与拟合质控，`Analyze/Epistasis/Tobit_model.ipynb` 与 `Analyze/Epistasis/tobit.py` 做上位性模型拟合，`Analyze/Landscape/Phylogeny.ipynb` 与 `Analyze/Landscape/force-directed-layout.ipynb` 做系统发生与景观布局。 `.DS_Store`、`.gitignore`、`omicron_ab_landscape.Rproj` 是仓库自身的管理文件，不承载数据。

### 兄弟交付的元数据表

兄弟交付里承载数据的部分如下，其余是流程代码（`Snakefile`、`scripts/`、`notebooks/`、 `environment.yaml`、`run_snake.sbatch`）与配置，不属于表格 schema。

- `Titeseq/metadata/replicate_info_RBD.tsv`（11 行）：一行一次 Tite-Seq 实验。字段为 `replicate`（单字母复制号）、`construct`（本 source 全为 `RBD`）、`solute`（该次实验的结合分子）、`sequencing_data_subdir`、`cytometry_data_subdir`、`collection_date`。取值与公开表列名后缀逐一对上：`i`/`j` 为 CB6，`e`/`v` 为 CoV555，`g`/`h` 为 REGN10987，`c`/`d` 为 S309，`a`/`b`/`x` 为 ACE2。四个抗体各两次实验，ACE2 三次。
- `Titeseq/metadata/sample_info_RBD.tsv`（535 行）：一行一个分选样本。字段为 `sample_name`、`sample_id`、`construct`、`solute`、`replicate`、`concentration`（样本标签）、`concentration_float`（该溶质的实测浓度）、`bin`、`P5`、`P7`、`col_i`、`row_i`、 `cell count`。该表把 `bin` 与浓度同时记下，是公开表中 `mean_log10PE<k>` 一类的分组索引在流程侧的来源；浓度列的单位未在该文件或 `metadata/README.md` 中标明。
- `Titeseq/metadata/config.yaml.RBD`：流程的运行配置，含起始残基号 331、武汉 Hu-1 与 BA.1 的 RBD 核苷酸序列、`mutation_names`（15 个替换，与公开表位点词典一致）、 `num_mutations: 15`，以及 `synonymously_coded_mutations`（为把部分替换放进测序读段而做的同义编码，例如 K417N 同时编码在 378 位）。
- `Titeseq/results/Kds/cleaned_Kds_RBD_ACE2.tsv`：流程对 ACE2 实验自身产出的 Kd 表，与公开包的 `cleaned_Kds_RBD_ACE2_low_filter.tsv` **列完全相同**（同为 98 列、 32,768 行），三组逐 replicate 列（`log10Kd_a/_b/_x`）与 `r2_a/_b/_x` 逐字节一致，即两者出自同一次流程运行与同一批拟合。差别只在合并前是否剔除拟合：

  | 规则 | 流程输出 `cleaned_Kds_RBD_ACE2.tsv` | 公开包 `..._low_filter.tsv` |
  | --- | --- | --- |
  | 单个 replicate 的 `log10Kd` | `sigma > 1` 时置空 | 保留 |
  | 汇总 `log10Kd` | 对保留的 replicate 取算术平均 | 对全部非空 replicate 取算术平均 |

  逐行核对：公开包相对流程输出多出 2,403（`a`）、1,897（`b`）、904（`x`）个 replicate 值，这些**全部**对应流程侧 `sigma > 1` 的拟合，没有一个是 `r2 < 0.8`；反向多出的为 0。流程输出的汇总列在全部 32,768 行上都等于其自身非空 replicate 的算术平均，公开包的汇总列在同样的 32,768 行上等于全部非空 replicate 的算术平均。因此文件名里的 `low_filter` 指**保留 `SE > 1` 的拟合、不施加论文 Methods 所述的 `SE ≤ 1` 剔除**；`r2 < 0.8` 一侧的剔除两边一致。该步骤在 R71 仓库与兄弟仓库的公开代码中都没有实现，只在 R71 自己的 `Omicron_ab_Landscape.Rmd` 里以文件名形式出现。
- `Titeseq/results/Kds/cleaned_expression_RBD.tsv`：同一流程产出的表达表。
- `Supplementary_Files/`（7 个数据文件 + `.DS_Store`）：建库用的 gblock 序列（BA.1、武汉 Hu-1、pETcon-RBD-201aa、ccDB 上下游）、golden gate 引物与片段表、 Illumina 建库测序引物表，以及 GISAID 补充表 PDF。

### 字段说明

- `geno`：15 位二进制字符串，位序与等位含义见“实验设计和数据口径”。取值集合为全部 `2^15` 个组合，不是枚举型标识符。
- 四张抗体 CSV 的无名列：导出索引，等于 `int(geno, 2)`，逐行成立。ACE2 的 TSV 无此列。
- `log10Kd_<r>`：该复制号单次 experiment 的 `K_D,app` 拟合值，按 `-log10(K_D,app [M])` 解读，越大亲和力越强。空值表示该次拟合未产出可用值，不是零。
- `A_<r>`、`B_<r>`：Hill 拟合的饱和荧光增量与背景荧光，对应论文 Methods 的 `A_s`、`B_s`；拟合边界为 `A` 10²–10⁶、`B` 1–10⁵。空值与 `log10Kd_<r>` 同步缺失。
- `r2_<r>`：该次拟合的决定系数；`sigma_<r>`：该次拟合的标准误（论文 Methods 的 `SE`）。
- `mean_log10PE<k>_<r>`、`std_log10PE<k>_<r>`：该次 experiment 第 `<k>` 组的平均与标准差对数荧光。`<k>` 与浓度、bin 的对应关系见“亲和力表的列结构与记录关系”。
- `Mean fluorescence expression_<r>`、`Std fluorescence expression_<r>`：该次 experiment 的表达荧光均值与标准差；只出现在 REGN10987 的 `g` 与 ACE2 的 `a`、`b` 区块，其余区块没有对应列。
- `log10Kd`：跨 replicate 汇总的 `K_D,app`；按论文 Methods，两个 replicate 的拟合在剔除 `r² < 0.8` 或 `SE > 1` 后取平均。空值表示没有可用汇总值。
- `log10Kd_pinned`：本次发布的五张表中与 `log10Kd` **逐行完全相同**（含空值位置），可视为同一列；`Omicron_ab_Landscape.Rmd` 读取的是这一列。名字中的“pinned”指论文绘图时的封顶处理，该处理在 Rmd 内完成，没有写进发布值。
- `err_log10Kd`：`log10Kd` 的误差列。`is_clean` 为真的行全部带该值，没有例外；判为非结合型的行多数为空，但也有带值的行（CB6 129 行、LY-CoV555 2,798 行、 REGN10987 351 行、S309 0 行），因此它与 `is_non_binder` 不是互斥的两组。
- `mean_sigma`：各 replicate `sigma_<r>` 的算术平均，逐行成立（32,768 行全部满足）。非结合型行上可能取到很大的数值（单次拟合未收敛所致），不宜直接当作测量精度使用。
- `max_fluo`、`min_fluo`：该基因型在全部浓度上的最大与最小估计对数荧光； `difference = max_fluo − min_fluo`，逐行成立。
- `is_non_binder`：布尔字段，原始取值 `True`/`False`。`True` 等价于 `difference < 1`，逐行成立；判定阈值与依据见“实验设计和数据口径”。
- `is_clean`：布尔字段，原始取值 `True`/`False`。`True` 等价于两个 replicate 同时满足 `r2_<r> ≥ 0.8` 且 `sigma_<r> ≤ 1`，逐行成立。非结合型行可以同时 `is_clean = False`。
- ACE2 表没有 `max_fluo`、`min_fluo`、`difference`、`is_non_binder`、`is_clean` 五列，下游按“全部视为结合型且通过 QC”处理。

### 数据示例

以下两行取自真实文件。第一行是全零基因型（武汉 Hu-1 RBD），在四个抗体下都是正常结合型：

```text
CB6       geno=000000000000000  log10Kd=9.805360779020472  err_log10Kd=0.0211163419661701
          mean_sigma=0.2847608079211605  difference=2.558907446938231
          is_non_binder=False  is_clean=True   （_i: log10Kd_i=9.784244437054303, r2_i=0.9894,
                                                _j: log10Kd_j=9.826477120986643, r2_j=0.9557）
CoV555    geno=000000000000000  log10Kd=10.194023765881775
REGN10987 geno=000000000000000  log10Kd=9.95926773815847
S309      geno=000000000000000  log10Kd=9.343234421070015
```

第二行是全一基因型（BA.1 RBD）。CB6、LY-CoV555 与 REGN10987 判为非结合型，S309 与 ACE2 仍有有限亲和力：

```text
CB6       geno=111111111111111  log10Kd=（空）  is_non_binder=True   is_clean=False
                                difference=0.3769914057813817
CoV555    geno=111111111111111  log10Kd=（空）  is_non_binder=True   is_clean=False
                                difference=0.3391712046123856
REGN10987 geno=111111111111111  log10Kd=（空）  is_non_binder=True   is_clean=False
                                difference=0.35225373219413747
S309      geno=111111111111111  log10Kd=8.586620530697918  is_non_binder=False  is_clean=True
ACE2      geno=111111111111111  log10Kd=9.478874391830967
```

每行代表一个基因型在某一个抗体下的汇总测量，包含两（ACE2 为三）次 experiment 的拟合结果与它们的汇总；不是两次独立样本、也不是同一样本的重复表示。非结合型行的 `mean_sigma`（CB6 该行为 11.694824769069571）来自未收敛的拟合，不代表结合测量精度。

## PDB 数据库

审计范围是论文正文、图注与仓库 notebook 中出现的结构线索，再回到 RCSB 核验条目身份。论文 Figure 8 的图注明确写出四个抗体足迹所用的结构“Structure of SARS-CoV-2 BA.1 RBD with each antibody footprint annotated (PDB ID 7KMG, 6WPT, 7C01, and 6XDG)”；Methods 的 Structural analysis 一节写出 ACE2 参考结构“a 2.79 Å cryo-electron microscopy structure of Omicron BA.1 complexed with ACE2 (PDB ID: 7WPB)”，用于以 ChimeraX 计算 ACE2 与各突变残基的埋藏面积。因此本 source 有五个可由一手材料追溯的锚点，分别对应数据集中的四个抗体与 ACE2。仓库 notebook 本身不加载结构文件，`Analyze/Structure/Antibodies.ipynb` 只把位点编号换算为残基号（339、371、…、505），不构成额外的结构证据。

| 数据集对象 | complex_id | PDB | 角色 → author chain | 实体描述（RCSB） | 序列长度 |
| --- | --- | --- | --- | --- | ---: |
| LY-CoV555（CoV555） | `CoV555-RBD` | `7KMG` | heavy A、light B、antigen C | Fab heavy / Fab light / Spike protein S1 | 229 / 212 / 205 |
| S309 | `S309-spike` | `6WPT` | heavy D、light E、antigen A | S309 heavy / S309 light / spike glycoprotein | 127 / 107 / 1,281 |
| CB6（LY-CoV016） | `CB6-RBD` | `7C01` | heavy C、light D、antigen A | CB6 heavy / CB6 light / Spike protein S1 | 233 / 217 / 229 |
| REGN10987 | `REGN10987-RBD` | `6XDG` | heavy C、light A、antigen E | REGN10987 heavy / REGN10987 light / Spike protein S1 | 225 / 216 / 251 |
| ACE2 | `ACE2-BA1-RBD` | `7WPB` | antigen A、receptor D | spike glycoprotein / ACE2 | 1,205 / 805 |

角色由 RCSB 的 polymer entity 描述确定，author chain 由实体级 `auth_asym_ids` 与逐链实例交叉核对后选定，再与下载的完整 mmCIF 的 `_atom_site` 循环逐行比对（每个 FASTA 记录的 `author_chain` 必须映射到该记录 `label_asym`）。6XDG 同时含 REGN10933 的重链与轻链，本次只取 REGN10987 的两条链，没有把 REGN10933 当作数据集中的抗体。7KMG、6WPT、7C01 的抗原与抗体实体都各有多个同序列副本；由于副本级证据不足， FASTA 记录的是该 polymer entity 的 canonical 序列，不对具体副本作主张。

| 文件 | 大小 | SHA-256 |
| --- | ---: | --- |
| `pdb/sequences/rcsb_pdb_7KMG.fasta` | 867 bytes | `e14ca2b9fd86bdd82ba966c782bb1a343917d4585753687f9d76d1c2943e5fba` |
| `pdb/sequences/rcsb_pdb_6WPT.fasta` | 1.71 KiB（1,748 bytes） | `037d6ac2488988c6c057f130f378b49933c0727003b14c1f579ba355bcbf752b` |
| `pdb/sequences/rcsb_pdb_7C01.fasta` | 891 bytes | `20449d7b62347bf9ce97a49e4eb9589e7a90ec1819494c7f73f9be584ac9ee0f` |
| `pdb/sequences/rcsb_pdb_6XDG.fasta` | 923 bytes | `82147acd4bca1f0e78312a021adb6e12eb15a5503a0f7572bf7166cfa24701cc` |
| `pdb/sequences/rcsb_pdb_7WPB.fasta` | 2.12 KiB（2,174 bytes） | `c2724511d1c8101c66981f5b278d5a061bd084e1da8a15ac4b3d82e2431687fd` |
| `pdb/structures/7KMG.cif` | 1.00 MiB（1,049,928 bytes） | `a7ae8618bc70cdd0b15fb6e1a02d8b22dabcfffd074da5790b18e7c298804a4d` |
| `pdb/structures/6WPT.cif` | 2.64 MiB（2,766,575 bytes） | `74fc4a87045b16f7f66719a54a10feeaf13ad91592580c9774712d77843de0e9` |
| `pdb/structures/7C01.cif` | 1.93 MiB（2,027,454 bytes） | `0bdaaf541b6e150c2deb5809475b0222228b4539baaa0d9c5a890ee49695e3ae` |
| `pdb/structures/6XDG.cif` | 969.04 KiB（992,298 bytes） | `3f622dd22e619e57eec108c8acdb340e5fc3939233c1fd19a6d4cbfc9d7fbbab` |
| `pdb/structures/7WPB.cif` | 803.69 KiB（822,975 bytes） | `cde0cf0e88c4f9558d29f80153ec871f2d04a296dbbb5d6a42071e7ca8dd3fc6` |

`pdb/` 合计 10 个文件、7.31 MiB（7,665,833 bytes）。FASTA 由 RCSB canonical entity 序列加项目角色 header 生成，不是 RCSB 条目 FASTA 的原始字节；mmCIF 保留来源字节。

映射强度必须按对象区分，不能一律当成“实验构建体的结构”：

- 四个抗体复合物（7KMG、6WPT、7C01、6XDG）的抗原分别是武汉 Hu-1 谱系的 Spike protein S1 或完整 spike 胞外域构建，而本数据集的抗原是 BA.1 背景下的 RBD 变体。它们支持“该抗体结合 RBD 的参考结构”，不是本次测得的任一变体的结构。
- 6WPT 的抗原实体是完整 spike 糖蛋白（1,281 aa），6WPT 的抗体实体只有 VH/VL 两个结构域（127 / 107 aa），不是完整 Fab；6XDG 的抗原实体含 251 aa 的 S1 构建； 7KMG 与 7C01 的抗原实体分别为 205 aa 与 229 aa 的 S1 构建。本 source 不裁剪这些序列到 RBD 区间，需要 RBD 边界时应在 `processed/` 阶段按明确规则处理。
- ACE2 的锚点是 `7WPB`，与论文的结构分析直接对应，且是五个锚点中唯一使用 BA.1 抗原的条目；`7WPB` 的抗原实体同样是完整 spike（1,205 aa）而非 RBD-only 构建。
- 数据集记录侧没有逐行 PDB 键：四张抗体表以抗体（而非变体）为单位连接到锚点，连接关系是“抗体 → 参考复合物”，不是“变体 → 结构”。README 不提供逐基因型的结构映射，也不得据此为每个基因型复制结构文件。

## 采集过程记录

- 2026-09-24：核验仓库身份、可见性、默认分支、tag/release 与固定 commit；确认共享存储无 R71 正式目录。当时记录的 `source_version`、tree 与 blob 计数成为本轮的起点。
- 2026-09-27：按固定 commit `78a479925134820e8c2cc296108e79b65fa22ef6` 与 tree `2aec2e9ebaa2a459372068f31d8d9f5e7c0580f9` 下载 GitHub payload 至 `.../SRC_R71_OMICRON_AB_LANDSCAPE/.staging/snapshot-2023-11-10.partial`，逐文件按 Git blob 编码重算 SHA-1，得到 81 blob、275,083,357 bytes、inventory SHA-256 `d96ed528…`，bare cache `git fsck --strict` 退出码 0。该次执行以 root 身份完成，脚本自己的校验因此通过。
- 2026-09-28：接手时发现上一轮产物对非 root 用户不可读。`omicron_ab_landscape/` 与 cache 中的 `repository.git/` 权限为 `drwx--S---+ root shared-data`，该共享盘的 default ACL 把组权限算成 mask `---`，组内其它用户连列目录都被拒绝。根因是脚本用 `mktemp -d` 建临时目录后 `mv` 成正式名字：`mktemp -d` 固定建 0700，`mv` 保留该模式。已在 `download_r72_omicron_ab_landscape.sh` 的两个 `mktemp -d` 之后各加 `chmod 2775`，并加 `umask 002`。
- 2026-09-28：把两处被锁目录改名保留（`.staging/rootlocked-20260927-staging.partial` 与 `snapshot-2023-11-10/rootlocked-20260927-repository.git`），以 `yangwuyu` 身份重跑修好的脚本。重跑得到相同的 81 blob、275,083,357 bytes 与 inventory SHA-256 `d96ed528…`，说明上一轮下载的字节身份本身没有问题，只是权限错误。两个 root 锁定目录为非空目录且当前账号无写权限，无法自行删除，见 `Q04`。
- 2026-09-28：从 eLife 官方接口核验论文版本：v1 状态 `poa`、v2 状态 `vor`，两者 `published` 均为 2023-02-21，v2 的 `versionDate` 为 2023-02-23。归档 version of record v2，文件名日期取 v2 自身的 `versionDate`。正文 PDF/XML 与两份补充材料从 eLife CDN 同一 v2 路径取得，逐文件记录字节数与 SHA-256；PDF 起始字节与 19 页结构通过检查。原始下载名为 `elife-83442-v2.pdf` 一类，落地时改写为 `OmicronAbLandscape_2023-02-23_eLife-v2.*`，字节与哈希未变。
- 2026-09-28：从 ENA portal API 固定 `PRJNA877045` 的 run 级 inventory，存于 cache 的 `run/` 目录（`ena_runs.tsv`，736 runs、1,472 个 FASTQ、67.72 GiB （72,717,382,225 bytes），全部为 ILLUMINA NovaSeq 6000 的 AMPLICON/SYNTHETIC/PCR）。直连 `ftp.sra.ebi.ac.uk` 在 12 秒内超时（HTTP 000），经节点代理实测约 0.91 MB/s，全量串行约 22 小时。本轮未下载 reads，见 `Q01`。
- 2026-09-28：按 PDB 硬性要求执行覆盖审计，从论文图注与 Methods 定位五个锚点，目视核对 RCSB entity 描述与 author/label 链编号，再用本 skill 的 `fetch_pdb_reference_data.py` 取得五个锚点的 canonical FASTA 与完整 mmCIF。该脚本的 `tempfile.mkdtemp` 同样会留下 0700 目录，本次一并加 `os.chmod(0o2775)`；下载结果通过脚本自带的 FASTA↔mmCIF 链映射校验。
- 2026-09-28：实际解析五张亲和力表。确认行数均为 32,768、`geno` 唯一、五表基因型集合相同；确认 `is_clean` 等价于两个 replicate 同时 `r² ≥ 0.8` 且 `SE ≤ 1`、 `is_non_binder` 等价于 `difference < 1`、`mean_sigma` 为 replicate `sigma` 均值、 `difference = max_fluo − min_fluo`、`log10Kd` 与 `log10Kd_pinned` 逐行相同，以上关系在四张抗体文件的各 32,768 行全部成立。另以全一基因型复核 BA.1 逃逸模式（CB6、LY-CoV555、REGN10987 非结合，S309 与 ACE2 仍结合）。
- 2026-09-28：比对论文报告的可用变体数与本版本表的可复算数，两者不一致，记入 `Q02`。论文 Methods 自述的处理链（含 Tite-Seq snakemake 流程）与上游 README 自述的 `TiteSeq/` 目录均不在固定 tree 中，记入 `Q03`。
- 2026-09-28：在 staging 运行 `scripts/validate_r72_omicron_ab_landscape.py`，通过后按固定 README 合同 lint，再用原子重命名发布为 `SRC_R71_OMICRON_AB_LANDSCAPE/snapshot-2023-11-10`，并在正式目录复跑同一 validator。cache 中的 ENA inventory、API 响应与验证 JSON 不进入 source version。
- 2026-09-28：追查 `Q03`。完整克隆 `desai-lab/omicron_ab_landscape`（9 个 commit）后确认，`TiteSeq/`、`Analysis/`、`Additional_data/` 在**任何一个 commit 中都不存在**，上游 README 的目录描述自 `9ab630d` 起就与实际 tree 不符。改查同一实验室的 `desai-lab/compensatory_epistasis_omicron`，在其 `Titeseq/` 下找到 Tite-Seq 流程本体（Snakefile、脚本、notebook、运行配置与元数据表），并确认 `Q03` 与 `Q05` 所需的一手定义都在其中：`replicate_info_RBD.tsv` 给出各复制号对应的 `solute`（四个抗体各两次实验，ACE2 三次），`sample_info_RBD.tsv` 同时记录 `bin` 与浓度， `config.yaml.RBD` 给出起始残基号 331 与 15 个替换的核苷酸参考。`Q03` 结案。
- 2026-09-28：把该仓库作为兄弟交付纳入本 source version。固定其 tag `v0` （commit `08be590a…`、tree `d80a38cf…`），按选择性快照规则只取 `Titeseq/`、 `Supplementary_Files/`、`LICENSE`、`README.md`，共 47 个文件、63.35 MiB （66,423,763 bytes），逐文件按 Git blob 编码与固定 tree 核对，纳入内容 inventory SHA-256 为 `e333dcc4…`。完整 tree 为 636 blob、660.00 MiB，其余三个顶层目录是前一篇论文的分析与图表产物，未纳入。
- 2026-09-28：`Q06` 的部分材料随兄弟交付到位：`Supplementary_Files/` 内的 `Supplementary_File_7_gisaid_supplemental_table_epi_set_20220615uq.pdf` 即论文所用的 GISAID 补充表，无需 GISAID 账号即可从公开仓库取得；完整系统发生输入仍需 GISAID 注册，`Q06` 降级为 partial 并保留。
- 2026-09-28：比对公开包 ACE2 表与兄弟交付的流程输出，解出 `low_filter` 的含义。两份文件的逐 replicate 列与 `r2` 列逐字节一致，说明同一次流程运行；差别只在合并前是否把 `sigma > 1` 的 replicate 的 `log10Kd` 置空：流程输出置空并按保留值取平均，公开表保留全部非空值取平均。公开表多出的 replica 值（`a` 2,403、`b` 1,897、 `x` 904）全部对应流程侧 `sigma > 1` 的拟合，无一对应 `r2 < 0.8`，反向为 0。 `low_filter` 即“不做 `SE ≤ 1` 剔除”，`Q05` 结案。
- 2026-09-28：为 `Q02` 逐项核算论文报告数与发布表可复算数的差距。在九种自然定义（`is_non_binder`、`is_clean`、任一 replicate 有拟合值、≥1 个 replicate 通过 `r2 ≥ 0.8` 且 `SE ≤ 1`、两个 replicate 都通过、以及各自与 `is_non_binder` 的并集）下，没有任何一种能复现论文的 32,603 / 27,485 / 31,479 / 32,650；发布表在全部四种抗体上都给出**更多**可用变体。结论与四种口径的完整对照写入 README 的 `Q02`。
- 2026-09-28：启动 `Q01` 的原始测序 reads 下载。`scripts/download_r72_omicron_ab_landscape_reads.sh` 从 ENA portal API 重新固定 `PRJNA877045` 的 run 级 inventory，校验得到 736 runs、 1,472 个 FASTQ、72,717,382,225 bytes，与既有记录一致后开始串行下载；直连 `ftp.sra.ebi.ac.uk` 在 12 秒内超时，改用节点代理。下载器逐对象校验官方 bytes 与 MD5，已完成对象写入状态文件，可断点续跑；脚本退出前不发布 `sra/`。
- 2026-09-29 至 09-30：reads 串行下载遇链路拥堵多次断流。09-29 确认 `SRR21428958_2` 为 ENA 上游缺失（inventory 有官方 bytes/MD5，URL 却返回目录占位符），加入跳过名单并在脚本加载状态前硬过滤，随后续传。09-30 下载完成：1,471 个对象全部以官方 bytes/MD5 校验通过，`READS VERIFIED 1471 objects, 72688229805 bytes`。进程中途死过一次（该对象经 40 次重试后失败退出），以相同脚本重启并从状态文件续传，未重下已完成对象。
- 2026-09-30：把 staging 的 `sra/` 装配进正式版本目录（`mv` 原子移动，与 payload 同级），删除 staging 残留。以补丁后的 `scripts/validate_r72_omicron_ab_landscape.py` （增加跳过对象豁免、总量按落盘对象扣减）在正式目录运行 `--require-sra`，通过： 1,471 个 FASTQ 逐一对照 ENA inventory 的官方 bytes 与 MD5，跳过对象保持官方计数。 README 同步结案 `Q01`、新增 `Q08` 记录上游缺失对象。
- 2026-09-30：复核正式目录时确认 `SRR21428958_2.fastq.gz` 已补入。该文件大小 29,152,420 bytes、MD5 `83874b26ddfc6ab41d0b677930bd7143` 均与 ENA inventory 一致，且 gzip 完整性校验通过；`sra/` 现为完整的 1,472 个对象 / 72,717,382,225 bytes。当前环境下未能重新确认 ENA 公共端点的可用性（经代理返回 403、直连超时），故本记录只确认本地交付补齐，不把它表述为 ENA 服务已恢复。

## 参考文献

- 作者仓库：<https://github.com/desai-lab/omicron_ab_landscape>
- 固定 commit：<https://github.com/desai-lab/omicron_ab_landscape/commit/78a479925134820e8c2cc296108e79b65fa22ef6>
- 兄弟交付（Tite-Seq 流程与元数据，tag `v0`）：<https://github.com/desai-lab/compensatory_epistasis_omicron/tree/v0>
- 兄弟交付固定 commit：<https://github.com/desai-lab/compensatory_epistasis_omicron/commit/08be590a7a4ad8976a82caf9c736b9763d2aae33>
- 论文 DOI：<https://doi.org/10.7554/eLife.83442>
- eLife 文章页：<https://elifesciences.org/articles/83442>
- Europe PMC：<https://europepmc.org/article/PMC/PMC9949795>
- Software Heritage 归档（论文发表时的仓库状态，非本项目固定 commit）： `swh:1:rev:9ab630decfa835b2551430ed693796ef366b1aff`
- ENA BioProject：<https://www.ebi.ac.uk/ena/browser/view/PRJNA877045>
- NCBI BioProject：<https://www.ncbi.nlm.nih.gov/bioproject/PRJNA877045>
- GISAID 系统发生输入（需注册）：EPI_SET ID `EPI_SET_20220615uq`， <https://doi.org/10.55876/gis8.220615uq>
- RCSB 条目：<https://www.rcsb.org/structure/7KMG>、<https://www.rcsb.org/structure/6WPT>、 <https://www.rcsb.org/structure/7C01>、<https://www.rcsb.org/structure/6XDG>、 <https://www.rcsb.org/structure/7WPB>

## 其他

### 数据范围和限制

本次公开包达到 `verified public-package onboarding`：作者固定 commit 的完整 payload、 eLife version of record v2 的正文 PDF/XML 与两份补充材料、五个 RCSB 锚点的 canonical FASTA 与完整 mmCIF，以及兄弟交付中论文直接引用的 Tite-Seq 流程与元数据，均已取得并独立验收。

`complete-study acquisition` 为 `partial`：系统发生分析所用 GISAID 序列集的补充表已取得、完整树仍需注册（`Q06`）；论文报告的可用变体数与发布表可复算数不一致，差因待作者确认（`Q02`）。原始测序 reads 已随 `sra/` 完整取得（`Q01`、`Q08` 均结案）。

使用边界有三点需要保留。第一，本 source 的自变量是抗原 RBD 基因型，抗体固定，五张表是同一批 32,768 个基因型对五个固定结合分子（四个抗体与 ACE2）的测量；它支持“抗原变体如何影响给定抗体的结合”，不支持“在固定抗原下比较不同抗体序列”。第二，五个结合分子之间的记录不独立：同一 `geno` 在五个文件里是同一个抗原变体的五次不同测量，跨抗体合并时必须保留抗体维度。第三，`log10Kd` 是两（ACE2 为三）次 experiment 拟合的汇总，其中经 `r²`／`SE` 判据剔除过拟合不佳的值；缺失来自拟合失败或判据剔除，不是零亲和力。

### 完整性与验收

`scripts/validate_r72_omicron_ab_landscape.py` 对发布目录做独立检查，覆盖：

- Git payload 的 81 个文件、275,083,357 bytes 与内容 SHA-256 inventory `d96ed528f6ea30beb6eff2736f90388c7d68b6965e75ce0775218d674d3121f2`；payload 内无 `.git`、无 `.partial` 残留。
- 四个论文对象的字节数与 SHA-256，以及 PDF 起始字节。
- 兄弟交付的 47 个文件、66,423,763 bytes 与内容 SHA-256 inventory `e333dcc4f9eced922417e667de6d3216003bc39335b7545c6cea48fc377b1c7e`，以及 `LICENSE`、`README.md`、`Titeseq/Snakefile`、`Titeseq/metadata/replicate_info_RBD.tsv` 的存在性。
- 五个锚点的 10 个文件字节数与 SHA-256；每个 FASTA 记录的 `role`/`complex`/ `author_chain`/`label_asym` 与配置一致，且与 mmCIF `_atom_site` 循环解析出的 author↔label 映射一致；mmCIF 可解析出聚合物原子行。
- 五张表的字段数、行数、`geno` 唯一性与五表基因型集合一致；`log10Kd` 有限值计数、 `is_clean` 与 `is_non_binder` 计数；以及上节列出的五条逐行恒等式。
- 全一基因型的 BA.1 逃逸模式。
- `sra/` 的 1,472 个 FASTQ 逐对象对照 ENA inventory 的官方 bytes 与 MD5。
- 顶层布局、README 必填 H2 与 source 身份字段。

发布前在 staging 运行一次，发布后在正式目录复跑同一脚本，两次均通过；`sra/` 加入后以 `--require-sra` 在正式目录复跑，全部通过。

### 许可和再分发边界

论文正文采用 CC BY 4.0（eLife 页面与文章元数据均记录该许可，版权方写作“Moulana, Dupic et al.”）。该许可覆盖论文文本本身。

作者 GitHub 仓库没有 `LICENSE`、`LICENCE` 或 `COPYING` 文件，GitHub 仓库元数据的 `license` 字段为 `null`，固定 commit 的 License API 返回 404，仓库内也没有任何许可声明。因此**上游未特别说明覆盖仓库数据的许可，使用与再分发范围不明确**。论文正文的 CC BY 4.0 不能自动推广到仓库中的数据与代码。

兄弟交付的 `compensatory_epistasis_omicron` 带有 MIT 许可（Copyright (c) 2022 Thomas Dupic），按其文本覆盖该仓库的 Software，即其中的流程代码；它不是数据许可，也不覆盖 R71 仓库的任何对象。同一交付中 `Supplementary_Files/` 与 `Titeseq/results/` 属于该仓库的数据产物，其许可同样未被该 MIT 文本说明。

原始测序数据在 NCBI/ENA 的 BioProject `PRJNA877045` 下，遵守该数据库自身的条款； RCSB 的 FASTA 与 mmCIF 遵守 RCSB 条款；GISAID 序列集另有其注册与使用条款。本 README 不替代任何原始权利声明，也不把其中一层的许可套用到另一层。许可未特别说明不阻塞本次接入发布，但其对接入以外用途的限制见 `Q07`。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 全部 `2^15 = 32,768` 个 RBD 基因型的 `K_D,app` | 五张表各 32,768 行、`geno` 唯一且集合相同 | 已包含（行数）；数值可用性见下行 |
| 每个抗体获得约 30,000 个变体的 `K_D,app`（论文报告 32,603 / 27,485 / 31,479 / 32,650） | 本版本表在九种自然判据下可复算 16,422–32,720 个可用变体，均多于论文数字 | 部分包含，差异未解释（`Q02`） |
| ACE2 表的过滤口径 | 与兄弟交付的流程输出逐 replicate 列一致，差别只在合并前是否剔除 `SE > 1` 的拟合 | 已包含（`Q05` 已结案） |
| 原始测序读数存于 `PRJNA877045` | ENA inventory 与 `sra/` 均为 736 runs / 1,472 FASTQ / 67.72 GiB；各对象 bytes 与 MD5 对照通过 | 已包含（`Q01`、`Q08` 已结案） |
| 仓库含 Tite-Seq 分析流程 `TiteSeq/`（上游 README 与论文 Code Availability 指向该仓库） | R71 仓库 9 个 commit 均无该目录；流程位于兄弟仓库，已作为兄弟交付纳入 | 已包含（兄弟交付） |
| 逐 bin 荧光与拟合参数 | `mean_log10PE*`、`std_log10PE*`、`A`、`B`、`r2`、`sigma` 各 replicate 区块 | 已包含 |
| 上位性系数与逐基因型预测 | `lasso_*`、`ACE2_5order_*`、`thomas_version_*`、`Analyze/Structure/*` | 已包含 |
| 系统发生分析输入 | GISAID EPI_SET `EPI_SET_20220615uq`；补充表 PDF 随兄弟交付取得，完整树需注册 | 部分包含（`Q06`） |
| 抗体—RBD 结构足迹（Figure 8C）与 ACE2 接触面积（Methods） | 论文点名 7KMG、6WPT、7C01、6XDG、7WPB | 已包含（外部数据库锚点） |
| event-level FCS 或分选原始文件 | 固定 tree 与 ENA project 均未发现 | 未公开 |

## 待解决问题与处理进展

- `Q02`（最近更新：2026-09-28；差异已定位，原因待作者确认）：论文写“we obtain K_D,app for at least ~30,000 variants to each of the mAbs”，列出 32,603（LY-CoV016）、 27,485（LY-CoV555）、31,479（REGN10987）、32,650（S309）。把该句按不同自然定义落到本版本发布表上，结果如下（“≥1 rep 通过”= 至少一个 replicate 的 `log10Kd` 非空且该 replicate 的 `r2 ≥ 0.8` 且 `sigma ≤ 1`；“两 rep 均通过”= `is_clean`）：

  | 抗体 | `is_non_binder` | `is_clean` | 任一 rep 有拟合值 | ≥1 rep 通过 | 两 rep 均通过 | 论文 |
  | --- | ---: | ---: | ---: | ---: | ---: | ---: |
  | LY-CoV016（CB6） | 16,470 | 15,760 | 16,511 | 16,422 | 15,760 | 32,603 |
  | LY-CoV555 | 17,898 | 13,088 | 19,867 | 16,637 | 13,088 | 27,485 |
  | REGN10987 | 10,837 | 19,888 | 23,686 | 23,265 | 19,888 | 31,479 |
  | S309 | 0 | 32,602 | 32,768 | 32,768 | 32,602 | 32,650 |

  再取“有拟合值”或“通过”与 `is_non_binder` 的并集，得到 32,720 / 32,339 / 32,350 / 32,768（有拟合值 ∪ 非结合）与 32,717 / 32,038 / 32,333 / 32,768（≥1 rep 通过 ∪ 非结合）。九种口径没有一种等于论文数字，且差距方向一致：发布表在四个抗体上都给出 **更多**可用变体（最接近的一种仍分别多 117、4,854、871、118）。因此差异不是某处少读了一列，而是论文的分析与本次发布之间在判据或流程版本上不同。旁证是同一流程对 ACE2 的输出确实会因是否剔除 `SE > 1` 的拟合而产生不同的可用数（见“兄弟交付的元数据表”）。本次不动发布值，也不假定哪一侧为准。下一步：请作者说明论文计数的确切判据与所用表格版本，或确认中间过滤步骤。关闭条件为取得可复算的一致口径，并在正文写明发布表与论文数字的对应关系。
- `Q04`（最近更新：2026-09-28；待 root 清理）：`2026-09-27` 那轮以 root 身份执行留下两个对普通用户不可读的目录：`.staging/rootlocked-20260927-staging.partial` 与 `cache/.../snapshot-2023-11-10/rootlocked-20260927-repository.git`。它们只含上一轮同身份的 payload 与 bare cache，当前对发布内容没有作用。非空且无写权限，本账号无法自行删除；已在脚本中修掉产生该问题的 `mktemp -d` 模式，重跑不再复现。下一步：由具备 root 的执行者删除这两个目录（`chmod -R g+rwX` 后删除，或直接以 root 删除）。关闭条件为两个目录清除，`.staging/` 下不再留 root 锁定的残留。
- `Q06`（最近更新：2026-09-28；部分到位）：`Analyze/Landscape/Phylogeny.ipynb` 与 `data/fig4_phylogeny.csv` 依赖 GISAID 的 SARS-CoV-2 系统发生集合（EPI_SET ID `EPI_SET_20220615uq`，截至 2022-06-15）。该集合的补充表已随兄弟交付取得（`Supplementary_Files/Supplementary_File_7_gisaid_supplemental_table_epi_set_20220615uq.pdf`），但完整系统发生树仍需 GISAID 注册与同意条款，本次未申请。缺少完整输入不影响亲和力表的使用，只影响该图的独立复现。下一步：需要复现该图时按 GISAID 流程申请。关闭条件为取得该 EPI_SET（或作者提供的等价输入）并记录获取方式与条款。
- `Q07`（最近更新：2026-09-28；非接入发布阻塞）：上游未特别说明覆盖仓库数据的许可， R71 仓库无 `LICENSE`，GitHub 元数据 `license` 为 `null`。兄弟交付的 `LICENSE` 为 MIT（Copyright (c) 2022 Thomas Dupic），按其文本只覆盖该仓库的 Software，即流程代码，不能据此推断 R71 仓库的数据、也没有覆盖本 source 的亲和力表。论文正文的 CC BY 4.0 只覆盖论文文本。已核实的事实与分层情况写在“许可和再分发边界”。该未说明事项不阻塞本次公开入口的接入发布；AI 研究、衍生数据、对外再分发与商用的具体条件仍不明确。下一步：作者或正式条款提供覆盖相应对象的许可。关闭条件为获得明确覆盖数据与代码且能确定使用与再分发范围的条款或作者授权。
