from app.models.workflow_execution import WorkflowExecution
from app.models.workflow import Workflow
from app.execution.runtime.workflow_execution_service import (
    mark_workflow_running,
    mark_workflow_failed,
)
from app.execution.runtime.dag_executor import run_dag_execution
from app.execution.runtime.workflow_finalizer import finalize_workflow_execution
from app.core.logger import logger


def runtime_processor(db, workflow_execution_id: int):
    workflow_execution = (
        db.query(WorkflowExecution)
        .filter(WorkflowExecution.id == workflow_execution_id)
        .first()
    )

    if not workflow_execution:
        logger.warning(
            "workflow_execution_not_found",
            extra={"extra_data": {"workflow_execution_id": workflow_execution_id}},
        )
        return

    # Guard: skip if already past PENDING (duplicate delivery from Redis)
    if workflow_execution.status not in ("PENDING", "PAUSED"):
        logger.info(
            "workflow_execution_already_processed",
            extra={
                "extra_data": {
                    "workflow_execution_id": workflow_execution_id,
                    "status": workflow_execution.status,
                }
            },
        )
        return

    try:
        mark_workflow_running(db=db, workflow_execution=workflow_execution)

        # FIX C1: was missing .first() — returned Query object, not Workflow instance
        workflow = (
            db.query(Workflow)
            .filter(Workflow.id == workflow_execution.workflow_id)
            .first()
        )

        if not workflow:
            logger.error(
                "workflow_definition_not_found",
                extra={
                    "extra_data": {
                        "workflow_execution_id": workflow_execution_id,
                        "workflow_id": workflow_execution.workflow_id,
                    }
                },
            )
            mark_workflow_failed(
                db=db,
                workflow_execution=workflow_execution,
                error="workflow_definition_not_found",
            )
            return

        dag = workflow.parsed_rule_json or {}

        # FIX H6: empty DAG must fail — not silently complete
        if not dag.get("steps"):
            logger.error(
                "workflow_dag_empty",
                extra={"extra_data": {"workflow_execution_id": workflow_execution_id}},
            )
            mark_workflow_failed(
                db=db,
                workflow_execution=workflow_execution,
                error="workflow_dag_has_no_steps",
            )
            return

        payload = {"entity_id": workflow_execution.entity_id}

        run_dag_execution(
            db=db,
            workflow_execution=workflow_execution,
            dag=dag,
            payload=payload,
        )

        finalize_workflow_execution(db=db, workflow_execution=workflow_execution)

    except Exception as e:
        logger.exception(
            "runtime_processor_failed",
            extra={
                "extra_data": {
                    "workflow_execution_id": workflow_execution.id,
                    "error": str(e),
                }
            },
        )
        # FIX M3: call mark_workflow_failed directly — not finalize_workflow_execution
        # OLD: finalize was called in except — with zero steps it vacuously marked COMPLETED
        try:
            mark_workflow_failed(
                db=db,
                workflow_execution=workflow_execution,
                error=str(e),
            )
        except Exception as state_err:
            logger.error(
                "runtime_processor_failed_to_mark_failed",
                extra={
                    "extra_data": {
                        "workflow_execution_id": workflow_execution.id,
                        "error": str(state_err),
                    }
                },
            )
