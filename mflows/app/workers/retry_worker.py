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

            # Fetch all events due for retry
            due_events = redis_client.zrangebyscore(RETRY_QUEUE, 0, now)

            if due_events:
                # Atomically remove from retry queue first, then push to main queue
                # This prevents double-processing if two workers run simultaneously
                pipeline = redis_client.pipeline()
                for raw_event in due_events:
                    pipeline.zrem(RETRY_QUEUE, raw_event)
                removed_counts = pipeline.execute()

                for raw_event, removed in zip(due_events, removed_counts):
                    if removed == 0:
                        # Another worker already claimed this event
                        continue

                    retry_data = json.loads(raw_event)
                    redis_client.lpush(MAIN_QUEUE, json.dumps(retry_data))

                    logger.info(
                        "event_requeued",
                        extra={"extra_data": {"event_id": retry_data.get("event_id")}},
                    )

            time.sleep(1)

        except Exception as e:
            logger.error(
                "retry_worker_error",
                extra={"extra_data": {"error": str(e)}},
            )
            time.sleep(1)


if __name__ == "__main__":
    start_retry_worker()
