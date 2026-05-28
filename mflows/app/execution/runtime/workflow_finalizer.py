from app.models.execution_step import ExecutionStep
from app.execution.runtime.workflow_execution_service import (
    mark_workflow_completed,
    mark_workflow_failed,
    mark_workflow_waiting_approval,
)
from app.core.logger import logger


def finalize_workflow_execution(db, workflow_execution):
    steps = (
        db.query(ExecutionStep)
        .filter(ExecutionStep.workflow_execution_id == workflow_execution.id)
        .all()
    )

    statuses = [step.status for step in steps]

    # FIX: DLQ is permanent failure — must mark workflow FAILED
    # OLD: DLQ was not checked — workflow could complete even with DLQ steps
    if any(status == "DLQ" for status in statuses):
        mark_workflow_failed(
            db=db,
            workflow_execution=workflow_execution,
            error="one_or_more_steps_moved_to_dlq",
        )
        return

    # FIX: RETRY_SCHEDULED means execution is still in progress — do not finalize yet
    # OLD: not checked — workflow could be finalized while a step was pending retry
    if any(status == "RETRY_SCHEDULED" for status in statuses):
        logger.info(
            "workflow_finalization_deferred_retry_pending",
            extra={
                "extra_data": {
                    "workflow_execution_id": workflow_execution.id,
                }
            },
        )
        return

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
        # FIX M6: was directly assigning workflow_execution.status — bypassed state machine
        # OLD: workflow_execution.status = "WAITING_APPROVAL" + db.commit()
        mark_workflow_waiting_approval(db=db, workflow_execution=workflow_execution)
        return

    logger.info(
        "workflow_execution_still_active",
        extra={
            "extra_data": {
                "workflow_execution_id": workflow_execution.id,
            }
        },
    )
