from typing import Any, Dict

from amt2abc.compiler.graph import AMTGraph
from amt2abc.compiler.matcher import GoalMatcher
from amt2abc.parser.amt_parser import AMTParser
from amt2abc.parser.gs_parser import GSParser


class CompilerPipeline:
    def __init__(self, amt_dir: str = "data/amt") -> None:
        self.amts = AMTParser(amt_dir).load_all()
        self.graph = AMTGraph()
        self.graph.build(self.amts)
        self.matcher = GoalMatcher(self.amts)

    def compile(self, goal_text: str) -> Dict[str, Any]:
        goal = GSParser().parse_text(goal_text)
        matches = self.matcher.match(goal)
        return {
            "goal": goal_text,
            "matched_amts": [
                {"id": amt.id, "name": amt.name, "score": round(s, 2)}
                for amt, s in matches
            ],
            "recommended_abcs": [],
        }
