from fastapi import FastAPI, Request, Response, HTTPException
from limiter import RateLimiter
from startegy.sliding_local import SlidingWindowLocalLimiter
from startegy.sliding_redis import SlidingWindowRedisLimiter
import time
from limiter import get_limit_config
from .mointor.monitor import rate_limit_monitor
from .config.rateLimit import TIER_LIMITS, get_user_tier
from .luascript import SLIDING_WINDOW_LUA

app = FastAPI()

startegy = SlidingWindowLocalLimiter()

limiter = RateLimiter(startegy)


@app.get("/")
async def home(request: Request):
    user_id = request.headers.get("X-User-ID", "anon")
    ip = request.client.host
    endpoint = request.url.path

    config = get_limit_config(user_id, ip, endpoint)
    allowed, remaining, retry_after = limiter.is_allowed(
        user_id, config["limit"], config["window"]
    )

    # allowed, remaining, retry_after = limiter.is_allowed(user_id)
    now = time.time()
    headers = {
        "X-RateLimit-Limit": str(startegy.limit),
        "X-RateLimit-Remaining": str(remaining),
        "X-RateLimit-Reset": str(now + retry_after if retry_after else now),
    }

    if not allowed:
        headers = {"Retry-After": str(retry_after)}
        raise HTTPException(
            status_code=429, detail="Too Many Requests", headers=headers
        )
    return {"message": "OK", "remaining": remaining}


@app.get("/rate-limit/monitor")
def monitor():
    return rate_limit_monitor


@app.get("/check")
def check(request: Request):
    user_id = request.headers.get("X-User-ID", "anon")
    allowed, remaining, retry_after = SLIDING_WINDOW_LUA.is_allowed(user_id)

    headers = {
        "X-RateLimit-Limit": str(SLIDING_WINDOW_LUA.limit),
        "X-RateLimit-Remaining": str(remaining),
        "X-RateLimit-Reset": str(int(time.time()) + retry_after),
    }

    if not allowed:
        headers["Retry-After"] = str(retry_after)
        raise HTTPException(
            status_code=429, detail="Rate limit exceeded", headers=headers
        )

    return Response("✅ Allowed", headers=headers)


@app.get("/check_limit")
def check(request: Request):
    user_id = request.headers.get("X-User-ID", "anon")
    tier = get_user_tier(request)

    config = TIER_LIMITS.get(tier, TIER_LIMITS["default"])
    limit = config["limit"]
    window = config["window"]

    # Use Redis Lua-based limiter (or local if preferred)
    allowed, remaining, retry_after = SLIDING_WINDOW_LUA.is_allowed(
        user_id, limit, window
    )

    headers = {
        "X-RateLimit-Limit": str(limit),
        "X-RateLimit-Remaining": str(remaining),
        "X-RateLimit-Reset": str(int(time.time()) + retry_after),
        "X-Tier": tier,
    }

    if not allowed:
        headers["Retry-After"] = str(retry_after)
        raise HTTPException(
            status_code=429, detail=f"Rate limit exceeded ({tier})", headers=headers
        )

    return Response(f"✅ {tier} allowed", headers=headers)
