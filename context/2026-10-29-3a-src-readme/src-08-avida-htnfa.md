---
- tags:
  - context
---

# SRC_R08_AVIDA_HTNFA 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [三张 CSV 的关系](#三张-csv-的关系)
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

- `source_id`：`SRC_R08_AVIDA_HTNFA`
- `source_version`：`snapshot-2025-06-26`
- 原作者或发布机构：COGNANO

### 来源方背景

[公司介绍](https://www.cognano.co.jp/about)列出发布方的日本法律主体为株式会社 COGNANO，2014 年 10 月 17 日设立，总部位于京都市左京区，主营 VHH 抗体设计、制造和计算机辅助药物发现；该页另列美国支社 COGNANOUS, Inc.。公司围绕羊驼抗体建立序列与结合数据资源，并将这些数据用于抗体设计研究。

[官方数据集目录](https://www.cognano.co.jp/datasets)列出 AVIDa-hTNFa、AVIDa-hIL6、AVIDa-SARS-CoV-2 和 VHHCorpus，呈现其持续发布抗体序列与结合数据的工作。公司与 Google 合作的 AVIDa-hIL6 研究获 [NeurIPS 2023 接收](https://www.cognano.co.jp/news/avida-hil6-paper-neurips2023)，与樱花互联网研究所合作的 AVIDa-SARS-CoV-2 研究获 [NeurIPS 2024 Datasets and Benchmarks Track 接收](https://www.cognano.co.jp/news/avida-sars-cov-2-paper-neurips2024)。

## 实验设计和数据口径

COGNANO 将 AVIDa-hTNFa 描述为由两只经人肿瘤坏死因子 alpha（TNFα）蛋白免疫的羊驼产生的抗原—抗体相互作用数据集。公开标签表记录 VHH 序列与野生型人 TNFα 的结合或不结合，`label=1` 表示 binder，`label=0` 表示 non-binder。上游没有发布连续亲和力、动力学常数或阳性样本内部顺序，因此本 source 只能直接支持二元分类，不能把正例继续解释为相互可排序的 $K_D$ 数据。

`AVIDa-hTNFa.csv` 有 5,580 行，其中 682 行为正例、4,898 行为负例，涉及 5,577 条唯一 VHH 序列。3 条正例序列同时出现在 `happy` 和 `jessica` 两只羊驼下；没有序列同时带正、负标签。按行随机划分会把这 3 组同序列记录分到不同集合，建模时应按 VHH 序列分组。

`corpus-hTNFa.csv` 是无结合标签的 VHH 语料，共 216,225 行、216,059 条唯一序列。标签表中的 5,577 条唯一 VHH 全部出现在语料中；166 条序列分别出现在两只羊驼下。无标签语料不能当作负例。两张 VHH 表的序列均只含 20 种标准氨基酸字符，所有行以 6 个组氨酸结尾；字符串还包含上游构建体片段，不应直接当作已经裁剪、编号或标准化的 VHH 可变区。

`antigen_sequences.csv` 只有 `TNFa-WT-beads` 一条 233 aa 人 TNFα 前体序列。`beads` 是上游原始标签的一部分；dataset card 没有说明具体筛选平台、筛选轮次、实验重复、阈值或标签汇总规则。本项目不依据文件名补写这些方法细节。公开包属于处理后公开表，不是事件级或仪器级实验原始数据。

## 论文原文

- 标题：未识别到 AVIDa-hTNFa 对应的公开主论文
- 作者：上游页面未提供
- 发表来源：无；COGNANO 页面和 Hugging Face dataset card 均未引用论文
- 归档文本版本：无；未识别到可归档的 R08 论文
- 发布日期：无；数据集初始提交日期为 2025-02-14，不作为论文发布日期
- DOI：无；一手数据页未提供
- PMID / PMCID：无
- 本地文件：无；`articles/` 为空目录
- 文件大小：不适用
- SHA-256：不适用
- 文本许可：不适用；数据集许可另见“许可和再分发边界”
- 补充材料：无

检索发现的 AVIDa-hIL6 和 AVIDa-SARS-CoV-2 论文属于同系列其他数据集，不能作为 AVIDa-hTNFa 的主论文归档。缺少论文意味着当前无法从 Methods 或补充材料恢复免疫、建库、筛选和标签判定的完整过程。

## 仓库内容

上游入口为 Hugging Face dataset repository `COGNANO/AVIDa-hTNFa`。本 source 固定 revision `60c8288fd3721b0dca4f76655b491cfe7dd82d5d`；该提交时间为 2025-06-26T06:52:06Z，因此版本名为 `snapshot-2025-06-26`，不是本项目下载日期。仓库公开、非 gated，固定 revision 有 5 个文件；`corpus-hTNFa.csv` 是 Git LFS 对象，其余文件为普通 Git blob。

```text
snapshot-2025-06-26/
└── AVIDa-hTNFa/
    ├── .gitattributes
    ├── AVIDa-hTNFa.csv
    ├── README.md
    ├── antigen_sequences.csv
    └── corpus-hTNFa.csv
```

`README.md` 是上游 dataset card，`.gitattributes` 记录 LFS 跟踪规则；三张 CSV 分别保存二元标签数据、单条抗原序列和无标签 VHH 语料。本项目按固定 revision 保存文件字节，不改写 CSV。

## 数据结构

### 三张 CSV 的关系

| 文件 | 行数 | 唯一序列数 | 记录粒度 |
| --- | ---: | ---: | --- |
| `AVIDa-hTNFa.csv` | 5,580 | 5,577 VHH | 一条 VHH、一个抗原标签和一个二元结合标签 |
| `corpus-hTNFa.csv` | 216,225 | 216,059 VHH | 一条无结合标签的 VHH 语料记录 |
| `antigen_sequences.csv` | 1 | 1 antigen | 一个抗原标签及其完整公开序列 |

标签表与语料表通过原样 `VHH_sequence` 连接；5,577 条 labelled 唯一序列均能在 corpus 中找到。`subject_name` 和 `subject_sex` 共同区分两只羊驼：雄性 `happy` 与雌性 `jessica`。序列可跨 subject 重复，因此 `VHH_sequence` 不是 corpus 的行级唯一键。

### 字段说明

| 文件 | 字段 | 原始表示与含义 |
| --- | --- | --- |
| labelled、corpus | `VHH_sequence` | 大写标准氨基酸字符串；labelled 长 106–172 aa，corpus 长 100–185 aa；含构建体片段与末端 His 标签 |
| labelled | `Ag_label` | 字符串；固定为 `TNFa-WT-beads`，与抗原表连接 |
| labelled | `label` | 字符串化二元整数；`1` 为结合，`0` 为不结合；无缺失值 |
| labelled、corpus | `subject_species` | 字符串；固定为 `alpaca` |
| labelled、corpus | `subject_name` | 字符串；`happy` 或 `jessica` |
| labelled、corpus | `subject_sex` | 字符串；分别为 `male` 或 `female` |
| antigen | `Ag_label` | 字符串；固定为 `TNFa-WT-beads` |
| antigen | `Ag_sequence` | 大写标准氨基酸字符串；233 aa 人 TNFα 前体公开序列 |

三张 CSV 均有表头，没有空字段或非标准氨基酸字符。`label` 是上游发布的实验分类结果，不是本项目派生值；corpus 没有 `label`，其记录不得按缺失标签解释为阴性。

### 数据示例

下列内容逐字摘自固定 revision 的真实文件。为避免把长序列误认作独立结构样本，每张表只展示一行。

```text
AVIDa-hTNFa.csv
VHH_sequence=MKYLLPTAAAGLLLLAAQPAMAQVQLQESGGGLVQPGGSLRLSCKASGFTMNTATVGWFRQAPGKEREGVSCISSADVTNYADSVKGRFTISRDNPKNAVSLQMNSLKPEDTGVYYCAASRTYYPFCAGTNNFQSWGQGTQVTVSSHHHHHH
Ag_label=TNFa-WT-beads, label=1, subject_species=alpaca, subject_name=happy, subject_sex=male

corpus-hTNFa.csv
VHH_sequence=MKYLLPTAAAGLLLLAAQPAMAQVQLQESGGGLVQPGGSLRLSCKASGFTMNTATVGWFRQAPGKEREGVSCISSADVTNYADSVKGRFTISRDNPKNAVSLQMNSLKPEDTGVYYCAASRTYYPFCAGTNNFQSWGQGTQVTVSSHHHHHH
subject_species=alpaca, subject_name=happy, subject_sex=male

antigen_sequences.csv
Ag_label=TNFa-WT-beads
Ag_sequence=MSTESMIRDVELAEEALPKKTGGPQGSRRCLFLSLFSFLIVAGATTLFCLLHFGVIGPQREEFPRDLSLISPLAQAVRSSSRTPSDKPVAHVVANPQAEGQLQWLNRRANALLANGVELRDNQLVVPSEGLYLIYSQVLFKGQGCPSTHVLLTHTISRIAVSYQTKVNLLSAIKSPCQRETPEGAEAKPWYEPIYLGGVFQLEKGDRLSAEINRPDYLDFAESGQVYFGIIAL
```

前两段是同一 VHH 在 labelled 与 corpus 中的对应记录，不是两个独立样本。抗原行是所有 labelled 记录共享的外部对象。

## PDB 数据库

公开 CSV 没有逐 VHH PDB ID，也没有 AVIDa-hTNFa VHH—TNFα 实验复合物。PDB 子任务采用 RCSB `1TNF` 作为人 TNFα 靶点代表结构：它是 2.6 Å X 射线结构，polymer entity 1 的 author chains A/B/C 是相同的 157 aa 成熟 TNFα。项目只在 FASTA 中保留 chain A，完整 mmCIF 则保留整个沉积条目。

数据集 233 aa 抗原序列末端 157 aa 与 1TNF entity 1 有 156/157 aa 相同；唯一差异位于成熟片段第 143 位，数据集为 `D`、1TNF 为 `L`。因此映射强度是“靶点代表结构”，不是严格实验构建体映射、逐行映射或 VHH 复合物结构。

| PDB | 连接对象 | FASTA | FASTA 大小 / SHA-256 | mmCIF | mmCIF 大小 / SHA-256 |
| --- | --- | --- | --- | --- | --- |
| 1TNF | `TNFa-WT-beads` 的靶点参考 | `pdb/sequences/rcsb_pdb_1TNF.fasta` | 235 bytes / `0b0d3d82937c855cacb51259b9014429ce68d2b18aa0cb91990d9d59c714200f` | `pdb/structures/1TNF.cif` | 374.25 KiB（383,234 bytes） / `c86bc5041124d7cdcc0585ded990b489ef603b0f0d2b6dbb45a0f76856594ba5` |

FASTA 与 mmCIF 均已解析核对；只存在一个外部锚点，不为 5,580 条 labelled 记录复制结构文件。

## 采集过程记录

- 2026-09-18：从资源执行清单确认 R08 为 AVIDa-hTNFa，读取当时项目配置并运行 context 检查；历史记录中的存储根为 `/data/shared/binding-ranking-storage`。
- 2026-10-08：复核当前 `project.toml`，共享存储根已为 `/data/shared/CX029_binding_ranking`；本 source 正式目录与 README 均位于当前根下，旧根仅保留为历史配置记录。
- 2026-09-18：用 Hugging Face API 和 `hf` CLI 核验公开/非 gated 状态、CC BY-NC 4.0、revision、提交时间、5-file tree、LFS 身份和 dataset card；固定 revision `60c8288fd3721b0dca4f76655b491cfe7dd82d5d`。
- 2026-09-18：本地下载固定 revision 做独立 schema 检查，统计三张 CSV 的行数、唯一序列、标签、重复关系、字符集、长度和跨表包含关系。
- 2026-09-18：核对 COGNANO 页面、dataset card 与学术索引，未找到 R08 主论文、DOI 或补充材料；拒绝用同系列 hIL6/SARS-CoV-2 论文替代，`articles/` 保持空目录。
- 2026-09-18：审计 RCSB 人 TNFα 条目，选择 1TNF 作为靶点代表结构；确认 entity 1、author chain A、157 aa 序列和公开抗原序列的一处差异。
- 2026-09-18：在 ab02 的共享存储 staging 中逐文件下载 Hugging Face payload。5 个文件均按固定字节数与 SHA-256 验收；35.50 MiB（37,227,105 bytes）的 LFS corpus 使用 `curl --continue-at -` 下载并通过上游 LFS SHA-256。
- 2026-09-18：用通用 PDB 工具获取 1TNF chain A FASTA 与完整 mmCIF，核对 RCSB API、FASTA、chain mapping、坐标内容和 SHA-256；staging 未留下 `.partial` 文件。
- 2026-09-18：按项目严格格式完成 README 并同步 staging；Markdownlint 为 `0 error(s)`。独立验证通过全部 8 个文件；README 以外的 7 个数据与 PDB 文件合计 36.87 MiB（38,665,326 bytes），顶层目录、CSV schema 与统计、PDB 两层文件和 README revision 均一致。
- 2026-09-18：staging 全部验收通过后原子发布为 `SRC_R08_AVIDA_HTNFA/snapshot-2025-06-26`。正式路径复跑独立验证通过，无 `.partial` 或 `__pycache__` 残留；本地与远端 README SHA-256 一致。

## 参考文献

- COGNANO：[AVIDa-hTNFa 官方页面](https://cognanous.com/datasets/avida-htnfa)。
- COGNANO：[Hugging Face dataset](https://huggingface.co/datasets/COGNANO/AVIDa-hTNFa)。
- COGNANO：[固定 revision](https://huggingface.co/datasets/COGNANO/AVIDa-hTNFa/tree/60c8288fd3721b0dca4f76655b491cfe7dd82d5d)。
- RCSB PDB：[1TNF](https://www.rcsb.org/structure/1TNF)。
- Eck MJ, Sprang SR. *The structure of tumor necrosis factor-alpha at 2.6 A resolution. Implications for receptor binding.* J Biol Chem. 1989;264:17595–17605. PMID: [2551905](https://pubmed.ncbi.nlm.nih.gov/2551905/)。

## 其他

### 数据范围和限制

本 source 取得当前固定 revision 的完整公开包。研究过程中的事件级实验数据、连续亲和力、筛选阈值、实验重复、候选选择过程和 R08 专属论文尚未公开。标签表包含 5,580 行、5,577 条唯一 VHH；216,225 条 corpus 行没有结合标签。

### 完整性与验收

上游 payload 共 5 个文件、36.51 MiB（38,281,857 bytes），逐项 SHA-256 与固定 revision/LFS 身份一致。CSV 可完整解析，行数、字段、值域、序列字符集和跨表关系通过独立验证。PDB 子任务有 1 个锚点、1 个 FASTA 和 1 个完整 mmCIF，两层均通过解析和哈希检查。版本顶层只允许 `AVIDa-hTNFa/`、`articles/`、`pdb/` 和 `README.md`；`articles/` 为空是已记录的论文缺口，不是遗漏下载。

### 许可和再分发边界

Hugging Face dataset card 标注数据集为 CC BY-NC 4.0，要求署名且限制商业使用。RCSB 补充文件遵循 wwPDB/RCSB 的使用政策；1TNF 原论文权利不由数据集许可覆盖。任何商业使用或对外再分发都应分别核对数据集、PDB 和引用材料的条款。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 两只经人 TNFα 免疫的羊驼产生的数据集 | labelled/corpus 中 `happy`、`jessica` 及 dataset card 描述 | 已包含公开表；免疫方法细节未公开 |
| VHH—野生型 TNFα 结合/不结合标签 | `AVIDa-hTNFa.csv` 的 5,580 行与 `label` | 已包含 |
| 无标签 VHH sequence corpus | `corpus-hTNFa.csv` 的 216,225 行 | 已包含 |
| 野生型 TNFα 序列 | `antigen_sequences.csv` 的 1 条 233 aa 序列 | 已包含 |
| 连续亲和力、动力学或阳性内部排序 | 三张 CSV 均无对应字段 | 未公开 |
| AVIDa-hTNFa 主论文和补充方法 | 官方页面与 dataset card 未给出引用 | 未识别到公开版本 |
| 样本级实验复合物结构 | 上游无 PDB 键；1TNF 仅为外部靶点代表结构 | 未公开 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-22；待来源方说明）：COGNANO 的 R08 页面和固定 dataset card 未给出该数据集专属论文或完整实验方法；筛选平台、轮次、重复、阈值及标签汇总规则仍不明确。已核对公开三表和一手数据页，当前仅将 `label` 解释为来源方发布的二元结合分类。下一步向来源方询问方法文档和逐样本标签判定口径；取得材料前不推断连续亲和力或负例的检测边界。
- `Q02`（最近更新：2026-09-22；待使用授权）：dataset card 标注 CC BY-NC 4.0，当前没有覆盖商业训练的单独授权材料。已在许可章节保留原始条款，企业内部评估和模型训练的具体使用范围须先由权利方或法务确认；确认结果及适用版本应补入采集过程记录。
