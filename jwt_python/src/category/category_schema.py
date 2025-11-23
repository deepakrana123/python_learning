from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional


class CategoryBase(BaseModel):
    name: str
    price: str
    category: str
    price: float
    stock: int
    rating: float
    published_by: str
    published_date: datetime


class CategoryCreateModel(CategoryBase):
    pass


class CategoryResponseModal(CategoryBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CategoryUpdateModal(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    rating: Optional[float] = None
    published_by: Optional[str] = None
    published_date: Optional[datetime] = None
