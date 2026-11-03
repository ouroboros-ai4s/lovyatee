---
- tags:
  - context
---

# SRC_R44_KIRBY 数据说明

## 数据集身份

- `source_id`：`SRC_R44_KIRBY`
- `source_version`：`snapshot-2024-06-21`
- 原作者或发布机构：Monica B. Kirby、Brian M. Petersen 等；Timothy A. Whitehead 课题组

### 来源方背景

Timothy A. Whitehead 是科罗拉多大学博尔德分校化学与生物工程系副教授。课题组官方研究页将其方向概括为蛋白质设计与工程，并结合下一代测序和高通量筛选研究蛋白质的亲和力、特异性与可演化性；R44 的抗体回溯文库和 MAGMA-seq 测量正属于这一技术脉络。

## 实验设计和数据口径

回溯八个 SARS-CoV-2 抗体从 inferred unmutated common ancestor（UCA）到成熟亲本的不同突变组合，构建配对 VH/VL Fab 文库，以酵母展示、S1 多浓度筛选和 barcode 测序获得计数；MAGMA-seq maximum likelihood estimator 拟合单价 Kd、最大荧光 Fmax 与置信区间。YL009/YL011 在 2.5–2,000 nM S1 浓度取样，部分浓度 Fc-PE stock 的亮度差异用作者 α=0.5345 校正。Kd 是高通量实验支持的拟合结果，不是每行独立 SPR 测量。

论文八个 focus parents 为 4A8、2-15、CC6.31、C118、1-20、CC12.1、1-57 和 002-S21F2；其中 4A8/CC12.1 结果复用 R42，CC12.1 还作内部对照。实际仓库两张 MLE 表为 1,356 和 1,878 条，各自 Variant 唯一，跨表共享 705 个 Variant，并集 2,529；Ab 列实际另含少量 2-7、5-7、C022 记录，不把全部 raw 行当成论文已过滤的八亲本结果。YL009 的 Success=True/False 为 818/538；YL011 为 901/977。Kd=20,000 的原始记录分别 415/336 条，Kd=0.01 分别 5/2 条。零 CI、求解边界与失败拟合应保留状态，不能当精确连续标签。

论文回归分析过滤 convergence=True、Avg_counts>500、CI upper>0、Kd<3,000 nM；特定 Figure 3 则用 Avg_counts>250。raw 表保留过滤前结果，不能混用这些口径。CDRH3 回溯库因亲和力太弱改用浓度加权分选概率的 −ln correlative binding score，方向越低结合越强；仅对 reference counts>1,000 的变体计算。该代理评分没有 KD 单位，Pgen/LL 是生成概率及其日志表示，不能作为新实测亲和力。底层 reads 的三个 SRA projects 本批未获取。

## 论文原文

- 标题：Retrospective SARS-CoV-2 human antibody development trajectories are largely sparse and permissive
- 作者：Monica B. Kirby, Brian M. Petersen, Jonathan G. Faris, Siobhan P. Kells, Kayla G. Sprenger, Timothy A. Whitehead
- 发表来源：PNAS 122(4), e2412787122，正式发表版；本地保存当前 DOI 对应的 PDF 与完整 PMC XML
- 发布日期：2025-01-22
- DOI：`10.1073/pnas.2412787122`
- PMID / PMCID：39841142 / PMC11789010
- 归档文本版本：正式发表版 PDF 与完整 XML
- 本地文件：`articles/Kirby_2025-01-22_PNAS-v1.pdf`；`articles/Kirby_2025-01-22_PNAS-v1.xml`
- 文件大小：articles/Kirby_2025-01-22_PNAS-v1.pdf = 6.37 MiB（6683298 bytes）；articles/Kirby_2025-01-22_PNAS-v1.xml = 162.18 KiB（166075 bytes）
- SHA-256：articles/Kirby_2025-01-22_PNAS-v1.pdf = `70cfda05dfbd241271c4bcbb0f150bf236b36d1b2cffbde5b37b992c26d4cd4d`；articles/Kirby_2025-01-22_PNAS-v1.xml = `cc52d128ecc53826be17405f2507f5caa7ea08f300aad847dc2fba609f74bb77`
- 文本许可：CC BY-NC-ND 4.0
- 补充材料：3 个公开附件，详见下表

| 文件 | 角色 | 大小 | SHA-256 |
| --- | --- | --- | --- |
| articles/Kirby_2025-01-22_PNAS-v1-dataset2.xlsx | Dataset S2 | 101.49 KiB（103923 bytes） | `cc7f76c47c48240b34d2c53f81babc68d898cbc323abf210d0d2711619546126` |
| articles/Kirby_2025-01-22_PNAS-v1-appendix.pdf | SI Appendix | 9.34 MiB（9794713 bytes） | `a485aff32f1daeccc662117613364334470658e8ef6b8dcfe561b24e459de781` |
| articles/Kirby_2025-01-22_PNAS-v1-dataset1.xlsx | Dataset S1 | 10.28 MiB（10776886 bytes） | `ed03cd8a1e0827c2bdf3bb1afd0e7870601f6fa1014e2e72f51a0a44c9e844fe` |

主文 PDF、完整 XML、SI Appendix 和 Dataset S1/S2 均已归档并核对 DOI 或文件身份；补充 ZIP 为 18,667,148 bytes，CRC 全部通过。论文及附件采用 CC BY-NC-ND 4.0。OpenAlex 在 2026-09-24 返回该正式论文被引 8 次；这是动态元数据快照，不是数据质量分数。仓库许可须按仓库自己的 MIT LICENSE 判断，不能用论文许可替代。

## 仓库内容

上游固定版本：[一手入口](https://github.com/WhiteheadGroup/Ab_retrospective_trajectories/tree/260cbd5b938db2c5b9b4e3a94fce35517234da20)。revision/commit `260cbd5b938db2c5b9b4e3a94fce35517234da20`，上游版本日期 `2024-06-21T19:16:13Z`；当前 source version 为 `snapshot-2024-06-21`，日期不是本次下载日期。

固定 commit 的完整 codeload archive，22 个 Git blob（包括根目录和 `CDRH3/` 内的 MIT LICENSE）全部按 tree 名称、大小与 blob SHA-1 验证；原归档不重压缩。主文和公开结果附件单独归档于 `articles/`，不把它们误称为仓库原有文件。

```text
snapshot-2024-06-21/
└── Ab_retrospective_trajectories/
    └── Ab_retrospective_trajectories-260cbd5b938db2c5b9b4e3a94fce35517234da20.tar.gz
```

压缩包内部为两个 MLE output CSV、50thpctKds.csv、CDRH3/data/ 下八个原表，以及过滤、制图和 regression notebooks。上游 README 只有标题，不能替代实际字段与论文方法。

## 数据结构

### MLE 结果与计数层级

仓库全部 11 张 CSV 已读取，共 59,378 条表格记录，包含重复浓度/bin/barcode 表示，不是 59,378 个独立抗体。YL009 和 YL011 schema 不完全相同：前者有 ER，后者有 Pijk/Modelijk；共同字段为 Variant、Kd、Fmax、Success、LL、Rijk、Concentrations、sorted fractions、Avg_counts、X^2_red_min、95% CI low/high、n、dg 和 Ab。列表列以字符串形式保留，不能按 CSV 行里的列表元素拆出独立抗体。

### CDRH3、序列与派生表

map_rep1/2 有 3,075/3,878 个 barcode 映射，rep1/2_combined 为 23,205/21,804 条 barcode×浓度/bin 计数；collapsed 为 2,005/1,967 条 Variant 聚合计数；probs.csv 196 条 Variant/Pgen/LL。YL013_YL014_wt.csv 七行使用 DNA seq，而非 AA。map 表 VH/VL 也是 DNA，第一条记录的 VL 与 VH 相同且 Gene_L 标作 VH；保留上游异常，不擅自认定真实配对轻链。Variant 是亲本+链+突变/密码子描述，不是完整氨基酸序列。50thpctKds.csv 七行是 Step×七亲本中位数派生摘要，不是额外 Kd 测量。

### 正式出版方附件

Dataset S1 为 26 个 sheets：README、YL009/YL011/YL013/YL014 barcode counts、两套 MLE all/filter、Rep comparison、两个 Score、Figure4A、六亲本 regression weights 和 Prob_OHE、VH3-53 antibodies。YL009/YL011 counts 分别 52,886/70,199 行，对应 1,394/1,918 个 Variant。附件 YL009 MLE all 1,356 行，与 Git 同键的 Kd/Fmax/CI/Success 一致；YL011 MLE all 1,894 行，比固定仓库多 16 个 Variant，1,878 个同键行中又有 1,707 行的 Kd/Fmax/CI 或 Success 至少一项不同。两者是不同结果版本，不能用附件静默覆盖 Git 表。两个 filtered sheets 的有效 Variant 行分别 515/526；Rep comparison 283 行；Score YL013/YL014 有 98/118 条有效记录，Excel max_row=1,000 是空白扩张。

Score 的实验代理评分 Score 越低越强，ll_IGoR、ll_AntiBERTy、ll_iglm 为模型/生成评分，不能把它们当实验标签或输入特征用于同终点评估。VH3-53 antibodies 有 537 个非空行，是额外参考 metadata 表；含 VH/VL AA、CDR、原始引用、模型/结构链接和 Excel 公式，不是新增 537 个本研究测定 KD。weights sheets 有两套多区域表头，Prob_OHE 为派生图表/模型输入，不是 KD 测量。

Dataset S2 有 Gene Blocks（50 个非空行）、Primers（34）、HCDR3 OligoPool（75）三个 DNA/构建体资料 sheets，物理行分别 963/911/999；未将这些资料误称成标准配对 AA 标签集。SI Appendix Table S6 提供原始 GenBank 版本化 accession，作为外部连接线索，不在 raw 中翻译、替换或拼接序列。

### 字段说明

| 文件或表 | 原始字段 | 类型/单位/方向 | 缺失、边界及来源 |
| --- | --- | --- | --- |
| 两个 MLE CSV | Variant / Ab | 变体复合标识、UCA 亲本键 | 保留 VH/VL 分隔及密码子；跨表 705 重复 Variant；非完整 AA |
| 两个 MLE CSV | Kd / Fmax | Kd nM 越低越强；Fmax 荧光量 | 求解边界 Kd 0.01/20,000、Fmax 5,000/90,000；失败状态不能忽略 |
| 两个 MLE CSV | Success / LL / X^2_red_min / Avg_counts | 拟合状态、似然/统计量、平均 counts | 后验拟合诊断；不作为仅序列预测任务的输入特征 |
| 两个 MLE CSV | 95% CI low / 95% CI high | 原始置信区间表示，与 Kd 拟合关联 | 存在零及异常排序表示，不在 raw 静默替换 |
| 两个 MLE CSV | Rijk / Concentrations / sorted fractions / n | 列表字符串；读数、nM 浓度、分选份额及点数 | YL009 另有 ER；YL011 另有 Pijk/Modelijk；顺序与浓度关联 |
| 两个 MLE CSV | dg | 上游计算的派生值 | 不能把列名理解为另一次自由能实验；使用前核对作者算法 |
| map_rep1/2.csv | Barcode / VH / VL / Gene_H / Gene_L / Variant[_L] | barcode、DNA 序列及链/突变注释 | 有 VL 实际标注 VH 的原始异常；不可直接当 AA 配对序列 |
| combined/collapsed CSV | Rijk / Rjk / Concentration / Bin / Hj / Gj / Nk / Njk / ref_\* | 测序计数、nM 浓度及分选/reference 参数 | 多浓度、多 bin、replicate 与聚合层级相互关联 |
| probs.csv | Variant / Pgen / LL | 生成概率和上游 log-likelihood | 不是 KD 或 neutralization；勿作为新增实验标签 |
| 50thpctKds.csv / wt.csv | Step / 各亲本；gene / seq / \*_start / \*_end | 派生中位数 nM；DNA 构建体与位置参数 | wt.csv 有原始尾部空列；不补全或重建蛋白 |
| Dataset S1 MLE all/filter | Variant / Kd / Fmax / Success / CI / Ab | 原拟合 nM 与诊断 | 附件比 Git 多 16 个 Variant，且 1,707 个同键拟合结果有差；不能静默合并/替换 |
| Dataset S1 Score YL013/YL014 | Score / ref_count / [浓度]nM / ll_IGoR / ll_AntiBERTy / ll_iglm | Score 无 KD 单位、越低越强；模型 log-likelihood 为预测/生成信息 | 有效评分 98/118 条，NS/not seen 与缺失不填零；不要将后验/模型分数混作实测 KD |
| Dataset S1 VH3-53 antibodies | VHorVHH / VL / CDRH3 / CDRL3 / 原始引用和链接 | 参考氨基酸与 metadata，含 Excel 公式 | 537 非空行不是本研究全部新增测量；formula 未在 raw 求值或改写 |
| Dataset S1 weights / Prob_OHE | LASSO / Ridge / Coefficient / OHE_Prob 或 prob_OHE | 派生模型/编码资料，无额外实验单位 | 多区域表头；不得按 max_row 算独立实验样本 |
| Dataset S2 | Name / Sequence / Purpose / Oligos in HCDR3 Oligo Pool | DNA/构建体资料原样文件 | 保留大小写和 N 等原始字符，不声称完整 AA 训练表 |

### 数据示例

来自 `YL009_MLEoutput_variants_bright_adjust.csv` 的第一条真实记录（仅摘录下列列）：

```json
{
  "Variant": "002-S21F2_UCA>VH:G25A-GCT;Q112Q-CAA|002-S21F2_UCA>VL:WT",
  "Kd": "20000.0",
  "Fmax": "5000.0",
  "Success": "False",
  "95% CI low": "0.0",
  "95% CI high": "0.0",
  "Ab": "002-S21F2_UCA"
}
```

这条真实记录同时落在 Kd/Fmax 边界且 Success=False、CI=0，适合说明为什么仅提取 Kd 数值会混淆有效测量与失败/边界结果。

## PDB 数据库

审计完整仓库与论文 structure 引用，并按亲本名称核对 RCSB experimental entries。接受六个 mature-parent 复合物参考锚点：4A8→7C2L，CC12.1→6XC3，2-15→7L5B，C118→7RKV，1-57→7LS9，002-S21F2→7U0P。亲本键 Ab/Variant 可将多条突变记录关联到共享参考 entry，但这些坐标不是回溯 UCA 或每个设计变体的结构。1-20、CC6.31 尚未接受可靠实验复合物锚点，覆盖为 partial；不能以六个结构声称八亲本全覆盖。

取得日期：2026-09-18。每个唯一 entry 保留完整 RCSB canonical entity FASTA 与完整沉积坐标，不选择性截断、不拼接设计序列。实体/链从 mmCIF `_entity` / `_entity_poly` 核对；canonical 序列与 FASTA entity 一致，坐标 `_entry.id` 与 PDB ID 一致，原子记录非空。

| PDB | 连接关系及证据 | polymer entity / author chains /长度 | FASTA/mmCIF |
| --- | --- | --- | --- |
| 7C2L | 4A8 共享亲本参考；Kirby Results 明确重复使用 R42 的 4A8 数据；R42 Fig. 3f | 1:A,B,C:1283aa；2:H,I,J:458aa；3:L,M,N:219aa | 两层 verified |
| 6XC3 | CC12.1 共享亲本参考；Kirby Results 明确重复使用 R42 的 CC12.1 数据；R42 Fig. 3g | 1:H:222aa；2:L:221aa；3:A:217aa；4:B:220aa；5:C:231aa | 两层 verified |
| 7L5B | 2-15 共享亲本参考；Kirby 主文亲本名称 + RCSB 2-15 heavy/light 实体名称 | 1:A:239aa；2:H:227aa；3:L:216aa | 两层 verified |
| 7RKV | C118 共享亲本参考；6P spike 不是实际 S1 construct；Kirby 主文亲本名称 + RCSB C118 实体及条目题名 | 1:A,B,C:1271aa；2:D,E,G:239aa；3:H,F,L:217aa | 两层 verified |
| 7LS9 | 1-57 共享亲本参考；Kirby 主文亲本名称 + RCSB 1-57 heavy/light 实体名称 | 1:A,B,C:1288aa；2:H,D,E:244aa；3:L,F,G:215aa | 两层 verified |
| 7U0P | 002-S21F2 共享亲本参考；Kirby 主文亲本名称 + RCSB 002-S21F2 条目题名 | 1:A,B,C:1208aa；2:E,D:449aa；3:I,F:215aa | 两层 verified |

| 文件 | 大小 | SHA-256 |
| --- | --- | --- |
| pdb/sequences/rcsb_pdb_7C2L.fasta | 2.18 KiB（2235 bytes） | `cd046ce4f10a78aba207e9604dc61f6fe6a5228a9bdfc9ee706947fff5cd1864` |
| pdb/structures/7C2L.cif | 4.01 MiB（4201655 bytes） | `3ecd808e0ee9c1e752de9a59c4a70bbb241b655be8ac64ee74354da272cbabd9` |
| pdb/sequences/rcsb_pdb_6XC3.fasta | 1.43 KiB（1467 bytes） | `bc7fb89cebb951769e7aaef2cbce5d6e4e1266de98fc775787456b165231f63b` |
| pdb/structures/6XC3.cif | 893.78 KiB（915233 bytes） | `24b820c5935e1ea7b2186d92ea5298e074e376cb6014a4d012be77d751ddc054` |
| pdb/sequences/rcsb_pdb_7L5B.fasta | 898 bytes | `72f3d25c83eefa8146f4d30d174a2c1007c24bf994e0a5cd5fb6cf4e92b1a5e7` |
| pdb/structures/7L5B.cif | 501.86 KiB（513908 bytes） | `d680845461302add139924c85874e7facbe19c4e743165ee3064bc0bc9e705da` |
| pdb/sequences/rcsb_pdb_7RKV.fasta | 1.95 KiB（1998 bytes） | `433b6e0e7db363457ede1e30a1cb6d83b0751e6aa3c34d11bdf93ac3d4b8a4c6` |
| pdb/structures/7RKV.cif | 3.31 MiB（3466278 bytes） | `0a02b88f0f7d19982212b9addbe0d7e055f090bf69acec242e103768da6739b8` |
| pdb/sequences/rcsb_pdb_7LS9.fasta | 1.98 KiB（2026 bytes） | `a62f5696dfc36d4b61e539d3dd6ea4a9a52afdd4998e82475d91a2d651a200a4` |
| pdb/structures/7LS9.cif | 3.29 MiB（3451236 bytes） | `947d95331590e4c9d424c16bdba1bc0b5fe3cab5ed670360d1169f45caf4d416` |
| pdb/sequences/rcsb_pdb_7U0P.fasta | 2.07 KiB（2115 bytes） | `d872612842e1440ccfcf23177acd7a1f2a860d8de5c1a4052cf627fa310ee282` |
| pdb/structures/7U0P.cif.gz | 725.20 KiB（742607 bytes） | `9f7aef27c30ecb552a43a69887d1f6ca40e5119cff8e3f203035105c89f32ece` |

共 6 个有效锚点、6 个 FASTA、6 个 mmCIF，12.69 MiB（13301656 bytes）。每个下载使用 `https://www.rcsb.org/fasta/entry/<PDB_ID>/download` 与 `https://files.rcsb.org/download/<PDB_ID>.cif`；共享已存 gzip 坐标直接原样复用，未重压缩。完整 entry 可含未参与该研究的抗体/实体；链身份与映射边界按上表及下文使用。

7C2L 的 4A8 H/I/J 与 L/M/N 为重轻链；6XC3 的 CC12.1 为 B/A，另含 CR3022 H/L，勿误选。7L5B 2-15 为 H/L；7RKV C118 为 D/E/G 与 H/F/L，抗原为 6P spike，并非本研究 S1 构建体。7LS9 1-57 为 H/D/E 与 L/F/G；7U0P 002-S21F2 为 E/D 与 I/F。完整 entry 包含不参与该源的其他实体/构建体，不推断拼接变体序列。

## 使用方式

```python
from pathlib import Path
import tarfile
import csv
import io
root = Path(dataset_root)
archive = next((root / 'Ab_retrospective_trajectories').glob('*.tar.gz'))
with tarfile.open(archive) as package:
    member = next(m for m in package if m.name.endswith('/YL009_MLEoutput_variants_bright_adjust.csv'))
    rows = list(csv.DictReader(io.TextIOWrapper(package.extractfile(member))))
```

保留 Variant、Ab、Success、CI 和浓度关系；按具体分析口径解释 raw 结果。

## 采集过程记录

2026-09-18：通过 GitHub 官方 API 固定 2024-06-21 commit，完整归档并逐 blob 验收，读取所有 11 张 CSV 与作者过滤脚本；核对跨库共享 Variant 和 DNA 字段异常。

2026-09-18：以 DOI、PMID/PMCID 交叉核对正式主文 XML，读方法、八亲本与公开范围；记录 MAGMA-seq 4A8/CC12.1 复用。对 Europe PMC 补充 ZIP 延长下载时限并检查 CRC 后才接受对象。六个已接受 PDB 锚点 FASTA/mmCIF 均验收，未伪造余下两个亲本的映射。

2026-09-18：公开附件包完整下载，三项 CRC 校验通过并原样提取；阅读所有 29 个 XLSX sheets 与 SI Appendix。区分 Excel 物理行/有效记录，记录附件 YL011 all 1,894 与固定 Git CSV 1,878 的 16 行键差额，以及 1,707 个同键拟合结果差异。

2026-09-24：复核 codeload 内根目录与 `CDRH3/` 的 LICENSE，确认固定仓库采用 MIT；通过 PMC 公开下载校验取得 11 页正式 PDF，并更新 OpenAlex 引用数快照。

2026-09-24：论文/补充的下载身份和通用名修正留痕如下；原始文件与描述性落盘名对应的大小和 SHA-256 均已核对，重命名没有改写内容。

| 下载一手 URL | 原始名 | 落盘路径 | 大小 |
| --- | --- | --- | --- |
| <https://pmc.ncbi.nlm.nih.gov/articles/PMC11789010/pdf/pnas.202412787.pdf> | pnas.202412787.pdf | articles/Kirby_2025-01-22_PNAS-v1.pdf | 6.37 MiB（6683298 bytes） |
| <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11789010/fullTextXML> | fullTextXML | articles/Kirby_2025-01-22_PNAS-v1.xml | 162.18 KiB（166075 bytes） |
| <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11789010/supplementaryFiles?includeInlineImage=false> | pnas.2412787122.sd02.xlsx | articles/Kirby_2025-01-22_PNAS-v1-dataset2.xlsx | 101.49 KiB（103923 bytes） |
| <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11789010/supplementaryFiles?includeInlineImage=false> | pnas.2412787122.sapp.pdf | articles/Kirby_2025-01-22_PNAS-v1-appendix.pdf | 9.34 MiB（9794713 bytes） |
| <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11789010/supplementaryFiles?includeInlineImage=false> | pnas.2412787122.sd01.xlsx | articles/Kirby_2025-01-22_PNAS-v1-dataset1.xlsx | 10.28 MiB（10776886 bytes） |

2026-09-24：本地 README 编辑后立即同步共享 staging，固定 markdownlint-cli2 0.20.0 按 skill 配置检查。发布、残留清理和当前缺口同步到本批交接；source version 不另发布 manifest、API 响应或审计文件。完整研究 acquisition 与本次公开包接入分开记录。

## 参考文献

- [固定上游数据版本](https://github.com/WhiteheadGroup/Ab_retrospective_trajectories/tree/260cbd5b938db2c5b9b4e3a94fce35517234da20)
- [主论文 DOI](https://doi.org/10.1073/pnas.2412787122)
- [当前官方 GitHub 仓库](https://github.com/WhiteheadGroup/Ab_retrospective_trajectories)
- [Whitehead 课题组官方研究页](https://www.colorado.edu/faculty/whitehead/research)
- [正式 PMC 全文与补充清单](https://pmc.ncbi.nlm.nih.gov/articles/PMC11789010/)
- [复用的 MAGMA-seq 研究](https://doi.org/10.1038/s41467-024-48072-z)
- [PDB 7C2L 及其原始结构论文](https://www.rcsb.org/structure/7C2L)
- [PDB 6XC3 及其原始结构论文](https://www.rcsb.org/structure/6XC3)
- [PDB 7L5B 及其原始结构论文](https://www.rcsb.org/structure/7L5B)
- [PDB 7RKV 及其原始结构论文](https://www.rcsb.org/structure/7RKV)
- [PDB 7LS9 及其原始结构论文](https://www.rcsb.org/structure/7LS9)
- [PDB 7U0P 及其原始结构论文](https://www.rcsb.org/structure/7U0P)

## 其他

### 完整性与验收

上游数据 payload 1 个文件、3.03 MiB（3177135 bytes）；其中核对 Git blob 身份的文件 22 个。文件 inventory 按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接的 SHA-256：`79bb1406af1a4fb29e2f007925edf3095ed706d15e7dad909c5dbd05aab81ef5`。codeload 内 22 个 Git blob 逐项核对官方 tree；论文/补充按 DOI、页数、ZIP CRC 与 SHA-256 验收。此 inventory 是项目本地摘要，不冒称上游官方 checksum。

### 数据范围和限制

固定 GitHub 仓库、正式论文及三个补充对象均已完整下载和验收，六个已接受 PDB 也通过 FASTA/mmCIF 两层核对，达到本项目 public-package 发布条件。它不是完整研究归档：三个 SRA 项目未下载；八个 focus parents 中只有六个存在已接受的参考复合物锚点；这些结构也不是每个回溯变体的实验结构。

### 许可和再分发边界

固定 GitHub tree 的根目录和 `CDRH3/` 均包含 MIT License，可在保留版权与许可声明的前提下使用、修改和分发，亦允许商业使用；论文与出版方附件采用 CC BY-NC-ND 4.0，允许带署名的非商业原样共享，但不授权分发改编版本。RCSB 文件保留其来源与使用条款。三类对象的许可边界分别保留，不能互相替代。

### 公开范围对照

| 论文或来源所指内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| GitHub methods/code 与 CSV | 22 blobs；11 CSV、59,378 原表行 | 已包含 |
| 两个回溯库 MLE output | 1,356/1,878 行；2,529 唯一 Variant 并集 | 已包含，但未按论文过滤 |
| 4A8 / CC12.1 亲本实验结果 | 复用 R42；不能重复算独立实验 | 外部既有来源 |
| SI Appendix / Dataset S1、S2 | 三个原附件，Dataset S1 26 sheets、S2 三 sheets，全部已读取 | 已包含 |
| 八 focus-parent 结构 | 六个已接受 mature-parent 锚点，非所有变体 | 部分包含 |
| 原始 sequencing | PRJNA1043249、PRJNA1043566、PRJNA1119481 | 本批未下载 |

## 待解决问题与处理进展

| 编号 | 待解决问题 | 当前证据与影响 | 后续处理 |
| --- | --- | --- | --- |
| Q01 | 1-20 与 CC6.31 尚无已接受的实验复合物锚点 | 其余六个成熟亲本均有可核验 RCSB entry；缺口只限制结构覆盖，不影响仓库、论文和标签文件的发布 | 后续如有作者或 RCSB 的可靠映射，再增量补充；当前不以预测结构代替 |
| Q02 | YL011 的固定 Git 结果与 Dataset S1 同键拟合值大量不同 | 附件比 Git 多 16 个 Variant，且 1,878 个同键中有 1,707 个拟合结果至少一项不同；两份原样版本均已保存 | 使用时显式选择版本；若需统一口径，应向作者确认修订关系，不静默覆盖 |
