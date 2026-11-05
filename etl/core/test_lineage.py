import pytest

from etl.core.lineage import get, join, kv, locator, split, step


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
