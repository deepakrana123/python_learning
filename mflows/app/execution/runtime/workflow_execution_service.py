from sqlalchemy.sql import func
from app.models.workflow_execution import WorkflowExecution

from app.execution.runtime.constants import (
    WORKFLOW_STATUS_PENDING,
    WORKFLOW_STATUS_RUNNING,
    WORKFLOW_STATUS_COMPLETED,
    WORKFLOW_STATUS_FAILED,
    WORKFLOW_STATUS_PAUSED,
    WORKFLOW_STATUS_WAITING_APPROVAL,
    FINAL_WORKFLOW_STATES,
)
from app.execution.runtime.execution_state_manager import validate_workflow_transition
from app.core.logger import logger


def create_workflow_execution(
    db, workflow_id: int, event_id: str, event_type: str = None, entity_id: str = None
):
    execution = WorkflowExecution(
        workflow_id=workflow_id,
        event_id=event_id,
        event_type=event_type,
        entity_id=entity_id,
        status=WORKFLOW_STATUS_PENDING,
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)
    return execution


def update_workflow_status(db, workflow_execution, new_status: str, error: str = None):

    # Guard: already in a terminal state — skip silently, do not raise
    db.refresh(workflow_execution)

    current_status = workflow_execution.status

    if current_status == new_status:
        return workflow_execution

    if current_status == new_status:
        logger.info(
            "workflow_transition_skipped_same_state",
            extra={
                "extra_data": {
                    "workflow_execution_id": workflow_execution.id,
                    "status": current_status,
                }
            },
        )
        return workflow_execution

    if current_status in FINAL_WORKFLOW_STATES and current_status != new_status:
        return workflow_execution

    valid = validate_workflow_transition(
        current_status=current_status,
        new_status=new_status,
    )
    if not valid:
        raise ValueError(
            f"Invalid workflow transition: {current_status} -> {new_status}"
        )

    workflow_execution.status = new_status
    workflow_execution.updated_at = func.now()

    if new_status == WORKFLOW_STATUS_RUNNING:
        workflow_execution.started_at = func.now()

    if new_status in FINAL_WORKFLOW_STATES:
        workflow_execution.completed_at = func.now()

    if error:
        workflow_execution.last_error = error

    db.commit()
    db.refresh(workflow_execution)
    return workflow_execution


def mark_workflow_running(db, workflow_execution):
    return update_workflow_status(
        db=db,
        workflow_execution=workflow_execution,
        new_status=WORKFLOW_STATUS_RUNNING,
    )


def mark_workflow_completed(db, workflow_execution):
    return update_workflow_status(
        db=db,
        workflow_execution=workflow_execution,
        new_status=WORKFLOW_STATUS_COMPLETED,
    )


def mark_workflow_failed(db, workflow_execution, error: str):
    return update_workflow_status(
        db=db,
        workflow_execution=workflow_execution,
        new_status=WORKFLOW_STATUS_FAILED,
        error=error,
    )


def mark_workflow_paused(db, workflow_execution):
    return update_workflow_status(
        db=db,
        workflow_execution=workflow_execution,
        new_status=WORKFLOW_STATUS_PAUSED,
    )


def mark_workflow_waiting_approval(db, workflow_execution):
    return update_workflow_status(
        db=db,
        workflow_execution=workflow_execution,
        new_status=WORKFLOW_STATUS_WAITING_APPROVAL,
    )
