# SRC_R76_TDC_ANTIBODYAFF 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [记录粒度与连接关系](#记录粒度与连接关系)
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

- `source_id`：`SRC_R76_TDC_ANTIBODYAFF`
- `source_version`：`dataverse-v105`
- 原作者或发布机构：Therapeutics Data Commons（TDC），Harvard University；数据集作者为 Kexin Huang、Tianfan Fu、Wenhao Gao、Yue Zhao、Yusuf Roohani、Jure Leskovec、Connor W. Coley、Cao Xiao、Jimeng Sun、Marinka Zitnik

### 来源方背景

TDC 是哈佛大学发起的开放科学项目，把药物治疗相关的机器学习数据集、任务、数据划分策略、模型评测与排行榜集中到一个可编程接口下。项目由 Marinka Zitnik 课题组主持，合作者分布在 Harvard、Stanford、Georgia Tech 等机构。[TDC 主页](https://tdcommons.ai)与[代码仓库](https://github.com/mims-harvard/TDC)是其主要入口，数据托管在 Harvard Dataverse 的 `doi:10.7910/DVN/21LKWG` 下。

TDC 不是原始实验的产出方，而是对既有公开数据的汇编与标准化层。本数据集的上游是 SAbDab（Structural Antibody Database），由牛津大学 OPIG 维护。理解这一点对使用本数据至关重要：SAbDab 提供结构与亲和力记录，TDC 负责筛出蛋白/肽抗原子集并整理成机器学习可直接读取的表格。

## 实验设计和数据口径

本数据集不是新实验，而是对 SAbDab 亲和力记录的一次筛选与重整。TDC 的任务页面把数据集命名为 `Protein_SAbDab`，说明它从 SAbDab 中只保留蛋白或肽类抗原，以便抗体与抗原两侧都能用氨基酸序列表示；糖类、小分子和未注释抗原不在本次筛选范围内。

公开表给出 493 行，每行是一个“抗体—抗原—亲和力值”三元组。TDC 页面用抗体与抗原两个维度描述规模：431 个不同抗体、401 个不同抗原。这两个数来自按序列去重，而不是按名称去重，因此与 493 行、313 个抗原名称都不是同一计数口径。

### 数值的含义与方向

`Y` 列是亲和力值的原始表示，取值从 4×10⁻¹³ 到 2×10⁻⁴，383 个不同取值，其中 7 行同为 2×10⁻⁸、5 行同为 1×10⁻⁹。这一量级与摩尔浓度的解离常数 KD 相符（皮摩尔到亚毫摩尔），TDC 任务页面把该任务定为回归并建议使用 log 亲和力值。公开表本身没有给出单位字段，也没有区分 KD、IC50 或 EC50；本 README 因此只记录数值与量级，不把整列统一解释为某一种测量类型，相关疑问见 `Q02`。

`Y` 的数值越小表示结合越强（若为 KD）。方向与常见的“分数越高越好”相反，下游若直接回归或排序必须显式处理方向；TDC 的 loader 不做翻转，只在文档中建议取对数。

### 一条记录对应一次上游测量

493 行中有 493 个不同的 `ID1`（PDB ID），且不存在 `(ID1, ID2)` 重复，431 个抗体序列与 401 个抗原序列各自对应若干行。这说明本表的行粒度是“一个 PDB 条目中的一对特定抗体—抗原”，不是“一个抗体”。同一个抗体序列若在多个 PDB 条目中出现，会以多行形式记录；同一抗原序列同理。用 `X1` 或 `X2` 去重会把这种多条目结构压平，进而低估上游的独立测量次数。

上游 SAbDab 记录的是文献中的结构-亲和力对，本表继承这一性质：每行背后是一次已发表实验，但公开表不含实验方法、温度、pH、缓冲体系、重复次数或测量误差。同一个 KD 可能来自 SPR、ITC 或 ELISA，本表未区分。

### 处理层级

本来源属于 `processed-public`：TDC 从 SAbDab 取数、筛选、去重、重命名列，并把抗体多条链合并成 Python 列表字符串。原始 SAbDab 导出、筛选脚本与逐条来源映射都未包含在本次取得范围内；TDC 的代码仓库提供 loader，但不提供生成本数据集的转换脚本。

## 论文原文

- 标题：*Artificial intelligence foundation for therapeutic science*
- 作者：Kexin Huang, Tianfu Fu, Wenhao Gao, Yue Zhao, Yusuf Roohani, Jure Leskovec, Connor W. Coley, Cao Xiao, Jimeng Sun, Marinka Zitnik
- 发表来源：Nature Chemical Biology 18, 1033–1036 (2022)
- 归档文本版本：正式发表版（在线核对，未本地归档）
- 发布日期：2022-10-01
- DOI：`10.1038/s41589-022-01131-2`
- PMID / PMCID：`36131149` / `PMC9529840`
- 正文在线入口：<https://doi.org/10.1038/s41589-022-01131-2>
- 本地归档：未归档
- 文本许可：未在本次可取得的页面中确认（PMC 记录标为非开放获取）
- 补充材料：未取得

该论文是 TDC 平台的总体介绍，不是本数据集专属的方法学论文；论文描述 TDC 的数据集族与任务体系，本数据集（`Protein_SAbDab`，任务名 AntibodyAff）只是其中一项。因此论文不能提供本表 493 行的逐条筛选规则或上游映射。

本次尝试了 PMC 的 PDF 入口、Europe PMC 的 `fullTextXML` 与 `fulltextRepo`、Nature 的 PDF 直链，分别返回 403、500、403 与 HTML 跳转页，未取得可核验的 PDF 字节。按 skill 规则，改为记录在线入口与未归档状态，并在“待解决问题与处理进展”跟踪，不虚构本地文件、大小或哈希。

## 仓库内容

数据来自 Harvard Dataverse 的 TDC 数据集 `doi:10.7910/DVN/21LKWG`，当前版本为 `105.0`，状态 `RELEASED`，发布时间 2025-08-27T12:05:20Z，首次存档日期 2020-10-14。该版本共 676 个文件，本数据集只取其中的 `protein_sabdab.csv`，文件 ID `4167357`，字节数 330,303，MD5 `f4d0dba68859f7ae2a042bd90423b22b`，`publicationDate` 与 `creationDate` 均为 2020-11-08。

`source_version` 使用 `dataverse-v105`：`v105` 直接来自 Dataverse 的版本号，不按下载日期命名。该版本是湖式数据集（一个 dataset 装 676 个文件）的一部分，因此 `source_version` 描述的是“本文件所在的 dataset 版本”，而文件自身的 `publicationDate` 仍为 2020-11-08。

```text
dataverse-v105/
└── protein_sabdab.csv
```

只有这一个 payload 文件。TDC 官方 loader 把该文件读入后按 8:1:1 随机划分，但公开的 CSV 不含划分列；划分由 loader 在运行时生成。本 README 记录的是原始表，不记录任何划分结果。

## 数据结构

### 记录粒度与连接关系

`protein_sabdab.csv` 有 493 行数据行、6 列：一个无名序列化索引列，以及 `ID1`、`X1`、`ID2`、`X2`、`Y`。`ID1` 是 PDB 条目 ID（小写，如 `1hh6`），`X1` 是该条目的抗体链序列，`X2` 是抗原序列，`ID2` 是抗原名称，`Y` 是亲和力值。

`X1` 不是单个序列，而是 Python 列表的字符串表示，包含重链与轻链两条序列，例如 `['QDQLQQ...', 'DIKMTQ...']`。全部 493 行都是 2 元素列表，没有可变长度。这意味着抗体侧在本表中恒为“重链 + 轻链”的形式，但不保证列表顺序在所有行都代表同一链角色；TDC 文档说明抗体序列按重链在前、轻链在后排列，本表未见反例，但公开表没有独立的链角色列。

`ID2` 是抗原名称，取值 313 个，包含蛋白名、肽名与复合描述（例如 `pep-4`、`signal-regulatory protein gamma`、`chimera of major allergen i polypeptide chain 2,majorallergen i polypeptide chain 1`）。名称不唯一对应序列：401 个不同 `X2` 对应 313 个名称，说明部分名称下存在多条不同序列，或同一序列被赋予不同名称。按名称聚类的做法会与按序列聚类得到不同分组，见 `Q03`。

### 字段说明

| 原始字段 | 表示、单位与来源 | 缺失与特殊编码 |
| --- | --- | --- |
| （空表头） | pandas 序列化时留下的索引列，取值 0—492 | 无缺失；不是数据字段 |
| `ID1` | PDB 条目 ID，小写 4 字符 | 无缺失；493 个取值，无重复 |
| `X1` | 抗体序列，Python 列表字符串，2 个元素（重链、轻链） | 无缺失；重链 114—454 aa，轻链 104—259 aa |
| `ID2` | 抗原名称，自由文本 | 无缺失；313 个不同名称 |
| `X2` | 抗原序列，单条氨基酸串 | 无缺失；3—1,676 aa，其中 107 行长度不超过 20 aa |
| `Y` | 亲和力值，数值，4×10⁻¹³—2×10⁻⁴ | 无缺失；383 个不同取值 |

`X1` 的字符串表示与 `.csv` 字段引号同时存在：序列列表本身含逗号与单引号，因此整个字段在 CSV 中被双引号包裹。直接按逗号切分会破坏该字段，必须使用标准 CSV 解析后再用 `ast.literal_eval` 还原列表。

`X2` 的长度跨三个数量级：最短 3 aa 是肽抗原，最长 1,676 aa 是完整膜蛋白胞外域。107 行的抗原长度不超过 20 aa，属于 TDC 筛选时保留的肽类抗原。把长度差异如此大的抗原放进同一模型时，需要长度分桶或截断策略，本表不提供这类标注。

`Y` 的数值精度不统一：多数值以两位有效数字给出（如 `1e-07`、`2.2e-09`），少数带浮点尾数（如 `1.6000000000000002e-10`）。后者是原始表以双精度文本写出时的表示误差，不是测量精度更高；同一数据在 R77 中写作 `1.6e-10`。本 README 保留原值，不做规范化。

### 数据示例

```text
ID1=1hh6,X1=['QDQLQQSGAELVRPGASVKLSCKALGYIFTDYEIHWVKQTPVHGLEWIGGIHPGSSGTAYNQKFKGKATLTADKSSTTAFMELSSLTSEDSAVYYCTRKDYWGQGTLVTVSAAKTTAPSVYPLVPVCGGTTGSSVTLGCLVKGYFPEPVTLTWNSGSLSSGVHTFPALLQSGLYTLSSSVTVTSNTWPSQTITCNVAHPASSTKVDKKIEPRV', 'DIKMTQSPSSMYTSLGERVTITCKASQDINSFLTWFLQKPGKSPKTLIYRANRLMIGVPSRFSGSGSGQTYSLTISSLEYEDMGIYYCLQYDDFPLTFGAGTKLDLKRADAAPTVSIFPPSSEQLTSGGASVVCFLNNFYPKEINVKWKIDGSERQNGVLDSWTEQDSKDSTYSMSSTLTLTKDEYERHNSYTCEATHKTSTSPIVKSFNRNEC']
ID2=pep-4,X2=DATPEDLGARL,Y=1e-07
```

这一行表示 PDB 条目 `1hh6` 中的抗体与一段 11 残基肽抗原的结合，亲和力 1×10⁻⁷。它是一次已发表测量的记录，不是重复实验；`X1` 中两条序列是该条目中该抗体的重链与轻链。

## PDB 数据库

`ID1` 列直接给出 PDB 条目，是逐行的外部锚点，映射强度为“逐行一对一”：493 行对应 493 个不同 PDB ID，不需要任何推断。这是本项目已接入来源中映射最强的一类。

项目按 `ID1` 的唯一值从 RCSB 取得每个条目的 entry 级 FASTA 与完整 mmCIF，未做选链或重建。493 个 ID 中 491 个成功取得；`3RVV` 与 `3RVW` 已于 2022-04-27 被 RCSB 撤销，`id_codes_replaced_by` 分别指向 `5VPL` 与 `5VPG`。这两个替代条目本身也在 493 个 ID 之中，且已单独取得，因此缺失的两个锚点可由其替代条目追溯，但本项目不用替代条目回填原 ID，保留原表的 493 个 ID 不变。

`pdb/` 共 982 个文件、579.02 MiB（607,146,339 bytes）：`sequences/` 下 491 个 `rcsb_pdb_<id>.fasta`，`structures/` 下 491 个 `<id>.cif`。FASTA 与 mmCIF 是 RCSB 的 entry 级原始下载，FASTA 包含该条目的全部 polymer entity，未做选链。按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接后的 inventory SHA-256 为 `9783594cd9cc592578595b2716a3e0947e2d5c4da653a9a73e325aff56f782d8`。未发布独立 PDB manifest。

| 项目 | 数值 |
| --- | ---: |
| 数据表锚点数 | 493 |
| 已取得条目的 FASTA | 491 |
| 已取得条目的 mmCIF | 491 |
| 未取得条目 | 2（`3RVV`、`3RVW`，RCSB 已撤销） |
| 文件总数 | 982 |
| 总字节数 | 607,146,339（579.02 MiB） |

链角色由 `X1` 的列表顺序给出，但与 PDB 条目内的 author chain 对应关系未在本表中标注。RCSB entry FASTA 保留了每个 entity 的 author chain 与描述，下游可据此把 `X1` 的两条序列匹配到具体链，但公开表没有给出这一映射。因此本 README 只声明“行级 PDB 锚点已固定”，不声明“抗体链角色已逐行确定”，后者属于使用阶段的工作。

## 采集过程记录

- 2026-10-28 用户指定存储根 `G:\abag-datasets`。项目无 `project.toml`、`developer.local.toml` 与 `workspace/`，因此 README 直接写入 source version 目录，未按 skill 的 `workspace/users/<user>/docs/readme/` 生成草稿；该偏差已获用户同意。
- 2026-10-28 从 TDC 任务页面取得 loader 名称 `AntibodyAff(name='Protein_SAbDab')`，在 TDC 源码中定位到数据集元数据：`protein_sabdab` 映射到 Dataverse 文件 ID `4167357`，下载端点前缀为 `https://dataverse.harvard.edu/api/access/datafile/`。随后直接以该端点取得 CSV，未安装 TDC 包。
- 2026-10-28 取得文件 330,303 bytes，MD5 `f4d0dba68859f7ae2a042bd90423b22b`，与 Dataverse 文件元数据一致。
- 2026-10-29 通过 Dataverse 导出接口 `api/datasets/export?exporter=dataverse_json&persistentId=doi%3A10.7910%2FDVN%2F21LKWG` 取得当前 dataset 版本 `105.0` 与 676 个文件的清单，确认 `protein_sabdab.csv` 的 ID、字节数、MD5、`publicationDate` 与 `creationDate`。
- 2026-10-29 独立验收：解析 CSV 确认 6 列、493 行；核对 `ID1` 无重复、`(ID1, ID2)` 无重复；解析 `X1` 的列表字符串确认 493 行均为 2 条链；统计 `X1`/`X2`/`ID2`/`Y` 的唯一值数与长度范围。
- 2026-10-29 按 skill 的 PDB 硬性要求，以 `ID1` 的 493 个唯一值为锚点从 RCSB 取得 entry FASTA 与 mmCIF，并发现在 `3RVV`、`3RVW` 上返回 404。查询 RCSB 的 `holdings/removed` 接口确认二者于 2022-04-27 撤销，替代条目为 `5VPL`、`5VPG`，且这两个替代条目本身在数据表内。
- 2026-10-29 论文 PDF 的三个入口（PMC、Europe PMC、Nature）分别返回 403、403/500 与 HTML 页，未取得可核验字节。改为在线入口记录，转入 `Q01`。
- 2026-10-29 发现 TDC 页面标注 `CC BY 3.0`，而 Dataverse dataset 标注 `CC0 1.0`。两者不一致，保留双方记录并转入 `Q04`。

## 参考文献

- TDC 任务页（AntibodyAff）：<https://tdcommons.ai/multi_pred_tasks/antibodyaff/>
- TDC 数据集（Harvard Dataverse）：<https://doi.org/10.7910/DVN/21LKWG>，版本 `105.0`
- 本数据集文件：<https://dataverse.harvard.edu/api/access/datafile/4167357>，`protein_sabdab.csv`
- TDC 代码仓库：<https://github.com/mims-harvard/TDC>
- 平台论文：Huang et al., *Artificial intelligence foundation for therapeutic science*, Nature Chemical Biology 18, 1033–1036 (2022)，DOI `10.1038/s41589-022-01131-2`
- 上游数据库：Dunbar et al., *SAbDab: the structural antibody database*, Nucleic Acids Research 42(D1):D1140 (2014)，DOI `10.1093/nar/gkt1043`
- 上游数据库更新：Schneider et al., *SAbDab in the age of biotherapeutics: updates including SAbDab-nano, the nanobody structure tracker*, Nucleic Acids Research 50(D1):D1368 (2022)，DOI `10.1093/nar/gkab1050`
- RCSB 条目：以 <https://www.rcsb.org/structure/1HH6> 为 URL 格式，其余 492 个 ID 见“PDB 数据库”；各条目页的 Primary Citation 给出原始结构论文

## 其他

### 数据范围和限制

本数据集只覆盖 SAbDab 中抗原为蛋白或肽的条目。糖类、小分子、病毒颗粒与未注释抗原被排除，因此它不代表 SAbDab 全库，也不代表抗体—抗原结合的全体测量类型。

`Y` 只给出数值，不给出测量方法、温度、pH、缓冲体系与重复次数。跨行比较亲和力绝对值时，这些未记录的差异会引入无法估计的误差；同一抗原下比较不同抗体（排序任务）受此影响较小，但也未经过本数据集的验证。

493 行由 493 个不同 PDB 条目构成，因此每一行都是不同结构背景下的测量，不能把它们当作同一抗体在同一抗原上的重复测量；反过来，按抗体序列分组时同一抗体可能出现在多个条目里，随机划分会造成近邻泄漏。

### 完整性与验收

| 文件 | 大小 | SHA-256 | MD5（Dataverse 官方） |
| --- | ---: | --- | --- |
| `protein_sabdab.csv` | 322.56 KiB（330,303 bytes） | `4f655925751b67331fa008001c6ca6d6d80a6d1ca736b8d89c89fca28c70b0af` | `f4d0dba68859f7ae2a042bd90423b22b` |

MD5 由 Dataverse 文件元数据给出，本次下载后复核一致；SHA-256 为本地计算，用于后续不依赖 MD5 的复核。CSV 可正常解析为 493 行 × 6 列，字段类型与长度范围已逐列统计，未发现截断或编码异常。

`pdb/` 的 982 个文件、607,146,339 bytes 已逐文件生成 SHA-256 并折叠为 inventory 摘要；两个缺失锚点的原因已由 RCSB 撤销记录确认，不作静默补齐。

### 许可和再分发边界

两层来源给出不同许可：

- TDC 任务页面在页面底部标注本数据集为 Creative Commons Attribution 3.0（CC BY 3.0），并链接到 <https://creativecommons.org/licenses/by/3.0/>。
- Harvard Dataverse 的 dataset 级许可字段为 `CC0 1.0`（Public Domain Dedication），覆盖整个 `doi:10.7910/DVN/21LKWG` 数据集。

两者对再分发的要求不同：CC0 不要求署名，CC BY 3.0 要求保留署名。本次未找到能说明哪一层优先的一手说明，因此按更严格的一侧（CC BY 3.0）使用，并要求署名 TDC 与 SAbDab。上游 SAbDab 自身条款未在本次取得范围内核对，若需再分发应另行追溯。该差异转入 `Q04`。

`pdb/` 内的 RCSB 文件适用 RCSB 自身条款，使用时应保留相应条目的原始结构引用。

### 公开范围对照

| 来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 493 个抗体—抗原配对 | CSV 493 行，493 个不同 `ID1` | 已包含 |
| 431 个抗体 | `X1` 序列去重后 431 个 | 已包含 |
| 401 个抗原 | `X2` 序列去重后 401 个 | 已包含 |
| 只保留蛋白/肽抗原 | `X2` 长度 3—1,676 aa，107 行不超过 20 aa | 已包含 |
| 抗体序列重链在前、轻链在后 | 493 行 `X1` 均为 2 元素列表 | 已包含；无独立链角色列 |
| 亲和力回归任务、建议取对数 | `Y` 为 4×10⁻¹³—2×10⁻⁴ 的连续值 | 已包含；单位与方法未标注 |
| 随机划分 | 公开 CSV 不含划分列 | 未包含于 CSV；由 loader 运行时生成 |
| SAbDab 原始记录与筛选脚本 | 未发现 | 未公开 |
| 逐条测量的方法、条件与误差 | 未发现 | 未公开 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-29；待取得全文）：TDC 平台论文 *Artificial intelligence foundation for therapeutic science* 的正文未能在本次取得。已核实 DOI、PMID `36131149`、PMCID `PMC9529840` 与题名，PMC PDF 入口返回 403、Europe PMC `fullTextXML` 与 `fulltextRepo` 返回 500 与 403、Nature PDF 直链返回 HTML 页。影响：论文中的数据集描述与统计口径只能依据 TDC 任务页，未经原文核对。当前处理：README 的论文条目记录在线入口与未归档状态，不虚构本地文件。下一步：通过机构订阅或其他合法入口取得 PDF 后补做身份核验并归档，关闭条件为字节数、SHA-256 与页内 DOI 一致。
- `Q02`（最近更新：2026-10-29；待上游说明）：`Y` 列未标注测量类型、单位与实验条件。已核实取值为 4×10⁻¹³—2×10⁻⁴ 的连续数、383 个不同值，量级与摩尔浓度 KD 相符。影响：不能确认整列是否为 KD，也不能把它与 IC50、EC50 混用；跨行绝对比较缺少条件信息。当前处理：README 只记录数值与量级，不解释为单位化的 KD。下一步：核对 SAbDab 原始记录的 `affinity_type` 字段或 TDC 生成脚本后关闭。
- `Q03`（最近更新：2026-10-29；待方法细节）：`ID2` 有 313 个名称而 `X2` 有 401 条序列，名称与序列不是一一对应。已核实 `ID2` 包含自由文本与复合描述（如含逗号的嵌合体名称）。影响：按 `ID2` 分组与按 `X2` 分组会得到不同的抗原集合，进而影响“同抗原排序”这类任务的分组正确性。当前处理：README 明确给出两个计数并建议按序列分组。下一步：核对上游是否存在一对多映射表，或确认是否只是命名不一致。
- `Q04`（最近更新：2026-10-29；待权利方澄清）：TDC 任务页标注 `CC BY 3.0`，Harvard Dataverse dataset 标注 `CC0 1.0`，两者对署名要求不同。已核实两个页面的原文与链接。影响：再分发时的署名义务取决于适用哪一层。当前处理：按更严格的一侧执行，要求署名 TDC 与 SAbDab。下一步：确认 Dataverse 的 dataset 级许可是否覆盖每个文件，或取得 TDC 对文件级许可的说明后关闭。
- `Q05`（最近更新：2026-10-29；信息缺口）：`3RVV` 与 `3RVW` 于 2022-04-27 被 RCSB 撤销，替代条目分别为 `5VPL` 与 `5VPG`。已核实 RCSB `holdings/removed` 返回的 `remove_date`、`id_codes_replaced_by`，且两个替代条目本身已在 493 个锚点中并已取得 FASTA 与 mmCIF。影响：这 2 行的结构锚点无法按原 ID 取得，但可通过替代条目追溯；本表保留原 ID 不变。当前处理：README 记录缺失原因与替代关系，不用替代条目回填文件名。下一步：确认替代条目与原始条目的序列是否一致，若一致可在使用阶段建立等价映射。
