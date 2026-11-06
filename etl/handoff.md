# ETL 交接

## 目标与成功标准

把 20 个 SRC 处理成 modeling 的 `3A = (3A_ID, antibody, antigen, affinity[])`，产出有效的 `3a` Parquet shards。**成功的标准是有产出，不是处处合规**：某条记录处理不了就按排除码写进 `reject_log` 继续，不要为一个边缘情形停机。

## 硬约束

- **affinity 五元组不改**：`(label, assay, condition, replicate, lineage[])`。`label` 不为 `None`，其余三项各自可为 `None`。额外信息只进 `lineage`。
- **不写根分区**：临时文件与缓存放 `/data_new/ywy/`（`env.sh` 已设 `TMPDIR`、`UV_CACHE_DIR`、`XDG_CACHE_HOME`、`RCSB_CACHE`）。根分区只剩约 3.7 GB。
- **刻意压缩的数据集不解包**，直接按需读取。
- **只在远程做**：全部开发、测试、提交在 `ssh 3x5090` 的 `/data_new/ywy/LOVYATEE`，分支 `etl-b-layer`。开工前确认 `etl-a-layer` 已合入 `origin/main`；**没合入就停下并告知 Pthahnix**。本地仓库不做任何写操作；完成后 push 该分支，由 Pthahnix 亲自 merge。
- **并行 worker 上限 32**（33 个登录用户，负载约 8）。
- **长任务**用 `setsid nohup <cmd> > <log> 2>&1 &` 启动并读日志，不要挂长连接 ssh。

## 环境入口

```bash
ssh 3x5090 'cd /data_new/ywy/LOVYATEE && source etl/env.sh && ...'
```

`env.sh` 提供：venv `/data_new/ywy/envs/etl`、`hmmscan`（`/data_new/ywy/tools/hmmer/usr/bin`）、`ETL_ROOT`、`PYTHONPATH`、`TMPDIR`、`UV_CACHE_DIR`、`XDG_CACHE_HOME`、`RCSB_CACHE`、`ETL_PROXY=http://127.0.0.1:17890`。

- **代理**：只有 RCSB 需要，`structref` 自己用 `ETL_PROXY`，不要设全局代理。mihomo 须以 `GODEBUG=tlsmlkem=0` 启动（主机重启后手动拉起）：`cd /data_new/ywy/tools/mihomo && GODEBUG=tlsmlkem=0 setsid nohup ./mihomo -d . -f config.yaml`。下载失败先看 `curl -s http://127.0.0.1:19090/proxies/PROXY` 的存活节点。
- **TLS**：这条线路对含 ML-KEM 的 ClientHello 不友好。自建 HTTPS 客户端时限定 `ctx.set_ecdh_curve("X25519")` 与 ALPN `http/1.1`，并对握手失败重试（`structref` 已这么做）。
- **数据**：`/data_new/ywy/dataset-abag/SRC_Rxx_*`。
- **版本**：见 `requirements.txt`（HMMER 3.4 不在 pip 里）。

## 工作对象

20 个 SRC。每个 SRC 的 inventory 在 `context/2026-10-30-3a-src-inventory/`，业务提示与建议顺序在 blueprint §6：

| 批次 | SRC |
| --- | --- |
| 第一 | R76、R77、R08、R74、R03、R80 |
| 第二 | R20（资源适配器，不产 `3A`）、R14、R15、R50、R75、R13、R11、R16 |
| 第三 | 按 `context/2026-11-01-20-src-data-etl-todo-list.md` 的顺序 |

```text
context/2026-11-04-3a-src-data-etl-blueprint.md        总体设计（§3 模块、§4 中间表、§6 SRC 映射）
context/2026-10-28-ab-ag-data-diversity/3a_src_data_etl_hash.md          ID 规则
context/2026-10-28-ab-ag-data-diversity/3a_src_data_etl_problem_ab.md    抗体方案
context/2026-10-28-ab-ag-data-diversity/3a_src_data_etl_problem_ag.md    抗原方案
context/2026-10-28-ab-ag-data-diversity/3a_src_data_etl_problem_aff.md   affinity 规则
```

## 共享模块

`core/` 下每个模块由同名 md 描述：`## 语义`、`## 接口`、`## 示例`。

| 模块 | 用途 |
| --- | --- |
| `lineage.py` | lineage 字符串拼装与解析；`step=` 名称约定 |
| `ids.py` | `AB_ID` / `AG_ID` / `3A_ID`，golden vector |
| `seqnorm.py` | 原始序列规范化与排除标记 |
| `resolve.py` | 候选按优先级择优，冲突只记录 |
| `vdomain.py` | ANARCI(IMGT) 编号 → 域区间、`vh`/`vl` 槽位；实测覆盖率见 md |
| `structref.py` | PDB/mmCIF → 链记录；RCSB 下载与撤销条目处理 |
| `mutate.py` | `apply_point`（点突变，A/B/C）与 `apply_region`（区间替换） |
| `antigen_bound.py` | 抗原链候选 → 有序裁剪后链列表 |
| `merge.py` | pair Parquet → `3a`、`stats`、`qa_sample`、`reject_log`、`manifest` |

**发现模块缺陷直接修**：改模块本身，不要加按 SRC 的分支（共享模块出现 SRC 特例即视为划分错误）。修改记一行到 `progress.md` 并重跑受影响的 SRC。

## 决策文件

AI 只用于把非结构化证据（README、metadata、表说明、文献语境）转成结构化论断，写到 `etl/decisions/<SRC>.yaml`（格式见 blueprint "AI 接缝"）。原则：

- **论断带可追溯证据**：`file` 或 `snapshot_file` 存在，`quote` 在其中逐字出现，`value` 中的序列在引用的 FASTA 或结构 entity 中逐字出现。
- **运行期不联网、不调用 AI**：只读决策文件。决策文件 hash 进缓存键（`merge` 的 `decision_files` 参数）。
- `applies_to` 限定文件、列、取值；不适用的行不继承。

## 进度记录

自己维护 `etl/progress.md`：每个 SRC 的状态、引入的 adapter、跑数命令、已知偏差、修过的模块。跨上下文续作以它为准。

## 验收（每个 SRC）

按阶段分别核对（blueprint §8）：

- `adapt`：源行数 = 产出 record 数 + 该 SRC 的 adapt reject 数；record 数可大于行数（R15 的 `mut`/`wt`）。
- `ab`、`ag`：distinct 键数 = ok 实体数 + reject 实体数。
- `assemble`：record 数 = pair 数 + reject 数。
- `merge`：`Σ len(affinity[])` = 全部 pair 的成立 observation 总数，每条恰好一次；`pair 数 - 3A 数` = 相同 `3A_ID` 的合并数。
- 某个 `reason_code` 命中过半记录时，先复查该排除条件是否适用于这个 SRC，再决定是否接受。
- **R76**：493 行对应 476 个源内唯一 `(X1, X2)` pair；最终 `3A` 数与 476 的差额必须能被 `reject_log` 与 ID 合并解释。
