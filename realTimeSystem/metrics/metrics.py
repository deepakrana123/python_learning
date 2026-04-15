import threading


class Metrics:
    def __init__(self):
        self.lock = threading.Lock()
        self.events_generated = 0
        self.events_processed = 0
        self.notifications_sent = 0
        self.dropped_events = 0
        self.rate_limited = 0

        self.latency_total = 0
        self.latency_count = 0
        self.avg_latency = 0

    def inc(self, field, value=1):
        with self.lock:
            setattr(self, field, getattr(self, field) + value)

    # def inc_generated(self):
    #     with self.lock:
    #         self.events_generated += 1

    # def inc_processed(self):
    #     with self.lock:
    #         self.events_processed += 1

    # def inc_notifications_sent(self):
    #     with self.lock:
    #         self.notifications_sent += 1

    def add_latency(self, seconds):
        with self.lock:
            self.avg_latency = (
                self.latency_total / self.self.latency_count
                if self.latency_count
                else 0
            )

    def snapshot(self):
        with self.lock:
            return {
                "generated": self.events_generated,
                "processed": self.events_processed,
                "notifications_sent": self.notifications_sent,
                "dropped_events": self.dropped_events,
                "rate_limited": self.rate_limited,
                "avg_latency": round(self.avg_latency, 3),
            }


metrics = Metrics()
