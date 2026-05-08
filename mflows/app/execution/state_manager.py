from app.models.event_processing import EventProcessing
from sqlalchemy.sql import func


def mark_failed(db, event_id: str, attempts: int, error: str):
    db.query(EventProcessing).filter(EventProcessing.event_id == event_id).update(
        {
            "status": "FAILED",
            "attempts": attempts,
            "last_error": error,
            "updated_at": func.now(),
        }
    )

    db.commit()


def mark_dlq(db, event_id: str):
    db.query(EventProcessing).filter(EventProcessing.event_id == event_id).update(
        {
            "status": "DLQ",
            "updated_at": func.now(),
        }
    )

    db.commit()


def mark_retry_scheduled(db, event_id: str):
    db.query(EventProcessing).filter(EventProcessing.event_id == event_id).update(
        {
            "status": "RETRY_SCHEDULED",
            "updated_at": func.now(),
        }
    )

    db.commit()
