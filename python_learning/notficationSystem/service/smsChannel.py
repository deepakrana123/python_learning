from .tokenBucketForRateLimiting import TokenBucket
from .batchBuffer import BatchBuffer
import threading


class SendResult:
    def __init__(self, success, retryable):
        self.success = success
        self.retryable = retryable


class SMSChannel:
    def __init__(self, tokenBucket: TokenBucket, batchBuffer: BatchBuffer):
        self.rate_limiter = tokenBucket(capacity=30, refill_rate=30)
        self.buffer = batchBuffer(
            batch_size=10, flush_interval=2, flush_callback=self._send_batch
        )
        self.semaphore = threading.Semaphore(5)

    def send(self, task):
        if task.is_batchable:
            self.buffer.add(task)
            return SendResult(True, False)
        return self._send_with_rate_limit(task)

    def _send_batch(self, tasks):
        allowed = []
        rejected = []
        for task in tasks:
            if self.rate_limiter.try_consume(1):
                allowed.append(task)
            else:
                rejected.append(task)
        if allowed:
            print(f"sending")
        for task in rejected:
            self._handle_rate_limited(task)

    def _send_with_rate_limit(self, task):
        if self.rate_limiter.try_consume(1):
            self._send_single()
        else:
            self._handle_rate_limited(task)

    def _handle_rate_limited(self):
        return SendResult(False, retryable=True)

    def _send_single(self, task):
        print(f"sending single sms:{task}")
