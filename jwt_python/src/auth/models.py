from sqlmodel import SQLModel, Field, Column
from datetime import datetime
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import func
from typing import Optional


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

    username: str = Field(
        ..., sa_column=Column(pg.VARCHAR(30), unique=True, index=True)
    )
    email: str = Field(..., sa_column=Column(pg.VARCHAR(120), unique=True, index=True))

    hash_password: str = Field(sa_column=Column(pg.TEXT), exclude=True)
    is_verified: bool = Field(default=False)

    phone_number: Optional[str] = Field(
        default=None, sa_column=Column(pg.VARCHAR(20), nullable=True, unique=True)
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now()),
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            pg.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
        ),
    )

    def __repr__(self):
        return f"<User {self.username}>"
