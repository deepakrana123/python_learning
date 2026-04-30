import json
import time
from app.core.redis_client import redis_client
from app.db.session import SessionLocal
from app.services.execution_service import process_event_service

RETRY_QUEUE = "workflow_retry"
MAIN_QUEUE = "workflow_events"


def start_worker():
    while True:
        now = int(time.time())
        events = redis_client.zrangebyscore(RETRY_QUEUE, 0, now)
        for event in events:
            redis_client.lpush(MAIN_QUEUE, event)

            redis_client.zrem(RETRY_QUEUE, event)
        time.sleep(1)


if __name__ == "__main__":
    start_worker()
