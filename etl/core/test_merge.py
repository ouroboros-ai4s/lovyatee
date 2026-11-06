import collections
import hashlib
import json

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from etl.core.ids import IdCollision, ab_id, ag_id, three_a_id
from etl.core.merge import OUT_SCHEMA, PAIR_SCHEMA, REJECT_SCHEMA, merge

VH, VL = "EVQLVESGGGLVQPGGSLRLSCAAS", "DIQMTQSPSSLSASVGDRVTITC"


def pair(src, record_key, *, vh=VH, vl=VL, ag=("MKTAYIAKQR",), ab_structure=None,
         ag_structure=None, ab_rank=None, ag_rank=None, ab_lineage=(), ag_lineage=(), obs=()):
    chains = list(ag)
    ab = ab_id(vh, vl) if (vh or vl) else None
    agid = ag_id(chains) if chains else None
    return {"src": src, "record_key": record_key, "AB_ID": ab, "AG_ID": agid,
            "3A_ID": three_a_id(ab, agid) if (ab and agid) else None,
            "vh": vh, "vl": vl, "ab_structure": ab_structure, "ab_structure_rank": ab_rank,
            "ab_lineage": list(ab_lineage), "ag_sequence": chains,
            "ag_structure": ag_structure, "ag_structure_rank": ag_rank,
            "ag_lineage": list(ag_lineage), "obs": list(obs)}


def o(label, lineage_str, assay=None, condition=None, replicate=None):
    return {"label": label, "assay": assay, "condition": condition,
            "replicate": replicate, "lineage": [lineage_str]}


def write_pairs(path, rows):
    table = pa.Table.from_pylist(rows, schema=PAIR_SCHEMA) if rows else PAIR_SCHEMA.empty_table()
    pq.write_table(table, path)


def test_same_3a_id_across_src_appends_each_obs_once(tmp_path):
    write_pairs(tmp_path / "R76.parquet", [pair("SRC_R76", "r1", obs=[
        o("1.2", "SRC_R76 | f.csv | row=1 | col=Y"),
        o("3.4", "SRC_R76 | f.csv | row=2 | col=Y")])])
    write_pairs(tmp_path / "R77.parquet", [pair("SRC_R77", "r1", obs=[
        o("1.2", "SRC_R77 | g.csv | row=9 | col=Y")])])
    rep = merge(str(tmp_path / "R*.parquet"), tmp_path / "out")
    t = pq.read_table(tmp_path / "out" / "3a")
    assert (rep.n_pairs, rep.n_3a, rep.n_obs) == (2, 1, 3)
    assert [a["lineage"][0][:7] for a in t["affinity"].to_pylist()[0]] == ["SRC_R76", "SRC_R76", "SRC_R77"]
    assert t.schema == OUT_SCHEMA


def test_structure_choice_and_alt_in_lineage(tmp_path):
    a = {"structure_id": "5VPL", "file_ref": "rcsb/5VPL.cif", "chain_map": "{}"}
    b = {"structure_id": "3RVV_snap", "file_ref": "SRC_R76/3RVV.cif", "chain_map": "{}"}
    write_pairs(tmp_path / "R76.parquet", [pair("SRC_R76", "r1", ag_structure=a, ag_rank=1,
                                                obs=[o("1", "SRC_R76 | f.csv | row=1 | col=Y")])])
    write_pairs(tmp_path / "R77.parquet", [pair("SRC_R77", "r1", ag_structure=b, ag_rank=0,
                                                obs=[o("1", "SRC_R77 | g.csv | row=1 | col=Y")])])
    merge(str(tmp_path / "R*.parquet"), tmp_path / "out")
    ag = pq.read_table(tmp_path / "out" / "3a")["antigen"].to_pylist()[0]
    assert ag["structure"]["structure_id"] == "3RVV_snap" and "structure_alt=5VPL" in ag["lineage"]


def test_id_collision_and_stored_id_mismatch_abort(tmp_path):
    ob = [o("1", "SRC_R76 | f | row=1 | col=Y")]
    x, y = pair("SRC_R76", "r1", obs=ob), pair("SRC_R76", "r2", vl=VL[:-1] + "A", obs=ob)
    y["AB_ID"] = x["AB_ID"]
    write_pairs(tmp_path / "c.parquet", [x, y])
    with pytest.raises(IdCollision):
        merge(str(tmp_path / "c.parquet"), tmp_path / "out")
    z = pair("SRC_R76", "r1", obs=ob)
    z["AB_ID"] = "0" * 32
    write_pairs(tmp_path / "m.parquet", [z])
    with pytest.raises(IdCollision):
        merge(str(tmp_path / "m.parquet"), tmp_path / "out2")
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


def test_all_null_and_empty_inputs(tmp_path):
    write_pairs(tmp_path / "a.parquet", [pair("SRC_R76", "r1", ab_structure=None, ag_structure=None,
                                              obs=[o("1", "SRC_R76 | f | row=1 | col=Y")])])
    write_pairs(tmp_path / "b.parquet", [])
    merge(str(tmp_path / "*.parquet"), tmp_path / "out")
    t = pq.read_table(tmp_path / "out" / "3a")
    assert t.schema == OUT_SCHEMA and t["antibody"].to_pylist()[0]["structure"] is None


def test_rerun_is_byte_identical(tmp_path):
    write_pairs(tmp_path / "p.parquet", [
        pair("SRC_R76", "r1", obs=[o("1", "SRC_R76 | f | row=1 | col=Y")]),
        pair("SRC_R77", "r1", ag=("GSHMLE",), obs=[o("2", "SRC_R77 | g | row=1 | col=Y")])])
    for d in ("o1", "o2"):
        merge(str(tmp_path / "p.parquet"), tmp_path / d, shards=4)
    files = sorted(p.relative_to(tmp_path / "o1") for p in (tmp_path / "o1").rglob("*") if p.is_file())
    assert files and all((tmp_path / "o1" / f).read_bytes() == (tmp_path / "o2" / f).read_bytes()
                         for f in files)


def test_stats(tmp_path):
    ka = o("515000", "SRC_R12 | f.csv | row=123 | col=affinity | affinity_type=ka (1/Ms)")
    write_pairs(tmp_path / "p.parquet", [
        pair("SRC_R76", "r1", obs=[o("1", "SRC_R76 | f.csv | row=1 | col=Y")]),
        pair("SRC_R77", "r1", obs=[o("1", "SRC_R77 | g.csv | row=1 | col=Y")]),
        pair("SRC_R12", "r1", vl=None, ag=("GSHMLE",), obs=[ka])])
    rej = [{"stage": "adapt", "reason_code": "empty_label", "src": "SRC_R76", "key": f"k{i}",
            "detail": "{}"} for i in (1, 2)]
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
        return pair("SRC_R76", f"r{i}", ag=("MKTAYIAKQR" + "A" * i,), ab_lineage=lin,
                    obs=[o("1", f"SRC_R76 | f | row={i} | col=Y")])
    layout = [(None, 20), ("trim", 20), ("split", 3), ("mutation_rebuild", 3), ("structure_recover", 3)]
    rows = [row(i, s) for i, s in enumerate(s for s, n in layout for _ in range(n))]
    write_pairs(tmp_path / "p.parquet", rows)

    def run(d, seed):
        merge(str(tmp_path / "p.parquet"), tmp_path / d, qa_seed=seed, qa_per_stratum=3)
        return pq.read_table(tmp_path / d / "qa_sample.parquet").to_pylist()

    a, a2, b = run("a", 0), run("a2", 0), run("b", 1)
    assert a == a2 and a != b
    assert collections.Counter(r["stratum"] for r in a) == {
        "direct": 3, "trim": 3, "split": 3, "mutation_rebuild": 3, "structure_recover": 3}


def test_manifest_fields(tmp_path):
    write_pairs(tmp_path / "p.parquet", [
        pair("SRC_R76", "r1", obs=[o("1", "SRC_R76 | f | row=1 | col=Y"),
                                   o("2", "SRC_R76 | f | row=2 | col=Y")]),
        pair("SRC_R77", "r1", obs=[o("3", "SRC_R77 | g | row=1 | col=Y")])])
    df = tmp_path / "R23.yaml"
    df.write_text("src: R23\nclaims: []\n")
    merge(str(tmp_path / "p.parquet"), tmp_path / "out", decision_files=[df])
    text = (tmp_path / "out" / "manifest.json").read_text()
    m = json.loads(text)
    assert set(m) == {"id_version", "rules_version", "code_commit", "tools", "decision_files",
                      "row_counts", "qa"}
    assert m["id_version"] == "v1" and set(m["tools"]) == {
        "daft", "duckdb", "pyarrow", "gemmi", "anarci", "hmmer"}
    assert m["decision_files"] == {"R23.yaml": hashlib.sha256(df.read_bytes()).hexdigest()}
    assert m["row_counts"] == {"pairs": 2, "3a": 1, "obs": 3, "rejected": 0, "merged": 1}
    assert set(m["qa"]) == {"seed", "per_stratum", "counts"} and str(tmp_path) not in text


def test_structure_pick_is_deterministic_across_runs(tmp_path):
    """同一 3A 下多条记录引用同一结构但链映射不同时，两轮 merge 必须选同一条。"""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from etl.core.merge import PAIR_SCHEMA, merge

    from etl.core import ids
    ab = ids.ab_id("EVQLV", None)
    ag = ids.ag_id(["MKTAY"])
    three = ids.three_a_id(ab, ag)
    struct = lambda cm: {"structure_id": "4YHP", "file_ref": None, "chain_map": cm}
    rows = []
    for i, cm in enumerate(['{"Q": "Q"}', '{"P": "P"}']):
        rows.append({
            "src": "SRC_RXX", "record_key": "row=%d" % i,
            "AB_ID": ab, "AG_ID": ag, "3A_ID": three,
            "vh": "EVQLV", "vl": None,
            "ab_structure": struct(cm), "ab_structure_rank": 10,
            "ab_lineage": ["step=trim | span=0-5"], "ag_sequence": ["MKTAY"],
            "ag_structure": struct(cm), "ag_structure_rank": 10,
            "ag_lineage": ["step=trim | span=0-5"],
            "obs": [{"label": "1", "assay": None, "condition": None, "replicate": None,
                     "lineage": ["SRC_RXX | a.csv | row=%d | col=x" % i]}],
        })
    src = tmp_path / "pair.parquet"
    pq.write_table(pa.Table.from_pylist(rows, schema=PAIR_SCHEMA), src)

    picks = []
    for n in range(2):
        out = tmp_path / ("m%d" % n)
        merge(str(src), out, shards=1, qa_per_stratum=1)
        picks.append((out / "3a" / "part-000.parquet").read_bytes())
    assert picks[0] == picks[1]
