import asyncio
from realTimeSystem.metrics.metrics import metrics
import time


def notification_consumer(stock, notification_queue, ws_manager, retry_queue):
    # WHY one loop per thread: same reasoning as retry_worker —
    # asyncio.run() creates/destroys a loop on every call. Reuse one loop instead.
    loop = asyncio.new_event_loop()
    while True:
        # ─────────────────────────────────────────────
        # PREVIOUS CODE:
        # data = notification_queue.pop(stock)
        # time.sleep(3)                ← BUG: sleep(3) runs BEFORE the empty check.
        # if not data:                   Every iteration waits 3 seconds regardless of
        #     time.sleep(0.1)            whether there's data. Max throughput = 1 msg / 3s.
        #     continue                   The 0.1s sleep after the check is also redundant —
        #                                pop() already has a built-in timeout.
        data = notification_queue.pop(stock)
        if not data:
            continue
        try:
            msg, timestamp = data
            now = time.time()
            latency = now - timestamp
            metrics.add_latency(latency)
            loop.run_until_complete(ws_manager.send(stock, msg))
            metrics.inc("notifications_sent")
        except Exception:
            payload = {"stock": stock, "msg": msg, "attempt": 1}
            retry_queue.push(stock, payload, time.time())


# ─────────────────────────────────────────────
# PREVIOUS CODE:
#
# def run_consumer_in_thread(stock, notification_queue, ws_manager, retry_queue):
#     async def _run():
#         await notification_consumer(...)   ← BUG: notification_consumer is a plain sync function,
#     asyncio.run(_run())                      not a coroutine. You can't `await` it.
#                                              This raises TypeError immediately.
#                                              The wrapper is unnecessary — just call the sync
#                                              function directly in a Thread.
#
# Removed entirely. Callers should use:
#   Thread(target=notification_consumer, args=(...), daemon=True).start()
