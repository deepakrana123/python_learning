from app.execution.actions import (
    send_reminder,
    escalate_case,
    assign_senior_officer,
    fail_randomly,
)

ACTION_MAP = {
    "send_reminder": send_reminder,
    "escalate_case": escalate_case,
    "assign_senior_officer": assign_senior_officer,
    "fail_randomly": fail_randomly,
}


def execute_action(action_name: str, payload: dict, config: dict):
    handler = ACTION_MAP.get(action_name)
    print(handler, "handler hello")
    if not handler:
        return {"status": "failed", "action": action_name, "reason": "unknown action"}

    return handler(payload, config)
