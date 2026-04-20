from realTimeSystem.ingestion.producer import latest_event_by_stock, latest_lock
import time


def consumer(stock, event_queue, processor):
    # ─────────────────────────────────────────────
    # PREVIOUS CODE:
    #
    # while True:
    #     batch = []
    #     for _ in range(10):
    #         key = event_queue.pop(stock)
    #         if key:
    #             batch.append(key)
    #     if batch:
    #         with latest_lock:
    #             event = latest_event_by_stock.get(stock)   ← BUG: pops up to 10 events from the queue
    #         if event:                                         but then only processes the SINGLE latest
    #             processor.process(event)                      event from latest_event_by_stock.
    #             time.sleep(1)                                 The 10 popped items are thrown away.
    #                                                           90% of events silently dropped.
    #                                                           Also sleep(1) inside the hot path
    #                                                           caps throughput to 1 event/sec per worker.
    #
    # WHY the fix works:
    # Each item popped from the queue IS the event object (after fixing producer.py).
    # We process each one directly — no need to look up latest_event_by_stock at all.
    # latest_event_by_stock is only needed by components that don't have queue access.
    while True:
        item = event_queue.pop(stock)
        if not item:
            continue
        event, _ = item  # item is (event, timestamp) tuple from PartitionQueue
        processor.process(event)
