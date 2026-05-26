from app.models.execution_step import ExecutionStep
from sqlalchemy.sql import func


# FIX: type hint was wrong — step_execution is an ExecutionStep object, not str
# OLD: def mark_failed(db, step_execution: str, attempts: int, error: str):
def mark_failed(db, step_execution, attempts: int, error: str):
    db.query(ExecutionStep).filter(ExecutionStep.id == step_execution.id).update(
        {
            "status": "FAILED",
            "attempts": attempts,
            "last_error": error,
            "updated_at": func.now(),
        }
    )

    db.commit()


def mark_dlq(db, step_execution, attempts: int):
    db.query(ExecutionStep).filter(ExecutionStep.id == step_execution.id).update(
        {
            "status": "DLQ",
            "attempts": attempts,
            "updated_at": func.now(),
        }
    )

    db.commit()


def mark_retry_scheduled(db, step_execution, attempts: int):
    db.query(ExecutionStep).filter(ExecutionStep.id == step_execution.id).update(
        {"status": "RETRY_SCHEDULED", "updated_at": func.now(), "attempts": attempts}
    )
    db.commit()
