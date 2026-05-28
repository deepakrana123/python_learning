from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"
    id = Column(BigInteger, primary_key=True, index=True)
    workflow_id = Column(
        BigInteger,
        ForeignKey("workflows.id"),
        nullable=False,
        index=True,
    )
    status = Column(
        String(30),
        default="QUEUED",
        nullable=False,
        index=True,
    )
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)
    error_text = Column(Text, nullable=True)
