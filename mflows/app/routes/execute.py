import json
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from app.schemas.execute import ExecuteWorkflow
from app.core.redis_client import redis_client
from app.db.session import SessionLocal
from app.models.workflow import Workflow
from app.models.workflow_run import WorkflowRun
from app.models.workflow_execution import WorkflowExecution
from app.core.logger import logger
from app.execution.runtime.workflow_execution_service import (
    mark_workflow_running,
    mark_workflow_paused,
)

router = APIRouter(prefix="/execute", tags=["execute"])


@router.post("/")
def publish_event(body: ExecuteWorkflow):
    db = SessionLocal()
    try:
        workflow = db.query(Workflow).filter(Workflow.id == body.workflow_id).first()
        if not workflow:
            raise HTTPException(status_code=404, detail="worflow not found")
        workflow_run = WorkflowRun(workflow_id=workflow.id, entity_id=body.entity_id)
        db.add(workflow_run)
        db.commit()
        db.refresh(workflow_run)

        workflow_execution = WorkflowExecution(
            workflow_id=workflow.id, workflow_run_id=workflow.id, status="PENDING"
        )
        db.add(workflow_execution)
        db.commit()
        db.refresh(workflow_execution)

        workflow_event = {"workflow_execution_id": workflow_execution.id}
        redis_client.lpush("workflow_events", json.dumps(workflow_event))

        logger.info(
            "workflow_execution_queued",
            extra={
                "extra_data": {
                    "workflow_run_id": workflow_run.id,
                    "workflow_execution_id": workflow_execution.id,
                    "workflow_id": workflow.id,
                }
            },
        )
        return {
            "success": True,
            "queued": True,
            "workflow_run_id": workflow_run.id,
            "workflow_execution_id": workflow_execution.id,
        }

    except IntegrityError:
        db.rollback()
        return {"success": False, "message": "duplicate execution ignore"}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@router.post("/{workflow_execution_id}/pause")
def pause_execution(
    workflow_execution_id: int,
):
    db = SessionLocal()

    try:

        execution = (
            db.query(WorkflowExecution)
            .filter(WorkflowExecution.id == workflow_execution_id)
            .first()
        )

        if not execution:
            return {
                "success": False,
                "message": "workflow execution not found",
            }

        mark_workflow_paused(
            db=db,
            workflow_execution=execution,
        )

        return {
            "success": True,
            "workflow_execution_id": execution.id,
            "status": execution.status,
        }

    finally:
        db.close()


@router.post("/{workflow_execution_id}/resume")
def resume_execution(
    workflow_execution_id: int,
):
    db = SessionLocal()

    try:

        execution = (
            db.query(WorkflowExecution)
            .filter(WorkflowExecution.id == workflow_execution_id)
            .first()
        )

        if not execution:
            return {
                "success": False,
                "message": "workflow execution not found",
            }

        mark_workflow_running(
            db=db,
            workflow_execution=execution,
        )

        return {
            "success": True,
            "workflow_execution_id": execution.id,
            "status": execution.status,
        }

    finally:
        db.close()
