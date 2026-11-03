---
tags:
  - context
---

# SRC_R50_GRAPHINITY 数据说明

## 数据集身份

- `source_id`：`SRC_R50_GRAPHINITY`
- `source_version`：`v1`
- 原作者或发布机构：Alissa M. Hummer、Constantin Schneider、Lewis Chinery、Charlotte M. Deane；Oxford Protein Informatics Group。

## 实验设计和数据口径

Graphinity 是抗体–抗原结合自由能变化（ΔΔG）预测研究。公开数据同时包含实验派生 benchmark 与计算生成的合成标签，二者必须分开建模和报告。

Experimental_ddG_645 来自 AB-Bind：645 个单点突变、29 个复合物。论文和固定 Git 包使用 ΔΔG = ΔG_WT − ΔG_mutant，因此负值表示突变削弱结合；27 个 non-binder 被人为赋值为 −8 kcal/mol，5 个复合物不是抗体–抗原体系，3 个相同突变有不同实验值。单独下载的 `Experimental_ddG_645.tar.gz` 保留了反号的上游表：范围 −1.57–8 kcal/mol，27 个 non-binder 是 +8；其数值与 Git 包 study CSV 逐行合并前必须显式换号。reverse mutation 是由原记录生成的反向样本，不是新增独立实验。Experimental_ddG_608 是从 SKEMPI 2.0 筛选的 608 个单点突变、44 个结构复合物，其独立归档和 Git study CSV 均按论文符号保存。

Synthetic_FoldX_ddG_942723 有 942,723 行、1,471 个复合物表示和 1,409 个来源 PDB ID；Synthetic_FlexddG_ddG_20829 有 20,829 行、1,302 个复合物表示和 1,246 个来源 PDB ID。两者从 SAbDab 结构的界面位点生成单点突变，分别由 FoldX 和 Rosetta Flex ddG 计算。FoldX/Flex 标签是计算结果，不是实验测量；负值同样表示预测的 destabilizing mutation。Flex ddG 使用 Rosetta 2020.08+release.cb1caba、nstruct=1，研究标签为 Talaris2014 结果经 GAM 重加权后的值。

论文配套的 CDR sequence-identity folds、随机 folds、dataset-size/diversity/noise 实验文件是既有记录的划分或扰动。它们不能当作额外独立抗体样本；训练/评价应按来源复合物和作者 split 控制泄漏，并保留实验与合成两种标签域。

## 论文原文

- 标题：Investigating the volume and diversity of data needed for generalizable antibody–antigen ΔΔG prediction
- 作者：Alissa M. Hummer；Constantin Schneider；Lewis Chinery；Charlotte M. Deane。
- 载体与版本：Nature Computational Science 5, 635–647 (2025)，Version of Record。
- 发布日期：2025-07-08。
- DOI：`10.1038/s43588-025-00823-8`
- PMID / PMCID：PMID 40629090 / PMCID PMC12374841。
- 本地主文：`articles/GRAPHINITY_2025-07-08_Nature-vor.pdf`
- 文件大小：4941387 bytes；16 页。
- SHA-256：`cae7a513ac4c99db05ef344e3b0ffc2cdceed6fbd174c0045b287631e5b310b7`
- 文本许可：主文末页标明 CC BY 4.0，© The Author(s) 2025。
- 补充材料：Supplementary Information、Reporting Summary、Peer Review File 各一份；Figure 2–4 Source Data 另以三份 ZIP 保存。

论文 PDF 集合如下。

| 文件 | bytes | 页数 | SHA-256 |
| --- | --- | --- | --- |
| articles/43588_2025_823_MOESM1_ESM.pdf | 3537109 | 13 | `16b65a60e1563c5a02b5c1bb7e47f53c3f1b7957d972e6c657914048e18a6722` |
| articles/43588_2025_823_MOESM2_ESM.pdf | 1868875 | 3 | `608f6cddecf34ab46b07a8be84fe6258b8c44b81e236d26d1cb70b478f7efab4` |
| articles/43588_2025_823_MOESM3_ESM.pdf | 223292 | 23 | `7682ee3f1e8896b7c997877e19e907b80f94edfac9925385c397439bb4188d5b` |
| articles/GRAPHINITY_2025-07-08_Nature-vor.pdf | 4941387 | 16 | `cae7a513ac4c99db05ef344e3b0ffc2cdceed6fbd174c0045b287631e5b310b7` |

## 仓库内容

一手入口包括 [Nature 论文页](https://www.nature.com/articles/s43588-025-00823-8)、[Zenodo 记录](https://doi.org/10.5281/zenodo.15384945)、Oxford 作者下载站，以及 GitHub 仓库固定 commit `281a72fde123d89bf29a50a73fc787f5d355e1b9`。作者 README 明确说明 FoldX mutant PDB 包因体积限制不在 Zenodo；208,666,883,874-byte 完整对象来自 Oxford 作者站，不能用 toy 包或 parquet 子集替代。`v1` 是本接入流程对该组明确对象使用的版本名；每个远端对象另以 URL、官方 MD5 或 HTTP identity、本地 SHA-256 固定。

```text
v1/
├── articles/                         # 主文和三份附属 PDF
├── Graphinity/
│   ├── 43588_2025_823_MOESM4_ESM.zip
│   ├── 43588_2025_823_MOESM5_ESM.zip
│   ├── 43588_2025_823_MOESM6_ESM.zip
│   ├── Graphinity-281a72f....tar.gz  # 固定 Git commit
│   ├── Experimental_ddG_608.tar.gz
│   ├── Experimental_ddG_645.tar.gz
│   ├── Synthetic_FoldX_ddG_942723.csv
│   ├── Synthetic_FlexddG_ddG_20829.csv
│   └── synthetic_*_pdbs.tar.gz       # WT/突变结构归档
└── pdb/
    ├── sequences/                    # RCSB 完整 entry FASTA
    └── structures/                   # RCSB 完整 mmCIF
```

归档保持上游压缩格式，不把约 768 GB 展开后的 FoldX 突变坐标复制进 raw tree。Git 固定包包含论文代码、划分文件、README 和 BSD 3-Clause 顶层许可证；作者 HTTP 包与 Zenodo 对象是独立数据交付，不能仅凭代码许可证推定全部对象的许可。

## 数据结构

### 四个数据族

Experimental_ddG_645/608 独立归档含实验派生 CSV 和 wild-type/mutant PDB 快照；Git 固定包另含论文实际使用的 study CSV 与划分文件。两份合成 CSV 是完整标签表；四个 synthetic structure tar.gz 分别覆盖 FoldX/Flex ddG 的 WT 和 mutant 坐标。论文 Source Data ZIP 保存图中预测、fold 和统计所用表，Git 固定包保存代码与重复的分析输入；这些副本用于复现和溯源，不能把同一 mutation 重复计数。

### 字段说明

| 文件 | 字段 | 表示、单位、方向与来源 |
| --- | --- | --- |
| Synthetic_FoldX_ddG_942723.csv | pdb; complex; ab_chain; ag_chain | 来源结构 ID、突变构建体 ID、抗体链和抗原链；complex 不是新的 PDB accession。 |
| Synthetic_FoldX_ddG_942723.csv | foldx_ddg; wt_foldx_dg; mut_foldx_dg | FoldX 计算值，kcal/mol；foldx_ddg 范围 −97.9287–28.8267，负值表示 destabilizing。 |
| Synthetic_FlexddG_ddG_20829.csv | pdb; complex; ab_chain; ag_chain | 来源结构/构建体/链标识；20,829 行均有这些键。 |
| Synthetic_FlexddG_ddG_20829.csv | flexddg_ddg; flexddg_ddg-talaris2014-gam; flexddg_ddg-talaris2014; wt_flexddg_dg-talaris2014; mut_flexddg_dg-talaris2014 | Flex ddG 计算输出；研究标签是 GAM 值，kcal/mol；不能把能量分量当实验 affinity。 |
| Git / Experimental_ddG_645.csv | pdb; complex; labels; chain_prot1; chain_prot2; ab_chain; ag_chain | 论文 study CSV；labels 范围 −8–1.57 kcal/mol，负值表示 destabilizing，27 个 non-binder 为 −8。 |
| 独立 Experimental_ddG_645 归档 CSV | #PDB; Partners(A_B); Protein-1; Protein-2; Mutation; labels; type; complex_orig; complex; chain_prot1; chain_prot2 | 上游反号表；labels 范围 −1.57–8，27 个 non-binder 为 +8。不能不换号就与 study CSV 混合。 |
| Experimental_ddG_608 CSV | pdb; complex 或 mut_id; labels; chain_prot1; chain_prot2; ab_chain; ag_chain | 608 行实验派生 ΔΔG，范围 −7.4197–4.9116 kcal/mol；独立归档与 Git study CSV 数值方向一致。 |
| Source Data ZIP | wt_pdb; mut_pdb; pred_score; true_label 等 | 论文图所用模型预测与标签；同一 mutation 可跨模型/fold 出现。空 CSV 占位文件原样保留。 |

### 数据示例

| 数据族 | pdb | complex | 抗体链 | 抗原链 | 标签 |
| --- | --- | --- | --- | --- | --- |
| FoldX | 1adq | 1adq_DH31A | HL | A | foldx_ddg = −1.81336 |
| Flex ddG | 1ahw | 1ahw_BA_C_NC160F | BA | C | flexddg_ddg = −2.64288 |

两行均是计算生成的单点突变记录。FoldX 表中 `(pdb, complex)` 有 76 组重复键，例如 7L7E 的同一突变可对应不同抗体链和不同能量；应把 `ab_chain`、`ag_chain` 纳入身份键。不要只按行随机划分。

## PDB 数据库

合成 FoldX 表列出 1,409 个上游 PDB ID。2026-09-19 从 RCSB 保存完整 entry FASTA 与完整 mmCIF，并逐对核对 entry ID、entity 序列和原子可读性。当前取得 1,399 个仍有效的原 ID pair；10 个 ID 已由 RCSB 标为 REMOVED，其中 9 个有 replacement，形成 9 条替代映射。两个 replacement 已同时出现在有效原 ID 集合中，因此磁盘上共有 1406 个不同 PDB entry pair。7CU4 无 replacement，保留不可取得证据，不用相似结构补造。

| 原 PDB ID | RCSB 状态 | 替代 PDB ID | 处理 |
| --- | --- | --- | --- |
| 3L5Y | REMOVED | 4PS4 | 替代 pair 已验收 |
| 3RVV | REMOVED | 5VPL | 替代 pair 已验收 |
| 4NX3 | REMOVED | 4WEB | 替代 pair 已验收 |
| 4K4M | REMOVED | 4QEX | 替代 pair 已验收 |
| 4WGV | REMOVED | 5M94 | 替代 pair 已验收 |
| 4WGW | REMOVED | 5M95 | 替代 pair 已验收 |
| 5USI | REMOVED | 6B9J | 替代 pair 已验收 |
| 6ERX | REMOVED | 6FXN | 替代 pair 已验收 |
| 7CU4 | REMOVED | 无 | 记录为不可取得 |
| 7N0S | REMOVED | 7R98 | 替代 pair 已验收 |

RCSB 文件用于来源 ID、序列和完整实验 entry 的参考锚定。作者结构归档中的 WT/突变 PDB 是计算流程使用的重编号、修复或突变坐标快照；它们与当前 RCSB entry 不是逐字节等价物，模型复现应使用作者归档，数据库身份检查可使用 `pdb/` pair。

## 使用方式

调用者先把 dataset_root 设为本 source version 目录。直接读取两份合成标签表；大结构包按需流式枚举，不要为查看 CSV 先整体解包。

```python
from pathlib import Path
import csv
import tarfile

dataset_root = Path(dataset_root)
with (dataset_root / "Graphinity/Synthetic_FoldX_ddG_942723.csv").open(
    newline="", encoding="utf-8-sig"
) as stream:
    first_mutation = next(csv.DictReader(stream))

archive_path = dataset_root / "Graphinity/synthetic_foldx_ddg_wt_pdbs.tar.gz"
with tarfile.open(archive_path, "r|gz") as archive:
    first_member = next(member for member in archive if member.isfile())
```

字段值保持上游字符串/浮点表示；reverse mutation、non-binder 特殊值和 split 文件需按具体实验配置解释。若使用独立 645 结构归档中的 CSV，先记录换号规则再与 Git study CSV 对齐，不能把 +8 和 −8 当成两类独立观测。

## 采集过程记录

1. 2026-09-18 至 2026-09-19 核验项目/开发者/存储配置，确认正式流程为 `onboarding_50_55` 的 `v1`，不执行旧的重复配置。
2. 从 publisher 保存主文、三份附属 PDF 和三份 Source Data ZIP；从 GitHub 固定 commit 下载 tar.gz；从 Zenodo 按官方大小和 MD5 下载五个对象。
3. 从 Oxford 作者站取得两份实验归档和 208,666,883,874-byte FoldX mutant 结构包；作者 README 明确说明后者因体积限制未进入 Zenodo。站点未给这三份对象独立 checksum；保存 ETag/Last-Modified，并在完成后冻结本地 SHA-256。主下载器从文件头向后、curl 辅助器从文件尾反向领取不重叠 range；两者都要求精确 206 Content-Range/相同 ETag，失败重试不拼接返回 200 的错误响应。
4. 全量流式审计 tar/zip 成员路径、链接/特殊对象、展开体积、CSV 行列和 PDB 可解析性；发现 Git 包中的零字节 CSV 占位后按空表记录，没有把它判成损坏或填充内容。
5. FoldX/Flex 两份完整标签 CSV 分别核验 942,723/20,829 行、字段、空值、非有限值、PDB 分布和数值范围；发现 FoldX 的 `(pdb, complex)` 有 76 组跨抗体链重复键，保留全部行并要求使用链字段区分。
6. 比较独立实验归档与 Git study CSV；确认 645 独立归档的标签整体采用相反方向（含 +8 non-binder），608 数值方向一致。raw 文件未改写，README 明示转换边界。
7. 对 1,409 个来源 PDB ID 查询 RCSB；1,399 个现存 ID 与 9 个 replacement 映射通过 FASTA/mmCIF 双层校验，7CU4 记录为已撤销且无替代。移除只有坐标、没有配对 FASTA 的旧撤销 ID 残留，不把不完整 pair 纳入交付。
8. README 从审计 JSON 生成并立即同步共享 source；固定版本 markdownlint、精确 inventory、文件 SHA-256、归档格式和 PDB pair 均通过后再原子发布。

## 参考文献

- [Hummer et al. 2025，Nature Computational Science 主文与补充材料](https://doi.org/10.1038/s43588-025-00823-8)。
- [Graphinity 数据记录，Zenodo 10.5281/zenodo.15384945](https://doi.org/10.5281/zenodo.15384945)。
- [Graphinity 固定代码来源，oxpig/Graphinity](https://github.com/oxpig/Graphinity/tree/281a72fde123d89bf29a50a73fc787f5d355e1b9)。
- [SAbDab：结构化抗体数据库](https://doi.org/10.1093/nar/gkt1043)。
- [AB-Bind](https://doi.org/10.1002/pro.2692) 与 [SKEMPI 2.0](https://doi.org/10.1093/bioinformatics/bty635)。
- [RCSB PDB 数据访问与 entry 状态](https://www.rcsb.org/)。

## 其他

### 完整性与验收

交付清单含 2828 个文件（README 不计）、227493977848 bytes：16 个论文/代码/数据对象，以及 1406 个不同 RCSB entry 的 FASTA/mmCIF pair。按“相对路径、bytes、单文件 SHA-256”排序生成的 inventory SHA-256 为 `558fcceddd698d36c2cbc2cbdbd0ead658e9f2b1bac6df25d744291ed54cc850`。这是一项本地集合摘要，不冒充上游 checksum。

大型数据对象身份如下；论文 PDF 的身份列在“论文原文”。

| 相对路径 | bytes | SHA-256（本地计算） |
| --- | --- | --- |
| Graphinity/43588_2025_823_MOESM4_ESM.zip | 126281909 | `71e5cbb18ff47ae1867bb4361cae6fe955e84e2b9129923a1e22a13e31765ef1` |
| Graphinity/43588_2025_823_MOESM5_ESM.zip | 18582715 | `7a5d199b6698820e05783b94749a626c9c4f46c44c44a42b3f865df89a55f409` |
| Graphinity/43588_2025_823_MOESM6_ESM.zip | 120933700 | `4da360a64bfffd4e9af72dfef8013e16e3ebb103efebb2187740579c1aadbe0c` |
| Graphinity/Graphinity-281a72fde123d89bf29a50a73fc787f5d355e1b9.tar.gz | 286704350 | `fcb73a6e7be95709098dd632493d84e2483f84b1cb846b9d92d61f312e32a843` |
| Graphinity/synthetic_flexddg_ddg_mutated_pdbs.tar.gz | 8281241307 | `e9ff9b82b42710fb097230c1612fb91586d244974a47c2ed88cc50aea3902add` |
| Graphinity/Synthetic_FlexddG_ddG_20829.csv | 1955658 | `ca11584ebb8a11e4aafa8a8421d9cddafa92cf29dd2546fd5d350871552f3fc6` |
| Graphinity/Synthetic_FoldX_ddG_942723.csv | 53363843 | `0b631278c33e018cddb0d68f9af7872b7e1294593caf334129ddda89134fd27d` |
| Graphinity/synthetic_flexddg_ddg_wt_pdbs.tar.gz | 8281133116 | `358d699d189e9bc6e5d72e307313c372fecf00ed7575eb05797eb11561e4bad8` |
| Graphinity/synthetic_foldx_ddg_wt_pdbs.tar.gz | 317331389 | `6e0b0cc593ca9204819fd820cbe1bf24bf1954ce8645afad25b0e12ff10eb1b1` |
| Graphinity/Experimental_ddG_608.tar.gz | 73861669 | `84b58ae40a20bde50caa1f6e6d18847bafa0bf63f8ba9deacf8724b808c228c0` |
| Graphinity/Experimental_ddG_645.tar.gz | 74925449 | `7a1eb5602bb6e554f0b636b763b98acb8162d28063b781df368fbbf08a889f3d` |
| Graphinity/synthetic_foldx_ddg_mutated_pdbs.tar.gz | 208666883874 | `a6d07921551783981ffcc4ce939846941aa844aa12bf2f207cf3a763cc91e97a` |

### 许可和再分发边界

主文及其 CC BY 4.0 范围内材料按论文 credit line 执行；Zenodo 记录标为 CC BY 4.0。Git 顶层代码许可证为 BSD 3-Clause，第三方子目录另有各自许可证。Oxford 作者下载站的实验/大结构归档未发现独立 checksum 或单独许可声明，因此保留原 URL、HTTP identity、论文/数据引用和本地 hash，不把 Git 代码许可证自动扩展到这些数据包。PDB 文件遵守 wwPDB/RCSB 引用政策。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 645/608 实验派生 benchmark | 两份完整作者归档、Git 固定副本与论文说明；645 的相反符号已标明 | 已包含 |
| 942,723 FoldX 标签及 WT/mutant 坐标 | 完整 CSV、WT 归档和 208.67 GB mutant 归档 | 已包含 |
| 20,829 Flex ddG 标签及 WT/mutant 坐标 | 完整 CSV和两个约 8.28 GB 归档 | 已包含 |
| 论文 Figure 2–4 复现数据 | 三份 publisher Source Data ZIP | 已包含 |
| 1,409 个历史来源 PDB ID | 1,399 个现存原 ID；9 条 replacement；7CU4 无替代 | 一项不可取得并已显式记录 |
| 新的实验 affinity 测量或仪器 raw | 本来源是既有实验派生和计算数据；无新增仪器记录 | 不在来源范围 |
