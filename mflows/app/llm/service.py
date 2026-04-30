import json
from app.llm.llmManager import LLMManager
from app.llm.validator import validate_workflow_json
from app.llm.repair import repair_json
from app.core.logger import logger


manager = LLMManager()


def clean_json(text: str):
    return text.replace("```json", "").replace("```", "").strip()


def parse_workflow_with_llm(raw_text: str):
    result = manager.call(raw_text)
    if not result["success"]:
        logger.error(
            "llm_all_providers_failed",
            extra={"extra_data": {"errors": result.get("errors")}},
        )
        return result

    raw_output = result["text"]
    logger.debug("llm_raw_output", extra={"extra_data": {"output_preview": raw_output[:100]}})

    try:
        parsed = json.loads(clean_json(raw_output))
    except Exception as e:
        logger.warning(
            "llm_json_parse_failed_attempting_repair",
            extra={"extra_data": {"error": str(e)}},
        )
        repaired = repair_json(raw_output)
        if not repaired["success"]:
            logger.error("llm_json_repair_failed")
            return {"success": False, "error": "invalid json"}
        parsed = repaired["data"]
        logger.info("llm_json_repaired_successfully")

    valid = validate_workflow_json(parsed)
    if not valid["is_valid"]:
        logger.error(
            "llm_validation_failed",
            extra={"extra_data": {"errors": valid["errors"]}},
        )
        return {"success": False, "error": valid["errors"]}

    logger.info(
        "llm_parse_success",
        extra={
            "extra_data": {
                "provider": result["provider"],
                "score": result.get("score", 0),
            }
        },
    )
    return {
        "success": True,
        "source": result["provider"],
        "score": result.get("score", 0),
        "data": parsed,
        "provider": result["provider"],
    }
