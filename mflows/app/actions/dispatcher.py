from app.actions.handlers import (
    send_reminder,
    approve_loan,
    escalate_ticket,
)


ACTION_MAP = {
    "send_reminder": send_reminder,
    "approve_loan": approve_loan,
    "escalate_ticket": escalate_ticket,
}


def execute_action(action_name: str, payload: dict, config: dict):
    handler = ACTION_MAP.get(action_name)

    if not handler:
        return {"status": "failed", "action": action_name, "reason": "unknown action"}

    return handler(payload, config)
