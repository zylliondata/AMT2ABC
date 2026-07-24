import json
from pathlib import Path
from typing import Any, Dict, List


class RegistryIndex:
    def __init__(self, path: str = "abc-registry/index.json") -> None:
        self.path = Path(path)

    def load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return {"abcs": []}
        with self.path.open(encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)
        return data

    def search(self, keyword: str) -> List[Dict[str, Any]]:
        data = self.load()
        kw = keyword.lower()
        return [
            abc
            for abc in data.get("abcs", [])
            if kw in abc.get("name", "").lower()
            or kw in abc.get("description", "").lower()
        ]
