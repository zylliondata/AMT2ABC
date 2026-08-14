from typing import Any, Dict, List

from pydantic import BaseModel, Field


class SECPStructure(BaseModel):
    subject: str = Field(default="", description="Main subject, e.g. 'mold'")
    attributes: List[str] = Field(default_factory=list)


class SECPFrame(BaseModel):
    """SECP four-dimension fingerprint: Structure / Event / Configuration / Process."""

    S: SECPStructure = Field(
        default_factory=SECPStructure,
        description="Structure dimension: subject and attributes",
    )
    E: List[str] = Field(default_factory=list, description="Events/actions")
    C: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configuration parameters",
    )
    P: List[str] = Field(default_factory=list, description="Process steps")


class CauseRef(BaseModel):
    entity: str = Field(default="")
    attribute: str = Field(default="")
    value_range: str = Field(default="")


class EffectRef(BaseModel):
    event: str = Field(default="")
    entity: str = Field(default="")


SECP = SECPFrame
