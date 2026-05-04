import json
import time
from app.core.redis_client import redis_client
from app.core.logger import logger

RETRY_QUEUE = "workflow_retry"
MAIN_QUEUE = "workflow_events"


def start_retry_worker():
    while True:
        try:
            now = int(time.time())
            events = redis_client.zrangebyscore(RETRY_QUEUE, 0, now)
            for event in events:
                retry_data = json.loads(event)
                redis_client.lpush(MAIN_QUEUE, json.dumps(retry_data))

                redis_client.zrem(RETRY_QUEUE, event)
                logger.info(
                    "event_requeued", extra={"extra": {"event_id": event["event_id"]}}
                )
            time.sleep(1)
        except Exception as e:
            logger.error(
                "retry_worker_error",
                extra={"extra_data": {"error": str(e)}},
            )


if __name__ == "__main__":
    start_retry_worker()
