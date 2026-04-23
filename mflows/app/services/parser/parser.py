import json
from app.services.llm.client import call_llm
from app.services.llm.prompts import WORKFLOW_PARSE_PROMPT
from app.services.llm.validator import validate_workflow_json
import re


def parse_with_regex(raw_text: str):
    text = raw_text.lower()
    match = re.search(r"salary above (\d+) approve loan", raw_text)
    if match:
        amount = int(match.group(1))
        return {
            "success": True,
            "data": {
                "trigger": "loan_request",
                "action": "approve_loan",
                "conditions": {"salary_gt": amount},
                "config": {},
            },
        }
    return {"success": False}


def parse_workflow(raw_text: str):
    regex_result = parse_with_regex(raw_text)
    if regex_result["success"]:
        parsed = regex_result["data"]
        valid = validate_workflow_json(parsed)
        if valid["is_valid"]:
            return {"success": True, "source": "regex", "score": 1.0, "data": parsed}
        llm_result = call_llm(prompt=WORKFLOW_PARSE_PROMPT, user_input=raw_text)
        if not llm_result["success"]:
            return {"success": False, "error": "all providers failed"}

    try:
        cleaned = clean_json(llm_result["text"])
        parsed = json.loads(cleaned)
    except Exception:
        return {"success": False, "error": "invalid json from llm"}
    valid = validate_workflow_json(parsed)

    if not valid["is_valid"]:
        return {"success": False, "error": valid["errors"]}

    return {
        "success": True,
        "source": llm_result["provider"],
        "score": llm_result["score"],
        "data": parsed,
    }


def parse_with_regex(raw_text: str):
    text = raw_text.lower()
    match = re.search(r"salary above (\d+)")
    if match:
        amount = int(match.group(1))
        return {
            "success": True,
            "data": {
                "trigger": "loan_request",
                "action": "approve_loan",
                "conditions": {"salary_gt": amount},
                "config": {},
            },
        }
    return {"success": False}


def clean_json(text: str):
    text = text.replace("```json", "")
    text = text.replace("```", "")
    return text.strip()
