---
- tags:
  - context
---

# SRC_R42_MAGMA_SEQ 数据说明

## 数据集身份

- `source_id`：`SRC_R42_MAGMA_SEQ`
- `source_version`：`snapshot-2024-06-10`
- 原作者或发布机构：Brian M. Petersen、Monica B. Kirby 等；Timothy A. Whitehead 课题组

## 实验设计和数据口径

MAGMA-seq 将配对重轻链 Fab 变体库、分子 barcode 与抗原筛选关联，酵母展示在多个抗原浓度和流式 bin 下分选；barcode 测序计数及分选参数输入 maximum likelihood estimation，得到单价 Kd、Fmax 与置信区间。论文报告两个 pooled libraries、多个亲本和 SARS-CoV-2 S1/流感 HA 系统，NA 亲本也用作跨靶点不结合对照。标签是实验支持的拟合生物物理参数，非逐变体低通量 SPR 实测。

仓库快照主要是方法代码、sample sequencing files、示例 scan counts 与三张流式事件表，真正结果还在 Supplementary Data 4（supplement6.xlsx）。该文件五个结果 sheet 分别有 858 条 barcode/153 唯一 Variant、153 条汇总 Variant、514 条 barcode/377 唯一 Variant、712 条 barcode/492 唯一 Variant、1,815 条 replicate-2 Variant。前三种记录层级及 replicate 不能相加成独立抗体；同一 Variant 可能出现于多个 barcode、sheet 和图表派生文件。多个 sheet 的 Excel max_row=1,000 主要是尾部空行，不能视为 999 个实验样本。

Kd 使用 nM，越低结合越强；Fmax 是饱和荧光/功能表达相关量，不能当亲和力标签。结果含 Success=False、Kd 到达 0.01/20,000 求解边界、Fmax 到达 5,000/90,000 边界；CI 列存在零及不满足简单有序区间的原始表示，应结合上游算法判断，raw 不静默修正。模型 regression coefficients、DDG、ddg/dg 是派生量，不是新增实验测量。R44 明确复用本研究的 4A8/CC12.1 结果，合并时需按来源/亲本/变体/assay 去重。原始 reads PRJNA1026152 本批未下载。

## 论文原文

- 标题：An integrated technology for quantitative wide mutational scanning of human antibody Fab libraries
- 作者：Brian M. Petersen, Monica B. Kirby et al.
- 载体与版本：Nature Communications 15, 3974，正式期刊全文
- 发布日期：2024-05-10
- DOI：`10.1038/s41467-024-48072-z`
- PMID / PMCID：38730230 / PMC11087541
- 本地文件：`articles/MAGMAseq_2024-05-10_NatureCommunications-v1.pdf`；`articles/MAGMAseq_2024-05-10_NatureCommunications-v1.xml`
- 文件大小：articles/MAGMAseq_2024-05-10_NatureCommunications-v1.pdf = 4568177 bytes；articles/MAGMAseq_2024-05-10_NatureCommunications-v1.xml = 186436 bytes
- SHA-256：articles/MAGMAseq_2024-05-10_NatureCommunications-v1.pdf = `8a02593a788e0161fa7c34289297b764c823032e1d559bef24ad7ee703c7cc56`；articles/MAGMAseq_2024-05-10_NatureCommunications-v1.xml = `a9f8ee1e9e9cf6096328e5f57b3e77e5da302792e8aba7eab17adb372958f480`
- 文本许可：CC BY 4.0
- 补充材料：9 个公开附件，详见下表

| 文件 | 角色 | bytes | SHA-256 |
| --- | --- | --- | --- |
| articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement1.pdf | 出版方补充对象 1 | 3755985 | `6d3612e2cd2d2553133ada4ec01960298dbaf2d4f73fd4f6dd497f2f5e4c170a` |
| articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement2.pdf | 出版方补充对象 2 | 141137 | `147445a6d80c7269aeecb9a06840500709db67447a60f9378a3aeeea3143d1cd` |
| articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement3.xlsx | 出版方补充对象 3 | 123599 | `b1a194f5b59c2e5c512810498853b96199e5740131e8d704a55ea5c25b77e322` |
| articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement4.xlsx | 出版方补充对象 4 | 32602 | `9753a02e6970f9f2d8cebfb90e83c346372d89ba04f4065ba3134453aa9b2266` |
| articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement5.xlsx | 出版方补充对象 5 | 94350 | `4c5b946ac6935a94120d8abd08b328766dda6240f418b09aa9eff8b112e9fdcb` |
| articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement6.xlsx | 出版方补充对象 6 | 599076 | `0d311671462bc61a4103e214cd1e272e8b159e40f516e21bd292817d366bc8e3` |
| articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement7.pdf | 出版方补充对象 7 | 2930346 | `bae3f9a87ea38628c3135fd281cc72f2843cfc592f08fe2c07f62a73af8876bc` |
| articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement8.pdf | 出版方补充对象 8 | 3696892 | `2f74158adbaa25401694850103dee27f624215ec5d4aa216a50366d3f9e83962` |
| articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement9.xlsx | 出版方补充对象 9 | 285231 | `94834b66d231f92983b4a918f061c416109417eac9e6bbdb064e4022b3cf16a9` |

归档主文 PDF 和同 DOI 完整 XML，以及出版方列出的全部九个对象：补充说明、reporting/peer-review/transparent-review 文件、五个 XLSX。supplement3–6 分别为 Supplementary Data 1–4，supplement9 为 Source Data；包含研究用结果及可复核图表数据，不代表底层全部 NGS reads。

## 仓库内容

上游固定版本：[一手入口](https://github.com/WhiteheadGroup/MAGMA-seq/tree/e2c923c4d5bc47fbddf07bd19823b38d74cc3ed9)。revision/commit `e2c923c4d5bc47fbddf07bd19823b38d74cc3ed9`，上游版本日期 `2024-06-10T18:27:57Z`；据此命名 `snapshot-2024-06-10`，日期不是本次下载日期。

完整固定 commit 的 codeload tar.gz 快照；78 个 blob、5,569,704 uncompressed bytes。独立比对全部 Git blob SHA-1，未发现 LFS pointer、submodule、链接或安全路径异常；归档保留，不重复解包。

```text
snapshot-2024-06-10/
└── MAGMA-seq/
    └── MAGMA-seq-e2c923c4d5bc47fbddf07bd19823b38d74cc3ed9.tar.gz
```

归档内有 MLE/、WT/、examples/、limits/、notebooks/、figures/、主分析脚本和说明。上游 source tree 不包含论文全部定量结果；这些结果由独立出版方 supplement6.xlsx 交付，归档于论文附件区。

## 数据结构

### 代码仓库表格

全部 8 张 CSV 已读取：三张 MLE/sigma 流式事件表共 27,889 行；WT/wt.csv 与 examples/example_wts.csv 各 4 行；examples/limit.csv 5 行、limits/limit.csv 20 行、examples/scan_output.csv 3,035 行。流式事件、barcode/count 条件和示例序列各有不同 schema，不能把所有行当实验亲和力样本。WT 的 seq 是核酸序列；examples/example_wts.csv 是示例参数，不是统一完整抗体 AA 表。

### 论文补充结果

全部五个 XLSX 的所有 sheet 均已打开。Supplementary Data 1（supplement3）包含 README/Plasmids/Libraries/Primers；Data 2（supplement4）Sheet1 为 isogenic/突变结果，存在多行和多区域表头；Data 3（supplement5）为 LASSO regression；Data 4（supplement6）含 README 和五个 barcode/variant 结果 sheets；Source Data（supplement9）有各主图和补图对应 sheets、heterogeneous header。不能对这些图表 sheets 使用单一统一表头。Data 4 五个结果 sheet 的有效 Variant 行与唯一 Variant 数见实验口径；Barcode、Variant、Ab 是连接键。未在 raw 中展开突变字符串或拼接完整序列。

Source Data Figure 1c 的 header（例如 Constant Light、YSD Measured 周围）和部分正文单元格带原始 U+00A0 非断行空格，实查包括 header 后第 5 行 Epitope=`Spike RBD\u00a0`、第 10 行 IGHV 字段前导 U+00A0。另有多行表头及 Excel 日期类型单元格；这些字面表示保留，不在 raw 接入中清洗。

### 字段说明

| 文件或表 | 原始字段 | 类型/单位/方向 | 缺失、边界及来源 |
| --- | --- | --- | --- |
| MLE/sigma 三表 | TIME / FSC-A / FSC-H / FSC-W / BSC-A / FITC-A-Compensated / PE-A-Compensated / Cy5-A-Compensated / Index | 事件级数值/仪器单位 | 实验流式事件；不是一行一个 Fab 的 KD |
| WT 与 example_wts | gene / vh_or_vl / seq / amplen / barcode_start / barcode_end / gene_start / gene_end / encoded_positions | 基因/链标识、核酸串及索引 | 空 encoded_positions 表示未指定；上游说明核酸位置 0-index、蛋白位置 1-index；示例参数非标签 |
| limit/scan_output | Variant / Rjk / Concentration / Bin / Hj / Gj / Nk / Njk / ref_variant / ref_total / Rijk | 变体、reads、浓度 nM、bin 及门限 | counts/条件输入；limit 表没有 Variant；Concentration 示例可含 0nM 字符串 |
| Data 4 结果 sheets | Barcode / Variant / Ab | barcode、复合突变字符串、亲本名称 | barcode sheet 与 collapsed sheet 不同粒度；Variant 含 VH/VL 信息和同义核酸变化，不是完整 AA 序列 |
| Data 4 结果 sheets | Kd / Fmax / Success | nM 越低越好；RFU；bool | 实验 MLE 拟合；Success=False 与求解边界须单独处理，不把 20,000 当精确弱结合 KD |
| Data 4 结果 sheets | 95% CI low / 95% CI high / LL / X^2_red_min / Avg_counts / n | nM CI、likelihood、拟合诊断、平均 reads、条件数 | 原值含零及异常 CI 表示；不同版本诊断字段并不保证相同，不以零 CI 填零 KD |
| Data 4/Source Data | Rijk / Concentrations / sorted fractions / ER | 列表的原字符串 | barcode reads、nM 浓度、分选比例或派生量；不在 raw 中重新序列化 |
| Data 3/4/Source Data | Coefficient weight / DDG (kcal/mol) / ddg / dg | 回归系数或上游计算量 | 模型/派生字段；部分单位由各 sheet/算法说明决定，不可统一视为新的实测标签 |

### 数据示例

来自 `articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement6.xlsx#4A8_CC121_combined` 的第一条真实记录（仅摘录下列列）：

```json
{
  "Variant": "4A8>VH:A9A-GCC;V20V-GTG;M59I-ATC;T98T-ACA;Q120K-AAA|4A8>VL:S7T-ACT;T94M-ATG;P100P-CCT;V109L-CTG",
  "Kd": 102.43,
  "Fmax": 18346.45,
  "Success": true,
  "95% CI low": 161.45,
  "95% CI high": 161.45
}
```

这里是一条 collapsed Variant 的 MLE 汇总；同一变体在 barcode sheet 可有多行，Source Data 中还可能再次出现。

## PDB 数据库

审计主文、补充说明、仓库及实际表字段；主文明确 7C2L/6XC3/3GBN/7T3D，另外按研究亲本 2-7 与 RCSB 条目名接受 7LSS。五个条目是共享亲本参考，不是每个变体的实测复合物。未提供逐 row 的 PDB 键；参考连接由 Ab 或 Variant 亲本名称完成，不以匹配亲本名声称所有变体严格序列一致。

取得日期：2026-09-18。每个唯一 entry 保留完整 RCSB canonical entity FASTA 与完整沉积坐标，不选择性截断、不拼接设计序列。实体/链从 mmCIF `_entity` / `_entity_poly` 核对；canonical 序列与 FASTA entity 一致，坐标 `_entry.id` 与 PDB ID 一致，原子记录非空。

| PDB | 连接关系及证据 | polymer entity / author chains /长度 | FASTA/mmCIF |
| --- | --- | --- | --- |
| 7C2L | 4A8 共享亲本参考；主文 Fig. 3f | 1:A,B,C:1283aa；2:H,I,J:458aa；3:L,M,N:219aa | 两层 verified |
| 6XC3 | CC12.1 共享亲本参考；主文 Fig. 3g | 1:H:222aa；2:L:221aa；3:A:217aa；4:B:220aa；5:C:231aa | 两层 verified |
| 3GBN | CR6261 与 H1 共享亲本参考；主文 Fig. 4d | 1:A:331aa；2:B:179aa；3:H:226aa；4:L:221aa | 两层 verified |
| 7T3D | 222-1C06 与 H1 共享亲本参考；主文 Fig. 5b | 1:A,E,F:331aa；2:B,G,I:174aa；3:D,M,N:107aa；4:C,J,K:120aa；5:H,O,P:122aa；6:L,Q,R:108aa | 两层 verified |
| 7LSS | 2-7 共享亲本参考；主文 Fig. 4a 亲本名称 + RCSB 条目中 Fab 2-7 名称 | 1:A,B,C:1288aa；2:L:108aa；3:H:119aa | 两层 verified |

| 文件 | bytes | SHA-256 |
| --- | --- | --- |
| pdb/sequences/rcsb_pdb_7C2L.fasta | 2235 | `cd046ce4f10a78aba207e9604dc61f6fe6a5228a9bdfc9ee706947fff5cd1864` |
| pdb/structures/7C2L.cif | 4201655 | `3ecd808e0ee9c1e752de9a59c4a70bbb241b655be8ac64ee74354da272cbabd9` |
| pdb/sequences/rcsb_pdb_6XC3.fasta | 1467 | `bc7fb89cebb951769e7aaef2cbce5d6e4e1266de98fc775787456b165231f63b` |
| pdb/structures/6XC3.cif | 915233 | `24b820c5935e1ea7b2186d92ea5298e074e376cb6014a4d012be77d751ddc054` |
| pdb/sequences/rcsb_pdb_3GBN.fasta | 1264 | `69e686f7933b2e04e3d94f75a6aa875a7ed01a96f062107b9352c2732b3f21fc` |
| pdb/structures/3GBN.cif.gz | 193315 | `1599b5fe02692d655bc79afdab02c218a66605005b626c08e262587c1cfb8f6d` |
| pdb/sequences/rcsb_pdb_7T3D.fasta | 1550 | `6a41e9ecb7b9dc69fafb0b3adfc6986c8d34ebcf5b3493fc0bffd04615e0137b` |
| pdb/structures/7T3D.cif.gz | 563335 | `5eb893fa63f7e23d01ecee12aa4d1b8bdf4083638cd7d4ffba872de8b2c57933` |
| pdb/sequences/rcsb_pdb_7LSS.fasta | 1764 | `2dd4e4c1bcff6dccf2dc0dec5bd78dcc49b141e95a6b6d1eed8a51e11f59528b` |
| pdb/structures/7LSS.cif | 2362843 | `346b59b01454f8f76cb76e311c9e2b5351119476072ebb704816c75e4fd86b42` |

共 5 个有效锚点、5 个 FASTA、5 个 mmCIF，8244661 bytes。每个下载使用 `https://www.rcsb.org/fasta/entry/<PDB_ID>/download` 与 `https://files.rcsb.org/download/<PDB_ID>.cif`；共享已存 gzip 坐标直接原样复用，未重压缩。完整 entry 可含未参与该研究的抗体/实体；链身份与映射边界按上表及下文使用。

7C2L：spike A/B/C、4A8 heavy H/I/J、light L/M/N；6XC3：CC12.1 heavy B、light A、RBD C，另外 CR3022 heavy H/light L 是同条目其他抗体；3GBN：HA A/B、CR6261 heavy H/light L；7T3D：222-1C06 heavy H/O/P、light L/Q/R，另有 2B05 C/J/K/D/M/N；7LSS：2-7 heavy H/light L、spike A/B/C。链对应均由 deposited entity 描述验证；这些实验结构的靶点株及 construct 不能当所有表格测量的严格映射。其他亲本未建立已接受复合物连接，覆盖范围限于上述五个共享参考。

## 使用方式

```python
from pathlib import Path
import openpyxl
root = Path(dataset_root)
book = openpyxl.load_workbook(
    root / 'articles' / 'MAGMAseq_2024-05-10_NatureCommunications-v1-supplement6.xlsx',
    read_only=True, data_only=False)
rows = book['4A8_CC121_combined'].iter_rows(values_only=True)
header = next(rows)
```

有效记录以 Variant 非空识别；其他 supplement/Source Data 含不同表头，不套用此入口。

## 采集过程记录

2026-09-18：解析作者 main 的 commit，再通过不可变 tree 枚举 78 个 blob；仓库日期 2024-06-10 用于 source version。小归档下载 staging，完整遍历与官方 tree 比对成功，归档原样保留。

2026-09-18：发布方主文/完整 XML DOI 核验通过；第一次补充 7/8/9 出现 TLS EOF/超时，第二轮重试全部九个对象取得。全部 CSV 和全部 XLSX sheet 实际检查，修正用 max_row 代表生物样本数的错误假设；区分 barcode/variant/regression/事件层。

2026-09-18：PDB metadata 初次 loop 访问方式错误触发 TypeError；改为按 entity_poly loop 读取 author chain，已有原始字节无需重写。五个唯一锚点两层重新验收通过。

2026-09-18：论文/补充的下载身份和通用名修正留痕如下；原始文件与描述性落盘名对应的 bytes/SHA-256 均已核对，重命名没有改写内容。

| 下载一手 URL | 原始名 | 落盘路径 | bytes |
| --- | --- | --- | --- |
| <https://www.nature.com/articles/s41467-024-48072-z.pdf> | s41467-024-48072-z.pdf | articles/MAGMAseq_2024-05-10_NatureCommunications-v1.pdf | 4568177 |
| <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11087541/fullTextXML> | fullTextXML | articles/MAGMAseq_2024-05-10_NatureCommunications-v1.xml | 186436 |
| <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-024-48072-z/MediaObjects/41467_2024_48072_MOESM1_ESM.pdf> | 41467_2024_48072_MOESM1_ESM.pdf | articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement1.pdf | 3755985 |
| <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-024-48072-z/MediaObjects/41467_2024_48072_MOESM2_ESM.pdf> | 41467_2024_48072_MOESM2_ESM.pdf | articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement2.pdf | 141137 |
| <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-024-48072-z/MediaObjects/41467_2024_48072_MOESM3_ESM.xlsx> | 41467_2024_48072_MOESM3_ESM.xlsx | articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement3.xlsx | 123599 |
| <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-024-48072-z/MediaObjects/41467_2024_48072_MOESM4_ESM.xlsx> | 41467_2024_48072_MOESM4_ESM.xlsx | articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement4.xlsx | 32602 |
| <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-024-48072-z/MediaObjects/41467_2024_48072_MOESM5_ESM.xlsx> | 41467_2024_48072_MOESM5_ESM.xlsx | articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement5.xlsx | 94350 |
| <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-024-48072-z/MediaObjects/41467_2024_48072_MOESM6_ESM.xlsx> | 41467_2024_48072_MOESM6_ESM.xlsx | articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement6.xlsx | 599076 |
| <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-024-48072-z/MediaObjects/41467_2024_48072_MOESM7_ESM.pdf> | 41467_2024_48072_MOESM7_ESM.pdf | articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement7.pdf | 2930346 |
| <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-024-48072-z/MediaObjects/41467_2024_48072_MOESM8_ESM.pdf> | 41467_2024_48072_MOESM8_ESM.pdf | articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement8.pdf | 3696892 |
| <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-024-48072-z/MediaObjects/41467_2024_48072_MOESM9_ESM.xlsx> | 41467_2024_48072_MOESM9_ESM.xlsx | articles/MAGMAseq_2024-05-10_NatureCommunications-v1-supplement9.xlsx | 285231 |

2026-09-18：本地 README 编辑后立即同步共享 staging，固定 markdownlint-cli2 0.20.0 按 skill 配置检查。发布、残留清理和当前缺口同步到本批交接；source version 不另发布 manifest、API 响应或审计文件。完整研究 acquisition 与本次公开包接入分开记录。

## 参考文献

- [固定上游数据版本](https://github.com/WhiteheadGroup/MAGMA-seq/tree/e2c923c4d5bc47fbddf07bd19823b38d74cc3ed9)
- [主论文 DOI](https://doi.org/10.1038/s41467-024-48072-z)
- [论文与全部补充对象](https://www.nature.com/articles/s41467-024-48072-z)
- [原始测序 BioProject，未下载](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1026152)
- [R44 论文，数据复用关系](https://doi.org/10.1073/pnas.2412787122)
- [PDB 7C2L 及其原始结构论文](https://www.rcsb.org/structure/7C2L)
- [PDB 6XC3 及其原始结构论文](https://www.rcsb.org/structure/6XC3)
- [PDB 3GBN 及其原始结构论文](https://www.rcsb.org/structure/3GBN)
- [PDB 7T3D 及其原始结构论文](https://www.rcsb.org/structure/7T3D)
- [PDB 7LSS 及其原始结构论文](https://www.rcsb.org/structure/7LSS)

## 其他

### 完整性与验收

公开 payload 1 个文件、3541288 bytes；完整 Git archive/tree 验证 blob 数 78。文件 inventory 按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接的 SHA-256：`9b1899c22e2818ac1b6ac65762e907f2a43f6a6f9aa15011c20e9c32d6d7451e`。Git blob/LFS 官方身份分别验证；此 inventory 是项目本地摘要，不冒称上游官方 checksum。

固定仓库及出版方全部九个补充对象已独立验收；五个已接受 PDB 两层完成。公开处理包接入完成；原始测序 reads 未取得，因此 complete-study acquisition 保持未完成。

### 许可和再分发边界

作者仓库标 MIT，保存其 LICENSE；论文及按正文声明覆盖的出版方附件为 CC BY 4.0，保留原作者引用与第三方内容标记。MIT 软件声明不自动替代论文实验数据条款；数据使用引用论文及原附件来源，外部 PDB 保留结构论文。

### 公开范围对照

| 论文或来源所指内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| MAGMA-seq 方法代码/示例 | 78 个 Git blob 固定快照 | 已包含 |
| 定量结果与 barcode/Variant 连接 | Data 4 的五个结果 sheets；Data 1–3 和 Source Data | 已包含公开处理范围 |
| 仪器事件/原始 reads | 仓库三张流式表与样例；PRJNA1026152 未下载 | 部分包含，非完整底层数据 |
| 逐变体实测复合物 | 五个共享亲本参考条目 | 未包含逐变体实验结构 |
