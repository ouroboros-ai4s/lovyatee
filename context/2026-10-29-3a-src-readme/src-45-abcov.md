---
- tags:
  - context
---

# SRC_R45_ABCOV 数据说明

## 数据集身份

- `source_id`：`SRC_R45_ABCOV`
- `source_version`：`figshare-5661658-v1`
- 原作者或发布机构：Puneet Rawat、Divya Sharma 等；IIT Madras Protein Bioinformatics Lab；派生的两张训练表由 Graylab FLAb 发布

### 来源方背景

IIT Madras 蛋白质生物信息学实验室官方页面记载，实验室于 2010 年 12 月在生物技术系成立，研究蛋白质序列—结构—功能关系、稳定性与相互作用，并开发数据库和分析工具。Ab-CoV 是该团队面向冠状病毒抗体资料建立的文献整理数据库，不是一家公司或一次单独实验。

## 实验设计和数据口径

Ab-CoV 的主线不是在统一条件下重新测量一批抗体，而是从多篇文献汇集冠状病毒相关抗体、纳米抗体、靶病毒、结合与中和终点、序列、文献及结构信息，并在此基础上计算序列相似性、界面特征和单点突变效应。因此，同一文件包中同时存在原文实验值、文献注释和计算派生值，不能把所有行当作同一种实验标签，也不能直接相加成独立抗体数。

正式 Figshare collection v1 包含 11 个 article records、12 个文件。`CoV-AbDab_220222.csv` 有 5,033 条抗体/纳米抗体记录；`Ab-CoV_interface_detail.csv` 有 133 个带 PDB 的抗体界面条目；`Ab-CoV_interface_mutation.csv` 对这些界面位点给出 29,010 行计算结果，每行列出 19 种非野生型替换值，因此共有 551,190 个突变估计，单位为 kcal/mol，这些不是新增实验测量。病毒蛋白表含 24 条记录，两张 identity 矩阵比较来源抗体/纳米抗体与 552 个治疗性抗体。中和和表位 CSV 使用跨多行的复合表头及记录布局，物理行数 10,857 和 67,919 不能直接解释为样本数。

作为便于建模的派生补充，FLAb 固定 commit 还提供 KD 141 行和 IC50 427 行。KD 表有 136 个唯一 heavy/light 对、1 条完全重复行和 32 行缺 light；KD 为 0.006–6,000 nM，`-log (KD M)` 与 `fitness` 相同，越高表示结合越强。IC50 表有 413 个唯一重轻链对、25 行缺 light；IC50 为 0.01–100,000 ng/ml，`fitness` 直接等于 IC50，越低表示中和越强。两表同名 `fitness` 的方向相反，KD 与 IC50 也不是同一种终点。

## 论文原文

- 标题：Ab-CoV: a curated database for binding affinity and neutralization profiles of coronavirus-related antibodies
- 作者：Puneet Rawat, Divya Sharma, R. Prabakaran, Fathima Ridha, Mugdha Mohkhedkar, Vani Janakiraman, M. Michael Gromiha
- 发表来源：Bioinformatics 38(16):4051–4052，正式发表版；在线发布日期 2022-06-30，卷期发布日期 2022-08-10
- 发布日期：2022-06-30
- DOI：`10.1093/bioinformatics/btac439`
- PMID / PMCID：35771624 / 无
- 归档文本版本：正式发表版在线文本
- 本地文件：未归档
- 文件大小：无本地正文文件
- SHA-256：无本地正文文件
- 文本许可：出版方页面未提供可随数据包再分发的明确文本许可；本地仅记录在线核对结果
- 补充材料：未取得可本地归档的正式主文 PDF；完整数据由论文指向的 Figshare collection 提供

已通过 DOI、PubMed、出版方页面和正式 Figshare collection 交叉核对论文与数据身份。出版方 PDF 端点对当前自动访问返回 HTTP 403，因此本 source 不保存主文 PDF，也不把在线核对冒充本地全文；这不影响 Figshare 数据包的完整取得。OpenAlex 在 2026-09-24 返回正式论文被引 11 次，该值是动态元数据快照。

## 仓库内容

上游固定版本：[一手入口](https://doi.org/10.6084/m9.figshare.c.5661658.v1)。Figshare collection `5661658` v1（DOI `10.6084/m9.figshare.c.5661658.v1`），上游版本日期 `2021-10-14T04:58:57Z`；当前 source version 为 `figshare-5661658-v1`，日期不是本次下载日期。

一手交付为 Figshare collection `5661658` v1 下的 11 个 article records、12 个文件，逐文件核对 article version、官方 bytes、MD5 与本地 SHA-256；四个 ZIP 均通过 CRC、路径安全和成员读取检查，共 2,648 个成员。另保留 FLAb 固定 commit 的两个处理表及三份说明/许可文件，五个 Git blob 均核对官方 tree。两层来源分目录保存，不把 FLAb 派生表冒充 Figshare 原始字段。

```text
figshare-5661658-v1/
├── Ab-CoV-Figshare/
│   ├── Ab-CoV_neut_profile.csv
│   ├── Ab-CoV_epitope_data.csv
│   ├── CoV-AbDab_220222.csv
│   ├── Ab-CoV_interface_detail.csv
│   ├── Ab-CoV_interface_mutation.csv
│   ├── Ab-CoV_viral_protein.csv
│   ├── Ab-CoV_identity_antibodies_VH-VL.csv
│   ├── Ab-CoV_identity_nanobodies_VH.csv
│   ├── Ab-CoV_viral_protein_calculations.zip
│   ├── IMGT-Collier-de-Perles_heavy_chain.zip
│   ├── IMGT-Collier-de-Perles_light_chain.zip
│   └── konwn PDBs.zip
└── FLAb/
    ├── LICENSE
    ├── README.md
    └── data/
        ├── README.md
        └── binding/
            ├── rawat2022abcov_kd.csv
            └── rawat2022abcov_ic50.csv
```

source version 固定的是 Figshare collection 5661658 v1，而 collection 中 `Ab-CoV_neut_profile.csv` 与 `CoV-AbDab_220222.csv` 所在 article 已更新到 v2；配置逐项记录实际 article version 和 DOI。官方数据库网页仍可浏览，但动态网页内容不作为这一不可变快照的一部分。上游结构归档名 `konwn PDBs.zip` 存在拼写错误，本地保留原名以维持身份。

## 数据结构

### 一手整理表和计算表

`CoV-AbDab_220222.csv` 是最适合按行读取的抗体元数据表，包含名称、Ab/Nb 类型、结合与中和对象、VH/VHH、VL、基因、CDR3、结构、来源和更新时间。`Ab-CoV_interface_detail.csv` 将 133 个 PDB 条目连接到抗体、靶点、序列、结构方法、文献及 paratope/epitope；`Ab-CoV_interface_mutation.csv` 是 FoldX、CUPSAT、mCSM 或 ProAffiMuSeq 的计算结果，不是 551,190 次湿实验。两张 identity CSV 是宽矩阵，单元格为序列相似性百分比。病毒蛋白表及其 ZIP 是序列、结构和接触/相互作用计算。

### 复合表头文件

`Ab-CoV_neut_profile.csv` 和 `Ab-CoV_epitope_data.csv` 把一个逻辑记录拆成多行，并使用两层表头；实际行宽分别在 5–9 列和 5–12 列之间变化。普通 `csv.DictReader` 会把这些物理行误当作独立样本，读取前必须先重建作者的分组和表头。当前 README 只报告可直接核验的物理布局，不给未经验证的逻辑样本数。

### FLAb 派生表

两张 FLAb CSV 提供标准氨基酸 heavy/light 与 KD 或 IC50，但缺少原库名称、病毒株、方法、文献和 PDB 键。空 light 是缺失信息，不能自动解释为 VHH；相同序列出现在两个表也不表示终点可互换。

### 字段说明

| 文件或表 | 原始字段 | 类型/单位/方向 | 缺失、边界及来源 |
| --- | --- | --- | --- |
| CoV-AbDab_220222.csv | Name / Ab or Nb / Binds to / Neutralising Vs | 名称、类型和分号分隔的靶标/病毒列表；`Ab` 或 `Nb` | 5,033 行；空值表示公开表未给出，不能补成阴性 |
| CoV-AbDab_220222.csv | VH or VHH / VL / CDRH3 / CDRL3 / Structures / Sources | 氨基酸序列、结构链接与来源引用 | 并非每行都有完整双链或结构；`Structures` 不能脱离行键展开 |
| Ab-CoV_interface_detail.csv | pdb_id / ab / binds_to / experimental_method / resolution | 结构连接、抗体、靶点、方法和分辨率 | 133 行；方法枚举为 `ELECTRON MICROSCOPY`、`X-RAY DIFFRACTION` |
| Ab-CoV_interface_detail.csv | vh_or_vhh / vl / paratope_\* / epitope_\* | 序列及结构/序列编号下的界面残基字符串 | 结构编号与序列编号不可混用；完整 PDB entry 还可能含无关实体 |
| Ab-CoV_interface_mutation.csv | method / method_type / Interface / A…Y | 计算方法、任务、界面侧和 19 个替换的 kcal/mol 值 | method 为 CUPSAT/FoldX/ProAffiMuSeq/mCSM；任务为结合变化或稳定性变化；Interface 为 Epitope/Paratope |
| Ab-CoV_viral_protein.csv | Accesssion / Protein Sequence / Experimental Structure / interaction counts | 24 个病毒蛋白的标识、序列、结构与计算计数 | 保留上游字段拼写 `Accesssion`；计数不是结合亲和力标签 |
| identity CSV | 首列来源抗体；其余 552 列为治疗性抗体 | VH–VL 或 VH 序列相似性百分比宽矩阵 | 抗体矩阵 922 行、纳米抗体矩阵 193 行；不是 552 个实验终点 |
| neut_profile / epitope_data | 两层表头与跨行记录 | 中和、EC50/KD、表位、结构和引用等混合字段 | 物理行宽可变，不能用普通单表头解析或将物理行数当样本数 |
| rawat2022abcov_kd.csv | heavy / light / Binding Affinity (KD nM) / -log (KD M) / fitness | 序列、KD nM 和 pKD；KD 越低越强，pKD/fitness 越高越强 | 141 行；light 缺 32；pKD=9−log10(KD nM)，不是另一项测量 |
| rawat2022abcov_ic50.csv | heavy / light / IC50 (ng/ml) / fitness | 序列和质量浓度中和终点；越低越强 | 427 行；light 缺 25；fitness 等于 IC50，与 KD 表方向相反 |
| 四个 ZIP | PDB / SVG / 计算 CSV 成员 | 214 个结构、2,408 个 Collier de Perles SVG、2 个支持文件、24 个病毒蛋白计算 CSV | 共 2,648 个成员；目录成员不算数据对象，均已通过 CRC 和安全路径检查 |

### 数据示例

来自 `Ab-CoV-Figshare/Ab-CoV_interface_detail.csv` 的第一条真实记录（仅摘录下列列）：

```json
{
  "pdb_id": "6WPT",
  "ab": "S309",
  "binds_to": "SARS-CoV,SARS-CoV-2",
  "experimental_method": "ELECTRON MICROSCOPY",
  "resolution": "3.7, 3.7",
  "vh_or_vhh": "QVQLVQSGAEVKKPGASVKVSCKASGYPFTSYGISWVRQAPGQGLEWMGWISTYNGNTNYAQKFQGRVTMTTDTSTTTGYMELRRLRSDDTAVYYCARDYTRGAWFGESLIGGFDNWGQGTLVTVSS",
  "vl": "EIVLTQSPGTLSLSPGERATLSCRASQTVSSTSLAWYQQKPGQAPRLLIYGASSRATGIPDRFSGSGSGTDFTLTISRLEPEDFAVYYCQQHDTSLTFGGGTKVEIK"
}
```

示例中的 6WPT 将 S309 的 VH/VL、靶点、结构方法和分辨率连接到同一 PDB 条目；它说明界面表能够逐行连接结构，但不代表所有数据库抗体都有结构。

## PDB 数据库

官方 `konwn PDBs.zip` 实际含 214 个唯一 PDB 文件。为避免此前只抓三个病毒靶点代表结构而遗漏正式交付，本次以 ZIP 文件名为完整候选集，逐一从 RCSB 保存 canonical entity FASTA 与完整 mmCIF；214 个 entry 全部通过配对验证。其中 133 个 PDB ID 同时出现在 `Ab-CoV_interface_detail.csv`，可以连接到具体抗体和界面记录；其余 81 个只由官方结构 ZIP 建立来源级连接，不能擅自分配给某一数据行。

取得日期：2026-09-24。每个唯一 entry 保留完整 RCSB canonical entity FASTA 与完整沉积坐标，不选择性截断、不拼接设计序列。实体/链从 mmCIF `_entity` / `_entity_poly` 核对；canonical 序列与 FASTA entity 一致，坐标 `_entry.id` 与 PDB ID 一致，原子记录非空。

结构连接较多，不在正文展开 428 个文件的逐项哈希。214 个 PDB ID 均来自官方结构 ZIP；其中 133 个同时有 `Ab-CoV_interface_detail.csv` 的逐行连接，其余 81 个只有该 ZIP 的来源级连接。全部 ID 与映射证据保存在可复现配置，并由发布检查逐项验证。

PDB 文件 inventory 按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接的 SHA-256：`1559b6ad9557b5c20461aafa147816803292c2086c9645e3e61041428fe498bd`。

共 214 个有效锚点、214 个 FASTA、214 个 mmCIF，379.08 MiB（397498524 bytes）。每个下载使用 `https://www.rcsb.org/fasta/entry/<PDB_ID>/download` 与 `https://files.rcsb.org/download/<PDB_ID>.cif`；共享已存 gzip 坐标直接原样复用，未重压缩。完整 entry 可含未参与该研究的抗体/实体；链身份与映射边界按上表及下文使用。

RCSB 文件保存完整 entry，可能包含抗体、抗原、对称拷贝、糖链或其他分子。对 133 个界面条目，可按原表的 PDB、抗体和 VH/VL 字段继续核对链；对其余 81 个只能声称属于官方结构归档。不得把完整 entry 的所有实体都当作抗体—抗原对，也不得把 FLAb 匿名序列行强行连接到 PDB。

## 使用方式

```python
from pathlib import Path
import csv
root = Path(dataset_root)
with (root / 'Ab-CoV-Figshare' / 'Ab-CoV_interface_detail.csv').open(newline='') as f:
    interfaces = list(csv.DictReader(f))
```

可直接逐行读取 interface、viral protein、identity、CoV-AbDab 和两张 FLAb 表；`Ab-CoV_neut_profile.csv` 与 `Ab-CoV_epitope_data.csv` 需先按两层表头和跨行记录重建。建模时必须保留实验/文献整理/计算派生的来源层级，并分别处理 KD、IC50、EC50 与计算 ΔΔG。

## 采集过程记录

2026-09-18：从公开资源清单追到 Ab-CoV 官方数据库与 FLAb 整理镜像，固定 FLAb commit 的五个对象；验证 Git blob，读取 KD/IC50 表并核对缺轻链、重复和标签方向。

2026-09-24：从官方数据库页面追到 DOI `10.6084/m9.figshare.c.5661658.v1`，确认这是作者正式数据 collection；取得 11 个 article records 的 12 个文件，并核对官方 bytes、MD5、本地 SHA-256、ZIP CRC 和 2,648 个成员。

2026-09-24：读取所有可直接解析的表和 ZIP 内计算 CSV；确认中和/表位 CSV 是复合跨行布局，停止将物理行数解释为抗体或表位数。将 PDB 范围从三个靶点代表修正为官方 ZIP 的 214 个 ID，全部完成 FASTA/mmCIF 两层验收；原三个代表文件移入共享运行证据保留，而非静默删除。

当前未取得对象：

| 对象 | 错误/边界 |
| --- | --- |
| 主文 PDF | 出版方 PDF 端点对当前自动访问返回 HTTP 403；未归档正文文件 |

2026-09-24：本地 README 编辑后立即同步共享 staging，固定 markdownlint-cli2 0.20.0 按 skill 配置检查。发布、残留清理和当前缺口同步到本批交接；source version 不另发布 manifest、API 响应或审计文件。完整研究 acquisition 与本次公开包接入分开记录。

## 参考文献

- [固定上游数据版本](https://doi.org/10.6084/m9.figshare.c.5661658.v1)
- [主论文 DOI](https://doi.org/10.1093/bioinformatics/btac439)
- [Ab-CoV 官方数据库](https://web.iitm.ac.in/bioinfo2/ab-cov/home)
- [IIT Madras Protein Bioinformatics Lab 官方简介](https://web.iitm.ac.in/bioinfo3/gromiha/index.html)
- [原论文 PubMed](https://pubmed.ncbi.nlm.nih.gov/35771624/)
- [FLAb 固定版本许可列表](https://github.com/Graylab/FLAb/blob/e05e3f0135783ffb7de412df6a1467e7a0031911/data/README.md)
- [RCSB PDB](https://www.rcsb.org/)：214 个 entry 的逐项 ID 与证据见本 source 的可复现配置

## 其他

### 完整性与验收

上游数据 payload 17 个文件、175.15 MiB（183661398 bytes）；其中核对 Git blob 身份的文件 5 个。文件 inventory 按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接的 SHA-256：`f25dfa845dcafffed4096aea78df5bb1e30af437544f0b5b5fcf37719b20d555`。Figshare 文件核对官方 bytes/MD5 和本地 SHA-256，四个 ZIP 逐成员检查 CRC 与安全路径；五个 FLAb 文件另核 Git blob。此 inventory 是项目本地摘要，不冒称上游官方 checksum。

### 数据范围和限制

作者正式 Figshare collection 的 12 个文件和 FLAb 的五个派生文件均已原样取得并通过完整性验收，214 个官方结构 ID 也完成 RCSB FASTA/mmCIF 验证，达到本项目 public-package 发布条件。该快照仍不等于动态官网的当前数据库，也不提供统一实验口径；中和/表位复合 CSV 的逻辑记录数以及不同版本宣称的抗体/表位规模尚不能由物理行数直接统一。

### 许可和再分发边界

Figshare collection 及其 11 个 article records 均标为 CC BY 4.0：允许共享、改编和商业使用，但须署名、链接许可证并说明改动。FLAb 根 LICENSE 明确要求逐 study 查看 `data/README.md`，其中 Ab-CoV 的 study-specific license 单元格为空，因此两张 FLAb 派生表的独立再分发许可未特别说明；本 source 如实保留该不确定性，不把 Figshare 的 CC BY 4.0 自动扩展到 FLAb 转换物。RCSB 派生下载另保留其来源和条款。

### 公开范围对照

| 论文或来源所指内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 作者正式 Figshare 数据交付 | 11 个 article records、12 个文件；官方 MD5 与本地 SHA-256 均核对 | 已包含 |
| 抗体、病毒、文献和结构 metadata | CoV-AbDab 5,033 行、病毒蛋白 24 行、界面 133 行 | 已包含 |
| 计算突变和结构特征 | 551,190 个替换估计、24 个病毒蛋白计算 CSV、identity 矩阵 | 已包含；不是实验标签 |
| 官方抗体结构归档 | 214 个 PDB；133 个有界面表逐行连接，81 个只有来源级连接 | 已包含并标注映射层级 |
| FLAb 建模派生表 | KD 141 行、IC50 427 行及三份说明/许可文件 | 已包含；许可边界单列 |
| 动态官网当前内容与论文全文 | 官网仅作在线核对；出版方 PDF 自动访问 403 | 不在固定数据快照中 |

## 待解决问题与处理进展

| 编号 | 待解决问题 | 当前证据与影响 | 后续处理 |
| --- | --- | --- | --- |
| Q01 | 正式主文 PDF 未本地归档 | DOI、PubMed、出版方页面和 Figshare 数据身份已核对；PDF 端点对自动访问返回 403，不影响正式数据包发布 | 如获得合法可下载版本再补充，同时保留原始 URL、大小和哈希 |
| Q02 | 不同版本的规模口径和两个复合 CSV 的逻辑记录数尚未统一 | Figshare collection 描述为 1,047 antibodies、3,326 epitopes，论文报告 1,780 antibodies 和 3,200+ epitopes；当前 CSV 的跨行结构无法用普通行数验证这些口径 | 后续依据作者 schema 或维护者说明重建逻辑记录；当前分别报告版本与物理布局 |
| Q03 | FLAb 两张派生表的 study-specific license 单元格为空 | 作者 Figshare 一手文件明确为 CC BY 4.0；不确定性只影响 FLAb 转换物的独立再分发/商业使用解释，不影响一手包接入 | 使用 FLAb 表前保留来源并向发布者确认；不要把 Figshare 许可外推 |
