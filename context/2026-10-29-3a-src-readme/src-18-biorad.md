---
- tags:
  - context
---

# SRC_R18_BIORAD 数据说明

## 数据集身份

- `source_id`：`SRC_R18_BIORAD`
- `source_version`：`snapshot-2024-12-20`
- 原作者或发布机构：Jason D. Gans、Justin E. Miller、Esen Sokullu、Nileena Velappan、Ramesh K. Jha / Los Alamos National Laboratory

### 来源方背景

论文五位作者均来自 Los Alamos National Laboratory（LANL）的 Bioscience Division。LANL [官方介绍](https://www.lanl.gov/about)显示，该实验室成立于 1943 年，位于美国新墨西哥州北部，是美国能源部国家核安全局的多项目联邦研发中心。BIORAD 将人工文献核查、蛋白复合物结构和机器学习评测结合起来，与本来源的跨学科数据整理性质直接相关。

## 实验设计和数据口径

BIORAD 不是新的结合实验，而是对 PDBbind 2020 中蛋白异二聚体亲和力记录的人工文献审计，并进一步观察数据订正对机器学习评测的影响。这里的 `KD` 是平衡解离常数，单位为 M；数值越小通常表示结合越强。

作者先将 RCSB PDB 中标注为异源二聚体的结构与 PDBbind 2020 蛋白—蛋白部分相交，再依据 PDB 主引用寻找 PubMed Central Open Access（PMC OA）论文。仓库保留 288 个用于结构和文献下载的 PDB 支持条目，对应 217 篇唯一 PMC 文献；其中 262 个 PDB 条目进入正式 `KD` 人工审核。公开仓库和论文没有提供其余 26 个支持条目未进入 `KD` 表的逐项理由，因此不能把这 26 条解释成某一类失败实验。

对 262 条审核对象，作者逐篇比对 PDB 结构中的蛋白构建体、序列、突变或修饰与论文中的亲和力测量对象，再把原 PDBbind 数值分为六类。补充表中的计数为：`Match` 211 条、`No KD` 24 条、`Different variant` 12 条、`Approximate` 10 条、`Units` 3 条、`Multisite KD` 2 条，共有 51/262（19.47%）不属于 `Match`。其中 `No KD` 不是“实验测得不结合”，而是作者没有在主引用中找到与该 PDB 构建体相匹配的 `KD`；`Multisite KD` 表示论文用多位点模型报告两个 `KD`，不能直接压成 PDBbind 的单一数值。

主数据形成关系如下。图中的 288→262 只表示公开清单与正式审核表的已验证集合关系，不补写未公开的逐条筛选原因。

```text
PDBbind 2020 蛋白—蛋白记录
  ∩ RCSB 异源二聚体
  ∩ 可定位 PMC OA 主引用
            │
            ├── 288 个结构/文献支持条目（217 个唯一 PMCID）
            │        │
            │        └── 262 个进入 KD 人工审核
            │               ├── 原 PDBbind：262 条
            │               ├── 仅修正 Units：262 条（3 个数值）
            │               ├── 仅修正 Different heterodimer：262 条（12 个数值）
            │               ├── 排除 No KD 24 条：238 条
            │               └── 再排除 Multisite KD 2 条并采用人工值：236 条
            │
            └── 其余 26 条未进入 KD 表：公开材料未逐项说明原因
```

五张 curation CSV 因而是同一批对象的不同分析版本，不能相加计为 1,260 个独立样本：

| 文件 | 记录数 | 处理口径 |
| --- | ---: | --- |
| `curation_pdbbind.csv` | 262 | PDBbind 原始 `KD` |
| `curation_units.csv` | 262 | 只修正 3 条单位错误 |
| `curation_different_heterodimers.csv` | 262 | 只把 12 条数值改为与结构构建体对应的 `KD`；论文称 `Different heterodimer`，附件分类值写作 `Different variant` |
| `curation_no_kd.csv` | 238 | 从原始 262 条中排除 24 条 `No KD` |
| `curation_all.csv` | 236 | 排除 24 条 `No KD` 和 2 条 `Multisite KD`，其余采用人工复核值 |

作者随后以蛋白复合物三维结构为输入，统计两个蛋白之间不超过 12 Å 的跨蛋白原子类型对，使用 100 棵树的随机森林，并进行 100 次五折、基于序列聚类的交叉验证。`cluster/` 保存不同最小簇间距离下的分组，`output/` 保存已经计算好的评测指标和逐 PDB 预测；这些是模型评测产物，不是新的实验测量，也不能作为训练标签再回灌模型。

固定仓库的预计算输出与正式论文方法存在两处需要特别区分的口径。第一，论文和仓库 README 写 `log10(KD)`，但源码调用 C++ `log()`，且本次对五个输出文件的每一条记录反算后，`log(Kd)` 都与自然对数 `ln(KD)` 一致。改变对数底数不会改变 Pearson 相关系数，但逐条对数值和 RMSE 会相差固定的尺度因子。第二，论文写明忽略所有氢原子，但五个输出的 atom inventory 都包含 3,557,566 个 H，固定源码中的 `REMOVE_HYDROGENS` 块也未启用。输出命令还引用了未随仓库交付的外部 `../data/PDBBind_hydrogen` 目录。因此，当前 `.out` 应按上游预计算结果原样保留：其中对数列按自然对数解释，但在作者澄清或独立复现前，不宣称它与正式论文描述的方法完全一致。这不改变五张 curation CSV 的 `KD` 数值口径。

## 论文原文

- 标题：The impact of curation errors in the PDBBind Database on machine learning predictions of protein–protein binding affinity
- 作者：Jason D. Gans；Justin E. Miller；Esen Sokullu；Nileena Velappan；Ramesh K. Jha
- 发表来源：*Database: The Journal of Biological Databases and Curation*，2025，baaf061
- 归档文本版本：正式发表版的 Europe PMC 全文 XML
- 发布日期：2025-09-24
- DOI：`10.1093/database/baaf061`
- PMID / PMCID：`40996705` / `PMC12462375`
- 本地文件：`articles/BIORAD_2025-09-24_Database-published.xml`
- 文件大小：85.37 KiB（87,421 bytes）
- SHA-256：`13a8f75ac14435b934c8de4da159250623b917dc8362c9ea53d4f9f69fa83c85`
- 文本许可：Creative Commons Attribution 4.0 International（CC BY 4.0）
- 补充材料：`articles/BIORAD_2025-09-24_supplement-baaf061_supplemental_file.zip`，30.93 KiB（31,669 bytes），SHA-256 `c0ab4a6d677e70bd790322bdb1ab51b1721d55a5aa858766aec06a42e592f150`
- 引用数（查询快照）：2（[OpenAlex W4414509437](https://openalex.org/W4414509437)，查询于 2026-09-24）

补充 ZIP 已通过完整 CRC、路径安全和成员唯一性检查，只含 `Supplementary_table_1.xlsx`。其中 `PDBBind_affinity_update` sheet 有 262 条非空记录和 5 个字段：`accession` 是 PDB ID；`PDBBind affinity value  (M)` 是原 PDBbind 数值；`PDBBind curation category` 是人工审核类别；`Curated affinity value  (M)` 是作者从文献复核后的数值；`comments` 记录具体依据。后两列分别有 26 个和 214 个空值：前者对应 24 条 `No KD` 与 2 条 `Multisite KD`，后者表示作者未为多数记录另写备注，不应填成数值 0。

`PDBBind curation category` 的当前附件取值如下；附件的 `Different variant` 与正文中的 `Different heterodimer` 指向同一类问题。

| 原始取值 | 记录数 | 含义 |
| --- | ---: | --- |
| `Match` | 211 | PDBbind `KD` 与人工核对值一致 |
| `No KD` | 24 | 主引用没有与该 PDB 构建体相匹配的 `KD` |
| `Different variant` | 12 | PDBbind 数值属于另一个蛋白异二聚体或构建体变体 |
| `Approximate` | 10 | PDBbind 给出近似值，主引用有更精确数值 |
| `Units` | 3 | PDBbind 数值的单位与主引用不一致 |
| `Multisite KD` | 2 | 主引用报告多位点模型的两个 `KD`，无法直接对应单一数值 |

数据快照固定于 2024-12-20 的 Git commit，早于论文在 2025-09-24 正式发表。正式论文用于解释这份固定数据的研究设计、分类和方法；它不会把 `source_version` 改成论文发布日期，也不会无依据改写仓库中的原始文件。

## 仓库内容

来源身份：

- `kind`：`github`
- `repository`：`lanl/BIORAD`
- `commit`：`abc0688f1a4333e5c0d5d377ae1ad0e7d318e83e`
- `tree`：`abc0688f1a4333e5c0d5d377ae1ad0e7d318e83e`
- `commit_date`：`2024-12-20T21:01:01Z`

`source_version` 的日期来自固定 commit。当前 payload 是该 commit 的完整 47 个 tracked 文件，共 1.09 MiB（1,145,893 bytes）；没有 Git LFS 指针或 submodule。下列目录树只展示上游 Git payload，不列项目生成的 README、归档论文或外部补取的 RCSB 文件。

```text
snapshot-2024-12-20/
└── BIORAD/
    ├── LICENSE
    ├── README.md
    ├── cluster/
    │   └── 5 个序列聚类文件
    ├── data/
    │   ├── 5 张 curation CSV
    │   ├── pdbbind_heterodimer_pdb.csv
    │   └── pdbbind_oa.csv
    ├── output/
    │   └── 5 个预计算评测输出
    ├── scripts/
    │   └── 3 个下载、加氢和批量运行脚本
    └── src/
        └── C++17 源码与 Makefile
```

`data/` 提供人工审核后的数值版本及结构/文献清单，`cluster/` 与这些数值版本一一对应，`output/` 是上游已运行结果，`scripts/` 和 `src/` 提供获取依赖与重跑模型的代码。仓库没有交付输出日志所引用的 1,305 个加氢 PDB 文件，也没有交付脚本可下载的 217 篇原始审核文献全文。

## 数据结构

### 亲和力表及其关系

五张 curation CSV 使用相同 6 列；每行代表一个 PDB 蛋白异二聚体记录在某一数据修订口径下的一项 `KD`，不是一次新的实验 replicate。每张表内 `accession` 唯一、无完整重复行、无缺失字段。

| 原始文件 | 非空记录数 | 唯一 PDB ID | X-RAY / NMR | `=` / `~` |
| --- | ---: | ---: | ---: | ---: |
| `BIORAD/data/curation_pdbbind.csv` | 262 | 262 | 238 / 24 | 257 / 5 |
| `BIORAD/data/curation_units.csv` | 262 | 262 | 238 / 24 | 257 / 5 |
| `BIORAD/data/curation_different_heterodimers.csv` | 262 | 262 | 238 / 24 | 257 / 5 |
| `BIORAD/data/curation_no_kd.csv` | 238 | 238 | 217 / 21 | 233 / 5 |
| `BIORAD/data/curation_all.csv` | 236 | 236 | 215 / 21 | 231 / 5 |

CSV 与正式补充表的集合关系和修订类别逐项一致，但数值精度并非逐单元格完全相同：前四张表各有 5 条、`curation_all.csv` 有 6 条 `affinity_value` 与附件相比存在不超过 0.2962% 的差异，表现为有效数字位数减少。公开材料没有说明具体舍入规则，因此需要精确保留作者人工摘录值时以补充表为准，需要复现仓库模型输入时以 CSV 原值为准，不能把两者宣称为字节或数值完全等价。

### 文献与结构支持清单

`BIORAD/data/pdbbind_heterodimer_pdb.csv` 不是常规行式 CSV，而是一行、无表头的 288 个逗号分隔 PDB ID。`BIORAD/data/pdbbind_oa.csv` 有 288 条非空映射、288 个唯一 PDB ID 和 217 个唯一 PMCID；它与单行 PDB 清单的 ID 集合完全相同。同一篇论文可以对应多个结构，因此 PMCID 不唯一。

262 个 curation ID 全部属于这 288 个支持 ID。多出的 26 个 ID 只出现在结构/文献支持清单和本项目补取的 PDB 文件中，不进入五张 curation 表、聚类或模型输出。

### 聚类与模型输出

每张 curation 表都有一份对应的 `cluster.align.*` 和 `.out` 文件。聚类文件按多个最小簇间序列距离保存完整分区；本次逐层展开后，每层都恰好覆盖相应表的全部 PDB ID，既无遗漏也无重复。输出中的逐 PDB 预测 ID 也与相应输入表完全一致。

| curation 口径 | 聚类层级数 | 每层起始/末尾簇数 | output 预测行数 |
| --- | ---: | ---: | ---: |
| PDBbind | 87 | 262 / 5 | 262 |
| Units only | 87 | 262 / 5 | 262 |
| Different heterodimer only | 87 | 262 / 5 | 262 |
| No KD only | 83 | 238 / 10 | 238 |
| Full correction | 85 | 236 / 9 | 236 |

`.out` 先记录运行参数、结构和 atom inventory，再包含一张按聚类距离汇总的 18 列指标表，最后包含一张 4 列逐 PDB 预测表。文件是上游预计算日志式结果，不是只有表格内容的标准 TSV；读取时应先定位对应表头。

### 字段说明

五张 curation CSV 的字段完全相同：

| 字段 | 原始表示 | 含义与使用边界 |
| --- | --- | --- |
| `accession` | 4 字符小写字符串 | PDB accession；也是连接支持清单、聚类、输出和本项目 RCSB 补充文件的主键 |
| `structure_format` | 字符串 | `NMR`，或 `X-RAY=<resolution>`；X 射线分辨率以 Å 表示，不是亲和力 |
| `year` | 4 位整数字符串 | 随上游结构记录保留的年份；当前观察范围为 2006–2018，仓库未另附字段字典进一步区分发布日期口径 |
| `affinity_type` | 分类字符串 | 当前五张表均为 `Kd`，即平衡解离常数 |
| `affinity_match` | 分类字符串 | `=` 表示等值记录，`~` 表示近似记录；这是数值比较符，不是人工审核类别 |
| `affinity_value` | 正浮点数字符串 | `KD`，单位 M；当前范围为 `2.90E-11`–`1.87E-03`，数值越小通常结合越强 |

**`affinity_match`（五张 curation CSV；取值范围依据：固定版本扫描及源码枚举）**

| 原始取值 | 262 条表中的记录数 | 含义 |
| --- | ---: | --- |
| `=` | 257 | 数值按等值关系输入 |
| `~` | 5 | 数值按近似关系输入；不等同于附件的 `Approximate` 分类 |

**`structure_format`（五张 curation CSV；取值范围依据：固定版本扫描及源码 parser）**

| 原始形式 | 262 条表中的记录数 | 含义 |
| --- | ---: | --- |
| `NMR` | 24 | 核磁共振结构，不附分辨率 |
| `X-RAY=<数值>` | 238 | X 射线结构，等号后的数值为 Å 分辨率 |

`BIORAD/data/pdbbind_oa.csv` 的字段为：

| 字段 | 原始表示 | 含义 |
| --- | --- | --- |
| `PDB` | 4 字符小写字符串 | 结构 accession，当前 288 个值均唯一 |
| `PMCID` | `PMC` 加数字 | PDB 主引用的 PMC ID；当前 217 个唯一值，可一对多连接 PDB |

`cluster.align.*` 的前五行是生成时间和参数注释；其后每行写作 `<minimum_distance>:(<cluster 1>)(<cluster 2>)...`。括号表示一个聚类，括号内以逗号分隔的 PDB ID 属于同一簇；`minimum_distance` 是序列比对距离阈值，不是结构距离或亲和力。

`.out` 指标表字段可按以下语义组还原：

| 字段或命名组 | 类型 | 含义 |
| --- | --- | --- |
| `min_cluster_distance` | 浮点数 | 对应聚类文件的最小簇间距离 |
| `number_of_clusters` | 整数 | 当前距离阈值下的簇数 |
| `ave_baseline_r`、`stdev_baseline_r`、`baseline_p_value` | 浮点数 | 氨基酸组成基线模型的 Pearson `r` 均值、标准差和置换检验 `p` 值 |
| `ave_baseline_RMSE`、`stdev_baseline_RMSE` | 浮点数 | 基线模型 RMSE 的均值和标准差；因内部目标为 `ln(KD)`，其误差尺度也是自然对数尺度 |
| `ave_baseline_R2`、`stdev_baseline_R2` | 浮点数 | 基线模型 `R²` 的均值和标准差 |
| `ave_model_r`、`stdev_model_r`、`model_p_value` | 浮点数 | 结构特征随机森林 Pearson `r` 的均值、标准差和置换检验 `p` 值 |
| `ave_model_RMSE`、`stdev_model_RMSE` | 浮点数 | 结构模型 RMSE 的均值和标准差，使用自然对数尺度 |
| `ave_model_R2`、`stdev_model_R2` | 浮点数 | 结构模型 `R²` 的均值和标准差 |
| `ave_model_R2(baseline)`、`stdev_model_R2(baseline)` | 浮点数 | 以组成基线为参照计算的模型 `R²` 均值和标准差 |

逐 PDB 预测表有 4 个字段：`accession` 是 PDB ID；`log(Kd)` 实际为输入 `KD` 的自然对数；`ave predict log(Kd)` 和 `stdev predict log(Kd)` 是上游多轮交叉验证预测的均值和标准差，也使用自然对数尺度。字段名本身没有写出底数，不能仅凭论文中的 `log10` 表述改读为常用对数。

### 数据示例

以下为 `BIORAD/data/curation_all.csv` 的第一条真实记录：

| 字段 | 原样值 |
| --- | --- |
| `accession` | `2kgx` |
| `structure_format` | `NMR` |
| `year` | `2009` |
| `affinity_type` | `Kd` |
| `affinity_match` | `=` |
| `affinity_value` | `1.10E-05` |

这行表示 PDB `2kgx` 在 Full correction 口径下的一项 `KD=1.10×10⁻⁵ M`，不是某个模型预测、replicate 或独立于其他 curation 表的新样本。

## PDB 数据库

PDB 锚点直接来自 `BIORAD/data/pdbbind_heterodimer_pdb.csv` 的 288 个 PDB ID，因此属于强主键映射；262 个 curation ID 全部在其中。每个锚点补取一份 RCSB 原始 per-entry FASTA 和一份完整 mmCIF，共 288 份 FASTA、288 份 mmCIF，合计 576 个文件、328.96 MiB（344,940,509 bytes）。

文件于 2026-09-18 从 RCSB 的 per-entry FASTA 端点 `https://www.rcsb.org/fasta/entry/<PDB_ID>/download` 和完整坐标端点 `https://files.rcsb.org/download/<PDB_ID>.cif.gz` 获取；保存时解压 mmCIF 的传输层 gzip，但不改写其中的 mmCIF 内容。

本次重新逐文件解析全部配对，共核对 585 条 polymer entity FASTA record 和 2,730,165 条坐标 atom row。每个文件的 entry ID、全部 polymer entity、author-chain 集合和 canonical sequence 均与对应完整 mmCIF 一致，288/288 对通过。原始 FASTA header 保留不改写，没有从结构坐标反推序列，也没有只保存作者选定的链。

此前拉取流程曾错误复用选择链或重写 header 的 FASTA 缓存；这些接入前暂存的错误副本已删除并重新获取。当前接受文件均通过原始 RCSB header 格式及完整 entity/chain/sequence 配对检查。确定性 inventory SHA-256 为 `5606cd0e1a6b4fc23e8c7e6de0a01154513b201fb7176e3d29f441d00f565762`，计算输入为按相对路径排序的 `relative_path<TAB>bytes<TAB>sha256<LF>`。

这些 RCSB 文件是完整原始结构证据，不是上游 `.out` 使用的 `PDBBind_hydrogen` 加氢 PDB 目录。它们可以支持 accession、链和序列核验，但不能直接声称已经补齐模型输出的精确运行输入。

## 采集过程记录

- 2026-09-18：读取项目配置与数据访问清单，固定 `lanl/BIORAD` commit `abc0688f1a4333e5c0d5d377ae1ad0e7d318e83e`，将 47 个 tracked 文件下载到 `.staging/snapshot-2024-12-20.partial`。逐文件复算 Git blob ID、字节数与 SHA-256，未执行上游代码。
- 2026-09-18：从 Europe PMC 归档正式发表版全文 XML，并按主文 XML 引用取得唯一 supplement ZIP；检查 DOI、PMID/PMCID、发布日期、ZIP CRC、成员路径、成员唯一性和 XLSX schema。主文从早期缓存名改为当前含日期和出版版本的文件名，改名前后字节与 SHA-256 不变。
- 2026-09-18：PDB 原始性检查发现先前缓存含选择链或重写 header 的 FASTA。删除本轮错误副本后，改取 288 个 PDB entry 的原始 RCSB FASTA 和完整 mmCIF，并执行完整 entity、author-chain 与 canonical sequence 配对检查。
- 2026-09-19：复核固定仓库根 LICENSE、仓库 README、论文 Data availability 和现行 PDBbind+ Terms of Use；没有注册账户、接受额外条款、联系作者或发送授权请求。条款入口及响应身份保留在共享审计 cache。
- 2026-09-24：运行常规独立 audit，47/47 个 Git 文件、6 张常规 CSV 表和 288/288 对 PDB 文件通过。新增 `review_biorad_content.py`，逐项核对 288/262/238/236 集合关系、补充表六类计数、五组 cluster/output 覆盖、CSV 与附件精度差异以及输出对数底数和氢原子证据。
- 2026-09-24：核对 LANL 一手背景、论文正式版身份和 OpenAlex 引用快照，按最新 source README 结构重写文档并同步暂存目录。进一步确认本项目的“发布”只是在共享存储内部将已验收目录原子移动到固定的本地 raw 路径，不会把文件上传或分发给第三方；据此完成本地接入，同时继续把 PDBbind 数据的外发限制记录为后续使用边界。

## 参考文献

- [BIORAD 固定 Git commit](https://github.com/lanl/BIORAD/tree/abc0688f1a4333e5c0d5d377ae1ad0e7d318e83e)
- [正式论文 DOI](https://doi.org/10.1093/database/baaf061)
- [Europe PMC 正式全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12462375/)
- [Europe PMC 全文 XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12462375/fullTextXML)
- [OpenAlex 论文记录](https://openalex.org/W4414509437)
- [Los Alamos National Laboratory 官方介绍](https://www.lanl.gov/about)
- [PDBbind+ Terms of Use](https://www.pdbbind-plus.org.cn/termofuse)
- [RCSB PDB](https://www.rcsb.org/)
- [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## 其他

### 数据范围和限制

当前 source 是公开 BIORAD Git 快照、该研究正式论文与附件，以及项目按 288 个公开 accession 补取的原始 RCSB 结构证据。它不是 PDBbind 2020 完整数据库，也没有归档 217 篇被人工审核的原始 PMC 论文全文、PDBbind 的 `INDEX_general_PP.2020` 原文件、上游 1,305 个加氢 PDB 运行目录或模型的逐折预测中间状态。

五张 curation 表高度非独立，只应按所需修订口径选择一张。`No KD` 表示找不到与结构构建体匹配的文献 `KD`，不能当作 non-binder 标签。人工审核仍受主引用公开内容和构建体匹配判断限制，也没有汇总不同 pH、温度、盐浓度等实验条件。

预计算 `.out` 的 accession、聚类阈值和输入 `KD` 对应关系已经验收，但对数底数、氢原子处理和缺失的加氢结构目录使其不能作为正式论文方法的自足复现包。CSV 与论文附件的少量有效数字差异也要求使用者明确选择“仓库模型输入”或“正式附件人工摘录值”，不要静默混用。

### 完整性与验收

固定 Git payload 的 47/47 个文件均通过大小和上游 Git blob 校验；6 张常规 CSV 表完成全量解析，五张 curation 表的记录数、主键、枚举、正值范围和集合关系通过；正式主文及唯一附件完成身份、哈希、归档和 XLSX 全量核对；288/288 对原始 RCSB FASTA/mmCIF 通过结构配对审计。共享 cache 中保存常规 audit、article audit 和 source-specific content review，临时报告不混入原始 source version。

技术获取、内容验收和本地接入发布均已完成；固定版本目录为 `hf://buckets/Pthahnix/dataset-abag/SRC_R18_BIORAD/snapshot-2024-12-20`。这里的“发布”仅指将验收通过的暂存目录原子移动到项目共享存储中的固定 raw 路径，`public` 是项目对来源可获取性的分类，不表示项目已把文件上传互联网、开放给新的第三方或取得额外再分发授权。

### 许可和再分发边界

代码、论文文本、数据和外部结构需要分层理解：

- 固定 Git 根目录带 BSD-3-Clause。该宽松许可允许代码使用、修改和商业使用，但再分发代码及其二进制形式时须保留版权、许可条件和免责声明；不能用作者名为衍生产品背书。
- 正式论文标明 CC BY 4.0；补充附件随论文一同发布，本次未在附件内部发现单独的许可文本。复用时应保留论文归属、遵守 CC BY 4.0，并在需要独立再分发附件时核对出版方的附件政策。
- Git 仓库公开，README 也称其包含 “source code and input data files”，但论文 Data availability 只明确写软件采用 BSD-3。核心 curation CSV 复用了 PDBbind 数值，因此不能仅凭代码 LICENSE 推定第三方数据也获 BSD-3 授权。
- 现行 PDBbind+ 官方条款授予个人、不可转让、非排他的使用权，并明确禁止未经 Fudan University 和 TopScience 特定书面授权向第三方再分发原始或衍生数据。该现行文本不能证明 2020 年历史条款完全相同；截至 2026-09-24 也尚未找到覆盖 BIORAD 子集的书面例外或权威数据许可。因此，不能据当前证据主张这些数值可自由对外再分发。
- 本项目补取的 RCSB FASTA/mmCIF 继续受 RCSB 自身政策约束；论文的 CC BY 4.0 和仓库的 BSD-3-Clause 都不会自动覆盖这些外部数据库文件。

本项目此次接入只是在同一项目共享存储内完成暂存目录到固定 raw 目录的原子移动，不构成向第三方公开再分发，因此上述数据层许可不阻塞本地接入。不过，这一内部操作不会扩大任何文件的权利范围；后续若要把含 PDBbind 数值的文件上传到外部平台、提供给当前授权范围之外的第三方，或用于需要额外权利的商业及衍生再分发，仍须先取得并核实相应授权。若只能确认代码许可，则应另行界定不含受限数值表的外发范围，不能把本地接入状态解释为已获公开再分发许可。

### 公开范围对照

| 目标组成 | 当前证据 | 状态 |
| --- | --- | --- |
| 固定 Git payload | 47/47 文件的 Git blob、大小、SHA-256 与格式审计 | 本地接入发布完成 |
| 正式论文与附件 | DOI/PMCID、全文 XML、唯一附件及逐成员/逐表核对 | 已归档并验收 |
| RCSB 结构证据 | 288 FASTA + 288 mmCIF 的完整 entity/chain/sequence 配对 | 已补齐并验收；不是模型加氢输入 |
| PDBbind 完整数据库 | 当前包只含 262 条审核表和 288 条支持清单 | 不在本 source 范围内 |
| 原始审核文献全集 | 映射到 217 个 PMCID，但未归档其全文 | 不在当前 payload；逐条审计依据由论文附件摘要 |
| 项目本地 raw 接入 | 仅在共享存储内从暂存目录原子移动到固定版本目录 | 已完成；不代表新增外发授权 |
| 向第三方公开再分发含 PDBbind 数值的文件 | 现行条款限制明确，未找到覆盖 BIORAD 子集的书面例外 | 未获确认；不在本次本地接入范围内 |

## 待解决问题与处理进展

- `Q01`（不阻塞本地接入，限制后续外发）：核心 CSV 复用了 PDBbind 数值；现行 PDBbind+ 条款禁止未经特定书面授权再分发 raw/derivative data，而仓库 BSD-3-Clause 和论文 CC BY 4.0 均不能明确覆盖这一第三方数据层。截至 2026-09-24 已核对仓库 LICENSE/README、论文 Data availability、正式附件和官方 Terms of Use，未发现 BIORAD 专属授权。本次只完成项目共享存储内的原子移动，不联系作者、不代用户接受条款，也不据此宣称获得外发权；若后续需要向授权范围外的第三方提供含相关数值的文件，须先取得并核实权威权利方对相应用途和分发方式的许可。
- `Q02`（影响模型输出解释与精确复现，不改变 curation 表）：正式论文描述 `log10(KD)` 且忽略氢原子，但固定源码和五个 `.out` 共同表明输出使用 `ln(KD)`，输入 inventory 含氢，且实际加氢 PDB 目录未交付。截至 2026-09-24 已逐行验证全部输出的对数值并核查源码开关，当前将 `.out` 标为上游预计算产物并按自然对数解释。关闭条件是作者说明正式论文与仓库输出的对应版本，或用可确认的方法和完整输入独立复现后确定应采用的口径。
- `Q03`（不阻塞已有表的使用，影响 288→262 的筛选解释）：288 个结构/PMC 支持 ID 中有 262 个进入 `KD` 审核表，另外 26 个的逐项排除原因没有在仓库或正式论文中单列。截至 2026-09-24 已确认两组 accession 的严格子集关系并列出差集，当前只将 288 解释为支持清单、262 解释为正式 `KD` 审核对象，不把差额归因于具体失败类型。取得作者筛选记录或权威逐条说明后关闭。
- `Q04`（不阻塞 CSV 使用，影响与正式附件的精确数值等价）：四张表各有 5 个值、`curation_all.csv` 有 6 个值与正式附件相比相差不超过 0.2962%，表现为有效数字减少，但上游没有说明舍入规则。截至 2026-09-24 已保留两种原始表示并完成逐项清单；模型复现使用 CSV，人工摘录复核使用附件。取得上游精度说明或确认这些值的生成规则后关闭。
