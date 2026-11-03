---
tags:
  - context
---

# SRC_R36_HUTCHINSON 数据说明

## 数据集身份

- `source_id`：`SRC_R36_HUTCHINSON`
- `source_version`：`snapshot-2026-08-17`
- 原作者或发布机构：Mark Hutchinson、Jeffrey A. Ruffolo 等；AstraZeneca / Johns Hopkins；FLAb 由 Gray Lab 整理

## 实验设计和数据口径

本研究优化抗鸡卵清溶菌酶（HEL）的 D44.1 抗体。NIP228 是部分可开发性实验的对照，不能用清单的‘NIP228/HEL 变体’名称推断本实验 parent。作者利用先前 D44.1 单点 DMS enrichment 与 DeepAb 结构预测置信度筛选有利突变，并组合成 4,602 个候选；选入‘Top 200’的构建体包含 parent、D44.1des 和 198 个新设计，另外测试低分组合组。DeepAb 指标是设计依据，公开 CSV 的 KD 来自实验拟合。

IgG 初筛在 Octet BLI 上固定 IgG、加入单浓度 HEL，拟合 1:1 动力学模型；部分 IgG 多浓度复测。选中候选消化成 Fab，固定生物素化 HEL、对溶液中 Fab 滴定。IgG KD 是表观亲和力，Fab 是另一朝向及价态的测量；主文讨论了朝向和 avidity 引起的 parent KD 差异，不能混为同一测量口径。DSF/SLS 的 Tm1、Tm2、Tonset、Tagg 是稳定性读数，单位 °C，不能当 KD。

8 张 binding CSV 共 362 行、197 个唯一 VH/VL 配对；4 张 Tm1 CSV 共 258 行；12 表合计覆盖 207 个唯一 VH/VL 配对，不能相加为独立样本。‘multikd’实际对应原始 Table S4 的低分 multi-mutant 组，不表示 replicate 数。Top 27 / single / Top 200 组重叠；同一 parent 在不同实验组有不同测量值，按序列去重也不能直接丢掉实验上下文。原 XLSX 的 Top 200 有 200 个构建体 ID、Top 27 sheet 有 30 个含失败项的构建体 ID；文件名不是成功测量数。

FLAb 保存处理后数值表而非仪器 sensorgram；所有 binding fitness 经逐行核验等于 -log10(KD/M)，方向为越大亲和力越高，KD 越小越好。原 XLSX 保留 NT（未测）、DNE（未表达）、Low Response（BLI 响应低于阈值）和 N/A；原作者未在这些表提供统一数值检测阈值，不能把特殊值变成零或无穷大。CSV 只保留可用数值，不代表每个设计都成功测量。12 张 CSV 均按 VH/VL 与数值对应到作者补充工作簿 Table S1–S4；主文将这些设计变体的结合测量写为 BLI，Tm1 测量写为 DSF/SLS。FLAb `flab_metadata.json` 将八张 binding 表统一标为 `SPR Kd`、四张 Tm1 表标为 `DSC`，这两个分类标签与作者对表中实验的说明不一致；主文另有针对亲本抗体的 SPR 参考测量。

## 论文原文

### Hutchinson 主文

- 标题：Toward enhancement of antibody thermostability and affinity by computational design in the absence of antigen
- 作者：Hutchinson Mark；Ruffolo Jeffrey A.；Haskins Nantaporn；Iannotti Michael；Vozza Giuliana；Pham Tony；Mehzabeen Nurjahan；Shandilya Harini；Rickert Keith；Croasdale-Wood Rebecca；Damschroder Melissa；Fu Ying；Dippel Andrew；Gray Jeffrey J.；Kaplan Gilad
- 发表来源：mAbs
- 归档文本版本：正式发表版（完整 JATS XML；PDF 端点返回 403）
- 发布日期：2024-06-20
- DOI：10.1080/19420862.2024.2362775
- PMID / PMCID：38899735 / PMC11195458
- 本地文件：`articles/Hutchinson_2024-06-20_mAbs-VoR.xml`
- 文件大小：184.47 KiB（188,894 bytes）
- SHA-256：`db3c2b399eb473889a8277ba3848b4706ed1e05ef420cb1a3c85f68032ed96b9`
- 文本许可：CC BY-NC 4.0
- 补充材料：2 个公开原文件，见下表

### SM3514 补充材料

- 标题：Supplemental tables for publication.xlsx
- 作者：与主文相同，Hutchinson Mark；Ruffolo Jeffrey A.；Haskins Nantaporn；Iannotti Michael；Vozza Giuliana；Pham Tony；Mehzabeen Nurjahan；Shandilya Harini；Rickert Keith；Croasdale-Wood Rebecca；Damschroder Melissa；Fu Ying；Dippel Andrew；Gray Jeffrey J.；Kaplan Gilad
- 发表来源：mAbs 正式主文的官方附件
- 归档文本版本：原始 XLSX（上游文件名 `KMAB_A_2362775_SM3514.xlsx`）
- 发布日期：2024-06-20（随主文，未标独立发布日期）
- DOI：归属主文 10.1080/19420862.2024.2362775；无独立 DOI
- PMID / PMCID：归属主文 38899735 / PMC11195458；无独立记录
- 本地文件：`articles/Hutchinson_2024-06-20_mAbs-supplement-SM3514.xlsx`
- 文件大小：295.02 KiB（302,104 bytes）
- SHA-256：`32d87933cb1b371b0f94d8d37572aa28f752e82865fe9483cd78cee330ebd869`
- 文本许可：随主文 CC BY-NC 4.0；未声明独立附件许可
- 补充材料：本文件是实验补充数据，无更下层独立附件

### SM3513 补充材料

- 标题：Supplementary Figures.docx
- 作者：与主文相同，Hutchinson Mark；Ruffolo Jeffrey A.；Haskins Nantaporn；Iannotti Michael；Vozza Giuliana；Pham Tony；Mehzabeen Nurjahan；Shandilya Harini；Rickert Keith；Croasdale-Wood Rebecca；Damschroder Melissa；Fu Ying；Dippel Andrew；Gray Jeffrey J.；Kaplan Gilad
- 发表来源：mAbs 正式主文的官方附件
- 归档文本版本：原始 DOCX（上游文件名 `KMAB_A_2362775_SM3513.docx`）
- 发布日期：2024-06-20（随主文，未标独立发布日期）
- DOI：归属主文 10.1080/19420862.2024.2362775；无独立 DOI
- PMID / PMCID：归属主文 38899735 / PMC11195458；无独立记录
- 本地文件：`articles/Hutchinson_2024-06-20_mAbs-supplement-SM3513.docx`
- 文件大小：1.81 MiB（1,898,001 bytes）
- SHA-256：`778357b99d5a5efe370b20bd7f3aaccbd1f5064873efe69164d0711d08284811`
- 文本许可：随主文 CC BY-NC 4.0；未声明独立附件许可
- 补充材料：本文件是补充图与说明，无更下层独立附件

## 仓库内容

一手固定 Git tree：[Graylab/FLAb](https://github.com/Graylab/FLAb/tree/e05e3f0135783ffb7de412df6a1467e7a0031911)；commit `e05e3f0135783ffb7de412df6a1467e7a0031911`，tree `98f2b0b97071b0766ec29e168b4e7c0ad7f3595c`。source_version 的日期来自该上游 commit（2026-08-17），不是下载日期。保留来源原始路径的选择性快照，不是整个 repository；所选 blobs 没有 LFS pointer 或 submodule，未保存 .git。

```text
snapshot-2026-08-17/
    FLAb/LICENSE
    FLAb/README.md
    FLAb/data/README.md
    FLAb/data/binding/README.md
    FLAb/data/binding/hutchinson2023enhancement_multikd_fab.csv
    FLAb/data/binding/hutchinson2023enhancement_multikd_igg.csv
    FLAb/data/binding/hutchinson2023enhancement_singlekd_fab.csv
    FLAb/data/binding/hutchinson2023enhancement_singlekd_igg.csv
    FLAb/data/binding/hutchinson2023enhancement_top200kd_fab.csv
    FLAb/data/binding/hutchinson2023enhancement_top200kd_igg.csv
    FLAb/data/binding/hutchinson2023enhancement_top27kd_fab.csv
    FLAb/data/binding/hutchinson2023enhancement_top27kd_igg.csv
    FLAb/data/flab_metadata.json
    FLAb/data/thermostability/hutchinson2023enhancement_multitm1_igg.csv
    FLAb/data/thermostability/hutchinson2023enhancement_singletm1_igg.csv
    FLAb/data/thermostability/hutchinson2023enhancement_top200tm1_igg.csv
    FLAb/data/thermostability/hutchinson2023enhancement_top27tm1_igg.csv
```

目录树只展示上游 payload。README 和 metadata 说明整理来源，CSV 为按 assay 分组的公开表；项目的论文归档和外部 PDB 补充在独立章节描述。

## 数据结构

### 原始表与连接关系

原始补充 XLSX 在 articles 中归档，属于实验数据解释入口：四张 sheet `Table S1 Top 200`、`Table S2 Top 27`、`Table S3 single mutations`、`Table S4 Low 15 Multi`。第 1 行说明、第 2–3 行是分组/多层表头，第 4 行开始是构建体，底部还有脚注。S1 的有效范围为 1071×80，但仅 207 行非空，不能把 used range 当样本数。S2、S3 部分值是 VLOOKUP 等公式，应读取已有 cached values (`data_only=True`)；raw 不重新计算公式。`ID` / `#`、`VH sequence`、`VL sequence` 连接重叠组；列含 `KD (M)`、`ka (1/Ms)`、`kdis (1/s)`、Tm 温度、逐位突变以及非数值失败编码。S4 的低分组还包含亲本。

S4 原始温度字符串包含 U+202F 窄非断行空格和 U+00A0，例如第 5 行 Tm2 / Tonset / Tagg；保留原字节，后续 processed 层须显式解析。四表不存在同一个统一 CSV header，Fab top200 的 KD 字段带原始后缀 `KD (M)2`；不改列名掩盖来源差异。CSV 的 heavy/light 是 Fv 的 VH/VL 可变区，未包含完整 IgG 恒定区。

| 文件 | 记录数 | 唯一序列 / VH-VL | 数值范围 |
| --- | --- | --- | --- |
| `hutchinson2023enhancement_multikd_fab.csv` | 15 | 15 | 1.89e-09 … 2.55e-08 |
| `hutchinson2023enhancement_multikd_igg.csv` | 15 | 15 | 2.64e-10 … 3.43e-09 |
| `hutchinson2023enhancement_singlekd_fab.csv` | 22 | 22 | 6.63e-09 … 2.88e-08 |
| `hutchinson2023enhancement_singlekd_igg.csv` | 23 | 23 | 2.55e-09 … 2.86e-08 |
| `hutchinson2023enhancement_top200kd_fab.csv` | 50 | 48 | 1.32e-09 … 2.88e-08 |
| `hutchinson2023enhancement_top200kd_igg.csv` | 182 | 182 | 5.06e-10 … 2.86e-08 |
| `hutchinson2023enhancement_top27kd_fab.csv` | 28 | 27 | 1.32e-09 … 2.88e-08 |
| `hutchinson2023enhancement_top27kd_igg.csv` | 27 | 26 | 6.55e-10 … 1.04e-08 |
| `hutchinson2023enhancement_multitm1_igg.csv` | 15 | 15 | 62.6 … 68.5 |
| `hutchinson2023enhancement_singletm1_igg.csv` | 23 | 23 | 64.0 … 70.5 |
| `hutchinson2023enhancement_top200tm1_igg.csv` | 192 | 192 | 55.8 … 73.6 |
| `hutchinson2023enhancement_top27tm1_igg.csv` | 28 | 27 | 58.8 … 73.4 |

### 字段说明

| 表 | 字段原始拼写 | 类型、单位、方向和来源 |
| --- | --- | --- |
| `hutchinson2023enhancement_multikd_fab.csv` | `heavy` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_multikd_fab.csv` | `light` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_multikd_fab.csv` | `KD (M) Fab binding kinetics (affinity)` | 浮点原文（含科学记数法）；M；实验拟合 KD，较小更好；按文件区分 Fab、IgG apparent 或 mouse-Fc avid |
| `hutchinson2023enhancement_multikd_fab.csv` | `-log10( KD (M) )` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `hutchinson2023enhancement_multikd_fab.csv` | `fitness` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `hutchinson2023enhancement_multikd_igg.csv` | `heavy` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_multikd_igg.csv` | `light` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_multikd_igg.csv` | `KD (M) IgG binding kinetics (single point apparent affinity)` | 浮点原文（含科学记数法）；M；实验拟合 KD，较小更好；按文件区分 Fab、IgG apparent 或 mouse-Fc avid |
| `hutchinson2023enhancement_multikd_igg.csv` | `-log( KD(M) )` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `hutchinson2023enhancement_multikd_igg.csv` | `fitness` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `hutchinson2023enhancement_singlekd_fab.csv` | `heavy` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_singlekd_fab.csv` | `light` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_singlekd_fab.csv` | `KD (M) Fab binding kinetics (affinity)` | 浮点原文（含科学记数法）；M；实验拟合 KD，较小更好；按文件区分 Fab、IgG apparent 或 mouse-Fc avid |
| `hutchinson2023enhancement_singlekd_fab.csv` | `-log10(KD (M) )` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `hutchinson2023enhancement_singlekd_fab.csv` | `fitness` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `hutchinson2023enhancement_singlekd_igg.csv` | `heavy` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_singlekd_igg.csv` | `light` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_singlekd_igg.csv` | `KD (M) IgG binding kinetics (single point apparent affinity)` | 浮点原文（含科学记数法）；M；实验拟合 KD，较小更好；按文件区分 Fab、IgG apparent 或 mouse-Fc avid |
| `hutchinson2023enhancement_singlekd_igg.csv` | `-log10(KD (M) )` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `hutchinson2023enhancement_singlekd_igg.csv` | `fitness` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `hutchinson2023enhancement_top200kd_fab.csv` | `heavy` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_top200kd_fab.csv` | `light` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_top200kd_fab.csv` | `KD (M)2 Binding kinetics (Fab, affinity)` | 浮点原文（含科学记数法）；M；实验拟合 KD，较小更好；按文件区分 Fab、IgG apparent 或 mouse-Fc avid |
| `hutchinson2023enhancement_top200kd_fab.csv` | `-log(KD Binding kinetics (Fab, affinity) )` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `hutchinson2023enhancement_top200kd_fab.csv` | `fitness` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `hutchinson2023enhancement_top200kd_igg.csv` | `heavy` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_top200kd_igg.csv` | `light` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_top200kd_igg.csv` | `KD (M) Binding kinetics (IgG, apparent affinity)` | 浮点原文（含科学记数法）；M；实验拟合 KD，较小更好；按文件区分 Fab、IgG apparent 或 mouse-Fc avid |
| `hutchinson2023enhancement_top200kd_igg.csv` | `-log10(KD M IgG)` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `hutchinson2023enhancement_top200kd_igg.csv` | `fitness` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `hutchinson2023enhancement_top27kd_fab.csv` | `heavy` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_top27kd_fab.csv` | `light` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_top27kd_fab.csv` | `KD (M) Fab binding kinetics (affinity)` | 浮点原文（含科学记数法）；M；实验拟合 KD，较小更好；按文件区分 Fab、IgG apparent 或 mouse-Fc avid |
| `hutchinson2023enhancement_top27kd_fab.csv` | `-log10(KD (M) Fab )` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `hutchinson2023enhancement_top27kd_fab.csv` | `fitness` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `hutchinson2023enhancement_top27kd_igg.csv` | `heavy` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_top27kd_igg.csv` | `light` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_top27kd_igg.csv` | `KD (M) IgG binding kinetics (single point apparent affinity)` | 浮点原文（含科学记数法）；M；实验拟合 KD，较小更好；按文件区分 Fab、IgG apparent 或 mouse-Fc avid |
| `hutchinson2023enhancement_top27kd_igg.csv` | `-log( KD (M) IgG )` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `hutchinson2023enhancement_top27kd_igg.csv` | `fitness` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `hutchinson2023enhancement_multitm1_igg.csv` | `heavy` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_multitm1_igg.csv` | `light` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_multitm1_igg.csv` | `Tm1 (°C) IgG Thermostability` | 浮点原文；°C；实验稳定性，较高更稳定；fitness 与 Tm1 相同 |
| `hutchinson2023enhancement_multitm1_igg.csv` | `fitness` | 浮点原文；°C；实验稳定性，较高更稳定；fitness 与 Tm1 相同 |
| `hutchinson2023enhancement_singletm1_igg.csv` | `heavy` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_singletm1_igg.csv` | `light` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_singletm1_igg.csv` | `Tm1 (C) IgG Thermostability` | 浮点原文；°C；实验稳定性，较高更稳定；fitness 与 Tm1 相同 |
| `hutchinson2023enhancement_singletm1_igg.csv` | `fitness` | 浮点原文；°C；实验稳定性，较高更稳定；fitness 与 Tm1 相同 |
| `hutchinson2023enhancement_top200tm1_igg.csv` | `heavy` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_top200tm1_igg.csv` | `light` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_top200tm1_igg.csv` | `Tm1 (C) Thermostability (IgG)` | 浮点原文；°C；实验稳定性，较高更稳定；fitness 与 Tm1 相同 |
| `hutchinson2023enhancement_top200tm1_igg.csv` | `fitness` | 浮点原文；°C；实验稳定性，较高更稳定；fitness 与 Tm1 相同 |
| `hutchinson2023enhancement_top27tm1_igg.csv` | `heavy` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_top27tm1_igg.csv` | `light` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `hutchinson2023enhancement_top27tm1_igg.csv` | `Tm1 (C) IgG Thermostability` | 浮点原文；°C；实验稳定性，较高更稳定；fitness 与 Tm1 相同 |
| `hutchinson2023enhancement_top27tm1_igg.csv` | `fitness` | 浮点原文；°C；实验稳定性，较高更稳定；fitness 与 Tm1 相同 |

`FLAb/data/flab_metadata.json` 是整个 FLAb 固定快照的索引，含 165 个文件条目；本版本仅取得其中与 Hutchinson 对应的 12 张表。其字段按原始键名分组如下，索引 `size` 表示记录数，单位为行：

| JSON 层级 | 原始字段名 | 类型、单位、缺失编码及来源 |
| --- | --- | --- |
| 顶层 | `files` | 165 个对象的数组；FLAb 整理的文件索引，无数值单位；本文件中非空 |
| 顶层 | `keys` | 对索引枚举值的对象；含 `assay`、`category`、`doi`、`key_words`、`study`、`year`、`license`、`size` 八个键；FLAb 整理，本文件中非空 |
| `files[]` | `name`、`path` | 原始文件名及相对路径字符串；无数值单位，165 个条目均存在；`path` 以索引自身位置为基准，未取得的其他 FLAb 文件不由此补造 |
| `files[]` | `assay`、`category` | FLAb 整理的测定名称及分类字符串；无数值单位，165 个条目均存在；本研究的 `SPR Kd`、`DSC` 分类与主文方法的差异见上文 |
| `files[]` | `doi`、`study`、`year` | FLAb 整理的论文链接、标题和发表年；字符串、字符串、整数；无数值单位，165 个条目均存在；其他来源条目可使用字面 `none` |
| `files[]` | `key_words` | 字符串数组，来源主题标签；无数值单位，165 个条目均存在；不作为实验标签 |
| `files[]` | `license` | FLAb 整理的许可字符串；无数值单位，165 个条目均存在；字面 `none` 表示索引未给出许可 |
| `files[]` | `size` | 整数，索引所称记录数（行）；不是文件字节数，165 个条目均存在；具体表行数仍以实际 CSV 为准 |

上述 CSV 全列缺失计数为 0，序列非法字符计数为 0，不含 NB/ND/检测边界字符串或不可见 Unicode。该事实仅针对 CSV；原 XLSX 的失败编码、公式和不可见字符见前文，不能将 CSV 的数值完备性推广到所有实验对象。

### 数据示例

`hutchinson2023enhancement_multikd_fab.csv` 第一条真实记录：

| heavy | light | KD (M) Fab binding kinetics (affinity) | -log10( KD (M) ) | fitness |
| --- | --- | --- | --- | --- |
| `QVQLQESGAEVMKPGASVKISCKATGYTFSTYWIEWVKQRPGHGLEWIGEILPGSGSTYYNEKFKGKATFTADTSSNTAYMQLSSLTSEDSAVYYCARGDGNYGYWGQGTTLTVSS` | `DIELTQSPATLSVTPGDSVSLSCRASQSISNNLHWYQQKSHESPRLLIKYVSQSSSGIPSRFSGSGSGTDFTLSINSVETEDFGMYFCQQSNSWPRTFGGGTKLEIK` | `2.55E-08` | `7.59345982` | `7.59345982` |

一行代表此实验组和 assay 格式的 VH/VL 数值记录；相同序列可在其他组/格式再次出现，并不构成独立抗体。

## PDB 数据库

审计主文 Figure 2、Methods、补充 XLSX、FLAb 表及 metadata；Figure 2 明确引用 PDB 1MLC 作为亲本 D44.1–HEL 复合物。因此接受一个共享 parent 锚点，不能把 197 个变体说成拥有各自实测复合物。RCSB 的 entity 1 为 D44.1 light，author chains A/C；entity 2 为 heavy，B/D；entity 3 为 HEL，E/F。FASTA 保留完整 entry 的所有 polymer entities，坐标保留整个 entry，包括晶体内重复链；不选择一份 chain 后修改 FASTA，不把设计 VH/VL 嫁接进去。连接规则是实验组共有的 D44.1 parent 关系，CSV 没有逐行 PDB ID。结构不是所有实验变体或 IgG 格式的严格 construct 映射。

2026-09-18 获取；每个接受锚点的 FASTA 与 mmCIF 均通过 entry ID、canonical polymer entity 序列和 atom_site 验证。PDB 补充按上述参考映射完成；实验变体 / ADI 抗体 / VHH 的逐样本复合物没有取得。

| PDB | 文件 | 大小 | SHA-256 |
| --- | --- | --- | --- |
| 1MLC | `pdb/sequences/rcsb_pdb_1MLC.fasta` | 780 bytes | `980b3d036b6e8aef2c09df6e6a44712535111f14c2eaaaa4106ed5d7afd7253d` |
| 1MLC | `pdb/structures/1MLC.cif` | 899.49 KiB（921,079 bytes） | `5536c79a3d73e09503f6a4d252bbca2dac5fa0e59b5424309f49cd0c34e8606e` |

FASTA：`https://www.rcsb.org/fasta/entry/<PDB>/download`；坐标：`https://files.rcsb.org/download/<PDB>.cif`。完整原样保存，不生成衍生序列或独立 PDB manifest。

## 使用方式

调用者赋值 `dataset_root` 为本 source version 目录，原样读取：

```python
import csv
from pathlib import Path
with (Path(dataset_root) / 'FLAb/data/binding/hutchinson2023enhancement_top200kd_igg.csv').open(encoding='utf-8', newline='') as handle:
    first = next(csv.DictReader(handle))
print(first)
```

XLSX 需注意多层表头和公式缓存值。

## 采集过程记录

- 2026-09-18 读取 project.toml、developer.local.toml、规则、资源清单及建设计划；context 工具成功。身份 wuhuawei，采用统一共享 storage root。枚举一手固定 Git tree / HF API，生成个人 workspace 中的版本/文件配置，选版本日期来自上游数据。
- 2026-09-18 将 payload 写至 `<source_id>/.staging/snapshot-2026-08-17.partial/`，以 curl 断点恢复；逐文件独立核对字节、Git blob 或 HF LFS SHA-256，保留原文件名与原始数值。下载代码、配置、研究和验收依据保存在个人 workspace。
- 2026-09-18 从 [主文一手入口](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11195458/fullTextXML) 取得全文，核对 DOI / 标题 / 版本；归档后复核 SHA-256。PMC、EuropePMC 和出版社 PDF 端点返回 403；废弃 PDF 路径，归档完整 EuropePMC JATS XML，不伪称 PDF 成功。官方 supplementaryFiles ZIP 全成员 CRC 遍历后仅保留所需 XLSX/DOCX，不发布 ZIP 中的重复正文图片。

| 原文件名 | 归档路径 | 改名依据 |
| --- | --- | --- |
| KMAB_A_2362775_SM3514.xlsx | `articles/Hutchinson_2024-06-20_mAbs-supplement-SM3514.xlsx` | 来源简称、正式发表日期、原补充编号；抽取/改名后字节数与 SHA-256 一致 |
| KMAB_A_2362775_SM3513.docx | `articles/Hutchinson_2024-06-20_mAbs-supplement-SM3513.docx` | 来源简称、正式发表日期、原补充编号；抽取/改名后字节数与 SHA-256 一致 |

- 2026-09-18 逐表读取全部 CSV / 所有 XLSX sheets，核对记录粒度、序列字符、缺失和数值变换；实际对象身份和原始失败值按原文解释，不做 raw 清洗。发现清单误称 NIP228，改正科学说明为 D44.1；top200 Fab 实际 50 行；362 行并集为 197 个 VH/VL。
- 2026-09-18 按一手证据审计 PDB，取得完整 entry FASTA/mmCIF，逐一比对 canonical entities 与完整坐标；不重建每条变体。最初系统 Python 缺少 openpyxl/pypdf/gemmi，改用已有个人 tools 中的隔离依赖，未改系统环境。
- 2026-09-18 生成本地 `workspace/users/<developer.user>/docs/readme/` 工作稿并立即同步本版本 README；执行 skill 的 markdownlint-cli2@0.20.0 至 0 errors，核对本地/共享 README 一致和 source 全文件 inventory，验收通过后原子重命名发布，清理 temporary API/论文缓存和空 staging。批次状态与 handoff 同步；公共总表只准备拟议修改，没有越权修改。

2026-09-22：复核全部四张 Tm1 CSV 的原始表头与数值；审计结果中 `fitness_transform_failed_lines` 均为空，`fitness` 逐行等于对应的 Tm1 温度。修正生成器把 Tm1 原始列误写为 `-log10(KD)` 的分支条件，并同步改正本 README 字段说明；binding CSV 的 `-log10(KD/M)` 口径未改变。同日将 12 张 CSV 的全部 620 行按 VH/VL 对应到作者补充工作簿 Table S1–S4，其中 Tm1 数值逐行一致，KD 数值与工作簿保留的较高精度值符合公开 CSV 的舍入表示；结合主文 Results 和 Methods，确认 FLAb 索引的 `SPR Kd` / `DSC` 分类不能作为本研究这些表的测量方法。

## 参考文献

- [固定数据版本](https://github.com/Graylab/FLAb/tree/e05e3f0135783ffb7de412df6a1467e7a0031911)
- [Toward enhancement of antibody thermostability and affinity by computational design in the absence of antigen](https://doi.org/10.1080/19420862.2024.2362775)
- [RCSB PDB 1MLC](https://www.rcsb.org/structure/1MLC)；条目中的 primary citation 用于结构引用。

## 其他

### 数据范围和限制

此版本是 FLAb 固定 tree 的选择性原样副本加原论文补充材料，不是整库 FLAb。R09 已包含相同 CSV；后续合并须按来源及原始测量去重。保留重叠组、parent、Fab/IgG 朝向和稳定性标签，避免随机按行划分导致泄漏。未取得原始仪器文件及每个变体的实测结构，不声明完整研究数据获得。

### 完整性与验收

全部 17 个 payload 文件、282.67 KiB（289,450 bytes）；按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接的 inventory SHA-256：`5a17257d76a4a091980b9c6fa06d61abb603b4f8e775a626a2d6fc2d404043de`。Git blob / LFS 身份、全表 parser 和数值/序列检查通过；外部论文/PDB 身份见对应章节。

| 上游 payload | 大小 | 本地 SHA-256 |
| --- | --- | --- |
| `FLAb/LICENSE` | 101 bytes | `d0cce20026928c70ed74bb1f4a2e0e0501842859a222c54e85a586501fffe739` |
| `FLAb/README.md` | 4.65 KiB（4,761 bytes） | `5a5184094ed4a13c64b1cb914a2168a58e3b16abe956b794a163888ec70996ff` |
| `FLAb/data/README.md` | 10.68 KiB（10,933 bytes） | `1991c2a8219786efa27e5db2980263469aaf57cb05e3b771cb6911b10dd75523` |
| `FLAb/data/binding/README.md` | 21.60 KiB（22,120 bytes） | `8d46652d19eabc090d3b51f7caa1bf80eca9f46a2ff889226028a938952b8da5` |
| `FLAb/data/binding/hutchinson2023enhancement_multikd_fab.csv` | 3.86 KiB（3,954 bytes） | `5962caef362d08d8c529939908d7a4528675bcd25235b59f3b74c521a68522c0` |
| `FLAb/data/binding/hutchinson2023enhancement_multikd_igg.csv` | 3.88 KiB（3,977 bytes） | `59db69b2d076e82f179a7bec47bdbc809644dea88d425d506f9c486bf7de1f0e` |
| `FLAb/data/binding/hutchinson2023enhancement_singlekd_fab.csv` | 5.63 KiB（5,768 bytes） | `db49813003127cbe133195fbf3879f52a5f671a46719ef1b989e91ccc14fb1bb` |
| `FLAb/data/binding/hutchinson2023enhancement_singlekd_igg.csv` | 5.91 KiB（6,049 bytes） | `669e69522525cba335fda5bfd7fd35a76c0c3ab76d13298de053ecd2489faaa9` |
| `FLAb/data/binding/hutchinson2023enhancement_top200kd_fab.csv` | 12.75 KiB（13,052 bytes） | `ecacc5ec299cd5c2b75ea32d5457098d88798bbf61f8b1b5b94d36d84b19082c` |
| `FLAb/data/binding/hutchinson2023enhancement_top200kd_igg.csv` | 46.08 KiB（47,185 bytes） | `a59ccddfab3bdfd61dc5f7275d5a8c077c2d9e60e1f74c53974d69586145a62e` |
| `FLAb/data/binding/hutchinson2023enhancement_top27kd_fab.csv` | 7.15 KiB（7,324 bytes） | `cedd18bdf9cae22842573cf5bb64b4a84722947d0e09cdd5e6bb16d14b5d26c8` |
| `FLAb/data/binding/hutchinson2023enhancement_top27kd_igg.csv` | 6.92 KiB（7,084 bytes） | `dbd87b8be24e4b14ea0e24ffbe02c014ee2b39200fc920b6084e30fa427e6424` |
| `FLAb/data/flab_metadata.json` | 93.92 KiB（96,170 bytes） | `132b54d574ff02ed81de29915249bdaeed1e33805f5189cc4d09c3deb0585fa3` |
| `FLAb/data/thermostability/hutchinson2023enhancement_multitm1_igg.csv` | 3.50 KiB（3,589 bytes） | `ded8db1c627e602e8aa14f4cad98c61d05cb0bfc38a5421d369f61dbb1864928` |
| `FLAb/data/thermostability/hutchinson2023enhancement_singletm1_igg.csv` | 5.34 KiB（5,471 bytes） | `cdc94741be47c4b6d1b750b81834514026373a0e7730a43c2c29e427811e66b9` |
| `FLAb/data/thermostability/hutchinson2023enhancement_top200tm1_igg.csv` | 44.20 KiB（45,265 bytes） | `74a6293f2be33d51acaaf102dea91b4584e24901cbbde843f1fa9daa450afce5` |
| `FLAb/data/thermostability/hutchinson2023enhancement_top27tm1_igg.csv` | 6.49 KiB（6,647 bytes） | `51398c33760f5652449800516a72d232a9e331a0d57c6749cef61e69c46fe6ac` |

### 许可和再分发边界

原论文 permissions 为 CC BY-NC 4.0；FLAb 的 LICENSE 指向逐 dataset 的 data/README.md，其中本研究同样标为 CC BY-NC 4.0。保留原论文的非商业及署名条件，不把 FLAb 汇编论文许可推广为每张表的许可。访问无需申请不等于可无限商业使用或再分发。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| FLAb 8 张 binding、4 张 Tm1 表 | 12 个原名 CSV，完整 Git blob / 数值核验 | 已包含 |
| 原论文四张实验补充表和补充图 | XLSX 四 sheets、DOCX | 已包含 |
| 所有候选仪器级原始曲线、逐变体实测结构 | 本包未提供 | 未获得 |

## 待解决问题与处理进展

截至 2026-09-22，本次对固定公开表、作者补充工作簿、主文测量方法与共享参考结构的复核范围内暂无待解决问题。仪器级曲线与逐变体实验结构仍按“公开范围对照”所列范围缺口处理。
