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

event_queue = PartitionQueue()
notification_queue = PartitionQueue()

rule_engine = RuleEngine()
dispatcher = Dispatcher(notification_queue)
processor = Processor(dispatcher, rule_engine)
ws_manager = WebSocketManager()
manager = Manager(rule_engine, processor, event_queue)


manager.add_rules(Rule("user1", "Apple", 180, Operator.GREATER_THAN))


def generate_rules(num_rules=100):
    rules = []

    for i in range(2, num_rules + 1):
        user_id = f"user{i}"
        rules.append(Rule(user_id, "Tesla", 1000, Operator.GREATER_THAN))
    return rules


for rule in generate_rules(100):
    manager.add_rules(rule)
manager.add_rules(Rule("user101", "Tesla", 200, Operator.LESS_THAN))

Thread(target=start_producer, args=(generate_event, event_queue), daemon=True).start()
Thread(
    target=manager.ensure_consumer,
    args=("Tesla", 5),
    daemon=True,
).start()
Thread(
    target=notification_consumer,
    args=("Tesla", notification_queue, ws_manager),
    daemon=True,
).start()

print("[Main] System running. Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
        # Optional: Print stats
        if int(time.time()) % 10 == 0:  # Every 10 seconds
            print(
                f"[STATS] Event queue: {event_queue.total_size()} | Notification queue: {notification_queue.total_size()}"
            )
except KeyboardInterrupt:
    print("\n[Main] Shutting down...")
