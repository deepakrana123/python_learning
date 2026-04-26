import json
from app.llm.client import call_llm
from app.llm.validator import validate_workflow_json
from app.llm.repair import repair_json


def clean_json(text: str):
    return text.replace("```json", "").replace("```", "").strip()


def parse_workflow_with_llm(raw_text: str):
    result = call_llm(raw_text, "parser")
    if not result["success"]:
        return result
    raw_output = result["text"]
    try:
        parsed = json.loads(clean_json(raw_output))
    except Exception:
        repaired = repair_json(raw_output)
        if not repaired["success"]:
            return {"success": False, "error": "invalid json"}
        parsed = repaired["data"]
    valid = validate_workflow_json(parsed)
    if not valid["is_valid"]:
        return {"success": False, "error": valid["errors"]}
    return {
        "success": True,
        "source": result["provider"],
        "score": result["score"],
        "data": parsed,
    }
