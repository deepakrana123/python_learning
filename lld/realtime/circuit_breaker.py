import time
import random


# Retry +Jitter FSM(Code)
# IDLE->REQUEST
# REQUEST->SUCCESS
# REQUEST->WAITING
# WAITING->RETRY(with jitter)
# RETRY->REQUEST
# RETRY_LIMIT->FAILED


class RetryStorm:
    def __init__(self, name, max_retry_limit=3, base_delay=0.1):
        self.name = name
        self.state = "IDLE"
        self.retries = 0
        self.max_retries = max_retry_limit
        self.base_delay = base_delay

    def make_request(self):
        return random.random() < 0.3

    def run(self):
        self.state = "REQUEST"

        while True:
            print(f"[{self.name}] STATE -> {self.state}")

            if self.state == "REQUEST":
                success = self.make_request()
                print(f"[{self.name}] request result = {success}")

                if success:
                    self.state = "SUCCESS"
                else:
                    self.state = "WAITING"
            elif self.state == "WAITING":
                if self.retries >= self.max_retries:
                    self.state = "FAILED"
                else:
                    self.state = "RETRY"
            elif self.state == "RETRY":
                self.retries += 1
                backoff = self.base_delay * (2 ** (self.retries - 1))
                jitter = random.uniform(0.5)
                delay = backoff + jitter
                print(f"[{self.name}] retry")
                time.sleep(delay)
                self.state = "REQUEST"

            elif self.state == "SUCCESS":
                pass
            elif self.state == "FAILED":
                pass


# CLOSED
#   ├─ success → stay CLOSED
#   └─ failure_count >= threshold → OPEN

# OPEN
#   └─ timeout_passed → HALF_OPEN

# HALF_OPEN
#   ├─ success → CLOSED
#   └─ failure → OPEN


class CircuitBreaker:
    def __init__(self, name, failure_threshold=3, open_timeout=5):
        self.name = name
        self.failure_threshold = failure_threshold
        self.state = "CLOSED"
        self.failure_count = 0
        self.open_timeout = open_timeout
        self.opened_at = None

    def call_down_stream(self):
        return random.random() < 0.3

    def allow_request(self):
        if self.state == "OPEN":
            if time.time() - self.open_timeout >= self.open_timeout:
                self.state = "HAL_OPEN"
                print(f"[{self.name}]->HALF_OPEN(testing)")
                return True
            return False

    def record_success(self):
        self.failure_count = 0
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
            print(f"[{self.name}]->closed")

    def record_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.opened_at = time.time()
            print(f"[{self.name}]->OPEN")

    def run(self, attempts=10):
        for i in range(attempts):
            print(f"\n[{self.name}] attempt {i}")

            if not self.allow_request():
                print(f"[{self.name}]")
                time.sleep(1)
                continue

            success = self.call_down_stream()
            print(f"[{self.name}] downstream result = {success}")
            if success:
                self.record_success()
            else:
                self.record_failure()
            time.sleep(1)


import time
import random
from concurrent.futures import ThreadPoolExecutor


def payment_service(req_id):
    print(f"[PAYMENT] start req {req_id}")
    time.sleep(3)  # slow service
    print(f"[PAYMENT] done req {req_id}")


def chat_service(req_id):
    print(f"[CHAT] start req {req_id}")
    time.sleep(0.5)
    print(f"[CHAT] done req {req_id}")


payment_pool = ThreadPoolExecutor(max_workers=2)  # bulkhead
chat_pool = ThreadPoolExecutor(max_workers=4)  # bulkhead


def simulate_requests():
    for i in range(6):
        print(f"\nDispatch request {i}")
        payment_pool.submit(payment_service, i)
        chat_pool.submit(chat_service, i)
        time.sleep(0.2)


simulate_requests()
