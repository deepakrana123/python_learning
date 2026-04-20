from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime


from app.db.session import Base


class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    raw_input = Column(Text, nullable=False)
    parsed_rule_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
