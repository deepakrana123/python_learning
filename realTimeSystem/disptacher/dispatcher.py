from realTimeSystem.queue.mainQueue import PartitionQueue


class Dispatcher:
    def __init__(self, notification_queue: PartitionQueue):
        self.notification_queue = notification_queue

    def disptach(self, event, after_matched):
        print(f"Matched rules: {len(after_matched)}")
        if len(after_matched) > 100:
            after_matched = after_matched[:50]
        for rule in after_matched:
            message = f"Alret {event.stock} crossed {rule.target_price}"
            print(self.notification_queue.total_size(), "notify queue")
            if self.notification_queue.size(event.stock) > 10000:
                return
            self.notification_queue.push(event.stock, message)
