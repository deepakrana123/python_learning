from app.parsers.extractors import extract_all
from app.parsers.intent_mapper import map_intents
from app.parsers.rule_builder import build_final_rule
from app.parsers.validator import validate_rule
from app.parsers.metrics import metrics
from app.parsers.cache import cache_store
from app.llm.service import parse_workflow_with_llm


def needs_llm(mapped: dict):
    action_conf = mapped["action_result"]["confidence"]
    trigger_conf = mapped["trigger_result"]["confidence"]

    return action_conf < 0.5 or trigger_conf < 0.5


def parse_workflow_text(text: str):
    metrics.total_requests += 1
    if text in cache_store:
        metrics.cache_hits += 1
        return cache_store[text]

    extracted = extract_all(text)
    mapped = map_intents(text)
    source = "rules"
    if needs_llm(mapped):
        llm_result = parse_workflow_with_llm(text)
        if llm_result["success"]:
            metrics.llm_hits += 1
        result = {
            "success": True,
            "source": "llm",
            "rule": llm_result["data"],
            "validation": {
                "is_valid": True,
                "errors": [],
            },
            "data": llm_result["data"],
            "score": llm_result["score"],
        }
        cache_store[text] = result
        return result
    rule = build_final_rule(extracted=extracted, mapped=mapped)
    validation = validate_rule(rule)
    result = {
        "success": validation["is_valid"],
        "source": source,
        "rule": rule,
        "validation": validation,
        "debug": {
            "extracted": extracted,
            "mapped": mapped,
        },
        "score": 1.0,
        "data": rule if validation["is_valid"] else None,
        "error": None if validation["is_valid"] else validation["errors"],
    }
    print(result, "result")
    if not result["success"]:
        metrics.failures += 1
    else:
        metrics.regex_hits += 1
    cache_store[text] = result
    return result
