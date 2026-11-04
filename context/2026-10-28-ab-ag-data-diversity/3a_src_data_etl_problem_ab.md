---
tags:
  - design
---

# VH VL VHH Sequence Cleaning Problem Inventory

本设计文件针对的是 [[2026-11-01-20-src-data-etl-todo-list]] 中的 `## 1. Data ETL Specification`.

## time

2026-11-01

## lineage

- 3a_src_data_etl_modeling.md: current MVP model for the processed Ab-Ag pair dataset.
- ../3a-src-inventory/src-03-abdesign-1-0.md: sequence and construct inventory.
- ../3a-src-inventory/src-08-avida-htnfa.md: sequence and tag inventory.
- ../3a-src-inventory/src-09-flab.md: heterogeneous antibody sequence inventory.
- ../3a-src-inventory/src-10-abrank.md: antibody and variant sequence inventory.
- ../3a-src-inventory/src-11-abbibench.md: paired heavy/light sequence inventory.
- ../3a-src-inventory/src-12-asd-agab-db.md: mixed antibody format inventory.
- ../3a-src-inventory/src-13-andd.md: mixed chain-slot and nanobody inventory.
- ../3a-src-inventory/src-14-ab-bind.md: structure-derived antibody sequence inventory.
- ../3a-src-inventory/src-15-skempi-2-0.md: structure and mutation sequence inventory.
- ../3a-src-inventory/src-16-guest.md: mixed Fab, Fv, scFv, and VHH inventory.
- ../3a-src-inventory/src-20-sabdab-sabdab2.md: SAbDab antibody chain inventory.
- ../3a-src-inventory/src-23-mit-ll-alphaseq.md: complete scFv and linker inventory.
- ../3a-src-inventory/src-50-graphinity.md: mixed structure-derived construct inventory.
- ../3a-src-inventory/src-74-abdesign-2-0.md: constant-region and His-tag inventory.
- ../3a-src-inventory/src-75-her2-aff-large-buzz.md: CDR-only sequence inventory.
- ../3a-src-inventory/src-76-tdc-antibodyaff.md: duplicated-slot and linker inventory.
- ../3a-src-inventory/src-77-akbar-sabdab-kd-csv.md: duplicated-slot and linker inventory.
- ../3a-src-inventory/src-78-mochibind-sampled-data.md: scFv and VHH inventory.
- ../3a-src-inventory/src-79-alphabind.md: scFv and VHH inventory.
- ../3a-src-inventory/src-80-antipasti.md: structure-derived mixed construct inventory.

## relation

None.

## description

### 问题

这份记录只列出 20 个 SRC 暴露出的 VH/VL/VHH 序列清洗问题，暂不决定具体清洗算法。它是 [processed Ab-Ag pair dataset model](3a_src_data_etl_modeling.md) 中 `vh_sequence`、`vl_sequence` 和 `AB_ID` 规则的前置问题清单。

1. **输入槽位和缺失值如何解析**：不同来源对重链、轻链和缺失值的表示方式不同，必须先明确什么能进入 `vh_sequence`、`vl_sequence`。
    - **H/L 分列**：源表分别提供 heavy 和 light 序列时，如何保持两条链的配对关系。
    - **列表字符串**：R76/R77 使用类似 `[heavy, light]` 的列表字符串，需要定义解析、转义和顺序规则。
    - **占位符**：R12/R13 等来源用空串、特殊字符串或占位序列表示不存在的链，需要统一为 `null` 还是拒绝。
    - **单槽位记录**：只有 H 或只有 L 的记录，必须区分 VHH、VH-only、VL-only、缺链和错误槽位。

2. **氨基酸字符如何规范化**：原始序列可能包含大小写、空白、换行、gap、终止符号或非标准字符，需要确定哪些字符可清洗、哪些必须进入 audit。
    - **大小写和空白**：是否统一为大写并删除所有非序列空白。
    - **gap 和终止符**：`-`、`.`、`*` 等字符是删除、解释为缺失，还是拒绝记录。
    - **未知残基**：`X`、`B`、`Z`、`J`、`U`、`O` 等字符是否允许保留。
    - **非氨基酸字符**：混入核酸、标签文本或结构文件残片时如何处理。

3. **Signal peptide 如何识别和裁剪**：R08 明确包含 22 aa 信号肽样前缀，但其他来源未必提供边界。
    - **来源明确边界**：有 dataset card 或构建体说明时，是否优先使用来源边界。
    - **预测边界**：没有来源边界时，是否允许使用预测工具，还是直接进入 audit。
    - **误裁风险**：不能仅按长度或 N 端疏水性盲目删除 VH/VHH 的真实 N 端残基。

4. **C 端 His-tag 和其他表达标签如何裁剪**：R08 有 `6×His`，R74 重链末尾有 `HHHHHH`，但标签不能与真实序列混淆。
    - **标签类型**：只处理明确识别的 His-tag，还是同时处理 FLAG、Myc、Strep 等标签。
    - **标签位置**：只裁剪末端连续标签，还是允许来源声明的内部标签。
    - **天然组氨酸**：如何避免误删真实 C 端 histidine 残基。
    - **标签边界证据**：标签边界来自字段、构建体说明还是序列模式。

5. **Constant region 如何裁剪为 VH/VL**：R03、R11、R12、R13、R14、R15、R16、R20、R50、R74、R76、R77、R80 含有 Fab、IgG、VH-CH1 或 VL-CL 量级序列。
    - **重链边界**：如何从完整重链中截取 VH，避免保留 CH1、铰链、Fc 或其他恒定区。
    - **轻链边界**：如何从完整轻链中截取 VL，避免保留 CL。
    - **结构边界优先级**：来源注释、PDB/mmCIF entity fragment、序列编号和预测边界发生冲突时如何取舍。
    - **未标构建体**：只凭长度不能区分 Fab、Fv、IgG 或其他构建体时如何处理。

6. **scFv linker 如何拆分**：R09、R16、R23、R78、R79、R80 含完整 scFv 单链，部分记录明确包含 linker。
    - **已知 linker 模式**：如 `GGGGSGGGGSGGGGS`，是否只按来源确认的模式拆分。
    - **未知 linker 模式**：没有明确 linker 序列或边界时如何定位 VH/VL。
    - **方向问题**：如何处理 VH-linker-VL 与 VL-linker-VH 两种顺序。
    - **linker 残留**：拆分后如何验证 linker 没有进入 VH 或 VL。

7. **H/L 槽位重复或错误映射如何处理**：R76/R77 有部分记录把含 linker 的同一条单链同时写入 H/L 两个槽位。
    - **同序列槽位**：H 与 L 完全相同时，不能直接当作有效 H/L pair。
    - **含 linker 槽位**：两个槽位都包含 linker 时，是否尝试还原单条 scFv。
    - **无法判定构建体**：不能确认拆分结果时应进入 audit，而不是生成 AB_ID。

8. **VHH 如何与普通 heavy-only 区分**：R08、R09、R12、R13、R15、R16、R20、R50、R78、R79、R80 同时存在 VHH、heavy-only 或单域样序列。
    - **显式来源标签**：VHH、Nanobody、sdAb、camelid 等标签作为 lineage 证据，不作为进入 processed dataset 的必要条件。
    - **长度证据**：长度只能辅助检查，不能单独把 heavy-only 判为 VHH。
    - **统一输出**：所有可用的 heavy-only 序列都保存为 vh_sequence，vl_sequence = None。
    - **构建体语义**：VHH、普通 VH-only 和无法确认类型的 heavy-only 都保留，具体类型只写入 lineage[]。

9. **WT、parent 和 mutation 如何重建完整序列**：R03、R09、R10、R12、R13、R14、R15、R50、R74 等包含突变体、parent 或 mutation 字段。
    - **突变表示**：如何解析单点突变、多个突变、插入、删除和范围突变。
    - **编号体系**：原始位点编号与序列索引、PDB 编号或 IMGT 编号不一致时如何映射。
    - **parent 缺失**：没有可靠 WT/parent 序列时是否拒绝重建。
    - **重建验证**：重建后的序列长度、字符和突变位置如何自检。

10. **结构辅助的 VH/VL 序列恢复如何进行**：R14、R15、R20、R50、R80 等来源需要从结构或 FASTA 链恢复序列。
    - **链选择**：如何从一个 PDB/mmCIF 中选择正确的抗体 H/L 链。
    - **残基缺失**：结构中缺失残基如何表示，是否允许补全。
    - **多实体结构**：同一结构包含多个抗体或多个链组合时如何保持配对。
    - **结构序列与表格序列冲突**：哪一个作为 `AB_ID` 的输入，另一份如何保留在 lineage/audit。

11. **CDR-only 或 partial sequence 如何处理**：R75 主要只有 10 aa CDR-H3，不能直接构成完整 VH/VL。
    - **CDR-only**：没有完整框架区时不得填充或猜测 VH/VL。
    - **VH-only study**：有完整 VH 但没有 VL 时，作为 heavy-only 保留；是否为 VHH 只写入 lineage，不作为进入条件。
    - **短片段**：仅有局部 variable-region 片段时进入 reject/audit。
    - **外部 scaffold**：若未来补齐 parent scaffold，需要保留原始 CDR 与重建依据。

12. **非抗体或无法确定抗体边界的记录如何处理**：部分来源包含 Fc-only、VL-only、普通蛋白链或构建体类型不明的记录。
    - **Fc-only**：R14 等只有 Fc/constant-region 的链不能作为 VH。
    - **VL-only**：R50、R80 等只有轻链的记录保留，输出 vh_sequence = None；不得凭空补出 VH。
    - **普通蛋白或错误 entity**：结构目录中没有抗体可变区的记录必须排除。
    - **模糊完整链**：不能可靠提取 VH/VL 时进入 audit，不凭长度猜测。

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

#### 数据保留与 `raw/audit` 术语

- `raw` 指现有的原始数据集及其原始目录，例如 `G:\abag-datasets`；本轮 ETL 不复制、覆盖或删除这些数据。
- `processed dataset` 只包含成功完成清洗、边界判定并满足 `AB_ID` 前置条件的记录。
- 本轮不在产物中创建 `raw/`、`audit/`、`reject/` 等目录，也不要求复制无法处理的记录。
- 文档中的 `audit` 表示处理时对“排除原因和原始定位”的判定信息，不表示一个新的数据集目录。无法可靠处理的记录留在原始数据集，不进入 processed dataset。
- 对进入 processed dataset 的记录，所有裁剪、判定和证据通过 `lineage[]` 记录；其中包含原始文件、表、行号或原始记录 ID，足以回到原始数据复核。

#### Canonical ID serialization

`AB_ID` 使用清洗后的 `vh_sequence` 和 `vl_sequence` 生成，不使用原始格式、结构、lineage 或来源名称。固定 canonical 规则为：

```python
canonical_ab = f"{vh_sequence or '<NONE>'}<SEP>{vl_sequence or '<NONE>'}"
AB_ID = hash(canonical_ab)
```

- `vh_sequence` 在前，`vl_sequence` 在后。
- Python `None` 统一序列化为 `<NONE>`；空字符串在前序列清洗阶段转换为 `None`。
- `<SEP>` 是固定字段分隔符，不属于规范化氨基酸序列字符。
- FASTA 标题、换行、空白和原始字段外壳不参与 hash。
- `None` 的槽位仍保留在 canonical 字符串中，避免不同 H/L 槽位状态发生身份碰撞。
- canonical 字符串、最终 hash 和必要的规范化信息写入 `lineage[]` 以便复现。

#### 1. 输入槽位和缺失值如何解析

- 同一条源记录中的 `heavy` 和 `light` 字段直接组成一个 H/L pair，分别映射到 `vh_sequence` 和 `vl_sequence`；记录行号或原始记录 ID 保持配对关系。
- 源表把两条链放在列表字符串中时，按来源约定的固定顺序解析，例如 `[heavy, light]` 转换为 `(vh_sequence, vl_sequence)`。元素数量不符、顺序无法确定或格式无法解析时，记录排除出 processed dataset，并保留原始定位，不进行猜测。
- 空字符串、`NA`、`None` 及来源定义的占位符统一转换为 Python `None`。序列化为 JSON 时，`None` 表示为 `null`。
- 两个序列字段最终只能是规范化后的氨基酸序列字符串或 `None`。FASTA 标题、换行和字段外壳由解析函数处理，不作为序列内容保留。
- 本项只负责输入槽位解析与缺失值归一化。VHH、普通 heavy-only、VL-only 及缺链记录的生物学有效性由后续构建体判定和 `AB_ID` 前置验证处理。
- 所有来源字段、配对方式、占位符转换和异常说明写入 `lineage[]`；每个 lineage 元素是一个字符串 description，不参与 `AB_ID` 去重。

#### 2. 氨基酸字符如何规范化

- 序列统一转换为大写，并删除空格、换行、制表符等非序列空白。
- `-`、`.`、`*` 等 gap 或终止符解释为该序列缺失。原始数据不删除，规范化记录写入缺失原因；是否在后续流程删除由第二轮 ETL 决定。
- `X`、`B`、`Z`、`J`、`U`、`O` 等未知残基保留为正常序列内容，并参与后续 `AB_ID` hash。
- 混入标签文本、数字、核酸内容或其他非法字符的记录，不进入本轮 processed dataset；原始数据保持不变，并保留原始定位和排除原因。
- 本轮“清洗掉”只表示从有效产物中排除，不表示删除原始数据。

规范化顺序为：

```text
解析 FASTA 外壳
→ 大写化并删除序列空白
→ 检查 gap/终止符并标记缺失
→ 保留允许的未知残基
→ 排除含非法字符的记录并记录原始定位与排除原因
```

#### 3–4. Signal peptide 与 C 端表达标签的统一裁剪方案

3 和 4 统一为 **N/C 端构建序列裁剪 pipeline**。所有发生 N/C 裁剪的序列，必须在 `lineage[]` 中记录可复现的边界、方法、证据、工具版本和冲突处理结果。

```latex
\begin{algorithm}[H]
\caption{N/C-terminal Construct Sequence Trimming}
\label{alg:nc-trimming}
\KwIn{
    raw antibody record $r$;
    source metadata $M$;
    source dataset $S$
}
\KwOut{
    processed VH/VHH sequence $s^*$;
    updated lineage[] $L$
}

\BlankLine
\textbf{Preserve raw input:}\\
Keep $r$ in the source dataset $S$ and record its source locator:
$\texttt{raw\_record\_ref}$,
$\texttt{raw\_sequence\_sha256}$,
source file, table, row number, and original record ID.

\BlankLine
\textbf{Preprocess:}\\
$s \leftarrow$ parse FASTA content from $r$;\\
$s \leftarrow \text{uppercase}(s)$;\\
$s \leftarrow \text{remove sequence whitespace}(s)$;\\
If $s$ contains invalid non-sequence characters, record the exclusion reason and source locator, then exclude $r$ from the processed dataset.\\
If $r$ is an scFv, split it into VH and VL before applying this algorithm.

\BlankLine
\textbf{Collect N-terminal candidates:}\\
$N_{\mathrm{cand}} \leftarrow \varnothing$;\\
Add source-defined signal-peptide boundary if available;\\
Add curated external boundary if an accession-level annotation exists;\\
Run SignalP~6.0 and Phobius;\\
Run ANARCI or IgBLAST/IMGT to identify the mature VH/VHH variable-region start;\\
Add all predicted boundaries and tool versions to $N_{\mathrm{cand}}$;\\
If no external boundary exists, use SignalP~6.0 as the N-terminal fallback.

\BlankLine
\textbf{Collect C-terminal candidates:}\\
$C_{\mathrm{cand}} \leftarrow \varnothing$;\\
Add source-defined tag or constant-region boundary if available;\\
Match known terminal tags and linker-tag combinations:
FLAG, HA, Myc, V5, Strep-tag~II, Twin-Strep, AviTag;\\
Run ANARCI or IgBLAST/IMGT to identify the mature VH/VHH variable-region end;\\
For long fusion tags or constant regions, run HMMER3, InterProScan/Pfam, or DIAMOND;\\
Add all predicted boundaries, matched profiles, and tool versions to $C_{\mathrm{cand}}$;\\
If no external boundary exists, use the VH/VHH variable-region end as the C-terminal fallback.

\BlankLine
\textbf{Resolve boundaries deterministically:}\\
$n^* \leftarrow \textsc{ResolveN}(N_{\mathrm{cand}})$;\\
$c^* \leftarrow \textsc{ResolveC}(C_{\mathrm{cand}})$;\\
Use the fixed priority:
\[
\text{source boundary}
>
\text{curated external annotation}
>
\text{multi-tool agreement}
>
\text{fixed fallback}
\]
If candidates conflict, select the highest-priority candidate; record all candidates and the conflict in lineage[].

\BlankLine
\textbf{Trim:}\\
$s^* \leftarrow s[n^*:c^*]$;\\
Remove the N-terminal signal peptide, C-terminal expression tag,
linker, constant region, or fusion domain selected by the resolved boundaries.\\
If $n^*$ or $c^*$ cannot be determined, leave $r$ in the source dataset and exclude it from the processed dataset.

\BlankLine
\textbf{Validate:}\\
Check that $s^*$ is non-empty;\\
Check that $s^*$ contains no selected terminal tag or constant-region suffix;\\
Check that $s^*$ is compatible with VH/VHH numbering;\\
Compute $\texttt{normalized\_sequence\_sha256}$ and
$\texttt{trimmed\_sequence\_sha256}$.

\BlankLine
\textbf{Record reproducible lineage:}\\
If N/C trimming occurred, append a serialized string description to lineage[] containing:
\begin{itemize}
    \item $\texttt{raw\_record\_ref}$ and source location;
    \item raw, normalized, and trimmed sequence hashes;
    \item selected N/C boundaries;
    \item all candidate boundaries;
    \item selected N/C methods;
    \item source and external evidence references;
    \item tool names and versions;
    \item matched tag or profile name;
    \item linker or constant-region decision;
    \item conflict status and fallback status;
    \item final trimming action.
\end{itemize}

\Return{$s^*$, $L$}
\end{algorithm}
```

进入 processed dataset 的 VH/VHH 序列都必须经过 N/C 端裁剪流程；每次裁剪都必须有完整的 `lineage[]` 记录。C 端初始标签库覆盖 FLAG、HA、Myc、V5、Strep-tag II、Twin-Strep、AviTag，以及 GST、MBP、SUMO、Fc 等长融合标签或恒定区。

#### 5. Constant region 如何裁剪为 VH/VL

Constant region 裁剪与 H/L 链判定统一为“变量区边界提取 + 结构交叉验证”流程。结构数据作为额外证据使用：只做链选择、序列提取、残基编号映射和边界核验，不对坐标或结构本身做复杂变换。

```latex
\begin{algorithm}[H]
\caption{Constant-Region Trimming and Structure Cross-Validation}
\label{alg:constant-region-trimming}
\KwIn{
    raw antibody record $r$;
    source metadata $M$;
    optional structure $P$;
    source dataset $S$
}
\KwOut{
    processed antibody $a^\ast$;
    updated lineage[] $L$
}

\BlankLine
\textbf{Preserve raw input:}\\
Keep $r$ and, when available, $P$ in the source dataset $S$ and record:
\texttt{raw\_record\_ref}, source file, table, row number,
original record ID, structure ID, and raw sequence hashes.

\BlankLine
\textbf{Apply previous normalization:}\\
Parse FASTA content, uppercase the sequence, remove sequence whitespace,
and apply the N/C trimming result from Algorithm~\ref{alg:nc-trimming}.\\
If $r$ is an scFv, split it into VH and VL before constant-region extraction.

\BlankLine
\textbf{Classify construct granularity:}\\
Classify $r$ using source annotations, construct descriptions, and sequence evidence as one of:
explicit VH, explicit VL, explicit VHH, full heavy chain, full light chain,
Fab/Fv, IgG/Fc, scFv, or unmarked construct.

\BlankLine
\textbf{Determine chain identity:}\\
Use the following evidence priority:
\[
\text{source H/L annotation}
>
\text{structure chain/entity annotation}
>
\text{ANARCI or IgBLAST/IMGT}
>
\text{VH/VL profile evidence}
\]
Assign each sequence to heavy, light, or VHH.
Do not infer H/L identity from length alone.

\BlankLine
\textbf{Collect sequence boundary candidates:}\\
For each assigned chain, collect:
\begin{itemize}
    \item source-defined VH/VL or variable/constant boundary;
    \item ANARCI or IgBLAST/IMGT variable-region numbering boundary;
    \item HMMER3, BLASTp, or DIAMOND profile boundary;
    \item known constant-region or fusion-domain boundary.
\end{itemize}

\BlankLine
\textbf{Use structure as cross-validation evidence:}\\
If $P$ is available:
\begin{enumerate}
    \item Parse PDB/mmCIF chain, entity, residue numbering, and observed residues.
    \item Select H/L chains using source IDs, entity annotations, and sequence alignment.
    \item Align the structure-derived chain sequence to the normalized source sequence.
    \item Map the structure's variable/constant transition onto the source sequence.
    \item Record chain IDs, entity IDs, numbering scheme, residue ranges,
    alignment identity, missing residues, and structure-derived boundaries.
\end{enumerate}
Use the structure to confirm or challenge the sequence-derived boundary.
Do not fill missing structural residues or remodel coordinates.

\BlankLine
\textbf{Resolve variable-region boundaries deterministically:}\\
For each chain, use:
\[
\text{source boundary}
>
\text{structure boundary}
>
\text{ANARCI/IgBLAST/IMGT boundary}
>
\text{profile boundary}
>
\text{fixed fallback}
\]
If structure and sequence evidence agree, mark the boundary as cross-validated.
If they conflict, select the highest-priority boundary and record all candidates,
the conflict, and the selected method in lineage[].

\BlankLine
\textbf{Extract mature variable sequences:}\\
For a heavy chain, retain only the mature VH region and remove signal peptide,
CH1, hinge, Fc, constant region, tags, and other C-terminal extensions.\\
For a light chain, retain only the mature VL region and remove signal peptide,
CL and other C-terminal extensions.\\
For a confirmed VHH, retain the mature VH region and set
\texttt{vl\_sequence} = \texttt{None}.

\BlankLine
\textbf{Handle unmarked constructs:}\\
If the variable region and chain identity are recoverable from the evidence,
process the record using the resolved boundaries.\\
If no reliable VH, VL, or VHH variable-region boundary can be established,
leave the record in the source dataset and exclude it from the processed dataset.
Do not fabricate a variable region from length or partial constant-region evidence.

\BlankLine
\textbf{Validate:}\\
Check that each retained sequence is non-empty and compatible with
VH/VL/VHH numbering.\\
Check that no selected constant-region suffix remains.\\
Check that the H/L pairing and, when available, structure chain mapping are preserved.\\
Compute normalized and trimmed sequence hashes for reproducibility.

\BlankLine
\textbf{Record reproducible lineage:}\\
For every processed sequence, append a serialized string description to lineage[]
containing:
\begin{itemize}
    \item raw record and source location;
    \item construct classification and H/L/VHH assignment;
    \item source, structure, numbering, and profile evidence;
    \item structure ID, chain ID, entity ID, numbering scheme, and residue range;
    \item source-to-structure alignment result and missing-residue status;
    \item all candidate boundaries and the selected boundary;
    \item removed region types: signal peptide, constant region, tag, linker, or fusion domain;
    \item method and tool versions;
    \item conflict, fallback, and cross-validation status;
    \item raw, normalized, and trimmed sequence hashes;
    \item final trimming action.
\end{itemize}

\Return{$a^\ast$, $L$}
\end{algorithm}
```

处理结果遵循三种路径：

- 粒度明确的 VH、VL、VHH、完整 heavy/light、Fab、Fv、IgG 或 scFv，按来源和序列边界直接处理。
- 粒度未标明但可由来源、结构、抗体编号和 profile 证据恢复的记录，经过交叉验证后处理。
- 无法可靠确定 VH/VL/VHH 变量区边界的记录留在原始数据集，不进入 processed dataset；本轮不复制到新的 audit/reject 目录。

结构验证只做轻量处理：选择正确的 chain/entity、提取观察到的残基、完成序列对齐和边界映射；结构坐标不参与改造，缺失残基不猜测补齐。

#### 6. scFv linker 如何拆分

本轮 20 个 SRC 中实际存在多种 scFv 表示：

- R09、R12、R23、R78、R79 存在完整单链 VH-linker-VL；R12、R23、R78 的本地源表确认大量记录使用 GGGGSGGGGSGGGGS。
- R13、R16、R50、R80 也有单链 scFv；R16 的 5C2B 是单条 254 aa 链，R80 的 scFv 主要从 PDB/mmCIF 结构链恢复。
- R80 出现 VL-linker-VH 反向构型和非标准 linker，例如 4F9L、3ETB、5A2I、5KOV。
- R76、R77 各有 21 条把同一条完整单链同时写入 H/L 两个槽位，其中 15 条含 GGGGSGGGGSGGGGS。
- R12 的 scfv.csv 同时包含完整单链记录和 754 条独立 H/L 槽位记录，不能按文件名统一假设输入形态。
- R16 的来源标签与 PDB FASTA 存在不一致：5C2B 是单链 scFv，而 4NKI、5I30 的结构 FASTA 表现为独立 Fab H/L 链，需按实际链实体和序列证据重新判定。
- R75 只有 CDR-H3 片段，没有逐行完整 scFv 序列，不能执行 linker 拆分。
- 在 20 个 SRC 的 inventory 和本地可读源文件中未发现明确的 tandem VHH、三段以上 variable-domain 或其他需要扩展当前 vh_sequence / vl_sequence 模型的多域构建体。

工程处理分为三条路径：

1. 已提供独立 H/L 序列的记录跳过 linker 拆分，直接进入 N/C 和 constant-region 清洗。
2. 单槽位完整 scFv、重复写入 H/L 的完整 scFv，以及 PDB/mmCIF 单链结构，执行 linker 候选定位和 VH/VL 验证。
3. 只有 CDR 或无法恢复完整两侧变量区的记录保留在原始数据集，不进入 processed dataset。

```latex
\begin{algorithm}[H]
\caption{scFv Linker Splitting for the 20 SRCs}
\label{alg:scfv-linker-splitting}
\KwIn{
    raw antibody record $r$;
    source metadata $M$;
    optional PDB/mmCIF structure $P$;
    source dataset $S$
}
\KwOut{
    processed VH/VL representation $a^\ast$;
    updated lineage[] $L$
}

\BlankLine
\textbf{Preserve source reference:}\\
Keep $r$ and, when available, $P$ in the source dataset $S$.
Record source file, table, row number, original ID, structure ID,
and raw sequence hashes.

\BlankLine
\textbf{Normalize input:}\\
Apply the rules from Items 1--5:
parse FASTA content, uppercase sequence characters,
remove sequence whitespace, and retain the source locator.

\BlankLine
\textbf{Classify input shape:}\\
Classify $r$ as:
\begin{itemize}
    \item independent heavy and light sequences;
    \item one full scFv sequence;
    \item the same full scFv duplicated in both H/L slots;
    \item a single-chain PDB/mmCIF entity;
    \item VHH/heavy-only;
    \item CDR-only or partial sequence.
\end{itemize}

\BlankLine
\textbf{Direct H/L path:}\\
If independent heavy and light sequences are present and neither is a full scFv,
skip linker splitting and pass both sequences to the N/C and constant-region
trimming pipelines.

\BlankLine
\textbf{Collect linker candidates for a full single chain:}\\
Add candidates in the following order:
\begin{itemize}
    \item source-defined linker sequence or boundary;
    \item exact known linker sequences observed in the 20 SRCs;
    \item G4S repeat patterns, including three- and four-repeat variants;
    \item ANARCI or IgBLAST/IMGT variable-domain hits on both sides;
    \item HMMER3 linker profiles for non-standard linker sequences.
\end{itemize}
The initial exact linker library includes:
\[
\texttt{GGGGSGGGGSGGGGS},
\quad
\texttt{GGGGSGGGGSGGGGSGGGGS},
\]
and the non-standard linker patterns observed in R80 structures.

\BlankLine
\textbf{Use structure when available:}\\
For a PDB/mmCIF single-chain entity, select the antibody chain/entity,
extract its observed sequence, align it to the normalized source sequence,
and map the linker and variable-domain boundaries.
Do not remodel coordinates or fill missing residues.

\BlankLine
\textbf{Validate each candidate cut:}\\
For every candidate linker boundary, require:
\begin{itemize}
    \item one complete VH and one complete VL variable-domain hit;
    \item the linker lies entirely between the two variable domains;
    \item either VH-linker-VL or VL-linker-VH orientation is obtained;
    \item no third variable-domain hit is present;
    \item the split does not leave linker residues in VH or VL.
\end{itemize}

\BlankLine
\textbf{Resolve the cut deterministically:}\\
Choose the highest-priority valid candidate:
\[
\text{source boundary}
>
\text{exact known linker}
>
\text{two-sided variable-domain agreement}
>
\text{HMMER3 profile}
>
\text{G4S fallback}
\]
If several candidates remain, choose the candidate with valid VH and VL
domains on both sides and the smallest unresolved inter-domain segment.
Record all candidates and the selected candidate in lineage[].

\BlankLine
\textbf{Normalize orientation and trim:}\\
For VH-linker-VL, assign the two fragments directly.\\
For VL-linker-VH, swap the fragments before writing the fields.\\
Remove the linker, then apply Items 3--5 to each fragment
for signal peptide, expression tag, and constant-region trimming.

\BlankLine
\textbf{Handle duplicated slots:}\\
If H and L slots contain the same full scFv sequence,
parse the sequence once, discard the duplicated slot interpretation,
and preserve both original slot locations in lineage[].

\BlankLine
\textbf{Handle unresolved records:}\\
If the record contains only a CDR, only a partial variable region,
or no candidate cut produces one valid VH and one valid VL,
leave it in the source dataset and exclude it from the processed dataset.
Do not infer a linker or variable-domain boundary from length alone.

\BlankLine
\textbf{Validate output:}\\
Check that the final VH and VL are non-empty, contain no linker residues,
pass antibody variable-domain numbering, and satisfy the AB_ID prerequisites.

\BlankLine
\textbf{Record reproducible lineage:}\\
For every split, append a serialized string description to lineage[]
containing:
\begin{itemize}
    \item source record and original H/L slot locations;
    \item construct classification;
    \item raw, normalized, and split sequence hashes;
    \item linker sequence, start/end positions, and orientation;
    \item all candidate cut positions and candidate methods;
    \item selected cut and selection priority;
    \item ANARCI/IgBLAST/IMGT results for both fragments;
    \item HMMER3 profile name and version when used;
    \item PDB/mmCIF ID, chain/entity ID, residue range, and alignment result;
    \item duplicated-slot status;
    \item conflict, fallback, and cross-validation status;
    \item final VH/VL assignment and trimming action.
\end{itemize}

\Return{$a^\ast$, $L$}
\end{algorithm}
```

这一轮不新增多域数据结构。当前 20 个 SRC 未发现明确的 tandem 或三段以上 variable-domain 构建体；如果实际运行时发现此类记录，不能静默压缩为一个 VH/VL pair，应按 unresolved 路径排除并保留原始定位。

#### 7. H/L 槽位重复或错误映射如何处理

本轮 20 个 SRC 中实际需要处理的槽位异常包括：

- R76、R77 各有 21 条 H/L 槽位规范化后完全相同的记录，其中 15 条含 GGGGSGGGGSGGGGS linker。
- R12 的 scfv.csv 同时包含完整单链记录和 754 条独立 H/L 槽位记录，不能按文件名统一解释。
- R13 的部分记录来源标记为 scFv，但仍使用 H/L 槽位，需要逐条判断槽位内容。
- R16 的 5C2B 是单链 scFv；4NKI、5I30 的 PDB FASTA 表现为独立 Fab H/L，来源标签与结构实体不能直接互换。
- R50、R80 存在从 PDB/mmCIF 单链 entity 恢复 scFv 的记录。
- R75 只有 CDR-H3，没有完整 VH/VL，不能通过槽位修复。

这里必须区分两种同序列情况：

- 原始表格的 H/L 两个槽位规范化后完全相同，且不含 linker：视为来源槽位映射错误，直接排除。
- PDB/mmCIF 中 Hchain 与 Lchain 使用同一 chain/entity，但结构明确标注为 single-chain scFv：这是结构表示方式，进入第 6 项，不视为槽位错误。

本项由多个确定性模块组成：

```latex
\begin{algorithm}[H]
\caption{H/L Slot Collision and Mis-Mapping Recovery}
\label{alg:hl-slot-recovery}
\KwIn{
    normalized raw record $r$;
    source metadata $M$;
    optional PDB/mmCIF structure $P$;
    source dataset $S$
}
\KwOut{
    processed antibody $a^\ast$ or exclusion status;
    updated lineage[] $L$
}

\BlankLine
\textbf{Preserve source reference:}\\
Keep $r$ and, when available, $P$ in $S$.
Record source file, table, row number, original ID, and raw sequence hashes.

\BlankLine
\textbf{Classify slot shape:}\\
After Items 1--2 normalization, classify the H/L slots as:
\begin{itemize}
    \item distinct H/L sequences;
    \item identical H/L sequences without linker;
    \item identical H/L sequences containing a linker;
    \item one full scFv in one slot and the other slot empty;
    \item possible H/L label exchange;
    \item structure-level single-chain entity;
    \item unresolved or partial construct.
\end{itemize}

\BlankLine
\textbf{Direct distinct H/L path:}\\
If H and L are distinct and neither contains a full scFv,
retain the pair and pass both sequences to Items 3--5.

\BlankLine
\textbf{Reject identical slots without linker:}\\
If normalized H equals normalized L and no linker is detected,
classify the record as a source slot-mapping error.
Exclude it from the processed dataset without choosing one slot as authoritative.

\BlankLine
\textbf{Recover duplicated full scFv:}\\
If normalized H equals normalized L and a linker is detected,
create one single-chain candidate, preserve both original slot locations,
and call Algorithm~\ref{alg:scfv-linker-splitting}.

\BlankLine
\textbf{Recover one-slot scFv:}\\
If one slot contains a full scFv and the other is empty,
call Algorithm~\ref{alg:scfv-linker-splitting} on the populated slot.

\BlankLine
\textbf{Resolve possible H/L exchange:}\\
If H and L are distinct but their labels are uncertain,
run ANARCI or IgBLAST/IMGT on both sequences.
Swap the slots only when one sequence is assigned VH and the other VL.
If both sequences receive the same chain assignment or either assignment fails,
continue to the unresolved-construct module.

\BlankLine
\textbf{Handle structure-level single-chain entities:}\\
If $P$ identifies a single-chain scFv entity, select the entity,
extract its observed sequence, and call Algorithm~\ref{alg:scfv-linker-splitting}.
Do not treat equal structure chain IDs as duplicated H/L table slots.

\BlankLine
\textbf{Recover unresolved constructs:}\\
Use source annotations, structure chain/entity evidence,
ANARCI or IgBLAST/IMGT, and the Item 5 boundary pipeline.
If the evidence produces one valid VH and one valid VL,
continue with Items 3--6.
If no reliable construct interpretation is obtained,
leave the record in $S$ and exclude it from the processed dataset.

\BlankLine
\textbf{Validate recovered pair:}\\
Require non-empty VH and VL sequences, no residual linker in either sequence,
valid variable-domain numbering, and valid AB_ID prerequisites.
Do not repair a collision by length-only inference.

\BlankLine
\textbf{Record reproducible lineage:}\\
For every recovered record, append a serialized string description to lineage[]
containing:
\begin{itemize}
    \item original H/L slot values and source locations;
    \item normalized H/L sequence hashes;
    \item slot-shape classification;
    \item equality and linker-detection results;
    \item duplicate-slot recovery action;
    \item VH/VL reassignment evidence and tool versions;
    \item PDB/mmCIF ID, chain/entity ID, and structure interpretation;
    \item all candidate interpretations and the selected route;
    \item conflict, fallback, and exclusion status;
    \item final VH/VL assignment and downstream pipeline calls.
\end{itemize}

\Return{$a^\ast$, $L$}
\end{algorithm}
```

本项不新增字段，也不创建新的 raw/audit/reject 目录。来源槽位错误的记录留在原始数据集中；可恢复的重复 scFv 经过第 6 项拆分后进入标准 VH/VL 表示。

#### 8. VHH 如何与普通 heavy-only 区分

本轮从模型输入的第一性原理出发：模型只需要可用的抗体序列，不需要依赖 VHH 或其他 heavy-only 的构建体名称。因此，VHH、普通 VH-only 和无法确认具体类型的 heavy-only 统一进入 processed dataset。

判定 pipeline 只负责记录来源语义，不负责决定序列是否进入产物：

```text
原始来源标签与构建体描述
  ↓
VHH / Nanobody / sdAb / camelid 等显式证据
  ↓
结构 entity、物种信息、ANARCI、IgBLAST/IMGT 和 VHH profile
  ↓
记录 lineage 中的构建体状态
  ├─ VHH
  ├─ heavy_only
  └─ heavy_only_unconfirmed
  ↓
统一输出：
  vh_sequence = cleaned heavy sequence
  vl_sequence = None
```

- 显式来源标签是 lineage 证据，不是进入 processed dataset 的必要条件。
- 长度只能辅助分析，不能单独把 heavy-only 判为 VHH。
- VHH、普通 VH-only 和未确认的 heavy-only 使用相同的序列表示和 AB_ID 规则。
- lineage[] 详细记录来源标签、结构和物种证据、工具及版本、判定状态和原始定位。
- 只有序列本身不可用时才排除，例如 CDR-only、无法恢复的局部片段、非抗体序列或非法字符。

本项不新增 format 字段。后续若需要区分 VHH、VH-only 或其他 heavy-only，直接读取 lineage[]。

#### 9. WT、parent 和 mutation 如何重建完整序列

本轮涉及 R03、R09、R10、R12、R13、R14、R15、R50、R74。突变记录统一分为三类：

- **A：SRC 已提供完整 mutant sequence**。直接使用清洗后的完整序列；mutation、WT 或 parent 字段只作为 lineage 证据保存。若元数据与完整序列不一致，记录冲突，不据此再次改写序列。
- **B：SRC 提供 parent 和可唯一解析的 mutation**。通过来源适配器读取 parent、mutation、链身份和编号信息，再使用共享模块重建 mutant sequence。
- **C：SRC 无法唯一重建**。缺少 parent、链身份、编号体系、序列位置、原始残基或新残基中的必要信息，或者存在多个同样成立的映射候选；记录排除原因，不生成 processed dataset 记录。

20 个 SRC 中实际出现的表示包括：R03 的显式 residue/position/new-residue 字段，R14/R15 的链与残基突变语法，R50/R74 的名称编码突变，以及 R09、R12 等同时提供突变元数据和完整序列的记录。R10 的 mutation 主要描述 antigen escape，R14、R15、R50 也可能将 mutation 施加在 antibody 或 antigen 任一交互对象上，因此必须先确定突变所属实体，再修改对应 parent sequence。

这是一个统一总流程，内部使用来源适配器和共享重建模块：

```latex
\begin{algorithm}[H]
\caption{WT/Parent/Mutation Sequence Recovery for the 20 SRCs}
\label{alg:mutation-sequence-recovery}
\KwIn{raw source record $r$; source metadata $M$; optional structure $P$}
\KwOut{processed sequence $s^\ast$ or exclusion status; lineage string $L$}

\BlankLine
\textbf{Preserve source reference:}\\
Keep $r$ and, when available, $P$ in the source dataset. Record source file,
table, row or record ID, raw fields, and raw sequence hashes.

\BlankLine
\textbf{Apply SRC adapter:}\\
Map the source-specific full sequence, parent, mutation, chain, numbering,
and entity fields into a common internal representation. Use one adapter for
each observed source syntax; keep reconstruction and validation shared.

\BlankLine
\textbf{Classify sequence evidence:}\\
\begin{itemize}
    \item If a valid full mutant sequence is provided, classify the record as A.
    \item Otherwise, if a parent sequence and a complete mutation description
    are available, classify it as a B candidate.
    \item Otherwise, classify it as C and exclude it from the processed dataset.
\end{itemize}

\BlankLine
\textbf{Use A directly:}\\
Normalize and pass the full mutant sequence to the downstream VH/VL/VHH
cleaning pipeline. Preserve mutation metadata and any conflict with the full
sequence in lineage; do not reconstruct an already provided sequence.

\BlankLine
\textbf{Resolve B entity and mapping:}\\
Determine whether the mutation belongs to antibody or antigen. Parse the
mutation into original residue, new residue, chain identity, numbering system,
and residue position. Enumerate the source-supported chain and numbering
interpretations and map each candidate to the parent sequence.

\BlankLine
\textbf{Accept only a unique reconstruction:}\\
Retain a candidate only when the parent chain, numbering system, sequence
position, and original residue agree. Apply all mutations in the record and
accept the result only when exactly one candidate remains.

\BlankLine
\textbf{Validate the reconstructed sequence:}\\
Check parent and mutant hashes, original-residue matches, new-residue matches,
successful application of every mutation, sequence characters and length. Use
an available full sequence or structure as an independent cross-check.

\BlankLine
\textbf{Handle C or failed B records:}\\
Leave the raw record in the source dataset and exclude it from the processed
dataset. Do not infer a parent, position, chain, or residue from sequence
similarity, length, or affinity values.

\BlankLine
\textbf{Record reproducible lineage:}\\
For every A or successfully reconstructed B record, append a serialized string
to lineage[] containing the source adapter, class A/B, raw mutation text,
parent and mutant hashes, entity and chain identity, numbering system,
candidate mappings, selected mapping, applied edits, validation results,
cross-validation evidence, and any conflict or fallback status. For C and
failed B records, record the source locator and exact exclusion reason.

\Return{$s^\ast$, $L$}
\end{algorithm}
```

B 类重建需要的最小可定位条件是：

```text
parent sequence
+ chain identity
+ numbering system
+ residue position
+ original residue
+ new residue
```

这些条件的解析、候选枚举、唯一性判断和验证都是工程步骤。只有一个候选通过原始残基校验时才重建；候选不唯一或校验失败时归入 C。本项不新增数据字段，重建结果继续进入既有的 `vh_sequence`、`vl_sequence`、`structure` 和 `lineage` 表示。

相关 SRC inventory：

- [R03 AbDesign 1.0](../2026-10-30-3a-src-inventory/src-03-abdesign-1-0-inventory.md)
- [R09 FLAb](../2026-10-30-3a-src-inventory/src-09-flab-inventory.md)
- [R10 AbRank](../2026-10-30-3a-src-inventory/src-10-abrank-inventory.md)
- [R12 ASD / AgAb DB](../2026-10-30-3a-src-inventory/src-12-asd-agab-db-inventory.md)
- [R13 ANDD](../2026-10-30-3a-src-inventory/src-13-andd-inventory.md)
- [R14 AB-Bind](../2026-10-30-3a-src-inventory/src-14-ab-bind-inventory.md)
- [R15 SKEMPI 2.0](../2026-10-30-3a-src-inventory/src-15-skempi-2-0-inventory.md)
- [R50 Graphinity](../2026-10-30-3a-src-inventory/src-50-graphinity-inventory.md)
- [R74 AbDesign 2.0](../2026-10-30-3a-src-inventory/src-74-abdesign-2-0-inventory.md)

#### 10. 结构辅助的 VH/VL 序列恢复

结构处理拆成最小的共享模块，不新增输出字段，也不改造结构坐标。结构只负责提供链、entity、配对、序列来源和交叉验证证据；最终的 N/C 裁剪、constant-region 裁剪和 linker 拆分继续调用第 3–6 项模块。

```text
source adapter
  -> resolve structure reference
  -> parse polymer entity and chain
  -> resolve heavy/light/VHH/scFv and H/L pairing
  -> recover sequence
  -> align with source or parent sequence
  -> call existing N/C, constant-region and linker modules
  -> validate coverage and write lineage
```

模块规则：

- **结构引用模块**：解析 PDB/mmCIF/FASTA 引用，记录结构 ID、文件和版本。
- **entity/chain 模块**：读取 entity、auth/label chain、分子类型和描述，排除 DNA、RNA、配体及普通蛋白实体。
- **链角色与配对模块**：按来源标注、结构 entity、序列比对和编号证据确定 H、L、VHH、scFv 或 antigen，并保持同一 complex 内的配对。
- **序列恢复模块**：序列来源按 `source sequence > linked FASTA > mmCIF canonical sequence/SEQRES > observed ATOM sequence` 处理。只接受唯一映射，不从结构缺口猜测残基。
- **交叉验证模块**：将恢复序列与来源或 parent 序列比对，记录 identity、覆盖范围、缺失和冲突。完整来源序列优先于结构；结构只作为验证或无来源时的恢复来源。
- **覆盖处理模块**：结构坐标缺失但 canonical sequence 完整时保留序列；结构和序列在 VH/VL 内部都缺失时保留 3A，将受影响槽位设为 `None`，不填 `X` 或虚构残基。
- **lineage 模块**：记录结构 ID、entity/chain、序列来源、配对选择、比对结果、缺失位置、冲突和最终选择。

第 10 项不建立独立置信度分数，采用可复现的证据顺序：完整 assay 来源序列高于唯一关联 FASTA/canonical sequence，高于仅有的 observed structure sequence；同级冲突写入 `lineage`，不静默覆盖。结构恢复结果随后进入第 5 项 VH/VL 边界流程；scFv 进入第 6 项，H/L 映射进入第 7 项，VHH 语义进入第 8 项，mutation 结果由第 9 项交叉验证。

相关 inventory：

- [R14 AB-Bind](../2026-10-30-3a-src-inventory/src-14-ab-bind-inventory.md)
- [R15 SKEMPI 2.0](../2026-10-30-3a-src-inventory/src-15-skempi-2-0-inventory.md)
- [R20 SAbDab / SAbDab2](../2026-10-30-3a-src-inventory/src-20-sabdab-sabdab2-inventory.md)
- [R50 Graphinity](../2026-10-30-3a-src-inventory/src-50-graphinity-inventory.md)
- [R80 ANTIPASTI](../2026-10-30-3a-src-inventory/src-80-antipasti-inventory.md)

相关设计：[processed Ab-Ag pair dataset model](3a_src_data_etl_modeling.md)。

#### 12. 非抗体或无法确定抗体边界的记录如何处理

本项沿用既有模块，只增加一个轻量的“模糊链判定模块”，负责判断完整或长链是否能唯一解释为 VH 或 VL。它不重新实现序列清洗，也不凭长度猜测链身份。

处理规则：

- **Fc-only 或 constant-only**：不进入 processed dataset。R14 的 1T83、3WJJ，以及 R15 的 1FC2 属于此类，不能作为 VH。
- **VL-only**：保留，输出 `vh_sequence = None` 和清洗后的 `vl_sequence`。R50、R80 中明确为 variable light domain 的记录按此处理。
- **普通蛋白或错误 entity**：不进入 processed dataset。结构 entity、来源描述和分子类型均不能支持抗体 variable region 时直接排除。
- **模糊完整链或长链**：交给模糊链判定模块；只有能够唯一确定 VH/VL 身份并提取变量区的记录才进入后续流程。

```text
完整或长链序列
  -> 复用第 3–4 项完成 N/C 清洗
  -> 复用第 5 项寻找 variable/constant 边界
  -> 使用来源注释、结构 entity、ANARCI/IMGT、IgBLAST/profile 判定 H 或 L
  -> 枚举 VH/VL 边界候选
  -> 检查编号、保守位点、序列比对和结构映射
  -> 唯一候选通过验证
       -> 输出 VH 或 VL
  -> 多候选、冲突或无法定位
       -> 不进入 processed dataset
```

模糊链的证据顺序为：来源或结构的明确 H/L 标注，随后是 ANARCI/IMGT 或 IgBLAST 的链判定，再由 variable-region profile、边界和结构比对复核。只有长度相似不能通过；Fc、constant-only、普通蛋白和错误 entity 不得被解释为 VH/VL。单独恢复出 VH 时仍可输出 `vl_sequence = None`，不要求额外确认其为 VHH。

最终仍调用第 3–6 项完成裁剪和 linker 处理，第 8 项记录 heavy-only 语义，第 10 项提供结构链证据。每条保留记录的 `lineage` 记录来源注释、结构 entity、工具结果、候选边界、最终链身份和冲突；排除记录记录原始定位和排除原因。原始数据不修改，也不复制到新的 reject/audit 目录。

相关 inventory：

- [R12 ASD / AgAb DB](../2026-10-30-3a-src-inventory/src-12-asd-agab-db-inventory.md)
- [R14 AB-Bind](../2026-10-30-3a-src-inventory/src-14-ab-bind-inventory.md)
- [R15 SKEMPI 2.0](../2026-10-30-3a-src-inventory/src-15-skempi-2-0-inventory.md)
- [R50 Graphinity](../2026-10-30-3a-src-inventory/src-50-graphinity-inventory.md)
- [R80 ANTIPASTI](../2026-10-30-3a-src-inventory/src-80-antipasti-inventory.md)

相关设计：[processed Ab-Ag pair dataset model](3a_src_data_etl_modeling.md)。

#### 11. CDR-only 或 partial sequence 如何处理

本轮 20 个 SRC 中，真正的 CDR-only 情形主要是 R75：记录只有 10 aa 的 CDR-H3，没有 VH、VL 或其他框架序列。R79 的 CDR study 仍提供完整 `mata_sequence`，R23 也提供完整 scFv；它们不走本项的母本补全路径。R75 明确共享 trastuzumab 的 `1N8Z` 参考复合物，可尝试从同一 SRC、其他 20 个 SRC 或来源明确引用的 PDB/FASTA 中恢复母本。

本项采用 AI 编排、确定性工具执行的候选母本恢复流程：

```text
识别 CDR-only 或 partial record
  -> 提取 CDR 类型、链身份、编号体系和实验背景
  -> 在同一 SRC 内搜索母本
  -> 在其余 20 个 SRC 中搜索同一母本、PDB 或实验体系
  -> 读取明确引用的 PDB/mmCIF/FASTA
  -> 枚举候选 VH/VL scaffold
  -> 按编号和框架两侧边界插入 CDR
  -> 用 ANARCI/IMGT、序列比对和长度检查验证
  -> 只接受唯一且可复现的候选
  -> 进入既有 VH/VL 清洗流程
```

AI 负责识别局部序列类型、规划母本检索、汇总证据和提出候选；确定性工具负责读取真实序列、按编号定位 CDR、执行拼接、计算 hash 和验证结果。AI 不得直接生成框架区、凭相似抗体填充序列，或用模型预测替代母本。

母本搜索顺序固定为：

```text
同一 SRC
> 20 个 SRC 内的同一实验或抗体母本
> 来源明确引用的 PDB/FASTA
```

找到唯一母本、CDR 边界明确且拼接验证通过时，生成规范 VH/VL 并进入第 3–5 项清洗。若找不到母本、候选不唯一、CDR 边界无法定位或验证失败，则不进入 processed dataset；原始记录仍留在原始数据源。

R75 的预期路径是：

```text
1N8Z trastuzumab VH/VL
  + R75 CDR-H3
  -> 重建 mutant VH
  -> 保留 parent VL
  -> 进入既有 VH/VL 清洗
```

实际处理时仍需用序列比对确认 `1N8Z` 的 H/L 链和 R75 的编号边界，不能只凭抗体名称拼接。每次恢复都在 `lineage` 中记录原始 CDR、母本候选、来源 SRC_ID/PDB、链身份、编号体系、插入位置、拼接前后 hash、验证结果、冲突和最终判定。

相关 inventory：

- [R11 AbBiBench](../2026-10-30-3a-src-inventory/src-11-abbibench-inventory.md)
- [R23 MIT-LL AlphaSeq](../2026-10-30-3a-src-inventory/src-23-mit-ll-alphaseq-inventory.md)
- [R75 HER2-aff-large / Buzz](../2026-10-30-3a-src-inventory/src-75-her2-aff-large-buzz-inventory.md)
- [R79 AlphaBind public experiments](../2026-10-30-3a-src-inventory/src-79-alphabind-inventory.md)

相关设计：[processed Ab-Ag pair dataset model](3a_src_data_etl_modeling.md)。
