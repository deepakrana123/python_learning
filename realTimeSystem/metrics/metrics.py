import threading
import time
from collections import deque


class Metrics:
    def __init__(self):
        self.lock = threading.Lock()
        self.events_generated = 0
        self.events_processed = 0
        self.notifications_sent = 0
        self.dropped_events = 0
        self.rate_limited = 0
        self.latency_total = 0.0
        self.latency_count = 0.0
        self.max_latency = 0.0
        self.recent_latencies = deque(maxlen=200)
        self.avg_latency = 0
        self.last_time = time.time()
        self.prev_generated = 0
        self.prev_processed = 0
        self.prev_sent = 0
        self.prev_dropped = 0
        self.prev_event_q = 0
        self.prev_notif_q = 0
        self.retry_attempted = 0
        self.retry_success = 0
        self.retry_failed = 0
        self.dlq_count = 0

    def inc(self, field, value=1):
        with self.lock:
            setattr(self, field, getattr(self, field) + value)

    def add_latency(self, seconds):
        with self.lock:
            self.latency_total += seconds
            self.latency_count += 1
            self.max_latency = max(self.max_latency, seconds)
            self.recent_latencies.append(seconds)

    def _p95(self):
        if not self.recent_latencies:
            return 0
        vals = sorted(self.recent_latencies)
        idx = max(0, int(0.95 * len(vals)) - 1)
        return vals[idx]

    def snapshot(self, event_q=0, notif_q=0):
        with self.lock:
            now = time.time()
            elapsed = max(now - self.last_time, 1)
            gen_rate = (self.events_generated - self.prev_generated) / elapsed
            proc_rate = (self.events_processed - self.prev_processed) / elapsed
            sent_rate = (self.notifications_sent - self.prev_sent) / elapsed
            drop_rate = (self.dropped_events - self.prev_dropped) / elapsed

            event_q_growth = (event_q - self.prev_event_q) / elapsed
            notif_q_growth = (notif_q - self.prev_notif_q) / elapsed

            avg = self.latency_total / self.latency_count if self.latency_count else 0

            result = {
                "generated": self.events_generated,
                "processed": self.events_processed,
                "notifications_sent": self.notifications_sent,
                "dropped_events": self.dropped_events,
                # "notification_dropped": self.notification_dropped,
                "rate_limited": self.rate_limited,
                "avg_latency": round(avg, 3),
                "p95_latency": round(self._p95(), 3),
                "max_latency": round(self.max_latency, 3),
                "gen_per_sec": round(gen_rate, 1),
                "proc_per_sec": round(proc_rate, 1),
                "sent_per_sec": round(sent_rate, 1),
                "drop_per_sec": round(drop_rate, 1),
                "event_queue": event_q,
                "notif_queue": notif_q,
                "event_q_growth": round(event_q_growth, 1),
                "notif_q_growth": round(notif_q_growth, 1),
                "retry_attempted": self.retry_attempted,
                "retry_success": self.retry_success,
                "retry_failed": self.retry_failed,
                "dlq_count": self.dlq_count,
            }
            self.last_time = now
            self.prev_generated = self.events_generated
            self.prev_processed = self.events_processed
            self.prev_sent = self.notifications_sent
            self.prev_dropped = self.dropped_events
            self.prev_event_q = event_q
            self.prev_notif_q = notif_q

            return result


metrics = Metrics()
