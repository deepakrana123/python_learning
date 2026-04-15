import time
from realTimeSystem.metrics.metrics import metrics


def start_metrics_reporter():
    while True:
        time.sleep(5)
        report = metrics.snapshot()

        print(
            f"[report] Generated: {report['generated']} | "
            f"Processed: {report['processed']} | "
            f"Notifications Sent: {report['notifications_sent']} | "
            f"Dropped Events: {report['dropped_events']} | "
            f"Rate Limited: {report['rate_limited']} | "
            f"Avg Latency: {report['avg_latency']} | "
            f"report",
        )
