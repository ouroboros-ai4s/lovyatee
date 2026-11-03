# SRC_R78_MOCHIBIND 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [采样表与配对文件](#采样表与配对文件)
  - [基线打分文件](#基线打分文件)
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

- `source_id`：`SRC_R78_MOCHIBIND`
- `source_version`：`snapshot-2026-05-19`
- 原作者或发布机构：Amazon Web Services 与 Brandeis University（Yunrui Li、Yue Zhao、Kemal Sonmez、Luca Giancardo、Lan Guo、Pengyu Hong、Nina Cheng、Melih Yilmaz）

### 来源方背景

本仓库由 Amazon Science 组织发布，作者名单中七人标注 Amazon Web Services、一人标注 Brandeis University 计算机系，通讯作者 Melih Yilmaz 为 AWS 方负责人。论文的 experiment 部分明确 MochiBind 是纯序列模型，与该仓库的定位一致：仓库同时提供模型实现、预训练权重、采样后的训练数据，以及 Graphinity、GeoDock、Boltz-2 三个基线的评测材料。

仓库声明为学术复现用途发布，不接受 pull request，以保持代码与论文一致；代码许可证为 CC BY-NC 4.0。数据部分标注来自 AlphaBind（A-Alpha Bio），其上游为 MIT License，这一点在许可章节分层说明。

## 实验设计和数据口径

本仓库的数据不是新测实验，而是从 AlphaBind 公开实验中采样得到的训练与验证集，配套论文的评测框架使用。

### 来源数据与四个抗原体系

`data/` 下的七个 CSV 覆盖四个抗原体系：PEM（人 PD-1）、PP489（TIGIT）、TRA（HER2）、VHH72（SARS-CoV-2 RBD）。其中 PEM、PP489、TRA 三个体系的验证集文件名带 `_val_`，训练集文件名带 `_clean`；VHH72 同样成对。文件名前缀 `df_` 与后缀 `_sampled_5k` 表明这些是从更大池中采样出的约 5,000 行子集，不是 AlphaBind 的全量数据。

每个 CSV 的一行是一个 scFv 候选对该体系的结合测量。`mata_description` 是候选标识，`matalpha_description` 是抗原体系标签，`alphaseq_affinity` 是 AlphaSeq 测量得到的表观亲和力分数，`mata_sequence` 是含 `GGGGSGGGGSGGGGS` 连接子的完整 scFv 序列，`hc`/`lc` 是从中拆出的重链与轻链，`antigen` 是抗原序列。

### 四个体系的序列结构差异

四个体系并非同一构造。PEM 与 TRA 的训练表中 `lc` 只有 1 个不同取值，说明轻链在所有候选间恒定，变异集中在重链；VHH72 的训练表没有 `lc` 列，只有 `hc` 与 `antigen`，且 `antigen` 有 4,580 个不同取值，与行数相同，说明每条记录携带不同的抗原序列（RBD 变体）。

这一差异有直接后果：把四个体系拼接成一个训练集时，VHH72 的行是“抗体 × 抗原变体”配对，其余三个是“抗体变体 × 固定抗原”。两者的样本含义不同，且 VHH72 的 `antigen` 唯一值数等于行数，若按行随机划分，同一抗原的不同版本会分散到两侧。

### 训练表与验证表的差别

训练表（`_clean`）列数为 11—16，验证表统一 15 列，多出 `predicted_affinity`、`avg_off_target_affinity`、`model`、`id` 四列。`model` 取值包括 `alphabind`、`esm_warm`、`esm_cold`、`ohe_warm`、`ohe_cold`，说明验证集的候选来自五种不同的生成或筛选来源；训练表没有 `model` 列，其候选来源未在表内标注。

`predicted_affinity` 是模型预测值而非实验值，取值范围 −0.277—1.707，与 `alphaseq_affinity` 的 1.1—7.2 不在同一尺度，不能当作实验标签使用。`avg_off_target_affinity` 是与靶外抗原的平均结合分数，用于评估特异性，同样不是本靶点的测量。

### 配对文件与基线打分

`sampled_pairs_200k_mata.pkl` 与 `sampled_pairs_200k_th0_mata.pkl` 是配对训练数据：每个抗原体系 200,000 个 `(候选A, 候选B, 差值, 亲和力A, 亲和力B)` 五元组，用于 pairwise ranking。两个文件的区别在筛选阈值，`th0` 版本接受亲和力差为 0 的对，`mata` 版本要求相对差超过阈值。这两个文件由仓库内的 `sample_alphabind_pairs.py` 生成，脚本定义了两条筛选条件：两条序列长度必须相同，且相对亲和力差与较大值之比需超过阈值。

`evaluation_src/baseline_data/` 下三个 pickle 是 Boltz-2 与 GeoDock 的打分结果，键为七个 CSV 的文件名主干，值为 `[候选标识, 分数, 亲和力]` 三元组。Boltz-2 提供 `iplddt` 与 `iptm` 两个指标，GeoDock 提供 `iplddt`。三个文件的分条数与对应 CSV 的行数基本一致但不完全相等：GeoDock 的 PEM 训练文件是 4,989 对 4,990，TRA 是 4,252 对 4,254，说明部分候选未取得结构打分。

```text
snapshot-2026-05-19/
└── ab-binding-eval/
    ├── checkpoint/            4 个抗原体系的 MochiBind 权重（.pt）
    ├── data/                  7 个 CSV + 2 个配对 pickle + 采样脚本
    ├── evaluation_src/        基线评测 notebook、Graphinity 微调代码
    │   └── baseline_data/     Boltz-2 与 GeoDock 的打分 pickle
    ├── model_src/             MochiBind 实现
    ├── generate_esm2_embedding.py
    └── requirements*.txt
```

## 论文原文

- 标题：*A systematic evaluation framework for universal antibody-antigen binding affinity prediction and candidate recommendation*
- 作者：Yunrui Li, Yue Zhao, Kemal Sonmez, Luca Giancardo, Lan Guo, Pengyu Hong, Nina Cheng, Melih Yilmaz
- 发表来源：iScience 29, 116522 (2026)
- 归档文本版本：正式发表版（Europe PMC 开放全文）
- 发布日期：2026-08-21
- DOI：`10.1016/j.isci.2026.116522`
- PMID / PMCID：`42564542` / `PMC13444443`
- 本地文件：`articles/MochiBind_2026-08-21_iScience-VoR.pdf`
- 文件大小：4.47 MiB（4,690,367 bytes）
- SHA-256：`cce242f0035d7a7ce04d06041dec300e595271470e1497d8752d8a4fe3f8cf7b`
- 文本许可：CC BY-NC-ND（Europe PMC 记录）
- 补充材料：`articles/MochiBind_2026-08-21_iScience-supplement.pdf`，301.45 KiB（308,685 bytes），SHA-256 `70381bca215d7768dad81d3656197b1a50367b84c0b715b4ccd5afd8f908ff10`；来自 Europe PMC `supplementaryFiles` 包内的 `mmc1.pdf`，3 页

论文的 Resource Availability 一节写明：数据为既有公开数据，入口为 `github.com/A-Alpha-Bio/alphabind`；代码存放于 `github.com/amazon-science/ab-binding-eval`，发表之日起公开。论文没有把 `ab-binding-eval` 描述为新的实验数据来源，这与本仓库的实际内容一致：仓库内是采样数据、权重与评测代码。

归档文件由 Europe PMC 渲染端点取得，发布方未给出有意义的原始文件名；本次按项目约定改名为 `MochiBind_2026-08-21_iScience-VoR.pdf`，日期取论文发表日，未改变字节。`AlphaBind` 上游论文（mAbs 17(1):2534626，DOI `10.1080/19420862.2025.2534626`）解释的是数据来源，不是本仓库的方法论，列在“参考文献”而不作为本来源的论文条目。

## 仓库内容

上游是 GitHub 仓库 `amazon-science/ab-binding-eval`，本次固定到 commit `0c693d815f7f0bf0a3dd5494205dca10fbc20c04`（提交日期 2026-05-19，提交信息 `use csv for embeddings, save only mean`）。`source_version` 的日期取自该 commit 的提交日期，不是下载日期；`snapshot-2026-05-19` 表示“在该日期的固定 tree 状态”，commit SHA 是文件身份的权威。

仓库使用 Git LFS 管理大文件：`.gitattributes` 对 `*.pkl`、`*.pt`、`*.bin` 与 `data/*.csv` 全部启用 LFS 过滤。16 个 LFS 对象在 `git lfs pull` 后逐一核对其 SHA-256 与 pointer 中声明的 `oid` 一致。

```text
snapshot-2026-05-19/
└── ab-binding-eval/
    ├── .gitattributes
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    ├── generate_esm2_embedding.py
    ├── requirements.txt / requirements-gpu.txt / requirements-graphinity.txt
    ├── checkpoint/
    │   ├── pem.pt
    │   ├── pp489.pt
    │   ├── tra.pt
    │   └── vhh72.pt
    ├── data/
    │   ├── df_pem_sampled_5k_clean.csv
    │   ├── df_pem_val_sampled_5k.csv
    │   ├── df_pp489_sampled_5k_clean.csv
    │   ├── df_pp489_val_sampled_5k.csv
    │   ├── df_tra_sampled_5k_clean.csv
    │   ├── df_vhh72_sampled_5k_clean.csv
    │   ├── df_vhh72_val_sampled_5k.csv
    │   ├── sample_alphabind_pairs.py
    │   ├── sampled_pairs_200k_mata.pkl
    │   └── sampled_pairs_200k_th0_mata.pkl
    ├── evaluation_src/
    │   ├── baseline_data/      boltz2_iplddt.pkl、boltz2_iptm.pkl、geodock_iplddt.pkl
    │   ├── graphinity_ft/      Graphinity 微调代码
    │   ├── boltz_retrieval.ipynb / geodock_retrieval.ipynb
    │   ├── mochibind_trainval.ipynb / pairwise_accuracy.ipynb
    │   └── .DS_Store
    └── model_src/
        ├── main_mean.py / model.py / dataset_mean.py / train_eval.py
```

工作树共 40 个文件（不含 `.git`），payload 合计 208.91 MiB（219,062,050 bytes）。四个 `.pt` 权重各 22,194,177 bytes，两个配对 pickle 各约 50 MB，构成体量的绝大部分。仓库 README 中的目录树写作 `cell_submission_code/`，与实际仓库根目录名不同；该差异保留在 README 中，不通过重命名掩盖，实际根目录为仓库名 `ab-binding-eval`。

## 数据结构

### 采样表与配对文件

七个 CSV 分属四个抗原体系，训练与验证各一。各表的行数、列数与几个关键基数如下：

| 文件 | 行数 | 列数 | 候选唯一值 | `lc` 唯一值 |
| --- | ---: | ---: | ---: | ---: |
| `df_pem_sampled_5k_clean.csv` | 4,990 | 12 | 4,990 | 1 |
| `df_pem_val_sampled_5k.csv` | 5,000 | 15 | 5,000 | 未单列统计 |
| `df_pp489_sampled_5k_clean.csv` | 4,630 | 12 | 4,630 | 1 |
| `df_pp489_val_sampled_5k.csv` | 5,000 | 15 | 5,000 | 未单列统计 |
| `df_tra_sampled_5k_clean.csv` | 4,254 | 16 | 4,254 | 1 |
| `df_vhh72_sampled_5k_clean.csv` | 4,580 | 11 | 4,580 | 无该列 |
| `df_vhh72_val_sampled_5k.csv` | 5,000 | 14 | 5,000 | 无该列 |

采样表合计 33,454 行。每行是一个独立候选，无重复候选标识；但同一候选的 `mata_sequence`、`hc`、`lc` 三个字段互为子串关系，不是三次测量。

两个配对 pickle 各含 4 个键（`pem`、`pp489`、`tra`、`vhh72`），每键 200,000 个五元组。五元组依次为候选 A 标识、候选 B 标识、A 与 B 的亲和力差、A 的亲和力、B 的亲和力。这两个文件不是新增数据，而是七个 CSV 中候选的两两组合，组合数远大于候选数，因此行数不能与任何候选计数比较。

### 基线打分文件

三个 pickle 的结构是 `{文件名主干: [[候选标识, 分数, 亲和力], ...]}`。候选标识与 CSV 的 `mata_description` 对应，第三项是 `alphaseq_affinity`。Boltz-2 的两个文件提供 `ipLDDT` 与 `ipTM`，GeoDock 提供一个 `ipLDDT`；GeoDock 的 `ipLDDT` 数值量级（如 93.7）与 Boltz-2 的（如 0.74）不同，两者不可直接比较。

### 字段说明

**训练表（`*_sampled_5k_clean.csv`）**

| 原始字段 | 表示、单位与来源 | 缺失与特殊编码 |
| --- | --- | --- |
| （空表头） | CSV 序列化索引，取值 0 起 | 无缺失；不是数据字段 |
| `Unnamed: 0` | 上游 DataFrame 的索引副本 | 无缺失；与上一列同值 |
| `mata_description` | 候选标识，如 `pair_194204`、`alphabind_1659_d4` | 无缺失 |
| `matalpha_description` | 抗原体系与表达构建标签，如 `huPD-1_RE(rebuilt)` | 无缺失 |
| `alphaseq_affinity` | AlphaSeq 测量的表观亲和力分数，1.1—7.2（PEM） | 无缺失；单位未在公开材料标注 |
| `mata_sequence` | 完整 scFv 序列，含 `GGGGSGGGGSGGGGS` 连接子 | 无缺失 |
| `edit_distance` | 相对亲本的编辑距离，整数 | 无缺失 |
| `parental_mean_aff` | 同一亲本候选组的平均亲和力 | 无缺失 |
| `parental_aff_margin` | 本候选亲和力减去亲本均值 | 无缺失；负值表示低于均值 |
| `hc` | 重链可变区序列 | 无缺失 |
| `lc` | 轻链可变区序列 | PEM/PP489/TRA 有，VHH72 无此列 |
| `antigen` | 抗原氨基酸序列 | 无缺失；VHH72 中每行不同 |

**验证表（`*_val_sampled_5k.csv`）**

| 原始字段 | 表示、单位与来源 | 缺失与特殊编码 |
| --- | --- | --- |
| （空表头）、`mata_description`、`matalpha_description`、`alphaseq_affinity`、`mata_sequence`、`edit_distance`、`parental_mean_aff`、`parental_aff_margin` | 与训练表同义 | 无缺失 |
| `predicted_affinity` | 模型预测的亲和力，−0.277—1.707 | 无缺失；与 `alphaseq_affinity` 不同尺度，不是实验值 |
| `avg_off_target_affinity` | 对靶外抗原的平均结合分数 | 无缺失；不是本靶点测量 |
| `model` | 候选生成来源 | 无缺失，取值见下方枚举表 |
| `id` | 候选在来源中的数值编号 | 无缺失 |
| `hc`、`lc`、`antigen` | 与训练表同义 | VHH72 验证表无 `lc` |

**`model`（验证表；取值范围依据：当前版本观察）**

| 原始取值 | 含义 |
| --- | --- |
| `alphabind` | AlphaBind 模型生成 |
| `esm_warm` | ESM 模型、warm-start 条件 |
| `esm_cold` | ESM 模型、cold-start 条件 |
| `ohe_warm` | one-hot 编码、warm-start 条件 |
| `ohe_cold` | one-hot 编码、cold-start 条件 |
| （空） | 未标注来源；PEM 验证集有 10 行 |

`warm`/`cold` 的具体定义未在公开材料中说明，`ohe` 推测为 one-hot encoding 的缩写，本 README 不对其展开解释。`model` 只出现在验证表，训练表没有对应列。

**`matalpha_description`（训练与验证表）**

| 原始取值 | 体系 | 含义 |
| --- | --- | --- |
| `huPD-1_RE(rebuilt)` | PEM | 人 PD-1 胞外域，重建的展示构建 |
| `TIGIT_22-137_POI-AGA2` | PP489 | TIGIT 22—137 片段，POI 接 AGA2 |
| `HER2-OPT_AGA2-POI` | TRA | HER2，优化构建，AGA2 接 POI |
| `SARS-CoV2_RBD_(6LZG)` | VHH72 | SARS-CoV-2 RBD，取自 PDB 6LZG |

四个取值各占一个体系，`6LZG` 是唯一在标签中直接给出 PDB ID 的体系。

### 数据示例

`df_pem_sampled_5k_clean.csv` 的一条记录：

```text
mata_description=pair_194204,matalpha_description=huPD-1_RE(rebuilt)
alphaseq_affinity=1.6771154597235238,edit_distance=2
parental_mean_aff=2.41336351499785,parental_aff_margin=-0.736
mata_sequence=QVQLVQSGVEVKK...GGGGSGGGGSGGGGS EIVLTQSPATLSLS...
hc=QVQLVQSGVEVKK...（120 aa）
lc=EIVLTQSPATLSLS...（111 aa）
```

该候选的 `mata_sequence` 长度 246 aa，恰为 `hc`（120）+ 连接子（15）+ `lc`（111），说明 scFv 构造是重链在前、轻链在后，以 `GGGGSGGGGSGGGGS` 连接。

`sampled_pairs_200k_mata.pkl` 的一个五元组：

```text
('esm_warm_1515_d4', 'esm_warm_197_d2', 1.1648, 1.8674, 3.0323)
```

它表示两个候选的配对：B 的亲和力 3.032 高于 A 的 1.867，差值 1.165。这是同一个抗原体系内两候选的比较，不是两次独立测量。

## PDB 数据库

本仓库的数据表只有一处直接引用结构：VHH72 体系的 `matalpha_description` 为 `SARS-CoV2_RBD_(6LZG)`。该标注指 SARS-CoV-2 RBD 与 ACE2 的复合物晶体结构 [6LZG](https://www.rcsb.org/structure/6LZG)，说明 VHH72 的抗原序列取自该条目。

其余三个体系（PEM、PP489、TRA）的表内没有任何 PDB ID，也没有结构列。它们的抗原与抗体序列以纯序列形式给出，不指向具体结构。论文对这些体系使用 Boltz-2 预测结构与 GeoDock 对接，属于计算产物，不是实验测定结构。

映射强度因此分两级：VHH72 是“体系级引用”，标签直接给出 PDB ID，但 4,580 条记录共享同一个参考结构，没有任何一条候选有此结构中的坐标；PEM、PP489、TRA 是“无锚点”，本次检索未在数据、README、代码与论文中找到可辩护的 PDB ID。

项目从 RCSB 取得 6LZG 的 entry 级 FASTA 与完整 mmCIF：

| 文件 | 大小 | SHA-256 |
| --- | ---: | --- |
| `pdb/sequences/rcsb_pdb_6LZG.fasta` | 966 bytes | `565df7341ada544d15c31ef805158bf6ce5d962010680d334ac12936e9fe41a3` |
| `pdb/structures/6LZG.cif` | 1.38 MiB（1,443,557 bytes） | `cdfa118da530978568ce4be216f4dd3b95d959b6841d06aa73762bb36980cffc` |

FASTA 有 2 条 entity：`6LZG_1`（ACE2，chain A）与 `6LZG_2`（Spike protein S1，chain B）。本数据只用到其中的 RBD（S1）序列；ACE2 出现在该结构中是因为条目本身是 RBD–ACE2 复合物，不是本数据的抗原。这一区别必须明确：6LZG 是本数据抗原序列的来源条目，不是本数据所测抗体的复合物。

`pdb/` 合计 2 个文件、1,444,523 bytes（1.38 MiB），inventory SHA-256 为 `6b4a66a964d17cb8339dc7b2f9247f33ded45970f7822c495c525c80c44cb2bd`。未发布独立 PDB manifest。

PEM、PP489、TRA 三个体系没有可辩护的逐条或体系级 PDB 锚点，按项目规则标为 partial 而非补齐：这部分的 PDB 子任务未完成，缺口已记录在“待解决问题与处理进展”`Q03`。

## 采集过程记录

- 2026-10-28 用户指定存储根 `G:\abag-datasets`。项目无 `project.toml`、`developer.local.toml` 与 `workspace/`，因此 README 直接写入 source version 目录，未按 skill 的 `workspace/users/<user>/docs/readme/` 生成草稿；该偏差已获用户同意。
- 2026-10-28 从 GitHub API 取得 `main` 分支 HEAD commit `0c693d815f7f0bf0a3dd5494205dca10fbc20c04`（2026-05-19），确认仓库使用 Git LFS（`.gitattributes` 对 `*.pkl`、`*.pt`、`*.bin`、`data/*.csv` 启用过滤）。
- 2026-10-28 `git clone` 后 checkout 到该 commit，执行 `git lfs pull` 拉取 16 个 LFS 对象。逐一比对本地 SHA-256 与 pointer 中声明的 `oid`，全部一致。
- 2026-10-28 曾尝试删除仓库内的 `evaluation_src/.DS_Store`，以保持 payload 只含源文件。随后意识到这属于修改上游 tree，用 `git checkout --` 恢复，保留该文件原样。
- 2026-10-29 独立验收：解析 7 个 CSV 确认列数、行数、候选唯一值数与 `lc` 基数；解析两个配对 pickle 确认 4 个键各 200,000 条五元组；解析三个基线 pickle 确认键集合、条数与三元组结构；核对 `mata_sequence` 长度等于 `hc` + 连接子 + `lc`。
- 2026-10-29 从 Europe PMC 取得论文正式发表版 PDF（4,690,367 bytes，14 页），核对首页题名、DOI、卷期与作者列表。同日重新以完整超时取得 `supplementaryFiles` ZIP（2,105,830 bytes，13 个成员），从包内取出 `mmc1.pdf`（308,685 bytes，3 页）作为补充材料归入 `articles/`，其余 12 个成员是图件渲染（GIF/JPG），未单独保留。
- 2026-10-29 按 PDB 硬性要求审计锚点：仅 VHH72 的标签直接给出 6LZG，据此取得 entry FASTA 与 mmCIF；PEM、PP489、TRA 检索数据、README、代码与论文后未找到可辩护锚点，标为 partial 并记录检索范围。
- 2026-10-29 发现仓库 README 的目录树写作 `cell_submission_code/`，与实际根目录 `ab-binding-eval/` 不一致；未重命名文件，差异记入本文“仓库内容”。

## 参考文献

- 代码仓库：<https://github.com/amazon-science/ab-binding-eval>，commit `0c693d815f7f0bf0a3dd5494205dca10fbc20c04`
- 平台论文：Li et al., *A systematic evaluation framework for universal antibody-antigen binding affinity prediction and candidate recommendation*, iScience 29, 116522 (2026)，DOI `10.1016/j.isci.2026.116522`
- Europe PMC：<https://europepmc.org/article/PMC/PMC13444443>
- 上游数据：Agarwal et al., *AlphaBind, a domain-specific model to predict and optimize antibody–antigen binding affinity*, mAbs 17(1):2534626 (2025)，DOI `10.1080/19420862.2025.2534626`
- 上游数据仓库：<https://github.com/A-Alpha-Bio/alphabind>，MIT License
- 参考结构：RCSB PDB [6LZG](https://www.rcsb.org/structure/6LZG)，SARS-CoV-2 RBD 与 ACE2 复合物
- 基线方法：Boltz-2、GeoDock、Graphinity，各自的原始论文见 `evaluation_src/` 内 notebook 与论文引用表

## 其他

### 数据范围和限制

本仓库提供的是采样后的子集，不是 AlphaBind 全量数据。七个 CSV 合计 33,454 行，而 AlphaBind 公开描述为约 750 万条实验记录；采样比例未在仓库中说明，因此不能用本仓库的行数估计上游规模。

四个抗原体系的结构不同：PEM、PP489、TRA 是固定抗原下的重链变体，VHH72 是抗体固定、抗原变化。把四者拼接训练时，样本含义不一致，且 VHH72 的抗原几乎逐行不同，按行随机划分会把同一抗原的不同版本分到两侧。

验证表包含 `predicted_affinity` 与 `avg_off_target_affinity` 两个模型派生字段。前者是预测值、后者是靶外信号，都不是实验标签；若用 `predicted_affinity` 作为回归目标，等于用模型输出训练模型。

配对 pickle 的行数是候选组合数（每个体系 200,000），不是候选数。以它计算“样本量”会高估一个数量级以上。

### 完整性与验收

| 文件 | 大小 | SHA-256 |
| --- | ---: | --- |
| `checkpoint/pem.pt` | 21.17 MiB（22,194,177 bytes） | `beacb0f8b30cc970c402617f7a5e00281eb0647710f77a01c5ac59c0ef83809a` |
| `checkpoint/pp489.pt` | 21.17 MiB（22,194,177 bytes） | `5ef13bda1e4ef22e48f1eb393d81dd9697456e4140a2f028d1e29d9db5a01580` |
| `checkpoint/tra.pt` | 21.17 MiB（22,194,177 bytes） | `1ba50c780727b93b6301b9d15faefd206780223338a56ea649fb511c7b6a5ae0` |
| `checkpoint/vhh72.pt` | 21.17 MiB（22,194,177 bytes） | `5c775e86d9664173a526fc351717c688901a079379f015fa93e2dd041909ea96` |
| `data/df_pem_sampled_5k_clean.csv` | 3.33 MiB（3,491,899 bytes） | `ec4c37584a0f0719be433562acfe24442c8f53a859483ec8e934066942dd633a` |
| `data/df_pem_val_sampled_5k.csv` | 3.58 MiB（3,758,492 bytes） | `f7b222080fca62f1b34923b7aa5b2874ded0af4d04f6b41e89f9c70afa71248a` |
| `data/df_pp489_sampled_5k_clean.csv` | 3.11 MiB（3,261,297 bytes） | `8cb7743d5b33e4bc72f0eb11439b5aef0e703d8fb2e9cf6ebf3e48b4596cef45` |
| `data/df_pp489_val_sampled_5k.csv` | 3.58 MiB（3,752,235 bytes） | `050dad7725396feee43ada9720227241017f29025ed141a079c0a9c846a2a97e` |
| `data/df_tra_sampled_5k_clean.csv` | 3.03 MiB（3,173,111 bytes） | `2862491103702539aeb00e3de33556973aeee831916ed39cb3491d3dd27af53a` |
| `data/df_vhh72_sampled_5k_clean.csv` | 2.47 MiB（2,590,359 bytes） | `0edd26634c4aaf133ecda12d1023c033550435ecfeb66c38b7d29785b357cb2c` |
| `data/df_vhh72_val_sampled_5k.csv` | 2.91 MiB（3,051,920 bytes） | `158d5c21c55b819c76729551407dda39112e38cf9db19b67a812d78483170526` |
| `data/sampled_pairs_200k_mata.pkl` | 48.48 MiB（50,834,146 bytes） | `a72c0c128b70b7e6c1b9392daf2bbd894415685fde422a4f894486856b3d4d2c` |
| `data/sampled_pairs_200k_th0_mata.pkl` | 48.48 MiB（50,832,915 bytes） | `45de9be5b5b23b6796cae4c28873daee0c9fe9021107a09438305effecddd6e0` |
| `evaluation_src/baseline_data/boltz2_iplddt.pkl` | 1.60 MiB（1,675,902 bytes） | `a5f74909649274659785c061c2a6e17e0ef1e903a3ce271acc4e185b8322f996` |
| `evaluation_src/baseline_data/boltz2_iptm.pkl` | 1.60 MiB（1,675,902 bytes） | `90b5df65866c2f6c7a4a6379f3060e6af34c24a046cda8b001a9e70e35ecfe80` |
| `evaluation_src/baseline_data/geodock_iplddt.pkl` | 1.92 MiB（2,010,065 bytes） | `43abe207f5b3effec44141a1c28ca801b64bd4881953ecb2cef2d8913cfc3f92` |

16 个 LFS 对象的 SHA-256 与 `.gitattributes` 所管理的 pointer 中声明的 `oid` 逐一一致；`git lfs ls-files` 显示全部为已解析状态（非指针）。工作树其余 24 个文件为普通 Git 对象，由 commit `0c693d8` 的 tree 固定，未逐一列出哈希。

`pdb/` 的完整性见“PDB 数据库”；PEM、PP489、TRA 三个体系的 PDB 子任务为 partial，缺口见 `Q03`。

### 许可和再分发边界

本仓库分为三层，许可各不相同：

- 代码：`LICENSE` 为 CC BY-NC 4.0，覆盖 `model_src/`、`evaluation_src/`、`generate_esm2_embedding.py`、`requirements*.txt` 等实现文件。仓库 README 声明为学术复现用途发布，不接受 pull request。
- 仓库内数据：`data/` 下的 CSV 与 pickle 来自 AlphaBind。仓库 README 指明 AlphaBind 数据结构以 MIT License 提供，并链接到 `A-Alpha-Bio/alphabind` 的特定 commit `15d2582` 下的 LICENSE 文件。MIT 与 CC BY-NC 4.0 在商用手续上不同，数据部分应按 MIT 处理。
- 论文文本：iScience 正式版为 CC BY-NC-ND，与代码和数据都不是同一层。

`checkpoint/` 下的四个 `.pt` 是论文训练产出的模型权重，随仓库以 CC BY-NC 4.0 发布；权重不是数据，不能按 MIT 解释。

`pdb/` 内的 RCSB 文件适用 RCSB 自身条款，使用时应保留 6LZG 的原始结构引用。

仓库 README 的 `LICENSE` 徽章写作 CC BY-NC 4.0，与 `LICENSE` 文件一致；数据层的 MIT 说明写在正文而非单独文件，因此本 README 按对象分层记录，不把单一许可扩展到全部内容。

### 公开范围对照

| 论文或仓库声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 四个抗原体系（PEM、PP489、TRA、VHH72） | 7 个 CSV 覆盖四个体系，训练与验证各一 | 已包含 |
| 每体系约 30,000 个实验表征变体 | 本仓库每体系 4,254—5,000 行，为采样子集 | 部分包含（采样后） |
| 采样 AlphaBind 数据用于训练与验证 | `data/` 下 CSV 与配对 pickle | 已包含 |
| 预训练 MochiBind 权重（四体系） | `checkpoint/` 4 个 `.pt`，各 22,194,177 bytes | 已包含 |
| 配对训练数据 | 2 个 pickle，每体系 200,000 五元组 | 已包含 |
| Boltz-2 与 GeoDock 基线打分 | 3 个 pickle，7 个键 | 已包含；GeoDock 部分键少于 CSV 行数 |
| 采样脚本 | `data/sample_alphabind_pairs.py` | 已包含 |
| 采样比例与筛选阈值说明 | 未发现 | 未公开 |
| AlphaBind 全量数据 | 未包含 | 未公开（需到上游仓库） |
| 三个非 VHH72 体系的 PDB 锚点 | 未发现 | 未公开 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-29；待上游说明）：七个 CSV 是 AlphaBind 的采样子集（合计 33,454 行），采样规则未在仓库中说明。已核实文件名含 `sampled_5k`、各表行数 4,254—5,000、训练与验证各一，且 `sample_alphabind_pairs.py` 只解释配对生成、不解释采样。影响：本仓库能支持的评测结论仅限这批采样候选，不能外推到 AlphaBind 全量；采样是否分层、是否按亲和力分桶都会影响模型表现的可比性。当前处理：README 明确标注采样性质与行数。下一步：核对 `model_src/dataset_mean.py` 或论文 Methods 中是否给出采样规则。
- `Q02`（最近更新：2026-10-29；已解决并结案）：论文补充材料首次下载被截断（1,118,208 bytes，非有效 zip）。复核时以 300 秒超时重新取得完整 ZIP（2,105,830 bytes，13 个成员），其 `mmc1.pdf` 为 3 页补充正文，已归入 `articles/MochiBind_2026-08-21_iScience-supplement.pdf` 并登记 SHA-256。补充正文未包含采样规则，采样问题继续由 `Q01` 跟踪。
- `Q03`（最近更新：2026-10-29；partial）：PEM、PP489、TRA 三个体系没有可辩护的 PDB 锚点。已核实：三个体系的 CSV 无 PDB 列，`matalpha_description` 只有展示构建标签；仓库 README、`evaluation_src/` 与论文均未给出对应晶体结构，论文对这些体系使用 Boltz-2 预测结构与 GeoDock 对接，属计算产物。影响：这三个体系的 PDB 子任务未完成，本来源的 PDB 子任务整体为 partial。当前处理：只保存 VHH72 的 6LZG，不用预测结构冒充实验锚点，不臆配其余体系的结构。下一步：若上游补充给出确切 PDB 或其抗原来源条目，再追加；否则接受 partial 状态。
- `Q04`（最近更新：2026-10-29；待说明）：仓库 README 的目录树根写作 `cell_submission_code/`，实际仓库根为 `ab-binding-eval/`。已核实 `git ls-tree` 的顶层条目只有 `checkpoint`、`data`、`evaluation_src`、`model_src` 与若干散文件，无 `cell_submission_code/` 目录。影响：按 README 的路径引用会找不到文件。当前处理：保留上游 tree 原样，README 中记录该差异。下一步：无需上游答复；下游按实际根目录引用。
- `Q05`（最近更新：2026-10-29；待字段定义）：验证表的 `predicted_affinity` 与 `avg_off_target_affinity` 来源、尺度与生成模型未在公开材料中说明。已核实 `predicted_affinity` 范围 −0.277—1.707，与 `alphaseq_affinity` 的 1.1—7.2 不同尺度；`avg_off_target_affinity` 无单位说明。影响：这两个字段是模型派生值，不能当实验标签；若误用会构成标签泄漏。当前处理：字段说明中明确标为模型派生并给出取值范围。下一步：核对生成这两个字段的 notebook（`evaluation_src/mochibind_trainval.ipynb`）以确认尺度。
