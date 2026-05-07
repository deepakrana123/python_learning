from app.llm.providers.ollama import try_call_ollama
from app.llm.prompt_loader import build_prompt
from app.llm.providers.gemini_rest import try_call_gemini_rest


def call_llm(user_input: str):
    providers = [
        try_call_ollama,
        try_call_gemini_rest,
    ]
    prompt = build_prompt("parser_v1.txt", {"user_input": user_input})
    errors = []
    for provider in providers:
        result = provider(prompt)
        if result["success"]:
            return result
        errors.append({"provider": result["provider"], "error": result["error"]})
    return {"success": False, "error": "all providers failed"}
