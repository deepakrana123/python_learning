def build_conditions(extracted: dict):
    conditions = []

    flags = extracted.get("flags", {})
    if flags.get("vip"):
        conditions.append("vip=true")
    if flags.get("premium"):
        conditions.append("premium=true")
    if extracted.get("repeat_count") is not None:
        conditions.append(f"repeat_count>={extracted['repeat_count']}")

    if extracted.get("amount_threshold") is not None:
        conditions.append(f"amount>{extracted['amount_threshold']}")
    return conditions


def build_rule(extracted: dict, mapped: dict):
    """
    Build final workflow rule object
    """

    action = mapped["action_result"]["action"]
    trigger = mapped["trigger_result"]["trigger"]

    rule = {
        "trigger": trigger,
        "conditions": build_conditions(extracted),
        "action": action,
        "delay_days": extracted.get("days"),
    }

    return rule


def apply_defaults(rule: dict):
    """
    Fill missing triggers based on action
    """

    if rule["trigger"] is None:

        if rule["action"] == "send_reminder":
            rule["trigger"] = "payment_due"

        elif rule["action"] == "escalate_case":
            rule["trigger"] = "complaint_created"

    return rule


def build_final_rule(extracted: dict, mapped: dict):
    rule = build_rule(extracted, mapped)
    rule = apply_defaults(rule)
    return rule
