import asyncio
from realTimeSystem.metrics.metrics import metrics
import time
from realTimeSystem.metrics.metrics import metrics


def notification_consumer(stock, notification_queue, ws_manager):
    while True:
        data = notification_queue.pop(stock)
        if not data:
            continue
        msg, timestamp = data
        now = time.time()
        latency = now - timestamp
        metrics.add_latency(latency)
        if msg:
            print(f"[Notify--{stock}] {msg}")
            asyncio.run(ws_manager.send(stock, msg))
            metrics.inc("notifications_sent")
