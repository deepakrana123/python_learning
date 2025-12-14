from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from .config import Config
import uuid
import logging

passwd_context = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRY = timedelta(minutes=50)
REFRESH_TOKEN_EXPIRY = timedelta(days=7)


def generate_password_hash(password: str) -> str:
    hash = passwd_context.hash(password)
    return hash


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_access_token(user_data: dict, expiry: timedelta, refresh: bool = False):
    if expiry is None:
        expiry = REFRESH_TOKEN_EXPIRY if refresh else ACCESS_TOKEN_EXPIRY
    payload = {
        "user": user_data,
        "jti": str(uuid.uuId4()),
        "refresh": refresh,
        "exp": datetime.utcnow() + expiry,
        "iat": datetime.utcnow(),
    }

    token = jwt.encode(
        payload=payload, key=Config.JWT_TOKEN, algorithm=[Config.JWT_ALGORITHIM]
    )
    return token


def decode_token(token: str):
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_TOKEN, algorithm=[Config.JWT_ALGORITHIM]
        )
        return token_data
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.PyJWKError as e:
        logging.expection(e)
        return None
