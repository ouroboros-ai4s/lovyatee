---
- tags:
  - context
---

# SRC_R12_ASD 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [原始交付与记录](#原始交付与记录)
  - [字段说明](#字段说明)
  - [数据示例](#数据示例)
- [PDB 数据库](#pdb-数据库)
- [使用方式](#使用方式)
- [采集过程记录](#采集过程记录)
- [参考文献](#参考文献)
- [其他](#其他)
  - [完整性与验收](#完整性与验收)
  - [许可和再分发边界](#许可和再分发边界)
  - [公开范围对照](#公开范围对照)
- [待解决问题与处理进展](#待解决问题与处理进展)

## 数据集身份

- `source_id`：`SRC_R12_ASD`
- `source_version`：`2.0`
- 原作者或发布机构：NaturalAntibody / Arkadiusz Czerwiński 等

### 来源方背景

ASD 由 [NaturalAntibody 官方页面](https://naturalantibody.com/asd/)发布，页面将 2.0 标为当前版本，并给出非商业研究使用范围。论文版权页列出的责任主体为波兰什切青的 NaturalAntibody S.A.（KRS `0000887528`）；其[官网](https://naturalantibody.com/about-us/)介绍抗体工程数据与计算工具。这里的公司身份和 ASD 发布责任，与表中各上游实验或专利的原始权利主体应分别判断。

## 实验设计和数据口径

ASD 是多来源抗体—抗原配对汇编，2.0 按 chains.antibody_chains、chains.target_chains 分离分子链，并保存研究和论文来源。binding 标签、KD、EC50、富集和结构配对等端点不能合并为统一 KD。patents、结构库和既有实验来源并非独立新实验。confidence 是来源置信注释，不是预测结合的实验值。旧论文和旧版规模不能替代 2.0 的 Delta snapshot 统计。数据以 Delta table 交付；必须应用事务 log 的 add/remove，只计 active parquet，不能拼接历史版本或忽略删除。

ASD 论文记录来源聚合、OCR/人工核验、序列补充与编号，不是新的统一亲和力实验。原来源可同时含 KD、IC50、delta-G、布尔标签及筛选代理量，必须根据每条记录的 affinity_type 和 provenance 解释。当前取得的是官方 2.0，对照论文旧聚合规模时不能将其直接当作本次 active snapshot 行数。 作者分别重建上游不足的序列、人工校验 OCR，并使用 RIOT 保留编号注释；这是来源提供的重建/聚合层，不是本项目 raw 补充生成。相同序列或亲本可跨 abbd、flab、skempiv2、ab-bind 等再收录，按来源和相同对象检查划分泄漏。论文 Methods/表中的早期 count 与 v9 的 patents、literature 等当前统计不同，保留本次实际 snapshot 为准。

## 论文原文

- 标题：ASD: antigen-specific antibody database
- 作者：Arkadiusz Czerwiński；Paweł Dudzic；Konrad Wójtowicz；Igor Jaszczyszyn；Weronika Bielska；Sonia Wrobel；Samuel Demharter；Roberto Spreafico；Victor Greiff；Konrad Krawczyk
- 载体与版本：mAbs
- 发布日期：2026-02-14
- DOI：`10.1080/19420862.2026.2623330`
- PMID / PMCID：41689452 / PMC12915772
- 本地文件：`articles/ASD_2026-02-14_mAbs-published.xml`
- 文件大小：153.55 KiB（157,236 bytes）
- SHA-256：4bc97b37019a6771a9cb97cf4f7f9aaf0205c633ffccd610ab5571a8be109527
- 文本许可：正式论文 XML 标明 CC BY-NC 4.0；与交付包 `LICENSE.txt` 分别核验
- 补充材料：经完整主文 XML 检查，无 supplementary-material/media 文件引用；不把外部数据仓库当作论文附件

## 仓库内容

来源身份：

- `kind`：`google-drive`
- `release_folder`：`1iSF3BZdDu2jjxIz3sSz5wjJMbPsAkPDM`
- `official_page`：`https://naturalantibody.com/asd/`

版本日期来自数据源 commit 或官方更新时间；正式版本名保留官方名称。以下树为已验收的上游 payload，不列项目 README、论文及 PDB 外部补充。

```text
2.0/
└── asd_2.0/
    ├── _delta_log/_last_checkpoint
    ├── _delta_log/_last_vacuum_info
    ├── _delta_log/._last_checkpoint.crc
    ├── _delta_log/._last_vacuum_info.crc
    ├── _delta_log/.00000000000000000000.crc.crc
    ├── _delta_log/.00000000000000000000.json.crc
    ├── _delta_log/.00000000000000000001.crc.crc
    ├── _delta_log/.00000000000000000001.json.crc
    ├── _delta_log/.00000000000000000002.crc.crc
    ├── _delta_log/.00000000000000000002.json.crc
    ├── _delta_log/.00000000000000000003.crc.crc
    ├── _delta_log/.00000000000000000003.json.crc
    └── …（其余来源文件保留原路径）
```

## 数据结构

### 原始交付与记录

| 原始文件 / sheet | 非空记录数 | 字段数 | 精确重复行 |
| --- | --- | --- | --- |
| `asd_2.0 / active Delta version 9` | 1177819 | 9 | 未去重；原样保留来源记录 |

只统计实际已解析的文件，未把来源介绍规模当作本次落盘统计。

本次完整 Drive 交付共 93 个文件、3.11 GiB（3,344,343,104 bytes）；Delta v0–v9 连续日志在实际协议约束下重放 add/remove，最终 v9 有 20 个 active Parquet、1,177,819 条记录，无 inactive Parquet。每个 active Parquet 的官方 Hadoop CRC 与 Delta 文件大小/numRecords 均独立核对；完整对象保留本地 acquisition SHA-256（不是官方密码学 checksum）。不 glob 历史日志或把多次 add 的记录重复拼接。20 个 active files 的顺序/身份可从日志重现，cache 报告不发布成旁路 manifest。逻辑表的九个顶层字段如下；未做重复行去重，记录数不是独立抗体、实验或生物对象数。

### 字段说明

dataset 为上游来源；affinity 和 affinity_type 共同解释原始读出及单位，二者在 Delta schema 中是字符串，不能默认有限浮点。chains 包含链序列和 RIOT numbering；metadata.target_pdb、target_uniprot、source_url、article_url 为结构与来源注释。nanobody/scfv 是分子形式标记；processed_measurement 是上游处理的信号，不当作独立实验。原样保留空值和字面 nan 等特殊编码。

实际 Delta schema：dataset/affinity/affinity_type/confidence/processed_measurement 为 nullable string；nanobody/scfv 为 nullable boolean；chains 为 struct，antibody_chains/target_chains 为 map<string,string>，antibody_chains_numbered 为 map<string,map<string,string>>，值允许 null；metadata 为 target_name/target_pdb/target_uniprot/source_url/article_url 的 nullable string struct。读出需按原 affinity_type 保留 M/nM、负 log、delta_g、ddg、ic_50、EC50、ka 等差异，不统一换算为 KD。实际特殊 affinity：fuzzy 的 h/m/l 分别 172,149/190,011/162,186；字面 nan 8,714；Kd (M) 的 I.C. 102（本包没有统一数值定义，保留原文，不猜检测阈值）；ic_50 的 >8.8 有 11 个删失读出；bool 同时有数值字符串和字面 False/True，不把其他 endpoint 的 0 或缺失当作阴性。confidence 的 high/medium/very_high 分别 374,684/190,869/612,266，是聚合来源置信注释。nanobody 有 127 个 null。

每行 chains 抗体 map 中含 heavy/light 槽位，不保证两条链都存在：共有 2,355,638 个 map 值，其中 175,114 为 null，282,166 为空字符串；实际非 null 长度为 0–467 aa。1,177,819 个 target map 值长度 6–34,350 aa，不能据“链序列”称全部是相同长度的完整 IgG/实验构建体。抗体/靶点含 X 的 map 值分别 9,159/2,536，不在 raw 中替换。literature 的六个链值含分号、星号或括号问号，其文件/原行号/字符位置在审阅 cache 留证；原字节不清洗。后续 processed 层需要单独解析这些原文异常，不能将它们默认当作可训练标准氨基酸串。

实际表头（保留原始字段名）：

- `asd_2.0 / active Delta version 9`：`dataset`、`affinity`、`affinity_type`、`chains`、`metadata`、`confidence`、`nanobody`、`scfv`、`processed_measurement`

字段原始表示与缺失统计（只统计审计解析结果，不在 raw 中填零）：

- `asd_2.0 / active Delta version 9`：缺失/特殊表示计数 `{"nanobody": 127}`；字段类型按 CSV 原始字符串或 XLSX 原类型保留。

### 数据示例

来自 `asd_2.0 / active Delta version 9` 的第一条真实记录；这里只摘录字段，不改写原始文件。

| 字段 | 原样值 |
| --- | --- |
| `dataset` | `abbd` |
| `affinity` | `6.0` |
| `affinity_type` | `-log Kd (M)` |
| `metadata` | `{'target_name': '', 'target_pdb': '4fqi', 'target_uniprot': '', 'source_url': 'https://huggingface.co/datasets/AbBibench/Antibody_Binding_Benchmark_Dataset', 'article_url': 'https://arxiv.org/abs/2506.04235'}` |
| `confidence` | `high` |
| `nanobody` | `False` |
| `scfv` | `False` |

每行按该来源的测量、配对或结构实例口径解释，不把结构表示或 replicate 当作新实验。完整字段保留在 payload 中。

## PDB 数据库

Active Delta snapshot metadata.target_pdb; target entry references are not per-antibody experimental complexes. Full native FASTA/mmCIF retain every canonical polymer; author/label chains must be selected from the original annotation and construct evidence.

当前接受锚点清单为 2227 个；最后一次审计有 0 个未完成两层配对。每个锚点取原样 per-entry FASTA 和完整 mmCIF，不嫁接 CDR、不生成逐变体重建序列。FASTA 的原始 header 保留 polymer entity 与 author/label chain；不猜测伙伴角色。只有全部接受锚点同时通过 FASTA 和坐标解析，且 FASTA entity ID 集合和完整序列与 mmCIF 的 canonical polymer 一致，才算完成。

PDB 文件审计摘要：4454 个文件，2.80 GiB（3,001,266,878 bytes）；inventory SHA-256：`de52d1ee671e226e76da6099d196bbf7ab41ad92abd1425a64d835c49667dbc5`。摘要按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接计算。缓存最初包含选择链/重写 header 的 FASTA，已清理本轮这类 staging 副本；现在只接受 RCSB native per-entry header。

## 使用方式

由调用者先赋值 `dataset_root`（Path），再读取；不在这里清洗或转换标签。

```python
import pandas as pd
table = pd.read_parquet(dataset_root / "asd_2.0" / active_parquet_filename)
```

active_parquet_filename 必须来自已审计的 Delta active file 清单，不能随意 glob 后拼接。

## 采集过程记录

2026-09-18：读取项目规范和执行清单，解析一手 API/tree/Drive 对象 metadata，固定本轮版本与文件身份。下载到共享 source 下 `.staging/<version>.partial`；HTTP 大文件使用精确 byte range 和全文件上游 checksum，Drive 保留对象 ID、MIME 与字节数，失败部分可续传。2026-09-18 按用户要求调整本轮 HTTP 为直连优先、连接失败回退环境代理，15 分钟后重试直连；各线程复用连接且保留 TLS/CA 校验。重启任务保留所有文件断点。

独立 audit 重新计算 hash、完整解析已取得表格并检查 PDB 两层文件；归档只有完成逐成员/CRC 与路径安全检查后才通过。PMC 访问被拒绝、非 OA XML 不可得和间歇代理连接失败均保留缺口，未关闭 TLS 验证。PDB 缓存原始性检查发现错误后清理本轮衍生 header 文件并重做。

README 草稿每次写入后立即同步到 staging 同名文件，随后运行 skill 固定 Markdownlint 配置。发布脚本仅在逐文件、论文/PDB、README 同步与固定格式检查通过后原子发布；发布状态与 接入过程记录 同步。

2026-09-18：主文从 `ASD_PMC12915772.xml` 改名为 `ASD_2026-02-14_mAbs-published.xml`，日期取该论文版本发布日期，改名前后大小和 SHA-256 一致。

2026-09-18：全部 93 个公开对象取得后，audit_delta.py 重放 v0–v9，核验 20 个 active Parquet 的官方 Hadoop CRC、Delta size/numRecords、全对象 hash，得到 1,177,819 行与 2,227 个 metadata.target_pdb 唯一锚点。2,227 对完整 native FASTA/mmCIF 全实体集合与 canonical 序列核对通过。全文 Methods/Availability 已阅读，没有 supplementary-material/media 文件引用。review_ready_content.py 遍历 active 行，复验类型、map 链、缺失/遮蔽、非数值和删失文本；六个原文链异常明确保留。冻结实际 LICENSE 边界后再执行发布复验。

2026-10-09：按新版 README 合同补充来源方身份及动态待办，清理论文 XML 许可字段的重复粘贴文本；93 个上游文件、Delta v9 及 2,227 对 PDB 参考未改动。

## 参考文献

- <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12915772/fullTextXML>
- <https://doi.org/10.1080/19420862.2026.2623330>
- <https://naturalantibody.com/asd/>
- <https://www.rcsb.org/>

## 其他

### 完整性与验收

上游声明 93 个文件；最近审计通过 93 个，待取得/核验 0 个。

公开包独立验收、论文/补充材料对照及 PDB 配对审计通过；不宣称全部底层实验数据取得。没有独立 manifest/API 响应/审计 JSON 发布在 source version 中；临时产物只保存在共享 cache。

| 上游 payload | 大小 | SHA-256 |
| --- | --- | --- |
| `asd_2.0/_delta_log/_last_checkpoint` | 4.68 KiB（4,797 bytes） | `71709e8a80f87bb33d2735603d152b1e5ec8f29945f2d471e1275f637cdbb108` |
| `asd_2.0/_delta_log/_last_vacuum_info` | 3 bytes | `ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356` |
| `asd_2.0/_delta_log/._last_checkpoint.crc` | 48 bytes | `8eb1922ed18d2fba5aaae0694f5378c4f56c363d9f2c4fcaffc52779f85306ed` |
| `asd_2.0/_delta_log/._last_vacuum_info.crc` | 12 bytes | `2aaf95c1d45e57e005e7434bce516a2a1edf9e8455e7818ae9af1f863f6bee35` |
| `asd_2.0/_delta_log/.00000000000000000000.crc.crc` | 228 bytes | `d894d81fc587fb5d570b17572f8082fe400437e208368d10d42a57c904890c8f` |
| `asd_2.0/_delta_log/.00000000000000000000.json.crc` | 232 bytes | `419918466073bafef931a253cdbb842eb1793e1eb9b1d56fccf68671c5374c9f` |
| `asd_2.0/_delta_log/.00000000000000000001.crc.crc` | 228 bytes | `b0122961d5b4651271777f419c201732dfebce7d1c2c95f60b520a9f7afa39fb` |
| `asd_2.0/_delta_log/.00000000000000000001.json.crc` | 248 bytes | `a8385b26e40b0f3e37ea790923d38160686e7c59fc8504b98cd5d2fe3a4cd383` |
| `asd_2.0/_delta_log/.00000000000000000002.crc.crc` | 228 bytes | `966d94e1333114878893fdcc08eb6abc937f2d010cbbf36fb61435921b26c3b2` |
| `asd_2.0/_delta_log/.00000000000000000002.json.crc` | 248 bytes | `4b3fb681353ffa377af35c87d6df27f952e40028158b24fab8888c502e0b4448` |
| `asd_2.0/_delta_log/.00000000000000000003.crc.crc` | 228 bytes | `f8c6e84edfd0be0666c31e1506ba2f9516c170967354190eed92b7fa79ae721e` |
| `asd_2.0/_delta_log/.00000000000000000003.json.crc` | 12 bytes | `1509e437c8e349ce6f8fe0008e42553ddadbf8c4e9c6f7fdd9a22b27b2735790` |
| `asd_2.0/_delta_log/.00000000000000000004.crc.crc` | 228 bytes | `dbe279465b0f0fe5a63d959d883f9876d5d64e494ae48d9ca1576f96c3e6ead5` |
| `asd_2.0/_delta_log/.00000000000000000004.json.crc` | 12 bytes | `c9067bb0e8412d8ab1c4cecdc53371454cbb41d7d17d43509773bf7f0bffd5bd` |
| `asd_2.0/_delta_log/.00000000000000000005.crc.crc` | 228 bytes | `32973465c34c04673519e5d46fe46572ebbd838b7e0b28ca9e8d99753bde84d0` |
| `asd_2.0/_delta_log/.00000000000000000005.json.crc` | 248 bytes | `72385eebb66304ebf1ccf3b71ea867f3b04cadb0cd563bcc87809034fbb8edfa` |
| `asd_2.0/_delta_log/.00000000000000000006.crc.crc` | 228 bytes | `f7c9ab4fe7b52548641c1e68b50cf22ee09d8aa3698f1e77a5156279f6107579` |
| `asd_2.0/_delta_log/.00000000000000000006.json.crc` | 12 bytes | `bdd398584ba2473a3c5bcb4aca23c2c3ea70d6a4a944f061f5df5b3a94f71087` |
| `asd_2.0/_delta_log/.00000000000000000007.crc.crc` | 228 bytes | `0f624bb14175248ccb7a4feaf7216d9220c08d2eb0ea233b57b39b921024a9bc` |
| `asd_2.0/_delta_log/.00000000000000000007.json.crc` | 12 bytes | `1c734722e34d1fdadb92ccbf9c69e8551b6ba9e5ddd6240455f7ac88f3cd7655` |
| `asd_2.0/_delta_log/.00000000000000000008.crc.crc` | 228 bytes | `3bc21baa106a80e158c3fd674b50544f2155773433fddfaaf027a68697b05ddc` |
| `asd_2.0/_delta_log/.00000000000000000008.json.crc` | 248 bytes | `08630726136dbb8da4b98e15ca2ca34b42baaf7bca590415e3c267dfe6a00c04` |
| `asd_2.0/_delta_log/.00000000000000000009.crc.crc` | 228 bytes | `d60fd8d0899265366ec2fe115d0cd86632910e607fb350b7bbc0ea9af17a00e2` |
| `asd_2.0/_delta_log/.00000000000000000009.json.crc` | 248 bytes | `1df7b592ae2edfac210764c68177dac91e4f5dfc84d7e7670e5c0e34a2b4d50a` |
| `asd_2.0/_delta_log/.00000000000000000010.checkpoint.parquet.crc` | 260 bytes | `9bfe28747c46d98df7ffa5973061c0330e97fcbe66a6de8c7d87e11825d85d2e` |
| `asd_2.0/_delta_log/.00000000000000000010.crc.crc` | 228 bytes | `99de83aa12e50a4dcf687ab0b94a4e24838881fadd698e778fb621569c739ac6` |
| `asd_2.0/_delta_log/.00000000000000000010.json.crc` | 12 bytes | `64c9a2baba833db63146488c4b2d8b980d20300d5eb4e205c20d7bba64444b63` |
| `asd_2.0/_delta_log/.00000000000000000011.crc.crc` | 228 bytes | `58becc47a64d1309a1035460349cdb9be88ef4be49e80926fa40da622145fcc8` |
| `asd_2.0/_delta_log/.00000000000000000011.json.crc` | 12 bytes | `de213b9699fb04852d1c7510b57fd2ab796d026370bd05179bb7007343f37c4b` |
| `asd_2.0/_delta_log/00000000000000000000.crc` | 27.37 KiB（28,031 bytes） | `ddb9ee754a6fb1f6739ba8b26da6cd2894a0c7dd365cdc78aa8b912a6451d4f5` |
| `asd_2.0/_delta_log/00000000000000000000.json` | 27.70 KiB（28,368 bytes） | `be812d864b0a849e9c6fba11687dcade20068c45262ea9b962c1c69f471f468e` |
| `asd_2.0/_delta_log/00000000000000000001.crc` | 27.41 KiB（28,067 bytes） | `876f0c6add1bf3ac223fb2c7f99ed75e2c10604b2d818333ee3777642c678040` |
| `asd_2.0/_delta_log/00000000000000000001.json` | 29.82 KiB（30,533 bytes） | `c2941a15933402d05c893ac545baaf7f04cb5ba62e6c3137a6f260a485df6151` |
| `asd_2.0/_delta_log/00000000000000000002.crc` | 27.37 KiB（28,028 bytes） | `9c856e2ed067998e6d024d5c3a4b00d154810946a237d1e18fb4691c9b6b30cf` |
| `asd_2.0/_delta_log/00000000000000000002.json` | 29.78 KiB（30,494 bytes） | `ab46be4aab2e424b03fb642194c02d4272da96602ae21dc8657e732b58e2562e` |
| `asd_2.0/_delta_log/00000000000000000003.crc` | 27.37 KiB（28,028 bytes） | `559589dc00dc3b220363ce764a1125dadb87934ac6536155315c0027c2ed90b9` |
| `asd_2.0/_delta_log/00000000000000000003.json` | 439 bytes | `83df979e8861c6ca29abaf7a0f35ddf1b2765d45fa98aba53811e7fac7305d6b` |
| `asd_2.0/_delta_log/00000000000000000004.crc` | 27.37 KiB（28,028 bytes） | `94313c4d87fd666036a6dc91d7c6a71e011e35d617d77ac330528b7a5f409c89` |
| `asd_2.0/_delta_log/00000000000000000004.json` | 358 bytes | `9f23c3a715abde57bffe9231fc3688d76aa181e06e36890e7893bbac8472429a` |
| `asd_2.0/_delta_log/00000000000000000005.crc` | 27.39 KiB（28,052 bytes） | `80084cfa9784311e2abd368d3026b63097af4a26026d773f5e802fbec7b904f6` |
| `asd_2.0/_delta_log/00000000000000000005.json` | 29.80 KiB（30,518 bytes） | `905e9a8ec88006e7de3e9e360c7757be2a981217dc84b181f4c409d3c721b120` |
| `asd_2.0/_delta_log/00000000000000000006.crc` | 27.39 KiB（28,052 bytes） | `c7caed380623638b6125f44cef33d903acba3e804e398a89aac0e01a9587db1c` |
| `asd_2.0/_delta_log/00000000000000000006.json` | 439 bytes | `c7171e20a43915dec523a30ef48c768e82697df01f5663ec0d3ef27044665691` |
| `asd_2.0/_delta_log/00000000000000000007.crc` | 27.39 KiB（28,052 bytes） | `2fb65f8cb96ab42d91f5d4f2a878b7b3fe22347a0926376644d652dd56e64023` |
| `asd_2.0/_delta_log/00000000000000000007.json` | 358 bytes | `d063cb64ebe9c32dd31ba4412efb6d4a2e796d5aed16d7279175537041562cab` |
| `asd_2.0/_delta_log/00000000000000000008.crc` | 27.37 KiB（28,023 bytes） | `39d477623e8974e5c6893b1499df423a2b311133e3c669a8507633fc0651d20f` |
| `asd_2.0/_delta_log/00000000000000000008.json` | 29.77 KiB（30,489 bytes） | `3f05770afe3ed0e23d56d3b324cb14c03c3b40a298ad8d6040ed89922ebe6220` |
| `asd_2.0/_delta_log/00000000000000000009.crc` | 27.38 KiB（28,040 bytes） | `37b1b949c085969ba56627a5673ae29cea0d73dc40299bcd6fc09f087c59da58` |
| `asd_2.0/_delta_log/00000000000000000009.json` | 29.79 KiB（30,506 bytes） | `0b82f75e2f548875d5306457ccf586e4dfb2052af04a8da9e477863045b0eeca` |
| `asd_2.0/.part-00000-c98d01e8-144f-4a77-a1c3-975c5d1e3800-c000.snappy.parquet.crc` | 935.13 KiB（957,572 bytes） | `9806a770460403dfc1dd9438dd67ed98003df56178dd8d620a799287da9ba6fd` |
| `asd_2.0/.part-00001-a0fcbb31-c899-475b-841e-ee3591094d4b-c000.snappy.parquet.crc` | 934.06 KiB（956,480 bytes） | `5ed7b200ab1afd371939bb1db3725553e74095c4fadc9991e894cd2a27d86dc9` |
| `asd_2.0/.part-00002-0bb88839-e8d0-4030-acb5-d386f5cc4256-c000.snappy.parquet.crc` | 937.54 KiB（960,044 bytes） | `5c25cc423c8360ebcda52edddb6b9b60ff2ef9a23272078042efca948d15ef95` |
| `asd_2.0/.part-00003-bc0f1d7e-b4b8-4243-b2f0-1b72324b63a1-c000.snappy.parquet.crc` | 934.13 KiB（956,552 bytes） | `734d2c8642f645dee1fdd268cb52076a1e1bc18d37a2b57298e5b130c4cee5cd` |
| `asd_2.0/.part-00004-40a4abd0-9a57-4686-9b44-fdcb594b0108-c000.snappy.parquet.crc` | 935.54 KiB（957,988 bytes） | `f2538628761afc0768574aea4e3fc870ffd1f967bdacf5cc04ab80124ddcf6ee` |
| `asd_2.0/.part-00005-8828c56e-0341-4b9a-9c75-d05618adf6b1-c000.snappy.parquet.crc` | 936.51 KiB（958,988 bytes） | `b38b544fd6d1116d7a25375a57285b235529439f1a61dd957393df6ffcdbc140` |
| `asd_2.0/.part-00006-680aced4-fb5e-4f4d-8e3e-e185d8ad25a7-c000.snappy.parquet.crc` | 932.65 KiB（955,036 bytes） | `f4679ec36cd3afd3e5bf2cc68ff7cf4fc1aed5afd73194ee1030f410811b6970` |
| `asd_2.0/.part-00007-addcee63-bbac-4b4e-867f-9963248fd77b-c000.snappy.parquet.crc` | 935.39 KiB（957,840 bytes） | `cd98b59b0b9efc06fc959e42332908b03802bfe351122cfea76bb9c26cfc2706` |
| `asd_2.0/.part-00008-dab48e8c-3816-4e8c-89a3-cca4d171da2c-c000.snappy.parquet.crc` | 936.09 KiB（958,552 bytes） | `9fe1d1ed3cffc50e85d115a82757f59878b089bcc5e49577e75e22f771378956` |
| `asd_2.0/.part-00009-538462f4-192c-4d20-9b9c-39ad7afd81c4-c000.snappy.parquet.crc` | 937.60 KiB（960,100 bytes） | `872aafe9839d437db3d7c6fc6c7d467fffe3807a596c8bbd3deee5f1b3fc3c4a` |
| `asd_2.0/.part-00010-153610d9-5610-4431-aed5-8e7d26c86c64-c000.snappy.parquet.crc` | 936.09 KiB（958,552 bytes） | `278050f718ab37e3da80322aea07b41d8165539d0abae9681b396b8c3545010f` |
| `asd_2.0/.part-00011-0097e1c9-6812-4fb7-ac70-b35b21227613-c000.snappy.parquet.crc` | 937.85 KiB（960,356 bytes） | `557d1a9451d3b570616f3e69edaa89a62fa27a0ad91ac5a1ba6bcb7c115269b0` |
| `asd_2.0/.part-00012-8a1d7492-bd29-4038-8023-97aa00394ab9-c000.snappy.parquet.crc` | 941.18 KiB（963,772 bytes） | `667696b8b8c6bcee564c036bbb6fdaf8e721a46a052ab65ab02a72a95a838df5` |
| `asd_2.0/.part-00013-285ac7a9-b9f3-40dc-a60d-6c00c46fded3-c000.snappy.parquet.crc` | 936.03 KiB（958,496 bytes） | `189ce75e05adb090e14ae3b0675b95af5e4011ce4f0dbcd943d171144f1dd2e8` |
| `asd_2.0/.part-00014-c69b1502-53f5-41ab-8bcb-da717ba5b910-c000.snappy.parquet.crc` | 932.65 KiB（955,032 bytes） | `2a7604f57c6ae2ab768e0b8f449f670270d37b54cdd024608cb99a275eea3ce8` |
| `asd_2.0/.part-00015-c7d762b2-b4f7-4b3f-91f0-189c5fc5700d-c000.snappy.parquet.crc` | 937.27 KiB（959,760 bytes） | `53c39a4b52eb8e9bcc699481d3d1bada9ab5e79295bd4425241987ce1d8790ef` |
| `asd_2.0/.part-00016-404fa71e-6700-4377-80d0-e292e6157179-c000.snappy.parquet.crc` | 932.54 KiB（954,916 bytes） | `ea03b382f30c5e73decf04dc34a9898f08933e7b9a24ba49eb040c739c514fbf` |
| `asd_2.0/.part-00017-f382c65c-6b53-44b2-8446-826daa647930-c000.snappy.parquet.crc` | 933.90 KiB（956,316 bytes） | `e3518605903466262dbfbb6d6bbb66f94f6d218cbef5cd02033e85a5e7eb295a` |
| `asd_2.0/.part-00018-366c525f-f3c3-4509-b721-b51fa5635a5b-c000.snappy.parquet.crc` | 935.10 KiB（957,544 bytes） | `42a97c0499bd1697f266a59b05692d09d19272e9843278a20c6d60af853be4fc` |
| `asd_2.0/.part-00019-e22506d4-1ad2-4b31-be9d-5b02f2fef76a-c000.snappy.parquet.crc` | 937.47 KiB（959,968 bytes） | `4e4501abd6035ad145f947c83c4c88fa033bba5f8dae877e82c8c9767c7a7405` |
| `asd_2.0/antibodies.csv` | 693.81 MiB（727,516,431 bytes） | `603901d2088ef91ca551fc020ac19fa74e1d801575b01aba6a00e1cc4cf2ee78` |
| `asd_2.0/nanobodies.csv` | 77.60 MiB（81,369,809 bytes） | `a0eae8c6d2d71a50f5d5351fc17bbb180fe0d4557429513c97ba55a5b0e4c8fa` |
| `asd_2.0/part-00000-c98d01e8-144f-4a77-a1c3-975c5d1e3800-c000.snappy.parquet` | 116.89 MiB（122,567,748 bytes） | `1f44d3c7c775f4deac2b37056a49f7f67e4bb18612f4b39e87e9137af198bf7a` |
| `asd_2.0/part-00001-a0fcbb31-c899-475b-841e-ee3591094d4b-c000.snappy.parquet` | 116.76 MiB（122,428,157 bytes） | `dff3c8b7323ff5dee5f3ffef8f97cb2c9331290be257ed5a3c710e7fde89b6fe` |
| `asd_2.0/part-00002-0bb88839-e8d0-4030-acb5-d386f5cc4256-c000.snappy.parquet` | 117.19 MiB（122,884,443 bytes） | `1e505a2d13c7d1101ea42f1cddb1c42c8b2819a9132099f232051aa7d724c1b6` |
| `asd_2.0/part-00003-bc0f1d7e-b4b8-4243-b2f0-1b72324b63a1-c000.snappy.parquet` | 116.77 MiB（122,437,619 bytes） | `7897166fa6aa4d821d845392be9f8f6c1975c2b306651bb682055ddfd6c2da6c` |
| `asd_2.0/part-00004-40a4abd0-9a57-4686-9b44-fdcb594b0108-c000.snappy.parquet` | 116.94 MiB（122,621,207 bytes） | `8aa04fa667b8ff23e32c2c984caaccc22120e6174344c452300042cc549000c1` |
| `asd_2.0/part-00005-8828c56e-0341-4b9a-9c75-d05618adf6b1-c000.snappy.parquet` | 117.06 MiB（122,749,123 bytes） | `8ba333cc87e36fe0b605f089e057b056aa037eabc726ee402c98b7d2deb1e204` |
| `asd_2.0/part-00006-680aced4-fb5e-4f4d-8e3e-e185d8ad25a7-c000.snappy.parquet` | 116.58 MiB（122,243,388 bytes） | `accbd710d0cbc9248ffe0e25b7f1fba2186826ce9bd80122884b1fefad001104` |
| `asd_2.0/part-00007-addcee63-bbac-4b4e-867f-9963248fd77b-c000.snappy.parquet` | 116.92 MiB（122,602,210 bytes） | `de261ce12d4746736843d87e1ebe94d70e331689ce8377f9b1367df79966e652` |
| `asd_2.0/part-00008-dab48e8c-3816-4e8c-89a3-cca4d171da2c-c000.snappy.parquet` | 117.01 MiB（122,693,319 bytes） | `1c3b1de540a0b592163dfa4ab8ac561b2804331d14a157c087dbf32c25992360` |
| `asd_2.0/part-00009-538462f4-192c-4d20-9b9c-39ad7afd81c4-c000.snappy.parquet` | 117.20 MiB（122,891,393 bytes） | `b9f39d27a0d5d411b864f0a8b17ed0a923a599f19bc9b29629daf24a0bac10d8` |
| `asd_2.0/part-00010-153610d9-5610-4431-aed5-8e7d26c86c64-c000.snappy.parquet` | 117.01 MiB（122,693,537 bytes） | `ccf8eb7346e2e910850d8c75a177517f98ebb7d1d6f7e22f62007109185fa2c0` |
| `asd_2.0/part-00011-0097e1c9-6812-4fb7-ac70-b35b21227613-c000.snappy.parquet` | 117.23 MiB（122,924,286 bytes） | `32c4bb5c0311e82210b1d5d7d7932a6463f05689ee7da0bcc03b25fb765b399f` |
| `asd_2.0/part-00012-8a1d7492-bd29-4038-8023-97aa00394ab9-c000.snappy.parquet` | 117.65 MiB（123,361,322 bytes） | `9561ed249bb83b937f8aa4d12016e4cfa0c3c658af6b729f77e1734ad24832b0` |
| `asd_2.0/part-00013-285ac7a9-b9f3-40dc-a60d-6c00c46fded3-c000.snappy.parquet` | 117.00 MiB（122,686,199 bytes） | `1e472c08b3ed3db0c1a46bc1de90386f2d2ac51e08f50dac02dc15d9e18b541b` |
| `asd_2.0/part-00014-c69b1502-53f5-41ab-8bcb-da717ba5b910-c000.snappy.parquet` | 116.58 MiB（122,242,714 bytes） | `1d0c9ce86013b510f8fa27925468387c2f109a9ba6e8a6d8bb0f40d060d6566b` |
| `asd_2.0/part-00015-c7d762b2-b4f7-4b3f-91f0-189c5fc5700d-c000.snappy.parquet` | 117.16 MiB（122,847,907 bytes） | `5142c02b1d75c457c48b8d375ba4670d54548a51cbb201b8f7c5bf7399055773` |
| `asd_2.0/part-00016-404fa71e-6700-4377-80d0-e292e6157179-c000.snappy.parquet` | 116.57 MiB（122,228,182 bytes） | `36c12ce30cc8348cbf96bcd207d1e86dc0278f3b1d9b8606367233d1ec8d8923` |
| `asd_2.0/part-00017-f382c65c-6b53-44b2-8446-826daa647930-c000.snappy.parquet` | 116.74 MiB（122,406,991 bytes） | `7e8d8b8b35c90baec54947578fd4c58f4cd2b0892b7f7a40f091c7a2017d3258` |
| `asd_2.0/part-00018-366c525f-f3c3-4509-b721-b51fa5635a5b-c000.snappy.parquet` | 116.89 MiB（122,564,473 bytes） | `49a3ac3d852a9d887ebd9cb09eb6caec7572929777c0f7ac3a76fd7091c672ea` |
| `asd_2.0/part-00019-e22506d4-1ad2-4b31-be9d-5b02f2fef76a-c000.snappy.parquet` | 117.18 MiB（122,874,538 bytes） | `6a9f5e27473e945e5dcbc2dc3fc56b8e2e4026f8188892fa34b48c98d04571d6` |
| `asd_2.0/scfv.csv` | 59.94 MiB（62,852,595 bytes） | `dfecf80cd03eb7246a8e6476647c0e5297aab1779f1b14913301340cdc66e802` |
| `asd_2.0/LICENSE.txt` | 18.89 KiB（19,346 bytes） | `3711f963c05d0be80d53e5923308a6dee31b203da23435c9cfb7c7b6e4dd5e19` |

### 许可和再分发边界

官方页面：非商业机构的非商业研究，CC BY-NC 4.0；商业用途需另行联系。此次不代用户联系或提交申请，上游组成部分仍需追溯。

本次交付 asd_2.0/LICENSE.txt 的实际标题为 Attribution-NonCommercial 4.0 International，和官方非商业研究范围一致；主文 XML 另明确 CC BY-NC 4.0。二者分别留证，不以论文许可代替数据许可。技术接入不承诺任何商业训练/商业用途已获授权；来源 metadata 保留每个研究引用。

### 公开范围对照

| 目标组成 | 当前证据 | 状态 |
| --- | --- | --- |
| 固定上游 payload | tracked config + 独立文件/格式审计 | 目标公开文件验收通过 |
| 论文原文 | 一手 DOI 和取得文件 hash；不可得项明确记录 | 主文与全部被引用附件已归档并解析 |
| PDB 原始序列与全坐标 | 接受锚点两层配对审计 | 两层已齐；非逐变体结构 |
| 完整研究底层数据 | 公开汇编或处理包不等于全部底层实验 | 未宣称获得 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-09；影响标签解释）：`affinity_type` 混合 KD、IC50、自由能、布尔与 fuzzy 等来源端点；当前包的 `Kd (M)` 中有 102 个字面 `I.C.`，来源文件未给出可核验的统一数值定义。已原样保留 endpoint、来源和特殊值，不把它换算为零、阴性或具体检测限；取得相应上游来源定义或作者说明，核实这 102 条的含义后关闭。
- `Q02`（最近更新：2026-10-09；影响逐抗体结构使用）：`metadata.target_pdb` 给出 2,227 个不同的 entry 级目标引用，但并不保证每行抗体与该 PDB 中的实验复合物或具体链严格对应。已取得全部 2,227 对原生 FASTA/mmCIF，并仅作为外部结构锚点；需要逐行构建体或链角色时，按拟用子集回查原始研究与链证据，形成可核验映射后关闭相应子集。
