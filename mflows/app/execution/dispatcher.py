from app.execution.actions import (
    send_reminder,
    escalate_case,
    assign_senior_officer,
    fail_randomly,
)
from app.core.logger import logger

ACTION_MAP = {
    "send_reminder": send_reminder,
    "escalate_case": escalate_case,
    "assign_senior_officer": assign_senior_officer,
    "fail_randomly": fail_randomly,
}


def execute_action(action_name: str, payload: dict, config: dict):
    handler = ACTION_MAP.get(action_name)

    if not handler:
        logger.error(
            "action_unknown",
            extra={"extra_data": {"action_name": action_name}},
        )
        return {"status": "failed", "action": action_name, "reason": "unknown action"}

    logger.info(
        "action_dispatched",
        extra={"extra_data": {"action_name": action_name}},
    )
    result = handler(payload, config)

    if result.get("status") == "success" or result.get("success"):
        logger.info(
            "action_success",
            extra={"extra_data": {"action_name": action_name, "result": result}},
        )
    else:
        logger.warning(
            "action_failed",
            extra={"extra_data": {"action_name": action_name, "result": result}},
        )

    return result
