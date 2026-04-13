import time
import random
from typing import Callable
from marketEvent import Rule, Operator
from mainQueue import SimpleQueue, PartitionQueue
from ruleEngine import RuleEngine
from dataclasses import dataclass
from threading import Thread


MAX_PER_STOCK = 5000
GLOBAL_LIMIT = 20000


@dataclass(frozen=True)
class MarketEvent:
    stock: str
    price: float
    timestamp: float

    def __str__(self):
        return f"{self.stock} (Price:{self.price}) {self.timestamp}"

    def __repr__(self):
        return f"Stock(stock={self.stock}) ,price={self.price} , timestamp={self.timestamp}"


companies = [
    ("Apple", 175.50),
    ("Microsoft", 420.75),
    ("Google", 140.25),
    ("Amazon", 185.30),
    ("Tesla", 245.80),
    ("Meta", 330.60),
    ("Netflix", 485.90),
    ("Nvidia", 895.40),
    ("Tata", 815.40),
    ("Adani", 89.40),
]


# class EventIngestions:
last_price_stock = {}


def generate_event():
    stock_name, price = random.choice(companies)
    base_price = last_price_stock.get(stock_name, price)
    new_price = base_price + random.uniform(-20, 20)
    last_price_stock[stock_name] = new_price
    timestamp = time.time()
    return MarketEvent("Tesla", new_price, timestamp)


def start_producer(generate_event: Callable, event_queue) -> None:
    while True:
        event = generate_event()
        stock = event.stock
        if event_queue.size(stock) > MAX_PER_STOCK:
            print(f"[BACKPRESSURE] Skipping {stock}")
            continue
        if event_queue.total_size() > GLOBAL_LIMIT:
            print("[GLOBAL BACKPRESSURE] slowing producer")
            time.sleep(0.05)
            continue

        event_queue.push(stock, event)
        print(f"[Producer] Generated:{event}", event_queue.total_size())
        time.sleep(0.01)


class Dispatcher:
    def __init__(self, notification_queue: PartitionQueue):
        self.notification_queue = notification_queue

    def disptach(self, event, after_matched):
        print(f"Matched rules: {len(after_matched)}")
        if len(after_matched) > 100:
            after_matched = after_matched[:50]
        for rule in after_matched:
            message = f"Alret {event.stock} crossed {rule.target_price}"
            print(self.notification_queue.total_size(), "notify queue")
            if self.notification_queue.size(event.stock) > 10000:
                return
            self.notification_queue.push(event.stock, message)


class Processor:
    def __init__(self, dispatch: Dispatcher, ruleEngine: RuleEngine):
        self.dispatcher = dispatch
        self.rule_engine = ruleEngine

    def process(self, event: MarketEvent) -> None:
        matched_rules = self.rule_engine.evaluate(event.stock, event.price)
        self.dispatcher.disptach(event, matched_rules)


def notification_consumer(stock, notification_queue):
    while True:
        msg = notification_queue.pop(stock)
        if msg:
            print(f"[Notify--{stock}] {msg}")
            time.sleep(2)


def consumer(stock, event_queue, processor):
    while True:
        event = event_queue.pop(stock)
        if event:
            print(f"[Consumer --{stock}] Processing {event}")
            processor.process(event)


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


event_queue = PartitionQueue()
notification_queue = PartitionQueue()

rule_engine = RuleEngine()
dispatcher = Dispatcher(notification_queue)
processor = Processor(dispatcher, rule_engine)

manager = Manager(rule_engine, processor, event_queue)


manager.add_rules(Rule("user1", "Apple", 180, Operator.GREATER_THAN))


def generate_rules(num_rules=100, min_price=180, max_price=220):
    rules = []

    for i in range(2, num_rules + 1):
        user_id = f"user{i}"
        rules.append(Rule(user_id, "Tesla", 1000, Operator.GREATER_THAN))
    return rules


for rule in generate_rules(100):
    manager.add_rules(rule)
manager.add_rules(Rule("user101", "Tesla", 200, Operator.LESS_THAN))

Thread(target=start_producer, args=(generate_event, event_queue), daemon=True).start()
Thread(target=manager.ensure_consumer, args=("Tesla", 5), daemon=True).start()
Thread(
    target=notification_consumer, args=("Tesla", notification_queue), daemon=True
).start()

while True:
    time.sleep(1)
