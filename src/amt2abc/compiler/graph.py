from typing import List

import networkx as nx

from amt2abc.models.amt import AMT


class AMTGraph:
    def __init__(self) -> None:
        self.graph: nx.DiGraph[str] = nx.DiGraph()

    def build(self, amts: List[AMT]) -> None:
        for amt in amts:
            for triplet in amt.triplets:
                self.graph.add_edge(
                    triplet.cause,
                    triplet.effect,
                    relation=triplet.relation,
                    mechanism=triplet.mechanism,
                    amt_id=amt.id,
                )

    def find_path(self, source: str, target: str) -> List[str]:
        try:
            path: List[str] = nx.shortest_path(
                self.graph, source=source, target=target
            )
            return path
        except (nx.NodeNotFound, nx.NetworkXNoPath):
            return []
