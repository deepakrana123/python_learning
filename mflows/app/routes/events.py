import json
from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError
import uuid
from app.schemas.event import EventCreate
from app.core.redis_client import redis_client
from app.db.session import SessionLocal
from app.models.event_processing import EventProcessing
from app.models.workflow_execution import WorkflowExecution
from app.core.logger import logger
from app.execution.runtime.workflow_execution_service import (
    mark_workflow_running,
    mark_workflow_paused,
)

router = APIRouter(prefix="/event", tags=["events"])


@router.post("/publish")
def publish_event(body: EventCreate):
    event_id = str(uuid.uuid4())
    event = {
        "event_id": event_id,
        "event_type": body.event_type,
        "entity_type": body.entity_type,
        "entity_id": body.entity_id,
    }
    try:
        db = SessionLocal()
        record = EventProcessing(
            event_id=event["event_id"],
            event_type=event["event_type"],
            entity_type=event["entity_type"],
            entity_id=event["entity_id"],
            status="RECEIVED",
        )
        db.add(record)
        db.commit()
        redis_client.lpush("workflow_events", json.dumps(event))
        logger.info(
            "event_received",
            extra={
                "extra_data": {
                    "event_id": event_id,
                    "event_type": event["event_type"],
                }
            },
        )
    except IntegrityError:
        db.rollback()
        return {"status": "duplicate_ignored"}
    except Exception as e:
        db.rollback()
        db.query(EventProcessing).filter(EventProcessing.event_id == event_id).delete()
        raise e
    finally:
        db.close()
    return {"success": True, "queued": True}


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
