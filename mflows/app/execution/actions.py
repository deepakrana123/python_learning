import random
import time


def send_reminder(payload, config):
    print("hello send reminder")
    time.sleep(1)
    return {
        "success": True,
        "message": "reminder sent",
        "payload": payload,
        "status": "success",
    }


def escalate_case(payload, config):
    time.sleep(1)
    print("hello send escalate case")
    return {
        "success": True,
        "message": "case escalated",
        "payload": payload,
        "status": "success",
    }


def assign_senior_officer(payload, config):
    print("hello send assign senior officer")
    return {"success": True, "officer_id": "EMP101", "status": "success"}


def fail_randomly(payload, config):
    if random.random() < 0.3:
        raise Exception("temporary failure")
    return {"success": True, "status": "success"}
