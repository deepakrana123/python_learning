import time
import json
from sqlalchemy.sql import func

from app.models.workflow import Workflow
from app.models.event_processing import EventProcessing
from app.execution.dispatcher import execute_action
from app.repositories import audit_repo
from app.repositories.entity_repo import fetch_entity_payload
from app.core.config import MAX_RETRIES, BASE_DELAY_SECONDS
from app.core.redis_client import redis_client
from app.core.logger import logger
import hashlib
import json


def build_execution_key(action, config):
    raw = json.dumps({"action": action, "config": config}, sort_keys=True)
    return hashlib.md5(raw.encode()).hexdigest()


def process_event_service(event, db):
    event_id = event["event_id"]
    executed_keys = set()
    updated = (
        db.query(EventProcessing)
        .filter(
            EventProcessing.event_id == event_id,
            EventProcessing.status.in_(["RECEIVED", "FAILED"]),
        )
        .update(
            {"status": "PROCESSING", "updated_at": func.now()},
            synchronize_session=False,
        )
    )
    db.commit()

    if updated == 0:
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
            rule = json.loads(workflow.parsed_rule_json)
            action = rule.get("action")
            if is_rule_matched(rule, event, payload):
                key = build_execution_key(action, rule.get("config", {}))
                if key in executed_keys:
                    continue

                result = execute_action(
                    action_name=action,
                    payload=payload,
                    config=rule.get("config", {}),
                )
                executed_keys.add(key)
                logger.info(
                    "execution_key_debug",
                    extra={
                        "extra_data": {
                            "action": action,
                            "config": rule.get("config", {}),
                            "key": key,
                        }
                    },
                )
                # Audit log
                # audit_repo.create(
                #     db=db,
                #     workflow_id=workflow.id,
                #     action=action,
                #     status=result.get("status", "unknown"),
                #     event_type=event["event_type"],
                #     request_payload=json.dumps(payload),
                #     response_payload=json.dumps(result),
                # )

                matched.append(workflow.id)

        db.query(EventProcessing).filter(EventProcessing.event_id == event_id).update(
            {"status": "COMPLETED", "updated_at": func.now()}
        )
        db.commit()

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

        row = (
            db.query(EventProcessing)
            .filter(EventProcessing.event_id == event_id)
            .first()
        )

        attempts = (row.attempts or 0) + 1

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

            retry_payload = {
                "event": event,
                "attempt": attempts,
            }

            redis_client.zadd(
                "workflow_retry",
                {json.dumps(retry_payload): retry_at},
            )

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
            dlq_payload = {
                "event": event,
                "attempts": attempts,
                "error": str(e),
                "failed_at": int(time.time()),
            }

            redis_client.lpush("workflow_dlq", json.dumps(dlq_payload))

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
