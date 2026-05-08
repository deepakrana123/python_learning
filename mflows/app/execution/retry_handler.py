from app.models.event_processing import EventProcessing
from app.execution.retry_policy import should_retry
from app.execution.retry import handle_retry_event, handle_dlq_event
from app.execution.state_manager import (
    mark_failed,
    mark_retry_scheduled,
    mark_dlq,
)


def handle_retry(db, event: dict, error):
    event_id = event["event_id"]
    row = db.query(EventProcessing).filter(EventProcessing.event_id == event_id).first()
    attempts = (row.attempts or 0) + 1
    mark_failed(
        db=db,
        event_id=event_id,
        attempts=attempts,
        error=str(error),
    )

    if should_retry(attempts):
        handle_retry_event(event=event, attempts=attempts)
        mark_retry_scheduled(db=db, event_id=event_id)
    else:
        handle_dlq_event(
            event=event,
            attempts=attempts,
            error=str(error),
        )

        mark_dlq(
            db=db,
            event_id=event_id,
        )
