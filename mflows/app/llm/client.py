import time
import json
from app.llm.providers.ollama import try_call_ollama
from app.llm.prompt_loader import build_prompt
from app.llm.providers.gemini_rest import try_call_gemini_rest


def call_llm(user_input: str):
    providers = [
        try_call_ollama,
        try_call_gemini_rest,
        # try_engineer_model,
        # try_paid_model,
    ]
    prompt = build_prompt("parser_v1.txt", {"user_input": user_input})
    errors = []
    for provider in providers:
        result = provider(prompt)
        if result["success"]:
            return result
        errors.append({"provider": result["provider"], "error": result["error"]})
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
