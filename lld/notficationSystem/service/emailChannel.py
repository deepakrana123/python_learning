from .tokenBucketForRateLimiting import TokenBucket
from .batchBuffer import BatchBuffer


class EmailChannel:
    def __init__(self, tokenBucket: TokenBucket, batchBuffer: BatchBuffer):
        self.rate_limiter = tokenBucket(capacity=30, refill_rate=30)
        self.buffer = batchBuffer(
            batch_size=10, flush_interval=2, flush_callback=self._send_batch
        )

    def send(self, task):
        if task.is_batchable:
            self.buffer.add(task)
        else:
            self._send_with_rate_limit(task)

    def _send_with_rate_limit(self, task):
        if self.rate_limiter.try_consume(task):
            self._send_single(task)
        else:
            self._handle_rate_limited(task)

    def _send_batch(self, tasks):
        allowed = []
        rejected = []
        for task in tasks:
            if self.rate_limiter.try_consume():
                allowed.append(task)
            else:
                rejected.append(task)
        if allowed:
            print(f"sending")
        for task in rejected:
            self._handle_rate_limited(task)

    def _send_with_rate_limit(self, task):
        if self.rate_limiter.try_consume():
            self._send_single()
        else:
            self._handle_rate_limited(task)

    def _handle_rate_limited(self, task):
        print(f"rate limited , retry later:{task}")

    def _send_single(self, task):
        print(f"sending single sms:{task}")

    def _send_batch(self, task):
        print(f"sending batch sms:{len(task)}")
