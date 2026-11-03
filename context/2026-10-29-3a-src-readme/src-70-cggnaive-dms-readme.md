---
- tags:
  - context
---

# SRC_R70_CGGNAIVE_DMS 数据说明

## 数据集身份

- `source_id`：`SRC_R70_CGGNAIVE_DMS`
- `source_version`：`snapshot-2025-02-03`
- 上游数据仓库：`jbloomlab/Ab-CGGnaive_DMS`
- 当前主快照 commit：`5ffc88950f760a297e2196ac449111e3db023e80`
- 当前主快照 Git tree：`01a221fd94dfba5ee351086b6c526d243137db4c`
- 论文关联 improved-Kd 输出 commit：`18e9a93c3e495d58030321322ceccfc635c7b7f2`
- 原作者或发布机构：Tyler N. Starr、Jesse D. Bloom 及合作者；正式论文由 William S.
  DeWitt、Gabriel D. Victora、Frederick A. Matsen IV 等团队共同完成

### 来源方背景

仓库 README 将 DMS 研究归于 Tyler Starr、Jesse Bloom 及合作者，并注明 improved
affinity fitting 由 Jared Galloway 和 William DeWitt 参与重构。正式 Cell 论文的作者
单位包括 University of Washington、Fred Hutchinson Cancer Research Center、The
Rockefeller University、The Scripps Research Institute、University of Utah、Yale
University 和 University of California, Berkeley；Gabriel D. Victora 是 lead contact。
这些身份来自本 source 保存的 Cell 正式全文 XML，不根据仓库用户名推断个人身份。

## 实验设计和数据口径

本 source 是 clone 2.1（仓库命名 `CGGnaive`）抗体的单氨基酸深度突变扫描。实验把
重链和轻链可变区连成 yeast-surface-displayed scFv，建立两个独立 barcode libraries，
用 anti-c-Myc 信号测量 surface expression，用 biotinylated chicken IgY 测量结合。
Tite-Seq 采用 `1e-6` 到 `1e-13` M 加 `0` M 的九个条件，每个条件四个 FACS bins，
再用 barcode counts 拟合 affinity。仓库还保留 Sort-Seq expression、TuGG binding 和
polyspecificity-related 中间字段；这些标签不能合并成同一种 affinity。

论文、构建表和发布表的计数口径不同：

| 层级 | 记录数 | 含义 |
| --- | ---: | --- |
| `CGGnaive_sites.csv` 全 scFv lookup | 235 positions | 112 H + 15 linker + 108 L/boundary |
| 论文 possible V(D)J replacements | 4,161 | 112 H + 107 L positions，各 19 个非亲本 aa |
| `codon_variant_table.csv` 实际构建 | 4,158 | 缺 `I129F`、`I129L`、`S134R` 三个 scFv-position IDs |
| 论文关联 improved-Kd 表 | 4,740 rows | 含 H/L、linker、自身 aa 和上游补齐行 |
| improved-Kd 双标签 replacement | 4,145 | 排除 linker、self、position 235 后，同时有有限 affinity/expression |
| 当前 main final table | 4,800 rows | 当前仓库的旧汇总/展示矩阵，不是论文 4,161-row universe |

`position=235`、`position_IMGT=128`、`chain=L` 的 terminal `R` 位于 Fab 的
variable/constant boundary；仓库 scFv lookup 包含它，论文的 V(D)J replacement 口径不
包含它。排除该位置的 19 个 replacement 后，220-position H/L 矩阵从 4,180 变为 4,161。

当前 main 的 `final_variant_scores.csv` 由 `collapse_scores.Rmd` 补齐每个 scFv position
的 20 个 canonical amino acids，因一个上游补齐循环在 linker position 113、114、115、
121、122 又各生成一组 `wildtype=NA` block，最终成为 4,800 行。文件原样保留，但分析
时不能把 4,800 当成实验单替换数，也不能把 self substitutions 或 linker rows 当成论文
V(D)J replacements。

Cell 配套 `gcreplay` notebook 指向 improved-Kd 输出。该文件后来从 branch tip 删除，
但仍可从历史 commit 和 Git LFS object 恢复。本 source 将其放在 `paper-linked/`，与
current main 的旧表并列保存。历史表中 `bind_CGG` 是 improved model 的 `log10(Ka)`
尺度，`delta_bind_CGG` 是相对 naive parent 的变化；数值越大表示亲和力越强。
`expr` 和 `delta_expr` 是 expression proxy，不是 affinity。

历史表可精确复现论文的 4,145 双标签分母、1,272 个 single-nucleotide accessible
替换、149 个 affinity-enhancing replacement、55 个 single-nt enhancing replacement，
以及最好 `N108(L)R` 和最差 `Y38(H)E`。但是直接按原字段计算
`delta_bind_CGG <= -0.3 or delta_expr <= -0.3` 得到 1,482 个 deleterious，single-nt
子集为 404；论文正文写 1,474 和 400。该 8/4 条差异作为上游最终分类 mask 未公开的
口径问题保留，不修改原表数值。

## 论文原文

- 标题：*Replaying germinal center evolution on a quantified affinity landscape*
- 作者：William S. DeWitt 等
- 期刊：Cell 189(16), 4980–4996.e8
- 在线发表：2026-06-05；纸本期：2026-08-06
- DOI：`10.1016/j.cell.2026.05.013`
- PMID / PMCID：`42248140` / `PMC13360575`
- 文本许可：CC BY 4.0

`articles/` 保存 Europe PMC 正式全文 XML 和官方 supplementary bundle 中的三份原始
成员。PMC XML 的 `self-uri` 指向 `nihms-2177267.pdf`，但本次通过公开 PDF 页面取得的
是 HTML/访问阻断响应，不把该响应伪装成 PDF；正式全文内容由 XML 固定归档。

| 文件 | 精确 bytes | SHA-256 |
| --- | ---: | --- |
| `CGGnaive_2026-06-05_Cell.xml` | 287,208 | `06931052fb887e58ea2d24cf2909d91ddef6b7c605e98b8913c21bd90598f1d9` |
| `CGGnaive_2026-06-05_Cell-supplement-MMC1.pdf` | 17,183,773 | `d57fe061cfd15369a26540fcf5b57abe295787b6646c23ce41d7a1187b22440e` |
| `CGGnaive_2026-06-05_Cell-supplement-MMC2.xlsx` | 18,709 | `d4dbcfc53ff3ea83525f8f77da5246b783124db2cc54d8b1d800a83b5e43579a` |
| `CGGnaive_2026-06-05_Cell-supplement-MMC3.xlsx` | 11,168 | `8b84f7e70a797b715065c2a79531d3dcd42006631a1daa9f0f778a58f6cffdcd` |

MMC1 是补充方法和图；MMC2 包含 selected mutants、affinity ladder、重复 WT 测量和
clonal-burst BLI 表；MMC3 是 strains、donor DNA、sgRNA、primers 等序列材料。这些
小规模 BLI/构建材料与 DMS 逐替换表的记录粒度不同。

## 仓库内容

当前 `main` 固定于 2025-02-03 commit。唯一 tag `v1` 指向 2022-05-12 的更早 commit，
早于 improved-Kd pipeline 合并，因此本 source 不以旧 tag 命名。完整 current-main
payload 有 184 个文件、1,281,641,657 bytes；内容 inventory fingerprint 为
`dbfd37864fc77830452287b60a49412d906eda5e93caff6232808fab04990de1`。九个 Git LFS
pointer 已全部替换为真实对象，合计 1,241,922,322 bytes。

```text
snapshot-2025-02-03/
├── Ab-CGGnaive_DMS/
│   ├── data/
│   ├── exptl_data/
│   ├── results/
│   ├── docs/
│   ├── envs/
│   ├── *.ipynb、*.Rmd、Snakefile、config.yaml
│   └── README.md
├── paper-linked/
│   └── improved-Kd-fitting-18e9a93.../tite-seq-modeling/output/
│       └── final_variant_scores.csv
├── articles/
├── pdb/
│   ├── sequences/
│   └── structures/
└── README.md
```

仓库文件类型包括 97 PNG、21 FCS、14 Markdown、12 CSV、7 notebooks、6 HTML、
5 YML、4 R Markdown、3 YAML、3 PDF，以及 sequence、PDB、GenBank 和运行脚本。
`results/` 有 115 个文件；大表、分析 summary 和派生图均按上游原样保留。

## 数据结构

### 文件组与记录关系

| 文件或目录 | 行数或对象数 | 记录粒度与用途 |
| --- | ---: | --- |
| `data/CGGnaive_sites.csv` | 235 | scFv position 到 H/link/L、IMGT-like site、codon、FWR/CDR annotation 的 lookup |
| `data/PacBio_runs.csv` | 2 | 两个 library 的内部 PacBio path；不是公开 reads |
| `data/barcode_runs.csv` | 184 | TiteSeq 72、TuGG_TiteSeq 64、PSR 40、SortSeq 8 个 sample/run rows |
| `results/variants/codon_variant_table.csv` | 192,429 | barcode 到 codon/aa variant call；两 libraries 合并 |
| `results/counts/variant_counts.csv` | 17,703,468 | `barcode × sample` read counts |
| `results/aggregated_counts/prepped_barcode_counts.csv` | 6,330,016 | filtering/normalization 后的 `barcode × condition × bin` counts |
| `results/aggregated_counts/prepped_variant_counts.csv` | 797,428 | barcode aggregation 后的 `variant × condition × bin` counts |
| `results/binding_Kd/bc_binding.csv` | 192,429 | barcode-level Tite-Seq `log10Ka` fit |
| `results/binding_Kd/variant_binding.csv` | 19,579 | library-level variant binding summary，含 single 和 multi mutants |
| `results/expression_meanF/bc_expression.csv` | 192,429 | barcode-level expression estimate |
| `results/expression_meanF/variant_expression.csv` | 22,624 | library-level variant expression summary |
| current-main `final_variant_scores.csv` | 4,800 | 两 libraries collapse 后的旧 H/L/link 展示矩阵 |
| paper-linked `final_variant_scores.csv` | 4,740 | formal-paper-associated improved-Kd 表；论文亲和力分析优先使用 |
| `exptl_data/.../FCS_scFvpos/*.fcs` | 21 | FCS3.0，FACSAriaII，2021-06-24；共 393,092 events、每文件 9 parameters |
| `data/IgY-CH2_*.pdb` | 1 | 作者仓库中的 refinement-stage PDB，6 chains、4,870 atoms |

`variant_counts.csv` 是 17.7 million 个 count rows，不是 17.7 million 个不同抗体；
同一 barcode/variant 会跨 sample、concentration、bin 和 library 重复。`bc_*` 两表各有
192,429 rows，对应 barcode-level fits；`variant_*` 再按 library 和 variant 汇总。

仓库 README 明确说明 sequencing data 未包含。`PacBio_runs.csv`、`barcode_runs.csv`
的 `subreads`/`R1` 只指向 Fred Hutch 内部文件系统，`config.yaml` 的
`seqdata_source` 是 `HutchServer`。这些路径不是公开下载地址，不能据此声称已取得
PacBio subreads 或 Illumina FASTQ。

### 字段说明

- `site_scFv` 是 1–235 的 construct-linear position；`chain` 为 `H`、`link` 或 `L`；
  `site` 是 chain-local antibody numbering。linker 的 `site`、`KI_codon`、`annotation`
  为 `NA`，不能虚构为 antibody residue。
- `barcode_runs.csv` 的 `sample_type` 区分 `TiteSeq`、`TuGG_TiteSeq`、`PSR`、
  `SortSeq`；`sort_bin` 是 1–4 或空；表内 `concentration` 的编码应结合 `config.yaml`
  和 prepped table 解读，不能仅凭整数值写成摩尔浓度。
- `codon_variant_table.csv` 的 `aa_substitutions` 使用 scFv-linear notation，例如
  `N219R`；`n_aa_substitutions` 为 0、1 或多替换。`variant_call_support` 是 barcode
  variant-call support，不是 affinity score。
- count tables 的 `read_count` 是测序 reads；`estimated_cell_count` 是根据 sort/sample
  normalization 得到的估计 cell count。`barcode` 在 prepped variant table 是 aggregation
  后的 barcode 数量字段，不再是 barcode sequence。
- `variant_class` 区分 `wildtype`、`1 nonsynonymous`、`>1 nonsynonymous` 和 stop；
  `n_bc_*` 是支持 phenotype 的 barcode 数，`n_libs_*` 是有值的 library replicate 数。
- current-main final table 的 `bind_CGG`、`delta_bind_CGG` 是当前上游发布的旧拟合；
  `expr`、`delta_expr` 是 expression。作者 masking 门槛为至少 3 barcodes 且两个 libraries，
  不满足时为空，空值不能补 0。
- paper-linked 表的 `bind_CGG_old` 保留旧 affinity fit，末两列 `bind_CGG` 和
  `delta_bind_CGG` 是 improved fit。论文 affinity 结论应使用末两列；不要因为
  `bind_CGG_old` 数值更大就把它当更强的独立实验。
- paper-linked 表还包含 `bind_TuGG`/`delta_bind_TuGG` 和
  `psr`/`delta_psr`。它们是其他 assay/代理标签，不是 chicken-IgY affinity 的重复值。
- `single_nt` 表示该 amino-acid replacement 是否能由 knock-in codon 的单 nucleotide
  change 达到。它是 mutation accessibility annotation，不是构建成功或测量成功标记。
- `mutation` 使用 chain-local notation，如 `N108(L)R`；同一替换在 barcode/codon 表中
  对应 scFv-linear `N219R`。跨表连接必须使用 `CGGnaive_sites.csv` 转换位置，不能只按
  数字直接 join。

### 数据示例

paper-linked improved-Kd 表的最高 `delta_bind_CGG` row 为：

```text
target=CGG_naive, position=219, position_IMGT=108.0, chain=L,
mutation=N108(L)R, single_nt=False,
bind_CGG=9.532700397435505,
delta_bind_CGG=0.9080090119718216,
expr=10.47079, delta_expr=0.02012,
n_bc_bind_CGG=22.0, n_libs_bind_CGG=2.0
```

它是一条两-library collapsed mutation summary，不是单个 read、单个 FACS event 或一条
BLI trace。current-main 表中同一替换的 `bind_CGG=9.53148`、
`delta_bind_CGG=0.90843`，数值接近但来自不同发布表；训练时必须记录所选表版本。

## PDB 数据库

正式论文报告的 `9ODB` 是 high-affinity `2.1hi` Fab 与 chicken IgY CH2 domain 的
4.0 Å complex，不是 naive clone 2.1，也不是每个 DMS mutant 的结构。RCSB entry 有
三个 polymer entities、两个复合物拷贝形成的六条 coordinate chains、一个 model 和
4,862 atoms：IgY entity（author chains A/D）、Fab heavy（B/H）和 Fab light（C/L）。

| 文件 | 精确 bytes | SHA-256 | 验收 |
| --- | ---: | --- | --- |
| `pdb/sequences/rcsb_pdb_9ODB.fasta` | 1,274 | `ce472a8326baca6c2cabcc666fc347f727b87a206ecdbfd4a1d690ffa2816cd7` | 3 polymer records |
| `pdb/structures/9ODB.cif` | 650,716 | `3fa2140f19a75303dbcfbec7fa308b49d6f23d4285158fa0bb22a1e7bf3693dd` | mmCIF 完整解析，1 model、4,862 atoms |

`2.1hi` heavy variable region 相对 naive parent 有 D27A、K44R、S56G 三个
chain-continuous 替换，对应论文 antibody numbering D28A、K49R、S64G；light 有
A34G、Y36F、A46S、Q89H、N92Y，对应 A40G、Y42F、A52S、Q105H、N108Y。合计八个
替换，因此不得把 `9ODB` 复制给全部 DMS rows 或标成 naive reference complex。

作者仓库还原样包含 `data/IgY-CH2_EH2_final_real_space_refined_021.pdb`，为 390,593
bytes、SHA-256 `111a3b908eb719271daa8324ffedf85e855152605320fa1939bb2d0ec4025e93`，
解析为六 chains、4,870 atoms。它是上游 refinement-stage PDB；`pdb/` 下的 FASTA/mmCIF
才是本项目外部 PDB 子任务固定的 RCSB 正式 entry，两层对象不互相覆盖。

## 采集过程记录

- 2026-09-26：核验 Git branches、tag、current main commit/tree；选择论文方法链接所用
  current-main 不可变 commit，而不是 2022 年旧 `v1` tag。
- 2026-09-26：下载 codeload archive，验证 25,545,399 bytes 和 SHA-256
  `483331fe41097fee297b368fdc14ea1360ed60406fae4e4d7f481dfb50bd8866`；安全展开
  184-file tree，无 symlink/submodule。
- 2026-09-26：逐个解析并验证 9 个 Git LFS pointers，断点取得真实 payload；每个对象
  在替换 staging pointer 前通过 pointer-declared bytes 和 SHA-256。
- 2026-09-26：从 Europe PMC 固定正式全文 XML 与 supplementary bundle；bundle 为
  20,223,210 bytes、SHA-256 `c62e4d329fd6cf38b1654f479a7786d720b58892b848e8bd854f7453f7a3cfc1`，
  ZIP CRC 通过后只发布 MMC1–MMC3 官方成员。
- 2026-09-26：从 RCSB 固定 `9ODB` FASTA/mmCIF；验证 entry identity、polymer records、
  coordinate parse 和 2.1hi–naive sequence relationship。
- 2026-09-26（`R01` 结案）：追踪 Cell 配套 `gcreplay` notebook 后发现论文使用的 improved-Kd table
  已从 branch tip 删除；从历史 commit `18e9a93...` 按 Git LFS oid 恢复 805,752-byte
  原文件，验证 4,145 双标签分母并与 current-main 表分层保存。
- 2026-09-26：README 同步 staging 后运行独立 validator；全部门槛通过才以同文件系统
  原子 `mv` 发布，并在正式目录重复同一验收。cache、下载归档和 validation JSON 不进入
  source version。

## 参考文献

- Cell 正式论文：<https://doi.org/10.1016/j.cell.2026.05.013>
- Europe PMC：<https://europepmc.org/article/PMC/PMC13360575>
- 作者固定 current-main commit：<https://github.com/jbloomlab/Ab-CGGnaive_DMS/tree/5ffc88950f760a297e2196ac449111e3db023e80>
- improved-Kd 历史 commit：<https://github.com/jbloomlab/Ab-CGGnaive_DMS/tree/18e9a93c3e495d58030321322ceccfc635c7b7f2>
- 论文全研究仓库：<https://github.com/matsengrp/gcreplay>
- RCSB `9ODB`：<https://www.rcsb.org/structure/9ODB>

## 其他

### 数据范围和限制

本次达到 `verified public-package onboarding`：current-main 固定仓库、九个 hydrated Git
LFS objects、论文关联 improved-Kd table、正式全文 XML、三份补充和 `9ODB` FASTA/mmCIF
均已取得并验收。现有 processed package 已包含论文口径的 affinity、expression、barcode/
variant counts 和中间拟合结果，足以支持基于这些公开处理后标签的 AI 建模；未取得的底层
reads 不把公开包接入降级为未完成。它们对完整研究获取和端到端重处理的影响统一由文末
`Q01` 跟踪，本 source 不据此宣称 `complete-study acquisition` 已完成。

21 个 FCS 是仓库 `FCS_scFvpos` 实验对象，不等于全量 sequencing reads 或每个 sorted
library/bin 的完整 event-level archive。FCS events、barcode reads、barcode-level fits、
variant-level fits、collapsed summary 和 BLI supplement 是不同层级，不能直接加总样本量。

### 完整性与验收

独立 validator 校验 source-root allowlist、README contract、184-file repository content
fingerprint、九个 LFS hashes、12 张 CSV 的 header/行数、4,161/4,158/4,145 口径、current
main linker artifact、historical improved-Kd identity、21 个 FCS metadata、四个 article
objects、两张 XLSX CRC、`9ODB` 双层文件与结构/序列关系。source 内无 symlink、
`.partial`、未 hydration 的 LFS pointer、cache 或独立 validation report。

### 许可和再分发边界

Cell 正式全文明确采用 CC BY 4.0。`Ab-CGGnaive_DMS` 仓库没有 `LICENSE`/`COPYING`，
GitHub API 也没有识别到 license；论文文本许可不能自动推广到 repository data/code 或
历史 Git LFS payload。公开访问不等于已经取得明确的商业再分发授权。对外再分发、商业
使用或衍生发布前仍需向作者确认仓库对象的授权范围。RCSB 和第三方引用材料分别遵守其
来源条款，本 README 不替代原始权利声明。

### 与论文全研究仓库的边界

`matsengrp/gcreplay` 包含 Cell 全研究的 germinal-center lineages、10x、BLI、phylogeny、
fitness 和 animal-study analyses。R70 只接入 clone 2.1 DMS source；仅额外恢复该仓库
明确引用的 improved-Kd final table，不把 `gcreplay` 其余数据混入 R70，也不据此声称
完整 Cell 研究已取得。

## 待解决问题与处理进展

| ID | 状态 | 最近更新 | 问题、影响与后续触发条件 |
| --- | --- | --- | --- |
| Q01 | open | 2026-09-26 | 原始 PacBio/Illumina reads 只有 Hutch 内部绝对路径，未找到公开 accession。该缺口不影响使用现有 processed affinity/expression 标签开展 AI 建模，也不阻塞 `verified public-package onboarding`；它只限制从测序 reads 开始重新执行 barcode/variant calling、counting 和拟合，因此 `complete-study acquisition` 保持 `partial`。出现作者仓库更新、SRA/ENA accession 或作者交付时补采。 |
| Q02 | open | 2026-09-26 | Git 仓库数据/代码没有独立许可。当前不阻塞本地研究接入；对外再分发或商业使用前需作者或正式条款确认。 |
| Q03 | open | 2026-09-26 | historical improved-Kd 原字段重算 deleterious 为 1,482/404，论文写 1,474/400；差异不影响 4,145 分母和 extrema，但分类复现需论文最终 mask 或作者说明。 |
| Q04 | open | 2026-09-26 | PMC XML 声明的主文 PDF self-uri 当前未提供可验证 PDF bytes；正式全文 XML 已完整归档。若 PMC/Cell 提供稳定 PDF endpoint，再按同版 DOI/PMCID、bytes、hash 补入。 |
