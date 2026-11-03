---
- tags:
  - context
---

# SRC_R20_SABDAB 数据说明

## 数据集身份

- `source_id`：`SRC_R20_SABDAB`
- `source_version`：`snapshot-2026-09-11`
- 原作者或发布机构：Oxford Protein Informatics Group / Capel 等

### 来源方背景

[SAbDab 官方服务](https://sabdab.opig.stats.ox.ac.uk/)由牛津大学 Oxford Protein Informatics Group 提供；[SAbDab2 论文](https://doi.org/10.64898/2026.06.16.732554)将结构数据库的维护与链识别、编号和抗原注释方法联系起来。服务发布的是对 PDB 结构的整理视图，原始坐标与实验结合测量仍需分别追溯。

## 实验设计和数据口径

SAbDab2 从 PDB 抗体结构整理分子链、CDR、抗原和构建体注释。本次官方 last_update 为 2026-09-11，summary 实际 22,264 个 antibody instances、11,604 个 PDB accession。INSTANCE 是结构内实例，SABDAB_ID 合并相同抗体链身份；这些行不是独立结合实验或 KD 测量。antigen_type 包含蛋白、hapten、ion 等，不能把全部行当成蛋白抗原复合物。PDB structure 导出与外部 RCSB canonical entry 是不同层；前者可能带重编号和数据库注释，后者完整原样补充。

主文先对 PDB 蛋白序列用 ANARCII 识别/编号 antibody segments，再配对分类，按空间邻近注释抗原；链分段、重命名、结构编号和服务注释属于上游处理。实例 ID 与跨 PDB 共享的 SAbDab2 分子 ID 是不同粒度；服务导出的重编号结构不能代替 RCSB full-entry 原样参考文件。论文另给出的历史 ML-grade 训练/测试快照不是本次动态全量快照。 主文完整 8 页（2026-06-20 bioRxiv v1）已阅读，无另列外部 supplementary-media。主文五月规模与九月服务快照不同；本次 22,264 个唯一 INSTANCE、11,604 个 PDB entries、6,897 个唯一 SABDAB_ID，三者是不同粒度。作者重/轻链在 conserved IMGT 104 的 Cα 距离 <22 Å 时配对，22–28 Å 人工审核；蛋白/肽抗原依据 CDR 与 Cα/Cβ 的 7.5 Å 邻近，其他非水分子按 7.0 Å，并限制作者 biological assembly。这是结构邻近注释，不是实验 KD 或阴性标签。ML-grade 的 ≤3.5 Å、cropping/quality filters 及聚类 train/test splits 属另一 Zenodo 数据包，不能把其过滤条件套在本次全量服务快照。

## 论文原文

- 标题：SAbDab2: The structural antibody database in the age of machine learning
- 作者：Henriette L. Capel；Odysseas Vavourakis；Benjamin H. Williams；Christopher R. Taylor；Charlotte M. Deane
- 载体与版本：bioRxiv v1
- 发布日期：2026-06-20
- DOI：`10.64898/2026.06.16.732554`
- PMID / PMCID：未在本记录核验 / 未在本记录核验
- 本地文件：`articles/SABDAB_2026-06-20_bioRxiv-v1.pdf`
- 文件大小：1.37 MiB（1,440,043 bytes）
- SHA-256：b97d9d2e664d17753c47b6d1e50b6dc590e7c18bfae106b6cf1e28b3064241a2
- 文本许可：见出版方原文及 Crossref license URL；未把论文许可移用于数据
- 补充材料：经 8 页 bioRxiv v1 完整 PDF 检查，未列独立 supplement 附件。主文提到的历史 ML-grade Zenodo 快照与本次官方动态 summary/全结构导出不是同一范围，不以历史训练集代替当前来源。

## 仓库内容

来源身份：

- `kind`：`dynamic-api-export`
- `official_page`：`https://sabdab.opig.stats.ox.ac.uk`
- `snapshot_basis`：`Official last_update: Fri 11 Sep 2026 00:03:54`

版本日期来自数据源 commit 或官方更新时间；正式版本名保留官方名称。以下树为已验收的上游 payload，不列项目 README、论文及 PDB 外部补充。

```text
snapshot-2026-09-11/
└── SAbDab2/
    ├── sabdab2_summary.csv
    ├── sabdab_search_structures_20260918T143233.tar
```

## 数据结构

### 原始交付与记录

| 原始文件 / sheet | 非空记录数 | 字段数 | 精确重复行 |
| --- | --- | --- | --- |
| `SAbDab2/sabdab2_summary.csv` | 22264 | 53 | 0 |

只统计实际已解析的文件，未把来源介绍规模当作本次落盘统计。

官方更新时间 2026-09-11 的动态全量快照，无独立数据发布版本号，命名 snapshot-2026-09-11。两份官方来源文件完整取得，共 2.60 GiB（2,792,996,282 bytes）。导出 tar 有 11,605 个普通成员：与独立 CSV 字节完全一致的 SAbDab_summary.csv，加 11,604 个 full_structures/*.cif.gz。已逐一完整解压 gzip（含 CRC/trailer）、解析整个 mmCIF、核对 entry ID 与文件名和 CSV PDB 集合，一对一覆盖全部 11,604 个 accepted PDB entries。服务坐标为 model 1（CSV 使用零起始 model=0），共 127,597,709 个 atom records，解压坐标 9.59 GiB（10,300,757,479 bytes）；完整服务结构 inventory SHA-256 e821deb88d471439d5d096142d7b20fef3f0cb769946b5d1e028c80bd0289b7a。服务结构是作者重编号交付，RCSB canonical full-entry 坐标独立补充且保留完整原生实体/坐标，不互相替代。

### 字段说明

INSTANCE、PDB、SABDAB_ID、HEAVY_ID、LIGHT_ID 为实例和分子身份；Hchain/Lchain 是源链。VH/VL、CDR-H1…H3、CDR-L1…L3 为结构注释的序列，不自动等于全部实验构建体。antigen_chain、antigen_type、antigen_name 的 | 分隔项须对应读取；date 与 SABDABdepo_date/update_date 是不同时间口径。model、method、resolution、r_free/r_factor 描述结构，不是实验结合标签。type 和 construct 列描述分子格式。缺少 light 或 antigen 的实例不自动作为阴性。

CSV 共 53 字段。类型实际为 FAB 10470、FV 6954、SD-H 4614、SD-L 95、FAB+FC 40、VNAR 91。VH、VL 为上游 variable-domain 序列，不等于完整 IgG/整条多域原始 PDB polymer；缺失链与空 CDR 原样保留：VL/CDR-L1/L2/L3 各空 4705，VH/CDR-H3 空 95、CDR-H1 空 96、CDR-H2 空 189；所有非空 sequence 字段未发现非法字符。没有 KD/ΔG/affinity 数值列。INSTANCE 是具体 entry 的 antibody logical chain instance，SABDAB_ID 聚合同 IMGT variable-domain 编号序列，HEAVY_ID/LIGHT_ID 单独分组。Hchain/Lchain 使用服务 logical author-chain 标签，可能因 multi-domain splitting 与 RCSB 原始 author chain 不同，必须通过上游保留的 label_asym_id/label_seq_id 核对映射。antigen_chain/type/name 的 | 为同一 instance 的多抗原列表，不拆成额外实验测量。resolution 单位 Å，r_free/r_factor 为晶体学质量统计而不是 affinity，方法 XRAY/EM/NMR/scattering 等缺失统计保留；date/depo/update 各按原始日期格式读取，不把 export-job 创建日当数据版本日。

实际表头（保留原始字段名）：

- `SAbDab2/sabdab2_summary.csv`：`INSTANCE`、`PDB`、`SABDAB_ID`、`HEAVY_ID`、`LIGHT_ID`、`Hchain`、`Lchain`、`VH`、`CDR-H1`、`CDR-H2`、`CDR-H3`、`VL`、`CDR-L1`、`CDR-L2`、`CDR-L3`、`model`、`antigen_chain`、`antigen_type`、`antigen_name`、`short_header`、`date`、`SABDABdepo_date`、`SABDABupdate_date`、`compound`、`organism`、`organism_taxid`、`expression_system`、`expression_system_taxid`、`heavy_species`、`light_species`、`heavy_taxid`、`light_taxid`、`heavy_expression_system`、`light_expression_system`、`heavy_expression_system_taxid`、`light_expression_system_taxid`、`antigen_species`、`agtaxid`、`agexpression_system`、`agexpression_system_taxid`、`authors`、`method`、`resolution`、`r_free`、`r_factor`、`type`、`chainsharing_construct`、`chainsharing_construct_partners`、`non_chainsharing_construct`、`non_chainsharing_construct_partners`、`heavy_subclass`、`light_subclass`、`light_ctype`

字段原始表示与缺失统计（只统计审计解析结果，不在 raw 中填零）：

- `SAbDab2/sabdab2_summary.csv`：缺失/特殊表示计数 `{"antigen_species": 5213, "agtaxid": 5219, "agexpression_system": 6090, "agexpression_system_taxid": 6095, "chainsharing_construct": 20473, "chainsharing_construct_partners": 22110, "non_chainsharing_construct": 22182, "non_chainsharing_construct_partners": 22182, "heavy_subclass": 15017, "light_subclass": 15202, "r_free": 9705, "r_factor": 9440, "LIGHT_ID": 4705, "Lchain": 4705, "VL": 4705, "CDR-L1": 4705, "CDR-L2": 4717, "CDR-L3": 4705, "light_species": 4744, "light_taxid": 4756, "light_expression_system": 6909, "light_expression_system_taxid": 6917, "light_ctype": 4705, "antigen_chain": 2351, "antigen_type": 2351, "antigen_name": 2351, "expression_system": 2238, "expression_system_taxid": 2246, "heavy_expression_system": 2338, "heavy_expression_system_taxid": 2346, "HEAVY_ID": 95, "Hchain": 95, "VH": 95, "CDR-H1": 96, "CDR-H2": 189, "CDR-H3": 95, "heavy_species": 152, "heavy_taxid": 164, "resolution": 47, "organism_taxid": 67, "organism": 55}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

### 数据示例

来自 `SAbDab2/sabdab2_summary.csv` 的第一条真实记录；这里只摘录字段，不改写原始文件。

| 字段 | 原样值 |
| --- | --- |
| `INSTANCE` | `pdb_000010bt-A-E` |
| `PDB` | `pdb_000010bt` |
| `SABDAB_ID` | `sabdab2_H0635L00BE` |
| `HEAVY_ID` | `H0635` |
| `LIGHT_ID` | `L00BE` |
| `Hchain` | `A` |
| `Lchain` | `E` |

每行按该来源的测量、配对或结构实例口径解释，不把结构表示或 replicate 当作新实验。完整字段保留在 payload 中。

## PDB 数据库

已从实际 `sabdab2_summary.csv` 的 PDB 字段确定 11,604 个唯一 entry，并分别取得原生 FASTA 与完整 mmCIF。该审计证明 entry 级覆盖；服务对同一 PDB 的多个 `INSTANCE` 可使用经拆分或重编号的逻辑链，不能据完整 entry 文件自动断言每个实例的链角色和原始 author/label 链一一对应。

当前接受锚点清单为 11604 个；最后一次审计有 0 个未完成两层配对。每个锚点取原样 per-entry FASTA 和完整 mmCIF，不嫁接 CDR、不生成逐变体重建序列。FASTA 的原始 header 保留 polymer entity 与 author/label chain；不猜测伙伴角色。只有全部接受锚点同时通过 FASTA 和坐标解析，且 FASTA entity ID 集合和完整序列与 mmCIF 的 canonical polymer 一致，才算完成。

PDB 文件审计摘要：23208 个文件，15.39 GiB（16,522,270,262 bytes）；inventory SHA-256：`63d09cc14fadfcfbc2d2bf251dc642d086209f88473b1c504eb02d57bf8ab8b5`。摘要按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接计算。缓存最初包含选择链/重写 header 的 FASTA，已清理本轮这类 staging 副本；现在只接受 RCSB native per-entry header。

## 使用方式

由调用者先赋值 `dataset_root`（Path），再读取；不在这里清洗或转换标签。

```python
import pandas as pd
table = pd.read_csv(dataset_root / "SAbDab2/sabdab2_summary.csv")
```

## 采集过程记录

2026-09-18：读取项目规范和执行清单，解析一手 API/tree/Drive 对象 metadata，固定本轮版本与文件身份。下载到共享 source 下 `.staging/<version>.partial`；HTTP 大文件使用精确 byte range 和全文件上游 checksum，Drive 保留对象 ID、MIME 与字节数，失败部分可续传。2026-09-18 按用户要求调整本轮 HTTP 为直连优先、连接失败回退环境代理，15 分钟后重试直连；各线程复用连接且保留 TLS/CA 校验。重启任务保留所有文件断点。

独立 audit 重新计算 hash、完整解析已取得表格并检查 PDB 两层文件；归档只有完成逐成员/CRC 与路径安全检查后才通过。PMC 访问被拒绝、非 OA XML 不可得和间歇代理连接失败均保留缺口，未关闭 TLS 验证。PDB 缓存原始性检查发现错误后清理本轮衍生 header 文件并重做。

README 草稿每次写入后立即同步到 staging 同名文件，随后运行 skill 固定 Markdownlint 配置。发布脚本仅在逐文件、论文/PDB、README 同步与固定格式检查通过后原子发布；发布状态与 接入过程记录 同步。

2026-09-18：主文从 `SAbDab2_bioRxiv-2026.06.16.732554v1.pdf` 改名为 `SABDAB_2026-06-20_bioRxiv-v1.pdf`，日期取该论文版本发布日期，改名前后大小和 SHA-256 一致。

2026-09-18：沿用原官方 export job，断点下载完整 tar 并独立检查全部成员与来源 identity。逐个原样 gzip、完整 mmCIF 与 CSV/PDB coverage 内容核验通过。最后 2ADJ 原始 FASTA 因 TLS 连接失败，定向重试取得完整 native FASTA/mmCIF 并核对全 polymer。官网部署前端完整 bytes 与首页公开说明分别核实 CC BY 4.0，撤销没有一手许可证据的旧 blocker。完成内容审阅后交发布脚本重验 native 全覆盖及所有文件，固定 Markdownlint 为 0 errors 后原子发布。

2026-10-09：按新版 README 合同将 PDB 审计的旧“进行中”状态改为已完成的 11,604 对 entry 级覆盖，补充实例级链映射边界和动态待办；两份官方 payload、论文及 RCSB 文件未改动。

## 参考文献

- <https://www.biorxiv.org/content/10.64898/2026.06.16.732554v1.full.pdf>
- <https://doi.org/10.64898/2026.06.16.732554>
- <https://sabdab.opig.stats.ox.ac.uk>
- <https://www.rcsb.org/>
- <https://sabdab.opig.stats.ox.ac.uk/>

## 其他

### 完整性与验收

上游声明 2 个文件；最近审计通过 2 个，待取得/核验 0 个。

公开包独立验收、论文/补充材料对照及 PDB 配对审计通过；不宣称全部底层实验数据取得。没有独立 manifest/API 响应/审计 JSON 发布在 source version 中；临时产物只保存在共享 cache。

| 上游 payload | 大小 | SHA-256 |
| --- | --- | --- |
| `SAbDab2/sabdab2_summary.csv` | 16.49 MiB（17,290,682 bytes） | `176ff3a7b5dd901ae1055cf9e1b71122c1b63add4053c1fcd7bea0577604f1a6` |
| `SAbDab2/sabdab_search_structures_20260918T143233.tar` | 2.59 GiB（2,775,705,600 bytes） | `13a8c7d9e24873ce471b0dd01bf8f77ff881471f3f7ad03e49af0cd712b37761` |

### 许可和再分发边界

SAbDab2 官网首页明确服务数据采用 CC BY 4.0；论文同样声明 CC BY 4.0，但二者是分别核验的声明。PDB 原始条目保留 RCSB/wwPDB 条件与引用，服务派生编号/注释保留作者与快照引用。

官网首页明确数据按 CC BY 4.0 提供，已同时查证首页公开文本及实际部署 frontend bundle index-BaHLkXjt.js 的许可链接（<https://creativecommons.org/licenses/by/4.0/>）。2026-09-18 原部署 JS：3.84 MiB（4,030,119 bytes），SHA-256 a7cf2c0ef8afb26bc1289d3e57137614c4f980bed69a682f29e53f82d1cb6cb9，HTML/JS 证据只在 shared cache。数据许可来自服务自身声明，论文 CC BY 4.0 为独立声明，PDB 文件按 wwPDB/RCSB 原始数据条件处理。

### 公开范围对照

| 目标组成 | 当前证据 | 状态 |
| --- | --- | --- |
| 固定上游 payload | tracked config + 独立文件/格式审计 | 目标公开文件验收通过 |
| 论文原文 | 一手 DOI 和取得文件 hash；不可得项明确记录 | 主文与全部被引用附件已归档并解析 |
| PDB 原始序列与全坐标 | 接受锚点两层配对审计 | 两层已齐；非逐变体结构 |
| 完整研究底层数据 | 公开汇编或处理包不等于全部底层实验 | 未宣称获得 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-09；影响实例级结构使用，不阻塞 entry 级接入）：22,264 个 `INSTANCE` 共享 11,604 个 PDB entry，服务结构可能拆分或重编号链。全部 11,604 对 RCSB FASTA/mmCIF 已验收，但尚未对每个实例建立服务逻辑链至原始 author/label 链的可核验映射。当前只声明 entry 级覆盖，不把相同 PDB ID 当成实例级精确链标签；拟使用的实例子集按服务 `label_asym_id`、`label_seq_id` 与完整 mmCIF 逐项核对后关闭相应范围。
