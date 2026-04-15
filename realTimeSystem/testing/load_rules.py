import random
from realTimeSystem.model.market import Rule, Operator


def generate_rules(num_rules, choices, base_price):
    rules = []

    for i in range(1, num_rules + 1):
        user_id = f"user{i}"
        stock = random.choice(choices)
        price = base_price + random.randint(-100, 100)
        op = random.choice([Operator.GREATER_THAN, Operator.LESS_THAN])
        rules.append(Rule(user_id, stock, price, op))

    return rules


def load_rules(manager, mode="normal"):

    if mode == "normal":
        for rule in generate_rules(100, ["Google", "Amazon", "Apple"], 900):
            manager.add_rules(rule)

    elif mode == "hotspot":
        for rule in generate_rules(1000, ["Tesla"], 800):
            manager.add_rules(rule)

    elif mode == "balanced":
        for rule in generate_rules(
            300, ["Tesla", "Google", "Amazon", "Apple", "Tata"], 900
        ):
            manager.add_rules(rule)

    elif mode == "spam":
        for _ in range(100):
            manager.add_rules(Rule("user1", "Tesla", 800, Operator.GREATER_THAN))

    elif mode == "fanout":
        for i in range(1, 500):
            manager.add_rules(Rule(f"user{i}", "Tesla", 800, Operator.GREATER_THAN))

    else:
        raise ValueError("Unknown mode")
