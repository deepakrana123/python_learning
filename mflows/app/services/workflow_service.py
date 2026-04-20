from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.workflow_schemas import WorkflowCreate
from app.repositories.workflow_repository import (
    create_workflow,
    get_workflow_by_id,
    list_workflows_by_domain,
)
from app.services.parser.orchestrator import parse_workflow_text
import json


def create_workflow_service(payload: WorkflowCreate, db: Session):
    if payload.domain not in ["support", "loan"]:
        raise HTTPException(status_code=400, detail="Invalid domain")
    parse_result = parse_workflow_text(payload.raw_input)
    if not parse_result["validation"]["is_valid"]:
        raise HTTPException(status_code=400, detail=parse_result)
    workflow = create_workflow(
        db=db,
        name=payload.name,
        domain=payload.domain,
        raw_input=payload.raw_input,
        parsed_rule_json=json.dumps(parse_result["rule"]),
    )
    return workflow


def get_workflow_service(workflow_id: int, db=Session):
    workflow = get_workflow_by_id(db, workflow_id)
    if not workflow:
        raise HTTPException(status_code=400, detail="Workflow not found")
    return workflow


def list_workflow_service(domain, db):
    return list_workflows_by_domain(db, domain)


def debug_parse_service(raw_text):
    return parse_workflow_text(raw_text)
