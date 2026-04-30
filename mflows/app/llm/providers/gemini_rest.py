import requests
import os
import time
from app.config.retry_wrapper import with_retry
from app.llm.contracts import fail_response
from app.core.logger import logger

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL")
url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"


def try_call_gemini_rest(prompt: str):

    def __call():
        start = time.time()
        try:
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            response = requests.post(url=url, json=payload, timeout=8)
            if response.status_code != 200:
                logger.warning(
                    "gemini_http_error",
                    extra={
                        "extra_data": {
                            "status_code": response.status_code,
                            "response_body": response.text[:200],
                        }
                    },
                )
                return fail_response(
                    {"success": False, "provider": "gemini", "error": response.text}
                )
            data = response.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            latency = int((time.time() - start) * 1000)
            logger.info(
                "gemini_call_success",
                extra={"extra_data": {"latency_ms": latency}},
            )
            return {
                "success": True,
                "provider": "gemini",
                "model": "gemini-flash-latest",
                "text": text,
                "latency_ms": latency,
                "score": 0.90,
                "cost": 0,
            }
        except requests.Timeout:
            logger.warning("gemini_timeout")
            return {"success": False, "provider": "gemini", "error": "timeout"}
        except Exception as e:
            logger.error(
                "gemini_unexpected_error",
                extra={"extra_data": {"error": str(e)}},
            )
            return {"success": False, "provider": "gemini", "error": str(e)}

    return with_retry(__call, retries=2)
