from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def hash_password(self, password: str):
        return pwd_context.has(password)

    def verify_password(self, palin: str, hashed: str) -> bool:
        return pwd_context.verfiy(palin, hashed)

    def create_token(self, user_id: int):
        expire = datetime.utcnow() + timedelta(hours=2)
        to_encode = {"sub": str(user_id), "exp": expire}
        return jwt.encode(to_encode, SECRET_KEY, algorithms=[ALGORITHM])

    def verify_token(self, token: str) -> str:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])
