from app.execution.runtime.step_execution_service import (
    mark_step_running,
    mark_step_completed,
    mark_step_failed,
    create_step_execution,
)

from app.execution.dispatcher import execute_action
from app.execution.retry_handler import handle_retry
from app.repositories.step_retry_history_repo import record_retry_history
from app.core.logger import logger


def execute_workflow_step(db, workflow_execution, step_definition, payload):

    step_execution = None

    try:
        # FIX C4: DAG steps from dsl_parser have shape {"id", "trigger", "action", "depends_on"}
        # OLD: step_definition["rule"] — "rule" key doesn't exist, caused KeyError on every step
        print(step_definition, "step_definition")
        action = step_definition.get("action")
        config = step_definition.get("config", {})
        step_id = step_definition.get("id", "unknown")
        print(step_id, "step_id")
        step_execution = create_step_execution(
            db=db,
            workflow_execution_id=workflow_execution.id,
            step_name=action or step_id,
            step_id=step_id,
            input_payload=payload,
        )

        mark_step_running(db=db, step_execution=step_execution)

        result = execute_action(action_name=action, payload=payload, config=config)

        success = result.get("success") is True or result.get("status") == "success"
        print(success, "succes", result)
        if success:
            mark_step_completed(
                db=db, step_execution=step_execution, output_payload=result
            )

            return {"success": True, "result": result}

        mark_step_failed(db=db, step_execution=step_execution, error=str(result))

        retry_result = handle_retry(
            db=db, step_execution=step_execution, error=str(result)
        )

        # Write retry history
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
                "extra_data": {
                    "workflow_execution_id": workflow_execution.id,
                    "error": str(e),
                }
            },
        )

        if step_execution:
            if step_execution.status not in (
                "FAILED",
                "RETRY_SCHEDULED",
                "DLQ",
                "COMPLETED",
            ):
                mark_step_failed(db=db, step_execution=step_execution, error=str(e))
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
