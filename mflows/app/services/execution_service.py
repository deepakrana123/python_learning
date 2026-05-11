import json
from sqlalchemy.sql import func
from app.models.event_processing import EventProcessing
from app.execution.dispatcher import execute_action
from app.execution.matcher import get_matching_workflows
from app.execution.dedupe import build_workflow_execution_key, build_action_dedupe_key
from app.execution.retry_handler import handle_retry
from app.core.redis_client import redis_client
from app.core.logger import logger
from app.repositories import audit_repo


def process_event_service(event: dict, db):
    event_id = event["event_id"]
    executed_workflows = []
    matched_workflow_ids = []
    executed_keys = set()

    # Claim the event — only one worker processes it
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
        matched_workflows, payload = get_matching_workflows(db, event)

        for workflow in matched_workflows:
            rule = workflow.parsed_rule_json
            action = rule.get("action")
            config = rule.get("config", {})

            matched_workflow_ids.append(workflow.id)

            # Local dedupe
            exec_key = build_workflow_execution_key(event_id, workflow)
            if exec_key in executed_keys:
                logger.info(
                    "duplicate_action_skipped_local",
                    extra={"extra_data": {"event_id": event_id, "key": exec_key}},
                )
                continue

            # Distributed dedupe via Redis
            redis_key = f"exec:{event_id}:{exec_key}"
            lock_acquired = redis_client.set(redis_key, 1, nx=True, ex=3600)
            if not lock_acquired:
                logger.info(
                    "duplicate_action_skipped_distributed",
                    extra={"extra_data": {"event_id": event_id, "key": exec_key}},
                )
                continue

            # Action dedupe — skip if same action already ran for this event
            action_key = build_action_dedupe_key(event, action)
            if action_key in executed_keys:
                continue

            result = execute_action(
                action_name=action,
                payload=payload,
                config=config,
            )

            success = result.get("success") or result.get("status") == "success"

            if success:
                executed_keys.add(action_key)
                executed_workflows.append(workflow.id)

                audit_repo.create(
                    db=db,
                    workflow_id=workflow.id,
                    action=action,
                    status="success",
                    event_type=event["event_type"],
                    request_payload=json.dumps(payload),
                    response_payload=json.dumps(result),
                )

                logger.info(
                    "action_executed",
                    extra={
                        "extra_data": {
                            "event_id": event_id,
                            "workflow_id": workflow.id,
                            "action": action,
                            "config": config,
                            "success": success,
                            "key": exec_key,
                        }
                    },
                )

        # Mark event complete
        db.query(EventProcessing).filter(EventProcessing.event_id == event_id).update(
            {"status": "COMPLETED", "updated_at": func.now()}
        )
        db.commit()

        logger.info(
            "event_summary",
            extra={
                "extra_data": {
                    "event_id": event_id,
                    "matched_workflows": matched_workflow_ids,
                    "executed_workflows": executed_workflows,
                    "executed_actions": list(executed_keys),
                    "total_matched": len(matched_workflow_ids),
                    "total_executed": len(executed_keys),
                }
            },
        )
        logger.info(
            "event_completed",
            extra={
                "extra_data": {
                    "event_id": event_id,
                    "matched_workflows": matched_workflow_ids,
                }
            },
        )

    except Exception as e:
        handle_retry(db, event, e)
