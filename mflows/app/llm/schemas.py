ALLOWED_TRIGGERS = [
    "loan_requested",
    "payment_due",
    "payment_missed",
    "ticket_created",
    "complaint_created",
    "delivery_failed",
]

ALLOWED_ACTIONS = [
    "send_reminder",
    "escalate_case",
    "assign_senior_officer",
    "close_case",
    "reject_loan",
    "notify_manager",
]

REQUIRED_FIELDS = [
    "trigger",
    "action",
    # "conditions",
    # "config",
]
