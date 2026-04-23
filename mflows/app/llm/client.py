import os
from dotenv import load_dotenv
import time
from app.llm.prompt_loader import build_prompt

load_dotenv()


FREE_PROVIDER = os.getenv("FREE_PROVIDER", "groq")
LOCAL_ENABLED = os.getenv("LOCAL_ENABLED", "false").lower() == "true"
ENGINEER_PROVIDER = os.getenv("ENGINEER_PROVIDER", "openai")
PAID_PROVIDER = os.getenv("PAID_PROVIDER", "openai")


def call_llm(user_input: str, task_type: str = "parser"):
    providers = [try_free_model, try_free_model, try_engineer_model, try_paid_model]

    for provider_fn in providers:
        result = provider_fn(user_input, task_type)

        if result["success"]:
            return result

    return {"success": False, "error": "all providers failed"}


def try_free_model(user_input, task_type):
    start = time.time()
    try:
        prompt = build_prompt("parser_v1.txt", {"user_input": user_input})
        text = fake_call("Free_Model", prompt)
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


def try_local_model(user_input, task_type):
    return {"success": False, "provider": "local", "error": "disabled"}


def try_paid_model(user_input, task_type):
    return {"success": False, "provider": "engineer", "error": "not configured"}


def try_engineer_model(user_input, task_type):
    return {"success": False, "provider": "engineer", "error": "not configured"}


def fake_call(prompt):
    print("Prompt sent:")
    print(prompt)
    return {
        "trigger": "loan_request",
        "action": "approve_loan",
        "conditions": {"salary_gt": 50000},
        "config": {},
    }
