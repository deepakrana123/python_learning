import json
from app.llm.prompt_loader import build_prompt


def repair_json(broken_text: str):
    prompt = build_prompt("repair_v1.txt", {"model_output": broken_text})
    repaired = fake_repair_call(prompt)
    try:
        return {"success": True, "data": json.loads(repaired)}
    except:
        return {"success": False}


def fake_repair_call(prompt: str):
    return {
        "trigger": "loan_request",
        "action": "approve_loan",
        "conditions": {"salary_gt": 50000},
        "config": {},
    }
