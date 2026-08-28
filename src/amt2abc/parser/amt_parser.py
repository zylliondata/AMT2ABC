from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml  # type: ignore[import-untyped]

from amt2abc.models.amt import AMT


class AMTParseError(Exception):
    """Raised when an AMT YAML file cannot be parsed or validated."""


class AMTParser:
    def __init__(
        self,
        data_dir: str = "data/amt",
        strict: bool = True,
    ) -> None:
        self.data_dir = Path(data_dir)
        self.strict = strict

    def load_all(self) -> List[AMT]:
        amts: List[AMT] = []
        path = self._resolve_dir()
        if path is None:
            return amts
        for file in sorted(path.glob("*.yaml")):
            amts.append(self.load_one(file))
        return amts

    def load_one(self, path: Path) -> AMT:
        raw = self._read_yaml(path)
        try:
            return AMT(**raw)
        except Exception as exc:
            if self.strict:
                raise AMTParseError(
                    f"Invalid AMT in {path}: {exc}"
                ) from exc
            raise

    def load_text(self, text: str) -> AMT:
        raw = self._parse(text)
        try:
            return AMT(**raw)
        except Exception as exc:
            if self.strict:
                raise AMTParseError(f"Invalid AMT: {exc}") from exc
            raise

    def _resolve_dir(self) -> Optional[Path]:
        if self.data_dir.exists():
            return self.data_dir
        return None

    def _read_yaml(self, path: Path) -> Dict[str, Any]:
        try:
            with path.open(encoding="utf-8") as f:
                return self._parse(f.read())
        except OSError as exc:
            raise AMTParseError(f"Cannot read {path}: {exc}") from exc

    def _parse(self, text: str) -> Dict[str, Any]:
        try:
            raw = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise AMTParseError(f"Invalid YAML: {exc}") from exc
        if not isinstance(raw, dict):
            raise AMTParseError("AMT document must be a mapping")
        return raw
