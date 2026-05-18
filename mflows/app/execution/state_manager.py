from app.models.workflow_execution import WorkflowExecution
from sqlalchemy.sql import func


def mark_failed(db, workflow_execution: str, attempts: int, error: str):
    db.query(WorkflowExecution).filter(
        WorkflowExecution.id == workflow_execution.id
    ).update(
        {
            "status": "FAILED",
            "attempts": attempts,
            "last_error": error,
            "updated_at": func.now(),
        }
    )

    db.commit()


def mark_dlq(db, workflow_execution):
    db.query(WorkflowExecution).filter(
        WorkflowExecution.id == workflow_execution.id
    ).update(
        {
            "status": "DLQ",
            "updated_at": func.now(),
        }
    )

    db.commit()


def mark_retry_scheduled(db, workflow_execution):
    db.query(WorkflowExecution).filter(
        WorkflowExecution.id == workflow_execution.id
    ).update(
        {
            "status": "RETRY_SCHEDULED",
            "updated_at": func.now(),
        }
    )

    db.commit()
