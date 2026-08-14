from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from amt2abc.models.secp import CauseRef, EffectRef, SECPFrame


class Triplet(BaseModel):
    cause: str = Field(description="Cause variable, e.g. 'mold_temperature'")
    effect: str = Field(description="Effect variable, e.g. 'porosity_rate'")
    relation: Literal["increases", "decreases"] = Field(
        description="Causal relation direction",
    )
    mechanism: str = Field(description="Physical mechanism description")
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    formula: str = Field(default="", description="Mathematical formula")
    input_vars: List[str] = Field(default_factory=list)
    output_vars: List[str] = Field(default_factory=list)


class AMT(BaseModel):
    id: str = Field(description="Unique identifier, e.g. 'AMT_DC_THERMO_002'")
    name: str = Field(description="Human-readable name")
    domain: str = Field(description="Industrial domain, e.g. 'die_casting'")
    triplets: List[Triplet] = Field(description="Ordered list of causal triplets")
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    name_en: str = Field(default="")
    layer: str = Field(default="", description="Three-law layer: tian/fa/ren")
    evidence_source: str = Field(
        default="",
        description="physics_law | empirical_formula | expert_knowledge",
    )
    mcl_engine: str = Field(
        default="",
        description="numerical_calculation | rule_engine | machine_learning",
    )
    reference: str = Field(default="", description="ISO/reference standard")
    formula_dsl: str = Field(default="")
    secp: Optional[SECPFrame] = Field(default=None)
    cause: Optional[CauseRef] = Field(default=None)
    effect: Optional[EffectRef] = Field(default=None)
