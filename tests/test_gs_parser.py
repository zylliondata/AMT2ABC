import pytest
from amt2abc.models.gs import GoalStatement, GoalTarget
from amt2abc.parser.gs_parser import GSParseError, GSParser


def test_parse_text_reduce():
    gs = GSParser().parse_text("reduce porosity rate")
    assert gs.target_variable == "porosity"
    assert gs.desired_direction == "decrease"
    assert "porosity" in gs.keywords


def test_parse_text_increase():
    gs = GSParser().parse_text("increase mold temperature")
    assert gs.desired_direction == "increase"
    assert gs.target_variable == "mold"
    assert "temperature" in gs.keywords


def test_parse_text_no_direction():
    gs = GSParser().parse_text("porosity issue in die casting")
    assert gs.desired_direction is None
    assert gs.target_variable is None
    assert "porosity" in gs.keywords


def test_load_yaml(tmp_path):
    yaml_text = (
        "id: GS_DC_POROSITY_001\n"
        "text: Reduce porosity rate\n"
        "domain: die_casting\n"
        "target_variable: porosity_rate\n"
        "desired_direction: decrease\n"
        "priority: high\n"
        "keywords: [porosity]\n"
    )
    path = tmp_path / "goal.yaml"
    path.write_text(yaml_text, encoding="utf-8")
    gs = GSParser().load(str(path))
    assert gs.id == "GS_DC_POROSITY_001"
    assert gs.desired_direction == "decrease"
    assert gs.priority == "high"


def test_load_text():
    gs = GSParser().load_text(
        "text: improve quality\nkeywords: [quality]"
    )
    assert gs.text == "improve quality"
    assert gs.keywords == ["quality"]


def test_load_invalid_yaml(tmp_path):
    path = tmp_path / "bad.yaml"
    path.write_text("text: [unclosed", encoding="utf-8")
    with pytest.raises(GSParseError):
        GSParser().load(str(path))


def test_load_not_mapping():
    with pytest.raises(GSParseError):
        GSParser().load_text("- just\n- a\n- list")


def test_goal_target_model():
    target = GoalTarget(
        variable="porosity_rate",
        direction="decrease",
        reduction_pct=20,
        unit="%",
    )
    gs = GoalStatement(
        text="Reduce porosity by 20%",
        target=target,
        priority="high",
    )
    assert gs.target.reduction_pct == 20
    assert gs.priority == "high"


def test_load_all_empty(tmp_path):
    assert GSParser(data_dir=str(tmp_path)).load_all() == []


def test_load_all_from_data_dir():
    goals = GSParser(data_dir="data/goals").load_all()
    assert len(goals) >= 1
    assert goals[0].id == "GS_DC_POROSITY_001"
