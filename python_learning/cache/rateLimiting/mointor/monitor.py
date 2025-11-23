from collections import defaultdict
import time

rate_limit_monitor = defaultdict(lambda: {"allowed": 0, "blocked": 0})


import logging

logging.basicConfig(filename="ratelimit.log", level=logging.INFO)


def log_request(user_id, allowed, remaining, retry_after):
    status = "ALLOWED" if allowed else "BLOCKED"
    log_line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {status} | user={user_id} | remaining={remaining} | retry_after={retry_after}s"
    logging.info(log_line)
