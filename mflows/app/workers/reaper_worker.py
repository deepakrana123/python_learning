import time
from datetime import datetime, timedelta, timezone
from app.db.session import SessionLocal
from app.models.event_processing import EventProcessing
from app.core.redis_client import redis_client
from app.core.config import PROCESSING_TIMEOUT_SECONDS
from app.core.logger import logger
import json

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
                event.attempts += 1
                event.last_error = "Recovered from stuck PROCESSING state"
                retry_payload = {
                    "event": {"event_id": event.event_id},
                    "attempt": event.attempts,
                }
                redis_client.zadd(RETRY_QUEUE, json.dumps(retry_payload))
            time.sleep(5)
            db.commit()

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
