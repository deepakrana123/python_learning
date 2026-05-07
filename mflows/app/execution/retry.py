import time
import json
from sqlalchemy.sql import func
from app.models.event_processing import EventProcessing
from app.core.config import MAX_RETRIES, BASE_DELAY_SECONDS
from app.core.redis_client import redis_client
from app.core.logger import logger


def handle_retry(db, event: dict, error: Exception):
    event_id = event["event_id"]

    row = (
        db.query(EventProcessing)
        .filter(EventProcessing.event_id == event_id)
        .first()
    )
    attempts = (row.attempts or 0) + 1

    db.query(EventProcessing).filter(EventProcessing.event_id == event_id).update(
        {
            "status": "FAILED",
            "attempts": attempts,
            "last_error": str(error),
            "updated_at": func.now(),
        }
    )
    db.commit()

    if attempts <= MAX_RETRIES:
        delay = BASE_DELAY_SECONDS * (2 ** (attempts - 1))
        retry_at = int(time.time()) + delay
        retry_payload = {
            **event,
            "attempt": attempts,
        }

        redis_client.zadd(
            "workflow_retry",
            {json.dumps(retry_payload): retry_at},
        )

        logger.warning(
            "event_retry_scheduled",
            extra={
                "extra_data": {
                    "event_id": event_id,
                    "attempt": attempts,
                    "retry_in_seconds": delay,
                    "error": str(error),
                }
            },
        )

    else:
        dlq_payload = {
            "event": event,
            "attempts": attempts,
            "error": str(error),
            "failed_at": int(time.time()),
        }

        redis_client.lpush("workflow_dlq", json.dumps(dlq_payload))

        logger.error(
            "event_pushed_to_dlq",
            extra={
                "extra_data": {
                    "event_id": event_id,
                    "attempts": attempts,
                    "error": str(error),
                }
            },
        )
