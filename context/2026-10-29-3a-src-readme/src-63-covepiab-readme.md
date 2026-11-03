---
tags:
  - context
---

# SRC_R63_COVEPIAB 数据说明

## 数据集身份

- `source_id`：`SRC_R63_COVEPIAB`
- `source_version`：`snapshot-2023-11-07`
- 原作者或发布机构：浙江大学药学院药物基因组学团队（Feng Zhu、Zhan Zhou 团队）
- 接入范围：`public-subset`

### 来源方背景

[浙江大学药物基因组学团队](https://pgx.zju.edu.cn/)隶属浙江大学药学院，维护 CovEpiAb、COVIEdb、TSNAdb 等药物基因组学与免疫信息学资源。CovEpiAb 论文列出的主要责任单位是浙江大学药学院先进药物递送与释放系统全国重点实验室、浙江省抗肿瘤药物研究重点实验室；通讯作者为 Feng Zhu 和 Zhan Zhou。[团队资源页](https://pgx.zju.edu.cn/Resource.html)把 CovEpiAb 列为其免疫信息学数据库之一。

## 实验设计和数据口径

CovEpiAb 是跨论文、数据库和结构条目的持续汇编，不是一次统一条件下的实验。论文说明，维护方先从 CoV-AbDab 取得抗体清单，再用冠状病毒抗体相关关键词检索 PubMed，合并、预处理并为别名抗体统一名称；2023-11-07 官网状态报告 12,613 个抗体。当前保存的抗体结果页包含 12,604 行，覆盖 `AB1` 至 `AB12613` 中除 9 个编号外的记录。

论文称维护方从文献中人工整理抗体对不同病毒株的亲和力与中和实验，结合测量包括 SPR、BLI 和 ELISA，中和测量包括假病毒与活病毒 assay。结合的 $K_D$ 被统一为 nM，并按小于 10、10–1000、大于 1000 nM 分为高、中、低或无结合；中和的 $IC_{50}$ 被统一为 µg/mL，并按小于 1、1–10、大于 10 µg/mL 分为强、弱、无中和。原研究的条件、仪器、replicate 和检测边界并不统一；网页展示的归一化值与分档不能当作同一实验平台的直接测量。

当前 payload 的形成关系是：

```text
CoV-AbDab、PubMed 文献与人工整理
                 │
                 ▼
12,613 个官网抗体条目及实验／结构注释
                 │
        ┌────────┼─────────┐
        ▼        ▼         ▼
检索条件页   结果汇总页   抗体详情与下载区
选择词表     12,604 行    当前未取得完整导出
        │
        └────── 829 个唯一 PDB ID ──────► RCSB 审计
```

结果页的 `Bind` 和 `Neutralizing` 是抗体级病毒或变体名称汇总，可能用 `<br>` 并列多个对象；它们不是逐 assay 的数值记录。`Structure` 同样是一个抗体可对应多个 PDB ID 的汇总字段。官网还报告 6,641 条 affinity records 和 62,916 条 neutralizing records，但这些逐实验明细不在当前三个网页快照或补充工作簿中。

论文补充工作簿不是抗体实验明细，而是 COVEP 表位预测工具阈值、HLA 支持范围与人群频率、预测表位数量及跨人冠状病毒保守序列。它为论文方法与预测资源提供辅助证据，不能与抗体结果页按行拼接。

## 论文原文

- 标题：CovEpiAb: a comprehensive database and analysis resource for immune epitopes and antibodies of human coronaviruses
- 作者：Xue Zhang、JingCheng Wu、Yuanyuan Luo、Yilin Wang、Yujie Wu、Xiaobin Xu、Yufang Zhang、Ruiying Kong、Ying Chi、Yisheng Sun、Shuqing Chen、Qiaojun He、Feng Zhu、Zhan Zhou
- 发表来源：*Briefings in Bioinformatics* 25(3): bbae183
- 归档文本版本：正式发表全文的 Europe PMC NLM JATS XML
- 发布日期：2024-04-22
- DOI：[10.1093/bib/bbae183](https://doi.org/10.1093/bib/bbae183)
- PMID / PMCID：[38653491](https://pubmed.ncbi.nlm.nih.gov/38653491/) / [PMC11036340](https://pmc.ncbi.nlm.nih.gov/articles/PMC11036340/)
- 本地文件：`articles/CovEpiAb_2024-04-23_BriefingsInBioinformatics-FullText.xml`
- 文件大小：141.93 KiB（145,337 bytes）
- SHA-256：`14b6cf018ddd63309d020c8d2643ba49a5edcf817bd9eb5bc2e1631ff768f47f`
- 文本许可：[Creative Commons Attribution-NonCommercial 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/)
- 补充图：`articles/CovEpiAb_2024-04-23_BriefingsInBioinformatics-SupplementaryFigures.docx`，3.06 MiB（3,209,462 bytes），SHA-256 `545b9f0ad40fc7386279a60d19953e594c8e6ba5cbc97f5955db4b35c86dd03e`
- 补充表：`CovEpiAb/CovEpiAb_2024-04-23_BriefingsInBioinformatics-SupplementaryTables.xlsx`，46.03 KiB（47,136 bytes），SHA-256 `27f9930031cd0ee6911da54d973205c47f7b53b341ac25633223673d9c7db84c`

补充 DOCX 包含 Figure S1–S3 和三个内嵌图片：表位识别 assay 汇总、抗体 V/J gene usage，以及治疗性制品对 SARS-CoV-2 变体的敏感性。补充 XLSX 包含 Table S1–S5；其结构在“数据结构”中逐表说明。

## 仓库内容

上游不是 Git 仓库或不可变 release，而是 [CovEpiAb 官网](https://pgx.zju.edu.cn/covepiab/)及论文补充材料。官网首页和抗体检索页均注明最近更新于 2023-11-07，因此 source version 使用 `snapshot-2023-11-07`；2024-04-22 发表的论文和补充材料作为解释该官网状态的关联材料，不改变数据库快照名。

```text
snapshot-2023-11-07/
└── CovEpiAb/
    ├── CovEpiAb_2023-11-07_Home.html
    ├── CovEpiAb_2023-11-07_AntibodySearch.html
    ├── CovEpiAb_2023-11-07_AntibodySearchResults.html
    └── CovEpiAb_2024-04-23_BriefingsInBioinformatics-SupplementaryTables.xlsx
```

四个 payload 合计 4.57 MiB（4,794,521 bytes）；按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接计算的 inventory SHA-256 为 `26010f371912c50afef809528809706bd815d3294f68bdc54e6cd75c3074e30a`。网页是原始 HTTP 响应快照，结果页内嵌完整 DataTables 数组；工作簿是正式论文补充表。论文 XML、补充图和 RCSB 文件分别位于 source version 的 `articles/` 与 `pdb/`，不属于上述上游 payload 树。

## 数据结构

### 官网概览快照

`CovEpiAb_2023-11-07_Home.html` 是官网首页快照，保存十个 label—count 概览卡、新闻和入口链接。计数同时混合人工整理记录、实验记录与计算预测，不可直接相加为样本数。

| 首页标签 | 官网计数 | 口径 |
| --- | ---: | --- |
| `Validated B epitopes` | 66,210 | 实验验证的 B-cell epitope |
| `Validated T epitopes` | 3,209 | 实验验证的 T-cell epitope |
| `Antibodies` | 12,613 | 抗体汇编条目 |
| `Antibody structures` | 988 | 官网结构记录，不等于唯一 PDB ID 数 |
| `Affinity Records` | 6,641 | 亲和力实验记录，当前未取得明细导出 |
| `Neutralizing Records` | 62,916 | 中和实验记录，当前未取得明细导出 |
| `Virological characteristics` | 91 | 变体病毒学特征记录 |
| `Therapeutics Records` | 111 | 治疗性制品记录 |
| `In vitro activity Records` | 10,158 | 体外活性记录 |
| `Predicted T epitopes` | 237,401 | 计算预测的 T-cell epitope |

### 抗体检索页与结果表

`CovEpiAb_2023-11-07_AntibodySearch.html` 保存检索表单的全部当前选项。除了 `Type`、`Structure` 和数值区间以外，多数选项是当前快照观察到的开放词表，不应外推为未来版本的封闭枚举。

| 检索字段 | 当前非空唯一选项数 | 内容 |
| --- | ---: | --- |
| `Type` | 2 | `Ab`、`Nb` |
| `Name` | 12,604 | 抗体显示名或别名 |
| `Protein` | 29 | 靶蛋白或表位区域 |
| `Origin` | 178 | 抗体来源开放文本 |
| `Bind_Virus` | 146 | 结合病毒株或变体 |
| `Neutra_Virus` | 219 | 中和病毒株或变体 |
| `HeavyV` / `HeavyJ` | 152 / 21 | 重链 V/J gene 及物种 |
| `LightV` / `LightJ` | 157 / 27 | 轻链 V/J gene 及物种 |
| `Structure` | 2 | `Available`、`Unavailable` |
| `PDBID` | 829 | 四字符 PDB ID |

`CovEpiAb_2023-11-07_AntibodySearchResults.html` 内嵌 12,604 × 7 的 JavaScript 数组，七列依次为 `ID`、`Name`、`Type`、`Protein`、`Bind`、`Neutralizing`、`Structure`。`ID` 中包含指向详情页的 HTML；其余多值字段以 `<br>` 分隔。当前有 11,830 行 `Bind` 非空、6,988 行 `Neutralizing` 非空、589 行 `Structure` 非空。

结果页的 `Type` 实测分布为：

| 原始取值 | 当前记录数 | 含义 |
| --- | ---: | --- |
| `Ab` | 11,799 | 常规抗体条目 |
| `Nb` | 787 | nanobody／单域抗体条目 |
| `scFv` | 17 | single-chain variable fragment 条目 |
| `VH Ab` | 1 | 仅重链可变区的抗体条目 |

### 论文补充表

`CovEpiAb_2024-04-23_BriefingsInBioinformatics-SupplementaryTables.xlsx` 有五个 sheet。标题、空白分隔行和分组表头均保留原样，所以“总行数”不是纯数据行数。

| Sheet | 总行 × 总列 | 数据范围 |
| --- | ---: | --- |
| `Table S1` | 19 × 3 | B/T-cell epitope prediction 工具及阈值 |
| `Table S2` | 124 × 8 | COVEP 支持的 HLA allele 列表 |
| `Table S3` | 134 × 17 | 入选 HLA allele 在人群中的计数和频率 |
| `Table S4` | 67 × 6 | 七种人冠状病毒各蛋白的预测表位数量 |
| `Table S5` | 119 × 4 | SARS-CoV-2 与其他 HCoV 同源蛋白中的保守序列 |

Table S2 的非空 allele 数为 HLA-A 51、HLA-B 91、HLA-C 19、HLA-DRB 120、HLA-DPA 5、HLA-DPB 75、HLA-DQA 20、HLA-DQB 35。Table S4 覆盖 SARS-CoV-2、SARS-CoV、MERS-CoV、HCoV-229E、HCoV-HKU1、HCoV-NL63 和 HCoV-OC43。Table S5 有 S 9、M 1、N 2、ORF1ab 104 段保守序列；论文说明 E 蛋白没有识别到保守序列。

### 字段说明

首页 HTML 没有独立表头，其实际数据字段就是“官网概览快照”列出的十个 label—count 对以及 `Last updated on Nov 7, 2023`。新闻、导航和说明文字是页面内容，不是额外的数据列。

抗体检索页字段如下：

| 原始字段 | 原始表示、单位和含义 |
| --- | --- |
| `csrfmiddlewaretoken` | Django 表单请求状态字段；不是数据标识，不应用于跨快照连接。 |
| `Type`、`Name` | 抗体类别和显示名选择器。检索页类别只有 `Ab`、`Nb`，但结果页还存在 `scFv` 与 `VH Ab`。 |
| `Protein`、`Origin` | 靶蛋白／表位区域和抗体来源开放词表；空选项表示不限定。 |
| `Bind_Virus`、`Neutra_Virus` | 结合或中和的病毒株、变体及突变组合开放词表；名称中的 `weak` 或强度词是原始文本的一部分。 |
| `HeavyV`、`HeavyJ`、`LightV`、`LightJ` | V/J gene 与物种选择词表；`ND` 表示上游未确定。 |
| `Structure`、`PDBID` | 是否有结构和 PDB entry 选择器。`PDBID` 是条目级标识，不包含 chain 角色。 |
| `Affinity_SPR`、`Affinity_BLI` | 结合亲和力区间；网页说明单位为 nM。当前区间为 `min-0.1`、`0.1-1.0`、`1.0-10.0`、`10.0-100.0`、`100.0-max`；较小值表示更强结合。 |
| `Affinity_ELISA_IC50`、`Affinity_ELISA_EC50` | ELISA 区间；当前区间为 `min-0.01`、`0.01-0.1`、`0.1-0.25`、`0.25-1.0`、`1.0-max`。页面只统一说明 binding affinity 为 nM，未逐字段给出更细 assay 条件。 |
| `IC50_LiveVirus`、`IC50_PseudoVirus` | 活病毒和假病毒中和 $IC_{50}$ 区间，单位 µg/mL；区间同 ELISA 五档，较小值表示更强中和。 |
| `Search` | 值为 `Search` 的提交按钮；不是数据字段。 |

抗体结果页七列如下：

| 原始字段 | 原始表示与含义 |
| --- | --- |
| `ID` | HTML 详情链接和 `AB<number>` 标识。当前 12,604 个值唯一；缺少 `AB126`、`AB134`、`AB196`、`AB332`、`AB333`、`AB630`、`AB4842`、`AB5739`、`AB10182`。 |
| `Name` | 抗体名称字符串；结果页每行非空。 |
| `Type` | 当前观察到 `Ab`、`Nb`、`scFv`、`VH Ab`，分布见上表。 |
| `Protein` | 靶蛋白或表位区域字符串；每行非空。 |
| `Bind` | 已报告结合的病毒、变体或突变组合；多值用 `<br>` 分隔，空白不能解释为统一阴性。 |
| `Neutralizing` | 已报告中和的病毒、变体或突变组合；多值用 `<br>` 分隔，空白不能解释为统一阴性。 |
| `Structure` | 一个或多个四字符 PDB ID，以 `<br>` 分隔；空白表示该结果行没有展示结构，不证明结构不存在。 |

补充工作簿的全部数据字段如下：

| Sheet | 原始字段 | 原始表示、单位和含义 |
| --- | --- | --- |
| `Table S1` | `Tool`、`Threshold` | 表位预测工具名和原始阈值字符串；第三列为空的排版占位。`>` 表示得分下界，`<` 表示上界，`average` 表示相对该工具平均值。 |
| `Table S2` | `HLA-A`、`HLA-B`、`HLA-C`、`HLA-DRB`、`HLA-DPA`、`HLA-DPB`、`HLA-DQA`、`HLA-DQB` | COVEP 可选 HLA allele 字符串；各列长度不同，尾部空白不是缺失实验值。 |
| `Table S3` | `HLA Locus`、`Source` | 第一列为 HLA locus，合并单元格展开时需向下填充；第二列实际保存具体 allele，如 `A*01:01`。 |
| `Table S3` | `LWK`、`YRI`、`ASW`、`CLM`、`MXL`、`PUR`、`CHB`、`CHD`、`CHS`、`JPT`、`CEU`、`FIN`、`GBR`、`TSI`、`Han dynasty` | 人群中的 `count (frequency%)` 字符串；`NA` 表示补充表没有该组合的数值。前 14 列来自 1000 Genomes 分组，最后一列标题在文件中为 `Zhou et al.`／`Han dynasty`。 |
| `Table S4` | `Coronavirus`、`Protein`、`Length` | 病毒名称、蛋白名和蛋白氨基酸长度；合并的病毒单元格需向下填充。 |
| `Table S4` | `No. B`、`No. T1`、`No. T2` | 预测 B-cell、MHC-I T-cell 和 MHC-II T-cell epitope 数量；均为非负整数，不是实验验证条目数。 |
| `Table S5` | `Protein`、`Start`、`End`、`Sequence` | SARS-CoV-2 蛋白、1-based inclusive 起止坐标和保守氨基酸序列；空白蛋白单元格需向下填充。全部 116 行均满足 `End - Start + 1 = len(Sequence)`。 |

### 数据示例

下面两行是抗体结果页内嵌数组的真实记录，HTML 换行在这里写成分号：

```text
ID=AB1
Name=Roberts_201
Type=Ab
Protein=S; RBD
Bind=SARS-CoV-1
Neutralizing=SARS-CoV-1
Structure=
```

```text
ID=AB13
Name=2B04
Type=Ab
Protein=S; RBD
Bind=SARS-CoV-2_WT
Neutralizing=SARS-CoV-2_WT; SARS-CoV-2_WT+D614G; SARS-CoV-2_WT+N501Y+D614G; SARS-CoV-2_Alpha(B.1.1.7)
Structure=7K9H; 7K9I
```

第一行没有结构字段，第二行把一个抗体与两个 PDB entry 关联；二者都只是抗体级汇总，不是逐 assay 数值行。

补充表中的真实记录包括：

```text
Table S1: Tool=Bepipred; Threshold=>0.35
Table S3: HLA Locus=HLA-A; Source=A*01:01; LWK=2 (1.11%); CEU=26 (17.33%); Han dynasty=766 (3.58%)
Table S4: Coronavirus=SARS-CoV-2; Protein=ORF1ab; Length=7096; No. B=1026; No. T1=4995; No. T2=5467
Table S5: Protein=S; Start=815; End=826; Sequence=RSFIEDLLFNKV
```

这些行分别表示预测阈值、人群 allele 频率、蛋白级预测计数和一段保守序列，粒度彼此不同，不能纵向拼接。

## PDB 数据库

结构锚点来自抗体检索页的 `PDBID` 选择器，并与结果页 `Structure` 列交叉核对。检索页和结果页共指向 829 个唯一 PDB ID；其中 `7NY5` 在 2026-09-25 的 RCSB holdings 状态为 `REMOVED`，RCSB 指向的最新替代 entry 为 `7P40`，而 `7P40` 已经是 CovEpiAb 的独立锚点，因此本版本拒绝重复或伪造 `7NY5` 文件，接受 828 个现存 entry。

当前 `pdb/` 有 828 个 RCSB entry 的完整 FASTA 与 mmCIF，共 1,656 个文件、1.59 GiB（1,711,163,110 bytes），确定性 inventory SHA-256 为 `e2f83cc938de542640e1f903ecda7b1e0b4b20931053735e8c07064108b94b86`。828 个 FASTA 文件共有 2,612 个 polymer records。独立验收逐个解析 FASTA 和 mmCIF，确认文件 identity、entry ID、mmCIF atom records 以及两种格式中的 canonical polymer sequence 集合一致。

映射强度是“抗体结果行—PDB entry”直接关联：589 个结果行的 `Structure` 非空，一个抗体可连接多个 entry。但公开结果页没有 antibody/antigen author-chain、polymer entity、实验 construct 边界或逐链角色说明，因此 828 个 entry 只能作为可追溯的完整结构锚点，不能把其中所有 polymer chain 自动标成该抗体的重链、轻链或抗原，也不能把官网的 988 条 `Antibody structures` 解读为 988 个唯一 PDB entry。

PDB archive 数据文件采用 [CC0 1.0](https://www.rcsb.org/pages/usage-policy)；使用时仍应尽可能引用各 entry 的原始结构作者和相应论文。

## 采集过程记录

- 2026-09-25：读取项目配置、开发者身份、项目级数据清单与本 skill 的 README 合同；确认当前开发者为 `wuhuawei`，共享存储根为 `/data/shared/CX029_binding_ranking`。
- 2026-09-25：从 CovEpiAb 官方首页、抗体检索页和无筛选的 `antibody/search_list/` 结果页保存三份 HTML；从正式论文入口取得 Supplementary Table S1–S5，并将网页状态固定为 `snapshot-2023-11-07`。下载均写入 source-level staging，未改写原文件。
- 2026-09-25：从 Europe PMC 取得正式全文 XML，从 OUP 正式补充入口取得 Figure S1–S3 DOCX；以 DOI、PMID、PMCID、标题、文件长度和 SHA-256 验证身份。
- 2026-09-25：检查官网新闻中“Provided data download files”指向的 `/covepiab/help#nav_Downloads`；`/covepiab/help`、`/help/`、`/download`、`/download/` 均返回 HTTP 404。保留浏览／检索快照和论文补充作为公开子集，不把失败路径描述成完整数据库已开放或已取得。
- 2026-09-25：从检索页发现 829 个唯一 PDB ID；拒绝已撤回的 `7NY5`，对其余 828 个 entry 下载 RCSB FASTA 与原样完整 mmCIF。下载脚本使用临时文件、断点可重跑和原子替换；没有写入占位文件。
- 2026-09-25：独立审计通过 6 个配置对象、4 个 payload、828 对 RCSB 文件、12,604 行结果数组、五个 XLSX sheet 和三个补充图；同时复核所有字段、枚举、缺失编号、结构 ID 与序列一致性。
- 2026-09-25：第一次调用原子发布器时把本地 README 相对路径多写了一层；发布器在审计和目录移动前以 `Missing or unsafe local README` 拒绝执行，staging 未改变。随后改用从 workflow 目录到 `../../docs/readme/r63.md` 的正确路径，并重新核对 staged README 字节一致性。
- 2026-09-25：通过 `scripts/publish.py` 把完整 staging 原子移动为正式目录 `SRC_R63_COVEPIAB/snapshot-2023-11-07`；发布器在移动前后分别运行独立审计，两次均确认 4 个 payload、1,656 个 PDB 文件和 828 个 PDB pair。发布后再次同步本 README，并完成最终只读审计。

## 参考文献

- [CovEpiAb 官方入口](https://pgx.zju.edu.cn/covepiab/)
- [CovEpiAb 抗体检索](https://pgx.zju.edu.cn/covepiab/antibody/)
- Zhang X, Wu J, Luo Y, et al. [CovEpiAb: a comprehensive database and analysis resource for immune epitopes and antibodies of human coronaviruses](https://doi.org/10.1093/bib/bbae183). *Briefings in Bioinformatics*. 2024;25(3):bbae183.
- [PMC 正式全文与补充材料](https://pmc.ncbi.nlm.nih.gov/articles/PMC11036340/)
- [COVEP 源代码](https://github.com/zjupgx/COVEP)；该代码入口用于解释预测流程，不属于当前 source payload。
- [RCSB PDB 使用政策](https://www.rcsb.org/pages/usage-policy)

## 其他

### 数据范围和限制

当前版本是“公开可验证子集”，不是论文所称 CovEpiAb 全库的导出。它能支持抗体名称、类别、靶蛋白、定性结合／中和对象、PDB entry 和检索词表审计，也能支持论文补充表的 COVEP/HLA/保守序列复核；它不含抗体详情页中的完整重轻链序列、来源文献、逐实验 $K_D$／$IC_{50}$ 明细、assay 条件、原始曲线、逐孔数据或全库 epitope/variant/therapeutics 表。

网页快照中的计数是不同实体和处理层次：12,613 个抗体、6,641 个 affinity records、62,916 个 neutralizing records、988 条结构记录及 237,401 个计算预测 T epitopes 不能相加为独立实验数。结果表的 12,604 行也不能用来替代未取得的逐实验记录。

### 完整性与验收

四个 payload 文件、两份论文材料和 1,656 个 RCSB 文件的路径、字节数、SHA-256、格式和内部 identity 均通过独立审计；source version 内没有旁路 manifest、API 响应、临时文件或符号链接。XLSX sheet shape、HLA 列计数、病毒／蛋白覆盖、保守序列坐标、DOCX 媒体、论文标题与 DOI 均经内容级检查。

完整性结论只适用于上述文件集合。官网完整下载端点不可用、9 个抗体 ID 未出现在结果数组、网页与论文的实验记录计数口径存在歧义，因此 source 状态为 `published-verified public-subset` 时仍不表示完整研究数据库已经获得。

### 许可和再分发边界

- 正式论文 XML 和两份补充材料随论文采用 CC BY-NC 4.0；非商业复用、分发和改编需保留署名及许可条件，商业复用需另行取得许可。
- CovEpiAb 官网页脚写有 `Copyright © 2022. CovEpiAb All rights reserved.`，未发现覆盖数据库内容、网页快照或上游汇编记录的独立开放数据许可。论文文本的 CC BY-NC 4.0 不能自动扩展到数据库及其各上游来源。本项目可保存并审计公开入口的内部研究快照，但不能据此宣称允许对外再分发或商业使用。
- RCSB/wwPDB archive 的 FASTA 与 mmCIF 数据文件采用 CC0 1.0；应尽可能引用原始结构作者与 entry 论文。
- COVEP GitHub 代码不在本 source version 内；其代码许可不能代替 CovEpiAb 数据许可。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 12,613 个抗体 | 首页计数 12,613；结果页 12,604 行、9 个编号缺失 | 部分取得，计数差异待确认 |
| 抗体结合与中和实验明细 | 首页计数 6,641 affinity、62,916 neutralizing；结果页只保存抗体级对象汇总 | 完整数值明细未取得 |
| 988 条抗体结构记录 | 结果页 589 个有结构的抗体行、829 个唯一 PDB ID | 828 个现存 RCSB entry 已完整补齐；1 个撤回 |
| B/T-cell epitope 与预测资源 | 首页保留总计数；Table S1–S5 保留预测阈值、HLA、预测计数与保守序列 | 论文补充范围已取得，全库 epitope 导出未取得 |
| 主论文和 Supplementary Figure/Table | XML、DOCX、XLSX 均通过 identity 和 hash 验证 | 已取得 |
| COVEP 代码 | 论文指向公开 GitHub | 本 source 不纳入代码；不影响数据库子集发布 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-25；不阻塞公开子集发布，阻塞完整研究数据获得）：论文称所有 CovEpiAb 数据可在官网取得，首页也曾发布下载通知，但 `/covepiab/help#nav_Downloads` 及已核对的相关 download 路径当前均返回 404。现有替代证据是首页、检索页、12,604 行结果页和论文补充材料；下一步是站点恢复下载页、发现可验证的一手导出端点，或维护方提供正式全库文件后，补齐 affinity、neutralization、epitope、variant 与 therapeutics 明细并重新验收。
- `Q02`（最近更新：2026-09-25；不阻塞公开子集发布，影响抗体总量解释）：官网报告 12,613 个抗体，但结果数组只有 12,604 个唯一 `AB` ID，缺少 9 个明确编号。当前保留两种口径且不补造行；下一步需用官方全库导出或维护方说明确认这些编号是删除、隐藏、权限过滤还是页面生成遗漏。
- `Q03`（最近更新：2026-09-25；不阻塞公开子集发布，影响实验记录总量解释）：官网分别报告 6,641 条 affinity 和 62,916 条 neutralizing records，而论文 Methods 和 Results 把 62,916 描述为 affinity 与 neutralizing experimental data points。当前不相加或改写任何口径；待正式导出或作者数据字典说明总数、子集关系和去重键后关闭。
- `Q04`（最近更新：2026-09-25；不阻塞项目内研究快照，限制对外再分发和商业用途）：官网未给出数据库级开放许可，页脚保留 all rights reserved；论文 CC BY-NC 4.0 只覆盖论文及其补充材料。当前按对象分层记录许可，不把论文许可外推到数据库；若需对外发布 CovEpiAb 网页或数据库内容，须取得维护方明确授权或找到覆盖目标对象的一手条款。
