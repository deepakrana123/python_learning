import random
import time
from app.core.logger import logger


def send_reminder(payload, config):
    time.sleep(1)
    logger.info(
        "action_send_reminder_success", extra={"extra_data": {"payload": payload}}
    )
    return {
        "success": True,
        "message": "reminder sent",
        "payload": payload,
        "status": "success",
    }


def escalate_case(payload, config):
    time.sleep(1)
    logger.info(
        "action_escalate_case_success", extra={"extra_data": {"payload": payload}}
    )
    return {
        "success": True,
        "message": "case escalated",
        "payload": payload,
        "status": "success",
    }


def assign_senior_officer(payload, config):
    logger.info(
        "action_assign_senior_officer_success",
        extra={"extra_data": {"payload": payload}},
    )
    return {"success": True, "officer_id": "EMP101", "status": "success"}


def fail_randomly(payload, config):
    if random.random() < 0.3:
        logger.error(
            "action_fail_randomly_triggered",
            extra={"extra_data": {"payload": payload}},
        )
        raise Exception("temporary failure")
    logger.info("action_fail_randomly_success")
    return {"success": True, "status": "success"}


def approve_loan(payload, config):
    amount = config.get("max_amount", 10000)
    logger.info(
        "action_approve_loan_success",
        extra={"extra_data": {"payload": payload, "approved_limit": amount}},
    )
    return {"status": "success", "action": "approve_loan", "approved_limit": amount}


def escalate_ticket(payload, config):
    logger.info(
        "action_escalate_ticket_success", extra={"extra_data": {"payload": payload}}
    )
    return {"status": "success", "action": "escalate_ticket"}


def validate_payment_handler(payload, config):
    logger.info("validate_payment_handler", extra={"extra_data": {"payload": payload}})
    return {"status": "success", "action": "validate_payment"}
