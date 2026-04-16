import time
from realTimeSystem.metrics.metrics import metrics


def retry_worker(stock, retry_queue, dl_queue, ws_manager):
    while True:

        data = retry_queue.pop(stock)
        if not data:
            continue
        item, ts = data
        msg = item["msg"]
        attempt = item["attempt"]
        try:
            ws_manager.send(stock, msg)
            metrics.inc("retry_success")
        except Exception:
            if attempt < 3:
                item["attempt"] += 1
                time.sleep(1)
                retry_queue.push(stock, item, time.time())
                metrics.inc("retry_attempted")
            else:
                dl_queue.push(stock, item, time.time())
                metrics.inc("dlq_count")
