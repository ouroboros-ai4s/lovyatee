# ETL A 层 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 3x5090 的 `etl-a-layer` 分支上交付 `etl/`：8 个共享模块加 `merge`（各带 md 与最小自检）、`env.sh`、依赖文件、`handoff.md`，使执行者 cc 可以直接开始 B 层。

**Architecture:** 共享模块是 `etl/core/` 下的纯函数文件，只做业务语义，不含 SRC 名称或特例；数据条件（无域、槽位冲突、突变无法映射）以 `reason` 返回，不抛异常。`merge` 用 DuckDB 读各 SRC 的 `pair` Parquet，输出 `3a` shards、`stats`、`qa_sample`、`reject_log`、`manifest`。B 层（adapter、跑数、决策文件）不在本计划内，A 层合入 main 之后另写 plan。

**Tech Stack:** Python 3.12.3、Daft 0.7.26、DuckDB 2.0.0、pyarrow 25.0.1、gemmi 0.7.5、ANARCI 2026.2.13.2 + HMMER 3.4、uv 0.13.7、pytest 9.2.0。

**Spec:** `context/2026-11-04-3a-src-data-etl-blueprint.md`（§3 模块、§4 中间表、§5 环境、§7 交付物）。ID 与序列化以 `context/2026-10-28-ab-ag-data-diversity/3a_src_data_etl_hash.md` 为准；字符与槽位规则见同目录 `3a_src_data_etl_problem_ab.md` 第 1、2、7、9、10 项，抗原规则见 `3a_src_data_etl_problem_ag.md` 第 3–7 项，affinity lineage 写法见 `3a_src_data_etl_problem_aff.md` 第 2–4 项。

## Global Constraints

- **只在远程做。** 全部开发、测试、提交在 `ssh 3x5090` 的 `/data_new/ywy/LOVYATEE`，分支 `etl-a-layer`。本计划写完之后，本地 `D:\LOVYATEE` 不做任何写操作：不 checkout、不 commit、不 pull、不落中间文件。文件用 `ssh 3x5090 'cat > path' <<'EOF'` 写入，不经本地中转。
- **分支。** 只在 `etl-a-layer` 提交，不动 `main`。Task 10 把该分支 push 到 origin，由 Pthahnix 亲自 merge。每次 commit 用 `git commit -m "<msg>" -m "<attribution>"`，attribution 为当前会话规定的署名行。
- **命令简写。** `[host] <cmd>` 表示 `ssh 3x5090 'cd /data_new/ywy/LOVYATEE && source etl/env.sh && <cmd>'`。Task 1 之前没有 `env.sh`，用裸 `ssh 3x5090 'cd /data_new/ywy/LOVYATEE && <cmd>'`。
- **不写根分区。** 临时文件与缓存放 `/data_new/ywy/`（`TMPDIR`、`UV_CACHE_DIR`、`XDG_CACHE_HOME`）。`/data_new/ywy/abag_final` 与 `/data_new/ywy/_tmp_paircalc` 不是本任务的，不碰。
- **并行 worker 以 32 为上限**（33 个登录用户，负载约 8）。
- **SSH 偶发断开。** 命令失败先重试；超过一分钟的任务用 `setsid nohup <cmd> > <log> 2>&1 &` 启动并读日志。
- **版本固定。** Python 3.12.3、Daft 0.7.26、DuckDB 2.0.0、pyarrow 25.0.1、gemmi 0.7.5、ANARCI 2026.2.13.2、HMMER 3.4、uv 0.13.7、pytest 9.2.0。不引入 Ray、Snakemake、Airflow。
- **ID 公式（hash 文档）。** `H(s)=sha256(s.encode("utf-8")).hexdigest()[:32]`；`AB_ID=H("ab/v1:"+(vh or "<NONE>")+"<SEP>"+(vl or "<NONE>"))`；`AG_ID=H("ag/v1:"+"<SEP>".join(chains))`；`3A_ID=H("3a/v1:"+AB_ID+"|"+AG_ID)`。链序不得排序后再 hash。
- **affinity 五元组不改：** `(label, assay, condition, replicate, lineage[])`。`label` 不为 `None`，其余三项各自可为 `None`。额外信息只进 lineage。
- **lineage 语法：** 用 ` | ` 分隔的片段，定位为 `SRC_Rxx | <文件> | row=N | ...`，其余片段为 `key=value`。实体 lineage 的每个元素以 `step=<名称>` 开头。
- **模块无 SRC 特例。** `etl/core/*.py` 不出现 SRC 名称或按 SRC 的分支；测试文件可以引用 SRC 的真实数据。
- **数据条件不抛异常。** 排除码（`no_domain`、`slot_collision`、`mutation_unassigned` 等）是默认处置，模块以 `reason` 字段返回；只有调用方违反契约（空链表、非法字符传给 `ids`）才 `raise ValueError`。
- **schema 显式声明。** 每张 Parquet 表用 pyarrow 声明 schema，全为 `None` 的列也要保持类型。
- **测试位置。** `etl/core/test_<模块>.py`，真实序列取自 `/data_new/ywy/dataset-abag/SRC_Rxx_*`，文件与列名查 `context/2026-10-30-3a-src-inventory/` 下对应的 inventory 文档。标记 `network` 的测试经 mihomo 访问 RCSB，标记 `data` 的测试读 SRC 数据。
- **模块 md** 含三节：`## 语义`、`## 接口`、`## 示例`，示例用测试里的真实序列。
- **与 blueprint 的两处顺序差异：** `env.sh` 提前到 Task 1（每个任务都要它）；`resolve` 提前到 Task 4（`structref`、`antigen_bound` 依赖它）。blueprint §7.2 的"只在 main 工作"被本次指令取代：A、B 两批各在远程独立分支完成。

## Review Focus

1. `merge` 读到全 `None` 的结构列或零行的 `pair` 文件时，输出 schema 仍等于 `OUT_SCHEMA`，不因类型推断为 `null` 而失败。（Task 9 `test_all_null_and_empty_inputs`）
2. 序列以终止符 `*` 结尾、或含内部 `-`：`seqnorm` 返回 `seq=None` 且带 `gap` 标记，不截断、不抛异常，调用方据标记自行预处理。（Task 3 `test_trailing_stop_and_internal_gap`）
3. 空串、过短、非抗体的输入交给 `vdomain`：返回 `reason="no_domain"`，不抛异常。（Task 5 `test_unnumberable_inputs_return_no_domain`）
4. 带插入码的位点（52A）与未指定链的突变：位点按 `(编号, 插入码)` 精确映射；未指定链且多条链同样成立时归 C 类，不猜。（Task 7 `test_insertion_code_position`、`test_empty_chain_ambiguous_is_C`）
5. 同源多聚体抗原的相同链保留为列表中的多个元素，不去重，且顺序参与 `AG_ID`。（Task 8 `test_homodimer_keeps_both_chains`）

---

## 文件结构

```text
etl/
  __init__.py
  pytest.ini                 注册 network / data 标记
  env.sh                     Task 1
  requirements.txt           Task 10
  handoff.md                 Task 10
  core/
    __init__.py
    lineage.py  ids.py  seqnorm.py  resolve.py      Task 1–4
    vdomain.py  structref.py  mutate.py             Task 5–7
    antigen_bound.py  merge.py                      Task 8–9
    <每个模块>.md  test_<每个模块>.py  test_docs.py
```

依赖方向：`lineage` ← `seqnorm`、`resolve`、各模块；`ids` ← `merge`；`resolve` ← `structref`、`antigen_bound`；`vdomain` ← `mutate`；`structref` 的 `ChainRecord` 经调用方粘合到 `mutate.ParentChain`（见 Task 7）。

---

### Task 1: 分支、脚手架、env.sh、lineage

**Files:**
- Create: `etl/__init__.py`、`etl/core/__init__.py`（空文件）、`etl/pytest.ini`、`etl/env.sh`
- Create: `etl/core/lineage.py`、`etl/core/lineage.md`、`etl/core/test_lineage.py`

**Interfaces:**
- Produces（`etl/core/lineage.py`）：
```python
SEP = " | "
def kv(key: str, value: object) -> str                  # "key=value"；值里的 "|" 转义为 "\|"，换行换成空格
def locator(src: str, file: str, *frags: str) -> str    # src 须匹配 ^SRC_R\d+$，否则 ValueError
def step(name: str, *frags: str) -> str                 # "step=<name>" 开头
def join(*frags: str) -> str
def split(s: str) -> list[str]                          # 按未转义的 " | " 切分
def get(s: str, key: str) -> str | None                 # 返回第一个 key 的反转义值
```
- Produces（`env.sh`）：激活 `/data_new/ywy/envs/etl`，PATH 加 `/data_new/ywy/tools/hmmer/usr/bin`，导出 `ETL_ROOT`（仓库根）、`PYTHONPATH`（含 `ETL_ROOT`）、`TMPDIR=/data_new/ywy/tmp`、`UV_CACHE_DIR=/data_new/ywy/cache/uv`、`XDG_CACHE_HOME=/data_new/ywy/cache/xdg`、`RCSB_CACHE=/data_new/ywy/cache/rcsb`、`ETL_PROXY=http://127.0.0.1:17890`，并 `mkdir -p` 这些目录。

- [ ] **Step 1: 建分支**

Run: `ssh 3x5090 'cd /data_new/ywy/LOVYATEE && git fetch origin && git switch -c etl-a-layer origin/main && git branch --show-current'`
Expected: 输出 `etl-a-layer`。

- [ ] **Step 2: 写 `etl/env.sh`、`etl/pytest.ini`（markers: `network`、`data`）、两个 `__init__.py`，验证环境**

Run: `ssh 3x5090 'cd /data_new/ywy/LOVYATEE && source etl/env.sh && python -c "import daft,duckdb,pyarrow,gemmi,anarci;print(daft.__version__,duckdb.__version__,pyarrow.__version__,gemmi.__version__)" && which hmmscan && echo $TMPDIR'`
Expected: `0.7.26 2.0.0 25.0.1 0.7.5`、`/data_new/ywy/tools/hmmer/usr/bin/hmmscan`、`/data_new/ywy/tmp`。

- [ ] **Step 3: 写失败的测试 `etl/core/test_lineage.py`**

```python
def test_locator_format():
    assert locator("SRC_R76", "protein_sabdab.csv", "row=123", "ID1=1ABC") == \
        "SRC_R76 | protein_sabdab.csv | row=123 | ID1=1ABC"

def test_locator_rejects_bad_src():
    with pytest.raises(ValueError): locator("R76", "f.csv")

def test_kv_roundtrip_with_special_chars():
    s = join(locator("SRC_R09", "kothiwal2025htp_DCC_spr.csv", "row=4"), kv("col", "SPR kinetics - KD (nM)"))
    assert get(s, "col") == "SPR kinetics - KD (nM)"
    t = join(kv("col", "a | b"), kv("x", "1"))
    assert get(t, "col") == "a | b" and len(split(t)) == 2

def test_aff_type_column_example():
    s = "SRC_R12 | f.csv | row=123 | col=affinity | affinity_type=ka (1/Ms)"
    assert get(s, "affinity_type") == "ka (1/Ms)" and split(s)[0] == "SRC_R12"

def test_step_and_missing_key():
    assert step("trim", "n_len=22") == "step=trim | n_len=22"
    assert get(step("trim"), "step") == "trim" and get(step("trim"), "nope") is None

def test_newline_in_value_becomes_space():
    assert kv("k", "a\nb") == "k=a b"
```

- [ ] **Step 4: 运行，确认失败**

Run: `[host] pytest etl/core/test_lineage.py -v`
Expected: FAIL，`ModuleNotFoundError: etl.core.lineage`。

- [ ] **Step 5: 实现 `etl/core/lineage.py`**，签名见 Interfaces。转义用反斜杠；`split` 用负向后行断言 `(?<!\\) \| ` 切分。

- [ ] **Step 6: 写 `etl/core/lineage.md`**，说明语法、`step=` 名称约定：merge 的 qa_sample 依据 `trim`、`split`、`mutation_rebuild`、`structure_recover` 四个名称分层，无这四者为 `direct`；其余名称（`seqnorm`、`resolve`、`slot_swap`、`slot_single` 等）自由使用。

- [ ] **Step 7: 运行，确认通过**

Run: `[host] pytest etl/core/test_lineage.py -v`
Expected: 6 passed。

- [ ] **Step 8: Commit**

```bash
[host] git add etl && git commit -m "feat(etl): scaffold, env.sh and lineage"
```

---

### Task 2: ids

**Files:**
- Create: `etl/core/ids.py`、`etl/core/ids.md`、`etl/core/test_ids.py`

**Interfaces:**
- Produces：
```python
ID_VERSION = "v1"
class IdCollision(Exception): ...
def H(s: str) -> str
def ab_canonical(vh: str | None, vl: str | None) -> str      # 即传给 H 的完整字符串，含 "ab/v1:" 前缀
def ag_canonical(chains: Sequence[str]) -> str               # 含 "ag/v1:" 前缀
def ab_id(vh: str | None, vl: str | None) -> str
def ag_id(chains: Sequence[str]) -> str
def three_a_id(ab: str, ag: str) -> str
def check_collisions(pairs: Iterable[tuple[str, str]]) -> None   # (id, canonical)；同 id 对应不同 canonical 则抛 IdCollision
```

- [ ] **Step 1: 写失败的测试**。向量由 host 上的 `sha256sum` 独立算出（不经本模块）：

```python
VH, VL = "EVQLVESGGGLVQPGGSLRLSCAAS", "DIQMTQSPSSLSASVGDRVTITC"
def test_golden_vectors():
    assert ab_id(VH, VL) == "e3530acaf90a5cf523a8b903e5372108"
    assert ab_id(VH, None) == "59f042dd1616144d9f65b9a11841453f"
    assert ab_id(None, VL) == "de2aae6e62343da45bae33b3a8a080eb"
    assert ag_id(["MKTAYIAKQR"]) == "55ed5a94b7b3b6807cce2bb54e47868e"
    assert ag_id(["MKTAYIAKQR", "GSHMLE"]) == "68fc1ebba8e066070e2faaca2d29e264"
    assert three_a_id(ab_id(VH, VL), ag_id(["MKTAYIAKQR"])) == "3aa15df2f9fb69f637d53f45e9843941"
    assert ab_canonical(VH, None) == "ab/v1:" + VH + "<SEP><NONE>"

def test_chain_order_matters():
    assert ag_id(["GSHMLE", "MKTAYIAKQR"]) == "ce1862b24e9e2302a97209f63b878a97"

def test_empty_string_is_none():
    assert ab_id(VH, "") == ab_id(VH, None) == "59f042dd1616144d9f65b9a11841453f"

def test_contract_violations():
    for bad in [lambda: ab_id(None, None), lambda: ab_id("", ""), lambda: ag_id([]),
                lambda: ag_id([""]), lambda: ag_id(["evq"]), lambda: ab_id("EV<SEP>Q", None),
                lambda: ab_id("EVQ1", None)]:
        with pytest.raises(ValueError): bad()

def test_check_collisions():
    check_collisions([("x", "a"), ("x", "a"), ("y", "b")])
    with pytest.raises(IdCollision): check_collisions([("x", "a"), ("x", "b")])
```

- [ ] **Step 2: 运行，确认失败**：`[host] pytest etl/core/test_ids.py -v`，Expected: `ModuleNotFoundError`。

- [ ] **Step 3: 实现 `ids.py`**（hashlib）。序列只接受 `^[A-Z]+$`；空串先转 `None`；`vh` 与 `vl` 都为 `None` 时 `ValueError`。

- [ ] **Step 4: 写 `ids.md`**：说明 canonical 就是传给 `H` 的字符串、版本升级规则（清洗或序列化规则变化时升 `v1`，不原地改写）、`merge` 在规模上用 SQL 做同样的碰撞检查。

- [ ] **Step 5: 运行，确认通过**：Expected: 5 passed。

- [ ] **Step 6: Commit**：`[host] git add etl/core/ids.* etl/core/test_ids.py && git commit -m "feat(etl): ids with golden vectors"`

---

### Task 3: seqnorm

**Files:**
- Create: `etl/core/seqnorm.py`、`etl/core/seqnorm.md`、`etl/core/test_seqnorm.py`

**Interfaces:**
- Consumes: `lineage.step`、`lineage.kv`
- Produces：
```python
class SeqNorm(NamedTuple):
    seq: str | None
    flags: tuple[str, ...]            # 取值：placeholder, gap, unknown_residue, illegal_char, multi_record
    @property
    def lineage(self) -> tuple[str, ...]   # 无 flags 为 ()，否则 (step("seqnorm", kv("flags", "gap,...")),)
def normalize(raw: str | None, placeholders: Collection[str] = ()) -> SeqNorm
```
规则（ab 方案第 2 项）：去掉以 `>` 开头的行（多于一个标题行为 `multi_record`）→ 大写并删除全部空白 → 空为 `placeholder` → 与 `placeholders` 中任一项（忽略大小写）相等为 `placeholder` → 含 `-`、`.`、`*` 为 `gap` → 含非 `A-Z` 字符为 `illegal_char` → `X B Z J U O` 保留序列并加 `unknown_residue`。`placeholder`、`gap`、`illegal_char`、`multi_record` 时 `seq=None`。文本占位符（`NA`、`None`）由 adapter 通过 `placeholders` 传入，模块自身不猜。

- [ ] **Step 1: 写失败的测试**

```python
def test_cleaning_and_fasta_shell():
    assert normalize(" evq lve\n") == ("EVQLVE", ())
    assert normalize(">1ABC_H mol:protein\nEVQL\nVESG\n") == ("EVQLVESG", ())

def test_trailing_stop_and_internal_gap():        # Review Focus 2
    assert normalize("EVQLV*") == (None, ("gap",))
    assert normalize("EVQ-LV") == (None, ("gap",))
    assert normalize("EVQLV*").lineage == ("step=seqnorm | flags=gap",)

def test_unknown_residue_kept():
    assert normalize("EVQXLVB") == ("EVQXLVB", ("unknown_residue",))

def test_illegal_and_multi_record():
    assert normalize("EVQ1LV") == (None, ("illegal_char",))
    assert normalize(">a\nEVQ\n>b\nLVE") == (None, ("multi_record",))

def test_placeholders():
    for raw in [None, "", "  \n"]: assert normalize(raw) == (None, ("placeholder",))
    assert normalize("NA") == ("NA", ())
    assert normalize("na", placeholders={"NA"}) == (None, ("placeholder",))
```

- [ ] **Step 2: 运行，确认失败**：`[host] pytest etl/core/test_seqnorm.py -v`，Expected: `ModuleNotFoundError`。
- [ ] **Step 3: 实现 `normalize`**（正则与字符串方法即可）。
- [ ] **Step 4: 写 `seqnorm.md`**：写明 adapter 对源特有外壳（尾部 `*`、`NA` 占位）在调用前自行处理，并列出本模块返回的全部 flag。
- [ ] **Step 5: 运行，确认通过**：Expected: 5 passed。
- [ ] **Step 6: Commit**：`[host] git add etl/core/seqnorm.* etl/core/test_seqnorm.py && git commit -m "feat(etl): seqnorm"`

---

### Task 4: resolve

**Files:**
- Create: `etl/core/resolve.py`、`etl/core/resolve.md`、`etl/core/test_resolve.py`

**Interfaces:**
- Consumes: `lineage.kv`
- Produces：
```python
LEVELS = ("source_native", "source_fasta_or_rebuilt", "structure_canonical", "structure_observed", "external_accession")
@dataclass(frozen=True)
class Candidate: source: str; value: object
@dataclass(frozen=True)
class Resolved:
    selected: Candidate | None
    candidates: tuple[Candidate, ...]            # 按 order 的优先级，同级保持输入顺序
    conflict: bool                               # 不同 value 多于一种
    def lineage_frags(self) -> list[str]         # ["resolved=<source>|none", "candidates=src:val;src:val", "conflict=1"(仅冲突时)]
def resolve(candidates: Sequence[Candidate], order: Sequence[str],
            on_tie: Literal["pick_top", "reject"],
            tie_break: Callable[[Sequence[Candidate]], Candidate | None] | None = None) -> Resolved
```
语义：取 `order` 中最高且有候选的一级；该级只有一种 value 则选中；同级有多种 value 为 tie：`reject` 返回 `selected=None`，`pick_top` 用 `tie_break` 选，没有 `tie_break` 取该级输入顺序第一个。`source` 不在 `order` 中抛 `ValueError`。`LEVELS` 是抗原与结构序列证据的统一词表（ag 方案第 6 项的优先级）。

- [ ] **Step 1: 写失败的测试**

```python
ORDER = ["source", "structure"]
def test_higher_level_wins_and_conflict_recorded():
    r = resolve([Candidate("structure", "AAA"), Candidate("source", "AAB")], ORDER, "reject")
    assert r.selected == Candidate("source", "AAB") and r.conflict
    assert r.lineage_frags() == ["resolved=source", "candidates=source:AAB;structure:AAA", "conflict=1"]

def test_agreement_has_no_conflict():
    r = resolve([Candidate("source", "AAA"), Candidate("structure", "AAA")], ORDER, "reject")
    assert not r.conflict and r.lineage_frags() == ["resolved=source", "candidates=source:AAA;structure:AAA"]

def test_same_level_tie():
    cs = [Candidate("source", "AAAA"), Candidate("source", "AA")]
    assert resolve(cs, ORDER, "reject").selected is None
    assert resolve(cs, ORDER, "pick_top").selected.value == "AAAA"
    assert resolve(cs, ORDER, "pick_top", tie_break=lambda c: min(c, key=lambda x: len(x.value))).selected.value == "AA"

def test_empty_and_unknown_source():
    assert resolve([], ORDER, "reject") == Resolved(None, (), False)
    with pytest.raises(ValueError): resolve([Candidate("web", "A")], ORDER, "reject")
```

- [ ] **Step 2: 运行，确认失败**：`[host] pytest etl/core/test_resolve.py -v`，Expected: `ModuleNotFoundError`。
- [ ] **Step 3: 实现**。
- [ ] **Step 4: 写 `resolve.md`**：列出各调用点的配置（ab 方案第 3–5 项 `pick_top`；第 6 项同级取两侧域有效且未解释片段最短者，`pick_top` 加 `tie_break`；ag 方案第 6 项 `reject`），并说明首版只有 ANARCI 一个工具，"多工具一致"层不可达。
- [ ] **Step 5: 运行，确认通过**：Expected: 4 passed。
- [ ] **Step 6: Commit**：`[host] git add etl/core/resolve.* etl/core/test_resolve.py && git commit -m "feat(etl): resolve"`

---

### Task 5: vdomain

**Files:**
- Create: `etl/core/vdomain.py`、`etl/core/vdomain.md`、`etl/core/test_vdomain.py`

**Interfaces:**
- Consumes: `lineage.step`、`lineage.kv`、`resolve.resolve`、`resolve.Candidate`
- Produces：
```python
LINKERS = ("GGGGSGGGGSGGGGS", "GGGGSGGGGSGGGGSGGGGS")      # 另匹配 (GGGGS)+ 重复
TAGS = {"His6": "HHHHHH", "FLAG": "DYKDDDDK", "HA": "YPYDVPDYA", "Myc": "EQKLISEEDL",
        "V5": "GKPIPNPLLGLDST", "StrepII": "WSHPQFEK", "AviTag": "GLNDIFEAQKIEWHE",
        "TwinStrep": "WSHPQFEKGGGSGGGSGGSAWSHPQFEK"}
@dataclass(frozen=True)
class Hints: linker: str | None = None; spans: tuple[tuple[int, int], ...] | None = None   # 0 起，右开，坐标同输入序列
@dataclass(frozen=True)
class Domain:
    start: int; end: int; chain_type: str                    # "H" | "K" | "L"
    residue_index: Mapping[tuple[int, str], int]             # IMGT (编号, 插入码) -> 输入序列的 0 起下标，不含 gap
@dataclass(frozen=True)
class Parse: seq: str; domains: tuple[Domain, ...]           # 按 start 升序
@dataclass(frozen=True)
class Construct: vh: str | None; vl: str | None; reason: str | None; lineage: tuple[str, ...]
def parse(seq: str, hints: Hints | None = None) -> Parse                  # lru_cache 包一层，同序列只跑一次 ANARCI
def parse_batch(seqs: Sequence[str], hints: Sequence[Hints | None] | None = None) -> list[Parse]   # 一次 ANARCI 调用，ncpu=1
def derive(p: Parse, hints: Hints | None = None) -> Construct
def to_fv(seq: str, hints: Hints | None = None) -> Construct              # derive(parse(seq, hints), hints)
def pair_slots(h: str | None, l: str | None, h_hints: Hints | None = None, l_hints: Hints | None = None) -> Construct
```
`reason` 取值：`None`（成功）、`no_domain`、`slot_collision`、`unresolved`。ANARCI 以 IMGT 编号运行，`allow={"H","K","L"}`（TCR 链型视为无域）。

派生规则（blueprint §3，不得改写）：
- 0 个域：`no_domain`。
- 1 个域：H → `vh`，K/L → `vl`，另一槽 `None`。VHH 与普通 VH-only 不区分，只写 lineage。
- 2 个域且恰为一条 H 加一条 K/L：两域之间的残余必须是 linker（`hints.linker`、`LINKERS`、`(GGGGS)+` 之一），否则 `unresolved`。VL-linker-VH 时按链型换入 `vh`、`vl`，lineage 写 `orientation=VL-VH`。
- 其他（同类型两域、多于 2 域）：`unresolved`。
- `pair_slots`：两槽不同且都不是完整 scFv，逐槽 `to_fv`，H 槽要得 H、L 槽要得 K/L；两槽恰好反过来则互换并写 `step=slot_swap`；两槽同为 H 或同为 K/L 为 `unresolved`。两槽规范化后相同：该序列 `to_fv` 得到 scFv 则按单链处理并写 `step=slot_single`（保留两个槽位），否则 `slot_collision`。只有一槽非空：`to_fv` 该槽。一槽是 scFv、另一槽不同序列：`unresolved`。
- lineage 元素：有裁剪时 `step=trim | span=<start>-<end> | n_len=<n> | c_len=<n> | c_tag=<TAGS 名，无则省略>`（按 `TAGS` 序列长度降序匹配，已被较长标签覆盖的区段不再匹配，多个标签按在残余中的位置用 `+` 连接）；scFv 时 `step=split | orientation=VH-VL|VL-VH | linker=<序列>`；`pair_slots` 的 `slot_swap`、`slot_single` 元素置于 lineage 首位。
- `hints.spans` 给出时：对每个 span 的子序列运行 ANARCI，找不到域则该 span 视为无域；找到则域边界取 span（来源边界优先），ANARCI 自己的边界与之不同时 lineage 追加 `conflict=1 | anarci_span=<s>-<e>`。

- [ ] **Step 1: 取真实序列**。在 host 上用 DuckDB 读 inventory 指明的文件，各取一条：R08 一条带信号肽与 `HHHHHH` 的 VHH（`R08_VHH`）；R74 一条末尾为 `HHHHHH` 的完整突变重链（`R74_HEAVY`）；R76 一条 H、L 槽规范化后相同且含 `GGGGSGGGGSGGGGS` 的行（21 行中的 15 行之一，`R76_SCFV`）；R76 一条正常的 H/L 对（`R76_H`、`R76_L`）。再用已安装的 `anarci` 直接取出该 H/L 对的 VH、VL 域序列（`R76_VH`、`R76_VL`），另取一条不同的 R76 重链（`R76_H2`）。把序列字面量写入测试文件。

- [ ] **Step 2: 写失败的测试**（序列用 Step 1 的字面量）

```python
def test_vhh_signal_peptide_and_his_tag():                    # R08
    c = to_fv(R08_VHH)
    assert c.reason is None and c.vl is None and c.vh in R08_VHH and 100 < len(c.vh) < 140
    assert get(c.lineage[0], "c_tag") == "His6" and 18 <= int(get(c.lineage[0], "n_len")) <= 26

def test_full_heavy_with_constant_and_his_tag():              # R74
    c = to_fv(R74_HEAVY)
    assert c.vh is not None and get(c.lineage[0], "c_tag") == "His6" and int(get(c.lineage[0], "c_len")) > 50

def test_scfv_with_g4s_linker_splits():                       # R76 slot-identical row
    c = to_fv(R76_SCFV)
    assert c.reason is None and c.vh and c.vl
    assert get(c.lineage[-1], "step") == "split" and get(c.lineage[-1], "linker") == "GGGGSGGGGSGGGGS"

def test_reversed_scfv_swaps_into_fields():                   # 用 R76 正常 H/L 对拼 VL+linker+VH
    c = to_fv(R76_VL + "GGGGSGGGGSGGGGS" + R76_VH)
    assert (c.vh, c.vl) == (R76_VH, R76_VL) and get(c.lineage[-1], "orientation") == "VL-VH"

def test_unknown_linker_is_unresolved_unless_hinted():
    s = R76_VH + "AAAAAAAAAAAA" + R76_VL
    assert to_fv(s).reason == "unresolved"
    assert to_fv(s, Hints(linker="AAAAAAAAAAAA")).reason is None

def test_pair_slots_cases():
    assert pair_slots(R76_H, R76_L).reason is None
    assert pair_slots(R76_L, R76_H).lineage[0].startswith("step=slot_swap")
    assert pair_slots(R76_H, R76_H).reason == "slot_collision"
    assert pair_slots(R76_SCFV, R76_SCFV).lineage[0].startswith("step=slot_single")
    assert pair_slots(R76_H, R76_H2).reason == "unresolved"       # 另一条不同的 H
    assert pair_slots(R76_H, None).vl is None and pair_slots(None, R76_L).vh is None

def test_unnumberable_inputs_return_no_domain():              # Review Focus 3
    for s in ["", "A" * 8, "GGGGSGGGGS", NON_ANTIBODY_PROTEIN]:
        assert to_fv(s).reason == "no_domain"

def test_hint_span_overrides_anarci_and_records_conflict():
    d = parse(R74_HEAVY).domains[0]
    c = to_fv(R74_HEAVY, Hints(spans=((d.start, d.end + 2),)))
    assert c.vh == R74_HEAVY[d.start:d.end + 2] and get(c.lineage[0], "conflict") == "1"

def test_parse_batch_matches_single():
    seqs = [R76_H, R76_L, R08_VHH, R74_HEAVY]
    assert [(p.domains[0].start, p.domains[0].end) for p in parse_batch(seqs)] == \
           [(parse(s).domains[0].start, parse(s).domains[0].end) for s in seqs]
```
`NON_ANTIBODY_PROTEIN` 取任一 R76 行的抗原链。

- [ ] **Step 3: 运行，确认失败**：`[host] pytest etl/core/test_vdomain.py -v`，Expected: `ModuleNotFoundError`。
- [ ] **Step 4: 实现**。`parse_batch` 调 `anarci.anarci(...)`，从返回的编号结果取每个域的起止与 `((pos, ins), aa)` 列表（先读已安装版本的签名再绑定）；`derive` 与 `pair_slots` 按上述规则；`parse` 加 `functools.lru_cache(maxsize=100_000)`。
- [ ] **Step 5: 运行，确认通过**：Expected: 全部 passed。
- [ ] **Step 6: 实测覆盖**。在 host 上对 R08、R74、R76、R77 的全部 distinct 抗体序列（含 scFv 与 VHH）跑 `parse_batch`（multiprocessing，不超过 32 进程；一次性脚本不入库），统计各 SRC 的 `no_domain`、`unresolved` 占比与 `to_fv` 成功率。
- [ ] **Step 7: 写 `vdomain.md`**：三节外加 `## 实测覆盖`，填入 Step 6 的表（SRC、distinct 序列数、`no_domain` 数与占比、ANARCI 版本、日期），并写明结论：占比是否不可接受、是否需要第二个工具（blueprint §3 的判据：某 SRC 无来源边界且 `no_domain` 占比不可接受）。示例写 Daft 用法：`@daft.func.batch(..., batch_size=500, use_process=True)` 内调 `parse_batch`。
- [ ] **Step 8: Commit**：`[host] git add etl/core/vdomain.* etl/core/test_vdomain.py && git commit -m "feat(etl): vdomain with measured ANARCI coverage"`

---

### Task 6: structref

**Files:**
- Create: `etl/core/structref.py`、`etl/core/structref.md`、`etl/core/test_structref.py`

**Interfaces:**
- Consumes: `resolve.resolve`、`resolve.Candidate`、`resolve.LEVELS`、`lineage.step`、`lineage.kv`
- Produces：
```python
class StructureNotFound(Exception): ...
@dataclass(frozen=True)
class ChainRecord:
    chain_id: str                                    # 作者链号
    entity_id: str
    is_protein: bool
    full_seq: str                                    # entity SEQRES，单字母，非标准残基为 X；无 SEQRES 时等于 observed_seq
    observed_seq: str                                # 有坐标的残基，按链顺序
    index_of: Mapping[tuple[int, str], int]          # 作者 (残基号, 插入码) -> full_seq 的 0 起下标
    def observed_segments(self) -> tuple[str, ...]   # 按 full_seq 下标连续的已观察片段
    def consistent_with(self, seq: str) -> bool      # 每个已观察片段都在 seq 中出现
@dataclass(frozen=True)
class Structure:
    structure_id: str; requested_id: str; replaced_from: str | None
    file: Path; sha256: str
    chains: Mapping[str, ChainRecord]
    lineage: tuple[str, ...]
def open_structure(ref: str | Path, cache_dir: Path | None = None) -> Structure
def pick_sequence(rec: ChainRecord, source: str | None = None, fasta: str | None = None) -> tuple[str | None, tuple[str, ...]]
```
`open_structure`：`ref` 是现有文件路径（SRC 自带快照，优先）则直接解析；否则当 PDB ID 处理——先查 `cache_dir`（默认 `$RCSB_CACHE`）下的 `<ID>.cif`，未命中则经 `ETL_PROXY` 从 `https://files.rcsb.org/download/<ID>.cif` 下载，原子写入缓存。下载 404 时查 `https://data.rcsb.org/rest/v1/holdings/removed/<ID>` 的 `rcsb_repository_holdings_removed.id_codes_replaced_by`（已在 host 上验证：`3RVV` → `["5VPL"]`），恰好一个替代则改取它并令 `replaced_from=<ID>`，lineage 写 `step=structure_open | replaced_from=3RVV | structure_id=5VPL`；其余情形抛 `StructureNotFound`。代理只用于 RCSB，不设全局代理。
`pick_sequence`：按 `resolve.LEVELS` 前四级（`source_native` ← `source`，`source_fasta_or_rebuilt` ← `fasta`，`structure_canonical` ← `rec.full_seq`，`structure_observed` ← `rec.observed_seq`）用 `resolve(..., on_tie="pick_top")`；结果来自后两级时 lineage 含 `step=structure_recover`。空串候选忽略；只接受唯一映射，不从结构缺口补残基。

- [ ] **Step 1: 写失败的测试**

```python
@pytest.mark.data
def test_snapshot_3BDY_pdb():                                  # R14 自带快照
    s = open_structure(R14_DIR / "AB-Bind-Database" / "3BDY.pdb")
    h = s.chains["H"]
    assert (len(h.full_seq), len(h.observed_seq)) == (230, 216)
    assert sum(map(len, h.observed_segments())) == 216 and len(h.index_of) == 216
    assert h.consistent_with(h.full_seq) and not h.consistent_with("A" * 230)

@pytest.mark.network
def test_rcsb_1N8Z_lengths(tmp_path):
    s = open_structure("1N8Z", cache_dir=tmp_path)
    assert sorted(len(c.full_seq) for c in s.chains.values()) == [214, 220, 607]
    her2 = next(c for c in s.chains.values() if len(c.full_seq) == 607)
    assert len(her2.observed_seq) == 581

@pytest.mark.network
def test_obsolete_ids_resolve(tmp_path):
    for old, new in [("3RVV", "5VPL"), ("3RVW", "5VPG")]:
        s = open_structure(old, cache_dir=tmp_path)
        assert (s.structure_id, s.replaced_from) == (new, old) and f"replaced_from={old}" in s.lineage[0]

@pytest.mark.network
def test_cache_hit_needs_no_network(tmp_path, monkeypatch):
    open_structure("1N8Z", cache_dir=tmp_path)
    monkeypatch.setenv("ETL_PROXY", "http://127.0.0.1:9")
    assert open_structure("1N8Z", cache_dir=tmp_path).structure_id == "1N8Z"

@pytest.mark.network
def test_dna_chain_is_not_protein_and_unknown_id_raises(tmp_path):
    assert not any(c.is_protein for c in open_structure("1BNA", cache_dir=tmp_path).chains.values())
    with pytest.raises(StructureNotFound): open_structure("0ZZZ", cache_dir=tmp_path)

def test_pick_sequence_priority():
    rec = ChainRecord("H", "1", True, "ABCDEFG", "ABCEFG", {}, )
    assert pick_sequence(rec, source="XBCDEFG")[0] == "XBCDEFG"
    seq, lin = pick_sequence(rec)
    assert seq == "ABCDEFG" and lin[0].startswith("step=structure_recover")
    assert pick_sequence(ChainRecord("H", "1", True, "", "ABCEFG", {}))[0] == "ABCEFG"
```

- [ ] **Step 2: 运行，确认失败**：`[host] pytest etl/core/test_structref.py -v`，Expected: `ModuleNotFoundError`。
- [ ] **Step 3: 实现**。解析用 gemmi（PDB 与 mmCIF 同一入口，先 `setup_entities()`）；下载用标准库 `urllib` 加显式 `ProxyHandler({"https": ETL_PROXY})`。
- [ ] **Step 4: 写 `structref.md`**：写明作者编号是 `index_of` 的编号方案（SKEMPI、AB-Bind 突变用它），R50 的作者重编号快照按它映射；`Structure.sha256` 供调用方放入缓存键；覆盖信息为 `len(observed_seq)` 对 `len(full_seq)`。
- [ ] **Step 5: 运行，确认通过**：Expected: 全部 passed。
- [ ] **Step 6: Commit**：`[host] git add etl/core/structref.* etl/core/test_structref.py && git commit -m "feat(etl): structref"`

---

### Task 7: mutate

**Files:**
- Create: `etl/core/mutate.py`、`etl/core/mutate.md`、`etl/core/test_mutate.py`

**Interfaces:**
- Consumes: `vdomain.parse`、`vdomain.to_fv`、`vdomain.Domain`、`structref.open_structure`、`structref.ChainRecord`、`seqnorm.normalize`、`lineage.step`、`lineage.kv`
- Produces：
```python
class Edit(NamedTuple):
    id: str; chain: str; orig: str; pos: int; new: str; numbering: str; ins: str = ""   # chain="" 表示未指定
@dataclass(frozen=True)
class ParentChain:
    seq: str
    numberings: Mapping[str, Mapping[tuple[int, str], int]] = field(default_factory=dict)  # "seq_1based" 内置
@dataclass(frozen=True)
class PointResult:
    cls: Literal["B", "C"]; chains: dict[str, str] | None; reason: str | None
    lineage: tuple[str, ...]; sites: tuple[tuple[str, str, int], ...]   # (edit.id, 链, 0 起下标)
@dataclass(frozen=True)
class RegionResult: vh: str | None; vl: str | None; reason: str | None; lineage: tuple[str, ...]
def apply_point(entity: Literal["ab", "ag"], parent: Mapping[str, ParentChain], edits: Sequence[Edit]) -> PointResult
def apply_region(parent_h: str, parent_l: str | None, span: tuple[int, int], replacement: str,
                 chain: Literal["H", "L"] = "H") -> RegionResult
```
粘合示例（写入 md）：`ParentChain(rec.full_seq, {"pdb_author": rec.index_of})`；`ParentChain(seq, {"imgt": dom.residue_index})`。

`apply_point` 规则（ab 方案第 9 项 A/B/C）：A 类（来源已给完整序列）不经本函数。每个 edit 的候选链为 `edit.chain`，为空则取全部 parent 链；候选必须同时满足编号方案存在、`(pos, ins)` 可映射、该位残基等于 `orig`，且全体候选恰好一个才接受。`reason` 取值：`no_numbering`、`unmapped_position`、`orig_mismatch`、`ambiguous_chain`、`conflicting_edits`（同链同位两个 edit）、`unsupported_edit`（`new` 不是单个 `A-Z` 字母）。空 `edits` 返回 `cls="B"`，链原样，`lineage=()`。成功时 `lineage=(step("mutation_rebuild", kv("entity", entity), "class=B", kv("numbering", ...), kv("edits", "H:S52A>G,...")),)`，其中每项格式为 `<链>:<orig><pos><ins>><new>`。长度不变，调用方可按位置继承可变域边界。
`apply_region` 规则（R75：IMGT 107–116，闭区间）：对 `parent_h`（`chain="L"` 时对 `parent_l`）跑 `vdomain.parse`，须恰好一个对应链型的域，取该域中 `(107,"")` 到 `(116,"")` 之间（按序列顺序，含插入码）的下标区间替换为 `replacement`，不校验被替换区间的原残基；再对新链 `parse`，要求仍是同一链型的一个域且区间外的残基与 parent 逐位相同。返回 parent 的 VH 与 VL 域序列，被替换的一条换成新序列，另一条原样。`reason`：`no_domain`、`region_boundary_missing`（107 或 116 缺位）、`bad_replacement`（`seqnorm` 不返回非空序列）、`region_mismatch`。

- [ ] **Step 1: 取真实突变**。读 R14 的突变表，选一条作用于 `3BDY` 抗体链的点突变，其 `orig` 与 `3BDY.pdb` 该位残基一致；写入测试。

- [ ] **Step 2: 写失败的测试**

```python
@pytest.mark.data
def test_point_mutation_on_real_parent():                      # R14 / 3BDY
    rec = open_structure(R14_3BDY).chains[CHAIN]
    r = apply_point("ab", {CHAIN: ParentChain(rec.full_seq, {"pdb_author": rec.index_of})}, [EDIT])
    i = rec.index_of[(EDIT.pos, EDIT.ins)]
    assert r.cls == "B" and r.chains[CHAIN][i] == EDIT.new
    assert r.chains[CHAIN][:i] + r.chains[CHAIN][i + 1:] == rec.full_seq[:i] + rec.full_seq[i + 1:]
    assert r.sites == ((EDIT.id, CHAIN, i),) and r.lineage[0].startswith("step=mutation_rebuild | entity=ab | class=B")

def test_c_class_reasons():
    p = {"H": ParentChain("ACDEFGHIK", {"pdb_author": {(n, ""): n - 1 for n in range(1, 10)}})}
    e = lambda **k: Edit("m", **{"chain": "H", "orig": "C", "pos": 2, "new": "A", "numbering": "pdb_author", **k})
    assert apply_point("ab", p, [e(orig="D")]).reason == "orig_mismatch"
    assert apply_point("ab", p, [e(pos=99)]).reason == "unmapped_position"
    assert apply_point("ab", p, [e(numbering="imgt")]).reason == "no_numbering"
    assert apply_point("ab", p, [e(new="AG")]).reason == "unsupported_edit"
    assert apply_point("ab", p, [e(), e(new="G")]).reason == "conflicting_edits"
    assert apply_point("ab", p, [e(orig="D")]).chains is None

def test_empty_edits_is_wt():
    p = {"H": ParentChain("ACDE")}
    r = apply_point("ab", p, [])
    assert r.cls == "B" and r.chains == {"H": "ACDE"} and r.lineage == ()

def test_insertion_code_position():                            # Review Focus 4
    p = {"H": ParentChain("ACDE", {"pdb_author": {(52, ""): 1, (52, "A"): 2}})}
    e = Edit("m", "H", "D", 52, "G", "pdb_author", "A")
    assert apply_point("ab", p, [e]).chains == {"H": "ACGE"}
    assert apply_point("ab", p, [e._replace(ins="", orig="C")]).chains == {"H": "AGDE"}

def test_empty_chain_ambiguous_is_C():                         # Review Focus 4
    n = {"pdb_author": {(1, ""): 0}}
    p = {"A": ParentChain("CD", n), "B": ParentChain("CD", n)}
    e = Edit("m", "", "C", 1, "G", "pdb_author")
    assert apply_point("ag", p, [e]).reason == "ambiguous_chain"
    assert apply_point("ag", p, [e._replace(chain="B")]).chains == {"A": "CD", "B": "GD"}

def test_seq_1based_builtin():
    r = apply_point("ag", {"A": ParentChain("MKTAY")}, [Edit("m", "A", "T", 3, "S", "seq_1based")])
    assert r.chains == {"A": "MKSAY"}

@pytest.mark.network
def test_region_replace_1N8Z_cdrh3(tmp_path):
    s = open_structure("1N8Z", cache_dir=tmp_path)
    H = next(c for c in s.chains.values() if len(c.full_seq) == 220).full_seq
    L = next(c for c in s.chains.values() if len(c.full_seq) == 214).full_seq
    r = apply_region(H, L, (107, 116), "ARDYYGSSYF")
    assert r.reason is None and "ARDYYGSSYF" in r.vh and r.vl == to_fv(L).vl
    assert len(r.vh) == len(to_fv(H).vh)                       # 107–116 无插入码时长度不变
    assert apply_region(H, L, (107, 116), "ar1").reason == "bad_replacement"
    assert apply_region("GGGG", L, (107, 116), "ARDYYGSSYF").reason == "no_domain"
```

- [ ] **Step 3: 运行，确认失败**：`[host] pytest etl/core/test_mutate.py -v`，Expected: `ModuleNotFoundError`。
- [ ] **Step 4: 实现**。
- [ ] **Step 5: 确认区间边界**。在 host 上打印 `1N8Z` 重链 IMGT 105–117 的残基，确认 107–116 是 10 个编号位且位于 CDR-H3；若不是，改测试中的区间并回报给 Pthahnix（blueprint 要求该区间用 `1N8Z` 实测确认）。
- [ ] **Step 6: 写 `mutate.md`**：写明 `region` 区间的实测结果、`chain=""` 的搜索规则、同源多链要由 adapter 展开成每链一个 `Edit`、突变落在被 `vdomain` 裁掉的区段时清洗后序列与 parent 相同（落入同一 `AB_ID`）并以 `sites` 写入 lineage。
- [ ] **Step 7: 运行，确认通过**：Expected: 全部 passed。
- [ ] **Step 8: Commit**：`[host] git add etl/core/mutate.* etl/core/test_mutate.py && git commit -m "feat(etl): mutate point and region modes"`

---

### Task 8: antigen_bound

**Files:**
- Create: `etl/core/antigen_bound.py`、`etl/core/antigen_bound.md`、`etl/core/test_antigen_bound.py`

**Interfaces:**
- Consumes: `resolve.resolve`、`resolve.Candidate`、`resolve.LEVELS`、`lineage.step`、`lineage.kv`、`structref.ChainRecord`（测试里）
- Produces：
```python
@dataclass(frozen=True)
class SeqCandidate: level: str; seq: str                  # level ∈ resolve.LEVELS
@dataclass(frozen=True)
class Boundary: level: str; start: int; end: int; label: str   # 0 起右开，坐标在选中的序列上；label 如 signal_peptide、tag、mature_chain、domain
@dataclass(frozen=True)
class Chain:
    key: str                                              # 记录内唯一，如链号
    is_protein: bool = True
    order: int | None = None                              # 来源明确的链位置
    entity: str | None = None                             # 结构 entity 号
    candidates: tuple[SeqCandidate, ...] = ()
    boundaries: tuple[Boundary, ...] = ()
    observed_segments: tuple[str, ...] | None = None      # 来自 ChainRecord.observed_segments()，仅用于一致性核对
@dataclass(frozen=True)
class Bound: chains: tuple[str, ...] | None; keys: tuple[str, ...]; reason: str | None; lineage: tuple[str, ...]
def bound(chains: Sequence[Chain]) -> Bound
```
规则（ag 方案第 3、4、6 项落成代码）：
1. 任一链 `is_protein=False`：`reason="non_protein"`。链集合为空：`no_sequence`。
2. 每条链的序列：对 `candidates` 做 `resolve(order=LEVELS, on_tie="reject")`。同级冲突 `sequence_conflict`；无候选 `no_sequence`。存在冲突时追加 lineage 元素 `step=resolve | chain=<key> | <resolve.lineage_frags() 的各片段>`。
3. 每条链的边界：`boundaries` 按 `LEVELS` 做 `resolve(on_tie="reject")`，同级不同 `(start,end)` 为 `boundary_ambiguous`；`0 <= start < end <= len(序列)` 不成立为 `boundary_out_of_range`。按选中边界裁剪，lineage 元素 `step=trim | chain=<key> | span=<s>-<e> | label=<label> | removed_n=<n> | removed_c=<n>`；无边界则整条保留。
4. 结构核对：`observed_segments` 给出时，每个片段都出现在选中序列中为 `structure=consistent`，否则 `structure=mismatch`，写成 lineage 元素 `step=structure_check | chain=<key> | structure=consistent|mismatch`；不一致只记录，不排除，序列以来源为准。
5. 链序：所有链都有 `order` 时按 `order` 排，`order` 重复为 `order_ambiguous`；部分有部分无为 `order_ambiguous`；都没有时按 `(entity, key)` 的字典序。相同序列的链不去重。
6. 成功时 `chains` 为按链序排列的裁剪后序列，`keys` 为对应的链 key。

- [ ] **Step 1: 写失败的测试**（含 1 个结构真实数据）

```python
def C(key, seq, **k): return Chain(key, candidates=(SeqCandidate("source_native", seq),), **k)

def test_trim_by_source_boundary():
    c = Chain("A", candidates=(SeqCandidate("source_native", "MKYLLPTAAAGLLLLAAQPAMA" + "DKTHTCPPCP"),),
              boundaries=(Boundary("source_native", 22, 32, "mature_chain"),))
    b = bound([c])
    assert b.chains == ("DKTHTCPPCP",) and "step=trim" in b.lineage[0] and "removed_n=22" in b.lineage[0]

def test_homodimer_keeps_both_chains():                         # Review Focus 5
    b = bound([C("B", "MKTAYIAKQR", entity="1"), C("A", "MKTAYIAKQR", entity="1")])
    assert b.chains == ("MKTAYIAKQR", "MKTAYIAKQR") and b.keys == ("A", "B")

def test_order_rules():
    assert bound([C("A", "AAA", order=2), C("B", "BBB", order=1)]).chains == ("BBB", "AAA")
    assert bound([C("A", "AAA", order=1), C("B", "BBB")]).reason == "order_ambiguous"
    assert bound([C("A", "AAA", order=1), C("B", "BBB", order=1)]).reason == "order_ambiguous"

def test_exclusions():
    assert bound([Chain("D", is_protein=False)]).reason == "non_protein"
    assert bound([]).reason == "no_sequence" and bound([Chain("A")]).reason == "no_sequence"
    two = Chain("A", candidates=(SeqCandidate("source_native", "AAA"), SeqCandidate("source_native", "AAB")))
    assert bound([two]).reason == "sequence_conflict"
    amb = Chain("A", candidates=(SeqCandidate("source_native", "AAAAA"),),
                boundaries=(Boundary("source_native", 0, 3, "domain"), Boundary("source_native", 1, 4, "domain")))
    assert bound([amb]).reason == "boundary_ambiguous"
    oor = Chain("A", candidates=(SeqCandidate("source_native", "AAA"),), boundaries=(Boundary("source_native", 0, 9, "domain"),))
    assert bound([oor]).reason == "boundary_out_of_range"

def test_higher_level_wins_and_structure_mismatch_is_recorded_not_fatal():
    c = Chain("A", candidates=(SeqCandidate("source_native", "AAAA"), SeqCandidate("structure_canonical", "AAAB")),
              observed_segments=("BB",))
    b = bound([c])
    assert b.chains == ("AAAA",) and "structure=mismatch" in " ".join(b.lineage) and "conflict=1" in " ".join(b.lineage)

@pytest.mark.network
def test_her2_from_1N8Z_observed_segments_are_consistent(tmp_path):
    rec = next(c for c in open_structure("1N8Z", cache_dir=tmp_path).chains.values() if len(c.full_seq) == 607)
    b = bound([Chain(rec.chain_id, candidates=(SeqCandidate("structure_canonical", rec.full_seq),),
                     observed_segments=rec.observed_segments())])
    assert b.chains == (rec.full_seq,) and "structure=consistent" in " ".join(b.lineage)
```

- [ ] **Step 2: 运行，确认失败**：`[host] pytest etl/core/test_antigen_bound.py -v`，Expected: `ModuleNotFoundError`。
- [ ] **Step 3: 实现**。
- [ ] **Step 4: 写 `antigen_bound.md`**：把上面六条规则连同 ag 方案第 3、4、6 项的出处写成可编码的规则表，并写明三件事：非蛋白实体（DNA/RNA、配体、离子）整体排除；排除码是默认处置，某个码命中一个 SRC 的大部分记录时说明条件与该 SRC 不符，由 cc 现场调整并记入 lineage；`bound` 不判断链是否属于实验抗原，这由 adapter 与决策文件决定。
- [ ] **Step 5: 运行，确认通过**：Expected: 全部 passed。
- [ ] **Step 6: Commit**：`[host] git add etl/core/antigen_bound.* etl/core/test_antigen_bound.py && git commit -m "feat(etl): antigen_bound"`

---

### Task 9: merge（含 stats、qa_sample、manifest）

**Files:**
- Create: `etl/core/merge.py`、`etl/core/merge.md`、`etl/core/test_merge.py`

**Interfaces:**
- Consumes: `ids.ab_id`、`ids.ag_id`、`ids.three_a_id`、`ids.IdCollision`、`lineage.split`、`lineage.get`
- Produces：
```python
PAIR_SCHEMA: pa.Schema     # assemble 的输出，每个 SRC 一组 Parquet
# src str, record_key str, AB_ID str, AG_ID str, 3A_ID str, vh str, vl str,
# ab_structure struct<structure_id str, file_ref str, chain_map str(JSON)>, ab_structure_rank int32, ab_lineage list<str>,
# ag_sequence list<str>, ag_structure struct<...同上>, ag_structure_rank int32, ag_lineage list<str>,
# obs list<struct<label str, assay str, condition str, replicate str, lineage list<str>>>
OUT_SCHEMA: pa.Schema      # 3A_ID, antibody{AB_ID, vh_sequence, vl_sequence, structure, lineage}, antigen{AG_ID, sequence, structure, lineage}, affinity[{label, assay, condition, replicate, lineage}]
REJECT_SCHEMA: pa.Schema   # stage, reason_code, src, key, detail（均为 str，detail 为 JSON）
@dataclass(frozen=True)
class MergeReport: n_pairs: int; n_3a: int; n_obs: int; n_rejected: int   # n_pairs 为有效 pair 行数；n_rejected 为本阶段写入 reject_log 的行数
def merge(pair_glob: str, out_dir: Path, *, reject_glob: str | None = None, shards: int = 16,
          qa_seed: int = 0, qa_per_stratum: int = 50, decision_files: Sequence[Path] = (),
          rules_version: str = "v1") -> MergeReport
```
输出布局：`out_dir/3a/part-<k>.parquet`（processed dataset 只有这一项）、`out_dir/stats/{coverage,rejects,label_types,overlap}.parquet`、`out_dir/qa_sample.parquet`、`out_dir/reject_log.parquet`、`out_dir/manifest.json`。

行为：
1. 有效性：`vh`、`vl` 全空，或 `ag_sequence` 为空或含空串，或 `obs` 为空，或有 `label` 为 `None`，则该 pair 不进 `3a`，写 `reject_log(stage="merge", reason_code="invalid_3a", src, key=record_key, detail=JSON)`，不中止。
2. ID 校验（对有效 pair）：SQL 校验同一 `AB_ID`/`AG_ID`/`3A_ID` 只对应一个 canonical（`(vh,vl)`、`ag_sequence`、`(AB_ID,AG_ID)`），并对 distinct 行用 `ids.*` 重算与存储值比较；不一致抛 `IdCollision`，写入 `out_dir` 之前就中止。
3. 分组：按 `3A_ID`；`affinity` 为各 pair 的 `obs` 按 `(src, record_key, obs 下标)` 排序后的拼接，每条恰好一次；实体 `lineage` 取并集并按字典序排序；`structure` 取 `(rank, src, structure_id)` 最小者，其余的 `structure_id` 以 `structure_alt=<id>` 元素追加到实体 lineage；`rank` 为 `None` 排在最后。
4. 对账断言：`Σ len(affinity)` 等于有效 pair 的 obs 总数；`n_pairs - n_3a` 为相同 `3A_ID` 的合并数，写入 manifest 的行数。
5. 分片：`int(3A_ID[:8], 16) % shards`，每片内按 `3A_ID` 排序，用 `OUT_SCHEMA` 写出。
6. `stats`：`coverage`（按 SRC：pair 数，`vh`、`vl`、`ab_structure`、`ag_structure` 为 `None` 的数量）；`rejects`（按 `(src, stage, reason_code)` 计数，含 `reject_glob` 读入的各阶段与本阶段的行）；`label_types`（按 obs lineage 解析：`(src, col, rest)`，`rest` 为 `col=` 之后其余片段以 ` | ` 连接，无则空串）；`overlap`（每个 `3A_ID` 的 SRC 集合，取自 obs lineage 首片段的 `SRC_Rxx`，排序去重）。列名：`coverage(src, n_pairs, vh_null, vl_null, ab_structure_null, ag_structure_null)`、`rejects(src, stage, reason_code, n)`、`label_types(src, col, rest, n)`、`overlap(3A_ID, srcs)`；`qa_sample(3A_ID, stratum)`。
7. `qa_sample`：分层 = 该 `3A` 实体 lineage 里出现的 `step=` 名称，取 `structure_recover > mutation_rebuild > split > trim` 中最高者，一个都没有为 `direct`；每层按 `md5(f"{seed}|{3A_ID}")` 升序取 `qa_per_stratum` 个。
8. `manifest.json`（键排序、无时间戳、无绝对路径）：`id_version`、`rules_version`、`code_commit`（`git rev-parse HEAD`）、`tools`（daft、duckdb、pyarrow、gemmi、anarci、hmmer 版本）、`decision_files`（文件名 → sha256）、`row_counts`（键 `pairs`、`3a`、`obs`、`rejected`、`merged`，`merged` 为 `pairs - 3a`）、`qa`（键 `seed`、`per_stratum`、`counts`）。

- [ ] **Step 1: 写失败的测试**。测试文件内放三个夹具函数：`pair(src, record_key, *, vh=VH, vl=VL, ag=("MKTAYIAKQR",), ab_structure=None, ag_structure=None, ab_rank=None, ag_rank=None, ab_lineage=(), ag_lineage=(), obs=()) -> dict`（`AB_ID`、`AG_ID`、`3A_ID` 由 `ids` 算出，`vh` 与 `vl` 全为 `None` 时 `AB_ID` 与 `3A_ID` 为 `None`，`ag` 为空时 `AG_ID` 与 `3A_ID` 为 `None`）、`o(label, lineage_str, assay=None, condition=None, replicate=None) -> dict`（`lineage` 为单元素列表）、`write_pairs(path, rows) -> None`（按 `PAIR_SCHEMA` 写 Parquet，`rows` 可为空）。序列用 Task 2 的 `VH`、`VL`。

```python
def test_same_3a_id_across_src_appends_each_obs_once(tmp_path):
    write_pairs(tmp_path / "R76.parquet", [pair("SRC_R76", "r1", obs=[o("1.2", "SRC_R76 | f.csv | row=1 | col=Y"), o("3.4", "SRC_R76 | f.csv | row=2 | col=Y")])])
    write_pairs(tmp_path / "R77.parquet", [pair("SRC_R77", "r1", obs=[o("1.2", "SRC_R77 | g.csv | row=9 | col=Y")])])
    rep = merge(str(tmp_path / "R*.parquet"), tmp_path / "out")
    t = pq.read_table(tmp_path / "out" / "3a")
    assert (rep.n_pairs, rep.n_3a, rep.n_obs) == (2, 1, 3)
    assert [a["lineage"][0][:7] for a in t["affinity"].to_pylist()[0]] == ["SRC_R76", "SRC_R76", "SRC_R77"]
    assert t.schema == OUT_SCHEMA

def test_structure_choice_and_alt_in_lineage(tmp_path):
    a = {"structure_id": "5VPL", "file_ref": "rcsb/5VPL.cif", "chain_map": "{}"}
    b = {"structure_id": "3RVV_snap", "file_ref": "SRC_R76/3RVV.cif", "chain_map": "{}"}
    write_pairs(tmp_path / "R76.parquet", [pair("SRC_R76", "r1", ag_structure=a, ag_rank=1, obs=[o("1", "SRC_R76 | f.csv | row=1 | col=Y")])])
    write_pairs(tmp_path / "R77.parquet", [pair("SRC_R77", "r1", ag_structure=b, ag_rank=0, obs=[o("1", "SRC_R77 | g.csv | row=1 | col=Y")])])
    merge(str(tmp_path / "R*.parquet"), tmp_path / "out")
    ag = pq.read_table(tmp_path / "out" / "3a")["antigen"].to_pylist()[0]
    assert ag["structure"]["structure_id"] == "3RVV_snap" and "structure_alt=5VPL" in ag["lineage"]

def test_id_collision_and_stored_id_mismatch_abort(tmp_path):
    ob = [o("1", "SRC_R76 | f | row=1 | col=Y")]
    x, y = pair("SRC_R76", "r1", obs=ob), pair("SRC_R76", "r2", vl=VL[:-1] + "A", obs=ob)
    y["AB_ID"] = x["AB_ID"]                                   # 同 AB_ID，不同 (vh, vl)
    write_pairs(tmp_path / "c.parquet", [x, y])
    with pytest.raises(IdCollision): merge(str(tmp_path / "c.parquet"), tmp_path / "out")
    z = pair("SRC_R76", "r1", obs=ob); z["AB_ID"] = "0" * 32  # 存储值与重算不符
    write_pairs(tmp_path / "m.parquet", [z])
    with pytest.raises(IdCollision): merge(str(tmp_path / "m.parquet"), tmp_path / "out2")
    assert not (tmp_path / "out" / "3a").exists() and not (tmp_path / "out2" / "3a").exists()

def test_invalid_pairs_go_to_reject_log(tmp_path):
    good = [o("1", "SRC_R76 | f | row=1 | col=Y")]
    write_pairs(tmp_path / "p.parquet", [
        pair("SRC_R76", "ok", obs=good),
        pair("SRC_R76", "no_chain", vh=None, vl=None, obs=good),
        pair("SRC_R76", "no_ag", ag=(), obs=good),
        pair("SRC_R76", "no_obs", obs=[]),
        pair("SRC_R76", "no_label", obs=[o(None, "SRC_R76 | f | row=4 | col=Y")])])
    rep = merge(str(tmp_path / "p.parquet"), tmp_path / "out")
    rl = pq.read_table(tmp_path / "out" / "reject_log.parquet").to_pylist()
    assert (rep.n_3a, rep.n_rejected) == (1, 4)
    assert sorted(r["key"] for r in rl) == ["no_ag", "no_chain", "no_label", "no_obs"]
    assert {(r["stage"], r["reason_code"]) for r in rl} == {("merge", "invalid_3a")}

def test_all_null_and_empty_inputs(tmp_path):                 # Review Focus 1
    write_pairs(tmp_path / "a.parquet", [pair("SRC_R76", "r1", ab_structure=None, ag_structure=None)])
    write_pairs(tmp_path / "b.parquet", [])                   # 零行
    rep = merge(str(tmp_path / "*.parquet"), tmp_path / "out")
    t = pq.read_table(tmp_path / "out" / "3a")
    assert t.schema == OUT_SCHEMA and t["antibody"].to_pylist()[0]["structure"] is None

def test_rerun_is_byte_identical(tmp_path):
    write_pairs(tmp_path / "p.parquet", [
        pair("SRC_R76", "r1", obs=[o("1", "SRC_R76 | f | row=1 | col=Y")]),
        pair("SRC_R77", "r1", ag=("GSHMLE",), obs=[o("2", "SRC_R77 | g | row=1 | col=Y")])])
    for d in ("o1", "o2"): merge(str(tmp_path / "p.parquet"), tmp_path / d, shards=4)
    files = sorted(p.relative_to(tmp_path / "o1") for p in (tmp_path / "o1").rglob("*") if p.is_file())
    assert files and all((tmp_path / "o1" / f).read_bytes() == (tmp_path / "o2" / f).read_bytes() for f in files)

def test_stats(tmp_path):
    ka = o("515000", "SRC_R12 | f.csv | row=123 | col=affinity | affinity_type=ka (1/Ms)")
    write_pairs(tmp_path / "p.parquet", [
        pair("SRC_R76", "r1", obs=[o("1", "SRC_R76 | f.csv | row=1 | col=Y")]),
        pair("SRC_R77", "r1", obs=[o("1", "SRC_R77 | g.csv | row=1 | col=Y")]),
        pair("SRC_R12", "r1", vl=None, ag=("GSHMLE",), obs=[ka])])
    rej = [{"stage": "adapt", "reason_code": "empty_label", "src": "SRC_R76", "key": f"k{i}", "detail": "{}"} for i in (1, 2)]
    pq.write_table(pa.Table.from_pylist(rej, schema=REJECT_SCHEMA), tmp_path / "rej.parquet")
    merge(str(tmp_path / "p.parquet"), tmp_path / "out", reject_glob=str(tmp_path / "rej.parquet"))
    rd = lambda n: pq.read_table(tmp_path / "out" / "stats" / f"{n}.parquet").to_pylist()
    assert {"src": "SRC_R12", "col": "affinity", "rest": "affinity_type=ka (1/Ms)", "n": 1} in rd("label_types")
    assert {"src": "SRC_R76", "stage": "adapt", "reason_code": "empty_label", "n": 2} in rd("rejects")
    assert [r["srcs"] for r in rd("overlap") if len(r["srcs"]) > 1] == [["SRC_R76", "SRC_R77"]]
    assert next(r for r in rd("coverage") if r["src"] == "SRC_R12")["vl_null"] == 1

def test_qa_sample_stratified_and_deterministic(tmp_path):
    def row(i, step):
        lin = [f"step={step} | span=0-5"] if step else []
        return pair("SRC_R76", f"r{i}", ag=("MKTAYIAKQR" + "A" * i,), ab_lineage=lin, obs=[o("1", f"SRC_R76 | f | row={i} | col=Y")])
    layout = [(None, 20), ("trim", 20), ("split", 3), ("mutation_rebuild", 3), ("structure_recover", 3)]
    rows = [row(i, s) for i, s in enumerate(s for s, n in layout for _ in range(n))]
    write_pairs(tmp_path / "p.parquet", rows)
    def run(d, seed):
        merge(str(tmp_path / "p.parquet"), tmp_path / d, qa_seed=seed, qa_per_stratum=3)
        return pq.read_table(tmp_path / d / "qa_sample.parquet").to_pylist()
    a, a2, b = run("a", 0), run("a2", 0), run("b", 1)
    assert a == a2 and a != b
    assert collections.Counter(r["stratum"] for r in a) == {"direct": 3, "trim": 3, "split": 3, "mutation_rebuild": 3, "structure_recover": 3}

def test_manifest_fields(tmp_path):
    write_pairs(tmp_path / "p.parquet", [
        pair("SRC_R76", "r1", obs=[o("1", "SRC_R76 | f | row=1 | col=Y"), o("2", "SRC_R76 | f | row=2 | col=Y")]),
        pair("SRC_R77", "r1", obs=[o("3", "SRC_R77 | g | row=1 | col=Y")])])
    df = tmp_path / "R23.yaml"; df.write_text("src: R23\nclaims: []\n")
    merge(str(tmp_path / "p.parquet"), tmp_path / "out", decision_files=[df])
    text = (tmp_path / "out" / "manifest.json").read_text(); m = json.loads(text)
    assert set(m) == {"id_version", "rules_version", "code_commit", "tools", "decision_files", "row_counts", "qa"}
    assert m["id_version"] == "v1" and set(m["tools"]) == {"daft", "duckdb", "pyarrow", "gemmi", "anarci", "hmmer"}
    assert m["decision_files"] == {"R23.yaml": hashlib.sha256(df.read_bytes()).hexdigest()}
    assert m["row_counts"] == {"pairs": 2, "3a": 1, "obs": 3, "rejected": 0, "merged": 1}
    assert set(m["qa"]) == {"seed", "per_stratum", "counts"} and str(tmp_path) not in text
```

- [ ] **Step 2: 运行，确认失败**：`[host] pytest etl/core/test_merge.py -v`，Expected: `ImportError`（`merge` 未定义）。
- [ ] **Step 3: 实现 `merge.py`**。DuckDB 用显式列类型读各 SRC 的 Parquet；输出经 pyarrow 转 `OUT_SCHEMA` 后写出，Daft 不参与。
- [ ] **Step 4: 写 `merge.md`**：写明 `PAIR_SCHEMA` 是 B 层 assemble 的输出契约、`structure` 指针对象 `{structure_id, file_ref, chain_map}` 中 `chain_map` 为 JSON 字符串、`rank` 的含义（SRC 自带快照优先于 RCSB 由 adapter 赋小值）、`merge` 的断言与 `reject_log` 的写法，以及 blueprint §8 的对账公式。
- [ ] **Step 5: 运行，确认通过**：Expected: 全部 passed。
- [ ] **Step 6: Commit**：`[host] git add etl/core/merge.* etl/core/test_merge.py && git commit -m "feat(etl): merge with stats, qa_sample and manifest"`

---

### Task 10: 依赖文件、handoff.md、总验证、push

**Files:**
- Create: `etl/requirements.txt`、`etl/handoff.md`、`etl/core/test_docs.py`

**Interfaces:**
- Consumes: 全部模块与 md。
- Produces: `etl/handoff.md`，cc 的入口。

`handoff.md` 内容（保持短，blueprint §7.2）：
- 目标与成功标准：产出有效的 `3a` shards；成功的标准是有产出，不是处处合规（原则 5）。
- 硬约束：affinity 五元组不改；不写根分区；刻意压缩的数据集不解包；B 层在远程 `etl-b-layer` 分支工作（开工前 `etl-a-layer` 须已合入 `origin/main`，否则停下并告知 Pthahnix），本地不做任何写操作，完成后 push 该分支，由 Pthahnix 亲自 merge。
- 环境入口：`source etl/env.sh`；代理 `ETL_PROXY`（mihomo 须以 `GODEBUG=tlsmlkem=0` 启动，主机重启后手动拉起）；数据路径 `/data_new/ywy/dataset-abag/SRC_Rxx_*`；blueprint §5.1 的实测环境。
- 工作对象：20 个 SRC 的清单（R 编号、数据目录名、对应 `context/2026-10-30-3a-src-inventory/` 的 inventory 文档），建议顺序与业务提示指向 blueprint §6。
- 共享模块用法：逐个链到 `core/<模块>.md`；发现缺陷可直接修模块，不加按 SRC 的分支，修改记一行并重跑受影响的 SRC。
- 决策文件原则：论断带可追溯证据，运行期不联网、不调用 AI；格式见 blueprint "AI 接缝"。
- 进度记录：cc 自己维护 `etl/progress.md`，用于跨上下文续作。

- [ ] **Step 1: 写失败的测试 `etl/core/test_docs.py`**

```python
def test_every_module_has_md_with_three_sections():
    for py in CORE.glob("*.py"):
        if py.name.startswith(("test_", "__")): continue
        text = py.with_suffix(".md").read_text()
        assert all(h in text for h in ("## 语义", "## 接口", "## 示例")), py.name

def test_handoff_links_resolve_and_requirements_pin_versions():
    h = (ETL / "handoff.md").read_text()
    for target in re.findall(r"\]\(([^)#]+)\)", h):
        if not target.startswith("http"): assert (ETL / target).exists(), target
    r = (ETL / "requirements.txt").read_text().lower()
    for pin in ["daft==0.7.26", "duckdb==2.0.0", "pyarrow==25.0.1", "gemmi==0.7.5", "pytest==9.2.0"]:
        assert pin in r
    assert re.search(r"^anarci==2026\.2\.13\.2", r, re.M)
```

- [ ] **Step 2: 运行，确认失败**：`[host] pytest etl/core/test_docs.py -v`，Expected: FAIL（`handoff.md` 不存在）。
- [ ] **Step 3: 生成 `etl/requirements.txt`**：`[host] uv pip freeze > etl/requirements.txt`，并在文件首行注释 HMMER 3.4 的安装位置 `/data_new/ywy/tools/hmmer/usr/bin`（pip 之外）。
- [ ] **Step 4: 写 `etl/handoff.md`**，内容见上。
- [ ] **Step 5: 在干净 shell 里全量验证**

Run: `ssh 3x5090 'env -i HOME=$HOME PATH=/usr/bin:/bin bash -c "cd /data_new/ywy/LOVYATEE && source etl/env.sh && pytest etl -v 2>&1 | tail -15"'`
Expected: 末行形如 `N passed`，0 failed、0 error。任何失败先修再继续。

- [ ] **Step 6: Commit**

```bash
[host] git add etl && git commit -m "feat(etl): requirements, handoff and docs check"
```

- [ ] **Step 7: 核对隔离与分支**

Run: `ssh 3x5090 'cd /data_new/ywy/LOVYATEE && git status --short | wc -l && git rev-parse main origin/main && git log --oneline origin/main..etl-a-layer'`
Expected: `0`（工作区干净）；`main` 与 `origin/main` 同一哈希；列出 10 条 `feat(etl)` 提交（Task 1–10 各一条）。

- [ ] **Step 8: push 分支**

```bash
ssh 3x5090 'cd /data_new/ywy/LOVYATEE && git push -u origin etl-a-layer'
```
Expected: push 输出含 `etl-a-layer -> etl-a-layer`；`git ls-remote --heads origin etl-a-layer` 返回一行。

- [ ] **Step 9: 回报**：给 Pthahnix 分支名、`pytest` 通过数、`vdomain.md` 的 `no_domain` 实测占比、`mutate.md` 里 `1N8Z` 的区间确认结果，等待其亲自 merge 到 `main`。
