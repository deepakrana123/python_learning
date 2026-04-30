import json
import time
from app.core.redis_client import redis_client
from app.db.session import SessionLocal
from app.services.execution_service import process_event_service


def start_worker():
    while True:
        item = redis_client.brpop("workflow_events", timeout=5)

        if not item:
            continue

        _, raw = item
        try:
            event = json.loads(raw)
            db = SessionLocal()
            process_event_service(event, db)
            db.close()
        except Exception as e:
            print("worker error:", e)


if __name__ == "__main__":
    start_worker()
