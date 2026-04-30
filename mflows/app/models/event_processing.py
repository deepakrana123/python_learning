from sqlalchemy import Column, String, Integer, DateTime, Text
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base
from sqlalchemy.sql import func


class EventProcessing(Base):
    __tablename__ = "event_processing"

    event_id = Column(String, primary_key=True, index=True)
    status = Column(String(50), nullable=False, index=True)
    workflow_id = Column(String, nullable=True, index=True)
    attempts = Column(Integer, default=0, nullable=False)
    last_error = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"<EventProcessing(event_id={self.event_id}, status={self.status}, attempts={self.attempts})>"
