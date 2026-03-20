import time
import random


class RetryFSM:
    def __init__(self, name, max_retries=3, base_delay=1.0):
        self.name = name
        self.state = "IDLE"
        self.retries = 0
        self.max_retries = max_retries
        self.base_delay = base_delay

    def make_request(self):
        # 30% success rate
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
                jitter = random.uniform(0, 0.5)
                delay = backoff + jitter

                print(f"[{self.name}] retry #{self.retries}, " f"sleep {delay:.2f}s")
                time.sleep(delay)
                self.state = "REQUEST"

            elif self.state == "SUCCESS":
                print(f"[{self.name}] SUCCESS 🎯")
                break

            elif self.state == "FAILED":
                print(f"[{self.name}] FAILED ❌")
                break


# fsm = RetryFSM("A", max_retries=3, base_delay=1)
# fsm.run()
# fsm1 = RetryFSM("B", max_retries=3, base_delay=1)
# fsm1.run()
# fsm2 = RetryFSM("C", max_retries=4, base_delay=1)
# fsm2.run()

import time
import random


class CircuitBreaker:
    def __init__(self, name, failure_threshold=3, open_timeout=5):
        self.name = name
        self.state = "CLOSED"
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.open_timeout = open_timeout
        self.opened_at = None

    def call_downstream(self):
        # Simulate flaky service (30% success)
        return random.random() < 0.3

    def allow_request(self):
        if self.state == "OPEN":
            if time.time() - self.opened_at >= self.open_timeout:
                self.state = "HALF_OPEN"
                print(f"[{self.name}] → HALF_OPEN (testing)")
                return True
            return False
        return True

    def record_success(self):
        self.failure_count = 0
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
            print(f"[{self.name}] → CLOSED (recovered)")

    def record_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.opened_at = time.time()
            print(f"[{self.name}] → OPEN (circuit tripped)")

    def run(self, attempts=10):
        for i in range(attempts):
            print(f"\n[{self.name}] Attempt {i+1}, STATE={self.state}")

            if not self.allow_request():
                print(f"[{self.name}] fast-fail (circuit open)")
                time.sleep(1)
                continue

            success = self.call_downstream()
            print(f"[{self.name}] downstream result = {success}")

            if success:
                self.record_success()
            else:
                self.record_failure()

            time.sleep(1)


# cb = CircuitBreaker("Service-B", failure_threshold=3, open_timeout=5)
# cb.run(attempts=15)

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
