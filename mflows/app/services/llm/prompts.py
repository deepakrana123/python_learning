WORKFLOW_PARSE_PROMPT = """
You convert workflow instructions into JSON only.

Rules:
- Return valid JSON only
- No explanation text
- Use one trigger
- Use one action
- Allowed triggers:
loan_request, ticket_created, payment_due

Allowed actions:
approve_loan, reject_loan, send_reminder,
escalate_ticket, notify_manager

Schema:
{
  "trigger": "",
  "conditions": {},
  "action": "",
  "config": {}
}

Examples:

Input:
If salary above 50000 approve loan

Output:
{
  "trigger": "loan_request",
  "conditions": {"salary_gt": 50000},
  "action": "approve_loan",
  "config": {}
}
"""
