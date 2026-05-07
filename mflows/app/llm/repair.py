import json


def repair_json(text: str):
    try:
        return {"success": True, "data": json.loads(text)}
    except Exception:
        return {"success": False}


def apply_llm_patch(rule: dict, llm_data: dict):
    if not llm_data.get("success"):
        return rule

    patch = llm_data["data"]
    if rule.get("trigger") is None:
        rule["trigger"] = patch.get("trigger")

    if rule.get("action") is None:
        rule["action"] = patch.get("action")

    if patch.get("conditions"):
        rule.setdefault("conditions", [])
        rule["conditions"].extend(patch["conditions"])

    if patch.get("config"):
        rule.setdefault("config", {}).update(patch["config"])

    return rule
    
    

