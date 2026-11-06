import pytest

from etl.core.resolve import Candidate, Resolved, resolve

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
