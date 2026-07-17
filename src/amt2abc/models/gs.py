from typing import List, Optional

from pydantic import BaseModel, Field


class GoalStatement(BaseModel):
    text: str = Field(description="Raw goal text, e.g. 'Reduce porosity rate'")
    domain: Optional[str] = Field(default=None)
    target_variable: Optional[str] = Field(default=None)
    desired_direction: Optional[str] = Field(
        default=None,
        description="'increase' or 'decrease'",
    )
    constraints: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
