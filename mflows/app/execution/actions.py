import random
import time


def send_reminder(payload):
    time.sleep(1)
    return {"success": True, "message": "reminder sent", "payload": payload}


def escalate_case(payload):
    time.sleep(1)
    return {"success": True, "message": "case escalated", "payload": payload}


def assign_senior_officer(payload):
    return {"success": True, "officer_id": "EMP101"}


def fail_randomly(payload):
    if random.random() < 0.3:
        raise Exception("temporary failure")
    return {"success": True}
