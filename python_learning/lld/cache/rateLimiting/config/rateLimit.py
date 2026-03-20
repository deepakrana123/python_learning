from fastapi import Request

RATE_LIMIT_CONFIG = {
    "user123": {"limit": 10, "window": 60},  # user-based
    "192.168.1.10": {"limit": 5, "window": 30},  # IP-based
    "/login": {"limit": 3, "window": 15},  # endpoint-based
    "default": {"limit": 20, "window": 60},  # fallback
}

TIER_LIMITS = {
    "free": {"limit": 10, "window": 60},
    "premium": {"limit": 100, "window": 60},
    "admin": {"limit": 1000, "window": 60},
    "default": {"limit": 5, "window": 60},
}


def get_limit_config(user_id, ip, endpoint):
    if user_id in RATE_LIMIT_CONFIG:
        return RATE_LIMIT_CONFIG[user_id]
    if ip in RATE_LIMIT_CONFIG:
        return RATE_LIMIT_CONFIG[ip]
    if endpoint in RATE_LIMIT_CONFIG:
        return RATE_LIMIT_CONFIG[endpoint]
    return RATE_LIMIT_CONFIG["default"]


def get_user_tier(request: Request):
    return request.headers.get("X-Tier", "default").lower()
