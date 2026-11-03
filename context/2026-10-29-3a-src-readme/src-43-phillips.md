# SRC_R43_PHILLIPS 数据说明

- [数据集身份](#数据集身份)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [Genotype、测量与派生层](#genotype测量与派生层)
  - [文件层级和连接边界](#文件层级和连接边界)
  - [出版方 v3 与固定仓库对照](#出版方-v3-与固定仓库对照)
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

## 数据集身份

- `source_id`：`SRC_R43_PHILLIPS`
- `source_version`：`snapshot-2021-09-22`
- 原作者或发布机构：Angela M. Phillips、Katherine R. Lawrence 等；Michael M. Desai 课题组

## 实验设计和数据口径

用 Tite-Seq 测定两个广谱流感抗体 CR6261 与 CR9114 的组合完备重链成熟轨迹。CR6261 选择 11 个重链位点，理论上 2^11=2,048 个 germline/somatic 组合，分别对 H1、H9 HA 测量；CR9114 选择 16 个位点，2^16=65,536 个组合，分别对 H1、H3 与 influenza B HA 测量。抗体以 scFv 在酵母表面展示，在多个抗原浓度下按流式荧光 bin 分选，通过 barcode/变体测序频数推断滴定曲线；三次 biological replicates 后汇总 mean 与 SEM。数据包含组合 library，行间由共享位点、亲本、replicate、抗原和处理层高度相关。

论文 Figure 1 source 与固定仓库的完整 landscape 表分别含 CR6261 2,048、CR9114 65,536 个唯一二进制 genotype，长度 11/16。0/1 表示对应位点的 germline/somatic 状态，不是氨基酸字母；mutation_* 与论文 alignment 才定义位点替换。CR6261 filtered mean-bin 合并表保留 1,917 个 genotype；H1/H9 mean 分别缺 30/75，值域 7.0–9.7286 和 7.0–10.1500。CR9114 mean-bin 合并表保留全 65,536 个 genotype；H1/H3/fluB mean 分别缺 442/1/2，值域 7.0–9.8345、6.0–9.0419、6.0–8.0608。不能将 filtered 与 unfiltered、replicate、figure source、回归派生表相加成独立抗体。

mean-bin 表的 mean 是 −log10(KD[M])，越大亲和力越强；H1/H9 滴定窗口为 10⁻¹²–10⁻⁷ M，因此边界 pKD 为 12/7；H3/fluB 为 10⁻¹¹–10⁻⁶ M，边界 pKD 为 11/6。论文明确超出窗口的推断值钉在边界，所以等于 7/6 等边界值不是精确弱亲和力。CR9114 maximum-likelihood 表 h*_mean 保留代码内部 ln(KD[M]) 的负值（例如 −7 到约 −21.7），不是与 mean-bin pKD 同量纲；不能只换符号，需按自然对数与十进制对数换算并保留推断方法。ML 的 SEM 也属于该参数化。图表、线性模型系数、force-directed coordinates、路径概率均是相同实验数据的派生表示。底层 SRA PRJNA741613 不在本次固定 Git tree 中。

## 论文原文

- 标题：Binding affinity landscapes constrain the evolution of broadly neutralizing anti-influenza antibodies
- 作者：Angela M. Phillips, Katherine R. Lawrence et al.
- 载体与版本：eLife 10:e71393，2021-11-03 Version of Record v3；首次发布日期 2021-09-07，与仓库 commit 日期分开记录
- 发布日期：2021-11-03
- DOI：`10.7554/eLife.71393`
- PMID / PMCID：34491198 / PMC8476123
- 本地文件：`articles/Phillips_2021-11-03_eLife-v3.pdf`；`articles/Phillips_2021-11-03_eLife-v3.xml`
- 文件大小：articles/Phillips_2021-11-03_eLife-v3.pdf = 7852160 bytes；articles/Phillips_2021-11-03_eLife-v3.xml = 439553 bytes
- SHA-256：articles/Phillips_2021-11-03_eLife-v3.pdf = `a85dfc9f3b11b1e8c7f5e035b8e689c6b858397a052f726c1307282e32d73957`；articles/Phillips_2021-11-03_eLife-v3.xml = `e3992f783df803aab922ddae299eb0dfea42c0bb57f44b4d135f5009b5b61935`
- 文本许可：CC BY 4.0
- 补充材料：8 个公开附件，详见下表

| 文件 | 角色 | bytes | SHA-256 |
| --- | --- | --- | --- |
| articles/Phillips_2021-11-03_eLife-v3-fig1-data1.csv | 出版方 figure source data fig1-data1.csv | 12258680 | `ee31f8fc26fce2730d2ae772e7a095aa334b4c6c5d8e7fbfe4b4a5a1c9a794fe` |
| articles/Phillips_2021-11-03_eLife-v3-fig1-data2.csv | 出版方 figure source data fig1-data2.csv | 358244 | `6acc7dc8352d694db5f3aedb36e8c4216f61d400b4d85828c056f08580e9c61e` |
| articles/Phillips_2021-11-03_eLife-v3-fig1-data3.xlsx | 出版方 figure source data fig1-data3.xlsx | 16969 | `02e6adff1002098cf5de2e05bd49a3b9f67a086b9b88ece0dd85b9767cd0e995` |
| articles/Phillips_2021-11-03_eLife-v3-fig2-data1.csv | 出版方 figure source data fig2-data1.csv | 1053782 | `9bc91e5515e297af73edc34f17ec60d99ad82d1a83b5944657001e092bde7e76` |
| articles/Phillips_2021-11-03_eLife-v3-fig2-data2.csv | 出版方 figure source data fig2-data2.csv | 140833 | `1d7289172fe5a6cacd0de80a047121756111cae774f75f349a5371ef90039999` |
| articles/Phillips_2021-11-03_eLife-v3-fig2-data3.xlsx | 出版方 figure source data fig2-data3.xlsx | 30573 | `90a9a58a911520b879b95883a6b8325217a8bc78c0b0f4fb87d383594b94fe4a` |
| articles/Phillips_2021-11-03_eLife-v3-fig5-data1.csv | 出版方 figure source data fig5-data1.csv | 115132 | `6f03c9c06616a8dc07d5ad4edcfcceba89dc36015337f1fd9c6725ae8e1e7333` |
| articles/Phillips_2021-11-03_eLife-v3-fig5-data2.csv | 出版方 figure source data fig5-data2.csv | 3831 | `9a15ba8b120fe23f14046a80358a326e4e6740485686f02940238fda06e115fd` |

正式 v3 PDF、当前 DOI 对应 PMC XML和八个 publisher figure source data 全部归档。PDF/figure sources 由明确 v3 CDN 文件名确认；当前 PMC XML 作为 DOI 全文保存，不假定其 bytes 与某一历史 XML 快照相同。论文与附件 CC BY 4.0。

## 仓库内容

上游固定版本：[一手入口](https://github.com/klawrence26/bnab-landscapes/tree/514d62f387070f43b8a172f02e60c70137f8a8b8)。revision/commit `514d62f387070f43b8a172f02e60c70137f8a8b8`，上游版本日期 `2021-09-22T10:53:53Z`；据此命名 `snapshot-2021-09-22`，日期不是本次下载日期。

固定 commit 的完整 3,862-file tree，逐个从 raw.githubusercontent.com 续传并验证官方 Git blob SHA-1。recursive tree 的 10,186,669,438 bytes 包含七个 Git LFS pointer；按 pointer OID 从 media.githubusercontent.com 取得 464,751,893 bytes 实际对象，同时验证 pointer blob SHA-1、pointer SHA-256、OID SHA-256 和声明大小。解析后的 raw payload 合计 10,651,420,405 bytes；不重打包、不只选择结果表。codeload 整包和浅克隆失败后没有用部分归档冒充完整 tree。

```text
snapshot-2021-09-22/
├── .DS_Store
├── .gitattributes
├── LICENSE
├── README.md
├── CR6261/
│   ├── Epistasis_linear_models/
│   ├── Expression_meanbin/
│   ├── Isogenic_validation/
│   ├── Kd_maxlikelihood/
│   ├── Kd_meanbin/
│   └── Raw_data/
├── CR9114/
│   ├── Epistasis_linear_models/
│   ├── Expression_meanbin/
│   ├── Isogenic_validation/
│   ├── Kd_maxlikelihood/
│   ├── Kd_meanbin/
│   ├── Raw_data/
│   └── Seq_pipeline/
└── Figures/
    ├── Appendix2/
    └── Figure1/ … Figure5/
```

CR6261 1,391 files、CR9114 2,101 files、Figures 366 files，另有四个根文件。七个 LFS 路径已替换为 OID 对应实际内容，README 的 payload bytes 按实际落盘对象计。目录同时含 flow events、sequencing counts、拟合中间表、validation、notebooks、模型及图件；完整保留不代表各层都能作为监督样本。

## 数据结构

### Genotype、测量与派生层

主 genotype key 为长度 11 或 16 的二进制字符串，按亲本定义的成熟位点编码；CR6261 表多用 variant，CR9114 ML 表用 sequence，同值域但字段名不统一。repa/repb/repc 与 repx/repy/repz 是不同抗原的三次 biological replicate；mean/sem 是汇总，不应同时把 replicate 和 mean 当独立标签。pos*、som_mut、mutation_* 是位点/突变数/描述，variant_int 是编码派生整数；fdl_x/y 是图布局坐标，绝非生物物理标签。

### 文件层级和连接边界

Raw_data 保存分选/测序的底层表，Kd_meanbin 和 Kd_maxlikelihood 保存不同方法/参数化的拟合层，Expression_meanbin 是表达估计，Isogenic_validation 为选定克隆验证，Epistasis_linear_models 与 Figures 为后验建模/呈现。文件名中的 adj/unadj、fil/unfilt、keepall、merg、avg、all 和 ML 表示处理分支，不能依路径相邻推断行独立。以 antibody、antigen、genotype、replicate、inference method 和 processing branch 组成分析键；同一 genotype 多文件出现是重复表示。

### 出版方 v3 与固定仓库对照

eLife v3 Figure 1 source data 1/2 与仓库 CR9114/CR6261 mean-bin filtered merged 表逐行比较：数据行 bytes 与顺序全部相同，分别为 65,536/1,917 行；差异只在 header 命名。出版方把 genotype 键写作 genotype，并给 replicate 加 h1_/h3_/fluB_/h9_ 前缀；仓库用 variant 及 repa/repx 等上下文相关名。读取时应使用各文件自己的 header，不应因数值行相同就把两个文件计作独立实验。

### 字段说明

| 文件或表 | 原始字段 | 类型/单位/方向 | 缺失、边界及来源 |
| --- | --- | --- | --- |
| Figure1 / Kd_meanbin | variant / sequence | 11/16 位二进制 genotype key | 0/1 是 germline/somatic 状态；不是 AA；CR6261/CR9114 不能仅凭相同 bit string 连接 |
| Figure1 / Kd_meanbin | rep[a-c] / rep[x-z] | 三次 biological replicate 的 −log10(KD[M]) | 抗原映射依具体表头；缺失/边界不得填作零 |
| Kd_meanbin | h1_mean / h9_mean / h3_mean / fluB_mean | 平均 pKD，越高越强 | H1/H9 弱端 7，H3/fluB 弱端 6；窗口边界不是精确值 |
| Kd_meanbin | h\*_sem / fluB_sem | 三次 replicate 的标准误，pKD 单位 | 0 可来自三条都钉边界，不表示无实验误差 |
| Kd_maxlikelihood | h1_mean / h3_mean / fluB_mean | ML 内部 ln(KD[M])，更负表示更强 | 不能与 pKD 直接拼接；缺失数和值域与 mean-bin 不同 |
| landscape / Figure tables | variant_int / pos\* / som_mut / mutation_\* | 编码整数、位点状态、成熟突变数和替换描述 | 连接/解释字段；不能作为纯序列模型的无泄漏输入时应事先定义任务 |
| Figures/Figure1 | H1_log10Kd / H3_log10Kd / H9_log10Kd / FluB_log10Kd | 论文 figure source 的 pKD 表示 | 列名含 log10Kd 但论文图注定义 −logKD；需以方法/值域解释 |
| Figures/Figure1 | fdl_x / fdl_y | force-directed graph 布局坐标 | 从 genotype/affinity 派生，存在后验标签泄漏 |
| Expression / validation / regression | 表达、isogenic affinity、coefficient/prediction 字段 | 独立验证或同一测量的派生层 | 只在读取对应 schema 后使用；不按文件数量计新抗体 |

### 数据示例

来自 `bnab-landscapes/Figures/Figure1/20210504_fdl_6261.csv` 的第一条真实记录（仅摘录下列列）：

```json
{
  "variant": "00000000000",
  "H1_log10Kd": "7.0",
  "H9_log10Kd": "7.0",
  "som_mut": "0.0"
}
```

该真实记录来自论文 CR6261 landscape；variant 是 11-bit genotype。H1/H9 数值是 pKD 表示，不能当 nM，fdl 坐标没有纳入示例。

## PDB 数据库

论文 Figure 2 的结构分析与引用提供亲本级强证据。接受 CR6261–H1→3GBN；CR9114–H5→4FQI、CR9114–H3→4FQY。3GBN 直接覆盖 CR6261/H1；4FQY 直接覆盖 CR9114/H3；论文说明缺少 CR9114/H1 结构并用可用 CR9114/H5 结构分析共享表位，因此 4FQI 是明确代理，不是 H1 exact structure。无逐 genotype PDB 键，三者均由全部相关变体共享。

取得日期：2026-09-18。每个唯一 entry 保留完整 RCSB canonical entity FASTA 与完整沉积坐标，不选择性截断、不拼接设计序列。实体/链从 mmCIF `_entity` / `_entity_poly` 核对；canonical 序列与 FASTA entity 一致，坐标 `_entry.id` 与 PDB ID 一致，原子记录非空。

| PDB | 连接关系及证据 | polymer entity / author chains /长度 | FASTA/mmCIF |
| --- | --- | --- | --- |
| 3GBN | CR6261-H1 共享亲本参考；主文 Structural analysis 明确 PDB ID | 1:A:331aa；2:B:179aa；3:H:226aa；4:L:221aa | 两层 verified |
| 4FQI | CR9114-H5 共享参考；研究 H1 用其代理，不能称 H1 复合物；主文 Structural analysis 明确 H5/H1 的映射边界 | 1:A:334aa；2:B:177aa；3:H:230aa；4:L:216aa | 两层 verified |
| 4FQY | CR9114-H3 共享亲本参考；主文 Structural analysis 明确 PDB ID | 1:A:323aa；2:B:174aa；3:H:224aa；4:L:216aa | 两层 verified |

| 文件 | bytes | SHA-256 |
| --- | --- | --- |
| pdb/sequences/rcsb_pdb_3GBN.fasta | 1264 | `69e686f7933b2e04e3d94f75a6aa875a7ed01a96f062107b9352c2732b3f21fc` |
| pdb/structures/3GBN.cif.gz | 193315 | `1599b5fe02692d655bc79afdab02c218a66605005b626c08e262587c1cfb8f6d` |
| pdb/sequences/rcsb_pdb_4FQI.fasta | 1227 | `5b8ff6a0c9105190397118bcb3dde505f0f85015248f78014739a4c88a344cb4` |
| pdb/structures/4FQI.cif | 936682 | `b437010518bc4ced413aa08bf21f965855a9704164e10b8bc0a7ef0084f60c8f` |
| pdb/sequences/rcsb_pdb_4FQY.fasta | 1207 | `53091848b13fad9d0c30190f8dade5ae6d21d7d0b9b873abfd15dbcff1ae02fa` |
| pdb/structures/4FQY.cif.gz | 390612 | `5ddaa5d3b45e791252972317f4dd23c58c71fbc3fdcd633cbd959938b7f848b1` |

共 3 个有效锚点、3 个 FASTA、3 个 mmCIF，1524307 bytes。每个下载使用 `https://www.rcsb.org/fasta/entry/<PDB_ID>/download` 与 `https://files.rcsb.org/download/<PDB_ID>.cif`；共享已存 gzip 坐标直接原样复用，未重压缩。完整 entry 可含未参与该研究的抗体/实体；链身份与映射边界按上表及下文使用。

3GBN entity 3 author H 为 CR6261 heavy、entity 4 L 为 light，HA1/HA2 为 A/B；4FQI entity 3 H、entity 4 L 为 CR9114，HA1/HA2 为 A/B；4FQY 同样为 CR9114 H/L 与 H3 HA A/B。实验 landscape 只组合重链成熟位点且以 scFv 展示；完整 PDB entry 中轻链/HA/其它坐标不等于每个 variant 的 exact construct。禁止将 bit genotype 嫁接到坐标生成 raw 伪结构。

## 使用方式

```python
from pathlib import Path
import csv
root = Path(dataset_root)
path = root / 'bnab-landscapes' / 'Figures' / 'Figure1' / '20210504_fdl_6261.csv'
with path.open(newline='') as f:
    rows = list(csv.DictReader(f))
```

按 antibody、antigen、method 和 genotype 分组；pKD 与 ML ln(KD[M]) 分开解析。

## 采集过程记录

2026-09-18 至 2026-09-19：由 GitHub API 固定 2021-09-22 commit 并读取 recursive tree。codeload 多次超时且不能可靠 Range 续传，浅 clone 也未完成；终止旧进程并保留失败诊断后，按 3,862 个官方 tree blob 并发续传。每个普通文件以 Git blob SHA-1 验证；首次全表审计检出七个未解析 LFS pointer 后停止发布。随后用官方 pointer 的 OID/size 拉取七个真实对象（464,751,893 bytes），pointer blob 和实际对象双重验收；3,862 个路径全部完成后才使用完整 individual-file inventory。

2026-09-18 至 2026-09-19：核对 eLife 发布历史，将最初按 first-publication 命名的 PDF/XML 更正为 2021-11-03 Version of Record v3，并验证改名前后 bytes/SHA-256 不变；另取得八个 v3 figure source data。读取全文方法、滴定边界、重复和数据可用性；独立核对五张关键 landscape 表的行数、二进制 genotype、缺失和值域。三个 PDB 锚点 canonical FASTA/mmCIF 两层验收。

2026-09-19：将 eLife v3 Figure 1 CR9114/CR6261 定量表与固定 Git mean-bin filtered merged 表逐行核对；65,536/1,917 个数据行及顺序逐 byte 相同，只有字段名不同。该重复关系进入训练去重说明。

2026-09-18：论文/补充的下载身份和通用名修正留痕如下；原始文件与描述性落盘名对应的 bytes/SHA-256 均已核对，重命名没有改写内容。

| 下载一手 URL | 原始名 | 落盘路径 | bytes |
| --- | --- | --- | --- |
| <https://cdn.elifesciences.org/articles/71393/elife-71393-v3.pdf> | elife-71393-v3.pdf | articles/Phillips_2021-11-03_eLife-v3.pdf | 7852160 |
| <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8476123/fullTextXML> | fullTextXML | articles/Phillips_2021-11-03_eLife-v3.xml | 439553 |
| <https://cdn.elifesciences.org/articles/71393/elife-71393-fig1-data1-v3.csv> | elife-71393-fig1-data1-v3.csv | articles/Phillips_2021-11-03_eLife-v3-fig1-data1.csv | 12258680 |
| <https://cdn.elifesciences.org/articles/71393/elife-71393-fig1-data2-v3.csv> | elife-71393-fig1-data2-v3.csv | articles/Phillips_2021-11-03_eLife-v3-fig1-data2.csv | 358244 |
| <https://cdn.elifesciences.org/articles/71393/elife-71393-fig1-data3-v3.xlsx> | elife-71393-fig1-data3-v3.xlsx | articles/Phillips_2021-11-03_eLife-v3-fig1-data3.xlsx | 16969 |
| <https://cdn.elifesciences.org/articles/71393/elife-71393-fig2-data1-v3.csv> | elife-71393-fig2-data1-v3.csv | articles/Phillips_2021-11-03_eLife-v3-fig2-data1.csv | 1053782 |
| <https://cdn.elifesciences.org/articles/71393/elife-71393-fig2-data2-v3.csv> | elife-71393-fig2-data2-v3.csv | articles/Phillips_2021-11-03_eLife-v3-fig2-data2.csv | 140833 |
| <https://cdn.elifesciences.org/articles/71393/elife-71393-fig2-data3-v3.xlsx> | elife-71393-fig2-data3-v3.xlsx | articles/Phillips_2021-11-03_eLife-v3-fig2-data3.xlsx | 30573 |
| <https://cdn.elifesciences.org/articles/71393/elife-71393-fig5-data1-v3.csv> | elife-71393-fig5-data1-v3.csv | articles/Phillips_2021-11-03_eLife-v3-fig5-data1.csv | 115132 |
| <https://cdn.elifesciences.org/articles/71393/elife-71393-fig5-data2-v3.csv> | elife-71393-fig5-data2-v3.csv | articles/Phillips_2021-11-03_eLife-v3-fig5-data2.csv | 3831 |

2026-09-18：本地 README 编辑后立即同步共享 staging，固定 markdownlint-cli2 0.20.0 按 skill 配置检查。发布、残留清理和当前缺口同步到本批交接；source version 不另发布 manifest、API 响应或审计文件。完整研究 acquisition 与本次公开包接入分开记录。

## 参考文献

- [固定上游数据版本](https://github.com/klawrence26/bnab-landscapes/tree/514d62f387070f43b8a172f02e60c70137f8a8b8)
- [主论文 DOI](https://doi.org/10.7554/eLife.71393)
- [eLife Version of Record 与发布历史](https://elifesciences.org/articles/71393)
- [固定 GitHub commit](https://github.com/klawrence26/bnab-landscapes/tree/514d62f387070f43b8a172f02e60c70137f8a8b8)
- [底层 reads 项目 PRJNA741613](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA741613)
- [PDB 3GBN 及其原始结构论文](https://www.rcsb.org/structure/3GBN)
- [PDB 4FQI 及其原始结构论文](https://www.rcsb.org/structure/4FQI)
- [PDB 4FQY 及其原始结构论文](https://www.rcsb.org/structure/4FQY)

## 其他

### 完整性与验收

公开 payload 3862 个文件、10651420405 bytes；完整 Git archive/tree 验证 blob 数 3862。文件 inventory 按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接的 SHA-256：`1d94ec9756a92b1b57d9bfbd2d85747d48f2581b7402372679f9d846e959f963`。Git blob/LFS 官方身份分别验证；此 inventory 是项目本地摘要，不冒称上游官方 checksum。

固定 Git tree 3,862 个路径（含七个已解析 LFS 对象、实际 payload 10,651,420,405 bytes）和 10 个论文/figure source 对象已取得；关键 landscape 语义、全表 inventory、Git/LFS 身份、文章格式与三个 PDB 两层均验收后可声明 verified public-package onboarding。底层 SRA reads 未纳入，因此不声明 complete-study acquisition。

### 许可和再分发边界

仓库根 LICENSE 为 MIT，适用于固定仓库代码/文件时保留版权与许可文本；eLife v3 正文与 publisher figure source data 为 CC BY 4.0，保留作者、DOI、版本与修改说明。PDB 外部 entry 保留结构原论文引用及 wwPDB/RCSB 来源。

### 公开范围对照

| 论文或来源所指内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| CR6261 11-site 完整 landscape | Figure1 表 2,048 个唯一 genotype | 已包含 |
| CR9114 16-site 完整 landscape | Figure1 表 65,536 个唯一 genotype | 已包含 |
| 三次 biological replicates 与 mean/SEM | 主处理表含对应字段；缺失和边界已记录 | 已包含 |
| flow/sort/counts、表达、validation、模型/图件 | 完整 Git tree 对应目录 | 已包含，多层相关表示 |
| eLife 定量 figure source data | v3 八个 CSV/XLSX；Figure 1 两个主表数据行与 Git 对应表相同，仅 header 改名 | 已包含，重复表示 |
| 原始测序 reads | PRJNA741613 不在 Git tree | 本批未下载 |
| 逐 genotype 实验结构 | 三亲本/抗原锚点由多 genotype 共享 | 未包含 |
