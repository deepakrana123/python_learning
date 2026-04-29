import json
from fastapi import APIRouter
from app.schemas.event import EventCreate
from app.core.redis_client import redis_client
import uuid

router = APIRouter(prefix="/event", tags=["events"])


@router.post("/publish")
def publish_event(body: EventCreate):
    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": body.event_type,
        "entity_type": body.entity_type,
        "entity_id": body.entity_id,
    }
    redis_client.lpush("workflow_events", json.dumps(event))
    return {"success": True, "queued": True}
