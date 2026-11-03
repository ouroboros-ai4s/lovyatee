---
tags:
  - context
---

# SRC_R15_SKEMPI2 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [原始交付与记录](#原始交付与记录)
  - [字段说明](#字段说明)
  - [数据示例](#数据示例)
- [PDB 数据库](#pdb-数据库)
- [使用方式](#使用方式)
- [采集过程记录](#采集过程记录)
- [参考文献](#参考文献)
- [其他](#其他)
  - [完整性与验收](#完整性与验收)
  - [许可和再分发边界](#许可和再分发边界)
  - [公开范围对照](#公开范围对照)
- [待解决问题与处理进展](#待解决问题与处理进展)

## 数据集身份

- `source_id`：`SRC_R15_SKEMPI2`
- `source_version`：`2.0`
- 原作者或发布机构：Jankauskaitė J、Jiménez-García B、Dapkūnas J、Fernández-Recio J、Moal IH / BSC 与共同机构

### 来源方背景

[正式论文的作者单位](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6361233/fullTextXML)包括维尔纽斯大学生物技术研究所、Barcelona Supercomputing Center、乌得勒支大学、CSIC 分子生物学研究所及 EMBL-EBI。该跨机构团队维护的是文献和结构基础上的突变结合数据库；表中测量仍来自各原研究，而非同一实验室统一重测。

## 实验设计和数据口径

SKEMPI 2.0 汇编结构已知的蛋白—蛋白相互作用突变，包含一般 PPI 和抗体相关子集。实际 CSV 有 7,085 行、345 个 PDB accession，带 KD、动力学、焓和熵等异质测量。原论文记录 440 个突变使结合低于检测范围；必须保留不等式、未检出和检测边界，不能把 parsed 列中的空值当成零。重复突变、重复实验、共享亲本和同源体系须分开追溯；不能只按 PDB ID 随机切分。官方 cleaned 结构可能删链并重新编号，Mutation(s)_PDB 与 Mutation(s)_cleaned 不是同一编号体系。

作者逐篇人工核对文献、结构物种、构建体、辅因子和实验条件后汇编数据；部分 KD/动力学/热力学值由论文所给公式换算。CSV 的 wild-type 列指 PDB 中实际结构状态，反向突变回生物学野生型时不能按列名假定对象身份。实际 7,085 行、348 个带伙伴链后缀的复合物键、345 个唯一 accession，均不是 7,085 个独立结构。当前 CSV 的 mutant KD 有 159 个不等式表示、278 个 n.b/n.b.；wt KD 有 41 个不等式表示、2 个 n.b/n.b.。mutant parsed 列有 285 个空值，保留原始字符串和空值，不填零。论文报告的 440 个结合消失突变是论文口径，不替代本次表的字段统计。Temperature 单位 K；KD 单位 M，小值表示更强结合，非结合与检测边界须另行处理。

## 论文原文

- 标题：SKEMPI 2.0: an updated benchmark of changes in protein–protein binding energy, kinetics and thermodynamics upon mutation
- 作者：Justina Jankauskaitė；Brian Jiménez-García；Justas Dapkūnas；Juan Fernández-Recio；Iain H Moal
- 载体与版本：Bioinformatics
- 发布日期：2018-07-18
- DOI：`10.1093/bioinformatics/bty635`
- PMID / PMCID：30020414 / PMC6361233
- 本地文件：`articles/SKEMPI2_2018-07-18_Bioinformatics-published.xml`
- 文件大小：134.99 KiB（138,231 bytes）
- SHA-256：217ee714475783f13b8c0228af4d507d94aca89867075559f30eb5b84156ed6c
- 文本许可：正式论文 XML 标明 CC BY 4.0，需保留原作者署名
- 补充材料：`articles/SKEMPI2_2018-07-18_supplement-bty635_supplementary_table.xls`，2.13 MiB（2,233,856 bytes），SHA-256 `8a56365255e93b559389827fdb6c5cf762e7190764647b7febdceed5e09bf054`

主文引用的 bty635_supplementary_table.xls 已从官方 Europe PMC 附件包取得并完整解析：Sheet1 有 7,085 个非空数据行、50 个物理列。该 XLS 的表头被拆为多个单元格，和官网当前 29 列 CSV 不同，不能用 CSV 表头直接套读该补充表。以原样归档保留差异，不在 raw 中修复。

## 仓库内容

来源身份：

- `kind`：`http-release`
- `official_page`：`https://life.bsc.es/pid/skempi2/database/index`

版本日期来自数据源 commit 或官方更新时间；正式版本名保留官方名称。以下树为已验收的上游 payload，不列项目 README、论文及 PDB 外部补充。

```text
2.0/
└── SKEMPI2/
    ├── skempi_v2.csv
    ├── SKEMPI2_PDBs.tgz
```

## 数据结构

### 原始交付与记录

| 原始文件 / sheet | 非空记录数 | 字段数 | 精确重复行 |
| --- | --- | --- | --- |
| `SKEMPI2/skempi_v2.csv` | 7085 | 29 | 11 |

只统计实际已解析的文件，未把来源介绍规模当作本次落盘统计。

cleaned 归档的 1,381 个普通成员包含 345 个真实 PDB 坐标文件、345 个 residue mapping 文件和 691 个上游 AppleDouble 成员。带 ._ 前缀的资源分支不是额外结构；上游压缩包原样保留，不把它们计作样本。mapping 连接原编号与从一开始的 cleaned 编号，不能把两种 Mutation 字段混用。

### 字段说明

`#Pdb` 为 PDB 与伙伴链；Mutation(s)_PDB / Mutation(s)_cleaned 分别为原始和 cleaned 位点。Affinity_mut (M)、Affinity_wt (M) 单位 M，KD 越小结合越强；对应 _parsed 字段是来源预处理副本，不能丢掉原始边界文本。`kon_*` 单位 M^(-1)s^(-1)，`koff_*` 单位 s^(-1)，`dH_*` 单位 kcal mol^(-1)，`dS_*` 单位 cal mol^(-1) K^(-1)，Temperature、Method、Reference、Notes 保留实验条件及追溯。空字符串和不等式按原样保存，亲和力单位不移用于其他字段。

Hold_out_type 在当前表包含空值、Pr/PI、AB/AG、AB/AG,Pr/PI 和 TCR/pMHC；这些为上游同源分组，并非绝对功能类别。应结合 Hold_out_proteins 和共享亲本/伙伴设计 split，避免相关体系跨训练和测试。

实际表头（保留原始字段名）：

- `SKEMPI2/skempi_v2.csv`：`#Pdb`、`Mutation(s)_PDB`、`Mutation(s)_cleaned`、`iMutation_Location(s)`、`Hold_out_type`、`Hold_out_proteins`、`Affinity_mut (M)`、`Affinity_mut_parsed`、`Affinity_wt (M)`、`Affinity_wt_parsed`、`Reference`、`Protein 1`、`Protein 2`、`Temperature`、`kon_mut (M^(-1)s^(-1))`、`kon_mut_parsed`、`kon_wt (M^(-1)s^(-1))`、`kon_wt_parsed`、`koff_mut (s^(-1))`、`koff_mut_parsed`、`koff_wt (s^(-1))`、`koff_wt_parsed`、`dH_mut (kcal mol^(-1))`、`dH_wt (kcal mol^(-1))`、`dS_mut (cal mol^(-1) K^(-1))`、`dS_wt (cal mol^(-1) K^(-1))`、`Notes`、`Method`、`SKEMPI version`

字段原始表示与缺失统计（只统计审计解析结果，不在 raw 中填零）：

- `SKEMPI2/skempi_v2.csv`：缺失/特殊表示计数 `{"kon_mut (M^(-1)s^(-1))": 5241, "kon_mut_parsed": 5241, "kon_wt (M^(-1)s^(-1))": 5232, "kon_wt_parsed": 5232, "koff_mut (s^(-1))": 5241, "koff_mut_parsed": 5241, "koff_wt (s^(-1))": 5225, "koff_wt_parsed": 5225, "dH_mut (kcal mol^(-1))": 6642, "dH_wt (kcal mol^(-1))": 6642, "dS_mut (cal mol^(-1) K^(-1))": 6642, "dS_wt (cal mol^(-1) K^(-1))": 6642, "Notes": 4023, "Hold_out_type": 3774, "Affinity_mut_parsed": 285, "Affinity_wt_parsed": 2, "Temperature": 4}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

### 数据示例

来自 `SKEMPI2/skempi_v2.csv` 的第一条真实记录；这里只摘录字段，不改写原始文件。

| 字段 | 原样值 |
| --- | --- |
| `#Pdb` | `1CSE_E_I` |
| `Mutation(s)_PDB` | `LI45G` |
| `Mutation(s)_cleaned` | `LI38G` |
| `iMutation_Location(s)` | `COR` |
| `Hold_out_type` | `Pr/PI` |
| `Hold_out_proteins` | `Pr/PI` |
| `Affinity_mut (M)` | `5.26E-11` |

每行按该来源的测量、配对或结构实例口径解释，不把结构表示或 replicate 当作新实验。完整字段保留在 payload 中。

## PDB 数据库

CSV #Pdb entry prefix with author-chain suffixes. Mutation(s)_PDB uses original PDB residue numbering; Mutation(s)_cleaned uses upstream cleaned-coordinate numbering from one. Full RCSB entry files are shared structural references, not experimentally measured mutant structures.

当前接受锚点清单为 345 个；最后一次审计有 0 个未完成两层配对。每个锚点取原样 per-entry FASTA 和完整 mmCIF，不嫁接 CDR、不生成逐变体重建序列。FASTA 的原始 header 保留 polymer entity 与 author/label chain；不猜测伙伴角色。只有全部接受锚点同时通过 FASTA 和坐标解析，且 FASTA entity ID 集合和完整序列与 mmCIF 的 canonical polymer 一致，才算完成。

PDB 文件审计摘要：690 个文件，258.99 MiB（271,572,065 bytes）；inventory SHA-256：`8a2ebba914c6b0a50f0499f583f86cefe558ab9fb5ffa8fe6cf9dd73820720ed`。摘要按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接计算。缓存最初包含选择链/重写 header 的 FASTA，已清理本轮这类 staging 副本；现在只接受 RCSB native per-entry header。

## 使用方式

由调用者先赋值 `dataset_root`（Path），再读取；不在这里清洗或转换标签。

```python
import pandas as pd
table = pd.read_csv(dataset_root / "SKEMPI2/skempi_v2.csv", sep=";")
```

## 采集过程记录

2026-09-18：读取项目规范和执行清单，解析一手 API/tree/Drive 对象 metadata，固定本轮版本与文件身份。下载到共享 source 下 `.staging/<version>.partial`；HTTP 大文件使用精确 byte range 和全文件上游 checksum，Drive 保留对象 ID、MIME 与字节数，失败部分可续传。2026-09-18 按用户要求调整本轮 HTTP 为直连优先、连接失败回退环境代理，15 分钟后重试直连；各线程复用连接且保留 TLS/CA 校验。重启任务保留所有文件断点。

独立 audit 重新计算 hash、完整解析已取得表格并检查 PDB 两层文件；归档只有完成逐成员/CRC 与路径安全检查后才通过。PMC 访问被拒绝、非 OA XML 不可得和间歇代理连接失败均保留缺口，未关闭 TLS 验证。PDB 缓存原始性检查发现错误后清理本轮衍生 header 文件并重做。

README 草稿每次写入后立即同步到 staging 同名文件，随后运行 skill 固定 Markdownlint 配置。发布脚本仅在逐文件、论文/PDB、README 同步与固定格式检查通过后原子发布；发布状态与 docs/status.md 同步。

2026-09-18：主文从 `SKEMPI2_PMC6361233.xml` 改名为 `SKEMPI2_2018-07-18_Bioinformatics-published.xml`，日期取该论文版本发布日期，改名前后大小和 SHA-256 一致。

2026-09-18：按 DOI 一致的主文 XML 所列文件名，从官方 Europe PMC supplementaryFiles 包取得全部被引用的附件，检查完整 ZIP CRC、路径安全及成员唯一性；原文件名及每个文件大小和 SHA-256 已记录。

2026-10-09：按新版 README 合同核对来源方背景、公开包与研究底层数据的范围，并补齐动态待办章节；CSV、cleaned 归档、论文附件及 345 对 PDB 文件未改动。

## 参考文献

- <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6361233/fullTextXML>
- <https://doi.org/10.1093/bioinformatics/bty635>
- <https://life.bsc.es/pid/skempi2/database/index>
- <https://www.rcsb.org/>
- <https://life.bsc.es/pid/skempi2/info/terms>

## 其他

### 完整性与验收

上游声明 2 个文件；最近审计通过 2 个，待取得/核验 0 个。

公开包独立验收、论文/补充材料对照及 PDB 配对审计通过；不宣称全部底层实验数据取得。没有独立 manifest/API 响应/审计 JSON 发布在 source version 中；临时产物只保存在共享 cache。

| 上游 payload | 大小 | SHA-256 |
| --- | --- | --- |
| `SKEMPI2/skempi_v2.csv` | 1.53 MiB（1,602,208 bytes） | `76f8e60d09eaa4f05fb265063886859a86895c0b2fb225e31fe82928a883972d` |
| `SKEMPI2/SKEMPI2_PDBs.tgz` | 29.07 MiB（30,482,090 bytes） | `82418131a3864aa8484ea6ec300e58f9bc0349e21530f83f7ce336b41589a95a` |

### 许可和再分发边界

官网 Terms of USE 明确采用 CC BY 4.0；保留数据库、原实验论文和 PDB 引用。

### 公开范围对照

| 目标组成 | 当前证据 | 状态 |
| --- | --- | --- |
| 固定上游 payload | tracked config + 独立文件/格式审计 | 目标公开文件验收通过 |
| 论文原文 | 一手 DOI 和取得文件 hash；不可得项明确记录 | 主文与全部被引用附件已归档并解析 |
| PDB 原始序列与全坐标 | 接受锚点两层配对审计 | 两层已齐；非逐变体结构 |
| 完整研究底层数据 | 公开汇编或处理包不等于全部底层实验 | 未宣称获得 |

## 待解决问题与处理进展

截至 `2026-10-09`，本次公开包、论文附件、标签边界与 345 对 PDB 参考的核验范围内暂无待解决问题。各原研究的实验曲线和重复测量不属于本次 SKEMPI 2.0 公开包；这不表示完整研究底层数据已取得。
