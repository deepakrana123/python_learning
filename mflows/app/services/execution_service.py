import time
import json
from app.models.workflow import Workflow
from app.models.event_processing import EventProcessing
from app.execution.dispatcher import execute_action
from app.repositories import audit_repo
from app.repositories.entity_repo import fetch_entity_payload
from sqlalchemy.sql import func
from app.core.config import MAX_RETRIES, BASE_DELAY_SECONDS
from app.core.redis_client import redis_client
from app.core.logger import logger
from app.metrics.execution_metrics import execution_metrics


def process_event_service(event, db):
    event_id = event["event_id"]
    execution_metrics.total_events += 1

    updated = (
        db.query(EventProcessing).filter(EventProcessing.even_id == event_id),
        EventProcessing.status.in_(["RECEIVED", "FAILED"]),
    ).update(
        {"status": "Processing", "updated_at": func.now()}, synchronize_session=False
    )
    db.commit()

    if updated == 0:
        execution_metrics.events_lost_race += 1
        logger.warning(
            "event_lost_race",
            extra={"extra_data": {"event_id": event_id}},
        )
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
                execution_metrics.total_actions_executed += 1
                result = execute_action(
                    action_name=action, payload=payload, config=rule.get("config", {})
                )

                if result.get("status") == "success" or result.get("success"):
                    execution_metrics.action_successes += 1
                else:
                    execution_metrics.action_failures += 1
                    logger.warning(
                        "workflow_action_failed",
                        extra={
                            "extra_data": {
                                "event_id": event_id,
                                "workflow_id": workflow.id,
                                "action": action,
                                "result": result,
                            }
                        },
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

        execution_metrics.total_workflows_matched += len(matched)

        if not matched:
            logger.info(
                "event_no_workflows_matched",
                extra={
                    "extra_data": {
                        "event_id": event_id,
                        "event_type": event["event_type"],
                    }
                },
            )

        db.query(EventProcessing).filter(EventProcessing.event_id == event_id).update(
            {"status": "COMPLETED", "updated_at": func.now()}
        )
        db.commit()
        execution_metrics.events_completed += 1
        logger.info(
            "event_completed",
            extra={
                "extra_data": {
                    "event_id": event_id,
                    "matched_workflows": matched,
                }
            },
        )
        return {"success": True, "matched_workflows": matched}

    except Exception as e:
        execution_metrics.events_failed += 1
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

        if attempts <= MAX_RETRIES:
            delay = BASE_DELAY_SECONDS * (2 ** (attempts - 1))
            retry_at = int(time.time()) + delay
            redis_client.zadd("workflow_retry", {json.dumps(event): retry_at})
            execution_metrics.retries_scheduled += 1
            logger.warning(
                "event_retry_scheduled",
                extra={
                    "extra_data": {
                        "event_id": event_id,
                        "attempt": attempts,
                        "retry_in_seconds": delay,
                        "error": str(e),
                    }
                },
            )
        else:
            redis_client.lpush("workflow_dlq", json.dumps(event))
            execution_metrics.dlq_pushes += 1
            logger.error(
                "event_pushed_to_dlq",
                extra={
                    "extra_data": {
                        "event_id": event_id,
                        "attempts": attempts,
                        "error": str(e),
                    }
                },
            )


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
