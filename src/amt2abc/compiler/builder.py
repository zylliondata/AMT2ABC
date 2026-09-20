import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set, Tuple

from amt2abc.compiler.graph import AMTGraph
from amt2abc.models.amt import AMT
from amt2abc.parser.amt_parser import AMTParser


@dataclass
class BuildReport:
    """Diagnostics collected while building an AMT graph."""

    amt_count: int = 0
    variable_count: int = 0
    variable_edge_count: int = 0
    amt_edge_count: int = 0
    duplicate_ids: List[str] = field(default_factory=list)
    amts_without_triplets: List[str] = field(default_factory=list)
    isolated_variables: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.duplicate_ids and not self.amts_without_triplets

    def to_dict(self) -> Dict[str, Any]:
        return {
            "amt_count": self.amt_count,
            "variable_count": self.variable_count,
            "variable_edge_count": self.variable_edge_count,
            "amt_edge_count": self.amt_edge_count,
            "duplicate_ids": self.duplicate_ids,
            "amts_without_triplets": self.amts_without_triplets,
            "isolated_variables": self.isolated_variables,
            "warnings": self.warnings,
            "ok": self.ok,
        }


class GraphBuilder:
    """Fluent builder that assembles an :class:`AMTGraph` from AMTs."""

    def __init__(self) -> None:
        self._amts: List[AMT] = []

    def add_amt(self, amt: AMT) -> "GraphBuilder":
        self._amts.append(amt)
        return self

    def add_amts(self, amts: Iterable[AMT]) -> "GraphBuilder":
        self._amts.extend(amts)
        return self

    def from_directory(self, data_dir: str = "data/amt") -> "GraphBuilder":
        self._amts.extend(AMTParser(data_dir).load_all())
        return self

    def validate(self) -> BuildReport:
        report = BuildReport(amt_count=len(self._amts))

        seen: Set[str] = set()
        for amt in self._amts:
            if amt.id in seen:
                report.duplicate_ids.append(amt.id)
            seen.add(amt.id)
            if not amt.triplets:
                report.amts_without_triplets.append(amt.id)

        graph = AMTGraph()
        graph.build(self._amts)

        report.variable_count = graph.graph.number_of_nodes()
        report.variable_edge_count = graph.graph.number_of_edges()
        report.amt_edge_count = graph.amt_graph.number_of_edges()

        report.isolated_variables = [
            node
            for node in graph.graph.nodes
            if graph.graph.in_degree(node) == 0
            and graph.graph.out_degree(node) == 0
        ]

        if report.duplicate_ids:
            report.warnings.append(
                f"duplicate AMT ids: {sorted(set(report.duplicate_ids))}"
            )
        if report.amts_without_triplets:
            report.warnings.append(
                f"AMTs without triplets: {report.amts_without_triplets}"
            )
        return report

    def build(self) -> AMTGraph:
        graph = AMTGraph()
        graph.build(self._amts)
        return graph

    def build_checked(self) -> Tuple[AMTGraph, BuildReport]:
        report = self.validate()
        graph = self.build()
        return graph, report

    def export_json(self, path: str) -> Path:
        graph = self.build()
        payload = {
            "report": self.validate().to_dict(),
            "graph": graph.to_dict(),
        }
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        return out
