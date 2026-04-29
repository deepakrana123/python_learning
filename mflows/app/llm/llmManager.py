import time
from app.llm.prompt_loader import build_prompt
from app.llm.providers.ollama import try_call_ollama
from app.llm.providers.gemini_rest import try_call_gemini_rest


class LLMManager:
    def __init__(self):
        self.providers = [
            try_call_ollama,
            try_call_gemini_rest,
        ]

    def call(self, user_input: str):
        start = time.time()
        prompt = build_prompt("parser_v1.txt", {"user_input": user_input})
        errors = []
        fallback_used = False
        for index, provider in enumerate(self.providers):
            result = provider(prompt)
            if result["success"]:
                result["total_latency_ms"] = int((time.time() - start) * 1000)
                result["fallback_used"] = index > 0
                result["errors_before_success"] = errors
                return result
            errors.append({"provider": result["provider"], "error": result["error"]})

        return {
            "success": False,
            "provider": None,
            "error": "all providers failed",
            "errors": errors,
            "total_latency_ms": int((time.time() - start) * 1000),
        }
