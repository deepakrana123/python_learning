from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.auth.service import AuthService
from app.models.user import User
from sqlalchemy.orm import Session
from app.db import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
auth_service = AuthService()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    try:
        user_id = auth_service.verify_token(token)
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="not_found")
        return user
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
