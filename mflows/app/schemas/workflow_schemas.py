from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WorkflowCreate(BaseModel):
    name: str
    domain: str
    raw_input: str


class DebugParseRequest(BaseModel):
    raw_input: str


class WorkflowResponse(BaseModel):
    id: int
    name: str
    domain: str
    raw_input: str
    parsed_rule_json: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True  # for pydantic v1 if v2 from pydantic import ConfigDict


# model_config = ConfigDict(from_attributes=True)
