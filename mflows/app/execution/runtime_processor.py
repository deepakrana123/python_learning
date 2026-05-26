from app.execution.workflow_loader import load_active_workflows
from app.execution.matcher import get_matching_workflows
from app.repositories.entity_repo import fetch_entity_payload

from app.execution.runtime.workflow_execution_service import (
    create_workflow_execution,
    mark_workflow_running,
)

# from app.execution.runtime. import run_dag_execution  # OLD: incomplete import path
from app.execution.runtime.dag_executor import run_dag_execution
from app.execution.runtime.workflow_finalizer import (
    finalize_workflow_execution,
)

from app.execution.dedupe import is_duplicate_execution
from app.core.logger import logger


def runtime_processor(db, event: dict):
    workflows = load_active_workflows(db)

    payload = fetch_entity_payload(db, event["entity_type"], event["entity_id"])

    matched_workflows = get_matching_workflows(
        workflows=workflows, event=event, payload=payload
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

    for workflow in matched_workflows:
        workflow_execution = None  # FIX: defined before try so except block can reference it
        try:
            if is_duplicate_execution(
                event_id=event["event_id"], workflow_id=workflow.id
            ):
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
                workflow_id=workflow.id,
                event_id=event["event_id"],
                event_type=event["event_type"],
                entity_id=event["entity_id"],
            )
            mark_workflow_running(db=db, workflow_execution=workflow_execution)
            dag = workflow.parsed_rule_json
            run_dag_execution(
                db=db,
                workflow_execution=workflow_execution,
                dag=dag,
                payload=payload,
            )

            finalize_workflow_execution(
                db=db,
                workflow_execution=workflow_execution,
            )

        except Exception as e:
            logger.exception(
                "runtime_processor_failed",
                extra={
                    "extra_data": {
                        "event_id": event["event_id"],
                        "workflow_id": workflow.id,
                        "error": str(e),
                    }
                },
            )
            # FIX: finalize workflow on exception so it doesn't stay RUNNING forever
            # OLD: only logged, workflow stayed RUNNING until reaper recovered it
            if workflow_execution:
                finalize_workflow_execution(db=db, workflow_execution=workflow_execution)
    logger.info(
        "runtime_processor_completed",
        extra={
            "extra_data": {
                "event_id": event["event_id"],
                "matched_count": len(matched_workflows),
            }
        },
    )
