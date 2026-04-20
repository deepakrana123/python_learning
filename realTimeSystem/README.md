# RealTimeSystem

A multi-threaded, event-driven system for processing real-time market price events and delivering user notifications via WebSocket based on configurable price rules.

---

## Architecture

```
Producer (ingestion/producer.py)
    │  generates MarketEvent objects, pushes to PartitionQueue
    ▼
PartitionQueue (queues/mainQueue.py)
    │  thread-safe, partitioned by stock symbol
    ▼
Consumer (consumer/consumer.py)  ←── one thread per stock
    │  pops events, passes to Processor
    ▼
Processor (processor/processor.py)
    │  calls RuleEngine.evaluate() → matched rules
    ▼
Dispatcher (disptacher/dispatcher.py)
    │  rate-limits per user, pushes to notification PartitionQueue
    ▼
NotificationQueue (PartitionQueue)
    │
    ▼
NotificationConsumer (consumer/notification_consumer.py)  ←── one thread per stock
    │  sends via WebSocketManager
    ├── success → metrics
    └── failure → RetryQueue
                      │
                      ▼
              RetryWorker (retry_worker.py)
                  │  exponential backoff, max 3 attempts
                  └── exhausted → DLQ
```

**Supporting components:**
- `auto_scaler.py` — monitors queue depth, spawns extra consumer threads when backlog exceeds threshold
- `queues/queueEvication.py` — background worker that evicts expired and overflowed queue items
- `rateLimiter.py` — per-user token bucket, prevents notification spam
- `rule/ruleEngine.py` — stores and evaluates price rules with priority and expiry
- `eventStore/eventStore.py` — thread-safe key-value store for latest event per stock
- `metrics/` — counters, latency tracking, periodic reporter
- `manager/manager.py` — orchestrates consumer thread lifecycle

---

## Data Flow Detail

1. `start_producer()` generates `MarketEvent(stock, price, timestamp)` objects continuously
2. Events are pushed into `PartitionQueue` keyed by stock symbol
3. One `consumer` thread per stock pops events and calls `processor.process(event)`
4. `Processor` evaluates all active rules for that stock via `RuleEngine`
5. Matched rules go to `Dispatcher`, which rate-limits per `user_id` and enqueues notification messages
6. `notification_consumer` threads pop messages and send via `WebSocketManager`
7. Failed sends are pushed to a retry queue; after 3 attempts they go to the dead-letter queue (DLQ)

---


## Running the System

```bash
# Install dependencies
pip install -r requirements.txt

# Run the main entry point
python event_generation.py
```


