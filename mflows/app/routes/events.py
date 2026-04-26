from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.event import TriggerRequest, TriggerResponse
from app.db.session import get_db
from app.services.execution_service import process_event_service

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", response_model=TriggerResponse)
def process_event(payload: TriggerRequest, db: Session = Depends(get_db)):
    return process_event_service(payload, db)
