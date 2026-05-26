from app.execution.runtime.step_execution_service import (
    mark_step_running,
    mark_step_completed,
    mark_step_failed,
    create_step_execution,
)

from app.execution.dispatcher import execute_action
from app.execution.retry_handler import handle_retry
from app.core.logger import logger


def execute_workflow_step(db, workflow_execution, step_definition, payload):

    step_execution = None

    try:
        rule = step_definition["rule"]
        action = rule.get("action")
        config = rule.get("config", {})
        step_execution = create_step_execution(
            db=db,
            workflow_execution_id=workflow_execution.id,
            step_name=action,
            input_payload=payload,
        )

        mark_step_running(db=db, step_execution=step_execution)

        result = execute_action(action_name=action, payload=payload, config=config)

        success = result.get("success") is True or result.get("status") == "success"

        if success:
            mark_step_completed(
                db=db, step_execution=step_execution, output_payload=result
            )

            return {"success": True, "result": result}

        mark_step_failed(db=db, step_execution=step_execution, error=str(result))

        handle_retry(db=db, step_execution=step_execution, error=str(result))

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
            # FIX: only call mark_step_failed if not already in a terminal state
            # prevents double mark_step_failed + double handle_retry if handle_retry threw
            # OLD: called unconditionally — caused double retry queue entry
            if step_execution.status not in ("FAILED", "RETRY_SCHEDULED", "DLQ", "COMPLETED"):
                mark_step_failed(db=db, step_execution=step_execution, error=str(e))
                handle_retry(db=db, step_execution=step_execution, error=str(e))
        return {"success": False, "error": str(e)}
