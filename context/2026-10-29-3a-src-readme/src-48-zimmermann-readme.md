---
tags:
  - context
---

# SRC_R48_ZIMMERMANN 数据说明

## 数据集身份

- `source_id`：`SRC_R48_ZIMMERMANN`
- `source_version`：`snapshot-2026-08-17`
- 原作者或发布机构：Jörg Zimmermann 等、Floyd E. Romesberg、Steven G. Boxer 和 Charles L. Brooks III 等共同作者；PNAS 发表原研究，Graylab/FLAb 提供后续标准化表

### 来源方背景

原研究由 The Scripps Research Institute 化学系、分子生物学系与 Stanford University 化学系合作完成，Floyd E. Romesberg 是通讯作者。Romesberg 团队的公开研究方向包括蛋白质功能进化与光谱学；Steven G. Boxer 是 Stanford 化学教授，其实验室从物理化学角度研究生物系统的结构和功能。两者都是学术机构内的研究团队，公司成立时间、融资、营收和上市状态不适用。本来源的发布关系是“学术团队原研究—PNAS 正式论文及补充材料—FLAb 后续汇编”。

## 实验设计和数据口径

这项研究以抗荧光素抗体 4-4-20 为对象，研究从胚系到成熟抗体的体细胞突变如何改变结合、构象异质性和蛋白质动力学。成熟抗体相对胚系序列含 2 个轻链可变区变化和 10 个重链可变区变化。作者在胚系轻链和成熟轻链两种背景中，分别以成熟重链为基准，再将这 10 个位点逐一回变为胚系残基。

主要的结合实验链可概括为：

```text
2 种 VL 背景 ×（成熟 VH 基准 + 10 个 VH 单点回变）= 22 个拟表征条件
  └─ Fab 表达与纯化
       ├─ 胚系 VL 背景的 P17S、R38C 因表达差未表征
       └─ 余下 20 个条件用 SPR 测荧光素结合
            ├─ 平衡条件得到 KD
            ├─ 动力学条件得到 koff
            └─ 由 koff / KD 计算 kon
```

抗体均以 Fab 形式表达，先经 protein G 亲和层析和阳离子交换纯化。SPR 使用 Biacore 3000，将偶联荧光素的 BSA 固定到 CM5 芯片，再让不同 Fab 浓度流过表面。这是同一类 SPR 实验数据的不同分析：信号先证明是否有可观察结合，平衡响应随浓度的关系用来求 `KD`，解离曲线用来求 `koff`，`kon` 则由两者派生。`KD` 越小通常表示亲和力越强；不结合或信号太弱时通常无法稳定定量拟合，不等于把 `KD` 定义为零。

PNAS Table 1 因此有 22 个位置，其中 2 个用破折号表示未表征，其余 20 个有数值 `KD`。FLAb 将这 20 个序列对与点估计整理成 CSV，又额外重复了 1 条 P17S/成熟 VL 记录，因而是 21 行、20 种唯一序列组合。表中不保留变体名、`kon`、`koff`、测量误差或 sensorgram，不能把每行当成完整的 SPR 原始记录。

**链字段需反向解读：** CSV 的原 `heavy` 字段是 112-aa 轻链可变区，原 `light` 字段才是 118-aa 重链可变区。证据不只是长度推测：两列分别与论文补充序列的 VL/VH 变化模式一致，而成熟背景的原 `heavy` 还与 1FLR author chain L 可变区前缀完全一致。raw 文件保留上游表头，读取时必须显式更正语义。

论文的 3PEPS、DSS、荧光寿命和分子动力学用于回答构象异质性与动力学问题；它们是同一研究的其他表征，不是当前 FLAb `KD` CSV 的新增结合标签。

## 论文原文

### 正式发表版

- 标题：Antibody evolution constrains conformational heterogeneity by tailoring protein dynamics
- 作者：Jörg Zimmermann, Erin L. Oakman, Ian F. Thorpe, Xinghua Shi, Paul Abbyad, Charles L. Brooks III, Steven G. Boxer, Floyd E. Romesberg
- 发表来源：*Proceedings of the National Academy of Sciences* 103(37), 13722–13727 (2006)，Version of Record
- 归档文本版本：共同作者课题组公开的正式版 PDF；与 DOI、题名、卷期和页码一致
- 在线发布日期：2006-09-05；卷期日期：2006-09-12
- DOI：[10.1073/pnas.0603282103](https://doi.org/10.1073/pnas.0603282103)
- PMID / PMCID：16954202 / PMC1564241
- OpenAlex：work `W2132524280`，截至 2026-09-24 引用数 121；该计数会随时间变化
- 本地主文：`articles/Zimmermann_2006-09-05_PNAS-AuthorCopy.pdf`
- 文件大小：1.02 MiB（1,072,547 bytes）；6 页
- SHA-256：`ade3a2dd9b0881e475d3fc520d13a32420f1ad584627801692f49c1044b36279`
- 文本许可：© 2006 National Academy of Sciences of the USA；公开页面和归档副本未标明 CC 许可
- 补充材料：PNAS/PMC 关联的 7 个 PDF 均已取得；它们补充序列、结构示意和光谱/动力学分析，没有另一张可代替正文 Table 1 的 `KD` 原始数据表

| 对象 | 本地文件 | 主要内容 | 大小 | SHA-256 |
| --- | --- | --- | --- | --- |
| Supplementary Figure 5 | `articles/Zimmermann_2006-09-05_PNAS-Supplementary-Figure-5.pdf` | 可变区序列对齐与 Kabat 编号 | 121.52 KiB（124,440 bytes）；1 页 | `ea275d27974abc6beb2a3b35764402e5cba1d9621a40b04e2ed13299ceff2452` |
| Supplementary Figure 6 | `articles/Zimmermann_2006-09-05_PNAS-Supplementary-Figure-6.pdf` | 突变簇结构图与稳态光谱参数 | 539.96 KiB（552,914 bytes）；1 页 | `ea1b7fc4d99e0ceffa052a8c0665d3bb8e89ff4e91588ca1fed50a212e890f71` |
| Supplementary Figure 7 | `articles/Zimmermann_2006-09-05_PNAS-Supplementary-Figure-7.pdf` | 补充光谱/时间分辨图 | 589.92 KiB（604,080 bytes）；1 页 | `4ad6fd57e962a5c9917a58916bed03fac73bbf95d92ba5b5a10ed6f6b5cb52b0` |
| Supplementary Figure 8 | `articles/Zimmermann_2006-09-05_PNAS-Supplementary-Figure-8.pdf` | 补充光谱图，包括正文引用的稳态光谱 | 589.95 KiB（604,105 bytes）；1 页 | `4a305b7fe239ca4b3d94f08e25c039eac967181974a0cf301969867435532c88` |
| Supplementary Table 3 | `articles/Zimmermann_2006-09-05_PNAS-Supplementary-Table-3.pdf` | 单残基能隙波动与动力学拟合 | 25.24 KiB（25,848 bytes）；1 页 | `197edf1f81f73a2f9a175e343b06cfef5a408b85a145f37c3d75a32f381d7b03` |
| Supplementary Table 4 | `articles/Zimmermann_2006-09-05_PNAS-Supplementary-Table-4.pdf` | 稳态光谱与重组能参数 | 21.50 KiB（22,016 bytes）；1 页 | `3a402d3c2824b8a03c127f2d035de49cf9ff29391cc1d972969c6d333642c89b` |
| Supplementary Text | `articles/Zimmermann_2006-09-05_PNAS-Supplementary-Text.pdf` | 平均谐振力常数及 Table 3 参数定义 | 83.59 KiB（85,594 bytes）；2 页 | `24f5b69ab645f7c989f4e6bca16975e3b27da42751928edb7410d1835daba61b` |

## 仓库内容

FLAb 为选择性快照，固定 commit `e05e3f0135783ffb7de412df6a1467e7a0031911`（committer 日期 2026-08-17），只保留与 R48 直接相关的一张结合表，不声称取得完整 FLAb tree。`source_version` 由这个可追溯 commit 日期命名，不是 2006 年实验日期或本次下载日期。

```text
snapshot-2026-08-17/
  FLAb/data/binding/zimmerman2020antibody_4420_kd.csv
```

目录树只列数据 payload。`articles/`、`pdb/` 和 README 是本项目另行保存的论文、结构与版本说明材料，不计入 FLAb payload。上游文件名中的 `zimmerman2020` 与原论文作者拼写 Zimmermann、发表年 2006 不一致；为保持 Git blob 身份，本项目不改名或改写 raw CSV。

## 数据结构

### 文件和记录关系

唯一的 CSV 有 21 行、6 列，共 20 种唯一 VL/VH 序列组合；第 21–22 行是完全相同的额外副本。它不等于 21 个独立设计，也不包含论文中两个因表达差而未表征的胚系 VL 条件。两种轻链背景、共享重链基准和完全重复行都需在数据划分时显式处理。

| 文件 | 数据行 | 唯一序列对 | 唯一 VL | 唯一 VH | 额外整行副本 | 空值 |
| --- | --- | --- | --- | --- | --- | --- |
| `FLAb/data/binding/zimmerman2020antibody_4420_kd.csv` | 21 | 20 | 2 | 18 | 1 | 0 |

序列和数值与一手论文对照后还有两个不应被沉默修复的差异：胚系 VL / VH V84A 的 FLAb `KD` 是 8 µM，PNAS Table 1 是 9 ± 2 µM；12 条成熟 VL 背景记录的实际 VH 线性第 37 位为 S，而论文补充序列与 1FLR 成熟 VH 均为 V，胚系回变为 F。这两点均保留原件并在末节继续跟踪。

### 字段说明

| 文件/表 | 原字段 | 类型、单位、方向与取值 | 含义/限制 |
| --- | --- | --- | --- |
| FLAb binding CSV | `heavy` | 氨基酸字符串，112 aa；2 种值，无缺失或非标准字符 | 字段名与实际链相反；实为 VL，9 行胚系背景、12 行成熟背景 |
| FLAb binding CSV | `light` | 氨基酸字符串，118 aa；18 种值，无缺失或非标准字符 | 字段名与实际链相反；实为 VH，包含基准与单点回变序列 |
| FLAb binding CSV | `KD (microM)` | 浮点，µM，0.03–150；越小通常表示亲和力越强 | 从论文 SPR 平衡 `KD` 整理的点估计；不含论文的 ± 误差 |
| FLAb binding CSV | `KD (M)` | 浮点，M，3e-8–1.5e-4；越小通常表示亲和力越强 | 逐行等于 `KD (microM) × 10^-6`，是单位换算列 |
| FLAb binding CSV | `-log(KD M)` | 浮点，3.823908741–7.522878745；越大表示 `KD` 越小 | 逐行等于 `-log10(KD (M))`，是标签派生列 |
| FLAb binding CSV | `fitness` | 浮点，与 `-log(KD M)` 逐行完全一致 | 派生副本；预测同一 `KD` 时不得当作输入 |

### 数据示例

| 真实文件/位置 | 实际值摘录 | 解释范围 |
| --- | --- | --- |
| CSV 第 2 行 | `KD (microM)=150`，`KD (M)=0.00015`，`-log(KD M)=fitness=3.823908741` | 原 `heavy` 112 aa（实为 VL）；原 `light` 118 aa（实为 VH） |
| CSV 第 21–22 行 | 两行全部 6 个字段完全一致；`KD (microM)=0.18` | P17S / 成熟 VL 的一个额外整行副本 |

示例只用于说明真实布局，未在文档中重复展开完整序列。建模时应从原 CSV 读取，将 `-log(KD M)` 和 `fitness` 视为 `KD` 的派生表示，避免标签泄漏。

## PDB 数据库

本来源只接受 `1FLR` 作为共享的成熟 4-4-20 Fab–fluorescein 参考结构。PNAS 正文 reference 34 是 Whitlow 等 1995 年论文，与 RCSB 1FLR primary citation DOI `10.1093/protein/8.8.749` 一致，因此这一连接不是仅凭抗体名称推测。论文也明确说明，胚系复合物是从 1FLR 把 12 个体细胞突变改回胚系残基后建模、能量最小化得到，并不是另一个通过实验测得的 PDB 结构。

| RCSB entry | 参考用途 | polymer entity 与链映射 |
| --- | --- | --- |
| [1FLR](https://www.rcsb.org/structure/1FLR) | 成熟 4-4-20 共享参考；不是每个回变体的实验结构 | entity 1: label A / author L，219 aa；entity 2: label B / author H，219 aa |

已取得 1 个原始 FASTA（602 B（602 bytes），SHA-256 `484ed8c75e21c1093302d306ab2f0f16459864b28fdb7e249451fbebd799a5a8`）和 1 个完整 mmCIF（423.92 KiB（434,097 bytes），SHA-256 `3523749d0d6fd1367a96cb878659b00457abc88a7659e00c1ea87f6d6f345157`），坐标中的小分子配体也原样保留。路径分别是 `pdb/sequences/rcsb_pdb_1FLR.fasta` 和 `pdb/structures/1FLR.cif`；mmCIF 仅对 RCSB `.cif.gz` 无损解压，没有重序列化。

PDB 子集 inventory SHA-256：`8cd25c5860fb5a9bb5a20fe64d4e2c48d1ebd3cf83d1c200f595f0ecce8ba7ea`。最终验收已重新执行修正参数顺序后的配对脚本，逐 polymer entity 核对 FASTA 与 mmCIF canonical sequence，并检查 entry identity、坐标和链引用。本项目没有 CDR graft、补环、生成回变体或把同一结构按 CSV 行复制。

## 使用方式

CSV 使用 UTF-8 和原表头。下面示例保留 raw 字段，但在内存中显式把实际链角色改成 `vl`/`vh`；不要在 raw 目录交换列或覆盖原文件。

```python
import csv
from pathlib import Path

path = Path(dataset_root) / "FLAb/data/binding/zimmerman2020antibody_4420_kd.csv"
with path.open(encoding="utf-8-sig", newline="") as stream:
    raw_rows = list(csv.DictReader(stream))
rows = [{**row, "vl": row["heavy"], "vh": row["light"]} for row in raw_rows]
```

进行序列分组、突变标注或模型分割前，还应显式去除或标识那一条完全重复记录，并审查末节记录的 V84A 数值差异与 VH 序列差异。

## 采集过程记录

2026-09-18：固定 FLAb commit `e05e3f0135783ffb7de412df6a1467e7a0031911`，对所选 Git blob 进行 bytes、blob SHA-1 和本地 SHA-256 核对后，将 CSV 按原字节写入共享 staging。从共同作者 Boxer Lab 公开目录取得 6 页正式版主文；PDF 内嵌字体将 DOI 斜线抽取为特殊 glyph，只在身份比对时做映射，原 PDF 没有重写。

2026-09-18：根据正文 reference 34 与 RCSB primary citation 建立 1FLR 连接，取得原始 FASTA 与完整 mmCIF。独立 PDB 审计曾因 `verify_pair` 参数顺序传错而失败；调用修正后已对 R48 重跑完整配对验证，本次最终审计也再次通过。

2026-09-19：从 PNAS 正式页面固定 7 个补充对象的 publisher 原名和 PMC 镜像名。当时 publisher/PMC 直接请求为 403、TLS EOF 或超时，PMC OA 批量分发也没有该文章包，因此未保存任何错误响应。

2026-09-24：按 PMC 公开文件页的 SHA-256 browser proof-of-work 流程完成验证，从 `/articles/instance/1564241/bin/` 依次取得全部 7 个 PDF。每个对象均通过 PDF 头、页数、bytes 和 SHA-256 验证，未修复或重写原文件。

2026-09-24：读取主文全部 6 页与补充材料全部 8 页，再将 CSV 的所有序列、`KD` 和派生列与 PNAS Table 1、补充序列、1FLR 逐项核对。由此确认链字段反转、21 行中的 1 条额外完全副本、V84A 的 8/9 µM 差异和 VH 线性第 37 位差异。完成全包 hash/格式/PDB 审计后，按定义范围发布本地 `processed-public` 快照；未凭公开可访问状态推断对外再分发许可。

| 归档本地路径 | 上游原名 | 大小 | 原字节 SHA-256 |
| --- | --- | --- | --- |
| `FLAb/data/binding/zimmerman2020antibody_4420_kd.csv` | zimmerman2020antibody_4420_kd.csv | 5.60 KiB（5,737 bytes） | `e5745a0cddd395621887d9dcab041d57686cef92b3f2039d00e7f54663d11295` |
| `articles/Zimmermann_2006-09-05_PNAS-AuthorCopy.pdf` | 4006c9_cbc865e499924875bb84191b3b6df30e.pdf | 1.02 MiB（1,072,547 bytes） | `ade3a2dd9b0881e475d3fc520d13a32420f1ad584627801692f49c1044b36279` |
| `articles/Zimmermann_2006-09-05_PNAS-Supplementary-Figure-5.pdf` | 03282fig5.pdf | 121.52 KiB（124,440 bytes） | `ea275d27974abc6beb2a3b35764402e5cba1d9621a40b04e2ed13299ceff2452` |
| `articles/Zimmermann_2006-09-05_PNAS-Supplementary-Figure-6.pdf` | 03282fig6.pdf | 539.96 KiB（552,914 bytes） | `ea1b7fc4d99e0ceffa052a8c0665d3bb8e89ff4e91588ca1fed50a212e890f71` |
| `articles/Zimmermann_2006-09-05_PNAS-Supplementary-Figure-7.pdf` | 03282fig7.pdf | 589.92 KiB（604,080 bytes） | `4ad6fd57e962a5c9917a58916bed03fac73bbf95d92ba5b5a10ed6f6b5cb52b0` |
| `articles/Zimmermann_2006-09-05_PNAS-Supplementary-Figure-8.pdf` | 03282fig8.pdf | 589.95 KiB（604,105 bytes） | `4a305b7fe239ca4b3d94f08e25c039eac967181974a0cf301969867435532c88` |
| `articles/Zimmermann_2006-09-05_PNAS-Supplementary-Table-3.pdf` | 03282table3.pdf | 25.24 KiB（25,848 bytes） | `197edf1f81f73a2f9a175e343b06cfef5a408b85a145f37c3d75a32f381d7b03` |
| `articles/Zimmermann_2006-09-05_PNAS-Supplementary-Table-4.pdf` | 03282table4.pdf | 21.50 KiB（22,016 bytes） | `3a402d3c2824b8a03c127f2d035de49cf9ff29391cc1d972969c6d333642c89b` |
| `articles/Zimmermann_2006-09-05_PNAS-Supplementary-Text.pdf` | 03282suptext.pdf | 83.59 KiB（85,594 bytes） | `24f5b69ab645f7c989f4e6bca16975e3b27da42751928edb7410d1835daba61b` |

## 参考文献

- [PNAS 正式论文与补充材料](https://doi.org/10.1073/pnas.0603282103)。
- [PMC 全文记录](https://pmc.ncbi.nlm.nih.gov/articles/PMC1564241/)。
- [FLAb 固定版本](https://github.com/Graylab/FLAb/tree/e05e3f0135783ffb7de412df6a1467e7a0031911)。
- [Boxer Lab 公开论文目录](https://www.boxerlab.stanford.edu/miscellaneous)。
- [Boxer Lab 官方研究介绍](https://www.boxerlab.stanford.edu/)。
- [Scripps 的 Floyd Romesberg 研究背景](https://www.scripps.edu/faculty/romesberg/)。
- [OpenAlex work W2132524280](https://openalex.org/W2132524280)。
- [RCSB 1FLR](https://www.rcsb.org/structure/1FLR)。
- [1FLR 原始结构论文](https://doi.org/10.1093/protein/8.8.749)。

使用时应同时引用原始 PNAS 论文与实际使用的 FLAb 固定版本；使用结构时再保留 1FLR 原论文引用，不要只引后续汇编表。

## 其他

### 数据范围和限制

当前版本是 `processed-public` 组合快照：数据 payload 是 FLAb 从论文 `KD` 整理的 1 张 CSV，论文归档包含主文和全部 7 个公开补充 PDF，结构归档包含成熟共享参考 1FLR。完整快照不表示取得未公开的 SPR sensorgram、逐浓度响应、独立 replicate、表达产量或全部 MD 轨迹。

### 完整性与验收

独立验收全部 11 个文件（不含 README），共 3.37 MiB（3,531,980 bytes）；inventory SHA-256 `d0f3fdee5c36c28ce79c57fa0ee1a8e3579a71b2b5b6833c7c70ebe3b05502ec`。规则是将每个文件记为 `relative_path<TAB>bytes<TAB>sha256<LF>`，按路径排序后再取 hash；README 排除，没有意外文件。CSV 全部记录和全部派生关系、PDF 全部页、PDB 两层序列/坐标配对均已读取验证。hash 只固定原件身份，不代替科学含义或许可核验。

源目录只保留 payload、`articles/`、`pdb/` 和 README，不发布 API JSON、manifest 或审计报告。派生审计、脚本和交接文档保留在开发者 workspace；真实数据与结构文件不进入 Git。

### 许可和再分发边界

PNAS 主文与补充材料标注 © 2006 National Academy of Sciences，未标明 CC 许可；FLAb 对该表的 metadata 也没有给出可识别的原数据许可。“可公开读取”不等于已获得对外再分发或商业使用授权。按本项目现行规则，许可未特别说明不阻止将可访问原件作为本地研究快照发布，但必须保留此不确定性，不宣称已获原作者再分发许可。RCSB 文件另按其数据库条款使用。

### 公开范围对照

| 论文或来源内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| FLAb 标准化 `KD` CSV | 21 行、20 种唯一序列对、1 个额外整行副本；Git blob/SHA-256 一致 | 取得 |
| PNAS 正式主文 | 6 页共同作者公开副本，DOI/作者/卷期/页码核验 | 取得 |
| PNAS 补充材料 | Figure 5–8、Table 3–4、Supplementary Text 共 7 PDF，全部页/hash 核验 | 全部取得 |
| 一手 SPR 完整底层输出 | FLAb 仅保留 KD 点估计；未公开 sensorgram/逐浓度数据 | 不在当前公开交付中 |
| 共享成熟参考结构 | 1FLR FASTA + 完整 mmCIF，一手引文建立连接 | 取得；非逐变体覆盖 |
| 原数据使用/再分发条款 | PNAS © 2006 NAS；FLAb metadata 未给出可识别数据许可 | 未特别说明；已记录 |

## 待解决问题与处理进展

- Q01：原研究数据与 FLAb 所选 CSV 未附可识别的数据许可；本项目可作本地 processed-public 研究快照，但对外再分发或商业使用需另行确认。
- Q02：FLAb 中对应 germline-VL / VH V84A 的 KD 为 8 µM，而 PNAS Table 1 为 9 ± 2 µM；已保留两个上游原值，待来源维护者确认。
- Q03：FLAb 的 12 条 mature-VL-context 记录在原 `light` 字段（实际 VH）的线性第 37 位为 S，而论文补充序列与 1FLR 成熟 VH 为 V、胚系回变为 F；原表不改写，待 FLAb 维护者确认。

上述项均不阻止已定义的本地研究快照，但会影响对外授权表述或单条数据的精确解读。关闭条件分别是：取得原数据所有者的明确条款；由论文/FLAb 维护者确认 V84A 点估计和成熟 VH 线性第 37 位序列。未取得新证据前，raw 文件不做改值或改序列。
