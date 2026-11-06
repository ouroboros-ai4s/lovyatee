import pytest

from etl.core.antigen_bound import Boundary, Chain, SeqCandidate, bound
from etl.core.structref import open_structure


def C(key, seq, **k):
    return Chain(key, candidates=(SeqCandidate("source_native", seq),), **k)


def test_trim_by_source_boundary():
    c = Chain("A", candidates=(SeqCandidate("source_native", "MKYLLPTAAAGLLLLAAQPAMA" + "DKTHTCPPCP"),),
              boundaries=(Boundary("source_native", 22, 32, "mature_chain"),))
    b = bound([c])
    assert b.chains == ("DKTHTCPPCP",) and "step=trim" in b.lineage[0] and "removed_n=22" in b.lineage[0]


def test_homodimer_keeps_both_chains():
    b = bound([C("B", "MKTAYIAKQR", entity="1"), C("A", "MKTAYIAKQR", entity="1")])
    assert b.chains == ("MKTAYIAKQR", "MKTAYIAKQR") and b.keys == ("A", "B")


def test_order_rules():
    assert bound([C("A", "AAA", order=2), C("B", "BBB", order=1)]).chains == ("BBB", "AAA")
    assert bound([C("A", "AAA", order=1), C("B", "BBB")]).reason == "order_ambiguous"
    assert bound([C("A", "AAA", order=1), C("B", "BBB", order=1)]).reason == "order_ambiguous"


def test_exclusions():
    assert bound([Chain("D", is_protein=False)]).reason == "non_protein"
    assert bound([]).reason == "no_sequence" and bound([Chain("A")]).reason == "no_sequence"
    two = Chain("A", candidates=(SeqCandidate("source_native", "AAA"),
                                 SeqCandidate("source_native", "AAB")))
    assert bound([two]).reason == "sequence_conflict"
    amb = Chain("A", candidates=(SeqCandidate("source_native", "AAAAA"),),
                boundaries=(Boundary("source_native", 0, 3, "domain"),
                            Boundary("source_native", 1, 4, "domain")))
    assert bound([amb]).reason == "boundary_ambiguous"
    oor = Chain("A", candidates=(SeqCandidate("source_native", "AAA"),),
                boundaries=(Boundary("source_native", 0, 9, "domain"),))
    assert bound([oor]).reason == "boundary_out_of_range"


def test_higher_level_wins_and_structure_mismatch_is_recorded_not_fatal():
    c = Chain("A", candidates=(SeqCandidate("source_native", "AAAA"),
                               SeqCandidate("structure_canonical", "AAAB")),
              observed_segments=("BB",))
    b = bound([c])
    assert b.chains == ("AAAA",) and "structure=mismatch" in " ".join(b.lineage) \
        and "conflict=1" in " ".join(b.lineage)


@pytest.mark.network
def test_her2_from_1N8Z_observed_segments_are_consistent(tmp_path):
    rec = next(c for c in open_structure("1N8Z", cache_dir=tmp_path).chains.values()
               if len(c.full_seq) == 607)
    b = bound([Chain(rec.chain_id, candidates=(SeqCandidate("structure_canonical", rec.full_seq),),
                     observed_segments=rec.observed_segments())])
    assert b.chains == (rec.full_seq,) and "structure=consistent" in " ".join(b.lineage)
