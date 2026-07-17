from amt2abc.compiler.graph import AMTGraph
from amt2abc.compiler.matcher import GoalMatcher
from amt2abc.compiler.pipeline import CompilerPipeline
from amt2abc.models.amt import AMT, Triplet
from amt2abc.models.gs import GoalStatement


def test_graph_build():
    amt = AMT(
        id="g001",
        name="test",
        domain="test",
        triplets=[
            Triplet(
                cause="temp",
                effect="porosity",
                relation="increases",
                mechanism="m1",
            ),
        ],
    )
    graph = AMTGraph()
    graph.build([amt])
    assert graph.graph.has_edge("temp", "porosity")


def test_graph_find_path():
    amt = AMT(
        id="g001",
        name="test",
        domain="test",
        triplets=[
            Triplet(cause="a", effect="b", relation="increases", mechanism="m1"),
            Triplet(cause="b", effect="c", relation="increases", mechanism="m2"),
        ],
    )
    graph = AMTGraph()
    graph.build([amt])
    path = graph.find_path("a", "c")
    assert path == ["a", "b", "c"]


def test_matcher_score():
    amt = AMT(
        id="m001",
        name="temperature control",
        domain="test",
        triplets=[
            Triplet(
                cause="temp",
                effect="porosity",
                relation="increases",
                mechanism="thermal",
            ),
        ],
        tags=["porosity", "mold"],
    )
    goal = GoalStatement(text="reduce porosity", keywords=["porosity"])
    matcher = GoalMatcher([amt])
    matches = matcher.match(goal)
    assert len(matches) == 1
    assert matches[0][0].id == "m001"


def test_pipeline_no_data(tmp_path):
    pipeline = CompilerPipeline(amt_dir=str(tmp_path))
    result = pipeline.compile("reduce porosity")
    assert result["goal"] == "reduce porosity"
    assert result["matched_amts"] == []
