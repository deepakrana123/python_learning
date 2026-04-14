from realTimeSystem.ingestion.producer import latest_event_by_stock, latest_lock


def consumer(stock, event_queue, processor):
    while True:
        batch = []
        for _ in range(10):
            key = event_queue.pop(stock)
            if key:
                batch.append(key)
        if batch:
            with latest_lock:
                event = latest_event_by_stock.get(stock)
            if event:
                processor.process(event)
