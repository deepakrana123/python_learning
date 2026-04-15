import time
from threading import Thread


MAX_WORKERS = 10
QUEUE_THRESHOLD = 3000


def autoscaler(manager, event_queue):
    while True:
        for stock in manager.active_consumer:
            qsize = event_queue.size(stock)
            workers = manager.active_consumers[stock]
            if qsize > QUEUE_THRESHOLD:
                manager.ensure_consumer(stock, 1)
                print(
                    f"[AUTOSCALE] Added worker for {stock}. " f"Workers={workers + 1}"
                )
        time.sleep(5)


def start_autoscaler(manager, event_queue):
    Thread(target=autoscaler, args=(manager, event_queue), daemon=True).start()
