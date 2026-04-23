from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.workflow import (
    WorkflowCreate,
    WorkflowResponse,
    DebugParseRequest,
)
from typing import List
from app.services.workflow_service import (
    create_workflow_service,
    get_workflow_service,
    list_workflow_service,
    debug_parse_service,
)

router = APIRouter(prefix="/workflows")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=WorkflowResponse)
def create_workflow(payload: WorkflowCreate, db: Session = Depends(get_db)):
    return create_workflow_service(payload, db)


@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    return get_workflow_service(workflow_id, db)


@router.get("/", response_model=List[WorkflowResponse])
def get_all_worflow(domain: str | None = None, db: Session = Depends(get_db)):
    return list_workflow_service(domain, db)


@router.post("/debug-parse")
def debug_parse(payload: DebugParseRequest):
    return debug_parse_service(payload.raw_input)
