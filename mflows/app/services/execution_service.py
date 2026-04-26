import json
from app.models.workflow import Workflow
from app.actions.dispatcher import execute_action
from app.repositories import audit_repo


def process_event_service(payload, db):
    workflows = db.query(Workflow)
    matched_workflows = []
    actions = []
    execution_results = []
    try:
        for workflow in workflows:
            rule = json.loads(workflow.parsed_rule_json)
            if not rule:
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
                    audit_repo.create(
                        db=db,
                        workflow_id=workflow.id,
                        action=action,
                        status=result.get("status", "unknown"),
                        event_type=payload.event_type,
                        request_payload=json.dumps(payload.payload),
                        response_payload=json.dumps(result),
                    )

        db.commit()
        return {
            "success": True,
            "event_type": payload.event_type,
            "matched_count": len(matched_workflows),
            "matched_workflows": matched_workflows,
            "actions": actions,
            "execution_results": execution_results,
        }

    except Exception:
        db.rollback()
    raise


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
