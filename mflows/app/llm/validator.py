from app.llm.schemas import (
    ALLOWED_TRIGGERS,
    ALLOWED_ACTIONS,
    REQUIRED_FIELDS,
)


def validate_workflow_json(data: dict):
    errors = []
    if not isinstance(data, dict):
        return {"is_valid": False, "errors": ["response must be object"]}
    print(data, "data")
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"missing field: {field}")

    if data.get("trigger") not in ALLOWED_TRIGGERS:
        errors.append("invalid trigger")
    if data.get("action") not in ALLOWED_ACTIONS:
        errors.append("invalid actions")
    if "conditions" in data and not isinstance(data.get("conditions", []), list):
        errors.append("conditions must be list")
    delay = data.get("delay_days")
    if delay is not None:
        if not isinstance(delay, int):
            errors.append("delay must an integer")
        elif delay < 0:
            errors.append("delay_days cannot be negative")
        elif delay > 365:
            errors.append("delay_days too large")
    config = data.get("config")
    if config is not None and not isinstance(config, dict):
        errors.append("config must be object")
    return {"is_valid": len(errors) == 0, "errors": errors}
