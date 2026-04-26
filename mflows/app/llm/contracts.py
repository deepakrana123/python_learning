from typing import Option, Dict, Any


def success_response(provider, model, text, latency_ms, score=0.8, cost=0):
    return {
        "success": True,
        "provider": provider,
        "model": model,
        "text": text,
        "latency_ms": latency_ms,
        "score": score,
        "cost": cost,
    }


def fail_response(provider, error):
    return {"success": False, "provider": provider, "error": str(error)}
