import json
from sqlalchemy.orm import Session
from app.models.workflow import Workflow
from app.services.actions.dispatcher import execute_action
from app.models.audit_log import AuditLog
import json


def process_event_service(payload, db):
    workflows = db.query(Workflow)
    matched_workflows = []
    actions = []
    execution_results = []
    for workflow in workflows:
        try:
            rule = json.loads(workflows.parsed_rule_json)
        except:
            continue

        if is_rule_matched(rule, payload):
            matched_workflows.append(workflow.id)
            action = rule.get("action")
            config = rule.get("config")
            if action:
                actions.append(action)
                result = execute_action(
                    action_name=action, payload=payload.payload, config=config
                )
                execution_results.append(result)
                log = AuditLog(
                    workflow_id=workflow.id,
                    action=action,
                    status=result.get("status", "unknown"),
                    event_type=payload.event_type,
                    request_payload=json.dumps(payload.payload),
                    response_payload=json.dumps(result),
                )
                db.add(log)
                db.commit()
    return {
        "success": True,
        "event_type": payload.event_type,
        "matched_count": len(matched_workflows),
        "matched_workflows": matched_workflows,
        "actions": actions,
        "execution_results": execution_results,
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
