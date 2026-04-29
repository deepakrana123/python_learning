import time
import random


def with_retry(fn, retries=3, base_delay=1, max_delay=8):
    last_result = None
    for attempt in range(retries):
        result = fn()
        if result["success"]:
            result["retries_used"] = attempt
            return result
        last_result = result
        error_text = str(result.get("error", "")).lower()
        retryable = any(
            word in error_text
            for word in ["timeout", "429", "500", "502", "503", "connection"]
        )
        if not retryable:
            result["retries_used"] = attempt
            return result
        if attempt < retries - 1:
            delay = min(base_delay * (2**attempt), max_delay)
            jitter = random.uniform(0, 0.5)
            time.sleep(delay + jitter)
    print(retries, "hlo retries")
    last_result["retries_used"] = retries
    return last_result
