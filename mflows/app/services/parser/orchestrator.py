from app.services.parser.extractors import extract_all
from app.services.parser.intent_mapper import map_intents
from app.services.parser.rule_builder import build_final_rule
from app.services.parser.validator import validate_rule


def needs_llm(mapped: dict):
    action_conf = mapped["action_result"]["confidence"]
    trigger_conf = mapped["trigger_result"]["confidence"]

    return action_conf < 0.5 or trigger_conf < 0.5


def llm_fallback_parse(text: str):
    return {
        "action_result": {"action": None, "confidence": 0.0},
        "trigger_result": {"trigger": None, "confidence": 0.0},
    }


def parse_workflow_text(text: str):
    extracted = extract_all(text)

    mapped = map_intents(text)
    mapped = map_intents(text)
    if needs_llm(mapped):
        llm_result = llm_fallback_parse(text)

        if mapped["action_result"]["action"] is None:
            mapped["action_result"] = llm_result["action_result"]

        if mapped["trigger_result"]["trigger"] is None:
            mapped["trigger_result"] = llm_result["trigger_result"]
    rule = build_final_rule(extracted=extracted, mapped=mapped)

    validation = validate_rule(rule)

    return {
        "input_text": text,
        "extracted": extracted,
        "mapped": mapped,
        "rule": rule,
        "validation": validation,
    }
