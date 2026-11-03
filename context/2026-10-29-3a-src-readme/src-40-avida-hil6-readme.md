---
- tags:
  - context
---

# SRC_R40_AVIDA_HIL6 数据说明

- [数据集身份](#数据集身份)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
  - [arXiv v2 主文](#arxiv-v2-主文)
  - [公开补充材料 1](#公开补充材料-1)
  - [公开补充材料 2](#公开补充材料-2)
  - [NeurIPS 正式主文](#neurips-正式主文)
  - [NeurIPS 独立 datasheet](#neurips-独立-datasheet)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [FASTQ 与库关系](#fastq-与库关系)
  - [FASTA 氨基酸交付](#fasta-氨基酸交付)
  - [Zenodo 原标签表与计数归档](#zenodo-原标签表与计数归档)
  - [字段说明](#字段说明)
  - [数据示例](#数据示例)
- [PDB 数据库](#pdb-数据库)
- [使用方式](#使用方式)
- [采集过程记录](#采集过程记录)
- [参考文献](#参考文献)
- [其他](#其他)
  - [数据范围和限制](#数据范围和限制)
  - [完整性与验收](#完整性与验收)
  - [许可和再分发边界](#许可和再分发边界)
  - [公开范围对照](#公开范围对照)

## 数据集身份

- `source_id`：`SRC_R40_AVIDA_HIL6`
- `source_version`：`1.0.0`
- 原作者或发布机构：Hirofumi Tsuruta 等；COGNANO / Google

## 实验设计和数据口径

用人 IL-6 WT 与 30 个位点的 alanine mutant 混合物四次免疫一只羊驼，收集血液/淋巴组织建立 12 个母库；扩增 VHH、构建噬菌体展示库，对 31 个 IL-6 版本和无 IL-6 阴性对照各做一轮 biopanning，WT 三次重复，形成 408 个子库。NGS paired reads 去 singleton、翻译并按 VHH 计数。标签由母库/子库比例差异的双样本比例 Z 检验形成；跨相关库取最小 p-value，比例上升且 p≤0.05 为 binder，下降且 p≤0.05 为 non-binder，其余 non-significant。再用阴性对照排除 noise；对不显著阴性对照使用经验 p-value 比阈值 10^2.5。标签不是直接 SPR/BLI KD，也不能给阳性内部排序。

公开 HF 表有 573,891 个唯一 (VHH_sequence, Ag_label) 配对：20,980 个 label=1、552,911 个 label=0；38,599 条唯一公开 VHH_sequence 字符串。31 个抗原键均在 antigen_sequences.csv 唯一出现，无孤立 join、重复配对或冲突标签；计数与论文一致。论文另述 non-significant 的 1,998,127 配对及 325,865 unique VHH，这些不在本 HF 四对象包内，不把它们当负例补入。12 库及 WT replicate 在标签形成阶段已汇总，CSV 每行不是一个独立 wet-lab replicate。

VHH_sequence 是公开的表达构建体氨基酸串，大多数保留表达用 N 端信号序列（568,080 行以 MKYLLPTAAAGLLLLAAQPAMA 起始，另有前缀变体），全部带末端 HHHHHH 标签；WT 抗原串为 218 aa，包含 27 aa N 端前缀、185 aa mature IL-6 区域及末端 HHHHHH，不能把整串都称为成熟 IL-6 或仅可变域。保留来源字节和表示，不裁剪。所有序列只含标准 20 种大写氨基酸；表无缺失和不可见 Unicode。训练划分必须按 VHH 关系和抗原版本设计；论文按抗原版本划分训练/测试，同一 VHH 跨靶点可能重现，不能随机按配对行宣称泛化到新抗体。

此版本补齐原作者声明的全部 420 个库：12 个 Mother、12 个无 IL-6 阴性对照 Serum、30×12 个 mutant 子库及 3×12 个 WT replicate 子库，共 408 个子库。每库恰有 R1/R2 两个来源 FASTQ 和一个经作者处理的氨基酸 FASTA；35 个库组各有 a–l 共 12 个库。840 FASTQ 全遍历得到 40365943 个 paired read records；420 FASTA 共 24036149 条序列记录。read、FASTA record、唯一 VHH、VHH–抗原配对分别计数，不把重复测序记录当独立抗体。

官方 datasheet 的 collection timeframe 是 2019 年 3–4 月；这个实验时间与 2023 数据/论文版本和 2024 HF 表示版本的发布日期分别记录。WT 三组重复最后汇总为 `IL-6_WTs`，固定作者实现对三组 signed-log-p score 作平均；论文的最小 p-value 描述与代码的 WT 合并策略应一并阅读，本次未重新运行或改写来源统计标签。

作者 Appendix A.2 明示 MiSeq paired-end 300-bp 测序；实际原始 FASTQ 的 read 长度范围为 35–301 nt，含 N；每条质量字符串与序列等长。作者公开脚本明确 Trimmomatic 使用 Phred+33。FASTA 是 cutadapt/Trimmomatic、paired-read merge、primer/vector 提取、翻译、stop/His6 截取、去 X 和 ≥100 aa 长度过滤后的交付，不是仪器原始数据；本次只保存作者原文件，未重跑该处理。实际 FASTA 长度为 100–187 aa，重复 VHH 可以有不同 read header。libtable 是 singleton 过滤和跨库计数层，原 CSV 是最终二元标签层；统计标注过程不是连续亲和力测量。

420 FASTA 的精确序列字符串并集为 5784663 条，这是来源表达串的去重计数，不等于已确认的独立抗体克隆数，也包含后续 singleton/标签过滤排除的记录；全部 38,599 个 labelled VHH 均能在 FASTA 中找到。未生成 noise/non-significant 的新标签表；这种重建属于 processed 阶段。

## 论文原文

### arXiv v2 主文

- 标题：AVIDa-hIL6: A Large-Scale VHH Dataset Produced from an Immunized Alpaca for Predicting Antigen-Antibody Interactions
- 作者：Hirofumi Tsuruta；Hiroyuki Yamazaki；Ryota Maeda；Ryotaro Tamura；Jennifer N. Wei；Zelda Mariet；Poomarin Phloyphisut；Hidetoshi Shimokawa；Joseph R. Ledsam；Lucy Colwell；Akihiro Imura
- 载体与版本：arXiv 2306.03329v2，20 页（NeurIPS 2023 Datasets and Benchmarks 研究）
- 发布日期：2023-10-11
- DOI：10.48550/arXiv.2306.03329
- PMID / PMCID：无 / 无
- 本地文件：`articles/AVIDaHIL6_2023-10-11_arXiv-v2.pdf`
- 文件大小：8609048 bytes
- SHA-256：`80e63a221461dbc9c9c29aa8f01b905048a6e9bcc93357f14d02141d1d6a0eb7`
- 文本许可：arXiv non-exclusive distribution license (abs-page license link)
- 补充材料：2 个独立公开材料，见下列小节；主文 Appendix 已包含在 20 页 PDF

### 公开补充材料 1

- 标题：arXiv v2 原始 LaTeX 与六个原始图形 PDF
- 作者：与主文相同，Hirofumi Tsuruta；Hiroyuki Yamazaki；Ryota Maeda；Ryotaro Tamura；Jennifer N. Wei；Zelda Mariet；Poomarin Phloyphisut；Hidetoshi Shimokawa；Joseph R. Ledsam；Lucy Colwell；Akihiro Imura
- 载体与版本：arXiv 2306.03329v2 source package
- 发布日期：2023-10-11（arXiv v2 submission history）
- DOI：归属主文 10.48550/arXiv.2306.03329；无独立 DOI
- PMID / PMCID：无 / 无
- 本地文件：`articles/AVIDaHIL6_2023-10-11_arXiv-v2-source.tar.gz`
- 文件大小：8076633 bytes
- SHA-256：`5b62d2af47be4dfc027d0e0607639a6dfbc54f37945479042026c3b8d3f298a9`
- 文本许可：arXiv non-exclusive distribution license (abs-page license link)
- 补充材料：本文件是来源补充归档；内部成员安全遍历及完整 gzip CRC 通过，未生成派生数据

### 公开补充材料 2

- 标题：作者公开预处理、统计标签、分析与 benchmark 源代码
- 作者：COGNANO，作者官方仓库
- 载体与版本：GitHub immutable commit 72ae4f743bfe51ea350f21b9b94e0cb1bdd5264f
- 发布日期：2024-11-19（Git committer date for exact immutable revision）
- DOI：无独立 DOI；固定作者 GitHub revision 已核验
- PMID / PMCID：无 / 无
- 本地文件：`articles/AVIDaHIL6_2024-11-19_GitHub-72ae4f743bfe.tar.gz`
- 文件大小：925309 bytes
- SHA-256：`15c58bf94a020a580352891573400936eb8bca6868afdfe575f0da50e3c8c629`
- 文本许可：MIT code license; referenced experimental data remain CC BY-NC 4.0
- 补充材料：本文件是来源补充归档；内部成员安全遍历及完整 gzip CRC 通过，未生成派生数据

### NeurIPS 正式主文

- 标题：AVIDa-hIL6: A Large-Scale VHH Dataset Produced from an Immunized Alpaca for Predicting Antigen-Antibody Interactions
- 作者：Hirofumi Tsuruta；Hiroyuki Yamazaki；Ryota Maeda；Ryotaro Tamura；Jennifer N. Wei；Zelda Mariet；Poomarin Phloyphisut；Hidetoshi Shimokawa；Joseph R. Ledsam；Lucy Colwell；Akihiro Imura
- 载体与版本：NeurIPS 2023 Datasets and Benchmarks official paper，20 页
- 发布日期：2023（具体日期未公开）；用户明确允许按已公示年份填写，内嵌生成日期不作发布日期
- DOI：10.52202/075280-1823
- PMID / PMCID：无 / 无
- 本地文件：`articles/AVIDaHIL6_2023_NeurIPS2023-main.pdf`
- 文件大小：8543930 bytes
- SHA-256：`90582af207c47e5144a142b19a6a7c25a1b587cf0be738dc9eb6850c100e4c70`
- 文本许可：Authors retain copyright; NeurIPS publishing licence is non-exclusive; no separate text CC licence declared by the PDF/abstract. Internal research archive; data licence is separately CC BY-NC 4.0.
- 补充材料：独立 6 页 datasheet，见下一小节；主文 Appendix 在本 PDF

### NeurIPS 独立 datasheet

- 标题：AVIDa-hIL6: A Large-Scale VHH Dataset Produced from an Immunized Alpaca for Predicting Antigen-Antibody Interactions — Datasheet
- 作者：Hirofumi Tsuruta；Hiroyuki Yamazaki；Ryota Maeda；Ryotaro Tamura；Jennifer N. Wei；Zelda Mariet；Poomarin Phloyphisut；Hidetoshi Shimokawa；Joseph R. Ledsam；Lucy Colwell；Akihiro Imura
- 载体与版本：NeurIPS 2023 Datasets and Benchmarks official datasheet，6 页
- 发布日期：2023（具体日期未公开）；用户明确允许按已公示年份填写，内嵌生成日期不作发布日期
- DOI：10.52202/075280-1823；随主文，无独立 DOI
- PMID / PMCID：无 / 无
- 本地文件：`articles/AVIDaHIL6_2023_NeurIPS2023-datasheet.pdf`
- 文件大小：139868 bytes
- SHA-256：`5ed8635227c01c704bd60978af5fb3165dfcd38aec502f12b569d9ead7b5c3a1`
- 文本许可：Authors retain copyright; NeurIPS publishing licence is non-exclusive; no separate text CC licence declared by the PDF/abstract. Internal research archive; data licence is separately CC BY-NC 4.0.
- 补充材料：本文件为独立 datasheet，无更下层附件

## 仓库内容

一手 [Zenodo record 7935862](https://zenodo.org/records/7935862)，版本 `1.0.0`、publication_date 2023-06-01，DOI `10.5281/zenodo.7935862`。版本目录使用上游正式版本名，不改写为下载日期快照。concept DOI 7935861 会跳转到 version record，下载脚本直接固定 7935862；保存该记录全部两对象。

测序交付来自作者项目页链接的 [NGS_raw_data](https://drive.google.com/drive/folders/1dfB2jcwb8NrHQnqRcK4m6RRs95c5nZVm) 和 [VHH_sequences](https://drive.google.com/drive/folders/1pWqgUzCSW_agGPTcMNPpMzZTmfotWL4K)。Drive 没有不可变 release，这是与 Zenodo 原始发布一起归档的可变对象快照，以每对象 ID、version、modified/created、字节数、官方 MD5 固定传输身份，不把正式 `1.0.0` 说成 Drive 的平台 release。HF `snapshot-2024-11-19` 曾作为同一标签的精简表示单独保存；逐项覆盖审计确认全部 573,891 个标签、31 个抗原序列和三个 subject 常量均由本版本数据或固定作者代码包含，HF data card 的来源/许可/schema 信息也已写入本 README。按用户决定删除该冗余 raw 版本，只在仓库配置、历史 publication 和 `docs/audits/r40-hf-redundancy.json` 保留身份与删除证据。

```text
1.0.0/
├── AVIDa-hIL6-sequencing/
│   ├── NGS_raw_data/       840 个原名 *.fastq.gz
│   └── VHH_sequences/      420 个原名 *.fasta
└── AVIDa-hIL6-Zenodo/
    ├── il6_aai_dataset.csv
    └── libtable.tar.gz
```

FASTA 与 FASTQ 通过库名连接；一个 FASTA 对应两个 mate 文件。tar 原样保留，不把解压表重新序列化成新 raw 文件。没有原生在线文档或平台导出对象。

## 数据结构

### FASTQ 与库关系

每个 `.fastq.gz` 为四行 FASTQ：read header、DNA read、`+`、ASCII 质量字符串。R1/R2 通过去 mate 表示后的 read ID 逐条连接，所有库的两 mate 数和 read ID 均一致。gzip 包括 trailer/CRC 在内已读到 EOF；N 为原始歧义碱基，未清洗。库后缀 a–l 对应采样库；Mother 是筛选前，Serum 是无靶点对照，不是第三种实验抗原。

| 库组 | 库数 | paired read records | FASTA records |
| --- | --- | --- | --- |
| Mother | 12 | 983796 | 441045 |
| Serum | 12 | 993943 | 524008 |
| IL-6_WT-1 | 12 | 880999 | 495320 |
| IL-6_WT-2 | 12 | 966623 | 519514 |
| IL-6_WT-3 | 12 | 998852 | 552746 |
| 30 个 mutant 组 | 360 | 35541730 | 21503516 |

### FASTA 氨基酸交付

header 保留来源序列/翻译标识及 `;sample=<库名>`，不能假定与仪器 FASTQ read ID 逐条相等。序列是来源表达串，未裁剪信号前缀或 His6；精确信号前缀记录为 23525564，His6 后缀记录为 24036149。已逐文件检查实际 header、长度、字符、重复序列数；不同 header 可对应同一序列，不能将记录数当唯一抗体数。全体 FASTA 的非标准氨基酸字符计数为 `{}`，raw 中不做替换。

### Zenodo 原标签表与计数归档

原 `il6_aai_dataset.csv` 的字段为 `VHH_sequence`, `label`, `Ag_label`, `Ag_sequence`。全部 573,891 个 (VHH_sequence, Ag_label) 键及 label 与固定 HF 版本精确相等；每个 Ag_label 的 Ag_sequence 也与 HF 抗原表精确相等。Zenodo 将抗原串写入每一配对行，HF 分成六列动物 metadata 主表和两列抗原表；schema 差异不是不同独立样本。

`libtable.tar.gz` 完整安全遍历得到以下原始计数表：

| 归档成员 | 记录数 | 字段数 | 未压缩 bytes |
| --- | --- | --- | --- |
| libtable/libtable_IL-6_T48A.tsv | 78803 | 39 | 18526878 |
| libtable/libtable_IL-6_E51A.tsv | 77413 | 39 | 18194832 |
| libtable/libtable_IL-6_D54A.tsv | 92840 | 39 | 21857374 |
| libtable/libtable_IL-6_L120A.tsv | 82809 | 39 | 19481231 |
| libtable/libtable_IL-6_L90A.tsv | 82348 | 39 | 19391592 |
| libtable/libtable_IL-6_P42A.tsv | 81319 | 39 | 19119512 |
| libtable/libtable_IL-6_I57A.tsv | 92867 | 39 | 21842380 |
| libtable/libtable_IL-6_T165A.tsv | 73023 | 39 | 17190671 |
| libtable/libtable_IL-6_WTs.tsv | 118129 | 63 | 33474174 |
| libtable/libtable_IL-6_I60A.tsv | 91470 | 39 | 21512395 |
| libtable/libtable_IL-6_L126A.tsv | 85228 | 39 | 20056562 |
| libtable/libtable_IL-6_S81A.tsv | 93511 | 39 | 21994687 |
| libtable/libtable_IL-6_L129A.tsv | 80217 | 39 | 18877506 |
| libtable/libtable_IL-6_S135A.tsv | 79340 | 39 | 18671869 |
| libtable/libtable_IL-6_E108A.tsv | 80655 | 39 | 18983370 |
| libtable/libtable_IL-6_G63A.tsv | 89011 | 39 | 20929614 |
| libtable/libtable_IL-6_C72A.tsv | 96607 | 39 | 22723901 |
| libtable/libtable_IL-6_D168A.tsv | 74333 | 39 | 17499065 |
| libtable/libtable_IL-6_F102A.tsv | 82196 | 39 | 19341390 |
| libtable/libtable_IL-6_Q144A.tsv | 72310 | 39 | 17004154 |
| libtable/libtable_IL-6_P93A.tsv | 85355 | 39 | 20088961 |
| libtable/libtable_IL-6_Q45A.tsv | 77845 | 39 | 18298158 |
| libtable/libtable_IL-6_T117A.tsv | 75225 | 39 | 17703501 |
| libtable/libtable_IL-6_F153A.tsv | 71820 | 39 | 16897560 |
| libtable/libtable_IL-6_E87A.tsv | 98275 | 39 | 23141949 |
| libtable/libtable_IL-6_K69A.tsv | 98069 | 39 | 23080518 |
| libtable/libtable_IL-6_C78A.tsv | 83600 | 39 | 19681496 |
| libtable/libtable_IL-6_E138A.tsv | 73392 | 39 | 17258336 |
| libtable/libtable_IL-6_G105A.tsv | 75319 | 39 | 17723508 |
| libtable/libtable_IL-6_D162A.tsv | 71059 | 39 | 16722612 |
| libtable/libtable_IL-6_D99A.tsv | 86471 | 39 | 20346611 |

归档还原样保留 1 个 AppleDouble 文件系统 metadata 成员；已核对魔数并完整读取，不把它们解码成实验 TSV 或计为 VHH 数据。所有表逐行核对库频次为非负整数、total 等于各库频次之和、表内 ID/sequence 唯一；实际 total 范围为 2–70344。

表 ID 是各 table 的本地记录键，不保证跨抗原表指向同一个 VHH；跨表应使用原 sequence 字符串。Mother/Serum 可出现在多个表中，不能重复累计为新的生物库。计数和 total 是测序频次，不是 KD 或独立 wet-lab replicate 数；本次未从频次重建统计标签。

### 字段说明

| 文件 | 字段原始拼写 | 类型、单位、来源和边界 |
| --- | --- | --- |
| *.fastq.gz | header / DNA / + / quality | 四行记录；DNA 为 A/C/G/T/N；quality 为 Phred+33 ASCII，每碱基一字符；无亲和力单位 |
| *.fasta | header;sample / sequence | 字符串；作者处理的氨基酸表达串；保留信号/His6，sample 指库，重复序列不是独立抗体 |
| il6_aai_dataset.csv | VHH_sequence / Ag_sequence | 完整来源氨基酸构建体字符串；不是仅 CDR，不能按成熟序列的位置直接使用 mutant 数字 |
| il6_aai_dataset.csv | Ag_label / label | 31 个抗原键；0/1 为统计标注的 non-binder/binder，无连续 KD 单位 |
| libtable 原始 TSV | #ONU ID | 字符串；各表内的来源 ID，不能假定跨表为同一抗体 |
| libtable 原始 TSV | sequence | 氨基酸表达串；跨表连接和独立字符串去重的键，未裁剪信号/His6 |
| libtable 原始 TSV | total | 非负整数原文；该行所有库列出现频次的和，无亲和力单位 |
| libtable 原始 TSV | IL-6_C72A-a / IL-6_C72A-b / IL-6_C72A-c / IL-6_C72A-d / IL-6_C72A-e / IL-6_C72A-f / IL-6_C72A-g / IL-6_C72A-h / IL-6_C72A-i / IL-6_C72A-j / IL-6_C72A-k / IL-6_C72A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_C78A-a / IL-6_C78A-b / IL-6_C78A-c / IL-6_C78A-d / IL-6_C78A-e / IL-6_C78A-f / IL-6_C78A-g / IL-6_C78A-h / IL-6_C78A-i / IL-6_C78A-j / IL-6_C78A-k / IL-6_C78A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_D162A-a / IL-6_D162A-b / IL-6_D162A-c / IL-6_D162A-d / IL-6_D162A-e / IL-6_D162A-f / IL-6_D162A-g / IL-6_D162A-h / IL-6_D162A-i / IL-6_D162A-j / IL-6_D162A-k / IL-6_D162A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_D168A-a / IL-6_D168A-b / IL-6_D168A-c / IL-6_D168A-d / IL-6_D168A-e / IL-6_D168A-f / IL-6_D168A-g / IL-6_D168A-h / IL-6_D168A-i / IL-6_D168A-j / IL-6_D168A-k / IL-6_D168A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_D54A-a / IL-6_D54A-b / IL-6_D54A-c / IL-6_D54A-d / IL-6_D54A-e / IL-6_D54A-f / IL-6_D54A-g / IL-6_D54A-h / IL-6_D54A-i / IL-6_D54A-j / IL-6_D54A-k / IL-6_D54A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_D99A-a / IL-6_D99A-b / IL-6_D99A-c / IL-6_D99A-d / IL-6_D99A-e / IL-6_D99A-f / IL-6_D99A-g / IL-6_D99A-h / IL-6_D99A-i / IL-6_D99A-j / IL-6_D99A-k / IL-6_D99A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_E108A-a / IL-6_E108A-b / IL-6_E108A-c / IL-6_E108A-d / IL-6_E108A-e / IL-6_E108A-f / IL-6_E108A-g / IL-6_E108A-h / IL-6_E108A-i / IL-6_E108A-j / IL-6_E108A-k / IL-6_E108A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_E138A-a / IL-6_E138A-b / IL-6_E138A-c / IL-6_E138A-d / IL-6_E138A-e / IL-6_E138A-f / IL-6_E138A-g / IL-6_E138A-h / IL-6_E138A-i / IL-6_E138A-j / IL-6_E138A-k / IL-6_E138A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_E51A-a / IL-6_E51A-b / IL-6_E51A-c / IL-6_E51A-d / IL-6_E51A-e / IL-6_E51A-f / IL-6_E51A-g / IL-6_E51A-h / IL-6_E51A-i / IL-6_E51A-j / IL-6_E51A-k / IL-6_E51A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_E87A-a / IL-6_E87A-b / IL-6_E87A-c / IL-6_E87A-d / IL-6_E87A-e / IL-6_E87A-f / IL-6_E87A-g / IL-6_E87A-h / IL-6_E87A-i / IL-6_E87A-j / IL-6_E87A-k / IL-6_E87A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_F102A-a / IL-6_F102A-b / IL-6_F102A-c / IL-6_F102A-d / IL-6_F102A-e / IL-6_F102A-f / IL-6_F102A-g / IL-6_F102A-h / IL-6_F102A-i / IL-6_F102A-j / IL-6_F102A-k / IL-6_F102A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_F153A-a / IL-6_F153A-b / IL-6_F153A-c / IL-6_F153A-d / IL-6_F153A-e / IL-6_F153A-f / IL-6_F153A-g / IL-6_F153A-h / IL-6_F153A-i / IL-6_F153A-j / IL-6_F153A-k / IL-6_F153A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_G105A-a / IL-6_G105A-b / IL-6_G105A-c / IL-6_G105A-d / IL-6_G105A-e / IL-6_G105A-f / IL-6_G105A-g / IL-6_G105A-h / IL-6_G105A-i / IL-6_G105A-j / IL-6_G105A-k / IL-6_G105A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_G63A-a / IL-6_G63A-b / IL-6_G63A-c / IL-6_G63A-d / IL-6_G63A-e / IL-6_G63A-f / IL-6_G63A-g / IL-6_G63A-h / IL-6_G63A-i / IL-6_G63A-j / IL-6_G63A-k / IL-6_G63A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_I57A-a / IL-6_I57A-b / IL-6_I57A-c / IL-6_I57A-d / IL-6_I57A-e / IL-6_I57A-f / IL-6_I57A-g / IL-6_I57A-h / IL-6_I57A-i / IL-6_I57A-j / IL-6_I57A-k / IL-6_I57A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_I60A-a / IL-6_I60A-b / IL-6_I60A-c / IL-6_I60A-d / IL-6_I60A-e / IL-6_I60A-f / IL-6_I60A-g / IL-6_I60A-h / IL-6_I60A-i / IL-6_I60A-j / IL-6_I60A-k / IL-6_I60A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_K69A-a / IL-6_K69A-b / IL-6_K69A-c / IL-6_K69A-d / IL-6_K69A-e / IL-6_K69A-f / IL-6_K69A-g / IL-6_K69A-h / IL-6_K69A-i / IL-6_K69A-j / IL-6_K69A-k / IL-6_K69A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_L120A-a / IL-6_L120A-b / IL-6_L120A-c / IL-6_L120A-d / IL-6_L120A-e / IL-6_L120A-f / IL-6_L120A-g / IL-6_L120A-h / IL-6_L120A-i / IL-6_L120A-j / IL-6_L120A-k / IL-6_L120A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_L126A-a / IL-6_L126A-b / IL-6_L126A-c / IL-6_L126A-d / IL-6_L126A-e / IL-6_L126A-f / IL-6_L126A-g / IL-6_L126A-h / IL-6_L126A-i / IL-6_L126A-j / IL-6_L126A-k / IL-6_L126A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_L129A-a / IL-6_L129A-b / IL-6_L129A-c / IL-6_L129A-d / IL-6_L129A-e / IL-6_L129A-f / IL-6_L129A-g / IL-6_L129A-h / IL-6_L129A-i / IL-6_L129A-j / IL-6_L129A-k / IL-6_L129A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_L90A-a / IL-6_L90A-b / IL-6_L90A-c / IL-6_L90A-d / IL-6_L90A-e / IL-6_L90A-f / IL-6_L90A-g / IL-6_L90A-h / IL-6_L90A-i / IL-6_L90A-j / IL-6_L90A-k / IL-6_L90A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_P42A-a / IL-6_P42A-b / IL-6_P42A-c / IL-6_P42A-d / IL-6_P42A-e / IL-6_P42A-f / IL-6_P42A-g / IL-6_P42A-h / IL-6_P42A-i / IL-6_P42A-j / IL-6_P42A-k / IL-6_P42A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_P93A-a / IL-6_P93A-b / IL-6_P93A-c / IL-6_P93A-d / IL-6_P93A-e / IL-6_P93A-f / IL-6_P93A-g / IL-6_P93A-h / IL-6_P93A-i / IL-6_P93A-j / IL-6_P93A-k / IL-6_P93A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_Q144A-a / IL-6_Q144A-b / IL-6_Q144A-c / IL-6_Q144A-d / IL-6_Q144A-e / IL-6_Q144A-f / IL-6_Q144A-g / IL-6_Q144A-h / IL-6_Q144A-i / IL-6_Q144A-j / IL-6_Q144A-k / IL-6_Q144A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_Q45A-a / IL-6_Q45A-b / IL-6_Q45A-c / IL-6_Q45A-d / IL-6_Q45A-e / IL-6_Q45A-f / IL-6_Q45A-g / IL-6_Q45A-h / IL-6_Q45A-i / IL-6_Q45A-j / IL-6_Q45A-k / IL-6_Q45A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_S135A-a / IL-6_S135A-b / IL-6_S135A-c / IL-6_S135A-d / IL-6_S135A-e / IL-6_S135A-f / IL-6_S135A-g / IL-6_S135A-h / IL-6_S135A-i / IL-6_S135A-j / IL-6_S135A-k / IL-6_S135A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_S81A-a / IL-6_S81A-b / IL-6_S81A-c / IL-6_S81A-d / IL-6_S81A-e / IL-6_S81A-f / IL-6_S81A-g / IL-6_S81A-h / IL-6_S81A-i / IL-6_S81A-j / IL-6_S81A-k / IL-6_S81A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_T117A-a / IL-6_T117A-b / IL-6_T117A-c / IL-6_T117A-d / IL-6_T117A-e / IL-6_T117A-f / IL-6_T117A-g / IL-6_T117A-h / IL-6_T117A-i / IL-6_T117A-j / IL-6_T117A-k / IL-6_T117A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_T165A-a / IL-6_T165A-b / IL-6_T165A-c / IL-6_T165A-d / IL-6_T165A-e / IL-6_T165A-f / IL-6_T165A-g / IL-6_T165A-h / IL-6_T165A-i / IL-6_T165A-j / IL-6_T165A-k / IL-6_T165A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_T48A-a / IL-6_T48A-b / IL-6_T48A-c / IL-6_T48A-d / IL-6_T48A-e / IL-6_T48A-f / IL-6_T48A-g / IL-6_T48A-h / IL-6_T48A-i / IL-6_T48A-j / IL-6_T48A-k / IL-6_T48A-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_WT-1-a / IL-6_WT-1-b / IL-6_WT-1-c / IL-6_WT-1-d / IL-6_WT-1-e / IL-6_WT-1-f / IL-6_WT-1-g / IL-6_WT-1-h / IL-6_WT-1-i / IL-6_WT-1-j / IL-6_WT-1-k / IL-6_WT-1-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_WT-2-a / IL-6_WT-2-b / IL-6_WT-2-c / IL-6_WT-2-d / IL-6_WT-2-e / IL-6_WT-2-f / IL-6_WT-2-g / IL-6_WT-2-h / IL-6_WT-2-i / IL-6_WT-2-j / IL-6_WT-2-k / IL-6_WT-2-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | IL-6_WT-3-a / IL-6_WT-3-b / IL-6_WT-3-c / IL-6_WT-3-d / IL-6_WT-3-e / IL-6_WT-3-f / IL-6_WT-3-g / IL-6_WT-3-h / IL-6_WT-3-i / IL-6_WT-3-j / IL-6_WT-3-k / IL-6_WT-3-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | Mother-a / Mother-b / Mother-c / Mother-d / Mother-e / Mother-f / Mother-g / Mother-h / Mother-i / Mother-j / Mother-k / Mother-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |
| libtable 原始 TSV | Serum-a / Serum-b / Serum-c / Serum-d / Serum-e / Serum-f / Serum-g / Serum-h / Serum-i / Serum-j / Serum-k / Serum-l | 非负整数原文；各库的 VHH 出现次数；零表示该库未观测该串，不是非结合 label；无亲和力单位 |

### 数据示例

`IL-6_C72A-a.fasta` 第一条真实记录：

```text
>1333_1 1:N:0:271;sample=IL-6_C72A-a
MKYLLPTAAAGLLLLAAQPAMAQVQLQESGGGEVQPGGSLTLSCAASGSSFSVDSMGWYRQPPGKQRELIADITSSGRTDYADSVKGRFTISRNNAKNTVYLQMNSLKPEDTAVYYCHKGMDYWGKGTQVTVSSHHHHHH
```

一条记录是该库的处理后 read 表示，不是唯一 VHH。原标签 CSV 第一条真实配对：

| VHH_sequence | label | Ag_label | Ag_sequence |
| --- | --- | --- | --- |
| MKYLLPTAAAGLLLLAAQPAMAQVQLQESGGGLVQAGGSLRLSCAASGRTFSSYAMGWFRQAPGKEREFVAAISWSGGSTYYADSVKGRFTISRDNANNTVYLQMNSLKPEDTAVYACAADLLYHPGSWNDYWGQGTQVTVSSHHHHHH | 1 | IL-6_WTs | MNSFSTSAFGPVAFSLGLLLVLPAAFPAPVPPGEDSKDVAAPHRQPLTSSERIDKQIRYILDGISALRKETCNKSNMCESSKEALAENNLNLPKMAEKDGCFQSGFNEETCLVKIITGLLEFEVYLEYLQNRFESSEEQARAVQMSTKVLIQFLQKKAKNLDAITTPDPTTNASLLTKLQAQNQWLQDMTTHLILRSFKEFLQSSLRALRQMHHHHHH |

一行是汇总后的 VHH–抗原版本标签；该 VHH 可关联其他 Ag_label。第一个 libtable 的第一条真实行：

| #ONU ID | IL-6_T48A-a | IL-6_T48A-b | IL-6_T48A-c | IL-6_T48A-d | IL-6_T48A-e | IL-6_T48A-f | IL-6_T48A-g | IL-6_T48A-h | IL-6_T48A-i | IL-6_T48A-j | IL-6_T48A-k | IL-6_T48A-l | Mother-a | Mother-b | Mother-c | Mother-d | Mother-e | Mother-f | Mother-g | Mother-h | Mother-i | Mother-j | Mother-k | Mother-l | Serum-a | Serum-b | Serum-c | Serum-d | Serum-e | Serum-f | Serum-g | Serum-h | Serum-i | Serum-j | Serum-k | Serum-l | total | sequence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Onu1 | 388 | 0 | 3 | 22 | 9379 | 1006 | 97 | 13 | 5 | 0 | 5 | 6 | 4 | 0 | 0 | 0 | 978 | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 1090 | 4 | 1 | 15 | 14808 | 4135 | 16 | 11 | 3 | 0 | 14 | 5 | 32027 | MKYLLPTAAAGLLLLAAQPAMAQVQLQESGGGLVQAGGSLRLSCIASGSTFSSYRMGWFRQAPGKEREFVAAISHFGISTYYADSVKGRFTISRDNAKNIVYLQMNSLKPEDTASYYCAADGDPYHRNYERLGEYDYWGQGTQVTVSSHHHHHH |

## PDB 数据库

审计论文 Methods / Appendix、作者数据 card 和全部两个 CSV；没有逐 VHH PDB ID 或配对实测复合物。接受靶点代表 1IL6：RCSB entity 1、author chain A、INTERLEUKIN-6、UniProt P05231，185 aa。canonical FASTA 的完整 185 aa 在公开 WT 构建体位置 28–212 精确出现，前面 27 aa 和后面 HHHHHH 不在该参考实体；这只支持 mature WT 靶点区域关系，不能映射 30 个 mutant 的实验坐标，也不能映射 38,599 个 VHH 的结合界面。只有一个外部锚点、一个 FASTA record 和一个完整 mmCIF，不能声称 573,891 份结构覆盖。FASTA 与 mmCIF canonical 序列一致，坐标解析通过。

2026-09-18 获取；每个接受锚点的 FASTA 与 mmCIF 均通过 entry ID、canonical polymer entity 序列和 atom_site 验证。PDB 补充按上述参考映射完成；实验变体 / ADI 抗体 / VHH 的逐样本复合物没有取得。

| PDB | 文件 | 大小 / bytes | SHA-256 |
| --- | --- | --- | --- |
| 1IL6 | `pdb/sequences/rcsb_pdb_1IL6.fasta` | 236 | `02e1ae336b1a7a41da6b70f2bc44e4662883964071cc9b27da7ec8324c12aa67` |
| 1IL6 | `pdb/structures/1IL6.cif` | 285898 | `e099e7abd3d7509a99566ba0c62a1697d31c32541b5fe07ef47ed5f7e0495997` |

FASTA：`https://www.rcsb.org/fasta/entry/<PDB>/download`；坐标：`https://files.rcsb.org/download/<PDB>.cif`。完整原样保存，不生成衍生序列或独立 PDB manifest。

新增 FASTQ/FASTA/计数表/CSV 未提供新的逐配对结构锚点；本版本复用同一 WT 靶点代表，逐字节复制已有已验收 RCSB 原文件后重新核对完整 entity canonical 序列、entry ID、atom_site、bytes/SHA-256，不替换或拼接任何 VHH/IL-6 mutant 序列。

## 使用方式

调用者将 `dataset_root` 赋为本 source version 目录；CSV 与 tar 分别读取，FASTQ 使用 gzip/FASTQ parser，FASTA 使用氨基酸 FASTA parser：

```python
import csv
from pathlib import Path
with (Path(dataset_root) / 'AVIDa-hIL6-Zenodo/il6_aai_dataset.csv').open(encoding='utf-8', newline='') as handle:
    first = next(csv.DictReader(handle))
print(first['Ag_label'], first['label'])
```

## 采集过程记录

1. 2026-09-18 用户要求严格完成 skill 接入范围。纠正此前将 HF 四对象称为整体完成的过早判断，保留 HF 已发布版本；重新对照作者项目页、固定 GitHub README、论文 Methods/Appendix 和 Zenodo API，发现额外 libtable.tar.gz。
2. 2026-09-18 Drive 网页每目录只显示首屏 50 项；改用包含 shared-drive 参数的匿名 v2 API 完整枚举，核对真实容器名称、对象 ID、MIME、字节、version、修改日和官方 MD5，得到 840 FASTQ / 420 FASTA。所有对象为普通二进制文件；浏览器应用 key 仅在内存使用，不写入配置、URL 日志或 Git。
3. 2026-09-18 先采用 API media 下载，部分文件返回 403，而同一公开文件的标准网页下载端点返回 206；改用 Google Drive 官方公共网页下载端点，严格检查 Range/Content-Range，再验官方 MD5。早期仅杀 Python 主进程使 curl 子进程未退出，重试出现 Zenodo partial 并发写入；tar partial 超过官方大小，隔离两个不可信 partial 并重新下载，未将其发布。改为同进程 requests stream 与逐对象文件锁，失败立即停止，消除孤儿进程写入路径。
4. 2026-09-18 payload 写至 `<source_id>/.staging/1.0.0.partial/`，网络中断仅保留可恢复的原字节前缀，文件完成后独立核对官方字节/MD5。Zenodo 长时 504/TLS 失败后查阅 2026-09-15 官方性能说明，采用透明自动客户端 User-Agent；record API 恢复 200。CSV 官方端点支持 HTTP gzip，本次仅解码 HTTP 传输包络，解码出的完整原文件再验官方 220,007,854 bytes / MD5，无 CSV 重序列化；原 byte-range prefix 在完整替代传输通过身份验证后清理。840 FASTQ 逐记录完整读取、gzip CRC/序列质量/mate ID 验收；420 FASTA 全解析；tar 完整安全遍历和表格 shape/schema 读取；原 CSV 的所有 labelled pairs 与冻结 HF 值精确比对。未重建 processed 标签或裁剪 raw 序列。
5. 2026-09-19 复用已取得的 arXiv v2（原名 2306.03329v2.pdf，按来源/发布日期改为 AVIDaHIL6_2023-10-11_arXiv-v2.pdf）及 1IL6 完整 FASTA/mmCIF，复制前后 bytes/SHA-256 相同并重新解析；另归档 arXiv v2 原始源包（9 成员）与固定 GitHub 代码归档（35 文件逐项 Git blob/大小比对），并保存官方 NeurIPS 20 页主文与独立 6 页 datasheet。NeurIPS 只公示出版年 2023；用户明确允许年级字段/文件名，记录本次例外，不将内嵌生成日 2023-10-10 当发布日期。所有支持文件原名、改名依据、bytes/SHA-256 核对与数据/文本/代码/PDB 分层许可分别保留。
6. 2026-09-19 本地工作稿编辑后立即同步本版本 README；严格格式合同、固定 markdownlint-cli2@0.20.0、全 payload/支持材料 inventory/no-sidecar 和无覆盖发布 gate 全部通过后原子发布。随后同步研究记录、状态、交接和学习回顾；公共总表只准备补丁，未越过 workspace 规则。
7. 2026-09-19 用户要求完整版本已覆盖精简版本时只保留完整版本。重新校验 HF 历史 inventory，逐项证明标签、抗原、subject 常量、论文与 PDB 均由 1.0.0 覆盖；`.gitattributes` 仅为 LFS 传输规则，data card 的来源/许可/schema 已进入本 README。随后删除 `snapshot-2024-11-19` raw 目录，保留冻结哈希和 `r40-hf-redundancy.json` 审计证据，再次同步 README 并通过 1.0.0 发布检查。

## 参考文献

- [作者项目页](https://cognanous.com/datasets/avida-hil6)
- [Zenodo 固定 record 7935862 / 1.0.0](https://zenodo.org/records/7935862)
- [固定作者 README 与预处理脚本](https://github.com/cognano/AVIDa-hIL6/tree/72ae4f743bfe51ea350f21b9b94e0cb1bdd5264f)
- [arXiv 2306.03329v2](https://arxiv.org/abs/2306.03329v2)
- [NeurIPS 2023 正式主文和独立 datasheet](https://proceedings.neurips.cc/paper_files/paper/2023/hash/8339dacd9df7ffe9623760f74169dd1e-Abstract.html)
- [NeurIPS 作者版权与出版许可说明](https://neurips.cc/FAQ)
- [HF 固定 revision](https://huggingface.co/datasets/COGNANO/AVIDa-hIL6/tree/cd783d573e015f83364e42287810ad597850aeed)
- [RCSB PDB 1IL6](https://www.rcsb.org/structure/1IL6)；保留条目原始结构论文引用。

## 其他

### 数据范围和限制

本版本覆盖作者声明的全部测序/序列目录和固定 Zenodo 全文件集合；HF 精简表示的全部科学字段经审计由本版本数据或固定作者代码覆盖，故不再保留为独立 raw 版本，避免后续重复计数。non-significant/noise 不在最终标签 CSV 中，原计数表提供来源计数输入；本次不把它们赋为非结合。原始仪器项目、实验验证图像/sensorgram 和逐 VHH 实测复合物未因此取得，不扩大‘完整公开交付接入’为未核验的所有实验材料获得。

### 完整性与验收

共 1262 个 payload / 21615383570 bytes，官方 MD5 和字节数逐对象通过，全部 FASTQ/FASTA/tar/CSV 内容验收通过。排序 `relative_path<TAB>bytes<TAB>sha256<LF>` 的 inventory SHA-256 为 `d28c0803d7724da094f9869b873f639d88086edeb03b7cfddf9f3c3aa0605ad5`；每文件来源 ID、官方 MD5 和本地 SHA-256 可通过仓库冻结配置/验收事实复核，source version 内无独立 manifest/API metadata/验证旁路文件。HF 删除前的 8 文件 / 113,577,359 bytes 冻结身份和覆盖判断保留在仓库审计事实中，不混入本 source version inventory。

### 许可和再分发边界

作者项目、GitHub 数据说明和 Zenodo 记录为 CC BY-NC 4.0：保留署名和非商业条件；GitHub MIT 为代码许可，不能用于覆盖实验数据许可。arXiv 文本为 non-exclusive distribution license，不等同数据许可；NeurIPS 作者保留版权并向 NeurIPS 授予非独占出版许可；公开 PDF/abstract 未单独标注文本 CC 许可，本项目保存内部研究归档，不能用数据 CC BY-NC 4.0 授予未声明的文本再分发权。外部分发论文需核对权利，公开可读不赋予无限第三方再分发权。PDB 参考需保留原结构引用。

### 公开范围对照

| 来源承诺 | 实际核验文件 | 状态 |
| --- | --- | --- |
| 840 FASTQ / 420 FASTA | 全目录、1260 对象官方 MD5；420 mate/FASTA 库 | 已包含 |
| Zenodo 1.0.0 全文件 | 原 CSV 与 libtable.tar.gz；全表与归档安全/CRC 验收 | 已包含 |
| 573,891 二元配对 | 原 CSV 与固定 HF 全配对 label / 抗原一致；精简 HF raw 已去重删除 | 已包含于 1.0.0 |
| 统计标签流程/补充 Methods | 20 页 arXiv v2、20 页正式主文、6 页 datasheet、原始源包和固定作者代码归档 | 已归档/核对 |
| WT 靶点代表结构 | 1IL6 canonical FASTA + 完整 mmCIF | 已补充 |
| 仪器项目、逐 VHH 实测复合物、重建 noise/non-significant 标签 | 无逐配对结构交付；未运行后续 processed 流程 | 未获得/未生成 |
