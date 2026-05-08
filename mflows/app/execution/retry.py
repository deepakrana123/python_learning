import time
import json
from app.execution.constants import REDIS_RETRY_QUEUE, REDIS_DLQ
from app.core.redis_client import redis_client
from app.core.logger import logger
from app.execution.retry_policy import calculate_delay


def handle_retry_event(event, attempts, error):
    delay = calculate_delay(attempts)
    retry_at = int(time.time()) + delay
    retry_payload = {
        **event,
        "attempt": attempts,
    }
    redis_client.zadd(
        REDIS_RETRY_QUEUE,
        {json.dumps(retry_payload): retry_at},
    )

    logger.warning(
        "event_retry_scheduled",
        extra={
            "extra_data": {
                "event_id": event["event_id"],
                "attempt": attempts,
                "retry_in_seconds": delay,
                "error": str(error),
            }
        },
    )


def handle_dlq_event(event, attempts, error):
    dlq_payload = {
        "event": event,
        "attempts": attempts,
        "error": str(error),
        "failed_at": int(time.time()),
    }

    redis_client.lpush(REDIS_DLQ, json.dumps(dlq_payload))

    logger.error(
        "event_pushed_to_dlq",
        extra={
            "extra_data": {
                "event_id": event["event_id"],
                "attempts": attempts,
                "error": str(error),
            }
        },
    )
