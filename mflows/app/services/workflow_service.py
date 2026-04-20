from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.workflow import Workflow
from app.schemas.workflow_schemas import WorkflowCreate
from app.repositories.workflow_repository import (
    create_workflow,
    get_workflow_by_id,
    list_workflows_by_domain,
)


def create_workflow_service(payload: WorkflowCreate, db: Session):
    if payload.domain not in ["support", "loan"]:
        raise HTTPException(status_code=400, detail="Invalid domain")
    return create_workflow(
        db,
        name=payload.name,
        domain=payload.domain,
        raw_input=payload.raw_input,
        parsed_rule_json="",
    )


def get_workflow_service(workflow_id: int, db=Session):
    return get_workflow_by_id(db, workflow_id)
