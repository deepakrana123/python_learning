from startegy.base import IRateLimiterStrategy


class RateLimiter:
    def __init__(self, strategy):
        self.startegy = strategy

    def is_allowed(self, user_id):
        return self.startegy.is_allowed(user_id)
