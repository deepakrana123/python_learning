def normalize(text: str) -> str:
    return text.lower().strip()


ACTION_PATTERNS = {
    "send_reminder": [
        "remind",
        "send reminder",
        "notify customer",
        "send notification",
    ],
    "escalate_case": [
        "escalate",
        "raise to manager",
        "send to supervisor",
        "escalation",
    ],
    "assign_senior_officer": [
        "assign senior officer",
        "assign to senior",
        "assign to manager",
    ],
    "close_case": [
        "close case",
        "resolve ticket",
        "close ticket",
    ],
    "reject_loan": [
        "reject loan",
        "reject application",
        "decline loan",
    ],
    "notify_manager": [
        "notify manager",
        "alert manager",
        "inform manager",
    ],
}


TRIGGER_PATTERNS = {
    "loan_requested": [
        "loan request",
        "loan applied",
        "apply loan",
    ],
    "payment_due": [
        "payment due",
        "emi due",
        "due payment",
    ],
    "payment_missed": [
        "missed emi",
        "payment missed",
        "missed payment",
    ],
    "ticket_created": [
        "ticket created",
        "ticket raised",
        "new ticket",
        "issue created",
        "ticket",
        "tickets",
    ],
    "complaint_created": [
        "complaint created",
        "complaint raised",
    ],
    "delivery_failed": [
        "delivery failed",
        "order failed",
    ],
}


def map_action(text: str):
    text = normalize(text)

    for action, patterns in ACTION_PATTERNS.items():
        for pattern in patterns:
            words = pattern.split()
            if all(word in text for word in words):
                return {"action": action, "confidence": 0.95}

    return {"action": None, "confidence": 0.0}


def map_trigger(text: str):
    text = normalize(text)
    for trigger, phrases in TRIGGER_PATTERNS.items():
        for pattern in phrases:
            # if phrase in text:
            #     return {"trigger": trigger, "confidence": 0.90}
            words = pattern.split()
            if all(word in text for word in words):
                return {"trigger": trigger, "confidence": 0.9}
    return {"trigger": None, "confidence": 0.0}


def infer_trigger_from_action(action: str):
    """Single source of truth for action → trigger inference.
    Used by intent_mapper, rule_builder, and orchestrator.
    """
    if action == "send_reminder":
        return "payment_due"

    if action == "escalate_case":
        return "complaint_created"

    if action in ["assign_senior_officer", "close_case"]:
        return "ticket_created"

    if action in ["reject_loan", "notify_manager"]:
        return "loan_requested"

    return None


# def map_intents(text: str):
#     return {
#         "action_result": map_action(text),
#         "trigger_result": map_trigger(text),
#     }


def map_intents(text: str):
    action_result = map_action(text)
    trigger_result = map_trigger(text)
    if trigger_result["trigger"] is None and action_result["action"]:
        trigger_result = {
            "trigger": infer_trigger_from_action(action_result["action"]),
            "confidence": 0.6,
        }

    return {
        "action_result": action_result,
        "trigger_result": trigger_result,
    }
