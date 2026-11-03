# SRC_R19_DIPS_PLUS 数据说明

## 数据集身份

- `source_id`：`SRC_R19_DIPS_PLUS`
- `source_version`：`1.1.0`
- 原作者或发布机构：Alex Morehead、Chen Chen、Ada Sedova、Jianlin Cheng

### 来源方背景

[正式论文作者单位](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10400622/fullTextXML)包括美国密苏里大学电气工程与计算机科学系及 Oak Ridge National Laboratory。作者团队发布的是用于蛋白界面预测的结构对与计算特征；PDB 条目、DB5 案例和外部特征工具各有自身来源，不能把它们当作同一批新测量。

## 实验设计和数据口径

DIPS-Plus 是一般蛋白复合物的界面/接触结构数据及计算特征，研究报告最终 42,112 个结构对，不含统一实验 KD。raw、interim complexes、pruned pairs、external features 和 DB5 是不同交付阶段，不把它们的成员数相加当作独立样本。外部特征分为八个连续 part，单个 part 不是可独立解压的 gzip 包。interim complex catalog 的候选空间明显大于最终筛选集；用其全部 accession 会造成错误覆盖。pickle/dill 可能包含可执行反序列化对象，本次只做 opcode 和 archive 成员检查，不运行上游对象。

主文流程先将 PDB 结构转为链对表示，使用 30% sequence-identity 过滤防止分区泄漏，再添加 PSAIA、HHsuite、DSSP 等特征，进行分区和缺失特征填补。42,112 是最终结构对口径，不是 KD 测量；源文件中的插补、预测和接触标签不构成新的亲和力实验。

## 论文原文

- 标题：DIPS-Plus: The enhanced database of interacting protein structures for interface prediction
- 作者：Alex Morehead；Chen Chen；Ada Sedova；Jianlin Cheng
- 载体与版本：Scientific Data
- 发布日期：2023-08-03
- DOI：`10.1038/s41597-023-02409-3`
- PMID / PMCID：37537186 / PMC10400622
- 本地文件：`articles/DIPS_PLUS_2023-08-03_ScientificData-published.xml`
- 文件大小：125.21 KiB（128,210 bytes）
- SHA-256：7fefece9646f8ff9291a783c0f19397de78de04dbecf813d3f53ba9552ffdabe
- 文本许可：正式论文 XML 标明 CC BY 4.0；第三方材料按其单独声明判断
- 补充材料：经完整主文 XML 检查，无 supplementary-material/media 文件引用；不把外部数据仓库当作论文附件

## 仓库内容

来源身份：

- `kind`：`zenodo`
- `record`：`5134732`
- `publication_date`：`2021-06-07`

版本日期来自数据源 commit 或官方更新时间；正式版本名保留官方名称。以下树为已验收的上游 payload，不列项目 README、论文及 PDB 外部补充。

```text
1.1.0/
└── DIPS_PLUS/
    ├── interim_external_feats_dips.tar.gz.partad
    ├── final_raw_db5.tar.gz
    ├── interim_pairs_pruned_dips.tar.gz
    ├── interim_pairs_db5.tar.gz
    ├── final_raw_dips.tar.gz
    ├── interim_complexes_db5.tar.gz
    ├── interim_complexes_dips.tar.gz
    ├── interim_external_feats_db5.tar.gz
    ├── interim_external_feats_dips.tar.gz.partaa
    ├── interim_external_feats_dips.tar.gz.partab
    ├── interim_external_feats_dips.tar.gz.partac
    ├── interim_external_feats_dips.tar.gz.partae
    └── …（其余来源文件保留原路径）
```

## 数据结构

### 原始交付与记录

| 原始文件 / sheet | 非空记录数 | 字段数 | 精确重复行 |
| --- | --- | --- | --- |
| `final_raw_dips.tar.gz` 的最终 Pair 成员 | 42,112 | 8 个 Pair 字段；双方 atom table 各 24 列 | 未作跨成员值级去重 |
| `final_raw_db5.tar.gz` 的最终 Pair 成员 | 230 | 同上 | 未作跨成员值级去重 |

只统计实际已解析的文件，未把来源介绍规模当作本次落盘统计。

全部 15 个原交付文件完整取得、官方 hash/size 验收通过，共 41.55 GiB（44,610,464,744 bytes）。八个外部特征 gzip 分卷按原顺序流式连接，完整 gzip trailer/tar 路径与全部 526118 个成员（524399 普通文件）检查通过，解压后 112.86 GiB（121,178,300,916 bytes）。原始分卷不重写、不放额外解压副本。最终 DIPS raw 有 42112 个 Pair .dill 加 4 个列表/统计文件；实际全量列表 41449（排除 >1000 residues 的 663），train 33159、val 8290。DB5 raw 有 230 个 Pair .dill 加 5 个列表/统计文件，train 140、val 35、test 55，都是文件列表口径，不是三批新的实验测量。所有 42342 个最终序列化 Pair 的字面 header/opcode 与 atom table 字段已检查，未执行 dill/pickle，未把中间候选 catalog 当最终入选。

### 字段说明

interim `complexes.dill` 的序列化记录包含 name、bound_filenames、unbound_filenames 和 data 映射；原始字符串以 accession.pdbN 表示 PDB biological assembly 线索。最终 Pair/atom/residue/contact schema 已按下述固定 raw 成员核验；这些字段不含实验 KD。partaa–partah 已按原顺序与官方 MD5 验收，拼接后的 gzip/tar 也已完整检查。

最终 Pair namedtuple 字段为 complex、df0、df1、pos_idx、neg_idx、srcs、id、sequences；df0/df1 的实际 24 列为 pdb_name、model、chain、residue、resname、ss_value、rsa_value、rd_value、avg_cx、s_avg_cx、s_ch_avg_cx、s_ch_s_avg_cx、max_cx、min_cx、hsaac、cn_value、sequence_feats、amide_norm_vec、x、y、z、element、atom_name、aid。x/y/z 是 Å 坐标；ss 为 DSSP H/B/E/G/I/T/S/-，- 表示未知；数值 NaN 不是无接触。hsaac 42 维、HMM sequence_feats 27 维、normal vector 3 维；来源预处理/归一化/插补必须保留来源方法，不重新解释为实验 KD。主文 positive contact 按 bound state 双方 residue 非氢 atom 距离 ≤6 Å，pos_idx 是 DataFrame row ID 连接，不是序列位置或链标签；DIPS bound 和 DB5 unbound 是不同评估输入条件。引用的统计 CSV 为作者生成的汇总，此内容复核没有重建全部数值矩阵，不把作者统计当重新计算的测量。

### 数据示例

来自最终 `DIPS_PLUS/final_raw_dips.tar.gz` 的真实成员 `raw/cx/5cxc.pdb1_0.dill`（1655207 bytes）；字面序列化记录的 complex 为 `5cxc.pdb1`，Pair 字段为 `complex`、`df0`、`df1`、`pos_idx`、`neg_idx`、`srcs`、`id`、`sequences`。此例直接检查原记录 opcode/header，未执行反序列化、没有构造新数值记录；只说明一个最终结构对及其原始 schema，不代表一个 KD 测量。

## PDB 数据库

Final DIPS record names establish 11967 parent entry references. All 230 final DB5 case parents are connected to the original official benchmark5.tgz and its literal README alias declarations; 9QFW is the historical case alias for 1QFW, not the current entry 9QFW. 634 canonical DB5 supporting references include all original bound/unbound table refs and earlier current-table additions. All 230 bound author-chain sets uniquely match the original official table. Full native entries are supporting coordinates, not new affinity measurements. Original unbound construct/chain equality is not inferred from cleaned filenames or current table mappings.

当前接受锚点清单为 12601 个；最后一次审计有 0 个未完成两层配对。每个锚点取原样 RCSB FASTA 和完整 mmCIF，不嫁接 CDR、不生成逐变体重建序列。原始 header 保留不改写；现行接口提供 polymer entity/chain 注释，历史 SEQRES 提供 author chain、mol 和 length。只有全部接受锚点同时通过完整 FASTA 和坐标解析，且现行 FASTA 全 entity ID 集合或历史 SEQRES 全 author-chain 集合，以及每条完整 canonical 序列与所选完整 mmCIF 一致，才算完成。原始 mol:na 核酸记录同样全序列核对；不猜测伙伴角色。

PDB 文件审计摘要：25202 个文件，14.20 GiB（15,247,869,078 bytes）；inventory SHA-256：`78c83bfc7adb25f92ebab1a59664ea23d03ec25a68fbcf9fdec6aff5737d719c`。摘要按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接计算。缓存最初包含选择链/重写 header 的 FASTA，已清理本轮这类 staging 副本；现在只接受 RCSB 原始 header 和字面完整序列。

官方 RCSB 不可变历史快照按 S3 原始 size、单段或多段 ETag、完整 gzip CRC/trailer 验收。每个补入 entry 的全部字面记录必须与所选完整原始 entry 坐标逐链一致；不以替代条目补序列。快照身份：

- `20190101`：<https://pdbsnapshots.s3.amazonaws.com/20190101/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 25.61 MiB（26,857,360 bytes）；SHA-256 `055a10bd392391156a0a88bcc5cda5e1f3674e415977c417901dd2713bf2b827`。
- `20200722`：<https://pdbsnapshots.s3.amazonaws.com/20200722/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 30.30 MiB（31,768,833 bytes）；SHA-256 `9be6c03243187f2ecbdaa68f7262b1d69de85ce36ea5a4a729e137e3807e59b7`。
- `20210105`：<https://pdbsnapshots.s3.amazonaws.com/20210105/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 32.59 MiB（34,177,430 bytes）；SHA-256 `567ceb743a5ec6da30bc5c95a1462993c781adca7dfce737df889a249d5eaeaa`。
- `20230102`：<https://pdbsnapshots.s3.amazonaws.com/20230102/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 41.51 MiB（43,523,160 bytes）；SHA-256 `9c9b08fa5ad62e015d4331bd0124f35e04a31119a29ab388de381aa206f54120`。
- `20240101`：<https://pdbsnapshots.s3.amazonaws.com/20240101/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 46.62 MiB（48,889,608 bytes）；SHA-256 `91d0291d19dab4ab66f79ee4fad99c94ca190c27d87d3427182c5ed084d1c03a`。
- `20260101`：<https://pdbsnapshots.s3.amazonaws.com/20260101/pub/pdb/derived_data/pdb_seqres.txt.gz>，压缩后 58.83 MiB（61,683,307 bytes）；SHA-256 `e3babb9599a7892b40ae32144b38681a68525cff78389494fa24826768127a75`。

## 使用方式

由调用者先赋值 `dataset_root`（Path），再读取；不在这里清洗或转换标签。

```python
import tarfile
with tarfile.open(dataset_root / "DIPS_PLUS/final_raw_dips.tar.gz") as archive:
    names = archive.getnames()
```

## 采集过程记录

2026-09-18：读取项目规范和执行清单，解析一手 API/tree/Drive 对象 metadata，固定本轮版本与文件身份。下载到共享 source 下 `.staging/<version>.partial`；HTTP 大文件使用精确 byte range 和全文件上游 checksum，Drive 保留对象 ID、MIME 与字节数，失败部分可续传。2026-09-18 按用户要求调整本轮 HTTP 为直连优先、连接失败回退环境代理，15 分钟后重试直连；各线程复用连接且保留 TLS/CA 校验。重启任务保留所有文件断点。

独立 audit 重新计算 hash、完整解析已取得表格并检查 PDB 两层文件；归档只有完成逐成员/CRC 与路径安全检查后才通过。PMC 访问被拒绝、非 OA XML 不可得和间歇代理连接失败均保留缺口，未关闭 TLS 验证。PDB 缓存原始性检查发现错误后清理本轮衍生 header 文件并重做。

README 草稿每次写入后立即同步到 staging 同名文件，随后运行 skill 固定 Markdownlint 配置。发布脚本仅在逐文件、论文/PDB、README 同步与固定格式检查通过后原子发布；发布状态与 接入过程记录 同步。

2026-09-18：主文从 `DIPSPlus_PMC10400622.xml` 改名为 `DIPS_PLUS_2023-08-03_ScientificData-published.xml`，日期取该论文版本发布日期，改名前后大小和 SHA-256 一致。

2026-09-18 继续逐项补齐：取得原作者 benchmark5.tgz（5.0，37.07 MiB（38,867,186 bytes）），原README字面声明9QFW→1QFW、BAAD→3AAD、BOYV→1OYV、BP57/CP57→3P57。全部230最终DB5案例的四份原处理结构可得；bound author-chain合集与原始Table_BM5.xlsx的230行逐例唯一匹配（原表脚注*单独解析），原bound与双方unbound引用632项，加保留的2项现行官方表支持参考，共634项，与11967个DIPS parent不重叠，共12601。未把现行9QFW当旧case，也不从处理文件名推断unbound原ID。8个已撤回原始ID均经官方holdings API核验并补齐原始full mmCIF及历史全链native SEQRES。校验器补入官方DNA mol:na格式，1FZP全部原始protein/DNA链与full canonical一致，不生成序列。R19采用经全ETag/CRC验证的20260101官方SEQRES快照减少逐条FASTA请求，仅全canonical匹配时原样复制，否则回退现行端点；全部12601份原生FASTA与12601份完整坐标已取得；2026-09-18T22:14:35Z的独立全量审计重新解析所有配对，missing与pdb_missing均为空。PDB inventory共25202文件、14.20 GiB（15,247,869,078 bytes）、SHA-256 78c83bfc7adb25f92ebab1a59664ea23d03ec25a68fbcf9fdec6aff5737d719c。全部15交付文件重新核验官方checksum/size及完整SHA-256；8项归档验收仅在所有原始输入完整字节及顺序与此前全CRC/trailer证明一致时复用，PDB验收不复用。

2026-10-09：按新版 README 合同移除“主要数据尚未解析”的旧阶段状态，与已完成的 42,342 个最终 Pair 字面 schema 审计一致；补充来源背景、动态待办和最终包读取路径。15 件 Zenodo 原件与 12,601 对 PDB 文件未改动。

## 参考文献

- <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10400622/fullTextXML>
- <https://doi.org/10.1038/s41597-023-02409-3>
- <https://zenodo.org/records/5134732>
- <https://www.rcsb.org/>
- <https://data.rcsb.org/rest/v1/holdings/removed/1A2K>
- <https://data.rcsb.org/rest/v1/holdings/removed/1BVS>
- <https://data.rcsb.org/rest/v1/holdings/removed/1ERK>
- <https://data.rcsb.org/rest/v1/holdings/removed/1FZP>
- <https://data.rcsb.org/rest/v1/holdings/removed/3CU7>
- <https://data.rcsb.org/rest/v1/holdings/removed/3RVW>
- <https://data.rcsb.org/rest/v1/holdings/removed/3WWZ>
- <https://data.rcsb.org/rest/v1/holdings/removed/4OJY>
- <https://zlab.umassmed.edu/benchmark/benchmark5.tgz>
- <https://zlab.wenglab.org/benchmark/Table_BM5.xlsx>
- <https://pdbsnapshots.s3.amazonaws.com/20190101/pub/pdb/derived_data/pdb_seqres.txt.gz>
- <https://pdbsnapshots.s3.amazonaws.com/20200722/pub/pdb/derived_data/pdb_seqres.txt.gz>
- <https://pdbsnapshots.s3.amazonaws.com/20210105/pub/pdb/derived_data/pdb_seqres.txt.gz>
- <https://pdbsnapshots.s3.amazonaws.com/20230102/pub/pdb/derived_data/pdb_seqres.txt.gz>
- <https://pdbsnapshots.s3.amazonaws.com/20240101/pub/pdb/derived_data/pdb_seqres.txt.gz>
- <https://pdbsnapshots.s3.amazonaws.com/20260101/pub/pdb/derived_data/pdb_seqres.txt.gz>

## 其他

### 完整性与验收

上游声明 15 个文件；最近审计通过 15 个，待取得/核验 0 个。

公开包独立验收、论文/补充材料对照及 PDB 配对审计通过；不宣称全部底层实验数据取得。没有独立 manifest/API 响应/审计 JSON 发布在 source version 中；临时产物只保存在共享 cache。

| 上游 payload | 大小 | SHA-256 |
| --- | --- | --- |
| `DIPS_PLUS/interim_external_feats_dips.tar.gz.partad` | 4.00 GiB（4,294,967,296 bytes） | `a149607509afd5b63d99aa94ac587c73a0ec5817f44376ddfa0e11168dcef82d` |
| `DIPS_PLUS/final_raw_db5.tar.gz` | 40.84 MiB（42,819,028 bytes） | `ac63b41d02e21216b16f24aa4651bfc26bad003b42cee68af26b139cb36d65e4` |
| `DIPS_PLUS/interim_pairs_pruned_dips.tar.gz` | 2.61 GiB（2,800,994,993 bytes） | `1ce8e157b147cec782d52d6b096939f7fcf66bad88640bb08a9669a9194d75ff` |
| `DIPS_PLUS/interim_pairs_db5.tar.gz` | 14.71 MiB（15,423,020 bytes） | `427e46228651ca65235520e2a4a688f46753cf9912cc9dd91d4bfb84debb72ec` |
| `DIPS_PLUS/final_raw_dips.tar.gz` | 7.21 GiB（7,738,488,420 bytes） | `2d87898f36fff69b73a848e18887f5ec0f0ce75350e02fae95f9447a044d6758` |
| `DIPS_PLUS/interim_complexes_db5.tar.gz` | 6.25 KiB（6,404 bytes） | `ced917d5b794c70b199878ac0f59180c9cda8cbcbad0c99c6948af7d2cad7b54` |
| `DIPS_PLUS/interim_complexes_dips.tar.gz` | 2.22 MiB（2,328,377 bytes） | `399d6b8947765cd2828437cccd9c21e5bc6e72b60564cac3bec058474d1305ab` |
| `DIPS_PLUS/interim_external_feats_db5.tar.gz` | 278.25 MiB（291,768,113 bytes） | `fcc10c37286a5077bcd8c96fdf5a4503af68f1c1a708238519615bd9b2d56908` |
| `DIPS_PLUS/interim_external_feats_dips.tar.gz.partaa` | 4.00 GiB（4,294,967,296 bytes） | `c8f791146b18919aae8b1e34d8f43839c5a3a8764230e546317f2250acad21f1` |
| `DIPS_PLUS/interim_external_feats_dips.tar.gz.partab` | 4.00 GiB（4,294,967,296 bytes） | `c41e1053b6382f1dcb2c4925ae965dfb8dd67201197ffe9003ca926d8fa42a82` |
| `DIPS_PLUS/interim_external_feats_dips.tar.gz.partac` | 4.00 GiB（4,294,967,296 bytes） | `30afa82c96e64673f93a291ed94ddf10417eb20bce4ac6e6b3495e72b41cce77` |
| `DIPS_PLUS/interim_external_feats_dips.tar.gz.partae` | 4.00 GiB（4,294,967,296 bytes） | `e47728ba0b3e5a93434c765a0b0ef5dca36cf4a5cf986d7437b04e82d6bbd533` |
| `DIPS_PLUS/interim_external_feats_dips.tar.gz.partaf` | 4.00 GiB（4,294,967,296 bytes） | `b1e04488fba441f9654170f707b3e33096127d69dbf1e03689e81eb3fae067e5` |
| `DIPS_PLUS/interim_external_feats_dips.tar.gz.partah` | 3.40 GiB（3,653,865,317 bytes） | `8b892ca09ff6f2be3f9877921cc1b12fb938dea4d7583536029884c687a6cb49` |
| `DIPS_PLUS/interim_external_feats_dips.tar.gz.partag` | 4.00 GiB（4,294,967,296 bytes） | `def17123e8f442060ac550d85d70c669062579c17a90afd463193038d3e220a2` |

### 许可和再分发边界

Zenodo 5134732 数据标为 CC BY 4.0；作者程序为 GPL-3.0，二者分开记录。PDB 和各外部特征工具仍需引用。

固定 Zenodo 1.1.0 的数据按其 metadata 的 CC BY 4.0 条件处理；代码 GPL-3.0 与数据许可分开。主文 CC BY 4.0 另独立保留。作者官方 DB5.5 supporting table 另明确 work CC BY 4.0，实际 HTML/表格比对证据留在 cache，不据此改写历史 DB5 case 原编号或猜测 alias/PDB 关系。 原始5.0 tar/table是映射一手证据，与目标Zenodo delivery分开缓存在cache；现行作者官网work CC BY4.0声明不被伪装成tar内独立LICENSE。

### 公开范围对照

| 目标组成 | 当前证据 | 状态 |
| --- | --- | --- |
| 固定上游 payload | tracked config + 独立文件/格式审计 | 目标公开文件验收通过 |
| 论文原文 | 一手 DOI 和取得文件 hash；不可得项明确记录 | 主文与全部被引用附件已归档并解析 |
| PDB 原始序列与全坐标 | 接受锚点两层配对审计 | 两层已齐；非逐变体结构 |
| 完整研究底层数据 | 公开汇编或处理包不等于全部底层实验 | 未宣称获得 |

## 待解决问题与处理进展

截至 `2026-10-09`，本次 1.1.0 交付文件、最终 Pair 字面 schema、DB5 原始案例映射、论文附件范围及 12,601 对 PDB 参考的核验范围内暂无待解决问题。未执行不受信任的 dill/pickle 反序列化，也未重算所有外部特征矩阵；这两项不属于本次 raw source 接入验收。
