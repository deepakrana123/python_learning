from fastapi import ApiRouter, Request, Depends, HttpExceution  # type: ignore
from app.core.database import SessionLocal
from sqlalchemy.orm import Session  # type: ignore
from app.schemas.user import UserCreate, ForgotPassword, ResetPassword
from app.services.auth_service import create_user, forgot_password, reset_password  # type: ignore


router = ApiRouter()


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(getDb)):
    return create_user(db, user.username, user.password)


@router.post("/login")
def login_user(user: UserCreate, request: Request, db: Session = Depends(getDb)):
    tokens = login_user(db, user.username, user.password)
    if not tokens:
        raise HttpExceution(status_code=401, detail="Invalid credentials")
    return tokens


@router.get("/user/{user_id}")
def get_single_user(user_id: int, db: Session = Depends(getDb)):
    return get_single_user(user_id)


@router.post("/forget-password")
def forget_pw(data: ForgotPassword, db: Session = Depends(getDb)):
    return forgot_password(db, data)


@router.post("/reset-password")
def forget_pw(data: ResetPassword, db: Session = Depends(getDb)):
    return reset_password(db, data)
