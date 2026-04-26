import time
import json


def build_mpt(user_input: str):
    return WORKFLOW_PARSE_PROMPT.replace("{input}", user_input)


def call_llm(user_input: str, task_type: str = "parser"):
    providers = [
        try_free_model,
        try_engineer_model,
        try_paid_model,
    ]
    for provider in providers:
        result = provider(user_input, task_type)
        if result["success"]:
            return result
    return {"success": False, "error": "all providers failed"}


def try_free_model(user_input, task_type):
    start = time.time()
    try:
        text = fake_call(user_input)
        return {
            "success": True,
            "provider": "free",
            "model": "fake-groq",
            "score": 0.82,
            "latency_ms": int((time.time() - start) * 1000),
            "cost": 0,
            "text": text,
        }

    except Exception as e:
        return {"success": False, "provider": "free", "error": str(e)}


def try_engineer_model(user_input, task_type):
    return {"success": False, "provider": "engineer", "error": "not configured"}


def try_paid_model(user_input, task_type):
    return {"success": False, "provider": "paid", "error": "not configured"}


def fake_call(user_input: str):
    return json.dumps(
        {
            "trigger": "loan_request",
            "action": "approve_loan",
            "conditions": {"salary_gt": 50000},
            "config": {},
        }
    )
