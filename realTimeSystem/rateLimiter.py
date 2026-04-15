import threading
from realTimeSystem.metrics.metrics import metrics
import time


class RateLimiter:
    def __init__(self, interval=1):
        self.interval = 1
        self.user_last_sent = {}
        self.lock = threading.Lock()

    def allow(self, user_id):
        now = time.time()
        with self.lock:
            last = self.user_last_sent.get(user_id, 0)
            if now - last < self.interval:
                metrics.inc("rate_limited")
                return False
            self.user_last_sent[user_id] = now
            return True
