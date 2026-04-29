import json
from app.llm.llmManager import LLMManager
from app.llm.validator import validate_workflow_json
from app.llm.repair import repair_json


manager = LLMManager()


def clean_json(text: str):
    return text.replace("```json", "").replace("```", "").strip()


def parse_workflow_with_llm(raw_text: str):
    result = manager.call(raw_text)
    if not result["success"]:
        return result
    raw_output = result["text"]
    print(raw_output, "hlo raw_output")
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
        "score": result.get("score", 0),
        "data": parsed,
        "provider": result["provider"],
    }
