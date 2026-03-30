from uuid import uuid4
from ..domain.models import Notification
from collections import defaultdict


class Event:
    def __init__(self, event_type: str, payload: dict):
        self.event_type = event_type
        self.payload = payload


class Action:
    def __init__(self, action: str, payload: dict):
        self.action_type = action
        self.payload = payload


class ConditionEvaluator:
    OPERATORS = {
        ">": lambda a, b: a > b,
        "<": lambda a, b: a < b,
        "==": lambda a, b: a == b,
    }

    def evaluate(self, payload: dict, condition: dict) -> bool:
        field = condition["field"]
        op = condition["operator"]
        value = condition["value"]

        actual = payload.get(field)

        if op not in self.OPERATORS:
            raise Exception(f"unsupported operator")
        return self.OPERATORS[op](actual, value)


class RuleMatcher:
    def __init__(self, condition_evaluator: str):
        self.condition_evaluator = condition_evaluator

    def match(self, event, rule) -> bool:
        if event.event_type != rule["event_type"]:
            return False
        for condition in rule["conditions"]:
            if not self.condition_evaluator.evaluate(event.payload, condition):
                return False
        return True


class RuleEngine:
    def __init__(self, rules: list):
        self.rule_index = defaultdict(list)
        for rule in rules:
            self.rule_index[rule["event"]].append(rule)
        self.conditon_evaluator = ConditionEvaluator()
        self.rule_matcher = RuleMatcher(self.conditon_evaluator)

    def process(self, event: Event):
        actions = []
        for rule in self.rule_index.get(event.event_type, []):
            if self.rule_matcher.match(event, rule):
                actions.extend(self._generate_actions(rule, event))
        return actions

    def _generate_actions(self, rule, event):
        actions = []
        for action_cfg in rule["actions"]:
            action_payload = {**action_cfg, "event_payload": event}
            actions.append(Action(action_cfg["type"], action_payload))
        return actions


class ActionMapper:
    def to_notification(self, action):
        payload = action.payload

        return Notification(
            id=uuid4(),
            user_id=payload.get("user_id"),
            template_id=payload.get("template"),
            channels=[payload.get("channel")],
            data=payload.get("event_payload"),
        )
