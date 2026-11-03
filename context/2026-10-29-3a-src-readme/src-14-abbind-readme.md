---
tags:
  - context
---

# SRC_R14_ABBIND 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [文件关系与记录粒度](#文件关系与记录粒度)
  - [计算结果归档](#计算结果归档)
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
- [待解决问题与处理进展](#待解决问题与处理进展)

## 数据集身份

- `source_id`：`SRC_R14_ABBIND`
- `source_version`：`snapshot-2019-04-10`
- 原作者或发布机构：Sarah Sirin、James R. Apgar、Eric M. Bennett、Amy E. Keating 及其所在的 MIT Keating Lab / Pfizer Global Biotherapeutics Technologies 研究团队

### 来源方背景

AB-Bind 由论文作者团队整理。Sarah Sirin 与 Amy E. Keating 当时来自 MIT 生物学系，James R. Apgar 与 Eric M. Bennett 来自 Pfizer Global Biotherapeutics Technologies；论文同时说明 Pfizer 为 Sarah Sirin 的博士后研究提供了经费，并为 Rosetta 和 Discovery Studio 计算提供资源。[MIT Keating Lab](https://keatinglab.mit.edu/research/) 的研究将计算建模和设计与分子生物学、蛋白化学、结构生物学及高通量实验结合，用于研究蛋白质识别；[MIT 教师页](https://be.mit.edu/faculty/amy-e-keating/) 记载 Amy E. Keating 于 2002 年加入 MIT 生物学系、2014 年加入生物工程系。这些背景说明了数据汇编和计算评测的责任主体及合作关系。

## 实验设计和数据口径

AB-Bind 没有为数据库统一重做一批结合实验。作者从已发表文献中手工汇集亲本复合物及其界面突变体的结合数据，再将不同研究报告的亲和力变化统一表示为
`ddG(kcal/mol) = ΔG_mutant − ΔG_parent`。因此，负值表示突变体比亲本结合更强，正值表示结合减弱；每行记录的是一个文献来源下的突变及其相对亲本变化，而不是绝对 `KD`。

当前固定版本包含 1,101 行、32 个亲本体系，其中 27 个以晶体结构为起点，5 个以同源模型为起点。按 `Mutation` 中逗号分隔的突变成分计数，645 行是单一成分突变，456 行包含两个或更多突变成分；后者包括多位点突变，也有一条带缺失表示的记录。论文正文一处写成“466 multi-point mutants”，但同一段随后给出的 92 个双侧突变和 364 个单侧多突变相加为 456，实际 CSV/XLSX 扫描也为 456，因此本说明采用文件可复核的 456。

```text
多篇已发表研究中的亲本/突变体结合结果
                    │ 手工汇编并统一为 ΔΔG
                    ▼
        32 个亲本体系、1,101 条记录
          ├── 27 个晶体结构体系：1,014 条
          └── 5 个同源模型体系：87 条
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
实验 CSV/XLSX：同一张表    计算 ZIP：7 种方法的预测表
1,101 行、16 列          覆盖行数因方法而异
```

结合数据来自 9 类 `Assay Name`。其中表面等离子体共振（SPR）通常由芯片上的实时结合/解离响应估计动力学或结合常数；KinExA 在溶液平衡后测游离抗原并拟合亲和力；ELISA、噬菌体 ELISA、AlphaScreen、酵母展示流式检测和两类酶活抑制实验则通过各自的信号或活性读数评估结合。作者从各原研究换算 `ΔΔG`，但公开表没有逐实验原始曲线、重复测量、拟合参数或统一检测限。跨体系、跨 assay 的数值精度和检测范围不同，建模或比较时应保留 `#PDB`、`Assay Name` 和文献来源信息。

公开表有 51 行 `ddG(kcal/mol)` 字面值为 `8`。补充材料说明，作图时对“在相应 assay 灵敏度内未检测到结合”的变体统一赋值 `8 kcal/mol`。这些值应按检测边界下的强烈减弱/非结合占位处理，不宜解释为精确测得恰好 `8 kcal/mol`。全表按 `ddG` 符号统计，负值、零和正值分别有 281、45 和 775 行；其中正值计数包含上述 51 行占位。

作者还从每个亲本坐标出发，用 bASA、Rosetta、dDFIRE、DFIRE、STATIUM、FoldX 和 Discovery Studio 评价突变。公开 ZIP 保存方法级的实验值/计算分数对照表，未保存每个突变体的计算结构。7 张表的行数和键表示并不完全一致，不能按归档内行号直接拼接，也不能用其中的 `expt` 覆盖主实验表。

## 论文原文

- 标题：AB-Bind: Antibody binding mutational database for computational affinity predictions
- 作者：Sarah Sirin；James R. Apgar；Eric M. Bennett；Amy E. Keating
- 发表来源：*Protein Science* 25(2), 393–409
- 归档文本版本：正式发表版（Version of Record）
- 在线发布日期：2015-11-06；纸本卷期：2016-02
- DOI：[`10.1002/pro.2829`](https://doi.org/10.1002/pro.2829)
- PMID / PMCID：[`26473627`](https://pubmed.ncbi.nlm.nih.gov/26473627/) / [`PMC4815335`](https://pmc.ncbi.nlm.nih.gov/articles/PMC4815335/)
- 本地文件：`articles/ABBind_2015-11-06_ProteinScience-Version-of-Record.pdf`
- 文件大小：3.37 MiB（3,533,169 bytes），17 页
- SHA-256：`8f17a3c32d5a5afeb66bfe2cf2f1311252145a5f0e284aebd35dc1f5e45b6355`
- 文本许可：© 2015 The Protein Society；文章页面未声明 Creative Commons 许可。仅凭 PMC 免费阅读状态不能确定正文、附件或数据文件的再分发范围
- 补充材料：
  - `articles/ABBind_2015-11-06_ProteinScience-Version-of-Record-supplement1.docx`：1.18 MiB（1,238,694 bytes），SHA-256 `6fa07bf1a655b9aa2b8f48b3084c7272bc45db5c1403b7c36442bd5326141de5`；含 Figure S1–S7、Table S1–S14、实验方法简介及计算/PyMOL 脚本
  - `articles/ABBind_2015-11-06_ProteinScience-Version-of-Record-supplement2.xlsx`：127.62 KiB（130,684 bytes），SHA-256 `119b4775b6a31a37fc7ec8c91e22375ed0612a59d03bbe55ae7816286983382b`；与固定 Git commit 中的 `AB-Bind_experimental_data.csv.xlsx` 字节完全一致

截至 2026-09-24，[OpenAlex 正式论文记录](https://openalex.org/W2283896596) 的 `cited_by_count` 为 197。该数值是查询日快照，会随数据库更新而变化。

## 仓库内容

数据来自 [`sarahsirin/AB-Bind-Database`](https://github.com/sarahsirin/AB-Bind-Database)，固定在 commit [`f5af13df80000ad9e438a6ccf1147bd5f9d55dba`](https://github.com/sarahsirin/AB-Bind-Database/tree/f5af13df80000ad9e438a6ccf1147bd5f9d55dba)。该 commit 的提交时间为 2019-04-10T22:05:48Z，因此本项目将版本命名为 `snapshot-2019-04-10`。固定 tree 共 36 个上游文件、18.49 MiB（19,384,479 bytes）；以下树按文件类型归组，省略上游和项目 README。

```text
snapshot-2019-04-10/
└── AB-Bind-Database/
    ├── <27 个晶体亲本体系>.pdb
    ├── HM_1KTZ.pdb
    ├── HM_1YY9.pdb
    ├── HM_2NYY.pdb
    ├── HM_2NZ9.pdb
    ├── HM_3BN9.pdb
    ├── AB-Bind_experimental_data.csv
    ├── AB-Bind_experimental_data.csv.xlsx
    └── ABbind_compt_data.zip
```

32 个 PDB 格式文件是作者整理的亲本结构或同源模型。CSV 和 XLSX 是同一张实验汇总表的两种格式；ZIP 是 7 种计算方法的结果归档。上游 `README.md` 仅含项目名，没有额外 schema 或许可说明。

## 数据结构

### 文件关系与记录粒度

| 文件或对象 | 当前版本内容 | 关系与使用口径 |
| --- | ---: | --- |
| `AB-Bind_experimental_data.csv` | 1,101 行 × 16 列；126.59 KiB（129,633 bytes） | CP1252 编码的实验汇总主表 |
| `AB-Bind_experimental_data.csv.xlsx` | 1,101 行 × 16 列；127.62 KiB（130,684 bytes） | 与 CSV 逐单元格语义一致 |
| 正式论文 supplement 2 | 1,101 行 × 16 列；127.62 KiB（130,684 bytes） | 与仓库 XLSX 字节及 SHA-256 一致 |
| 32 个上游 `.pdb` | 27 个晶体亲本结构、5 个同源模型 | 每个体系共享的建模起点，不是 1,101 个突变体各自的实验结构 |
| `ABbind_compt_data.zip` | 17 个成员、14 个普通文件；75.61 KiB（77,428 bytes） | 7 张有效 `.dat` 表及 7 个 macOS AppleDouble 元数据文件 |

用 `#PDB + Mutation` 作为字面键，1,101 行形成 1,096 个唯一键，没有完全重复行。5 个键各出现两次，并带有不同的实验 `ddG`：`1DVF/A:Y49A`、`1N8Z/H:Y100aF`、`1N8Z/L:H91F`，以及 `1T83` 的两组四成分突变。它们是来源汇编保留的不同实验值，不能仅按键去重。

在 1,101 行中，突变链只位于 `Protein-1` 的有 510 行，只位于 `Protein-2` 的有 510 行，同时涉及两侧伙伴的有 81 行。这里的两侧由 `Partners(A_B)` 中下划线左右的链组定义，不能把所有记录都解释为“抗体侧单点突变”。

### 计算结果归档

ZIP 中 7 个有效 `.dat` 文件均使用分号分隔的 `#pdb;mutation;expt;comp` schema。不同计算程序成功处理的突变集合、重复键和突变位点写法不同；插入码的大小写差异也会使字面连接漏配。因此应按方法分别审阅，并在规范化突变表示后显式连接，不能依赖行号。

| 有效文件 | 计算方法 | 行数 | 当前文件中的 `comp` 范围 |
| --- | --- | ---: | ---: |
| `bASA_all_side.dat` | 界面埋藏可及表面积变化（bASA） | 1,106 | -110.9–157.4 |
| `d_studio_expt_comp.dat` | Discovery Studio | 1,039 | -3.94–11.29 |
| `dDfire.dat` | dDFIRE | 1,106 | -2.481–3.353 |
| `dfire.dat` | DFIRE | 1,106 | -3.089–3.958 |
| `foldX_IE.dat` | FoldX interaction energy | 1,094 | -5.215–20.725 |
| `rosetta_expt_comp.dat` | Rosetta | 1,073 | -10.605–22.43 |
| `statium_expt_comp.dat` | STATIUM | 1,110 | -4.332–11.757 |

`comp` 是各方法自身的计算分数，不是共同单位下的实验标签。补充材料的评测脚本按方法处理方向：多数能量函数以更负为更有利，bASA 则以界面埋藏面积增加为有利。归档内 `expt` 的范围为 -3.373 至 9.0，并与主表的非结合占位及部分突变键表示不同；主表 `ddG(kcal/mol)` 才是本版本的实验汇总字段。

### 字段说明

实验 CSV/XLSX 的 16 个字段如下。

| 原始字段 | 来源与含义 | 取值或使用边界 |
| --- | --- | --- |
| `#PDB` | 亲本体系标识 | 27 个 PDB accession 和 5 个 `HM_` 同源模型 ID，共 32 个当前观察值 |
| `Partners(A_B)` | 复合物两侧的链组；下划线左、右分别对应 `Protein-1`、`Protein-2` | 当前版本观察到 14 种链组，见下表 |
| `Protein-1` | 下划线左侧链组对应的伙伴名称 | 文献汇编文本 |
| `Protein-2` | 下划线右侧链组对应的伙伴名称 | 文献汇编文本 |
| `Mutation` | `链:原残基-位点-新残基` 的突变表示；多成分以逗号分隔 | 位点可含小写插入码；一条记录使用 `delta(...)` 表示缺失 |
| `ddG(kcal/mol)` | 文献实验结果统一得到的 `ΔG_mutant − ΔG_parent` | kcal/mol；负值增强、正值减弱；字面值 `8` 含非结合删失占位 |
| `PDB Res. (Angstroms)` | 亲本晶体结构分辨率 | Å；5 个同源模型体系的 87 行为空 |
| `PDB R-value` | 亲本结构精修 R 值 | 无量纲；同源模型行为空 |
| `PDB R-free` | 亲本结构的交叉验证 R-free | 无量纲；空白或 `na` 均按缺失处理 |
| `PDB pH` | 结构解析实验的 pH | 与结合 assay 的 pH 分开使用；空白或 `na` 表示未提供 |
| `PDB T (K)` | 结构解析实验温度 | K；空白或 `na` 表示未提供 |
| `PDB MolProbity clashscore` | 亲本结构的 MolProbity 原子冲突评分 | 同源模型行为空 |
| `PDB DOI` | 亲本结构论文 DOI | 原始文本含前导空格及少量异常字符，raw 中未改写 |
| `Assay Name` | 原研究的结合测定类别 | 当前版本观察到 9 类，见下表 |
| `Assay pH` | 结合实验 pH | 594 行缺失或为特殊缺失值；`1JTG` 的 31 行原样为 `25`，见文末 `Q02` |
| `Assay Temp (Celcius)` | 结合实验温度；保留上游字段拼写 | °C；394 行缺失或为特殊缺失值 |

结构和 assay 条件的缺失/特殊值合计为：`PDB Res. (Angstroms)`、`PDB R-value`、`PDB MolProbity clashscore`、`PDB DOI` 各 87 行，`PDB R-free` 190 行，`PDB pH` 336 行，`PDB T (K)` 256 行，`Assay pH` 594 行，`Assay Temp (Celcius)` 394 行。这里将空白以及 `na`、`n/a`、`nan`、`null`、反斜杠等审计规则识别的特殊表示合并计数，raw 文件保持原值。

**`Assay Name`（实验 CSV/XLSX；取值范围依据：当前 source version 扫描和补充材料定义）**

| 原始取值 | 当前记录数 | 含义 |
| --- | ---: | --- |
| `SPR` | 335 | 表面等离子体共振，实时检测芯片上的结合与解离 |
| `AlphaScreen` | 271 | 基于供体/受体微珠接近产生信号，常用于竞争实验 |
| `ELISA` | 117 | 抗原包被板上的酶联免疫检测 |
| `KinExA` | 88 | 平衡后定量游离抗原并拟合溶液相亲和力 |
| `Phage ELISA` | 75 | 由展示抗体的噬菌体检测包被抗原 |
| `Enzymatic 2` | 70 | MT-SP1 蛋白酶抑制实验，以抗体浓度与稳态反应速率得到 `IC50` |
| `Yeast Disp. Flow Cyt` | 54 | 酵母表面展示结合后用流式细胞术读取信号 |
| `Enzymatic 1` | 48 | HyHEL-10 抑制溶菌酶活性的动力学实验，用活性变化估计结合/解离速率 |
| `Other` | 43 | 上游未归入上述八类；具体口径须回到对应原始文献 |

**`Partners(A_B)`（实验 CSV/XLSX；取值范围依据：当前 source version 扫描）**

每个值均表示“下划线左侧链组对应 `Protein-1`，右侧链组对应 `Protein-2`”。字母是来源 PDB/模型中的链 ID，不是固定的抗体/抗原角色。

| 原始取值 | 当前记录数 | 原始取值 | 当前记录数 |
| --- | ---: | --- | ---: |
| `A_HL` | 282 | `AB_C` | 271 |
| `C_HL` | 127 | `A_B` | 84 |
| `HL_Y` | 48 | `G_HL` | 46 |
| `HL_P` | 43 | `AB_CD` | 39 |
| `HL_VW` | 38 | `HL_V` | 34 |
| `E_HL` | 27 | `A_BC` | 27 |
| `A_D` | 24 | `HL_I` | 11 |

计算 `.dat` 文件的字段如下；4 个字段在 7 张有效表中相同。

| 原始字段 | 含义 | 使用边界 |
| --- | --- | --- |
| `#pdb` | 亲本体系 ID | 大小写与主表 `#PDB` 不同 |
| `mutation` | 计算条目的突变表示 | 与主表的插入码和部分键写法不完全一致 |
| `expt` | 归档随计算结果保存的实验对照值 | 非结合记录可为 `9`，不要覆盖主表 `ddG(kcal/mol)` |
| `comp` | 对应方法的计算分数 | 尺度、单位和有利方向依方法而异 |

### 数据示例

以下是 `AB-Bind_experimental_data.csv` 的第一条真实记录。`PDB DOI` 值开头的 `␠` 用来可视化 raw 中的一个 ASCII 空格；原始空值也保持标明。

| 字段 | 原样值 |
| --- | --- |
| `#PDB` | `1AK4` |
| `Partners(A_B)` | `A_D` |
| `Protein-1` | `huCyc-A` |
| `Protein-2` | `HIV-1 CAPSID (N-Term)` |
| `Mutation` | `D:L483T,D:V486P,D:H487A,D:A488M,D:I491L,D:A492P,D:M496I` |
| `ddG(kcal/mol)` | `0.57` |
| `PDB Res. (Angstroms)` | `2.36` |
| `PDB R-value` | `0.238` |
| `PDB R-free` | `0.306` |
| `PDB pH` | `7` |
| `PDB T (K)` | `100` |
| `PDB MolProbity clashscore` | `4.71` |
| `PDB DOI` | `␠10.1016/S0092-8674(00)81823-1` |
| `Assay Name` | `SPR` |
| `Assay pH` | `6.5` |
| `Assay Temp (Celcius)` | 空字符串 |

这行表示文献汇编中的一个七成分突变及其相对亲本结合自由能变化；同一行携带共享亲本结构的质量信息和原研究 assay 条件。

## PDB 数据库

上游 payload 自带 27 个晶体亲本 PDB 文件和 5 个同源模型。本项目另按 27 个可辩护 RCSB accession 补充了当前完整条目的原始 FASTA 与 mmCIF，用于核对完整 polymer entity、author chain 和 canonical sequence：`1AK4`、`1BJ1`、`1CZ8`、`1DQJ`、`1DVF`、`1FFW`、`1JRH`、`1JTG`、`1KTZ`、`1MHP`、`1MLC`、`1N8Z`、`1T83`、`1VFB`、`1YY9`、`2JEL`、`2NY7`、`2NYY`、`2NZ9`、`3BDY`、`3BE1`、`3BN9`、`3HFM`、`3K2M`、`3NGB`、`3NPS`、`3WJJ`。

5 个 `HM_` 体系没有独立的 RCSB accession；后缀所指条目是建模模板。论文补充材料给出的映射如下。

| AB-Bind 模型 ID | 建模对象 | RCSB 模板 | 报告的模板序列一致性 |
| --- | --- | --- | --- |
| `HM_1YY9` | Hu-225 | `1YY9` | 重链 81%，轻链 80% |
| `HM_3BN9` | Epithin | `3BN9` chain A | 87% |
| `HM_2NYY` | Bont/A2 | `2NYY` chain A | 90% |
| `HM_2NZ9` | Bont/A2 | `2NZ9` chain A | 90% |
| `HM_1KTZ` | TGFβ1 | `1KTZ` chain A | 76% |

因此，32 个来源体系映射到 27 个外部 accession：27 个晶体体系直接使用同名 accession，5 个同源模型复用各自模板 accession。这个关系只确立到 entry 层级。`Partners(A_B)` 和 `Mutation` 使用上游 payload 内作者整理 PDB 或同源模型的链名；逐文件检查确认 32 个自带 PDB 都包含相应链。对照 RCSB 当前 mmCIF 时，`1DQJ`、`1MLC`、`1N8Z`、`1VFB`、`1YY9`、`2NYY`、`2NZ9` 和 `3BN9` 的 AB-Bind `H`/`L` 链名不直接出现在 RCSB author-chain ID 中，跨文件定位前需要另做链映射。外部补充文件是 RCSB 完整 entry 的参考序列和坐标，不是作者整理 PDB 的逐字节副本，也不是突变体结构。

27 对 FASTA/mmCIF 均已解析；每对文件内部的 polymer entity、FASTA header 所列 author chain 和完整 canonical sequence 已逐项交叉核验。PDB 补充目录共 54 个文件、25.23 MiB（26,456,781 bytes）；按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接计算的 inventory SHA-256 为 `03f8b8f426eac80df7c8c3cf63b9951c243fe8230da8d181b5ba144eac777766`。早期缓存曾混入选择链并改写 header 的 FASTA，本轮已删除这些衍生副本并全部按 RCSB 原始 header 和完整 entry 重取、复验。

## 使用方式

CSV 使用 CP1252 编码；读取时显式指定编码即可。这里不在 raw source 内清洗 DOI、修正 pH 或改写非结合占位。

```python
import pandas as pd

table = pd.read_csv(
    dataset_root / "AB-Bind-Database/AB-Bind_experimental_data.csv",
    encoding="cp1252",
)
```

## 采集过程记录

- 2026-09-18：从 GitHub API 固定 `sarahsirin/AB-Bind-Database` 的 commit 和 36 个文件清单，下载到共享 source 的 `.staging/snapshot-2019-04-10.partial/`。逐文件核对 Git blob 身份、大小和 SHA-256；CSV/XLSX 完整解析，计算 ZIP 通过 CRC、成员和路径安全检查。
- 2026-09-18：按实验表和归档内容提取 27 个 RCSB accession。首次 PDB 缓存审计发现部分 FASTA 是选择链并改写 header 的衍生文件，随即清除本轮 staging 中的错误副本，重取原始完整 FASTA 和 mmCIF，并加入 entity/author-chain/canonical-sequence 交叉检查。
- 2026-09-18 至 2026-09-19：出版方 PDF 和两个附件入口返回 403，Europe PMC BioC/OAI 又不为该标准版权文章提供可复用全文包。期间只记录 DOI、PMCID、失败入口和补充材料原名，没有把网页文本或题录当作原文件。
- 2026-09-24：从 PMC 正文页面确认三个逐文件下载入口，完成页面要求的浏览器工作量证明后逐件取得正式 PDF、DOCX 和 XLSX。PDF 通过标题、DOI 和 17 页解析核验；DOCX/XLSX 通过 OOXML ZIP CRC、路径安全和关键 XML 检查。文件按项目命名规则改名，原名 `PRO-25-393.pdf`、`PRO-25-393-s001.docx`、`PRO-25-393-s002.xlsx` 保留在文献记录中。
- 2026-09-24：逐表复核 1,101 行实验记录、单/多成分突变、非结合占位、assay 枚举、重复键、5 个同源模型及 7 张计算表。确认正式 supplement 2 与固定 Git XLSX 字节相同；补充材料缺口结案。
- 2026-09-24：针对旧 PDB 选链脚本的问题重新审计 R14。R14 实际使用的是拒绝改写 header 和选择链副本的完整 entry 获取流程，未使用按抗体/抗原角色生成 FASTA 的通用脚本；当前 27 对文件没有残留受影响副本。验收同时补强为逐 entity 核对 FASTA header 的 author-chain 集合与 mmCIF，并确认表内链名全部存在于 32 个上游自带 PDB。重新从 RCSB 当前端点取得 27 个条目后，全部 FASTA 的 entity、header 和序列语义一致，27 个 mmCIF 逐字节一致；9 个 FASTA 仅记录顺序不同，因内容未变而保留 9 月 18 日原始下载字节。
- 2026-09-24：再次核对固定 commit、当前 Git 仓库、上游 README、正式论文和两份补充材料。当前仓库仍停在同一 commit，文件树中没有许可证文件，README 仍只有项目名；论文和补充材料也未特别说明 AB-Bind 数据文件的使用与再分发许可。因此将许可范围记为不明确，不能据此推定允许或禁止再分发；本轮最初依照当时的停止条件保留在 staging。
- 2026-09-24：项目随后明确许可判定口径：上游通过公开入口主动提供必要 payload、完成合理的一手核验且没有发现与当前接入发布方式冲突的条款时，许可未特别说明作为非阻塞未决事项披露。R14 的其他验收已经全部通过，因此满足 `verified public-package onboarding` 的发布条件；这项流程判断不表示已经取得商用、衍生或另行再分发授权。

README 工作副本每次写入后同步到 staging，并使用 skill 固定 Markdownlint 配置检查。共享 cache 保存独立审计 JSON 和失败过程证据；它们不作为旁路文件写入 source payload。

## 参考文献

- [Sirin S, Apgar JR, Bennett EM, Keating AE. AB-Bind: Antibody binding mutational database for computational affinity predictions. *Protein Science*. 2016;25(2):393–409.](https://doi.org/10.1002/pro.2829)
- [AB-Bind-Database 固定 commit](https://github.com/sarahsirin/AB-Bind-Database/tree/f5af13df80000ad9e438a6ccf1147bd5f9d55dba)
- [PMC 正式论文与关联补充材料入口](https://pmc.ncbi.nlm.nih.gov/articles/PMC4815335/)
- [RCSB Protein Data Bank](https://www.rcsb.org/)
- [MIT Keating Lab research](https://keatinglab.mit.edu/research/)

使用实验记录时应引用 AB-Bind 论文，并根据 `PDB DOI` 追溯和引用产生相应测量的原研究；使用 RCSB 补充结构时同时遵守并引用对应 PDB 条目及其 primary citation。

## 其他

### 数据范围和限制

本 source 是已发表研究的二次汇编和计算评测包，覆盖 32 个亲本体系及其公开突变数据，不包含全部原始传感曲线、板读数、流式事件、实验重复、统一重测结果或每个计算突变体的坐标。体系还包括 Fc receptor、nanobody 和其他抗体样相互作用，范围宽于经典“抗体—抗原”二元复合物。

来源表中的结构质量字段属于共享亲本，不能当作每条突变体各自测得的结构。多个突变可能共享亲本、文献和 assay；5 个重复 `#PDB + Mutation` 键还保留了不同实验值。随机按行切分会让高度相关记录跨越训练集和测试集，建模时更适合按亲本体系、文献或同源关系设计分组。

### 完整性与验收

固定 Git commit 的 36 个上游文件均通过大小、Git blob/本地 SHA-256 和格式检查；两张实验表可完整解析，计算 ZIP 的全部成员通过 CRC 和路径安全检查。论文 PDF 及两份明确引用的补充材料均已取得并通过身份与容器检查；27 对外部 RCSB FASTA/mmCIF 也全部通过序列—坐标一致性验收。

上述技术内容已经齐全。固定 payload 由上游公开 Git 入口主动提供，合理核验后没有发现与本次项目接入发布方式明确冲突的条款；按当前项目规则，许可未特别说明作为 `Q01` 持续跟踪，但不阻塞本次公开包接入。R14 因而满足 `verified public-package onboarding`，不据此声称取得完整研究底层数据或确认特定后续用途的授权。

### 许可和再分发边界

许可按三层分别处理：

- 固定 commit 与截至 2026-09-24 的当前 Git 仓库均没有 `LICENSE`、SPDX 标识或作者给出的数据许可；上游 README 只有项目名。
- 正式论文标注 © 2015 The Protein Society，未声明 Creative Commons 许可；两份补充材料也没有特别说明 AB-Bind 数据文件的许可。本地归档用于核验，不将论文版权条款推定为数据许可。
- 外部补取的 FASTA/mmCIF 适用 RCSB PDB 的使用政策和逐条目引用要求，其条件不覆盖 AB-Bind 实验表或计算结果。

现有一手材料没有说明固定 payload 可以按何种条件使用和再分发，因此这里将权限状态记为**不明确**，而不是推定允许或推定禁止。固定 payload 来自上游公开 Git 入口，当前未发现与项目接入发布方式明确冲突的条款；按项目现行规则，这项不确定性不阻塞本次 source package 发布。`Q01` 继续跟踪许可证据，并限制对商用、衍生和另行再分发权限的判断。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 1,101 条突变记录、32 个亲本体系 | CSV/XLSX 逐行扫描；27 个晶体体系和 5 个同源模型 | 已核实 |
| 645 个单一成分突变、其余为多成分突变 | 实际文件为 645 + 456；正文一处“466”与其后分项及文件不一致 | 已按文件核实并说明 |
| 7 种结构计算方法的比较 | ZIP 内 7 张有效 `.dat` 表及 supplement 1 的脚本/方法说明 | 已核实；覆盖并非逐行一致 |
| 正式论文和两个关联附件 | 17 页 PDF、DOCX supplement 1、XLSX supplement 2 | 已归档并验收 |
| 亲本结构与同源模型 | 上游 32 个 PDB 格式文件；外部补充 27 对 RCSB FASTA/mmCIF | 已核实；没有逐突变体结构 |
| 完整底层实验数据 | 公开包仅提供汇总 `ΔΔG` 和方法级计算表 | 未声称取得 |
| 数据使用与再分发许可 | 固定/当前 Git 仓库、上游 README、论文及补充材料均未特别说明覆盖固定 payload 的许可 | 范围不明确；不阻塞本次接入发布，仍限制商用、衍生和另行再分发判断 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-24；不阻塞本次接入发布，限制后续用途判断）：AB-Bind 数据许可未被上游特别说明，使用与再分发范围因而不明确。复核的固定 commit 与当前 Git 仓库相同，二者的文件树均无许可证文件，最小上游 README 只有项目名；正式论文及两份补充材料也没有给出覆盖实验表、计算表和作者整理结构的数据许可。固定 payload 由上游通过公开 Git 入口主动提供，且未发现与本次项目接入发布方式明确冲突的条款，因此按当前规则可以在其他验收通过后完成公开包接入；这不表示已经取得商用、衍生或另行再分发授权。下一步仍需作者、仓库或权利方提供可核验且明确覆盖该固定 payload 的条款，复核覆盖范围后方可关闭本事项。
- `Q02`（最近更新：2026-09-24；不阻塞整体内容验收）：`1JTG` 的 31 条 SPR 记录在实验表中同时写为 `Assay pH=25`、`Assay Temp (Celcius)=25`，supplement 1 的 Table S1 也原样如此；pH 25 在物理上异常。产生这些数据的[原始研究摘要](https://doi.org/10.1021/bi981772z)说明结合实验考察了不同 pH、最高亲和力出现在 pH 7.5，但没有据此确定这 31 条记录应填的具体 pH。raw 保留 `25`，按 assay pH 分层分析时将这些值视为待确认；下一步核对原始研究完整方法、逐实验条件或作者勘误，只有得到明确证据才更正文档解释或派生数据。
