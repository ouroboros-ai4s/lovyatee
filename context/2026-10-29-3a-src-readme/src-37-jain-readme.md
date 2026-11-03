---
tags:
  - context
---

# SRC_R37_JAIN 数据说明

## 数据集身份

- `source_id`：`SRC_R37_JAIN`
- `source_version`：`snapshot-2026-08-17`
- 原作者或发布机构：Tushar Jain 等；Adimab / Sanofi；FLAb 由 Gray Lab 整理

## 实验设计和数据口径

研究从 HEL 发现实验的 334 个近种系人 IgG1 候选中，按高通量可开发性实验选择 41 个多样候选，并加入两条 framework 变体，得到 43 个用于 Tg32 小鼠 PK 和体外表征的抗体。HEL 和鼠溶菌酶结合只是原研究的两个 assay；清除率、半衰期、非特异性、自互作及 pI 均不能当亲和力标签。

亲和力在 Octet HTX BLI 上拟合 1:1 模型；Methods 描述 AHC 捕获 IgG、100 nM 抗原关联 3 分钟、解离 3 分钟。原补充表分别命名 `Octet b-Hen Lysozyme Kd Monovalent (M)` 与 `Octet IgG KD b-Mouse Lysozyme-Fc Avid (M)`，必须保留单价 HEL 和多价 Fc 融合靶点的区别；1:1 拟合本身不能消除 avidity。KD 单位 M，越小越好；FLAb fitness / neg_log_kd 为 -log10(KD/M)，越大越好。

原 XLSX 有 43 个 ADI 抗体 ID 和 43 个 VH/VL 配对。HEL 有 31 个数值与 12 个 `N.B.`；mouse-Lysozyme-Fc 有 2 个数值与 41 个 `N.B.`。原脚注明确 N.B. 是 assay 条件下未观察到结合、无法赋予 KD，不能赋零。FLAb 的 31+2 行只保留数值，两个 mouse 配对也出现在 HEL 表，所以数值表并集为 31 个抗体。按精确 VH/VL 连接全部 33 行，发现 FLAb KD 全部是原 XLSX 数值舍入至一位有效数字；没有一行保留原始精确数值。做精细定量比较时应读原 XLSX，不人为恢复已经丢失的精度。

标签是处理后实验拟合结果，不是从 PK 推导的 KD；raw 层未生成标准化抗体表、未修补缺失或回填非结合标签。抗原序列、Fc fusion 和完整 IgG 并不包含在两张 CSV 中。

## 论文原文

### Jain 主文

- 标题：Assessment and incorporation of in vitro correlates to pharmacokinetic outcomes in antibody developability workflows
- 作者：Jain Tushar；Prinz Bianka；Marker Alexander；Michel Alexander；Reichel Katrin；Czepczor Valerie；Klieber Sylvie；Sun Wei；Kathuria Sagar；Oezguer Bruederle Sevim；Lange Christian；Wahl Lena；Starr Charles；Masiero Alessandro；Avery Lindsay
- 发表来源：mAbs
- 归档文本版本：正式发表版（完整 JATS XML；PDF 端点返回 403）
- 发布日期：2024-07-31
- DOI：10.1080/19420862.2024.2384104
- PMID / PMCID：39083118 / PMC11296533
- 本地文件：`articles/Jain_2024-07-31_mAbs-VoR.xml`
- 文件大小：151.60 KiB（155,237 bytes）
- SHA-256：`030c11c9150c40c16fb84e6ea253a30adcdf2ec4720f6c829a3e3f766cfa41c7`
- 文本许可：CC BY-NC 4.0
- 补充材料：1 个公开原文件，见下表

### SM4152 补充材料

- 标题：Supplemental Information_revised for resubmission.xlsx
- 作者：与主文相同，Jain Tushar；Prinz Bianka；Marker Alexander；Michel Alexander；Reichel Katrin；Czepczor Valerie；Klieber Sylvie；Sun Wei；Kathuria Sagar；Oezguer Bruederle Sevim；Lange Christian；Wahl Lena；Starr Charles；Masiero Alessandro；Avery Lindsay
- 发表来源：mAbs 正式主文的官方附件
- 归档文本版本：原始 XLSX（上游文件名 `KMAB_A_2384104_SM4152.xlsx`）
- 发布日期：2024-07-31（随主文，未标独立发布日期）
- DOI：归属主文 10.1080/19420862.2024.2384104；无独立 DOI
- PMID / PMCID：归属主文 39083118 / PMC11296533；无独立记录
- 本地文件：`articles/Jain_2024-07-31_mAbs-supplement-SM4152.xlsx`
- 文件大小：58.54 KiB（59,940 bytes）
- SHA-256：`716ee160f66cf1c103902221db46f96ed4c57e559ed20ead08653007c693e43a`
- 文本许可：随主文 CC BY-NC 4.0；未声明独立附件许可
- 补充材料：本文件是实验补充数据，无更下层独立附件

## 仓库内容

一手固定 Git tree：[Graylab/FLAb](https://github.com/Graylab/FLAb/tree/e05e3f0135783ffb7de412df6a1467e7a0031911)；commit `e05e3f0135783ffb7de412df6a1467e7a0031911`，tree `98f2b0b97071b0766ec29e168b4e7c0ad7f3595c`。source_version 的日期来自该上游 commit（2026-08-17），不是下载日期。保留来源原始路径的选择性快照，不是整个 repository；所选 blobs 没有 LFS pointer 或 submodule，未保存 .git。

```text
snapshot-2026-08-17/
    FLAb/LICENSE
    FLAb/README.md
    FLAb/data/README.md
    FLAb/data/binding/README.md
    FLAb/data/binding/jain2024assessment_Hen_Lys_kd.csv
    FLAb/data/binding/jain2024assessment_mouse_Ly_kd.csv
    FLAb/data/flab_metadata.json
```

目录树只展示上游 payload。README 和 metadata 说明整理来源，CSV 为按 assay 分组的公开表；项目的论文归档和外部 PDB 补充在独立章节描述。

## 数据结构

### 原始表与连接关系

补充 XLSX 的五张 sheet 均已读取：`Germline and IVIVC` 包含 43 个 ADI ID、assay category、germline/CDR、PK、多种可开发性和两列 KD；第 1–2 行是多层表头，数据从第 3 行开始，末尾有单位和 N.B. 脚注。`Fv Sequence` 的 `mAb name`、`VH`、`VL` 连接 43 个抗体；`Details for pI calculation` 包含恒定区片段和计算口径，不能直接拼成新 raw 完整 IgG；`By VH Family, IVIVC` 是重复的分组/公式层；`Rank Correlations Tg32` 是 assay 级汇总，不是新增抗体。

`Germline and IVIVC` 的 KD 字段保持原始精度和 `N.B.` 表示，FLAb CSV 没有 ADI ID，需要通过两条完整 VH/VL 字符串对应，不能只按一个 CDR 连接。部分 workbook 单元格是公式，应区分公式文本与缓存值。原脚注包含 U+00A0，`Rank Correlations Tg32` 的 `Category of Measure` 后含 U+200B 零宽空格；raw 保留这些字符。

| 文件 | 记录数 | 唯一序列 / VH-VL | 数值范围 |
| --- | --- | --- | --- |
| `jain2024assessment_Hen_Lys_kd.csv` | 31 | 31 | 3e-10 … 5e-07 |
| `jain2024assessment_mouse_Ly_kd.csv` | 2 | 2 | 1e-07 … 4e-07 |

### 字段说明

| 表 | 字段原始拼写 | 类型、单位、方向和来源 |
| --- | --- | --- |
| `jain2024assessment_Hen_Lys_kd.csv` | `heavy` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `jain2024assessment_Hen_Lys_kd.csv` | `light` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `jain2024assessment_Hen_Lys_kd.csv` | `Octet b-Hen Lysozyme Kd Monovalent (M)` | 浮点原文（含科学记数法）；M；实验拟合 KD，较小更好；按文件区分 Fab、IgG apparent 或 mouse-Fc avid |
| `jain2024assessment_Hen_Lys_kd.csv` | `neg_log_kd` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `jain2024assessment_Hen_Lys_kd.csv` | `fitness` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `jain2024assessment_mouse_Ly_kd.csv` | `heavy` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `jain2024assessment_mouse_Ly_kd.csv` | `light` | 字符串；VH/VL 可变区氨基酸；非完整 IgG，无数值单位；序列来自原实验构建体 |
| `jain2024assessment_mouse_Ly_kd.csv` | `Octet IgG KD b-Mouse Lysozyme-Fc Avid (M)` | 浮点原文（含科学记数法）；M；实验拟合 KD，较小更好；按文件区分 Fab、IgG apparent 或 mouse-Fc avid |
| `jain2024assessment_mouse_Ly_kd.csv` | `neg_log_kd` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |
| `jain2024assessment_mouse_Ly_kd.csv` | `fitness` | 浮点原文；无量纲 -log10(KD/M)，较大更好；FLAb 后续派生，不能同时作为输入与目标 |

`FLAb/data/flab_metadata.json` 是整个 FLAb 固定快照的索引，含 165 个文件条目；本版本仅取得其中两张 Jain binding 表。其字段按原始键名分组如下，索引 `size` 的单位为行：

| JSON 层级 | 原始字段名 | 类型、单位、缺失编码及来源 |
| --- | --- | --- |
| 顶层 | `files` | 165 个对象的数组；FLAb 整理的文件索引，无数值单位；本文件中非空 |
| 顶层 | `keys` | 对索引枚举值的对象；含 `assay`、`category`、`doi`、`key_words`、`study`、`year`、`license`、`size` 八个键；FLAb 整理，本文件中非空 |
| `files[]` | `name`、`path` | 原始文件名及相对路径字符串；无数值单位，165 个条目均存在；未取得的其他 FLAb 文件不由此补造 |
| `files[]` | `assay`、`category` | FLAb 整理的测定名称及分类字符串；无数值单位，165 个条目均存在；本研究两张表均标为 `Octet Kd` / `binding` |
| `files[]` | `doi`、`study`、`year` | FLAb 整理的论文链接、标题和发表年；字符串、字符串、整数；无数值单位，165 个条目均存在；其他来源条目可使用字面 `none` |
| `files[]` | `key_words` | 字符串数组，来源主题标签；无数值单位，165 个条目均存在；不作为实验标签 |
| `files[]` | `license` | FLAb 整理的许可字符串；无数值单位，165 个条目均存在；字面 `none` 表示索引未给出许可 |
| `files[]` | `size` | 整数，索引所称记录数（行）；不是文件字节数，165 个条目均存在；具体表行数仍以实际 CSV 为准 |

上述 CSV 全列缺失计数为 0，序列非法字符计数为 0，不含 NB/ND/检测边界字符串或不可见 Unicode。该事实仅针对 CSV；原 XLSX 的失败编码、公式和不可见字符见前文，不能将 CSV 的数值完备性推广到所有实验对象。

### 数据示例

`jain2024assessment_Hen_Lys_kd.csv` 第一条真实记录：

| heavy | light | Octet b-Hen Lysozyme Kd Monovalent (M) | neg_log_kd | fitness |
| --- | --- | --- | --- | --- |
| `EVQLVESGGGLVKPGGSLRLSCAASGFTFSSYSMNWVRQAPGKGLEWVSSISSSSSYIYYADSVKGRFTISRDNAKNSLYLQMNSLRAEDTAVYYCARGTWDYGMDVWGQGTMVTVSS` | `DIQMTQSPSSLSASVGDRVTITCRASQSISSYLNWYQQKPGKAPKLLIYAASSLQSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQEYSTPFTFGGGTKVEIK` | `1e-09` | `9.0` | `9.0` |

一行代表此实验组和 assay 格式的 VH/VL 数值记录；相同序列可在其他组/格式再次出现，并不构成独立抗体。

## PDB 数据库

审计原论文、五张补充 sheets、FLAb 两张 binding 表和 metadata，未发现这些 ADI 抗体的逐行 PDB 键或匹配实验复合物。根据一手实验靶点和 RCSB 条目接受两个靶点代表：1AKI 的 entity 1 / author chain A 是鸡溶菌酶，129 aa，UniProt P00698；1IVM entity 1 / author chain A 是鼠 lysozyme M，130 aa，UniProt P08905，完整 NMR ensemble 有 20 个 models。只按 assay 靶点类别关联 HEL 或 mouse 表，没有已验证的实验 construct 序列，不能声称精确映射，更不能把 1IVM 当成 mouse-lysozyme-Fc 结构。两者都不是这些 ADI 抗体的复合物。全部 entry FASTA 与完整坐标同时保存、canonical entity 序列一致；无逐抗体结构覆盖。

2026-09-18 获取；每个接受锚点的 FASTA 与 mmCIF 均通过 entry ID、canonical polymer entity 序列和 atom_site 验证。PDB 补充按上述参考映射完成；实验变体 / ADI 抗体 / VHH 的逐样本复合物没有取得。

| PDB | 文件 | 大小 | SHA-256 |
| --- | --- | --- | --- |
| 1AKI | `pdb/sequences/rcsb_pdb_1AKI.fasta` | 176 bytes | `7373f54f5b5a78a9d9eb48bf19859614f7ed20bcd77f1003ae8f24cdc1cc982d` |
| 1AKI | `pdb/structures/1AKI.cif` | 152.39 KiB（156,047 bytes） | `16d16e232218abc7ce6352d76126821c23e7a79d88e1fc709368f269c6762f47` |
| 1IVM | `pdb/sequences/rcsb_pdb_1IVM.fasta` | 179 bytes | `ceef4490655d75900c10d4d022d1b354d96c2d25c55e875d8a5cf4ac48575e2d` |
| 1IVM | `pdb/structures/1IVM.cif` | 3.51 MiB（3,679,549 bytes） | `2c36901e72e769ec05aa02bf0b23f3e71920ccdf76e243ae513b497b57615dbb` |

FASTA：`https://www.rcsb.org/fasta/entry/<PDB>/download`；坐标：`https://files.rcsb.org/download/<PDB>.cif`。完整原样保存，不生成衍生序列或独立 PDB manifest。

## 使用方式

调用者赋值 `dataset_root` 为本 source version 目录，原样读取：

```python
import csv
from pathlib import Path
with (Path(dataset_root) / 'FLAb/data/binding/jain2024assessment_Hen_Lys_kd.csv').open(encoding='utf-8', newline='') as handle:
    first = next(csv.DictReader(handle))
print(first)
```

XLSX 需注意多层表头和公式缓存值。

## 采集过程记录

- 2026-09-18 读取 project.toml、developer.local.toml、规则、资源清单及建设计划；context 工具成功。身份 wuhuawei，采用统一共享 storage root。枚举一手固定 Git tree / HF API，生成个人 workspace 中的版本/文件配置，选版本日期来自上游数据。
- 2026-09-18 将 payload 写至 `<source_id>/.staging/snapshot-2026-08-17.partial/`，以 curl 断点恢复；逐文件独立核对字节、Git blob 或 HF LFS SHA-256，保留原文件名与原始数值。下载代码、配置、研究和验收依据保存在个人 workspace。
- 2026-09-18 从 [主文一手入口](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11296533/fullTextXML) 取得全文，核对 DOI / 标题 / 版本；归档后复核 SHA-256。PMC、EuropePMC 和出版社 PDF 端点返回 403；废弃 PDF 路径，归档完整 EuropePMC JATS XML，不伪称 PDF 成功。官方 supplementaryFiles ZIP 全成员 CRC 遍历后仅保留所需 XLSX/DOCX，不发布 ZIP 中的重复正文图片。

| 原文件名 | 归档路径 | 改名依据 |
| --- | --- | --- |
| KMAB_A_2384104_SM4152.xlsx | `articles/Jain_2024-07-31_mAbs-supplement-SM4152.xlsx` | 来源简称、正式发表日期、原补充编号；抽取/改名后字节数与 SHA-256 一致 |

- 2026-09-18 逐表读取全部 CSV / 所有 XLSX sheets，核对记录粒度、序列字符、缺失和数值变换；实际对象身份和原始失败值按原文解释，不做 raw 清洗。检出原 XLSX 的 N.B. 和不可见 Unicode；33 行 FLAb 值全部为一位有效数字舍入，精确原值留在附件。
- 2026-09-18 按一手证据审计 PDB，取得完整 entry FASTA/mmCIF，逐一比对 canonical entities 与完整坐标；不重建每条变体。最初系统 Python 缺少 openpyxl/pypdf/gemmi，改用已有个人 tools 中的隔离依赖，未改系统环境。
- 2026-09-18 生成本地 `workspace/users/<developer.user>/docs/readme/` 工作稿并立即同步本版本 README；执行 skill 的 markdownlint-cli2@0.20.0 至 0 errors，核对本地/共享 README 一致和 source 全文件 inventory，验收通过后原子重命名发布，清理 temporary API/论文缓存和空 staging。批次状态与 handoff 同步；公共总表只准备拟议修改，没有越权修改。

2026-09-22：复核两张 CSV 的原始列名、既有独立审计与 FLAb 索引的十个原始字段；将索引的 `size` 明确为记录数，补齐字段说明，并按最新版合同拆分论文发表来源与归档版本、换算文件大小。公开包及论文所述未交付范围维持既有边界，本地工作稿与共享 README 同步后重新通过 Markdownlint。

## 参考文献

- [固定数据版本](https://github.com/Graylab/FLAb/tree/e05e3f0135783ffb7de412df6a1467e7a0031911)
- [Assessment and incorporation of in vitro correlates to pharmacokinetic outcomes in antibody developability workflows](https://doi.org/10.1080/19420862.2024.2384104)
- [RCSB PDB 1AKI](https://www.rcsb.org/structure/1AKI)；条目中的 primary citation 用于结构引用。
- [RCSB PDB 1IVM](https://www.rcsb.org/structure/1IVM)；条目中的 primary citation 用于结构引用。

## 其他

### 数据范围和限制

本 source 的 payload 只选 FLAb 的两张 binding 表及说明；完整论文的原补充 XLSX 已另行归档，提供被 CSV 省略的 53 个 assay-level N.B. 结果和原始数值精度。R09 有相同整理表，不能重复计入。43 个抗体不是 86 个独立 KD 数值。所有底层传感器曲线、334 个候选的全量记录和逐抗体复合物未获得，不声明 complete-study acquisition。

### 完整性与验收

全部 7 个 payload 文件、139.68 KiB（143,036 bytes）；按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接的 inventory SHA-256：`956aee59357afc3a207900c5fe3b5c7c9d2d49926dde588620d55e506e5b2780`。Git blob / LFS 身份、全表 parser 和数值/序列检查通过；外部论文/PDB 身份见对应章节。

| 上游 payload | 大小 | 本地 SHA-256 |
| --- | --- | --- |
| `FLAb/LICENSE` | 101 bytes | `d0cce20026928c70ed74bb1f4a2e0e0501842859a222c54e85a586501fffe739` |
| `FLAb/README.md` | 4.65 KiB（4,761 bytes） | `5a5184094ed4a13c64b1cb914a2168a58e3b16abe956b794a163888ec70996ff` |
| `FLAb/data/README.md` | 10.68 KiB（10,933 bytes） | `1991c2a8219786efa27e5db2980263469aaf57cb05e3b771cb6911b10dd75523` |
| `FLAb/data/binding/README.md` | 21.60 KiB（22,120 bytes） | `8d46652d19eabc090d3b51f7caa1bf80eca9f46a2ff889226028a938952b8da5` |
| `FLAb/data/binding/jain2024assessment_Hen_Lys_kd.csv` | 8.16 KiB（8,360 bytes） | `982099b57da2cd4951cf987b7fb97586b0e67769b2711ba1f4e664b643bcb363` |
| `FLAb/data/binding/jain2024assessment_mouse_Ly_kd.csv` | 591 bytes | `bd1caa101ff3f25c61d697a8f333c8f307a79c3c9ee855de0bb3335bf2e0920b` |
| `FLAb/data/flab_metadata.json` | 93.92 KiB（96,170 bytes） | `132b54d574ff02ed81de29915249bdaeed1e33805f5189cc4d09c3deb0585fa3` |

### 许可和再分发边界

原论文 permissions 为 CC BY-NC 4.0；FLAb 的 LICENSE 指向逐 dataset 的 data/README.md，其中本研究同样标为 CC BY-NC 4.0。保留原论文的非商业及署名条件，不把 FLAb 汇编论文许可推广为每张表的许可。访问无需申请不等于可无限商业使用或再分发。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| FLAb binding 数值子集 | 31 行 HEL + 2 行 mouse；并集 31 个 VH/VL | 已包含 |
| 原文 43 个抗体的序列、assay 与 PK 补充表 | 五-sheet XLSX，包含 N.B. 和未舍入 KD | 已包含 |
| 334 个发现候选全量表、仪器曲线、逐抗体复合物 | 当前文件未提供 | 未获得 |

## 待解决问题与处理进展

截至 2026-09-22，本次对固定公开 CSV、FLAb 索引、作者补充工作簿与两个靶点参考结构的核验范围内暂无待解决问题。未公开的发现候选全表、仪器曲线和逐抗体复合物仍按“公开范围对照”所列边界处理。
