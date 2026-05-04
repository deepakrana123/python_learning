import time
from sqlalchemy.sql import func
from app.models.workflow import Workflow
from app.models.event_processing import EventProcessing
from app.execution.dispatcher import execute_action
from app.repositories.entity_repo import fetch_entity_payload
from app.core.config import MAX_RETRIES, BASE_DELAY_SECONDS
from app.core.redis_client import redis_client
from app.core.logger import logger
import hashlib
import json
from app.repositories import audit_repo


def build_execution_key(action, config):
    raw = json.dumps({"action": action, "config": config}, sort_keys=True)
    return hashlib.md5(raw.encode()).hexdigest()


def process_event_service(event, db):
    event_id = event["event_id"]
    executed_workflows = []
    matched_workflows = []
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
        for workflow in workflows:
            rule = json.loads(workflow.parsed_rule_json)
            action = rule.get("action")
            config = rule.get("config", {})
            if not is_rule_matched(rule, event, payload):
                continue
            matched_workflows.append(workflow.id)
            key = build_execution_key(action, config)

            if key in executed_keys:
                logger.info(
                    "duplicate_action_skipped_local",
                    extra={"extra_data": {"event_id": event_id, "key": key}},
                )
                continue
            redis_key = f"exec:{event_id}:{key}"
            lock_acquired = redis_client.set(
                redis_key,
                1,
                nx=True,
                ex=3600,  # TTL = 1 hour
            )
            if not lock_acquired:
                logger.info(
                    "duplicate_action_skipped_distributed",
                    extra={"extra_data": {"event_id": event_id, "key": key}},
                )
                continue
            result = execute_action(
                action_name=action,
                payload=payload,
                config=config,
            )

            success = result.get("success") or result.get("status") == "success"
            executed_keys.add(key)
            executed_workflows.append(workflow.id)
            audit_repo.create(
                db=db,
                workflow_id=workflow.id,
                action=action,
                status="success" if success else "failed",
                event_type=event["event_type"],
                request_payload=json.dumps(payload),
                response_payload=json.dumps(result),
            )

            # Logging
            logger.info(
                "action_executed",
                extra={
                    "extra_data": {
                        "event_id": event_id,
                        "workflow_id": workflow.id,
                        "action": action,
                        "config": config,
                        "success": success,
                        "key": key,
                    }
                },
            )

        logger.info(
            "event_summary",
            extra={
                "extra_data": {
                    "event_id": event_id,
                    "matched_workflows": matched_workflows,
                    "executed_workflows": executed_workflows,
                    "executed_actions": list(executed_keys),
                    "total_matched": len(matched_workflows),
                    "total_executed": len(executed_keys),
                }
            },
        )
        db.query(EventProcessing).filter(EventProcessing.event_id == event_id).update(
            {"status": "COMPLETED", "updated_at": func.now()}
        )
        db.commit()
        logger.info(
            "event_completed",
            extra={
                "extra_data": {
                    "event_id": event_id,
                    "matched_workflows": matched_workflows,
                }
            },
        )
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
