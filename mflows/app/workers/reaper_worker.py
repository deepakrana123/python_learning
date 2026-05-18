import time
import json
from datetime import datetime, timedelta, timezone
from app.db.session import SessionLocal
from app.models.workflow_execution import WorkflowExecution
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
                db.query(WorkflowExecution)
                .filter(
                    WorkflowExecution.status == "PROCESSING",
                    WorkflowExecution.updated_at < timeout_threshold,
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

            db.commit()

            for event in stuck_events:
                retry_payload = {
                    "event_id": event.event_id,
                    "attempt": event.attempts,
                    "source": "reaper",
                }
                retry_at = int(time.time())  # retry immediately
                redis_client.zadd(RETRY_QUEUE, {json.dumps(retry_payload): retry_at})

                logger.info(
                    "reaper_event_requeued",
                    extra={
                        "extra_data": {
                            "event_id": event.event_id,
                            "attempts": event.attempts,
                        }
                    },
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
