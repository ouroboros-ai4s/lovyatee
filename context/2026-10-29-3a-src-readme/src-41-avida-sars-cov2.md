---
- tags:
  - context
---

# SRC_R41_AVIDA_SARS_COV2 数据说明

## 数据集身份

- `source_id`：`SRC_R41_AVIDA_SARS_COV2`
- `source_version`：`snapshot-2024-10-17`
- 原作者或发布机构：COGNANO；Hirofumi Tsuruta 等作者

## 实验设计和数据口径

两只经 SARS-CoV-2 抗原免疫的羊驼生成 VHH 文库；通过不同抗原与呈递方式的亲和筛选，再比较筛选前后 NGS 序列比例，以统计检验赋予 binder/non-binder 标签。论文说明约 97% 比例没有显著变化的候选被排除，未入表不等于不结合。公开表是筛选后处理标签集，既不是连续 KD 测量，也不是完整原始 reads。

总表 77,003 条 VHH—抗原/条件配对：22,002 个 label=1、55,001 个 label=0，36,100 个唯一 VHH，VHH 长度 94–166 aa。17 个 Ag_label 对应 17 条不同公开抗原序列；论文的 12 种抗原/变体口径与按 bead/cell construct 计数的 17 个条件不可混淆，面板包括 OC43 与 S2-domain。相同变体名的 bead/cell 序列长度可以不同，不能删掉后缀合并序列。

train.csv 包含 puta 的 49,685 对（15,400 阳性）；test.csv 包含 christy 的 27,318 对（6,602 阳性）。两表行互斥、并集严格等于总表，但有 264 条相同 VHH 跨 train/test；动物划分不保证序列互斥。不同抗原上的同一 VHH 是相关记录；评估新序列泛化应额外检查序列/谱系重叠。二元阳性内部没有定量排序依据。VHHCorpus-2M 是另一个无标签语料，本 source 未下载，也不计入实验配对规模。

## 论文原文

- 标题：A SARS-CoV-2 Interaction Dataset and VHH Sequence Corpus for Antibody Language Models
- 作者：Hirofumi Tsuruta, Hiroyuki Yamazaki, Ryota Maeda, Ryotaro Tamura, Akihiro Imura
- 载体与版本：arXiv:2405.18749v3，2024-10-16 版本；同时对应 NeurIPS 2024 研究
- 发布日期：2024-10-16
- DOI：`10.48550/arXiv.2405.18749`
- PMID / PMCID：无 / 无
- 本地文件：`articles/AVIDaSARSCoV2_2024-10-16_arXiv-v3.pdf`
- 文件大小：articles/AVIDaSARSCoV2_2024-10-16_arXiv-v3.pdf = 4429530 bytes
- SHA-256：articles/AVIDaSARSCoV2_2024-10-16_arXiv-v3.pdf = `42e025e4c84a8bad733dbc30c0b70c16e42e512fe913cf65b4d4598984dca74c`
- 文本许可：arXiv non-exclusive distribution license；不是数据的 CC BY-NC 4.0
- 补充材料：无独立补充文件；arXiv v3 主文包含附录与方法

论文数据许可与 PDF 文本许可不同；这里保存公开研究用原文，不把 arXiv 的非独占分发许可当成数据 CC 许可。

## 仓库内容

上游固定版本：[一手入口](https://huggingface.co/datasets/COGNANO/AVIDa-SARS-CoV-2/tree/2fd3633e5d0ebd5e21308e3a9a1adec26db86560)。revision/commit `2fd3633e5d0ebd5e21308e3a9a1adec26db86560`，上游版本日期 `2024-10-17T06:37:29.000Z`；据此命名 `snapshot-2024-10-17`，日期不是本次下载日期。

完整 HF revision 文件集合；LFS 总表按官方 SHA-256 验证，其余五个普通 Git blob 验证 SHA-1。不保留 Hugging Face 下载缓存，六个源文件原样落盘。

```text
snapshot-2024-10-17/
└── AVIDa-SARS-CoV-2/
    ├── .gitattributes
    ├── README.md
    ├── AVIDa-SARS-CoV-2.csv
    ├── antigen_sequences.csv
    ├── train.csv
    └── test.csv
```

总表是主入口，train/test 是同一总表的动物划分；antigen_sequences.csv 通过 Ag_label 连接抗原。

## 数据结构

### 配对表与抗原表

三个配对 CSV 使用相同六列：VHH_sequence、Ag_label、label、subject_species、subject_name、subject_sex。抗原表两列为 Ag_label、Ag_sequence，共 17 行；每个键唯一且所有配对键均能连接。总表、train/test 是同一标签集的不同表示，不能合并后得到 154,006 条独立样本。原文件采用 UTF-8，序列保留原字节，不重建或清洗。

### 字段说明

| 文件或表 | 原始字段 | 类型/单位/方向 | 缺失、边界及来源 |
| --- | --- | --- | --- |
| 三个配对 CSV | VHH_sequence | 氨基酸字符串；VHH 域，不是完整 IgG | 实验测序所得；94–166 aa；序列长度不代表完整抗体构建体 |
| 三个配对 CSV | Ag_label | 条件键，17 个枚举 | 须保留 _bead/_cell 后缀；包括 Alpha+E484K_cell、WT_cell、OC43_bead 等 |
| 三个配对 CSV | label | 整数 0/1，无连续亲和力单位 | 0 为统计支持的 non-binder、1 为 binder；来自比例变化，不是实测 KD |
| 三个配对 CSV | subject_species / subject_name / subject_sex | alpaca；puta/christy；male/female | 动物来源 metadata；与上游 train/test 分组关联 |
| antigen_sequences.csv | Ag_label / Ag_sequence | 条件键与抗原氨基酸串；521–1,328 aa | 17 条不同的原构建体序列；外部 spike 结构不保证精确覆盖这些 construct |

### 数据示例

来自 `AVIDa-SARS-CoV-2/AVIDa-SARS-CoV-2.csv` 的第一条真实记录（仅摘录下列列）：

```json
{
  "VHH_sequence": "MKYLLPTAAAGLLLLAAQPAMAQVQLQESGGGLVQPGGSLRLSCVASGFTLDYNAIGWFRQAPGKEREGVSCISPSGTSTKYEDSVKGRFTISRDNAKNTVYLQMNNLKPEDTAVYYCAAATPSYYYCSYYVSEYDDWGQGTQVTVSS",
  "Ag_label": "Alpha+E484K_cell",
  "label": "1",
  "subject_name": "christy"
}
```

一行表示某个 VHH 在某一抗原/条件中的二元配对标签。相同 VHH 可出现在多行，不是每行一个独立抗体。

## PDB 数据库

审计 HF payload、论文 v3 主文及附录：无逐 VHH 或逐配对 PDB 键。按公开靶点名称与 RCSB 实验条目连接，接受 6VSB（SARS-CoV-2 spike）和 6NZK（OC43 spike）作为两个靶点代表。两者均不是这 36,100 个 VHH 的实验复合物；不声称 17 个 construct 的逐条结构覆盖。

取得日期：2026-09-18。每个唯一 entry 保留完整 RCSB canonical entity FASTA 与完整沉积坐标，不选择性截断、不拼接设计序列。实体/链从 mmCIF `_entity` / `_entity_poly` 核对；canonical 序列与 FASTA entity 一致，坐标 `_entry.id` 与 PDB ID 一致，原子记录非空。

| PDB | 连接关系及证据 | polymer entity / author chains /长度 | FASTA/mmCIF |
| --- | --- | --- | --- |
| 6VSB | SARS-CoV-2 spike 靶点代表；不是 VHH 复合物或逐条件 construct；antigen_sequences.csv 的 WT_cell / SARS-CoV-2 条件与 RCSB 实验 spike 条目 | 1:A,B,C:1288aa | 两层 verified |
| 6NZK | OC43 spike 靶点代表；不是该 VHH 的复合物；antigen_sequences.csv 的 OC43_bead 与 RCSB Human coronavirus OC43 spike 条目 | 1:A,B,C:1322aa | 两层 verified |

| 文件 | bytes | SHA-256 |
| --- | --- | --- |
| pdb/sequences/rcsb_pdb_6VSB.fasta | 1389 | `9271cf16f39322f975db032f566b99ce739c2c14a9ed6aaddce7a69a4f3a25b0` |
| pdb/structures/6VSB.cif | 2514466 | `be3b6f34a8fe2118434e215cbf5bd00443a6eeed8953914299a15cc3db30b1fa` |
| pdb/sequences/rcsb_pdb_6NZK.fasta | 1404 | `d8a65e7665cd4dbd81541ab95c7678788a960e58041e9967cd51bb0a94ef0ba1` |
| pdb/structures/6NZK.cif | 3115073 | `c6bdd9f56f72b87897f497abb7963843d09524a6903127a0b792348440c0ccd9` |

共 2 个有效锚点、2 个 FASTA、2 个 mmCIF，5632332 bytes。每个下载使用 `https://www.rcsb.org/fasta/entry/<PDB_ID>/download` 与 `https://files.rcsb.org/download/<PDB_ID>.cif`；共享已存 gzip 坐标直接原样复用，未重压缩。完整 entry 可含未参与该研究的抗体/实体；链身份与映射边界按上表及下文使用。

6VSB、6NZK 的 polymer entity 1 为 spike，author chains A/B/C；三条同实体链不等于三个独立靶点。6VSB 的沉积序列含稳定化/融合构建体，6NZK 对应 OC43，均不能直接当 antigen_sequences.csv 的严格一致序列。

## 使用方式

```python
from pathlib import Path
import csv
root = Path(dataset_root)  # 调用者先赋值为 source version 目录
with (root / 'AVIDa-SARS-CoV-2' / 'AVIDa-SARS-CoV-2.csv').open(newline='') as f:
    pairs = list(csv.DictReader(f))
```

抗原另读 antigen_sequences.csv，以 Ag_label 连接；不要把标签换算为 KD。

## 采集过程记录

2026-09-18：读取项目上下文与资源清单，通过公开 HF API 解析 revision，再查询固定 revision 的完整对象 metadata。官方 lastModified 2024-10-17 是该数据版本日期；六个文件进入同根 staging，LFS 总表校验官方 SHA-256，普通文件校验 Git blob SHA-1。

2026-09-18：独立读取四张 CSV，检查标签枚举、抗原连接、重复、唯一序列与长度；验证 train/test 行并集及 264 条共享 VHH。通过 arXiv 历史确定 v3 日期并归档 PDF。RCSB 6VSB/6NZK 两层取得并校验；不为每条数据复制结构。

2026-09-18：论文/补充的下载身份和通用名修正留痕如下；原始文件与描述性落盘名对应的 bytes/SHA-256 均已核对，重命名没有改写内容。

| 下载一手 URL | 原始名 | 落盘路径 | bytes |
| --- | --- | --- | --- |
| <https://arxiv.org/pdf/2405.18749v3> | 2405.18749v3 | articles/AVIDaSARSCoV2_2024-10-16_arXiv-v3.pdf | 4429530 |

2026-09-18：本地 README 编辑后立即同步共享 staging，固定 markdownlint-cli2 0.20.0 按 skill 配置检查。发布、残留清理和当前缺口同步到本批交接；source version 不另发布 manifest、API 响应或审计文件。完整研究 acquisition 与本次公开包接入分开记录。

## 参考文献

- [固定上游数据版本](https://huggingface.co/datasets/COGNANO/AVIDa-SARS-CoV-2/tree/2fd3633e5d0ebd5e21308e3a9a1adec26db86560)
- [主论文 DOI](https://doi.org/10.48550/arXiv.2405.18749)
- [HF 数据 DOI](https://doi.org/10.57967/hf/2331)
- [固定 arXiv v3](https://arxiv.org/abs/2405.18749v3)
- [作者标签代码](https://github.com/cognano/AVIDa-SARS-CoV-2)
- [PDB 6VSB 及其原始结构论文](https://www.rcsb.org/structure/6VSB)
- [PDB 6NZK 及其原始结构论文](https://www.rcsb.org/structure/6NZK)

## 其他

### 完整性与验收

公开 payload 6 个文件、27629516 bytes；完整 Git archive/tree 验证 blob 数 0。文件 inventory 按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接的 SHA-256：`e612eeb09f101ce6a23d109383705662c6f8e7c3109b8450ea9f7cf89fd15242`。Git blob/LFS 官方身份分别验证；此 inventory 是项目本地摘要，不冒称上游官方 checksum。

本次完整 HF 公开处理包已下载并独立验收，论文及两个已接受靶点 PDB 两层完成；可声明 verified public-package onboarding。未获得完整底层 NGS 事件/reads，complete-study acquisition 不作完成声明。

### 许可和再分发边界

数据集明确 CC BY-NC 4.0，保留 COGNANO 署名及版本；PDF 为 arXiv non-exclusive distribution license，不能将其推广为数据许可。外部 PDB 为 RCSB/wwPDB 原始条目，应保留各结构论文引用。

### 公开范围对照

| 论文或来源所指内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 77,003 个有标签配对 | 总表 77,003 行；train/test 并集相等 | 已包含 |
| 抗原序列 | 17 个条件键与 17 条原序列 | 已包含 |
| 逐 VHH 实测复合物或连续 KD | 公开表没有对应字段；仅外部靶点结构 | 未包含 |
| VHHCorpus-2M | 另一个独立无标签语料 | 不在本 source 范围 |
