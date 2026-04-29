import json
from app.models.workflow import Workflow
from app.execution.dispatcher import execute_action
from app.repositories import audit_repo
from app.repositories.entity_repo import fetch_entity_payload


def process_event_service(event, db):
    workflows = (
        db.query(Workflow)
        .filter(Workflow.status == "active")
        .order_by(Workflow.priority.desc())
        .all()
    )
    payload = fetch_entity_payload(db, event["entity_type"], event["entity_id"])
    matched = []
    for workflow in workflows:
        rule = json.loads(workflow.parsed_rule_json)
        if is_rule_matched(rule, event, payload):
            print("hlo rule matched")
            action = rule.get(
                "action",
            )
            print(action, "hlo action")
            result = execute_action(
                action_name=action, payload=payload, config=rule.get("config", {})
            )

            audit_repo.create(
                db=db,
                workflow_id=workflow.id,
                action=action,
                status=result["status"],
                event_type=event["event_type"],
                request_payload=json.dumps(payload),
                response_payload=json.dumps(result),
            )

            matched.append(workflow.id)
    db.commit()
    return {"success": True, "matched_workflows": matched}


def is_rule_matched(rule, event, data):
    if rule.get("trigger") != event["event_type"]:
        return False

    conditions = rule.get("conditions", [])

    for cond in conditions:

        if cond == "vip=true":
            if data.get("customer_type", "").lower() != "vip":
                return False

        elif cond.startswith("amount>"):
            value = int(cond.split(">")[1])
            if data.get("loan_amount", 0) <= value:
                return False

        elif cond.startswith("repeat_count>="):
            value = int(cond.split(">=")[1])
            if data.get("repeat_count", 0) < value:
                return False

    return True
