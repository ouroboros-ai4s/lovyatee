# SRC_R49_GARBINSKI_GSK 数据说明

## 数据集身份

- `source_id`：`SRC_R49_GARBINSKI_GSK`
- `source_version`：`snapshot-2026-08-17`
- 原作者或发布机构：GSK（Luis Garbinski 提供未发表内部数据）；Johns Hopkins Gray Lab（Michael Chungyoun、Jeffrey Gray，将数据整理进 FLAb2 并公开）

### 来源方背景

[GSK 公司文件](https://www.gsk.com/media/7905/gsk-2021-final-base-prospectus-100521.pdf)记载 GSK plc 于 1999 年在英格兰和威尔士注册；[官方沿革](https://www.gsk.com/en-gb/company/history-and-heritage/)说明 Glaxo Wellcome 与 SmithKline Beecham 的合并于 2000 年生效，并将其 legacy roots 追溯到 1715 年伦敦的 Plough Court Pharmacy。2022 年消费者健康业务分拆为 Haleon 后，GSK 转为聚焦专科药物和疫苗的生物制药公司。[全球总部](https://www.gsk.com/en-gb/contact-us)位于伦敦。根据 [GSK 2025 年报](https://www.gsk.com/en-gb/investors/financial-reports/annual-report-2025/)，普通股在伦敦证券交易所上市，并以 ADS 形式在纽约证券交易所交易，代码均为 `GSK`（上市状态核查于 2026-09-24）。本 source 能直接确认的 GSK 责任是 Luis Garbinski 向 FLAb2 提供内部抗体结合、表达和热稳定性数据；公开材料没有给出其在该实验中的具体职务或完整实验团队。

[Gray Lab](https://graylab.jhu.edu/people.php) 隶属 Johns Hopkins University，研究方向包括计算蛋白结构预测与设计、蛋白质对接和治疗性抗体。Michael Chungyoun 与 Jeffrey Gray 在 FLAb2 中汇编多项抗体 developability 数据，并通过 [FLAb 固定仓库版本](https://github.com/Graylab/FLAb/tree/e05e3f0135783ffb7de412df6a1467e7a0031911)公开本 source 的三张处理表。

## 实验设计和数据口径

FLAb2 将本组材料列作 `Garbinski et al. unpublished (2023)`：Luis Garbinski 向 FLAb2 提供 GSK 内部测得的结合、表达和热稳定性数据，原始研究没有对应的 2023 年论文。当前公开产物是三张处理后 CSV，没有仪器曲线、逐 replicate 读数或实验记录。FLAb metadata 分别把端点标为 `SPR Kd`、`HEK` 表达和 `nanoDSF`。SPR（表面等离子共振）可从结合/解离响应拟合平衡解离常数 $K_D$；nanoDSF 通过随温度变化的内源荧光观察蛋白热转变。原始抗原构建体、浓度梯度、拟合模型、HEK 细胞系统、表达定量方法、nanoDSF 升温程序和重复设计均未公开，因此文档只解释现有字段，不补造实验细节。

三张表合起来覆盖 94 个不同的重链/轻链可变区序列对。表达表包含全部 94 对；热稳定性表是其中 86 对，KD 表是其中 81 对。74 对同时具有三个端点，另有 12 对只有表达与 Tm1、7 对只有表达与 KD、1 对只有表达。三表没有同一端点内的重复序列对，也没有缺失单元格。关系如下；分支表示有证据的集合包含关系，不表示先做表达再筛选 KD 或 Tm1，因为送测与缺失规则没有公开。

```text
94 个唯一重/轻链序列对（以表达表为全集）
├── Expression：94 对
├── Tm1（nanoDSF）：86 对
└── KD（SPR）：81 对

交集：74 对三项都有；12 对仅 Expression+Tm1；
      7 对仅 Expression+KD；1 对仅 Expression
```

序列核验还在 94 对中识别出 AM14、D25、Motavizumab 和 RSB1 四个可唯一连接到 PDB 的参考序列对，且四者都出现在三张表。D25、Motavizumab 和 RSB1 的重、轻链分别精确命中相应 PDB entity 的变量区子序列；AM14 轻链同样命中，重链则对应于省略 PDB entity 最前端 Glu 后的连续片段。四个参考抗体都有与 RSV F 结合的实验复合物结构，因此 RSV F 是目前最有力的数据背景解释。不过，三张 CSV 与 FLAb2 都没有直接写出这次 GSK KD 实验所用的 antigen construct，故下游元数据应把 RSV F 标为“由可唯一匹配的参考序列和结构证据支持、尚待原始记录确认”，不应伪装成 CSV 明示字段。

其余 90 对没有样本名或亲本标签。为检查数据组成，本项目对全部 94 对按完整重链与轻链到四个 PDB 支持的参考对的 Levenshtein 距离之和做最近参考分组，得到 AM14 34 对、D25 25 对、Motavizumab 11 对、RSB1 24 对；最佳与次佳参考的最小距离差为 52。这个分组仅用于审计序列族，不是上游公开的设计谱系、分类标签或候选选择规则。

KD 列范围为 1.23 × 10⁻¹¹–3.00 × 10⁻⁸；原 `KD` 表头没有单位，但同表 `-log (KD (M) )` 明确按 M 计算，且 `fitness` 与该负对数逐行相同。较小 KD 表示更强结合，负对数与 `fitness` 则较大表示更强；三列是同一端点的原值与派生表示，建模时只能选定一种标签，不能把另两列作为输入。表达范围为 68.29–373.75 µg/mL，FLAb 标记较高为有利。`Tm1 (nanoDSF)` 范围为 35.2–76.8，FLAb 标记较高为有利，但原列没有写温度单位；在取得原始说明前不把这些数值擅自注明为 °C。检测上下限、拟合失败、误差、独立重复数和候选选择偏差均无法从公开表恢复。

## 论文原文

FLAb2 是当前三张表的公开解释依据；它明确说明 GSK 数据未关联独立论文。因此，本节归档 FLAb2 预印本，而不是虚构一篇 `Garbinski 2023` 原论文。

- 标题：Fitness Landscape for Antibodies 2: Benchmarking Reveals That Protein AI Models Cannot Yet Consistently Predict Developability Properties
- 作者：Michael Chungyoun、Jeffrey J. Gray
- 发表来源：bioRxiv
- 归档文本版本：v1 预印本
- 发布日期：2025-12-27
- DOI：[10.64898/2025.12.27.696706](https://doi.org/10.64898/2025.12.27.696706)
- PMID / PMCID：`41497662` / `PMC12767642`
- 本地文件：`articles/Chungyoun_2025-12-27_bioRxiv-FLAb2-v1.pdf`
- 文件大小：7.00 MiB（7,335,203 bytes）
- SHA-256：`dc5c31ef9ea506b2d4c78a8fdec085ce74bf1a06fea0b5d54f325b3728a3d9c2`
- 文本许可：[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- 补充材料：同一 54 页 PDF 的后半部分包含 Supplementary Information；Table S1 明示该未发表来源有 86 个 Tm、94 个 expression 和 81 个 binding 序列—标签对
- 引用数（查询快照）：12（[OpenAlex W7117407955](https://openalex.org/W7117407955)，查询于 2026-09-24）

## 仓库内容

数据来自 Gray Lab 的 FLAb 仓库，固定 commit `e05e3f0135783ffb7de412df6a1467e7a0031911`；该 commit 的 committer 日期为 2026-08-17，因此版本目录命名为 `snapshot-2026-08-17`。这个日期是 FLAb 快照日期，不是 GSK 实验日期或 FLAb2 预印本发布日期。本 source 只保留与 Garbinski/GSK 条目对应的三张普通 Git blob，属于选择性 `processed-public` 快照，不声称包含完整 FLAb 仓库。

```text
snapshot-2026-08-17/
└── FLAb/data/
    ├── binding/garbinski2023_kd.csv
    ├── expression/garbinski2023_exp.csv
    └── thermostability/garbinski2023_tm1.csv
```

三张 CSV 保留上游路径、文件名和原始字节。论文归档与 RCSB 参考结构是本项目为解释和核验另行补充的材料，不属于上述 FLAb payload。

## 数据结构

### 文件和记录关系

每行是一组重链/轻链可变区序列对在一个端点上的处理后记录。三表以 `(heavy, light)` 连接；表达表是当前 94 对序列的全集，KD 与 Tm1 分别是其子集。没有原始样本 ID、候选名称、replicate ID 或测量批次，不能从相同行号连接文件。

| 文件 | 数据行 | 唯一序列对 | 实际字段 | 当前数值范围 |
| --- | --- | --- | --- | --- |
| `garbinski2023_kd.csv` | 81 | 81 | `heavy`, `light`, `KD`, `-log (KD (M) )`, `fitness` | KD=1.23e-11–3e-08; -log (KD (M) )=7.522878745–10.91009489; fitness=7.522878745–10.91009489 |
| `garbinski2023_exp.csv` | 94 | 94 | `heavy`, `light`, `Expression (µg/mL)`, `fitness` | Expression (µg/mL)=68.29–373.75; fitness=68.29–373.75 |
| `garbinski2023_tm1.csv` | 86 | 86 | `heavy`, `light`, `Tm1 (nanoDSF)`, `fitness` | Tm1 (nanoDSF)=35.2–76.8; fitness=35.2–76.8 |

### 字段说明

| 文件或表 | 原字段 | 类型、单位、方向与缺失 | 来源与使用边界 |
| --- | --- | --- | --- |
| 全部三表 | `heavy`、`light` | 标准氨基酸字符串，无空值；heavy 120/121/122/126 aa，light 106/107/108/110/112/113/114 aa | FLAb 整理的可变区样式序列；不是完整 IgG 构建体 |
| binding | `KD` | 科学计数法浮点；表头未写单位，派生列支持 M；较小通常结合更强；无空值 | FLAb metadata 标为 `SPR Kd`；原始曲线、拟合与检测边界未公开 |
| binding | `-log (KD (M) )` | 浮点，逐行等于 −log₁₀(KD/M)；较大通常结合更强；无空值 | 由 `KD` 派生，不是第二次实验测量 |
| binding | `fitness` | 浮点，与 `-log (KD (M) )` 逐行相同；无空值 | FLAb 统一建模标签；预测同一端点时不可作输入特征 |
| expression | `Expression (µg/mL)` | 浮点，µg/mL；FLAb 标记较大有利；无空值 | FLAb metadata 标为 `HEK`；具体细胞系和定量方法未公开 |
| expression | `fitness` | 浮点，与 `Expression (µg/mL)` 逐行相同；无空值 | FLAb 统一建模标签；不是独立测量 |
| thermostability | `Tm1 (nanoDSF)` | 浮点；原列未写温度单位；FLAb 标记较大有利；无空值 | nanoDSF 第一热转变汇总值；原始熔解曲线和拟合规则未公开 |
| thermostability | `fitness` | 浮点，与 `Tm1 (nanoDSF)` 逐行相同；无空值 | FLAb 统一建模标签；不是独立测量 |

### 数据示例

下表不是文件中的名称列，而是通过重/轻链序列与 RCSB 抗体链精确匹配后加上的可读标识；数值均来自三张 CSV 中对应的真实记录。

| PDB 支持的参考序列对 | KD（原表） | `-log (KD (M) )` | Expression (µg/mL) | Tm1（原表） |
| --- | --- | --- | --- | --- |
| AM14 | 1.53E-11 | 10.81530857 | 373.75 | 55.4 |
| D25 | 3.57E-11 | 10.44733178 | 317.56 | 74 |
| Motavizumab | 9.22E-11 | 10.03526908 | 285.24 | 46.6 |
| RSB1 | 1.13E-10 | 9.946921557 | 358.86 | 50.3 |

每行仍代表一个序列对的三个端点记录，不表示三种实验在同一次运行中完成，也不把四个参考对自动定义为上游标注的 controls。

## PDB 数据库

PDB 审计先对 94 个公开序列对做精确子序列匹配，再选择能覆盖四个参考抗体且含 RSV F 的最小结构集合。结果采用 4ZYP（同时覆盖 AM14、Motavizumab）、4JHW（D25）和 6W52（RSB1）。这些是四个参考对的实验复合物锚点；其余 90 对只有最近参考分组，没有逐条实验结构，项目没有据此生成变体结构、补环或 CDR graft。

| 参考抗体 | 采用的 RCSB entry | CSV 变量区与完整 PDB polymer 的关系 |
| --- | --- | --- |
| AM14 | 4ZYP | 完整 entity 在 CSV heavy 前有 1 aa，在 CSV light 前有 0 aa；变量区长度 122/108 aa；CSV heavy 相比 PDB 变量区省略最前端 Glu，其余连续匹配 |
| D25 | 4JHW | 完整 entity 在 CSV heavy 前有 0 aa，在 CSV light 前有 0 aa；变量区长度 126/107 aa |
| Motavizumab | 4ZYP | 完整 entity 在 CSV heavy 前有 0 aa，在 CSV light 前有 0 aa；变量区长度 120/106 aa |
| RSB1 | 6W52 | 完整 entity 在 CSV heavy 前有 19 aa，在 CSV light 前有 20 aa；变量区长度 121/110 aa |

| RCSB entry | 结构内容 | 保存的完整 polymer entities |
| --- | --- | --- |
| [4ZYP](https://www.rcsb.org/structure/4ZYP) | Crystal Structure of Motavizumab and Quaternary-Specific RSV-Neutralizing Human Antibody AM14 in Complex with Prefusion RSV F Glycoprotein | Fusion glycoprotein F0,Fibritin / author chain A,B,C / 498 aa; Motavizumab antibody Fab heavy chain / author chain J,K,N / 225 aa; Motavizumab antibody light chain / author chain L,M,O / 213 aa; AM14 antibody Fab heavy chain / author chain F,H,D / 227 aa; AM14 antibody light chain / author chain G,I,E / 215 aa |
| [4JHW](https://www.rcsb.org/structure/4JHW) | Crystal Structure of Respiratory Syncytial Virus Fusion Glycoprotein Stabilized in the Prefusion Conformation by Human Antibody D25 | D25 antigen-binding fragment heavy chain / author chain H / 230 aa; D25 light chain / author chain L / 214 aa; Fusion glycoprotein F0 / author chain F / 498 aa |
| [6W52](https://www.rcsb.org/structure/6W52) | Prefusion RSV F bound by neutralizing antibody RSB1 | Fusion glycoprotein F0 / author chain A / 82 aa; Fusion glycoprotein F1 fused with Fibritin trimerization domain / author chain B / 414 aa; RSB1 Fab Heavy Chain / author chain H / 283 aa; RSB1 Fab Light Chain / author chain L / 236 aa |

每个 entry 保存一份 RCSB 原始 full-entry FASTA 和一份完整 mmCIF，共 5.35 MiB（5,609,718 bytes）。FASTA 位于 `pdb/sequences/rcsb_pdb_<ID>.fasta`，坐标位于 `pdb/structures/<ID>.cif`；mmCIF 由 RCSB `.cif.gz` 无损解压，没有裁链或重序列化。PDB 子集 inventory SHA-256 为 `f0182256e00d11a1f42929bf22b01d0c3e0d158b7baece6757e4df41183e9324`。

本次重新使用修正后的配对验收：逐 polymer entity 比较原始 FASTA 与 mmCIF canonical sequence，同时检查 entry identity、全部 author-chain 覆盖和原子坐标。4ZYP 为 5 个 polymer entities，4JHW 为 3 个，6W52 为 4 个，均通过双层核验。此前其他来源中曾出现的 `verify_pair` 参数顺序错误没有带入本次结果。

## 使用方式

三表按 `(heavy, light)` 连接。读取 raw source 时保留原字段和单位状态，不在原目录补写抗原、温度单位或缺失记录。

```python
import csv
from pathlib import Path

with (Path(dataset_root) / "FLAb/data/binding/garbinski2023_kd.csv").open(
    encoding="utf-8-sig", newline=""
) as stream:
    binding_rows = list(csv.DictReader(stream))
```

## 采集过程记录

2026-09-18：从 FLAb 固定 commit `e05e3f0135783ffb7de412df6a1467e7a0031911` 的完整 Git tree 核验三张 CSV，并按原字节复制到 source staging。用户已授权共享 raw 目录写入及内部 AI 研究归档；该授权没有被写成 GSK 的对外再分发许可。

2026-09-18：首次独立核验得到 3 个 payload、65,974 bytes；当时 FLAb metadata 的 publication/DOI/license 均为 `None`/`none`，尚未找到解释数据来源的论文或结构连接，因此保留 partial。

2026-09-19：追溯三张表的首次加入历史。binding、expression、thermostability 分别由 Michael Chungyoun 在 `d7b52c0e8b997a1a9ff79a7572d12ce707395b9c`、`c41e56e03ded4c97585915d99ff6623a4ce424c1`、`005e6c1580f27aa4ba169807e391ed6b4dc717f8` 中于 2025-08-06 上传，提交信息均为 `Add files via upload`。这些提交固定了 FLAb 汇编 provenance，但没有附原始 GSK 协议。

2026-09-24：复核新出现的 FLAb2 v1。其致谢明确写明 Luis Garbinski 在 GSK 提供结合、表达和热稳定性内部数据，补充 Table S1 把来源标为未发表并列出 86/94/81 三类数量。由此关闭“没有任何可识别公开解释来源”的旧判断；原始 GSK 研究仍没有独立论文。

2026-09-24：自动归档器首次请求 bioRxiv PDF 连续收到 HTTP 429。浏览器式临时请求在限流窗口后取得 54 页官方文件；现有 R09 归档副本字节和 PDF metadata 不同，因此没有直接复用。归档器随后增加对 `Retry-After` 的有界处理，并从同一 v1 URL 按 7,335,203 bytes 和 SHA-256 `dc5c31ef9ea506b2d4c78a8fdec085ce74bf1a06fea0b5d54f325b3728a3d9c2` 重新取得正式原件，逐页解析通过。

2026-09-24：对 94 个唯一序列对完成集合审计和 PDB 精确序列反查，确认四个参考对及三张表的 74/12/7/1 重叠关系。补取 4ZYP、4JHW、6W52 的 3 份原始 FASTA 和 3 份完整 mmCIF，并用修正参数顺序后的验收器全量重跑。随后更新本地 README 并即时同步 source staging。

2026-09-24：在 CSV、论文、PDB、README、inventory 和 Markdown lint 全部通过后，将 staging 原子发布为 `SRC_R49_GARBINSKI_GSK/snapshot-2026-08-17`；发布后再次按正式目录复核，数据集专属许可和原始实验细节仍作为非阻塞未决项保留。

## 参考文献

- [FLAb 固定版本](https://github.com/Graylab/FLAb/tree/e05e3f0135783ffb7de412df6a1467e7a0031911)。
- [FLAb2 bioRxiv v1](https://doi.org/10.64898/2025.12.27.696706)。
- [FLAb2 PMC 记录](https://pmc.ncbi.nlm.nih.gov/articles/PMC12767642/)。
- [4ZYP：AM14、Motavizumab 与 prefusion RSV F](https://www.rcsb.org/structure/4ZYP)；结构论文 DOI [10.1371/journal.ppat.1005035](https://doi.org/10.1371/journal.ppat.1005035)。
- [4JHW：D25 与 prefusion RSV F](https://www.rcsb.org/structure/4JHW)；结构论文 DOI [10.1126/science.1234914](https://doi.org/10.1126/science.1234914)。
- [6W52：RSB1 与 prefusion RSV F](https://www.rcsb.org/structure/6W52)；结构论文 DOI [10.1371/journal.ppat.1008943](https://doi.org/10.1371/journal.ppat.1008943)。
- [GSK 官方沿革](https://www.gsk.com/en-gb/company/history-and-heritage/)与 [2025 年报](https://www.gsk.com/en-gb/investors/financial-reports/annual-report-2025/)。
- [Gray Lab 团队介绍](https://graylab.jhu.edu/people.php)与 [论文列表](https://graylab.jhu.edu/publications.php)。

使用本 source 时应同时引用 FLAb2、固定 commit，以及实际使用到的结构原论文；`Garbinski et al. unpublished (2023)` 不是可独立检索的正式论文。

## 其他

### 数据范围和限制

当前版本完整保存 FLAb2 公开的三张 Garbinski/GSK 处理表、用于解释它们的 FLAb2 v1，以及覆盖四个由 PDB 支持的参考对的共享结构。它不包含 GSK 的原始传感图、表达测定原始读数、nanoDSF 曲线、候选库、实验批次、失败样本或内部记录。最适合把它作为 94 个相关抗体序列对的多端点 `processed-public` 小数据集；KD 任务使用前需显式保留“抗原由参考序列推断、原 construct 待确认”的 provenance。

### 完整性与验收

独立验收全部 10 个文件（README 不计），共 12.41 MiB（13,010,895 bytes）；source inventory SHA-256 为 `f5bee6765d20d10c086797006df59b551c3dceb7f888c3770919308b9f068235`。inventory 规则为按路径排序的 `relative_path<TAB>bytes<TAB>sha256<LF>`。三张 CSV 全行、全字段、空值、重复和数值范围均已扫描；54 页 PDF 全页读取；三组 PDB FASTA/mmCIF 逐 polymer 配对。source 目录没有发布 API JSON、manifest 或审计报告，机器可读审计保留在开发者 workspace。

### 许可和再分发边界

FLAb 顶层 `LICENSE` 把数据许可指向 `data/README.md`；该表没有 Garbinski/GSK 这一行，`flab_metadata` 对三张表的 license 字面值均为 `none`。因此，上游未特别说明覆盖这组三张表的许可，使用与再分发范围不明确。当前文件通过作者维护的公开仓库主动提供，也没有发现与本次本地 source package 接入明确冲突的条款，故许可沉默不阻塞本次发布；它不构成允许商用、衍生或对外再分发的授权。

FLAb2 预印本文本采用 CC BY 4.0，该许可覆盖论文文本，不自动扩展为 GSK 内部实验数据许可。RCSB 原始 FASTA/mmCIF 仍按 RCSB 的数据使用政策处理。各对象的许可层次应分别保留。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| FLAb2 Table S1 的 86 Tm、94 expression、81 binding | 三张 CSV 分别 86/94/81 个唯一序列对，均无端点内重复 | 取得并一致 |
| GSK 内部 binding/expression/thermostability 数据 | FLAb2 致谢与三张处理表 | 处理后数据取得；原始实验记录未公开 |
| 94 对序列的跨端点关系 | 表达全集 94；74/12/7/1 精确集合分区 | 已核验 |
| 四个参考抗体及 RSV F 背景 | 四个可唯一连接 PDB 的参考序列对；4ZYP、4JHW、6W52 实验复合物 | 参考结构取得；具体 GSK antigen construct 待确认 |
| FLAb2 v1 与整合补充 | 官方 54 页 PDF，全文与 Table S1 已解析 | 取得 |
| GSK 原始 protocol、replicate、误差和检测边界 | 公开表及预印本未给出 | 未公开 |
| 数据专属许可 | FLAb metadata `none`，`data/README.md` 无对应条目 | 未特别说明；不阻塞本地接入 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-09-24；不阻塞本次接入发布）：GSK 未发表交付没有公开候选生成或选择规则、完整 SPR/表达/nanoDSF 条件、重复设计、误差和检测边界，因而无法复现实验或判断每个数值的不确定性。当前保留原字段、范围和缺口，不补造方法；下一步等待 GSK/FLAb 提供原始 protocol、实验记录或正式论文后关闭。
- `Q02`（最近更新：2026-09-24；影响抗原元数据）：CSV 与 FLAb2 未直接写出 KD assay 的 antigen construct。四个 PDB 支持的参考序列对分别连接 AM14、D25、Motavizumab、RSB1 的 RSV F 复合物，已将 RSV F 记录为强证据支持的背景，并把三份最小共享结构集归档；在 GSK 或原始记录确认具体 RSV F 构建体、株系和固定/分析物方向后关闭。
- `Q03`（最近更新：2026-09-24；不阻塞本次本地接入，限制商用和再分发判断）：FLAb 对本组数据标记 license `none`，且数据许可表没有对应条目。已分开记录论文 CC BY 4.0、数据许可沉默和 RCSB 条款；下一步由来源方明确 GSK 数据的使用、衍生、商用和再分发范围后关闭。
