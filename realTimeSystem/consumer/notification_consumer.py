import asyncio
from realTimeSystem.metrics.metrics import metrics
import time


def notification_consumer(stock, notification_queue, ws_manager, retry_queue):
    while True:
        data = notification_queue.pop(stock)
        if not data:
            time.sleep(0.1)
            continue
        try:
            msg, timestamp = data
            now = time.time()
            latency = now - timestamp
            metrics.add_latency(latency)
            asyncio.run(ws_manager.send(stock, msg))
            metrics.inc("notifications_sent")
        except Exception:
            payload = {"stock": stock, "msg": msg, "attempt": 1}
            retry_queue.push(stock, payload, time.time())


def run_consumer_in_thread(stock, notification_queue, ws_manager, retry_queue):
    async def _run():
        await notification_consumer(stock, notification_queue, ws_manager, retry_queue)

    asyncio.run(_run())
