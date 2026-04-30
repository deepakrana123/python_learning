import json
from app.core.redis_client import redis_client
from app.db.session import SessionLocal
from app.services.execution_service import process_event_service

QUEUE = "workflow_events"


def worker():
    while True:
        item = redis_client.brpop(QUEUE, timeout=5)
        if not item:
            continue
        _, event_data = item
        event = json.loads(event_data)
        db = SessionLocal()
        try:
            process_event_service()
        except Exception as e:
            print(f"[WORKER ERROR] {str(e)}")
        finally:
            db.close()
