from app.execution.retry_policy import should_retry

from app.execution.retry import (
    handle_retry_event,
    handle_dlq_event,
)

from app.execution.state_manager import (
    mark_failed,
    mark_retry_scheduled,
    mark_dlq,
)


def handle_retry(
    db,
    workflow_execution,
    step_execution,
    error,
):

    attempts = (workflow_execution.attempts or 0) + 1
    mark_failed(
        db=db,
        workflow_execution=workflow_execution,
        step_execution=step_execution,
        attempts=attempts,
        error=str(error),
    )

    # retry path
    if should_retry(attempts):

        handle_retry_event(
            workflow_execution=workflow_execution,
            step_execution=step_execution,
            attempts=attempts,
            error=str(error),
        )

        mark_retry_scheduled(
            db=db,
            workflow_execution=workflow_execution,
            step_execution=step_execution,
        )

        return

    # DLQ path
    handle_dlq_event(
        workflow_execution=workflow_execution,
        step_execution=step_execution,
        attempts=attempts,
        error=str(error),
    )

    mark_dlq(
        db=db,
        workflow_execution=workflow_execution,
        step_execution=step_execution,
    )
