---
- tags:
  - context
---

# SRC_R38_INTACT 数据说明

## 数据集身份

- `source_id`：`SRC_R38_INTACT`
- `source_version`：`snapshot-2026-01-14`
- 原作者或发布机构：EMBL-EBI IntAct 与参与提供证据的 IMEx / 来源数据库

## 实验设计和数据口径

IntAct 是人工整理的分子相互作用数据库，整合多篇论文、物种、分子类型与检测方法，不是一场统一抗体实验。本包保留非聚类 MITAB27 证据导出，属于处理后数据库表；项目 raw 仅表示来源原样输入。上游 README 说明每行一个 binary interaction evidence；不同 assay、出版物、条件和 construct 不可汇总成同一 KD。

主表 1,787,425 行、独立阴性表 983 行；ZIP 中的阴性成员与外部 TXT 完全同字节，只算一次。主表 916,318 个唯一原始 interaction identifier 字段值，并不是相同数量的抗体或所有唯一实验。95,405 行含 MI:0407 direct interaction，933,611 行标注 MI:1060 spoke expansion；n-ary 复合物被扩展成二元边，行数会膨胀，而且二元边不保证直接接触。所有主表 Negative=false、阴性表 true 仅表示数据库证据极性，不能将整个表作为 antibody binder/non-binder。

Interaction parameter 可含 kd、kon、koff、IC50、EC50、温度及其他单位；kd 出现 59,213 次是字段项计数，不是 59,213 个可用于抗体训练的独立 KD。intact-miscore 是派生证据评分，不能当亲和力；不要把缺失参数填零。多值 ID、同一 interaction 的展开行、mutant features、未知/未分配文献键和实验来源都应保留。

按参与者 alias/type/annotation 审计，主表 7,828 行命中 antibody/nanobody/VHH/scFv/immunoglobulin，其中 446 行是 MI:0407；这是候选数，不是已确认抗体数。类型字段没有 MI:2440 antibody。Ki-67 名称来自检测它的抗体，BiP 是 immunoglobulin-binding chaperone，HAVCR1/TCF3 也不是抗体。检测方法含免疫学试剂同样不能证明参与者是抗体。

明确标为 antibody hc/lc 的 SG/19 复合物记录有 x-ray 与 pdbe 证据，但 Interaction type 标为 MI:0915 physical association；仅筛 MI:0407 会漏掉这些记录。当前未建立人工验证的抗体直接结合子集、统一抗原/抗体序列表或 KD 标签；这些属于后续 processed 流程。不能声称已获得预制的 R38 抗体 benchmark。

## 论文原文

### IntAct 数据库论文

- 标题：The IntAct database: efficient access to fine-grained molecular interaction data
- 作者：del Toro Noemi；Shrivastava Anjali；Ragueneau Eliot；Meldal Birgit；Combe Colin；Barrera Elisabet；Perfetto Livia；How Karyn；Ratan Prashansa；Shirodkar Gautam；Lu Odilia；Mészáros Bálint；Watkins Xavier；Pundir Sangya；Licata Luana；Iannuccelli Marta；Pellegrini Matteo；Martin Maria Jesus；Panni Simona；Duesbury Margaret；Vallet Sylvain D；Rappsilber Juri；Ricard-Blum Sylvie；Cesareni Gianni；Salwinski Lukasz；Orchard Sandra；Porras Pablo；Panneerselvam Kalpana；Hermjakob Henning
- 发表来源：Nucleic Acids Research
- 归档文本版本：正式发表版（完整 JATS XML）
- 发布日期：2021-11-11
- DOI：10.1093/nar/gkab1006
- PMID / PMCID：34761267 / PMC8728211
- 本地文件：`articles/IntAct_2021-11-11_NAR-VoR.xml`
- 文件大小：81.56 KiB（83,519 bytes）
- SHA-256：`0b7422b9efc9da7d8c80245a99a1ced2a1ee3d1010724d28ab3c064b65b68d16`
- 文本许可：CC BY 4.0
- 补充材料：主文 XML 未声明独立 supplementary media

### SG19 结构来源论文

- 标题：Crystal structure of α5β1 integrin ectodomain: Atomic details of the fibronectin receptor
- 作者：Nagae Masamichi；Re Suyong；Mihara Emiko；Nogi Terukazu；Sugita Yuji；Takagi Junichi
- 发表来源：Journal of Cell Biology
- 归档文本版本：正式发表版（完整 JATS XML）
- 发布日期：2012-03-26
- DOI：10.1083/jcb.201111077
- PMID / PMCID：22451694 / PMC3317794
- 本地文件：`articles/IntActNagae_2012-03-26_JCB-VoR.xml`
- 文件大小：120.31 KiB（123,201 bytes）
- SHA-256：`85bbb410a68387279e01f0a61babb622be2426453ded03880af9366a7f22b50e`
- 文本许可：CC BY-NC-SA 3.0
- 补充材料：主文 XML 未声明独立 supplementary media

## 仓库内容

一手 [IntAct current FTP](https://ftp.ebi.ac.uk/pub/databases/intact/current/psimitab/) 的四个对象。版本日期来自 intact.zip 的 Last-Modified 2026-01-14，而非 2026-09-18 下载日。current URL 可变，ETag 保护本次获取；本地 SHA-256 冻结对象副本，不宣称这是不可变的上游 release。README/CHANGES 正文包含历史说明，不代表正文在对象日期发生了科学更新。

| 对象 | Last-Modified | ETag | 大小 |
| --- | --- | --- | --- |
| IntAct/psimitab/intact.zip | Wed, 14 Jan 2026 11:51:57 GMT | `"50836a8b-64857bc3f8ba1"` | 1.26 GiB（1,350,789,771 bytes） |
| IntAct/psimitab/intact_negative.txt | Wed, 14 Jan 2026 11:51:17 GMT | `"4f064c-64857b9dd2a38"` | 4.94 MiB（5,178,956 bytes） |
| IntAct/psimitab/README | Wed, 14 Jan 2026 11:55:43 GMT | `"8d7-64857c9b23391"` | 2.21 KiB（2,263 bytes） |
| IntAct/CHANGES | Wed, 14 Jan 2026 11:13:33 GMT | `"107b-6485732e97e86"` | 4.12 KiB（4,219 bytes） |

```text
snapshot-2026-01-14/
    IntAct/CHANGES
    IntAct/psimitab/README
    IntAct/psimitab/intact.zip
    IntAct/psimitab/intact_negative.txt
```

ZIP 是完整原始交付归档；独立阴性 TXT 是同一负证据的另一官方交付对象。README 解释导出，CHANGES 解释历史格式变化；本目录不是整个 IntAct FTP 镜像。

## 数据结构

### ZIP 成员和记录关系

| 原始成员 | 未压缩大小 | CRC32 |
| --- | --- | --- |
| intact.txt | 10.40 GiB（11,165,428,413 bytes） | `f4dd73ec` |
| intact_negative.txt | 4.94 MiB（5,178,956 bytes） | `ed1228c4` |

两 TXT 均是 UTF-8、第一行 # 开头的 42 列 MITAB27 表头、TAB 分隔、| 分隔字段内多值。全部行严格为 42 列，完整读取到 EOF 通过 ZIP CRC；没有解压重写。缺失用字面 `-` 或空串，分别统计，不补齐值。interaction identifier 可重复，且没有统一的抗体序列列或抗体 ID 键；原对象、文献和证据级键构成后续审计上下文。

### 字段说明

| 列（1-based） | 原字段名 | 原表示、单位/方向、含义 | 主表缺失 -/空串数 |
| --- | --- | --- | --- |
| 1 | `#ID(s) interactor A` | 字符串 / 来源实验或文献整理；参与者 A 的命名空间 ID；非氨基酸序列，未保证一个 ID 对应所有实验 construct | 0 |
| 2 | `ID(s) interactor B` | 字符串 / 来源实验或文献整理；参与者 B 的命名空间 ID；与 A 组成二元证据行 | 324 |
| 3 | `Alt. ID(s) interactor A` | 字符串 / 来源实验或文献整理；A 的其他数据库 ID；\| 分隔，可含 isoform 与多个历史 ID | 28826 |
| 4 | `Alt. ID(s) interactor B` | 字符串 / 来源实验或文献整理；B 的其他数据库 ID；\| 分隔，不是实验 replicate | 17704 |
| 5 | `Alias(es) interactor A` | 字符串 / 来源实验或文献整理；A 的显示名、gene name、同义名；名字含 antibody 不足以证明它是抗体 | 0 |
| 6 | `Alias(es) interactor B` | 字符串 / 来源实验或文献整理；B 的显示名、gene name、同义名；保留原始 psi-mi/uniprotkb 表示 | 324 |
| 7 | `Interaction detection method(s)` | 字符串 / 来源实验或文献整理；实验检测方法 PSI-MI CV；抗体检测试剂不能变成参与者身份 | 0 |
| 8 | `Publication 1st author(s)` | 字符串 / 来源实验或文献整理；出版物第一作者表示；文献归属，不是样本 ID | 2599 |
| 9 | `Publication Identifier(s)` | 字符串 / 来源实验或文献整理；PubMed / DOI / IMEx 等文献键；可有未分配 PMID，不删记录 | 0 |
| 10 | `Taxid interactor A` | 字符串 / 来源实验或文献整理；A 的来源 taxonomy ID / 名称；不是整个实验的 host | 0 |
| 11 | `Taxid interactor B` | 字符串 / 来源实验或文献整理；B 的来源 taxonomy ID / 名称；同样不等于 assay host | 324 |
| 12 | `Interaction type(s)` | 字符串 / 来源实验或文献整理；相互作用类型 PSI-MI CV；MI:0407 direct interaction，MI:0915 physical association 等不能互换 | 0 |
| 13 | `Source database(s)` | 字符串 / 来源实验或文献整理；提供证据的数据库；非仪器单位 | 0 |
| 14 | `Interaction identifier(s)` | 字符串 / 来源实验或文献整理；原相互作用证据键；可同时有 intact / imex / pdbe，一证据可扩展为多行 | 0 |
| 15 | `Confidence value(s)` | 字符串 / 来源实验或文献整理；置信评分，例如 intact-miscore；派生证据质量，没有 KD 单位或抗体亲和力方向 | 142 |
| 16 | `Expansion method(s)` | 字符串 / 来源实验或文献整理；多参与者实验的二元化方法；MI:1060 spoke expansion 不是直接接触保证 | 853814 |
| 17 | `Biological role(s) interactor A` | 字符串 / 来源实验或文献整理；A 的生物角色 PSI-MI CV；证据注释 | 0 |
| 18 | `Biological role(s) interactor B` | 字符串 / 来源实验或文献整理；B 的生物角色 PSI-MI CV；证据注释 | 324 |
| 19 | `Experimental role(s) interactor A` | 字符串 / 来源实验或文献整理；A 的实验角色 PSI-MI CV，例如 bait/prey；不是 replicate ID | 0 |
| 20 | `Experimental role(s) interactor B` | 字符串 / 来源实验或文献整理；B 的实验角色 PSI-MI CV；实验角色与分子类型独立 | 324 |
| 21 | `Type(s) interactor A` | 字符串 / 来源实验或文献整理；A 的分子类型 PSI-MI CV；protein 包含大量非抗体，不足以筛选抗体 | 0 |
| 22 | `Type(s) interactor B` | 字符串 / 来源实验或文献整理；B 的分子类型 PSI-MI CV；本快照没有 MI:2440 antibody 类型行 | 324 |
| 23 | `Xref(s) interactor A` | 字符串 / 来源实验或文献整理；A 的数据库交叉引用，可能有 pdbe/rcsb pdb；是蛋白 reference，不自动表示此复合物 | 57898 |
| 24 | `Xref(s) interactor B` | 字符串 / 来源实验或文献整理；B 的数据库交叉引用；需要逐条核对结构与此证据的关系 | 31609 |
| 25 | `Interaction Xref(s)` | 字符串 / 来源实验或文献整理；相互作用交叉引用；与 interactor xref 层级不同 | 1501382 |
| 26 | `Annotation(s) interactor A` | 字符串 / 来源实验或文献整理；A 的注释 key:value；含一般 function 与实验信息，不因文字提到抗体就当抗体 | 1405108 |
| 27 | `Annotation(s) interactor B` | 字符串 / 来源实验或文献整理；B 的注释 key:value；保留引号、多值和 Unicode | 1397049 |
| 28 | `Interaction annotation(s)` | 字符串 / 来源实验或文献整理；相互作用注释；含 figure legend、curation depth、dataset、coverage 等 | 40835 |
| 29 | `Host organism(s)` | 字符串 / 来源实验或文献整理；实验 host taxonomy ID / 名称；与 A/B 物种区分 | 0 |
| 30 | `Interaction parameter(s)` | 字符串 / 来源实验或文献整理；实验参数 key:value(unit)，有 kd/kon/koff/ic50/ec50 等；数值/单位需逐参数解释，KD 越低较强，IC50/EC50 不能直接当 KD | 1726876 |
| 31 | `Creation date` | 字符串 / 来源实验或文献整理；数据库创建日期字符串；不是实验发生日或数据版本日 | 0 |
| 32 | `Update date` | 字符串 / 来源实验或文献整理；数据库更新日期字符串；不是独立新样本 | 0 |
| 33 | `Checksum(s) interactor A` | 字符串 / 来源实验或文献整理；A 的校验标识（如 rogid）；不是完整序列下载 | 75505 |
| 34 | `Checksum(s) interactor B` | 字符串 / 来源实验或文献整理；B 的校验标识；不把它重建为序列 | 29629 |
| 35 | `Interaction Checksum(s)` | 字符串 / 来源实验或文献整理；相互作用 checksum / rigid；派生标识，不是亲和力标签 | 21911 |
| 36 | `Negative` | 字符串 / 来源实验或文献整理；原文布尔 true/false；true 为 curated negative evidence，受实验条件约束，不是统一抗体二元 benchmark 标签 | 0 |
| 37 | `Feature(s) interactor A` | 字符串 / 来源实验或文献整理；A 的实验 feature / 范围 / 突变注释；无需重新构建 raw 突变序列 | 589622 |
| 38 | `Feature(s) interactor B` | 字符串 / 来源实验或文献整理；B 的实验 feature / 范围 / 突变注释；不能无条件视为 WT 完整链 | 1408461 |
| 39 | `Stoichiometry(s) interactor A` | 字符串 / 来源实验或文献整理；A 的 stoichiometry 字符串；缺失不是 1 | 1729130 |
| 40 | `Stoichiometry(s) interactor B` | 字符串 / 来源实验或文献整理；B 的 stoichiometry 字符串；多构象/副本不增加独立实验数 | 1724267 |
| 41 | `Identification method participant A` | 字符串 / 来源实验或文献整理；参与者 A 的识别方法 PSI-MI CV；与 interaction detection method 区分 | 0 |
| 42 | `Identification method participant B` | 字符串 / 来源实验或文献整理；参与者 B 的识别方法 PSI-MI CV；来源实验/文献的整理注释 | 324 |

### 数据示例

`intact.txt` 第一条真实行的等价字段摘录（其他 35 列未展示）：

| #ID(s) interactor A | ID(s) interactor B | Interaction detection method(s) | Publication Identifier(s) | Interaction type(s) | Interaction identifier(s) | Negative |
| --- | --- | --- | --- | --- | --- | --- |
| `uniprotkb:O43426` | `uniprotkb:P49418` | `psi-mi:"MI:0084"(phage display)` | `pubmed:10542231\|mint:MINT-5211933` | `psi-mi:"MI:0407"(direct interaction)` | `intact:EBI-7121552\|mint:MINT-16056` | `false` |

这一行表示此文献/检测方法下的一条二元相互作用证据；参与者是蛋白，不是抗体样本。相同蛋白配对可在不同证据行重复，同一多参与者证据也可展开成多个配对。

## PDB 数据库

审计完整 MITAB27 的 participant aliases/types/annotations、Interaction identifier、Interaction Xref 和 participant Xref；同时核对 IntAct 论文与 RCSB。初次正则遗漏 pdbe 命名空间及 identifier 内结构键，纠正后重新完整遍历 ZIP。只接受可连接到明确 SG/19 抗体参与者的一手结构证据，不把全库蛋白 PDB xref 当作抗体复合物。

接受 3VI3 / 3VI4：原始 interaction identifier 分别为 EBI-26987514 / IM-29254-3 / pdbe:3vi3 和 EBI-26987501 / IM-29254-1 / pdbe:3vi4，文献 PubMed 22451694。antibody hc 为 EBI-26988198、identity accession HE578877；lc 为 EBI-26987527、HE578878。一手结构论文 DOI 10.1083/jcb.201111077 与 RCSB 均确认 α5β1 headpiece–SG/19 Fab；3VI3 无 RGD ligand，3VI4 含 RGD。

这两组键连接共享多参与者结构证据，不是所有展开二元边的独立结构、亲和力或直接接触证明。两条结构各有两份晶体内复制：entity 1 α5，chains A/C，632 aa；entity 2 β1，B/D，454 aa；entity 3 SG/19 light，L/E，219 aa；entity 4 heavy，H/F，218 aa；3VI4 另有 entity 5 RGD peptide，G/I，5 aa。未选择单份链、未重建 raw HC/LC，也不把 Fab 当完整 IgG。

审查七个明确 immunoglobulin/scFv/SG19 参与者标识的 21 行；其 interaction PDB 键只包含 3VI3/3VI4。其他关键词候选仍需文献/construct 级科学分类，未声明全库抗体结构覆盖。接受参考锚点的 PDB 获取子任务完成；抗体直接结合筛选与其他候选的逐对象映射不在本次已完成范围。

2026-09-18 获取，每个接受锚点的原始完整 RCSB entry FASTA 和完整 mmCIF 已通过 entry ID、全部 polymer canonical 序列一致性与 atom_site 检查；所有原始 polymer entities 保留。

| PDB | 本地路径 | 大小 | SHA-256 |
| --- | --- | --- | --- |
| 3VI3 | `pdb/sequences/rcsb_pdb_3VI3.fasta` | 1.75 KiB（1,796 bytes） | `65824714251f09e80004e199582397635cb88120518699f0b6f1894c1e790a79` |
| 3VI3 | `pdb/structures/3VI3.cif` | 2.34 MiB（2,451,361 bytes） | `37e7cbdcd08ae88a60deed625034b04a8ec55c20f2c9c06797dd9781d247cacf` |
| 3VI4 | `pdb/sequences/rcsb_pdb_3VI4.fasta` | 1.81 KiB（1,855 bytes） | `cb6e5c2207c1eab2409c95b75463b92a82248286cc6215159131578a2f806b53` |
| 3VI4 | `pdb/structures/3VI4.cif` | 2.37 MiB（2,488,516 bytes） | `db3c6f6cf8fd45bc5c9bc790b9940c39fb1cfb0f791892b70cdcddff00c2688d` |

FASTA：`https://www.rcsb.org/fasta/entry/<PDB>/download`；mmCIF：`https://files.rcsb.org/download/<PDB>.cif`。没有独立 PDB manifest 或重建的逐行 FASTA。

## 使用方式

调用者将 `dataset_root` 赋为 source version 目录；直接读 ZIP，字段按 TAB 切分：

```python
import io
from pathlib import Path
import zipfile
with zipfile.ZipFile(Path(dataset_root) / 'IntAct/psimitab/intact.zip') as archive:
    with archive.open('intact.txt') as raw, io.TextIOWrapper(raw, encoding='utf-8') as handle:
        header = next(handle).rstrip('\r\n').split('\t')
        first = next(handle).rstrip('\r\n').split('\t')
print(dict(zip(header, first)))
```

## 采集过程记录

1. 2026-09-18 读取项目/身份/清单/计划并运行 context；保存下载方案至个人 workspace。HEAD 核对四个官方 FTP 对象大小、ETag、Last-Modified，使用源对象日期命名。current 可变，所有传输带 If-Match；不另建抗体加工文件。
2. 2026-09-18 curl 断点下载 ZIP 较慢，保留 74,670,080 bytes 前缀，停止本批确切进程并改用 16 MiB 的 ETag/Content-Range 保护分块。第一次 range 流式读取超时未被 requests 异常类捕获；修正 urllib3 HTTPError 重试，保留完成/部分区间并继续，按顺序合并后大小 1,350,789,771 bytes。小文件 SSL 重连由 curl retry-all-errors 恢复。没有把部分 ZIP 发布。
3. 2026-09-18 完整遍历两个 ZIP 成员，验证重复成员/路径/symlink、42 列 UTF-8、全行类型/参数/缺失和 CRC；ZIP negative 与 standalone SHA-256 相同，避免重复计数。独立计算全部 payload SHA-256。
4. 2026-09-18 关键词命中大量非抗体，审计候选参与者身份；首次漏 pdbe / identifier 的 PDB 线索，修正并重新遍历全表，找到 SG/19 一手记录与 3VI3/3VI4。归档数据库主文和结构主文完整 EuropePMC JATS XML，核对 DOI/版本/许可。通用函数初次把 IntAct 文件名误标 mAbs；核对字节/hash 完全相同后改为 IntAct_2021-11-11_NAR-VoR.xml 并删除重复旧名。结构文章改为 IntActNagae_2012-03-26_JCB-VoR.xml；日期均来自相应正式版本的公布日。
5. 2026-09-18 获取 3VI3/3VI4 完整原始 FASTA/mmCIF，用 gemmi 对照全部实体与完整原子坐标；额外 RGD 实体保留，不能将参考覆盖宣称为数据库每条记录的结构覆盖。
6. 2026-09-18 写本地 README 后立即同步共享 staging，固定 markdownlint-cli2@0.20.0 / skill config 验至 0 errors；独立来源身份、文件 allowlist、canonical PDB、README 合同/同步验收通过后 no-replace 原子发布。清理本批临时证据缓存及空 staging，同步个人状态/handoff；公共清单只准备个人修改建议。

2026-09-22：按最新版 README 合同复核 42 个 MITAB27 原始字段在“字段说明”中的覆盖，将论文发表来源与归档版本分开记录，并将文件大小改为可读单位与精确字节并列。本次文档复核未重算 1.26 GiB 归档哈希或重新构造抗体子集；共享 README 与工作稿同步，Markdownlint 重新通过。

## 参考文献

- [IntAct 官方 FTP](https://ftp.ebi.ac.uk/pub/databases/intact/current/psimitab/)
- [IntAct 数据库论文](https://doi.org/10.1093/nar/gkab1006)
- [MITAB 官方格式](https://github.com/HUPO-PSI/miTab)
- [SG/19 结构来源论文](https://doi.org/10.1083/jcb.201111077)
- [RCSB 3VI3](https://www.rcsb.org/structure/3VI3)、[RCSB 3VI4](https://www.rcsb.org/structure/3VI4)

## 其他

### 数据范围和限制

本版本完成约定四个 MITAB27 对象和接受参考锚点的原样接入，不是整个 FTP / PSI XML / 生物实验 raw 的全研究获取，也不是处理后的抗体直接结合子集。后续筛选需要分子身份、价态、construct、文献和参数单位逐项验证；按 protein 类型、检测方法、文本关键词或 confidence 简单过滤不足以生成亲和力排名数据。

### 完整性与验收

全部 4 个 payload 文件、1.26 GiB（1,355,975,209 bytes）；固定官方对象长度 / ETag 与本地 SHA-256，UTF-8 schema 全行和全部 ZIP CRC 通过。按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序 inventory SHA-256：`6e4d18d216b0537e368e32fb6a8f591f844eb1eaccbd33e7142f70a7f348e696`。

| 上游 payload | 大小 | SHA-256 |
| --- | --- | --- |
| `IntAct/CHANGES` | 4.12 KiB（4,219 bytes） | `aa7b737b23dcd1b995e5e3817f08e54a3f73a8862e67d55e5947c459142f1950` |
| `IntAct/psimitab/README` | 2.21 KiB（2,263 bytes） | `c2ba5d37522ea3928fc68e947aec7307709da6c87a4421fada372d7501cc7130` |
| `IntAct/psimitab/intact.zip` | 1.26 GiB（1,350,789,771 bytes） | `8409c87570d9dc9d3bc3676615e29146b2d8b89bfdbf2d30efa5b46484dc7a79` |
| `IntAct/psimitab/intact_negative.txt` | 4.94 MiB（5,178,956 bytes） | `19c9ca88450a64228871c79e7c5eaf2d80d4cd63c60080236685ec7c39c2cda4` |

### 许可和再分发边界

数据库主文 Data availability 与 XML 明示 IntAct 数据 CC BY 4.0，数据库论文文本也为 CC BY 4.0。结构来源论文 XML 明示最初六个月的非商业条款，之后 CC BY-NC-SA 3.0；该旧论文的文本许可不等于数据库许可。保留数据原始来源与出版物引用，不能推广为各原始论文或所有外部资源的统一许可。

### 公开范围对照

| 来源声明 | 本地证据 | 状态 |
| --- | --- | --- |
| 未聚类 MITAB27 positive / negative export | ZIP 两成员全行 + 同字节独立阴性 TXT | 已取得约定对象 |
| 完整数据库各格式与底层研究材料 | 仅选择 MITAB27，不镜像 XML/全部实验文件 | 未完整获取 |
| 抗体直接结合子集 | 没有官方预制文件；尚未做 processed 科学筛选 | 尚未创建 |
| SG/19 结构证据 | 3VI3/3VI4 原始 FASTA/mmCIF + 原论文 | 已取得共享参考 |

## 待解决问题与处理进展

截至 2026-09-22，本次对 MITAB27 固定交付、字段说明、论文归档及 SG/19 结构锚点的复核范围内暂无待解决的来源疑问。尚未构建的抗体直接结合子集属于后续 processed 工作，当前原始交付的范围见“数据范围和限制”。
