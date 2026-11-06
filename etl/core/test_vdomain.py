"""真实序列取自 /data_new/ywy/dataset-abag (SRC_R08/R74/R76)，字面量。"""

R76_H = 'QDQLQQSGAELVRPGASVKLSCKALGYIFTDYEIHWVKQTPVHGLEWIGGIHPGSSGTAYNQKFKGKATLTADKSSTTAFMELSSLTSEDSAVYYCTRKDYWGQGTLVTVSAAKTTAPSVYPLVPVCGGTTGSSVTLGCLVKGYFPEPVTLTWNSGSLSSGVHTFPALLQSGLYTLSSSVTVTSNTWPSQTITCNVAHPASSTKVDKKIEPRV'
R76_L = 'DIKMTQSPSSMYTSLGERVTITCKASQDINSFLTWFLQKPGKSPKTLIYRANRLMIGVPSRFSGSGSGQTYSLTISSLEYEDMGIYYCLQYDDFPLTFGAGTKLDLKRADAAPTVSIFPPSSEQLTSGGASVVCFLNNFYPKEINVKWKIDGSERQNGVLDSWTEQDSKDSTYSMSSTLTLTKDEYERHNSYTCEATHKTSTSPIVKSFNRNEC'
R76_H2 = 'ADLVQSGAVVKKPGDSVRISCEAQGYRFPDYIIHWIRRAPGQGPEWMGWMNPMGGQVNIPWKFQGRVSMTRDTSIETAFLDLRGLKSDDTAVYYCVRDRSNGSGKRFESSNWFLDLWGRGTAVTIQSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKRVEPK'
R76_VH = 'QDQLQQSGAELVRPGASVKLSCKALGYIFTDYEIHWVKQTPVHGLEWIGGIHPGSSGTAYNQKFKGKATLTADKSSTTAFMELSSLTSEDSAVYYCTRKDYWGQGTLVTVSA'
R76_VL = 'DIKMTQSPSSMYTSLGERVTITCKASQDINSFLTWFLQKPGKSPKTLIYRANRLMIGVPSRFSGSGSGQTYSLTISSLEYEDMGIYYCLQYDDFPLTFGAGTKLDLK'
R76_SCFV = 'EVKLLEQSGAELVKPGASVRLSCTASGFNIKDTYMSWVKQRPEQGLEWIGRIDPANGDTKYDPKFQGKATITADTSSNTAYLHLSSLTSGDTAVYYCSRGWEGFAYWGQGTLVTVSAGGGGSGGGGSGGGGSELVMTQTPASLAVSLGQRATISCRASENVDRYGNSFMHWYQQKAGQPPKLLIYRASNLESGIPARFSGSGSRTDFTLTINPVEADDVATYFCQRSNEVPWTFGGGTKLEIKRPLEHHHHHH'
R08_VHH = 'MKYLLPTAAAGLLLLAAQPAMAQVQLQESGGGLVQPGGSLRLSCKASGFTMNTATVGWFRQAPGKEREGVSCISSADVTNYADSVKGRFTISRDNPKNAVSLQMNSLKPEDTGVYYCAASRTYYPFCAGTNNFQSWGQGTQVTVSSHHHHHH'
R74_HEAVY = 'QVQLVQSGVEVKKPGASVKVSCKASGYTFTNYYMYWVRQAPGQGLEWMGGINPSNGGTNFNEKFKNRVTLTTDSSTTTAYMELKSLQFDDTAVYYCARRDYRFDMGFDYWGQGTTVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCDKTHHHHHH'
NON_ANTIBODY = 'DATPEDLGARL'

ALL = {
    'R76_H': R76_H,
    'R76_L': R76_L,
    'R76_H2': R76_H2,
    'R76_VH': R76_VH,
    'R76_VL': R76_VL,
    'R76_SCFV': R76_SCFV,
    'R08_VHH': R08_VHH,
    'R74_HEAVY': R74_HEAVY,
    'NON_ANTIBODY': NON_ANTIBODY,
}

from etl.core.lineage import get
from etl.core.vdomain import Hints, parse, parse_batch, pair_slots, to_fv

SCFV_LINKER = "GGGGSGGGGSGGGGS"


def test_vhh_signal_peptide_and_his_tag():
    c = to_fv(R08_VHH)
    assert c.reason is None and c.vl is None and c.vh in R08_VHH and 100 < len(c.vh) < 140
    assert get(c.lineage[0], "c_tag") == "His6" and 18 <= int(get(c.lineage[0], "n_len")) <= 26


def test_full_heavy_with_constant_and_his_tag():
    c = to_fv(R74_HEAVY)
    assert c.vh is not None and get(c.lineage[0], "c_tag") == "His6" and int(get(c.lineage[0], "c_len")) > 50


def test_scfv_with_g4s_linker_splits():
    c = to_fv(R76_SCFV)
    assert c.reason is None and c.vh and c.vl
    assert get(c.lineage[-1], "step") == "split" and get(c.lineage[-1], "linker") == SCFV_LINKER


def test_reversed_scfv_swaps_into_fields():
    c = to_fv(R76_VL + SCFV_LINKER + R76_VH)
    assert (c.vh, c.vl) == (R76_VH, R76_VL) and get(c.lineage[-1], "orientation") == "VL-VH"


def test_unknown_linker_is_unresolved_unless_hinted():
    s = R76_VH + "AAAAAAAAAAAA" + R76_VL
    assert to_fv(s).reason == "unresolved"
    assert to_fv(s, Hints(linker="AAAAAAAAAAAA")).reason is None


def test_single_chain_hint_accepts_unrecognised_linker():
    """来源声明的单链构建体：两域之间没有可识别的 G4S linker 时仍按 scFv 拆分。"""
    seq = R76_VH + "AAAAGSASTKGP" + R76_VL
    assert to_fv(seq).reason == "unresolved"
    c = to_fv(seq, Hints(single_chain=True))
    assert c.reason is None and c.vh and c.vl
    assert "step=split" in c.lineage[-1] and "linker=AAAAGSASTKGP" in c.lineage[-1]


def test_pair_slots_cases():
    assert pair_slots(R76_H, R76_L).reason is None
    assert pair_slots(R76_L, R76_H).lineage[0].startswith("step=slot_swap")
    assert pair_slots(R76_H, R76_H).reason == "slot_collision"
    assert pair_slots(R76_SCFV, R76_SCFV).lineage[0].startswith("step=slot_single")
    assert pair_slots(R76_H, R76_H2).reason == "unresolved"
    assert pair_slots(R76_H, None).vl is None and pair_slots(None, R76_L).vh is None


def test_unnumberable_inputs_return_no_domain():
    for s in ["", "A" * 8, "GGGGSGGGGS", NON_ANTIBODY]:
        assert to_fv(s).reason == "no_domain"


def test_hint_span_overrides_anarci_and_records_conflict():
    d = parse(R74_HEAVY).domains[0]
    c = to_fv(R74_HEAVY, Hints(spans=((d.start, d.end + 2),)))
    assert c.vh == R74_HEAVY[d.start:d.end + 2] and get(c.lineage[0], "conflict") == "1"


def test_parse_batch_matches_single():
    seqs = [R76_H, R76_L, R08_VHH, R74_HEAVY]
    assert [(p.domains[0].start, p.domains[0].end) for p in parse_batch(seqs)] == \
           [(parse(s).domains[0].start, parse(s).domains[0].end) for s in seqs]
