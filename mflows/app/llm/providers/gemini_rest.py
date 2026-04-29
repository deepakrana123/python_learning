import requests
import os
import time
from app.config.retry_wrapper import with_retry
from app.llm.contracts import fail_response

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
                return fail_response(
                    {"success": False, "provider": "gemini", "error": response.text}
                )
            data = response.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return {
                "success": True,
                "provider": "gemini",
                "model": "gemini-flash-latest",
                "text": text,
                "latency_ms": int((time.time() - start) * 1000),
                "score": 0.90,
                "cost": 0,
            }
        except requests.Timeout:
            return {"success": False, "provider": "gemini", "error": "timeout"}
        except Exception as e:
            return {"success": False, "provider": "gemini", "error": str(e)}

    return with_retry(__call, retries=2)
