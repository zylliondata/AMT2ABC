from typing import Any, Dict, List, Optional, Set, Tuple

from amt2abc.compiler.graph import AMTGraph
from amt2abc.models.amt import AMT
from amt2abc.models.gs import GoalStatement


class GoalMatcher:
    """Keyword-only matcher used as a fallback when no target variable exists."""

    def __init__(self, amts: List[AMT]) -> None:
        self.amts = amts

    def match(self, goal: GoalStatement) -> List[Tuple[AMT, float]]:
        scored: List[Tuple[AMT, float]] = []
        keywords: Set[str] = set(
            w.lower() for w in goal.keywords or goal.text.lower().split()
        )
        for amt in self.amts:
            score = self._score(amt, keywords)
            if score > 0:
                scored.append((amt, score))
        scored.sort(key=lambda x: -x[1])
        return scored

    def _score(self, amt: AMT, keywords: Set[str]) -> float:
        text = (amt.name + " " + " ".join(amt.tags)).lower()
        for t in amt.triplets:
            text += " " + t.cause + " " + t.effect + " " + t.mechanism
        text_lower = text.lower()
        matches = sum(1 for kw in keywords if kw in text_lower)
        return matches / max(len(keywords), 1)


TARGET_WEIGHT = 0.6
UPSTREAM_WEIGHT = 0.3
KEYWORD_WEIGHT = 0.4


class GraphMatcher:
    """Graph-aware matcher: locate the target variable in the causal graph,
    seed candidate AMTs from those that influence it, and rank them with
    keyword evidence."""

    def __init__(
        self,
        amts: List[AMT],
        graph: Optional[AMTGraph] = None,
    ) -> None:
        self.amts = amts
        self.graph = graph if graph is not None else self._build(amts)
        self._keyword = GoalMatcher(amts)

    def _build(self, amts: List[AMT]) -> AMTGraph:
        graph = AMTGraph()
        graph.build(amts)
        return graph

    def resolve_target(self, target: str) -> Optional[str]:
        """Map a user-provided variable name onto an actual graph variable.

        Prefers exact matches, then variables that contain the target token,
        then variables contained in the target token.
        """
        nodes: List[str] = list(self.graph.graph.nodes)
        if target in nodes:
            return target
        for node in nodes:
            if target in node:
                return node
        for node in nodes:
            if node in target:
                return node
        return None

    def match(self, goal: GoalStatement) -> List[Tuple[AMT, float]]:
        keywords: Set[str] = set(
            w.lower() for w in goal.keywords or goal.text.lower().split()
        )

        if not goal.target_variable:
            return self._keyword.match(goal)

        target = self.resolve_target(goal.target_variable)
        if target is None:
            return self._keyword.match(goal)

        direct_ids = set(self.graph.amts_causing(target))
        upstream_ids = set(self.graph.amts_caused_by(target))
        for var in self.graph.upstream(target):
            upstream_ids.update(self.graph.amts_caused_by(var))

        scored: List[Tuple[AMT, float]] = []
        for amt in self.amts:
            kw = self._keyword._score(amt, keywords)
            graph_bonus = 0.0
            if amt.id in direct_ids:
                graph_bonus += TARGET_WEIGHT
            if amt.id in upstream_ids:
                graph_bonus += UPSTREAM_WEIGHT
            score = graph_bonus + kw * KEYWORD_WEIGHT
            if score > 0:
                scored.append((amt, score))
        scored.sort(key=lambda x: -x[1])
        return scored

    def influencing_subgraph(
        self, goal: GoalStatement
    ) -> Dict[str, Any]:
        """AMT-layer subgraph that can influence the goal's target variable."""
        if not goal.target_variable:
            return {"target": None, "amts": [], "edges": []}

        target = self.resolve_target(goal.target_variable)
        if target is None:
            return {"target": goal.target_variable, "amts": [], "edges": []}

        amt_ids: Set[str] = set(self.graph.amts_causing(target))
        for var in self.graph.upstream(target):
            amt_ids.update(self.graph.amts_caused_by(var))

        edges: List[Dict[str, str]] = [
            {"from": u, "to": v, "via": d.get("via", "")}
            for u, v, d in self.graph.amt_graph.edges(data=True)
            if u in amt_ids and v in amt_ids
        ]
        return {
            "target": target,
            "amts": sorted(amt_ids),
            "edges": edges,
        }
