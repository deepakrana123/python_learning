from threading import Thread
from realTimeSystem.queues.mainQueue import PartitionQueue
from realTimeSystem.rule.ruleEngine import RuleEngine
from realTimeSystem.disptacher.dispatcher import Dispatcher
from realTimeSystem.processor.processor import Processor
from realTimeSystem.manager.manager import Manager
from realTimeSystem.ingestion.producer import generate_event, start_producer
from realTimeSystem.consumer.notification_consumer import (
    notification_consumer,
)
from realTimeSystem.web_socket_manager import WebSocketManager
from realTimeSystem.metrics.reporter import start_metrics_reporter
from realTimeSystem.rateLimiter import RateLimiter
from realTimeSystem.testing.load_rules import load_rules
from realTimeSystem.retry_worker import retry_worker
from realTimeSystem.model.market import companies
import time

app = {}


def build_system():
    event_queue = PartitionQueue()
    notification_queue = PartitionQueue()
    retry_queue = PartitionQueue()
    dlq_queue = PartitionQueue()
    rule_engine = RuleEngine()
    ws_manager = WebSocketManager()
    rate_limiter = RateLimiter(interval=1)
    dispatcher = Dispatcher(notification_queue, rate_limiter)
    processor = Processor(dispatcher, rule_engine)
    manager = Manager(rule_engine, processor, event_queue)
    app["event_queue"] = event_queue
    app["notification_queue"] = notification_queue
    app["rule_engine"] = rule_engine
    app["ws_manager"] = ws_manager
    app["manager"] = manager
    app["retry_queue"] = retry_queue
    app["dlq_queue"] = dlq_queue


def load_rules_mode(mode):
    load_rules(app["manager"], mode=mode)


def retry_thread():
    for value in companies:
        Thread(
            target=retry_worker,
            args=(value, app["retry_queue"], app["dlq_queue"], app["ws_manager"]),
            daemon=True,
        ).start()


def starts():
    for _ in range(20):
        Thread(
            target=start_producer,
            args=(generate_event, app["event_queue"]),
            daemon=True,
        ).start()


def start_services():
    starts()
    retry_thread()

    Thread(
        target=start_metrics_reporter,
        args=(app["event_queue"], app["notification_queue"]),
        daemon=True,
    ).start()


def start_workers():
    worker_map = {}
    for value in companies:
        worker_map[value] = worker_map.get(value, 0) + 1
    for stock, count in worker_map.items():
        app["manager"].ensure_consumer(stock, count)
        Thread(
            target=notification_consumer,
            args=(
                stock,
                app["notification_queue"],
                app["ws_manager"],
                app["retry_queue"],
            ),
            daemon=True,
        ).start()


def run_forever():
    try:
        while True:
            time.sleep(10)
            eq = app["event_queue"].total_size()
            nq = app["notification_queue"].total_size()
            # for stock in companies:
            #     print(f"[starts] event queue {stock}={app["event_queue"].size(stock)}")
            print(f"[STATS] Event Queue={eq} | Notify Queue={nq}")
    except KeyboardInterrupt:
        print("Shutting down...")


if __name__ == "__main__":
    build_system()
    load_rules_mode("hotspot")
    start_services()
    start_workers()
    run_forever()
