import json
from pathlib import Path
from typing import Any, Dict, List

from amt2abc.models.abc import ABC


class ABCParser:
    def __init__(self, data_dir: str = "data/abc") -> None:
        self.data_dir = Path(data_dir)

    def load_all(self) -> List[ABC]:
        abcs: List[ABC] = []
        if not self.data_dir.exists():
            return abcs
        for path in sorted(self.data_dir.glob("*.json")):
            abcs.append(self.load_one(path))
        return abcs

    def load_one(self, path: Path) -> ABC:
        with path.open(encoding="utf-8") as f:
            raw: Dict[str, Any] = json.load(f)
        return ABC(**raw)
