# redis_client.py
from redis.asyncio import Redis
from ..config import Config
import uuid
from datetime import datetime, timedelta
import jwt
import json

# decode_responses=True → JSON-like behavior
# ✔ Single client → connection pooling
redis = Redis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True
)


class TokenService:
    @staticmethod
    def generate_jti():
        return str(uuid.uuid4())

    @staticmethod
    def encode(data: dict, expiry_minutes: int, refresh: bool = False):
        jti = TokenService.generate_jti()
        exp = datetime.utcnow() + timedelta(minutes=expiry_minutes)

        payload = {
            **data,
            "jti": jti,
            "iat": datetime.utcnow(),
            "exp": exp,
            "refresh": refresh,
        }

        token = jwt.encode(payload, Config.JWT_TOKEN, algorithm=[Config.JWT_ALGORITHIM])
        return token, jti, exp


class AccessTokenService:
    @staticmethod
    async def blacklist(jti: str, exp: datetime):
        ttl = max(int((exp - datetime.utcnow())).total_seconds(), 1)
        await redis.setex(f"access:blacklist:{jti}", ttl, "1")

    @staticmethod
    async def is_blacklisted(jti: str) -> bool:
        return await redis.exists(f"access:blacklist:{jti}") == 1


class RefreshTokenService:
    MAX_SESSIONS = 5

    @staticmethod
    async def store(user_id: int, jti: str, exp: datetime, device: str):
        """
        Store refresh token per device
        """
        # ttl = int((exp - datetime.utcnow())).total_seconds()
        # key = f"refresh:{user_id}:{device}"
        # await redis.hset(key, mapping={"jti": jti, "exp": exp.timestamp()})
        # await redis.expire(key, ttl)
        # await redis.sadd(f"user:session:{user_id}", device)
        key = f"refresh:{user_id}"
        session_data = {
            "jti": jti,
            "device": device,
            "exp": exp.timestamp(),
        }

        # store sessions as json array

        session_json = await redis.get(key)
        sessions = json.load(session_json)

        # remove old session if same device

        sessions = [s for s in sessions if s["device"] != device]

        if len(sessions) >= RefreshTokenService.MAX_SESSIONS:
            sessions.pop(0)

        sessions.append(session_data)
        await redis.set(key, json.dump(sessions))
        ttl = max(int((exp - datetime.utcnow()).total_seconds()), 1)
        await redis.expire(key, ttl)

    @staticmethod
    async def validate(user_id: int, device: str, jti: str):
        # key = f"refresh:{user_id}:{device}"
        # saved = await redis.hgetall(key)
        # if not saved:
        #     return False
        # return saved.get("jti") == jti
        """
        Validate refresh token JTI
        """
        key = f"refresh:{user_id}"
        sessions_json = await redis.get(key)
        if not sessions_json:
            return False

        sessions = json.loads(sessions_json)
        for s in sessions:
            if s["jti"] == jti:
                if datetime.utcnow().timestamp < s["exp"]:
                    return True
        return False

    @staticmethod
    async def revoke(user_id: str, jti: str):
        """Revoke a refresh token"""

        key = f"refresh:{user_id}"
        sessions_json = await redis.get(key)
        if not sessions_json:
            return
        sessions = json.load(sessions_json)
        sessions = [s for s in sessions]
        if sessions:
            await redis.set(key, json.dumps(sessions))
        else:
            await redis.delete(key)
