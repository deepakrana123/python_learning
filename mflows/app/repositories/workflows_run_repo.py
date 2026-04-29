from app.models.workflow_run import WorkflowRun
from sqlalchemy.sql import func


def create(db, workflow_id, event_type, entity_id):
    row = WorkflowRun(
        workflow_id=workflow_id,
        event_type=event_type,
        entity_id=entity_id,
        status="running",
    )
    db.add(row)
    db.flush()
    return row


def mark_success(db, row):
    row.status = "success"
    row.finished_at = func.now()


def mark_failed(db, row, error):
    row.status = "failed"
    row.error_text = str(error)
    row.finished_at = func.now()
