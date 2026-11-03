---
tags:
  - context
---

# SRC_R34_ABLIFT 数据说明

## 数据集身份

- `source_id`：`SRC_R34_ABLIFT`
- `source_version`：`snapshot-2019-08-23`
- 原作者或发布机构：Warszawski 等，Weizmann Institute of Science / Fleishman 课题组；FLAb 整理由 Gray Lab 发布

## 实验设计和数据口径

D44.1 是抗 hen egg-white lysozyme 的抗体。研究先用酵母展示与深测序比较结合选择池和表达参考池，按突变相对 WT 的读数频率比计算选择系数，再分析 vL–vH 界面中可容忍或提高结合的单点变体。Methods 定义用于分析的 −ln(S)；S4 标题是 Log-enrichment。富集是受表达、选择门和测序计数影响的实验派生量，不能直接等同热力学 KD。

研究再用 PSSM 与 Rosetta 稳定性评估限定可容忍突变组合，设计 D44.1des、抗 VEGF 的 G6 变体和抗 QSOX1 的 h492.1 变体。D44.1des 的亲和力/稳定性、少数 G6 的 SPR 以及 h492.1 的功能抑制验证是不同实验口径。归一化荧光、Rosetta 能量和酶抑制结果也不能合并为同一 KD 标签。S2 包含 18 个 G6 设计加亲本；S3 包含 20 个 h492.1 设计加亲本；技术读数和共享亲本不能当成独立抗体家族。

论文报告 2,294 个 D44.1 单点突变用于分析；本次 S4 有 115 个位置、2,209 个非空单元格，FLAb 有 2,048 个 VH/VL 单点变体。它们是不同粒度，包含 WT 单元格、缺失和子集选择，不是三个相等的样本数。逐项比对发现全部 FLAb KD 列都匹配 exp(−round(S4 单元格, 2))，fitness 匹配 −log10(KD 列)。因此这 2,048 个 KD 不是新增的逐变体物理测量。该数学关系来自本批比较，未取得 FLAb 的逐步生成记录；不要把对数富集的符号、舍入值或名义 nM 当成可靠的绝对亲和力标定。

## 论文原文

### Warszawski 2019

- 标题：Optimizing antibody affinity and stability by the automated design of the variable light-heavy chain interfaces
- 作者：Shira Warszawski；Aliza Borenstein Katz；Rosalie Lipsh；Lev Khmelnitsky；Gili Ben Nissan；Gabriel Javitt；Orly Dym；Tamar Unger；Orli Knop；Shira Albeck；Ron Diskin；Deborah Fass；Michal Sharon；Sarel J. Fleishman
- 载体与版本：PLoS Computational Biology；published PDF
- 发布日期：2019-08-23
- DOI：[10.1371/journal.pcbi.1007207](https://doi.org/10.1371/journal.pcbi.1007207)
- PMID / PMCID：31442220 / PMC6728052
- 本地文件：`articles/AbLIFT_2019-08-23_EuropePMC-published.xml`；`articles/AbLIFT_2019-08-23_PLOS-published.pdf`
- 文件大小：AbLIFT_2019-08-23_EuropePMC-published.xml：186889 bytes；AbLIFT_2019-08-23_PLOS-published.pdf：2366825 bytes
- SHA-256：AbLIFT_2019-08-23_EuropePMC-published.xml：`fbc7b8eb051ba20ba0a8046b046243c73324b174d0e42644cc772c17c9960a1b`；AbLIFT_2019-08-23_PLOS-published.pdf：`08bd5d3b821004fb86148871cea293b5206be6303758f349f59c5563bc7e74c8`
- 文本许可：CC BY 4.0；第三方内容依其注明条件
- 补充材料：`articles/AbLIFT_2019-08-23_PLOS-S1Fig.tif`；`articles/AbLIFT_2019-08-23_PLOS-S2Fig.tif`；`articles/AbLIFT_2019-08-23_PLOS-S3Fig.tif`；`articles/AbLIFT_2019-08-23_PLOS-S4Fig.tif`；`articles/AbLIFT_2019-08-23_PLOS-S5Fig.tif`；`articles/AbLIFT_2019-08-23_PLOS-S6Fig.tif`；`articles/AbLIFT_2019-08-23_PLOS-S1Protocol.txt`；`articles/AbLIFT_2019-08-23_PLOS-S2Protocol.txt`；`articles/AbLIFT_2019-08-23_PLOS-S3Protocol.txt`；`articles/AbLIFT_2019-08-23_PLOS-S1Text-DNASequences.docx`；`articles/AbLIFT_2019-08-23_PLOS-S2Text-G6IgGSequences.docx`；原始 S1–S4 表位于 `AbLIFT/`，其中 S1 实际重复 S4，见后文

补充材料逐文件身份：

| 文件 | bytes | SHA-256 |
| --- | --- | --- |
| `articles/AbLIFT_2019-08-23_PLOS-S1Fig.tif` | 2154586 | `eb77b525c87b358a0c0a8fef2460cf51890c343b6a74b53d218a55078a6b0444` |
| `articles/AbLIFT_2019-08-23_PLOS-S2Fig.tif` | 794782 | `5f650b7cdb77b73d52714f83b0cc18b1f7f1ebe65c8bd48184ef760323051190` |
| `articles/AbLIFT_2019-08-23_PLOS-S3Fig.tif` | 219136 | `c3295fd8d87d22d509f19e6fbe7e89ff9de36200d19fbfa58ba36dc0f22f6cad` |
| `articles/AbLIFT_2019-08-23_PLOS-S4Fig.tif` | 1137132 | `d38d246bd6b2c1da5cb09eeb2305f76da17139e5ec26561b8cd555a6467342e6` |
| `articles/AbLIFT_2019-08-23_PLOS-S5Fig.tif` | 1377524 | `2ca71d318f8de59ca49b64e81155965d0f957d9c679d2940ece5a151d7241791` |
| `articles/AbLIFT_2019-08-23_PLOS-S6Fig.tif` | 214914 | `d7e2eeeda2ceead524b371ff4b390f2cbc9edc38a1664c1dc595c2cc4f3316ae` |
| `articles/AbLIFT_2019-08-23_PLOS-S1Protocol.txt` | 4818 | `00eb74d1e2a3acd3ec018525d33ff464e00639387c122cf20d4ef9a2f45c93ca` |
| `articles/AbLIFT_2019-08-23_PLOS-S2Protocol.txt` | 3755 | `0b85e20ae9404fabaa1db06905188ed2d82006f6bf1ca50654e5f5ae2e46eca7` |
| `articles/AbLIFT_2019-08-23_PLOS-S3Protocol.txt` | 3225 | `a0a88b12091eb5a805587b62e7ba794852864c0e47458a4afd76a583057e8f8f` |
| `articles/AbLIFT_2019-08-23_PLOS-S1Text-DNASequences.docx` | 13943 | `a33f4e435b36627b244c65a4000357b39d717308bb1ec51df756cba0904eb27e` |
| `articles/AbLIFT_2019-08-23_PLOS-S2Text-G6IgGSequences.docx` | 13057 | `39e9f0e81089765e570e8bbc335f7fcb9d42ccb7251c1cbbcd9c8f7ca0803a20` |

## 仓库内容

一手入口为 PLOS DOI 的四张表和论文补充材料；无数据 release 号，版本 `snapshot-2019-08-23` 取论文公布日期。另保留 FLAb 固定 commit `e05e3f0135783ffb7de412df6a1467e7a0031911` 的一个派生 CSV。这是公开原生表加固定派生表的选择性组合，不是 FLAb 全仓库快照。

```text
snapshot-2019-08-23/
├── AbLIFT/
│   ├── journal.pcbi.1007207.s007.xlsx
│   ├── journal.pcbi.1007207.s008.docx
│   ├── journal.pcbi.1007207.s009.docx
│   └── journal.pcbi.1007207.s010.xlsx
└── FLAb/
    └── warszawski2019_d44_Kd.csv
```

四个附件分别标为 S1–S4；实际 s007 与 s010 内容相同，后文保留这项发布方差异。CSV 是 FLAb 的整理结果。

## 数据结构

### 原生补充表与派生表

S4 的 Sheet1 有三行列头、20 行替换氨基酸及 115 个位置列。vL 为 47 列、vH 为 68 列；未填充的链标题需要沿用前一链标记解释，raw 表本身没有被填充。共有 2209 个非空数值，范围 -4.100742618–10.2006636298593。S2 的一个 Word 表为 19 行 × 14 列；S3 为 21 行 × 14 列。位置名和表头有 NBSP，保持字面值。

PLOS 把 s007 说明为 6GC2 的晶体学统计，但实际下载字节 SHA-256 与 s010 完全相同，解析后同样是上述富集矩阵。保留两份原名文件及差异，不声称取得真正的晶体统计表。FLAb CSV 为 2,048 行 × 6 列，无空值或列宽异常，全部是单点变体。作者另有三份 Rosetta protocol TXT、构建体 DNA DOCX 和 G6/G6des13 蛋白序列 DOCX，作为科学补充归档在 articles；没有执行其中任何流程。

### 字段说明

| 文件 / 原始字段 | 表示、单位与来源 | 缺失、方向与边界 |
| --- | --- | --- |
| S4：三行列头 vL/vH、位置、WT；首列替换氨基酸 | 115 位置 × 20 aa 的原生矩阵；实验派生 Log-enrichment，无量纲 | 空单元格保持缺失；WT 接近零；Methods 的 −ln(S) 与此表的 Log-enrichment 标注不可无核对混用 |
| S2：Position、L A43 … H M107 | 链/亲本氨基酸/作者位置；设计替换身份 | 连字符表示该设计未替换该位点，不能当作序列缺失 |
| S2：Normalized fluorescence [a.u] | 酵母展示归一化荧光；实验汇总 | 该 assay 内较高代表更高归一化结合信号，不等于 KD |
| S2：Total score [R.e.u]；S3：Total score [R.e.u] | Rosetta 计算能量，R.e.u | 计算分数通常较低较有利；不能作为实验亲和力标签 |
| FLAb：heavy、light | 114 aa VH、108 aa VL 变量区字符串，非全长 IgG | 本批全部 2,048 行是单点变体；与 1MLC author numbering 核对 |
| FLAb：KD (nM)、-log10 (KD (M) ) | 上游命名为 KD/pKD 的派生列；不是独立 SPR 测量 | KD 列范围 3.72e-05–60.3402876；单位仅是上游列标注，未证明物理 nM |
| FLAb：fitness、-log(Kd [nM]) | 两列相同，匹配 −log10(KD 列) | 不能依列名忽略与富集矩阵的变换关系；避免标签派生列泄漏 |

### 数据示例

| S4 位置 / 替换 | 原始 Log-enrichment 单元格 |
| --- | --- |
| vL 22 S→R | -1.19990985959298 |
| vH 11 V→I | 0.609740762 |

FLAb 首行的原始值：`KD (nM)=0.5433508691`、`-log10 (KD (M) )=9.264919634`、`fitness=0.2649196339406016`。VH 为 `QVQLQESGAEIMKPGASVKISCKATGYTFSTYWIEWVKQRPGHGLEWIGEILPGSGSTYYNEKFKGKATFTADTSSNTAYMQLSSLTSEDSAVYYCARGDGNYGYWGQGTTLTV`，VL 为 `DIELTQSPATLSVTPGDSVSLSCRASQSISNNLHWYQQKSHESPRLLIKYVSQSSSGIPSRFSGSGSGTDFTLSINSVETEDFGMYFCQQSNSWPRTFGGGTKLEIKR`；依据 1MLC 原始 author numbering，该行是 vH V11I。对应 S4 数值 0.609740762，经两位小数舍入后 exp(−0.61) 匹配该 KD 列，说明此行是富集表的派生表示，不能增加独立实验样本数。

## PDB 数据库

论文及补充中采用 D44.1、G6、492.1 和对照 F10.6.6 的结构。所有单点变体共享亲本参考；6GC2 是游离 D44.1des Fab，并非设计体与 HEL 的复合物。4IJ3 是论文用于设计的 492.1/QSOX1 参考，不能据此声称全部人源化设计具有实测复合物。

获取日期为 2026-09-18。一手入口为 RCSB 的 `https://www.rcsb.org/fasta/entry/<PDB_ID>/download` 与 `https://files.rcsb.org/download/<PDB_ID>.cif.gz`。复用共享缓存时保留其原始 `.cif` 或 `.cif.gz` 字节；缓存未通过身份检查时重新获取。保存完整条目的全部 polymer entities 和完整坐标，不筛链、不拼接变体序列。验证 entry ID、FASTA entity ID、canonical 序列与 mmCIF `_entity_poly.pdbx_seq_one_letter_code_can` 一致，并确认存在原子坐标。

接受 7 个唯一 ID，7 对通过配对检查，14 个已验收文件，共 4161380 bytes。按 `relative_path<TAB>bytes<TAB>sha256<LF>` 排序拼接的 inventory SHA-256：`f8fdaa8a565bf9f6af3d85169149696334f50b327e8d0316a74fb79823ccf333`。PDB 子任务状态为 `verified`。

| PDB | 连接角色及经 entity 描述核对的 author chains |
| --- | --- |
| 1MLC | D44.1/HEL：轻链 A,C；重链 B,D；HEL E,F |
| 1MLB | 游离 D44.1：轻链 A；重链 B |
| 6GC2 | 游离 D44.1des：轻链 L；重链 H |
| 2FJG | G6/VEGF：轻链 L,A；重链 H,B；VEGF V,W |
| 4IJ3 | 492.1/QSOX1：QSOX1 A；轻链 B；重链 C |
| 1P2C | F10.6.6/HEL 对照：轻链 A,D；重链 B,E；HEL C,F |
| 2Q76 | 游离 F10.6.6 对照：轻链 A,C；重链 B,D |

| 原始文件 | bytes | SHA-256 |
| --- | --- | --- |
| `pdb/sequences/rcsb_pdb_1MLB.fasta` | 578 | `bc21cbb5b99c3b5d456ec6b86ea5f671f57423e1fc2fb303b951d94b6b30515c` |
| `pdb/structures/1MLB.cif` | 390615 | `f1190d9327c181baa7987bce0118ebd17408bb5738c44616121e354231fd408f` |
| `pdb/sequences/rcsb_pdb_1MLC.fasta` | 780 | `afed58a819c379d1d70be24c0b782647d45b7736c931fa4d8a9acce0046ed005` |
| `pdb/structures/1MLC.cif` | 921079 | `5536c79a3d73e09503f6a4d252bbca2dac5fa0e59b5424309f49cd0c34e8606e` |
| `pdb/sequences/rcsb_pdb_1P2C.fasta` | 789 | `8a967adb3c0a83d1c5d2d637682296328d5c17d047c8b71b134e4d42392b254a` |
| `pdb/structures/1P2C.cif` | 989717 | `29395c0d93f7238a2fff11e77d5eb0856968cb9780170b9e0e4c9b8c2adf3a3c` |
| `pdb/sequences/rcsb_pdb_2FJG.fasta` | 783 | `1d318ed5770ea6eb19c4472d0f424e0af78ba64648eebb608eecc95b02e85e1f` |
| `pdb/structures/2FJG.cif` | 858207 | `d9778b03d09c63b0f406fabdf1b63e19750163b403a0d9e27c8c4f715ab3544c` |
| `pdb/sequences/rcsb_pdb_2Q76.fasta` | 578 | `4d6d3b28fcddf53479afb4bae8d70d7c22fc435333e1182ab71c364d6e444dba` |
| `pdb/structures/2Q76.cif` | 740437 | `48799059f164aa0c006a34a20b1f758cd47cd82776dec63364d56943f936127a` |
| `pdb/sequences/rcsb_pdb_4IJ3.fasta` | 869 | `ea5d6274235b8fd13660778e590993a47046277aa4df09758dbe7ba238b2d0d2` |
| `pdb/structures/4IJ3.cif.gz` | 154031 | `13eabb3d0ebb8aba55f61aa12132c02d0055f965977bcdee4cc7d8d40d9c70a6` |
| `pdb/sequences/rcsb_pdb_6GC2.fasta` | 593 | `4ec3855f2f1b4cbe0d02748ec922e7b2696a7f075d50b9fb8f72aee677811226` |
| `pdb/structures/6GC2.cif.gz` | 102324 | `b58e71d272143521a011641d26abc3f357200e08397b58a758211b7b4d555293` |

外部条目中的链角色以 entity 描述和 `_entity_poly.pdbx_strand_id` 核对；这里保存全部链。上游表给出的角色链与具体实验序列仍须逐构建体验证，不能用相同 PDB ID 自动推定所有抗体序列或抗原构建体相同。

## 使用方式

```python
import pandas as pd

matrix = pd.read_excel(dataset_root / "AbLIFT/journal.pcbi.1007207.s010.xlsx", header=[0, 1, 2])
flab = pd.read_csv(dataset_root / "FLAb/warszawski2019_d44_Kd.csv")
```

使用调用者指定的 dataset_root；S2/S3 是 DOCX，不能交给 XLSX parser。

## 采集过程记录

1. 2026-09-18，从 PLOS 主文核对 DOI、Supplementary captions、Methods 和结构引用，选择四张原生表及固定 FLAb commit 的相关 CSV，下载进入 staging。
2. 初始把 S2/S3 按 XLSX 命名；实际 ZIP 内含 word/document.xml，结合 PLOS captions 修正为 DOCX。改名前后大小和 SHA-256 保持一致。再次发现 s007 和 s010 的 SHA 完全相同；通过备用参数顺序/DOI 路径重查仍重复，记录发布方附件差异。
3. 归档主文 PDF 与 Europe PMC 同 DOI XML；原始通用名按论文 2019-08-23 日期改为 AbLIFT 开头。补充 s014/s015 最初误作 protocol TXT，实际是 DOCX 的 S1/S2 Text；按 XML captions 和 Office MIME 内容修正扩展名，双端 hash 未变。
4. 逐个解析全部原生表和 FLAb CSV，按 1MLC 亲本 author numbering 比较 2,048 个单点变体，确认 KD 列是舍入后富集值的指数变换。只保存审计证据，没有修改 raw 数值或生成变体参考序列。
5. 为七个唯一 PDB ID 同时取得 canonical FASTA 和完整 mmCIF。旧共享缓存中 1MLC、2FJG 的自定义 FASTA 标题未通过 full-entry 身份检查，保留旧 hash 诊断后从 RCSB 重取；原共享 source 未被修改。重新配对核验全部通过。
6. 工作稿每次生成立即同步 raw README；最终发布器执行固定版本 Markdownlint、字节与白名单复核后才原子移动版本目录。运行记录、状态及交接位于当前开发者的流程与 context 目录。

## 参考文献

- [PLOS 主文及全部补充入口](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007207)
- [固定 FLAb 派生表](https://github.com/Graylab/FLAb/blob/e05e3f0135783ffb7de412df6a1467e7a0031911/data/binding/warszawski2019_d44_Kd.csv)
- [1MLC 原始结构及结构论文](https://www.rcsb.org/structure/1MLC)、[1MLB](https://www.rcsb.org/structure/1MLB)、[6GC2](https://www.rcsb.org/structure/6GC2)
- [2FJG](https://www.rcsb.org/structure/2FJG)、[4IJ3](https://www.rcsb.org/structure/4IJ3)、[1P2C](https://www.rcsb.org/structure/1P2C)、[2Q76](https://www.rcsb.org/structure/2Q76)

## 其他

### 数据范围和限制

公开包目标是四个表的当前公开字节、固定 FLAb 相关表、主文/科学补充和七个 PDB 配对。它不等于完整研究获取：真正的 S1 晶体统计附件未取得，全部仪器原始记录和富集值生成过程未在这些表中交付。

### 完整性与验收

| payload | bytes | SHA-256 |
| --- | --- | --- |
| `AbLIFT/journal.pcbi.1007207.s007.xlsx` | 39940 | `423d572c788eacbb518efbb8c3184c17e8fd1a6c5e54b91f3b982a4ad9a143b8` |
| `AbLIFT/journal.pcbi.1007207.s008.docx` | 18863 | `1d1ce8e4363f10696d01788612d991ac3c7c856a85e825d750ef63c42dafdff4` |
| `AbLIFT/journal.pcbi.1007207.s009.docx` | 19169 | `d4255b896ceb28470d010e79e725c5c584f990446f6c7bba241e4c5f9aa57297` |
| `AbLIFT/journal.pcbi.1007207.s010.xlsx` | 39940 | `423d572c788eacbb518efbb8c3184c17e8fd1a6c5e54b91f3b982a4ad9a143b8` |
| `FLAb/warszawski2019_d44_Kd.csv` | 589041 | `bda66c936962b290bc78a58227e3c9fe3cbb49ce8bcbea5fee044e47f2e7cb8f` |

已取得 payload 共 5 个、706953 bytes；排序拼接的 inventory SHA-256：`67a3b8788e5880a5667b319f04dc0924a9a6699f0708b1633571672376d687cd`。上游未给出 checksum 的交付只将 SHA-256 作为本次字节身份，不能称为官方校验和。归档按成员检查重复/逃逸路径、链接和膨胀范围，逐个读取正规成员；ZIP 校验 CRC，gzip 校验尾部。表格按原始 encoding、header 和列宽检查，保留所有原值。

### 许可和再分发边界

PLOS 论文及其补充材料为 CC BY；FLAb 固定 commit 的 data/README.md 对 Warszawski 2019 条目标明 CC BY 4.0；保留该条目许可及原数据条件。Rosetta 软件依 RosettaCommons 条件，论文可读不授予软件商用许可。PDB 原始条目依 wwPDB/RCSB 数据政策，保留原论文及条目引用。

### 公开范围对照

| 论文或来源声称的内容 | 实际公开文件证据 | 状态 |
| --- | --- | --- |
| D44.1 DMS 2,294 点 | S4 115 位置、2,209 非空单元格；FLAb 2,048 点 | 公开处理表；口径有差异 |
| S1 晶体统计 | s007 下载字节重复 s010 | 真实 S1 待确认 |
| G6/h492.1 设计 | S2 18 设计+亲本；S3 20 设计+亲本 | 公开设计/汇总表 |
| 逐变体 SPR KD | FLAb KD 与 S4 数学变换一致 | 不能宣称已包含 |
| 参考结构 | 七个 full-entry FASTA/mmCIF 配对 | 已核验；非逐变体结构 |
