from amt2abc.models.abc import ABC
from amt2abc.models.amt import AMT, Triplet
from amt2abc.models.gs import GoalStatement
from amt2abc.models.secp import SECP


def test_amt_model():
    amt = AMT(
        id="test-001",
        name="Test AMT",
        domain="die_casting",
        triplets=[
            Triplet(
                cause="temp",
                effect="porosity",
                relation="increases",
                mechanism="thermal expansion",
            ),
        ],
    )
    assert amt.id == "test-001"
    assert len(amt.triplets) == 1


def test_abc_model():
    abc = ABC(
        id="test-control",
        name="Test Control",
        category="control",
        industry="die_casting",
    )
    assert abc.category == "control"


def test_goal_statement():
    gs = GoalStatement(text="Reduce porosity", keywords=["porosity", "reduce"])
    assert gs.text == "Reduce porosity"
    assert len(gs.keywords) == 2


def test_secp_model():
    secp = SECP(id="secp-test", domain="die_casting")
    assert secp.domain == "die_casting"
