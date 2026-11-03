# SRC_R47_ROSACE 数据说明

## 数据集身份

- `source_id`：`SRC_R47_ROSACE`
- `source_version`：`snapshot-2023-04-06`
- 原作者或发布机构：Angelo Rosace 等、Pietro Sormanni 课题组及共同作者；Springer Nature 发布原始附件，FLAb 提供后续整理表

## 实验设计和数据口径

论文研究计算筛选对抗体/蛋白溶解性和构象稳定性的影响，并检查抗原结合是否保留。六个抗体亲本是 Nb.B201（HSA）、Adalimumab/Golimumab（TNFα）、CR3022/H11-D4/H11-H4（冠状病毒 RBD）。42 个设计加 6 个 WT 共 48 个亲本内表征对象，不等于 48 个独立亲本。模型/稳定性 benchmark 和抗体实验不能混成同一 binding 数据池。

补充 Table S1 给出含连接肽/标签的 WT scFv/VHH construct；FLAb heavy/light 是分离可变区，不能当完整表达构建体。抗原结合使用 BLI 1:1 拟合，补充 Table S5 包含 KD(M)、动力学/误差/R²；FLAb 的通用 SPR 注释不能覆盖原方法。结合 KD 较低通常较强，部分极慢解离导致拟合不稳定，H11-H4 三突变缺失，不能把最小数值当已证实最佳结合。Figure S9 的 ±3 倍区间是论文采用的判定范围，不是每点测量置信区间。

Source Data `Fig S9` 有 48 个 KD 位置，47 有限，C37 为字符串 `nan`，未改零。**单位冲突：** 表头是 `KD (nM)`，但 C3 字面值 `1.2999999999999999E-10` 与 Supplementary Table S5 的 WT Adalimumab `1.3E-10 M` 一致，实际数值采用 M 尺度。`KD Error (nM)` 同样不能仅凭表头盲目换算；原工作簿按字节保留，后续使用需显式依据原表处理。

FLAb binding 仅 Adalimumab 14 行和 Golimumab 5 行；CIC rep1/rep2 各 19 行，Tm rep1 19 行，总计 8 CSV/76 行，实际共享同 19 种设计。CIC 保留时间 min 通常较低表示较低多反应性，Tm °C 较高表示较高热稳定性，二者不是 KD。M 单位的 -log10(KD) 与 fitness=-log10(KD[nM]) 相差 9，不可当同一列或让其预测原 KD。训练划分应按亲本/序列检查重复，并检查与 FLAb/R09 和蛋白 benchmark 的重合。

公开包为实验/计算汇总和绘图 Source Data，不是全部仪器事件或原始 sensorgram。稳定性表的逆向记录和复测不构成新增独立生物对象；本次不做合并、去重、单位换算或标签变换。

## 论文原文

### 主文

- 标题：Automated optimisation of solubility and conformational stability of antibodies and proteins
- 作者：Angelo Rosace, Anja Bennett, Marc Oeller, Mie M. Mortensen, Laila Sakhnini, Nikolai Lorenzen, Christian Poulsen, Pietro Sormanni
- 载体与版本：Nature Communications 14, 1937 (2023)，Version of Record
- 发布日期：2023-04-06
- DOI：[10.1038/s41467-023-37668-6](https://doi.org/10.1038/s41467-023-37668-6)（所附主论文 DOI）
- PMID / PMCID：37024501 / PMC10079162
- 本地文件：`articles/Rosace_2023-04-06_NatureCommunications.pdf`
- 文件大小：2,067,869 bytes；15 页
- SHA-256：`d566a17e666f1183e3562a1c2deb51269163410ade23dda39c7bed2d715ecfc5`
- 文本许可：CC BY 4.0；第三方材料例外以原 credit line 为准
- 补充材料：已取得 13 个独立 PDF 补充对象；数据工作簿/归档见数据结构。publisher 15 个补充对象全部取得（13 PDF、2 XLSX）。

### Supplement-MOESM10

- 标题：Automated optimisation of solubility and conformational stability of antibodies and proteins — Supplementary File 7
- 作者：Angelo Rosace, Anja Bennett, Marc Oeller, Mie M. Mortensen, Laila Sakhnini, Nikolai Lorenzen, Christian Poulsen, Pietro Sormanni
- 载体与版本：Nature Communications 14, 1937 (2023)，独立补充 PDF
- 发布日期：2023-04-06
- DOI：[10.1038/s41467-023-37668-6](https://doi.org/10.1038/s41467-023-37668-6)（所附主论文 DOI）
- PMID / PMCID：37024501 / PMC10079162
- 本地文件：`articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM10.pdf`
- 文件大小：4,021,534 bytes；13 页
- SHA-256：`0e93b17e8349fd5307ddfb3dfd271ef6fd9e1820c59d4c509416efc1914accb7`
- 文本许可：CC BY 4.0；第三方材料例外以原 credit line 为准
- 补充材料：Supplementary File 7；相关数据对象见数据结构。

### Supplement-MOESM11

- 标题：Automated optimisation of solubility and conformational stability of antibodies and proteins — Supplementary File 8
- 作者：Angelo Rosace, Anja Bennett, Marc Oeller, Mie M. Mortensen, Laila Sakhnini, Nikolai Lorenzen, Christian Poulsen, Pietro Sormanni
- 载体与版本：Nature Communications 14, 1937 (2023)，独立补充 PDF
- 发布日期：2023-04-06
- DOI：[10.1038/s41467-023-37668-6](https://doi.org/10.1038/s41467-023-37668-6)（所附主论文 DOI）
- PMID / PMCID：37024501 / PMC10079162
- 本地文件：`articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM11.pdf`
- 文件大小：2,259,852 bytes；9 页
- SHA-256：`4ece08f1b7e74bcb779f5ba5a3d313e381c08099d778c1ed22f93b55d468cc1c`
- 文本许可：CC BY 4.0；第三方材料例外以原 credit line 为准
- 补充材料：Supplementary File 8；相关数据对象见数据结构。

### Supplement-MOESM12

- 标题：Automated optimisation of solubility and conformational stability of antibodies and proteins — Supplementary File 9
- 作者：Angelo Rosace, Anja Bennett, Marc Oeller, Mie M. Mortensen, Laila Sakhnini, Nikolai Lorenzen, Christian Poulsen, Pietro Sormanni
- 载体与版本：Nature Communications 14, 1937 (2023)，独立补充 PDF
- 发布日期：2023-04-06
- DOI：[10.1038/s41467-023-37668-6](https://doi.org/10.1038/s41467-023-37668-6)（所附主论文 DOI）
- PMID / PMCID：37024501 / PMC10079162
- 本地文件：`articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM12.pdf`
- 文件大小：2,232,558 bytes；9 页
- SHA-256：`6aeaec4d7751047005c20f0df13345b5bb69ca0886cb7582b5a426b37d474420`
- 文本许可：CC BY 4.0；第三方材料例外以原 credit line 为准
- 补充材料：Supplementary File 9；相关数据对象见数据结构。

### Supplement-MOESM14

- 标题：Automated optimisation of solubility and conformational stability of antibodies and proteins — Supplementary File 11
- 作者：Angelo Rosace, Anja Bennett, Marc Oeller, Mie M. Mortensen, Laila Sakhnini, Nikolai Lorenzen, Christian Poulsen, Pietro Sormanni
- 载体与版本：Nature Communications 14, 1937 (2023)，独立补充 PDF
- 发布日期：2023-04-06
- DOI：[10.1038/s41467-023-37668-6](https://doi.org/10.1038/s41467-023-37668-6)（所附主论文 DOI）
- PMID / PMCID：37024501 / PMC10079162
- 本地文件：`articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM14.pdf`
- 文件大小：223,880 bytes；3 页
- SHA-256：`0707bfe7ff118cac42b70ffb2e8d3d37c6e232a05c82520379c34d7a081c3eba`
- 文本许可：CC BY 4.0；第三方材料例外以原 credit line 为准
- 补充材料：Supplementary File 11；相关数据对象见数据结构。

### Supplement-MOESM2

- 标题：Automated optimisation of solubility and conformational stability of antibodies and proteins — Peer Review File
- 作者：Angelo Rosace, Anja Bennett, Marc Oeller, Mie M. Mortensen, Laila Sakhnini, Nikolai Lorenzen, Christian Poulsen, Pietro Sormanni
- 载体与版本：Nature Communications 14, 1937 (2023)，独立补充 PDF
- 发布日期：2023-04-06
- DOI：[10.1038/s41467-023-37668-6](https://doi.org/10.1038/s41467-023-37668-6)（所附主论文 DOI）
- PMID / PMCID：37024501 / PMC10079162
- 本地文件：`articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM2.pdf`
- 文件大小：191,471 bytes；18 页
- SHA-256：`0de51e90d2c88bb70cc634c6270429174e861f7d61743bd6436d0bc8bf5cf397`
- 文本许可：CC BY 4.0；第三方材料例外以原 credit line 为准
- 补充材料：Peer Review File；相关数据对象见数据结构。

### Supplement-MOESM3

- 标题：Automated optimisation of solubility and conformational stability of antibodies and proteins — Description of Additional Supplementary Files
- 作者：Angelo Rosace, Anja Bennett, Marc Oeller, Mie M. Mortensen, Laila Sakhnini, Nikolai Lorenzen, Christian Poulsen, Pietro Sormanni
- 载体与版本：Nature Communications 14, 1937 (2023)，独立补充 PDF
- 发布日期：2023-04-06
- DOI：[10.1038/s41467-023-37668-6](https://doi.org/10.1038/s41467-023-37668-6)（所附主论文 DOI）
- PMID / PMCID：37024501 / PMC10079162
- 本地文件：`articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM3.pdf`
- 文件大小：89,273 bytes；1 页
- SHA-256：`752ce592c5979e3fa7da0081bb449a9ce0cc3544e6ce4e58ac80d67589ea30c6`
- 文本许可：CC BY 4.0；第三方材料例外以原 credit line 为准
- 补充材料：Description of Additional Supplementary Files；相关数据对象见数据结构。

### Supplement-MOESM4

- 标题：Automated optimisation of solubility and conformational stability of antibodies and proteins — Supplementary File 1
- 作者：Angelo Rosace, Anja Bennett, Marc Oeller, Mie M. Mortensen, Laila Sakhnini, Nikolai Lorenzen, Christian Poulsen, Pietro Sormanni
- 载体与版本：Nature Communications 14, 1937 (2023)，独立补充 PDF
- 发布日期：2023-04-06
- DOI：[10.1038/s41467-023-37668-6](https://doi.org/10.1038/s41467-023-37668-6)（所附主论文 DOI）
- PMID / PMCID：37024501 / PMC10079162
- 本地文件：`articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM4.pdf`
- 文件大小：6,359,273 bytes；17 页
- SHA-256：`ee4afcc95db236c4db6f6b33947bb72b38638b0c69605ca4496fb73807a4775a`
- 文本许可：CC BY 4.0；第三方材料例外以原 credit line 为准
- 补充材料：Supplementary File 1；相关数据对象见数据结构。

### Supplement-MOESM5

- 标题：Automated optimisation of solubility and conformational stability of antibodies and proteins — Supplementary File 2
- 作者：Angelo Rosace, Anja Bennett, Marc Oeller, Mie M. Mortensen, Laila Sakhnini, Nikolai Lorenzen, Christian Poulsen, Pietro Sormanni
- 载体与版本：Nature Communications 14, 1937 (2023)，独立补充 PDF
- 发布日期：2023-04-06
- DOI：[10.1038/s41467-023-37668-6](https://doi.org/10.1038/s41467-023-37668-6)（所附主论文 DOI）
- PMID / PMCID：37024501 / PMC10079162
- 本地文件：`articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM5.pdf`
- 文件大小：2,480,549 bytes；10 页
- SHA-256：`053e2c948f9e33f52dedc39b902b29718c3714075496ca10ffcadc3e657773f9`
- 文本许可：CC BY 4.0；第三方材料例外以原 credit line 为准
- 补充材料：Supplementary File 2；相关数据对象见数据结构。

### Supplement-MOESM6

- 标题：Automated optimisation of solubility and conformational stability of antibodies and proteins — Supplementary File 3
- 作者：Angelo Rosace, Anja Bennett, Marc Oeller, Mie M. Mortensen, Laila Sakhnini, Nikolai Lorenzen, Christian Poulsen, Pietro Sormanni
- 载体与版本：Nature Communications 14, 1937 (2023)，独立补充 PDF
- 发布日期：2023-04-06
- DOI：[10.1038/s41467-023-37668-6](https://doi.org/10.1038/s41467-023-37668-6)（所附主论文 DOI）
- PMID / PMCID：37024501 / PMC10079162
- 本地文件：`articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM6.pdf`
- 文件大小：5,170,791 bytes；11 页
- SHA-256：`ab28b1464f6fe1f88e106ea25e37e94f0352616d6473344dfedb345d27650435`
- 文本许可：CC BY 4.0；第三方材料例外以原 credit line 为准
- 补充材料：Supplementary File 3；相关数据对象见数据结构。

### Supplement-MOESM7

- 标题：Automated optimisation of solubility and conformational stability of antibodies and proteins — Supplementary File 4
- 作者：Angelo Rosace, Anja Bennett, Marc Oeller, Mie M. Mortensen, Laila Sakhnini, Nikolai Lorenzen, Christian Poulsen, Pietro Sormanni
- 载体与版本：Nature Communications 14, 1937 (2023)，独立补充 PDF
- 发布日期：2023-04-06
- DOI：[10.1038/s41467-023-37668-6](https://doi.org/10.1038/s41467-023-37668-6)（所附主论文 DOI）
- PMID / PMCID：37024501 / PMC10079162
- 本地文件：`articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM7.pdf`
- 文件大小：4,380,422 bytes；14 页
- SHA-256：`e2e45f484f5a00f78f0729e84555ffa5b6f0a13499918ebbc263ed64858f0ce7`
- 文本许可：CC BY 4.0；第三方材料例外以原 credit line 为准
- 补充材料：Supplementary File 4；相关数据对象见数据结构。

### Supplement-MOESM8

- 标题：Automated optimisation of solubility and conformational stability of antibodies and proteins — Supplementary File 5
- 作者：Angelo Rosace, Anja Bennett, Marc Oeller, Mie M. Mortensen, Laila Sakhnini, Nikolai Lorenzen, Christian Poulsen, Pietro Sormanni
- 载体与版本：Nature Communications 14, 1937 (2023)，独立补充 PDF
- 发布日期：2023-04-06
- DOI：[10.1038/s41467-023-37668-6](https://doi.org/10.1038/s41467-023-37668-6)（所附主论文 DOI）
- PMID / PMCID：37024501 / PMC10079162
- 本地文件：`articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM8.pdf`
- 文件大小：3,032,101 bytes；11 页
- SHA-256：`1daad2a7f4978939a7a4ad495567c3aeabfeaebb853c43b2b672dc115c7010c1`
- 文本许可：CC BY 4.0；第三方材料例外以原 credit line 为准
- 补充材料：Supplementary File 5；相关数据对象见数据结构。

### Supplement-MOESM9

- 标题：Automated optimisation of solubility and conformational stability of antibodies and proteins — Supplementary File 6
- 作者：Angelo Rosace, Anja Bennett, Marc Oeller, Mie M. Mortensen, Laila Sakhnini, Nikolai Lorenzen, Christian Poulsen, Pietro Sormanni
- 载体与版本：Nature Communications 14, 1937 (2023)，独立补充 PDF
- 发布日期：2023-04-06
- DOI：[10.1038/s41467-023-37668-6](https://doi.org/10.1038/s41467-023-37668-6)（所附主论文 DOI）
- PMID / PMCID：37024501 / PMC10079162
- 本地文件：`articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM9.pdf`
- 文件大小：5,323,105 bytes；11 页
- SHA-256：`493f8ed429a3554af65f12f15f8d9aee254fc37d860f1a61e0a9045eaddae845`
- 文本许可：CC BY 4.0；第三方材料例外以原 credit line 为准
- 补充材料：Supplementary File 6；相关数据对象见数据结构。

### Supplementary Information

- 标题：Automated optimisation of solubility and conformational stability of antibodies and proteins — Supplementary Information
- 作者：Angelo Rosace, Anja Bennett, Marc Oeller, Mie M. Mortensen, Laila Sakhnini, Nikolai Lorenzen, Christian Poulsen, Pietro Sormanni
- 载体与版本：Nature Communications 14, 1937 (2023)，独立补充 PDF
- 发布日期：2023-04-06
- DOI：[10.1038/s41467-023-37668-6](https://doi.org/10.1038/s41467-023-37668-6)（所附主论文 DOI）
- PMID / PMCID：37024501 / PMC10079162
- 本地文件：`articles/Rosace_2023-04-06_NatureCommunications-SupplementaryInformation.pdf`
- 文件大小：11,867,348 bytes；31 页
- SHA-256：`e468be57aa4305836cfae55409b8d5735dccb84bf7aa88c9c853bda700e1939e`
- 文本许可：CC BY 4.0；第三方材料例外以原 credit line 为准
- 补充材料：Supplementary Information；相关数据对象见数据结构。

## 仓库内容

FLAb 为选择性快照，固定 commit `e05e3f0135783ffb7de412df6a1467e7a0031911`，committer 日期 2026-08-17；只保留本来源关联表，不声称完整 FLAb tree。所选表为普通 Git blobs，没有所选 payload 的 LFS/submodule。 一手论文和 Source Data 发布日期为 2023-04-06，因此命名 snapshot-2023-04-06；publisher 文件链接没有不可变 release 版本，本地大小/SHA-256 固定取得原件。

```text
snapshot-2023-04-06/
  FLAb/data/binding/rosace2023automated_kd_adalimumab.csv
  FLAb/data/binding/rosace2023automated_kd_golimumab.csv
  FLAb/data/polyreactivity/rosace2023automated_CICRT1_adalimumab.csv
  FLAb/data/polyreactivity/rosace2023automated_CICRT1_golimumab.csv
  FLAb/data/polyreactivity/rosace2023automated_CICRT2_adalimumab.csv
  FLAb/data/polyreactivity/rosace2023automated_CICRT2_golimumab.csv
  FLAb/data/thermostability/rosace2023automated_tm1_adalimumab.csv
  FLAb/data/thermostability/rosace2023automated_tm1_golimumab.csv
  Rosace-source-data/41467_2023_37668_MOESM13_ESM.xlsx
  Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx
```

FLAb 表按原目录/文件名保存；其他交付对象按来源名称隔离。payload 不包括本项目另加的论文、README 或 RCSB 文件。

## 数据结构

### 文件和记录关系

FLAb 8 CSV 按 binding、polyreactivity、thermostability 区分端点；同一序列在四类读数中共享，不带统一独立实验 ID。KD 表的两个 -log 列和 fitness 为派生读数。

`41467_2023_37668_MOESM15_ESM.xlsx` 全部 17 sheets 已解析；`Fig 1A`/`Fig S2` 是蛋白稳定性 benchmark（分别 81/79 唯一 PDB，后者为子集），字段含 pdb、mutation、is_reverse、experimental_DDG、foldX_DDG。`Fig S9` 是抗体 KD；`Fig S11` 是 19 个结构的实验/模型比较。其他 sheets 含不同表征和绘图数据，不直接作为新增结合样本。

MOESM13 是 DMS 汇编 Supplementary File 10，有 3 sheets，其中 `Notes Identified discrepancies` 上游为空。主 sheet 包含 Protein、Variant、Fitness score、Conservation、Number of contacts、SASA、BLOSUM Score、Change in charge type、Mutation PDB、offset applied、Site solvent exposure、pdb file、Site identified from、Shortlisted mutation；原错拼与空 sheet 均保持。算法输出是派生变量，若预测同源实验 fitness 需检查泄漏。其 pdb file 明示 7 个蛋白参考，不能称为六亲本抗体结合表。

| 文件 | 数据行数 | 唯一序列组合 | 额外整行副本 | 原序列列长度 aa | 空值 |
| --- | --- | --- | --- | --- | --- |
| `FLAb/data/binding/rosace2023automated_kd_adalimumab.csv` | 14 | 14 | 0 | heavy=[121], light=[107] | 0 |
| `FLAb/data/binding/rosace2023automated_kd_golimumab.csv` | 5 | 5 | 0 | heavy=[126], light=[108] | 0 |
| `FLAb/data/polyreactivity/rosace2023automated_CICRT1_adalimumab.csv` | 14 | 14 | 0 | heavy=[121], light=[107] | 0 |
| `FLAb/data/polyreactivity/rosace2023automated_CICRT1_golimumab.csv` | 5 | 5 | 0 | heavy=[126], light=[108] | 0 |
| `FLAb/data/polyreactivity/rosace2023automated_CICRT2_adalimumab.csv` | 14 | 14 | 0 | heavy=[121], light=[107] | 0 |
| `FLAb/data/polyreactivity/rosace2023automated_CICRT2_golimumab.csv` | 5 | 5 | 0 | heavy=[126], light=[108] | 0 |
| `FLAb/data/thermostability/rosace2023automated_tm1_adalimumab.csv` | 14 | 14 | 0 | heavy=[121], light=[107] | 0 |
| `FLAb/data/thermostability/rosace2023automated_tm1_golimumab.csv` | 5 | 5 | 0 | heavy=[126], light=[108] | 0 |

### 工作簿覆盖

| 工作簿 | Sheet | 有值行数（含表头） | 唯一明示 PDB |
| --- | --- | --- | --- |
| 41467_2023_37668_MOESM13_ESM.xlsx | Supplementary_table_DMS_validat | 25362 | 7 |
| 41467_2023_37668_MOESM13_ESM.xlsx | Number of mutations | 10 | 0 |
| 41467_2023_37668_MOESM13_ESM.xlsx | Notes Identified discrepancies | 0 | 0 |
| 41467_2023_37668_MOESM15_ESM.xlsx | Fig 1A | 1512 | 81 |
| 41467_2023_37668_MOESM15_ESM.xlsx | Fig 1B | 6 | 0 |
| 41467_2023_37668_MOESM15_ESM.xlsx | Fig 3D | 20 | 0 |
| 41467_2023_37668_MOESM15_ESM.xlsx | Fig 4 | 15 | 0 |
| 41467_2023_37668_MOESM15_ESM.xlsx | Fig 5 | 37 | 0 |
| 41467_2023_37668_MOESM15_ESM.xlsx | Fig S1 | 26 | 0 |
| 41467_2023_37668_MOESM15_ESM.xlsx | Fig S2 | 988 | 79 |
| 41467_2023_37668_MOESM15_ESM.xlsx | Fig S3 | 48 | 0 |
| 41467_2023_37668_MOESM15_ESM.xlsx | Fig S4 | 47 | 0 |
| 41467_2023_37668_MOESM15_ESM.xlsx | Fig S5 | 52 | 0 |
| 41467_2023_37668_MOESM15_ESM.xlsx | Fig S6 | 18 | 0 |
| 41467_2023_37668_MOESM15_ESM.xlsx | Fig S7 | 18 | 0 |
| 41467_2023_37668_MOESM15_ESM.xlsx | Fig S8 | 15 | 0 |
| 41467_2023_37668_MOESM15_ESM.xlsx | Fig S9 | 50 | 0 |
| 41467_2023_37668_MOESM15_ESM.xlsx | Fig S10 | 2 | 0 |
| 41467_2023_37668_MOESM15_ESM.xlsx | Fig S11 | 21 | 19 |
| 41467_2023_37668_MOESM15_ESM.xlsx | Fig S12 | 24 | 0 |

空 sheet 是上游事实；表头占行、多段布局和绘图点不能一律按有值行数计独立样本。

### 字段说明

| 文件或表 | 原字段 | 类型、单位、方向与缺失 | 来源/限制 |
| --- | --- | --- | --- |
| FLAb binding | `Ab`, `Mutations`, `heavy`, `light` | 字符串；Adalimumab 121/107 aa，Golimumab 126/108 aa | 亲本、设计和分离可变区；无空序列 |
| FLAb binding | `KD (M)` | 浮点，M，较低通常较强 | BLI 实验拟合汇总；不是通用 SPR |
| FLAb binding | `-log10( KD (M) )` / `-log10(KD (M) )` | 浮点，-log10(M)，较高通常较强 | 派生；两个文件空格拼写不同 |
| FLAb binding | `fitness`, `-log(Kd [nM])` | 浮点，实值验证为 -log10(nM)，与上一列相差 9 | 派生重复，不作预测同一标签的输入 |
| FLAb CIC | `CIC RT (min) rep1`, `CIC RT (min) rep2`, `fitness` | 浮点，min，通常较低较好 | 重复多反应性测量；fitness 重复读数 |
| FLAb Tm | `Tm (C) rep1`, `fitness` | 浮点，°C，较高通常较稳定 | 实验热稳定性端点 |
| MOESM15 Fig S9 | `KD (nM)`, `KD Error (nM)` | XLSX 数值/字符串 nan；表头与 M 尺度冲突 | 实验汇总；C37 nan 不补零，单位不按表头盲换 |
| MOESM15 Fig 1A/Fig S2 | `pdb`, `mutation`, `is_reverse`, `experimental_DDG`, `foldX_DDG` | 字符串/布尔或数值；ΔΔG 量纲依原表及论文 | 实验稳定性与计算预测，逆向行是派生 |
| MOESM13 DMS | `Protein`, `Variant`, `Fitness score`, `pdb file` 等 | 字符串/数值；各蛋白实验标度不统一 | 捆绑基准及计算特征，不并入抗体 KD |

### 数据示例

| 真实文件/位置 | 实际值摘录（序列仅给已核对长度） | 序列范围 |
| --- | --- | --- |
| `rosace2023automated_kd_adalimumab.csv` 第 2 行 | Ab=Adalimumab, Mutations=WT, KD (M)=1.3e-10, -log10( KD (M) )=9.886056648, fitness=0.8860566476931633, -log(Kd [nM])=0.8860566476931633 | 原 heavy 121 aa / light 107 aa |
| `rosace2023automated_kd_golimumab.csv` 第 2 行 | Ab=Golimumab, Mutations=WT, KD (M)=3.4e-10, -log10(KD (M) )=9.468521083, fitness=0.46852108295774486, -log(Kd [nM])=0.46852108295774486 | 原 heavy 126 aa / light 108 aa |
| `rosace2023automated_CICRT1_adalimumab.csv` 第 2 行 | CIC RT (min) rep1=10.532, fitness=10.532 | 原 heavy 121 aa / light 107 aa |
| `rosace2023automated_CICRT1_golimumab.csv` 第 2 行 | CIC RT (min) rep1=12.1, fitness=12.1 | 原 heavy 126 aa / light 108 aa |
| `rosace2023automated_CICRT2_adalimumab.csv` 第 2 行 | CIC RT (min) rep2=10.5105, fitness=10.5105 | 原 heavy 121 aa / light 107 aa |
| `rosace2023automated_CICRT2_golimumab.csv` 第 2 行 | CIC RT (min) rep2=12.07, fitness=12.07 | 原 heavy 126 aa / light 108 aa |
| `rosace2023automated_tm1_adalimumab.csv` 第 2 行 | Tm (C) rep1=57.9, fitness=57.9 | 原 heavy 121 aa / light 107 aa |
| `rosace2023automated_tm1_golimumab.csv` 第 2 行 | Tm (C) rep1=62.4, fitness=62.4 | 原 heavy 126 aa / light 108 aa |

每项是原 CSV 首条数据记录的等价摘录，序列未在文档重复展开。每行是一种端点记录，不等于一个独立亲本；重复和不同端点关系如上。

## PDB 数据库

接受 114 个唯一锚点：补充 Table S1/S3 的 7 个亲本输入、DMS pdb file 的 7 个蛋白输入、Source Data Fig 1A 的 81 个稳定性背景及 Fig S11 的 19 个结构比较背景。Fig S2 的 79 个是 Fig 1A 子集，不另复制。每个 ID 的证据列在下表，保留完整条目所有 polymer entities，未按数据行复制或裁剪。

主亲本链映射：5VNW C/D 为 Nb.B201 entity 2（120 aa）、A/B 为 HSA entity 1（585 aa）；原始 entry 是 HSA 结合复合物，论文设计输入取无抗原 Nb 链，不把整个 PDB 称为游离态。3WD5 H/L 为 Adalimumab，A 为 TNFα；5YOY H/E 为 Golimumab，C 为 TNFα；6W41 H/L 为 CR3022，C 为 SARS-CoV-2 RBD。7JN5 H/L 同为 CR3022，但 F 是 SARS-CoV RBD，不说是同株复合物。6YZ5 F 是 H11-D4、E 是 RBD。

**6ZBP 链编号漂移：** 2023 年原补充表指定 B 为 H11-H4、A 为抗原；本次 RCSB 字面 FASTA/mmCIF 的 author chains 是 FFF（entity 2，134 aa）与 EEE（entity 1，210 aa）。两层逐 entity canonical sequence 验证一致，但不能假装现在有 A/B 或重写成旧链名。共享设计输入和当前数据库修订并非每个实验变体的严格 construct/坐标对应。其余 107 个背景不是新增抗体结合实验，也不把 AlphaFold/作者裁剪模型冒充原 RCSB 实验坐标。

| RCSB entry | 接受锚点的一手连接证据 | 全部 polymer entities 与 author chains（canonical 长度） |
| --- | --- | --- |
| [1A2P](https://www.rcsb.org/structure/1A2P) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B,C, 110 个残基, BARNASE |
| [1AAR](https://www.rcsb.org/structure/1AAR) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B, 76 个残基, DI-UBIQUITIN |
| [1AMQ](https://www.rcsb.org/structure/1AMQ) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 396 个残基, ASPARTATE AMINOTRANSFERASE |
| [1ANK](https://www.rcsb.org/structure/1ANK) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B, 214 个残基, ADENYLATE KINASE |
| [1AXB](https://www.rcsb.org/structure/1AXB) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 263 个残基, TEM-1 BETA LACTAMASE |
| [1AYF](https://www.rcsb.org/structure/1AYF) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B, 105 个残基, ADRENODOXIN |
| [1BOY](https://www.rcsb.org/structure/1BOY) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 219 个残基, HUMAN TISSUE FACTOR |
| [1BP2](https://www.rcsb.org/structure/1BP2) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 123 个残基, PHOSPHOLIPASE A2 |
| [1BPI](https://www.rcsb.org/structure/1BPI) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 58 个残基, BOVINE PANCREATIC TRYPSIN INHIBITOR |
| [1BVC](https://www.rcsb.org/structure/1BVC) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 153 个残基, APOMYOGLOBIN |
| [1C2R](https://www.rcsb.org/structure/1C2R) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B, 116 个残基, CYTOCHROME C2 |
| [1C9O](https://www.rcsb.org/structure/1C9O) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B, 66 个残基, COLD-SHOCK PROTEIN |
| [1CAH](https://www.rcsb.org/structure/1CAH) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 259 个残基, CARBONIC ANHYDRASE II |
| [1CLW](https://www.rcsb.org/structure/1CLW) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 554 个残基, TAILSPIKE PROTEIN |
| [1CSP](https://www.rcsb.org/structure/1CSP) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 67 个残基, COLD SHOCK PROTEIN B(CSPB) |
| [1CYC](https://www.rcsb.org/structure/1CYC) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B, 103 个残基, FERROCYTOCHROME C |
| [1CYO](https://www.rcsb.org/structure/1CYO) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 93 个残基, CYTOCHROME B5 |
| [1DYJ](https://www.rcsb.org/structure/1DYJ) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B, 159 个残基, DIHYDROFOLATE REDUCTASE |
| [1EL1](https://www.rcsb.org/structure/1EL1) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B, 130 个残基, LYSOZYME C |
| [1FKJ](https://www.rcsb.org/structure/1FKJ) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 107 个残基, FK506 BINDING PROTEIN |
| [1FNF](https://www.rcsb.org/structure/1FNF) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 368 个残基, FIBRONECTIN |
| [1FRD](https://www.rcsb.org/structure/1FRD) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 98 个残基, HETEROCYST [2FE-2S] FERREDOXIN |
| [1FTG](https://www.rcsb.org/structure/1FTG) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 168 个残基, APOFLAVODOXIN |
| [1FXA](https://www.rcsb.org/structure/1FXA) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B, 98 个残基, [2FE-2S] FERREDOXIN |
| [1GNX](https://www.rcsb.org/structure/1GNX) | Rosace-source-data/41467_2023_37668_MOESM13_ESM.xlsx:Supplementary_table_DMS_validat | entity 1: author A,B, 479 个残基, BETA-GLUCOSIDASE |
| [1H7M](https://www.rcsb.org/structure/1H7M) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 102 个残基, 50S RIBOSOMAL PROTEIN L30E |
| [1HFY](https://www.rcsb.org/structure/1HFY) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B, 123 个残基, ALPHA-LACTALBUMIN |
| [1HFZ](https://www.rcsb.org/structure/1HFZ) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B,C,D, 124 个残基, ALPHA-LACTALBUMIN |
| [1IGV](https://www.rcsb.org/structure/1IGV) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 75 个残基, VITAMIN D-DEPENDENT CALCIUM-BINDING PROTEIN, INTESTINAL |
| [1IO2](https://www.rcsb.org/structure/1IO2) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 213 个残基, RIBONUCLEASE HII |
| [1IOB](https://www.rcsb.org/structure/1IOB) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 153 个残基, INTERLEUKIN-1 BETA |
| [1JIW](https://www.rcsb.org/structure/1JIW) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author P, 470 个残基, ALKALINE METALLOPROTEINASE; entity 2: author I, 106 个残基, PROTEINASE INHIBITOR |
| [1KFW](https://www.rcsb.org/structure/1KFW) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 435 个残基, chitinase B |
| [1L63](https://www.rcsb.org/structure/1L63) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 164 个残基, LYSOZYME |
| [1LZ1](https://www.rcsb.org/structure/1LZ1) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 130 个残基, HUMAN LYSOZYME |
| [1M40](https://www.rcsb.org/structure/1M40) | Rosace-source-data/41467_2023_37668_MOESM13_ESM.xlsx:Supplementary_table_DMS_validat | entity 1: author A, 263 个残基, BETA-LACTAMASE TEM |
| [1MGR](https://www.rcsb.org/structure/1MGR) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 99 个残基, Guanyl-specific ribonuclease Sa3 |
| [1MSI](https://www.rcsb.org/structure/1MSI) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 70 个残基, TYPE III ANTIFREEZE PROTEIN ISOFORM HPLC 12 |
| [1ND4](https://www.rcsb.org/structure/1ND4) | Rosace-source-data/41467_2023_37668_MOESM13_ESM.xlsx:Supplementary_table_DMS_validat | entity 1: author A,B, 264 个残基, Aminoglycoside 3'-phosphotransferase |
| [1OH0](https://www.rcsb.org/structure/1OH0) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B, 131 个残基, STEROID DELTA-ISOMERASE |
| [1OIA](https://www.rcsb.org/structure/1OIA) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B, 95 个残基, U1 SMALL NUCLEAR RIBONUCLEOPROTEIN A |
| [1ONC](https://www.rcsb.org/structure/1ONC) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 104 个残基, P-30 PROTEIN |
| [1PGA](https://www.rcsb.org/structure/1PGA) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 56 个残基, PROTEIN G |
| [1PIN](https://www.rcsb.org/structure/1PIN) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 163 个残基, PEPTIDYL-PROLYL CIS-TRANS ISOMERASE |
| [1POH](https://www.rcsb.org/structure/1POH) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 85 个残基, HISTIDINE-CONTAINING PHOSPHOCARRIER PROTEIN HPR |
| [1QLP](https://www.rcsb.org/structure/1QLP) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 394 个残基, ALPHA-1-ANTITRYPSIN |
| [1RGG](https://www.rcsb.org/structure/1RGG) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B, 96 个残基, RIBONUCLEASE |
| [1RIS](https://www.rcsb.org/structure/1RIS) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A | entity 1: author A, 101 个残基, RIBOSOMAL PROTEIN S6 |
| [1RN1](https://www.rcsb.org/structure/1RN1) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B,C, 104 个残基, RIBONUCLEASE T1 ISOZYME |
| [1ROP](https://www.rcsb.org/structure/1ROP) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 63 个残基, ROP PROTEIN |
| [1RTB](https://www.rcsb.org/structure/1RTB) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 124 个残基, RIBONUCLEASE A |
| [1SHF](https://www.rcsb.org/structure/1SHF) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B, 59 个残基, FYN TYROSINE KINASE SH3 DOMAIN |
| [1SHG](https://www.rcsb.org/structure/1SHG) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 62 个残基, ALPHA-SPECTRIN SH3 DOMAIN |
| [1STN](https://www.rcsb.org/structure/1STN) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 149 个残基, STAPHYLOCOCCAL NUCLEASE |
| [1SUP](https://www.rcsb.org/structure/1SUP) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 275 个残基, SUBTILISIN BPN' |
| [1TEN](https://www.rcsb.org/structure/1TEN) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 90 个残基, TENASCIN |
| [1TPK](https://www.rcsb.org/structure/1TPK) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B,C, 88 个残基, TISSUE PLASMINOGEN ACTIVATOR |
| [1TUP](https://www.rcsb.org/structure/1TUP) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author E, 21 个残基, DNA (5'-D(*TP*TP*TP*CP*CP*TP*AP*GP*AP*CP*TP*TP*GP*CP*CP*CP*A P*AP*TP*TP*A)-3'); entity 2: author F, 21 个残基, DNA (5'-D(*AP*TP*AP*AP*TP*TP*GP*GP*GP*CP*AP*AP*GP*TP*CP*TP*A P*GP*GP*AP*A)-3'); entity 3: author A,B,C, 219 个残基, PROTEIN (P53 TUMOR SUPPRESSOR ) |
| [1UBQ](https://www.rcsb.org/structure/1UBQ) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 76 个残基, UBIQUITIN |
| [1VQB](https://www.rcsb.org/structure/1VQB) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 87 个残基, GENE V PROTEIN |
| [219L](https://www.rcsb.org/structure/219L) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 164 个残基, T4 LYSOZYME |
| [2AFG](https://www.rcsb.org/structure/2AFG) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B,C,D, 140 个残基, ACIDIC FIBROBLAST GROWTH FACTOR |
| [2AKY](https://www.rcsb.org/structure/2AKY) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 220 个残基, ADENYLATE KINASE |
| [2BQA](https://www.rcsb.org/structure/2BQA) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 130 个残基, LYSOZYME |
| [2CG9](https://www.rcsb.org/structure/2CG9) | Rosace-source-data/41467_2023_37668_MOESM13_ESM.xlsx:Supplementary_table_DMS_validat | entity 1: author A,B, 677 个残基, ATP-DEPENDENT MOLECULAR CHAPERONE HSP82; entity 2: author X,Y, 134 个残基, CO-CHAPERONE PROTEIN SBA1 |
| [2CI2](https://www.rcsb.org/structure/2CI2) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author I, 83 个残基, CHYMOTRYPSIN INHIBITOR 2 |
| [2CRK](https://www.rcsb.org/structure/2CRK) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 381 个残基, PROTEIN (CREATINE KINASE) |
| [2HMB](https://www.rcsb.org/structure/2HMB) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 132 个残基, MUSCLE FATTY ACID BINDING PROTEIN |
| [2HPR](https://www.rcsb.org/structure/2HPR) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 87 个残基, HISTIDINE-CONTAINING PHOSPHOCARRIER PROTEIN HPR |
| [2IFB](https://www.rcsb.org/structure/2IFB) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 131 个残基, INTESTINAL FATTY ACID BINDING PROTEIN |
| [2IMM](https://www.rcsb.org/structure/2IMM) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 114 个残基, IGA-KAPPA MCPC603 FV (LIGHT CHAIN) |
| [2LZM](https://www.rcsb.org/structure/2LZM) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 164 个残基, T4 LYSOZYME |
| [2RN2](https://www.rcsb.org/structure/2RN2) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 155 个残基, RIBONUCLEASE H |
| [2TRX](https://www.rcsb.org/structure/2TRX) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B, 108 个残基, THIOREDOXIN |
| [2UYZ](https://www.rcsb.org/structure/2UYZ) | Rosace-source-data/41467_2023_37668_MOESM13_ESM.xlsx:Supplementary_table_DMS_validat | entity 1: author A, 158 个残基, SUMO-CONJUGATING ENZYME UBC9; entity 2: author B, 79 个残基, SMALL UBIQUITIN-RELATED MODIFIER 1 |
| [2ZTA](https://www.rcsb.org/structure/2ZTA) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B, 34 个残基, GCN4 LEUCINE ZIPPER |
| [3BCI](https://www.rcsb.org/structure/3BCI) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 186 个残基, Disulfide bond protein A |
| [3CHY](https://www.rcsb.org/structure/3CHY) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 128 个残基, CHEY |
| [3D2A](https://www.rcsb.org/structure/3D2A) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 181 个残基, Lipase |
| [3MBP](https://www.rcsb.org/structure/3MBP) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 370 个残基, MALTODEXTRIN-BINDING PROTEIN |
| [3PGK](https://www.rcsb.org/structure/3PGK) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 416 个残基, PHOSPHOGLYCERATE KINASE |
| [3S4Y](https://www.rcsb.org/structure/3S4Y) | Rosace-source-data/41467_2023_37668_MOESM13_ESM.xlsx:Supplementary_table_DMS_validat | entity 1: author A,B, 247 个残基, Thiamin pyrophosphokinase 1 |
| [3SSI](https://www.rcsb.org/structure/3SSI) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 113 个残基, STREPTOMYCES SUBTILISIN INHIBITOR |
| [3WD5](https://www.rcsb.org/structure/3WD5) | main-paper/shared-binding reference | entity 1: author A, 157 个残基, Tumor necrosis factor; entity 2: author L, 213 个残基, Adalimumab Light Chain; entity 3: author H, 219 个残基, Adalimumab Heavy Chain |
| [451C](https://www.rcsb.org/structure/451C) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 82 个残基, CYTOCHROME C551 |
| [4LYZ](https://www.rcsb.org/structure/4LYZ) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A, 129 个残基, HEN EGG WHITE LYSOZYME |
| [4NIF](https://www.rcsb.org/structure/4NIF) | Rosace-source-data/41467_2023_37668_MOESM13_ESM.xlsx:Supplementary_table_DMS_validat | entity 1: author A,D, 333 个残基, Ribosomal protein S6 kinase alpha-1; entity 2: author B,E, 362 个残基, Mitogen-activated protein kinase 1 |
| [5AZU](https://www.rcsb.org/structure/5AZU) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A; Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S2 | entity 1: author A,B,C,D, 128 个残基, AZURIN |
| [5CRO](https://www.rcsb.org/structure/5CRO) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig 1A | entity 1: author O,A,B,C, 66 个残基, CRO REPRESSOR PROTEIN |
| [5VNW](https://www.rcsb.org/structure/5VNW) | main-paper/shared-binding reference | entity 1: author A,B, 585 个残基, Serum albumin; entity 2: author C,D, 120 个残基, Nb.b201 |
| [5YOY](https://www.rcsb.org/structure/5YOY) | main-paper/shared-binding reference | entity 1: author A,B,C,J,K,L, 173 个残基, Tumor necrosis factor; entity 2: author D,E,F,M,N,O, 119 个残基, Golimumab light chain variable region; entity 3: author G,H,I,P,Q,R, 129 个残基, Golimumab heavy chain variable region |
| [6W41](https://www.rcsb.org/structure/6W41) | main-paper/shared-binding reference | entity 1: author H, 222 个残基, CR3022 Fab heavy chain; entity 2: author L, 221 个残基, CR3022 Fab light chain; entity 3: author C, 231 个残基, Spike protein S1 |
| [6YZ5](https://www.rcsb.org/structure/6YZ5) | main-paper/shared-binding reference | entity 1: author E, 210 个残基, Spike glycoprotein; entity 2: author F, 134 个残基, Nanobody H11-D4 |
| [6ZBP](https://www.rcsb.org/structure/6ZBP) | main-paper/shared-binding reference | entity 1: author EEE, 210 个残基, Spike glycoprotein; entity 2: author FFF, 134 个残基, H11-H4 |
| [7JN5](https://www.rcsb.org/structure/7JN5) | main-paper/shared-binding reference | entity 1: author H, 221 个残基, CR3022 heavy chain; entity 2: author L, 221 个残基, CR3022 light chain; entity 3: author F, 230 个残基, Spike glycoprotein |
| [7PS3](https://www.rcsb.org/structure/7PS3) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author H, 230 个残基, Beta-32 heavy chain; entity 2: author L, 214 个残基, Beta-32 light chain |
| [7PS4](https://www.rcsb.org/structure/7PS4) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author E,A, 210 个残基, Spike protein S1; entity 2: author H,B, 230 个残基, Beta-38 Fab heavy chain; entity 3: author L,C, 216 个残基, Beta-38 Fab light chain |
| [7Q0G](https://www.rcsb.org/structure/7Q0G) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author E, 210 个残基, Spike protein S1; entity 2: author H, 222 个残基, FI-3A Fab heavy chain; entity 3: author L, 214 个残基, FI-3A Fab light chain; entity 4: author B, 216 个残基, Beta-49 Fab light chain; entity 5: author A, 223 个残基, Beta-49 Fab heavy chain |
| [7QF0](https://www.rcsb.org/structure/7QF0) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author A, 206 个残基, Spike protein S1; entity 2: author H, 229 个残基, CV2.2325 heavy chain; entity 3: author L, 214 个残基, CV2.2325 light chain |
| [7QU1](https://www.rcsb.org/structure/7QU1) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author A, 234 个残基, Fab MAC1 heavy chain; entity 2: author B, 217 个残基, Fab MAC1 light chain; entity 3: author C, 182 个残基, Pre-glycoprotein polyprotein GP complex |
| [7RXI](https://www.rcsb.org/structure/7RXI) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author L, 214 个残基, Fab234 light chain; entity 2: author H, 225 个残基, Fab234 heavy chain; entity 3: author A, 66 个残基, Circumsporozoite protein |
| [7RYU](https://www.rcsb.org/structure/7RYU) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author H, 235 个残基, Ab1303 Fab heavy chain; entity 2: author L, 217 个残基, Ab1303 Fab light chain |
| [7S4G](https://www.rcsb.org/structure/7S4G) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author A,C,E,H, 223 个残基, heavy chain Fab 1G4; entity 2: author B,D,F,L, 220 个残基, light chain Fab 1G4; entity 3: author G,I,J,K, 9 个残基, Lymphocyte antigen 6 complex locus protein G6d |
| [7SEG](https://www.rcsb.org/structure/7SEG) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author L,B, 236 个残基, anti-CD16a Fab light chain; entity 2: author H,A, 247 个残基, anti-CD16A Fab heavy chain; entity 3: author D,C, 180 个残基, Low affinity immunoglobulin gamma Fc region receptor III-A |
| [7SG5](https://www.rcsb.org/structure/7SG5) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author H, 226 个残基, CIS43_Var2 Fab Heavy chain; entity 2: author L, 220 个残基, CIS43_Var2 Fab Light chain; entity 3: author A, 15 个残基, PfCSP peptide 21 |
| [7SG6](https://www.rcsb.org/structure/7SG6) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author H, 226 个残基, CIS43_Var10 Fab Heavy chain; entity 2: author L, 220 个残基, CIS43_Var10 Fab Light chain; entity 3: author A, 15 个残基, PfCSP peptide 21 |
| [7SJS](https://www.rcsb.org/structure/7SJS) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author H, 217 个残基, CC40.8 Fab heavy chain; entity 2: author L, 214 个残基, CC40.8 Fab light chain; entity 3: author C, 25 个残基, stem helix peptide of Spike protein S2' |
| [7SO5](https://www.rcsb.org/structure/7SO5) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author H, 215 个残基, Fab B2 HC; entity 2: author L, 216 个残基, Fab B2 LC; entity 3: author A, 541 个残基, Toxin B |
| [7TP4](https://www.rcsb.org/structure/7TP4) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author Z, 205 个残基, Spike protein S1; entity 2: author H, 227 个残基, K398.22 heavy chain; entity 3: author L, 214 个残基, K398.22 light chain |
| [7TTM](https://www.rcsb.org/structure/7TTM) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author A, 230 个残基, Spike protein S1; entity 2: author H, 230 个残基, 1040 heavy chain; entity 3: author L, 216 个残基, 1040 light chain |
| [7U8C](https://www.rcsb.org/structure/7U8C) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author BA2, 17 个残基, Mesothelin, cleaved form; entity 2: author H, 214 个残基, MORab 15B6 Fab heavy chain; entity 3: author L, 213 个残基, MORab 15B6 Fab light chain |
| [7Z0X](https://www.rcsb.org/structure/7Z0X) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author H, 237 个残基, THSC20.HVTR26 Fab heavy chain; entity 2: author L, 216 个残基, THSC20.HVTR26 Fab light chain; entity 3: author R, 205 个残基, Spike protein S1 |
| [7ZF6](https://www.rcsb.org/structure/7ZF6) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author H, 228 个残基, Omi-12 heavy chain; entity 2: author L, 215 个残基, Omi-12 light chain |
| [7ZWI](https://www.rcsb.org/structure/7ZWI) | Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx:Fig S11 | entity 1: author A,D, 429 个残基, Gametocyte surface protein P45/48; entity 2: author B,E, 444 个残基, 32F3 heavy chain; entity 3: author C,F, 213 个残基, 32F3 light chain |

取得 114 个原始 FASTA 与 114 个完整 mmCIF，共 57,065,079 bytes。FASTA 路径 `pdb/sequences/rcsb_pdb_<ID>.fasta`，坐标路径 `pdb/structures/<ID>.cif`。原始入口分别为 `https://www.rcsb.org/fasta/entry/<ID>/display` 与 `https://files.rcsb.org/download/<ID>.cif.gz`（无损解压，不重序列化坐标）。

PDB 子集 inventory SHA-256：`4ed2267ed3e7daaaeb58181661951898aafd671337930302a21488a2705a5464`；规则为相对路径、bytes、逐文件 SHA-256，以 TAB 分隔并以 LF 结尾，按路径排序后计算。逐 polymer canonical 序列与原始 FASTA 一致，并校验 entry identity、原子坐标/链引用；无 CDR graft、补环、变体重建或按行复制。缺失坐标残基与 canonical FASTA 全序列的差异是数据库事实，未人为补全。

## 使用方式

调用者将 `dataset_root` 设为本版本目录（partial 来源需明确选择 staging）。CSV 使用 UTF-8 和原表头；不在 raw 目录清洗或换算。

```python
import csv
from pathlib import Path
with (Path(dataset_root) / "FLAb/data/binding/rosace2023automated_kd_adalimumab.csv").open(encoding="utf-8-sig", newline="") as stream:
    rows = list(csv.DictReader(stream))
```

## 采集过程记录

2026-09-18：从当前项目配置确认身份和存储根，选择论文/Source Data 发布日 2023-04-06；FLAb 后续版本单独固定 commit，不用下载日伪造版本。用户确认共享存储写入后，按 Git blob/字节身份复用已有 R09 的 8 CSV。

2026-09-18：从 Springer Nature 一手链接枚举全部 15 个补充对象及主文，原字节归档到 staging；读取全部工作簿 sheets/PDF 页。Supplementary Information（31 页）及部分附件有原始 xref 指向异常，pypdf 可读并报告警告，原 PDF 未修复重写；bytes/SHA-256 固定了当前原件。依赖尚未完成解包时一次导入失败，完成依赖安装后重试通过。

2026-09-18：比对 Fig S9 C3 与补充 Table S5，确认 nM 表头/M 数值尺度冲突；记录 C37 nan、拟合限制、M/nM 对数差异，未改写标签。审计输入与所有工作簿明确 PDB 列/keys，扩展到 114 个唯一背景；取得所有原始 FASTA/完整 mmCIF。当前 6ZBP EEE/FFF 与论文 A/B 的链编号差异按原样保留。

2026-09-18：初次独立 PDB 审计使用错误 verify_pair 参数顺序而失败；修正调用后重新完成全部字节、格式和 entity sequence 配对验收，无意外旁路文件。编写严格格式 README 并即时同步 shared staging；通过文档与工作区范围检查后，发布脚本重新验证 inventory/README，再原子晋升为 snapshot-2023-04-06。该脚本在执行前默认为计划模式。

2026-10-16：确认 DOI `10.1021/BI971546+` 的官方 ShortDOI 为 `10/bqhq2h`；参考文献链接改用等价的 `https://doi.org/10/bqhq2h`，避免文档平台把 URL 路径末尾的加号错误规范化为空格，原 DOI 文本保持明确记录。

| 归档本地路径 | 上游原名 | bytes | 原字节 SHA-256 |
| --- | --- | --- | --- |
| `FLAb/data/binding/rosace2023automated_kd_adalimumab.csv` | rosace2023automated_kd_adalimumab.csv | 4512 | `179f8927cd120913c9ea97c5fca5cd9792fe694da124399189560c246dc467bb` |
| `FLAb/data/binding/rosace2023automated_kd_golimumab.csv` | rosace2023automated_kd_golimumab.csv | 1665 | `5c016bf3d74f2e042de10c73d6869986becac84a9a76921429243ea44420bf61` |
| `FLAb/data/polyreactivity/rosace2023automated_CICRT1_adalimumab.csv` | rosace2023automated_CICRT1_adalimumab.csv | 3465 | `1378b8297d7d812c1c041e10eb9b62166f775c6e5f2e4d11d893490ce34be758` |
| `FLAb/data/polyreactivity/rosace2023automated_CICRT1_golimumab.csv` | rosace2023automated_CICRT1_golimumab.csv | 1280 | `382a539c796d4388c475bc1f9ed0bc9ec7ea08377d9de3cd087ef1078cde18ed` |
| `FLAb/data/polyreactivity/rosace2023automated_CICRT2_adalimumab.csv` | rosace2023automated_CICRT2_adalimumab.csv | 3495 | `3cc6f17b8d9c803241c11db3ad0332a0b674d9dc36a692b48ca61585369f9d1a` |
| `FLAb/data/polyreactivity/rosace2023automated_CICRT2_golimumab.csv` | rosace2023automated_CICRT2_golimumab.csv | 1282 | `207a8e156b364cda08474f79966c19fc8dcc02bc79ef1d7eff932457652a74dc` |
| `FLAb/data/thermostability/rosace2023automated_tm1_adalimumab.csv` | rosace2023automated_tm1_adalimumab.csv | 3397 | `eaa1fddba5702e22ae2858994f0911cbaf1efaab92f9a58546aa3f96f43657a7` |
| `FLAb/data/thermostability/rosace2023automated_tm1_golimumab.csv` | rosace2023automated_tm1_golimumab.csv | 1266 | `4c7998d6f2159baeb8a3bc506d2065e18b9c2e2e69e2266c43a761b2d41fb0b2` |
| `Rosace-source-data/41467_2023_37668_MOESM13_ESM.xlsx` | 41467_2023_37668_MOESM13_ESM.xlsx | 1848798 | `226b888e498120db8b9486934f1afd5d6b9b0989b6679d26c10d8db2f9518ab0` |
| `Rosace-source-data/41467_2023_37668_MOESM15_ESM.xlsx` | 41467_2023_37668_MOESM15_ESM.xlsx | 163094 | `56b330941e6162497159b3e03ad614def8e198caa13bf2cb1cd075c6aaf26822` |
| `articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM10.pdf` | 41467_2023_37668_MOESM10_ESM.pdf | 4021534 | `0e93b17e8349fd5307ddfb3dfd271ef6fd9e1820c59d4c509416efc1914accb7` |
| `articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM11.pdf` | 41467_2023_37668_MOESM11_ESM.pdf | 2259852 | `4ece08f1b7e74bcb779f5ba5a3d313e381c08099d778c1ed22f93b55d468cc1c` |
| `articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM12.pdf` | 41467_2023_37668_MOESM12_ESM.pdf | 2232558 | `6aeaec4d7751047005c20f0df13345b5bb69ca0886cb7582b5a426b37d474420` |
| `articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM14.pdf` | 41467_2023_37668_MOESM14_ESM.pdf | 223880 | `0707bfe7ff118cac42b70ffb2e8d3d37c6e232a05c82520379c34d7a081c3eba` |
| `articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM2.pdf` | 41467_2023_37668_MOESM2_ESM.pdf | 191471 | `0de51e90d2c88bb70cc634c6270429174e861f7d61743bd6436d0bc8bf5cf397` |
| `articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM3.pdf` | 41467_2023_37668_MOESM3_ESM.pdf | 89273 | `752ce592c5979e3fa7da0081bb449a9ce0cc3544e6ce4e58ac80d67589ea30c6` |
| `articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM4.pdf` | 41467_2023_37668_MOESM4_ESM.pdf | 6359273 | `ee4afcc95db236c4db6f6b33947bb72b38638b0c69605ca4496fb73807a4775a` |
| `articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM5.pdf` | 41467_2023_37668_MOESM5_ESM.pdf | 2480549 | `053e2c948f9e33f52dedc39b902b29718c3714075496ca10ffcadc3e657773f9` |
| `articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM6.pdf` | 41467_2023_37668_MOESM6_ESM.pdf | 5170791 | `ab28b1464f6fe1f88e106ea25e37e94f0352616d6473344dfedb345d27650435` |
| `articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM7.pdf` | 41467_2023_37668_MOESM7_ESM.pdf | 4380422 | `e2e45f484f5a00f78f0729e84555ffa5b6f0a13499918ebbc263ed64858f0ce7` |
| `articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM8.pdf` | 41467_2023_37668_MOESM8_ESM.pdf | 3032101 | `1daad2a7f4978939a7a4ad495567c3aeabfeaebb853c43b2b672dc115c7010c1` |
| `articles/Rosace_2023-04-06_NatureCommunications-Supplement-MOESM9.pdf` | 41467_2023_37668_MOESM9_ESM.pdf | 5323105 | `493f8ed429a3554af65f12f15f8d9aee254fc37d860f1a61e0a9045eaddae845` |
| `articles/Rosace_2023-04-06_NatureCommunications-SupplementaryInformation.pdf` | 41467_2023_37668_MOESM1_ESM.pdf | 11867348 | `e468be57aa4305836cfae55409b8d5735dccb84bf7aa88c9c853bda700e1939e` |
| `articles/Rosace_2023-04-06_NatureCommunications.pdf` | s41467-023-37668-6.pdf | 2067869 | `d566a17e666f1183e3562a1c2deb51269163410ade23dda39c7bed2d715ecfc5` |

## 参考文献

- [FLAb 固定版本](https://github.com/Graylab/FLAb/tree/e05e3f0135783ffb7de412df6a1467e7a0031911)。
- [主论文和全部 publisher 附件](https://www.nature.com/articles/s41467-023-37668-6)。
- [PubMed 身份](https://pubmed.ncbi.nlm.nih.gov/37024501/)。
- [1A2P 原始结构论文（RCSB citation DOI）](https://doi.org/10.1107/S0907444998010865)。
- [1ANK 原始结构论文（RCSB citation DOI）](https://doi.org/10.1002/prot.340190304)。
- [1AXB 原始结构论文（RCSB citation DOI）](https://doi.org/10.1021/bi972501b)。
- [1AYF 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/S0969-2126(98)00031-8)。
- [1BOY 原始结构论文（RCSB citation DOI）](https://doi.org/10.1038/370662a0)。
- [1BP2 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/0022-2836(81)90081-4)。
- [1BPI 原始结构论文（RCSB citation DOI）](https://doi.org/10.1107/S0907444995008675)。
- [1BVC 原始结构论文（RCSB citation DOI）](https://doi.org/10.1006/jmbi.1994.0142)。
- [1C2R 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/0022-2836(91)90109-J)。
- [1C9O 原始结构论文（RCSB citation DOI）](https://doi.org/10.1006/jmbi.2000.3602)。
- [1CAH 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/0022-2836(92)90327-G)。
- [1CLW 原始结构论文（RCSB citation DOI）](https://doi.org/10.1006/jmbi.1999.3165)。
- [1CSP 原始结构论文（RCSB citation DOI）](https://doi.org/10.1038/364164a0)。
- [1CYO 原始结构论文（RCSB citation DOI）](https://doi.org/10.1107/S0907444995007827)。
- [1DYJ 原始结构论文（RCSB citation DOI）](https://doi.org/10.1021/bi00008a039)。
- [1FKJ 原始结构论文（RCSB citation DOI）](https://doi.org/10.1107/S0907444994014514)。
- [1FNF 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/S0092-8674(00)81002-8)。
- [1FRD 原始结构论文（RCSB citation DOI）](https://doi.org/10.1021/bi00077a033)。
- [1FTG 原始结构论文（RCSB citation DOI）](https://doi.org/10.1038/nsb0496-329)。
- [1FXA 原始结构论文（RCSB citation DOI）](https://doi.org/10.1021/bi00231a003)。
- [1H7M 原始结构论文（RCSB citation DOI）](https://doi.org/10.1021/BI027131S)。
- [1HFY 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/S0969-2126(96)00075-5)。
- [1HFZ 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/S0969-2126(96)00075-5)。
- [1IO2 原始结构论文（RCSB citation DOI）](https://doi.org/10.1110/ps.48001)。
- [1JIW 原始结构论文（RCSB citation DOI）](https://doi.org/10.1074/jbc.M104020200)。
- [1L63 原始结构论文（RCSB citation DOI）](https://doi.org/10.1021/bi00105a002)。
- [1LZ1 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/0022-2836(81)90125-X)。
- [1M40 原始结构论文（RCSB citation DOI）](https://doi.org/10.1021/ja0259640)。
- [1MGR 原始结构论文（RCSB citation DOI）](https://doi.org/10.1074/jbc.M208425200)。
- [1MSI 原始结构论文（RCSB citation DOI）](https://doi.org/10.1038/384285a0)。
- [1ND4 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/S0022-2836(03)00121-9)。
- [1OH0 原始结构论文（RCSB citation DOI）](https://doi.org/10/bqhq2h)（ShortDOI `10/bqhq2h`；原 DOI `10.1021/BI971546+`）。
- [1OIA 原始结构论文（RCSB citation DOI）](https://doi.org/10.1038/348515A0)。
- [1ONC 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/0022-2836(94)90017-5)。
- [1PGA 原始结构论文（RCSB citation DOI）](https://doi.org/10.1021/bi00181a032)。
- [1PIN 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/S0092-8674(00)80273-1)。
- [1QLP 原始结构论文（RCSB citation DOI）](https://doi.org/10.1110/ps.9.7.1274)。
- [1RGG 原始结构论文（RCSB citation DOI）](https://doi.org/10.1107/S0907444995007669)。
- [1RN1 原始结构论文（RCSB citation DOI）](https://doi.org/10.1021/bi00127a013)。
- [1ROP 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/0022-2836(87)90039-8)。
- [1SHG 原始结构论文（RCSB citation DOI）](https://doi.org/10.1038/359851a0)。
- [1STN 原始结构论文（RCSB citation DOI）](https://doi.org/10.1002/prot.340100203)。
- [1SUP 原始结构论文（RCSB citation DOI）](https://doi.org/10.1107/S0907444996007500)。
- [1TPK 原始结构论文（RCSB citation DOI）](https://doi.org/10.1021/bi00116a037)。
- [1UBQ 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/0022-2836(87)90679-6)。
- [1VQB 原始结构论文（RCSB citation DOI）](https://doi.org/10.1073/pnas.91.6.2071)。
- [2AFG 原始结构论文（RCSB citation DOI）](https://doi.org/10.1021/bi9521755)。
- [2BQA 原始结构论文（RCSB citation DOI）](https://doi.org/10.1006/jmbi.1998.1906)。
- [2CG9 原始结构论文（RCSB citation DOI）](https://doi.org/10.1038/NATURE04716)。
- [2CI2 原始结构论文（RCSB citation DOI）](https://doi.org/10.1021/bi00375a036)。
- [2CRK 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/S0014-5793(98)01355-6)。
- [2HPR 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/S0969-2126(94)00122-7)。
- [2IFB 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/0022-2836(89)90392-6)。
- [2IMM 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/0022-2836(92)90398-4)。
- [2LZM 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/0022-2836(87)90636-X)。
- [2RN2 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/0022-2836(92)90260-Q)。
- [2TRX 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/0022-2836(90)90313-B)。
- [2UYZ 原始结构论文（RCSB citation DOI）](https://doi.org/10.1038/sj.emboj.7601711)。
- [3BCI 原始结构论文（RCSB citation DOI）](https://doi.org/10.1074/jbc.M707838200)。
- [3D2A 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/j.jmb.2008.05.063)。
- [3MBP 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/S0969-2126(97)00253-0)。
- [3WD5 原始结构论文（RCSB citation DOI）](https://doi.org/10.1074/jbc.M113.491530)。
- [451C 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/0022-2836(82)90335-7)。
- [4LYZ 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/0022-2836(74)90598-1)。
- [4NIF 原始结构论文（RCSB citation DOI）](https://doi.org/10.1073/pnas.1417571112)。
- [5AZU 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/0022-2836(91)80173-R)。
- [5CRO 原始结构论文（RCSB citation DOI）](https://doi.org/10.1006/jmbi.1998.1849)。
- [5VNW 原始结构论文（RCSB citation DOI）](https://doi.org/10.1038/s41594-018-0028-6)。
- [5YOY 原始结构论文（RCSB citation DOI）](https://doi.org/10.1002/pro.3407)。
- [6W41 原始结构论文（RCSB citation DOI）](https://doi.org/10.1126/science.abb7269)。
- [7JN5 原始结构论文（RCSB citation DOI）](https://doi.org/10.1371/journal.ppat.1009089)。
- [7PS3 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/j.chom.2021.11.013)。
- [7PS4 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/j.chom.2021.11.013)。
- [7Q0G 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/j.chom.2021.11.013)。
- [7QF0 原始结构论文（RCSB citation DOI）](https://doi.org/10.1084/jem.20220638)。
- [7QU1 原始结构论文（RCSB citation DOI）](https://doi.org/10.1128/mbio.02650-21)。
- [7RXI 原始结构论文（RCSB citation DOI）](https://doi.org/10.1371/journal.ppat.1010409)。
- [7RYU 原始结构论文（RCSB citation DOI）](https://doi.org/10.1038/s41467-022-28424-3)。
- [7S4G 原始结构论文（RCSB citation DOI）](https://doi.org/10.1158/1535-7163.MCT-21-0599)。
- [7SEG 原始结构论文（RCSB citation DOI）](https://doi.org/10.1038/s41375-021-01478-w)。
- [7SG5 原始结构论文（RCSB citation DOI）](https://doi.org/10.1084/jem.20220323)。
- [7SG6 原始结构论文（RCSB citation DOI）](https://doi.org/10.1084/jem.20220323)。
- [7SJS 原始结构论文（RCSB citation DOI）](https://doi.org/10.1126/scitranslmed.abi9215)。
- [7SO5 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/j.crstbi.2022.03.003)。
- [7TP4 原始结构论文（RCSB citation DOI）](https://doi.org/10.1126/scitranslmed.abl9605)。
- [7TTM 原始结构论文（RCSB citation DOI）](https://doi.org/10.1126/scitranslmed.abn6859)。
- [7U8C 原始结构论文（RCSB citation DOI）](https://doi.org/10.1073/pnas.2202439119)。
- [7Z0X 原始结构论文（RCSB citation DOI）](https://doi.org/10.1371/journal.ppat.1010465)。
- [7ZF6 原始结构论文（RCSB citation DOI）](https://doi.org/10.1016/j.cell.2022.05.014)。
- [7ZWI 原始结构论文（RCSB citation DOI）](https://doi.org/10.1038/s41467-022-33379-6)。

使用时保留来源版本、主文和所用捆绑基准的原引用。结构及各 benchmark 的原文引文以原 payload 和 RCSB citation 为准，不能只引用 FLAb。

## 其他

### 数据范围和限制

本次完成定义的公开论文附件快照及 FLAb 子集接入，属于 `processed-public`。完整快照指主文、publisher 15 个补充对象和列明的 PDB/FLAb 范围，不声称取得全部仪器底层数据或作者未发布的实验。

### 完整性与验收

独立验收全部 252 个文件（不含 README），共 108,797,359 bytes；inventory SHA-256 `2b387eb44296f18c0e89682628faf9bb2285756ca5bdc3274b295966799a2088`。规则：逐文件记录 `relative_path<TAB>bytes<TAB>sha256<LF>`，按路径排序后 hash；README 排除，无意外文件。payload 逐文件 hash、表格全部记录/归档全部成员、PDF 全页、XLSX CRC 和全部 sheets 已读；PDB 双层验收如前。hash 固定原件身份，不替代来源、单位或许可核验。

源目录只保留 payload、articles、pdb 和 README，不发布 API JSON、manifest 或验证报告。派生审计/脚本/交接保留开发者 workspace；真实表格/结构未进入 Git。

### 许可和再分发边界

主论文声明 CC BY 4.0；publisher 附件按正文许可和各自 credit line 使用，peer-review 文档不自动等同新的实验数据授权。捆绑稳定性/DMS 基准需保留原论文引用和其原条款；FLAb 代码许可不自动覆盖全部数据。RCSB 文件使用其数据库条款。

### 公开范围对照

| 论文或来源内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 主文及 publisher 15 个补充对象 | 14 PDF（含主文）与 2 XLSX 全部取得、hash/格式核验 | 完成 |
| FLAb 两亲本 8 表 | 76 行端点记录，19 种设计共享 | 完成所选子集 |
| 六亲本完整 KD 汇总 | Source Data Fig S9 48 个位置/47 finite；Table S5 保留误差与缺失 | 取得 |
| 可辩护 PDB 锚点 | 114 FASTA + 114 完整 mmCIF，全部 entity/链序列配对核验 | 完成 |
| 全部底层仪器输出 | publisher 当前交付为汇总/绘图与设计文件 | 不在本快照承诺范围 |
