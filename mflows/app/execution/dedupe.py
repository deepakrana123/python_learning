import hashlib
import json


def build_workflow_execution_key(event_id: str, workflow) -> str:
    raw = f"{event_id}:{workflow.id}"
    return hashlib.md5(raw.encode()).hexdigest()


def build_action_dedupe_key(event: dict, action: str) -> str:
    raw = json.dumps(
        {
            "event_type": event["event_type"],
            "entity_id": event["entity_id"],
            "action": action,
        },
        sort_keys=True,
    )
    return hashlib.md5(raw.encode()).hexdigest()
