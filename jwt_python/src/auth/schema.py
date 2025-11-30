from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
import uuid


class UserCreateModel(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)
    phone_number: str | None


class UserBaseModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str

    is_verified: bool
    phone_number: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str
