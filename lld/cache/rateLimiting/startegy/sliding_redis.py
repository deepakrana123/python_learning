import time
from .base import IRateLimiterStrategy


class SlidingWindowRedisLimiter(IRateLimiterStrategy):
    def __init__(self, redis_client, limit, window):
        self.redis = redis_client
        self.limit = limit
        self.window = window

    def is_allowed(self, user_id, limit=None, window=None):
        self.limit = limit or self.limit
        self.window = window or self.window
        now = int(time.time())
        key = f"sliding:{user_id}"

        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, now)
        pipe.zcard(key)
        pipe.zad(key, {str(now): now})
        pipe.expire(key, self.window)
        _, count, *_ = pipe.execute()

        if count < self.limit:
            return True, self.limit - count, 0
        else:
            earliest = self.redis.zrange(key, 0, 0, withscores=True)
            if earliest:
                retry_after = self.window - (now - int(earliest[0][1]))
            else:
                retry_after = self.window
            return False, 0, retry_after
