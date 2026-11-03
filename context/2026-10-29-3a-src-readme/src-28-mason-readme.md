---
tags:
  - context
---

# SRC_R28_MASON 数据说明

## 数据集身份

- `source_id`：`SRC_R28_MASON`
- `source_version`：`snapshot-2020-09-02`
- 原作者或发布机构：Derek M. Mason、Sai T. Reddy 等；ETH Zurich

## 实验设计和数据口径

以 trastuzumab / HER2 为系统，在哺乳动物细胞展示完整 IgG，通过 CRISPR/HDR 引入突变，分选/测序，再由处理后的阳性/阴性 CDRH3 训练分类模型。公开 DMS_opt 是分析快照，数据含测序统计和分类，不是每条 CDR3 精确 KD。最终 Nature 论文与早期 bioRxiv v2 的规模/验证结果不同，不能把预印本数字当最终实验文件计数。

公开 AgNeg 有 27,539 行/27,456 条唯一 AASeq，AgPos 有 11,300 行/11,277 条唯一 AASeq；两表共有 2,342 条相同 AASeq，合并仅 36,391 条唯一 CDR3。Count/Fraction 是测序计数/频率，AgClass=0/1 是分选分类，AASeq 仅 CDR3。共同序列、亲本、分选轮次和重复需分组，不能将相同 CDR3 的正负记录视为两个独立对象，也不能拼接亲本生成未发布的完整抗体。

## 论文原文

### bioRxiv v2 主文

- 标题：Deep learning enables therapeutic antibody optimization in mammalian cells by deciphering high-dimensional protein sequence space
- 作者：Derek M Mason; Simon Friedensohn; Cédric R Weber; Christian Jordi; Bastian Wagner; Simon Meng; Pablo Gainza; Bruno E Correia; Sai T Reddy
- 载体与版本：bioRxiv v2
- 发布日期：2019-05-30
- DOI：10.1101/617860
- PMID / PMCID：无 / 无
- 本地文件：`articles/MASON_2019-05-30_bioRxiv-v2.pdf`
- 文件大小：MASON_2019-05-30_bioRxiv-v2.pdf：4626880 bytes
- SHA-256：MASON_2019-05-30_bioRxiv-v2.pdf：`e5162a70fa33e20eb9250d3c9f6b0ae90066f0dec15e3c746221e0cf0f7973a5`
- 文本许可：CC BY-NC-ND 4.0 (preprint PDF statement verified; final-article supplements retain their separate publisher terms)
- 补充材料：无其他独立补充文件。

### 最终文章公开补充

- 标题：Optimization of therapeutic antibodies by predicting antigen specificity from antibody sequence via deep learning
- 作者：Mason, Derek M.; Friedensohn, Simon; Weber, Cédric R.; Jordi, Christian; Wagner, Bastian; Meng, Simon M.; Ehling, Roy A.; Bonati, Lucia; Dahinden, Jan; Gainza, Pablo; Correia, Bruno E.; Reddy, Sai T.
- 载体与版本：Nature Biomedical Engineering 正式文章的公开补充（未取得最终主文）
- 发布日期：2021-04-15
- DOI：10.1038/s41551-021-00699-9
- PMID / PMCID：33859386 / 无
- 本地文件：`articles/MASON_2021-04-15_NatureBiomedicalEngineering-published-supplement-1.pdf`；`articles/MASON_2021-04-15_NatureBiomedicalEngineering-published-supplement-2.pdf`
- 文件大小：MASON_2021-04-15_NatureBiomedicalEngineering-published-supplement-1.pdf：4348861 bytes；MASON_2021-04-15_NatureBiomedicalEngineering-published-supplement-2.pdf：104184 bytes
- SHA-256：MASON_2021-04-15_NatureBiomedicalEngineering-published-supplement-1.pdf：`e48cbea43b4b22b2bd2ab3738d9bc3d95a993ccd60a961133194243da56effb3`；MASON_2021-04-15_NatureBiomedicalEngineering-published-supplement-2.pdf：`173780a076fd2946c8b936f90f0a478d98e586db58a95d9167d7335b95169641`
- 文本许可：未单独核实明确再分发许可；公开补充按原发布页条款保存
- 补充材料：已归档 2 个文件。

| 本地文件 | 角色 | bytes | SHA-256 |
| --- | --- | --- | --- |
| `articles/MASON_2021-04-15_NatureBiomedicalEngineering-published-supplement-1.pdf` | Final article Supplementary Information | 4348861 | `e48cbea43b4b22b2bd2ab3738d9bc3d95a993ccd60a961133194243da56effb3` |
| `articles/MASON_2021-04-15_NatureBiomedicalEngineering-published-supplement-2.pdf` | Final article Reporting Summary | 104184 | `173780a076fd2946c8b936f90f0a478d98e586db58a95d9167d7335b95169641` |

最终主文未取得。补充属于 2021-04-15 的最终文章，不能归入 2019-05-30 的预印本版本。

## 仓库内容

- 一手入口：<https://github.com/dahjan/DMS_opt>；commit `eec710e5af3a99b2d52e45fc858bc2a9a25b5a62`，tree `e4daecd71029b51d34c7aac80e484ff577253a66`；上游日期 2020-09-02。

完整公开 Git tree、合法公开的作者预印本和最终文章补充材料、共享亲本 PDB；最终主文付费，全部大规模原始/分析数据按论文研究用途向作者申请。本次未取得申请部分。

快照日期来自已固定 commit `eec710e5af3a99b2d52e45fc858bc2a9a25b5a62` 的 committer 日期 2020-09-02；不是下载日期。原交付归档保持压缩格式，验收时读取所有成员，不在 raw 中重新生成数据表。

```text
snapshot-2020-09-02/
  DMS_opt/
    DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62.tar.gz
```

Git 快照全部 blob 与固定 commit tree 校验；eec710e5af3a99b2d52e45fc858bc2a9a25b5a62：42 个 blob，LFS 0，submodule 0。

## 数据结构

### 原始交付与记录粒度

Git 包完整保留 data/、训练代码和环境。两个主要 CSV 有首列无名 index，后为 Count、Fraction、NucSeq、AASeq、AgClass；TXT 是上游各分选/重复交付的测序统计文本，按原布局保留。Eisenberg.csv 和 pKas.csv 没有 header，首行 A 也是数据，各 20 个氨基酸，不是 19 行带表头的表。

| 原始表或 sheet | 非空数据行 | 列数 |
| --- | --- | --- |
| `DMS_opt/DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62.tar.gz!DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62/data/Eisenberg.csv` | 20 | 3 |
| `DMS_opt/DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62.tar.gz!DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62/data/mHER_H3_AgNeg.csv` | 27539 | 6 |
| `DMS_opt/DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62.tar.gz!DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62/data/mHER_H3_AgPos.csv` | 11300 | 6 |
| `DMS_opt/DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62.tar.gz!DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62/data/pKas.csv` | 20 | 4 |

表行数包含重复条件、示例和派生副本，不求和作为独立生物对象。下表列名保持原始拼写；空表头以 `（空列名）` 标出，未修改文件。

### 字段说明

无名首列：上游行索引；Count：测序计数；Fraction：该上游表的相对频率（无量纲）；NucSeq：上游核苷酸片段；AASeq：CDRH3，不是完整 IgG；AgClass：0 阴性/1 阳性分选标签，有利方向为 1；无逐序列 KD。Eisenberg/pKas 为辅助理化查表，原文件无列名，审计报告中的列名仅为 parser 说明。

| 原始表或 sheet | 字段（原始顺序） | 原始表示与特殊值 |
| --- | --- | --- |
| `DMS_opt/DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62.tar.gz!DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62/data/Eisenberg.csv` | `amino_acid`, `hydrophobicity`, `hydrophobicity_2` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `DMS_opt/DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62.tar.gz!DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62/data/mHER_H3_AgNeg.csv` | `（空列名）`, `Count`, `Fraction`, `NucSeq`, `AASeq`, `AgClass` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `DMS_opt/DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62.tar.gz!DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62/data/mHER_H3_AgPos.csv` | `（空列名）`, `Count`, `Fraction`, `NucSeq`, `AASeq`, `AgClass` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：无 |
| `DMS_opt/DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62.tar.gz!DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62/data/pKas.csv` | `amino_acid`, `pka_carboxyl`, `pka_amino`, `pka_sidechain` | CSV 字符串或 XLSX 原类型/公式；观察到缺失/特殊码：pka_sidechain=13 |

### 数据示例

来自 `DMS_opt/DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62.tar.gz!DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62/data/mHER_H3_AgNeg.csv` 的第一条真实非空数据行：

| 原始字段 | 原始值 |
| --- | --- |
| （空列名） | 0 |
| Count | 7 |
| Fraction | 6.899141451125989e-06 |
| NucSeq | TGTAGCAGGTACACTATCTGCAGTTTCTACAAGCTCCAGTATTGG |
| AASeq | YTICSFYKLQ |
| AgClass | 0 |

这是该原始表的一条记录；粒度按前述定义，不把结构表示、重复或归档成员当独立抗体。

## PDB 数据库

bioRxiv v2 原文明确用 PDB 1N8Z 的 trastuzumab 进行计算重设计，与公开 HER2 CDRH3 系统有一手连接。1N8Z 是共享亲本 Fab/HER2 复合物，不是每个 CDR3 变体的结构，不自动赋予逐行 VH/VL。

本次审计接受 1 个唯一锚点，每个都有 RCSB 完整 entry FASTA 与完整 gzip mmCIF，共 2 个文件 / 213626 bytes。逐对检查 entry ID、非空 _atom_site 及 canonical polymer 序列一致。FASTA 保留 RCSB entity ID、原始头和序列，没有从坐标重建序列；坐标保留完整原文件。author/label chain 与 entity 的原始映射在 FASTA 头及 mmCIF `_struct_asym`、`_entity_poly`、`_atom_site.auth_asym_id` 中，不臆造链角色。

文件路径为 `pdb/sequences/rcsb_pdb_<PDB>.fasta`、`pdb/structures/<PDB>.cif.gz`。确定性 inventory SHA-256：`f0cfab033229e7c2b155ef00be8037cd518f512bea7c3d0498468b40fd654b5d`；算法为按相对路径排序，逐文件组成 `path<TAB>bytes<TAB>sha256<LF>`（UTF-8）再计算 SHA-256。

| PDB | FASTA bytes / SHA-256 | mmCIF.gz bytes / SHA-256 |
| --- | --- | --- |
| 1N8Z | 1272 / `e7525106a38eaa6af60b88b93b8675a1fe916a02278990ca16ad6cbc0f08ba24` | 212354 / `3a59b29e39203f1bacc9147a8b143071c77b103c597a0a9e3bdfc6c965b70951` |

## 使用方式

由调用者将 `dataset_root` 赋为该 source_version 目录。以下仅读原始入口，不清洗、换算或修补 raw。

```python
import tarfile
with tarfile.open(dataset_root / "DMS_opt/DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62.tar.gz") as archive:
    print(archive.getnames()[:5])
```

## 采集过程记录

2026-09-18：保存固定 DMS_opt Git tree、2019-05-30 bioRxiv v2 原主文，以及 2021-04-15 最终文章的两份公开补充；未取得付费最终主文和需申请的大规模原始数据。主表正负 CDR3 交集和无表头理化表均按实际字节检查。仓库缺少 LICENSE，README 对不存在 LICENSE.md 的引用不作为许可。1N8Z 按预印本所述亲本结构补充。

2026-09-18：全部正式 payload 按来源身份、大小和官方/本地 checksum 独立验收；原始表与附件已读取，FASTA 和完整 mmCIF 逐对核验。工作 README 同步共享版本，规定的 markdownlint 为零错误后发布。具体 API、原始下载日志、失败和重试记录保存在共享本批采集目录，未向任何作者发送消息或申请。

2026-09-18：复核 skill 版本规则，核实并保留 `snapshot-2020-09-02`，补充一手版本命名依据。同步来源配置、PDB 配置、工作与共享 README 及当前结构化验收/发布记录；旧文档和原验收记录保留在 runs 的 version-migration-history。修订前后按相对路径、字节数和 SHA-256 比对全部科学文件，内容保持原样；修订 README 使用规定的 markdownlint 配置验收。

2026-09-18：README 工作稿迁入由 developer.user 定位的个人 docs/readme。初版采集记录混用了跨来源的通用描述，本次按实际来源、下载与重试记录修订。论文及附件命名补齐平台和版本，R28 最终文章补充采用其自身 2021-04-15 发布日期。以下名称变更均核对原文件字节数及 SHA-256，内容未改写；原始文件名与下载 URL 保留在采集记录中。

- `articles/MASON_2019-05-30_bioRxiv-v2.pdf` → `articles/MASON_2019-05-30_bioRxiv-v2.pdf`；4626880 bytes，SHA-256 `e5162a70fa33e20eb9250d3c9f6b0ae90066f0dec15e3c746221e0cf0f7973a5`。
- `articles/MASON_2019-05-30_supplement-1.pdf` → `articles/MASON_2021-04-15_NatureBiomedicalEngineering-published-supplement-1.pdf`；4348861 bytes，SHA-256 `e48cbea43b4b22b2bd2ab3738d9bc3d95a993ccd60a961133194243da56effb3`。
- `articles/MASON_2019-05-30_supplement-2.pdf` → `articles/MASON_2021-04-15_NatureBiomedicalEngineering-published-supplement-2.pdf`；104184 bytes，SHA-256 `173780a076fd2946c8b936f90f0a478d98e586db58a95d9167d7335b95169641`。

旧文档和结构化报告保存在共享 runs/documentation-reorganization；修订后本地与共享 README 同步并执行规定的 Markdownlint。

- 上游原始名称 `617860v2.full.pdf`；入口 <https://www.biorxiv.org/content/10.1101/617860v2.full.pdf>。
- 上游原始名称 `41551_2021_699_MOESM1_ESM.pdf`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41551-021-00699-9/MediaObjects/41551_2021_699_MOESM1_ESM.pdf>。
- 上游原始名称 `41551_2021_699_MOESM2_ESM.pdf`；入口 <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41551-021-00699-9/MediaObjects/41551_2021_699_MOESM2_ESM.pdf>。

## 参考文献

- [数据源固定版本/入口](https://github.com/dahjan/DMS_opt)
- [归档主文 DOI](https://doi.org/10.1101/617860)
- [最终文章 DOI](https://doi.org/10.1038/s41551-021-00699-9)
- [primary PDF](https://www.biorxiv.org/content/10.1101/617860v2.full.pdf)
- [Final article Supplementary Information](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41551-021-00699-9/MediaObjects/41551_2021_699_MOESM1_ESM.pdf)
- [Final article Reporting Summary](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41551-021-00699-9/MediaObjects/41551_2021_699_MOESM2_ESM.pdf)
- [PDB 1N8Z（条目含原始结构论文）](https://www.rcsb.org/structure/1N8Z)

## 其他

### 完整性与验收

| payload | bytes | SHA-256 |
| --- | --- | --- |
| `DMS_opt/DMS_opt-eec710e5af3a99b2d52e45fc858bc2a9a25b5a62.tar.gz` | 7341985 | `800481476766569b305a9cc40d5b3f54291deb6d87350afde34ffedea97ca8d0` |

原始 payload 合计 7341985 bytes；inventory SHA-256 `69dee603638aafc82655352029b402bbb42386e20f7c792b6c02a1c85ac77a42`（与 PDB 同一算法）。归档成员全部读取；统计与 API/验收报告保存于共享 runs，不作为 raw 附属 manifest 发布。每个文件与论文/PDB 身份均可重验，不执行交付包中的训练代码或模型反序列化。

### 许可和再分发边界

固定 Git tree 没有 LICENSE 文件；README 指向不存在的 LICENSE.md，不能据此发明开源许可证。作者预印本及 Nature 补充的许可分别按实际文件/页面，最终主文未越过付费访问边界。公开分析仓库不等于无限制再分发授权。

### 公开范围对照

| 范围 | 本次证据与状态 |
| --- | --- |
| 已取得的公开部分 | 完整公开 Git tree、合法公开的作者预印本和最终文章补充材料、共享亲本 PDB；最终主文付费，全部大规模原始/分析数据按论文研究用途向作者申请。本次未取得申请部分。 |
| 论文/来源未公开或未取得部分 | 仅按本文具体缺口报告；未访问限制不冒称完成。 |
| processed / release | 未生成；本层仅上游原样输入。 |
