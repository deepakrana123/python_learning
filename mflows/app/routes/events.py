import json
from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError
import uuid
from app.schemas.event import EventCreate
from app.core.redis_client import redis_client
from app.db.session import SessionLocal
from app.models.event_processing import EventProcessing

router = APIRouter(prefix="/event", tags=["events"])


@router.post("/publish")
def publish_event(body: EventCreate):
    event_id = str(uuid.uuid4())
    event = {
        "event_id": event_id,
        "event_type": body.event_type,
        "entity_type": body.entity_type,
        "entity_id": body.entity_id,
    }
    try:
        db = SessionLocal()
        record = EventProcessing(event_id=event["event_id"], status="RECEIVED")
        db.add(record)
        db.commit()
        redis_client.lpush("workflow_events", json.dumps(event))
    except IntegrityError:
        db.rollback()
        return {"status": "duplicate_ignored"}
    except Exception as e:
        db.rollback()
        db.query(EventProcessing).filter(EventProcessing.event_id == event_id).delete()
        raise e
    finally:
        db.close()
    return {"success": True, "queued": True}
