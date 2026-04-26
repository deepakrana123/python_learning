def build_conditions(extracted: dict):
    conditions = []
    flags = extracted.get("flags", {})

    if flags.get("vip"):
        conditions.append("vip=true")

    if flags.get("premium"):
        conditions.append("premium")

    if extracted.get("repeat_count") is not None:
        conditions.append(f"repeat_count>={extracted['repeat_count']}")

    if extracted.get("amount_threshold") is not None:
        conditions.append(f"amount>{extracted['amount_threshold']}")

    return conditions


def apply_defaults(rule: dict):
    if rule["trigger"] is None:
        if rule["action"] == "send_reminder":
            rule["trigger"] = "payment_due"

        elif rule["action"] == "escalate_case":
            rule["trigger"] = "complaint_created"
    return rule


def build_final_rule(extracted: dict, mapped: dict):
    rule = {
        "trigger": mapped["trigger_result"]["trigger"],
        "action": mapped["action_result"]["action"],
        "conditions": build_conditions(extracted),
        "delay_days": extracted.get("days"),
    }

    return apply_defaults(rule)
