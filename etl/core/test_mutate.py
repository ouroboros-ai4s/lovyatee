from pathlib import Path

import pytest

from etl.core.mutate import Edit, ParentChain, apply_point, apply_region
from etl.core.structref import open_structure
from etl.core.vdomain import parse, to_fv

R14_3BDY = Path("/data_new/ywy/dataset-abag/SRC_R14_ABBIND/snapshot-2019-04-10/"
                "AB-Bind-Database/3BDY.pdb")
CHAIN = "H"
EDIT = Edit("H:D31A", CHAIN, "D", 31, "A", "pdb_author")


@pytest.mark.data
def test_point_mutation_on_real_parent():
    rec = open_structure(R14_3BDY).chains[CHAIN]
    r = apply_point("ab", {CHAIN: ParentChain(rec.full_seq, {"pdb_author": rec.index_of})}, [EDIT])
    i = rec.index_of[(EDIT.pos, EDIT.ins)]
    assert r.cls == "B" and r.chains[CHAIN][i] == EDIT.new
    assert r.chains[CHAIN][:i] + r.chains[CHAIN][i + 1:] == rec.full_seq[:i] + rec.full_seq[i + 1:]
    assert r.sites == ((EDIT.id, CHAIN, i),) and r.lineage[0].startswith("step=mutation_rebuild | entity=ab | class=B")


def test_c_class_reasons():
    p = {"H": ParentChain("ACDEFGHIK", {"pdb_author": {(n, ""): n - 1 for n in range(1, 10)}})}
    e = lambda **k: Edit("m", **{"chain": "H", "orig": "C", "pos": 2, "new": "A",
                                 "numbering": "pdb_author", **k})
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


def test_insertion_code_position():
    p = {"H": ParentChain("ACDE", {"pdb_author": {(52, ""): 1, (52, "A"): 2}})}
    e = Edit("m", "H", "D", 52, "G", "pdb_author", "A")
    assert apply_point("ab", p, [e]).chains == {"H": "ACGE"}
    assert apply_point("ab", p, [e._replace(ins="", orig="C")]).chains == {"H": "AGDE"}


def test_empty_chain_ambiguous_is_C():
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
    assert len(r.vh) == len(to_fv(H).vh)
    assert apply_region(H, L, (107, 116), "ar1").reason == "bad_replacement"
    assert apply_region("GGGG", L, (107, 116), "ARDYYGSSYF").reason == "no_domain"
