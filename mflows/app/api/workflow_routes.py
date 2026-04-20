from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.workflow_schemas import (
    WorkflowCreate,
    WorkflowResponse,
    DebugParseRequest,
)
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


@router.post("/", response_model=WorkflowCreate)
def create_workflow(payload: WorkflowCreate, db: Session = (get_db)):
    return create_workflow_service(payload, db)


@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(workflow_id: int, db: Session = (get_db)):
    return get_workflow_service(workflow_id, db)
