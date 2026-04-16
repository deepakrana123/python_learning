from realTimeSystem.model.market import companies
import time
from realTimeSystem.metrics.metrics import metrics


def evict_expire(queue, stock, ttl):

    while True:
        items, ts = queue.pop(stock)
        now = time.now()
        if not items:
            break

        payload, ts = items
        if now - ts > ttl:
            metrics.inc("expired_count")
            continue
        queue.push(stock, payload, ts)
        break


def evict_overflow(queue, stock, max_size):
    events = queue[stock]
    if events is None:
        return []
    while events.size(stock) > max_size:
        events.pop()
        metrics.inc("evicted_count")


def queue_maintenance_worker(app):
    while True:
        for stock in companies:
            evict_expire(app["event_queue"], stock)
            evict_overflow(app["event_queue"], stock, max_size=5000)
            evict_expire(app["notification_queue"], stock)
        time.sleep(2)
