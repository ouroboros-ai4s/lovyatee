---
tags:
  - conclusion
---

# Antigen Sequence and Structure Cleaning Problem Inventory

## time

2026-11-01

## lineage

- 3a_src_data_etl_modeling.md: current MVP model for the processed Ab-Ag pair dataset.
- ../3a-src-inventory/src-03-abdesign-1-0.md: direct antigen sequence with reference-PDB provenance.
- ../3a-src-inventory/src-08-avida-htnfa.md: fixed TNF-alpha target with direct sequence.
- ../3a-src-inventory/src-09-flab.md: mixed fixed targets and AbRank antigen sequences.
- ../3a-src-inventory/src-10-abrank.md: direct antigen sequences with PDB anchors.
- ../3a-src-inventory/src-11-abbibench.md: benchmark-level reference antigens reconstructed from structures.
- ../3a-src-inventory/src-12-asd-agab-db.md: large source-native antigen sequence collection.
- ../3a-src-inventory/src-13-andd.md: direct sequences, multi-chain separators, and missing values.
- ../3a-src-inventory/src-14-ab-bind.md: parent-PDB antigen entities without row-level sequences.
- ../3a-src-inventory/src-15-skempi-2-0.md: multi-chain partner antigens and reference structures.
- ../3a-src-inventory/src-16-guest.md: single-chain and multi-chain antigens reconstructed from PDB/FASTA.
- ../3a-src-inventory/src-20-sabdab-sabdab2.md: structure-chain antigens, NA chains, and non-protein entities.
- ../3a-src-inventory/src-23-mit-ll-alphaseq.md: fixed 14-aa peptide target without row-level antigen fields.
- ../3a-src-inventory/src-50-graphinity.md: antigen chains reconstructed from structure-linked FASTA.
- ../3a-src-inventory/src-74-abdesign-2-0.md: fixed PD-1 target derived from a reference structure.
- ../3a-src-inventory/src-75-her2-aff-large-buzz.md: fixed HER2 extracellular-domain target.
- ../3a-src-inventory/src-76-tdc-antibodyaff.md: direct source-native antigen sequences and entity names.
- ../3a-src-inventory/src-77-akbar-sabdab-kd-csv.md: direct source-native antigen sequences and duplicate source snapshot.
- ../3a-src-inventory/src-78-mochibind-sampled-data.md: four fixed antigen constructs with direct sequences.
- ../3a-src-inventory/src-79-alphabind.md: fixed campaign-level antigen constructs without bundled sequences.
- ../3a-src-inventory/src-80-antipasti.md: PDB-chain antigen recovery with unresolved NA/non-protein entities.

## relation

None.

## description

### 问题

这份记录从完整的 AI-native ETL 工作流列出 20 个 SRC 的抗原侧问题。核心任务是：从每条 affinity 实验的来源语境中恢复一个可用于 `3A` 的实验抗原对象，再将其统一为 `antigen = (AG_ID, sequence: list[FASTA], structure, lineage)`。下面按工作流中的决策节点组织问题，不把工具解析步骤单独当成问题。

1. **实验抗原对象如何从来源语境中确定**：每条记录需要先回答“这次实验实际测量的抗原是什么”。
    - 逐行直接序列、活动级固定目标、结构引用和外部说明如何汇合为同一个候选对象。
    - 抗原名称、assay 描述、construct 名称和参考结构不一致时，哪个代表实验对象。
    - 参考复合物中的伙伴蛋白、辅助分子或结构载体如何与真正的 assay antigen 区分。
    - 只有名称或活动上下文、没有逐行序列时，如何提出可追溯的候选。

2. **候选序列和结构如何被 AI-native workflow 恢复**：来源可能直接给序列，也可能只给 PDB、FASTA、accession 或文献线索。
    - 候选检索范围、母本查找、结构链读取和外部数据库映射如何编排。
    - 来源序列、来源 FASTA、PDB/mmCIF canonical/SEQRES、observed structure sequence 的证据顺序如何确定。
    - 结构缺口、未解析端点、缺失文件或多条同样成立的候选如何处理。
    - AI 负责检索和提出候选，哪些步骤必须由确定性序列比对和结构检查完成。

3. **实验构建体的真实边界如何重建**：同一名称可能指向全长蛋白、成熟蛋白、胞外域、结构域、短肽或表达构建体。
    - signal peptide、propeptide、成熟链和实验截短边界如何从来源证据中恢复。
    - His-tag、Fc、GST、MBP、linker、biotin 标签及其他融合载体如何与目标抗原分离。
    - 结构链只覆盖构建体一部分时，如何对应到实验实际使用的片段。
    - 边界无法唯一确定时，保留哪些候选信息，何时停止恢复。

4. **单链、多链和非蛋白抗原如何形成一个对象**：20 个 SRC 同时出现单链蛋白、寡聚体、多链伙伴、短肽以及 DNA/RNA/小分子等实体。
    - 多链抗原（如 `gp120+CD4`、三聚体）是一个 antigen 还是多个 antigen，链顺序如何固定。
    - 同一复合物中的辅助链、结构伙伴和真正参与结合的抗原如何区分。
    - 多链边界如何同时反映在 sequence、structure 和 AG_ID 输入中。
    - 短肽是否按正常 antigen sequence 保留，非蛋白实体是否进入本轮产物。

5. **WT、parent、突变体和实验状态如何恢复**：抗原可能直接给出实验变体，也可能只给 parent 与突变描述。
    - 完整变体序列存在时如何优先使用并保留状态信息。
    - parent、链身份、编号体系、位置和残基信息足够时如何唯一重建。
    - 如何判定 mutation 属于 antigen，而不是 antibody 或其他复合物伙伴。
    - 状态不能唯一重建时，如何结束候选链并处理该 affinity 记录。

6. **来源、序列和结构冲突时如何裁决**：恢复结果必须同时符合实验语境和可验证的分子证据。
    - assay 明确构建体、来源直接序列、结构链和外部数据库冲突时的证据优先级。
    - 序列一致但结构只覆盖部分片段，或结构一致但来源序列包含表达附件时如何判定。
    - 候选之间如何通过编号、长度、比对覆盖、实体类型和结构映射收敛到唯一结果。
    - 无法收敛时保留原始记录，但不生成不确定的 processed antigen。

7. **最终 antigen 表示和身份如何统一**：输出必须能直接挂入既有的 `3A` 模型。
    - 清洗后的实验片段作为 `sequence`，可用结构作为 `structure`，缺失结构使用 `None`。
    - 多链分隔符、未知残基、短肽和序列空白如何形成稳定的 canonical sequence。
    - `AG_ID = hash(canonical_sequence_list)` 的输入边界如何固定，避免名称、结构或来源差异改变同一序列的身份。
    - 序列无法恢复但结构存在、或结构无法获得但序列可靠时，是否允许分别保留。

8. **跨源合并和 lineage 如何使结果可复现**：同一实验、同一序列和同一结构可能在多个 SRC 或快照中重复出现。
    - 同序列异名、同名异序列、同一结构多条链和同源数据快照如何合并。
    - 同一个 AG_ID 下如何保留多个结构引用、实验构建体和 source provenance。
    - lineage 如何记录来源定位、候选检索、边界裁剪、链选择、变体重建、冲突裁决、工具版本和最终 hash。
    - 任何 `None`、排除或未恢复状态如何留下足够信息，使后续 workflow 能重新处理。

相关 20 个 inventory：

- [R03 AbDesign 1.0](../2026-10-30-3a-src-inventory/src-03-abdesign-1-0-inventory.md)
- [R08 AVIDa-hTNFa](../2026-10-30-3a-src-inventory/src-08-avida-htnfa-inventory.md)
- [R09 FLAb](../2026-10-30-3a-src-inventory/src-09-flab-inventory.md)
- [R10 AbRank](../2026-10-30-3a-src-inventory/src-10-abrank-inventory.md)
- [R11 AbBiBench](../2026-10-30-3a-src-inventory/src-11-abbibench-inventory.md)
- [R12 ASD / AgAb DB](../2026-10-30-3a-src-inventory/src-12-asd-agab-db-inventory.md)
- [R13 ANDD](../2026-10-30-3a-src-inventory/src-13-andd-inventory.md)
- [R14 AB-Bind](../2026-10-30-3a-src-inventory/src-14-ab-bind-inventory.md)
- [R15 SKEMPI 2.0](../2026-10-30-3a-src-inventory/src-15-skempi-2-0-inventory.md)
- [R16 Guest antibody benchmark](../2026-10-30-3a-src-inventory/src-16-guest-inventory.md)
- [R20 SAbDab / SAbDab2](../2026-10-30-3a-src-inventory/src-20-sabdab-sabdab2-inventory.md)
- [R23 MIT-LL AlphaSeq](../2026-10-30-3a-src-inventory/src-23-mit-ll-alphaseq-inventory.md)
- [R50 Graphinity](../2026-10-30-3a-src-inventory/src-50-graphinity-inventory.md)
- [R74 AbDesign 2.0](../2026-10-30-3a-src-inventory/src-74-abdesign-2-0-inventory.md)
- [R75 HER2-aff-large / Buzz](../2026-10-30-3a-src-inventory/src-75-her2-aff-large-buzz-inventory.md)
- [R76 TDC AntibodyAff](../2026-10-30-3a-src-inventory/src-76-tdc-antibodyaff-inventory.md)
- [R77 Akbar SAbDab Kd CSV](../2026-10-30-3a-src-inventory/src-77-akbar-sabdab-kd-csv-inventory.md)
- [R78 MochiBind sampled data](../2026-10-30-3a-src-inventory/src-78-mochibind-sampled-data-inventory.md)
- [R79 AlphaBind public experiments](../2026-10-30-3a-src-inventory/src-79-alphabind-inventory.md)
- [R80 ANTIPASTI](../2026-10-30-3a-src-inventory/src-80-antipasti-inventory.md)

### 方案

#### 1. 实验抗原对象如何从来源语境中确定

本项的目标是把每条 affinity 记录绑定到“这次实验实际使用的抗原对象”。它先确定对象身份和来源定位，再把候选交给第 2 项“候选序列和结构如何被 AI-native workflow 恢复”以及第 3 项“实验构建体的真实边界如何重建”。这两个组件完成后，才允许生成最终的 `antigen = (AG_ID, sequence, structure, lineage)`；本项不提前凭名称生成序列，也不把参考结构自动当作实验抗原。

已确定的裁决原则是：AI 只能从 SRC 的字段、metadata、README、结构标识和其他明确来源线索中检索、抽取、整理和交叉核验；不得凭名称相似、常识、长度或模型判断补写来源没有给出的对象、序列或边界。证据无法把记录唯一绑定到实验抗原时，直接排除，不生成 processed antigen。

```latex
\begin{algorithm}[H]
\caption{Experimental Antigen Object Resolution}
\label{alg:antigen-object-resolution}
\KwIn{affinity record $r$; source files and metadata $M$; optional PDB/accession references}
\KwOut{resolved antigen context $c$ or exclusion status; lineage string $L$}

\tcp{The AI may extract and cross-reference explicit source evidence only.}
$C \leftarrow$ collect explicit antigen/target/construct fields from $r$
\If{$C = \varnothing$}{
    $C \leftarrow$ collect the fixed target inherited from the table/activity/benchmark context in $M$
}
\If{$C = \varnothing$}{
    $C \leftarrow$ collect source-specified PDB, chain, partner, UniProt or accession candidates
}
\If{$C$ contains no unique candidate tied to $r$}{
    record the source locator and exclusion reason in $L$;
    \Return{exclude}
}

$c \leftarrow$ bind the unique source-supported candidate to $r$;
$c \leftarrow$ pass $c$ to sequence/structure recovery (Component 2) and construct-boundary recovery (Component 3);
\If{either component cannot determine a unique result}{
    record the unresolved evidence and reason in $L$;
    \Return{exclude}
}
\Return{$c$, $L$}
\end{algorithm}
```

#### 1.1 记录上下文先于抗原字段

- 每条 affinity 记录先保留 `SRC_ID`、原始文件、表名、活动或实验批次、原始行号/记录 ID，以及可用的 accession、PDB_ID、样本 ID。
- 这些字段组成该记录的实验上下文。抗原对象的判断必须在这个上下文内完成，不能脱离表名、活动说明或复合物身份单独读取一个名称。
- 同一个 SRC 内存在多个表、多个活动或多个参考结构时，记录只能继承自己所属上下文的抗原定义，不能把同源数据的目标扩散到其他记录。

#### 1.2 三类来源分支

| 来源分支 | 适用情形 | 对象确定方式 |
| --- | --- | --- |
| 逐行直接提供抗原 | 记录已有 `antigen sequence`、`Ag_name`、`Ag_ID`、construct 或等价字段，例如 R03、R10、R12、R13、R76、R77 | 读取该行的 source-native antigen 信息，并保留行级定位；序列规范化和构建体边界交给第 2、3 项 |
| 活动/表级固定目标 | 大量 antibody 只针对少数固定抗原，例如 R08、R23、R74、R75、R78、R79，以及 R09、R11 中的固定目标或参考复合物 | 从 README、metadata、表名、活动说明或 benchmark metadata 确定目标，再将目标继承到同一活动或表中的 affinity 记录 |
| PDB/结构复合物定义 | 记录只给 PDB_ID、chain、partner、accession 或结构实体，例如 R14、R15、R16、R20、R50、R80；R03、R11 也可能以参考结构补充对象定位 | 根据来源指定的复合物和链/partner 关系识别抗体侧以外的实验抗原候选，再由第 2 项恢复序列和结构，由第 3 项确定实际构建体片段 |

三类分支是同一 workflow 的不同入口，不是三套互不相容的方案。一个 SRC 内混合多种形态时，按记录上下文逐条分流；混合来源不新增字段，也不改变最终 `antigen` 模型。

#### 1.3 抗原对象候选的确定顺序

对每条记录按以下顺序搜集证据：

1. 先读取该 affinity 记录自身的 antigen/target/construct 字段。
2. 没有逐行字段时，读取该记录所属活动、表、实验批次或 benchmark metadata 的固定目标。
3. 仍没有明确目标时，解析来源给出的 PDB_ID、chain、partner、UniProt 或其他 accession，识别与 antibody 配对的非抗体候选。
4. 只有名称或文献语境时，使用来源 README、论文说明和数据包 metadata 建立可追溯候选；候选必须能回指到具体记录上下文。
5. 任何候选都要保留其来源定位、对象名称/实体标识、链或 partner 定义，以及它与 affinity 记录的绑定理由。

这里的“顺序”是候选发现顺序。若不同证据之间出现序列、结构或构建体边界冲突，本项不擅自覆盖，转交第 6 项“来源、序列和结构冲突时如何裁决”；在冲突未解决前不生成 processed antigen。

#### 1.4 AI-native workflow 与确定性收敛

- AI 只负责从 README、metadata、表格说明、论文语境和结构标识中抽取明确线索、建立来源引用和整理候选；它不对缺失信息作主观推断。
- 确定性步骤负责读取明确字段、按活动上下文继承目标、解析 chain/partner 关系、校验候选是否回指原始记录，并把唯一候选交给第 2、3 项组件。
- AI 不能凭空补写抗原序列，不能仅凭“HER2”“PD-1”等名称选择任意数据库序列，也不能把复合物中的辅助蛋白、表达载体、配体、DNA/RNA 或离子自动认定为 assay antigen。
- 一个记录只有在抗原对象唯一、来源定位可复现、且后续序列/边界组件能够继续处理时，才进入 processed dataset。无法唯一确定的记录留在原始数据源，不复制进产物。

#### 1.5 与第 2、3 项组件的接口

本项向后续组件传递的只是可追溯的候选对象上下文：来源定位、候选名称或 entity、PDB/accession、chain/partner、活动继承关系和判断理由。它不是最终新增的数据字段；最终仍只落入既定的 `sequence`、`structure` 和 `lineage`。

- 第 2 项根据候选上下文寻找 source-native sequence、随包 FASTA、PDB/mmCIF、UniProt 或其他可靠序列来源，并恢复结构引用。
- 第 3 项根据 assay construct、成熟蛋白、表达标签、结构覆盖和来源边界，把候选恢复到实验实际使用的抗原片段。
- 第 2、3 项任一项无法收敛时，当前记录不生成 `AG_ID`，也不生成 `3A`；原始 affinity 记录仍保留在来源数据中。

#### 1.6 `lineage` 记录要求

每个最终抗原的 `lineage` 至少记录：

- `SRC_ID`、原始文件/表/活动、行号或记录 ID；
- 使用的来源分支：逐行字段、活动/表级固定目标，或 PDB/结构复合物；
- 原始 antigen name、target、construct、PDB_ID、accession、chain/partner 等定位信息；
- 若发生上下文继承，记录继承自哪个活动、表或 metadata 条目；
- 第 2、3 项使用的候选来源、结构/序列映射、边界处理和最终判定；
- 候选冲突、未恢复、排除或 `None` 的原因。

示例：`SRC-15 / skempi_v2.csv / PDB=1XYZ / Protein-2=gp120+CD4；由 accession 与 partner 字段确定为抗体侧实验伙伴；序列由 PDB chain A/B 恢复；构建体边界由组件 3 判定；结果进入 processed antigen。`

#### 2. 候选序列和结构如何被 AI-native workflow 恢复（多模块集合）

本项接收第 1 项已经唯一绑定的抗原候选，目标是从来源证据中恢复一条可复现的 sequence，并尽可能绑定对应 structure。它不根据抗原名称生成序列，不把相似蛋白或任意数据库命中当作来源证据。

```latex
\begin{algorithm}[H]
\caption{Antigen Sequence and Structure Recovery}
\label{alg:antigen-sequence-structure-recovery}
\KwIn{resolved antigen context $c$; source files and metadata $M$; local and explicitly referenced external records}
\KwOut{ordered sequence list $S$; optional overall structure $p$; evidence lineage $L$ or exclusion status}

$E \leftarrow$ collect sequence and structure evidence explicitly linked to $c$;
$E \leftarrow E \cup$ source-native row/target sequence and construct metadata;
$E \leftarrow E \cup$ bundled FASTA, PDB/mmCIF and local structure snapshots;
$E \leftarrow E \cup$ explicitly referenced UniProt/accession records;

\If{the candidate is found only by an unlinked name or semantic similarity}{
    record the missing source link in $L$; \Return{exclude}
}
$S \leftarrow$ normalize, compare and order the candidate chain sequences in $E$;
$P \leftarrow$ map the selected chain set to the overall structure candidate in $E$;
\If{$S$ has no unique source-supported ordered chain list}{
    record all candidates and the unresolved reason in $L$; \Return{exclude}
}
$S \leftarrow$ select the unique ordered chain list supported by the source context;
$p \leftarrow$ retain the mapped overall structure/complex, or set $p = \mathrm{None}$ when structure evidence is absent;
record every source locator, mapping, comparison and tool version in $L$;
\Return{$S$, $p$, $L$}
\end{algorithm}
```

该集合包含四个入口模块：逐行 source-native sequence、活动/表级固定目标、随包 FASTA/结构文件、以及来源明确引用的 PDB/mmCIF 或 UniProt/accession。AI 只负责从这些入口检索和整理明确线索；序列比对、chain/entity 映射、长度和覆盖检查负责确定性收敛。结构可以缺失并记录为 `None`，但 sequence 必须能够唯一恢复，否则记录不进入 processed dataset。恢复结果统一为有序链序列列表 `S`；单链是单元素列表，多链保留每条链，结构保留为对应的整体结构或复合物。

#### 3. 实验构建体的真实边界如何重建（多模块集合）

本项接收第 2 项恢复的候选 sequence/structure，目标是去掉不属于 assay 实际抗原的部分，保留实验使用的构建体片段。输出不是数据库 canonical 全长，而是来源能够确定的实验片段。

```latex
\begin{algorithm}[H]
\caption{Experimental Antigen Construct-Boundary Recovery}
\label{alg:antigen-construct-boundary-recovery}
\KwIn{recovered ordered sequence list $S$; optional overall structure $p$; antigen context $c$; source metadata $M$}
\KwOut{bounded experimental sequence list $S^\ast$; overall structure $p^\ast$ or exclusion status; lineage string $L$}

$B \leftarrow$ collect explicit assay/construct boundaries from $c$ and $M$;
$B \leftarrow B \cup$ source-described mature chain, domain, peptide or expression construct boundaries;
$B \leftarrow B \cup$ deterministic sequence annotations for signal peptide, propeptide, tags, fusion partners and linkers;
$B \leftarrow B \cup$ structure entity, chain, residue-number and observed-coverage boundaries from $p$;

$B^\ast \leftarrow$ retain only boundaries tied to the experimental antigen and supported by reproducible evidence;
\If{$B^\ast$ is not unique}{
    record the competing boundaries and evidence in $L$; \Return{exclude}
}
$S^\ast \leftarrow$ trim each chain sequence in $S$ to $B^\ast$;
$p^\ast \leftarrow$ retain the overall structure mapped to the bounded chain set, or set $p^\ast = \mathrm{None}$;
\If{the trim cannot be reproduced from the recorded boundary}{
    record the failure in $L$; \Return{exclude}
}
record the boundary, removed regions, evidence, mapping and tool versions in $L$;
\Return{$S^\ast$, $p^\ast$, $L$}
\end{algorithm}
```

该集合包含来源边界、成熟链/结构域边界、信号肽和 propeptide 边界、表达标签或融合载体边界、以及结构覆盖交叉验证模块。任何裁剪都必须有来源描述或可复现的确定性证据；AI 不能凭经验猜测 signal peptide、tag、成熟链或实验片段的边界。边界无法唯一确定时直接排除，并在 `lineage` 中记录原始序列、候选边界、被移除的区段、证据和失败原因。

#### 4. 单链、多链和非蛋白抗原如何形成一个对象（多模块集合）

本轮保留四类 protein antigen：单链蛋白/片段、同源多聚体、异源多链蛋白复合物和短肽。DNA/RNA、配体、离子及其他非蛋白实体不进入 processed dataset。多链抗原仍是一个 `antigen` 对象，链集合用有序 `sequence: list[FASTA]` 保存；单链和短肽也是长度为 1 的列表。`structure` 保存该链集合对应的整体结构或复合物结构，不 list 化；没有结构时为 `None`。

```latex
\begin{algorithm}[H]
\caption{Antigen Chain-Set Object Formation}
\label{alg:antigen-chain-set-object}
\KwIn{bounded protein-chain candidates $C$; optional overall structure $p$; source context $c$}
\KwOut{antigen object $(AG\_ID, S, p, L)$ or exclusion status}

$C \leftarrow$ retain only protein chains explicitly tied to the experimental antigen;
\If{$C = \varnothing$ or $C$ contains DNA/RNA, ligand, ion or other non-protein entity}{
    record the exclusion reason in $L$; \Return{exclude}
}
$O \leftarrow$ order chains by source order, then structure entity/chain order, then stable chain-ID order;
\If{$O$ is not uniquely determined}{
    record competing chain sets/orderings in $L$; \Return{exclude}
}
$S \leftarrow$ assemble the bounded FASTA sequence for each chain in $O$;
\If{any chain sequence or its membership in the experimental antigen is unresolved}{
    record the unresolved chain and evidence in $L$; \Return{exclude}
}
$p \leftarrow$ retain the overall structure/complex mapped to $O$, or set $p = \mathrm{None}$;
$AG\_ID \leftarrow$ hash(canonical serialization of $S$);
record chain IDs, chain order, sequence/structure mapping and exclusions in $L$;
\Return{$(AG\_ID, S, p, L)$}
\end{algorithm}
```

AI 只负责抽取、检索、整理和交叉核验来源线索，不得因为名称相似、常识或模型判断而补入链。链集合或顺序无法确定时排除；结构可以缺失，但不能用不确定的结构替代已确定的链集合。

#### 5. WT、parent、突变体和实验状态如何恢复

本项复用抗体序列清洗文档[第 9 项](3a_src_data_etl_problem_ab.md)，但将重建粒度改为抗原的有序链序列列表 `sequence: list[FASTA]`。目标是恢复 affinity 记录实际使用的 WT、parent 或 mutant 抗原；不能从名称、相似性、长度或结构自行推断未给出的状态。

```latex
\begin{algorithm}[H]
\caption{WT/Parent/Mutation Antigen Sequence Recovery}
\label{alg:antigen-mutation-sequence-recovery}
\KwIn{resolved antigen context $c$; source record $r$; ordered antigen-chain candidates $S$; optional structure $p$}
\KwOut{experimental sequence list $S^\ast$; structure $p$ or exclusion status; lineage string $L$}

Preserve the raw state fields, mutation text, source locator, parent reference,
chain/entity identifiers and raw sequence hashes in $L$.

\eIf{the source provides a complete experimental antigen sequence list}{
    $S^\ast \leftarrow$ normalize the provided sequences in source order;
    classify the record as A;
}{
    \eIf{the source provides a parent sequence and a complete mutation description}{
        classify the record as B;
        determine the mutated antigen entity and chain scope;
        parse each mutation into original residue, new residue, numbering system
        and position;
        enumerate only source-supported chain/numbering mappings;
        apply all mutations to the corresponding parent-chain sequences;
    }{
        classify the record as C; record the exact missing evidence in $L$;
        \Return{exclude}
    }
}

\If{the experimental WT/parent/mutant state is not explicitly bound to $r$}{
    record the unresolved state in $L$; \Return{exclude}
}
\If{the selected mapping is not unique, an original residue disagrees, or any
mutation cannot be applied exactly}{
    record all candidates and the failure in $L$; \Return{exclude}
}
\If{a structure $p$ exists}{
    use it only to cross-check chain identity, residue mapping and sequence edits;
    do not use it to invent a missing parent, mutation or experimental state;
}
validate sequence characters, chain count, chain order, mutation application and
the available independent source/structure evidence;
record class A/B, raw mutation, state, chain scope, parent and mutant hashes,
selected mapping, applied edits, validation results and tool versions in $L$;
\Return{$S^\ast$, $p$, $L$}
\end{algorithm}
```

处理口径固定如下：

- **A 类**：来源直接给出实验使用的完整 WT、parent 或 mutant 序列。直接使用；突变字段和状态字段只进入 `lineage`，不再次改写序列。
- **B 类**：来源给出 parent 与可完整解析的 mutation。先确认 mutation 属于 antigen 而不是 antibody 或复合物伙伴，再按链身份和编号体系逐链重建。多链抗原必须明确 mutation 作用于指定链、全部同源链或来源明确的链集合。
- **C 类**：缺少 parent、链身份、编号体系、位置、原始残基、新残基或实验状态，或存在多个同样成立的映射。保留原始记录，排除出 processed dataset。
- $S^\ast$ 始终保持问题 4 定义的有序 `list[FASTA]`；单链或短肽是长度为 1 的列表，多链 mutation 只修改对应链。
- `structure` 保留问题 4 定义的整体结构或复合物结构，可为 `None`；结构只作交叉验证。
- `lineage` 必须记录原始状态、mutation 文本、抗原实体和链范围、parent/结果序列 hash、编号体系、每次编辑、验证证据、工具版本及排除原因，保证可以复现。

#### 6. 来源、序列和结构冲突时如何裁决

本项复用第 5 项的确定性恢复方式，将冲突处理统一为“证据分级、逐链比较、唯一结果收敛”。输入仍是问题 4 定义的有序抗原链序列列表 `S` 和整体结构 `p`；不新增数据字段，也不因结构覆盖范围改变 `sequence` 的链集合。

证据优先级固定为：

1. assay 或 construct 明确声明的实验状态、实验片段和 source-native sequence。
2. 来源明确关联的 FASTA，或由 parent + mutation 唯一重建的实验序列。
3. 来源明确关联的 PDB/mmCIF canonical sequence 或 SEQRES。
4. PDB/mmCIF 中实际观察到的结构序列。
5. 仅有明确 accession/PDB 关联时才允许使用的外部数据库记录。

名称相似、普通数据库搜索结果和模型常识不构成证据。第 3 项负责处理表达标签、融合蛋白和成熟链边界；第 5 项负责处理 WT、parent、mutant 状态；第 6 项只裁决这些结果之间的证据冲突。

```latex
\begin{algorithm}[H]
\caption{Antigen Source--Sequence--Structure Conflict Resolution}
\label{alg:antigen-conflict-resolution}
\KwIn{antigen context $c$; candidate sequence lists $S_i$; optional structures $p_j$; boundary result $S^\ast$; lineage $L$}
\KwOut{selected sequence list $S^\dagger$; selected structure $p^\dagger$ or exclusion status; updated lineage $L$}

$E \leftarrow$ collect only source-linked assay, sequence, mutation and structure evidence;
rank every evidence item by the fixed priority order;
normalize every candidate into the chain order fixed by Problem 4;

\If{the experimental construct, state or chain set is not uniquely identified}{
    record all candidates and the unresolved source context in $L$;
    \Return{exclude}
}

\ForEach{chain position shared by candidate sequences}{
    compare residues, numbering and coverage across evidence levels;
    \If{a higher-priority candidate conflicts with a lower-priority candidate}{
        retain the higher-priority candidate;
        record both values, the overlap, the difference and the reason in $L$;
    }
    \If{same-priority evidence conflicts, or no priority rule selects one candidate}{
        record the competing candidates and exact conflict in $L$;
        \Return{exclude}
    }
}

\If{a structure covers only part of a selected sequence}{
    compare only the observed overlap;
    retain the complete selected sequence and record uncovered residues in $L$;
}
\If{a source-linked full sequence conflicts with structure sequence}{
    retain the source-linked sequence;
    retain the structure as evidence and record the mismatch in $L$;
}
\If{the boundary result $S^\ast$ or mutation result is not reproducible}{
    record the failed boundary/state reconstruction in $L$;
    \Return{exclude}
}

$S^\dagger \leftarrow$ selected bounded sequence list in the fixed chain order;
$p^\dagger \leftarrow$ mapped overall structure or $\mathrm{None}$;
record evidence ranks, chain mappings, residue comparisons, coverage, conflicts,
decision, source locators and tool versions in $L$;
\Return{$S^\dagger$, $p^\dagger$, $L$}
\end{algorithm}
```

最终口径：

- 结构不完整时，结构只验证重叠残基，不能把完整实验序列截成 observed fragment。
- source-native 实验序列与结构不一致时，保留实验序列；结构仍可保存，但冲突必须进入 `lineage`。
- 同级来源互相冲突，或不同证据无法唯一收敛时，保留原始记录但不生成 processed antigen。
- 多链抗原逐链比较，链集合和顺序沿用问题 4；structure 始终保存整体结构或复合物结构。
- `AG_ID` 只对最终裁决后的 $S^\dagger$ 计算；名称、结构、来源和冲突状态不进入 hash。
- `lineage` 记录候选来源、证据等级、链映射、比较区间、差异、边界和 mutation 结果、最终裁决及排除原因。

#### 7. 最终 antigen 表示和身份如何统一

本项只负责把前 1–6 项已经唯一确定的结果收敛到既定 `antigen` 模型。最终硬前置条件是：必须得到至少一条可复现的实验抗原序列；结构可以缺失。

canonical serialization 固定为：

```python
canonical_ag = "<SEP>".join(canonical_sequence_list)
AG_ID = hash(canonical_ag)
```

其中 `canonical_sequence_list` 是问题 4 确定的有序链序列列表。单链和短肽是长度为 1 的列表；多链按已确定的链顺序排列。`<SEP>` 只表示链边界，不属于氨基酸序列内容。

```latex
\begin{algorithm}[H]
\caption{Final Antigen Representation and Identity}
\label{alg:final-antigen-representation}
\KwIn{resolved antigen sequence list $S^\dagger$; optional overall structure $p^\dagger$; lineage $L$}
\KwOut{antigen $(AG\_ID, sequence, structure, lineage)$ or exclusion status}

\If{$S^\dagger$ is missing, empty, or cannot be reproduced}{
    record the exact sequence failure in $L$;
    \Return{exclude}
}
\If{only structure evidence exists}{
    recover a unique sequence from the structure through the earlier recovery modules;
    \If{sequence recovery fails}{
        record the failure in $L$; \Return{exclude}
    }
}
$canonical\_ag \leftarrow$ join the ordered canonical sequences in $S^\dagger$
with the literal separator \texttt{<SEP>};
$AG\_ID \leftarrow hash(canonical\_ag)$;
$p^\dagger \leftarrow$ retain the mapped overall structure, or set
$p^\dagger = \mathrm{None}$ when structure is unavailable;
record chain order, canonical string, hash, structure status and source lineage in $L$;
\Return{$(AG\_ID, S^\dagger, p^\dagger, L)$}
\end{algorithm}
```

固定口径：

- sequence 可靠、structure 缺失：保留 antigen，`structure = None`。
- structure 存在但 sequence 缺失：只有在前置模块能够从 structure 唯一恢复 sequence 时才保留。
- sequence 和 structure 同时缺失，或 structure 无法恢复出唯一 sequence：排除。
- `AG_ID` 只由最终有序 canonical sequence 列表计算；名称、structure、来源、lineage 和 affinity 不参与 hash。
- `lineage` 记录最终链顺序、`<SEP>` 拼接结果、`AG_ID`、结构是否缺失，以及 sequence 恢复或排除原因。

#### 8. 跨源合并和 lineage 如何使结果可复现

跨源合并只合并最终 canonical sequence 相同的 antigen。来源名称、结构引用和实验来源不参与 `AG_ID` 去重；它们全部追加到同一个 antigen 的 `lineage`。

每条 lineage description 至少记录：

- `SRC_ID`、原始文件/表、行号或记录 ID；
- affinity 记录与 antigen 的绑定依据；
- 使用的序列、FASTA、PDB/mmCIF、accession 或 parent/mutation 来源；
- antigen chain 集合、固定顺序、边界裁剪和 mutation 重建；
- 来源、序列、结构冲突及最终裁决；
- canonical sequence、`<SEP>` 拼接结果和 `AG_ID`；
- structure 是否缺失、使用的工具及版本；
- 无法唯一恢复或被排除时的具体原因。

同一 `AG_ID` 可以保留多个结构引用、多个来源定位和多个实验构建体说明；这些信息只追加到 `lineage`，不覆盖已有记录。任何 `None`、冲突或排除状态都必须写明原因，使后续 workflow 能从原始定位重新执行处理。
