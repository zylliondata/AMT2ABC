from typing import Any, Dict, List

from pydantic import BaseModel, Field


class ABC(BaseModel):
    id: str = Field(description="Unique identifier, e.g. 'mold-temp-control'")
    name: str = Field(description="Human-readable name")
    category: str = Field(
        description="Category: 'form', 'monitoring', 'control', 'general'",
    )
    industry: str = Field(description="Industry domain, e.g. 'die_casting'")
    description: str = Field(default="")
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    source_amts: List[str] = Field(
        default_factory=list,
        description="AMT IDs that this ABC implements",
    )
