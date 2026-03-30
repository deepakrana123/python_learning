import random


class RetryManager:
    def __init__(self, base_delay=1, max_delay=60, max_retries=5):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.max_retires = max_retries

    def should_retry(self, task, result):
        if not result.retryable:
            return False

        if task["attempt"] >= self.max_retires:
            return False
        return True

    def get_backoff_delay(self, attempt):
        delay = min(self.base_delay * (2**attempt), self.max_delay)
        jitter = random.uniform(0, delay * 0.2)
        return jitter + delay
