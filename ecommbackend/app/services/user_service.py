import uuid
from app.models.user import User
from app.core.database import SessionLocal
from sqlalchemy.orm import Session  # type: ignore
from passlib.context import CryptContext  # type: ignore
from app.utils.redis import redis_client
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt  # type: ignore
from app.utils.email_utils import send_reset_email
from fastapi import HTTPException  # type: ignore


SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")
ALGORITHIM = "HS256"
ACCESS_TOKEN_EXPIRE_MINTUES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
MAX_ATTEMPTS = 5
BLOCK_TIME_SECOND = 10


def is_rate_limiting(key: str):
    attempts = redis_client.get(key)
    if attempts and attempts > MAX_ATTEMPTS:
        return True
    return False


def reset_attempts(key: str):
    redis_client.delete(key)


def increament_attack(key: str):
    if redis_client.exists(key):
        redis_client.incr(key)
    else:
        redis_client.set(key, 1, ex=BLOCK_TIME_SECOND)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINTUES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHIM)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHIM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHIM)
        return payload
    except JWTError:
        return None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)


def store_refresh_token(user_id: int, token: str):
    redis_client.set(
        f"refresh_token:{user_id}", token, ex=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )


def create_user(db: Session, username: str, password: str):
    hashed = get_hashed_password(password)
    user = User(username, hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str):
    redis_key = f"login_attempts:{username}"
    if is_rate_limiting(redis_key):
        raise HTTPException(status_code=400, message="To Many attempts")

    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.hashed_password):
        return user
    increament_attack(redis_key)
    return None


def login_user(db: Session, username: str, password: str):
    user = authenticate_user(db, username, password)
    if not user:
        return None
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    store_refresh_token(user.id, refresh_token)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def get_single_users(db: Session, user_id):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    return None


def forgot_password(db: Session, email: str):
    user = db.query(User).filter(User.email == email)
    if not user:
        return {"message": "if the"}
    token = str(uuid.uuid4())
    redis_client.setx(f"reset_token{token}", 900, user.id)
    send_reset_email(email, token)
    return {"message": "Reset Link"}


def reset_password(db: Session, token: str, new_password: str):
    user_id = redis_client.get(f"reset_token:{token}")
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user:
        user.hashed_password = get_hashed_password(user)
        db.commit()
        redis_client.delete(f"reset_token:{token}")
        return {"message": "Password"}
    raise HTTPException(status_code=400, detail="User not found")
