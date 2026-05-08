from app.repositories.entity_repo import fetch_entity_payload
from app.execution.workflow_loader import load_active_workflows
from app.execution.matcher import get_matching_workflows


def processor(db, event: dict):
    workflows = load_active_workflows(db)
    payload = fetch_entity_payload(db, event["entity_type"], event["entity_id"])
    matched = get_matching_workflows(workflows=workflows, event=event, payload=payload)
    return matched
