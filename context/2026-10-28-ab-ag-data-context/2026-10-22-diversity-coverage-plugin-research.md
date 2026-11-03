---
tags:
  - context
---

# Diversity Coverage Plugin Research

## Decision

本项目的最小完整产物是一个跨宿主的 `MCP + skill` plugin，暂名 `diversity-coverage`。

它不实现一个固定的 cluster 方法，也不让 AI 每次重新发明 diversity 定义。固定的是声明和证书语义；AI 只负责提出、解释和编排任务所需的声明与测量协议，MCP 负责可复算的观测和计算，人类负责确认最终判定。

核心计算保持为：

```text
S = Measure(D, O, X)
C = Evaluate(S, R, V, T, M)
A = Materialize(C, use_case)
```

其中 `C` 是带适用条件的 coverage certificate，`A` 是具体用途的 action plan：预训练数据配方、数据划分、推理风险评估或新增数据选择。

## Existing evidence

- `odrerir/son/diversity_is_a_task_conditioned_coverage_claim.md` 已将最小证书写成 `(D, O, X, R, V, T, M, result)`，并区分 similarity structure、coverage 和 generalization。
- `odrerir/tools/` 已有 MMseqs2、Foldseek、US-align、HMMER、HHsearch、InterProScan、zsasa、FreeSASA、Faiss 等 `O/X` 测量实现。工具名本身不等于科学相似性定义，结果必须保存输入、版本、参数、对应关系和缺失状态。
- `context/2026-10-22-training-data-similarity-and-protein-complex-structure-prediction.md` 已有三个可复用的用途：误差分析、风险校准、训练样本选择。
- `G:/OUROBOROS-AI4S/plm-scaling-law/context/2026-09-28-21-30-plm-scaling-research/report/2026-09-29-analysis-report-1.md` 表明 `rep_only`、`cluster → member`、`none` 是暴露和采样策略，不是 diversity 的定义。

## Product shape

### Skill layer

`skills/diversity-coverage/SKILL.md` 是唯一的主入口。它应当保持短，只定义状态机、确认门槛和调用 MCP 的顺序；详细的测量协议、结果 schema 和适用边界放在 references 中，按分支加载。

Skill 的运行状态：

```text
draft
  -> proposal
  -> human_review
  -> revised (zero or more times)
  -> locked
  -> measured
  -> validated
  -> certified
```

`explore` 可以在 `locked` 前运行，但结果只能标记为 provisional，不能生成正式 diversity claim。只有 `locked` 后的声明才能进入正式测量；只有 `validated` 且通过人类最终确认，才能导出 `certified` 结果。

### MCP layer

MCP 只暴露深接口，不暴露一堆绑定具体工具的浅接口。第一版最小表面：

```text
measure_similarity(declaration, query, reference)
evaluate_coverage(similarity_artifact, declaration)
materialize_plan(certificate, use_case, budget)
get_run(run_id)
```

每个工具都返回结构化 JSON、来源和运行元数据；失败返回明确的 execution error；输入在服务器端再次校验。工具不替人类做最终确认，也不把缺失值填成零相似度。

### Cross-host packaging

同一 plugin 根目录共用 `skills/`、`.mcp.json`、server 和 references，同时提供两个宿主 manifest：

```text
diversity-coverage/
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
├── .mcp.json
├── skills/diversity-coverage/SKILL.md
├── skills/diversity-coverage/references/
├── server/
└── tests/
```

Claude Code 的 manifest 位于 `.claude-plugin/plugin.json`，Codex 的 manifest 位于 `.codex-plugin/plugin.json`；两者都可指向同一 `skills/` 和 `.mcp.json`。不要把可加载组件放进 manifest 目录本身。

## Human-in-the-loop contract

人类确认不是一句“确认一下”，而是一组可审计的锁定条件。正式执行前必须逐项确认：

1. `D` 的来源、版本、合并、去重、质量过滤和采样规则。
2. `O` 的比较对象及单位；例如单链、链对、界面、组装体或表面 patch。
3. `X` 的字段、表示、比对方法、阈值、链对应和聚合方式。
4. `R` 的参考域或目标域，以及它在本次主张中的角色。
5. `V` 的 held-out 集、独立验证器和通过条件。
6. `T` 的任务行为，以及 `M` 的模型、checkpoint、暴露状态和规模；未知必须显式标为 unknown。
7. 将要生成的用途：recipe、split、risk 或 collection plan。

人类可以要求重做、替换协议或拒绝主张。修改任一声明后，旧结果失效并生成新 `run_id`；不能在旧结果上静默覆盖。

## Certificate shape

```json
{
  "run_id": "...",
  "status": "provisional | locked | certified | rejected",
  "declarations": {"D": {}, "O": {}, "X": {}, "R": {}, "V": {}, "T": {}, "M": {}},
  "similarity_artifacts": [],
  "coverage_profile": {},
  "result": {},
  "claims": [{"text": "...", "strength": "...", "supported_by": [], "limits": []}],
  "uncertainties": [],
  "human_decisions": []
}
```

`coverage_profile` 保留阈值、对象层、分层和参考域信息，不压缩成一个 universal score。`claims` 必须带结论强度和 validity envelope：纯对象 coverage、任务相关迁移、训练干预收益和推理风险是四种不同强度的主张。

## First anchored use case

第一版先锚定 antibody–antigen structure prediction / SPM，不阻止后续扩展。建议输入为 SAbDab2、AVIDbase、OpenAlphaSeq 的声明式合并；核心 `O/X` 先做单链序列、链对序列、单链结构和整体组装几何；界面、表面、进化谱作为条件性扩展。

三种 adapter 共用同一个 certificate：

- `recipe`：比较不同 sampling、cluster/member exposure、权重和 token 预算造成的 coverage profile，再由训练对照验证收益。
- `split`：按声明的对象和测量协议划分，报告独立性和暴露状态；性能下降不能单独解释为泄漏。
- `risk`：把目标到参考集的 similarity/coverage 与模型 confidence 组合，但必须在固定 `T/M` 和独立 `V` 上校准。

## Research questions and gates

### Q1 — Does one certificate semantics support three uses?

Gate: 同一份 `(D,O,X,R,V,T,M)` schema 能够生成 recipe、split、risk 三类结果，且每类都能指出自己的验证器和不可迁移边界。

### Q2 — Where must AI stop?

Gate: AI 可以提出 `O/X/V` 候选和测量计划，但在声明未锁定、验证器未独立或模型暴露未知时，系统只能输出 provisional 或 downgraded claim。

### Q3 — Is the plugin surface small enough?

Gate: skill 入口、四个 MCP 深接口和结构化 certificate 足以覆盖首期用例；不为每个算法、阈值和下游任务新增一个工具。

## Primary sources

- MCP Tools specification: https://modelcontextprotocol.io/specification/2025-06-18/server/tools.md
  - 要求工具发现、JSON Schema、结构化结果、错误区分、输入校验、超时、日志和 human-in-the-loop。
- Claude Code plugin creation: https://docs.anthropic.com/en/docs/claude-code/plugins/create.md
  - 规定 `.claude-plugin/plugin.json`、`skills/`、`.mcp.json`、`--plugin-dir` 和 `claude plugin validate`。
- Local Codex plugin manifest reference: `C:/Users/Strix/.codex/.tmp/plugins/.agents/skills/plugin-creator/references/plugin-json-spec.md`
  - 规定 `.codex-plugin/plugin.json`、`skills`、`mcpServers` 和 marketplace entry 的结构。
- Local installed plugin example: `C:/Users/Strix/.codex/.tmp/plugins/plugins/life-science-research/.codex-plugin/plugin.json`

现有项目根目录的 `.mcp.json` 含有内联凭据。新 plugin 不得复制这些值；应改用环境变量、宿主的 secret store 或安装时注入，并在发布前轮换已暴露凭据。

## Next work

1. 定义 `D/O/X/R/V/T/M` 的 JSON Schema 和状态枚举。
2. 为首期四个 MCP 接口写最小输入/输出契约。
3. 写 `diversity-coverage` skill 的 HITL 状态机和确认模板。
4. 用一个 SPM 数据配方案例走完 `provisional -> certified`，再决定是否实现 server。

当前跳过：没有创建 plugin 目录、MCP server 或工具包装代码，也没有发布 marketplace；先把 schema、确认门槛和首个案例锁定。主要风险是宿主对双 manifest 和 MCP 工具审批的版本差异，需要在原型阶段分别运行 Claude Code 与 Codex 的验证命令。

## Checkpoint: 001-2026-10-22 12:39:03 UTC

Phase: plugin-shape-and-hitl

Source: `problem-reframing`, MCP Tools specification, Claude Code plugin creation, local Codex plugin manifest reference

Status: complete

Input slice: Existing `odrerir` certificate definition, similarity tools, training-data similarity plan, PLM sampling report, current `.claude/`, `.codex/`, and `.mcp.json` layout; user-confirmed `MCP + skill` direction and human-in-the-loop requirement.

Process: Reframed the dominant “cluster algorithm” frame into a typed coverage-certificate compiler; compared the smallest cross-host plugin seam; extracted MCP security, structured-output, and confirmation requirements from primary specifications; fixed the first HITL state machine and certificate shape.

Results: The stable object is a certificate plus a use-case adapter. The first implementation boundary is one skill, four MCP deep interfaces, shared references, and dual host manifests. Exploratory measurements may run before lock, but only locked declarations can enter a formal run and only validated, human-approved output can be certified.

Delta:
  findings:
    - The existing repository already contains the scientific declaration slots and most measurement adapters; the missing layer is the host-facing orchestration contract.
    - Human confirmation is a protocol state, not a prose reminder: `draft -> proposal -> human_review -> locked -> measured -> validated -> certified`.
    - MCP structured results, input validation, error states, timeouts, and audit logs fit the certificate and provenance requirements.
  evidence_updates:
    - Added official MCP Tools specification and Claude Code plugin creation documentation as primary sources.
    - Added local Codex plugin manifest specification and installed plugin example.
  hypothesis_updates:
    - One certificate schema can support recipe, split, and risk adapters if each adapter declares its own validator and validity envelope.
    - A small skill plus deep MCP interfaces will be more portable and less context-heavy than a monolithic workflow.
  assumption_updates:
    - The first anchored use case is antibody–antigen structure prediction / SPM.
    - The current project’s tool wrappers are treated as measurement adapters, subject to protocol validation.
  uncertainties:
    - Exact Codex and Claude Code version behavior for dual manifests and plugin-provided MCP configuration remains to be tested in a prototype.
    - The executable language and process model for the local bioinformatics MCP server are not fixed.
  decisions:
    - Keep one context file for this research run.
    - Do not build or publish a plugin before the schema, confirmation gate, and first anchored case are locked.
    - Never copy inline credentials from the existing `.mcp.json` into a plugin.
  open_questions:
    - Which SPM checkpoint and training exposure ledger will be the first concrete `M` instance?
    - Which held-out antigen/family panel will serve as the first independent `V`?
  recommended_jumps:
    - target: `build-domain-ontology`
      reason: Freeze the JSON-level meanings and allowed unknown states for `D/O/X/R/V/T/M/result` before implementation.


## Checkpoint: 002-2026-10-22

Phase: contract-and-plugin-prototype

Status: prototype complete; host installation still unverified

Decision: Freeze the first cross-host seam as a dependency-free Python MCP server plus one model-invoked skill. The server keeps only four deep tools: `measure_similarity`, `evaluate_coverage`, `materialize_plan`, and `get_run`. The skill owns the human conversation and approval gates.

Schema decisions:

- Every declaration contains object slots `D`, `O`, `X`, `R`, `V`, `T`, `M`, a positive `revision`, `state`, and an auditable `human_decisions` array.
- `X.metric` is currently `provided` or `feature_jaccard`. `provided` is the adapter seam for MMseqs2, Foldseek, US-align, HMMER, HHsearch, surface, and embedding tools; the server does not redefine their scientific measurements.
- `V.coverage_threshold` is required for formal evaluation. Missing or unknown required values produce a typed error instead of an invented zero or a universal score.
- Seven slot approvals are required for formal evaluation. An additional `certificate` approval is required before `materialize_plan` can emit a certified recipe, split, or risk plan.
- Declaration changes are content-addressed and produce a new `run_id`; old artifacts are never silently overwritten.
- `M.status: unknown` is allowed, but risk materialization reports that no calibrated model confidence was supplied. Coverage remains relative to the declared validator and measurement protocol.

Implemented under `diversity-coverage/`:

- dual manifests for Claude Code and Codex;
- shared `.mcp.json` using a plugin-local working directory;
- machine-readable `server/schema.json`;
- dependency-free stdio MCP server with structured results and typed tool errors;
- HITL skill instructions and three contract tests covering provisional gating, certified materialization, and revision invalidation.

Validation: `python -m unittest discover -s diversity-coverage/tests -v` passes (3 tests); `claude plugin validate diversity-coverage` passes with only the optional icon warning; all JSON manifests parse.

Remaining uncertainty: Codex exposes no local `plugin validate` command. A real Codex install/load test requires a local marketplace entry or installation action and is deferred until the plugin contract is reviewed. The prototype is in-memory and the supplied measurement adapter is not a replacement for production sequence/structure tools.

SPM smoke run: with `D = SAbDab2 + AVIDbase + OpenAlphaSeq`, `O = antibody-antigen-pair`, `X = provided/spm-similarity-v0`, `R = antibody-antigen production`, `V = held-out-antigen-family-v0` at threshold `0.8`, `T = SPM`, and `M.status = unknown`, the first locked run returned `validated_pending_human` with query coverage `0.5`. After the human approved the certificate and revision `2` forced a new measurement, the run returned `certified`; the recipe adapter emitted the two target IDs under the declared coverage-stratified rule. This demonstrates the intended provisional-to-certified loop without claiming SPM generalization.

Validation update: the contract suite now has 5 passing tests, including the separate certificate gate and certificate tamper rejection.

Boundary hardening after the smoke run: evaluation now accepts only a measured artifact issued by the same in-memory server, and materialization accepts only the server-issued certified certificate. Pair scores and feature inputs are range/type checked. This keeps the prototype from treating a caller-supplied JSON object as a trusted certificate.
