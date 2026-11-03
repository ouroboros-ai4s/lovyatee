---
- tags:
  - context
---

# SRC_R77_AKBAR_SABDAB_KD 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [与 TDC 表的对应关系](#与-tdc-表的对应关系)
  - [字段说明](#字段说明)
  - [数据示例](#数据示例)
- [PDB 数据库](#pdb-数据库)
- [采集过程记录](#采集过程记录)
- [参考文献](#参考文献)
- [其他](#其他)
  - [数据范围和限制](#数据范围和限制)
  - [完整性与验收](#完整性与验收)
  - [许可和再分发边界](#许可和再分发边界)
  - [公开范围对照](#公开范围对照)
- [待解决问题与处理进展](#待解决问题与处理进展)

## 数据集身份

- `source_id`：`SRC_R77_AKBAR_SABDAB_KD`
- `source_version`：`zenodo-13120765`
- 原作者或发布机构：Rahmad Akbar（University of Oslo）

### 来源方背景

Rahmad Akbar 是奥斯陆大学免疫信息学方向的研究者，与 Victor Greiff 课题组合作，工作集中在抗体库分析、抗体语言模型与免疫信息学工具。Zenodo 记录只署其一人，`affiliation` 字段未填。

本记录是一份小型再发布数据集：作者把通过 Therapeutics Data Commons 取得的 SAbDab 亲和力表导出为 CSV，连同导出脚本一并上传。它没有配套论文，也没有实验产出；来源方背景因此只能说明发布者的研究领域，不构成本数据的实验或方法依据。

## 实验设计和数据口径

本数据集不含新实验。它的全部内容是一张 493 行的表，来自 SAbDab 经 TDC 处理的 `Protein_SAbDab` 数据集，作者用 TDC 的 loader 取出后以 `to_csv` 原样写出。记录描述也写明数据是“Obtained from SAbDab via Therapeutic Data Commons”。

因此本表的实验设计、测量口径与限制完全继承 TDC 与 SAbDab：每行是一个 PDB 条目中的一对特定抗体—抗原及其已发表亲和力值，不区分 SPR、ITC、ELISA 等方法，不记录温度、缓冲体系、重复次数或误差。`Y` 是亲和力数值，取值 4×10⁻¹³—2×10⁻⁴，量级与摩尔浓度 KD 相符，但公开材料未标注单位或测量类型。

### 与同源表的关系

本表与 `SRC_R76_TDC_ANTIBODYAFF` 的 `protein_sabdab.csv` 是同一份上游数据的两次导出：493 行的顺序逐行相同，`ID`、`X1`、`ID2`、`X2` 四列的字符串逐行完全相同，`Y` 只有文本精度差异。52 行的数值文本不同，例如本表写 `2.74e-11` 而上游写 `2.7399999999999997e-11`，两者作为 IEEE 双精度数在 2.2×10⁻¹⁶ 的相对误差内相等，是本表在导出时对浮点做了更短的十进制表示，不是数值差异。

这一点决定了两者的使用边界：本表可作为 TDC 表的易读替身（列名更清楚、浮点更短），但不构成独立的第二份证据。把它们当作两个数据源相加会重复计入同一批 493 次测量。

## 论文原文

本数据集没有配套论文。Zenodo record 的 `metadata` 不含 `related_identifiers` 指向任何论文，description 只说明数据来自 SAbDab 经 TDC 取得。

因此本节不记录论文条目，也不把 TDC 平台论文或 SAbDab 数据库论文写成本数据集的论文：那两篇分别解释数据生成平台与上游数据库，不是本记录的产出依据。它们在“参考文献”中作为上游来源列出。

- 标题：无
- 作者：无
- 发表来源：无
- 归档文本版本：无
- 发布日期：无
- DOI：无
- PMID / PMCID：无
- 正文在线入口：无
- 本地归档：未归档
- 文本许可：不适用
- 补充材料：无

## 仓库内容

上游是 Zenodo record `13120765`，属于 concept `13120764` 的唯一版本。记录创建与发布于 2024-07-29，`metadata.version` 未填。`source_version` 因此使用不可变 record 号 `zenodo-13120765`，不按下载日期命名。

Record 共 2 个对象，均为普通文件、无登录要求：

```text
zenodo-13120765/
├── antibody_affinity_protein_sabdab.csv
└── get_antibody_affinity_data.py
```

`antibody_affinity_protein_sabdab.csv` 是数据本体。`get_antibody_affinity_data.py` 是 418 bytes 的导出脚本，内容只有四步：`from tdc.multi_pred import AntibodyAff`、`data = AntibodyAff(name='Protein_SAbDab')`、`data.get_data().to_csv(outfile, index=False)`、调用自身。脚本里写死了输出路径 `outfile/antibody_affinity_protein_sabdab.csv`，没有版本固定、没有校验、没有参数。

该脚本解释了本表列名的来源：`Antibody_ID`、`Antibody`、`Antigen_ID`、`Antigen`、`Y` 是 TDC loader 在内存中重命名后的字段，不是 TDC 发布文件的原始列名（原始列为 `ID1`、`X1`、`ID2`、`X2`、`Y`）。两表内容因此一致而列名不同。

## 数据结构

### 与 TDC 表的对应关系

| 本表字段 | TDC `protein_sabdab.csv` 字段 | 关系 |
| --- | --- | --- |
| `Antibody_ID` | `ID1` | 同名同值，PDB 条目 ID |
| `Antibody` | `X1` | 同值，抗体链序列的 Python 列表字符串 |
| `Antigen_ID` | `ID2` | 同值，抗原名称 |
| `Antigen` | `X2` | 同值，抗原序列 |
| `Y` | `Y` | 数值等价，文本精度不同 |

TDC 表另有一个无名序列化索引列（取值 0—492），本表没有该列，因为导出时用了 `index=False`；本表也没有任何索引列，行号即文件内位置。

493 行、493 个不同 `Antibody_ID`，`(Antibody_ID, Antigen_ID)` 无重复。431 个不同抗体序列、401 个不同抗原序列、313 个不同抗原名称，与 TDC 表逐一相同。

### 字段说明

全部 5 列均为文本存储，无空值。

| 原始字段 | 表示、单位与来源 | 缺失与特殊编码 |
| --- | --- | --- |
| `Antibody_ID` | PDB 条目 ID，小写 4 字符 | 无缺失；493 个取值，无重复 |
| `Antibody` | 抗体序列，Python 列表字符串，2 个元素（重链、轻链） | 无缺失；重链 114—454 aa，轻链 104—259 aa |
| `Antigen_ID` | 抗原名称，自由文本 | 无缺失；313 个不同名称 |
| `Antigen` | 抗原序列，单条氨基酸串 | 无缺失；3—1,676 aa，107 行不超过 20 aa |
| `Y` | 亲和力数值，4×10⁻¹³—2×10⁻⁴ | 无缺失；380 个不同取值 |

`Antibody` 字段在 CSV 中被双引号包裹，内部是含单引号与逗号的列表字符串，必须先用标准 CSV 解析再用 `ast.literal_eval` 还原，不能按逗号切分。

`Y` 当前有 380 个不同取值，比 TDC 表的 383 个少 3 个。差额来自浮点文本合并：TDC 中写作 `2.7399999999999997e-11` 与 `2.74e-11` 之类的不同字符串，在本表统一为同一种写法后可能变成同值。数值本身未变，详见“与 TDC 表的对应关系”。

### 数据示例

```text
Antibody_ID=1hh6
Antibody=['QDQLQQSGAELVRPGASVKLSCKALGYIFTDYEIHWVKQTPVHGLEWIGGIHPGSSGTAYNQKFKGKATLTADKSSTTAFMELSSLTSEDSAVYYCTRKDYWGQGTLVTVSAAKTTAPSVYPLVPVCGGTTGSSVTLGCLVKGYFPEPVTLTWNSGSLSSGVHTFPALLQSGLYTLSSSVTVTSNTWPSQTITCNVAHPASSTKVDKKIEPRV', 'DIKMTQSPSSMYTSLGERVTITCKASQDINSFLTWFLQKPGKSPKTLIYRANRLMIGVPSRFSGSGSGQTYSLTISSLEYEDMGIYYCLQYDDFPLTFGAGTKLDLKRADAAPTVSIFPPSSEQLTSGGASVVCFLNNFYPKEINVKWKIDGSERQNGVLDSWTEQDSKDSTYSMSSTLTLTKDEYERHNSYTCEATHKTSTSPIVKSFNRNEC']
Antigen_ID=pep-4
Antigen=DATPEDLGARL
Y=1e-07
```

这一行与 TDC 表首行完全对应，表示 PDB 条目 `1hh6` 中抗体与 11 残基肽抗原的结合，亲和力 1×10⁻⁷。它是同一批 493 次测量中的一条，不是独立复现。

## PDB 数据库

`Antibody_ID` 直接给出 PDB 条目，映射强度为“逐行一对一”：493 行对 493 个不同 PDB ID，无需推断。锚点集合与 `SRC_R76_TDC_ANTIBODYAFF` 完全相同。

项目按这 493 个唯一 ID 从 RCSB 取得 entry 级 FASTA 与完整 mmCIF，未做选链或重建。491 个成功取得；`3RVV` 与 `3RVW` 已于 2022-04-27 被 RCSB 撤销，`id_codes_replaced_by` 分别指向 `5VPL` 与 `5VPG`，这两个替代条目本身也在 493 个 ID 内并已取得。

`pdb/` 共 982 个文件、579.02 MiB（607,146,339 bytes）：`sequences/` 与 `structures/` 各 491 个文件。按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接后的 inventory SHA-256 为 `92295c81515eca98211c5c9778064f2b6dee19d73b529ebcc5dc22f528c69386`。未发布独立 PDB manifest。

该目录的 mmCIF 与 `SRC_R76_TDC_ANTIBODYAFF` 的对应文件逐字节相同，493 个条目中有 491 个两处一致。FASTA 在两处的内容相同但 record 顺序不同：131 个文件里 entity 记录的排列顺序不一致，序列与 header 文本本身相同。两个来源在不同时间分别请求 RCSB，返回的 entity 顺序不同，导致同一内容形成不同字节。这是本目录与 R76 目录 inventory 摘要不同的唯一原因。

| 项目 | 数值 |
| --- | ---: |
| 数据表锚点数 | 493 |
| 已取得条目的 FASTA | 491 |
| 已取得条目的 mmCIF | 491 |
| 未取得条目 | 2（`3RVV`、`3RVW`，RCSB 已撤销） |
| 文件总数 | 982 |
| 总字节数 | 607,146,339（579.02 MiB） |

`Antibody` 列表中的两条链与 PDB author chain 的对应关系未在本表标注，需在使用阶段借助 entry FASTA 的 header 匹配。

## 采集过程记录

- 2026-10-28 用户指定存储根 `G:\abag-datasets`。项目无 `project.toml`、`developer.local.toml` 与 `workspace/`，因此 README 直接写入 source version 目录，未按 skill 的 `workspace/users/<user>/docs/readme/` 生成草稿；该偏差已获用户同意。
- 2026-10-28 通过 Zenodo API `https://zenodo.org/api/records/13120765` 取得 record metadata，确认 2 个文件、字节数、MD5 与 `CC BY` 之外的许可字段（`apache2.0`）。随后以 `/files/<name>/content` 端点逐个下载。
- 2026-10-28 下载完成后计算 MD5，两个文件均与 Zenodo 记录一致：CSV 为 `6f982caf45f4bfb921a2d759ee41913c`，脚本为 `588df8db4aa8135d8ad469352b79c74b`。
- 2026-10-29 复算并补记 SHA-256。校验 `get_antibody_affinity_data.py` 的内容，确认它调用 TDC loader 后以 `to_csv(index=False)` 写出，据此解释本表与 TDC 表的列名差异。
- 2026-10-29 与 `SRC_R76_TDC_ANTIBODYAFF/dataverse-v105/protein_sabdab.csv` 逐行比对：493 行顺序相同，`ID`/序列/抗原三列字符串完全相同，52 行 `Y` 的文本不同但数值差异在 2.2×10⁻¹⁶ 相对误差内。据此判定两表为同一上游数据的两次导出，转入 `Q01` 跟踪。
- 2026-10-29 按 skill 的 PDB 硬性要求，以 493 个 `Antibody_ID` 为锚点从 RCSB 取得 entry FASTA 与 mmCIF。`3RVV`、`3RVW` 返回 404，查询 RCSB `holdings/removed` 确认撤销日期与替代条目。
- 2026-10-29 对比本目录与 R76 目录的 `pdb/`：mmCIF 491 个逐字节相同；FASTA 内容相同但 131 个文件的 entity 顺序不同，故两份 inventory 摘要不同。该差异记录在本 README 而非通过重写文件消除。

## 参考文献

- Zenodo record：<https://zenodo.org/records/13120765>，DOI `10.5281/zenodo.13120765`
- Zenodo concept：<https://doi.org/10.5281/zenodo.13120764>
- 上游数据集（TDC `Protein_SAbDab`）：<https://doi.org/10.7910/DVN/21LKWG>，文件 `protein_sabdab.csv`
- TDC 任务页：<https://tdcommons.ai/multi_pred_tasks/antibodyaff/>
- TDC 代码仓库：<https://github.com/mims-harvard/TDC>
- 上游数据库：Dunbar et al., *SAbDab: the structural antibody database*, Nucleic Acids Research 42(D1):D1140 (2014)，DOI `10.1093/nar/gkt1043`
- 上游数据库更新：Schneider et al., *SAbDab in the age of biotherapeutics*, Nucleic Acids Research 50(D1):D1368 (2022)，DOI `10.1093/nar/gkab1050`
- RCSB 条目：以 <https://www.rcsb.org/structure/1HH6> 为 URL 格式，其余 492 个 ID 见“PDB 数据库”

## 其他

### 数据范围和限制

本数据集是 TDC `Protein_SAbDab` 的一次再导出，内容与 `SRC_R76_TDC_ANTIBODYAFF` 相同。它不提供新测量、不提供筛选脚本、不提供上游映射，因此不能作为独立数据源与 R76 互补或交叉验证。

与 R76 相同，本表只覆盖 SAbDab 中抗原为蛋白或肽的条目，`Y` 不区分测量方法与实验条件，493 行来自 493 个不同 PDB 条目而非同一抗体的重复测量。按抗体序列分组时同一抗体可能出现在多个条目内，随机划分会产生近邻泄漏。

### 完整性与验收

| 文件 | 大小 | MD5（Zenodo 官方） | SHA-256 |
| --- | ---: | --- | --- |
| `antibody_affinity_protein_sabdab.csv` | 320.37 KiB（328,055 bytes） | `6f982caf45f4bfb921a2d759ee41913c` | `1552bb0f4d3055539ad8542fa206fd0bb2e3b0117a57c38df58b5898212e0d0c` |
| `get_antibody_affinity_data.py` | 418 bytes | `588df8db4aa8135d8ad469352b79c74b` | `4c5ca2b11f9dfb5537857f4e778692c2664089caad3433e78bd80d700a2142a9` |

MD5 由 Zenodo record metadata 给出，下载后复核一致；SHA-256 为本地计算。CSV 可正常解析为 493 行 × 5 列，无空值，字段类型与长度范围已逐列统计。Python 脚本为纯文本、418 bytes，内容已逐行核对。

`pdb/` 的 982 个文件与 607,146,339 bytes 已逐文件生成 SHA-256 并折叠为 inventory 摘要；两个缺失锚点的撤销原因已由 RCSB 记录确认。

### 许可和再分发边界

Zenodo record 的 `metadata.license` 为 Apache License 2.0，覆盖本记录的两个文件。Apache 2.0 允许商用与再分发，要求保留版权与许可声明，并对修改标注明示。

该许可由本记录的发布者声明。数据内容源自 SAbDab 经 TDC 处理，上游的许可条件不因本记录改用 Apache 2.0 而失效；TDC 任务页标注 CC BY 3.0、Dataverse dataset 标注 CC0 1.0，SAbDab 自身条款未在本次取得范围内核对。若需对外再分发，应同时遵守上游条款，本 README 不把 Apache 2.0 解释为已覆盖上游内容。

`pdb/` 内的 RCSB 文件适用 RCSB 自身条款。

### 公开范围对照

| 来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| 约 500 个抗体及其 KD | CSV 493 行、493 个不同 `Antibody_ID` | 已包含 |
| 抗体序列、抗原序列、KD | `Antibody`、`Antigen`、`Y` 三列 | 已包含；KD 单位未标注 |
| 通过 TDC 从 SAbDab 取得 | 附带脚本调用 `AntibodyAff(name='Protein_SAbDab')` | 已包含 |
| 数据附带的 Python 取数代码 | `get_antibody_affinity_data.py` | 已包含 |
| 与 TDC 表的独立来源 | 逐行比对显示同一上游、同序、同值 | 未独立；属同一数据 |
| 测量方法、条件、误差 | 未发现 | 未公开 |
| SAbDab 原始记录与筛选过程 | 未发现 | 未公开 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-29；已核实，非缺口的独立性判断）：本表与 `SRC_R76_TDC_ANTIBODYAFF/dataverse-v105/protein_sabdab.csv` 是同一上游的两次导出。已核实 493 行顺序相同、`ID`/序列/抗原三列字符串逐行相同、52 行 `Y` 文本不同但数值相对误差不超过 2.2×10⁻¹⁶、唯一值数 380 对 383 的差额来自浮点文本合并。影响：把 R76 与 R77 当作两个独立来源会重复计入同一批 493 次测量，任何跨来源去重必须把它们视为同一测量身份。当前处理：两个 README 互相声明对应关系，不各自宣称独立性。下一步：无需上游答复；若下游构建统一清单，应按“同一测量身份”合并并在名称层保留两个 source_id 的别名。
- `Q02`（最近更新：2026-10-29；待上游说明）：`Y` 未标注单位与测量类型，取值 4×10⁻¹³—2×10⁻⁴。已核实其数值与 TDC 表逐行等价。影响：不能确认整列为 KD，也不能与 IC50/EC50 混用。当前处理：README 只记录数值与量级，不解释为 KD。下一步：核对 SAbDab 原始 `affinity_type` 字段后关闭。
- `Q03`（最近更新：2026-10-29；待说明）：记录声明 Apache 2.0，但内容源自 TDC 与 SAbDab，上游分别声明 CC BY 3.0 与 CC0 1.0（后者来自 Dataverse dataset 级字段）。已核实三个许可声明各自的页面与字段。影响：对外再分发时适用哪一层条款没有一手说明。当前处理：README 按上游更严格的署名要求执行，不把 Apache 2.0 当作已覆盖上游。下一步：确认发布者是否有权以 Apache 2.0 再许可该内容，或取得 TDC 对文件级许可的说明后关闭。
- `Q04`（最近更新：2026-10-29；信息缺口）：`3RVV`、`3RVW` 于 2022-04-27 被 RCSB 撤销，替代条目为 `5VPL`、`5VPG`，两者本身已在 493 个 ID 内并已取得。已核实 RCSB `holdings/removed` 的 `remove_date` 与 `id_codes_replaced_by`。影响：这 2 行的锚点无法按原 ID 取得，但可通过替代条目追溯。当前处理：保留原 ID 不变，不用替代条目回填文件名。下一步：核对替代条目与原条目的序列是否一致，若一致可在使用阶段建立等价映射。
