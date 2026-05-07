from app.models.workflow import Workflow
from app.repositories.entity_repo import fetch_entity_payload
from app.execution.conditions import is_rule_matched
from app.core.logger import logger


def get_matching_workflows(db, event: dict) -> tuple[list, dict]:
    """
    Loads all active workflows, fetches the entity payload,
    and returns (matched_workflows, payload).

    matched_workflows: list of Workflow objects whose rule matches the event
    payload: the entity data fetched for this event
    """
    workflows = (
        db.query(Workflow)
        .filter(Workflow.status == "active")
        .order_by(Workflow.priority.desc())
        .all()
    )

    payload = fetch_entity_payload(db, event["entity_type"], event["entity_id"])

    matched = []
    for workflow in workflows:
        rule = workflow.parsed_rule_json
        if is_rule_matched(rule, event, payload):
            matched.append(workflow)
        else:
            logger.debug(
                "workflow_not_matched",
                extra={
                    "extra_data": {
                        "workflow_id": workflow.id,
                        "event_type": event["event_type"],
                    }
                },
            )

    return matched, payload
