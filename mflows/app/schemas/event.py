from pydantic import BaseModel
from typing import Dict, Any


class EventCreate(BaseModel):
    event_type: str
    pentity_type: str
    entity_id: str
