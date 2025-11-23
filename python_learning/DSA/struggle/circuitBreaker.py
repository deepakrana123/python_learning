import time
import random


class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_time=5):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failure_count = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF-OPEN
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            # Check if cooldown is over
            if time.time() - self.last_failure_time > self.recovery_time:
                self.state = "HALF-OPEN"
            else:
                raise Exception("Circuit is OPEN. Failing fast.")

        try:
            result = func(*args, **kwargs)
            # Success → reset breaker
            self.failure_count = 0
            self.state = "CLOSED"
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
            raise e


# ------------------- Demo -------------------
# Fake service that fails randomly
def flaky_service():
    if random.random() < 0.7:
        raise Exception("Service failed!")
    return "Service success!"


cb = CircuitBreaker(failure_threshold=3, recovery_time=4)

for i in range(15):
    try:
        print(f"Call {i+1}: {cb.call(flaky_service)} | State={cb.state}")
    except Exception as e:
        print(f"Call {i+1} failed: {e} | State={cb.state}")
    time.sleep(1)
