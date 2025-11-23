from ..luascript import SLIDING_WINDOW_LUA
import time


class SlidingWindowLuaLimiter:
    def __init__(self, redis_client, limit, window):
        self.redis = redis_client
        self.limit = limit
        self.window = window
        self.sha = redis_client.script_load(SLIDING_WINDOW_LUA)

    def is_allowed(self, user_id):
        key = f"ratlimit:{user_id}"
        now = int(time.time())
        result = self.redis.evalsha(self.sha, 1, key, now, self.window, self.limit)
        allowed = result[0] == 1
        remaining = result[1]
        retry_after = result[2]
        return allowed, remaining, retry_after
