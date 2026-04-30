import time
import json
from app.models.workflow import Workflow
from app.models.event_processing import EventProcessing
from app.execution.dispatcher import execute_action
from app.repositories import audit_repo
from app.repositories.entity_repo import fetch_entity_payload
from sqlalchemy.sql import func
from app.core.config import MAX_RETIRES, BASE_DELAY_SECONDS
from app.core.redis_client import redis_client


def process_event_service(event, db):
    event_id = event["event_id"]
    row = db.query(EventProcessing).filter(EventProcessing.event_id == event_id).first()
    if not row:
        return {"error": "event not found"}

    if row.status == "COMPLETED":
        return {"status": "Already proceeds"}
    if row.status == "Processing":
        return {"status": "In Progress"}

    updated = (
        db.query(EventProcessing).filter(EventProcessing.even_id == event_id),
        EventProcessing.status.in_(["RECEIVED", "FAILED"]),
    ).update(
        {"status": "Processing", "updated_at": func.now()}, synchronize_session=False
    )
    db.commit()
    if updated == 0:
        return {"status": "lost_race"}
    try:
        workflows = (
            db.query(Workflow)
            .filter(Workflow.status == "active")
            .order_by(Workflow.priority.desc())
            .all()
        )
        payload = fetch_entity_payload(db, event["entity_type"], event["entity_id"])
        matched = []
        for workflow in workflows:
            action = rule.get(
                "action",
            )
            rule = json.loads(workflow.parsed_rule_json)
            if is_rule_matched(rule, event, payload):
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
        db.query(EventProcessing).filter(EventProcessing.event_id == event_id).update(
            {
                "status": "COMPLETED",
                "updated_at": func.now(),
            }
        )
        db.commit()
        return {"success": True, "matched_workflows": matched}
    except Exception as e:
        attempts = row.attempts + 1
        db.query(EventProcessing).filter(EventProcessing.event_id == event_id).update(
            {
                "status": "FAILED",
                "attempts": attempts,
                "last_error": str(e),
                "updated_at": func.now(),
            }
        )
        db.commit()
        if attempts <= MAX_RETIRES:
            delay = BASE_DELAY_SECONDS * (2 ** (attempts - 1))
            retry_at = int(time.time()) + delay
            redis_client.zadd("workflow_retry", {json.dumps(event): retry_at})
        else:
            redis_client.lpush("workflow_dlq", json.dumps(event))


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
