from app.execution.retry_policy import should_retry

from app.execution.retry import (
    handle_retry_event,
    handle_dlq_event,
)

from app.execution.state_manager import (
    mark_retry_scheduled,
    mark_dlq,
)


def handle_retry(
    db,
    step_execution,
    error,
):

    attempts = (step_execution.attempts or 0) + 1

    if should_retry(attempts):

        handle_retry_event(
            step_execution=step_execution,
            attempts=attempts,
            error=str(error),
        )

        mark_retry_scheduled(
            db=db,
            step_execution=step_execution,
            attempts=attempts,
        )

        return {
            "retry_scheduled": True,
            "attempts": attempts,
        }

    # DLQ path
    handle_dlq_event(
        step_execution=step_execution,
        attempts=attempts,
        error=str(error),
    )

    mark_dlq(
        db=db,
        step_execution=step_execution,
        attempts=attempts,
    )

    return {
        "retry_scheduled": False,
        "moved_to_dlq": True,
        "attempts": attempts,
    }
