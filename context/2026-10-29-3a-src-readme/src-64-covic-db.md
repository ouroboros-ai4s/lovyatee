# SRC_R64_COVIC_DB 数据说明

## 数据集身份

- `source_id`：`SRC_R64_COVIC_DB`
- `source_version`：`snapshot-2026-09-19`
- 原作者或发布机构：Coronavirus Immunotherapy Consortium（CoVIC）与 La Jolla Institute for Immunology（LJI；Erica Ollmann Saphire、Bjoern Peters 团队）

### 来源方背景

[CoVIC 官网](https://covic.lji.org/)将其定义为全球学术—产业非营利研究协作，目标是并行比较 SARS-CoV-2 抗体并加速抗体疗法研发。[LJI 于 2020-03-30 发布的成立公告](https://covic.lji.org/la-jolla-institute-for-immunology-to-host-coronavirus-immunotherapy-clearinghouse/)说明，Bill & Melinda Gates Foundation 提供 173 万美元资助建立 CoVIC，总部设在 LJI，由 Erica Ollmann Saphire 领导；公告同时指定 Alessandro Sette 和 Bjoern Peters 团队在 LJI 承载数据库工作。LJI 是 1988 年成立的独立非营利免疫学研究机构。

[CoVIC 项目介绍](https://covic.lji.org/about/)进一步记录了 COVID-19 Therapeutics Accelerator、NIAID 和 GHR Foundation 等支持关系。当前 source 的工作簿由多个 reference laboratories 产生，但 COVIC-DB 的盲化、提交规范、质量检查和公开发布由联盟及 LJI 数据库团队统一组织。

## 实验设计和数据口径

论文记载，60 个学术、政府和产业团队向 CoVIC 提交近 400 个抗 SARS-CoV-2 Spike 抗体或 antibody-like molecules。LJI 为每个提交对象分配 `COVIC-ID`，在保护贡献方知识产权的前提下向 8 个 reference laboratories 分发盲化样品。各实验室在各自负责的平台上平行测量结合动力学、ACE2 blocking、假病毒或真实病毒中和、Fc effector functions、小鼠体内保护、抗体逃逸和 pharmacokinetics 等性质。

```text
60 个贡献团队提交抗体与基础信息
                 │
                 ▼
LJI 分配 COVIC-ID、保存身份映射并盲化分发
                 │
                 ▼
8 个 reference laboratories 按统一模板开展不同 assay
                 │
                 ▼
字段词表、ID、数值格式、检测界限和突变语法自动校验
                 │
                 ▼
通过 QC 的结果进入 COVIC-DB ──► 18 个下载入口
                                      ├── 14 个 XLSX 已取得
                                      └── 4 个入口 HTTP 500
```

公开文件是实验室按 assay 提交并通过数据库校验的表格。14 个工作簿的 `Dataset` sheet 合计 14,859 行，覆盖 413 个不同 `Antibody label` 值；标签集合包含 COVIC 编号和 `CC12.3`、`CR3022`、阴性血浆及感染对照等实验对照。相同 label 会按 antigen、variant、subject、dose 或 endpoint 重复出现，每行的粒度取决于工作簿：Duke SPR 是 label—antigen 结合测量，Ragon 是 label—antigen effector-function 面板，Texas Biomed 和 Nexelis PK 是独立 subject 记录，其余中和或细胞功能表通常每个 label 一行或少量重复行。

数值来源也随 assay 不同：

- SPR 的 association rate、dissociation rate 和 $K_D$ 是动力学拟合结果；较低 $K_D$ 表示较强结合。Duke BLI 表提供 ACE2 response、percent blocking 和重复测量标准差。
- Nexelis 与 UTMB 中和表保存输入浓度、四参数 logistic（4-PL）拟合的 A/B/C/D、拟合优度及 $IC_{50}$、$IC_{80}$、$IC_{90}$。较低 IC 表示在该 assay 和单位下达到相同抑制水平所需浓度较低；µg/mL 和 ng/mL 不能未经换算混用。
- Ragon 表同时保存 7 组 effector-function 的实验值、0–1 normalized value 和定性等级，并另存人/鼠 Fc receptor 的 median fluorescence intensity（MFI）。Normalized value 和 qualitative value 是后续归一化与分档，不是新的独立测量。
- UNC 的中和值和上下检测界限包含 `>`、`<`，属于左右删失的边界字符串。Nexelis pseudovirus 表以 `NA`、空白和 comment 表示无可用 4-PL 拟合或没有达到中和阈值。
- Texas Biomed 保存 K18 hACE2 转基因小鼠的给药、逐日体重和生存结局；其病毒滴度及病理字段在当前公开导出中全部为空。Nexelis PK 的 Pre-Spike ELISA GMC 有数值或 `<50.3`，RBD GMC 在当前导出中全部为空。

论文发表时只有 40% 的抗体贡献方明确同意解除身份盲化，其余继续使用 COVIC-ID。当前 14 份下载表没有贡献方原名称、完整重轻链序列或 COVIC-ID 到 sequence 的公开映射，不能从 assay 数值还原这些信息。它们也不含传感器原始曲线、逐孔读数、图像或完整分析脚本；跨实验室比较应限定在论文所述并行标准化设计和各字段实际单位内。

## 论文原文

- 标题：Coronavirus Immunotherapeutic Consortium Database
- 作者：Mahita Jarjapu、Brendan Ha、Anais Gambiez 等 30 位作者
- 发表来源：*Database*, Volume 2023, baac112
- 归档文本版本：正式发表全文的 Europe PMC NLM JATS XML
- 发布日期：2023-02-10
- DOI：[10.1093/database/baac112](https://doi.org/10.1093/database/baac112)
- PMID / PMCID：[36763096](https://pubmed.ncbi.nlm.nih.gov/36763096/) / [PMC9913043](https://pmc.ncbi.nlm.nih.gov/articles/PMC9913043/)
- 本地文件：`articles/COVIC-DB_2023-02-10_Database-FullText.xml`
- 文件大小：99.91 KiB（102,308 bytes）
- SHA-256：`60248315b29f2e92f01cfc874d79cabde5eea767f03d8be3b198544a5d17b716`
- 文本许可：[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
- 补充材料：`articles/COVIC-DB_2023-02-10_Database-Supplementary.zip`，817.00 KiB（836,606 bytes），SHA-256 `6bca044813dd3b07505e184d562b38aa7d6eb11aa7667f5fe50fb726df73628f`

补充 ZIP 的唯一成员是 `suppl_data/Revised_Supp_Material.doc`，大小 878.00 KiB（899,072 bytes），SHA-256 为 `5dcfde16e0a08b1340ccf002d547aced75a2ed9b574dbe48567db667b63c7f73`。文档包含 COVIC-1 dashboard、使用 PDB `7DDD` 的 RBD-1 表位社区映射，以及 D614/Beta Spike affinity 相关图。

## 仓库内容

上游交付来自 [COVIC-DB Assay Downloads](https://covicdb.lji.org/downloads)，不是 Git 仓库或不可变 release。18 个下载端点均未给出 release identifier、`ETag` 或 `Last-Modified`。本项目把 2026-09-19 取得的 14 份有效 XLSX 精确字节固定为 `snapshot-2026-09-19`；论文发布日期 2023-02-10 只标识论文版本，不用作实时导出的版本日期。

```text
snapshot-2026-09-19/
└── COVIC-DB/
    ├── Duke - BLI.xlsx
    ├── Duke - SPR.xlsx
    ├── Nexelis - PK - Pre spike.xlsx
    ├── Nexelis-Pseudovirus.xlsx
    ├── Nexelis-Pseudovirus-Beta.xlsx
    ├── Nexelis-Pseudovirus-Delta.xlsx
    ├── Nexelis-Pseudovirus-Omicron.xlsx
    ├── Ragon - Functional Data.xlsx
    ├── Texas Biomed.xlsx
    ├── UNC.xlsx
    ├── UTMB - ADMP.xlsx
    ├── UTMB - ADNK.xlsx
    ├── UTMB.xlsx
    └── University of Wisconsin.xlsx
```

14 个 payload 合计 1.34 MiB（1,405,321 bytes）。按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接计算的 inventory SHA-256 为 `0b54604adbb510580544c0c8ca1b3b61e9c7afec31219b48c721467d21a7eac2`。论文和 PDB 补充分别保存在 source version 的 `articles/` 与 `pdb/`，不属于上游 assay payload 树。

## 数据结构

### 工作簿结构和交付范围

每个 XLSX 都有且只有三个 sheet，顺序为 `Instructions`、`Dataset`、`Terminology`。`Instructions` 逐列解释提交模板，`Dataset` 保存公开记录；`Terminology` 仅在需要受控词时填值。下表的“数据行”不含表头。

| 工作簿 | 数据行 | 字段数 | 主要记录粒度 |
| --- | ---: | ---: | --- |
| `Duke - BLI.xlsx` | 389 | 9 | 每个 label 的 RBD—ACE2 blocking 测量 |
| `Duke - SPR.xlsx` | 2,326 | 12 | label—antigen 动力学或无结合结论 |
| `Nexelis - PK - Pre spike.xlsx` | 3,307 | 7 | label—dose—subject 的 Pre-Spike ELISA GMC |
| `Nexelis-Pseudovirus.xlsx` | 362 | 13 | 每个 label 的 D614 pseudovirus 4-PL/IC 结果 |
| `Nexelis-Pseudovirus-Beta.xlsx` | 360 | 13 | 每个 label 的 Beta pseudovirus 4-PL/IC 结果 |
| `Nexelis-Pseudovirus-Delta.xlsx` | 361 | 13 | 每个 label 的 Delta pseudovirus 4-PL/IC 结果 |
| `Nexelis-Pseudovirus-Omicron.xlsx` | 359 | 13 | 每个 label 的 Omicron pseudovirus 4-PL/IC 结果 |
| `Ragon - Functional Data.xlsx` | 1,480 | 32 | label—antigen 的 Fc effector/Fc receptor 面板 |
| `Texas Biomed.xlsx` | 3,999 | 29 | label—dose—小鼠 subject 的体重与生存记录 |
| `UNC.xlsx` | 593 | 8 | virus backbone—mutation—label 的中和结果 |
| `UTMB - ADMP.xlsx` | 368 | 5 | 每个 label 的 antibody-dependent monocyte phagocytosis |
| `UTMB - ADNK.xlsx` | 371 | 7 | 每个 label 的 NK activation 三组 endpoint |
| `UTMB.xlsx` | 405 | 16 | 每个 label 的真实病毒中和 4-PL/IC 结果 |
| `University of Wisconsin.xlsx` | 179 | 5 | label—plaque 的 escape mutation |

### 跨文件关系和缺失编码

`Antibody label` 是跨表连接入口，但不是完整主键。14 个文件合计观察到 413 个不同 label，只有 51 个同时出现在全部现有导出；不同工作簿分别覆盖 75–405 个 label，并混入 assay-specific controls。相同 label 在 Duke SPR 可对应多个 antigen，在 Ragon 可对应四个 antigen，在体内与 PK 表则对应多个 dose 和 subject。跨表 join 必须同时保留文件、assay、antigen/variant、experiment、subject 和 dose 上下文。

数值在 XLSX 中大多以字符串保存。空白可能表示未测、未报告、无拟合或该公开导出未提供，具体解释依赖工作簿和 comment。当前文件还观察到三类显式特殊值：Nexelis 4-PL/IC 的 `NA`、UNC 与 PK 的 `<...`/`>...` 检测边界，以及自然语言 comment。Raw 层保留这些原值；不能把空白和 `NA` 统一转换成阴性或零，也不能直接去掉检测界限符号。

### 字段说明

以下分组覆盖 14 个 `Dataset` sheet 的全部原始字段；同一行列出多个字段时，组内命名规则可以还原每个表头。

| 适用工作簿 | 原始字段 | 原始表示、单位和含义 |
| --- | --- | --- |
| 全部 14 个工作簿 | `Antibody label` | 字符串；COVIC 盲化编号或实验对照名称。当前有 413 个不同值，不是 sequence ID。 |
| Duke BLI、Duke SPR、Ragon、Wisconsin、Nexelis PK | `Experiment identifier` | 实验/提交批次标识字符串；Wisconsin 当前 179 行均为空，Nexelis PK 当前有 45 个不同值。 |
| Duke BLI、Duke SPR、Ragon | `Tested antigen` | 实验所用 antigen 名称。Duke SPR 当前含 RBD、NTD、D614G/HexaPro、Beta 和 Omicron 等 8 种原始写法；Ragon 含 D614G Spike、RBD、S1、S2。 |
| Duke BLI、Duke SPR | `n` | 重复次数的字符串；当前均为 `3`。 |
| 多个 assay | `Comment` | 自由文本；用于无结合/无中和、检测边界、重测、样本量不足等说明。空白表示没有附加 comment。 |
| Duke SPR | `on rate; Ka in M^-1s^-1`、`Standard deviation in M^-1s^-1` | SPR association rate 及标准差，单位 M⁻¹s⁻¹；无可用拟合时为空。较高 Ka 表示更快结合。 |
| Duke SPR | `off rate; Kd in 1/s`、`Standard deviation in 1/s` | SPR dissociation rate 及标准差，单位 s⁻¹；较低 Kd 表示较慢解离。这里的小写 `Kd` 是 rate，不是 equilibrium $K_D$。 |
| Duke SPR | `dissociation constant; KD in M`、`Standard deviation in M` | 平衡解离常数及标准差，单位 M；较低 $K_D$ 表示较强结合。 |
| Duke SPR | `Qualitiative measure` | 上游表头保留拼写错误。术语 sheet 允许 `positive`、`negative`、`unknown`、`weak`、`moderate`、`strong`；当前只观察到 1,948 个 `positive` 和 378 个 `negative`。 |
| Duke BLI | `ACE 2 response; in nM`、`ACE 2 response; percent blocking`、`Standard deviation in percent` | ACE2 response 的 nM 表示、percent blocking 及百分比标准差；percent blocking 越高表示阻断比例越高。部分 blocking/SD 为空。 |
| Duke BLI | `Status` | 当前 389 行均为 `Approved`，表示提交记录状态。 |
| 4 个 Nexelis pseudovirus 与 UTMB | `mAb concentration (ug/mL)`、`Starting dilution fold`、`Starting concentration (ug/mL)` | 浓度和稀释设置，以 µg/mL 与倍数表示；是拟合输入条件。 |
| 4 个 Nexelis pseudovirus 与 UTMB | `4-PL curve parameter A`、`4-PL curve parameter B`、`4-PL curve parameter C`、`4-PL curve parameter D`、`4-PL curve R2` | 四参数 logistic 拟合的最小值、Hill slope、inflection point、最大值和拟合优度。Nexelis 中失败拟合可写 `NA`，UTMB 的 C 当前全空。 |
| UTMB | `R^2adj`、`Date` | Adjusted R-squared 与 assay 日期；日期在 XLSX 中以日期时间字符串保存，当前仅 32 行非空。 |
| 4 个 Nexelis pseudovirus | `neutralization IC50 (ug/mL)`、`neutralization IC80 (ug/mL)`、`neutralization IC90 (ug/mL)` | 假病毒中和浓度，单位 µg/mL；较低值表示更高 potency。未达到阈值或无拟合时为空或 `NA`，comment 保留具体说明。 |
| UTMB | `neutralization IC50 (ng/mL)`、`neutralization IC80 (ng/mL)`、`neutralization IC90 (ng/mL)` | 真实病毒中和浓度，单位 ng/mL；方向同上，与 µg/mL 字段单位不同。 |
| UTMB | `ref1 IC50 (ng/ml)`、`ref2 IC50 (ng/ml)` | 两个 reference antibody 的 IC50，单位 ng/mL；分别有 125 和 139 个空白。 |
| UNC | `Virus Backbone`、`Mutation` | Virus backbone 当前为 `WA-1` 或 `SA/B.1.351`；`Mutation` 是逗号分隔的 point mutation 或 deletion 字符串。 |
| UNC | `neutralization IC50 (ng/mL)`、`neutralization IC80 (ng/mL)`、`MPI (%)`（原表头末尾含一个空格） | 中和 IC50/IC80 和 maximum percent inhibition。IC 字段可为数值或 `<0.16`、`<0.32`、`>12500`、`>25000` 等删失字符串；MPI 表头的尾随空格是原始 schema 的一部分。 |
| UNC | `ULOD (ng/mL)`、`LLOD (ng/mL)` | Upper/lower limit of detection；当前原值为 `>25000`/`>12500` 和 `<0.003`/`<0.16`/`<0.32`。 |
| Ragon | `ADCP (Phagocytic Score)`、`ADNP (Phagocytic Score)`、`ADCD (MFI C3)`、`ADNKA % CD107a+`、`ADNKA % MIP-1b+`、`mADCP (Phagocytic Score)`、`mADNP (Phagocytic Score)` | 7 组直接 assay endpoint：人/鼠 phagocytosis、C3 deposition MFI 及 NK activation 百分比；名称中的单位或 score 类型按原表保留。 |
| Ragon | 上述 7 个 endpoint 各自的 `<endpoint> normalized value` | 从直接 endpoint 派生的 0–1 normalized value；个别记录为空。 |
| Ragon | 上述 7 个 endpoint 各自的 `<endpoint> qualitative value` | 分档值。术语 sheet 允许 `positive`、`negative`、`unknown`、`weak`、`moderate`、`strong`；当前只观察到 `weak`、`moderate`、`strong`。 |
| Ragon | `FcgR2aR (MFI)`、`FcgR3aV (MFI)`、`FcgR2b (MFI)`、`FcgR3b (MFI)`、`FcRn (MFI)` | 对人 Fc receptors 的 median fluorescence intensity；当前每列 1,480 行均非空。 |
| Ragon | `mFcR2 (MFI)`、`mFcR3 (MFI)`、`mFcR4 (MFI)` | 对鼠 Fc receptors 的 median fluorescence intensity；当前每列 1,480 行均非空。 |
| UTMB ADMP | `Mean Phagocytosis (% infected cells)`、`Fold increase over virus control`、`Phagocytic Score` | 感染细胞平均 phagocytosis 百分比、相对 no-antibody virus control 的倍数及分档。当前 score 为 `weak`、`moderate`、`strong`，16 行为空。 |
| UTMB ADMP、Texas Biomed | `Batch` | 批次标识字符串；只在各自文件内解释。 |
| UTMB ADNK | `ADNKA % CD107a+`、`ADNKA % IFNg+`、`ADNKA % TNFa+` | NK cells 表达 CD107a、IFNγ、TNFα 的百分比；每列有 30–33 个空白。 |
| UTMB ADNK | `Fold-change ADNKA % CD107a+`、`Fold-change ADNKA % IFNg+`、`Fold-change ADNKA % TNFa+` | 相对 virus control 的 fold-change，与对应百分比 endpoint 成对。 |
| Wisconsin | `Plaque`、`Mutation` | Plaque pick 编号和 escape mutation 字符串；各有 168 行非空。 |
| Texas Biomed、Nexelis PK | `Dose (mg/kg)`、`Subject` | 给药剂量和 subject ID；subject 在各文件内均为 3,999 或 3,307 个不同字符串。 |
| Texas Biomed | `Group`、`Animal Model Strain` | 实验组字符串与动物模型；当前所有 3,999 行的 strain 均为 `K18 hACE2 transgenic mice`。 |
| Texas Biomed | `Weight day 0` 至 `Weight day 10` | 小鼠逐日体重，单位 g；死亡或停止观察后后续日期为空。 |
| Texas Biomed | `Day of death`、`Death reason` | 结局日和原因；当前原因观察到 `ethical euthanization`、`survived until end`、`unplanned death`，另有 1 个空白。 |
| Texas Biomed | `Viral titer nasal turbinates day 2`、`Viral titer nasal turbinates day 4`、`Viral titer lung day 2`、`Viral titer lung day 4` | 模板定义单位 PFU/mL；当前四列全部为空。 |
| Texas Biomed | `Inflammation`、`Edema`、`Vasculitis`、`Necrosis`、`Hemorrhage`、`Morphologic diagnosis/findings` | 前五项模板定义为 0–5 病理 score，最后一项为形态学诊断自由文本；当前六列全部为空。 |
| Nexelis PK | `GMC for Pre-Spike IgG ELISA (ELU/mL)`、`GMC for RBD IgG ELISA (ELU/mL)` | IgG ELISA geometric mean concentration，单位 ELU/mL。Pre-Spike 当前均非空并含 577 个 `<50.3`；RBD 当前 3,307 行全部为空。 |

### 数据示例

下面均为 `Dataset` sheet 的真实记录摘录；为便于阅读，只显示代表性字段。

```text
file=Duke - SPR.xlsx
Experiment identifier=DU-KJL-000079
Antibody label=COVIC-1
Tested antigen=SARS2-RBD-No Tag
n=3
on rate; Ka in M^-1s^-1=25979.7852616159
off rate; Kd in 1/s=0.0374557124021545
dissociation constant; KD in M=1.45935560587441e-06
Qualitiative measure=positive
```

这是一条 label—antigen SPR 拟合记录；同一 label 在该文件还可对应其他 antigen。

```text
file=Nexelis-Pseudovirus.xlsx
Antibody label=COVIC-6
mAb concentration (ug/mL)=2000
Starting dilution fold=10
Starting concentration (ug/mL)=200
4-PL curve parameter C=34.85
4-PL curve R2=0.987
neutralization IC50 (ug/mL)=36.3
neutralization IC80 (ug/mL)=74.9
neutralization IC90 (ug/mL)=118
```

这是一条 D614 pseudovirus 的 label 级拟合和中和浓度记录。

```text
file=UNC.xlsx
Virus Backbone=WA-1
Mutation=D614G
Antibody label=COVIC-1
neutralization IC50 (ng/mL)=245
neutralization IC80 (ng/mL)=662
MPI (%) =100
ULOD (ng/mL)=>25000
LLOD (ng/mL)=<0.003
```

这里的 ULOD/LLOD 是该行测量边界；其他 UNC 行的 IC 字段本身也可能是边界字符串。

```text
file=Ragon - Functional Data.xlsx
Experiment identifier=1
Tested antigen=SARS-CoV-2 D614G Spike
Antibody label=COVIC-1
ADCP (Phagocytic Score)=3.848647054797381
ADCP (Phagocytic Score) normalized value=0.4076480829358036
ADCP (Phagocytic Score) qualitative value=weak
FcgR2aR (MFI)=6.087372930574111
```

这是 COVIC-1 对一个 antigen 的 effector-function 面板行；同一行还有其余 6 组 endpoint 和 7 个 Fc receptor MFI 字段。

```text
file=Texas Biomed.xlsx
Batch=1
Antibody label=COVIC-124
Dose (mg/kg)=0.5
Subject=E1A1
Group=Treated_COVIC-124_0.5
Animal Model Strain=K18 hACE2 transgenic mice
Weight day 0=17.1
Weight day 6=12.5
Day of death=6
Death reason=ethical euthanization
```

这是一只动物的纵向体重和生存汇总行，不是 11 条独立日记录。

```text
file=Nexelis - PK - Pre spike.xlsx
Antibody label=COVIC-124
Experiment identifier=1
Dose (mg/kg)=0.5
Subject=E1A1
GMC for Pre-Spike IgG ELISA (ELU/mL)=<50.3
GMC for RBD IgG ELISA (ELU/mL)=
```

这是一条 subject 级 PK/ELISA 记录；`<50.3` 是检测界限，空 RBD GMC 是当前公开导出的系统性缺失。

## PDB 数据库

PDB 审计以论文和正式补充材料为依据。主文没有给出工作簿记录到结构的逐行 PDB ID；补充图 2 则明确说明使用 PDB `7DDD` 映射 COVIC-1 所属 RBD-1 epitope community 的 residues。本项目因此只接受 `7DDD` 作为“共享表位可视化框架”，没有把一般 Spike 结构或其他抗体复合物扩展成 COVIC label 的结构标签。

[RCSB 7DDD](https://www.rcsb.org/structure/7DDD) 是 3.00 Å cryo-EM 的闭合态 SARS-CoV-2 Spike homo-trimer，author chains 为 A/B/C，共享一个长度 1,261 的 protein entity。当前 mmCIF 有 25,503 个 atom records。结构本身不含 COVIC-1 或其他 COVIC 抗体；补充材料只是把 epitope-community residues 映射到这套 Spike 表面，因此没有可辩护的 antibody chain、row-level construct 或 assay-specific chain 对应。

2026-09-25 从 RCSB 取得一对当前 entry 文件：

- `pdb/sequences/rcsb_pdb_7DDD.fasta`：1.33 KiB（1,362 bytes），SHA-256 `391b2b89e9becc5e49a1065a71270a58734d849b7ee966b9bc992338ecb82398`。
- `pdb/structures/7DDD.cif`：2.46 MiB（2,582,637 bytes），SHA-256 `9483977dfaa0cb2ae8f37fc2cf651fe7a73cda1f2a99387a705fe06bf0432bcf`。

两项合计 2.46 MiB（2,583,999 bytes），inventory SHA-256 为 `b4a3624ab68588204d8c390a3b5ea85a8715d1f188c33314e3a01a196929ce3b`。验收确认 FASTA 与 mmCIF 的 entry ID 均为 `7DDD`、mmCIF 含 `atom_site`，且唯一 polymer entity 的 canonical sequence 完全一致。RCSB 页面当前标记 entry version 1.2（2024-11-06 修订）；本地文件是 2026-09-25 取得的当前 RCSB 快照，不代表 2023 年论文附件中的结构字节。

## 采集过程记录

- 2026-09-19：批次工作流从 COVIC-DB 18 个广告端点中取得 14 个 XLSX，并将精确字节暂存；assay 8、9、16、21 返回 HTTP 500，没有创建空文件或错误页占位。同期从 Europe PMC 取得正式全文 XML，并解析 OUP 页面链接取得正式补充 ZIP。
- 2026-09-19：初始配置暂以论文日期命名 `snapshot-2023-02-10`，并用 `6VSB` 作为弱 Spike 代表结构；当时尚未完成补充材料中的结构证据核读，因此均保留待复核。
- 2026-09-25：重新访问下载页和全部 18 个端点；14 个成功端点的 XLSX 容器 bytes/SHA-256 均变化，但逐 sheet、逐单元格与冻结文件一致。四个失败端点仍返回 5,124-byte HTTP 500 HTML。新增只读 `recheck_r64.py` 固化这项检查，不保存实时响应。
- 2026-09-25：确认论文发布日期不能标识实时导出版本，把 source version 更正为 `snapshot-2026-09-19`，并为 14 个 XLSX、全文 XML 和补充 ZIP 在配置中固定精确 bytes/SHA-256；暂存目录同步改名。
- 2026-09-25：用 ZIP 安全检查和 OLE magic 核验补充包，并用 `antiword 0.37` 核读唯一 Word 成员。补充图 2 明确指定 `7DDD` 后，删除可重新取得但证据较弱的 `6VSB` 对，改取 `7DDD` FASTA 与完整 mmCIF。
- 2026-09-25：逐表核对三个 sheet、全部表头、14,859 个数据行、特殊值、检测界限、413 个 label 及跨表覆盖；修正审计草稿中误写的聚合行数和 Duke SPR 定性计数，并把 R64 专用语义检查接入主审计。文件集合、文章身份、ZIP、payload hashes 和 PDB pair 全部通过 staging 审计。
- 2026-09-25：固定版 markdownlint、workspace scope、发布前审计均通过；发布脚本在目录移动前后各运行完整审计，把暂存目录原子发布为 `SRC_R64_COVIC_DB/snapshot-2026-09-19`。发布后再次独立审计通过，并删除空的 `.staging` 父目录。

## 参考文献

- [COVIC-DB Assay Downloads](https://covicdb.lji.org/downloads)
- [COVIC-DB dashboard](https://covicdb.lji.org/)
- [Jarjapu et al. (2023), Coronavirus Immunotherapeutic Consortium Database](https://doi.org/10.1093/database/baac112)
- [Europe PMC / PMC9913043 全文记录](https://pmc.ncbi.nlm.nih.gov/articles/PMC9913043/)
- [Coronavirus Immunotherapy Consortium 官网](https://covic.lji.org/)
- [LJI 的 CoVIC 成立公告](https://covic.lji.org/la-jolla-institute-for-immunology-to-host-coronavirus-immunotherapy-clearinghouse/)
- [RCSB PDB 7DDD](https://www.rcsb.org/structure/7DDD)
- [Zhang et al. (2021), Development and structural basis of a two-MAb cocktail for treating SARS-CoV-2 infections](https://doi.org/10.1038/s41467-020-20465-w)
- [RCSB PDB 文件下载服务](https://www.rcsb.org/docs/programmatic-access/file-download-services)
- [RCSB PDB 使用政策](https://www.rcsb.org/pages/usage-policy)

## 其他

### 数据范围和限制

当前版本是 14/18 个广告 assay 的公开子集。它保留了跨实验室平行表征的广度，但不同文件的数值单位、拟合模型、antigen/variant 和记录粒度不同，不能把所有行堆叠成单一 $K_D$ 或 IC 回归表。跨 assay 建模需要显式保留实验来源，并处理重复 label、controls、检测界限、`NA`、系统性空列和不同浓度单位。

公开工作簿不提供贡献方身份、重轻链序列、isotype、完整 epitope community 表或 COVIC-ID 到结构/sequence 的连接。随机按行拆分还会使同一 label、subject group、variant 或 antigen 的相关记录跨 split 泄漏。Texas Biomed 的日体重在一行内重复测量，Ragon 的 raw/normalized/qualitative 是同一 endpoint 的不同表示，也不能作为相互独立样本。

### 完整性与验收

Source version 含 14 个 payload、2 个论文对象和 1 对 RCSB 文件，共 18 个文件、4.70 MiB（4,928,234 bytes），另有一份项目生成的 `README.md`。验收覆盖固定文件集合、每个配置对象的 bytes/SHA-256、XLSX sheet 顺序、全部表头和行数、论文标题/DOI/许可短语、补充 ZIP 成员和 OLE identity、PDB entry/entity/atom/sequence，以及 symlink、`.partial` 和旁路文件检查。

Payload inventory 为 1,405,321 bytes / `0b54604adbb510580544c0c8ca1b3b61e9c7afec31219b48c721467d21a7eac2`；PDB inventory 为 2,583,999 bytes / `b4a3624ab68588204d8c390a3b5ea85a8715d1f188c33314e3a01a196929ce3b`。2026-09-25 的实时复核确认下载页仍列出同一组 18 个 assay，14 个可用导出的单元格值与冻结版本一致，4 个端点仍为 HTTP 500。当前目录没有 symlink、manifest、HTTP 响应、验证日志或 partial 文件。

### 许可和再分发边界

主论文明确写明 COVIC-DB 中的数据 released without license restrictions，并在 Data availability 指向公开数据库与 assay 下载页；下载工作簿没有另附命名的标准许可证文件。本项目据此保存和发布本次公开导出，同时保留论文引用、来源 URL、快照日期和哈希。该表述覆盖数据库已经公开的数据，不扩展到仍被盲化、尚未公开的贡献方身份或序列映射。

论文 XML 和所属补充材料采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，再利用时需署名、提供许可链接并标明改动。RCSB 补取的 FASTA 和 mmCIF 属于 wwPDB Core Archive data；[RCSB usage policy](https://www.rcsb.org/pages/usage-policy)说明其适用 CC0 1.0，并鼓励引用原始结构作者。各 assay 所涉及的抗体知识产权、原始实验记录和第三方论文权利不会因数据库数据公开而自动转移。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 60 个团队贡献近 400 个抗体，8 个 reference laboratories 并行测试 | 14 个 assay 工作簿、413 个 label 值、14,859 行 | 已取得公开结果子集；label 集合含 controls，不能与论文抗体数直接一一对应 |
| Binding affinity、ACE2 blocking、中和、Fc functions、in vivo protection、escape 和 PK | Duke、Nexelis、UTMB、Ragon、Texas、UNC、Wisconsin 文件 | 主要 assay 家族均有公开文件，但 4 个广告导出缺失 |
| 18 个 raw submitted data 下载入口 | 下载页列 18 项；14 个有效 XLSX，4 个 HTTP 500 | 部分取得，失败项持续跟踪 |
| COVIC-ID 与贡献方身份信息 | 当前 XLSX 只含盲化 label；论文称 40% 贡献方同意解除盲化 | 当前下载包未提供 identity/sequence mapping |
| 标准模板、受控词和自动 QC | 每个工作簿有 `Instructions`/`Terminology`；schema 与特殊值通过审计 | 当前公开表可复核；底层 QC 日志未公开 |
| Epitope community 可视化 | 补充图 2 指定 PDB `7DDD`；RCSB FASTA/mmCIF 已配对 | 有共享 Spike 框架；没有 row-level antibody structure mapping |
| 主论文与补充图 | Europe PMC JATS XML、OUP 补充 ZIP/Word | 已归档并核读 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-25；不阻塞 14 个已取得导出的 public-subset 发布）：下载页列出的 `Carterra - SPR`（assay 8）、`Carterra - BLI`（9）、`UTMB-ADE1`（16）和 `Nexelis - PK - RBD`（21）均返回 HTTP 500。2026-09-19 与 2026-09-25 两次检查结果相同，当前不保存错误页或虚构空文件；下一步用 `recheck_r64.py` 定期检查，任一端点恢复后创建新 snapshot、核验 schema/许可并补充，不覆盖本版本。
- `Q02`（最近更新：2026-09-25；影响完整研究数据和 sequence/structure 用途）：论文记载 40% 贡献方允许解除身份盲化，但当前 assay 下载不含贡献方原名称、完整重轻链序列或 COVIC-ID 映射。当前只把 label 当作盲化连接键，PDB 也仅保留共享可视化锚点；下一步等待 COVIC-DB 发布可下载且有明确公开授权的 identity/sequence 表，取得后核对 COVIC-ID、序列、结构和现有 14 个表的连接关系再关闭。
- `Q03`（最近更新：2026-09-25；影响精确重建和未来版本判定）：实时 XLSX 端点没有 release identifier、`ETag` 或 `Last-Modified`，且同一单元格内容会生成不同 ZIP 容器字节。当前以 2026-09-19 精确文件哈希冻结本版本，并以逐单元格比较监测语义变化；下一步等待维护方提供正式 release/version metadata，或在任何单元格、schema、端点集合变化时建立新的日期 snapshot 后关闭或更新本项。
