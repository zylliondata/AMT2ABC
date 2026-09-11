from typing import Any, Dict, List, Set, Tuple

import networkx as nx

from amt2abc.models.amt import AMT


class AMTGraph:
    """Two-layer causal graph over AMTs.

    - ``graph`` (variable layer): nodes are variables, edges are causal relations.
    - ``amt_graph`` (AMT layer): nodes are AMT ids, edges chain AMTs when the
      effect of one triplet matches the cause of another.
    """

    def __init__(self) -> None:
        self.graph: nx.DiGraph = nx.DiGraph()
        self.amt_graph: nx.DiGraph = nx.DiGraph()
        self._amts: Dict[str, AMT] = {}

    def build(self, amts: List[AMT]) -> None:
        self.graph.clear()
        self.amt_graph.clear()
        self._amts = {amt.id: amt for amt in amts}

        for amt in amts:
            self.amt_graph.add_node(amt.id, name=amt.name, domain=amt.domain)
            for triplet in amt.triplets:
                self.graph.add_node(triplet.cause)
                self.graph.add_node(triplet.effect)
                self.graph.add_edge(
                    triplet.cause,
                    triplet.effect,
                    relation=triplet.relation,
                    mechanism=triplet.mechanism,
                    amt_id=amt.id,
                    weight=triplet.weight,
                    confidence=triplet.confidence,
                )

        self._link_amts()

    def _link_amts(self) -> None:
        effects: Dict[str, List[str]] = {}
        causes: Dict[str, List[str]] = {}
        for amt in self._amts.values():
            for triplet in amt.triplets:
                effects.setdefault(triplet.effect, []).append(amt.id)
                causes.setdefault(triplet.cause, []).append(amt.id)
        for variable, up_ids in effects.items():
            for down_id in causes.get(variable, []):
                for up_id in up_ids:
                    if up_id != down_id:
                        self.amt_graph.add_edge(
                            up_id, down_id, via=variable
                        )

    def find_path(self, source: str, target: str) -> List[str]:
        return self._shortest(self.graph, source, target)

    def find_amt_path(self, source: str, target: str) -> List[str]:
        return self._shortest(self.amt_graph, source, target)

    def _shortest(self, g: nx.DiGraph, source: str, target: str) -> List[str]:
        if source not in g or target not in g:
            return []
        try:
            path: List[str] = nx.shortest_path(g, source=source, target=target)
            return path
        except nx.NetworkXNoPath:
            return []

    def upstream(self, variable: str) -> List[str]:
        if variable not in self.graph:
            return []
        return sorted(nx.ancestors(self.graph, variable))

    def downstream(self, variable: str) -> List[str]:
        if variable not in self.graph:
            return []
        return sorted(nx.descendants(self.graph, variable))

    def amts_causing(self, variable: str) -> List[str]:
        """AMT ids that have ``variable`` as an effect (they can influence it)."""
        result: Set[str] = set()
        if variable in self.graph:
            for pred in self.graph.predecessors(variable):
                result.add(self.graph.edges[pred, variable]["amt_id"])
        return sorted(result)

    def amts_caused_by(self, variable: str) -> List[str]:
        """AMT ids that have ``variable`` as a cause."""
        result: Set[str] = set()
        if variable in self.graph:
            for succ in self.graph.successors(variable):
                result.add(self.graph.edges[variable, succ]["amt_id"])
        return sorted(result)

    def connected_components(self) -> List[List[str]]:
        components = [
            sorted(c)
            for c in nx.weakly_connected_components(self.amt_graph)
        ]
        return sorted(components, key=len, reverse=True)

    def subgraph(self, variables: List[str]) -> "AMTGraph":
        selected = set(variables)
        nodes = [
            v for v in self.graph.nodes if v in selected
        ]
        sub = AMTGraph()
        sub.graph = self.graph.subgraph(nodes).copy()
        amt_ids = {
            d["amt_id"]
            for _, _, d in sub.graph.edges(data=True)
            if "amt_id" in d
        }
        sub._amts = {i: self._amts[i] for i in amt_ids if i in self._amts}
        sub.amt_graph = self.amt_graph.subgraph(list(amt_ids)).copy()
        return sub

    def to_dict(self) -> Dict[str, Any]:
        return {
            "variables": sorted(self.graph.nodes),
            "amt_nodes": sorted(self.amt_graph.nodes),
            "amt_edges": [
                {"from": u, "to": v, "via": d.get("via")}
                for u, v, d in self.amt_graph.edges(data=True)
            ],
        }

    def stats(self) -> Dict[str, int]:
        return {
            "variables": self.graph.number_of_nodes(),
            "variable_edges": self.graph.number_of_edges(),
            "amts": self.amt_graph.number_of_nodes(),
            "amt_edges": self.amt_graph.number_of_edges(),
        }

    def amt_edge_details(self) -> List[Tuple[str, str, str]]:
        return [
            (u, v, d.get("via", ""))
            for u, v, d in self.amt_graph.edges(data=True)
        ]
