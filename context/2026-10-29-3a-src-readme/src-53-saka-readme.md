---
- tags:
  - context
---

# SRC_R53_SAKA 数据说明

## 数据集身份

- `source_id`：`SRC_R53_SAKA`
- `source_version`：`snapshot-2021-03-12`
- 原作者或发布机构：Chugai Pharmaceutical Co., Ltd. Research Division（Koichiro Saka、Taro Kakuzaki、Reiji Teramoto 等）。

### 来源方背景

[中外制药公司概要](https://www.chugai-pharm.co.jp/english/profile/about/outline.html)记载其创立于 1925 年、总部位于日本东京，主营药品的研发、生产、销售及进出口；论文作者均隶属其中位于镰仓或御殿场的 Research Division。公司在 2002 年与 Roche 建立战略联盟并成为 Roche Group 成员；[公司现行联盟说明](https://www.chugai-pharm.co.jp/english/profile/strategy/roche_alliance.html)称 Roche 持有 59.89% 的流通股，公司继续在东京证券交易所 Prime Market 上市。上述上市和持股状态核验于 2026-09-24。

## 实验设计和数据口径

研究从抗犬尿氨酸抗体 F02 出发。犬尿氨酸是小分子抗原，因此本研究没有可下载的抗原蛋白 FASTA；生成犬尿氨酸的 IDO 酶也不是本次结合测量的靶点。作者依据 F02–犬尿氨酸晶体分析和单点突变结果设计重链库，但论文把这部分背景数据注明为 unpublished。库在 HCDR1、HCDR2 和 HCDR3 的 17 个 Kabat 编号位置引入允许残基，理论组合空间约为 2×10^17；实际构建得到超过 4×10^10 个 transformants。

当前公开数据形成过程可概括为：

```text
F02 亲本 + 17 个重链 CDR 可变位置
  └─ 噬菌体展示库：理论约 2×10^17；实际 >4×10^10 transformants
       └─ 犬尿氨酸两轮 panning
            ├─ 每轮抽取 96 个克隆做 phage ELISA：0 / 3 / 23 个阳性
            └─ round 0 / 1 / 2 的 NGS 汇总（Table 2）
                 └─ 选出 959 条两轮后富集 VH 训练 LSTM
                      └─ 生成 2,000,000 条序列
                           ├─ 10 条最低 NLL + 32 条分层 NLL 候选做 SPR
                           ├─ 10 条最高 NGS read-count 候选做 SPR
                           └─ F02 parent 作为 Control 做 SPR
                                ├─ Table 3：10 ML + 10 Freq + 1 Control
                                └─ Figure 10：42 条 ML 的聚合关系；32 条未逐条公开
```

这里的 ELISA 先用 450 nm 吸光度判断噬菌体克隆是否出现结合信号，阈值为吸光度大于 0.2。表 2 给出的 NGS reads 为 890,801、912,660、1,227,934；经作者流程识别为抗体结构的 Total sequences 为 453,896、789,338、1,083,376，其中 Unique sequences 为 444,170、786,040、1,051,847。论文 Results 说明按两轮后 read count 从高到低选择、不超过 1,000 条，并用 read count 大于 3 的 959 条 VH 训练模型。NGS read count 和单位置 enrichment 描述筛选富集程度，均不是亲和力。

LSTM 为每条序列给出负对数似然 NLL；NLL 越低，模型给出的 sequence likelihood 越高。作者从 200 万条生成序列中取 10 条最低 NLL 序列，并另取 32 条覆盖 NLL 10–25.5 的序列；再从两轮 panning 的 NGS 中取 read count 最高的 10 条。合计 52 条候选加 1 条亲本进入表达和结合评价。Figure 10 汇总了 42 条 ML 候选的 NLL–亲和力关系，但主文 Table 3 只逐行公开最低 NLL 的 10 条 ML、10 条 Freq 和 1 条 Control；其余 32 条 ML 的序列与 KD 没有结构化公开表。

SPR 测量中，抗体先被捕获到固定有 protein A/G 的 CM5 芯片，犬尿氨酸作为 analyte 流过；作者用未捕获抗体的 flow cell 作参考，并计算有、无犬尿氨酸的响应差。Biacore 软件随后用 steady-state affinity model 拟合 KD。Table 3 的 KD 单位为 M，越低表示亲和力越强；21 行均为有限数值，范围 4.2×10^-8–7.7×10^-5 M。该表的 NLL 是模型输出，KD 才是实验拟合值；Supplementary Fig. 2 只给亲本与最佳候选的 sensorgram 图片，没有逐候选原始响应时序或 replicate 曲线。

Table 1 给出了包含 17 个 `X` 占位符的 123-aa 重链可变区模板，Table 3 则逐行给出 X1–X17 的残基。按位置顺序替换即可在 processed 层确定性还原 21 条完整 VH，不能再把公开范围描述成“只有 17-aa 向量”。raw 层仍保留 publisher 原表和图片，不另生成拼接序列。论文公开包没有 VL。相关专利家族 WO2015083764 的 SEQ ID NO:95 与 Table 1 加 Control 残基还原出的 VH 完全一致，并在一项犬尿氨酸重链库实例中把该 VH 与 VL SEQ ID NO:97 配对；由于论文没有引用该专利或明确给出其实际 VL 标识，这一关系作为外部候选映射保留，未把 SEQ ID NO:97 写成已确认的本研究轻链。

以 DOI、PMID 和题名检索 NCBI SRA、BioProject 与 GEO 均未发现关联 accession。当前交付因此是论文公开子集：包含主文表格、补充说明和图片，不包含全量 NGS reads、959 条训练序列、200 万条生成序列、32 条中间 NLL 候选明细或全部 SPR 原始曲线。所有公开候选共享同一亲本和实验体系，建模划分应避免把近邻变体随机拆分后夸大泛化能力。

## 论文原文

- 标题：Antibody design using LSTM based deep generative model from phage display library for affinity maturation
- 作者：Koichiro Saka；Taro Kakuzaki；Shoichi Metsugi 等。
- 发表来源：Scientific Reports 11, 5852 (2021)。
- 归档文本版本：正式发表版（Version of Record）。
- 发布日期：2021-03-12
- DOI：`10.1038/s41598-021-85274-7`
- PMID / PMCID：PMID 33712669 / PMCID PMC7955064。
- 本地文件：`articles/SAKA_2021-03-12_ScientificReports-Version-of-Record.pdf`
- 文件大小：1.75 MiB（1,834,950 bytes）
- SHA-256：`d89c369f266f8b80854b5b9f66d9374c6bdb96616ff026cd9a3c0e38237d79c9`
- 文本许可：CC BY 4.0。
- 补充材料：`Saka/41598_2021_85274_MOESM1_ESM.docx` 及两张 JPG；另保存主文 Table 1–3 页面和 Table 1 原始 PNG。
- 引用数（查询快照）：151（[OpenAlex W3135044423](https://openalex.org/W3135044423)，查询于 2026-09-24）。

## 仓库内容

一手入口为 [Scientific Reports 正式论文页](https://www.nature.com/articles/s41598-021-85274-7)、主文 Table 1–3 和三项 Supplementary MediaObjects。版本名 `snapshot-2021-03-12` 取自正式发表日期 2021-03-12；这是 publisher 公开交付的选择性快照，不是论文全部底层实验数据的归档。

```text
snapshot-2021-03-12/
└── Saka/
    ├── Table-1.html
    ├── Table-2.html
    ├── Table-3.html
    ├── 41598_2021_85274_Tab1_HTML.png
    ├── 41598_2021_85274_MOESM1_ESM.docx
    ├── 41598_2021_85274_MOESM2_ESM.jpg
    └── 41598_2021_85274_MOESM3_ESM.jpg
```

三个表页按 publisher 字节保存。Table 1 在网页中是图片，因而同时保存表页 HTML 与原始 PNG；Table 2 和 Table 3 的 HTML 含真实 table 元素。DOCX 只收录 Supplementary Fig. 1–2 的图注，两张 JPG 是对应图像。

## 数据结构

### 主文表与补充对象

Table 1 是重链库设计图，给出固定 framework/CDR 片段、X1–X17 与 Kabat 位置及每个位置允许的氨基酸。其重链模板按 X1–X17 顺序写为：

```text
QVQLVQSGAEVKKPGSSVKVSCKASGGX1FSX2YX3ISWVRQAPGQGLEWMG
X4X5X6PIX7X8X9AX10YAQKFQGRVTITADESTSTAYMELSSLRSEDTAVYYCAR
DX11X12VX13X14X15X16X17GAFDIWGQGTLVTVSS
```

Table 2 有 1 行表头和 3 条 panning-round 汇总。Table 3 有两层表头，第一层为 Analysis、Position、NLL、KD，第二层列出 17 个位置；其后 21 条数据分别为 10 ML、10 Freq 和 1 Control。17-position 残基串在当前版本内均唯一，但它们属于同一亲本背景。

DOCX 可作为 Office Open XML 归档完整解析，含 0 个 Word table。两张 JPG 分别为 ELISA 汇总图和亲本/最佳候选 SPR sensorgram；PNG 为 Table 1 图。图像没有可直接读取的逐事件原始数组。

### 字段说明

| 文件 | 字段（原始拼写） | 原始表示、单位、方向与来源 |
| --- | --- | --- |
| Table-2.html | Panning round | 整数字符串；当前版本观察值为 `0`、`1`、`2`，分别代表 panning 前、一次和两次 panning 后。 |
| Table-2.html | NGS reads | 原始测序 read 计数，整数、无单位。 |
| Table-2.html | Total sequences | 作者用 BLAST-based software 提取的具有抗体结构的 sequence 计数，整数、无单位。 |
| Table-2.html | Unique sequences | Total sequences 中的唯一 sequence 计数，整数、无单位。 |
| Table-2.html | Unique/Total | 作者给出的 Unique sequences / Total sequences 比例，小数字符串、无单位。 |
| Table-3.html | Analysis | 来源组字符串；当前版本观察到 `ML`、`Freq`、`Control` 三种值，具体含义见下表。 |
| Table-3.html | 28; 31; 33; 50; 51; 52; 54; 55; 56; 58; 96; 97; 99; 100; 100a; 100b; 100c | Kabat 编号位置的单字母残基；21×17 均为标准 20-aa 字母，`100a`–`100c` 是插入编号。 |
| Table-3.html | NLL | LSTM negative log likelihood，小数字符串；低值对应高模型 likelihood。Control 用 `-`，不是数值零。 |
| Table-3.html | K D (M)（HTML 中 D 为下标） | SPR steady-state KD，科学计数字符串，单位 M，低值表示更强亲和力；21 行均有有限值。 |
| Tab1_HTML.png; MOESM2/3 JPG | 像素与图注 | 库设计、ELISA 450-nm 吸光度、SPR 响应 RU/时间等图形信息；不是结构化测量字段。 |

**`Analysis`（Table-3.html；取值范围依据：当前版本完整扫描）**

| 原始取值 | 当前记录数 | 含义 |
| --- | --- | --- |
| `ML` | 10 | LSTM 生成序列中公开的最低 NLL 组。 |
| `Freq` | 10 | 两轮 panning 后 NGS read count 最高组。 |
| `Control` | 1 | F02 亲本参照。 |

### 数据示例

| Analysis | 17-position 残基串 | NLL | K D (M) |
| --- | --- | --- | --- |
| ML | WRLVVSSGRRAPRGRPH | 9.01 | 5.7E-07 |
| ML | WRLVVDSGVRVPSGRPH | 9.27 | 4.2E-08 |
| Control | TSAGIIFGTNAPVARPR | - | 7.7E-05 |

三行分别是 Table 3 的第 1 条 ML、亲和力最强的公开 ML 和最后一条 Control。每行代表一个抗体构建体的 17 个可变位点、模型分数和一次汇总 KD；把残基串代入 Table 1 模板得到完整 VH 属于后续 processed 层派生。

## PDB 数据库

PDB 子任务状态为 blocked/partial：当前没有可辩护的 F02–犬尿氨酸 PDB 锚点。审计覆盖主文、三张主文表、补充 DOCX/JPG、相关 F02 专利线索和 RCSB full-text 检索。论文所述晶体分析没有给出 accession；专利披露了相关序列、晶体分析叙述和图，但没有可下载的原子坐标或 PDB ID。

RCSB 检索曾返回 1MCJ 和 5X2M。1MCJ 是免疫球蛋白轻链二聚体与肽配体体系，5X2M 是鱼味觉受体与 glutamine 体系，均与论文 F02 构建体无证据连接。犬尿氨酸是小分子，保存 IDO 等代谢酶结构也不能形成抗体–抗原参考映射，因此两类候选均被拒绝。

本版本接受的 PDB 锚点为 0，FASTA 与 mmCIF 文件数均为 0，也未创建空 `pdb/` 目录。该结构缺口不影响论文公开表格和附件作为 `public-subset` 接入，但 PDB 子任务仍保持 partial，不能据此声称完整研究数据或结构覆盖已经获得。

## 使用方式

调用者先把 `dataset_root` 设为当前 source version 目录。Table 3 的前两行是合并表头；读取时保留 publisher 原始科学计数法和 Control 的 `-`。若要重建 VH，应在 processed 层按 Table 1 的 X1–X17 顺序显式生成并保存转换规则，raw source 不承担这一派生。

## 采集过程记录

1. 2026-09-18 核验 publisher 正式论文页、发布日期、DOI、CC BY 4.0 和全部公开补充入口，在 `SRC_R53_SAKA/.staging/snapshot-2021-03-12.partial` 取得正式论文、三张表页、Table 1 PNG、DOCX 和两张 JPG。
2. 实际解析 DOCX 后确认其中没有数据表，随后直接保存并解析主文 Table 1–3；Table 1 为图片，Table 2/3 为 HTML table，未用 OCR 生成伪原始表。
3. 独立核验 8 个文件的大小、SHA-256 和格式：PDF 13 页，DOCX 18 个 ZIP 成员，Table 2 为 3 条数据，Table 3 为 21 条数据，全部图片可读。
4. 2026-09-24 重新逐段核对 Methods、Results、图表与补充材料，厘清 959 条训练序列、200 万条生成序列、52 条实验候选和 Table 3 的 21 条逐行公开记录之间的关系；同时确认其余 32 条 ML 候选只在 Figure 10 聚合展示。
5. 重新读取 Table 1 后确认公开模板可与 Table 3 残基确定性还原完整 VH；再核对 WO2015083764 家族专利，Control VH 与 SEQ ID NO:95 完全一致，但论文的 VL 连接仍未达到确定映射强度。
6. 以 DOI、PMID 和题名检索 NCBI SRA、BioProject、GEO，并复核 RCSB 与专利结构线索；没有发现全量序列 accession 或 F02 PDB accession，PDB 子任务保留 blocked/partial。
7. 正式论文原名 `s41598-021-85274-7.pdf` 按项目约定改为 `SAKA_2021-03-12_ScientificReports-Version-of-Record.pdf`；改名前后均为 1,834,950 bytes，SHA-256 未变。
8. 本地 README 写入后立即同步共享 source；固定 markdownlint、完整文件 audit、精确 SHA-256、workspace scope 和最终目录残留检查均通过后，将已核验公开子集原子发布。

## 参考文献

- [Saka et al. 2021，Scientific Reports 正式发表版](https://doi.org/10.1038/s41598-021-85274-7)。
- [主文 Table 1：F02 library 设计](https://www.nature.com/articles/s41598-021-85274-7/tables/1)。
- [主文 Table 2：NGS 汇总](https://www.nature.com/articles/s41598-021-85274-7/tables/2)。
- [主文 Table 3：逐行公开的抗体与 KD](https://www.nature.com/articles/s41598-021-85274-7/tables/3)。
- [WO2015083764A1 专利记录](https://patentscope.wipo.int/search/en/detail.jsf?docId=WO2015083764)。
- [Chugai 公司概要](https://www.chugai-pharm.co.jp/english/profile/about/outline.html)与[公司历史](https://www.chugai-pharm.co.jp/english/profile/overview/history/age01.html)。
- [RCSB 1MCJ](https://www.rcsb.org/structure/1MCJ)与[5X2M](https://www.rcsb.org/structure/5X2M)（检索后拒绝的候选）。

## 其他

### 数据范围和限制

本版本是 `verified public-subset onboarding`。它完整保存并验收了论文页面直接公开的表格与补充材料，可用于研究公开 20 条候选和 1 条亲本在共享 VH 背景下的 NLL 与犬尿氨酸 KD；完整研究 acquisition 仍未完成。全量 NGS、959 条训练序列、200 万条生成序列、32 条额外 ML 实验记录、确定的 VL 与仪器级 SPR 数据不在当前交付中。

### 完整性与验收

交付含 8 个上游文件，共 2.40 MiB（2,516,778 bytes）。publisher 没有提供这些对象的统一 checksum；下表 SHA-256 是本次下载后的本地身份，结合 DOI、URL、文件大小和格式核验使用。

| 相对路径 | 大小 | SHA-256（本地计算） |
| --- | --- | --- |
| Saka/41598_2021_85274_MOESM1_ESM.docx | 23.38 KiB（23,938 bytes） | `2e5138dc46f82a617fb8b08c2e136a78800c547df49a5baee72df2155834f740` |
| Saka/41598_2021_85274_MOESM2_ESM.jpg | 50.65 KiB（51,865 bytes） | `1e2d09849b3460fd2c413b64ba621c1279e3154202e58776b178eb18e7ddb53b` |
| Saka/41598_2021_85274_MOESM3_ESM.jpg | 59.80 KiB（61,238 bytes） | `7bebe89f6dfd21ae560193b2fecc1acb4c560e348469f11c4ff453289dd86074` |
| articles/SAKA_2021-03-12_ScientificReports-Version-of-Record.pdf | 1.75 MiB（1,834,950 bytes） | `d89c369f266f8b80854b5b9f66d9374c6bdb96616ff026cd9a3c0e38237d79c9` |
| Saka/Table-1.html | 158.36 KiB（162,165 bytes） | `cf3b55a7255af7fb0bae9c2e3486a53b971813e0c52b18bc8d3e74e08f01ba34` |
| Saka/Table-2.html | 159.32 KiB（163,147 bytes） | `042f062f92f1ad14c5889aa4a27fdaac64cd2d0849f1625c48d8d3f1f77ed41b` |
| Saka/Table-3.html | 175.71 KiB（179,928 bytes） | `ef6ab317b33db651a68675343908af8ab28c3d37fc2e7ae8c37eb5cdc7eea5f4` |
| Saka/41598_2021_85274_Tab1_HTML.png | 38.62 KiB（39,547 bytes） | `9517501344e55149ce56757788e458cfdebd3953c5d4596022d317667aa062e9` |

### 许可和再分发边界

正式论文标明 CC BY 4.0，并说明文章中的图片及其他第三方材料在没有单独 credit line 时纳入同一许可。当前归档的主文表页、Table 1 图片和补充图未见排除它们的单独 credit line；使用和再分发时仍应保留作者、论文、DOI、许可及文件来源。该许可结论只覆盖当前 publisher 文章交付，不扩展到未公开的 NGS、晶体坐标、未来取得的作者数据或本次未归档的专利材料。

### 公开范围对照

| 研究中的对象 | 当前公开证据 | 当前状态 |
| --- | --- | --- |
| F02 重链库设计 | Table 1 的完整 VH 模板、17 个位置及允许残基 | 已包含；可在 processed 层还原 Table 3 各 VH |
| panning 与 NGS 规模 | Table 2 的 round 0/1/2 汇总 | 已包含统计；逐条 reads/序列未公开 |
| 最低 NLL 与高频候选 KD | Table 3 的 10 ML、10 Freq、1 Control | 已包含 21 条结构化记录 |
| 32 条分层 NLL 候选 | Figure 10 的聚合关系和论文分组统计 | 逐条序列与 KD 未取得 |
| SPR 原始响应 | Supplementary Fig. 2 的 parent/best 图片 | 没有原始 sensorgram 数组或逐 replicate 曲线 |
| F02 轻链与晶体结构 | 专利提供相关序列线索，论文无明确 VL ID/PDB accession | 映射与结构覆盖 partial |

## 待解决问题与处理进展

| 未决事项 | 当前证据与影响 | 当前处理 | 下一步与关闭条件 |
| --- | --- | --- | --- |
| 全量序列与 32 条额外 ML 候选未公开 | 论文只给 NGS 汇总、Figure 10 聚合统计和 21 行 Table 3；NCBI accession 检索无结果 | 正式版本限定为 `public-subset`，不从图中数字化或补造明细 | 作者或维护方发布能核验的序列/KD 文件后，新增版本并比对记录范围 |
| 论文实际使用的 VL 尚未唯一确认 | 专利 SEQ ID NO:95 与公开 Control VH 完全一致，专利的相关重链库实例使用 VL SEQ ID NO:97；论文未给专利或 VL 标识 | 记录为外部候选映射，不把专利 VL 写入 raw 或当作确定构建体 | 获得论文、补充材料或作者说明对 VL 的明确连接后关闭 |
| F02–犬尿氨酸结构没有 PDB accession | 论文称设计依据的晶体/突变数据 unpublished；专利只有结构叙述/图，无原子坐标；RCSB 候选不匹配 | PDB 子任务标为 blocked/partial；公开表格仍按已接受的部分接入发布 | 出现可验证 accession 或作者坐标，并完成 FASTA/mmCIF 双层验收后关闭 |
| 正文有两处筛选措辞不一致 | Methods 出现“round 2 高于 round 3”，但全文只报告 round 0–2；Results 一处写“highest NLL”，而 Methods 和表中实际选择为 lowest NLL | 采用与表格和其余 Methods 一致的口径：两轮后 read count 与最低 NLL；不据疑似笔误生成标签 | 作者勘误或方法说明明确原句后关闭 |
