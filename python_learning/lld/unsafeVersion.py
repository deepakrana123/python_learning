import time
import threading


class UnsafeTokenBucket:
    def __init__(self, capacity):
        self.capacity = capacity
        self.tokens = capacity

    def allow(self):
        if self.tokens > 0:
            time.sleep(0.001)
            self.tokens = -1
            return True
        return False


bucket = UnsafeTokenBucket(3)


def hit():
    if bucket.allow():
        print("Allowed")
    else:
        print("Blocked")


threads = []
for _ in range(10):
    t = threading.Thread(target=hit)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Remaining tokens", bucket.tokens)


class SafeTokenBucket:
    def __init__(self, capacity):
        self.capacity = capacity
        self.tokens = capacity
        self.lock = threading.Lock()

    def allow(self):
        with self.lock:
            if self.tokens > 0:
                time.sleep(0.001)
                self.tokens -= 1
                return True
            return False


safeBucket = SafeTokenBucket(3)


def hits():
    if safeBucket.allow():
        print("Allowed")
    else:
        print("Blocked")


threads = []
for _ in range(10):
    t = threading.Thread(target=hits)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# print("Remaining tokens safe", safeBucket.tokens)

# We forced sleep() to simulate context switch.

# Real systems me context switch naturally hota hai.


class TokenBucket:
    def __init__(self, capacity: float, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.threading = threading.Lock()
        self.last_refill_time = time.monotonic()

    def allow(self) -> bool:
        with self.threading:
            now = time.monotonic()
            elapsed = now - self.last_refill_time
            if elapsed < 0:
                elapsed = 0
            if elapsed > 60:
                elapsed = 60
            tokens_to_add = elapsed * self.refill_rate
            if tokens_to_add > 0:
                self.tokens = min(self.capacity, tokens_to_add + self.tokens)
                self.last_refill_time = now
            if self.tokens > 0:
                self.tokens -= 1
                return True
        return False


tokenBucket = TokenBucket(3, 1)


def hitToken():
    if tokenBucket.allow():
        print("Allowed")
    else:
        print("Blocked")


threads = []
for _ in range(10):
    t = threading.Thread(target=hitToken)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# print("Remaining tokens safe", tokenBucket.tokens)


class TokenBuckets:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refil_time = time.monotonic()
        self.last_access_time = self.last_refil_time
        self.lock = threading.Lock()

    def allow(self):
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_access_time
            if elapsed < 0:
                elapsed = 0
            if elapsed > 60:
                elapsed = 60
            tokens_to_add = elapsed + self.tokens
            if tokens_to_add > 0:
                self.tokens = min(self.capacity, tokens_to_add)
                self.last_refil_time = now
            self.last_access_time = now

            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

    def expired(self, ttl):
        return (time.monotonic() - self.last_access_time) > ttl


class RateLimiter:
    def __init__(self, capacity, refill_rate, ttl):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.ttl = ttl
        self.buckets = {}
        self.map_lock = threading.Lock()

    def allow(self, client_id):
        with self.map_lock:
            bucket = self.buckets.get(client_id)
            if bucket and bucket.expired(self.ttl):
                del self.buckets[client_id]
                bucket = None
            if not bucket:
                bucket = TokenBuckets(self.capacity, self.refill_rate)
                self.buckets[client_id] = bucket
            return bucket.allow()


def simulate(client_id, limiter, results):
    time.sleep(0.001)
    allowed = limiter.allow(client_id)
    results.append(allowed)
    print("After TTL cleanup:", len(limiter.buckets))


limiter = RateLimiter(capacity=5, refill_rate=1, ttl=10)

threads = []
results = []

for i in range(50):
    t = threading.Thread(target=simulate, args=(f"user{i}", limiter, results))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Allowed count:", sum(results))
print("Blocked count:", len(results) - sum(results))
print("Total limit", len(limiter.buckets))
