from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

import yaml  # type: ignore[import-untyped]

from amt2abc.models.gs import GoalStatement


class GSParseError(Exception):
    """Raised when a goal statement YAML cannot be parsed or validated."""


STOP_WORDS = {
    "a",
    "an",
    "the",
    "of",
    "and",
    "in",
    "for",
    "by",
    "to",
    "on",
    "at",
    "rate",
    "level",
    "our",
    "from",
}

DIRECTION_WORDS: Dict[str, Literal["increase", "decrease"]] = {
    "decrease": "decrease",
    "reduce": "decrease",
    "lower": "decrease",
    "cut": "decrease",
    "minimize": "decrease",
    "increase": "increase",
    "raise": "increase",
    "boost": "increase",
    "maximize": "increase",
    "improve": "increase",
    "enhance": "increase",
}


class GSParser:
    def __init__(
        self,
        data_dir: str = "data/goals",
        strict: bool = True,
    ) -> None:
        self.data_dir = Path(data_dir)
        self.strict = strict

    def load_all(self) -> List[GoalStatement]:
        goals: List[GoalStatement] = []
        if not self.data_dir.exists():
            return goals
        for file in sorted(self.data_dir.glob("*.yaml")):
            goals.append(self.load(str(file)))
        return goals

    def load(self, path: str) -> GoalStatement:
        p = Path(path)
        try:
            with p.open(encoding="utf-8") as f:
                raw = self._parse(f.read())
        except OSError as exc:
            raise GSParseError(f"Cannot read {p}: {exc}") from exc
        try:
            return GoalStatement(**raw)
        except Exception as exc:
            if self.strict:
                raise GSParseError(
                    f"Invalid goal statement in {p}: {exc}"
                ) from exc
            raise

    def load_text(self, text: str) -> GoalStatement:
        raw = self._parse(text)
        try:
            return GoalStatement(**raw)
        except Exception as exc:
            if self.strict:
                raise GSParseError(f"Invalid goal statement: {exc}") from exc
            raise

    def parse_text(self, text: str) -> GoalStatement:
        """Heuristically parse a natural-language goal, e.g. 'Reduce porosity rate'."""
        lowered = text.lower()
        words = [
            w.strip(".,;:!?()[]")
            for w in lowered.split()
            if w.strip(".,;:!?()[]")
        ]

        direction: Optional[Literal["increase", "decrease"]] = None
        direction_index = -1
        for index, word in enumerate(words):
            if word in DIRECTION_WORDS:
                direction = DIRECTION_WORDS[word]
                direction_index = index
                break

        target_variable: Optional[str] = None
        if direction_index >= 0:
            for token in words[direction_index + 1 :]:
                if token not in STOP_WORDS:
                    target_variable = token
                    break

        keywords = [
            w for w in words if len(w) > 2 and w not in STOP_WORDS
        ]
        return GoalStatement(
            text=text,
            target_variable=target_variable,
            desired_direction=direction,
            keywords=keywords,
        )

    def _parse(self, text: str) -> Dict[str, Any]:
        try:
            raw = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise GSParseError(f"Invalid YAML: {exc}") from exc
        if not isinstance(raw, dict):
            raise GSParseError("Goal statement document must be a mapping")
        return raw
