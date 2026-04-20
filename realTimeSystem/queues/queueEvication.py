from realTimeSystem.model.market import companies
import time
from realTimeSystem.metrics.metrics import metrics

def evict_expire(queue, stock, ttl):

    while True:
        now = time.time()
        front = queue.peek(stock)
        if front is None:
            break
        payload, ts = front
        if now - ts > ttl:
            queue.pop(stock)  
            metrics.inc("expired_count")
        else:
            break


def evict_overflow(queue, stock, max_size):

    while queue.size(stock) > max_size:
        queue.pop(stock)
        metrics.inc("evicted_count")


def queue_maintenance_worker(app):
    while True:
        for stock in companies:
            evict_expire(app["event_queue"], stock, ttl=10)
            evict_overflow(app["event_queue"], stock, max_size=5000)
            evict_expire(app["notification_queue"], stock, ttl=30)
         time.sleep(2)
