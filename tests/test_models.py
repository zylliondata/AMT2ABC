from amt2abc.models.abc import ABC
from amt2abc.models.amt import AMT, Triplet
from amt2abc.models.gs import GoalStatement
from amt2abc.models.secp import SECP, CauseRef, EffectRef, SECPFrame, SECPStructure


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


def test_amt_secp_fields():
    amt = AMT(
        id="test-secp",
        name="Test",
        domain="die_casting",
        triplets=[],
        layer="天理",
        evidence_source="physics_law",
        mcl_engine="numerical_calculation",
        formula_dsl="q = -k*dT/dx",
        secp=SECPFrame(
            S=SECPStructure(subject="模具", attributes=["模温分布"]),
            E=["热传导"],
            C={"k": "80-120 W/(m·K)"},
            P=["冷却", "带热"],
        ),
        cause=CauseRef(entity="模具", attribute="模温", value_range="200-400°C"),
        effect=EffectRef(event="缩孔形成", entity="压铸件"),
    )
    assert amt.layer == "天理"
    assert amt.secp is not None
    assert amt.secp.S.subject == "模具"
    assert amt.secp.C["k"] == "80-120 W/(m·K)"
    assert amt.cause is not None
    assert amt.cause.entity == "模具"


def test_triplet_weight_confidence():
    t = Triplet(
        cause="a",
        effect="b",
        relation="decreases",
        mechanism="m",
        weight=0.9,
        confidence=0.8,
        formula="y = k*x",
    )
    assert t.weight == 0.9
    assert t.confidence == 0.8
    assert t.formula == "y = k*x"


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
    secp = SECP(
        S=SECPStructure(subject="模具"),
        E=["热传导"],
        C={},
        P=[],
    )
    assert secp.S.subject == "模具"
