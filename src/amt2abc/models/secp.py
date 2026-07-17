from typing import List

from pydantic import BaseModel, Field


class StructureDimension(BaseModel):
    entities: List[str] = Field(default_factory=list)
    relationships: List[str] = Field(default_factory=list)


class EventDimension(BaseModel):
    triggers: List[str] = Field(default_factory=list)
    conditions: List[str] = Field(default_factory=list)


class ConfigurationDimension(BaseModel):
    parameters: dict = Field(default_factory=dict)
    constraints: List[str] = Field(default_factory=list)


class ProcessDimension(BaseModel):
    steps: List[str] = Field(default_factory=list)
    control_loops: List[str] = Field(default_factory=list)


class SECP(BaseModel):
    id: str
    domain: str
    structure: StructureDimension = Field(default_factory=StructureDimension)
    event: EventDimension = Field(default_factory=EventDimension)
    configuration: ConfigurationDimension = Field(
        default_factory=ConfigurationDimension,
    )
    process: ProcessDimension = Field(default_factory=ProcessDimension)
