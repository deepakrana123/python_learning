from app.execution.runtime.step_execution_service import (
    mark_step_running,
    mark_step_completed,
    mark_step_failed,
    create_step_execution,
)
from app.execution.dispatcher import execute_action
from app.execution.retry_handler import handle_retry
from app.repositories.step_retry_history_repo import record_retry_history
from app.core.tracing import generate_span_id, inject_trace_into_payload, build_log_context
from app.services import trace_service
from app.core.logger import logger


def execute_workflow_step(db, workflow_execution, step_definition, payload):

    step_execution = None

    try:
        action  = step_definition.get("action")
        config  = step_definition.get("config", {})
        step_id = step_definition.get("id", "unknown")

        # Generate span_id for this step
        # parent_span_id points to the workflow trace root
        span_id        = generate_span_id()
        parent_span_id = getattr(workflow_execution, "trace_id", None)

        step_execution = create_step_execution(
            db=db,
            workflow_execution_id=workflow_execution.id,
            step_name=action or step_id,
            step_id=step_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            input_payload=payload,
        )

        mark_step_running(db=db, step_execution=step_execution)

        # Emit STEP_STARTED trace event
        trace_service.record_step_started(
            db=db,
            workflow_execution=workflow_execution,
            step_execution=step_execution,
        )

        logger.info(
            "step_started",
            extra={
                "extra_data": build_log_context(
                    workflow_execution=workflow_execution,
                    execution_step=step_execution,
                    extra={"action": action},
                )
            },
        )

        # Inject trace context into payload before dispatching
        traced_payload = inject_trace_into_payload(
            payload=payload,
            workflow_execution=workflow_execution,
            execution_step=step_execution,
        )

        # Emit ACTION_DISPATCHED trace event
        trace_service.record_action_dispatched(
            db=db,
            workflow_execution=workflow_execution,
            step_execution=step_execution,
            action_name=action,
        )

        result  = execute_action(action_name=action, payload=traced_payload, config=config)
        success = result.get("success") is True or result.get("status") == "success"

        if success:
            mark_step_completed(
                db=db, step_execution=step_execution, output_payload=result
            )

            # Emit ACTION_SUCCESS + STEP_COMPLETED trace events
            trace_service.record_action_success(
                db=db,
                workflow_execution=workflow_execution,
                step_execution=step_execution,
                action_name=action,
                result=result,
            )
            trace_service.record_step_completed(
                db=db,
                workflow_execution=workflow_execution,
                step_execution=step_execution,
                result=result,
            )

            logger.info(
                "step_completed",
                extra={
                    "extra_data": build_log_context(
                        workflow_execution=workflow_execution,
                        execution_step=step_execution,
                        extra={"action": action},
                    )
                },
            )

            return {"success": True, "result": result}

        # Action returned non-success
        mark_step_failed(db=db, step_execution=step_execution, error=str(result))

        # Emit ACTION_FAILED + STEP_FAILED trace events
        trace_service.record_action_failed(
            db=db,
            workflow_execution=workflow_execution,
            step_execution=step_execution,
            action_name=action,
            error=str(result),
        )
        trace_service.record_step_failed(
            db=db,
            workflow_execution=workflow_execution,
            step_execution=step_execution,
            error=str(result),
        )

        logger.warning(
            "step_failed",
            extra={
                "extra_data": build_log_context(
                    workflow_execution=workflow_execution,
                    execution_step=step_execution,
                    extra={"action": action, "error": str(result)},
                )
            },
        )

        retry_result = handle_retry(
            db=db, step_execution=step_execution, error=str(result)
        )

        record_retry_history(
            db=db,
            step_execution=step_execution,
            attempt_number=retry_result.get("attempts", 1),
            trigger="retry" if retry_result.get("retry_scheduled") else "dlq",
            status_at_attempt=step_execution.status,
            error=str(result),
        )

        return {"success": False, "result": result}

    except Exception as e:
        logger.exception(
            "step_execution_failed",
            extra={
                "extra_data": build_log_context(
                    workflow_execution=workflow_execution,
                    execution_step=step_execution,
                    extra={"error": str(e)},
                )
            },
        )

        if step_execution:
            if step_execution.status not in ("FAILED", "RETRY_SCHEDULED", "DLQ", "COMPLETED"):
                mark_step_failed(db=db, step_execution=step_execution, error=str(e))

                trace_service.record_step_failed(
                    db=db,
                    workflow_execution=workflow_execution,
                    step_execution=step_execution,
                    error=str(e),
                )

                retry_result = handle_retry(
                    db=db, step_execution=step_execution, error=str(e)
                )
                record_retry_history(
                    db=db,
                    step_execution=step_execution,
                    attempt_number=retry_result.get("attempts", 1),
                    trigger="retry" if retry_result.get("retry_scheduled") else "dlq",
                    status_at_attempt=step_execution.status,
                    error=str(e),
                )

        return {"success": False, "error": str(e)}
