---
- tags:
  - context
---

# SRC_R16_GUEST 数据说明

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

- `source_id`：`SRC_R16_GUEST`
- `source_version`：`snapshot-2020-11-17`
- 原作者或发布机构：Guest JD、Vreven T、Zhou J、Moal I、Jeliazkov JR、Gray JJ、Weng Z、Pierce BG

### 来源方背景

[Pierce Lab 官方 benchmark 页面](https://piercelab.ibbr.umd.edu/antibody_benchmark/)同时提供案例 Excel、结合/游离结构仓库及实验亲和力说明；[正式论文](https://doi.org/10.1016/j.str.2021.01.005)由 Guest、Pierce 等跨机构作者完成。该团队维护的是对接与亲和力评价案例，数值仍来自各案例原研究，不代表 67 个案例由同一实验流程重测。

## 实验设计和数据口径

Guest benchmark 提供 67 个抗体—抗原案例的 bound/unbound 结构，主要用于对接和小规模亲和力评价。固定 Git affinity TXT 实际有 42 行数值 KD；官方 XLSX 有 67 个非空案例、42 个数值 KD 和 51 个数值 ΔG，其余 59 行只有格式。51 个亲和力案例不等于 51 个 KD。每个案例的四个结构表示不是四次实验：r/l 表示抗体/抗原，b/u 表示结合态/游离态；游离组件可来自另一个 PDB。固定 Git TXT 与官网 XLSX 的 42 个共有案例，其 KD 和 ΔG 数值逐项一致；`5SV3` 均为 0.0627 nM 和 -13.92 kcal/mol。

主文以 ≤3.25 Å 分辨率、抗原长度 ≥30 aa 和 unbound 匹配 ≥98% identity、80% coverage 搜索并人工排查突变/缺失界面，固定 commit 的最终 benchmark 为 67 个非冗余 bound/unbound cases。主文 51 个 affinity 是 ΔG 的实验来源汇编口径；真实 XLSX 有 51 个数字 ΔG 和 42 个数字 KD，Git affinity TXT 为 42 条，不能把三者相加或静默补缺失。ΔG=RT ln KD，T 使用原研究实际温度，单位 kcal/mol；ΔG 越负/KD 越小表示越强。主文为未报温度的案例向原实验作者索取信息，并按结构中的 Fab/IgG/scFv 格式选择对应 affinity。对接/能量模型得分不是新的实验值。

## 论文原文

- 标题：An Expanded Benchmark for Antibody-Antigen Docking and Affinity Prediction Reveals Insights into Antibody Recognition Determinants
- 作者：Johnathan D. Guest；Thom Vreven；Jing Zhou；Iain Moal；Jeliazko R. Jeliazkov；Jeffrey J. Gray；Zhiping Weng；Brian G. Pierce
- 载体与版本：Structure
- 发布日期：2021-02-03
- DOI：`10.1016/j.str.2021.01.005`
- PMID / PMCID：33539768 / PMC8178184
- 本地文件：`articles/GUEST_2021-02-03_PMC-author-manuscript-v1.xml`
- 文件大小：221.68 KiB（227,005 bytes）
- SHA-256：bcf55eacb73735ae3829a8665dc56e4d1d523f0583c850ebaf6899f1550f41dd
- 文本许可：This file is available for text mining. It may also be used consistent with the principles of fair use under the copyright law.
- 补充材料：`articles/GUEST_2021-02-03_supplement-NIHMS1665739-supplement-1.pdf`，2.04 MiB（2,139,632 bytes），SHA-256 `b1879042adabb822236422b837a832cdf8c2c75e41387961c3492a8cb76faece`

原始出版方完整 PDF 17 页，所有被引用的 Table S1–S9 与 Figure S1–S3 已取得并阅读。S1 给出 67 cases 身份，S2 给 CDR 定义和原样缺失（IgNAR 2I25 无 CDR2 等价环），S3 列出 28 新增实验 KD（nM）、ΔG（kcal/mol）、20–37°C 实验温度及 SPR/BLI/ITC 方法和引用；S4 为构象变化，S5–S7 为模型排名，S8–S9 为同一组实验 ΔG 的预测相关性，不作为额外实验。model rank 1001/字面 - 代表未找到对应准确度预测，不填成 KD。

## 仓库内容

来源身份：

- `kind`：`github`
- `repository`：`piercelab/antibody_benchmark`
- `commit`：`e788056bbedb4be83fa1f934feb2007ffb18ec59`
- `tree`：`e788056bbedb4be83fa1f934feb2007ffb18ec59`
- `commit_date`：`2020-11-17T01:02:47Z`

版本日期来自数据源 commit 或官方更新时间；正式版本名保留官方名称。以下树为已验收的上游 payload，不列项目 README、论文及 PDB 外部补充。

```text
snapshot-2020-11-17/
└── antibody_benchmark/
    ├── LICENSE
    ├── README.md
    ├── antibody_antigen_affinities.txt
    ├── antibody_antigen_cases.txt
    ├── pdbs/1AHW_l_b.pdb
    ├── pdbs/1AHW_l_u.pdb
    ├── pdbs/1AHW_r_b.pdb
    ├── pdbs/1AHW_r_u.pdb
    ├── pdbs/1DQJ_l_b.pdb
    ├── pdbs/1DQJ_l_u.pdb
    ├── pdbs/1DQJ_r_b.pdb
    ├── pdbs/1DQJ_r_u.pdb
    └── …（其余来源文件保留原路径）
```

## 数据结构

### 原始交付与记录

| 原始文件 / sheet | 非空记录数 | 字段数 | 精确重复行 |
| --- | --- | --- | --- |
| `antibody_benchmark/antibody_antigen_affinities.txt` | 42 | 4 | 0 |
| `antibody_benchmark/antibody_antigen_cases.txt` | 67 | 9 | 0 |
| `antibody_benchmark/antibody_benchmark_cases.xlsx:Combined.New` | 67 | 11 | 0 |

只统计实际已解析的文件，未把来源介绍规模当作本次落盘统计。

固定 Git commit 共 284 blobs，另有官网完整 XLSX（不声称随固定 commit 发布），共 285 个来源文件、87.46 MiB（91,713,088 bytes）。实际 XLSX 67 个非空 cases、11 个字段，其中 Kd (nM) 为 42 个数值、ΔG (kcal/mol) 为 51 个数值；与根 affinity TXT 42 条是不同粒度。67 个案例的所有原始 complex/unbound author-chain 键逐项与官方明确 CC BY 4.0 的同一 benchmark 比对通过。清理后的 bound/unbound receptor/ligand PDB 是派生表示，不计为新实验，不替代 194 个 full native PDB 参考条目。

### 字段说明

Complex PDB、Antibody PDB、Antigen PDB 含 accession 与 author chain 后缀；复合物冒号前后区分伙伴。I-RMSD (Å) 为界面构象 RMSD，ΔASA (Å2) 为可及表面积变化，Category 为 Rigid/Medium/Difficult，这些不是亲和力。Kd (nM) 越小有利；ΔG (kcal/mol) 越负结合越强。New 的 X 为版本新增标记，不是结合正例。TXT 使用 TAB；XLSX 的 Combined.New sheet 要跳过全空格式行。

实际表头（保留原始字段名）：

- `antibody_benchmark/antibody_antigen_affinities.txt`：`Case`、`New`、`Kd (nM)`、`ΔG (kcal/mol)`

- `antibody_benchmark/antibody_antigen_cases.txt`：`Complex PDB`、`Antibody PDB`、`Antibody`、`Antigen PDB`、`Antigen`、`I-RMSD (Å)`、`ΔASA (Å2)`、`Category`、`New`

- `antibody_benchmark/antibody_benchmark_cases.xlsx:Combined.New`：`Complex PDB`、`Antibody PDB`、`Antibody`、`Antigen PDB`、`Antigen`、`I-RMSD (Å)`、`ΔASA (Å2)`、`Category`、`New`、`Kd (nM)`、`ΔG (kcal/mol)`

字段原始表示与缺失统计（只统计审计解析结果，不在 raw 中填零）：

- `antibody_benchmark/antibody_antigen_affinities.txt`：缺失/特殊表示计数 `{"New": 14}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `antibody_benchmark/antibody_antigen_cases.txt`：缺失/特殊表示计数 `{"New": 26}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

- `antibody_benchmark/antibody_benchmark_cases.xlsx:Combined.New`：缺失/特殊表示计数 `{"New": 26, "Kd (nM)": 14, "ΔG (kcal/mol)": 4}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

### 数据示例

来自 `antibody_benchmark/antibody_antigen_affinities.txt` 的第一条真实记录；这里只摘录字段，不改写原始文件。

| 字段 | 原样值 |
| --- | --- |
| `Case` | `1S78` |
| `New` | `X` |
| `Kd (nM)` | `500` |
| `ΔG (kcal/mol)` | `-8.45` |

每行按该来源的测量、配对或结构实例口径解释，不把结构表示或 replicate 当作新实验。完整字段保留在 payload 中。

## PDB 数据库

Cases table Complex PDB/Antibody PDB/Antigen PDB prefixes; source specifies author chain suffixes and bound/unbound roles. Full canonical entry files are preserved. 192 original benchmark accessions plus 2 RCSB-evidenced superseding references. RCSB removed holdings confirms 3RVW -> 5VPG (2022-04-27) and 4ZAI -> 7JNY (2020-10-07). Original native FASTA endpoints return 404; preserve obsolete full mmCIF where available and save full native FASTA/mmCIF of the superseding entry as an additional reference, without rewriting source table IDs or claiming identical chains/coordinates. Original sequence gaps are now closed by complete literal RCSB historical SEQRES records in the fixed upstream 2020 example archive, matched to every author chain and complete canonical polymer sequence of the original obsolete mmCIF; no sequences rebuilt or headers rewritten.

当前接受锚点清单为 194 个；最后一次审计有 0 个未完成两层配对。每个锚点取原样 per-entry FASTA 和完整 mmCIF，不嫁接 CDR、不生成逐变体重建序列。FASTA 的原始 header 保留 polymer entity 与 author/label chain；不猜测伙伴角色。只有全部接受锚点同时通过 FASTA 和坐标解析，且 FASTA entity ID 集合和完整序列与 mmCIF 的 canonical polymer 一致，才算完成。

PDB 文件审计摘要：388 个文件，177.50 MiB（186,122,390 bytes）；inventory SHA-256：`d803f96879ed2c3ebb7a2225cecdf162e5235a185217604a251f9244305b3e4d`。摘要按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接计算。缓存最初包含选择链/重写 header 的 FASTA，已清理本轮这类 staging 副本；现在只接受 RCSB native per-entry header。

已撤回条目的历史原始序列例外：从已验收的 RCSB SEQRES 历史归档复制该 entry 的全部字面记录，保留原始 header、换行和序列字节。以完整 obsolete mmCIF 的明确 author-chain 集合及 canonical 全序列逐链核对，缺链、重复链、长度或序列不一致均不通过，不从坐标生成 FASTA。上述 per-entry/entity header 描述适用于现行端点文件，历史记录保留 RCSB 的 chain/molecule/length header。归档来源：<https://raw.githubusercontent.com/piercelab/antibody_benchmark/e788056bbedb4be83fa1f934feb2007ffb18ec59/scripts/example/pdb_seqres_8_2020.fa.tar.gz>；归档 SHA-256 `fcfac4ddc495b81da23e9f25b1adddf448f3dd10316c7eefa4dd769434a47aae`；成员 `pdb_seqres_8_2020.fa`（183211395 bytes）。

## 使用方式

由调用者先赋值 `dataset_root`（Path），再读取；不在这里清洗或转换标签。

```python
import pandas as pd
table = pd.read_csv(dataset_root / "antibody_benchmark/antibody_antigen_affinities.txt", sep="\t")
```

## 采集过程记录

2026-09-18：读取项目规范和执行清单，解析一手 API/tree/Drive 对象 metadata，固定本轮版本与文件身份。下载到共享 source 下 `.staging/<version>.partial`；HTTP 大文件使用精确 byte range 和全文件上游 checksum，Drive 保留对象 ID、MIME 与字节数，失败部分可续传。2026-09-18 按用户要求调整本轮 HTTP 为直连优先、连接失败回退环境代理，15 分钟后重试直连；各线程复用连接且保留 TLS/CA 校验。重启任务保留所有文件断点。

独立 audit 重新计算 hash、完整解析已取得表格并检查 PDB 两层文件；归档只有完成逐成员/CRC 与路径安全检查后才通过。PMC 访问被拒绝、非 OA XML 不可得和间歇代理连接失败均保留缺口，未关闭 TLS 验证。PDB 缓存原始性检查发现错误后清理本轮衍生 header 文件并重做。

README 草稿每次写入后立即同步到 staging 同名文件，随后运行 skill 固定 Markdownlint 配置。发布脚本仅在逐文件、论文/PDB、README 同步与固定格式检查通过后原子发布；发布状态与 接入过程记录 同步。

2026-09-18：主文从 `Guest_PMC8178184.xml` 改名为 `GUEST_2021-02-03_PMC-author-manuscript-v1.xml`，日期取该论文版本发布日期，改名前后大小和 SHA-256 一致。

2026-09-18：按 PMC 更新后的官方 Cloud Service 获取完整作者稿 XML；旧 OA FTP/API 已退役，欧洲 PMC fullTextXML 不可得不等于论文不可得。XML MD5 与云 metadata 的 3b69f83b734ce3bd0eeae008358d1059 一致。出版方 media endpoint 提供全文引用的唯一补充 PDF。原文件命名按论文 2021-02-03 首发日期和 PMC author manuscript v1 身份改写，bytes/SHA 不变。 数据许可核验补充：官方完整 benchmark 页面明确 work CC BY 4.0；独立 reviewer 核对 67/67 complex 和 134/134 双方 unbound chain 键，全通过，不将旧许可 blocker 遗留为当前状态。

2026-09-18：按 DOI 一致的完整主文逐项核对全部引用附件，从原出版方公开 media endpoint 原样取得完整 PDF，解析全部页并核对 Table S1–S9；原文件名、来源端点、大小和 SHA-256 已记录。

2026-10-09：按新版 README 合同复核来源方背景、结构和亲和力案例粒度；将 `5SV3` 的来源值差异列入动态待办。已验收结构、论文与附件未改动。

2026-10-09（`Q01` 已结案）：重新直接读取正式目录中的固定 Git TXT 与官网 XLSX，按案例 ID 对齐全部 42 个共有数值案例，KD 和 ΔG 均逐项相等；`5SV3` 在两个文件里同为 0.0627 nM、-13.92 kcal/mol。此前的来源差异判断不成立，正文已更正，故从动态清单移除。

## 参考文献

- <https://pmc-oa-opendata.s3.amazonaws.com/PMC8178184.1/PMC8178184.1.xml>
- <https://doi.org/10.1016/j.str.2021.01.005>
- <https://github.com/piercelab/antibody_benchmark>
- <https://www.rcsb.org/>
- <https://data.rcsb.org/rest/v1/holdings/removed/3RVW>
- <https://data.rcsb.org/rest/v1/holdings/removed/4ZAI>
- <https://zlab.umassmed.edu/benchmark/benchmark5.5.html>

## 其他

### 完整性与验收

上游声明 285 个文件；最近审计通过 285 个，待取得/核验 0 个。

公开包独立验收、论文/补充材料对照及 PDB 配对审计通过；不宣称全部底层实验数据取得。没有独立 manifest/API 响应/审计 JSON 发布在 source version 中；临时产物只保存在共享 cache。

| 上游 payload | 大小 | SHA-256 |
| --- | --- | --- |
| `antibody_benchmark/LICENSE` | 18.21 KiB（18,650 bytes） | `7e7170e3cebf88a9f60c7b8421418323c09304da1af4d5e90f4da1dc1c8a2661` |
| `antibody_benchmark/README.md` | 3.61 KiB（3,700 bytes） | `1ec61a9225cd567fabd55619e78c99ce5741acd49469d0c3120fef9b500b1238` |
| `antibody_benchmark/antibody_antigen_affinities.txt` | 788 bytes | `34ee4ee6c718ca0977d8ad44661db32a79db3c6600c5a27886ff42c7da4455e0` |
| `antibody_benchmark/antibody_antigen_cases.txt` | 4.97 KiB（5,087 bytes） | `8f2d2bb7a3fc186145d4bd4e932103fe1e3d126cd05fc432c2baa6168add3790` |
| `antibody_benchmark/pdbs/1AHW_l_b.pdb` | 127.51 KiB（130,572 bytes） | `b259b12aeba489d2d292b308262a34269e4cab24591d42ef0490cc0f767b5fc6` |
| `antibody_benchmark/pdbs/1AHW_l_u.pdb` | 125.14 KiB（128,142 bytes） | `1d751efe068a6840ef32a0c62c55acf7478c219be2e730d9ad242acdae83bd24` |
| `antibody_benchmark/pdbs/1AHW_r_b.pdb` | 261.35 KiB（267,624 bytes） | `79c37c7f180d463d9dd173b303321478e07cd5dd3e7426580dfffd60d0d86b74` |
| `antibody_benchmark/pdbs/1AHW_r_u.pdb` | 254.90 KiB（261,020 bytes） | `90856326fa824ecdf1a9cf9408a32fb66f0ebfd69477d9107ff17533321ddb68` |
| `antibody_benchmark/pdbs/1DQJ_l_b.pdb` | 79.18 KiB（81,081 bytes） | `ca5cbdd26dd4de56f69c93133e20725b2ce4dddd7a784dc4d10a3eb0a324927a` |
| `antibody_benchmark/pdbs/1DQJ_l_u.pdb` | 77.15 KiB（79,004 bytes） | `13775afaa986a8c50aa617caa1cf1ee23017f09d6818248b2fb1f31a73054203` |
| `antibody_benchmark/pdbs/1DQJ_r_b.pdb` | 256.61 KiB（262,764 bytes） | `1c7e3a9cfb2b34d0f4c89269719e597e99f311c8ddc7c26d24e72c97a56f54e6` |
| `antibody_benchmark/pdbs/1DQJ_r_u.pdb` | 250.27 KiB（256,280 bytes） | `7ea6c3584678e06f4e005e33a1d6fd44268fd5d57bbd64098069ef818e59520d` |
| `antibody_benchmark/pdbs/1E6J_l_b.pdb` | 129.65 KiB（132,759 bytes） | `d7bfdd2fb34e9315124f9ccb76ca957966eed99f01da51e8a2aea004d25af866` |
| `antibody_benchmark/pdbs/1E6J_l_u.pdb` | 44.21 KiB（45,271 bytes） | `bb0f88caa5df6221124feabf927a8e8a90afc5b67926ec1f9ec4493dd7834b50` |
| `antibody_benchmark/pdbs/1E6J_r_b.pdb` | 259.06 KiB（265,275 bytes） | `89d3d311269b833b80bfb5b6f86cfc99bf2a73c0b72ede5a0cd070893f84bbc2` |
| `antibody_benchmark/pdbs/1E6J_r_u.pdb` | 252.82 KiB（258,887 bytes） | `510a4c5d60fd395ed7611c2b8d6bbd1a85c01504e189e2c700089f856e03cf03` |
| `antibody_benchmark/pdbs/1JPS_l_b.pdb` | 127.43 KiB（130,491 bytes） | `83ace8670aadd99c5fe7497c142918e669a153111ee747cc40c8335187c00b01` |
| `antibody_benchmark/pdbs/1JPS_l_u.pdb` | 113.18 KiB（115,897 bytes） | `5c5bbfa99b1f8b727dc4fd26ab1d3eba6e8317ceb37024c6c08d8b9b70795650` |
| `antibody_benchmark/pdbs/1JPS_r_b.pdb` | 256.84 KiB（263,007 bytes） | `7f55dc43f1849ee51675875553b7187485df1d34eb8f9283d3db3e9f30c815cb` |
| `antibody_benchmark/pdbs/1JPS_r_u.pdb` | 250.04 KiB（256,043 bytes） | `ec112c0d131ff01111741e788f0df1a5735f773ec4d38e235eb1be8350986e35` |
| `antibody_benchmark/pdbs/1MLC_l_b.pdb` | 79.18 KiB（81,081 bytes） | `b4e36709e6bb6849d5ee0495fad045d80b00cb87de4d41abed119d5d52898ed0` |
| `antibody_benchmark/pdbs/1MLC_l_u.pdb` | 77.15 KiB（79,004 bytes） | `40451e58a7645eacdedf73bbc7baf21507ca028851e4fe58c4b61533853897d2` |
| `antibody_benchmark/pdbs/1MLC_r_b.pdb` | 260.24 KiB（266,490 bytes） | `0277e69641ec5562808fc5ea7850a1f81f43befcf2b32e1122a98788e111c2f2` |
| `antibody_benchmark/pdbs/1MLC_r_u.pdb` | 253.82 KiB（259,914 bytes） | `1c36bcf0238462e8640b051ea737258e158f614bec93e1646e8eaae58914f5b3` |
| `antibody_benchmark/pdbs/1S78_l_b.pdb` | 343.85 KiB（352,107 bytes） | `06e62140732f69e2e6c6679448b8e0bb8230353cd4454882b09653c4d3244ab4` |
| `antibody_benchmark/pdbs/1S78_l_u.pdb` | 316.76 KiB（324,364 bytes） | `a3c9162bb9cb7eab7148b7c7b92f24c4f13440862cafafd37a511c8dbdd6925b` |
| `antibody_benchmark/pdbs/1S78_r_b.pdb` | 262.78 KiB（269,082 bytes） | `098726a09382cd8ea14e9990a960442c814d5318ebb834f40568592d54c25d81` |
| `antibody_benchmark/pdbs/1S78_r_u.pdb` | 270.16 KiB（276,639 bytes） | `f2f236cb3af2f777cae754c204c34caaccdc11a31f2a83419efc13c8e7973bf2` |
| `antibody_benchmark/pdbs/1VFB_l_b.pdb` | 79.18 KiB（81,081 bytes） | `c0e1fc5cb8ca481fed70b109220a7598794b36ef09ce2c0a9a07d6e3b5ff6964` |
| `antibody_benchmark/pdbs/1VFB_l_u.pdb` | 77.15 KiB（79,004 bytes） | `7a6af40c28d152d26de4d8a203b8cb8dfef58f7ed67556b415a205b46a280b7c` |
| `antibody_benchmark/pdbs/1VFB_r_b.pdb` | 136.85 KiB（140,130 bytes） | `002a1ca3299a4ea9367ab7ee8d59cadf69ef93bd71bf892a2fb26a2f3764581e` |
| `antibody_benchmark/pdbs/1VFB_r_u.pdb` | 134.32 KiB（137,543 bytes） | `4dfeb48407b3715d4105b68d1ed55fb5ebbd54ebb15ab82abd2a11439d568641` |
| `antibody_benchmark/pdbs/1WEJ_l_b.pdb` | 68.66 KiB（70,308 bytes） | `0fde47bffa5c1fb5ce88b606cd6e8eb89557b0d16f617b6c1f84120f780deb95` |
| `antibody_benchmark/pdbs/1WEJ_l_u.pdb` | 67.05 KiB（68,655 bytes） | `aa2104b5c43e7459c4048c3d68ea5e9858b9ae75618cfba9066ab38b098c0e59` |
| `antibody_benchmark/pdbs/1WEJ_r_b.pdb` | 264.20 KiB（270,540 bytes） | `0ccf1f3e1a109dcfe63f3c8e8262e057dec8a70c7084652fb465072a95a4986d` |
| `antibody_benchmark/pdbs/1WEJ_r_u.pdb` | 255.98 KiB（262,126 bytes） | `97511522193c627b5786cc89ea4ca895b75be9f28c91bdf4672983cd1f6c3304` |
| `antibody_benchmark/pdbs/2DD8_l_b.pdb` | 122.13 KiB（125,064 bytes） | `08e3fb45708b46d18b55344d3bd85f6392144cb461b573eddf5cf622e18290fa` |
| `antibody_benchmark/pdbs/2DD8_l_u.pdb` | 119.31 KiB（122,176 bytes） | `118a17bd3e84aadc1a337c4bc4793857c2c29227cf49aae474817998cae82248` |
| `antibody_benchmark/pdbs/2DD8_r_b.pdb` | 254.31 KiB（260,415 bytes） | `875bd016f284a6e4e15bf8d602743c8e71fdaa9f7a3b45e04dccdc7f9711aacb` |
| `antibody_benchmark/pdbs/2DD8_r_u.pdb` | 258.73 KiB（264,936 bytes） | `ef023dab91b24eb734bfa088ed5fa7a65e4ae5f538966ced14a0cd3e79fad9a5` |
| `antibody_benchmark/pdbs/2FD6_l_b.pdb` | 150.77 KiB（154,386 bytes） | `3a32e768b1754f7b1e8a66222ba373507b061f01ef0ed06406a1b2fec5921069` |
| `antibody_benchmark/pdbs/2FD6_l_u.pdb` | 157.39 KiB（161,164 bytes） | `bbcecc80f2d9f5b6d8b6154307f6d3f9b4c9c54e0245f7dccaa09915a23bd3ea` |
| `antibody_benchmark/pdbs/2FD6_r_b.pdb` | 261.54 KiB（267,812 bytes） | `7cec73f6e48ec0bf3176d16994b6121062947e25266f40ee4102faddc24a76ba` |
| `antibody_benchmark/pdbs/2FD6_r_u.pdb` | 251.58 KiB（257,623 bytes） | `5e59d2a97d3a2470e8406d831b2930333626e8255b5e1d3a25026ebfae56509d` |
| `antibody_benchmark/pdbs/2FJG_l_b.pdb` | 121.10 KiB（124,011 bytes） | `94e55cbcc72f356d16f9956a8fa08c090d19e167c205b7b7dbaf319d09239682` |
| `antibody_benchmark/pdbs/2FJG_l_u.pdb` | 138.77 KiB（142,096 bytes） | `bd6304ba9f7cdeff02f5df7691cc230a61f81f9615c2740ab15814a3522f74de` |
| `antibody_benchmark/pdbs/2FJG_r_b.pdb` | 258.27 KiB（264,465 bytes） | `99a5c68a1331900dac95fa95f17f7068affa251fc947ec79be1fe363f1e785d7` |
| `antibody_benchmark/pdbs/2FJG_r_u.pdb` | 263.43 KiB（269,750 bytes） | `270f37bbed4391cd4a741cdcd56648eb6c52e345add1cdda226080368a47b41f` |
| `antibody_benchmark/pdbs/2I25_l_b.pdb` | 79.10 KiB（81,000 bytes） | `2be474f81b1774aebd9dcf6147b86e9d257f88a0b67084c0e586036c513ba0df` |
| `antibody_benchmark/pdbs/2I25_l_u.pdb` | 77.23 KiB（79,083 bytes） | `b341c0eb5b431a437d8121939e3cf0c032afe8b048dd80069adce9bf45fb1054` |
| `antibody_benchmark/pdbs/2I25_r_b.pdb` | 70.23 KiB（71,913 bytes） | `9970329c680b90a6881f37458047eeb92b7e4b48294374fd598a2583b31ab3ad` |
| `antibody_benchmark/pdbs/2I25_r_u.pdb` | 67.28 KiB（68,892 bytes） | `3eefb7595392ea57320c7956d001e608313df2a2e778f7d68602241cfc4de82f` |
| `antibody_benchmark/pdbs/2VIS_l_b.pdb` | 164.21 KiB（168,156 bytes） | `400ea13116f80b16e7f728402d75ab30208e4953ebff9218e6fea5aa5f8236fd` |
| `antibody_benchmark/pdbs/2VIS_l_u.pdb` | 572.14 KiB（585,868 bytes） | `b8f0a8d6f4b707362c49a4ff85c4408a6638af75361814a95c50989d88b9802b` |
| `antibody_benchmark/pdbs/2VIS_r_b.pdb` | 257.95 KiB（264,141 bytes） | `612c96fa67b9717080ad9925c03b37219519df88655418c581dfcad663a21ddf` |
| `antibody_benchmark/pdbs/2VIS_r_u.pdb` | 251.58 KiB（257,623 bytes） | `104b54caa226e22d07e81180286d504cbc097468fe94293cbfe672cf1b26c6ca` |
| `antibody_benchmark/pdbs/2VXT_l_b.pdb` | 99.27 KiB（101,655 bytes） | `9b56a42c5ba711d1daeb5182f48006e6bb4059c46baa3d53434429be32c6c3df` |
| `antibody_benchmark/pdbs/2VXT_l_u.pdb` | 100.78 KiB（103,194 bytes） | `e1fe7c4f94a67e4e787a9a98e87ea25ce25dd27674b8d675b01b7c148b46aa08` |
| `antibody_benchmark/pdbs/2VXT_r_b.pdb` | 255.50 KiB（261,630 bytes） | `eb4ffb649fa809528416f1dab83e06e0df622693231032e500884073d2469c17` |
| `antibody_benchmark/pdbs/2VXT_r_u.pdb` | 260.56 KiB（266,814 bytes） | `8b17a8b6e8a6a5bd718875b34defa660a3a7fb57e77c2e4d1b0488ff2764c461` |
| `antibody_benchmark/pdbs/2W9E_l_b.pdb` | 65.50 KiB（67,068 bytes） | `95b2ba53fb18cd8271ca1e1388984d51e590d9b371ee63684fb9c0b0c69d42e1` |
| `antibody_benchmark/pdbs/2W9E_l_u.pdb` | 69.37 KiB（71,037 bytes） | `0070fec91a15163c42df2508f0b0b2a67d5d7f957788255d09eb7a304412df93` |
| `antibody_benchmark/pdbs/2W9E_r_b.pdb` | 257.00 KiB（263,169 bytes） | `be1e944dd459b34532ae12ba9e87387d26cf5b53bf1c34d19c6f0851e82ac8bd` |
| `antibody_benchmark/pdbs/2W9E_r_u.pdb` | 257.16 KiB（263,331 bytes） | `fe5d774c92561ea4a381587365ef4dab6a0ff356f1123c66d8616de30385c5ef` |
| `antibody_benchmark/pdbs/3EO1_l_b.pdb` | 140.64 KiB（144,018 bytes） | `9029ff6f90e5dee3ebe8b6ee3d0b7d149fe2d7483df4ef3a0348677061c128cf` |
| `antibody_benchmark/pdbs/3EO1_l_u.pdb` | 140.64 KiB（144,018 bytes） | `9cf05862bb4fc9004f9e74d514bd4385bc6ddb589adf7989937b78f714789071` |
| `antibody_benchmark/pdbs/3EO1_r_b.pdb` | 257.08 KiB（263,250 bytes） | `aa7ff8caf1c8c98f5093a072e107b3390059773854617fb2caf074e4484390ce` |
| `antibody_benchmark/pdbs/3EO1_r_u.pdb` | 259.53 KiB（265,761 bytes） | `7e41d48bc8df4a8e3648266033dec53f2ae9f0f6782432dff57d5eb3c65f8722` |
| `antibody_benchmark/pdbs/3EOA_l_b.pdb` | 113.75 KiB（116,478 bytes） | `908e142cc3c8928c9c4bda4bcb2ee356b70c5d4159a69cffb9ea8c79ab83e758` |
| `antibody_benchmark/pdbs/3EOA_l_u.pdb` | 114.93 KiB（117,693 bytes） | `a456a568fc4e4529e911b3ba4ad81c96fb9b967626ab0ac102fe63c69da6589e` |
| `antibody_benchmark/pdbs/3EOA_r_b.pdb` | 259.93 KiB（266,166 bytes） | `854fbe6676b2fa3ec8bd55da4b551d7f78aff0bc083119a4916cf3b17d1b6a7d` |
| `antibody_benchmark/pdbs/3EOA_r_u.pdb` | 258.74 KiB（264,951 bytes） | `9da259d30c5d2297b240739e2a935eb49a826c8497dd7e38ecbd41fb32d3e335` |
| `antibody_benchmark/pdbs/3G6D_l_b.pdb` | 64.71 KiB（66,258 bytes） | `b77d0a7434fc97f92fcd38296d7125a001acaa4cac735fdde58a1de4566346b8` |
| `antibody_benchmark/pdbs/3G6D_l_u.pdb` | 68.82 KiB（70,470 bytes） | `7c8dd75bd31aef7558fc366277016631dc210a5bc4ac993a9c90c21a905c6e13` |
| `antibody_benchmark/pdbs/3G6D_r_b.pdb` | 255.97 KiB（262,116 bytes） | `95827e3c9674d03c08b8e3775ea44ab6778ca24a3e5f72757ce2f208abb2f72d` |
| `antibody_benchmark/pdbs/3G6D_r_u.pdb` | 255.81 KiB（261,954 bytes） | `254b9d70ab5d4123653ea094dbd4ec3575143fec4001c33954a0d82aadaf3160` |
| `antibody_benchmark/pdbs/3HI6_l_b.pdb` | 114.38 KiB（117,126 bytes） | `57708b53252001f2d672a81c0ce1b187d4259100c01f22ad455c3e358fb164e6` |
| `antibody_benchmark/pdbs/3HI6_l_u.pdb` | 113.19 KiB（115,911 bytes） | `c5a972d856462dd5e41512d71fd031c4b4a1ab937e6013c8f55c20e4f6089eb2` |
| `antibody_benchmark/pdbs/3HI6_r_b.pdb` | 256.29 KiB（262,440 bytes） | `4e3b1dce37d49c85b3dd2d6e82e519cd42c9c954c7dc5919a7f17a7b22168aae` |
| `antibody_benchmark/pdbs/3HI6_r_u.pdb` | 258.74 KiB（264,951 bytes） | `95759ea6a16adc844ea303b03d0dc66e43b45f875366b1c0ab0dd4171f73a64a` |
| `antibody_benchmark/pdbs/3HMX_l_b.pdb` | 291.17 KiB（298,161 bytes） | `10ff2cc27916c17fbf98d3c90a355b29a5eb1c46fba22c1e4872caec3f0871b3` |
| `antibody_benchmark/pdbs/3HMX_l_u.pdb` | 260.09 KiB（266,328 bytes） | `3c92e26075ec851090d70f82cd764946b93d2ab2af738725d8b463c73c635dce` |
| `antibody_benchmark/pdbs/3HMX_r_b.pdb` | 260.32 KiB（266,571 bytes） | `c1a32f8611385693e8106d7988970e8136524a5c57be4231b1286bdf4aac8b1d` |
| `antibody_benchmark/pdbs/3HMX_r_u.pdb` | 260.96 KiB（267,219 bytes） | `7341e20da5b514c5d22b8ab8de79b643c5afaed4ccbdfd51a987f19bb602cf38` |
| `antibody_benchmark/pdbs/3L5W_l_b.pdb` | 61.30 KiB（62,775 bytes） | `cac072d92b513b06227ecb61f1f55ccb477ce6f12cea444ba36bd9d3eccd4b91` |
| `antibody_benchmark/pdbs/3L5W_l_u.pdb` | 68.82 KiB（70,470 bytes） | `4e490e657e2a1ef40f73e63a502ed72aef39617d66f0db63341a3f3db6a06665` |
| `antibody_benchmark/pdbs/3L5W_r_b.pdb` | 262.70 KiB（269,001 bytes） | `0ffbd93992dccb9eb72dc1d23b60e72b1033f0570898e395d381725cd74b2f2a` |
| `antibody_benchmark/pdbs/3L5W_r_u.pdb` | 259.29 KiB（265,518 bytes） | `8210f35aece3179ce5399ef481b88ad44abbf165bf57e10fd2b7d5dcfb23b9db` |
| `antibody_benchmark/pdbs/3MJ9_l_b.pdb` | 153.46 KiB（157,140 bytes） | `4deaf8dec709342452fc69bd75735098b4df305dc4c0be73fa9621f80be0ea27` |
| `antibody_benchmark/pdbs/3MJ9_l_u.pdb` | 154.41 KiB（158,115 bytes） | `3b4087e2cf2f5deab4237e0af044a5a2f07d25257d45f1a80bcb3c8683ded49b` |
| `antibody_benchmark/pdbs/3MJ9_r_b.pdb` | 249.49 KiB（255,474 bytes） | `34d9e20fbc948b3eaef6cd6c2d7d1d5a127c7b4a5e97172f59e1117cd635e5ae` |
| `antibody_benchmark/pdbs/3MJ9_r_u.pdb` | 256.13 KiB（262,280 bytes） | `de665883e52e700b3752f1bfa95a7aed52953d81b969561f8c6e6d8b96d93bcc` |
| `antibody_benchmark/pdbs/3MXW_l_b.pdb` | 96.98 KiB（99,306 bytes） | `19447d39579011b5f7ab0b39e850af4f33b15d8a19788bf7905d60bd8ba8f4b9` |
| `antibody_benchmark/pdbs/3MXW_l_u.pdb` | 103.07 KiB（105,543 bytes） | `5ddebabcec72203206caa34a11c0820502cd2ba02cc86a6b458b3e7c27c5e260` |
| `antibody_benchmark/pdbs/3MXW_r_b.pdb` | 261.91 KiB（268,191 bytes） | `214086790c99863f66f89629f2cf2758a7f6f9c8823a9a8bc09970e8e36e30ce` |
| `antibody_benchmark/pdbs/3MXW_r_u.pdb` | 261.91 KiB（268,191 bytes） | `46f47d3e24ab73fa6aa0d79ab3fbb87df97b0fecdba2a3d6417d08cfaea65dcd` |
| `antibody_benchmark/pdbs/3RJQ_l_b.pdb` | 190.95 KiB（195,534 bytes） | `4c3d48412e3f348d6d9ab8b78e7d1977d1c51e9e7127705e9681380fa8fe5032` |
| `antibody_benchmark/pdbs/3RJQ_l_u.pdb` | 229.06 KiB（234,558 bytes） | `1549b6c9767db4443fc397aaf71608e58cbe452db05c373fa2afdb1da58cb6f4` |
| `antibody_benchmark/pdbs/3RJQ_r_b.pdb` | 77.20 KiB（79,056 bytes） | `6d27dbd0145934fe924fdebe0858332a3d7d43585a802620fa6a36c04a22a8b2` |
| `antibody_benchmark/pdbs/3RJQ_r_u.pdb` | 80.33 KiB（82,253 bytes） | `8e86e8acaa7044b80a3cc84a48b0cdce5453c084ed5112d3813e30fe1cddfe5e` |
| `antibody_benchmark/pdbs/3RVW_l_b.pdb` | 139.06 KiB（142,398 bytes） | `38b21dfec7a66fcf6249181d73752061df379ad563d5fc80af9e77b36a0a3630` |
| `antibody_benchmark/pdbs/3RVW_l_u.pdb` | 138.67 KiB（141,993 bytes） | `841e25140dae856e5dea59556217ae23cffed6709d5498b9809292caef0fa48e` |
| `antibody_benchmark/pdbs/3RVW_r_b.pdb` | 263.09 KiB（269,406 bytes） | `3b55eabe79cb0950038605afe35b4676670337aab09dd671148c88e72489c08c` |
| `antibody_benchmark/pdbs/3RVW_r_u.pdb` | 267.21 KiB（273,618 bytes） | `5806d07d08eadeed05ae1588a48f6e43b4ea20edd5a9fab7bb1a3df6fe00bb0c` |
| `antibody_benchmark/pdbs/3SE8_l_b.pdb` | 225.99 KiB（231,417 bytes） | `19ebb92d59dc47e8708f6d6050cf722d02c762cabd3310dac1e22e8c3663fa9e` |
| `antibody_benchmark/pdbs/3SE8_l_u.pdb` | 229.55 KiB（235,056 bytes） | `9604fcf081b5a8d4f3d172c764071418c77c84d3689140ca7fb9f9b79febf46e` |
| `antibody_benchmark/pdbs/3SE8_r_b.pdb` | 269.34 KiB（275,805 bytes） | `9b3e1a110c0ab876809c0b99f4a7b7525ee2e62eddd3754a0edaaa2af1380bbf` |
| `antibody_benchmark/pdbs/3SE8_r_u.pdb` | 277.29 KiB（283,943 bytes） | `e6b1c2bc815ed712869f2697b5b15b3a614e74c63ae4f821030edd4593b37804` |
| `antibody_benchmark/pdbs/3U7Y_l_b.pdb` | 220.22 KiB（225,504 bytes） | `b80909c79dd6c12591a50c147f64f27e212cf7533aa68fa3c4bd6b9f582fca12` |
| `antibody_benchmark/pdbs/3U7Y_l_u.pdb` | 229.55 KiB（235,056 bytes） | `bf9a51f32ec6c7ecb5644f4ee6ef99191850eef6f8e90cf5b5cea3d3e0278e0f` |
| `antibody_benchmark/pdbs/3U7Y_r_b.pdb` | 264.36 KiB（270,702 bytes） | `51cd2efef47bd88cc5f2551251b63848745b8e2dee14b98bc828adc45d13dbef` |
| `antibody_benchmark/pdbs/3U7Y_r_u.pdb` | 276.96 KiB（283,611 bytes） | `a7dc8a91999c805add58846ad071d4e670e8859c5f3b561fc0aebc2c6e3c5777` |
| `antibody_benchmark/pdbs/3V6Z_l_b.pdb` | 93.50 KiB（95,742 bytes） | `e542b786b42b0bf1fe74900453cb378642b6c9f57f817d9a1eeac35bb1206ef8` |
| `antibody_benchmark/pdbs/3V6Z_l_u.pdb` | 88.99 KiB（91,125 bytes） | `85e1bc83378a6e35e7c55b0410e1bd82c31586ed08883e604f521b6e32afdd9f` |
| `antibody_benchmark/pdbs/3V6Z_r_b.pdb` | 265.70 KiB（272,079 bytes） | `ae1fab84ffc91a621ab140618b3455d316098dbf625862bb0628c8c3f82d7690` |
| `antibody_benchmark/pdbs/3V6Z_r_u.pdb` | 263.96 KiB（270,297 bytes） | `356e08efb5417644847e5b95d040382cfe3c5e671cb82538a7bd1ebe49035af5` |
| `antibody_benchmark/pdbs/3WD5_l_b.pdb` | 281.68 KiB（288,441 bytes） | `01b6d6d627c2fb28649de984882b2d4d8a905e9fbb6a1bf2a8dcd36299738ebf` |
| `antibody_benchmark/pdbs/3WD5_l_u.pdb` | 287.91 KiB（294,816 bytes） | `c04a4fe2b1cf77702f8d8478e6a62d8ecad8f2456780c4e2d72b7c1c7f247931` |
| `antibody_benchmark/pdbs/3WD5_r_b.pdb` | 256.68 KiB（262,845 bytes） | `92ed6801735ac0fa9b07aa7e233d789a8a08e056d56ca977de3b3fc084fe7725` |
| `antibody_benchmark/pdbs/3WD5_r_u.pdb` | 252.08 KiB（258,130 bytes） | `fc3ecd5fe025b4ebd84355be9c843a0946d2dff81c7b78ccf89b01bc5a42d455` |
| `antibody_benchmark/pdbs/4DN4_l_b.pdb` | 38.44 KiB（39,366 bytes） | `6f63009ceb436af239b35da90ddfb42fe43f94acfb4532be9dbee35676b39a4e` |
| `antibody_benchmark/pdbs/4DN4_l_u.pdb` | 44.93 KiB（46,008 bytes） | `625652e66c470d8cc61b5109131f899bcdd70c6869c871b8b72e6f36f1846fef` |
| `antibody_benchmark/pdbs/4DN4_r_b.pdb` | 254.94 KiB（261,063 bytes） | `b7a0e66741a6770792dae28cf353fc3ccc5cb9426dae7a72d0f33880eae5fe03` |
| `antibody_benchmark/pdbs/4DN4_r_u.pdb` | 253.76 KiB（259,848 bytes） | `b9f98a56ed5884ffb15bbbcc0eaf96bdcaf3259121ce5181fe374e08808936ba` |
| `antibody_benchmark/pdbs/4DW2_l_b.pdb` | 139.46 KiB（142,803 bytes） | `e73e02943a6d9834abf2eca27b8e791a73d4acd77be43112105ba4f6dd05b094` |
| `antibody_benchmark/pdbs/4DW2_l_u.pdb` | 159.84 KiB（163,676 bytes） | `5782c8e1b4bb12b64608c6c8798778785d8316aeee6a19fed7f56faef23c9a24` |
| `antibody_benchmark/pdbs/4DW2_r_b.pdb` | 257.00 KiB（263,169 bytes） | `eb87537808e4d18b4030f9a37604c366c57c8f466395e894b751c698e9a2687c` |
| `antibody_benchmark/pdbs/4DW2_r_u.pdb` | 265.62 KiB（271,991 bytes） | `d1fb0d6a9ddf0adfc41b186d5f6f620b06cb52f6e0936f4f312b3689ff17bb3f` |
| `antibody_benchmark/pdbs/4ETQ_l_b.pdb` | 141.83 KiB（145,233 bytes） | `db93e2f32b8ea8ca9d8fbd48d9f91fde8de095773cbb6978c4a36acb8eb288d5` |
| `antibody_benchmark/pdbs/4ETQ_l_u.pdb` | 152.30 KiB（155,957 bytes） | `4f38208c49837c42a19477a1e44c63a210bfbd3f67a722d5d999df7fb4f6e9f9` |
| `antibody_benchmark/pdbs/4ETQ_r_b.pdb` | 260.01 KiB（266,247 bytes） | `c9b1400b03d9e8fce413a6a83e69747914b76f19c74be399007369d28410d737` |
| `antibody_benchmark/pdbs/4ETQ_r_u.pdb` | 267.40 KiB（273,817 bytes） | `23859db5bdb89ac07191e4424ac77069028d4e88bdf15f2c6efc91233f2bbb34` |
| `antibody_benchmark/pdbs/4FP8_l_b.pdb` | 165.08 KiB（169,047 bytes） | `40e4636dc1bfda4205e1c6da7450124a10a9b998f484b8ca676f6ec59805733d` |
| `antibody_benchmark/pdbs/4FP8_l_u.pdb` | 932.29 KiB（954,666 bytes） | `6169b441bf3ae185e2c6837665320dc9fd5d3b2feb5d466acbecf8878f87a13e` |
| `antibody_benchmark/pdbs/4FP8_r_b.pdb` | 270.13 KiB（276,615 bytes） | `6913c5a2932cb0d7b99073b4daac0eaaceb5de2bf2e4005f94b668f7b818b04c` |
| `antibody_benchmark/pdbs/4FP8_r_u.pdb` | 273.96 KiB（280,540 bytes） | `a3503d17bb4c821d0c7e3f0d9a3a73d70f522e523da28a128a06eb9ca204af9c` |
| `antibody_benchmark/pdbs/4FQI_l_b.pdb` | 946.85 KiB（969,570 bytes） | `57ec4551a5185dc3bef81eb1868d4c9e975056933c8575a65fa2dca32d3e79c9` |
| `antibody_benchmark/pdbs/4FQI_l_u.pdb` | 941.86 KiB（964,467 bytes） | `414f8a626770e451fba6d260d869247c4358cdf2972311fffdf65366f2ef29f7` |
| `antibody_benchmark/pdbs/4FQI_r_b.pdb` | 250.28 KiB（256,284 bytes） | `32fbfd421018a9973e9c8bc314945bb8a432f1a028726baa8faebae9e484c135` |
| `antibody_benchmark/pdbs/4FQI_r_u.pdb` | 254.47 KiB（260,577 bytes） | `da80c52d4e3a3dfb198f35a85fb06d29a29d7700c47932d4a622228b2bf53537` |
| `antibody_benchmark/pdbs/4G6J_l_b.pdb` | 94.37 KiB（96,633 bytes） | `036d34e7931d060e71237e077aaf356c505259beea130bd772ca65d3d6b15576` |
| `antibody_benchmark/pdbs/4G6J_l_u.pdb` | 95.40 KiB（97,686 bytes） | `9909544290cd62f4600c4514767c56c2ab9306834b5ff8887216d2141d38533d` |
| `antibody_benchmark/pdbs/4G6J_r_b.pdb` | 258.90 KiB（265,113 bytes） | `c704f8971a38b95a6daef0bc3fa294342ad040166266d7111751fbf9e51d1931` |
| `antibody_benchmark/pdbs/4G6J_r_u.pdb` | 258.90 KiB（265,113 bytes） | `bf76e0a794404370331d1965744ed2069c239ab8d49f88b513219176d17279ca` |
| `antibody_benchmark/pdbs/4G6M_l_b.pdb` | 95.00 KiB（97,281 bytes） | `12f122f559f80c0787fba5316f7269781205ea74e1e428b89cf284002bdb0e49` |
| `antibody_benchmark/pdbs/4G6M_l_u.pdb` | 95.40 KiB（97,686 bytes） | `00743481c976bd5eb4af8930634cb674ec23d0dd7388626721617d05ac0fd7dd` |
| `antibody_benchmark/pdbs/4G6M_r_b.pdb` | 261.04 KiB（267,300 bytes） | `3cc2eb8e2f69fcb68f4db71e4868ef45ee1a22909514f57360cc1c9dc62bc831` |
| `antibody_benchmark/pdbs/4G6M_r_u.pdb` | 260.32 KiB（266,571 bytes） | `7d537474f0bb6409bab9ab160b4c6adafc9ad060aa51fde2a9953d2cb546fc5d` |
| `antibody_benchmark/pdbs/4GXU_l_b.pdb` | 933.09 KiB（955,485 bytes） | `3786b3e6e83e25e2242f40fd88d522de68a389bfdb4ef9bd6a86fdd7a34251ab` |
| `antibody_benchmark/pdbs/4GXU_l_u.pdb` | 901.05 KiB（922,671 bytes） | `8af9b21c30cf104c87484689570d6bd379399c85db4cca1be9999ab3b9693afb` |
| `antibody_benchmark/pdbs/4GXU_r_b.pdb` | 260.48 KiB（266,733 bytes） | `0df9ea32bf920807ee271f49177c99393e7a83726e632a3ded2632f0e07ec74a` |
| `antibody_benchmark/pdbs/4GXU_r_u.pdb` | 260.48 KiB（266,733 bytes） | `eab0528ad447180af8453651d5074450a21e2ba1b95be35ceb49d587fa3ac9a4` |
| `antibody_benchmark/pdbs/4M3K_l_b.pdb` | 160.73 KiB（164,592 bytes） | `10baeb05880fb44ba8e6830b537faec119147c973fb2782a13e75a6218a1fe7e` |
| `antibody_benchmark/pdbs/4M3K_l_u.pdb` | 162.76 KiB（166,664 bytes） | `82863b6d99e7b59677fbf1efb1f601e6c383a776ec50d41f09c77b045391a3b1` |
| `antibody_benchmark/pdbs/4M3K_r_b.pdb` | 68.03 KiB（69,660 bytes） | `b67a584d9ef07ae6c7a105639a5abb571b8da2e02b081c3eedc274d5867864ab` |
| `antibody_benchmark/pdbs/4M3K_r_u.pdb` | 70.11 KiB（71,795 bytes） | `f893ab6f6ba550fc220dd8f52c232c70f4c32ee0a906f56a70ee43372b2072b6` |
| `antibody_benchmark/pdbs/4M5Z_l_b.pdb` | 132.42 KiB（135,594 bytes） | `8187e67ebc18dd2483b2f97e44eb4b391d9102e8f5e3da9758eb061fcbad9553` |
| `antibody_benchmark/pdbs/4M5Z_l_u.pdb` | 137.31 KiB（140,602 bytes） | `e18ddd54ae4438dbd2e17c821063737e4a3f54306bb24034bcdbd272e5abb367` |
| `antibody_benchmark/pdbs/4M5Z_r_b.pdb` | 257.40 KiB（263,574 bytes） | `4d4e9ab6dab06b37ba40323b3ae9213bd87a2b5ce497dac5cf640d4683af1525` |
| `antibody_benchmark/pdbs/4M5Z_r_u.pdb` | 265.37 KiB（271,742 bytes） | `623b9e3f788c05182456a0594bb426a8d04ebecb6d562c6f2bdfb93c10f89e5c` |
| `antibody_benchmark/pdbs/4POU_l_b.pdb` | 72.93 KiB（74,682 bytes） | `d667ed2ed480ab803c523c8340218428ed9a26d7dd2ae7ab258292cad3930d4c` |
| `antibody_benchmark/pdbs/4POU_l_u.pdb` | 78.06 KiB（79,929 bytes） | `26f7a2d42acaa20bd3baf5d7e57a85bd9a60ceb32076369c64dd2763f994f76e` |
| `antibody_benchmark/pdbs/4POU_r_b.pdb` | 71.51 KiB（73,224 bytes） | `4484eb9d5612ac83de20758fcc23867ac51fbb1f613a6e5d7cfd5c1c26455254` |
| `antibody_benchmark/pdbs/4POU_r_u.pdb` | 73.60 KiB（75,364 bytes） | `a661c11dadf27eafed2d6c3d453e44a9f968a47b0d6af040969c07d26ed4f01a` |
| `antibody_benchmark/pdbs/4Y7M_l_b.pdb` | 147.60 KiB（151,146 bytes） | `2d354b7609aa28dd27829c3463d66035ed6bbd5283094a4a7413a2ba00873862` |
| `antibody_benchmark/pdbs/4Y7M_l_u.pdb` | 148.17 KiB（151,724 bytes） | `9d3bc09bfee4094f8144d06932beefb718a17c856362494850b25d505dcdb63b` |
| `antibody_benchmark/pdbs/4Y7M_r_b.pdb` | 75.86 KiB（77,679 bytes） | `ad4e6c5fe68f5f3d9d2187b9e5fffd24eb141c6b613e08e11b619f0add4f8daf` |
| `antibody_benchmark/pdbs/4Y7M_r_u.pdb` | 80.73 KiB（82,668 bytes） | `127b957cca7a26544ae2db1543896e8b6c56f5937b80e6d3a0dd0698ccbde3a2` |
| `antibody_benchmark/pdbs/5C7X_l_b.pdb` | 73.25 KiB（75,006 bytes） | `c123d34918bb17b6f01422f1c6351dc32aa9508a0e0106673e737aa47fcc48e1` |
| `antibody_benchmark/pdbs/5C7X_l_u.pdb` | 78.70 KiB（80,593 bytes） | `4d593264a2e077dcd72ec4277be597b278f342d7b602c777e0eefd93dec7aba4` |
| `antibody_benchmark/pdbs/5C7X_r_b.pdb` | 251.62 KiB（257,661 bytes） | `a3879deac0dc68775683c93e7f9241f67e4123b7323362b152227f89d792ef5f` |
| `antibody_benchmark/pdbs/5C7X_r_u.pdb` | 256.70 KiB（262,861 bytes） | `703e5b1293897b43cd12465ddde7c39bccd399b149637f0f84f43b92df511624` |
| `antibody_benchmark/pdbs/5CBA_l_b.pdb` | 38.92 KiB（39,852 bytes） | `aad41e4b061b22a6f958d5f039f78a2fe5593c9c1974e5483e127152396f1174` |
| `antibody_benchmark/pdbs/5CBA_l_u.pdb` | 53.50 KiB（54,780 bytes） | `aeb997acd99294419202107f2cdb34a4ccbc47e3193edda2112dda9730d27c42` |
| `antibody_benchmark/pdbs/5CBA_r_b.pdb` | 143.49 KiB（146,934 bytes） | `ebd6913d9a7c38c381d886cb41ecf073fc75cbd51a9f0a68972aa4e7f5de7d57` |
| `antibody_benchmark/pdbs/5CBA_r_u.pdb` | 146.63 KiB（150,147 bytes） | `a6453ef32caaa4ed5af98211580c82581399b559dfeb436e855298255ddc2cb5` |
| `antibody_benchmark/pdbs/5E5M_l_b.pdb` | 70.88 KiB（72,576 bytes） | `19b5b83cdc3f4f871b5a1dc604428f1a6be483a9f80401b12ffe3a3b26ef482d` |
| `antibody_benchmark/pdbs/5E5M_l_u.pdb` | 72.87 KiB（74,617 bytes） | `cc60b4decc67a1c0183f1b94380cb7cfaffaea86648e80953e2f0b38eceb2bc1` |
| `antibody_benchmark/pdbs/5E5M_r_b.pdb` | 65.97 KiB（67,554 bytes） | `6b9e43246bb8649f04d90762e151eaba8eab6571bd23c7414de0807b7de44dd0` |
| `antibody_benchmark/pdbs/5E5M_r_u.pdb` | 68.09 KiB（69,720 bytes） | `221a4ca59d23856c6a8d5a5a69def581ad072ae7804b35094b3c0481ed42d09c` |
| `antibody_benchmark/pdbs/5GRJ_l_b.pdb` | 134.95 KiB（138,186 bytes） | `11ce1080538b16c57f6f4c6be3e0ef0294ed6ed497820be1efea1a2a1ef052cf` |
| `antibody_benchmark/pdbs/5GRJ_l_u.pdb` | 138.44 KiB（141,764 bytes） | `8585f25540a6b3e46cf7e086a7995671cf6f935b69dad946056e0380b5e10173` |
| `antibody_benchmark/pdbs/5GRJ_r_b.pdb` | 133.84 KiB（137,052 bytes） | `2a74dd9a7fbf72a2c8496ce7c920fe5bad41d0f3c0da8dc480d909cc2851e35b` |
| `antibody_benchmark/pdbs/5GRJ_r_u.pdb` | 261.64 KiB（267,924 bytes） | `740d083f0052edef88686bfee87ee2792ca0325d07a227c9d953d21ee90a17ad` |
| `antibody_benchmark/pdbs/5HGG_l_b.pdb` | 154.56 KiB（158,274 bytes） | `54bba59d303db7b3fc0175c902e6fab166a00ebf2c15a9317a73b61490d00946` |
| `antibody_benchmark/pdbs/5HGG_l_u.pdb` | 162.19 KiB（166,083 bytes） | `98ebd158d6abeae5e0fa35551dc3fbd3f858c4a8ad001ba5f886da903deafb5a` |
| `antibody_benchmark/pdbs/5HGG_r_b.pdb` | 77.84 KiB（79,704 bytes） | `735b1c8aa0fbf4ec72be6eb2b6db406f525395f77f32defc1586f94a27e7ef40` |
| `antibody_benchmark/pdbs/5HGG_r_u.pdb` | 76.68 KiB（78,518 bytes） | `2d1a242b4a6e09847dd2194b3ce48547d03f9df1e6ad5814a1ec9156208396be` |
| `antibody_benchmark/pdbs/5HYS_l_b.pdb` | 280.42 KiB（287,145 bytes） | `be5a7357f74af23cb7a08cd498d76a62cdf6c70eb3450cd670f3fb430373ca60` |
| `antibody_benchmark/pdbs/5HYS_l_u.pdb` | 281.50 KiB（288,259 bytes） | `965c62f3357a28477f4959b71c2c143f900dc8d02c888e6f751e0a3a943a8198` |
| `antibody_benchmark/pdbs/5HYS_r_b.pdb` | 268.31 KiB（274,752 bytes） | `8f09184daa6ddc81ee89f5334b6cc4f98c2ffed142139b8d23987ea353d02407` |
| `antibody_benchmark/pdbs/5HYS_r_u.pdb` | 269.51 KiB（275,975 bytes） | `d8a2e0824ad24f455da30beecf2dcd44c3ef783488f5f06068e324f29fa23c73` |
| `antibody_benchmark/pdbs/5JMO_l_b.pdb` | 286.58 KiB（293,463 bytes） | `e7aa3f0f57ee99db95ee2eaa62fb966a76a51d21aa9bc661e06b33762e83b35f` |
| `antibody_benchmark/pdbs/5JMO_l_u.pdb` | 292.28 KiB（299,298 bytes） | `8e5222b86cc6587f380e49efb4f90cd00478e5fac261219173d776ded1bc9d91` |
| `antibody_benchmark/pdbs/5JMO_r_b.pdb` | 70.00 KiB（71,685 bytes） | `2c9a05b9bb29a0cd7d42c87762d10eda1cedbd184295ff0f20fd13287473c2f0` |
| `antibody_benchmark/pdbs/5JMO_r_u.pdb` | 71.81 KiB（73,538 bytes） | `0446340afd961b7197ef7895b3466c9c751b1fabf1ae8b3fa07aab8e26c2880f` |
| `antibody_benchmark/pdbs/5KOV_l_b.pdb` | 276.93 KiB（283,581 bytes） | `b0b8b8dff274342b4387e1fd8c9d8fc5f8b09158eeb55586ef5b86aa9e1f6bc7` |
| `antibody_benchmark/pdbs/5KOV_l_u.pdb` | 287.66 KiB（294,567 bytes） | `1f59fbbe95574b4a9cad07c52a6dc75067c23f2a00211ce93ce32ae209af6123` |
| `antibody_benchmark/pdbs/5KOV_r_b.pdb` | 137.64 KiB（140,940 bytes） | `664105ab8518aab2d5555308bb695164c8988e9f85fbb7dc58c963c0beeacbd5` |
| `antibody_benchmark/pdbs/5KOV_r_u.pdb` | 264.48 KiB（270,829 bytes） | `de631ef651d85f5af08718bbae10d3f7981ed50c4bbe05126cb4e7f1b08bcd14` |
| `antibody_benchmark/pdbs/5O14_l_b.pdb` | 134.79 KiB（138,024 bytes） | `4076e65526b9c09e55683ec45894044910ad44527806a1361efecacb0527e4f8` |
| `antibody_benchmark/pdbs/5O14_l_u.pdb` | 148.17 KiB（151,724 bytes） | `3a2d3675dae4906ad6aa4ef03752afa407db31fd777b57d31e8d933da944c195` |
| `antibody_benchmark/pdbs/5O14_r_b.pdb` | 257.08 KiB（263,250 bytes） | `6cf365a8172c923d656e1582a1e705eba7098f67ebf8e04012ec25c4e51aeab6` |
| `antibody_benchmark/pdbs/5O14_r_u.pdb` | 274.21 KiB（280,789 bytes） | `f6ca78d3801ef5180d5498ea608a2d7015f60e2f5b3fc6bd40d36c2c6a221312` |
| `antibody_benchmark/pdbs/5O1R_l_b.pdb` | 68.50 KiB（70,146 bytes） | `853a74c3f6ab046d02343f32de5b35a74569acfe35174199b9548bf3cbfe58d2` |
| `antibody_benchmark/pdbs/5O1R_l_u.pdb` | 92.73 KiB（94,952 bytes） | `ce2bfd687e4e2d77b57b326ebbfe503706f1516919a647d973bbd91b5b2f76cb` |
| `antibody_benchmark/pdbs/5O1R_r_b.pdb` | 259.53 KiB（265,761 bytes） | `fa0811c0f55985cd404b637b0cddf5db07cb73d94ad85be747b690a7c3be6fc4` |
| `antibody_benchmark/pdbs/5O1R_r_u.pdb` | 266.83 KiB（273,236 bytes） | `3e5d4168f85de0e4dd64bc6d5c5be19a7293f8ad2d818f5dd68a4709dc2c900d` |
| `antibody_benchmark/pdbs/5SV3_l_b.pdb` | 104.57 KiB（107,082 bytes） | `ba5f4237aa291331a07b1e78480f7171242130f5d94c02d50ef03819129bb19d` |
| `antibody_benchmark/pdbs/5SV3_l_u.pdb` | 165.19 KiB（169,154 bytes） | `f465dc139e28a38bde42ba06e95f2e5d33fa0e31fbad8321c805522fbe17cb11` |
| `antibody_benchmark/pdbs/5SV3_r_b.pdb` | 74.83 KiB（76,626 bytes） | `d60d11429a4a2e0acd3abad0af0a2936ff687761112c7e665f97ffba99481bd6` |
| `antibody_benchmark/pdbs/5SV3_r_u.pdb` | 78.22 KiB（80,095 bytes） | `91522d0fdfecfabc87cec1b94ce41b762e20a6696f75319d16f52a386359926e` |
| `antibody_benchmark/pdbs/5VNW_l_b.pdb` | 367.82 KiB（376,650 bytes） | `a93b8a2cc16c781f4150870d8b3ec69236007bd38a322879a82e9f37dc699f3e` |
| `antibody_benchmark/pdbs/5VNW_l_u.pdb` | 351.70 KiB（360,137 bytes） | `8ddbb765b5858535f4ef93748dfb67a6746aece3c036bfa2eea98addb23cc20b` |
| `antibody_benchmark/pdbs/5VNW_r_b.pdb` | 73.96 KiB（75,735 bytes） | `0e9abb380fc96685b6dc940b1a20995ee81271d59dc7e2aa9f6a89749b2e13c8` |
| `antibody_benchmark/pdbs/5VNW_r_u.pdb` | 77.97 KiB（79,846 bytes） | `ff903eeb57b10580846abb2ea912599e4021d3f83a2b69d8a31c6d60f6f7f9be` |
| `antibody_benchmark/pdbs/5WHK_l_b.pdb` | 219.67 KiB（224,937 bytes） | `72132177f4bcd98dc0f9fa89db9359b79e0c96ce14c3fd5bdd4dff04bf13f8cf` |
| `antibody_benchmark/pdbs/5WHK_l_u.pdb` | 234.90 KiB（240,534 bytes） | `5c1aa839bbc22c0ede0b798a3b3ba4a7e9c6cd151f5495c808fbec0b97f10709` |
| `antibody_benchmark/pdbs/5WHK_r_b.pdb` | 244.19 KiB（250,047 bytes） | `a25cdf1cbef52bfe0ff999c871842b86aa96b8d1e481f98673e34de43cc878fc` |
| `antibody_benchmark/pdbs/5WHK_r_u.pdb` | 250.54 KiB（256,553 bytes） | `7246c3df9d13d567894c6fca69632ddb6113a4cf04e8b6cd1ad15b7dd868ecad` |
| `antibody_benchmark/pdbs/5WK3_l_b.pdb` | 36.54 KiB（37,422 bytes） | `df407ff8b8bbd37e87ba9c05bf7bda4f017df1dd063de5da4477fbb35237dabd` |
| `antibody_benchmark/pdbs/5WK3_l_u.pdb` | 44.90 KiB（45,982 bytes） | `de16a3c94ca8a67ac63ad8db1ff18e5861425b7eba7967c10ccd4b764c6028a4` |
| `antibody_benchmark/pdbs/5WK3_r_b.pdb` | 262.85 KiB（269,163 bytes） | `8cfe95e5d879691857bee84401f5920e9ec6bf6e9c0e86ce7e924c435776f9f6` |
| `antibody_benchmark/pdbs/5WK3_r_u.pdb` | 272.91 KiB（279,461 bytes） | `3ab6ed651461e3f282d59bfd9d844e90e277269d72245ae1ed1725697c7b2a35` |
| `antibody_benchmark/pdbs/5WUX_l_b.pdb` | 258.27 KiB（264,465 bytes） | `4df1a22044956b2832d1de40b8722f49b5cfc235f5a709bdf37d9798ba7c7b51` |
| `antibody_benchmark/pdbs/5WUX_l_u.pdb` | 287.91 KiB（294,816 bytes） | `09f153027c26cbeb025045e84e04484ff024f38fa797f20c394d82b7f2abd74f` |
| `antibody_benchmark/pdbs/5WUX_r_b.pdb` | 256.45 KiB（262,602 bytes） | `00af1620fa33e47dd609a4de2f9fe4002cbd99c6ab6a5dccc4477e4c12306cdc` |
| `antibody_benchmark/pdbs/5WUX_r_u.pdb` | 266.67 KiB（273,070 bytes） | `b708c319c4cd53fc71f31d6b97ade12003cefde9dcd9f1f9b800b0654b851c91` |
| `antibody_benchmark/pdbs/5X0T_l_b.pdb` | 47.38 KiB（48,519 bytes） | `ea3cbcf5c5d85c052c796082c3701c4bc87d2cc6cdea2bf13aeed60636e10427` |
| `antibody_benchmark/pdbs/5X0T_l_u.pdb` | 112.58 KiB（115,287 bytes） | `a49b1840587861c9df755f0e472a39491945c9886a8e4b253206fc5a4c4ee9e8` |
| `antibody_benchmark/pdbs/5X0T_r_b.pdb` | 260.80 KiB（267,057 bytes） | `b739e53dde10a6ec01c18880aaae45a9ff8985bcc918db4bf22dcdef0192f4e9` |
| `antibody_benchmark/pdbs/5X0T_r_u.pdb` | 267.24 KiB（273,651 bytes） | `b670ba77090b12c36d0bc1d80b743824641c3d982bc89cd51123cbd88f61a97d` |
| `antibody_benchmark/pdbs/5Y9J_l_b.pdb` | 271.24 KiB（277,749 bytes） | `f2e16b6a88b69e1989d704da5d26b1e32a57b461c2adf17186f3f3dd4e000950` |
| `antibody_benchmark/pdbs/5Y9J_l_u.pdb` | 285.64 KiB（292,492 bytes） | `90bf7cd25e0972617ff98bc070c369f75008a4afcde4810d310c0cb83992c9a5` |
| `antibody_benchmark/pdbs/5Y9J_r_b.pdb` | 252.10 KiB（258,147 bytes） | `32f47ab2e7e724c4a84432567232c38dab699f1b8d98941fe26d95b577b6176e` |
| `antibody_benchmark/pdbs/5Y9J_r_u.pdb` | 257.02 KiB（263,193 bytes） | `4aa76e04645083d81142aa39373d196b85ac812dd1137a524a44eb1df9605217` |
| `antibody_benchmark/pdbs/6A0Z_l_b.pdb` | 172.44 KiB（176,580 bytes） | `0fe43ff93bda1a43d04a7a21e2535d16f3b8381fb8e8c9fd90ecf0feb5dfc3b8` |
| `antibody_benchmark/pdbs/6A0Z_l_u.pdb` | 212.36 KiB（217,460 bytes） | `bd8c26bb264b1d2352da77a3ecabc107fd38a70780eb05b8a4beb5dfd0fe9b38` |
| `antibody_benchmark/pdbs/6A0Z_r_b.pdb` | 263.01 KiB（269,325 bytes） | `815c97dc639ece990b9358026654e099a48f7521f72aaf159200af8246679ad6` |
| `antibody_benchmark/pdbs/6A0Z_r_u.pdb` | 270.72 KiB（277,220 bytes） | `184404a6256ed737deaec8e843c6993661058bbc44231e8d6d274b5e4ced87b3` |
| `antibody_benchmark/pdbs/6A77_l_b.pdb` | 54.26 KiB（55,566 bytes） | `676133e91af5cbe49b38cca69adfed6802a13c20eb400596513d905ba9df7dbb` |
| `antibody_benchmark/pdbs/6A77_l_u.pdb` | 55.85 KiB（57,187 bytes） | `7275ea0bc942a1514ca9d48a511d3a58e60544fca7dd639d795d92f8df66f3b5` |
| `antibody_benchmark/pdbs/6A77_r_b.pdb` | 256.68 KiB（262,845 bytes） | `f45a049682d5eaad0ba6e0d2bbcce72b8d0f310ab1cc505fe32a07a13eaa9286` |
| `antibody_benchmark/pdbs/6A77_r_u.pdb` | 261.56 KiB（267,841 bytes） | `d3651dea7b5b1f413b03e6c45a9d46d03e0411d23206c5c1a6047a518d4df764` |
| `antibody_benchmark/pdbs/6AL0_l_b.pdb` | 113.12 KiB（115,830 bytes） | `19c3cdaa2f7a2109d4c868324e905a6699b794500cc287e8ff35d1cc5d33ed92` |
| `antibody_benchmark/pdbs/6AL0_l_u.pdb` | 117.29 KiB（120,101 bytes） | `eac296eeaa48a5b2748a4c1765da507460680bc223ddbbf195d396fec347c992` |
| `antibody_benchmark/pdbs/6AL0_r_b.pdb` | 258.58 KiB（264,789 bytes） | `d4fe99503f04f42d7d30a7d4dcd2d457170adf1991468ee00503d9d7a9f59d8a` |
| `antibody_benchmark/pdbs/6AL0_r_u.pdb` | 258.00 KiB（264,189 bytes） | `9643c5ff4a797089a6b28ff9c582502db19dcabb79f7f4d183d95cfa2b660818` |
| `antibody_benchmark/pdbs/6B0S_l_b.pdb` | 39.95 KiB（40,905 bytes） | `620d53d25f5b88b0862591ea7bc057afb8091bdda956d1afc789ad1952e71549` |
| `antibody_benchmark/pdbs/6B0S_l_u.pdb` | 45.96 KiB（47,061 bytes） | `01cd2b28cd7d6302d94f717ddfeeba48fde98cf3b4f919d4858a38c93b6fc897` |
| `antibody_benchmark/pdbs/6B0S_r_b.pdb` | 254.79 KiB（260,901 bytes） | `edd90e191b636ccb4167b4c26e104263f9a55c82d2291a64b85500c5cca52d34` |
| `antibody_benchmark/pdbs/6B0S_r_u.pdb` | 266.18 KiB（272,572 bytes） | `542d59f45105a43a85ece6900dddc83d0e7ffb01b5cc13f28bfdb4c2b85f2017` |
| `antibody_benchmark/pdbs/6BPC_l_b.pdb` | 190.63 KiB（195,210 bytes） | `97fc85bb67ce2b8a844f62f0c8c5161a3850cafe782d462213bd93ed5a17ec26` |
| `antibody_benchmark/pdbs/6BPC_l_u.pdb` | 207.74 KiB（212,729 bytes） | `e6e0aac8b35e28fe4967d83ec37062e2f8d324fdf1d7f206c63d13d6bb137bf4` |
| `antibody_benchmark/pdbs/6BPC_r_b.pdb` | 257.48 KiB（263,655 bytes） | `25b9ae0f545cebdd019ca7489d3db8c9de1a1f7e155a412f435d2782dffd4ca6` |
| `antibody_benchmark/pdbs/6BPC_r_u.pdb` | 262.54 KiB（268,837 bytes） | `ab4ffec95ad108cf8f30234506c589e5840794af6e8ba9239d710704897fe65c` |
| `antibody_benchmark/pdbs/6CWG_l_b.pdb` | 164.06 KiB（167,994 bytes） | `9ec1b20795d85500e5a0c966609af11b2cc1d9f11706e366c511b20fa54fa647` |
| `antibody_benchmark/pdbs/6CWG_l_u.pdb` | 165.19 KiB（169,154 bytes） | `0d7f2e0b93d80a5b7acd3b882efc0f40996148e58e4cf4da87d4094d95ed4fbb` |
| `antibody_benchmark/pdbs/6CWG_r_b.pdb` | 74.99 KiB（76,788 bytes） | `4d68c3099db5e4a224ca7c5e36e4efd7f688a0f9d2cf18a736b1c241db909084` |
| `antibody_benchmark/pdbs/6CWG_r_u.pdb` | 79.76 KiB（81,672 bytes） | `24a05fcc89f1bb3a749d39ce160449dcb56aeb871a832ccce587f0b61fcaebb1` |
| `antibody_benchmark/pdbs/6DBG_l_b.pdb` | 176.55 KiB（180,792 bytes） | `75dd6d90ac72e1eac47af39e05ea7fb558785e99d6236eb725df65047d8167dd` |
| `antibody_benchmark/pdbs/6DBG_l_u.pdb` | 185.05 KiB（189,489 bytes） | `a4d8b9fcc330c994cabf347213205be1c18b2b6c74a3f086f95eabb748fdee22` |
| `antibody_benchmark/pdbs/6DBG_r_b.pdb` | 68.50 KiB（70,146 bytes） | `2e61e3fc9d6b8d3d48037ab6814e19517ba20c786f5ec9fe62e3f7d1a39188c3` |
| `antibody_benchmark/pdbs/6DBG_r_u.pdb` | 76.76 KiB（78,601 bytes） | `d0076101e76ba4cccfcd409f1f0f8fef6ef01b2707c858f1be30e183aeb969fe` |
| `antibody_benchmark/pdbs/6EY6_l_b.pdb` | 241.97 KiB（247,779 bytes） | `9d9ea28f48feda335e09da40d9be0c26accd93fe39b7054614151567d49a27f3` |
| `antibody_benchmark/pdbs/6EY6_l_u.pdb` | 362.56 KiB（371,259 bytes） | `7f2584e8bd4bc8909f608728372c95630de80cccff9554338f079045b70138e5` |
| `antibody_benchmark/pdbs/6EY6_r_b.pdb` | 77.60 KiB（79,461 bytes） | `f9e0366548ddb93c239a57820d0ca0651ad2b2f0899fa0f7b209232ff3cee29c` |
| `antibody_benchmark/pdbs/6EY6_r_u.pdb` | 79.51 KiB（81,423 bytes） | `dc6915723f7b3c65a3c8b29911f9876cbddd50c409527554411c6ed7c695115a` |
| `antibody_benchmark/pdbs/6OC3_l_b.pdb` | 134.55 KiB（137,781 bytes） | `3c39a6e14bf20f08a257e7fa139f1367aafc44dc9f894f9a585d06fd65f3dc09` |
| `antibody_benchmark/pdbs/6OC3_l_u.pdb` | 138.93 KiB（142,262 bytes） | `9a7c88cabaabe1d8205fc134ea8d1df923ccc25b28c67071ae1518444b6346b2` |
| `antibody_benchmark/pdbs/6OC3_r_b.pdb` | 262.62 KiB（268,920 bytes） | `7e58fce5789e7faa6dd5c908076d0345412f832dc95f169fd9e9f3331f47014b` |
| `antibody_benchmark/pdbs/6OC3_r_u.pdb` | 267.80 KiB（274,232 bytes） | `7fd93401ea3a063d92633891668c6457cde75a3e2c2d85dae49a74bce51e009f` |
| `antibody_benchmark/preliminary_cases/preliminary_cases.camelids.txt` | 165 bytes | `a29dbd3fc557966411d3404825c5f86be2fefacf4a95411989a25130a17ff433` |
| `antibody_benchmark/preliminary_cases/preliminary_cases.txt` | 645 bytes | `623aebcdf2d2325bd3a46fb70d5d63e00bd54655062954e01481dd4011d005b1` |
| `antibody_benchmark/scripts/README.md` | 2.01 KiB（2,062 bytes） | `1ac0eccffc2b0fd64e2682ccab8950ac48b8ae17844e790161c7ae65eea54d98` |
| `antibody_benchmark/scripts/example/all_antibody_structures_8_2020.txt` | 2.90 MiB（3,042,188 bytes） | `8e205b2d0da3fe33b6a3bbf98094d8d42d57962411ba5771d343d51130631810` |
| `antibody_benchmark/scripts/example/bm5.5.txt` | 335 bytes | `2018615b0815c98ca19f83faea81617e128e3349fb2eab273652687fc4937ef0` |
| `antibody_benchmark/scripts/example/bound_unbound_pdbs.camelids.txt` | 37.56 KiB（38,464 bytes） | `d8740c524368326b4c634ce30a99f8ee698c8a4bcda31cabbbee7f4c47499ee3` |
| `antibody_benchmark/scripts/example/bound_unbound_pdbs.txt` | 96.77 KiB（99,095 bytes） | `cf8aeff174d010d10f2fda5602027ffeadf6a302ce6f26015c7d644abd6444ba` |
| `antibody_benchmark/scripts/example/pdb_resolutions_8_2020.txt` | 1.85 MiB（1,942,929 bytes） | `e52a643d893a4e4352cf1bfe31078de0a956b09ef09e302b6cf39703ed99da79` |
| `antibody_benchmark/scripts/example/pdb_seqres_8_2020.fa.tar.gz` | 30.47 MiB（31,950,231 bytes） | `fcfac4ddc495b81da23e9f25b1adddf448f3dd10316c7eefa4dd769434a47aae` |
| `antibody_benchmark/scripts/get_antibody_benchmark.pl` | 7.32 KiB（7,499 bytes） | `8797310cd3dc950ed0e4227cad8772b7e6ac5069ae5974bb5a90432191020f1e` |
| `antibody_benchmark/scripts/get_antibody_benchmark_camelids.pl` | 7.06 KiB（7,233 bytes） | `206e17984502693d138017cb704c67ee177f5342bb6ae24dfa866bc3b5922021` |
| `antibody_benchmark/scripts/get_cases.pl` | 2.67 KiB（2,730 bytes） | `b95ff50c1640734fffebad161791eb8a18e210218ac3dfb260ab602d52f24cdd` |
| `antibody_benchmark/antibody_benchmark_cases.xlsx` | 15.69 KiB（16,065 bytes） | `6bca70dd05a64f3581f4501d1a238427f05dbc3e079066ed2ec5a9ea97e24965` |

### 许可和再分发边界

固定 Git repository LICENSE 的实际文本为 Creative Commons Attribution 4.0 International；README 同样明确整个 work 采用 CC BY 4.0。原 GNU GPL v2 说明错误，已按实际文件修正。独立官网 XLSX 与论文文本的条件分别保留，不自动以 Git 许可替代。PDB 原始条目与源文献仍需引用。

固定 Git LICENSE 与 README 明确整个 antibody benchmark work 为 CC BY 4.0，而非 GPL v2。另独立核验作者官方完整 Docking Benchmark 5.5 页面：页面列明 Guest 扩展、链接 Pierce 数据仓库，并明确整个 work 使用 Creative Commons Attribution 4.0 International。真实 XLSX 全部 67 个 Complex PDB 及双方 unbound author-chain 键与此官方许可 benchmark 完全一致，许可范围按同一作者 benchmark work 留证，未用出版方论文许可证代替数据许可。官方 HTML 原始字节与 SHA-256、67 项逐一比对结果只存 shared cache。主文是 PMC author manuscript v1，官方 cloud metadata license_code=TDM，XML明确 text-mining/fair-use；内部解释/文本分析归档，不宣称可按 CC BY 再分发论文。原出版方补充 PDF 保留出版方条件与引用，不套用 Git 许可；任何外部再分发必须分别遵循这些数据、文本及 PDB 条款。

### 公开范围对照

| 目标组成 | 当前证据 | 状态 |
| --- | --- | --- |
| 固定上游 payload | tracked config + 独立文件/格式审计 | 目标公开文件验收通过 |
| 论文原文 | 一手 DOI 和取得文件 hash；不可得项明确记录 | 主文与全部被引用附件已归档并解析 |
| PDB 原始序列与全坐标 | 接受锚点两层配对审计 | 两层已齐；非逐变体结构 |
| 完整研究底层数据 | 公开汇编或处理包不等于全部底层实验 | 未宣称获得 |

## 待解决问题与处理进展

截至 `2026-10-09`，本次固定 Git TXT、官网 XLSX、论文附件及结构文件的核验范围内暂无待解决问题。原研究未公开的逐次实验记录不属于本次 raw source 接入范围。
