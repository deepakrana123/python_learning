ALLOWED_TRIGGERS = {
    "loan_requested",
    "payment_due",
    "payment_missed",
    "ticket_created",
    "complaint_created",
    "delivery_failed",
}


ALLOWED_ACTIONS = {
    "send_reminder",
    "escalate_case",
    "assign_senior_officer",
    "close_case",
    "reject_loan",
    "notify_manager",
}


def validate_rule(rule: dict):
    errors = []
    if not rule.get("trigger"):
        errors.append("trigger is required")
    if not rule.get("action"):
        errors.append("action is required")

    if rule.get("trigger") and rule["trigger"] not in ALLOWED_TRIGGERS:
        errors.append("invalid trigger")

    if rule.get("action") and rule["action"] not in ALLOWED_ACTIONS:
        errors.append("invalid action")

    delay = rule.get("delay_days")

    if delay is not None:
        if not isinstance(delay, int):
            errors.append("delay_days must be integer")
        elif delay < 0:
            errors.append("delay_days cannot be negative")
        elif delay > 365:
            errors.append("delay_days too large")

    if not isinstance(rule.get("conditions", []), list):
        errors.append("conditions must be list")
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
    }
