---
- tags:
  - context
---

# SRC_R74_ABDESIGN2 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [亲和力主表](#亲和力主表)
  - [成药性测量表](#成药性测量表)
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

- `source_id`：`SRC_R74_ABDESIGN2`
- `source_version`：`snapshot-2026-02-23`
- 原作者或发布机构：NaturalAntibody / `NATURALANTIBODY SPÓŁKA AKCYJNA`（Konrad Krawczyk 创办并主持研发）

### 来源方背景

NaturalAntibody 是专注抗体数据的波兰公司，业务是把抗体序列与结构的收集、生成和分析接入计算抗体工程。[公司介绍](https://naturalantibody.com/about-us/)把创始人写作 Konrad Krawczyk，并说明 Michał Krawczyk 同为创始人；该页面同时列出平台、抗体数据库族（含 AbDesign、AbDesign 2.0、Antigen Specific Antibody Database 等）和 LAP、CLAP、RIOT 等工具。Konrad Krawczyk 在页面上被描述为曾在 University of Oxford 构建计算抗体平台，并任 University of Southern Denmark 助理教授。

[波兰国家法院登记册当前摘录](https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/0000887528?rejestr=P&format=json)（本项目的 R03 接入于 2026-09-24 核验过该入口）显示现有法律主体 `NATURALANTIBODY SPÓŁKA AKCYJNA` 于 2021-03-08 登记，KRS 编号 `0000887528`，注册地在什切青并设克拉科夫分支。`S.A.` 是法律形式，不足以判断上市状态；本次核验没有取得能确认上市与否的一手披露，因此本 README 不作上市或未上市的表述。本次未重新取得公司成立时间与主要所在地的独立一手页面，[公司介绍](https://naturalantibody.com/about-us/)未载明成立日期与总部地址。

## 实验设计和数据口径

AbDesign 2.0 是单一抗体—抗原体系的深度突变扫描：亲本抗体为 pembrolizumab，靶点为 PD-1，参考复合物为 [5GGS](https://www.rcsb.org/structure/5GGS)。研究对象是重链上按位点穷举的单点替换，不是从抗原出发设计新抗体，也不是轻链或表位侧的变异。

公开材料给出的总体口径为 576 个独特重链单点突变、3,150 项生物物理表征和 346 个成功产出的抗体。当前 `affinity.csv` 的实际记录与之对应但不完全相等：576 条有名记录包含 1 条 `5GGS_WT` 和 575 条突变体，另有 2 条未计入 576 的 assay 对照行。因此“576 个突变”应理解为 `5GGS_WT` 加 575 个突变体这一包含亲本在内的工作集，`5GGS__…` 命名的纯突变记录是 575 条。README 以下涉及突变体的数字均按 575 计，并在需要时同时给出含 WT 的 576。

### 突变位点与替换集合

575 条记录的 `name` 统一采用 `5GGS__<重链ID>_<轻链ID>_<抗原链ID>__<WT残基>_<位点>_<新残基>` 的构造，例如 `5GGS__A_B_Z__A_T_28_M`。解析后得到 32 个突变位点，全部位于重链，位点为 28、30—34、50、52、54、55、57、59、60、63、72、76、77、84、85、87、93、98—108。

31 个位点各有 18 种替换，缺少的总是半胱氨酸；位点 28 为 17 种，除半胱氨酸外也不含丙氨酸。全部 575 条记录的 `WT残基` 字段与亲本重链序列 `heavy_sequence` 同一位点的残基逐一相符，未发现命名与序列冲突。把 575 条记录的 `heavy_sequence` 与 WT 行比较，每条恰有一处不同，说明这些行是单点替换而非组合突变。

公开数据中没有任何替换引入半胱氨酸，这与官方页面“位点穷举、除一个位点外无缺失突变”的表述方向一致：缺失发生在氨基酸选择层面，而不是位点层面。

### 结合测量与 KD 的来源

`affinity.csv` 的 `binding`、`kd`、`kon`、`koff`、`r2` 来自同一批动力学测量：`kon` 的单位量级（5.6×10⁴—6.8×10⁵）与 `koff`（1.05×10⁻⁴—6.26×10⁻²）相乘应得到 `kd`，实测 389 行中 332 行的 `kd × kon / koff` 落在 1±2%，384 行落在 1±20%，其余偏离最大到 11.2 倍。这说明三者出自同一次拟合，但公开表没有给出拟合模型、残差和置信区间；偏离的行不能据字段关系反推哪一层被四舍五入或另有来源，相关疑问见 `Q02`。

`binding` 是二值判定列，取值为 `1`、`0` 和空。当前状态是：467 条突变体为 `1`，98 条为 `0`，10 条为空；556 条非空判定的记录中，388 条突变体带 `kd`。全部 388 个突变体 KD 都出现在 `binding=1` 的行上，`binding=0` 的 98 行没有任何 KD 值。因此 `binding` 与“是否给出定量动力学结果”在当前公开表中高度一致，但公开材料没有说明这一判定是沿用实验侧的通过/不通过阈值，还是发布时按“是否拟合成功”回填。

10 条 `binding` 为空的记录全部没有 KD，且其中既有 `qc_hplc=1` 也有 `qc_hplc=0`，说明空判定不等于表达或纯度失败。

### 成药性测量的对象与覆盖

五个成药性表覆盖同一组 346 个成功产出的抗体（WT 加 345 个突变体），全部是 `affinity.csv` 的 576 条有名记录的子集，没有出现主表之外的名称。346 中 252 个同时带 KD，294 个 `binding=1`；未进入这 346 的 230 个突变体只有结合相关字段。

`nano_dsf.csv` 测量热稳定性，给出三个熔解温度 Tm1、Tm2、Tm3；`Tm1` 缺 17 行、`Tm3` 缺 20 行，`Tm2` 无缺失，说明三峰解卷积并不总能分出三个转变。`ac_sins.csv` 给出自相互作用倾向的 λmax 与 Δλ。`hydrophobicity.csv` 给出疏水性荧光计数与相对水的归一化值。`polyreactivity.csv` 给出对 BVP、Ovoalbumin、dsDNA、Heparin 四种非特异结合物的 OD 与归一化多反应性分数。

`polyreactivity.csv` 的行粒度是“抗体 × 抗原”，每个抗体 4 行，因此 346 × 4 = 1,384 行对应 346 个抗体，另有 24 行属于 6 个未命名的参考抗体。`total_polyreactivity_score` 在同一抗体的 4 行中取值相同，是跨抗原汇总后的单一分数，与逐抗原的 `mean_od` 不是同一层级；按行求均值会重复计入该总分。

五张成药性表还夹带未命名的参考抗体行，用于横向对照：`nano_dsf.csv` 有 Pembrolizumab IgG4；`ac_sins.csv` 有 Adalimumab、Ixekizumab；`hydrophobicity.csv` 有 Denosumab、Ixekizumab、Pembrolizumab IgG4；`polyreactivity.csv` 有 Adalimumab、Briakinumab、Emibetuzumab、Ixekizumab、Palivizumab、Pembrolizumab。这些行的 `name` 为空、抗体名写在各表首列，既不属于 576 条突变集，也不属于 346 条产出集，建模时应单独剔除。

### 您在评估这批数据前需要知道的三个计数

第一，`affinity.csv` 的 578 行由 576 条有名记录（1 WT + 575 突变体）和 2 条 assay 对照构成，后者的 `order_number` 列写的是 `Negative Control` 与 `Positive control`（阳性对照名称末尾带一个空格），没有 `name`。第二，`binding` 为空并不等于不结合，98 条 `binding=0` 同样不等于亲和力为零，公开表没有给出这类记录是否属于“未检出”或“未测”。第三，`expression_yield_final` 的最小值为 0，说明该列存在表达量为零的记录，而它们仍可能出现在结合表里；构建训练集时需要显式决定如何处理零产量行。

```text
公开对象（Drive 文件夹与 6 个 CSV）
576 条有名记录 = 1 条 5GGS_WT + 575 条单点突变（32 个重链位点）
    │
    ├─ affinity.csv           576 条 + 2 条 assay 对照 = 578 行
    │     ├─ binding=1        467 条突变体（含 388 条带 KD 的突变体）+ WT
    │     ├─ binding=0         98 条突变体，无 KD
    │     └─ binding 空        10 条突变体，无 KD
    │
    └─ 成功产出并做成药性表征的 346 条（WT + 345 突变体）
          ├─ production_summary.csv  346 行（每抗体 1 行）
          ├─ nano_dsf.csv            346 行 + 1 条参考抗体
          ├─ ac_sins.csv             346 行 + 2 条参考抗体
          ├─ hydrophobicity.csv      346 行 + 3 条参考抗体
          └─ polyreactivity.csv      346×4 行 + 6×4 条参考抗体行
```

## 论文原文

官方页面明确说明本数据集目前没有正式论文。截至 2026-10-29，`https://naturalantibody.com/ab-design2/` 写明 “There is no formal manuscript for AbDesign 2.0 yet.”，并建议引用网站本身：

- 标题：AbDesign 2.0: Exhaustive Mutational Mapping and Developability Database
- 作者：未署名
- 发表来源：无正式出版渠道；官方建议引用网站页面
- 归档文本版本：无
- 发布日期：无
- DOI：无
- PMID / PMCID：无
- 正文在线入口：<https://naturalantibody.com/abdesign2/>
- 本地归档：未归档
- 文本许可：不适用（无可归档文本）
- 补充材料：无

同一发布方的 AbDesign 1.0 有正式论文（mAbs 17(1):2567319，DOI `10.1080/19420862.2025.2567319`），但该论文对应的是 R03 的 14 个亲本复合物数据集，不是本来源的 pembrolizumab 单体系数据。两者不可互相替代解释；本 README 的方法口径只取自官方页面与落盘文件。官方页面所建议的引用文本与在线入口见“参考文献”。

## 仓库内容

上游通过 NaturalAntibody 官方页面的 Google Drive 文件夹交付，没有 release、record version 或版本号。`source_version` 的日期 `2026-02-23` 取自 Drive 六个 CSV 对象的 `Last-Modified` 响应头（全部为 `Mon, 23 Feb 2026 11:43:08 GMT`，`LICENSE.txt` 为 `Fri, 06 Feb 2026 09:18:02 GMT`），不是本次下载日期。Drive 对象可被原位替换，因此本 README 记录字节数与 SHA-256，快照名不应解释为上游正式版本号。

```text
snapshot-2026-02-23/
└── pd_1/
    ├── affinity.csv
    ├── production_summary.csv
    ├── nano_dsf.csv
    ├── ac_sins.csv
    ├── hydrophobicity.csv
    └── polyreactivity.csv
└── column_specs.json
└── LICENSE.txt
```

`pd_1/` 保留 Drive 子文件夹的真实名称，其中是六个 CSV。`column_specs.json` 是上游对原始 Excel 列名到标准化列名的映射说明，顶层只有 `affinity` 与 `developability` 两个表组，`developability` 下按 Production summary、nanoDSF、AC-SINS、Hydrophobicity、Polyreactivity 五个 sheet 分组。`LICENSE.txt` 是 CC BY-NC 4.0 全文。文件均按上游原始字节保存，未改名、未重新序列化。

## 数据结构

### 亲和力主表

`pd_1/affinity.csv` 有 578 行数据行、14 列。列依次为 `group`、`order`、`order_number`、`name`、`expression_yield_final`、`binding`、`qc_hplc`、`qc_sds_page`、`kd`、`kon`、`koff`、`r2`、`heavy_sequence`、`light_sequence`。

行由三部分构成：1 条 `5GGS_WT`、575 条 `5GGS__…` 突变体和 2 条 assay 对照。`order_number` 取 `1_1`…`1_576` 形式，突变行的编号与 `order` 一致；`group` 恒为 `1`，仅两条对照为空。所有突变行的 `light_sequence` 完全相同，与 `5GGS_WT` 一致：本数据集只变重链。`heavy_sequence` 是含 CH1 与铰链区、末尾带 `HHHHHH` 的重链片段，长度 232 aa，与 5GGS 的 polymer entity 1 序列逐字相同。

### 成药性测量表

五张表共享 `order_number`、`group`、`order`、`name` 四个标识列（`production_summary.csv` 列序略有不同，为 `order_number`、`group`、`order`、`name`），并以 `name` 与主表连接。各表最后一个共同特征是都附 `heavy_sequence`、`light_sequence` 两列，取值与主表一致，属于重复携带的标识信息而非独立测量。

| 文件 | 行数 | 列数 | 行粒度 | 额外参考抗体行 |
| --- | ---: | ---: | --- | ---: |
| `affinity.csv` | 578 | 14 | 抗体（含 2 条 assay 对照） | 0 |
| `production_summary.csv` | 346 | 14 | 抗体 | 0 |
| `nano_dsf.csv` | 347 | 12 | 抗体 | 1 |
| `ac_sins.csv` | 348 | 9 | 抗体 | 2 |
| `hydrophobicity.csv` | 349 | 9 | 抗体 | 3 |
| `polyreactivity.csv` | 1,408 | 11 | 抗体 × 抗原（每抗体 4 行） | 24（6 抗体 × 4 抗原） |

`production_summary.csv` 的 `mass_excof` 是分子量或消光系数的合并字段，取值 1,410—1,505，落在单一蛋白消光系数区间；公开材料未说明是哪一项或两值的组合，标为待确认。

### 字段说明

以下按文件覆盖实际表头的全部字段。CSV 中的数值、布尔和序列均以文本存储，数值列用空字符串表示缺失，`0` 不表示缺失但可能表示测量下限或失败，具体见各字段说明。

**`affinity.csv`（14 列）**

| 原始字段 | 表示、单位与来源 | 缺失与特殊编码 |
| --- | --- | --- |
| `group` | 实验批次组号，整数 | 两条 assay 对照为空 |
| `order` | 组内顺序号，整数 | 两条 assay 对照为空 |
| `order_number` | `<group>_<order>` 形式的对象编号 | 两条对照在此写 `Negative Control`、`Positive control` |
| `name` | 抗体标识；WT 为 `5GGS_WT`，突变为 `5GGS__A_B_Z__<WT>_<位点>_<新>` | 两条对照为空 |
| `expression_yield_final` | 表达产量，无量纲相对值，0—1.566 | 2 行缺失（即两条对照）；最小值为 0 |
| `binding` | 二值结合判定，`1`/`0` | 10 行缺失 |
| `qc_hplc` | SEC-HPLC 质控通过标记，`1`/`0` | 1 行缺失 |
| `qc_sds_page` | SDS-PAGE 质控通过标记，`1`/`0` | 566 行缺失，仅 12 行有值 |
| `kd` | 解离常数 KD，M，6.69×10⁻¹⁰—1.89×10⁻⁶ | 189 行缺失 |
| `kon` | 结合速率常数，M⁻¹s⁻¹，5.61×10⁴—6.85×10⁵ | 189 行缺失，与 `kd` 同步 |
| `koff` | 解离速率常数，s⁻¹，1.05×10⁻⁴—6.26×10⁻² | 189 行缺失，与 `kd` 同步 |
| `r2` | 拟合优度，无量纲，0.843—0.992 | 189 行缺失，与 `kd` 同步 |
| `heavy_sequence` | 重链氨基酸序列，232 aa | 两条对照为空；1 行首尾带空格 |
| `light_sequence` | 轻链氨基酸序列，218 aa 加尾部空格中 1 行共 219 字符 | 两条对照为空 |

`kd`、`kon`、`koff`、`r2` 四列的缺失行集合完全相同（同为 189 行），说明它们是同一次拟合的四个输出，不会单独缺失。`qc_sds_page` 只对 12 行有值且取值为 `0` 6 行、`1` 6 行，其余 566 行为空，与该列在其余行属于未测状态相符。

**`production_summary.csv`（14 列）**

| 原始字段 | 表示、单位与来源 | 缺失与特殊编码 |
| --- | --- | --- |
| `order_number`、`group`、`order`、`name` | 与主表同义的标识列 | 无缺失 |
| `pi` | 等电点，无量纲，7.92—8.45 | 无缺失 |
| `mass_excof` | 分子量或消光系数合并字段，1,410—1,505 | 无缺失；两项含义未在公开材料中拆分 |
| `akta_yield_1st_[mg]` | 首次 AKTA 纯化产量，mg | 无缺失 |
| `akta_yield_2nd_[mg]` | 二次 AKTA 纯化产量，mg | 无缺失 |
| `akta_yield_final_[mg]` | 最终纯化产量，mg，0.907—4.89 | 无缺失 |
| `qc_sec_hplc` | SEC-HPLC 质控，`1`/`0` | 无缺失 |
| `qc_sds_page` | SDS-PAGE 质控，`1`/`0` | 336 行缺失，10 行有值 |
| `qc_final` | 最终质控通过，全部为 `1` | 无缺失 |
| `heavy_sequence`、`light_sequence` | 与主表相同的序列副本 | 无缺失 |

`qc_final` 全部为 `1` 是筛选结果：本表只包含成功产出并进入成药性表征的 346 个抗体。

**`nano_dsf.csv`（12 列）**

| 原始字段 | 表示、单位与来源 | 缺失与特殊编码 |
| --- | --- | --- |
| `order_number`、`group`、`order`、`name` | 标识列 | 1 条参考抗体行 `name` 为空 |
| `tm1_[celsius]` | 第一熔解温度，°C，29.9—69.04 | 17 行缺失；最小值 29.9 显著低于全体中位数 65.05 |
| `tm1_std` | 第一熔解温度标准差 | 与 `tm1` 同步缺失 |
| `tm2_[celsius]` | 第二熔解温度，°C，63—76.92 | 无缺失 |
| `tm2_std` | 第二熔解温度标准差 | 无缺失 |
| `tm3_[celsius]` | 第三熔解温度，°C，77.06—91.51 | 20 行缺失 |
| `tm3_std` | 第三熔解温度标准差 | 与 `tm3` 同步缺失 |
| `heavy_sequence`、`light_sequence` | 序列副本 | 无缺失 |

`tm1` 的最小值 29.9 °C 与其余分布（中位 65.05 °C）差距悬殊，可能是解卷积把不完整转变拟合成了低值峰，也可能是真实去折叠温度；公开材料未给出判定规则，见 `Q03`。

**`ac_sins.csv`（9 列）**

| 原始字段 | 表示、单位与来源 | 缺失与特殊编码 |
| --- | --- | --- |
| `order_number`、`group`、`order`、`name` | 标识列 | 2 条参考抗体行 `name` 为空 |
| `lambda_max_[nm]` | 最大吸收波长，nm，530.5—549.5 | 无缺失 |
| `delta_lambda_[nm]` | 相对参考的波长位移，nm，−8.5—10.5 | 无缺失；负值表示蓝移 |
| `std` | 标准差 | 无缺失 |
| `heavy_sequence`、`light_sequence` | 序列副本 | 无缺失 |

`ac_sins.csv` 的 `std` 是单一标准差列，不与三列数值分别对应，需按测量对象理解为 Δλ 的标准差。

**`hydrophobicity.csv`（9 列）**

| 原始字段 | 表示、单位与来源 | 缺失与特殊编码 |
| --- | --- | --- |
| `order_number`、`group`、`order`、`name` | 标识列 | 3 条参考抗体行 `name` 为空 |
| `mean_value_afu_[counts]` | 疏水性荧光平均计数，AFU，6,124—35,460 | 无缺失 |
| `values_normalized_to_water` | 相对水的归一化值，无量纲，0.187—1.034 | 无缺失 |
| `std` | 标准差 | 无缺失 |
| `heavy_sequence`、`light_sequence` | 序列副本 | 无缺失 |

**`polyreactivity.csv`（11 列）**

| 原始字段 | 表示、单位与来源 | 缺失与特殊编码 |
| --- | --- | --- |
| `order_number`、`group`、`order`、`name` | 标识列 | 24 行（6 个参考抗体 × 4 抗原）`name` 为空 |
| `total_polyreactivity_score` | 跨四种抗原汇总的多反应性总分，2.785—71.89 | 无缺失；同一抗体的 4 行取值相同 |
| `antigen` | 非特异结合物名称 | 无缺失，见下方取值表 |
| `mean_od` | 平均光密度，4 次重复，0.01—1.2 | 无缺失 |
| `polyreactivity_score_normalized_to_adalimumab` | 相对 adalimumab 的归一化多反应性分数，0.416—34.71 | 无缺失 |
| `std` | 标准差 | 无缺失 |
| `heavy_sequence`、`light_sequence` | 序列副本 | 无缺失 |

**`antigen`（`polyreactivity.csv`；取值范围依据：当前 source version 观察）**

| 原始取值 | 含义 |
| --- | --- |
| `BVP` | 牛痘病毒蛋白（bovine viral protein）类包被抗原；上游未展开全称 |
| `Ovoalbumin` | 鸡卵清蛋白 |
| `dsDNA` | 双链 DNA |
| `Heparin` | 肝素 |

四个取值各出现 352 次，即 346 个抗体加 6 个参考抗体各测一次。

**`binding`（`affinity.csv`；取值范围依据：上游页面与当前版本观察）**

| 原始取值 | 当前记录数 | 含义 |
| --- | ---: | --- |
| `1` | 469 | 判为结合；其中 388 条带 KD |
| `0` | 99 | 判为不结合；均无 KD |
| （空） | 10 | 未给出判定；均无 KD |

**`qc_hplc`、`qc_sds_page`、`qc_sec_hplc`、`qc_final`（质控列；取值范围依据：当前版本观察）**

| 原始取值 | 含义 |
| --- | --- |
| `1` | 该项质控通过 |
| `0` | 该项质控未通过 |
| （空） | 该项未测或未记录 |

`binding`、质控列和 `name` 中的 `A`/`B`/`Z` 链 ID 均为来源定义的标识或判定值。`name` 本身不是枚举字段，包含 576 个不同取值，应作为连接键处理；其内部构造规则见“突变位点与替换集合”。

### 数据示例

`affinity.csv` 中一条带 KD 的突变记录：

```text
group=1,order=10,order_number=1_10,name=5GGS__A_B_Z__A_T_28_M
expression_yield_final=0.441,binding=1,qc_hplc=1,qc_sds_page=
kd=9.2754247433018e-09,kon=239229.589827924,koff=0.00221414192797851,r2=0.98394586906725
```

这是亲本重链第 28 位苏氨酸换成甲硫氨酸的单点突变体，`kd × kon / koff` 为 9.28×10⁻⁹ × 2.39×10⁵ / 2.21×10⁻³ ≈ 1.002，与表中 KD 自洽。它代表一个实验对象的一次测量，不是一次重复实验。

`affinity.csv` 中一条无 KD 的非结合记录：

```text
group=1,order=349,order_number=1_349,name=5GGS__A_B_Z__A_Q_87_P
expression_yield_final=0.038,binding=,qc_hplc=0,kd=,kon=,koff=,r2=
```

它同时具有低产量与 HPLC 质控未通过，`binding` 为空。这类记录既不能当作 confirmed non-binder，也不能直接删除而不说明。

`polyreactivity.csv` 中同一抗体的四行：

```text
order_number=1_1,name=5GGS_WT,total_polyreactivity_score=5.229,antigen=BVP,mean_od=0.117
order_number=1_1,name=5GGS_WT,total_polyreactivity_score=5.229,antigen=Ovoalbumin,mean_od=0.018
order_number=1_1,name=5GGS_WT,total_polyreactivity_score=5.229,antigen=dsDNA,mean_od=0.022
order_number=1_1,name=5GGS_WT,total_polyreactivity_score=5.229,antigen=Heparin,mean_od=0.021
```

四行是同一亲本抗体的四种非特异结合物测量，属同一实验对象的不同测定，不是四个独立样本；`total_polyreactivity_score` 在四行重复，只应计一次。

## PDB 数据库

本来源的每一条记录都指向同一个参考复合物：pembrolizumab Fab 与 PD-1 的晶体结构 [5GGS](https://www.rcsb.org/structure/5GGS)。映射强度是“共享参考复合物”：576 条记录通过 `name` 前缀 `5GGS` 与主表 `heavy_sequence`、`light_sequence` 连接到该条目，但没有任何一条突变体有实验测定的结构；官方页面对成药性表征的抗体给出的是实验生物物理测量，对结合结构只指向该亲本复合物。

链角色由主表的 `name` 字段直接给出，不需要额外推断：`5GGS__A_B_Z__…` 中的 `A`、`B`、`Z` 分别标注重链、轻链与抗原链。项目据此从 RCSB 取得 entry 级 FASTA 与完整 mmCIF，并核对三条 canonical 序列与主表 `5GGS_WT` 行逐字相符：重链 232 aa（entity `5GGS_1`，author chain A/C）、轻链 218 aa（entity `5GGS_2`，author chain B/D）、抗原 PD-1 123 aa（entity `5GGS_3`，author chain E/F）。轻链在主表中多出 1 个尾部空格，去除空格后与 entity 序列一致。

`pdb/` 共 2 个文件、1.64 MiB（1,722,542 bytes）：`sequences/rcsb_pdb_5GGS.fasta` 与 `structures/5GGS.cif`。FASTA 是 RCSB 的 entry 级原始下载，未做选链或重建；mmCIF 是 RCSB 完整坐标。按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接后的 inventory SHA-256 为 `8bb35ce5482ed670d0852dc79f41767c27739041aa1a466868acac6d9fad635f`。未发布独立 PDB manifest。

| 文件 | 大小 | SHA-256 |
| --- | ---: | --- |
| `pdb/sequences/rcsb_pdb_5GGS.fasta` | 768 bytes | `3cc41ab99e5096f3bc021520c1ec72cdd022cf948336b17011fa2fbaee4d2e76` |
| `pdb/structures/5GGS.cif` | 1.64 MiB（1,721,774 bytes） | `9fa3febc15076e0893bbe9c4750794a301158ac8291daa30a0de85da094c642f` |

这条补充不提供任何突变体的结构。5GGS 是亲本 Fab 的晶体结构，576 条记录中的 575 个单点突变体只有序列与测量值；把它们当作“有实验结构”的样本会高估结构覆盖。若下游需要突变体结构，只能使用计算建模结果，并应在 processed 层明确标注其派生性质。

## 采集过程记录

- 2026-10-28 在本地 Windows 环境通过 FlClash HTTP 代理 `127.0.0.1:7892` 访问上游。项目当前没有 `project.toml` 与 `developer.local.toml`，也没有 `workspace/` 目录，因此本来源的存储根按用户指定使用 `G:\abag-datasets`，README 直接写在该 source version 目录，未按 skill 的 `workspace/users/<user>/docs/readme/` 路径生成草稿。该偏差已向用户说明并获准，属本次接入的实际执行方式。
- 2026-10-28 先取得 Drive 文件夹页面的实时对象列表。文件夹 `1bvIUWkoH7RhamxuJjPGtIfodAXV_40U4` 下有 1 个共享子文件夹 `pd_1`、`column_specs.json` 与 `LICENSE.txt`。`pd_1` 内有 6 个 CSV。
- 2026-10-28 用 `https://drive.google.com/uc?id=<file-id>` 逐文件下载。`affinity.csv` 与 `nano_dsf.csv` 首次以 `export=download` 形式请求时分别返回 HTTP 000 与 303，改用不带 `export` 的 `uc?id=` 端点后均返回 200，字节数与预期一致；失败响应未落盘，也未覆盖任何已有文件。
- 2026-10-28 逐文件记录 `Content-Disposition` 与 `Last-Modified` 响应头，六个 CSV 的 `Last-Modified` 同为 `2026-02-23 11:43:08 GMT`，`LICENSE.txt` 为 `2026-02-06 09:18:02 GMT`，`source_version` 由此定为 `snapshot-2026-02-23`。
- 2026-10-29 独立验收：按字节数与 SHA-256 固定 8 个 payload 文件；解析 6 个 CSV 确认列数、行数与表头；核对 576 条有名记录与 2 条 assay 对照；解析 575 条突变名称并与亲本重链逐位点比对；核对 KD、kon、koff、r2 四列的缺失行集合一致；核对五张成药性表的 346 条抗体全部是主表子集。
- 2026-10-29 按 skill 的 PDB 硬性要求审计锚点。主表 `name` 字段直接标注链角色，据此从 RCSB 取得 5GGS 的 entry FASTA 与完整 mmCIF，并核对三条 canonical 序列与主表 `5GGS_WT` 一致。`heavy_sequence` 与 entity 1 逐字相同，`light_sequence` 去尾部空格后与 entity 2 逐字相同。
- 2026-10-29 官方页面明确“尚无正式论文”，因此本来源不归档论文 PDF。AbDesign 1.0 的 mAbs 论文属于 R03，未混入本目录。
- 2026-10-29 发现 `kd × kon / koff` 在 389 行中有 57 行偏离 1 超过 2%（最大 11.2 倍）。该现象只在验收中记录，未修改任何原始数值，转入 `Q02` 跟踪。

## 参考文献

- AbDesign 2.0 官方页面：<https://naturalantibody.com/ab-design2/>
- AbDesign 2.0 数据集页：<https://naturalantibody.com/abdesign2/>
- 上游 Google Drive 文件夹：<https://drive.google.com/drive/folders/1bvIUWkoH7RhamxuJjPGtIfodAXV_40U4>
- 官方建议引用：*AbDesign 2.0: Exhaustive Mutational Mapping and Developability Database*，<https://naturalantibody.com/abdesign2>
- 参考复合物：RCSB PDB [5GGS](https://www.rcsb.org/structure/5GGS)，PD-1 与 pembrolizumab Fab 复合物；原始结构论文见该条目页 Primary Citation
- 同发布方的 AbDesign 1.0（另一数据集，不解释本来源）：Janusz et al., *mAbs* 17(1):2567319，DOI `10.1080/19420862.2025.2567319`
- NaturalAntibody 公司介绍：<https://naturalantibody.com/about-us/>
- 波兰国家法院登记册：<https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/0000887528?rejestr=P&format=json>

## 其他

### 数据范围和限制

本来源是单一抗体、单一位点集的重链深度突变扫描，只覆盖 pembrolizumab 的重链可变区与部分框架位点，轻链在所有记录中恒定。它不提供跨抗原、跨抗体家族的比较能力，也不覆盖表位侧的抗原突变。用它评估“通用亲和力预测”时，同一亲本的 575 个突变体彼此高度相关，随机按行拆分会把近重复结构分散到训练与测试两侧。

346 条成药性记录是成功产出的子集，不是随机子集；用它们估计全部 575 个突变体的成药性分布会有幸存者偏差。

### 完整性与验收

| 文件 | 大小 | SHA-256 |
| --- | ---: | --- |
| `LICENSE.txt` | 18.89 KiB（19,346 bytes） | `3711f963c05d0be80d53e5923308a6dee31b203da23435c9cfb7c7b6e4dd5e19` |
| `column_specs.json` | 9.13 KiB（9,352 bytes） | `bdc842580a0dab3d32b927284eeec31849b27f6e7c7d88688c7663879d07949e` |
| `pd_1/affinity.csv` | 308.96 KiB（316,375 bytes） | `800740bab0827cafad611fb0e24dc2140819ad9b7e04c17f82188180e7079ef4` |
| `pd_1/production_summary.csv` | 175.01 KiB（179,214 bytes） | `788a01df4b78eb2f0d0745dbdc93a65b18d679d1489fcc8b748f20e2d89b4907` |
| `pd_1/nano_dsf.csv` | 198.89 KiB（203,660 bytes） | `0f2c21ce21ec32a65712c20ca0534da689aa1fab03092d59560088e482064a32` |
| `pd_1/ac_sins.csv` | 169.40 KiB（173,463 bytes） | `d1736b54f5fb6abd86c15f84f6153bea097908e03fd0cd758efafcf76eefe090` |
| `pd_1/hydrophobicity.csv` | 179.63 KiB（183,943 bytes） | `14ba9648935dce3b3258faa59d5b0dabe289466ca52a5bb8abbf1bbb796ec9ee` |
| `pd_1/polyreactivity.csv` | 700.95 KiB（717,772 bytes） | `e53d38bcdf62f325b1efe25ea52b271a508bf76ae86200d936a396b43a1f72a1` |

上游未提供官方 checksum，上表 SHA-256 为本次下载后本地计算，用于后续复核同一份字节，不代表上游签名。八个 payload 文件的格式可读性、表头完整性与行数均已独立核实；`pdb/` 的完整性与逐文件摘要见“PDB 数据库”。

### 许可和再分发边界

`LICENSE.txt` 是 Creative Commons Attribution-NonCommercial 4.0 International 全文。官方页面写明该数据库“free for non-commercial use by non-commercial entities”，商业实体应联系 NaturalAntibody。据此，本包在非商业实体内部研究范围内可用；商用、对外再分发和衍生发布不在当前已取得的授权范围内。

PDB 文件来自 RCSB，使用时应保留 5GGS 的原始结构引用，适用 RCSB 自身的条款。

### 公开范围对照

| 官方页面声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 576 个独特重链单点突变 | `affinity.csv` 576 条有名记录 = 1 WT + 575 突变体 | 部分包含：突变体为 575，与“576 个突变”的表述差 1 |
| 3,150 项生物物理表征 | 6 张表合计 3,595 行（含参考抗体与多抗原展开） | 待确认：官方未给出口径，无法与行数直接对齐 |
| 346 个成功产出的抗体 | 五张成药性表各覆盖 346 个抗体 | 已包含 |
| 完整动力学 KD/kon/koff | 389 行带四元组（388 突变体 + WT） | 已包含；拟合模型与误差未公开 |
| nanoDSF 热稳定性 | `nano_dsf.csv` 的 Tm1—Tm3 | 已包含 |
| 疏水性归一化值 | `hydrophobicity.csv` | 已包含 |
| AC-SINS 聚集倾向 | `ac_sins.csv` | 已包含 |
| 对 BVP、Ovoalbumin、dsDNA、Heparin 的多反应性总分 | `polyreactivity.csv` | 已包含 |
| 突变体实验结构 | 未发现；官方只指向亲本 5GGS | 未公开 |
| 逐孔原始读数、曲线、拟合参数与重复数 | 未发现 | 未公开 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-29；待上游澄清计数口径）：官方页面写“576 unique point mutations”，当前 `affinity.csv` 的 576 条有名记录包含 1 条 `5GGS_WT` 与 575 条突变体，纯突变记录为 575。已核实名称解析、位点分布与重链逐位点比对均自洽，575 条记录每条恰有一处替换；差异只可能来自 WT 是否计入。影响：任何以“576”为分母的比例推算都需要明确分母。当前处理：README 同时给出 575 与 576 两个口径并按突变体计。下一步：取得上游口径说明，或核对 `column_specs.json` 之外的发布说明后关闭。
- `Q02`（最近更新：2026-10-29；待方法细节）：389 行同时具备 `kd`、`kon`、`koff` 与 `r2`，其中 332 行的 `kd × kon / koff` 在 1±2%，384 行在 1±20%，最大偏离 11.2 倍。已核实四列缺失行集合完全一致，同属一次拟合输出；未找到拟合模型、加权方式或数值取整规则。影响：偏离较大的行不能据字段关系复算 KD，也不能判断是 KD 由独立拟合给出还是三参数联合拟合。当前处理：原始数值保持不变，不做换算或修正。下一步：向发布方确认 KD 是否由 `koff / kon` 派生以及有效数字处理规则。
- `Q03`（最近更新：2026-10-29；待方法细节）：`nano_dsf.csv` 的 `tm1_[celsius]` 最小值 29.9 °C 远低于中位数 65.05 °C，另有 17 行缺失 `tm1`、20 行缺失 `tm3`。已核实缺失成对出现（数值与标准差同步缺失），`tm2` 无缺失。影响：三峰解卷积失败或低值峰是否应视为无效，直接决定热稳定性标签的可用行数与阈值。当前处理：保留全部原始值，不设阈值剔除。下一步：确认解读卷积判定规则，或在 processed 层按缺失与分布另行定义过滤规则。
- `Q04`（最近更新：2026-10-29；待字段定义）：`production_summary.csv` 的 `mass_excof` 取值 1,410—1,505，量级符合单克隆抗体消光系数，但字段名把分子量与消光系数并列。已核实该列无缺失且取值集中，未见与 `pi` 或产量的关联线索。影响：若它是消光系数则可用于浓度换算，若含分子量则不能直接作单一标量使用。当前处理：在字段说明中标为合并字段，不参与任何换算。下一步：取得上游列定义或原始 Excel 表头后拆分。
- `Q05`（最近更新：2026-10-29；待上游说明）：`affinity.csv` 的 2 条 assay 对照行（`Negative Control`、`Positive control`）没有 `name`、`group` 与 `order`，`order_number` 列被写入对照名称（阳性对照名称末尾带一个空格），且阳性对照自带 KD 与 kon/koff。已核实它们不计入 576 条有名记录，也不在成药性表出现。影响：按 `name` 连接的流程会自动忽略它们，但按行读取的流程可能误把对照当成突变体。当前处理：README 明确标注，字段说明列出其特殊编码。下一步：确认是否需要为这类行建立独立标识。
- `Q06`（最近更新：2026-10-29；待上游说明）：五张成药性表混入 13 个未命名参考抗体条目（去重后为 Adalimumab、Briakinumab、Emibetuzumab、Ixekizumab、Palivizumab、Pembrolizumab/Pembrolizumab IgG4、Denosumab 共 7 个不同抗体名），其 `name` 为空、抗体名写在各表首列。已核实它们不属于 576 条突变集，也不在 346 条产出集。影响：按 `name` 过滤可自动剔除，但直接统计行数会把这些对照计入。当前处理：README 逐表列出其数量与身份。下一步：确认这些参考抗体是否应作为对照纳入下游分析。
- `Q07`（最近更新：2026-10-29；信息缺口）：官方页面所列 3,150 项表征与落盘 6 张表的行数关系没有公开口径。已核实各表的行粒度（抗体级、抗体 × 抗原级）与主要计数，但无法把“3,150”分解到具体测量类型。影响：无法用官方总量校验本包是否有缺表或缺行。当前处理：在公开范围对照中标为待确认。下一步：取得上游统计口径说明后重新对齐。
