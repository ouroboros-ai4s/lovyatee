from pathlib import Path

import pytest

from etl.core.structref import ChainRecord, StructureNotFound, open_structure, pick_sequence

R14_DIR = Path("/data_new/ywy/dataset-abag/SRC_R14_ABBIND/snapshot-2019-04-10")


@pytest.mark.data
def test_snapshot_3BDY_pdb():
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
    with pytest.raises(StructureNotFound):
        open_structure("0ZZZ", cache_dir=tmp_path)


def test_pick_sequence_priority():
    rec = ChainRecord("H", "1", True, "ABCDEFG", "ABCEFG", {})
    assert pick_sequence(rec, source="XBCDEFG")[0] == "XBCDEFG"
    seq, lin = pick_sequence(rec)
    assert seq == "ABCDEFG" and lin[0].startswith("step=structure_recover")
    assert pick_sequence(ChainRecord("H", "1", True, "", "ABCEFG", {}))[0] == "ABCEFG"
