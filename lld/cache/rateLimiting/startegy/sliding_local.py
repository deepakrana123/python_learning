from collections import defaultdict, deque
import time, threading, heapq
from .base import IRateLimiterStrategy
from ..mointor.monitor import rate_limit_monitor


class SlidingWindowLocalLimiter(IRateLimiterStrategy):
    def __init__(self, limit, window_size):
        self.limit = limit
        self.window_size = window_size
        self.user_requests = defaultdict()
        self.ttl_heap = []
        threading.Thread(target=self._clean_up, daemon=True).start()

    def is_allowed(self, user_id, limit=None, window=None):
        self.limit = limit or self.limit
        self.window_size = window or self.window_size
        now = int(time.time())
        window_start = now - self.window_size
        dq = self.user_requests[user_id]

        while dq and dq[0] < window_start:
            dq.popleft()
        if len(dq) < self.limit:
            dq.append(now)
            rate_limit_monitor[user_id]["allowed"] += 1
            heapq.heappush(self.ttl, (now + self.window_size, user_id))
            return True, self.limit - len(dq), 0
        else:
            rate_limit_monitor[user_id]["blocked"] += 1
            retry_after = self.window_size - (now - dq[0])
            return False, 0, retry_after

    def _cleanu_up(self):
        while True:
            now = int(time.time())
            while self.ttl_heap and self.ttl_heap[0][0] <= now:
                _, user_id = heapq.heappop()
                if user_id in self.user_requests:
                    del self.user_requests[user_id]
            time.sleep(1)
