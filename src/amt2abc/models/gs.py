from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class GoalTarget(BaseModel):
    """Quantified target for a goal statement."""

    variable: str = Field(description="Variable being targeted, e.g. 'porosity_rate'")
    direction: Literal["increase", "decrease"] = Field(
        description="Desired direction of change",
    )
    value: Optional[float] = Field(default=None, description="Target absolute value")
    unit: str = Field(default="", description="Unit of measure, e.g. '%'")
    reduction_pct: Optional[float] = Field(
        default=None,
        description="Relative reduction/increase percentage",
    )
    baseline: Optional[float] = Field(default=None, description="Baseline value")


class GoalStatement(BaseModel):
    text: str = Field(description="Raw goal text, e.g. 'Reduce porosity rate'")
    id: Optional[str] = Field(default=None)
    domain: Optional[str] = Field(default=None)
    target_variable: Optional[str] = Field(default=None)
    desired_direction: Optional[Literal["increase", "decrease"]] = Field(
        default=None,
        description="'increase' or 'decrease'",
    )
    constraints: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    priority: Literal["high", "medium", "low"] = Field(default="medium")
    target: Optional[GoalTarget] = Field(default=None)
    source: Optional[str] = Field(default=None)
