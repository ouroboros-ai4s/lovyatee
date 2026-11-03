# SRC_R51_MAVEDB 数据说明

## 数据集身份

- `source_id`：`SRC_R51_MAVEDB`
- `source_version`：`snapshot-2026-06-23`
- 原作者或发布机构：MaveDB；Jeremiah D. Heredia、Vahid Aslanzadeh、C. Anders Olson 等计分集原研究作者。

## 实验设计和数据口径

本 source 是 MaveDB 中五个明确列举的结合计分集快照，不是 MaveDB 全库，也不是对所有 protein–protein interaction assay 的关键词筛选结果。版本日期取五个记录中最晚的上游 `modificationDate`（2026-06-23）；每个计分集均保留稳定 URN。四个计分集以抗体结合为细胞分选读出，GB1 计分集以 IgG Fc 为结合对象。GB1 是细菌 IgG-binding protein 的突变扫描，不是候选抗体数据。

CCR5 与 CXCR4 实验分别对约七千个单氨基酸替换进行 Expi293F 细胞分选。`00000047-b-1` 的读出是抗体 2D7 结合，`00000048-c-1` 是抗体 12G5 结合；score 是两个 replicate 的 log2 enrichment 平均并按野生型归一化。CCR5 文件有 7,020 行，其中 6,895 个有限 score、125 个字符串 `NA`，有限值域 -7.622444692689999–2.9282988105400003。CXCR4 文件有 7,021 行，其中 6,996 个有限 score、25 个 `NA`，有限值域 -5–3.8503379019999997。较高分表示在该选择口径下相对富集更强；它不是 KD，也不能跨实验直接解释为共同的亲和力刻度。

INSR 两个计分集共享 19,100 个变体访问号，分别以 mAb 83-07 和 mAb 83-14 荧光结合信号分四个 bin。上游为使野生型在色标中居中，将正分重新缩放至负分范围；负分保持原尺度，因此不能把 score 当成原始对数亲和力或跨 assay 做线性比较。83-07 有 13,912 个有限 score、5,188 个 `NA`，值域 ±1.424359812043256；83-14 有 14,063 个有限 score、5,037 个 `NA`，值域 ±1.4062945062684111。FDR 与两个 replicate 列独立保留；缺失不补零。

GB1 实验用 mRNA display 测量 protein G B1 domain 对 IgG Fc 的结合。上游方法定义 `score = F_B,mut / F_B,wt`；值越高表示相对野生型结合比例越大，但仍不是以 M 为单位的 KD。导出含 536,476 行，全部 score 可解析，值域 0–14.46187297797798，其中 41,403 行为精确零。论文方法描述的设计库总复杂度与 MaveDB 实际导出行数不同，本 source 以下载文件的 536,476 行为事实，不补造缺失组合。

CSV 的 HGVS 坐标依赖 MaveDB 记录中的参考序列。CCR5/CXCR4 记录保存 1,053 nt DNA，分别映射 UniProt P51681/P61073；INSR 保存 955 aa 蛋白序列并映射 P06213；GB1 记录保存 221 aa 蛋白序列，方法指定 assay 区域为 protein G residues 228–282。参考序列本体属于上游记录元数据，本 source 不另存 API 响应 sidecar；使用时应以 URN 回查并保留访问日期。五个 CSV 中的 `accession` 各自唯一，不能跨计分集仅凭 HGVS 字符串合并样本。

这些分数是突变效应标签，replicate、FDR 和上游标准化结果均可能泄露实验结果。训练/评价划分应按实验、靶点和共享变体背景分组；不能把同一 INSR 变体在 83-07 与 83-14 两个 assay 中随机拆到两侧后宣称独立泛化。

## 论文原文

本 source 对应三项研究；论文文件的许可与 MaveDB 计分集 CC0 分开处理。

1. CCR5/CXCR4：Heredia et al., *Mapping Interaction Sites on Human Chemokine Receptors by Deep Mutational Scanning*，Journal of Immunology，2018-06-01，ePub 2018-04-20，DOI `10.4049/jimmunol.1800343`，PMID 29678950，PMCID PMC5964024。本地文件 `articles/MaveDB_Chemokine_2018-04-20_PMC-BioC.xml` 是 NCBI PMC BioC XML 公共访问衍生表示，162,603 bytes，SHA-256 `f79ce14fab43777f42b7cda10402f6eb937dc220c1a31cb861a5a4128269570e`。
2. INSR：Aslanzadeh et al., *Deep mutational scanning of the human insulin receptor ectodomain to inform precision therapy for insulin resistance*，bioRxiv v1，2024-09-08，DOI `10.1101/2024.09.07.611782`。本地文件 `articles/MaveDB_INSR_2024-09-08_bioRxiv-v1.pdf`，1,852,307 bytes，55 页，SHA-256 `3a00e844910b6c83f761e0a75f45f26fd28dbafe669c04193d3688f0eee14d84`。
3. GB1：Olson et al., *A comprehensive biophysical description of pairwise epistasis throughout an entire protein domain*，Current Biology，2014-11-17，ePub 2014-10-16，DOI `10.1016/j.cub.2014.09.072`，PMID 25455030，PMCID PMC4254498。本地文件 `articles/MaveDB_GB1_2014-10-16_PMC-BioC.xml` 是 NCBI PMC BioC XML 公共访问衍生表示，94,793 bytes，SHA-256 `11e4334c4743beed6f3ded5e2b55e887d612d9f45b65d7cde9799b6d02cf5e2a`。

BioC XML 是机器可读全文表示，不是出版社排版 PDF；没有把 XML 的生成日期当作论文版本日期。

## 仓库内容

MaveDB 一手记录入口是各 score-set URN 的网页/API；CSV 由公开 score endpoint 原样保存。`snapshot-2026-06-23` 锚定所选记录的最大修改日期，不表示当天冻结了 MaveDB 其他记录。上游没有 Git tree、LFS 或 submodule。

```text
snapshot-2026-06-23/
├── MaveDB/
│   ├── 00000047-b-1-scores.csv
│   ├── 00000048-c-1-scores.csv
│   ├── 00000105-a-1-scores.csv
│   ├── 00001239-a-2-scores.csv
│   └── 00001239-a-3-scores.csv
├── articles/
│   ├── MaveDB_Chemokine_2018-04-20_PMC-BioC.xml
│   ├── MaveDB_GB1_2014-10-16_PMC-BioC.xml
│   └── MaveDB_INSR_2024-09-08_bioRxiv-v1.pdf
└── pdb/
    ├── sequences/
    └── structures/
```

正式 source version 只包含上述原始计分 CSV、论文支持材料、每个接受 PDB 的两层原件和本 README。MaveDB API JSON、检索响应、审计报告与下载日志不进入 source version。

## 数据结构

### 五个计分集

| URN | 结合对象与 assay | 行数 | 有限 score / `NA` | score 方向 |
| --- | --- | ---: | ---: | --- |
| `urn:mavedb:00000047-b-1` | CCR5–抗体 2D7，细胞分选 | 7,020 | 6,895 / 125 | 较高为相对富集更强 |
| `urn:mavedb:00000048-c-1` | CXCR4–抗体 12G5，细胞分选 | 7,021 | 6,996 / 25 | 较高为相对富集更强 |
| `urn:mavedb:00001239-a-2` | INSR–mAb 83-07，四 bin | 19,100 | 13,912 / 5,188 | 上游重缩放分数，较高为更强读出 |
| `urn:mavedb:00001239-a-3` | INSR–mAb 83-14，四 bin | 19,100 | 14,063 / 5,037 | 上游重缩放分数，较高为更强读出 |
| `urn:mavedb:00000105-a-1` | GB1–IgG Fc，mRNA display | 536,476 | 536,476 / 0 | 相对 WT fraction bound，较高为更强 |

### 字段说明

| 文件范围 | 字段 | 原始表示、单位、方向与来源 |
| --- | --- | --- |
| 全部 CSV | `accession` | MaveDB 变体访问号；在各文件内唯一，无单位。 |
| 全部 CSV | `hgvs_nt`; `hgvs_splice`; `hgvs_pro` | 相对该 score set 参考序列的 HGVS 表示；不保证三列都适合所有变体类型，不应用 PDB 序列替代参考序列。 |
| 全部 CSV | `score` | 上游处理后的突变效应；较高表示该 assay 下结合选择读出更强。不是共同单位，也不是 KD。字符串 `NA` 表示缺失。 |
| CCR5/CXCR4 | `rep1`; `rep2` | 两个独立选择 replicate 的 log2 enrichment；数值或 `NA`，属于结果列。 |
| INSR | `FDR` | 上游显著性/错误发现率结果，0–1；缺失随 score 保留，不能当输入特征。 |
| INSR 83-07 | `a07BindR1`; `a07BindR2` | 83-07 binding 两个 replicate 的上游分数；数值或 `NA`。 |
| INSR 83-14 | `a14BindR1`; `a14BindR2` | 83-14 binding 两个 replicate 的上游分数；数值或 `NA`。 |

### 数据示例

| 文件 | accession 对应 HGVS protein | score | 解释 |
| --- | --- | ---: | --- |
| `00000047-b-1-scores.csv` | `p.Asp2Ala` | 1.4742712001894998 | CCR5 2D7 结合选择的平均归一化富集 |
| `00000048-c-1-scores.csv` | `p.Glu2Ala` | -0.1858884395 | CXCR4 12G5 结合选择分数 |
| `00000105-a-1-scores.csv` | `p.[Thr10Gly;Val38Tyr]` | 0.04172605973973975 | GB1 双突变体相对 WT fraction bound |

示例只展示原文件首条记录的部分列；它们来自不同 assay，数值不可直接排序为统一亲和力榜单。

## PDB 数据库

PDB 子任务：completed（五个经过映射审计的代表/复合物锚点均有 RCSB 原始两层文件）。这些结构不是 588,717 行变体的逐行坐标覆盖，也没有用模板重建任何突变体。

- [4MBS](https://www.rcsb.org/structure/4MBS) 是含 rubredoxin 融合和工程突变的 CCR5–maraviroc 结构。它只支持 CCR5 靶点身份，不包含实验抗体 2D7，也不等同于细胞 assay 构建体。
- [3ODU](https://www.rcsb.org/structure/3ODU) 是 CXCR4–T4 lysozyme chimera 与小分子拮抗剂 IT1t 的结构。它只支持 CXCR4 靶点身份，不包含 12G5。
- [4ZXB](https://www.rcsb.org/structure/4ZXB) 同时包含 INSR ectodomain、Fab 83-7 和 Fab 83-14，是两个 INSR 计分集的直接实验复合物参考；仍不是每个突变体的结构。
- [1PGA](https://www.rcsb.org/structure/1PGA) 是 standalone protein G B1 domain，支持 assay domain 的折叠参考，不含 IgG Fc。
- [1FCC](https://www.rcsb.org/structure/1FCC) 是 protein G C2 domain 与 human IgG1 Fc 的复合物，支持同源 Fc-binding interface。它不是论文使用的 B1 序列构建体，因此与 1PGA 分工记录结构与界面证据。

2026-09-19 对每个 entry 同时取得 RCSB 原样完整 FASTA 和完整 mmCIF，验证 FASTA polymer entities 与 mmCIF canonical entities 一致且坐标非空。保留全部 entry entity/链，没有裁链、拼接或生成结构。

| PDB | 文件 | bytes | SHA-256 |
| --- | --- | ---: | --- |
| 4MBS | `pdb/sequences/rcsb_pdb_4MBS.fasta` | 519 | `a1f17e8696d60ff8decbc0b8310a2192602d35596151ec1f24cdebfa5ee55152` |
| 4MBS | `pdb/structures/4MBS.cif.gz` | 304669 | `f674cf81a9ff26ff92a9e553a429ca01d0071a16ed275aeea5d7bd9b4f8d6cd7` |
| 3ODU | `pdb/sequences/rcsb_pdb_3ODU.fasta` | 593 | `6a4972aee08fd4efad7912c84501090d755353c77b6cb316f9b687c8ca300b18` |
| 3ODU | `pdb/structures/3ODU.cif.gz` | 394689 | `6d6c7fbdf5ffe1dd7c867ffbfc8cb68d6658d64c6a6775a0cfdf846b8f632643` |
| 4ZXB | `pdb/sequences/rcsb_pdb_4ZXB.fasta` | 2058 | `d0385440b797b29443cc980548217cf35251293091b44974ea6a8f07a1fa7003` |
| 4ZXB | `pdb/structures/4ZXB.cif.gz` | 695359 | `cc5ba0f4cba5d9ff301bb6ba0b2068af1051298500ff6fa291bd679ab7e693e0` |
| 1PGA | `pdb/sequences/rcsb_pdb_1PGA.fasta` | 115 | `a56ce69e9e80a566367b6b4b3a01a263d61e9b5c58dd55e9eb8e49a50bd6b561` |
| 1PGA | `pdb/structures/1PGA.cif.gz` | 20851 | `3758c785fd9dbb3f262ae8b40e614fbf1f2c4b69c91368c4f124a499dccc3246` |
| 1FCC | `pdb/sequences/rcsb_pdb_1FCC.fasta` | 412 | `35fc5d94310add9a0cf0660d3bad3e80ad69e3e7ae79d0f5cc9595620354dfae` |
| 1FCC | `pdb/structures/1FCC.cif` | 443502 | `92f4be40355db395b7058ee5fd3f39772168b684cfe5736700e03ac498a26867` |

## 使用方式

调用者先把 dataset_root 设为本 source version 路径；不要把路径写死到分析代码。

```python
from pathlib import Path
import csv

score_file = Path(dataset_root) / "MaveDB/00001239-a-2-scores.csv"
with score_file.open(encoding="utf-8", newline="") as stream:
    rows = csv.DictReader(stream)
    first_record = next(rows)
    score = None if first_record["score"] == "NA" else float(first_record["score"])
```

应保留 URN/文件名作为 assay 键；解析 `NA` 后仍需保留 missingness，不要把不同计分集拼接后直接按 score 数值排序。

## 采集过程记录

1. 2026-09-18 至 2026-09-19 读取项目/开发者配置并运行项目 context，确认工作文件属于 wuhuawei，真实数据根由 `project.toml` 提供。
2. 通过 MaveDB score-set 搜索和公开 API 枚举明确的 antibody-binding/IgG-Fc binding 记录；固定五个 URN、记录发布日期/修改日期、CC0 和实验元数据。范围选择是人工审阅结果，不宣称关键词召回全部相关 assay。
3. 从 MaveDB score endpoints 下载五个 CSV。GB1 大文件在先前中断后已完整取得；本次重新按 bytes、SHA-256、全行 CSV 解析和唯一 accession 验收，纠正旧状态记录中的“GB1 失败”。
4. 对全部 588,717 行检查列、有限值、`NA`、数值范围、唯一键与不可见 Unicode；原字节不作清洗。参考序列只从实时记录核对，不把 API JSON sidecar 放入 source version。
5. 分别取得 INSR bioRxiv v1 PDF，以及 CCR5/CXCR4 与 GB1 的 PMC BioC XML；校验文件格式、论文身份、PDF 页数与固定 SHA-256。论文公开访问不被解释成五个计分集之外的数据许可。
6. 审阅论文和 RCSB entry/entity 后接受 4MBS、3ODU、4ZXB、1PGA、1FCC，并逐对验证完整 FASTA/mmCIF。发现 1PGA 同一 mmCIF 的压缩和未压缩冗余副本后，比对解压字节相同，仅保留原已审计的 `.cif.gz`。
7. 本地 README 写入后立即同步 staging；固定 markdownlint、文件 allowlist、全部 SHA-256、格式与 PDB pair 通过后才原子发布。正式版本不保存 manifest、API 响应或下载日志。

## 参考文献

- [MaveDB](https://www.mavedb.org/)；[公开 API 文档](https://api.mavedb.org/docs)。
- [Heredia et al. 2018](https://doi.org/10.4049/jimmunol.1800343)；[PMC 全文记录](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5964024/)。
- [Aslanzadeh et al. bioRxiv v1](https://doi.org/10.1101/2024.09.07.611782)。
- [Olson et al. 2014](https://doi.org/10.1016/j.cub.2014.09.072)；[PMC 全文记录](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4254498/)。
- [4MBS](https://doi.org/10.2210/pdb4MBS/pdb)、[3ODU](https://doi.org/10.2210/pdb3ODU/pdb)、[4ZXB](https://doi.org/10.2210/pdb4ZXB/pdb)、[1PGA](https://doi.org/10.2210/pdb1PGA/pdb)、[1FCC](https://doi.org/10.2210/pdb1FCC/pdb)。

## 其他

### 完整性与验收

五个 CSV、三份论文支持材料和五对 PDB 两层文件构成固定 allowlist。所有 CSV 均从首行解析至 EOF，行数之和 588,717；XML/PDF 格式和 PDB entity/坐标均独立打开验证。上游未给这些下载对象统一 checksum，以下 SHA-256 是本次本地计算的身份摘要，不冒充官方 checksum。

| 相对路径 | bytes | SHA-256（本地计算） |
| --- | ---: | --- |
| `MaveDB/00000047-b-1-scores.csv` | 642936 | `7b9bbcbe74debd2325aaed7588b7902d5314e934e08d951e56e5dd1f01f1e430` |
| `MaveDB/00000048-c-1-scores.csv` | 638979 | `dbb9deb645fad5a29c4fff75356eacef01d86f9021edf23cf600a78e5a0d8072` |
| `MaveDB/00001239-a-2-scores.csv` | 2051917 | `eb873299ba5a775aa13a3e4029340d6912504d4a58a4367c18d5f0520b668764` |
| `MaveDB/00001239-a-3-scores.csv` | 2061691 | `f8aa47b62d1900bd86af8ee9d91ffb8c02319e91a8556f4fb516895bef40bd9b` |
| `MaveDB/00000105-a-1-scores.csv` | 41923816 | `8c350f9d5f5543667f87e9b5de0602641f88c05b60f44ee20b5b3e11cccbc806` |
| `articles/MaveDB_INSR_2024-09-08_bioRxiv-v1.pdf` | 1852307 | `3a00e844910b6c83f761e0a75f45f26fd28dbafe669c04193d3688f0eee14d84` |
| `articles/MaveDB_Chemokine_2018-04-20_PMC-BioC.xml` | 162603 | `f79ce14fab43777f42b7cda10402f6eb937dc220c1a31cb861a5a4128269570e` |
| `articles/MaveDB_GB1_2014-10-16_PMC-BioC.xml` | 94793 | `11e4334c4743beed6f3ded5e2b55e887d612d9f45b65d7cde9799b6d02cf5e2a` |

### 许可和再分发边界

五个 MaveDB score-set 记录均明确标为 CC0 1.0；该声明支持这些计分导出的再使用。论文 PDF/XML、PDB 文件和第三方内容遵循各自作者、publisher、PMC 与 RCSB/wwPDB 的条款，不能把 MaveDB 的 CC0 自动扩展给它们。使用或再分发时保留 URN、论文 DOI/PMCID、PDB accession、文件身份和本 snapshot 的范围说明。

### 公开范围对照

| 上游或论文内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 五个明确选择的结合 score sets | 五个完整 CSV，共 588,717 行 | 已包含并验收 |
| score-set 参考序列与完整元数据 | MaveDB 实时记录可按 URN 回查；source version 不存 API sidecar | 可回查，未复制为独立 payload |
| 原始测序 reads、FACS event、完整 bin counts | CSV 只有处理后 score/replicate/FDR；论文支持材料不是仪器原始包 | 未取得/不在本范围 |
| CCR5/CXCR4 assay 抗体复合物 | 4MBS/3ODU 仅为靶点代表，不含 2D7/12G5 | 未公开到本 source |
| INSR 两抗体复合物 | 4ZXB 同时含 INSR、Fab 83-7、Fab 83-14 | 已包含代表结构 |
| GB1 折叠与 Fc-binding interface | 1PGA 为 B1 domain；1FCC 为同源 C2–Fc 复合物 | 已包含、映射限制已明示 |
| 每个变体的实验结构 | PDB 锚点不是逐变体映射 | 未声称 |
