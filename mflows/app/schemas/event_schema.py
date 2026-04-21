from pydantic import BaseModel
from typing import Dict, Any


class EventRequest(BaseModel):
    event_type: str
    payload: Dict[str, any]


class EventResponse(BaseModel):
    event_type: str
    matched_workflows: list[int]
    actions: list[str]
