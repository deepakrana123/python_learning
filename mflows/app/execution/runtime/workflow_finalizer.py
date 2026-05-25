from app.models.execution_step import ExecutionStep
from app.execution.runtime.workflow_execution_service import (
    mark_workflow_completed,
    mark_workflow_failed,
)

from app.core.logger import logger


def finalize_workflow_execution(db, workflow_execution):
    steps = (
        db.query(ExecutionStep)
        .filter(ExecutionStep.workflow_execution_id == workflow_execution.id)
        .all()
    )

    statuses = [step.status for step in steps]

    if all(status == "COMPLETED" for status in statuses):
        mark_workflow_completed(db=db, workflow_execution=workflow_execution)
        return

    if any(status == "FAILED" for status in statuses):
        mark_workflow_failed(
            db=db,
            workflow_execution=workflow_execution,
            error="one_or_more_steps_failed",
        )

        return

    if any(status == "WAITING" for status in statuses):
        workflow_execution.status = "WAITING_APPROVAL"
        db.commit()

        return

    logger.info(
        "workflow_execution_still_active",
        extra={
            "extra_data": {
                "workflow_execution_id": workflow_execution.id,
            }
        },
    )
