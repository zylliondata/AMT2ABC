from pathlib import Path
from typing import Any, Dict, List

import yaml  # type: ignore[import-untyped]

from amt2abc.models.amt import AMT


class AMTParser:
    def __init__(self, data_dir: str = "data/amt") -> None:
        self.data_dir = Path(data_dir)

    def load_all(self) -> List[AMT]:
        amts: List[AMT] = []
        if not self.data_dir.exists():
            return amts
        for path in sorted(self.data_dir.glob("*.yaml")):
            amts.append(self.load_one(path))
        return amts

    def load_one(self, path: Path) -> AMT:
        with path.open(encoding="utf-8") as f:
            raw: Dict[str, Any] = yaml.safe_load(f)
        return AMT(**raw)
