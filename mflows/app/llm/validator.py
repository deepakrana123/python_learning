from app.llm.schemas import ALLOWED_TRIGGERS, ALLOWED_ACTIONS, REQUIRED_FIELDS


def validate_workflow_json(data: dict):
    errors = []

    if not isinstance(data, dict):
        return {"is_valid": False, "errors": ["response must be object"]}
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"missing field:{field}")
        if data.get("trigger") not in ALLOWED_TRIGGERS:
            errors.append("Invalid trigger")
        if data.get("action") not in ALLOWED_ACTIONS:
            errors.append("Invalid action")
        if "condititons" in data and not isinstance(data["conditions"], dict):
            errors.append("condititons must be object")
        if "config" in data and not isinstance(data["config"], dict):
            errors.append("config must be object")
    return {"is_valid": len(errors) == 0, "errors": errors}
