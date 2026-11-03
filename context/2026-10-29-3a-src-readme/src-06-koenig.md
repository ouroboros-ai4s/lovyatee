# SRC_R06_KOENIG 数据说明

- [数据集身份](#数据集身份)
  - [来源方背景](#来源方背景)
- [实验设计和数据口径](#实验设计和数据口径)
- [论文原文](#论文原文)
- [仓库内容](#仓库内容)
- [数据结构](#数据结构)
  - [FLAb binding 表](#flab-binding-表)
  - [FLAb expression 表](#flab-expression-表)
  - [FLAb 来源说明](#flab-来源说明)
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

- `source_id`：`SRC_R06_KOENIG`
- `source_version`：`snapshot-2026-08-17`
- 原作者或发布机构：Genentech 抗体工程团队（Patrick Koenig 等）；FLAb 整理由 Johns Hopkins University Gray Lab 发布

### 来源方背景

[Koenig 等人的原论文](https://pmc.ncbi.nlm.nih.gov/articles/PMC5278476/)出自 Genentech 抗体工程与研发团队。Genentech 于 1976 年在美国南旧金山创立，2009 年成为[罗氏集团成员](https://www.gene.com/about-us)；其美国总部亦承担罗氏在美国的制药业务总部职能。[2026 年公司概况](https://www.gene.com/download/pdf/Genentech-Fact-Sheet_April-2026.pdf)列出约 12,100 名美国员工，可见其研发与药物业务的规模。

Genentech 是早期将重组 DNA 技术用于药物开发的生物技术公司；其[公司历史回顾](https://www.gene.com/media/news-features/25th-anniversary-of-first-product-approval)列出首个获批的肿瘤治疗性抗体等研发里程碑。[Genentech 抗体工程介绍](https://www.gene.com/stories/engineering-therapeutic-antibodies)展示了该部门持续从事抗体结构和功能工程的背景。本版本所用的 FLAb 整理表另由 [Johns Hopkins University Gray Lab](https://r2.graylab.jhu.edu/flab) 发布，两方分别承担原研究与二次汇编角色。

## 实验设计和数据口径

原研究以高亲和力抗 VEGF 抗体 G6.31 Fab 为对象，分别对重链可变区 Kabat 2–113 位和轻链可变区 Kabat 2–107 位构建单点 NNK 饱和突变库。变体以 M13 噬菌体展示；未筛选库和经 anti-gD、protein A、protein L 或 VEGF 筛选的库接受 MiSeq 双端测序。每个突变的 enrichment ratio（ER）由筛选后频率除以筛选前频率得到，聚合了表达、折叠稳定性和配体结合等影响。

VEGF 筛选依次使用 5、0.5 和 0.1 nM 生物素化 VEGF 提高选择压力。论文用 anti-gD 筛选的 ER 代表稳定表达，用 VEGF 筛选的 ER 描述抗原结合景观。ER 是高通量筛选代理值，不是平衡解离常数。论文只从景观中选择少量 Fab 表达纯化，再用 Biacore T200 测定 SPR 动力学和 `K_d`；这些少量验证不能扩展为全库逐变体 SPR。

本 source 保存 FLAb 的两个整理表。两表各有 4,275 行、4,275 个唯一重轻链序列对，序列对集合完全相同；其中重链有 2,262 种，轻链有 2,015 种。FLAb inventory 写作 4,276，是把表头计入了行数。binding 表把每行表示为 `KD` 及其对数变换，expression 表保存 ER。FLAb 没有给出全量 binding 表从原始筛选结果到 `KD` 的逐行转换链，而论文也没有对 4,275 个变体逐一做 SPR。因此：

- expression 表可以作为局部单点突变的筛选代理信号使用，但仍需保留具体筛选语境。
- binding 表是 FLAb 的派生表示；在转换依据被独立证明前，不得把 4,275 行写成 4,275 次 SPR 测量，也不应用于绝对亲和力回归。
- 两表中的行共享同一 G6.31 parent，随机按行拆分会把极相近的单点突变分到训练集和测试集。
- `fitness` 的有利方向均为数值越大越好；这只是 FLAb 的建模方向约定，不消除实验与派生标签的差别。

## 论文原文

- 标题：Mutational landscape of antibody variable domains reveals a switch modulating the interdomain conformational dynamics and antigen binding
- 作者：Patrick Koenig、Chingwei V. Lee、Benjamin T. Walters、Vasantharajan Janakiraman、Jeremy Stinson、Thomas W. Patapoff、Germaine Fuh
- 发表来源：Proceedings of the National Academy of Sciences 114(4):E486–E495
- 归档文本版本：PMC 收录的作者手稿全文（HTML）
- 发布日期：2017-01-05（在线）；2017-01-24（印刷卷期）
- DOI：10.1073/pnas.1613231114
- PMID / PMCID：PMID 28057863；PMCID PMC5278476
- 本地文件：`articles/Koenig_2017-01-05_PMC-author-manuscript.html`
- 文件大小：247.28 KiB（253,216 bytes）
- SHA-256：`f76da997fd6239a3d88d869500df95ee405b435eb7e17a3573db3226782204c2`
- 文本许可：PMC 页面与 Crossref 未给出可据以授权数据再分发的明确许可；按未知处理
- 补充材料：未发现 PMC 可独立归档的机器可读 supplement；正文链接到 PNAS supplemental 页面，但当前命令行入口不可稳定取得
- 引用数（查询快照）：119（[OpenAlex W2570949719](https://openalex.org/W2570949719)，查询于 2026-09-21）

PMC 的 PDF 端点会向命令行客户端返回浏览器校验页。本 source 保存经 DOI、标题和正文段落核验的完整 HTML 作者手稿，没有把 1.77 KiB（1,817 bytes）的挑战页误存为 PDF。PDF 是同一正文的另一载体，当前数据解释不依赖补取它；PNAS supplemental 可能包含筛选和标签方法，仍单独追踪。HTML 引用的站外样式和图片不视为本地归档内容。

## 仓库内容

上游为 Gray Lab 的 FLAb GitHub 仓库，固定 commit 为 `e05e3f0135783ffb7de412df6a1467e7a0031911`，commit 日期 2026-08-17，因此版本名为 `snapshot-2026-08-17`。`FLAb/` 是选择性 commit 快照：只保留 Koenig 的两张数据表、解释它们所需的上游 README、上游 metadata 与 LICENSE 指针，不包含 FLAb 的其他研究、模型和评分产物。每个文件按固定 commit 的 Git blob SHA-1 和字节数验收。

```text
snapshot-2026-08-17/
└── FLAb/
    ├── LICENSE
    ├── README.md
    └── data/
        ├── README.md
        ├── binding/
        │   ├── README.md
        │   └── koenig2017mutational_kd_g6.csv
        ├── expression/
        │   ├── README.md
        │   └── koenig2017mutational_er_g6.csv
        ├── flab_metadata.csv
        └── flab_metadata.json
```

两张 CSV 是本 source 的数据 payload。目录 README 记录 FLAb 对 assay、规模和有利方向的声明；`flab_metadata.csv` 与 `flab_metadata.json` 是上游仓库自带的集合级索引，不是本项目生成的旁路 metadata。FLAb payload 共 9 个文件、2.46 MiB（2,580,723 bytes）。

## 数据结构

### FLAb binding 表

`FLAb/data/binding/koenig2017mutational_kd_g6.csv` 有 4,275 个数据行和 7 列，大小 1.24 MiB（1,296,731 bytes），SHA-256 为 `6c1aa637b32cd781d4100411e8f4f71324eab8df480ba7bce490b66dc89d4ff1`。每行是一个完整 G6.31 Fv 重轻链序列对及 FLAb 给出的派生 binding 数值。`KD (nM)` 范围为 0.0006943370987–60.0878083；全列都是有限正数，没有缺失值或失败状态。这种“全覆盖有限值”与论文只对少量候选做 SPR 的实验口径冲突，是禁止把全表当作逐条实测 `K_d` 的直接证据。

表内变换彼此一致：`KD (M) = KD (nM) × 10^-9`，`-ln(KD (nM) )` 使用自然对数，`-log( KD (M) )` 使用十进对数，`fitness` 等于 `-log( KD (M) )`。这些代数一致性只能证明列内转换正确，不能证明原始 `KD` 的实验来源。

### FLAb expression 表

`FLAb/data/expression/koenig2017mutational_er_g6.csv` 有 4,275 个数据行和 4 列，大小 1.04 MiB（1,093,769 bytes），SHA-256 为 `7ec320e663f01f1bfeee9c62eb2520d602a11e3cf12d8ca93a714e89ccb48e4f`。`enrichment ratio` 范围为 0.0009765625–3.177780504，无缺失或非有限值；`fitness` 与 ER 逐行相同。FLAb 把该表归为 Expression [ER]，但没有在该文件中保存筛选轮次、配体、原始 read counts 或重复身份。

### FLAb 来源说明

`data/binding/README.md` 将 binding 表描述为 Fv、G6.31–VEGF、`-log(Kd [M])` 且数值越大越有利。`data/expression/README.md` 将 expression 表描述为 G6.31 的 Expression [ER]。集合级 `data/README.md` 的 Koenig 行没有填写 license；JSON metadata 同样写作 `license: none`。这些上游说明原样保存，但 README 中的行数 4,276 包含表头，且 assay 简称不能覆盖论文方法的细粒度边界。

### 字段说明

| 文件 | 字段 | 原始表示 | 单位与方向 | 来源与限制 |
| --- | --- | --- | --- | --- |
| binding | `heavy` | 120-aa 字符串 | 无单位 | 完整重链可变区；2,262 种 |
| binding | `light` | 108-aa 字符串 | 无单位 | 完整轻链可变区；2,015 种 |
| binding | `-ln(KD (nM) )` | 十进制浮点文本 | 越大越有利 | `KD (nM)` 的负自然对数；FLAb 派生 |
| binding | `KD (nM)` | 十进制浮点文本 | nM，越小越有利 | FLAb 给出的全量派生值；不可等同逐行 SPR |
| binding | `KD (M)` | 十进制浮点文本 | M，越小越有利 | `KD (nM) × 10^-9` |
| binding | `-log( KD (M) )` | 十进制浮点文本 | 越大越有利 | `KD (M)` 的负十进对数 |
| binding | `fitness` | 十进制浮点文本 | 越大越有利 | 等于 `-log( KD (M) )` |
| expression | `heavy` | 120-aa 字符串 | 无单位 | 与 binding 表使用同一重链集合 |
| expression | `light` | 108-aa 字符串 | 无单位 | 与 binding 表使用同一轻链集合 |
| expression | `enrichment ratio` | 十进制浮点文本 | 无单位，越大越有利 | 高通量筛选代理值；FLAb 未保留原始 read counts |
| expression | `fitness` | 十进制浮点文本 | 越大越有利 | 等于 `enrichment ratio` |

两表均没有空字段、文本失败码或显式检测边界列。缺少失败状态不表示所有变体都得到可靠的定量亲和力。

### 数据示例

两表首行对应同一个真实序列对。为避免把派生列误认成独立测量，以下按原始字段分别摘录：

| 文件 | `heavy` | `light` | 主要原始数值 |
| --- | --- | --- | --- |
| binding | `EAQLVESGGGLVQPGGSLRLSCAASGFTISDYWIHWVRQAPGKGLEWVAGITPAGGYTYYADSVKGRFTISADTSKNTAYLQMNSLRAEDTAVYYCARFVFFLPYAMDYWGQGTLVTVSS` | `DIQMTQSPSSLSASVGDRVTITCRASQDVSTAVAWYQQKPGKAPKLLIYSASFLYSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQSYTTPPTFGQGTKVEIKR` | `KD (nM)=3.620217946`；`fitness=8.441265283` |
| expression | 同上 | 同上 | `enrichment ratio=0.8196785911`；`fitness=0.8196785911` |

每行代表共享 G6.31 parent 上的一个重轻链变体表示，不是新的独立抗体谱系，也不对应一份独立实验复合物结构。

## PDB 数据库

论文明确用 PDB 2FJG 的 G6 Fab–VEGF 晶体复合物解释突变位置，也在 Results、Fig. 3 和 Fig. S6 引用 2FJF。RCSB 将 2FJF 标为游离 G6 Fab，只有抗体重轻链；它不是另一份 G6–VEGF 复合物。2FJG 本 source 选取同一复合物副本中的 author chain A（Fab light，214 aa）、B（Fab heavy，227 aa）和 V（VEGF-A，102 aa），同时保存三条 canonical sequence 和完整 deposited mmCIF。逐链实例与 mmCIF 坐标记录确认三条 author chain 分别对应 label asym E、F、A。

| 连接对象 | PDB | 映射强度 | FASTA | FASTA SHA-256 | mmCIF | mmCIF SHA-256 |
| --- | --- | --- | --- | --- | --- | --- |
| G6–VEGF parent reference | 2FJG | 全数据共享参考，不是逐行结构 | `pdb/sequences/rcsb_pdb_2FJG.fasta`，789 bytes | `fb9219fe8f09d2db510dbf0a94c6a4518ab7ec420a6af64db5aa524f4ab461f5` | `pdb/structures/2FJG.cif`，838.09 KiB（858,207 bytes） | `d9778b03d09c63b0f406fabdf1b63e19750163b403a0d9e27c8c4f715ab3544c` |
| 游离 G6 Fab parent reference | 2FJF | 论文引用的游离亲本结构；entry/entity 级，不指定晶体副本 | `pdb/sequences/rcsb_pdb_2FJF.fasta`，693 bytes | `1f4408cd96013232e3f249271bb570ae2c74f42cc1a8c560ce16338c755ffa2f` | `pdb/structures/2FJF.cif`，3.80 MiB（3,980,639 bytes） | `a04b9fab61fe93cbd7579cf4f3395e045efd0b54bd7db45a8d620e09b95a736e` |

2FJG 和 2FJF 的抗体都是 G6；论文说明 G6.31 相对 G6 有四处 CDR-L3 替换。因此两种结构只能作为亲本构象与位点解释锚点，不能声称与 4,275 个变体逐条序列完全一致。2FJG FASTA 由 RCSB canonical 序列和项目角色 header 生成；2FJF FASTA 则保留 RCSB 完整 entry 原始字节，含重轻链两个 entity，不选择论文未指定的晶体副本。两份 mmCIF 均保留 RCSB 下载字节。

## 采集过程记录

- 2026-09-18：从新版资源清单确认 R06、论文 DOI、FLAb 文件名和 PDB 2FJG。读取 `project.toml` 得到共享存储根。Windows context 工具因把 Unix 路径判为非绝对路径而失败；未修改项目配置。
- 2026-09-18：核验 FLAb `main` 为 commit `e05e3f0135783ffb7de412df6a1467e7a0031911`，commit 日期 2026-08-17；读取 commit tree，锁定 9 个 payload blob 的路径、Git SHA-1 和字节数。
- 2026-09-18：第一次在 ab02 使用完整 `git clone --no-checkout`。传输到约 748 MB 时发生 `GnuTLS recv error (-9)`、`early EOF` 和 `index-pack failed`。失败缓存没有进入共享 source；确认精确路径后清理 `/data/ab02/yangwuyu/work/r06-koenig/git-cache/FLAb`。
- 2026-09-18：改为从固定 commit 的 `raw.githubusercontent.com` 逐个取得 9 个选定 blob，下载量约 2.6 MB；逐文件重新计算 Git blob SHA-1 和字节数，与 commit tree 完全一致。
- 2026-09-18：PMC PDF 入口在命令行返回 1.77 KiB（1,817 bytes）的浏览器挑战页，浏览器自动化接口又没有可用实例。改为归档 PMC 作者手稿全文 HTML，并核对 DOI、标题、正文和 247.28 KiB（253,216 bytes）的文件身份；挑战页未发布。
- 2026-09-18：用通用 PDB 工具从 RCSB 获取 2FJG 的三链 FASTA 与完整 mmCIF；工具独立核对 entry、polymer entity、author/label chain 和 FASTA sequence。
- 2026-09-18：读取两张 CSV，核对字段、4,275 行、4,275 个唯一序列对、两表序列集合、数值有限性和列间代数关系；保留“FLAb binding 全表不是逐条 SPR”的证据冲突。
- 2026-09-18：完成 README 后同步回 staging，执行 Python 验证、markdownlint、顶层残留检查和本地/远端 README SHA-256 比对；全部通过后再从 `.staging` 原子发布。
- 2026-09-22：用 RCSB 逐链实例与已存 mmCIF 复核 2FJG，修正 FASTA header 中轻链 `A` 的 label asym `C` 为 `E`、重链 `B` 的 label asym `D` 为 `F`。三条 canonical 序列正文和 mmCIF 字节保持原样；重新计算 FASTA SHA-256 并核对本地与共享 README。
- 2026-09-22：按在线发布日期与实际归档载体，将 PMC 作者手稿 HTML 从 `Koenig_2017_PNAS_PMC5278476.html` 改名为 `Koenig_2017-01-05_PMC-author-manuscript.html`；文件字节数和 SHA-256 未变，下载与验收脚本同步更新。
- 2026-10-08：从归档论文的 2FJF 引文与 RCSB 条目确认游离 G6 Fab 角色；补取 RCSB 完整 entry FASTA 和 mmCIF，分别核对 2 个 polymer entity、坐标解析、字节数与 SHA-256。未推断论文使用的具体晶体副本；原有 2FJG 和 FLAb payload 字节不变。
- 2026-10-08：复跑正式目录验证器，9 个 FLAb 文件、两张各 4,275 行的 CSV、论文 HTML 与两对 PDB 文件均通过。检查 FLAb Git 历史，binding 表于 2025-08-06 以文件上传进入仓库，已查版本中没有该表的逐行 `KD` 生成脚本。区分正文 PDF 与可能影响方法解释的补充材料，前者不再作为本次获取目标。

## 参考文献

- Koenig P, et al. Mutational landscape of antibody variable domains reveals a switch modulating the interdomain conformational dynamics and antigen binding. PNAS. 2017. <https://doi.org/10.1073/pnas.1613231114>
- PMC 作者手稿全文：<https://pmc.ncbi.nlm.nih.gov/articles/PMC5278476/>
- Gray Lab FLAb 固定 commit：<https://github.com/Graylab/FLAb/tree/e05e3f0135783ffb7de412df6a1467e7a0031911>
- FLAb Koenig binding 表：<https://github.com/Graylab/FLAb/blob/e05e3f0135783ffb7de412df6a1467e7a0031911/data/binding/koenig2017mutational_kd_g6.csv>
- RCSB PDB 2FJG：<https://www.rcsb.org/structure/2FJG>
- RCSB PDB 2FJF：<https://www.rcsb.org/structure/2FJF>
- Fuh G, et al. Structure-function studies of two synthetic anti-vascular endothelial growth factor Fabs and comparison with the Avastin Fab. J Biol Chem. 2006. <https://doi.org/10.1074/jbc.M507783200>

## 其他

### 数据范围和限制

本 source 是 FLAb 对 Koenig 研究的选择性整理快照，不含原始 MiSeq reads、逐轮 read counts、全部配体选择矩阵、PNAS supplemental 文件或 FLAb 的其余 240 个数据集。G6.31 单点突变景观适合研究同一 parent 周围的局部变化，不代表新抗体或新抗原上的泛化能力。

### 完整性与验收

- 顶层合同：`FLAb/`、`pdb/`、`articles/`、`README.md`，无额外 manifest、metadata 目录或验证报告。
- FLAb payload：9 个文件、2.46 MiB（2,580,723 bytes）；路径、大小和 Git blob SHA-1 与固定 commit tree 一致。
- 数据表：binding 与 expression 各 4,275 行；序列对各 4,275 个且集合相同；字段、有限值和派生关系通过独立验证。
- 论文与 PDB：文章 HTML 247.28 KiB（253,216 bytes）；2 个 PDB 锚点各有 1 个 FASTA 和 1 个完整 mmCIF，2FJG 为三条选链记录，2FJF 为两条原始 entity 记录。
- README：markdownlint 为 `0 error(s)`；发布后本地与远端 SHA-256 必须一致。

### 许可和再分发边界

FLAb 顶层 LICENSE 只要求查看每个 dataset 的来源许可；`data/README.md` 的 Koenig license 单元格为空，JSON metadata 写作 `none`。上游未特别说明覆盖这两张整理表的许可，使用与再分发范围不明确；论文可读及 RCSB 可下载不能代替数据许可。未发现与本项目公开包保存明确冲突的条款，此未决项本身不阻塞当前接入验收，但不构成商业使用、衍生物发布或对外再分发授权。上述用途须向原作者或 FLAb 维护方确认；引用保留 Koenig 论文、FLAb 固定 commit、PDB 2FJG 与 2FJF 来源。

### 公开范围对照

| 论文或来源声称的内容 | 当前文件证据 | 状态 |
| --- | --- | --- |
| G6.31 全可变区单点突变的筛选景观 | FLAb expression 表有 4,275 个唯一序列对和 ER | 已取得整理表示；缺原始 reads、轮次和重复 |
| 少量入选 Fab 的 SPR 与稳定性验证 | PMC 正文描述 Biacore 与 DSF | 已取得正文；没有独立机器可读验证表 |
| FLAb 的 Koenig binding benchmark | binding 表有 4,275 行全量有限 `KD` 派生列 | 已取得，但逐行实验来源未证明 |
| G6–VEGF 参考结构 | RCSB 2FJG FASTA 与完整 mmCIF | 已取得；仅共享 parent reference |
| 游离 G6 Fab 参考结构 | RCSB 2FJF FASTA 与完整 mmCIF | 已取得；entry/entity 级 parent reference |
| 论文正文与 supplemental | 已归档作者手稿全文 HTML；PNAS supplemental 入口返回交互挑战 | 正文已取得；补充方法材料待获取。另一种正文 PDF 载体不在本次目标范围 |

## 待解决问题与处理进展

- `Q01`（最近更新：2026-10-08；待 FLAb 维护方说明）：FLAb binding 表的 4,275 行均有有限 `KD`，原论文只对少量候选做 SPR。已核对论文实验方法、原表、列间代数变换及 Git 历史；该表以文件上传进入仓库，已查版本没有逐行生成脚本。目前按来源不明的派生标签保存，不视为逐行实测亲和力。取得原始筛选量到全量 `KD` 的转换方法和可核对的逐行依据后，才决定是否用于定量亲和力建模。
- `Q02`（最近更新：2026-10-08；非阻塞，待权利方说明）：FLAb 的 Koenig 数据许可字段为空或 `none`。已核对上游 LICENSE 指针和固定 commit，未发现与当前公开包接入明确冲突的条款；许可未说明不阻塞本项目接入，但不授权商业使用、衍生物发布或对外再分发。上述用途前须取得两张整理表的明确授权范围，并保存一手答复。
- `Q03`（最近更新：2026-10-08；补充材料待获取）：PNAS supplemental 可能解释筛选和标签形成方法，但期刊入口返回浏览器挑战，PMC 作者手稿 HTML 没有独立可归档的补充文件。当前只按已核实的正文与 CSV 解释数据；取得可验证的官方补充文件并核对其方法内容后关闭。正文 PDF 是另一载体，本次不再单独追索。
