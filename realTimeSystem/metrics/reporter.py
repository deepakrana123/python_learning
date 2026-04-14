import time
from realTimeSystem.metrics.metrics import metrics


def start_metrics_reporter():
    while True:
        time.sleep(5)
        generated, processed, notified = metrics.snapshot()

        print(
            f"[METRICS] Generated: {generated} | "
            f"Processed: {processed} | "
            f"Notifications: {notified}"
        )
