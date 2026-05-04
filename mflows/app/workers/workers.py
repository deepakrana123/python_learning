import json
import time
from app.core.redis_client import redis_client
from app.db.session import SessionLocal
from app.services.execution_service import process_event_service
from app.core.logger import logger


def start_worker():
    print("Polling queue...", flush=True)
    item = redis_client.brpop("workflow_events", timeout=5)
    while True:
        print(item, "item")
        if not item:
            continue
        _, raw = item
        try:
            event = json.loads(raw)
            db = SessionLocal()
            process_event_service(event, db)
            db.close()
        except Exception as e:
            logger.error(
                "worker_event_processing_error",
                extra={"extra_data": {"error": str(e)}},
            )


if __name__ == "__main__":
    start_worker()
