from realTimeSystem.disptacher.dispatcher import Dispatcher
from realTimeSystem.rule.ruleEngine import RuleEngine
from realTimeSystem.model.market import MarketEvent


class Processor:
    def __init__(self, dispatch: Dispatcher, ruleEngine: RuleEngine):
        self.dispatcher = dispatch
        self.rule_engine = ruleEngine

    def process(self, event: MarketEvent) -> None:
        matched_rules = self.rule_engine.evaluate(event.stock, event.price)
        self.dispatcher.disptach(event, matched_rules)
