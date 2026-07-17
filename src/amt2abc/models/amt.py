from typing import List

from pydantic import BaseModel, Field


class Triplet(BaseModel):
    cause: str = Field(description="Cause variable, e.g. 'mold_temperature'")
    effect: str = Field(description="Effect variable, e.g. 'porosity_rate'")
    relation: str = Field(
        description="Causal relation direction: 'increases', 'decreases'",
    )
    mechanism: str = Field(
        description="Physical mechanism description",
    )


class AMT(BaseModel):
    id: str = Field(description="Unique identifier, e.g. 'amt-die-casting-001'")
    name: str = Field(description="Human-readable name")
    domain: str = Field(description="Industrial domain, e.g. 'die_casting'")
    triplets: List[Triplet] = Field(description="Ordered list of causal triplets")
    tags: List[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
