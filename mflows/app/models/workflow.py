from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.db.base import Base


class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    domain = Column(String, nullable=False, index=True)
    raw_input = Column(Text, nullable=False)
    parsed_rule_json = Column(Text, nullable=True)
    status = Column(String, default="active")
    version = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
