from threading import Thread
from realTimeSystem.queues.mainQueue import PartitionQueue
from realTimeSystem.rule.ruleEngine import RuleEngine
from realTimeSystem.disptacher.dispatcher import Dispatcher
from realTimeSystem.processor.processor import Processor
from realTimeSystem.manager.manager import Manager
from realTimeSystem.model.market import Rule, Operator
import time
from realTimeSystem.ingestion.producer import generate_event, start_producer
from realTimeSystem.consumer.notification_consumer import notification_consumer
from realTimeSystem.web_socket_manager import WebSocketManager
from realTimeSystem.metrics.reporter import start_metrics_reporter
from realTimeSystem.rateLimiter import RateLimiter
import random

event_queue = PartitionQueue()
notification_queue = PartitionQueue()

rule_engine = RuleEngine()

ws_manager = WebSocketManager()
rate_limiter = RateLimiter(interval=1)
dispatcher = Dispatcher(notification_queue, rate_limiter)
processor = Processor(dispatcher, rule_engine)
manager = Manager(rule_engine, processor, event_queue)


def generate_rules(num_rules, choices, price):
    rules = []
    for i in range(1, num_rules + 1):
        user_id = f"user{i}"
        stock_name = random.choice(choices)
        price = price + random.randint(-100, 100)
        operator = random.choice([Operator.GREATER_THAN, Operator.LESS_THAN])
        rules.append(Rule(user_id, stock_name, price, operator))
    return rules


for rule in generate_rules(50, ["Google", "Amazon", "Apple"], 900):
    manager.add_rules(rule)
for rule in generate_rules(100, ["Tesla"], 800):
    manager.add_rules(rule)

for rule in [
    Rule("user1", "Google", 900, Operator.LESS_THAN),
    Rule("user1", "Amazon", 900, Operator.GREATER_THAN),
    Rule("user1", "Amazon", 900, Operator.GREATER_THAN),
    Rule("user1", "Apple", 900, Operator.GREATER_THAN),
    Rule("user1", "Apple", 900, Operator.GREATER_THAN),
    Rule("user1", "Apple", 900, Operator.GREATER_THAN),
    Rule("user1", "Tata", 900, Operator.GREATER_THAN),
    Rule("user1", "Nvidia", 900, Operator.GREATER_THAN),
    Rule("user1", "Microsoft", 900, Operator.GREATER_THAN),
    Rule("user1", "Google", 900, Operator.GREATER_THAN),
    Rule("user1", "Adani", 900, Operator.GREATER_THAN),
    Rule("user1", "Adani", 900, Operator.GREATER_THAN),
    Rule("user1", "Amazon", 900, Operator.GREATER_THAN),
]:
    manager.add_rules(rule)


Thread(target=start_producer, args=(generate_event, event_queue), daemon=True).start()
Thread(
    target=manager.ensure_consumer,
    args=("Tesla", 1),
    daemon=True,
).start()
Thread(
    target=notification_consumer,
    args=("Tesla", notification_queue, ws_manager),
    daemon=True,
).start()
Thread(
    target=manager.ensure_consumer,
    args=("Google", 2),
    daemon=True,
).start()
Thread(
    target=notification_consumer,
    args=("Google", notification_queue, ws_manager),
    daemon=True,
).start()
Thread(
    target=manager.ensure_consumer,
    args=("Amazon", 1),
    daemon=True,
).start()
Thread(
    target=notification_consumer,
    args=("Amazon", notification_queue, ws_manager),
    daemon=True,
).start()
Thread(
    target=manager.ensure_consumer,
    args=("Apple", 3),
    daemon=True,
).start()
Thread(
    target=notification_consumer,
    args=("Apple", notification_queue, ws_manager),
    daemon=True,
).start()
Thread(
    target=manager.ensure_consumer,
    args=("Tata", 3),
    daemon=True,
).start()
Thread(
    target=notification_consumer,
    args=("Tata", notification_queue, ws_manager),
    daemon=True,
).start()

Thread(
    target=start_metrics_reporter,
    daemon=True,
).start()

try:
    while True:
        time.sleep(10)
        print(
            f"[STATS] Event queue: {event_queue.total_size()} | Notification queue: {notification_queue.total_size()}"
        )
except KeyboardInterrupt:
    print("\n[Main] Shutting down...")
