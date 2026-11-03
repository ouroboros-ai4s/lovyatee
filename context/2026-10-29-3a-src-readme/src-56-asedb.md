# SRC_R56_ASEDB 数据说明

## 数据集身份

- `source_id`：`SRC_R56_ASEDB`
- `source_version`：`snapshot-2010-07-21`
- 原作者或发布机构：Kurt S. Thorn、Andrew A. Bogan；原 ASEdb 作者与维护者

## 实验设计和数据口径

ASEdb 是对已发表 alanine-scanning 实验的关系数据库汇编，包含蛋白–蛋白、蛋白–核酸及蛋白–小分子体系，不是单一抗体实验。作者从同行评审文献收集单残基改为 alanine 后的结合自由能变化；原论文说明排除了被原实验作者判为严重改变蛋白构象的突变。原文、历史 FAQ、Search 页面和实际 SQL 均已读取；此两页正式论文没有独立 Methods 标题或另列 Supplementary，正文描述数据库构建与筛选，Table 1 列原始系统及单体/复合物结构。

当前完整历史 SQL 有 mutation 3,043 行、system 101 行、reference 74 行。system 类型 P/D/S 分别为 91/4/6 个系统；相关 mutation 分别为 2,915/78/50 行。2001 论文声称 2,919 mutants，不等于较后历史 dump 的 3,043 行；不同方向的突变蛋白、配体条件和多个文献可以共享同一复合物。单条 mutation 不是新独立蛋白，sysID 也不是全球唯一生物对象。

ddG 是文献实验的结合自由能变化（kcal/mol；突变相对原体系，正值为结合减弱），不是模型打分。实际数值范围 -2.3 至 10.0；97 行 min_ddG=`>` 为下界删失，不能按精确值训练。1669 行 ddG 为数值 0，schema 又将该字段设为 NOT NULL default 0.000；原库没有额外测量/失败状态列，因此不能仅由零推断未测，也不能断言全部零都是精确测量。应保留 sysID、refID、原始值和边界，后续回查文献。

ASA 是作者使用 NACCESS 计算的侧链溶剂可及面积（Å²），非亲和力实验；monomer/complex/delta 的缺失分别有 435/2427/2429 行。SQL NULL、空字符串、数字 0、枚举 > 与默认日期各有不同含义，不统一填零。kon/koff 和 ratio 是混合体系的动力学信息；该 dump 未提供每条实验的温度、buffer、重复/误差、仪器原曲线或完整突变体序列，不扩展为统一条件 KD 数据。

mutation 有 33 个完全相同的重复行，名义连接键 (sysID,AA,Chain,position,pos_suff,refID) 有 38 个重复。system/refID 各自主键唯一；没有 sysID 孤儿，但一条 mutation 的 refID=0 无对应 reference。保留上游问题，不在 raw 去重或补引用。训练切分需考虑共享 sysID/PDB、野生型、突变位点和原文献，并核对与 SKEMPI/BID 等汇编的重叠。

## 论文原文

- 标题：ASEdb: a database of alanine mutations and their effects on the free energy of binding in protein interactions
- 作者：Kurt S. Thorn、Andrew A. Bogan
- 载体与版本：Bioinformatics 17(3), 284–285；原作者站点 reprint 的公共历史存档，2 页 PDF
- 发布日期：2001-03-01（正式出版）；该原站 reprint 捕获于 2010-07-21
- DOI：10.1093/bioinformatics/17.3.284
- PMID / PMCID：PMID 11294795；无已确认 PMCID
- 本地文件：`articles/ASEdb_2001-03-01_Bioinformatics.pdf`
- 文件大小：68689 bytes
- SHA-256：`e3a5e48de62cfc51f7a1f8b5ed3c3816ecdcbf406ba01012f0afebb41d510dd1`
- 文本许可：PDF 明示 © Oxford University Press 2001；公开原站 reprint 不代表 CC 授权
- 补充材料：两页正文和 Table 1；原文没有另列独立补充附件。数据库 dump 属上游 payload。

## 仓库内容

一手原站历史 FAQ 的 [全库下载链接](https://web.archive.org/web/20080604001256id_/http://nic.ucsf.edu:80/asedb/faq.php)明确指向 `downloads/hotspot.mysql`。本次取得该原站文件的 [2010-07-21 22:18:25 UTC 存档](https://web.archive.org/web/20100721221825id_/http://nic.ucsf.edu/asedb/downloads/hotspot.mysql)，283,414 bytes、固定本地 SHA-256；CDX 列出原 URL、capture timestamp、200 状态和 text/plain。使用 archive 的原内容入口保存文件，不把存档界面或 CDX/API 输出发布为 raw。

`snapshot-2010-07-21` 指这个已核验的历史文件捕获日期，不是新恢复的数据库 release 日期或本次下载日期。SQL 未给 dump 完成日期；mutation.add_date 范围 2000-07-01 至 2002-01-04，既不能拿最大记录日期替代整个文件版本，也不能推断 2010 年新实验。此包包含完整三个表的原 dump，未声称恢复原站服务、后续版本或所有仪器数据。

```text
snapshot-2010-07-21/
└── ASEdb/
    └── ASEdb_2010-07-21_Wayback-MySQLDump.mysql
```

表格、归档与其记录关系见数据结构；上游说明、许可或嵌入资源保留原始内容。

## 数据结构

### 关系表与历史边界

文件为 MySQL dump 10.9，声明原 server 4.1.11，三个 MyISAM 表声明 DEFAULT CHARSET=latin1，SET NAMES utf8；实际文件仅含 ASCII 字节，两者不构成当前解码冲突。全部 CREATE TABLE 与 INSERT tuple 已静态解析，逐 tuple 宽度严格等于表 schema；没有执行 SQL，也没有改写或重新导出 raw。

mutation.sysID 连接 system.sysID；mutation.refID 连接 reference.refID。system.PDB 与 dimer_struct 定义参考结构及原库单体/复合物标记；不是每个 mutation 都有独立结构。Chain 空字符串或 NULL 不补成 A，position 与 pos_suff 要联合保留，不能用 cleaned 编号代替。原 MySQL DROP/LOCK/SET 语句是上游内容，不应在已有数据库中直接执行。

| 原表 | 行数 | 字段数 |
| --- | --- | --- |
| mutation | 3043 | 17 |
| reference | 74 | 10 |
| system | 101 | 9 |

### 字段说明

| 原表.字段 | 原 SQL 类型与约束 | 含义 / 单位 / 特殊表示 | NULL 数 | 空字符串数 |
| --- | --- | --- | --- | --- |
| mutation.sysID | smallint(5) unsigned NOT NULL default '0' | 原库系统连接键；整数，跨来源不全局唯一 | 0 | 0 |
| mutation.AA | char(1) NOT NULL default '' | 被替换残基的原始单字母编码；不构成完整变体序列 | 0 | 0 |
| mutation.Chain | char(1) default NULL | 原作者链字符串；NULL/空不指定链，需回查体系 | 218 | 2689 |
| mutation.position | smallint(5) unsigned NOT NULL default '0' | 原编号整数，与 pos_suff 联合解释 | 0 | 0 |
| mutation.pos_suff | char(1) default NULL | 原编号插入后缀字符串；NULL 与空保留 | 222 | 2811 |
| mutation.ddG | float(6,3) NOT NULL default '0.000' | 实验结合自由能变化，kcal/mol；结合减弱为正，与 min_ddG 联读 | 0 | 0 |
| mutation.min_ddG | enum('>') default NULL | 边界枚举 >；NULL、空、> 分别保留，> 是下界 | 198 | 2748 |
| mutation.old_refID | char(2) default NULL | 旧文献连接键字符串，不替代 refID | 224 | 0 |
| mutation.monomer_ASA | float(6,2) default NULL | NACCESS 计算侧链单体 ASA，Å²；NULL 不是零 | 435 | 0 |
| mutation.complex_ASA | float(6,2) default NULL | NACCESS 计算复合物 ASA，Å²；NULL 不是零 | 2427 | 0 |
| mutation.delta_asa | float(6,2) default NULL | 原作者计算 ASA 变化，Å²；保留原数值，不重算 | 2429 | 0 |
| mutation.refID | smallint(5) unsigned NOT NULL default '0' | reference 主键或 mutation 文献连接键；0 孤儿不补引用 | 0 | 0 |
| mutation.add_date | date NOT NULL default '0000-00-00' | 数据库记录添加日期，YYYY-MM-DD；schema 默认 0000-00-00，不是实验日期 | 0 | 0 |
| mutation.kon_ratio | float default NULL | 原动力学比值字段，无量纲；原说明未明示分子/分母，不转为 KD | 2769 | 0 |
| mutation.koff_ratio | float default NULL | 原动力学比值字段，无量纲；原说明未明示分子/分母，不转为 KD | 2767 | 0 |
| mutation.min_kon_ratio | enum('>') default NULL | 比值下界枚举 >；本 dump 全 NULL | 3043 | 0 |
| mutation.min_koff_ratio | enum('>') default NULL | 比值下界枚举 >；不可与精确比值混用 | 3040 | 0 |
| reference.authors | text | 原引用作者文本 | 0 | 0 |
| reference.title | text | 原引用题名文本，可能含 HTML/数学标记或不完整题名 | 0 | 0 |
| reference.journal | varchar(40) default NULL | 原期刊名称字符串 | 0 | 0 |
| reference.volume | smallint(5) unsigned default NULL | 原卷号整数 | 0 | 0 |
| reference.start_page | smallint(5) unsigned default NULL | 原起始页整数 | 0 | 0 |
| reference.end_page | smallint(5) unsigned default NULL | 原终止页整数 | 0 | 0 |
| reference.year | year(4) default NULL | 原文献年份；不是测量或获取日期 | 0 | 0 |
| reference.URL | varchar(80) default NULL | 原外链字符串，varchar(80) 可能截断；不假定每条仍可访问 | 54 | 2 |
| reference.old_ref | char(2) default NULL | 旧文献 ID 字符串，不替代 refID | 15 | 0 |
| reference.refID | smallint(5) unsigned NOT NULL auto_increment | reference 主键或 mutation 文献连接键；0 孤儿不补引用 | 0 | 0 |
| system.sysID | smallint(5) unsigned NOT NULL auto_increment | 原库系统连接键；整数，跨来源不全局唯一 | 0 | 0 |
| system.mutated_protein | char(40) NOT NULL default '' | 原始被突变蛋白名称字符串 | 0 | 0 |
| system.partner_protein | char(40) NOT NULL default '' | 原始结合方名称/条件字符串 | 0 | 0 |
| system.type | enum('P','D','S') NOT NULL default 'P' | P=蛋白，D=核酸，S=小分子；不是抗体标签 | 0 | 0 |
| system.PDB | char(4) default NULL | 参考编号字符串；NULL/空为未给 accession | 19 | 6 |
| system.dimer_struct | enum('T','F') default NULL | 原库枚举 T/F，复合物/单体参考；不等于当前完整条目只有两个/一个实体 | 19 | 0 |
| system.dG | float(6,2) default NULL | 原体系自由能汇总，kcal/mol；不是逐突变 ddG | 14 | 0 |
| system.kon | float default NULL | 原动力学缔合字段；schema/当前原说明未给单位，需查原引用，不当 KD | 77 | 0 |
| system.koff | float default NULL | 原动力学解离字段；schema/当前原说明未给单位，需查原引用，不当 KD | 77 | 0 |

### 数据示例

mutation 实际第一条的原值摘录：

| 字段 | 原值 |
| --- | --- |
| sysID | `42` |
| AA | `F` |
| Chain | `H` |
| position | `100` |
| pos_suff | `` |
| ddG | `1.200` |
| min_ddG | `` |
| old_refID | `E` |
| monomer_ASA | `43.69` |
| complex_ASA | NULL |
| delta_asa | NULL |
| refID | `29` |
| add_date | `2000-07-01` |
| kon_ratio | `0.73` |
| koff_ratio | `5.3` |
| min_kon_ratio | NULL |
| min_koff_ratio | NULL |

sysID=42 的 system 是 Ab hu4D5-5 / p185HER2，PDB=1fvc、dimer_struct=F；该锚点是单体参考，不能标成这条记录的 HER2 结合复合物。refID=29 指向原 experimental reference。这里是原残基 F、链 H、position=100 的 alanine-scan 记录，不通过 RCSB FASTA 擅自生成变体序列。

## PDB 数据库

全部锚点直接来自原 system.PDB：76 个系统给出有效编号，32 个唯一 PDB；19 个系统为 NULL，6 个为空字符串。这些没有 accession 的系统不臆配结构。32 份完整 RCSB entity FASTA/mmCIF 均核验，原子/全部模型与伴侣完整保留；单体参考不会补成未知 partner 的复合物。

通过 mutation.sysID → system.PDB 建立参考级连接，原 dimer_struct=T/F 和原 Chain 字符串保持不变。大量 Chain 为空，部分 PDB 是单体；本阶段不声称逐突变残基、实验表达构建体或完整 mutant 序列已映射。作者链/entity 角色以下列完整原生元数据核对，不重命名伴侣或嫁接 alanine 后的新序列。2001 Table 1 的 CD4 原始参考 3CD4 与当前历史 SQL 的 1GC1 不同，以实际 dump 为本版本锚点，保留版本差异。

原 Chain 的 H/L 不总是当前 PDB 作者链名。sysID=42 的 1FVC：light entity 1 对应 A/C，heavy entity 2 对应 B/D，保留两套相同 entity 的链，不任意挑一套作新样本；sysID=44 的 1VFB：light A、heavy B、lysozyme C。1DVF 的原生描述将 D1.3 标为 entity 1/2（A/B），E5.2 标为 entity 3/4（C/D），可核实 sysID=55 与 7 的双方角色，但本次不臆断未明示的 H/L 与各实体一一关系；3HFM 的 sysID=43 原 H 与 native H 一致，L 为 light、Y 为 lysozyme。无 accession 的记录继续保留其原 H/L 字符串。角色连接来自完整原生 metadata，未改写 raw Chain 或假称全部原链字面相等。

获取/核验日期 2026-09-18。每个编号使用 RCSB `https://www.rcsb.org/fasta/entry/<PDB_ID>/download` 与 `https://files.rcsb.org/download/<PDB_ID>.cif`。校验 FASTA entity ID 集合及全序列与 mmCIF canonical entity 全序列严格相等，并核对 entry.id、非空原子坐标和 author-chain。共 32 个完整对，64 个文件，13,971,749 bytes。按相对路径排序拼接 `relative_path<TAB>bytes<TAB>sha256<LF>` 后 inventory SHA-256 为 `73bc9f967c700f5c6972e50e6d8c78ece335b309e20da4bd61de0ed49aac45b0`。

| PDB | FASTA bytes | FASTA SHA-256 | mmCIF bytes | mmCIF SHA-256 |
| --- | --- | --- | --- | --- |
| 1A4Y | 715 | `7db9ba1303d5c7b21a0b61bf5d24e234dc6b08f6ab630764a5b5a3a434b436bb` | 926830 | `a3a06dd7d8a9af55bdfdbdd000bab79b3eca743d3be7d37666719e59118152c9` |
| 1AHW | 860 | `b5796995439df253ddfd29e0096535477bb5c8940e9006afc48a92ae4539c3fc` | 1000193 | `a4251f240d2d2bc17054f42ef5749d9b30d52b683b3a27886df8a819b1d0aafc` |
| 1BDT | 441 | `5e4297bf072c10cefd5942abc1003693917edfe53a8ec24de1ff87df5537acef` | 301755 | `cf09b4ee4547a8b7909d40a307d2cd5b0edadff9363ae6ea15a49b4abf057d60` |
| 1BRS | 331 | `7357ab4884199f6f789aa246ca13b4d1f34f8375c4e63678b1fdb693dca82456` | 553617 | `1c98dcc3eac7ccb88657e3ab0f745121d7ddbd2fe11357c65dbaffdd5704f153` |
| 1BXI | 359 | `6d72999e5e1493ff59b5e6e0934475608c92acfe0a0a537dcc747a8b49126311` | 238394 | `36bc291bf3342306f4fdbae69415d9c4cdaeb8fb6471ec3e7c37870979338b79` |
| 1CBW | 552 | `266bf97d75238ceee57a3fceb1a684a1df5d8297b35b16d51843e77da5247c14` | 504084 | `8f6ca07d70ac4bfba3e147e22e9681280c9a22861f866819d94e70e74244350c` |
| 1CDC | 150 | `d2cdb528ed7346d48faf02666a3bfdd41bf82ed569551fc36ee7c996c9c7dc4b` | 200236 | `8294165e985b4c871d051e923e2558e4dded315fc387da80b02167b96e1398ad` |
| 1DAN | 915 | `72a201dd716d75579c24c9ea6312a220c8fb551c645f0f90145552ffae506385` | 615551 | `f9bac400ed66d9d78d85c1d847495f6a01c0370fef9bf815efa9b10767a2b4b4` |
| 1DFJ | 705 | `678246957ce8dac2ee12b40c0d45f2d190c5efcae47a09de12cf3a836e67eb88` | 482710 | `705e545e9f65204d544b0eb7bb3da90adee907a91f212b23a6d3314cb023a94b` |
| 1DVF | 636 | `d26e4163338aa6ab0adfca3c93d66994e7312bd0b0aff9026153489b51867bb9` | 428652 | `f36b57cb96045e3a31a361f4a138580914b4dfa766139b4039497dc087523509` |
| 1FC2 | 446 | `88151550f2b0c7fdf522113549d4f4d0093b2f327e9ce3e73cd2ade210299d96` | 285388 | `39f6c05d363d811dc799d0da325427d3aeeab90d4627f14bedb2f3a16eeab783` |
| 1FVC | 375 | `b3a0fcf7da0813e5d2ca16518c36fb78bc57f40bcf0e1d60458b0f363e035e4c` | 406518 | `1649cdc7f94d39b40f3f5987d78b21f1e10f79c10bf8ee1deba4a32937879d0f` |
| 1GC1 | 1200 | `42d28786a3d830ddf5f6cbdcfb2e1e030daea17beecbfb4a36722016adf02a75` | 865585 | `876ea09a257ed4c90560cee9d61623f7578e40596fd9d74b89dc5b2c933a44e2` |
| 1IL6 | 236 | `02e1ae336b1a7a41da6b70f2bc44e4662883964071cc9b27da7ec8324c12aa67` | 285898 | `e099e7abd3d7509a99566ba0c62a1697d31c32541b5fe07ef47ed5f7e0495997` |
| 1JCK | 630 | `ad89c36cfce669bd46e3d0d202e63cd0a2792fed47cfb8bc273d1380bd48e88e` | 773919 | `ab9fc195ae52d4981eea1de943e62f137775781041cb2e9612f107bccd93fed6` |
| 1MNM | 620 | `6bb5d1bada45e499e6a895cae97b6032705b9b891d081c691478c0030161f9a6` | 414475 | `0af5adff24c0c70904b3929eb53372651e8a7f7cd504c9e7f4c7b23f0a55f992` |
| 1NT3 | 181 | `e4e50fed174ffa3d9f3d4bdb8c1ae51f9c2b0291150af524aaadd298a9e66e64` | 140225 | `42bb20f954069e6048c34482ba8c23efc701bde6fcadebc4934c4d07a47da95f` |
| 1PNE | 184 | `4be3f4a35e9b63e40160b80a850913312b7315493d1eaa6e2226561212910a3b` | 166743 | `b08a0dafcb9d3f7fdc49ec89ca2ef42f449de5452dc099934f5dbe40f0a8c2f3` |
| 1RCB | 180 | `45060a8e663d286ada61cad7a8803ce78006f3449e6ef82c341f6c0787145d17` | 154658 | `2c08b77e45d783c616913720af7616e7764e5bb2507418ada23a1b94ee68090f` |
| 1RHG | 256 | `477a8e63f74580c24bdf42f04da57d39bb43ca6d9a2f5dbb4db7132bb953a436` | 444180 | `af0ca882b3634e38684d68d1e9881173766e9dd2b9953a72850ae1f0f65d453b` |
| 1ULO | 210 | `4d6b4e401adbfe002582c15256db56fea00b72206b005555169b0f3818d73024` | 238074 | `7141947348fe750758cf4c56149122ed25d6ca51fae9b72e6542340dac905a28` |
| 1VDE | 515 | `1fd383815a2ba5417b28ff6afd6595d836e06d45c3264a02e505deba947b8cc5` | 741138 | `24716d8822a12e092eaa37a4e67b27f096f69c7cce4601f26faae6cea005aa28` |
| 1VFB | 555 | `71c760e6d98a8a3003cd00400a155929afd9335e8668858472cdc6ee9b29a902` | 385884 | `d599fbb9391deb66c3b65d62944c6eae87a6b74cc0661d2ac9c2ced1df243a45` |
| 1WAP | 217 | `9d07c1286ae645aa25bbd7370f16067f8a40c2b15184d2bfc06a51076cad2612` | 1456412 | `a559d61572e06a2c00a9d550a570ac2e460c7799f08f250d1a3668ea745ccb77` |
| 2GF1 | 136 | `62e4ebbcb6285660be046d3f8ae6e820becf72f1d03c28ec2cec6c6e89b44783` | 98215 | `5d8997751e00d60cbf36064e1b49bde208e34103830169afe65d5a51e35031a5` |
| 2PTC | 392 | `1acfdc425a82a8af400d2cfe006572b76b8624ce01837c3c2aa9bdb831d2e1c6` | 284236 | `4b663a459fbbcb1052892c1ac2a1278ad8695f446e757133cbda0b780497e2df` |
| 3HFM | 783 | `c5b14a1d19d4167002764ba08ed0044c3ec10e02089cb9d4747182ae41348b97` | 462353 | `ff8360676ce94ed0e8bacf6c9d0c9bd460aa709f599e73f437a7082b01693c08` |
| 3HHR | 532 | `71fc450b086f4fb3822bda9cb9738b2591fa109da74aca93acb7d57f72f8c2d7` | 488128 | `088162b91d41731cde5c03776f8ae55015b55d636658e31966fe62b71e650cdc` |
| 3IL8 | 123 | `b0e71a1027cdcf708abf7922d121382fd2abe92b85e6c26c6587bf8c36a3fa52` | 119859 | `e68a70f459f63a64653808bf1b7c8ec1772fd7f8b5e533b28d9858edb68713a0` |
| 3INK | 204 | `1ff084af57326eda119d3478656159ce557e7ee3a5feb36d8a443aa555d3d96f` | 231972 | `487370ab1e3424e0c246e46ba0c3bd53f77e0060f489dbc62979f09771bdf626` |
| 4FGF | 214 | `024125226c9c8a7000c1834bded44976e7ca0829497b0eff2e424b4a85a6194b` | 158279 | `6f351d58dbf99fef876e6e2d6f663481510079461c7b0dab2aaa4204b5b4ba85` |
| 5EBX | 122 | `4aaf5dfa3057d79991203a9ab7061469f4d70cacc20aac4f1cc3ebf2a75951e0` | 103613 | `d168d7cfb1dcfbef409f5cdedc9870c85ede514d0c738da4cbeae3a3cc2ffc10` |

原生 polymer entity 角色（entity ID、作者链、字面描述）：

| PDB | entity | author chains | 原生实体描述 |
| --- | --- | --- | --- |
| 1A4Y | 1 | A,D | RIBONUCLEASE INHIBITOR |
| 1A4Y | 2 | B,E | ANGIOGENIN |
| 1AHW | 1 | A,D | IMMUNOGLOBULIN FAB 5G9 (LIGHT CHAIN) |
| 1AHW | 2 | B,E | IMMUNOGLOBULIN FAB 5G9 (HEAVY CHAIN) |
| 1AHW | 3 | C,F | TISSUE FACTOR |
| 1BDT | 1 | E | DNA (5'-D(*TP*AP*TP*AP*GP*TP*AP*GP*AP*GP*TP*GP*CP*TP*TP*CP*TP*AP*TP*CP*AP*T)-3') |
| 1BDT | 2 | F | DNA (5'-D(*AP*AP*TP*GP*AP*TP*AP*GP*AP*AP*GP*CP*AP*CP*TP*CP*TP*AP*CP*TP*AP*T)-3') |
| 1BDT | 3 | A,B,C,D | PROTEIN (GENE-REGULATING PROTEIN ARC) |
| 1BRS | 1 | A,B,C | BARNASE |
| 1BRS | 2 | D,E,F | BARSTAR |
| 1BXI | 1 | A | PROTEIN (COLICIN E9 IMMUNITY PROTEIN) |
| 1BXI | 2 | B | PROTEIN (COLICIN E9) |
| 1CBW | 1 | A,F | BOVINE CHYMOTRYPSIN |
| 1CBW | 2 | B,G | BOVINE CHYMOTRYPSIN |
| 1CBW | 3 | C,H | BOVINE CHYMOTRYPSIN |
| 1CBW | 4 | D,I | BPTI |
| 1CDC | 1 | B,A | CD2 |
| 1DAN | 1 | L | BLOOD COAGULATION FACTOR VIIA light chain |
| 1DAN | 2 | H | BLOOD COAGULATION FACTOR VIIA heavy chain |
| 1DAN | 3 | T | SOLUBLE TISSUE FACTOR |
| 1DAN | 4 | U | SOLUBLE TISSUE FACTOR |
| 1DFJ | 1 | E | RIBONUCLEASE A |
| 1DFJ | 2 | I | RIBONUCLEASE INHIBITOR |
| 1DVF | 1 | A | FV D1.3 |
| 1DVF | 2 | B | FV D1.3 |
| 1DVF | 3 | C | FV E5.2 |
| 1DVF | 4 | D | FV E5.2 |
| 1FC2 | 1 | C | FRAGMENT B OF PROTEIN A COMPLEX |
| 1FC2 | 2 | D | IMMUNOGLOBULIN FC |
| 1FVC | 1 | A,C | IGG1-KAPPA 4D5 FV (LIGHT CHAIN) |
| 1FVC | 2 | B,D | IGG1-KAPPA 4D5 FV (HEAVY CHAIN) |
| 1GC1 | 1 | G | ENVELOPE PROTEIN GP120 |
| 1GC1 | 2 | C | CD4 |
| 1GC1 | 3 | L | ANTIBODY 17B |
| 1GC1 | 4 | H | ANTIBODY 17B |
| 1IL6 | 1 | A | INTERLEUKIN-6 |
| 1JCK | 1 | A,C | 14.3.D T CELL ANTIGEN RECEPTOR |
| 1JCK | 2 | B,D | STAPHYLOCOCCAL ENTEROTOXIN C3 |
| 1MNM | 1 | E | DNA (STE6 OPERATOR DNA) |
| 1MNM | 2 | F | DNA (STE6 OPERATOR DNA) |
| 1MNM | 3 | A,B | PROTEIN (MCM1 TRANSCRIPTIONAL REGULATOR) |
| 1MNM | 4 | C,D | PROTEIN (MAT ALPHA-2 TRANSCRIPTIONAL REPRESSOR) |
| 1NT3 | 1 | A | PROTEIN (NEUROTROPHIN-3) |
| 1PNE | 1 | A | PROFILIN |
| 1RCB | 1 | A | INTERLEUKIN-4 |
| 1RHG | 1 | A,B,C | GRANULOCYTE COLONY-STIMULATING FACTOR |
| 1ULO | 1 | A | ENDOGLUCANASE C |
| 1VDE | 1 | A,B | PI-SCEI |
| 1VFB | 1 | A | IGG1-KAPPA D1.3 FV (LIGHT CHAIN) |
| 1VFB | 2 | B | IGG1-KAPPA D1.3 FV (HEAVY CHAIN) |
| 1VFB | 3 | C | HEN EGG WHITE LYSOZYME |
| 1WAP | 1 | A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V | TRP RNA-BINDING ATTENUATION PROTEIN |
| 2GF1 | 1 | A | INSULIN-LIKE GROWTH FACTOR I |
| 2PTC | 1 | E | BETA-TRYPSIN |
| 2PTC | 2 | I | TRYPSIN INHIBITOR |
| 3HFM | 1 | L | HYHEL-10 IGG1 FAB (LIGHT CHAIN) |
| 3HFM | 2 | H | HYHEL-10 IGG1 FAB (HEAVY CHAIN) |
| 3HFM | 3 | Y | HEN EGG WHITE LYSOZYME |
| 3HHR | 1 | A | HUMAN GROWTH HORMONE |
| 3HHR | 2 | B,C | HUMAN GROWTH HORMONE RECEPTOR (hGHbp) |
| 3IL8 | 1 | A | INTERLEUKIN-8 |
| 3INK | 1 | C,D | INTERLEUKIN-2 |
| 4FGF | 1 | A | BASIC FIBROBLAST GROWTH FACTOR |
| 5EBX | 1 | A | ERABUTOXIN A |

## 使用方式

依赖见接入代码 requirements；以下仅从原始文件读取。

```python
from pathlib import Path
# dataset_root 由调用者赋值为该 source version 目录。
dump = Path(dataset_root) / "ASEdb/ASEdb_2010-07-21_Wayback-MySQLDump.mysql"
text = dump.read_text(encoding="ascii")
print(dump.stat().st_size, text.count("CREATE TABLE "))
```

## 采集过程记录

1. 2026-09-18：读取项目/开发者身份、执行清单与一手来源；由配置读取共享存储根，代码和文档只写本人 workspace。
2. 固定上游版本并在对应 `.staging/snapshot-2010-07-21` 下载，使用断点续传、HTTP 长度及可得的官方校验；遇到环境直连失败采用现有 HTTP 路由回退。
3. 直连旧 asedb.org 得到已换主的娱乐网站，旧机构页面 HTTP 403，最初仅由下游论文取得十个参考 PDB，并准确记为缓存子集。2026-09-18 继续搜索原站 Internet Archive CDX，找到 FAQ 指向的原 MySQL 全库导出及原站 reprint；原内容入口实际 GET 均 200。先保留 storage cache，核对原 URL/capture、标题/DOI、SQL 全表/tuple/schema 和 bytes/SHA-256，再创建此历史 snapshot staging，下载并核验全部 32 个真正原库 PDB 锚点。新包与此前十对下游参考缓存分开，未将下游汇编冒充原库。

   原 dump 中发现 33 个完全重复行、38 个重复名义键、一个 refID=0 孤儿与 97 个下界删失；全文日期/规模和存档时间不混用。原数据全部保留，修订版没有删除错误、填补零或重建变体。

   先按 H/L 字面核验时发现与 1DVF 等原生作者链名不等；进一步读取完整 mmCIF 的实体与作者链，改为明确的参考实体/蛋白家族角色连接，并保留原链不确定性。首轮发布 lint 因原引用题名含 `<i>` 标记产生两项 MD033，发布器返回非零且未暴露 final；将题名以字面 code 展示后重做格式检查，原 SQL/PDF 均未改变。
4. 解析全部实际表/归档，独立核对文件集合、完整格式、哈希与 PDB 两层，保留上游差异。
5. README 工作稿每次写入立即同步共享目录；发布器复核固定格式、同步 hash 和 pinned markdownlint 0 errors 后原子发布。已于 2026-09-18T21:38:51.318870+00:00 从 staging 原子发布，当前为 final；本次修订 README 在同一次写入中覆盖同步 final，并重新审计和 lint。

依据来源、可核验日期、载体和附件角色整理 opaque 名称，改名前后 bytes/SHA-256 相同；中间名保留实际修订历史。dump 日期取已核验的原站文件历史 capture，论文取正式出版日期。具体映射如下：

| 上游原名 | 中间名（如有） | 本地相对路径 | 核对 bytes | 核对 SHA-256 |
| --- | --- | --- | --- | --- |
| hotspot.mysql | 无 | ASEdb/ASEdb_2010-07-21_Wayback-MySQLDump.mysql | 283414 | `ff1d48fd8f97630b474a0847d79a659fa585dffbfe9dc324b85440408bf2dd35` |
| asedb.pdf | 无 | articles/ASEdb_2001-03-01_Bioinformatics.pdf | 68689 | `e3a5e48de62cfc51f7a1f8b5ed3c3816ecdcbf406ba01012f0afebb41d510dd1` |

2026-09-18 逐条复审后：补齐全部已取得 PDB 的条目和原始结构论文主引用，以及涉及的上游汇编/对照引用。恢复原始历史三表 dump，核对全部原始 SQL 字段、删失/重复/孤儿与单体/复合物参考角色。相应修改同步个人状态、事实台账和交接，未取得的材料继续标明 partial/blocked。

## 参考文献

- [原站完整 MySQL 导出历史文件](https://web.archive.org/web/20100721221825id_/http://nic.ucsf.edu/asedb/downloads/hotspot.mysql)
- [原站 FAQ：全库下载与 NACCESS](https://web.archive.org/web/20080604001256id_/http://nic.ucsf.edu:80/asedb/faq.php)
- [原站 Search：类型与单位](https://web.archive.org/web/20080604000604id_/http://nic.ucsf.edu:80/asedb/search.php)
- [正式论文 DOI](https://doi.org/10.1093/bioinformatics/17.3.284)
- [原作者站点论文 reprint](https://web.archive.org/web/20100721222102id_/http://nic.ucsf.edu/asedb/asedb.pdf)
- [初始汇编原论文：Bogan & Thorn (1998), Anatomy of hot spots in protein interfaces](https://doi.org/10.1006/jmbi.1998.1843)

### PDB 条目与原始结构论文

以下主引用直接读取归档 mmCIF 的 `_citation` 元数据，按同一主引用合并；每个 PDB 链接均指向该原始条目，不把输入结构论文算作本来源的新实验。

| 原始 PDB 条目 | 结构论文主引用（标题、期刊、年份） | DOI / PMID |
| --- | --- | --- |
| [1A4Y](https://www.rcsb.org/structure/1A4Y) | Molecular recognition of human angiogenin by placental ribonuclease inhibitor--an X-ray crystallographic study at 2.0 A resolution.；EMBO J.；1997 | [DOI 10.1093/emboj/16.17.5162](https://doi.org/10.1093/emboj/16.17.5162)；[PMID 9311977](https://pubmed.ncbi.nlm.nih.gov/9311977/) |
| [1AHW](https://www.rcsb.org/structure/1AHW) | The mechanism of an inhibitory antibody on TF-initiated blood coagulation revealed by the crystal structures of human tissue factor, Fab 5G9 and TF.5G9 complex.；J.Mol.Biol.；1998 | [DOI 10.1006/jmbi.1997.1512](https://doi.org/10.1006/jmbi.1997.1512)；[PMID 9480775](https://pubmed.ncbi.nlm.nih.gov/9480775/) |
| [1BDT](https://www.rcsb.org/structure/1BDT) | Origins of DNA-binding specificity: role of protein contacts with the DNA backbone.；Proc.Natl.Acad.Sci.USA；1999 | [DOI 10.1073/pnas.96.3.811](https://doi.org/10.1073/pnas.96.3.811)；[PMID 9927650](https://pubmed.ncbi.nlm.nih.gov/9927650/) |
| [1BRS](https://www.rcsb.org/structure/1BRS) | Protein-protein recognition: crystal structural analysis of a barnase-barstar complex at 2.0-A resolution.；Biochemistry；1994 | [DOI 10.1021/bi00196a004](https://doi.org/10.1021/bi00196a004)；[PMID 8043575](https://pubmed.ncbi.nlm.nih.gov/8043575/) |
| [1BXI](https://www.rcsb.org/structure/1BXI) | Crystal Structure of the E.Coli Colicin E9 DNase Domain With its Cognate Immunity Protein Im9；Thesis；1998 | [PMID -1](https://pubmed.ncbi.nlm.nih.gov/-1/) |
| [1CBW](https://www.rcsb.org/structure/1CBW) | Crystal structures of bovine chymotrypsin and trypsin complexed to the inhibitor domain of Alzheimer's amyloid beta-protein precursor (APPI) and basic pancreatic trypsin inhibitor (BPTI): engineering of inhibitors with altered specificities.；Protein Sci.；1997 | [PMID 9300481](https://pubmed.ncbi.nlm.nih.gov/9300481/) |
| [1CDC](https://www.rcsb.org/structure/1CDC) | One sequence, two folds: a metastable structure of CD2.；Proc.Natl.Acad.Sci.USA；1995 | [DOI 10.1073/pnas.92.16.7337](https://doi.org/10.1073/pnas.92.16.7337)；[PMID 7638192](https://pubmed.ncbi.nlm.nih.gov/7638192/) |
| [1DAN](https://www.rcsb.org/structure/1DAN) | The crystal structure of the complex of blood coagulation factor VIIa with soluble tissue factor.；Nature；1996 | [DOI 10.1038/380041a0](https://doi.org/10.1038/380041a0)；[PMID 8598903](https://pubmed.ncbi.nlm.nih.gov/8598903/) |
| [1DFJ](https://www.rcsb.org/structure/1DFJ) | A structural basis of the interactions between leucine-rich repeats and protein ligands.；Nature；1995 | [DOI 10.1038/374183a0](https://doi.org/10.1038/374183a0)；[PMID 7877692](https://pubmed.ncbi.nlm.nih.gov/7877692/) |
| [1DVF](https://www.rcsb.org/structure/1DVF) | Crystal structure of an Fv-Fv idiotope-anti-idiotope complex at 1.9 A resolution.；J.Mol.Biol.；1996 | [DOI 10.1006/jmbi.1996.0629](https://doi.org/10.1006/jmbi.1996.0629)；[PMID 8950273](https://pubmed.ncbi.nlm.nih.gov/8950273/) |
| [1FC2](https://www.rcsb.org/structure/1FC2) | Crystallographic refinement and atomic models of a human Fc fragment and its complex with fragment B of protein A from Staphylococcus aureus at 2.9- and 2.8-A resolution.；Biochemistry；1981 | [DOI 10.1021/bi00512a001](https://doi.org/10.1021/bi00512a001)；[PMID 7236608](https://pubmed.ncbi.nlm.nih.gov/7236608/) |
| [1FVC](https://www.rcsb.org/structure/1FVC) | X-ray structures of the antigen-binding domains from three variants of humanized anti-p185HER2 antibody 4D5 and comparison with molecular modeling.；J.Mol.Biol.；1993 | [DOI 10.1006/jmbi.1993.1099](https://doi.org/10.1006/jmbi.1993.1099)；[PMID 8095303](https://pubmed.ncbi.nlm.nih.gov/8095303/) |
| [1GC1](https://www.rcsb.org/structure/1GC1) | Structure of an HIV gp120 envelope glycoprotein in complex with the CD4 receptor and a neutralizing human antibody.；Nature；1998 | [DOI 10.1038/31405](https://doi.org/10.1038/31405)；[PMID 9641677](https://pubmed.ncbi.nlm.nih.gov/9641677/) |
| [1IL6](https://www.rcsb.org/structure/1IL6) | Solution structure of recombinant human interleukin-6.；J.Mol.Biol.；1997 | [DOI 10.1006/jmbi.1997.0933](https://doi.org/10.1006/jmbi.1997.0933)；[PMID 9159484](https://pubmed.ncbi.nlm.nih.gov/9159484/) |
| [1JCK](https://www.rcsb.org/structure/1JCK) | Crystal structure of a T-cell receptor beta-chain complexed with a superantigen.；Nature；1996 | [DOI 10.1038/384188a0](https://doi.org/10.1038/384188a0)；[PMID 8906797](https://pubmed.ncbi.nlm.nih.gov/8906797/) |
| [1MNM](https://www.rcsb.org/structure/1MNM) | Crystal structure of the yeast MATalpha2/MCM1/DNA ternary complex.；Nature；1998 | [DOI 10.1038/35563](https://doi.org/10.1038/35563)；[PMID 9490409](https://pubmed.ncbi.nlm.nih.gov/9490409/) |
| [1NT3](https://www.rcsb.org/structure/1NT3) | Crystal structure of neurotrophin-3 homodimer shows distinct regions are used to bind its receptors.；Biochemistry；1998 | [DOI 10.1021/bi981254o](https://doi.org/10.1021/bi981254o)；[PMID 9836577](https://pubmed.ncbi.nlm.nih.gov/9836577/) |
| [1PNE](https://www.rcsb.org/structure/1PNE) | Crystallization and structure determination of bovine profilin at 2.0 A resolution.；J.Mol.Biol.；1994 | [DOI 10.1006/jmbi.1994.1461](https://doi.org/10.1006/jmbi.1994.1461)；[PMID 8046751](https://pubmed.ncbi.nlm.nih.gov/8046751/) |
| [1RCB](https://www.rcsb.org/structure/1RCB) | Crystal structure of human recombinant interleukin-4 at 2.25 A resolution.；FEBS Lett.；1992 | [DOI 10.1016/0014-5793(92)80739-4](https://doi.org/10.1016/0014-5793(92)80739-4)；[PMID 1511746](https://pubmed.ncbi.nlm.nih.gov/1511746/) |
| [1RHG](https://www.rcsb.org/structure/1RHG) | The structure of granulocyte-colony-stimulating factor and its relationship to other growth factors.；Proc.Natl.Acad.Sci.USA；1993 | [DOI 10.1073/pnas.90.11.5167](https://doi.org/10.1073/pnas.90.11.5167)；[PMID 7685117](https://pubmed.ncbi.nlm.nih.gov/7685117/) |
| [1ULO](https://www.rcsb.org/structure/1ULO) | Structure of the N-terminal cellulose-binding domain of Cellulomonas fimi CenC determined by nuclear magnetic resonance spectroscopy.；Biochemistry；1996 | [DOI 10.1021/bi961612s](https://doi.org/10.1021/bi961612s)；[PMID 8916925](https://pubmed.ncbi.nlm.nih.gov/8916925/) |
| [1VDE](https://www.rcsb.org/structure/1VDE) | Crystal structure of PI-SceI, a homing endonuclease with protein splicing activity.；Cell(Cambridge,Mass.)；1997 | [DOI 10.1016/S0092-8674(00)80237-8](https://doi.org/10.1016/S0092-8674(00)80237-8)；[PMID 9160747](https://pubmed.ncbi.nlm.nih.gov/9160747/) |
| [1VFB](https://www.rcsb.org/structure/1VFB) | Bound water molecules and conformational stabilization help mediate an antigen-antibody association.；Proc.Natl.Acad.Sci.USA；1994 | [DOI 10.1073/pnas.91.3.1089](https://doi.org/10.1073/pnas.91.3.1089)；[PMID 8302837](https://pubmed.ncbi.nlm.nih.gov/8302837/) |
| [1WAP](https://www.rcsb.org/structure/1WAP) | The structure of trp RNA-binding attenuation protein.；Nature；1995 | [DOI 10.1038/374693a0](https://doi.org/10.1038/374693a0)；[PMID 7715723](https://pubmed.ncbi.nlm.nih.gov/7715723/) |
| [2GF1](https://www.rcsb.org/structure/2GF1) | Solution structure of human insulin-like growth factor 1: a nuclear magnetic resonance and restrained molecular dynamics study.；Biochemistry；1991 | [DOI 10.1021/bi00236a022](https://doi.org/10.1021/bi00236a022)；[PMID 2036417](https://pubmed.ncbi.nlm.nih.gov/2036417/) |
| [2PTC](https://www.rcsb.org/structure/2PTC) | The Geometry of the Reactive Site and of the Peptide Groups in Trypsin, Trypsinogen and its Complexes with Inhibitors；Acta Crystallogr.,Sect.B；1983 | [PMID -1](https://pubmed.ncbi.nlm.nih.gov/-1/) |
| [3HFM](https://www.rcsb.org/structure/3HFM) | Structure of an antibody-antigen complex: crystal structure of the HyHEL-10 Fab-lysozyme complex.；Proc.Natl.Acad.Sci.USA；1989 | [DOI 10.1073/pnas.86.15.5938](https://doi.org/10.1073/pnas.86.15.5938)；[PMID 2762305](https://pubmed.ncbi.nlm.nih.gov/2762305/) |
| [3HHR](https://www.rcsb.org/structure/3HHR) | Human growth hormone and extracellular domain of its receptor: crystal structure of the complex.；Science；1992 | [PMID 1549776](https://pubmed.ncbi.nlm.nih.gov/1549776/) |
| [3IL8](https://www.rcsb.org/structure/3IL8) | Crystal structure of interleukin 8: symbiosis of NMR and crystallography.；Proc.Natl.Acad.Sci.USA；1991 | [DOI 10.1073/pnas.88.2.502](https://doi.org/10.1073/pnas.88.2.502)；[PMID 1988949](https://pubmed.ncbi.nlm.nih.gov/1988949/) |
| [3INK](https://www.rcsb.org/structure/3INK) | Response.；Science；1992 | [DOI 10.1126/science.257.5068.412](https://doi.org/10.1126/science.257.5068.412)；[PMID 17832837](https://pubmed.ncbi.nlm.nih.gov/17832837/) |
| [4FGF](https://www.rcsb.org/structure/4FGF) | Refinement of the structure of human basic fibroblast growth factor at 1.6 A resolution and analysis of presumed heparin binding sites by selenate substitution.；Protein Sci.；1993 | [PMID 7691311](https://pubmed.ncbi.nlm.nih.gov/7691311/) |
| [5EBX](https://www.rcsb.org/structure/5EBX) | The crystal structure of erabutoxin a at 2.0-A resolution.；J.Biol.Chem.；1989 | [PMID 2722828](https://pubmed.ncbi.nlm.nih.gov/2722828/) |

### 原库 experimental references

以下题名与 bibliographic fields 来自实际 reference 表，保留原拼写/缺漏；不是声明逐篇已归档或读完。原文 URL 可能缺失/截断，未猜测新 DOI。

| 原 refID | 作者 / 年份 | 原 experimental reference |
| --- | --- | --- |
| 1 | Ackermann, E. J., Ang, E. T.-H., Kanter, J. R., Tsigelny, I. and Taylor, P. (1998) | `Identification of pairwise interactions in the $alpha$-neurotoxin-nicotinic acetylcholine receptor complex through double mutant cycles`；J. Biol. Chem. 273:10958–10964 |
| 2 | Ashkenazi, A., Presta, L. G., Marsters, S. A., Camerato, T. R., Rosenthal, K. A., Fendly, B. M. and Capon, D. J. (1990) | `Mapping the CD4 binding site for human immunodeficiency virus by alanine-scanning mutagenesis`；Proc. Natl. Acad. Sci. USA 87:7150–7154 |
| 3 | Bass, S. H., Mulkerrin, M. G. and Wells, J. A. (1991) | `A systematic mutational analysis of hormone-binding determinants in the human growth hormone receptor`；Proc. Natl. Acad. Sci. USA 88:4498–4502 |
| 4 | Castro, M. M. and Anderson, S. (1996) | `Alanine pont-mutations in the reactive region of bovine pancreatic trypsin inhibitor: effects on the kinetics and thermodynamics of binding to $eta$-trypsin and $alpha$-chymotrypsin`；Biochemistry 35:11435–11446 |
| 5 | Cedergren, L., Andersson, R., Jansson, B., Uhlen, M. and Nilsson, B. (1993) | `Mutational analysis of the interaction between staphylococcal protein A and human IgG1`；Prot. Eng. 6:441–448 |
| 6 | Chen, C. and Shapiro, R. (1997) | `Site-specific mutagenesis reveals differences in the structural bases for tight binding of RNase inhibitor to angiogenin and RNase A`；Proc. Natl. Acad. Sci. USA 94:1761–1766 |
| 7 | Clackson, T. and Wells, J. A. (1995) | `A hot spot of binding energy in a hormone-receptor interface`；Science 267:383–386 |
| 8 | Cunningham, B. C. and Wells, J. A. (1989) | `High-resolution epitope mapping of hGH-receptor interactions by alanine-scanning mutagenesis`；Science 244:1081–1085 |
| 9 | Cunningham, B. C. and Wells, J. A. (1991) | `Rational design of receptor-specific variants of human growth hormone`；Proc. Natl. Acad. Sci. USA 88:3407–3411 |
| 10 | Cunningham, B. C. and Wells, J. A. (1993) | `Comparison of a structural and a functional epitope`；J. Mol. Biol. 234:554–563 |
| 11 | Dall'Acqua, W., Goldman, E. R., Eisenstein, E. and Mariuzza, R. A. (1996) | `A mutational analysis of the binding of two different proteins to the same antibody`；Biochemistry 35:9667–9676 |
| 12 | Dall'Acqua, W., Goldman, E. R., Lin, W., Teng, C., Tsuchiya, D., Li, H., Ysern, X., Braden, B. C., Li, Y., Smith-Gill, S. J. and Mariuzza, R. A. (1998) | `A mutational analysis of binding interactions in an antigen-antibody protein-protein complex`；Biochemistry 37:7981–7991 |
| 13 | Davis, S. J., Davies, E. A., Tucknott, M. G., Jones, E. and Merwe, P. (1998) | `The role of charged residues mediating low affinity protein-protein recognition at the cell surface by CD2`；Proc. Natl. Acad. Sci. USA 95:5490–5494 |
| 14 | Dennis, M. S., Carter, P. and Lazarus, R. A. (1993) | `Binding interactions of kistrin with platelet glycoprotein IIb-IIIa: analysis by site-directed mutagenesis`；Proteins: Struct. Func. Genet. 15:312–321 |
| 15 | Dickinson, C. D., Kelly, C. R. and Ruf, W. (1996) | `Identification of surface residues mediating tissue factor binding and catalytic function of the serine protease factor VIIa`；Proc. Natl. Acad. Sci. USA 93:14379–14383 |
| 16 | Ducancel, F., Merienne, K., Fromen-Romano, C., Tremeau, O., Pillet, L., Drevet, P., Zinn-Justin, S., Boulain, J. and Menez, A. (1996) | `Mimicry between receptors and antibodies`；J. Biol. Chem. 271:31345–31353 |
| 17 | Duncan, A. R. and Winter, G. (1988) | `The binding site for C1q on IgG`；Nature 332:738–740 |
| 18 | Gibbs, C. S., McCurday, S. N., Leung, L. L. and Paborsky, L. R. (1994) | `Identification of the factor VIIa bidning site of tissue factor by homologous loop swap and alanine scanning mutatgenesis`；Biochemistry 33:14003–14010 |
| 19 | Goldman, E. R., Dall'Acqua, W., Braden, B. C. and Mariuzza, R. A. (1997) | `Analysis of binding interactions in an idiotope-antiidiotope protein-protein complex by double mutant cycles`；Biochemistry 36:49–56 |
| 20 | Goldstein, S. A., Pheasant, D. J. and Miller, C. (1994) | `The charybdotoxin receptor of a Shaker K+ channel: peptide and channel residues mediating molecular recognition`；Neuron 12:1377–1388 |
| 21 | Hawkins, R. E., Russell, S. J., Baier, M. and Winter, G. (1993) | `The contribution of contact and non-contact residues of antibody in the affinity of binding to antigen`；J. Mol. Biol. 234:958–964 |
| 22 | Hebert, C. A., Vitangcol, R. V. and Baker, J. B. (1991) | `Scanning mutagenesis of interleukin-8 identifies a cluster of residues required for receptor binding`；J. Biol. Chem. 266:18989–18994 |
| 23 | Hebert, C. A., Chuntharapai, A., Smith, M., Colby, T., Kim, J. and Horuk, R. (1993) | `Partial functional mapping of the human interleukin-8 type A receptor`；J. Biol. Chem. 268:18549–18553 |
| 24 | Huang, M., Syed, R., Stura, E. A., Stone, M. J., Stefanko, R. S., Ruf, W., Edgington, T. A. and Wilson, I. A. (1998) | `The mechanism of an inhibitory antibody on TF-initiated blodd coagulation revealed by the crystal structures of human tissue factior, Fab 5G9, and TF-5G9 complex`；J. Mol. Biol. 275:873–894 |
| 25 | Imler, J., Miyajima, A. and Zurawski, G. (1992) | `Identification of three adjacent amino acids of interleukin-2 receptor $eta$ chain which control the affinity and the specificity of the interaction with interleukin-2`；EMBO J. 11:2047–2053 |
| 26 | Jansson, M., Anderson, G., Uhlen, M., Nilsson, B. and Kordel, J. (1998) | `The insulin-like growth factor (IGF) binding protein 1 binding epitope on IGF-I probed by heteronuclear NMR spectroscopy and mutational analysis`；J. Biol. Chem. 273:24701–24707 |
| 27 | Jin, L., Fendly, B. M. and Wells, J. A. (1992) | `High resolution functional analysis of antibody-antigen interactions`；J. Mol. Biol. 226:851–865 |
| 28 | Kam-Morgan, L. N., Smith-Gill, S. J., Taylor, M. G., Zhang, L., Wilson, A. C. and Kirsch, J. F. (1993) | `High-resolution mapping of the HyHEL-10 epitope of chicken lysozyme by site-directed mutagenesis`；Proc. Natl. Acad. Sci. USA 90:3958–3962 |
| 29 | Kelley, R. F. and O'Connell, M. P. (1993) | `Thermodynamic analysis of an antibody functional epitope`；Biochemistry 32:6828–6835 |
| 30 | Kelley, R. F., Costas, K. E., O'Connell, M. P. and Lazarus, R. A. (1995) | `Analysis of the factor VIIa binding site on human tissue factor: effects of tissue factor mutations on the kinetics and thermodynamics of binding`；Biochemistry 34:10383–10392 |
| 31 | Leong, S. R., Kabakoff, R. C. and Hebert, C. A. (1994) | `Complete mutagenesis of the extracellular domain of interleukin-8 (IL-8) type A receptor identifies charged residues mediating IL-8 binding and signal transduction`；J. Biol. Chem. 269:19343–19348 |
| 32 | Letzelter, F., Wang, Y. and Sebald, W. (1998) | `The interleukin-4 site-2 epitope determining binding of the common receptor $gamma$ chain`；Eur. J. Biochem. 257:11–20 |
| 33 | Li, X., Rock, F., Chong, P., Cockle, S., Keating, A., Ziltner, H. and Klein, M. (1993) | `Structure-function analysis of the C-terminal segment of human interleukin-6`；J. Biol. Chem. 268:22377–22384 |
| 34 | Li, W., Hamill, S. J., Hemmings, A. M., Moore, G. R., James, R. and Kleanthous, C. (1998) | `Dual recognition and the role of specificity-determining residues in colicin E9 DNase-immunity protein interactions`；Biochemistry 37:11771–11779 |
| 35 | Muller, Y. A., Li, B., Christinger, H. W., Wells, J. A., Cunningham, B. C. and Vos, A. M. (1997) | `Vascular endothelial growth factor: crystal structure and functional mapping of the kinase domain receptor binding site`；Proc. Natl. Acad. Sci. USA 94:7192–7197 |
| 36 | Muller, Y. A., Chen, Y., Christinger, H. W., Li, B., Cunningham, B. C., Lowman, H. B. and Vos, A. M. (1998) | `VEGF and the Fab fragment of a humanized neutralizing antibody: crystal structure of the complex at 2.4 A resolution and mutational analysis of the interface`；Structure 6:1153–1167 |
| 37 | Mynarcik, D. C., Yu, G. and Whittaker, J. (1996) | `Alanine-scanning mutagenesis of a C-terminal ligand binding domain of the insulin receptor $alpha$ subunit`；J. Biol. Chem. 271:2439–2442 |
| 38 | Okano, H., Cyert, M. C. and Ohya, Y. (1998) | `Importance of phenylalanine residues of yeast calmodulin for target binding and activation`；J. Biol. Chem. 273:26375–26382 |
| 63 | Schluter, K., Schleicher, M., , . and Jocksuch, B. (1998) | `Effects of single amino acid substitutions in the actin binding site on the biological activity of bovine profilin I`；J. Cell Sci. 111:3261–3273 |
| 40 | Rajpal, A., Taylor, M. G. and Kirsch, J. F. (1998) | `Quantitatiove evaluation of the chicken lysozyme epitope in the HyHEL-10 Fab complex: free energies and kinetics`；Prot. Sci. 7:1868–1874 |
| 41 | Ranganathan, R., Lewis, J. H. and MacKinnon, R. (1996) | `Spatial localization of the K+ channel selectivity filter by mutant cycle-based structure analysis`；Neuron 16:131–139 |
| 42 | Reidhaar-Olson, J. F., Souza-Hart, J. A. and Selick, H. E. (1996) | `Identification of residues critical to the activity of human granulocyte colony-stimulating factor`；Biochemistry 35:9034–9041 |
| 43 | Ruf, W., Miles, D. J., Rehemtulla, A. and Edgington, T. S. (1992) | `Tissue factor residues 157--167 are required for efficient proteolytic activation of factor X and factor VII`；J. Biol. Chem. 267:22206–22210 |
| 44 | Ruf, W., Schullek, J. R., Stone, M. J. and Edgington, T. S. (1994) | `Mutational mapping of function residues in tissue factor: identification of factor VII recognition determinants in both structural modules of the predicted cytokine receptor homology domain`；Biochemistry 33:1565–1572 |
| 45 | Ruf, W., Kelley, C. R., Schullek, J. R., Martin, D. M., Polikarpov, I., Boys, C. G., Tuddenham, E. G. and Edgington, T. S. (1995) | `Energetic contributions and topographical organization of ligand binding residues of tissue factor`；Biochemistry 34:6310–6315 |
| 46 | Sauve, K., Nachman, M., Spence, C., Bailon, P., Campbel, E., Tsien, W., Kondas, J., Hakimi, J. and Ju, G. (1991) | `Localization in human interleukin 2 of the binding site to the $alpha$ chain (p55) of the interleukin 2 receptor`；Proc. Natl. Acad. Sci. USA 88:4636–4640 |
| 47 | Schreiber, G. and Fersht, A. R. (1993) | `Interaction of barnase with its polypeptide inhibitor barstar studied by protein engineering`；Biochemistry 32:5145–5150 |
| 48 | Schreiber, G. and Fersht, A. R. (1995) | `Energetics of protein-protein interactions: analysis of the barnase-barstar interface by single mutations and double mutant cycles`；J. Mol. Biol. 248:478–486 |
| 49 | Shapiro, R. and Vallee, B. L. (1989) | `Site-directed mutagenesis of histidine-13 and histidine-114 of human angiogenin.  Alanine derivatives inhibit angiogenin-induced angiogenesis`；Biochemistry 28:7401–7408 |
| 50 | Shapiro, R. and Vallee, B. L. (1992) | `Identification of functional arginines in human angiogenin by site-directed mutagenesis`；Biochemistry 31:12477–12485 |
| 51 | Smith, L. A., Reid, P. F., Wang, F. C., Parcej, D. J., Schmidt, J. J., Olson, M. A. and Dolly, J. (1997) | `Site-directed mutagenesis of dendrotoxin K reveals amino acids critical for its interaction with neuronal K+ channels`；Biochemistry 36:7690–7696 |
| 53 | Springer, B. A., Pantoliano, M. W., Barbera, F. A., Gunyuzlu, P. L., Thompson, L. D., Herblin, W. F., Rosenfeld, S. A. and Book, G. W. (1994) | `Identification and concerted function of two receptor binding surfaces on basic fibroblast growth factor required for mitogenesis`；J. Biol. Chem. 269:26879–26884 |
| 54 | Tsumoto, K., Ogasahara, K., Ueda, Y., Watanabe, K., Yutani, K. and Kumagai, I. (1995) | `Role of Tyr residues in the contact region of anti-lysozyme monoclonal antibody HyHEL10 for antigen binding`；J. Biol. Chem. 270:18551–18557 |
| 55 | Urfer, R., Tsoulfas, P., Soppet, D., Escandon, E., Parada, L. F. and Presta, L. G. (1994) | `The binding epitopes of neurotrophin-3 to its receptors trkC and gp75 and the design of a multifunctional human neurotrophin`；EMBO J. 13:5896–5909 |
| 56 | Wallis, R., Leung, K., Osborne, M. J., James, R., Moore, G. R. and Kleanthous, C. (1998) | `Specificity in protein-protein recognition: conserved Im9 residues are the major determinants of stability in the colicin E9 DNase-Im9 complex`；Biochemistry 37:476–485 |
| 57 | Wang, Y., Shen, B. and Sebald, W. (1997) | `A mixed charge pair in human interleukin 4 dominates high-affinity interaction with the receptor $alpha$ chain`；Proc. Natl. Acad. Sci. USA 94:1657–1662 |
| 59 | Williams, P. F., Mynarcik, D. C., Yu, G. and Whittaker, J. (1995) | `Mapping of an NH2-terminal ligand binding site of the insulin receptor by alanine scanning mutagenesis`；J. Biol. Chem. 270:3012–3016 |
| 60 | Young, D. C., Zhan, H., Cheng, Q., Hou, J. and Matthews, D. J. (1997) | `Characterization of the receptor binding determinants of granulocyte colony stimulating factor`；Prot. Sci. 6:1228–1236 |
| 61 | Zhu, H., Ramnarayan, K., Anchin, J., Miao, W. Y., Sereno, A., Millman, L., Zheng, J., Balaji, V. and Wolff, M. E. (1995) | `Glu-96 of basic fibroblast growth factor is essential for high affinity receptor binding`；J. Biol. Chem. 270:21869–21874 |
| 62 | Zurawski, S. M., Vega, F., Jr., J., Doyle, E. L., Huyghe, B., Flaherty, K., McKay, D. B. and Zurawski, G. (1993) | `Definition and spatial location of mouse interleukin-2 residues that interact with its heterotrimeric receptor`；EMBO J. 12:5113–5119 |
| 64 | Churchill, H. R., Andersen, P. S., Parke, E. A., Mariuzza, R. A., , . and Kranz, D. M. (2000) | `Mapping the energy of superantigen <i>Staphylococcus</i> enterotoxin C3 recognition of an alpha/beta T cell receptor using alanine scanning mutagenesis`；J. Exp. Med. 191:835–846 |
| 65 | Leder, L., Llera, A., Lavoie, P. M., Lebedeva, M. I., Li, H., Sekaly, R.-P., Bohach, G. A., Gahr, P. J., Schlievert, P. M., Karjalainen, Mariuzza, R. A. (1998) | `A mutational analysis of the binding of staphylococcal enterotoxind B and C3 to the T cell receptor beta chain and major histocompatibility complex class II`；J. Exp. Med. 187:823–833 |
| 66 | Schwesinger, F., Ros, R., Strunz, T., Anselmetti, D., Guntherodt, J.-J., Honegger, A., Jermutus, L., Tiefenauer, L., and Pluckthun, A. (2000) | `Unbinding forces of single antibody-antigen complexes correlate with their thermal dissociation rates`；Proc. Natl. Acad. Sci. USA 97:9972–9977 |
| 67 | Shapiro, R., Ruiz-Gutierrez, M., Chen, C.-Z. (2000) | `Analysis of the interactions of human ribonuclease inhibitor with angiogenin and ribonuclease A by mutagenesis: importance of inhibitor residues inside versus outside the C-terminal \"hot-spot\"`；J. Mol. Biol. 302:497–519 |
| 68 | Acton, T. B., Mead, J., Steiner, A. M. and Vershon, A. K. (2000) | `Scanning mutagenesis of Mcm1: residues required for DNA binding, DNA bending, and transcriptional activation by a MADS-box protein`；Mol. Cell. Biol. 20:1–11 |
| 69 | Jacobsen, R. B., Koch, E. D., Lange-Malecki, B., Stocker, M., Verhey, J., Van Wagoner, R. M., Vyazovkina, A., Olivera, B. M., Terlau, H. (2000) | `Single amino acid substitutions in k-conotoxin PVIIA disrupt interaction with the shaker K+ channel`；J. Biol. Chem 275:24639–24644 |
| 70 | Kormos, J., Johnson, P. E., Brun, E., Tomme, P., McIntosh, L. P., Haynes, C. A., and Kilburn D.G. (2000) | `Binding site analysis of cellulose binding domain CBDN1 from endoglucanase C of Cellulomonas fimi by site-directed mutagenesis`；Biochemistry 39:8844–8852 |
| 71 | He, Z., Crist, M., Yen, H.-C., Duan, X., Quiocho, F. A., and Gimble, F. S. (1998) | `Amino acid residues in both the protein splicing and endonuclease domains of the PI-SceI intein mediate DNA binding`；J. Biol. Chem. 273:4607–4615 |
| 73 | Brown, B. M., Milla, M. E., Smith, T. L., and Sauer, R. T. (1994) | `Scanning mutagenesis of the Arc repressor as a functional probe of operator recognition`；Nature Struct. Biol. 1:164–168 |
| 72 | Yang, M., Chen, X.-P., Militello, K., Hoffman, R., Fernandez, B., Baumann, C., Bollnick, P. (1997) | `Alanine-scanning mutagenesis of <i>Bacillus subtilis trp</i> RNA-binding attenuation protein (TRAP) reveals residues invloved in tryptophan binding and RNA binding`；J. Mol. Biol. 270:696–710 |
| 74 | Dhalluin, C., Carlson, J. E., Zeng, L., He, C., Aggarwal, A. K., and Zhou, M.-M. (1999) | `Structure and ligand of a histone acetyltransferase bromodomain`；Nature 399:491–496 |
| 75 | Hatta, T., Konishi, H., Katoh, E., Natsume, T., Ueno, N., Kobayashi, Y., Yamazaki, T. (2000) | `Identification of the Ligand -Binding Site of the BMP Type IA Receptot for BMP-4`；Biopolymers 55:399–406 |
| 76 | Xiang, (2001) | `Determination`；J. 276:17380–17386 |
| 77 | Tahiri, B., Auzou, G. Nicolas, J.-C., Sultan, C., Lupo, B. (2001) | `Participation of critical residues from the extreme C-terminal end of the human androgen receptor in the ligand binding function`；Biochem. 40:8431–8437 |

## 其他

### 数据范围和限制

完整取得的是这个已固定的历史三表 dump 与参考结构，不是当前原站服务、每个突变的完整表达序列/实验结构或全部底层仪器数据。论文规模与文件规模不同，重复/孤儿/零默认值不能在 raw 静默修复。

### 完整性与验收

payload 共 1 文件、283,414 bytes；同样排序 inventory SHA-256 为 `be3a4cdaefff60840e7d068261aa170f0d424439ba81b02145cb8b4d92ff9154`。独立审计要求 config 中目标文件集合与实际完全一致（允许 source README，保留上游自己的 README），拒绝 symlink、旁路 JSON/API/manifest、partial 文件或缺少任何可公开 PDB 层。PDF 页数/签名、XLSX 全部 worksheet、ZIP 全部 CRC 与安全成员均按文件类型核验；研究审计结果只保存本人 context，不发布为 raw sidecar。

上游 payload 文件身份；SHA-256 为获取后固定的本地值：

| payload 文件 | bytes | SHA-256 |
| --- | --- | --- |
| ASEdb_2010-07-21_Wayback-MySQLDump.mysql | 283414 | `ff1d48fd8f97630b474a0847d79a659fa585dffbfe9dc324b85440408bf2dd35` |

### 许可和再分发边界

原站有意提供完整 MySQL 下载并要求发表时引用 ASEdb；未找到数据库独立 CC/开放再分发许可。保留原权利边界，仅用于本次研究归档，不据此宣称可公开再发布或商业使用。论文 © OUP 2001，原站 reprint 与公开存档不等于新 CC 授权；各原实验文献权利另行保留。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 历史全库 SQL | 三个完整表：3043/101/74 行，37 个原始字段 | 已取得此固定历史文件 |
| 2001 论文 2919 mutants | 2001 正式 PDF 2 页；晚期 dump 3043 行 | 不能混同规模 |
| 原库有 accession 的系统 | 76 系统、32 唯一 PDB，全 native FASTA/mmCIF | 已包含参考；非逐变体 |
| 25 个无 accession 系统 | 19 SQL NULL、6 空字符串 | 无可指定结构，不臆配 |
| 最新库/实验仪器 raw/完整变体序列 | 历史服务不可用、原 dump 没有这些内容 | 未获得完整研究范围 |
