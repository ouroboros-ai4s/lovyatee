---
- tags:
  - context
---

# SRC_R54_AINTIBODY 数据说明

## 数据集身份

- `source_id`：`SRC_R54_AINTIBODY`
- `source_version`：`snapshot-2026-08-19`
- 原作者或发布机构：M. Frank Erasmus、Andrew R. M. Bradbury 等；Specifica/IQVIA 与 Carterra、Sapidyne、Mosaic、Azenta 等合作方。

## 实验设计和数据口径

AIntibody 在同一 SARS-CoV-2 RBD 靶点上组织三项前瞻性挑战：已有抗体的 CDR 亲和力成熟、限定 HCDR3 簇内的候选排序、设计输入库之外的新 CDR 组合。输入来自展示库筛选及测序汇总，设计提交后合成完整 IgG，在统一测量流程下获得 SPR 动力学/亲和力、选定子集的 KinExA，以及五项成药性指标。公开序列列是轻/重链可变区，不是完整 IgG 常数区序列。

Dataset 1 有 185,097 个唯一 VL/VH 对：一个 parental 和三组 phase-1 分选群；这些没有逐行 KD。Dataset 2 有 32,059 个唯一 VL/VH 对，其中 142 行有有限数值 affinity，31,917 行缺失；relative abundance 是测序筛选比例，不能当成 KD。Dataset 3 有 715 条结果/控制记录、686 个唯一 VL/VH 对，25 组序列对重复。581 行带 KD_SPR（554 个不同序列对）、99 行带 KD_KinExA（94 个不同序列对），后者均已出现在 SPR 有值序列对中。challenge_sequence=True 有 517 行、494 个不同序列对；论文报告 511 个提交，原表布尔筛选口径并不等同于论文最终提交数，不静默删去六行以凑数。

亲和力单位为 M，较小 KD 代表较强结合；SPR association rate 单位 M⁻¹ s⁻¹、dissociation rate 单位 s⁻¹。KinExA 平衡拟合、screening KD estimate 与 SPR 应分开建标签。KD_SPR 的文件值域为 2.2e-11–2.05188e-4 M，KD_KinExA 为 2.92e-12–1.9e-7 M；这是公开有限值范围，不是共同检测范围。SPR protocol/fit 的下边界和失败机制见主文及补充图，不将缺失视为零或非结合。n_spr 在 414 行有值（1–8），其余 301 行缺失；论文所述 replicate 均值不能当成独立抗体样本。

Dataset 3 中 114 行 mean_ka < 1 且 mean_kd 很大，按字段名计算 mean_kd/mean_ka 与 KD_SPR 不一致（相对误差 >10%）；这些行的 ID 以 SP_mAbs2023 为例。98 行能按 VL/VH 连接到 Dataset 2，15 行的两个动力学值与 Dataset 2 的 on_rate/off_rate 精确反置，其余需另核数值精度或上游记录。疑似上游列值反置是有证据的推断；raw 不交换这些值，也不据其生成新 KD。

Dataset 1 的完整序列字符串含 13,415 个 `*` 和 217 个 `X`（按两个 sequence_aa 列累计）；它们被原样保留，不当作标准 20-aa 字母或在 raw 中修复。Dataset 2/3 可变区列通过 20-aa 字母检查。全部工作簿文本扫描未见 Cf 类不可见 Unicode 或 NBSP。

五项成药性结果来自 HIC、BVP、热稳定性 Tm、聚集温度 Tagg 和 AC-SINS；总分越低越好，论文使用 ≤3 的筛选规则。总分在 521 行有值、194 行缺失，值域 0–9；它不是 KD，也不是二元结合标签。按共享亲本、VL/VH 对和 HCDR3 簇分组控制 split 泄漏，组织排名、实验结果和后验成药性不能作为前瞻性预测输入。项目 raw 保存作者的实验汇总与输入表，不等同于仪器导出的全部 sensorgram/event 文件。

## 论文原文

- 标题：A blinded, prospective benchmark of in silico antibody discovery anchored to experimental affinity and developability
- 作者：Erasmus, M. Frank；Bedinger, Daniel；Hopkins, Elizabeth 等。
- 载体与版本：Nature Biotechnology，Version of Record。
- 发布日期：2026-08-19
- DOI：`10.1038/s41587-026-03238-6`
- PMID / PMCID：无（当前 publisher citation metadata 未列出；不据此推断不存在索引记录）
- 本地文件：`articles/AINTIBODY_2026-08-19_Nature-vor.pdf`
- 文件大小：7424151 bytes；30 页。
- SHA-256：`443a79d5dacf447a4dada1727f6b7a87c1ca85a9cd5030cc16edd270ab56fe8e`
- 文本许可：CC BY 4.0，publisher 主文 Rights and permissions。
- 补充材料：两份附属 PDF，分别为 Supplementary Information 与 Reporting Summary；两个 XLSX 为排名汇总和 Data 1–3 实验/输入表。

附属 PDF 保留 publisher MediaObject 文件名，文件身份如下。

| 文件 | bytes | SHA-256 |
| --- | --- | --- |
| articles/41587_2026_3238_MOESM1_ESM.pdf | 21695141 | `abcf7b71a1111902db4e1c89d4fe247bb166bad7cb9f40e63a8a5120f313d83e` |
| articles/41587_2026_3238_MOESM2_ESM.pdf | 3218503 | `228c7123d231b2b94c50ecdd55744a0638e46bc4f03b86e7d586699e00b465b4` |

## 仓库内容

一手入口为 [publisher 论文与补充材料](https://www.nature.com/articles/s41587-026-03238-6)。版本锚点是 2026-08-19 Version of Record；`snapshot-2026-08-19` 来自该发布日期，未使用下载日期。上游是论文补充交付，不是 Git 仓库；无 Git LFS/submodule。

```text
snapshot-2026-08-19/
└── AIntibody/
    ├── 41587_2026_3238_MOESM3_ESM.xlsx
    └── 41587_2026_3238_MOESM4_ESM.xlsx
```

MOESM3 是 Supplementary Tables 1–5 的组织级排名汇总；MOESM4 是合并 Supplementary Data 1–3 的三个 sheet。项目执行清单中“Data 3/4 两个 XLSX”描述与实际交付名称不一致，本次保留原始文件名并按实时 sheet 核验。

## 数据结构

### 输入与实验结果工作簿

MOESM4 三个 sheet 的第 1 行是说明、第 2 行是字段名，实际数据从第 3 行开始。Dataset 1 是 185,097 × 10；Dataset 2 是 32,059 × 16；Dataset 3 是 715 × 70。VL/VH 对可用于跨 sheet 连接，Dataset 3 的 ID 是来源内构建体/提交标识；同一个序列可由多组织提交或作为控制出现。PAPER_ID 的部分组织仍匿名，不能据此恢复贡献方身份。

### 组织级排名工作簿

MOESM3 的 Supplementary Table 1–5 分别对应 C1、C2-27F、C2-28F、C2-47F、C3；数据行数依次 26、27、27、27、24。前四表 18 列、最后一表 17 列；前两表重复出现 Participant 列名，后面有 Comment 或缺少最后列，读取时保留位置不能用字典悄悄丢列。Best/Median Affinity、IQR、Range、百分比和排名中有科学计数字符串、`-`、缺失及区间复合字符串，是组织级汇总，不能扩增为抗体样本。

### 字段说明

| 文件/sheet | 字段（原始拼写） | 原始表示、单位、方向与来源 |
| --- | --- | --- |
| MOESM4 / Dataset 1 | sort_population; Redundancy | parental/三个 phase1 群；测序计数（整数），parental 的 Redundancy 为 `-`；计数不是亲和力。 |
| MOESM4 / 全部 Dataset | sequence_aa_light; sequence_aa_heavy; cdr1_aa_light; cdr2_aa_light; cdr3_aa_light; cdr1_aa_heavy; cdr2_aa_heavy; cdr3_aa_heavy | VL/VH 与 CDR 字符串；Dataset 1 存在 `*`/`X`；无单位，不在 raw 重建常数区。 |
| MOESM4 / Dataset 2 | characterized; lsa_bin; cluster_cdr3_heavy | 是否已表征（布尔）、bin（数值或缺失）、HCDR3 簇（字符串或缺失）。 |
| MOESM4 / Dataset 2 | affinity; on_rate; off_rate | 实验值或缺失；M（低有利）、M⁻¹ s⁻¹、s⁻¹。 |
| MOESM4 / Dataset 2、3 | relative_abundance_10nM; relative_abundance_1nM | 实验筛选测序比例，无单位，或缺失；不能等同于 KD。 |
| MOESM4 / Dataset 3 | PAPER_ID; group; bucket; ID; company_group; cluster; challenge; challenge_sequence; control | 组织/分组/提交/挑战标识，布尔或字符串；缺失存在，控制列有 YES/NO。 |
| MOESM4 / Dataset 3 | sequence_light_heavy; fwr1_aa_light; fwr2_aa_light; fwr3_aa_light; fwr4_aa_light; fwr1_aa_heavy; fwr2_aa_heavy; fwr3_aa_heavy; fwr4_aa_heavy | 上游给定可变区串及框架片段；不是项目推断拼接。 |
| MOESM4 / Dataset 3 | KD_SPR; KD_KinExA; n_spr | SPR/KinExA 实验亲和力（M，低有利）与 SPR replicate 数；缺失不表示零。 |
| MOESM4 / Dataset 3 | mean_ka; mean_kd; stdev_ka; stdev_kd | SPR rate 均值和标准差；字段标称 M⁻¹ s⁻¹ / s⁻¹；114 行存在原始值反置疑点。 |
| MOESM4 / Dataset 3 | STDEV_SPR; RMAX_SPR; STDEV_RMAX_SPR; MEAN_RES_Sd; STDEV_RES_Sd; SPECIFIC_ACTIVITY_SPR; STDEV_SPECIFIC_ACTIVITY_SPR | SPR 汇总及拟合指标；部分为科学计数字符串；RMAX 为响应单位 RU，specific activity 按百分比解释，其余含义需结合补充图/fit，不作输入特征。 |
| MOESM4 / Dataset 3 | KinExA_Screen_KD_Estimate; KinExA_KD_95_CI_LOW; KinExA_KD_95_CI_HIGH; KinExA_activity; KinExA_activity_95_low; KinExA_activity_95_high; KinExA_notes | screening KD estimate 和 95% CI（M），activity 比例与文本 notes；screen estimate 不等于平衡 KD。 |
| MOESM4 / Dataset 3 | PPI; Container; Order ID/Alias; Challenge; Concentration (mg/mL); Mean KD (M); KD Std. Dev. (M) | 外部实验样品/板位/别名及重复汇总；浓度 mg/mL，KD M；Mean KD (M) 不保证与 KD_SPR 字面相等。 |
| MOESM4 / Dataset 3 | HIC RT in gradient (min); # Peaks observed; Main peak area (mAU-min); average BVP score; Tm, C; Tagg, C; average dPW | 成药性实测量：min、计数、mAU-min、BVP score、°C、°C、AC-SINS 波长移位；各项方向/阈值来自主文面板，不能共用单位。 |
| MOESM4 / Dataset 3 | construct performance, HIC RT; construct performance, BVP; construct performance, Tm; construct performance, Tagg; construct performance, AC-SINS; total_developability_score; Count_in_AM_Dataset | 规则判定字符串 Passing/Questionable/Failing 或缺失；总分 0–9（低有利）、输入库计数或缺失，均为后验结果/派生量。 |
| MOESM3 / Table 1–5 | Participant; Company Group; Method Class; Number of submissions; Best Affinity; Best Affinity Instrument; Best Binder Developability Score; Median Affinity; IQR (Q1 - Q3); Range (Min - Max); % Binders; % Dev Binders; DQ Reason; Organization Rank; Top Submission Rank; Pre-DQ Organization Rank; Pre-DQ Top Submission Rank | 组织级派生汇总；Best/Median Affinity 为 M，仪器 SPR/KinExA，`-` 为特殊编码，区间和百分号为复合字符串；部分表末列为 Comment/重复 Participant。 |

### 数据示例

| Dataset 3 / ID | PAPER_ID | bucket | KD_SPR (M) | KD_KinExA (M) | n_spr | total_developability_score |
| --- | --- | --- | --- | --- | --- | --- |
| 1176 | Aureka | C1 | 3.4e-10 | 9.47e-11 | 3 | 0 |

此行来自 Dataset 3 第 3 行，是一个提交/构建体的测量汇总，不是三条独立抗体。Dataset 2 第 3 行为 characterized=True、affinity=2.67e-11 M；Dataset 1 第 3 行为 parental、Redundancy=`-`。

## PDB 数据库

已审计主文、补充 PDF、两个 XLSX 的 PDB/结构线索；未发现逐提交的实验 PDB 连接键。主文描述的 AF3 结构分析属于预测，不当作新实验结构。

采用 [6M0J](https://www.rcsb.org/structure/6M0J) 为 Wuhan SARS-CoV-2 RBD 靶点代表实验结构：RCSB entity 2 描述为 Spike protein S1，author chain E，canonical polymer 229 aa；entity 1/chain A 为 ACE2，603 aa。连接键是主文中的 SARS-CoV-2 RBD 靶点身份，各 Dataset 共享这个代表锚点。SPR/KinExA 的不同 RBD 构建体（包括 RBD+SD1 319–591）并不与 6M0J 严格相等；6M0J 不是本批设计抗体复合物，也不提供逐设计覆盖。

2026-09-18 同时取得 RCSB 原样完整 entry FASTA 和完整 mmCIF，保留全部 entity/链、不剪裁、不嫁接 CDR。FASTA entity 序列与 mmCIF canonical entity 序列精确一致，2 entities、6,571 atoms。

| 文件 | bytes | SHA-256 |
| --- | --- | --- |
| pdb/sequences/rcsb_pdb_6M0J.fasta | 1001 | `0c00927ac0ba87015372fc0c25bfdaa1ab72528aff30789d49bfe2757821c7de` |
| pdb/structures/6M0J.cif | 739607 | `ec1bbd3e64524f4ec91803781fb065bc8bb7559a67b60fcc2bfb5a08dae3cba6` |

原始端点：[FASTA](https://www.rcsb.org/fasta/entry/6M0J/download)、[mmCIF](https://files.rcsb.org/download/6M0J.cif)。PDB 子任务：completed（靶点代表结构层）；逐抗体实验结构层未公开，不能宣传为 715 条结构匹配记录。

## 使用方式

调用者先赋值 dataset_root 为本 source version 路径。

```python
from pathlib import Path
import openpyxl
workbook = openpyxl.load_workbook(
    Path(dataset_root) / "AIntibody/41587_2026_3238_MOESM4_ESM.xlsx",
    read_only=True, data_only=False,
)
rows = workbook["Dataset 3"].iter_rows(min_row=2, values_only=True)
headers = next(rows)
first_record = dict(zip(headers, next(rows)))
```

保留数值字符串和空单元格；MOESM3 存在重复 header，需要按列位置读取。

## 采集过程记录

1. 2026-09-18 读取 project/developer 配置并运行项目 context；确认工作文档归 wuhuawei、数据根由 project.toml 提供。
2. 从 publisher 实时网页枚举四个补充对象，核验 DOI、发布日期、标题和 CC BY 4.0；发现清单对 XLSX 名称的描述漂移，按真实 sheet 修正解释，保留原始文件名。
3. 使用带失败重试的下载器写入 `SRC_R54_AINTIBODY/.staging/snapshot-2026-08-19.partial`。直连超时后使用已配置环境代理；未关闭 TLS 校验，未保存签名跳转 URL 或认证信息。
4. 主文原始名 s41587-026-03238-6.pdf 从通用入口保存为 AINTIBODY_2026-08-19_Nature-vor.pdf；下载字节直接落入新文件名，没有 PDF 改写，7,424,151 bytes 与 SHA-256 在重新读取时一致。两份附属 PDF 的原始对象名保留；全部 PDF 经过页数/首页面身份核验。
5. 独立扫描所有八个工作簿 sheet、值域/缺失/序列字符/不可见 Unicode、VL/VH 重复及测量覆盖；进一步用 Dataset 2 连接核对 114 行动力学疑点。发现上游问题后保留 raw 字节，README 明示边界。
6. 复用共享 raw 中的 6M0J RCSB 原样文件并独立核对 FASTA/mmCIF entry/entity/atoms；没有从其他开发者 workspace 导入代码。
7. 本地 README 每次写入立即同步 staging/正式目录；固定版本 markdownlint、全部文件 SHA-256、真实文件集合与 PDB pair 校验通过后，由 publish.py 原子重命名发布。此 source 是 processed-public 公开处理包接入；handoff/状态记录随发布同步，不声称完整仪器原始文件已获得。

## 参考文献

- [Erasmus et al. 2026，正式主文及补充交付](https://doi.org/10.1038/s41587-026-03238-6)。
- [AIntibody 作者维护页面](https://www.aintibody.org/)。
- [6M0J，Lan et al. 原始实验结构](https://doi.org/10.2210/pdb6M0J/pdb)；[原始结构论文](https://doi.org/10.1038/s41586-020-2180-5)。

## 其他

### 完整性与验收

两个 payload 文件、三份 article PDF 与一对 PDB 补充构成明确文件集合；工作簿全部 sheet 可读、无 raw 改写。下载站未公布文件 checksum，以下 SHA-256 为本次独立读取得到的身份摘要，不冒充官方 checksum。

| 相对路径 | bytes | SHA-256（本地计算） |
| --- | --- | --- |
| AIntibody/41587_2026_3238_MOESM3_ESM.xlsx | 35525 | `0d304d9f4dbbb8ef6355da86c2d3b4434e68278b3b0f213eb21340b56249c96e` |
| AIntibody/41587_2026_3238_MOESM4_ESM.xlsx | 12633679 | `ebab6cc496a636ab3cadaabd25d89e1dcbf69fadca533fc829c50bfeec500c20` |

### 许可和再分发边界

主文为 CC BY 4.0，publisher 声明其第三方材料除另有 credit line 外在此许可范围内；所下载工作簿未见独立限制性许可或 credit line。Data availability 的“无访问限制”不独自构成许可依据，数据引用仍需保留主文、对象名和本 snapshot；PDB 遵守 RCSB/wwPDB 引用政策。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 全部处理后输入与序列-结果映射 | MOESM4 Dataset 1–3 | 已包含 |
| SPR/KinExA、五项成药性指标 | Dataset 3 的 70 列；不同方法和缺失独立保留 | 已包含公开汇总 |
| 完整仪器级 sensorgram 或测序 reads | 补充 PDF 是图；XLSX 不是事件文件，当前四个对象未发现完整仪器包 | 未取得 |
| 逐设计实验复合物 | 表中无逐提交实验 PDB 键；另补 6M0J 只作靶点代表 | 未公开/未确认 |
