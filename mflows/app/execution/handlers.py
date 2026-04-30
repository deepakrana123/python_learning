from app.core.logger import logger


def send_reminder(payload, config):
    logger.info("action_send_reminder_success", extra={"extra_data": {"payload": payload}})
    return {"status": "success", "action": "send_reminder"}


def approve_loan(payload, config):
    amount = config.get("max_amount", 10000)
    logger.info(
        "action_approve_loan_success",
        extra={"extra_data": {"payload": payload, "approved_limit": amount}},
    )
    return {"status": "success", "action": "approve_loan", "approved_limit": amount}


def escalate_ticket(payload, config):
    logger.info("action_escalate_ticket_success", extra={"extra_data": {"payload": payload}})
    return {"status": "success", "action": "escalate_ticket"}
