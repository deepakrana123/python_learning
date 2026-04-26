from typing import List, Dict, Any
from pydantic import BaseModel


class TriggerRequest(BaseModel):
    event_type: str
    payload: Dict[str, Any]


class TriggerResponse(BaseModel):
    success: bool
    event_type: str
    matched_count: int
    matched_workflows: List[int]
    actions: List[str]
    execution_results: List[Dict[str, Any]]
