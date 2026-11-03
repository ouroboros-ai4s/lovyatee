---
- tags:
  - context
---

# SRC_R17_PDBBIND_PP 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
  - [从 PDB 条目到 PPI general set](#从-pdb-条目到-ppi-general-set)
  - [亲和力数值的形成与解释](#亲和力数值的形成与解释)
  - [当前包的规模与产物关系](#当前包的规模与产物关系)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [PPI 索引与结构](#ppi-索引与结构)
  - [其他索引和说明文件](#其他索引和说明文件)
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

- `source_id`：`SRC_R17_PDBBIND_PP`
- `source_version`：`2020`
- 原作者或发布机构：PDBbind 数据库团队（Renxiao Wang 课题组）

### 来源方背景

包内 `PDBbind-101.txt` 记载，PDBbind 原型由密歇根大学 Shaomeng Wang 课题组开发并于 2004 年首次发表，2006 年起由中国科学院上海有机化学研究所 Renxiao Wang 课题组维护，v2020 发布时已由其复旦大学团队维护。数据库把 PDB 中的三维结构与文献报告的实验结合数据连接起来，持续按 PDB 新增结构更新。现行 [PDBbind+ 官网](https://pdbbind-plus.org.cn/) 说明，该平台由复旦大学 Renxiao Wang 团队与上海陶术生物科技股份有限公司合作运营，于 2024 年 1 月上线；平台运营方和托管页面的变化没有改变本目录所保存数据的正式版本 `2020`。

## 实验设计和数据口径

### 从 PDB 条目到 PPI general set

PDBbind 是文献汇编数据库，本来源没有重新对 2,852 个复合物开展一套统一实验。其基本形成过程如下：

```text
截至 2020-01-01 已发布的 PDB 结构
  → 根据结构内容分类生物分子复合物
  → 检索相关 PDB 条目的原始文献并人工整理结合数据
  → PDBbind v2020 protein-protein general set
      ├─ 2,852 条 INDEX_general_PP.2020 记录
      └─ 2,852 件同 PDB ID 的原始 .ent.pdb 结构
```

包内 v2020 说明把有效 protein-protein complex 定义为至少两个不同蛋白分子，且每个分子至少有 20 个残基；任一侧短于 20 个残基的 peptide complex 被归入 protein-ligand 类别。2015 年方法论文描述的既有结构分类流程还会区分有生物学意义的界面与晶体堆积，但 v2020 包没有重新逐项公布分类程序的全部参数。因此，这里的 `protein-protein` 是 PDBbind 的数据库分类，不宜仅凭名称外推为所有可能的蛋白相互作用定义。

### 亲和力数值的形成与解释

2015 年方法论文说明，团队以相关 PDB 条目给出的 primary reference 为主要入口，用关键词程序辅助定位结合数据，再由两人独立阅读全文；只有结果一致时才正式记录。数据库收集三类常见端点：平衡解离常数 `Kd`、抑制常数 `Ki` 和产生 50% 抑制的浓度 `IC50`。同一复合物有多种端点时，论文给出的展示优先级是 `Kd > Ki > IC50`；有多组条件时，优先展示接近室温和中性 pH 的结果。v2020 包内说明进一步确认，该版本全部四类复合物的 23,496 条结合数据来自约 40,500 篇原始文献的人工整理。

当前 PPI 索引只保留每条记录选中的一个数值、端点、比较符和单位，并附一段自由文本说明；原始实验曲线、完整 assay 条件、逐条双人核对记录和被引用论文 PDF 均未随包提供。`Kd` 越小通常表示平衡结合越紧，`Ki` 越小通常表示抑制更强；`IC50` 还随底物浓度和 assay 设计变化。三者物理含义不同，跨端点排序前需要建立明确的任务口径，不能只换算单位后直接视作同一种亲和力。

比较符也影响标签性质：`=` 是按索引记录的确定值，`~` 是近似值，`<` 和 `>` 是上下界。后两类属于删失观测；若把它们当成恰好等于边界的点值，会引入系统误差。

### 当前包的规模与产物关系

`INDEX_general_PP.2020` 有 2,852 行和 2,852 个唯一 PDB ID，结构发布日期为 1981–2019。完整扫描得到以下分布：

| 维度 | 当前 v2020 PPI 观察值 |
| --- | --- |
| 端点 | `Kd` 2,618；`Ki` 171；`IC50` 63 |
| 比较符 | `=` 2,751；`~` 65；`<` 20；`>` 16 |
| 单位 | `nM` 1,567；`uM` 1,049；`pM` 200；`mM` 22；`fM` 14 |
| 结构分辨率表示 | 数值 2,652；`NMR` 200 |

每行索引与包内一件 `<pdb_id>.ent.pdb` 通过 PDB ID 一一对应。本包同时捆绑 v2020 其他类别的索引文件，但没有把 protein-ligand、protein-nucleic acid 或 nucleic acid-ligand 的结构包一并交付；这些索引只作为同版上下文，不计入本来源的 2,852 条 PPI 主记录。

## 论文原文

- 标题：PDB-wide collection of binding data: current status of the PDBbind database
- 作者：Zhihai Liu、Yan Li、Li Han、Jie Li、Jie Liu、Zhixiong Zhao、Wei Nie、Yuchen Liu、Renxiao Wang
- 发表来源：*Bioinformatics* 31(3): 405–412
- 归档文本版本：正式发表版完整 HTML
- 发布日期：2014-10-09
- DOI：[10.1093/bioinformatics/btu626](https://doi.org/10.1093/bioinformatics/btu626)
- PMID / PMCID：[PMID 25301850](https://pubmed.ncbi.nlm.nih.gov/25301850/) / 无 PMCID
- 正文在线入口：[Oxford Academic](https://academic.oup.com/bioinformatics/article/31/3/405/2365195)
- 本地归档：未归档；出版方页面可完整在线核对，但未显示明确的正文复用许可
- 文本许可：出版方将页面标为 `Free`，未特别说明覆盖正文的开放复用许可
- 补充材料：`articles/PDBbind_2014-10-09_Bioinformatics-published-supplement.zip`，62.14 KiB（63,636 bytes），SHA-256 `324807034a31d92aebfef081fe58cd92680fc693aeb01cf1ae4956384cf83103`；包内一件 `SupportingInformation.doc`，对应论文的 Supplementary Table S1 数据库比较，不是 v2020 PPI 数据表
- 引用数（查询快照）：701（[OpenAlex W2114162221](https://openalex.org/W2114162221)，查询于 2026-09-24）

这篇论文系统说明了 PDBbind 的结构分类、文献检索和人工核对方法，正文针对的最新数据是 v2013。当前 v2020 的版本边界、类别数量和文件说明以压缩包内 `PP/readme/PDBbind-101.txt` 及 `pdbbind_2020_intro.pdf` 为准；没有用旧论文的 v2013 数量替代 v2020 实际文件统计。

## 仓库内容

上游入口为 [PDBbind+ 下载页](https://www.pdbbind-plus.org.cn/download)，保存对象为原始 `PDBbind_v2020_PP.tar.gz`。`source_version=2020` 取自数据库正式版本名：包内说明称其以 2020-01-01 前正式发布的 PDB 内容为基础。PPI 索引标记“Latest update: July 2021”，总说明标记 2021 年 8 月更新；托管对象的 HTTP `Last-Modified` 为 2025-08-05。这些日期分别描述索引维护和对象托管状态，没有被改写为新的数据版本。

本次按用户要求选择原始 v2020 PPI 包；2025 年另行发布的免费 `v2020.R1` 未混入本目录，v2021 及后续付费版本也未获取。

```text
2020/
└── PDBbind_v2020/
    └── PDBbind_v2020_PP.tar.gz
```

原始归档保持压缩状态，大小 753.71 MiB（790,323,198 bytes）。包内有 `PP/` 根目录：2,852 件 PPI 原始 PDB-format 结构位于根下，11 个索引位于 `PP/index/`，版本说明 PDF 和文本位于 `PP/readme/`。

## 数据结构

### PPI 索引与结构

`PP/index/INDEX_general_PP.2020` 是本来源的主表。文件开头用注释给出版本、计数和字段顺序，随后每行以空白分隔 PDB ID、分辨率、发布年份和结合数据，并用 `//` 分隔 reference token 与自由文本说明。

`PP/<pdb_id>.ent.pdb` 是与主表逐 ID 对应的原始 PDB-format 坐标。完整遍历确认 2,852 件结构的 `HEADER` ID 都与文件名一致，且均含坐标记录。包内说明所称 protein-ligand “processed clean structures”不适用于 PPI；PPI 包保存的是原始结构表示，没有为每个相互作用伙伴另行拆分或清理。

### 其他索引和说明文件

| 文件组 | 行数或数量 | 作用 |
| --- | ---: | --- |
| `INDEX_general_PL.2020` | 19,443 | protein-ligand general set 索引，字段形态与 PPI 主表相近 |
| `INDEX_general_PN.2020` | 1,052 | protein-nucleic acid general set 索引 |
| `INDEX_general_NL.2020` | 149 | nucleic acid-ligand general set 索引 |
| `INDEX_refined_set.2020` | 5,316 | protein-ligand refined set 索引 |
| `INDEX_general_PL_data.2020`、`INDEX_refined_data.2020` | 19,443、5,316 | 增加 `-logKd/Ki` 的 protein-ligand 数值视图 |
| `INDEX_general_PL_name.2020`、`INDEX_refined_name.2020` | 19,443、5,316 | PDB ID、年份、UniProt ID 和 protein name 视图 |
| `INDEX_structure.2020` | 19,443 | protein-ligand processed structure 的分辨率、R-factor、R-free 和 delta-R 索引 |
| `2020_index.lst` | 157,974 | 无表头的六字段全库辅助列表；包内说明未定义后三个数值字段，因此不用于解释 PPI 标签 |
| `PDBbind-101.txt`、`pdbbind_2020_intro.pdf` | 1、1 | v2020 版本范围、目录和使用说明；PDF 为 2 页 |

这些附带索引提供同版数据库背景，但本来源的建模记录仍以 `INDEX_general_PP.2020` 的 2,852 行为边界。

### 字段说明

| 文件或记录 | 原始字段 | 原始表示与单位 | 含义和来源 |
| --- | --- | --- | --- |
| `INDEX_general_PP.2020` | `PDB code` | 四字符 PDB accession | 主键；连接同名 `.ent.pdb` 和外部 RCSB entry |
| `INDEX_general_PP.2020` | `resolution` | Å 数值或 `NMR` | PDB 结构分辨率；NMR 条目没有晶体学数值分辨率 |
| `INDEX_general_PP.2020` | `release year` | 四位整数 | 结构发布年份；当前观察范围 1981–2019 |
| `INDEX_general_PP.2020` | `binding data` | `<endpoint><operator><value><unit>` | 从原始文献整理并由 PDBbind 选中展示的一个结合端点 |
| `INDEX_general_PP.2020` | `reference` | `<pdb_code>.pdf` token | PDBbind 内部原始文献归档标识；对应 PDF 不在本包内。765 行的 token 与本行 PDB ID 不同，因此不能把它当作行主键 |
| `INDEX_general_PP.2020` | `ligand name` | `//` 后自由文本 | 可能包含伙伴名称、链长、实验值或整理备注；不是受控的 antibody/antigen 标签 |
| `*_data.2020` | `-logKd/Ki` | 十进制数 | protein-ligand 附带索引的负十进制对数视图；PPI 主表没有此字段 |
| `*_name.2020` | `Uniprot ID`、`protein name` | accession、自由文本 | protein-ligand 附带索引的蛋白注释 |
| `INDEX_structure.2020` | `R-factor`、`R-free`、`delta-R` | 十进制数；包内出现 `-1.000` 特殊值，但说明未定义其精确缺失语义 | protein-ligand processed structure 的晶体学质量索引；不属于 PPI 主表 |
| `PP/<pdb_id>.ent.pdb` | PDB flat-file records | 固定列文本记录 | 上游保存的完整 PDB-format 结构；字段语义遵循 PDB 文件格式 |

**`endpoint`（从 `binding data` 解析；取值范围依据：当前 v2020 PPI 全量扫描）**

| 原始取值 | 当前记录数 | 含义 |
| --- | ---: | --- |
| `Kd` | 2,618 | 平衡解离常数；同类可比条件下越小通常结合越紧 |
| `Ki` | 171 | 抑制常数；越小通常表示抑制更强，但依赖具体实验和模型 |
| `IC50` | 63 | 产生 50% 抑制的浓度；依赖 assay 条件，不能直接当作 `Kd` |

**`operator`（从 `binding data` 解析；取值范围依据：当前 v2020 PPI 全量扫描）**

| 原始取值 | 当前记录数 | 含义 |
| --- | ---: | --- |
| `=` | 2,751 | 索引记录的确定值 |
| `~` | 65 | 近似值 |
| `<` | 20 | 真值小于给定边界 |
| `>` | 16 | 真值大于给定边界 |

**`unit`（从 `binding data` 解析；取值范围依据：当前 v2020 PPI 全量扫描）**

| 原始取值 | 当前记录数 | 含义 |
| --- | ---: | --- |
| `fM` | 14 | femtomolar，`10^-15 M` |
| `pM` | 200 | picomolar，`10^-12 M` |
| `nM` | 1,567 | nanomolar，`10^-9 M` |
| `uM` | 1,049 | micromolar，`10^-6 M`；上游使用 ASCII `u` 表示微 |
| `mM` | 22 | millimolar，`10^-3 M` |

### 数据示例

以下两行逐字摘自 `INDEX_general_PP.2020`：

```text
1fc2  2.80  1981  Kd=22.5nM     // 1fc2.pdf (224-mer) Human Fc fragment, Kd=22.5+/-4.6nM, SpAb-1 and Fc gamma-1, pKd=7.65
3sgb  1.80  1983  Kd=17.9pM     // 3sgb.pdf (56-mer) TURKEY OVOMUCOID INHIBITOR (OMTKY3), 1.79 x 10-11M
```

每行代表一个由 PDB ID 锚定的复合物记录及一个被选中展示的文献结合端点。自由文本可能保留更细的实验注记，但它不是结构化 assay 表，也不能从两行格式推断所有记录具有相同实验条件。

## PDB 数据库

PPI 主表的 PDB code 是逐记录、直接的一对一外部结构锚点。除上游归档中的 2,852 件历史 PDB-format 文件外，本项目还按相同 2,852 个唯一 ID 保存 RCSB 原始完整 entry FASTA 与 full mmCIF：

- `pdb/sequences/rcsb_pdb_<PDB_ID>.fasta`：2,852 件完整 entry canonical polymer FASTA。
- `pdb/structures/<PDB_ID>.cif`：2,852 件完整 entry mmCIF。
- 合计 5,704 件，3.50 GiB（3,762,095,800 bytes）。按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接计算的 inventory SHA-256 为 `794e3e12e8549e79d738491fc91f77e9aa8608fb59c87141101a11e87605358f`。

2,849 个 ID 可由现行 RCSB native 文件覆盖。其余三个源 ID 已被撤回并有明确替代关系：`3OHM → 7SQ2`（2021-11-17）、`3PVM → 9TDL`（2026-07-29）、`4FXG → 5JPM`（2023-03-01）。本目录保留 PDBbind 索引实际使用的原 ID：坐标取自 RCSB obsolete full mmCIF，序列取自官方 2021-01-05 SEQRES 快照；每个条目的全部 author chain 和 canonical polymer 序列与 mmCIF 完全一致。替代条目没有加入锚点集合，也没有被描述为与原结构相同。

外部补充保存完整 entry，没有根据自由文本选择或标注“抗体链”“抗原链”等角色。一个 entry 可能包含多条 polymer chain、对称副本或其他分子；PDBbind PPI 索引本身没有提供可供全库统一验证的伙伴链字段。后续任务如需界面伙伴或抗体—抗原子集，应在 processed 层依据结构和外部注释另行定义。

RCSB 文件逐对验证了 entry ID、非空 canonical sequence、坐标、polymer entity 覆盖、FASTA entity 与 mmCIF canonical sequence，以及 FASTA author-chain 集合与 mmCIF 的对应关系。校验器会拒绝选链、改写 header 或仅含部分 entity 的缓存文件，因此此前 PDB 拉取脚本曾出现的选链 FASTA 问题没有进入本来源。

## 采集过程记录

- 2026-09-24：按用户要求把范围限定为原始 PDBbind v2020 PPI 包。核对官网、下载应用和 FAQ，确认 v2020 可直接获取，v2021 及以后需要购买对应订阅；没有注册、申请或购买后续版本，也没有混入 `v2020.R1`。
- 2026-09-24：从官方静态对象下载 `PDBbind_v2020_PP.tar.gz`。对象为 753.71 MiB（790,323,198 bytes），本地 acquisition SHA-256 为 `b85569464299a66392d05bd71b2b1f0d717082c7db97020c0d0f63a62f1ee341`。上游没有提供 whole-file cryptographic checksum；HTTP multipart ETag 为 `bbee7f923b36298500ee978d0a367c26-95`，没有把它当作 MD5。
- 2026-09-24：独立遍历完整 gzip/tar，验证 gzip trailer、成员路径和类型。归档有 2,867 个成员，其中 2,865 件 regular file，未压缩内容 3.04 GiB（3,263,511,209 bytes）；未发现绝对路径、`..` 穿越、符号链接或重复成员。
- 2026-09-24：全量解析 PPI 索引和 2,852 件上游结构，确认行、唯一 PDB ID、结构文件名和结构 `HEADER` ID 四者一致，并核对所有结构均含坐标。数据端点、比较符、单位和分辨率分布按实际原始值统计，没有把不等式或近似值改写为精确值。
- 2026-09-24：在线核对正式方法论文；出版方页面未显示明确正文复用许可，主文不落盘。论文引用的一件 supplement ZIP 从出版方公开端点归档，CRC、成员路径、大小和 SHA-256 均通过。
- 2026-09-24：首次 RCSB 补充取得 2,849 对现行 native FASTA/mmCIF；`3OHM`、`3PVM`、`4FXG` 的现行 FASTA 为 404。随后核对 removed holdings，以官方 obsolete mmCIF 和 2021-01-05 SEQRES 快照补齐原 ID，并对全部 2,852 对重新执行完整解析和 canonical sequence 交叉验证，最终缺口为 0。
- 2026-09-24：source README、论文记录、科学内容复核、许可边界与后续版本付费事项完成审阅；发布前重新运行 source audit、article audit、Markdownlint、目录白名单和 workspace scope 检查。

2026-10-09：按新版动态待办规则复核范围。v2021 及后续付费版本未列入当前 v2020 PPI 获取目标，移出待办；正式方法论文正文仍仅在线核对，保留其未归档事项。来源归档、索引及 2,852 对 PDB 文件未改动。

## 参考文献

- [PDBbind+ 官方主页](https://pdbbind-plus.org.cn/)
- [PDBbind+ 下载页](https://www.pdbbind-plus.org.cn/download)
- [PDBbind+ demo-user agreement](https://www.pdbbind-plus.org.cn/termofuse)
- [PDBbind v2020 protein-protein package](https://static.pdbbind-plus.org.cn/v2020-renew_website/PDBbind_v2020_PP.tar.gz)
- [Liu Z et al. PDB-wide collection of binding data: current status of the PDBbind database](https://doi.org/10.1093/bioinformatics/btu626)
- [RCSB PDB usage policy](https://www.rcsb.org/pages/usage-policy)
- [RCSB removed holding 3OHM](https://data.rcsb.org/rest/v1/holdings/removed/3OHM)
- [RCSB removed holding 3PVM](https://data.rcsb.org/rest/v1/holdings/removed/3PVM)
- [RCSB removed holding 4FXG](https://data.rcsb.org/rest/v1/holdings/removed/4FXG)
- [RCSB 2021-01-05 SEQRES snapshot](https://pdbsnapshots.s3.amazonaws.com/20210105/pub/pdb/derived_data/pdb_seqres.txt.gz)

## 其他

### 数据范围和限制

当前 source 是 v2020 的 protein-protein general set，并非抗体—抗原专库。2,852 条中包含多种蛋白—蛋白系统，索引没有结构化的 antibody、antigen、partner chain、物种或 assay method 字段。若项目需要抗体结合排序数据，应先建立有证据的子集与链角色映射，再考虑训练／测试划分；直接把 2,852 行全部当作抗体样本会改变原始数据含义。

每条记录只展示一个优先端点，同一复合物可能还有未展示的测量；自由文本也可能指出数值近似、结构与测量对象差异或“not found in reference”等情况。原始论文 PDF 和逐项 assay 条件不在交付包中，因此全库数值可用于文献汇编层面的建模和筛选，但不能据此重建统一实验协议或逐条复核底层曲线。

### 完整性与验收

原始归档的大小、本地 SHA-256、gzip trailer、全部 2,867 个成员、2,865 件 regular file 和 3.04 GiB（3,263,511,209 bytes）未压缩内容均已独立复核。主 PPI 索引 2,852 行、2,852 个唯一 ID、2,852 件上游 PDB 结构和 2,852 对外部 RCSB FASTA/mmCIF 全部闭合；论文 supplement 也通过独立 hash 和归档检查。

这证明本项目取得并完整保存了所选 v2020 PPI 公开包及项目要求的结构补充，不表示取得了 v2020 其他三类结构包、约 40,500 篇原始参考文献、论文底层整理日志、`v2020.R1` 或任何付费后续版本。

### 许可和再分发边界

PDBbind+ 当前页面允许 v2020 直接下载，但免费访问不等于开放许可。其 demo-user agreement 授予个人、不可转让、非独占的免费数据／服务使用权，并明确要求 raw data 不得向第三方再分发、传播、出借或转让；基于 raw data 生成的 derivative data 限本人及同一站点组织成员内部使用，未经复旦大学与上海陶术书面授权也不得向第三方再分发。本项目据此只把本目录作为内部 raw source 使用，不把它作为可对外镜像的开放数据包。

方法论文页面标为 `Free`，但没有显示明确的正文复用许可；主文因此只保留在线入口，出版方 supplement 仅在项目内部归档。RCSB/wwPDB 的原始 PDB archive 和 API 数据则按 [CC0 1.0](https://www.rcsb.org/pages/usage-policy) 提供，鼓励在可能时注明原结构作者；该 CC0 只覆盖 `pdb/` 外部补充，不能扩展到 PDBbind 整理的索引、注释或论文材料。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| v2020 全库 23,496 个复合物，包括 2,852 个 PPI | 包内总说明及四类 index 数量一致 | 已包含索引背景；本 source 只接入 PPI 结构包 |
| PPI general set 2,852 条及相应原始结构 | `INDEX_general_PP.2020` 2,852 行与 2,852 件 `.ent.pdb` 完全对应 | 已包含 |
| 从约 40,500 篇原始文献人工整理 v2020 全库结合数据 | PPI 行保留 reference token 和自由文本，原始文献 PDF 与核对日志不在包内 | 部分包含 |
| protein-ligand processed clean structures | 本包只有 PPI 原始 `.ent.pdb`；说明文件明确 processed structures 只为 protein-ligand 提供 | 不属于本包 |
| v2021 及后续数据库版本 | 官网要求购买对应版本订阅 | 不属于本次 v2020 PPI source version |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-09；影响离线复核，不阻塞 v2020 PPI 内部接入）：方法论文 `10.1093/bioinformatics/btu626` 的正式正文已在出版方页面在线核对，本地仍未归档。出版方页面标 `Free`，本次直接请求返回 Cloudflare 403 challenge；Europe PMC 对 PMID 25301850 标记 `isOpenAccess=N`、`inEPMC=N`、`hasPDF=N`，仅列需订阅的 DOI 入口。这些状态不证明正文不公开，也不给出再利用许可。当前保留在线入口及已验收的 supplement，不保存 challenge 页或冒用其他版本；取得出版方许可范围明确且身份可核验的正式正文文件并完成完整性检查后关闭。
- `Q02`（最近更新：2026-09-24；不阻塞内部 raw 接入）：现行 demo-user agreement 明确限制 PDBbind raw 和 derivative data 的第三方再分发，论文正文与 supplement 也未显示开放复用许可。当前目录仅供项目内部使用，飞书文档只同步数据说明而不上传 payload；任何对外数据发布、镜像或衍生数据共享均需先取得相应权利方书面授权。获得覆盖拟议用途的明确授权或许可后关闭本项。
