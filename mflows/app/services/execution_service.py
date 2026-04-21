import json
from sqlalchemy.orm import Session
from app.models.workflow import Workflow


def process_event_service(payload, db):
    workflows = db.query(Workflow)
    matched_workflows = []
    actions = []
    for workflow in workflows:
        try:
            rule = json.loads(workflows.parsed_rule_json)
        except:
            continue

        if is_rule_matched(rule, payload):
            matched_workflows.append(workflow.id)
            action = rule.get("action")
            if action:
                actions.append(action)
    return {
        "success": True,
        "event_type": payload.event_type,
        "matched_count": len(matched_workflows),
        "matched_workflows": matched_workflows,
        "actions": actions,
    }


def is_rule_matched(rule: dict, payload) -> dict:
    data = payload.payload

    if (
        rule.get("customer_type") == "vip"
        and data.get("customer_type") == "vip"
        and data.get("complaints", 0) >= 2
    ):
        return True

    if "salary_gt" in rule:
        if data.get("salary", 0) > rule["salary_gt"]:
            return True

    return False
