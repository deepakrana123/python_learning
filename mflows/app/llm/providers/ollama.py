import requests
import time
from app.llm.contracts import success_response, fail_response

from app.config.retry_wrapper import with_retry

OLLAMA_URL = "http://localhost:11434/api/generate"
# OLLAMA_URL = "http://localhost:9999/api/generate"


def try_call_ollama(prompt: str):
    def __call():
        start = time.time()
        try:
            res = requests.post(
                OLLAMA_URL,
                json={"model": "qwen2.5:7b", "prompt": prompt, "stream": False},
                timeout=1,
            )
            if res.status_code != 200:
                return fail_response("ollama", f"http_{res.status_code}")
            data = res.json()
            text = data.get("response", "").strip()
            if not text:
                return fail_response("ollama", "empty_response")

            return success_response(
                provider="ollama",
                model="qwen2.5:7b",
                text=data["response"],
                latency_ms=int((time.time() - start) * 1000),
                score=0.78,
                cost=0,
            )
        except requests.Timeout:
            return fail_response("ollama", "timeout")
        except Exception as e:
            return fail_response("ollama", str(e))

    return with_retry(__call, retries=1)
