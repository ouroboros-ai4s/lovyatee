---
tags:
  - context
---

# SRC_R79_ALPHABIND 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [AlphaSeq 实验表](#alphaseq-实验表)
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

- `source_id`：`SRC_R79_ALPHABIND`
- `source_version`：`snapshot-2025-07-24`
- 原作者或发布机构：A-Alpha Bio, Inc. 的 AlphaBind 研究团队；论文另有 NVIDIA 作者参与。

### 来源方背景

论文作者单位将主要作者列在美国西雅图 A-Alpha Bio 的 Data Science 部门，另列 NVIDIA Healthcare & Life Sciences 部门。该来源由 A-Alpha Bio 的 [AlphaBind 仓库](https://github.com/A-Alpha-Bio/alphabind)发布；本说明只据论文和仓库确认其与数据直接相关的研究和发布角色。

## 实验设计和数据口径

AlphaBind 论文利用大规模 AlphaSeq 蛋白互作数据预训练模型，并在抗体优化活动中以较小的公开 AlphaSeq 表做微调和验证。当前包只含这 8 张微调/验证 CSV，不含论文提及的数百万条预训练实验记录。每行是一组 Mat-A 展示候选抗体与 Mat-Alpha 展示靶标的蛋白互作记录；不是一个独立抗体、原始测序 read 或直接测得的摩尔浓度。每张表的 Mat-Alpha 靶标说明在文件内固定，Mat-Alpha 完整序列未逐行重复，需参照论文表 S1。

`alphaseq_affinity` 是 AlphaSeq 报告的 `log10(KD / nM)`；数值越小，对应的解离常数越小、结合越强。空值不是零。`parental_mean_aff` 是亲本重复测量的均值；`parental_aff_margin` 为当前行与亲本均值之差。验证表另外含模型预测值和提出候选的模型标识；预测值与 AlphaSeq 测量值不能混作同一标签。相同序列、亲本和靶标可能跨表或模型重复，不能把所有行当作独立生物样本。

| 文件组 | 文件数 | 记录数 | 有 `alphaseq_affinity` 的记录 |
| --- | ---: | ---: | ---: |
| fine-tuning | 3 | 86,798 | 81,859 |
| validation | 5 | 123,126 | 119,828 |
| 合计 | 8 | 209,924 | 201,687 |

## 论文原文

- 标题：AlphaBind, a domain-specific model to predict and optimize antibody-antigen binding affinity
- 作者：Aditya A. Agarwal、James Harrang、David Noble 等。
- 发表来源：*mAbs*，2025。
- 归档文本版本：PMC Version of Record，PMC12296056.1 的 JATS XML。
- 发布日期：2025-07-22。
- DOI：<https://doi.org/10.1080/19420862.2025.2534626>
- PMID / PMCID：40693434 / PMC12296056。
- 本地文件：`articles/AlphaBind_2025-07-22_mAbs-PMCv1.xml`
- 文件大小：129.7 KiB（132792 bytes）。
- SHA-256：`4f102492b58cd3709b612a5b518a8923b71789dc5f17dbb7cf5e4ef23ec90992`
- 文本许可：论文 XML 标明 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)；不据此推定 CSV 的许可。
- 补充材料：`articles/AlphaBind_supplementaryFiles.zip`，1.50 MiB（1576108 bytes），SHA-256 `522841ad004e3da9de7df0fec1d3b5a48affb83bdb052c866b2c20f738efde7c`；包含靶标等补充说明。

## 仓库内容

上游为 [A-Alpha Bio/alphabind](https://github.com/A-Alpha-Bio/alphabind)，固定 Git commit [`15d2582fb0d5c39fb0d479120cf109cbc0a6a554`](https://github.com/A-Alpha-Bio/alphabind/tree/15d2582fb0d5c39fb0d479120cf109cbc0a6a554)。`source_version` 采用该上游快照对应的 2025-07-24 日期；这里只归档论文相关的 AlphaSeq 数据目录，不代表完整代码仓库快照。Git blob ID 用于逐文件核验。

```text
snapshot-2025-07-24/
└── alphabind/
    └── manuscript/data/alphaseq/
        ├── README.md
        ├── fine-tuning/ (3 CSV)
        └── validation/ (5 CSV)
```

上游 `README.md` 提供字段定义。CSV 以原始文件名和原始字节保存，没有清洗或换算。

## 数据结构

### AlphaSeq 实验表

微调表分别覆盖 `aab-pp489`、`pembrolizumab-scfv`、`vhh72`；验证表另含 `trastuzumab-scfv-cdr` 和 `trastuzumab-scfv-full` 两种优化范围。微调表均为 7 列，验证表均为 11 列。8 个文件不是互斥划分的样本 ID 集；`id` 只在所属验证数据集内解释，不用作跨文件连接键。

| 活动 | 微调行数 | 验证行数 |
| --- | ---: | ---: |
| aab-pp489 | 26,913 | 37,346 |
| pembrolizumab-scfv | 29,897 | 37,489 |
| vhh72 | 29,988 | 37,070 |
| trastuzumab-scfv-cdr | 无 | 3,681 |
| trastuzumab-scfv-full | 无 | 7,540 |

### 字段说明

以下原始列名已逐一对照 8 张 CSV；空字符串表示未报告，不得当作零。除特别说明外，数值来自 AlphaSeq 实验或论文定义的派生量。

| 原始字段 | 适用文件 | 表示与含义 |
| --- | --- | --- |
| `mata_description` | 全部 | Mat-A 展示候选的文本标识；非全局唯一键。 |
| `matalpha_description` | 全部 | Mat-Alpha 展示靶标构建体的文本标识；每表扫描到 1 个取值。 |
| `alphaseq_affinity` | 全部 | AlphaSeq 报告的浮点 `log10(KD / nM)`；越小结合越强，可为空。 |
| `mata_sequence` | 全部 | Mat-A 候选氨基酸一字母序列；Mat-Alpha 序列不在表内。 |
| `edit_distance` | 全部 | 与亲本抗体序列的 Levenshtein 编辑距离，非亲和力单位。 |
| `parental_mean_aff` | 全部 | 亲本重复实验的平均 AlphaSeq 亲和力，与 `alphaseq_affinity` 同量纲。 |
| `parental_aff_margin` | 全部 | `alphaseq_affinity - parental_mean_aff`，越小表示相对亲本更强；测量缺失时为空。 |
| `predicted_affinity` | 验证 | 由 `model` 给出的预测亲和力，与实验列分开使用；可为空。 |
| `avg_off_target_affinity` | 验证 | 上游文件附带的平均脱靶亲和力；当前上游字段说明未定义聚合对象，保留原值，可为空。 |
| `model` | 验证 | 候选生成/预测模型：`ohe_cold`、`ohe_warm`、`esm_cold`、`esm_warm`、`alphabind`；部分对照行为空。`cold` 为无预训练，`warm` 为有预训练；`alphabind` 为论文完整模型。 |
| `id` | 验证 | 同一 AlphaSeq 数据集内的候选数值标识；对照行可为空。 |

### 数据示例

`aab-pp489_fine-tuning_alphaseq.csv` 的首行：`mata_description=candidate_0`，`matalpha_description=TIGIT_22-137_POI-AGA2`，`alphaseq_affinity=1.5485445307761552`，`edit_distance=1`，`parental_mean_aff=0.5127171697138021`，`parental_aff_margin=1.0358273610623532`。该行是一条候选与指定靶标的互作记录；其序列保留在原 CSV 的 `mata_sequence` 列。

## PDB 数据库

论文活动与已知结构有 5 个可辩护的参考锚点：`1n8z`（trastuzumab-HER2）、`3udw`（TIGIT 与配体 PVR）、`5jxe`（pembrolizumab-PD-1）、`6lzg`（SARS-CoV-2 RBD-ACE2）及 `6waq`（VHH72-SARS-CoV-1 RBD）。其中 `3udw` 和 `6lzg` 是靶标/受体参考复合物，并非当前 CSV 候选抗体的逐行结构；其余锚点也不与每条变体逐行对应。链角色未建立逐行映射，故保存完整 entry FASTA 和 mmCIF，没有生成带推定角色的选链序列。

RCSB 原始 entry FASTA 保存在 `pdb/sequences/rcsb_pdb_<id>.fasta`，完整坐标保存在 `pdb/structures/<id>.cif`。5 个锚点均有两类文件，共 10 文件、4.32 MiB（4530515 bytes）。按相对路径排序，将每行 `relative_path<TAB>bytes<TAB>sha256<LF>` 拼接后取 SHA-256，得 `6cf8da352ab340c59fcc700194f3389687be27f5b1425a6749267d34de3fcd50`。获取于 2026-10-29，入口分别为 `https://www.rcsb.org/fasta/entry/<id>/download` 与 `https://files.rcsb.org/download/<id>.cif`。

## 采集过程记录

- 2026-10-29：以固定 commit 的 Git blob 大小及对象哈希获取 8 个 CSV 和上游说明文件到 `G:\abag-datasets\SRC_R79_ALPHABIND\.staging`；保留原字节。
- 2026-10-29：归档 PMC 正式版 XML 及补充 ZIP；论文文本和数据文件分别核验身份，不把论文许可套用于数据。
- 2026-10-29：按论文活动检查 PDB 锚点，从 RCSB 取得 5 组原始 FASTA/mmCIF；结构只用于参考，不生成逐行抗体结构映射。
- 2026-10-29：扫描全部 8 张 CSV，记录 209,924 行及缺失值；执行 Git blob 验收与 PDB inventory 校验，并以同盘重命名发布本地版本。

## 参考文献

- [AlphaBind 固定 commit](https://github.com/A-Alpha-Bio/alphabind/tree/15d2582fb0d5c39fb0d479120cf109cbc0a6a554)及其 [`AlphaSeq Data Guide`](https://github.com/A-Alpha-Bio/alphabind/blob/15d2582fb0d5c39fb0d479120cf109cbc0a6a554/manuscript/data/alphaseq/README.md)。
- [Agarwal 等，*mAbs* 2025](https://doi.org/10.1080/19420862.2025.2534626)；[PMC 正文与补充材料](https://pmc.ncbi.nlm.nih.gov/articles/PMC12296056/)。
- [RCSB PDB](https://www.rcsb.org/)：`1n8z`、`3udw`、`5jxe`、`6lzg`、`6waq`。

## 其他

### 数据范围和限制

该包是论文公开的 AlphaSeq 微调与验证实验子集，不是全部预训练记录；它也不是从原始仪器输出重建的实验 raw data。候选、测量和模型预测的粒度不同，跨表去重及划分需另行设计。

### 完整性与验收

上游 9 个选定文件均符合固定 commit 的 Git blob 身份；8 个 CSV 均可读取，列头分别与 7/11 列规范相符。PDB 参考锚点 5/5 同时具有 FASTA 和 mmCIF。论文补充 ZIP 和 XML 已归档。该结论是已公开包的接入验收，不代表论文全部实验数据已取得。

### 许可和再分发边界

仓库根 [`LICENSE`](https://github.com/A-Alpha-Bio/alphabind/blob/15d2582fb0d5c39fb0d479120cf109cbc0a6a554/LICENSE)为 MIT，文本称覆盖软件及相关文档；尚不能仅据此断言实验 CSV 的商用、衍生及再分发授权。论文 XML 为 CC BY-NC 4.0；RCSB 补充文件另循其来源条款。上游未特别说明覆盖本批实验 CSV 的独立许可，使用与再分发范围不明确。公开下载且未发现与本地 source package 接入冲突的明确条款，因此不阻塞本次本地发布；后续对外再分发或商用判断仍待明确。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 数百万条 AlphaSeq 预训练测量 | 当前固定目录只有 8 张微调/验证 CSV | 未取得预训练全量 |
| 公开的微调与验证实验表 | 8 CSV、209,924 行，201,687 行有实验亲和力 | 本批已验收 |
| 实验活动的参考结构 | 5 个参考锚点各有 FASTA/mmCIF | 已补充，非逐行映射 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-29；不阻塞本地接入）：公开实验 CSV 的独立许可及商用、衍生、再分发范围尚不明确。已核查仓库 MIT 文本和论文 CC BY-NC 4.0；当前按公开包保存并限制后续权利推断。取得来源方明确覆盖 CSV 的条款后关闭。
- `Q02`（最近更新：2026-10-29；影响字段解释）：上游 AlphaSeq Data Guide 未定义验证表 `avg_off_target_affinity` 的靶标集合和聚合规则。当前仅保留原字段，不作统一脱靶标签；取得论文补充方法或作者定义后关闭。
