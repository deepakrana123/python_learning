import threading
from realTimeSystem.metrics.metrics import metrics
import time


class RateLimiter:
    def __init__(self, interval=1):
        # ─────────────────────────────────────────────
        # PREVIOUS CODE:
        # self.interval = 1   ← BUG: hardcoded literal 1, ignores the `interval` parameter entirely.
        #                       RateLimiter(interval=5) would still enforce 1-second windows.
        #                       The parameter exists but has zero effect.
        self.interval = interval
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
