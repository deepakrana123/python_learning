def normalize(text: str) -> str:
    return text.lower().strip()


ACTION_PATTERNS = {
    "send_reminder": [
        "send reminder",
        "notify customer",
        "remind customer",
    ],
    "escalate_case": [
        "escalate",
        "raise to manager",
        "send to supervisor",
    ],
    "assign_senior_officer": [
        "assign senior officer",
        "assign to senior",
    ],
    "close_case": [
        "close case",
        "resolve ticket",
    ],
}

TRIGGER_PATTERNS = {
    "complaint_created": [
        "complaint",
        "ticket raised",
    ],
    "payment_due": [
        "payment due",
        "emi due",
    ],
    "payment_missed": [
        "missed emi",
        "payment missed",
    ],
}


def map_action(text: str):
    text = normalize(text)
    for action, phrases in ACTION_PATTERNS.items():
        for phrase in phrases:
            if phrase in text:
                return {"action": action, "confidence": 0.95}
    return {"action": None, "confidence": 0.0}


def map_trigger(text: str):
    text = normalize(text)
    for trigger, phrases in TRIGGER_PATTERNS.items():
        for phrase in phrases:
            if phrase in text:
                return {"trigger": trigger, "confidence": 0.90}
    return {"trigger": None, "confidence": 0.0}


def map_intents(text: str):
    return {"action_result": map_action(text), "trigger_reuslt": map_trigger(text)}
