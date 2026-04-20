import time
from realTimeSystem.metrics.metrics import metrics
import asyncio
import random


# ─────────────────────────────────────────────
# PREVIOUS CODE — asyncio.run() misuse:
#
# def retry_worker(stock, retry_queue, dl_queue, ws_manager):
#     while True:
#         ...
#         try:
#             asyncio.run(ws_manager.send(stock, msg))   ← BUG: asyncio.run() creates a brand-new
#                                                           event loop on every single call, then tears
#                                                           it down. In a tight retry loop this is:
#                                                           1. Expensive — loop creation has overhead
#                                                           2. Unsafe — if ws_manager internally holds
#                                                              any async state (like open connections),
#                                                              it gets orphaned when the loop closes.
#                                                           3. Not reentrant — if called from within
#                                                              an already-running loop it raises RuntimeError.
#
# FIX: Create one event loop per worker thread and reuse it for all sends.
# WHY loop.run_until_complete() instead of asyncio.run():
# run_until_complete() runs a coroutine on an EXISTING loop without creating/destroying it.
# The loop lives for the lifetime of this worker thread — clean, efficient, safe.


def retry_worker(stock, retry_queue, dl_queue, ws_manager):
    loop = asyncio.new_event_loop()  
    while True:
        data = retry_queue.pop(stock)
        if not data:
            time.sleep(0.1)
            continue
        item, ts = data
        msg = item["msg"]
        attempt = item["attempt"]
        try:
            loop.run_until_complete(ws_manager.send(stock, msg))
            metrics.inc("retry_success")
        except Exception:
            metrics.inc("retry_failed")
            if attempt < 3:
                item["attempt"] += 1
                base = 2**attempt  
                delay = random.uniform(0, base)
                time.sleep(delay)
                retry_queue.push(stock, item, time.time())
                metrics.inc("retry_attempted")
            else:
                dl_queue.push(stock, item, time.time())
                metrics.inc("dlq_count")
