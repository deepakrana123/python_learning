from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.event import EventRequest, EventResponse
from app.db.session import SessionLocal
from app.services.execution_service import process_event_service

router = APIRouter(prefix="/events", tags=["Events"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=EventResponse)
def process_event(payload: EventRequest, db: Session = Depends(get_db)):
    return process_event_service(payload, db)
