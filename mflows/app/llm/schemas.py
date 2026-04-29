ALLOWED_TRIGGERS = ["loan_request", "ticket_created", "payment_due", "payment_missed"]

ALLOWED_ACTIONS = [
    "approve_loan",
    "reject_loan",
    "send_reminder",
    "escalate_ticket",
    "notify_manager",
    "escalate_case",
]

REQUIRED_FIELDS = [
    "trigger",
    "action",
    # "conditions",
    # "config",
]
