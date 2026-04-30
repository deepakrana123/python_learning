import time
from app.llm.prompt_loader import build_prompt
from app.llm.providers.ollama import try_call_ollama
from app.llm.providers.gemini_rest import try_call_gemini_rest
from app.core.logger import logger


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

        for index, provider in enumerate(self.providers):
            provider_name = getattr(provider, "__name__", f"provider_{index}")
            logger.info(
                "llm_provider_attempt",
                extra={"extra_data": {"provider": provider_name, "attempt_index": index}},
            )
            result = provider(prompt)

            if result["success"]:
                result["total_latency_ms"] = int((time.time() - start) * 1000)
                result["fallback_used"] = index > 0
                result["errors_before_success"] = errors
                if index > 0:
                    logger.warning(
                        "llm_fallback_provider_used",
                        extra={
                            "extra_data": {
                                "provider": result.get("provider"),
                                "fallback_index": index,
                                "prior_errors": errors,
                            }
                        },
                    )
                else:
                    logger.info(
                        "llm_provider_success",
                        extra={
                            "extra_data": {
                                "provider": result.get("provider"),
                                "latency_ms": result["total_latency_ms"],
                            }
                        },
                    )
                return result

            logger.warning(
                "llm_provider_failed",
                extra={
                    "extra_data": {
                        "provider": result.get("provider"),
                        "error": result.get("error"),
                    }
                },
            )
            errors.append({"provider": result["provider"], "error": result["error"]})

        total_ms = int((time.time() - start) * 1000)
        logger.error(
            "llm_all_providers_exhausted",
            extra={"extra_data": {"errors": errors, "total_latency_ms": total_ms}},
        )
        return {
            "success": False,
            "provider": None,
            "error": "all providers failed",
            "errors": errors,
            "total_latency_ms": total_ms,
        }
