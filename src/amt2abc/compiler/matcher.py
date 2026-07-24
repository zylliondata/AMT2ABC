from typing import List, Set, Tuple

from amt2abc.models.amt import AMT
from amt2abc.models.gs import GoalStatement


class GoalMatcher:
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
