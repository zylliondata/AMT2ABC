from amt2abc.compiler.graph import AMTGraph
from amt2abc.compiler.matcher import GoalMatcher
from amt2abc.compiler.pipeline import CompilerPipeline
from amt2abc.models.amt import AMT, Triplet
from amt2abc.models.gs import GoalStatement


def _amt(amt_id, triplets, name="test", domain="test"):
    return AMT(
        id=amt_id,
        name=name,
        domain=domain,
        triplets=[
            Triplet(
                cause=c,
                effect=e,
                relation=r,
                mechanism="m",
            )
            for c, e, r in triplets
        ],
    )


def test_graph_build():
    amt = _amt("g001", [("temp", "porosity", "increases")])
    graph = AMTGraph()
    graph.build([amt])
    assert graph.graph.has_edge("temp", "porosity")
    assert graph.amt_graph.has_node("g001")


def test_graph_find_path():
    amt = _amt(
        "g001",
        [
            ("a", "b", "increases"),
            ("b", "c", "increases"),
        ],
    )
    graph = AMTGraph()
    graph.build([amt])
    assert graph.find_path("a", "c") == ["a", "b", "c"]
    assert graph.find_path("c", "a") == []
    assert graph.find_path("missing", "a") == []


def test_graph_amt_linking():
    up = _amt("up", [("a", "shared", "increases")])
    down = _amt("down", [("shared", "b", "increases")])
    graph = AMTGraph()
    graph.build([up, down])
    assert graph.amt_graph.has_edge("up", "down")
    assert graph.amt_edge_details() == [("up", "down", "shared")]
    assert graph.find_amt_path("up", "down") == ["up", "down"]


def test_graph_upstream_downstream():
    amt = _amt(
        "g001",
        [
            ("a", "b", "increases"),
            ("b", "c", "increases"),
        ],
    )
    graph = AMTGraph()
    graph.build([amt])
    assert graph.upstream("c") == ["a", "b"]
    assert graph.downstream("a") == ["b", "c"]
    assert graph.upstream("unknown") == []


def test_graph_amts_causing():
    amt = _amt("m1", [("temp", "porosity", "increases")])
    graph = AMTGraph()
    graph.build([amt])
    assert graph.amts_causing("porosity") == ["m1"]
    assert graph.amts_caused_by("temp") == ["m1"]


def test_graph_connected_components():
    a = _amt("a", [("x1", "x2", "increases")])
    b = _amt("b", [("y1", "y2", "increases")])
    graph = AMTGraph()
    graph.build([a, b])
    components = graph.connected_components()
    assert len(components) == 2


def test_graph_subgraph():
    amt = _amt(
        "g001",
        [
            ("a", "b", "increases"),
            ("c", "d", "increases"),
        ],
    )
    graph = AMTGraph()
    graph.build([amt])
    sub = graph.subgraph(["a", "b"])
    assert set(sub.graph.nodes) == {"a", "b"}
    assert "c" not in sub.graph.nodes


def test_graph_stats_and_dict():
    amt = _amt("g001", [("a", "b", "increases")])
    graph = AMTGraph()
    graph.build([amt])
    stats = graph.stats()
    assert stats["variables"] == 2
    assert stats["variable_edges"] == 1
    assert stats["amts"] == 1
    data = graph.to_dict()
    assert "a" in data["variables"]
    assert data["amt_nodes"] == ["g001"]


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
