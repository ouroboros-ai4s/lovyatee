from etl.core.seqnorm import normalize


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
