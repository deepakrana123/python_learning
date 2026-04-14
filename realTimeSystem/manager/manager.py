from realTimeSystem.rule.ruleEngine import RuleEngine
from realTimeSystem.processor.processor import Processor
from realTimeSystem.queues.mainQueue import PartitionQueue
from realTimeSystem.consumer.consumer import consumer
from threading import Thread
from realTimeSystem.model.market import Rule


class Manager:
    def __init__(
        self, ruleEngine: RuleEngine, processor: Processor, event_queue: PartitionQueue
    ):
        self.rule_engine = ruleEngine
        self.processor = processor
        self.event_queue = event_queue
        self.active_consumers = {}

    def add_rules(self, rule: Rule):
        self.rule_engine.add_rule(rule)

    def ensure_consumer(self, stock, count=1):
        if stock not in self.active_consumers:
            self.active_consumers[stock] = 0
            for _ in range(count):
                Thread(
                    target=consumer,
                    args=(stock, self.event_queue, self.processor),
                    daemon=True,
                ).start()
                self.active_consumers[stock] += 1
