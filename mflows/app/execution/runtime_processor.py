from app.execution.workflow_loader import load_active_workflows
from app.execution.matcher import get_matching_workflows
from app.repositories.entity_repo import fetch_entity_payload

from app.execution.runtime.workflow_execution_service import (
    create_workflow_execution,
    mark_workflow_running,
    mark_workflow_completed,
    mark_workflow_failed,
)

from app.execution.runtime.step_execution_service import (
    create_execution_step,
    mark_step_running,
    mark_step_completed,
    mark_step_failed,
)

from app.execution.dispatcher import execute_action
from app.execution.retry_handler import handle_retry
from app.execution.dedupe import is_duplicate_execution

from app.core.logger import logger


def runtime_processor(db, event: dict):

    workflows = load_active_workflows(db)

    payload = fetch_entity_payload(
        db,
        event["entity_type"],
        event["entity_id"],
    )

    matched_workflows = get_matching_workflows(
        workflows=workflows,
        event=event,
        payload=payload,
    )

    logger.info(
        "runtime_processor_started",
        extra={
            "extra_data": {
                "event_id": event["event_id"],
                "matched_count": len(matched_workflows),
            }
        },
    )

    workflow_failed = False

    for workflow in matched_workflows:

        workflow_execution = None
        step = None

        try:

            if is_duplicate_execution(event, workflow):
                logger.info(
                    "duplicate_workflow_execution_skipped",
                    extra={
                        "extra_data": {
                            "event_id": event["event_id"],
                            "workflow_id": workflow.id,
                        }
                    },
                )
                continue

            workflow_execution = create_workflow_execution(
                db=db,
                workflow=workflow,
                event=event,
            )

            mark_workflow_running(
                db=db,
                workflow_execution=workflow_execution,
            )

            rule = workflow.parsed_rule_json

            action = rule.get("action")

            config = rule.get("config", {})

            step = create_execution_step(
                db=db,
                workflow_execution=workflow_execution,
                step_name=action,
                input_payload=payload,
            )

            mark_step_running(
                db=db,
                step=step,
            )

            result = execute_action(
                action_name=action,
                payload=payload,
                config=config,
            )

            success = result.get("success") is True or result.get("status") == "success"

            if success:

                mark_step_completed(
                    db=db,
                    step=step,
                    output=result,
                )

                mark_workflow_completed(
                    db=db,
                    workflow_execution=workflow_execution,
                    output=result,
                )

            else:

                workflow_failed = True

                mark_step_failed(
                    db=db,
                    step=step,
                    error=result,
                )

                mark_workflow_failed(
                    db=db,
                    workflow_execution=workflow_execution,
                    error=str(result),
                )

        except Exception as e:

            workflow_failed = True

            logger.exception(
                "runtime_processor_workflow_failed",
                extra={
                    "extra_data": {
                        "event_id": event["event_id"],
                        "workflow_id": workflow.id,
                        "error": str(e),
                    }
                },
            )

            if step:
                mark_step_failed(
                    db=db,
                    step=step,
                    error=str(e),
                )

            if workflow_execution:
                mark_workflow_failed(
                    db=db,
                    workflow_execution=workflow_execution,
                    error=str(e),
                )

    if workflow_failed:

        handle_retry(
            db=db,
            event=event,
            error=Exception("one_or_more_workflows_failed"),
        )

    logger.info(
        "runtime_processor_completed",
        extra={
            "extra_data": {
                "event_id": event["event_id"],
                "matched_count": len(matched_workflows),
            }
        },
    )
