
import yaml

from amt2abc.models.gs import GoalStatement


class GSParser:
    def load(self, path: str) -> GoalStatement:
        with open(path, encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        return GoalStatement(**raw)

    def parse_text(self, text: str) -> GoalStatement:
        return GoalStatement(text=text)
