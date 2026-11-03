---
tags:
  - context
---

# SRC_R80_ANTIPASTI 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [结构、汇总表和筛选数组](#结构汇总表和筛选数组)
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

- `source_id`：`SRC_R80_ANTIPASTI`
- `source_version`：`v1`
- 原作者或发布机构：Kevin Michalewicz、Mauricio Barahona、Barbara Bravi（Imperial College London）。

### 来源方背景

[论文 v1](https://arxiv.org/abs/2410.01523v1) 列明三位作者来自 Imperial College London 数学系；作者在 [Mendeley Data v1](https://doi.org/10.17632/j4rt98xpy7.1) 发布结构文件，在 [ANTIPASTI 仓库](https://github.com/kevinmicha/ANTIPASTI) 发布相关代码和汇总数据。本包把这两个明确不同的交付入口并列保留。

## 实验设计和数据口径

ANTIPASTI 以 SAbDab 收集的抗体-抗原复合物结构和实验解离常数 `KD` 为基础，使用弹性网络模型的正常模态计算残基相关图，再训练卷积神经网络预测亲和力。当前包保存结构和上游汇总/筛选数据，不包含逐行模型推断结果或计算得到的相关图。论文称训练集有 634 个结构；这不是当前 Mendeley 交付的 715 个 PDB 文件数，也不能直接等同于 Git 数组中的 701 个 `selected_entries`。

Git 汇总 TSV 有 1,266 行、715 个唯一 PDB ID；一个 PDB ID 可出现 1 至 12 行，所以行是抗体链、抗原及亲和力注释的记录，不等于独立结构。`affinity` 保留上游以 M（mol/L）记录的解离常数，越小结合越强；`delta_g` 是上游附带的自由能数值，37 行为 `NA`，没有用当前脚本重算。论文描述的筛选会排除特定不完整或不合适的结构；三份长度/筛选数组各 701 项，但公开文件没有可直接证明“634 训练结构 = 701 项中的某个具体子集”的逐项清单。本地 `raw` 表示按来源保存的公开输入，不是最初实验仪器原始记录。

## 论文原文

- 标题：ANTIPASTI: interpretable prediction of antibody binding affinity exploiting Normal Modes and Deep Learning
- 作者：Kevin Michalewicz、Mauricio Barahona、Barbara Bravi。
- 发表来源：arXiv:2410.01523。
- 归档文本版本：arXiv v1。
- 发布日期：2024-10-02。
- DOI：<https://doi.org/10.48550/arXiv.2410.01523>
- PMID / PMCID：无（本次归档版本为 arXiv v1）。
- 本地文件：`articles/ANTIPASTI_2024-10-02_arXiv-v1.pdf`
- 文件大小：9.20 MiB（9642918 bytes）。
- SHA-256：`8e6fc22e663dbaad339834414fad4c5ded701b4909c01ce942a3accd8a135919`
- 文本许可：本次归档 PDF 未给出可直接覆盖数据包的许可；论文文本与数据权利分开处理。
- 补充材料：无单独归档的补充文件。

## 仓库内容

结构文件来自 [Mendeley Data `j4rt98xpy7` v1](https://doi.org/10.17632/j4rt98xpy7.1)，正式版本名为 `v1`；该记录列出 715 个 Chothia 编号 PDB，合计 450435318 bytes。汇总表和 3 个 NumPy 数组来自 [kevinmicha/ANTIPASTI](https://github.com/kevinmicha/ANTIPASTI/tree/a8dc208ee4e33cdba707cbe0c9580f92a9668611) 的固定 commit `a8dc208ee4e33cdba707cbe0c9580f92a9668611`。这是两个上游入口的选择性组合，不是任何一个仓库的完整镜像。

```text
v1/
├── mendeley-data/
│   └── <pdb_id>.pdb (715 files)
└── ANTIPASTI/
    └── data/
        ├── sabdab_summary_all.tsv
        └── chain_lengths/
            ├── heavy_lengths.npy
            ├── light_lengths.npy
            └── selected_entries.npy
```

Mendeley 的 PDB 是作者提供的 Chothia 编号结构；Git 表和数组属于作者代码仓库的配套数据。两者均按原字节保存。

## 数据结构

### 结构、汇总表和筛选数组

715 个 `mendeley-data/<pdb_id>.pdb` 均可由 Biopython PDB parser 读取，文件名 PDB ID 的集合恰与 TSV `pdb` 的 715 个唯一值一致。TSV 是制表符分隔，含 30 列。`selected_entries.npy` 为 701 个 4 字符 ID，均出现在 TSV；另有 14 个 TSV PDB ID 未被选入。`heavy_lengths.npy`、`light_lengths.npy` 均为 701 个 `int64` 元素；按相同长度及文件名可判断它们与筛选列表配套，但数组位置的逐项生成规则尚未由本次归档文件单独证明，不据此重建训练划分。

### 字段说明

下表覆盖 `sabdab_summary_all.tsv` 的全部 30 个原始列。`NA` 是上游缺失编码；`TBD`、`Unknown`、`Other` 均保留原拼写。类别解释仅限本版本所见及字段原义。

| 原始字段 | 原始表示和含义 |
| --- | --- |
| `pdb` | 4 字符 PDB ID；可多行重复，是结构连接键。 |
| `Hchain` | 抗体重链 author chain 标识，文本；26 行为 `NA`。 |
| `Lchain` | 抗体轻链 author chain 标识，文本；168 行为 `NA`。 |
| `model` | PDB 模型编号，整数文本；非 ANTIPASTI 预测值。 |
| `antigen_chain` | 抗原链标识，文本；可为空/`NA` 或含多链表示。 |
| `antigen_type` | 抗原类别，含 `protein`、`peptide`、`Hapten`、`carbohydrate`、`nucleic-acid` 及 ` \| ` 连接的组合；22 行为 `NA`。 |
| `antigen_het_name` | 非标准抗原/异源组分名称，文本；多数为 `NA`。 |
| `antigen_name` | 抗原名称，文本；22 行为 `NA`。 |
| `short_header` | 结构简短标题，文本；3 行为 `NA`。 |
| `date` | 结构记录日期，原样文本，例如 `12/29/17`；不强制改写时区或年月日。 |
| `compound` | 结构复合物描述，文本。 |
| `organism` | 结构来源生物，文本；3 行为 `NA`。 |
| `heavy_species` | 重链来源物种，文本；57 行为 `NA`。 |
| `light_species` | 轻链来源物种，文本；246 行为 `NA`。 |
| `antigen_species` | 抗原来源物种，文本；100 行为 `NA`。 |
| `authors` | 结构条目作者文本。 |
| `resolution` | 结构分辨率数值文本，通常以埃为单位；本版本均非缺失。 |
| `method` | 结构测定方法；本版本 1,266 行均为 `X-RAY DIFFRACTION`。 |
| `r_free` | 晶体结构精修自由 R 因子，无量纲数值文本。 |
| `r_factor` | 晶体结构精修 R 因子，无量纲数值文本。 |
| `scfv` | 是否为单链可变片段，原始 `True` 61 行、`False` 1,205 行。 |
| `engineered` | 是否标注为工程化，原始 `True` 1,020 行、`False` 246 行。 |
| `heavy_subclass` | 重链亚类注释，文本；24 行为 `NA`。 |
| `light_subclass` | 轻链亚类注释，文本；168 行为 `NA`。 |
| `light_ctype` | 轻链常数区类型注释，文本；168 行为 `NA`。 |
| `affinity` | 实验解离常数 `KD`，以 M 表示的浮点文本；本版本全部 1,266 行有值，越小结合越强。 |
| `delta_g` | 作者汇总表中的自由能浮点文本；37 行为 `NA`，生成温度/单位细节不在当前文件内。 |
| `affinity_method` | 亲和力测定方法或上游原样来源标识，如 `SPR`、`BLI`、`ITC`、`ELISA`、`Unknown`、`Other`、`TBD`；少数值是数字文本，不能一概解释成实验方法。 |
| `temperature` | 测定温度原始文本；976 行为 `NA`，单位或统一口径未在 TSV 中声明。 |
| `pmid` | PMID 或 `TBD` 等原样文献标识文本；58 行为 `NA`。 |

### 数据示例

TSV 首行的 `pdb=6fe4`、`Hchain=F`、`Lchain=NA`、`antigen_chain=A`、`antigen_type=protein`、`affinity=9.6e-09`、`delta_g=-10.938139080820335`、`affinity_method=SPR`。这是与 `6fe4.pdb` 关联的一条注释记录，不是整个 PDB 文件或独立预测结果。

## PDB 数据库

连接键是 TSV `pdb` 与 Mendeley 文件名，故对全部 715 个唯一 ID 从 RCSB 补充完整 entry 序列和 mmCIF。没有把作者 Chothia 编号 PDB 覆盖为 RCSB 坐标，也没有依据 H/L 链列重写 RCSB 链角色。RCSB 原始 entry FASTA 为 `pdb/sequences/rcsb_pdb_<id>.fasta`，原始完整 mmCIF 为 `pdb/structures/<id>.cif`；记录到结构的映射为 PDB ID 级，1,266 行并非 1,266 个独立结构。

715/715 个 ID 均有完整 mmCIF 和可解析 FASTA。`3l5y`、`3rvv`、`3rvw` 已被 RCSB 标为 obsolete，FASTA endpoint 返回 404；其 canonical entity 序列从各自的 RCSB 归档 mmCIF 项目生成，FASTA header 明示来源，替代条目分别为 `4PS4`、`5VPL`、`5VPG`。其余 712 份 FASTA 为 RCSB endpoint 原始字节。共 1,430 文件、757.4 MiB（794220350 bytes）；按相对路径排序拼接 `relative_path<TAB>bytes<TAB>sha256<LF>` 的 SHA-256 为 `87287a9ac4bfcb42d24e5e52e41aa6d57bf066d432949180246609d13597f737`。获取于 2026-10-29，入口为 `https://www.rcsb.org/fasta/entry/<id>/download` 和 `https://files.rcsb.org/download/<id>.cif`。

## 采集过程记录

- 2026-10-29：从 Mendeley v1 API 枚举 715 个文件及官方 SHA-256，在 `G:\abag-datasets\SRC_R80_ANTIPASTI\.staging` 下载；逐项字节数和官方 SHA-256 全部通过，合计 450435318 bytes。
- 2026-10-29：按固定 Git commit 的 blob ID 获取 TSV 和三个 NumPy 数组；解析 1,266 行、715 个唯一 ID，逐一解析 715 个作者 PDB 文件。首次验收脚本对 Biopython atom 对象做布尔判断，误报 `6ddm.pdb`；修正为显式 `is None` 后全量复跑通过。
- 2026-10-29：归档 arXiv v1 PDF；从 RCSB 批量获取 715 个 mmCIF 和 712 个 entry FASTA。另 3 个 obsolete ID 的 FASTA endpoint 返回 404，按归档 mmCIF 的 canonical entity 序列生成剩余 3 份 FASTA，保留旧 ID 与替代条目关系。
- 2026-10-29：完成 PDB inventory、表格与论文核验；以同盘重命名发布本地 `v1`，未将该目录视为论文全部训练数据的完整获取。

## 参考文献

- [Michalewicz 等，ANTIPASTI，arXiv v1](https://arxiv.org/abs/2410.01523v1)。
- [Mendeley Data v1，DOI 10.17632/j4rt98xpy7.1](https://doi.org/10.17632/j4rt98xpy7.1)。
- [ANTIPASTI 固定 Git commit](https://github.com/kevinmicha/ANTIPASTI/tree/a8dc208ee4e33cdba707cbe0c9580f92a9668611)。
- [SAbDab](https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabdab)、[RCSB PDB](https://www.rcsb.org/)。

## 其他

### 数据范围和限制

Mendeley 结构、Git 汇总表和筛选数组不是单一独立样本表。论文训练集 634、筛选数组 701 和公开结构 715 的集合关系不能仅凭数量推定。公开包适合做来源级统计和结构检查，具体模型训练划分须另凭上游代码和方法确认。

### 完整性与验收

Mendeley 官方清单的 715/715 个文件均通过官方 SHA-256，且可解析；Git 4/4 个文件符合固定 commit blob。TSV 的唯一 PDB ID 与作者文件名集合完全一致；RCSB 715/715 个 ID 有结构及序列，含 3 份明确标注为从归档 mmCIF 生成的 FASTA。论文 PDF 为 35 页，可读取。此为公开包接入验收，不等于论文完整研究数据取得。

### 许可和再分发边界

Git 仓库 [`LICENSE`](https://github.com/kevinmicha/ANTIPASTI/blob/a8dc208ee4e33cdba707cbe0c9580f92a9668611/LICENSE) 为 MIT，覆盖软件及相关文档，不能自动扩展到 Mendeley PDB 或 TSV 的数据许可。Mendeley v1 API `license` 字段为空；上游未特别说明覆盖该数据的许可，使用与再分发范围不明确。arXiv 文本与 RCSB 原始文件各有独立条款。公开入口直接提供必要 payload，未见与本地接入明确冲突的条款，因此该权利疑问不阻塞本地 source package 发布；商用、衍生和对外再分发仍待明确。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 论文训练集 634 个结构 | Mendeley 715 PDB，Git 筛选数组 701 ID | 不能从当前数量重建 634 项训练清单 |
| 公布的抗体-抗原 PDB 与亲和力值 | 715 PDB 与 1,266 行 TSV，全部 ID 相连 | 本批已验收，记录可重复 |
| 完整的原始 PDB 参考序列/坐标 | RCSB 715 mmCIF、712 原始 FASTA 和 3 份归档 mmCIF 派生 FASTA | ID 级补齐；3 个 obsolete 例外已注明 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-29；不阻塞本地接入）：Mendeley PDB 与 Git TSV/数组的独立数据许可不明。已核查 Mendeley v1 API 空 `license` 与仓库 MIT 文本；目前只按公开包保存，不主张商用、衍生或对外再分发权。取得覆盖这些数据对象的明确条款后关闭。
- `Q02`（最近更新：2026-10-29；影响训练复现）：论文 634 个训练结构、701 个 `selected_entries` 与 715 个公开 PDB 的逐项关系尚未由归档文件单独证明。当前分别报告三个计数，不指定训练划分；核对上游固定 commit 的筛选代码与论文方法后关闭。
- `Q03`（最近更新：2026-10-29；影响部分字段解释）：`delta_g` 的实际计算温度/单位、`temperature` 单位及 `affinity_method` 中数字文本的含义未由当前 TSV 单独定义。当前保留原值，不作单位换算或方法合并；取得来源方数据字典或生成代码证据后关闭。
