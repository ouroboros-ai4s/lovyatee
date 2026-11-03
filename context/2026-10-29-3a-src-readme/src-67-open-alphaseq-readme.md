---
tags:
  - context
---

# SRC_R67_OPEN_ALPHASEQ 数据说明

## 数据集身份

- `source_id`：`SRC_R67_OPEN_ALPHASEQ`
- `source_version`：`snapshot-2025-12-04`
- 原作者或发布机构：A-Alpha Bio Inc.（Open AlphaSeq 维护团队）

### 来源方背景

[A-Alpha Bio 官方介绍](https://www.aalphabio.com/about/)将该机构描述为一家位于美国西雅图的生物技术公司，2017 年成立于华盛顿大学 Institute for Protein Design 和 Center for Synthetic Biology。公司以合成生物学和机器学习测量、预测及工程化蛋白质相互作用；AlphaSeq 是其高通量实验平台，AlphaBind 是以蛋白质相互作用数据训练的预测平台。本数据集由 A-Alpha Bio 在 Hugging Face 正式发布，九项实验的数据卡分别关联 2022 年的 SARS-CoV-2 抗体研究和 2025 年的 AlphaBind 研究。

## 实验设计和数据口径

### 九项实验与记录粒度

AlphaSeq 将待测蛋白分别展示在两种酵母交配型 MATa 和 MATα 的细胞表面。一次成功交配把两侧构建体的条形码带到同一个二倍体细胞中；测序得到的配对条形码计数经对照、重复和标定步骤转为相互作用亲和力估计。当前公开文件是处理后的配对结果，没有包含逐样本原始测序 reads、逐条形码计数矩阵或拟合中间量。

每行表示一个 MATa 构建体描述与一个 MATα 构建体描述的实验组合。描述后缀可标记技术重复、设计方法或突变；同一氨基酸序列因此会出现多行。九张表合计 1,705,908 行，完整行级哈希审计未发现完全重复行。表中的 1,378,079 行有有限的 `alphaseq_affinity`，其余 327,829 行没有点估计，数据卡将这种缺失解释为没有观察到该蛋白对的细胞融合或配对条形码 reads。

| 实验 | 设计范围 | 行数 | MATa 唯一非空序列 | MATα 唯一非空序列 | 有亲和力点估计 |
| --- | --- | ---: | ---: | ---: | ---: |
| `YM_0005` | 抗冠状病毒抗体面板 × SARS-CoV-2 RBD 单点突变库 | 163,882 | 62 | 2,431 | 96,855 |
| `YM_0549` | VHH72 Iter0 × 7 个病毒 RBD/相关目标 | 299,910 | 29,765 | 7 | 214,122 |
| `YM_1068` | VHH72 Iter1 × 8 个病毒 RBD/相关目标 | 407,803 | 36,862 | 8 | 288,697 |
| `YM_0693` | PP489 Iter0 scFv × 人/鼠 TIGIT | 134,580 | 26,726 | 2 | 101,204 |
| `YM_0988` | ABC001/PP489 Iter1 scFv × 人/鼠 TIGIT | 186,745 | 35,929 | 2 | 167,740 |
| `YM_0852` | Pembrolizumab Iter0 scFv × PD-1 | 120,208 | 29,883 | 1 | 120,074 |
| `YM_0985` | Pembrolizumab Iter1 scFv × PD-1 | 148,128 | 34,890 | 1 | 144,838 |
| `YM_0989` | Trastuzumab CDR 设计 scFv × HER2 | 94,604 | 20,828 | 1 | 94,576 |
| `YM_0990` | Trastuzumab CDR+framework 设计 scFv × HER2 | 150,048 | 37,077 | 1 | 149,973 |

表中的“唯一序列”对非空氨基酸字符串去重。负对照仍有描述字段，但相应序列为空；各表的描述数、序列数和行数因技术重复与控制组合而不同。`YM_0005` 数据卡将面板概括为 33 个抗体，实际表中有 67 个 MATa 描述和 62 个非空序列，其中包括部分抗体的 HL/LH 两种 scFv 方向、ACE2、VHH 和阴性对照。

### 亲和力估计和质量标记

`alphaseq_affinity` 的定义是 $\log_{10}(K_D/\mathrm{nM})$：数值越小表示估计结合越强。例如 `0` 对应 1 nM，`2` 对应 100 nM。该值来自 AlphaSeq 信号的实验标定和估计，并非逐候选 SPR 或 BLI 测量。九表的有限值范围为 -0.989 至 7.459。

`affinity_upper_bound` 和 `affinity_lower_bound` 是 Wilson score interval 推得的 95% 置信边界。上游将“upper”解释为更强边界，因此在 log10 KD 数值轴上更小；1,378,079 个同时具有点估计和两侧边界的行全部满足 `affinity_upper_bound <= alphaseq_affinity <= affinity_lower_bound`。`affinity_upper_bound` 在全部行中都有值，点估计缺失时仍可用于表达强度边界。

`normalized_affinity` 是对亲和力矩阵按两侧蛋白连续标准化所得的分数，更负表示相对于各自交互分布更具特异性。`above_background` 标记经 Benjamini–Hochberg 校正后相对 assay 背景达到 `q < 0.05` 的组合，共 534,909 行为 `true`。`sufficient_replicate_observations` 标记在超过一半重复样本中被观察到的组合，共 1,000,461 行为 `true`。这些标记描述 assay 观测与统计支持度，不把缺失点估计自动转换为确定的非结合标签。

### 跨实验关系

上游将 Iter0 定义为随机突变或 ESM 选择产生的 zero-shot 设计，将 Iter1 定义为用对应 Iter0 数据训练模型后生成的设计。VHH72、PP489/ABC001 和 Pembrolizumab 的 Iter0/Iter1 应按同一设计活动分组切分；随机拆行会把相同亲本、共享目标和少量完全相同序列分到训练与评价两侧。独立序列集合审计得到：

- `YM_0549` 与 `YM_1068` 共享 27 个 MATa 序列和 7 个 MATα 序列。
- `YM_0693` 与 `YM_0988` 共享 31 个 MATa 序列和 2 个 MATα 序列。
- `YM_0852` 与 `YM_0985` 共享 345 个 MATa 序列和 1 个 MATα 序列。
- `YM_0989` 与 `YM_0990` 共享 200 个 MATa 序列和 1 个 MATα 序列。

`YM_0989` 与 `YM_0990` 都属于 Iter0，但分别限制在 CDR 与扩展到 framework 的设计窗口。`YM_0005` 测试抗原侧 RBD 突变库，其任务方向与固定抗原下比较大量抗体序列的优化实验不同。

### 上游数据卡差异

实际 Parquet 与逐实验 README 有三处会影响使用的差异，本地原文件均未改写：

1. `YM_0985` 数据卡正文称 34,890 个 VHH 和 1 个 RBD；表头、描述前缀、序列形态和目标字段对应 Pembrolizumab scFv 与 PD-1。
2. `YM_0988` 数据卡正文沿用了 Iter0 的 26,726 个 scFv；该表实际有 35,929 个唯一非空 MATa 序列。
3. `YM_0990` 数据卡正文沿用了 20,828 个 VHH 和 `TrastuzumabCDR` 前缀；该表实际有 37,077 个唯一非空 scFv，描述使用 `TrastuzumabFull` 前缀。

此外，`YM_0005` 的 `m396_scFv_LH_Mod` 在 `mata_sequence` 中用 `&` 连接两段序列。通用氨基酸解析器需要先按该已知表示处理，不能静默删除字符。

## 论文原文

### AlphaSeq 方法论文

- 标题：High-throughput characterization of protein–protein interactions by reprogramming yeast mating
- 作者：David Younger、Stephanie Berger、David Baker、Eric Klavins
- 发表来源：Proceedings of the National Academy of Sciences 114(46), 12166–12171
- 归档文本版本：正式发表版 PDF
- 发布日期：2017-10-31
- DOI：[10.1073/pnas.1705867114](https://doi.org/10.1073/pnas.1705867114)
- PMID / PMCID：29087945 / PMC5699035
- 本地文件：`articles/OpenAlphaSeq_2017-10-31_PNAS-FullText.pdf`
- 文件大小：1.26 MiB（1,321,279 bytes）
- SHA-256：`24793159f54cf01a83d258181d098c9aa09c7712f5abfaf8f9c4ddee3a86103d`
- 文本许可：PNAS license；正文公共存档未标为开放再许可
- 补充材料：本 source version 未另存该论文补充材料

这篇论文解释 AlphaSeq/SynAg 的酵母交配、条形码配对和定量标定方法，是九项公开表共同的方法依据。

### YM_0005 数据论文

- 标题：Massively multiplexed affinity characterization of therapeutic antibodies against SARS-CoV-2 variants
- 作者：Emily Engelhart、Randolph Lopez、Ryan Emerson 等
- 发表来源：Antibody Therapeutics 5(2), 130–137
- 归档文本版本：正式发表版 JATS XML
- 发布日期：2022-05-12
- DOI：[10.1093/abt/tbac011](https://doi.org/10.1093/abt/tbac011)
- PMID / PMCID：35769631 / PMC9129155
- 本地文件：`articles/OpenAlphaSeq_2022-05-12_Antibody-Therapeutics-FullText.xml`
- 文件大小：69.06 KiB（70,713 bytes）
- SHA-256：`d549f100094a23cb11a9cb7ff9ff7c5a82f456d657c1ee50159c7a3778cd5d4b`
- 文本许可：CC BY-NC 4.0
- 补充材料：`articles/supplements-2022/` 中 6 个原始成员，合计 2.37 MiB（2,482,655 bytes），包括 3 个 DOCX/JPEG 补充组及其图件

这篇论文对应 `YM_0005` 的抗体面板与 SARS-CoV-2 RBD 深度突变测量。

### AlphaBind 与其余八项实验论文

- 标题：AlphaBind, a domain-specific model to predict and optimize antibody–antigen binding affinity
- 作者：Aishwarya A. Agarwal、Jack Harrang、David Noble 等
- 发表来源：mAbs 17(1), article 2534626
- 归档文本版本：正式发表版 JATS XML
- 发布日期：2025-07-22
- DOI：[10.1080/19420862.2025.2534626](https://doi.org/10.1080/19420862.2025.2534626)
- PMID / PMCID：40693434 / PMC12296056
- 本地文件：`articles/OpenAlphaSeq_2025-07-22_mAbs-FullText.xml`
- 文件大小：129.68 KiB（132,792 bytes）
- SHA-256：`4f102492b58cd3709b612a5b518a8923b71789dc5f17dbb7cf5e4ef23ec90992`
- 文本许可：CC BY-NC 4.0
- 补充材料：`articles/supplements-2025/` 中 2 个 XLSX，合计 39.77 KiB（40,729 bytes）

该论文解释 `YM_0549`、`YM_0693`、`YM_0852`、`YM_0985`、`YM_0988`、`YM_0989`、`YM_0990` 和 `YM_1068` 的模型设计活动。公开 Parquet 是独立的数据交付；论文补充工作簿用于核对研究方法与结果，不能替代九张完整表。

## 仓库内容

上游入口是 [Hugging Face `aalphabio/open-alphaseq`](https://huggingface.co/datasets/aalphabio/open-alphaseq)。本版本固定 revision `3fb6b28b3ee758a7dfeaca5f14949dc505e90fda`；Hugging Face API 给出的 revision 时间为 2025-12-04 02:17:51 UTC，因此发布目录命名为 `snapshot-2025-12-04`。仓库公开且非 gated。

`open-alphaseq/` 是该 revision 的完整 23 文件快照，共 42.61 MiB（44,676,842 bytes），包括 9 张 Parquet、根与逐实验 README、MIT LICENSE、Git/LFS 属性及教程 notebook。目录不包含 `.git/` 对象；大文件身份按 Hugging Face LFS SHA-256 验证，小文本按 Git blob ID 和字节数验证。

```text
snapshot-2025-12-04/
└── open-alphaseq/
    ├── LICENSE
    ├── README.md
    ├── data/
    │   ├── YM_0005/
    │   │   ├── README.md
    │   │   └── data.parquet
    │   ├── YM_0549/ ... YM_0990/
    │   └── YM_1068/
    │       ├── README.md
    │       └── data.parquet
    └── tutorials/
        └── analyze_data.ipynb
```

## 数据结构

### 文件和行数

9 张 `data.parquet` 都采用完全相同的 10 列 schema：前 4 列为 Arrow `large_string`，中间 4 列为 `double`，最后 2 列为 `bool`。每张表只有一个 row group。逐文件行数之和为 1,705,908，与固定 revision 的 Hugging Face 元数据和全表迭代计数一致。

| 文件 | 大小 | 行数 | 唯一序列对 | 完全重复行 |
| --- | ---: | ---: | ---: | ---: |
| `data/YM_0005/data.parquet` | 3.06 MiB（3,207,875 bytes） | 163,882 | 153,216 | 0 |
| `data/YM_0549/data.parquet` | 6.95 MiB（7,286,376 bytes） | 299,910 | 238,128 | 0 |
| `data/YM_0693/data.parquet` | 2.98 MiB（3,124,450 bytes） | 134,580 | 80,181 | 0 |
| `data/YM_0852/data.parquet` | 3.51 MiB（3,679,609 bytes） | 120,208 | 59,768 | 0 |
| `data/YM_0985/data.parquet` | 3.96 MiB（4,153,247 bytes） | 148,128 | 69,782 | 0 |
| `data/YM_0988/data.parquet` | 5.12 MiB（5,372,635 bytes） | 186,745 | 107,790 | 0 |
| `data/YM_0989/data.parquet` | 2.99 MiB（3,132,363 bytes） | 94,604 | 41,658 | 0 |
| `data/YM_0990/data.parquet` | 4.53 MiB（4,751,930 bytes） | 150,048 | 74,156 | 0 |
| `data/YM_1068/data.parquet` | 9.14 MiB（9,583,963 bytes） | 407,803 | 331,767 | 0 |

“唯一序列对”包含 `(None, sequence)` 等负对照组合；它用于判断相同序列组合的重复表示，不代表独立实验事件数。

### 字段说明

| 字段 | 类型 | 缺失与取值 | 含义 |
| --- | --- | --- | --- |
| `mata_description` | `large_string` | 不缺失 | MATa 构建体名称；含技术重复、设计方法与阴性对照标签 |
| `matalpha_description` | `large_string` | 不缺失 | MATα 构建体名称；含目标、同源物与阴性对照标签 |
| `mata_sequence` | `large_string` | 各表有 12–7,338 个空值 | MATa 展示蛋白的公开氨基酸字符串；负对照为空 |
| `matalpha_sequence` | `large_string` | 各表有 201–112,536 个空值 | MATα 展示蛋白的公开氨基酸字符串；负对照为空 |
| `alphaseq_affinity` | `double` | 327,829 个空值；有限范围 -0.989–7.459 | $\log_{10}(K_D/\mathrm{nM})$ 的 AlphaSeq 估计，越小越强 |
| `affinity_lower_bound` | `double` | 与点估计同时缺失 | 95% 区间的较弱边界，在 log10 KD 轴上通常较大 |
| `affinity_upper_bound` | `double` | 不缺失 | 95% 区间的较强边界，在 log10 KD 轴上通常较小 |
| `normalized_affinity` | `double` | 328,693 个空值 | 按双方交互分布连续标准化的特异性分数，越负越特异 |
| `above_background` | `bool` | 只有 `true`/`false`，不缺失 | 相对 assay 背景的 BH 校正检验是否达到 `q < 0.05` |
| `sufficient_replicate_observations` | `bool` | 只有 `true`/`false`，不缺失 | 是否在超过一半重复样本中观察到该相互作用 |

序列列通常只含标准大写氨基酸字符。`YM_0005` 的 `m396_scFv_LH_Mod` 是唯一含 `&` 的非空序列字符串；该字符位于轻、重链片段之间，当前版本原样保存。

### 数据示例

以下是 `YM_0852` 中 `WT_0` 与 PD-1 的一条原始记录；为便于阅读，两个序列只展示长度和首尾片段，数值与布尔字段保持原值。

```json
{
  "mata_description": "WT_0",
  "matalpha_description": "huPD-1_RE(rebuilt)",
  "mata_sequence": "246 aa: QVQLVQSGVE...TFGGGTKVEIK",
  "matalpha_sequence": "122 aa: LDSPDRPWNP...IKESLRAELRVTE",
  "alphaseq_affinity": 2.221054284783616,
  "affinity_lower_bound": 2.2614756269968135,
  "affinity_upper_bound": 2.180633209007299,
  "normalized_affinity": -1.4542460921687161,
  "above_background": true,
  "sufficient_replicate_observations": true
}
```

## PDB 数据库

上游数据包没有逐行结构字段。PDB 审计从论文、数据卡中的亲本或目标身份出发，保存 6 个有明确序列联系的 RCSB 条目；每个条目包含原样 FASTA 和完整 mmCIF。12 个文件合计 5.84 MiB（6,128,859 bytes），Gemmi 解析确认每个 mmCIF 的 PDB ID、聚合物序列和坐标原子均存在，RCSB FASTA 序列也能在相应 mmCIF 的 canonical polymer 中找到。

| PDB | 覆盖实验 | 结构作用 | 与公开序列的联系 |
| --- | --- | --- | --- |
| [1N8Z](https://www.rcsb.org/structure/1N8Z) | `YM_0989`、`YM_0990` | Trastuzumab/Herceptin Fab–HER2 亲本复合物 | scFv 的 VH/VL 分别匹配 Fab 可变区；120 aa HER2 构建体与沉积 ectodomain 有 104 aa 连续相同片段 |
| [3UDW](https://www.rcsb.org/structure/3UDW) | `YM_0693`、`YM_0988` | 人 TIGIT 目标参考结构 | 公开 TIGIT 构建体与结构中的 TIGIT 有 107 aa 连续相同片段；结构中没有 PP489/ABC001 |
| [5JXE](https://www.rcsb.org/structure/5JXE) | `YM_0852`、`YM_0985` | Pembrolizumab Fab–PD-1 亲本复合物 | PD-1 构建体完整包含结构中的 114 aa PD-1；scFv 的 VH/VL 匹配 Fab 可变区 |
| [6LZG](https://www.rcsb.org/structure/6LZG) | `YM_0005`、`YM_0549`、`YM_1068` | SARS-CoV-2 RBD 与 ACE2 参考结构 | 209 aa RBD 完全相同；`ACE2_Full` 比结构中的 596 aa ACE2 多 1 个 N 端残基 |
| [6WAQ](https://www.rcsb.org/structure/6WAQ) | `YM_0005`、`YM_0549`、`YM_1068` | VHH72–SARS-CoV-1 RBD 亲本复合物 | 数据中的 125 aa VHH72 完全匹配沉积 VHH 的前 125 aa |
| [6ZLR](https://www.rcsb.org/structure/6ZLR) | `YM_0005` | CR3022 Fab–SARS-CoV-2 RBD 亲本复合物 | CR3022 scFv 含沉积 VH/VL，可用 RBD 序列包含在结构构建体中 |

这些条目为亲本或目标级锚点。设计变体没有逐行实验复合物结构；3UDW 和 6LZG 主要证明目标构建体身份，不能当作候选抗体复合物。1N8Z 的 HER2 构建体并非逐字符完全相同，保留它是因为同一亲本抗体、同一目标域和长连续序列证据同时成立。

## 采集过程记录

- 2026-09-25：通过 Hugging Face API 确认仓库公开、非 gated，固定 revision `3fb6b28b3ee758a7dfeaca5f14949dc505e90fda` 和其 23 个对象清单。
- 2026-09-25：按固定 revision 下载全部对象；9 个 LFS Parquet 以字节数和 SHA-256 验证，小文件以字节数和 Git blob ID 验证。
- 2026-09-25（`Q04` 已结案）：从 Europe PMC 保存 2022、2025 正式全文 XML，并从动态生成的 supplement ZIP 中按 XML 引用白名单提取 8 个原始成员。ZIP 容器时间戳会随请求变化，因此发布包保存稳定的成员原字节及逐文件 SHA-256。
- 2026-09-25：归档 2017 AlphaSeq 方法论文 PDF；该公共全文入口当前对自动请求实施挑战，已取得文件以字节数、PDF 头尾和 SHA-256 固定。
- 2026-09-25（`Q03` 已结案）：下载 1N8Z、3UDW、5JXE、6LZG、6WAQ、6ZLR 的 RCSB FASTA/mmCIF，完成文件身份、Gemmi 全解析、坐标存在和 canonical polymer 配对检查；这些亲本或目标级锚点没有扩展为逐设计变体结构。
- 2026-09-25：流式读取全部 1,705,908 行，验证 10 列 schema、空值、有限数、布尔域、置信边界顺序、完全重复行和跨实验序列交集。
- 2026-09-25：本地 README 与 source version 内 README 逐字节同步，并在发布前运行固定 Markdownlint 和 README 结构检查。

## 参考文献

1. A-Alpha Bio. [Open Protein–Protein Interaction Affinity Datasets with AlphaSeq](https://huggingface.co/datasets/aalphabio/open-alphaseq), revision `3fb6b28b3ee758a7dfeaca5f14949dc505e90fda`.
2. Younger D, Berger S, Baker D, Klavins E. [High-throughput characterization of protein–protein interactions by reprogramming yeast mating](https://doi.org/10.1073/pnas.1705867114). PNAS. 2017;114(46):12166–12171.
3. Engelhart E, Lopez R, Emerson R, et al. [Massively multiplexed affinity characterization of therapeutic antibodies against SARS-CoV-2 variants](https://doi.org/10.1093/abt/tbac011). Antibody Therapeutics. 2022;5(2):130–137.
4. Agarwal AA, Harrang J, Noble D, et al. [AlphaBind, a domain-specific model to predict and optimize antibody–antigen binding affinity](https://doi.org/10.1080/19420862.2025.2534626). mAbs. 2025;17(1):2534626.
5. A-Alpha Bio. [About](https://www.aalphabio.com/about/). 核查于 2026-09-25.
6. RCSB Protein Data Bank. [1N8Z](https://www.rcsb.org/structure/1N8Z), [3UDW](https://www.rcsb.org/structure/3UDW), [5JXE](https://www.rcsb.org/structure/5JXE), [6LZG](https://www.rcsb.org/structure/6LZG), [6WAQ](https://www.rcsb.org/structure/6WAQ), [6ZLR](https://www.rcsb.org/structure/6ZLR).

## 其他

### 完整性与验收

本次发布覆盖固定 Hugging Face revision 的全部 23 个仓库对象，没有选择性省略数据文件。`open-alphaseq/` inventory 的 `relative_path<TAB>bytes<TAB>sha256<LF>` 汇总哈希为 `279436bbdb5a53a069aa5a4f4547d75e31f016951d63cebfbf9f1ea309116e25`；PDB 12 文件的同口径汇总哈希为 `9c4c3cb47ce91d66dca68788f49107f0feff127f9e005e57b47c034684ba75d6`。

验收逐表核对了 schema 与实际数据，不依赖上游 README 的汇总数字。9 张表没有 NaN 或正负无穷值，数值缺失使用 Arrow null；布尔列无 null；所有有限亲和力记录的置信边界顺序通过。原始测序 reads、逐样本条形码计数与标定中间文件未在 Hugging Face revision 中公开，本版本的完整性范围止于官方处理后交付。

### 许可和再分发边界

Hugging Face 固定 revision 根目录的 `LICENSE` 是 MIT License，上游数据卡明确允许学术与商业用途。该许可覆盖本次保存的 Open AlphaSeq 仓库交付。2022 和 2025 论文正文分别标为 CC BY-NC 4.0；2017 PNAS 正文仅标为 PNAS license。RCSB 文件、论文与补充材料按各自来源条款处理，不能用数据仓库的 MIT License 替代它们的文本或数据库条款。

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-25；非阻塞、待上游说明）：`YM_0005` 的 `m396_scFv_LH_Mod` 中 `&` 是否是上游约定的轻/重链分隔符，数据卡没有说明。该缺口不影响公开包原样发布，但会影响需要单一氨基酸字母表的模型输入；当前保留原字符串，不做推断性改写。下一步是等待上游给出表示规则，或在下游任务中把拆分或 linker 替换规则作为显式、可追溯的派生处理；取得一手说明后关闭。
- `Q02`（最近更新：2026-09-25；非阻塞、待上游修订）：`YM_0985`、`YM_0988`、`YM_0990` 的数据卡错误尚未看到上游修订。该差异不影响固定 revision 的文件身份与本次公开包发布，但会影响按数据卡读取分子类型、目标和唯一序列数；当前以 Parquet 实际 schema、序列与去重计数为准并保留差异记录。下一步是在上游发布新 revision 时复核数据卡与文件，并按不可变新版本重新接入；三项说明与实际文件一致后关闭。
