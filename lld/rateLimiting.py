import time
import threading
from collections import deque
from abc import ABC, abstractmethod
from enum import Enum
import heapq


class Algorithm(Enum):
    FIXED_WINDOW = 1
    SLIDING_LOG = 2
    SLIDING_COUNTER = 3
    TOKEN_BUCKET = 4


class RateLimitingStartegy:
    def __init__(self, max_request, window_seconds, algorithm=Algorithm.SLIDING_LOG):
        self.max_requests = max_request
        self.window = window_seconds
        self.algorithm = algorithm
        self.refill_rate = max_request / window_seconds

    def __repr__(self):
        return f"Config(limit={self.max_requests}/{self.window}s, algo={self.algorithm.name})"


class RateLimiterStrategy(ABC):
    @abstractmethod
    def allow_request(self, user_id, config, shared_data, lock):
        pass


class FixedWindowStrategy(RateLimiterStrategy):
    def allow_request(self, user_id, config, shared_data, lock):
        with lock:
            now = time.time()
            window_key = int(now / config.window)
            key = f"{user_id}"
            if key not in shared_data:
                shared_data[key] = 0
                old_key = f"{user_id}:{window_key - 1}"
                shared_data.pop(old_key, None)
            if shared_data[key] > config.max_requests:
                shared_data[key] += 1
                return True
            return False


class SlidingWindowLog(RateLimiterStrategy):
    def allow_request(self, user_id, config, shared_data, lock):
        with lock:
            now = time.time()
            cutoff = now - config.now

            if user_id not in shared_data:
                shared_data[user_id] = deque()

            queue = shared_data[user_id]
            while queue and queue[0] < cutoff:
                queue.popleft()
            if len(queue) < config.max_requests:
                queue.append(now)
                return True
            return False


class SlidingCounterStrategy(RateLimiterStrategy):
    def allow_request(self, user_id, config, shared_data, lock):
        with lock:
            now = time.time()
            current_window = int(now / config.window)
            current_window_start = current_window * config.window
            time_passed = now - current_window_start
            weight = time_passed / config.window

            if user_id not in shared_data:
                shared_data[user_id] = {
                    "prev_count": 0,
                    "curr_count": 0,
                    "prev_window": current_window - 1,
                    "curr_window": current_window,
                }

            data = shared_data[user_id]

            if data["curr_window"] != current_window:
                data["prev_count"] = data["curr_count"]
                data["curr_count"] = 0
                data["prev_window"] = data["curr_window"]
                data["curr_window"] = current_window
            estimated = data["prev_count"] * (1 - weight) + data["curr_count"]
            if estimated < config.max_requests:
                data["curr_count"] += 1
                return True
            return False


class TokenBucketStrategy(RateLimiterStrategy):
    def allow_request(self, user_id, config, shared_data, lock):
        with lock:
            now = time.time()
            if user_id not in shared_data:
                shared_data[user_id] = {
                    "tokens": config.max_requests,  # Start full
                    "last_refill": now,
                }
            data = shared_data[user_id]

            # Refill tokens
            elapsed = now - data["last_refill"]
            new_tokens = elapsed * config.refill_rate
            data["tokens"] = min(config.max_requests, data["tokens"] + new_tokens)
            data["last_refill"] = now

            if data["tokens"] >= 1:
                data["tokens"] -= 1
                return True
            return False
