from sqlmodel import SQLModel, Field, Column
from datetime import datetime
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import func
from typing import Optional


class CategoryBase(SQLModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        index=True,
        description="Name of the category",
    )
    category: str = Field(
        ...,
        min_length=2,
        max_length=50,
        index=True,
        description="Category type",
    )
    price: float = Field(..., ge=0, description="Price must be positive")
    stock: float = Field(..., ge=0, description="Stock should be greater then 1")
    rating: float = Field(
        ..., ge=0, description="Rating should be greater or equal to zero"
    )
    published_by: str = Field(..., min_length=2)
    published_date: datetime = Field(default_factory=datetime.now)


class Category(CategoryBase, table=True):
    __tablename__ = "categories"
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

    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            server_default=func.now(),
        ),
        default_factory=datetime.utcnow,
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
        ),
        default_factory=datetime.utcnow,
    )

    def __repr__(self):
        return f"<Category {self.name}>"


class CategoryUpdateModel(SQLModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    rating: Optional[float] = None
    published_by: Optional[str] = None
    published_date: Optional[datetime] = None
