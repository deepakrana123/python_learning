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


def enrich_rule(rule: dict, extracted: dict):
    rule = dict(rule or {})
    rule.setdefault("trigger", None)
    rule.setdefault("action", None)
    rule.setdefault("conditions", [])
    rule.setdefault("delay_days", None)
    rule.setdefault("entity_refs", {})
    rule.setdefault("config", {})
    if not isinstance(rule["conditions"], list):
        rule["conditions"] = []

    if not isinstance(rule["entity_refs"], dict):
        rule["entity_refs"] = {}

    if not isinstance(rule["config"], dict):
        rule["config"] = {}
    if extracted.get("days") is not None:
        rule["delay_days"] = extracted["days"]
    refs = extracted.get("entity_refs", {})
    if isinstance(refs, dict):
        rule["entity_refs"].update(refs)
    config = extracted.get("config", {})
    if isinstance(config, dict):
        rule["config"].update(config)
    flags = extracted.get("flags", {})
    if flags.get("vip"):
        rule["conditions"].append("vip=true")
    if flags.get("premium"):
        rule["conditions"].append("premium=true")
    if extracted.get("repeat_count") is not None:
        rule["conditions"].append(f"repeat_count>={extracted['repeat_count']}")
    if extracted.get("amount_threshold") is not None:
        rule["conditions"].append(f"amount>{extracted['amount_threshold']}")
    conds = rule.get("conditions", [])
    if conds is None:
        conds = []
    if not isinstance(conds, list):
        conds = [conds]

    normalized = []
    for item in conds:
        if isinstance(item, dict):
            for k, v in item.items():
                normalized.append(f"{k}={v}")
        else:
            normalized.append(str(item))

    rule["conditions"] = list(dict.fromkeys(normalized))

    return rule


def build_standard_response(
    success: bool,
    source: str,
    rule: dict,
    validation: dict,
    score: float,
    extracted: dict,
    mapped: dict,
):
    return {
        "success": success,
        "source": source,
        "rule": rule,
        "validation": validation,
        "debug": {
            "extracted": extracted,
            "mapped": mapped,
        },
        "score": score,
        "data": rule if success else None,
        "error": None if success else validation["errors"],
    }


def parse_workflow_text(text: str):
    metrics.total_requests += 1
    if text in cache_store:
        metrics.cache_hits += 1
        return cache_store[text]

    extracted = extract_all(text)
    mapped = map_intents(text)
    source = "rules"
    score = 1.0
    if needs_llm(mapped):
        llm_result = parse_workflow_with_llm(text)
        if llm_result["success"]:
            metrics.llm_hits += 1
            base_rule = llm_result.get("data", {})
            score = llm_result.get("score", {})
            source = "llm"
        else:
            metrics.failures += 1
            base_rule = build_final_rule(extracted=extracted, mapped=mapped)
            source = "rules_fallback"

    else:
        base_rule = build_final_rule(extracted=extracted, mapped=mapped)
    final_rule = enrich_rule(base_rule, extracted)
    validation = validate_rule(final_rule)
    if not needs_llm(mapped) and validation["is_valid"]:
        metrics.regex_hits += 1
    result = build_standard_response(
        success=validation["is_valid"],
        source=source,
        rule=final_rule,
        validation=validation,
        score=score,
        extracted=extracted,
        mapped=mapped,
    )
    if not result["success"]:
        metrics.failures += 1
    else:
        metrics.regex_hits += 1
    cache_store[text] = result
    return result
