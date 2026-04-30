import time
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.event_processing import EventProcessing
from app.core.redis_client import redis_client
from app.core.config import PROCESSING_TIMEOUT_SECONDS
from app.core.logger import logger
import json

MAIN_QUEUE = "workflow_events"


def reaper_worker():
    while True:
        db: Session = SessionLocal()

        try:
            timeout_threshold = datetime.utcnow() - timedelta(
                seconds=PROCESSING_TIMEOUT_SECONDS
            )

            stuck_events = (
                db.query(EventProcessing)
                .filter(
                    EventProcessing.status == "PROCESSING",
                    EventProcessing.updated_at < timeout_threshold,
                )
                .limit(100)
                .all()
            )
            for event in stuck_events:
                logger.warning(
                    "reaper_recovering_stuck_event",
                    extra={"extra_data": {"event_id": event.event_id}},
                )
                event.status = "FAILED"
                event.attempts += 1
                event.last_error = "Recovered from stuck PROCESSING state"
                db.commit()
                redis_client.lpush(MAIN_QUEUE, json.dumps({"event_id": event.event_id}))

        except Exception as e:
            logger.error(
                "reaper_worker_error",
                extra={"extra_data": {"error": str(e)}},
            )
            db.rollback()

        finally:
            db.close()
