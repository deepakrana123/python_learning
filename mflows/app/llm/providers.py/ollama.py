import requests
import time
from app.llm.contracts import success_response, fail_response


OLLAMA_URL = "http://localhost:11434/api/generate"


def call_ollama(prompt: str):
    start = time.time()
    try:
        res = requests.post(
            OLLAMA_URL,
            json={"model": "qwen2.5:7b", "prompt": prompt, "stream": False},
            timeout=8,
        )
        data = res.json()
        return success_response(
            provider="ollama",
            model="qwen2.5:7b",
            text=data["response"],
            latency_ms=int((time.time() - start) * 1000),
            score=0.78,
            cost=0,
        )
    except Exception as e:
        return fail_response("ollama", e)
