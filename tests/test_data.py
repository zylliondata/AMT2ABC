from amt2abc.parser.amt_parser import AMTParser


def test_bundled_amts_load():
    parser = AMTParser()
    amts = parser.load_all()
    assert len(amts) >= 3


def test_bundled_amt_ids_unique():
    parser = AMTParser()
    amts = parser.load_all()
    ids = [a.id for a in amts]
    assert len(ids) == len(set(ids))


def test_bundled_amt_triplets_valid():
    parser = AMTParser()
    for amt in parser.load_all():
        assert amt.triplets, f"AMT {amt.id} has no triplets"
        for t in amt.triplets:
            assert t.relation in {"increases", "decreases"}
            assert t.cause
            assert t.effect


def test_bundled_amt_porosity_goal_matches():
    parser = AMTParser()
    amts = parser.load_all()
    matched = [a for a in amts if "porosity" in a.tags or "缩孔" in a.tags]
    assert len(matched) >= 3


def test_bundled_amt_secp_structure():
    parser = AMTParser()
    for amt in parser.load_all():
        assert amt.secp is not None, f"AMT {amt.id} missing secp frame"
        assert amt.secp.S.subject, f"AMT {amt.id} missing secp.S.subject"
        assert amt.secp.E, f"AMT {amt.id} missing secp events"
        assert amt.secp.P, f"AMT {amt.id} missing secp process"
        assert amt.layer, f"AMT {amt.id} missing layer"
        assert amt.evidence_source, f"AMT {amt.id} missing evidence_source"


def test_bundled_amt_triplet_weights():
    parser = AMTParser()
    for amt in parser.load_all():
        for t in amt.triplets:
            assert 0.0 <= t.weight <= 1.0
            assert 0.0 <= t.confidence <= 1.0

