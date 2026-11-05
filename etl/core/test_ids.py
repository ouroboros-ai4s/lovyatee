import pytest

from etl.core.ids import (IdCollision, ab_canonical, ab_id, ag_canonical, ag_id,
                          check_collisions, three_a_id)

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
