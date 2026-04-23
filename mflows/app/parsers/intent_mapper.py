def normailze(text: str) -> str:
    return text.lower().strip()


ACTIONS_PATTERNS = {
    "send_reminder": [
        "send reminder",
        "notify customer",
        "remind customer",
        "issue reminder",
        "send notification",
    ],
    "escalate_case": [
        "escalate",
        "raise to manager",
        "send to supervisor",
        "escalate case",
    ],
    "assign_senior_officer": [
        "assign senior officer",
        "assign to senior",
        "route to senior agent",
        "assign manager",
    ],
    "close_case": ["close case", "resolve ticket", "mark resolved", "close complaint"],
}
TRIGGER_PATTERNS = {
    "complaint_created": ["complaint", "ticket raised"],
    "payment_due": ["payment due", "emi due", "loan due"],
    "payment_missed": ["missed emi", "payment missed", "defaulted payment"],
}


def map_action(text: str):
    text = normailze(text)
    for action, phrases in ACTIONS_PATTERNS.items():
        print(action, phrases)
        for phrase in phrases:
            if phrase in text:
                return {"action": action, "confidence": 0.95}
    return {"action": None, "confidence": 0.0}


def map_trigger(text: str):
    text = normailze(text)
    for trigger, pharses in TRIGGER_PATTERNS.items():
        for pharse in pharses:
            if pharse in text:
                return {"trigger": trigger, "confidence": 0.90}
    return {"trigger": None, "confidence": 0.0}


def map_intents(text: str):
    return {"action_result": map_action(text), "trigger_result": map_trigger(text)}
