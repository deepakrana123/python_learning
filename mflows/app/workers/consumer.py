import json
from app.core.redis_client import redis_client
from app.db.session import SessionLocal
from app.services.execution_service import process_event_service
from app.core.logger import logger
from concurrent.futures import ThreadPoolExecutor

QUEUE = "workflow_events"
MAX_WORKERS = 5


def handle_event(event):
    db = SessionLocal()
    try:
        process_event_service(event, db)
    except Exception as e:
        logger.error(
            "consumer_worker_error",
            extra={"extra_data": {"error": str(e), "event": event}},
        )
    finally:
        db.close()


def worker():
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    while True:
        item = redis_client.brpop(QUEUE, timeout=5)
        if not item:
            continue
        _, event_data = item
        event = json.loads(event_data)
        executor.submit(handle_event, event)


if __name__ == "__main__":
    print("Worker started...", flush=True)
    worker()
