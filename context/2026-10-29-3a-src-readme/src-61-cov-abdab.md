# SRC_R61_COV_ABDAB 数据说明

## 数据集身份

- `source_id`：`SRC_R61_COV_ABDAB`
- `source_version`：`snapshot-2024-02-08`
- 原作者或发布机构：牛津大学统计系 Oxford Protein Informatics Group（OPIG；Charlotte M. Deane 团队）

### 来源方背景

[OPIG](https://www.stats.ox.ac.uk/opig) 是牛津大学统计系的跨学科研究组，研究抗体、小分子和蛋白质，并把实验数据与深度学习、生成模型、计算统计及物理方法结合起来。其免疫信息学方向包括抗体结构预测、优化与设计，以及传染病研究。OPIG 官网注明团队由 [Charlotte Deane](https://www.stats.ox.ac.uk/people/charlotte-deane) 领导；[CoV-AbDab 正式页面](https://opig.stats.ox.ac.uk/webapps/covabdab/)则明确说明该组发布并维护这一冠状病毒抗体数据库。

## 实验设计和数据口径

CoV-AbDab 不是一次统一实验产生的数据集，而是持续维护的文献、专利和结构信息汇编。论文 Methods 说明，作者以冠状病毒结合抗体为检索对象，从 PubMed、bioRxiv、medRxiv、GenBank 和 Google Patents 收集论文与专利记录；社区也可以向维护方补交数据。作者只纳入已有实验结合或中和证据的个案，再为每个抗体或纳米抗体条目整理名称、抗原与变体、结合和中和结论、来源、序列、germline、结构及参考文献。

当前公开数据的形成关系可概括为：

```text
论文、预印本、专利、GenBank 与作者提交
                    │
                    ▼
       人工整理抗体／纳米抗体条目及证据
                    │
        ┌───────────┼────────────┐
        ▼           ▼            ▼
CSV 主表       ANARCI 编号     SAbDab / PDB 检索
12,918 行      与 V/J 注释      IMGT 编号结构归档
12,916 名称    24,442 个键      988 个 PDB 文件
        │                            │
        └────文件间存在已核实差异────┘
```

每个 CSV 行是一条维护记录，而不是一次 assay、一个独立实验样本或一个统一条件下的抗体—抗原测量。文件有 12,918 行和 12,916 个不同 `Name`；`R15-F7` 与 `ADI-62113` 各出现两行，而且来源、序列或功能注释并不完全相同，所以 `Name` 不能直接当作严格主键。类型列包含 12,117 行常规抗体（`Ab`）和 801 行纳米抗体／单域抗体（`Nb`）。

`Binds to`、`Doesn't Bind to`、`Neutralising Vs` 和 `Not Neutralising Vs` 汇总不同原始研究报告过的定性证据，并用分号并列多个病毒或变体；`(weak)` 等限定词也是原始注释的一部分。空白表示当前单元格没有记录，可能源于未测试、未报告或尚未整理，不能统一解释为阴性。主表没有共同 assay 条件、浓度、replicate、原始曲线、$K_D$、$IC_{50}$ 或其他可跨来源直接比较的连续亲和力数值，因此更适合支持文献证据检索、序列与结构索引，以及在重新追溯原始研究后的任务构造。

ANARCI 是用于抗原受体序列编号和 germline assignment 的软件；论文说明作者用它按 IMGT scheme 编号氨基酸序列，并分配 V/J gene origin。SAbDab 用于发现已经进入 PDB 的相关结构。论文还说明 ABodyBuilder 曾为有序列的条目生成全 Fv 或 VHH 同源模型，但当前公开快照没有可取得的模型文件，具体边界见文末待解决问题。

论文在 2020-08-05 描述的是当时 1,402 个条目的早期数据库；本 source version 对应官网标注的 2024-02-08 快照，内容已扩展到 12,916 个不同名称。早期论文中的数量用于解释建库方法，不能代替当前文件实查统计。

## 论文原文

### 正式发表版

- 标题：CoV-AbDab: the coronavirus antibody database
- 作者：Matthew I. J. Raybould、Aleksandr Kovaltsuk、Claire Marks、Charlotte M. Deane
- 发表来源：*Bioinformatics* 37(5):734–735
- 归档文本版本：正式发表版，在线核对
- 发布日期：2020-08-17
- DOI：[10.1093/bioinformatics/btaa739](https://doi.org/10.1093/bioinformatics/btaa739)
- PMID / PMCID：[32805021](https://pubmed.ncbi.nlm.nih.gov/32805021/) / [PMC7558925](https://pmc.ncbi.nlm.nih.gov/articles/PMC7558925/)
- 正文在线入口：[OUP 正式论文](https://academic.oup.com/bioinformatics/article/37/5/734/5893556)；[PMC 全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC7558925/)
- 本地归档：未归档排版正式版；本地保存下述作者接受稿
- 文本许可：OUP Standard Journals Publication Model；不采用 CoV-AbDab 数据的 CC BY 4.0 代替论文文本条款
- 补充材料：`articles/CoV-AbDab_2020-08-17_Bioinformatics-Supplementary.pdf`，20 页，1.28 MiB（1,338,199 bytes），SHA-256 `5ed4169925b71b707a46c402cda865d3d0bb23238cfb0ff2ead540042665092c`
- 引用数（查询快照）：439（[OpenAlex W3049166744](https://openalex.org/W3049166744)，查询于 2026-09-24）

### 作者接受稿

- 标题：CoV-AbDab: the Coronavirus Antibody Database
- 作者：Matthew I. J. Raybould、Aleksandr Kovaltsuk、Claire Marks、Charlotte M. Deane
- 发表来源：Oxford University Research Archive 中与上述 *Bioinformatics* 论文对应的稿件
- 归档文本版本：作者接受稿
- 发布日期：2020-08-17
- DOI：[10.1093/bioinformatics/btaa739](https://doi.org/10.1093/bioinformatics/btaa739)
- PMID / PMCID：[32805021](https://pubmed.ncbi.nlm.nih.gov/32805021/) / [PMC7558925](https://pmc.ncbi.nlm.nih.gov/articles/PMC7558925/)
- 本地文件：`articles/CoV-AbDab_2020-08-17_Author-Accepted-Manuscript.pdf`
- 文件大小：82.87 KiB（84,856 bytes）
- SHA-256：`ef5262c9e94b571e058f20e5b8d887c96b6b29e89f457f051440d445db6e81b1`
- 文本许可：[Oxford University Research Archive Terms of Use](https://ora.ox.ac.uk/terms_of_use)；ORA 记录注明版权人为 Raybould 等作者
- 补充材料：无；20 页补充 PDF 归在正式发表版条目下

作者接受稿完整包含主文的研究动机、数据来源、数据库内容和使用说明，但版面仍保留投稿阶段的 DOI、编辑和日期占位符；书目信息以正式发表版为准。

## 仓库内容

上游不是 Git 仓库或带 DOI 的不可变 release，而是 [CoV-AbDab 正式网页](https://opig.stats.ox.ac.uk/webapps/covabdab/)提供的 HTTP 文件。页面显示最近更新于 2024-02-08，文件名也使用 `080224`，因此本项目将版本命名为 `snapshot-2024-02-08`。服务器在 2026-09-24 报告三个对象的 `Last-Modified` 为 2024-11-05；由于页面内容与文件名没有同步变更，本项目使用下列精确字节数和 SHA-256 固定本次取得的对象，不把服务器文件时间解释为新的数据库版本。

```text
snapshot-2024-02-08/
└── CoV-AbDab/
    ├── CoV-AbDab_080224.csv
    ├── CoV-AbDab_ANARCINumberings_080224.json
    └── CoV-AbDab_PDBStructures_080224.tar.gz
```

CSV 是数据库主表，JSON 是 ANARCI 编号结果，TAR.GZ 是维护方提供的 IMGT-numbered PDB 结构归档。三项 payload 合计 353.60 MiB（370,774,781 bytes），确定性 inventory SHA-256 为 `04d1a550c1953edf93f38c1728032e187b3a2ea4d93417f493334e00356546f3`。

## 数据结构

### CSV 主表

`CoV-AbDab_080224.csv` 为 UTF-8 CSV，包含 12,918 行和 23 列。每行是一条数据库维护记录；同名记录可能来自不同文献或专利，且字段内容可能不同。四个功能证据字段和 `Structures` 可在单元格内用分号保存多个值，不能用简单的“非空即单一标签”方式解析。

序列覆盖情况如下：

| 字段 | 有序列 | `ND` | 空白 |
| --- | ---: | ---: | ---: |
| `VHorVHH` | 12,346 | 572 | 0 |
| `VL` | 10,523 | 1,589 | 806 |
| `CDRH3` | 12,907 | 11 | 0 |
| `CDRL3` | 12,051 | 56 | 811 |

801 个 `Nb` 行的 `VL` 均为空；12,117 个 `Ab` 行中另有 5 行 `VL` 为空、1,589 行为 `ND`。部分序列或 CDR 字段含尾随空格，`US10822379B1-#8` 的 `CDRL3` 还被误写为两个 RCSB URL；这些上游原值均未在 raw 层修正。

### ANARCI 编号 JSON

`CoV-AbDab_ANARCINumberings_080224.json` 是一个含 24,442 个键的 JSON object。抗体链通常使用 `<Name>_VH` 和 `<Name>_VL`，纳米抗体通常直接使用 `<Name>`；每个值是编号位置与单字符 residue 的列表，位置写成 `[IMGT_number, insertion_code]`，对齐缺口以 `-` 表示。

按当前 CSV 中的可用序列和上述命名规则可构造 22,866 个不同键。两文件的实测关系为：

| 关系 | 键数 |
| --- | ---: |
| CSV 与 JSON 共有 | 22,627 |
| CSV 有、JSON 无 | 239 |
| JSON 有、CSV 无 | 1,815 |
| 共有键中，去除 `-` 后仍与 CSV 序列不同 | 185 |

JSON residue 中还观察到 14 个空格、5 个小写 `l` 和 1 个小写 `q`。因此 JSON 是独立的上游交付对象，不能假定它与 CSV 当前版本逐键同步，也不能不经核对便用编号 JSON 覆盖 CSV 序列。

### IMGT 编号结构归档

`CoV-AbDab_PDBStructures_080224.tar.gz` 为 290.38 MiB（304,487,848 bytes），SHA-256 为 `d451576efaf813c783d7f2aac77f011b2d4c504e2f73852c3284c46a70217a59`。安全扫描得到一个 `Structures/` 目录和 988 个 `<pdb_id>_imgt.pdb` 文件；没有重复路径、绝对路径、目录穿越或链接成员。解压内容合计 1.22 GiB（1,308,012,307 bytes）。

这些是上游提供的 IMGT-numbered legacy PDB 文件，已经过编号处理。项目另从 RCSB 保存的 FASTA 和完整 mmCIF 位于 `pdb/`，两者来源和用途不同。

### 三个交付文件之间的关系

CSV 共出现 1,062 个可辨识 PDB 候选：1,054 个来自明确的 RCSB URL，另有 8 个只出现在 `Expected (...)` 文本中。结构归档的 988 个 ID 与这些候选有 959 个交集；CSV 有 103 个候选不在归档内，归档另有 29 个 ID 没有出现在 CSV 候选中。数量差异表明结构包不是 CSV `Structures` 列的逐项副本。

CSV 中还有两类明确错位：`US10822379B1-#8` 的 `7MJH`、`7MJI` URL 位于 `CDRL3`；S304 的 `7XCP` URL 只位于 `Sources`。PDB 审计纳入这些有直接行级证据的链接，但 raw CSV 保持原样。

### 字段说明

除 `Ab or Nb` 外，多数字段是开放文本或由多个 token 组成的汇总字段，不存在发布方给出的封闭枚举。下表覆盖 CSV 的全部 23 个原始字段。

| 字段 | 原始表示与含义 |
| --- | --- |
| `Name` | 发布名称或专利/研究中的条目标识；字符串。当前有 12,916 个不同值，但两个名称各出现两次，不能视为严格唯一键。 |
| `Ab or Nb` | 条目类型；当前版本只观察到 `Ab` 和 `Nb`，见下表。 |
| `Binds to` | 已报告结合的冠状病毒、变体或相关病毒；分号分隔开放文本，12,918 行均非空，当前观察到 258 种 token。`(weak)` 属于原值。 |
| `Doesn't Bind to` | 已报告不结合的对象；分号分隔开放文本，3,201 行非空。空白不代表经过统一阴性实验。 |
| `Neutralising Vs` | 已报告能够中和的对象；分号分隔开放文本，6,373 行非空。没有统一效价单位或阈值。 |
| `Not Neutralising Vs` | 已报告不能中和的对象；分号分隔开放文本，5,482 行非空。空白不等于阴性。 |
| `Protein + Epitope` | 靶蛋白和表位区域的人工/文献注释，如 `S; RBD`；当前观察到 43 种写法和 4 个空白，不是封闭本体。 |
| `Origin` | 生物学或工程来源的开放文本，如患者 B cells、免疫动物、phage display 或工程来源；当前 189 种写法和 5 个空白。 |
| `VHorVHH` | 抗体重链可变区或纳米抗体 VHH 氨基酸序列；字符串，`ND` 表示未披露。没有长度单位。 |
| `VL` | 轻链可变区氨基酸序列；`ND` 表示未披露，纳米抗体通常为空。 |
| `Heavy V Gene`、`Heavy J Gene` | ANARCI 或来源整理的重链 V/J germline assignment，通常同时写物种；`ND` 表示未确定。 |
| `Light V Gene`、`Light J Gene` | 轻链 V/J germline assignment；纳米抗体通常为空，`ND` 表示未确定。 |
| `CDRH3` | 重链或 VHH 的 CDR3 氨基酸字符串；少量为 `ND`，部分值有尾随空格。 |
| `CDRL3` | 轻链 CDR3 氨基酸字符串；纳米抗体通常为空，少量为 `ND`。一行被上游结构 URL 错占。 |
| `Structures` | 与条目关联的 RCSB URL 或状态文本；多个 URL 用分号连接。常见状态为 `ND`、空白、`Expected`；另有 `Expected (<PDB>)`、`ND, Despite structure in paper` 和 `See S309` 等自由文本。 |
| `ABB Homology Model (if no structure)` | 预留的 ABodyBuilder 模型字段；当前 12,918 行全部为空。 |
| `Sources` | 原始论文、预印本、专利或 PDB 来源的引用字符串及 URL；当前 689 种组合，全部非空。 |
| `Date Added` | 条目加入日期的字符串，通常形如 `Feb 8, 2024`；7 行日期晚于本快照日期，使用前需核查。 |
| `Last Updated` | 条目最后更新日期的字符串；5 行日期晚于本快照日期，另有 1 行写成更新说明而非日期。 |
| `Update Description` | 维护历史的自由文本；10,219 行为空。 |
| `Notes/Following Up?` | 完整性、争议、证据边界或待跟进事项的自由文本；不应把其中的 `Complete` 当作实验标签。 |

**`Ab or Nb`（`CoV-AbDab_080224.csv`；取值范围依据：当前 source version 扫描）**

| 原始取值 | 当前记录数 | 含义 |
| --- | ---: | --- |
| `Ab` | 12,117 | 常规抗体条目，可含重链与轻链信息。 |
| `Nb` | 801 | 纳米抗体或单域抗体条目；本版本的 `VL` 均为空。 |

`ND` 在序列、germline 或结构字段中表示上游没有披露或没有给出对应信息；空字符串与 `ND` 是不同的原始编码，raw 层没有合并。

### 数据示例

下面是 CSV 的真实字段摘录：

```text
Name=MR17_K99Y
Ab or Nb=Nb
Binds to=SARS-CoV2_WT
Neutralising Vs=
Protein + Epitope=S; RBD
VHorVHH=QVQLVESGGGLVQAGGSLRLSCAASGFPVEVWRMEWYRQAPGKEREGVAAIESYGHGTRYADSVKGRFTISRDNAKNTVYLQMNSLKPEDTAVYYCNVYDDGQLAYHYDYWGQGTQVTVSS
VL=
CDRH3=NVYDDGQLAYHYDY
Structures=https://www.rcsb.org/structure/7CAN
```

```text
Name=C017
Ab or Nb=Ab
Binds to=SARS-CoV2_WT
Doesn't Bind to=SARS-CoV1
Neutralising Vs=SARS-CoV2_WT
Not Neutralising Vs=SARS-CoV1
Protein + Epitope=S; RBD
CDRH3=AKAGVRGIAAAGPDLNFDH
CDRL3=QQRIT
Structures=ND
ABB Homology Model (if no structure)=
```

两段各代表一条数据库维护记录。第一条有明确 PDB URL；第二条在网页上仍有 model viewer，但当前 CSV 模型字段为空且模型下载失效。它们都不是同一标准条件下的定量亲和力测量。

## PDB 数据库

本项目先扫描 CSV 的明确 RCSB URL 和 `Structures` 中带具体 ID 的 `Expected (...)` 文本，共得到 1,062 个候选。绝大多数链接位于 `Structures`，表示该行抗体或纳米抗体涉及的结构；两处上游错位链接按“数据结构”所述纳入。这个关系是数据库行到 PDB entry 的行级引用，不进一步指定抗体重链、轻链、抗原的某个 author-chain 副本。

2026-09-24 查询 RCSB holdings 后，5 个候选没有当前可下载 entry：`7B11` 为 unreleased，`7KGL`、`7N01`、`7NY5`、`7SIX` 为 removed。其余 1,057 个有效 PDB ID 均取得：

- `pdb/sequences/rcsb_pdb_<PDB_ID>.fasta`：RCSB entry FASTA，共 1,057 个文件，1.39 MiB（1,455,092 bytes）。
- `pdb/structures/<PDB_ID>.cif`：RCSB 完整原始 mmCIF，共 1,057 个文件，1.96 GiB（2,099,733,627 bytes）。

两类合计 2,114 个文件、1.96 GiB（2,101,188,719 bytes），按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接得到的 inventory SHA-256 为 `ff6fd58c9ff646b948c3c7554c004648b36510de74c392703b25831065b10d40`。验收逐条核对 PDB ID、mmCIF `atom_site`、FASTA entity ID，并确认 3,305 个 FASTA polymer entity sequence 与相应 mmCIF 的 canonical entity sequence 完全一致。

这些 RCSB 文件是 2026-09-24 取得的当前 entry 快照，用于补全 canonical 序列和完整坐标；它们不是 12,918 条记录逐行各自独立的结构，也不替代上游结构包中的 IMGT 编号文件。5 个非当前可用候选和后续状态见文末动态清单。

## 采集过程记录

- 2026-09-19：批次工作流建立 `SRC_R61_COV_ABDAB/.staging/snapshot-2024-02-08`，取得 CSV、ANARCI JSON、论文附件和部分结构归档；结构归档留下 136,314,880-byte partial，尚未发布。
- 2026-09-24：重新核对官网 HTML、三个正式下载链接、CC BY 4.0 声明、页面更新时间和 HTTP 对象 metadata。确认批量下载区只显示 CSV、ANARCI JSON 和 PDB structures。
- 2026-09-24：发现原配置把 `PMC7492096` 误当作 CoV-AbDab；已确认错误 XML 实为另一篇论文并从 staging 删除，改从 Oxford University Research Archive 取得正确的 2 页作者接受稿。20 页正式补充 PDF 经标题和内容复核后保留。
- 2026-09-24：定位大结构包续传错误。服务器把 `.tar.gz` 响应另标为 `Content-Encoding: gzip`，旧脚本自动解码后生成 TAR 字节，却用解码后偏移续传压缩响应。验证两种字节流后删除无效 partial，改为保存原始 HTTP entity、核对 `Content-Range` 总量并重新续传；最终文件大小、SHA-256 和安全 TAR 扫描通过。
- 2026-09-24：核对 CSV 全部字段、12,918 行、重复名称、序列覆盖、日期异常和错位结构 URL；核对 JSON 24,442 个键、元素形状及与 CSV 的键和序列差异；核对结构归档 988 个 PDB 文件及其与 CSV 候选的集合差异。
- 2026-09-24：从 CSV 发现 1,062 个 PDB 候选。首轮 RCSB 下载对 5 个 ID 返回 404；随后用 RCSB holdings 区分 1 个 unreleased 和 4 个 removed 条目。对其余 1,057 个条目补齐 1,057 对 FASTA/mmCIF，并逐对验证 canonical polymer entities 和坐标内容。
- 2026-09-24：官网 HTML 中被注释的 2023-03-03 homology-model bulk URL 和 C017 单条模型下载均复核为 HTTP 404；记录为非阻塞的公开缺口，不用推断模型补齐。
- 2026-09-24：独立审计确认配置字节数与 SHA-256、文件集合、PDF 页数和身份、CSV/JSON schema、TAR 安全性、PDB 配对、无 symlink 和无残留 partial 均符合发布条件；README 与本地调研记录同步完成。
- 2026-09-24：发布脚本在移动前后各完成一次全量审计，并将暂存目录原子发布为 `SRC_R61_COV_ABDAB/snapshot-2024-02-08`；前后均为三项 payload 和 1,057 对 RCSB FASTA/mmCIF。
- 2026-09-24：source README 已同步到飞书[《SRC_R61_COV_ABDAB 数据说明》](https://bzwd25rbx0.feishu.cn/docx/RhtNdueK8oewqfxdAKWcVDMfnlc)；同步器回读确认正文顺序、代码、链接、SHA-256、无手工目录和父索引均一致。

## 参考文献

- [CoV-AbDab 官方数据库及下载页](https://opig.stats.ox.ac.uk/webapps/covabdab/)
- [CoV-AbDab 数据许可：CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- [Raybould et al. (2021), CoV-AbDab: the coronavirus antibody database](https://doi.org/10.1093/bioinformatics/btaa739)
- [Oxford University Research Archive 记录](https://ora.ox.ac.uk/objects/uuid:847edf55-57c1-4df0-a1dd-345094103e34)
- [Dunbar and Deane (2016), ANARCI](https://doi.org/10.1093/bioinformatics/btv552)
- [Dunbar et al. (2014), SAbDab](https://doi.org/10.1093/nar/gkt1043)
- [Leem et al. (2016), ABodyBuilder](https://doi.org/10.1080/19420862.2016.1205773)
- [RCSB PDB 文件下载服务](https://www.rcsb.org/docs/programmatic-access/file-download-services)
- [RCSB PDB 使用政策](https://www.rcsb.org/pages/usage-policy)

## 其他

### 数据范围和限制

当前 raw payload 是数据库维护方整理后的公开导出，不是各引用论文或专利的底层实验数据。它不含统一实验条件、原始传感曲线、plate/FACS/NGS 读数、replicate 或标准化定量亲和力，无法仅凭主表重现每个结合和中和结论。不同来源的测试对象、阈值、抗体格式和 assay 可能不同；任何监督学习任务都应先回到 `Sources` 追溯原始证据并定义一致标签。

条目之间也并非统计独立：同一抗体可以整合多篇研究、多个变体和多个 PDB，同名还可能有多行；相近克隆、成熟谱系或同一专利系列可能进一步相关。随机按行拆分会造成明显的序列、名称、来源和结构泄漏。

### 完整性与验收

本次公开 payload 为 3 个文件、353.60 MiB（370,774,781 bytes），inventory SHA-256 为 `04d1a550c1953edf93f38c1728032e187b3a2ea4d93417f493334e00356546f3`。论文归档含 2 页作者接受稿和 20 页补充材料。外部 PDB 补充含 2,114 个文件、1.96 GiB（2,101,188,719 bytes），inventory SHA-256 为 `ff6fd58c9ff646b948c3c7554c004648b36510de74c392703b25831065b10d40`。

验收覆盖：精确文件集合、字节数与 SHA-256、CSV 宽度和全表 schema、JSON 结构、PDF 页数与文本身份、TAR member 安全和成员集合、PDB FASTA/mmCIF 一一配对、entry ID、atom_site 及 canonical entity sequence。当前 source version 没有 symlink、旁路 manifest、metadata 响应或 `.partial` 文件。

### 许可和再分发边界

[CoV-AbDab 页面](https://opig.stats.ox.ac.uk/webapps/covabdab/)明确说明数据库中的数据采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，允许在署名、附许可链接并标明改动的条件下复制、再分发和改编，也允许商业使用。这里的许可覆盖 CoV-AbDab 数据交付，不自动改写数据库所引用论文、专利或第三方内容本身的权利。

项目从 RCSB 补取的 FASTA 和 mmCIF 属于 wwPDB Core Archive data；[RCSB usage policy](https://www.rcsb.org/pages/usage-policy)说明这些数据适用 CC0 1.0，并鼓励归属原始结构作者。论文正式文本采用 OUP 的出版条款，ORA 作者接受稿采用 ORA Terms of Use 和作者版权，不能用数据库 CC BY 4.0 替代。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 全库抗体/纳米抗体条目和元数据 | CSV 12,918 行、12,916 个不同名称 | 已包含当前导出；不是底层实验原始数据 |
| 完整变量区序列、CDR3 和 germline（在可得时） | CSV 序列与 gene 字段；缺失用 `ND` 或空白编码 | 部分包含，覆盖取决于条目 |
| ANARCI IMGT 编号 | JSON 24,442 个键 | 已包含，但与 CSV 存在键和序列差异 |
| 已知抗体相关 PDB 结构 | 上游 TAR 988 个 IMGT-numbered PDB；CSV 1,062 个候选 | 部分对应；集合不一致 |
| 当前有效 PDB 的 canonical FASTA 与完整坐标 | 1,057 对 RCSB FASTA/mmCIF | 有效锚点全部补齐；5 个候选非当前可用 |
| ABodyBuilder 同源模型 | CSV 模型列全空；旧 bulk URL与单条示例下载均为 404 | 当前未取得 |
| 主论文与补充说明 | ORA 作者接受稿、正式版在线入口和 20 页补充 PDF | 可复核；排版正式 PDF 未本地归档 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-24；不阻塞当前公开包发布）：论文和旧网页说明曾提供 ABodyBuilder homology models，但当前 CSV 的模型列全部为空，HTML 中被注释的 `CoV-AbDab_HomologyModels_030323.tar.gz` 与 C017 viewer 指向的单条 PDB 均返回 404。当前只发布仍可验证的三项批量交付，不用重新建模结果替代上游文件；下一步等待维护方恢复模型下载、提供存档或明确模型撤下状态，取得后需核验模型数量、条目映射、格式和许可才能关闭。
- `Q02`（最近更新：2026-09-24；不阻塞 1,057 个有效锚点验收）：CSV 候选 `7B11` 在 RCSB 为 unreleased，`7KGL`、`7N01`、`7NY5`、`7SIX` 为 removed，因而没有当前 FASTA/mmCIF 对。当前已保留上游引用并排除虚假空文件；下一步定期检查 `7B11` 是否发布，并为 removed 条目查找 RCSB replacement mapping 或来源论文更正，获得可验证替代 ID 后更新映射。
- `Q03`（最近更新：2026-09-24；不阻塞数据解释）：OUP 排版正式 PDF 的自动请求返回 403，本地保存的是 ORA 明确标识的作者接受稿；正式正文已通过 DOI/PMC 在线核对，正式补充 PDF 已归档。若后续需要离线逐页复核出版版式，可由有正常浏览器访问条件的执行者下载并核对 DOI、页数与哈希后归档。
- `Q04`（最近更新：2026-09-24；影响跨文件连接和自动清洗）：CSV 与 ANARCI JSON 有 239 个 CSV-only keys、1,815 个 JSON-only keys 和 185 个共享键序列差异；CSV 还含重复名称、未来日期、非日期 `Last Updated` 和错位结构 URL。当前 raw 层保持原值，README 给出可用边界，任何 join 或清洗必须在 processed 层显式记录；下一步向维护方确认三个交付文件是否来自同一内部导出批次，并在新快照出现时重新比较，只有上游更正或可复现映射规则明确后关闭。
