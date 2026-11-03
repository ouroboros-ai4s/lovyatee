---
tags:
  - context
---

# ToDo List

- [ToDo List](#todo-list)
  - [1. Data ETL Specification](#1-data-etl-specification)
  - [2. Data ETL SRC-by-SRC](#2-data-etl-src-by-src)
    - [第一批: 小型、结构或字段较清楚](#第一批-小型结构或字段较清楚)
    - [第二批: 中型、多构建体或需要结构重建](#第二批-中型多构建体或需要结构重建)
    - [第三批: 大型或存在跨源重复](#第三批-大型或存在跨源重复)
  - [3. Data ETL Merge](#3-data-etl-merge)

## 1. Data ETL Specification

- [x] 固定 [`3A = (3A_ID, antibody, antigen, affinity[])`](2026-10-28-ab-ag-data-diversity/3a_src_data_etl_modeling.md).
- [x] 定义 [VH/VL/VHH 序列清洗、signal peptide、constant region、linker、His-tag 处理规则](2026-10-28-ab-ag-data-diversity/3a_src_data_etl_problem_ab.md).
- [x] 定义 [抗原实验片段的序列和结构截取规则](2026-10-28-ab-ag-data-diversity/3a_src_data_etl_problem_ag.md).
- [ ] 定义 `AB_ID`、`AG_ID`、`3A_ID` 的稳定 hash.
- [ ] 定义 affinity 的 `label_type`、单位、截断符号、assay、condition、replicate、source 保存方式.

## 2. Data ETL SRC-by-SRC

### 第一批: 小型、结构或字段较清楚

- [ ] `R03 AbDesign 1.0` [src-03-abdesign-1-0.md](2026-10-30-3a-src-inventory/src-03-abdesign-1-0-inventory.md).
- [ ] `R08 AVIDa-hTNFa` [src-08-avida-htnfa.md](2026-10-30-3a-src-inventory/src-08-avida-htnfa-inventory.md).
- [ ] `R74 AbDesign 2.0` [src-74-abdesign-2-0.md](2026-10-30-3a-src-inventory/src-74-abdesign-2-0-inventory.md).
- [ ] `R76 TDC AntibodyAff` [src-76-tdc-antibodyaff.md](2026-10-30-3a-src-inventory/src-76-tdc-antibodyaff-inventory.md).
- [ ] `R77 Akbar SAbDab Kd CSV` [src-77-akbar-sabdab-kd-csv.md](2026-10-30-3a-src-inventory/src-77-akbar-sabdab-kd-csv-inventory.md), (与 R76 做逐行重复验证，只保留一个 canonical measurement).
- [ ] `R80 ANTIPASTI` [src-80-antipasti.md](2026-10-30-3a-src-inventory/src-80-antipasti-inventory.md).

### 第二批: 中型、多构建体或需要结构重建

- [ ] `R13 ANDD` [src-13-andd.md](2026-10-30-3a-src-inventory/src-13-andd-inventory.md).
- [ ] `R11 AbBiBench` [src-11-abbibench.md](2026-10-30-3a-src-inventory/src-11-abbibench-inventory.md).
- [ ] `R16 Guest antibody benchmark` [src-16-guest.md](2026-10-30-3a-src-inventory/src-16-guest-inventory.md).
- [ ] `R14 AB-Bind` [src-14-ab-bind.md](2026-10-30-3a-src-inventory/src-14-ab-bind-inventory.md), (需要判断 mutation record 是否能可靠重建抗体序列).
- [ ] `R15 SKEMPI 2.0` [src-15-skempi-2-0.md](2026-10-30-3a-src-inventory/src-15-skempi-2-0-inventory.md), (需要处理 WT/mutant、突变字符串和 reference structure).
- [ ] `R20 SAbDab / SAbDab2` [src-20-sabdab-sabdab2.md](2026-10-30-3a-src-inventory/src-20-sabdab-sabdab2-inventory.md), (本身无 affinity，作为结构和序列解析资源，不直接产生 3A affinity pair).
- [ ] `R50 Graphinity` [src-50-graphinity.md](2026-10-30-3a-src-inventory/src-50-graphinity-inventory.md), (computational ddG 单独保存 label type，不与实验 Kd 混合).
- [ ] `R75 HER2-aff-large / Buzz` [src-75-her2-aff-large-buzz.md](2026-10-30-3a-src-inventory/src-75-her2-aff-large-buzz-inventory.md), (主要只有 CDR-H3，不能直接构成完整 Fv/VHH).

### 第三批: 大型或存在跨源重复

- [ ] `R79 AlphaBind public experiments` [src-79-alphabind.md](2026-10-30-3a-src-inventory/src-79-alphabind-inventory.md).
- [ ] `R23 MIT-LL AlphaSeq` [src-23-mit-ll-alphaseq.md](2026-10-30-3a-src-inventory/src-23-mit-ll-alphaseq-inventory.md), (predicted affinity 与空 label 分开处理).
- [ ] `R78 MochiBind sampled data` [src-78-mochibind-sampled-data.md](2026-10-30-3a-src-inventory/src-78-mochibind-sampled-data-inventory.md), (作为 AlphaBind 子集做重复检测).
- [ ] `R10 AbRank` [src-10-abrank.md](2026-10-30-3a-src-inventory/src-10-abrank-inventory.md), (与 R09 内嵌 AbRank 数据做 measurement-level 去重).
- [ ] `R09 FLAb` [src-09-flab.md](2026-10-30-3a-src-inventory/src-09-flab-inventory.md), (规模大，包含多个重复来源和多种 antibody format).
- [ ] `R12 ASD / AgAb DB` [src-12-asd-agab-db.md](2026-10-30-3a-src-inventory/src-12-asd-agab-db-inventory.md), (最大汇编源，最后处理，避免重复计数).

## 3. Data ETL Merge

- [ ] 逐源输出 source-local canonical records。
- [ ] 按规范化 `(AB_ID, AG_ID)` 做跨源 pair 去重。
- [ ] 将同一 pair 的全部 affinity observations 聚合为 `affinity[]`。
- [ ] 保留 source provenance、原始 record ID 和重复判定原因。
- [ ] 生成 sequence/structure coverage、reject reason、label type 和 source overlap 统计。
- [ ] 输出 Parquet shards、全局 manifest、schema 和可复现运行日志。
- [ ] 随机抽样人工检查 3A_ID、VH/VL/VHH、抗原片段和结构链映射。
