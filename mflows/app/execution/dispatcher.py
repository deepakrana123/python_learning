import os
from app.execution.actions import (
    send_reminder,
    escalate_case,
    assign_senior_officer,
    fail_randomly,
    validate_payment_handler,
)
from app.execution.chaos_actions import (
    chaos_send_reminder,
    chaos_escalate_case,
    chaos_notify_manager,
    chaos_reject_loan,
    chaos_close_case,
    chaos_assign_senior_officer,
)
from app.core.logger import logger

# Production action map — real implementations
_PRODUCTION_ACTION_MAP = {
    "send_reminder": send_reminder,
    "escalate_case": escalate_case,
    "assign_senior_officer": assign_senior_officer,
    "fail_randomly": fail_randomly,
    "validate_payment": validate_payment_handler,
    "notify_manager": send_reminder,       # placeholder — same as reminder for now
    "reject_loan": fail_randomly,          # placeholder
    "close_case": escalate_case,           # placeholder
}

# Chaos action map — fake third-party integrations with configurable failure modes
# Activated when CHAOS_MODE=true in environment
_CHAOS_ACTION_MAP = {
    "send_reminder": chaos_send_reminder,
    "escalate_case": chaos_escalate_case,
    "assign_senior_officer": chaos_assign_senior_officer,
    "notify_manager": chaos_notify_manager,
    "reject_loan": chaos_reject_loan,
    "close_case": chaos_close_case,
    "validate_payment": chaos_send_reminder,   # reuse chaos pattern
    "fail_randomly": fail_randomly,
}

# Switch between real and chaos actions via env var
_CHAOS_ENABLED = os.getenv("CHAOS_MODE", "false").lower() == "true"
ACTION_MAP = _CHAOS_ACTION_MAP if _CHAOS_ENABLED else _PRODUCTION_ACTION_MAP


def execute_action(action_name: str, payload: dict, config: dict) -> dict:
    handler = ACTION_MAP.get(action_name)

    if not handler:
        logger.error(
            "action_unknown",
            extra={"extra_data": {"action_name": action_name, "chaos_enabled": _CHAOS_ENABLED}},
        )
        return {"status": "failed", "action": action_name, "reason": "unknown action"}

    logger.info(
        "action_dispatched",
        extra={
            "extra_data": {
                "action_name": action_name,
                "chaos_enabled": _CHAOS_ENABLED,
                "chaos_mode": config.get("chaos_mode", "none") if _CHAOS_ENABLED else "disabled",
            }
        },
    )

    try:
        result = handler(payload, config)
    except Exception as e:
        # Let exceptions propagate — step_executor handles them
        logger.warning(
            "action_raised_exception",
            extra={"extra_data": {"action_name": action_name, "error": str(e)}},
        )
        raise

    if result.get("status") == "success" or result.get("success"):
        logger.info(
            "action_success",
            extra={"extra_data": {"action_name": action_name}},
        )
    else:
        logger.warning(
            "action_failed",
            extra={"extra_data": {"action_name": action_name, "result": result}},
        )

    return result
