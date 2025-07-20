from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.auth.service import AuthService
from app.db import get_db
from app.models.user import User


router = APIRouter()
auth_service = AuthService()


class RegisterSchema(BaseModel):
    username: str
    password: str


class LoginSchema(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(payload: RegisterSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if user:
        raise HTTPException(400, detail="User not found")
    hashed = auth_service.hash_password(payload.password)
    new_user = User(username=payload.username, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    return {"msg": "User registered successfully"}


@router.post("/login")
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not auth_service.verify_password(
        payload.password, user.hashed_password
    ):
        raise HTTPException(400, detail="User not found")
    token = auth_service.create_token(user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def get_me(user: User = Depends(get_db(get_current_user))):
    return {"id": user.id, "username": user.username}
