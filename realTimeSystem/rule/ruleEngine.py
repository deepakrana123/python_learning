import threading
from typing import List, Dict
from collections import defaultdict
from realTimeSystem.model.market import Rule


class RuleEngine:
    def __init__(self):
        self.rules_by_stock: Dict[str, List[Rule]] = defaultdict(list)
        self.lock = threading.Lock()

    def add_rule(self, rule: Rule) -> None:
        # ─────────────────────────────────────────────
        # PREVIOUS CODE:
        # if not rule.stock:
        #     return ValueError("stock is not in market")   ← BUG: `return` not `raise`.
        # if rule.target_price <= 0:                          Returns the exception object as a value
        #     return ValueError("Price cannot be in negative") and exits the function silently.
        #                                                       The caller gets None back, no error raised.
        #                                                       Invalid rules are accepted into the engine.
        if not rule.stock:
            raise ValueError("stock is not in market")
        if rule.target_price <= 0:
            raise ValueError("Price cannot be in negative")
        with self.lock:
            self.rules_by_stock[rule.stock].append(rule)

    def get_rule(self, stock: str) -> List[Rule]:

        with self.lock:
            rules = self.rules_by_stock.get(stock, [])
            active_rules = [rule for rule in rules if rule.is_active()]
            active_rules.sort(key=lambda r: r.priority, reverse=True)
            return active_rules

    def evaluate(self, stock: str, price: float) -> List[Rule]:
        matched = []
        rules = self.get_rule(stock)
        for rule in rules:
            if rule.matches(price):
                matched.append(rule)
        return matched

    def cleanup(self):
        with self.lock:
            for stock in list(self.rules_by_stock.keys()):
                rules = self.rules_by_stock[stock]
                self.rules_by_stock[stock] = [r for r in rules if r.is_active()]
                if not self.rules_by_stock[stock]:
                    del self.rules_by_stock[stock]


import time
import threading


def start_cleanup_worker(engine: RuleEngine, interval: int = 60):
    def run():
        while True:
            engine.cleanup()
            time.sleep(interval)

    threading.Thread(target=run, daemon=True).start()
