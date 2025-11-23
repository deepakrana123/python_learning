from sqlmodel import SQLModel, Field, Column
from datetime import datetime
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import func
from typing import Optional

"""
class User:
uid:uuid.UUID,


"""


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            index=True,
            nullable=False,
            unique=True,
        ),
    )

    username: str = Field(..., min_length=3, max_length=50, unique=True, index=True)
    email: str = Field(..., unique=True, index=True)
    hash_password: str = Field(exclude=True)
    is_verified: bool = Field(default=False)
    phone_number: Optional[str] = Field(
        default=None, sa_column=Column(pg.VARCHAR(20), nullable=True, unique=True)
    )

    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now()),
        default_factory=datetime.utcnow,
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now()),
        default_factory=datetime.utcnow,
    )

    def __repr__(self):
        return f"<User {self.username}>"
