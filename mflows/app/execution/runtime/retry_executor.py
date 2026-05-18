from app.execution.dispatcher import execute_action

from app.execution.runtime.step_execution_service import (
    mark_step_running,
    mark_step_completed,
    mark_step_failed,
)

from app.execution.runtime.workflow_execution_service import (
    mark_workflow_completed,
    mark_workflow_failed,
)

from app.execution.retry_handler import handle_retry

from app.core.logger import logger


def execute_retry(
    db,
    workflow_execution,
    step_execution,
):

    try:

        logger.info(
            "retry_execution_started",
            extra={
                "extra_data": {
                    "workflow_execution_id": workflow_execution.id,
                    "step_execution_id": step_execution.id,
                    "step_name": step_execution.step_name,
                }
            },
        )
        db.refresh(workflow_execution)

        if workflow_execution.status != "RETRY_SCHEDULED":
            return

        # move step back to RUNNING
        mark_step_running(
            db=db,
            step_execution=step_execution,
        )

        # current architecture:
        # workflow = single executable action
        rule = workflow_execution.workflow.parsed_rule_json

        action = rule.get("action")

        config = rule.get("config", {})

        result = execute_action(
            action_name=action,
            payload=step_execution.input_payload,
            config=config,
        )

        success = result.get("success") is True or result.get("status") == "success"

        if success:

            mark_step_completed(
                db=db,
                step_execution=step_execution,
                output_payload=result,
            )

            mark_workflow_completed(
                db=db,
                workflow_execution=workflow_execution,
            )

            logger.info(
                "retry_execution_completed",
                extra={
                    "extra_data": {
                        "workflow_execution_id": workflow_execution.id,
                        "step_execution_id": step_execution.id,
                    }
                },
            )

            return

        # retry failed again
        mark_step_failed(
            db=db,
            step_execution=step_execution,
            error=str(result),
        )

        mark_workflow_failed(
            db=db,
            workflow_execution=workflow_execution,
            error=str(result),
        )

        handle_retry(
            db=db,
            workflow_execution=workflow_execution,
            step_execution=step_execution,
            error=str(result),
        )

    except Exception as e:

        logger.exception(
            "retry_execution_failed",
            extra={
                "extra_data": {
                    "workflow_execution_id": workflow_execution.id,
                    "step_execution_id": step_execution.id,
                    "error": str(e),
                }
            },
        )

        try:

            if step_execution.status != "FAILED":

                mark_step_failed(
                    db=db,
                    step_execution=step_execution,
                    error=str(e),
                )

            if workflow_execution.status != "FAILED":

                mark_workflow_failed(
                    db=db,
                    workflow_execution=workflow_execution,
                    error=str(e),
                )

        except Exception as state_error:

            logger.error(
                "retry_execution_state_update_failed",
                extra={
                    "extra_data": {
                        "workflow_execution_id": workflow_execution.id,
                        "step_execution_id": step_execution.id,
                        "error": str(state_error),
                    }
                },
            )

        handle_retry(
            db=db,
            workflow_execution=workflow_execution,
            step_execution=step_execution,
            error=str(e),
        )
