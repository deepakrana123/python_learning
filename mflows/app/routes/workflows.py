from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.workflow import (
    WorkflowCreate,
    WorkflowResponse,
    DebugParseRequest,
)
from typing import List
from app.services import workflow_service

router = APIRouter(prefix="/workflows")


@router.post("/", response_model=WorkflowResponse)
def create_workflow(payload: WorkflowCreate, db: Session = Depends(get_db)):
    try:
        return workflow_service.create_workflow_service(payload, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    try:
        return workflow_service.get_workflow_service(workflow_id, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[WorkflowResponse])
def get_all_worflow(domain: str | None = None, db: Session = Depends(get_db)):
    return workflow_service.list_workflow_service(domain, db)


@router.post("/debug-parse")
def debug_parse(payload: DebugParseRequest):
    return workflow_service.debug_parse_service(payload.raw_input)
