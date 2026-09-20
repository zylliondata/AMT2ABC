import json

from amt2abc.compiler.builder import GraphBuilder
from amt2abc.compiler.graph import AMTGraph
from amt2abc.models.amt import AMT, Triplet


def _amt(amt_id, triplets, name="test", domain="test"):
    return AMT(
        id=amt_id,
        name=name,
        domain=domain,
        triplets=[
            Triplet(cause=c, effect=e, relation=r, mechanism="m")
            for c, e, r in triplets
        ],
    )


def test_builder_add_and_build():
    builder = GraphBuilder().add_amt(_amt("a", [("x", "y", "increases")]))
    graph = builder.build()
    assert isinstance(graph, AMTGraph)
    assert graph.graph.has_edge("x", "y")


def test_builder_add_amts():
    builder = GraphBuilder().add_amts(
        [
            _amt("a", [("x", "y", "increases")]),
            _amt("b", [("y", "z", "increases")]),
        ]
    )
    graph = builder.build()
    assert graph.amt_graph.has_edge("a", "b")


def test_builder_validate_ok():
    builder = GraphBuilder().add_amt(_amt("a", [("x", "y", "increases")]))
    report = builder.validate()
    assert report.ok
    assert report.amt_count == 1
    assert report.variable_count == 2
    assert report.variable_edge_count == 1


def test_builder_validate_duplicate_ids():
    builder = GraphBuilder().add_amts(
        [
            _amt("dup", [("x", "y", "increases")]),
            _amt("dup", [("y", "z", "increases")]),
        ]
    )
    report = builder.validate()
    assert not report.ok
    assert report.duplicate_ids == ["dup"]


def test_builder_validate_no_triplets():
    builder = GraphBuilder().add_amt(_amt("empty", []))
    report = builder.validate()
    assert not report.ok
    assert report.amts_without_triplets == ["empty"]


def test_builder_build_checked():
    builder = GraphBuilder().add_amt(_amt("a", [("x", "y", "increases")]))
    graph, report = builder.build_checked()
    assert isinstance(graph, AMTGraph)
    assert report.ok


def test_builder_from_directory():
    builder = GraphBuilder().from_directory()
    graph, report = builder.build_checked()
    assert report.amt_count >= 3
    assert graph.graph.number_of_nodes() >= 3


def test_builder_export_json(tmp_path):
    builder = GraphBuilder().add_amt(_amt("a", [("x", "y", "increases")]))
    out = builder.export_json(str(tmp_path / "graph.json"))
    assert out.exists()
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "graph" in payload
    assert "report" in payload
    assert payload["report"]["ok"] is True


def test_build_report_to_dict():
    builder = GraphBuilder().add_amt(_amt("a", [("x", "y", "increases")]))
    data = builder.validate().to_dict()
    assert data["amt_count"] == 1
    assert data["ok"] is True
