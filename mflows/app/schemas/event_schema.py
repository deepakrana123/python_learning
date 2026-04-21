from typing import List, Dict, Any
from pydantic import BaseModel


class EventRequest(BaseModel):
    event_type: str
    payload: Dict[str, Any]


class EventResponse(BaseModel):
    success: bool
    event_type: str
    matched_count: int
    matched_workflows: List[int]
    actions: List[str]
