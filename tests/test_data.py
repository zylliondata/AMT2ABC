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
