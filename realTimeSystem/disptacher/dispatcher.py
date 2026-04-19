from realTimeSystem.queues.mainQueue import PartitionQueue
from realTimeSystem.rateLimiter import RateLimiter
from realTimeSystem.model.market import (
    MAX_NOTIFICATIONS_PER_EVENT,
    MAX_NOTIFICATION_QUEUE_SIZE,
)


class Dispatcher:
    def __init__(self, notification_queue: PartitionQueue, rate_limiter: RateLimiter):
        self.notification_queue = notification_queue
        self.rate_limiter = rate_limiter

    def disptach(self, event, after_matched):
        if not after_matched:
            return
        if len(after_matched) > 100:
            after_matched = after_matched[:MAX_NOTIFICATIONS_PER_EVENT]
        for rule in after_matched:
            if not self.rate_limiter.allow(rule.user_id):
                continue
            message = f"Alret {event.stock} crossed {rule.target_price}"
            if self.notification_queue.size(event.stock) > MAX_NOTIFICATION_QUEUE_SIZE:
                return
            self.notification_queue.push(event.stock, message, event.timestamp)
