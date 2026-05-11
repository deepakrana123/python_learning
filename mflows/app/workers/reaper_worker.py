import time
import json
from datetime import datetime, timedelta, timezone
from app.db.session import SessionLocal
from app.models.event_processing import EventProcessing
from app.core.redis_client import redis_client
from app.core.config import PROCESSING_TIMEOUT_SECONDS
from app.core.logger import logger

BATCH_SIZE = 50
RETRY_QUEUE = "workflow_retry"


def start_reaper():
    while True:
        db = SessionLocal()
        try:
            timeout_threshold = datetime.now(timezone.utc) - timedelta(
                seconds=PROCESSING_TIMEOUT_SECONDS
            )

            stuck_events = (
                db.query(EventProcessing)
                .filter(
                    EventProcessing.status == "PROCESSING",
                    EventProcessing.updated_at < timeout_threshold,
                )
                .limit(BATCH_SIZE)
                .all()
            )

            for event in stuck_events:
                logger.warning(
                    "reaper_recovering_event",
                    extra={"extra_data": {"event_id": event.event_id}},
                )
                event.status = "FAILED"
                event.attempts = (event.attempts or 0) + 1
                event.last_error = "Recovered from stuck PROCESSING state"

            # Commit DB changes BEFORE writing to Redis
            # If we crash after commit but before Redis write, the reaper
            # will pick it up again on next cycle (safe — idempotent)
            db.commit()

            # Now push to Redis retry queue
            for event in stuck_events:
                retry_payload = {
                    "event_id": event.event_id,
                    # NOTE: full event payload (entity_type, entity_id, event_type)
                    # requires raw_payload column on EventProcessing.
                    # Until that column exists, the consumer must re-fetch from DB.
                    "attempt": event.attempts,
                    "source": "reaper",
                }
                retry_at = int(time.time())  # retry immediately
                redis_client.zadd(RETRY_QUEUE, {json.dumps(retry_payload): retry_at})

                logger.info(
                    "reaper_event_requeued",
                    extra={"extra_data": {"event_id": event.event_id, "attempts": event.attempts}},
                )

        except Exception as e:
            logger.error(
                "reaper_worker_error",
                extra={"extra_data": {"error": str(e)}},
            )
            db.rollback()

        finally:
            db.close()

        time.sleep(5)


if __name__ == "__main__":
    print("Reaper worker started...", flush=True)
    start_reaper()
