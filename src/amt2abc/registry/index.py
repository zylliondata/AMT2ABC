import json
from pathlib import Path
from typing import List


class RegistryIndex:
    def __init__(self, path: str = "abc-registry/index.json"):
        self.path = Path(path)

    def load(self) -> dict:
        if not self.path.exists():
            return {"abcs": []}
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)

    def search(self, keyword: str) -> List[dict]:
        data = self.load()
        kw = keyword.lower()
        return [
            abc
            for abc in data.get("abcs", [])
            if kw in abc.get("name", "").lower()
            or kw in abc.get("description", "").lower()
        ]
