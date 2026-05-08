import requests

# URL = "http://127.0.0.1:8000/api/event/publish"
URL = "http://127.0.0.1:8000/api/workflows"
abc = [
    {
        "name": "Loan Payment Reminder",
        "domain": "loan",
        "raw_input": "Send reminder 2 days before payment due",
    },
    {
        "name": "Missed EMI Escalation",
        "domain": "loan",
        "raw_input": "Escalate case when payment missed",
    },
    {
        "name": "VIP Payment Reminder",
        "domain": "loan",
        "raw_input": "Send reminder for VIP customers before EMI due",
    },
    {
        "name": "Premium Customer Alert",
        "domain": "loan",
        "raw_input": "Notify manager for premium customer loan request",
    },
    {
        "name": "Loan Rejection Risk",
        "domain": "loan",
        "raw_input": "Reject loan request if customer is risky",
    },
    {
        "name": "High Value Loan Alert",
        "domain": "loan",
        "raw_input": "Notify manager if loan amount exceeds 50000",
    },
    {
        "name": "Urgent Ticket Handling",
        "domain": "support",
        "raw_input": "Assign senior officer for urgent tickets",
    },
    {
        "name": "Complaint Escalation",
        "domain": "support",
        "raw_input": "Escalate complaint when customer raises issue",
    },
    {
        "name": "Ticket Resolution",
        "domain": "support",
        "raw_input": "Close case after complaint resolved",
    },
    {
        "name": "Reminder Retry Workflow",
        "domain": "loan",
        "raw_input": "Send reminder if payment due after 2 days with retry 3 times",
    },
    {
        "name": "Manager Escalation",
        "domain": "support",
        "raw_input": "Raise to manager if complaint created",
    },
    {
        "name": "Missed Payment Retry",
        "domain": "loan",
        "raw_input": "Send reminder for missed payment with retry 2 times",
    },
    {
        "name": "VIP Complaint Escalation",
        "domain": "support",
        "raw_input": "Escalate VIP complaint immediately",
    },
    {
        "name": "Urgent Complaint Assignment",
        "domain": "support",
        "raw_input": "Assign senior officer when urgent complaint created",
    },
    {
        "name": "Loan Approval Notification",
        "domain": "loan",
        "raw_input": "Notify manager when loan requested",
    },
    {
        "name": "Risky Customer Loan",
        "domain": "loan",
        "raw_input": "Reject application for risky customer",
    },
    {
        "name": "Retry Escalation Workflow",
        "domain": "support",
        "raw_input": "Escalate case if reminder fails",
    },
    {
        "name": "Delayed Reminder",
        "domain": "loan",
        "raw_input": "Send reminder after 5 days of payment due",
    },
    {
        "name": "Support Ticket Assignment",
        "domain": "support",
        "raw_input": "Assign senior officer when ticket created",
    },
    {
        "name": "High Priority Ticket",
        "domain": "support",
        "raw_input": "Assign to manager for high priority tickets",
    },
    {
        "name": "Complaint Auto Close",
        "domain": "support",
        "raw_input": "Close case after complaint completed",
    },
    {
        "name": "Premium EMI Reminder",
        "domain": "loan",
        "raw_input": "Remind premium customer before payment due",
    },
    {
        "name": "Loan Fraud Detection",
        "domain": "loan",
        "raw_input": "Reject loan if customer marked fraudulent",
    },
    {
        "name": "Missed EMI Notification",
        "domain": "loan",
        "raw_input": "Notify manager for missed EMI",
    },
    {
        "name": "Urgent Payment Escalation",
        "domain": "loan",
        "raw_input": "Escalate missed payment urgently",
    },
    {
        "name": "Delivery Failure Escalation",
        "domain": "support",
        "raw_input": "Escalate case when delivery failed",
    },
    {
        "name": "Support Retry Handler",
        "domain": "support",
        "raw_input": "Retry reminder 3 times before escalation",
    },
    {
        "name": "Ticket Closure Workflow",
        "domain": "support",
        "raw_input": "Close ticket when issue resolved",
    },
    {
        "name": "Large Loan Review",
        "domain": "loan",
        "raw_input": "Notify manager if loan amount exceeds 100000",
    },
    {
        "name": "Customer Reminder",
        "domain": "loan",
        "raw_input": "Notify customer before payment due",
    },
    {
        "name": "Urgent Manager Notification",
        "domain": "support",
        "raw_input": "Inform manager for urgent complaint",
    },
    {
        "name": "VIP Ticket Routing",
        "domain": "support",
        "raw_input": "Assign senior officer for VIP ticket",
    },
    {
        "name": "Premium Loan Escalation",
        "domain": "loan",
        "raw_input": "Escalate premium customer complaint",
    },
    {
        "name": "Complaint Retry Flow",
        "domain": "support",
        "raw_input": "Retry escalation 2 times on complaint",
    },
    {
        "name": "Late Payment Reminder",
        "domain": "loan",
        "raw_input": "Send reminder after missed payment",
    },
    {
        "name": "Fraud Loan Rejection",
        "domain": "loan",
        "raw_input": "Decline loan for fraudulent application",
    },
    {
        "name": "Issue Escalation",
        "domain": "support",
        "raw_input": "Send to supervisor when ticket raised",
    },
    {
        "name": "Urgent Reminder Workflow",
        "domain": "loan",
        "raw_input": "Urgently remind customer before EMI due",
    },
    {
        "name": "Support Officer Assignment",
        "domain": "support",
        "raw_input": "Assign senior officer for complaint created",
    },
    {
        "name": "Reminder Failure Escalation",
        "domain": "loan",
        "raw_input": "Send reminder, if fails escalate",
    },
    {
        "name": "Critical Complaint Flow",
        "domain": "support",
        "raw_input": "Escalate urgent complaint to manager",
    },
    {
        "name": "Loan Risk Notification",
        "domain": "loan",
        "raw_input": "Alert manager for risky loan request",
    },
    {
        "name": "Customer Escalation",
        "domain": "support",
        "raw_input": "Raise complaint to supervisor",
    },
    {
        "name": "Payment Delay Workflow",
        "domain": "loan",
        "raw_input": "Send reminder 3 days after payment due",
    },
    {
        "name": "Ticket Retry Assignment",
        "domain": "support",
        "raw_input": "Assign senior officer after 2 failed attempts",
    },
    {
        "name": "Complaint Manager Alert",
        "domain": "support",
        "raw_input": "Notify manager when complaint created",
    },
    {
        "name": "VIP Missed EMI",
        "domain": "loan",
        "raw_input": "Escalate VIP customer missed payment",
    },
    {
        "name": "Loan Reminder Retry",
        "domain": "loan",
        "raw_input": "Retry payment reminder 4 times",
    },
    {
        "name": "Urgent Ticket Escalation",
        "domain": "support",
        "raw_input": "Escalate urgent tickets immediately",
    },
    {
        "name": "High Amount Approval",
        "domain": "loan",
        "raw_input": "Notify manager if amount greater than 75000",
    },
]


for payload in abc:
    requests.post(URL, json=payload)
