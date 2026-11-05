"""各 SRC 的 pair Parquet → 3a shards、stats、qa_sample、reject_log、manifest。

ponytail: 全部查询走 _run（execute + 立即取完），DuckDB 2.0 的 execute 结果不取完会锁住连接。
"""
import hashlib
import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

from etl.core import ids
from etl.core.lineage import get

STAGE = "merge"
STRATA = ("structure_recover", "mutation_rebuild", "split", "trim")
RANK_MAX = 2147483647

STRUCT = pa.struct([("structure_id", pa.string()), ("file_ref", pa.string()),
                    ("chain_map", pa.string())])
OBS = pa.struct([("label", pa.string()), ("assay", pa.string()), ("condition", pa.string()),
                 ("replicate", pa.string()), ("lineage", pa.list_(pa.string()))])
PAIR_SCHEMA = pa.schema([
    ("src", pa.string()), ("record_key", pa.string()),
    ("AB_ID", pa.string()), ("AG_ID", pa.string()), ("3A_ID", pa.string()),
    ("vh", pa.string()), ("vl", pa.string()),
    ("ab_structure", STRUCT), ("ab_structure_rank", pa.int32()),
    ("ab_lineage", pa.list_(pa.string())),
    ("ag_sequence", pa.list_(pa.string())),
    ("ag_structure", STRUCT), ("ag_structure_rank", pa.int32()),
    ("ag_lineage", pa.list_(pa.string())),
    ("obs", pa.list_(OBS)),
])
OUT_SCHEMA = pa.schema([
    ("3A_ID", pa.string()),
    ("antibody", pa.struct([("AB_ID", pa.string()), ("vh_sequence", pa.string()),
                            ("vl_sequence", pa.string()), ("structure", STRUCT),
                            ("lineage", pa.list_(pa.string()))])),
    ("antigen", pa.struct([("AG_ID", pa.string()), ("sequence", pa.list_(pa.string())),
                           ("structure", STRUCT), ("lineage", pa.list_(pa.string()))])),
    ("affinity", pa.list_(OBS)),
])
REJECT_SCHEMA = pa.schema([("stage", pa.string()), ("reason_code", pa.string()),
                           ("src", pa.string()), ("key", pa.string()),
                           ("detail", pa.string())])

VALID = """(coalesce(vh, '') <> '' or coalesce(vl, '') <> '')
      and ag_sequence is not null and len(ag_sequence) > 0
      and len(list_filter(ag_sequence, lambda x: coalesce(x, '') = '')) = 0
      and obs is not null and len(obs) > 0
      and len(list_filter(obs, lambda x: x.label is null)) = 0"""


@dataclass(frozen=True)
class MergeReport:
    n_pairs: int
    n_3a: int
    n_obs: int
    n_rejected: int


def _run(con: duckdb.DuckDBPyConnection, sql: str, params=None):
    return con.execute(sql, params or []).fetchall()


def _load(con: duckdb.DuckDBPyConnection, pair_glob: str) -> int:
    _run(con, "create or replace table pairs as select *, (%s) as valid from read_parquet(?)"
         % VALID, [pair_glob])
    return _run(con, "select count(*) from pairs where valid")[0][0]


def _rejects(con: duckdb.DuckDBPyConnection) -> list[dict]:
    rows = _run(con, """
        select 'merge', 'invalid_3a', src, record_key,
               json_object('vh_null', vh is null, 'vl_null', vl is null,
                           'ag_sequence', ag_sequence, 'n_obs', len(obs))
        from pairs where not valid order by src, record_key
    """)
    return [dict(zip(("stage", "reason_code", "src", "key", "detail"), r)) for r in rows]


def _check_ids(con: duckdb.DuckDBPyConnection) -> None:
    """同一 ID 只对应一个 canonical；distinct 行用 ids.* 重算与存储值比较。"""
    dup = _run(con, """
        select AB_ID from pairs where valid and AB_ID is not null group by 1
        having count(distinct coalesce(vh, '<NONE>') || '<SEP>' || coalesce(vl, '<NONE>')) > 1
        union all
        select AG_ID from pairs where valid and AG_ID is not null group by 1
        having count(distinct array_to_string(ag_sequence, '<SEP>')) > 1
        union all
        select "3A_ID" from pairs where valid and "3A_ID" is not null group by 1
        having count(distinct AB_ID || '|' || AG_ID) > 1
    """)
    if dup:
        raise ids.IdCollision("id maps to several canonicals: %r" % (dup[0][0],))
    for vh, vl, ab, ag, three, chains in _run(con, """
            select distinct vh, vl, AB_ID, AG_ID, "3A_ID", ag_sequence
            from pairs where valid"""):
        want_ab = ids.ab_id(vh or None, vl or None)
        want_ag = ids.ag_id(list(chains))
        if want_ab != ab or want_ag != ag or ids.three_a_id(want_ab, want_ag) != three:
            raise ids.IdCollision("stored id does not match canonical: %r" % (three,))


def _group(con: duckdb.DuckDBPyConnection) -> None:
    """按 3A_ID 分组；structure 取 (rank, structure_id, src) 最小者，affinity 按来源顺序拼接。"""
    _run(con, """
        create or replace table obs_rows as
        select p."3A_ID", p.src, p.record_key, u.o, u.idx
        from pairs p, unnest(p.obs) with ordinality as u(o, idx)
        where p.valid
    """)
    _run(con, """
        create or replace table affinity_agg as
        select "3A_ID", list(o order by src, record_key, idx) as affinity
        from obs_rows group by 1
    """)
    for side in ("ab", "ag"):
        _run(con, """
            create or replace table %s_pick as
            select "3A_ID", %s_structure as structure from (
                select "3A_ID", %s_structure,
                       row_number() over (partition by "3A_ID" order by
                           coalesce(%s_structure_rank, %d),
                           coalesce(%s_structure.structure_id, ''), src) as rn
                from pairs where valid and %s_structure is not null
            ) where rn = 1
        """ % (side, side, side, side, RANK_MAX, side, side))
    _run(con, """
        create or replace table grouped as
        select p."3A_ID",
            any_value(p."AB_ID") as ab_id, any_value(p.vh) as vh, any_value(p.vl) as vl,
            any_value(p."AG_ID") as ag_id, any_value(p.ag_sequence) as ag_sequence,
            any_value(a.structure) as ab_structure, any_value(g.structure) as ag_structure,
            list_sort(list_distinct(flatten(list(p.ab_lineage)))) as ab_lineage,
            list_sort(list_distinct(flatten(list(p.ag_lineage)))) as ag_lineage,
            coalesce(any_value(af.affinity), []) as affinity
        from pairs p left join affinity_agg af using ("3A_ID")
        left join ab_pick a using ("3A_ID") left join ag_pick g using ("3A_ID")
        where p.valid group by p."3A_ID" order by p."3A_ID"
    """)


def _add_alts(con: duckdb.DuckDBPyConnection) -> None:
    """未被选中的结构以 structure_alt=<id> 追加到实体 lineage。"""
    _run(con, """
        create or replace table alts as
        select "3A_ID", 'structure_alt=' || structure_id as frag, 'ab' as side from (
            select p."3A_ID", p.ab_structure.structure_id as structure_id
            from pairs p join grouped g using ("3A_ID")
            where p.valid and p.ab_structure is not null
              and p.ab_structure.structure_id is distinct from g.ab_structure.structure_id
            group by 1, 2
        ) union all
        select "3A_ID", 'structure_alt=' || structure_id, 'ag' from (
            select p."3A_ID", p.ag_structure.structure_id as structure_id
            from pairs p join grouped g using ("3A_ID")
            where p.valid and p.ag_structure is not null
              and p.ag_structure.structure_id is distinct from g.ag_structure.structure_id
            group by 1, 2
        )
    """)
    _run(con, """
        create or replace table grouped2 as
        select g.*,
            list_sort(list_distinct(g.ab_lineage
                + coalesce((select list(a.frag) from alts a
                            where a."3A_ID" = g."3A_ID" and a.side = 'ab'), []))) as ab_lineage2,
            list_sort(list_distinct(g.ag_lineage
                + coalesce((select list(a.frag) from alts a
                            where a."3A_ID" = g."3A_ID" and a.side = 'ag'), []))) as ag_lineage2
        from grouped g
    """)


def _write_3a(con: duckdb.DuckDBPyConnection, out: Path, shards: int) -> int:
    target = out / "3a"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    # 显式 cast 每个字段：全 None 的列在 Arrow 里会退化成 null 类型，cast 到 OUT_SCHEMA 会失败
    _run(con, """
        create or replace table flat as
        select "3A_ID",
            struct_pack("AB_ID" := ab_id,
                        vh_sequence := cast(vh as varchar),
                        vl_sequence := cast(vl as varchar),
                        structure := case when ab_structure is null then null else
                            struct_pack(structure_id := ab_structure.structure_id,
                                        file_ref := ab_structure.file_ref,
                                        chain_map := cast(ab_structure.chain_map as varchar)) end,
                        lineage := ab_lineage2) as antibody,
            struct_pack("AG_ID" := ag_id,
                        sequence := ag_sequence,
                        structure := case when ag_structure is null then null else
                            struct_pack(structure_id := ag_structure.structure_id,
                                        file_ref := ag_structure.file_ref,
                                        chain_map := cast(ag_structure.chain_map as varchar)) end,
                        lineage := ag_lineage2) as antigen,
            list_transform(affinity, lambda o: struct_pack(
                label := o.label, assay := cast(o.assay as varchar),
                condition := cast(o.condition as varchar),
                replicate := cast(o.replicate as varchar),
                lineage := o.lineage)) as affinity
        from grouped2 order by "3A_ID"
    """)
    # ponytail: 逐行取回后按 OUT_SCHEMA 重建分片；全 None 列在 Arrow 里会退化成 null 类型
    rows = _run(con, 'select "3A_ID", antibody, antigen, affinity from flat order by "3A_ID"')
    records = []
    for row in rows:
        bucket = int(row[0][:8], 16) % shards
        records.append((bucket, row[0], {"3A_ID": row[0], "antibody": row[1],
                                         "antigen": row[2], "affinity": row[3]}))
    records.sort(key=lambda item: (item[0], item[1]))
    ids_col = [r[1] for r in records]
    for k in range(shards):
        part = [r[2] for r in records if r[0] == k]
        pq.write_table(pa.Table.from_pylist(part, schema=OUT_SCHEMA),
                       target / ("part-%03d.parquet" % k), compression="zstd")
    return len(ids_col)


def _stratum(lineage: Sequence[str]) -> str:
    names = {get(line, "step") for line in lineage}
    return next((name for name in STRATA if name in names), "direct")


def _write_qa(con: duckdb.DuckDBPyConnection, out: Path, seed: int, per: int) -> dict:
    rows = _run(con, 'select "3A_ID", ab_lineage2, ag_lineage2 from grouped2')
    by_stratum: dict[str, list[tuple[str, str]]] = {}
    for three, ab_line, ag_line in rows:
        stratum = _stratum(list(ab_line or []) + list(ag_line or []))
        digest = hashlib.md5(("%d|%s" % (seed, three)).encode()).hexdigest()
        by_stratum.setdefault(stratum, []).append((digest, three))
    picked, counts = [], {}
    for stratum in sorted(by_stratum):
        chosen = sorted(by_stratum[stratum])[:per]
        counts[stratum] = len(chosen)
        picked.extend({"3A_ID": three, "stratum": stratum} for _, three in chosen)
    schema = pa.schema([("3A_ID", pa.string()), ("stratum", pa.string())])
    table = pa.Table.from_pylist(picked, schema=schema) if picked else schema.empty_table()
    pq.write_table(table, out / "qa_sample.parquet")
    return counts


def _write_stats(con: duckdb.DuckDBPyConnection, out: Path, rejects: list[dict]) -> None:
    stats = out / "stats"
    stats.mkdir(parents=True, exist_ok=True)
    table = (pa.Table.from_pylist(rejects, schema=REJECT_SCHEMA) if rejects
             else REJECT_SCHEMA.empty_table())
    pq.write_table(table, out / "reject_log.parquet")
    _run(con, """
        create or replace table coverage as
        select src, count(*) as n_pairs,
               count(*) filter (where vh is null) as vh_null,
               count(*) filter (where vl is null) as vl_null,
               count(*) filter (where ab_structure is null) as ab_structure_null,
               count(*) filter (where ag_structure is null) as ag_structure_null
        from pairs where valid group by src order by src
    """)
    pq.write_table(con.sql("select * from coverage").arrow().read_all(),
                   stats / "coverage.parquet")
    _run(con, "create or replace table obs_flat as select src, unnest(obs) as o from pairs where valid")
    _run(con, """
        create or replace table obs_parts as
        select src, string_split(list_extract(o.lineage, 1), ' | ') as parts from obs_flat
    """)
    _run(con, """
        create or replace table label_types as
        select src, substr(v, 5) as col,
               case when idx < len(parts)
                    then array_to_string(list_slice(parts, idx + 1, len(parts)), ' | ')
                    else '' end as rest,
               count(*) as n
        from obs_parts t, unnest(t.parts) with ordinality as l(v, idx)
        where v like 'col=%'
        group by 1, 2, 3 order by 1, 2, 3
    """)
    pq.write_table(con.sql("select * from label_types").arrow().read_all(),
                   stats / "label_types.parquet")
    _run(con, """
        create or replace table overlap as
        select "3A_ID",
               list_sort(list(distinct split_part(list_extract(o.lineage, 1), ' ', 1))) as srcs
        from (select "3A_ID", unnest(affinity) as o from grouped2) group by 1 order by 1
    """)
    pq.write_table(con.sql("select * from overlap").arrow().read_all(),
                   stats / "overlap.parquet")
    _run(con, "create or replace table rej_counts as select stage, reason_code, src, "
              "count(*) as n from read_parquet(?) group by 1, 2, 3 order by 3, 1, 2",
         [str(out / "reject_log.parquet")])
    pq.write_table(con.sql("select * from rej_counts").arrow().read_all(),
                   stats / "rejects.parquet")


def _tool_versions() -> dict:
    import anarci
    import daft
    import gemmi
    try:
        out = subprocess.run(["hmmscan", "-h"], capture_output=True, text=True).stdout
        hmmer = next((line.split()[-1] for line in out.splitlines()
                      if line.startswith("# HMMER")), "unknown")
    except Exception:
        hmmer = "missing"
    return {"daft": daft.__version__, "duckdb": duckdb.__version__,
            "pyarrow": pa.__version__, "gemmi": gemmi.__version__,
            "anarci": getattr(anarci, "__version__", "unknown"), "hmmer": hmmer}


def _code_commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def merge(pair_glob: str, out_dir: Path, *, reject_glob: str | None = None, shards: int = 16,
          qa_seed: int = 0, qa_per_stratum: int = 50,
          decision_files: Sequence[Path] = (), rules_version: str = "v1") -> MergeReport:
    out = Path(out_dir)
    con = duckdb.connect()
    n_pairs = _load(con, pair_glob)
    rejects = _rejects(con)
    _check_ids(con)
    _group(con)
    _add_alts(con)
    n_3a = _run(con, "select count(*) from grouped2")[0][0]
    n_obs = _run(con, "select coalesce(sum(len(affinity)), 0) from grouped2")[0][0]
    expected = _run(con, "select coalesce(sum(len(obs)), 0) from pairs where valid")[0][0]
    assert n_obs == expected, "affinity does not reconcile: %d != %d" % (n_obs, expected)

    out.mkdir(parents=True, exist_ok=True)
    _write_3a(con, out, shards)
    qa = _write_qa(con, out, qa_seed, qa_per_stratum)
    if reject_glob:
        extra = _run(con, "select stage, reason_code, src, key, detail from read_parquet(?)",
                     [reject_glob])
        rejects = rejects + [dict(zip(("stage", "reason_code", "src", "key", "detail"), r))
                             for r in extra]
    _write_stats(con, out, rejects)
    manifest = {
        "id_version": ids.ID_VERSION,
        "rules_version": rules_version,
        "code_commit": _code_commit(),
        "tools": _tool_versions(),
        "decision_files": {Path(p).name: hashlib.sha256(Path(p).read_bytes()).hexdigest()
                           for p in decision_files},
        "row_counts": {"pairs": n_pairs, "3a": n_3a, "obs": n_obs,
                       "rejected": len(_rejects(con)), "merged": n_pairs - n_3a},
        "qa": {"seed": qa_seed, "per_stratum": qa_per_stratum, "counts": qa},
    }
    (out / "manifest.json").write_text(json.dumps(manifest, sort_keys=True, indent=1))
    return MergeReport(n_pairs, n_3a, n_obs, len(_rejects(con)))
