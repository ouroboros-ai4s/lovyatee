---
tags:
  - context
---

# SRC_R11_ABBIBENCH 数据说明

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

- `source_id`：`SRC_R11_ABBIBENCH`
- `source_version`：`snapshot-2026-05-02`
- 原作者或发布机构：AbBiBench 作者团队（Xinyan Zhao 等）

### 来源方背景

[论文 v2 作者与单位页](https://arxiv.org/html/2506.04235v2)列有 UTHealth Houston 的 McWilliams School of Biomedical Informatics、Texas Therapeutics Institute，以及其他合作单位。作者团队将已有抗体突变结合研究整理为评价基准；这里的发布责任主体是 AbBiBench 作者团队，不是各原始实验的统一执行机构。

## 实验设计和数据口径

AbBiBench 汇编抗体突变的结合实验信号，以抗体—抗原参考复合物为结构背景，用于亲和力成熟和设计评价。实际 HF 快照含 17 张 CSV，重链、轻链序列和 binding_score 三类列；字段顺序不完全相同。binding_score 是上游各研究整理的信号，不据统一列名假定所有表都是相同单位的实测 KD。只能按上游研究、抗原、抗体背景和实验端点建立比较组。论文 v2 摘要称超过 184,500 次测量，不能替代本快照的实际行数。AAYL 别名及 Zenodo mutant_structure 是模型/派生结构交付，不把每个模型等同于独立实验复合物。

当前固定 HF 快照有 17 张 CSV；论文主表的 14 assays、内嵌 supplement 所述 16 assays 与此文件数不同，不能以文件数当独立实验数量。作者汇编 phage/yeast display 等研究的变体；论文说明 KD 使用负对数、enrichment 使用对数，使其基准分数的大值对应较强结合。逐表原始观察量、转换底数和阈值仍需与各原研究及生成代码核对，不能套用原 KD 的小值方向，也不能把不同 assay 的 `binding_score` 当成统一物理单位。后验模型分数和 mutant 模型坐标不是独立实验标签或实验结构。

## 论文原文

- 标题：AbBiBench: A Benchmark for Antibody Binding Affinity Maturation and Design
- 作者：Zhao, Xinyan；Tang, Yi-Ching；Singh, Akshita；Cantu, Victor J；An, KwanHo；Lee, Junseok；Stogsdill, Adam E；Hamdi, Ibraheem M；Ramesh, Ashwin Kumar；An, Zhiqiang；Jiang, Xiaoqian；Kim, Yejin
- 载体与版本：arXiv v2
- 发布日期：2025-10-10
- DOI：`10.48550/arXiv.2506.04235`
- PMID / PMCID：未在本记录核验 / 未在本记录核验
- 本地文件：`articles/ABBIBENCH_2025-10-10_arXiv-v2.pdf`
- 文件大小：1003.93 KiB（1,028,025 bytes）
- SHA-256：7009bb93e8eba70952d62635852ecb3b514aa760166771f5330134fd20712a2f
- 文本许可：见出版方原文及 Crossref license URL；未把论文许可移用于数据
- 补充材料：无独立补充文件；arXiv v2 完整 PDF 共 27 页，第 16–27 页内嵌 Supplement Materials（数据、测量口径与计算方法），已逐页检查，不另造附件。

## 仓库内容

来源身份：

- `kind`：`huggingface+zenodo`
- `repository`：`AbBibench/Antibody_Binding_Benchmark_Dataset`
- `revision`：`556fd6913aa231c0d342a8658818be8f963fd582`
- `commit_date`：`2026-05-02T16:03:59.000Z`

版本日期来自数据源 commit 或官方更新时间；正式版本名保留官方名称。以下树为已验收的上游 payload，不列项目 README、论文及 PDB 外部补充。

```text
snapshot-2026-05-02/
└── ABBIBENCH/
    ├── README.txt
    ├── mutant_structure.tar.gz
└── Antibody_Binding_Benchmark_Dataset/
    ├── .DS_Store
    ├── .gitattributes
    ├── README.md
    ├── binding_affinity/1mhp_LC_benchmarking_data.csv
    ├── binding_affinity/1mlc_benchmarking_data.csv
    ├── binding_affinity/1n8z_benchmarking_data.csv
    ├── binding_affinity/2fjg_benchmarking_data.csv
    ├── binding_affinity/3gbn_h1_benchmarking_data.csv
    ├── binding_affinity/3gbn_h9_benchmarking_data.csv
    ├── binding_affinity/4d5_her2_benchmarking_data_trimmed.csv
    ├── binding_affinity/4fqi_h1_benchmarking_data.csv
    ├── binding_affinity/4fqi_h3_benchmarking_data.csv
    └── …（其余来源文件保留原路径）
```

## 数据结构

### 原始交付与记录

| 原始文件 / sheet | 非空记录数 | 字段数 | 精确重复行 |
| --- | --- | --- | --- |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/1mhp_LC_benchmarking_data.csv` | 69 | 3 | 2 |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/1mlc_benchmarking_data.csv` | 1229 | 3 | 0 |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/1n8z_benchmarking_data.csv` | 419 | 3 | 0 |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/2fjg_benchmarking_data.csv` | 2223 | 3 | 0 |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/3gbn_h1_benchmarking_data.csv` | 1887 | 3 | 0 |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/3gbn_h9_benchmarking_data.csv` | 1842 | 3 | 0 |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/4d5_her2_benchmarking_data_trimmed.csv` | 2080 | 3 | 0 |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/4fqi_h1_benchmarking_data.csv` | 65094 | 3 | 0 |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/4fqi_h3_benchmarking_data.csv` | 65535 | 3 | 0 |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/5a12_ang2_benchmarking_data.csv` | 944 | 3 | 0 |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/5a12_vegf_benchmarking_data.csv` | 29981 | 3 | 0 |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl49_ML_benchmarking_data.csv` | 8953 | 3 | 0 |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl49_benchmarking_data.csv` | 4312 | 3 | 0 |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl50_LC_benchmarking_data.csv` | 11473 | 3 | 0 |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl51_benchmarking_data.csv` | 4320 | 3 | 0 |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl52_LC_benchmarking_data.csv` | 13324 | 3 | 0 |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/g6_LC_benchmarking_data.csv` | 2014 | 3 | 0 |

只统计实际已解析的文件，未把来源介绍规模当作本次落盘统计。

本次 17 张 CSV 共 215,699 行（不是去重后的独立对象），与论文的 184,500+、14 主表 assays/16 supplementary assays 分别保留。重链长度有 117–121 aa 和 211/215 aa，轻链有 107–115 aa 和 213 aa；因此不能把所有链称为全长 IgG，也不能把它们全称为同一可变区长度。全部链字符串无 X 和本轮约定字符集之外字符。所有 binding_score 可解析为有限数值，但跨 assay 不能据此直接比较绝对亲和力。模型归档有 88,946 个 .pdb，9 个分组：4fqi 65,536、2fjg 2,223、1n8z 419、aayl51 4,320、1mlc 1,229、aayl49_ML 8,953、3gbn 1,917、1mhp 37、aayl49 4,312。逐个成员读到 FoldX/BuildModel 标记及原始 ATOM 坐标；完整 gzip trailer 和所有 88,956 个成员已审计。模型数量不等于表行数，归档不覆盖每个 2026 HF 表；例如较新的 5a12 两表没有本模型包对应分组。没有稳定行级键时不靠文件顺序声称模型与表一一对应。

### 字段说明

heavy_chain_seq、light_chain_seq 是上游给出的氨基酸序列；binding_score 为原样数值，具体单位、有利方向和处理方法必须逐表回到原实验核验。metadata.json 给出共享结构、链和 affinity_data 路径，部分路径在当前 tree 中不存在；缺失路径不自行重命名修复。

heavy_chain_seq/light_chain_seq 为来源字符串（链范围按各 assay/construct 解释）；binding_score 的负 log KD 或 log enrichment 方向来自主文 Methods 及内嵌 supplement，大值更有利；不能由同一字段名推定所有读出是统一单位的 KD。每张表的列顺序、真实行数和 raw 缺失统计如下保留。metadata 的 1mlc_LC、1mhp affinity_data 指向本固定 tree 不存在的 CSV；这是上游注释漂移，不把已有文件改名或补造缺失表。5a12_vegf 的 epitope/paratope 注释与 antigen_chain 声明存在冲突，后续伙伴/位点选择须再核验；canonical 完整条目不按这些弱注释删链。

实际表头（保留原始字段名）：

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/1mhp_LC_benchmarking_data.csv`：`heavy_chain_seq`、`light_chain_seq`、`binding_score`

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/1mlc_benchmarking_data.csv`：`heavy_chain_seq`、`binding_score`、`light_chain_seq`

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/1n8z_benchmarking_data.csv`：`heavy_chain_seq`、`binding_score`、`light_chain_seq`

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/2fjg_benchmarking_data.csv`：`heavy_chain_seq`、`binding_score`、`light_chain_seq`

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/3gbn_h1_benchmarking_data.csv`：`heavy_chain_seq`、`binding_score`、`light_chain_seq`

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/3gbn_h9_benchmarking_data.csv`：`heavy_chain_seq`、`binding_score`、`light_chain_seq`

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/4d5_her2_benchmarking_data_trimmed.csv`：`heavy_chain_seq`、`light_chain_seq`、`binding_score`

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/4fqi_h1_benchmarking_data.csv`：`heavy_chain_seq`、`binding_score`、`light_chain_seq`

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/4fqi_h3_benchmarking_data.csv`：`heavy_chain_seq`、`binding_score`、`light_chain_seq`

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/5a12_ang2_benchmarking_data.csv`：`heavy_chain_seq`、`light_chain_seq`、`binding_score`

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/5a12_vegf_benchmarking_data.csv`：`heavy_chain_seq`、`light_chain_seq`、`binding_score`

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl49_ML_benchmarking_data.csv`：`heavy_chain_seq`、`binding_score`、`light_chain_seq`

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl49_benchmarking_data.csv`：`heavy_chain_seq`、`binding_score`、`light_chain_seq`

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl50_LC_benchmarking_data.csv`：`heavy_chain_seq`、`light_chain_seq`、`binding_score`

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl51_benchmarking_data.csv`：`heavy_chain_seq`、`binding_score`、`light_chain_seq`

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl52_LC_benchmarking_data.csv`：`heavy_chain_seq`、`light_chain_seq`、`binding_score`

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/g6_LC_benchmarking_data.csv`：`heavy_chain_seq`、`light_chain_seq`、`binding_score`

字段原始表示与缺失统计（只统计审计解析结果，不在 raw 中填零）：

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/1mhp_LC_benchmarking_data.csv`：缺失/特殊表示计数 `{}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/1mlc_benchmarking_data.csv`：缺失/特殊表示计数 `{}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/1n8z_benchmarking_data.csv`：缺失/特殊表示计数 `{}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/2fjg_benchmarking_data.csv`：缺失/特殊表示计数 `{}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/3gbn_h1_benchmarking_data.csv`：缺失/特殊表示计数 `{}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/3gbn_h9_benchmarking_data.csv`：缺失/特殊表示计数 `{}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/4d5_her2_benchmarking_data_trimmed.csv`：缺失/特殊表示计数 `{}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/4fqi_h1_benchmarking_data.csv`：缺失/特殊表示计数 `{}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/4fqi_h3_benchmarking_data.csv`：缺失/特殊表示计数 `{}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/5a12_ang2_benchmarking_data.csv`：缺失/特殊表示计数 `{}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/5a12_vegf_benchmarking_data.csv`：缺失/特殊表示计数 `{}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl49_ML_benchmarking_data.csv`：缺失/特殊表示计数 `{}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl49_benchmarking_data.csv`：缺失/特殊表示计数 `{}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl50_LC_benchmarking_data.csv`：缺失/特殊表示计数 `{}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl51_benchmarking_data.csv`：缺失/特殊表示计数 `{}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl52_LC_benchmarking_data.csv`：缺失/特殊表示计数 `{}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `Antibody_Binding_Benchmark_Dataset/binding_affinity/g6_LC_benchmarking_data.csv`：缺失/特殊表示计数 `{}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

### 数据示例

来自 `Antibody_Binding_Benchmark_Dataset/binding_affinity/1mhp_LC_benchmarking_data.csv` 的第一条真实记录；这里只摘录字段，不改写原始文件。

| 字段 | 原样值 |
| --- | --- |
| `binding_score` | `8.924453038607469` |

每行按该来源的测量、配对或结构实例口径解释，不把结构表示或 replicate 当作新实验。完整字段保留在 payload 中。

## PDB 数据库

metadata.json pdb fields; shared experimental reference complexes, not per-mutant structures. AAYL model aliases are not PDB accessions.

当前接受锚点清单为 8 个；最后一次审计有 0 个未完成两层配对。每个锚点取原样 per-entry FASTA 和完整 mmCIF，不嫁接 CDR、不生成逐变体重建序列。FASTA 的原始 header 保留 polymer entity 与 author/label chain；不猜测伙伴角色。只有全部接受锚点同时通过 FASTA 和坐标解析，且 FASTA entity ID 集合和完整序列与 mmCIF 的 canonical polymer 一致，才算完成。

PDB 文件审计摘要：16 个文件，6.40 MiB（6,710,298 bytes）；inventory SHA-256：`e7ff0f8859b8d7e438b5bb7746c3c1ae8e4fb8ca7afa7bcbf2c7fa798760808f`。摘要按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接计算。缓存最初包含选择链/重写 header 的 FASTA，已清理本轮这类 staging 副本；现在只接受 RCSB native per-entry header。

## 使用方式

由调用者先赋值 `dataset_root`（Path），再读取；不在这里清洗或转换标签。

```python
import pandas as pd
table = pd.read_csv(dataset_root / "Antibody_Binding_Benchmark_Dataset/binding_affinity/1mlc_benchmarking_data.csv")
```

## 采集过程记录

2026-09-18：读取项目规范和执行清单，解析一手 API/tree/Drive 对象 metadata，固定本轮版本与文件身份。下载到共享 source 下 `.staging/<version>.partial`；HTTP 大文件使用精确 byte range 和全文件上游 checksum，Drive 保留对象 ID、MIME 与字节数，失败部分可续传。2026-09-18 按用户要求调整本轮 HTTP 为直连优先、连接失败回退环境代理，15 分钟后重试直连；各线程复用连接且保留 TLS/CA 校验。重启任务保留所有文件断点。

独立 audit 重新计算 hash、完整解析已取得表格并检查 PDB 两层文件；归档只有完成逐成员/CRC 与路径安全检查后才通过。PMC 访问被拒绝、非 OA XML 不可得和间歇代理连接失败均保留缺口，未关闭 TLS 验证。PDB 缓存原始性检查发现错误后清理本轮衍生 header 文件并重做。

README 草稿每次写入后立即同步到 staging 同名文件，随后运行 skill 固定 Markdownlint 配置。发布脚本仅在逐文件、论文/PDB、README 同步与固定格式检查通过后原子发布；发布状态与 接入过程记录 同步。

2026-09-18：主文从 `AbBiBench_arxiv-2506.04235v2.pdf` 改名为 `ABBIBENCH_2025-10-10_arXiv-v2.pdf`，日期取该论文版本发布日期，改名前后大小和 SHA-256 一致。

2026-09-18：结构包断点恢复后全部 37 个文件独立 checksum 通过；全归档验收完成后，review_ready_content.py 对全部 17 表检查数值/链长度/特殊字符，对全部 88,946 个模型成员检查原始 provenance header 和 ATOM 表达，并复核 metadata 的失效路径。主文 27 页及内嵌第 16–27 页 supplement 已阅读、身份核验。8 个 canonical PDB 全实体序列与完整 mmCIF 一致。模型包与 HF 不同发布时间和覆盖范围均已明确，公开包审阅完成后执行独立发布验收。

2026-10-09：按新版 source README 合同复核标签、结构连接与动态待办；新增来源方背景和三项解释边界，未改动来源 payload。

## 参考文献

- <https://arxiv.org/pdf/2506.04235v2>
- <https://doi.org/10.48550/arXiv.2506.04235>
- <https://huggingface.co/datasets/AbBibench/Antibody_Binding_Benchmark_Dataset>
- <https://zenodo.org/records/16557372>
- <https://www.rcsb.org/>
- <https://huggingface.co/datasets/AbBibench/Antibody_Binding_Benchmark_Dataset/blob/556fd6913aa231c0d342a8658818be8f963fd582/README.md>

## 其他

### 完整性与验收

上游声明 37 个文件；最近审计通过 37 个，待取得/核验 0 个。

公开包独立验收、论文/补充材料对照及 PDB 配对审计通过；不宣称全部底层实验数据取得。没有独立 manifest/API 响应/审计 JSON 发布在 source version 中；临时产物只保存在共享 cache。

| 上游 payload | 大小 | SHA-256 |
| --- | --- | --- |
| `Antibody_Binding_Benchmark_Dataset/.DS_Store` | 6.00 KiB（6,148 bytes） | `4982c6ac20a52194f405305259109ccaa0b5d16219c73914b0567427ee53babc` |
| `Antibody_Binding_Benchmark_Dataset/.gitattributes` | 2.65 KiB（2,712 bytes） | `fa052c17f77470abf9875c16786865ab5ca136c50996a4f1a8124855d11c33a8` |
| `Antibody_Binding_Benchmark_Dataset/README.md` | 385 bytes | `0d036ce99cd8f532a28b0d7828697f7caafc093eadfc3a07334c3021e7914c22` |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/1mhp_LC_benchmarking_data.csv` | 16.54 KiB（16,942 bytes） | `19609658bc63be90f67cd9ebef2d5118d1f7583393c072e7706f77cb7d4283a5` |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/1mlc_benchmarking_data.csv` | 288.05 KiB（294,963 bytes） | `b7455794e73086dd5aba9536c75e7317b88349c5d0c7a36d39b91a98a8463407` |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/1n8z_benchmarking_data.csv` | 102.30 KiB（104,757 bytes） | `2ca138b0c6324b3cfa074dfdaa9fced69d2777e7e90d384d1cfb2fb2bd720348` |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/2fjg_benchmarking_data.csv` | 534.63 KiB（547,464 bytes） | `2e9827c1b6cedd282bd7674dae8017e3ffc1442309ffcbdd3eaef6e5be1bce2c` |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/3gbn_h1_benchmarking_data.csv` | 457.43 KiB（468,404 bytes） | `aa3071f443c19a916dbf206a7a2e6ec8c6fd792a55ed4cc32cb22cf33aa92206` |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/3gbn_h9_benchmarking_data.csv` | 444.32 KiB（454,981 bytes） | `34b58d003206555e717f341e2e08aee4cc0a320a327ab8d7fb0c00c695b3a22d` |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/4d5_her2_benchmarking_data_trimmed.csv` | 497.17 KiB（509,099 bytes） | `b76308178f61ed7f8d8fa84b7daa78aae86ca7cf146584e59e6dce6c6f27031d` |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/4fqi_h1_benchmarking_data.csv` | 15.48 MiB（16,234,561 bytes） | `2c401c2056e4b035d07667e86f5bb5d47bae8db9b9539eb4f4cba8401c18cfac` |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/4fqi_h3_benchmarking_data.csv` | 14.84 MiB（15,565,895 bytes） | `b7054a65c9816f08db962b3c926f1040ade98c8b02bdf9a66e332cb047fe7933` |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/5a12_ang2_benchmarking_data.csv` | 408.25 KiB（418,048 bytes） | `6a597b41c47e432710f7f6a8b9e1d58c6cff34e3305eacc74855e6450f239fd3` |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/5a12_vegf_benchmarking_data.csv` | 12.53 MiB（13,139,563 bytes） | `d6fcb46ce73945ea4885e5926eae01925c540062563e233b81d1be688712bed7` |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl49_ML_benchmarking_data.csv` | 2.14 MiB（2,245,998 bytes） | `0b10ebfcba39006482448a6c67480023cc97dd34666692c0fe4e6abaf74a7bfd` |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl49_benchmarking_data.csv` | 1.03 MiB（1,081,437 bytes） | `478d1f89d28dc862048721f3b3ecc9fec26fbecccc7880723c0fcc3da2bf54ef` |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl50_LC_benchmarking_data.csv` | 2.74 MiB（2,877,358 bytes） | `13362d984706b20a8f56af0d5bfca836e9704349644770c4cbf0b6f706d76f79` |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl51_benchmarking_data.csv` | 1.05 MiB（1,096,445 bytes） | `fa24948a92ef968010e2ad8d7b41f96644e90893627140efd107eab710073abf` |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/aayl52_LC_benchmarking_data.csv` | 3.11 MiB（3,261,751 bytes） | `60856de6b2d11d6fc7c6eac469c2416fde6d3d2097511aab2594799d4e9a05fb` |
| `Antibody_Binding_Benchmark_Dataset/binding_affinity/g6_LC_benchmarking_data.csv` | 486.14 KiB（497,811 bytes） | `529c8d3e837b5c57fadbf757e9f03e210420b978c145a009e122182cf5d86285` |
| `Antibody_Binding_Benchmark_Dataset/complex_structure/1mhp.pdb` | 701.55 KiB（718,389 bytes） | `c5102bd972832a95e9035171578f974f78ecb3b0442351e64e282ba24a5ea9a1` |
| `Antibody_Binding_Benchmark_Dataset/complex_structure/1mhp_hla.pdb` | 251.44 KiB（257,478 bytes） | `fcf5a1e70ce840b71d52e72247fd6eddd5bd52fef3198f36cb2627e74e581270` |
| `Antibody_Binding_Benchmark_Dataset/complex_structure/1mlc_bae.pdb` | 216.51 KiB（221,707 bytes） | `7d792ecab8d9e5167ab44914bb434967838d94aa548940887b7b6378f08e5b9b` |
| `Antibody_Binding_Benchmark_Dataset/complex_structure/1n8z_bac.pdb` | 495.50 KiB（507,394 bytes） | `09de02dbb5f9e6500d575689146e16588bf417b98702568995cf47dd61e9d496` |
| `Antibody_Binding_Benchmark_Dataset/complex_structure/2fjg_hlv.pdb` | 197.14 KiB（201,867 bytes） | `55afab057c7b2c9d9f43326247268243044b5929659cf4e79d83e7d6506c1d9a` |
| `Antibody_Binding_Benchmark_Dataset/complex_structure/3gbn_hlab.pdb` | 450.86 KiB（461,683 bytes） | `16701963540b4f24cd46d7dc9b7c6e3d7ba124c93325ef785b1feeebb7af28b0` |
| `Antibody_Binding_Benchmark_Dataset/complex_structure/4fqi_hlab.pdb` | 464.66 KiB（475,816 bytes） | `d3a23d95d5a2817cd1cee12a9cccb73884b1d1d74de2af03aa9dccc1b5679b76` |
| `Antibody_Binding_Benchmark_Dataset/complex_structure/4zff_hld.pdb` | 317.52 KiB（325,144 bytes） | `3189a78bcba7152734f0cc2363a7de2d78e7b11dae30f0804282c903e331b489` |
| `Antibody_Binding_Benchmark_Dataset/complex_structure/4zfg_hla.pdb` | 397.89 KiB（407,440 bytes） | `e91684c81f5961d9582dc65875a7bbd749deba1ed24d408decdd5f5cd6cf0359` |
| `Antibody_Binding_Benchmark_Dataset/complex_structure/AAYL49_bca.pdb` | 145.76 KiB（149,254 bytes） | `9ac2d6c286de45c829d1a8c452004d738196d96a2562a94fa773118e05de3cf9` |
| `Antibody_Binding_Benchmark_Dataset/complex_structure/AAYL50_bca.pdb` | 145.76 KiB（149,254 bytes） | `9ac2d6c286de45c829d1a8c452004d738196d96a2562a94fa773118e05de3cf9` |
| `Antibody_Binding_Benchmark_Dataset/complex_structure/AAYL51_bca.pdb` | 147.39 KiB（150,926 bytes） | `b28c848c5d24015d5f6c41344f3f583aed01589cb1b07b1069f78e509929585a` |
| `Antibody_Binding_Benchmark_Dataset/complex_structure/AAYL52_bca.pdb` | 142.09 KiB（145,496 bytes） | `bae147c2150054ef3d99d5773a1102c36f6eb1ca36dee03143a6959ff8495f64` |
| `Antibody_Binding_Benchmark_Dataset/croissant.json` | 2.45 KiB（2,512 bytes） | `fe15969055f9ad4daa2910a34950b056795d5aa7bdc181baff827a8bd200590a` |
| `Antibody_Binding_Benchmark_Dataset/metadata.json` | 5.84 KiB（5,982 bytes） | `32d95c51193b496dd7c747820d008a628a19f7fe85f912dfc2eedb51bbda20e9` |
| `ABBIBENCH/README.txt` | 61 bytes | `45dc77ce7a8a9406c41cf753c981d9e950f18e915896610a5e8f5b01e9a3ffc1` |
| `ABBIBENCH/mutant_structure.tar.gz` | 7.66 GiB（8,225,939,457 bytes） | `11c5ff7b8139da6e20a1e7a5bb941aa1b334fdf789aedfaadc4a30d88390bfc6` |

### 许可和再分发边界

HF dataset card 标为 CC BY 4.0；Zenodo 16557372 的条款保留其官方 metadata。汇编中的上游实验许可须分别追溯，论文许可不自动覆盖全部上游表。

固定 HF dataset card 与 Zenodo 16557372 metadata 都明确 CC BY 4.0；这是作者公开交付包的许可，不将它扩展为所有原实验仪器输出的访问或使用授权。结构模型由作者用 FoldX 生成，引用软件不代表本项目重新生成或拥有其软件许可。

### 公开范围对照

| 目标组成 | 当前证据 | 状态 |
| --- | --- | --- |
| 固定上游 payload | tracked config + 独立文件/格式审计 | 目标公开文件验收通过 |
| 论文原文 | 一手 DOI 和取得文件 hash；不可得项明确记录 | 主文与全部被引用附件已归档并解析 |
| PDB 原始序列与全坐标 | 接受锚点两层配对审计 | 两层已齐；非逐变体结构 |
| 完整研究底层数据 | 公开汇编或处理包不等于全部底层实验 | 未宣称获得 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-09；影响跨 assay 标签比较）：17 张表共 215,699 行，但论文主表、supplement 和文件数分别采用 14、16、17 的口径；各表 `binding_score` 来源包括负对数 KD 和富集信号。已按来源表隔离，不把同名列当统一绝对亲和力；下一步逐表核对原始研究、生成代码、转换底数和筛选阈值，建立可复核的 assay 对照后关闭。
- `Q02`（最近更新：2026-10-09；影响结构伙伴解释）：固定 HF `metadata.json` 的 `1mlc_LC`、`1mhp` 路径在该 revision 的文件树中不存在，且 `5a12_vegf` 的 epitope/paratope 与 antigen-chain 注释冲突。已保留 8 个完整 RCSB entry 级参考，不按弱注释选定链或补造 CSV；取得作者修订的 metadata 或可核对的一手链映射后关闭。此项不阻塞已验收公开文件的接入。
