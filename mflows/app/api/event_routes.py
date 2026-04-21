from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.event_schema import EventRequest
from app.services.execution_service import process_event_service

router = APIRouter(prefix="/event")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def process_event(payload: EventRequest, db: Session):
    return process_event_service(payload, db)
