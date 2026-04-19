import time
from realTimeSystem.metrics.metrics import metrics
import asyncio
import random


def retry_worker(stock, retry_queue, dl_queue, ws_manager):
    while True:
        data = retry_queue.pop(stock)
        if not data:
            time.sleep(0.1)
            continue
        item, ts = data
        msg = item["msg"]
        attempt = item["attempt"]
        try:
            asyncio.run(ws_manager.send(stock, msg))
            metrics.inc("retry_success")
        except Exception:
            metrics.inc("retry_failed")
            if attempt < 3:
                item["attempt"] += 1
                base = 2**attempt  # 1,2,4
                delay = random.uniform(0, base)
                time.sleep(delay)
                retry_queue.push(stock, item, time.time())
                metrics.inc("retry_attempted")
            else:
                dl_queue.push(stock, item, time.time())
                metrics.inc("dlq_count")
