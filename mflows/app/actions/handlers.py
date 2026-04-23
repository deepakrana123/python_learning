def send_reminder(payload):
    print("Reminder sent:", payload)
    return {"status": "success", "action": "send_reminder"}


def approve_loan(payload, config):
    amount = config.get("max_amount", 10000)
    print("Loan approved:", payload)
    print("Max amount:", amount)

    return {"status": "success", "action": "approve_loan", "approved_limit": amount}


def escalate_ticket(payload):
    print("Ticket escalated:", payload)
    return {"status": "success", "action": "escalate_ticket"}
