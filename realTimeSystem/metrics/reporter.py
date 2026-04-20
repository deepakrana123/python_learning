import time
from realTimeSystem.metrics.metrics import metrics


def start_metrics_reporter(event_queue, notif_queue):
    while True:
        time.sleep(5)
        snap = metrics.snapshot(event_queue.total_size(), notif_queue.total_size())
        for k, v in snap.items():
            print(f"{k}: {v}")

        
