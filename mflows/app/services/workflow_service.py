from sqlalchemy.orm import Session
from app.schemas.workflow import WorkflowCreate
from app.repositories import workflow
from app.parsers.orchestrator import parse_workflow_text
from app.core.logger import logger

ALLOWED_DOMAINS = {"support", "loan"}


def create_workflow_service(payload: WorkflowCreate, db: Session):
    if payload.domain not in ALLOWED_DOMAINS:
        logger.warning(
            "workflow_invalid_domain",
            extra={"extra_data": {"domain": payload.domain}},
        )
        raise ValueError("Invalid domain")

    parse_result = parse_workflow_text(payload.raw_input)
    if not parse_result["validation"]["is_valid"]:
        logger.warning(
            "workflow_parse_invalid",
            extra={
                "extra_data": {
                    "errors": parse_result["validation"]["errors"],
                    "raw_input": payload.raw_input[:100],
                }
            },
        )
        raise ValueError("Workflow text is invalid")

    workflows = workflow.create(
        db=db,
        name=payload.name,
        domain=payload.domain,
        raw_input=payload.raw_input,
        parsed_rule_json=parse_result.get("data", {}),
    )
    db.commit()
    db.refresh(workflows)
    logger.info(
        "workflow_created",
        extra={
            "extra_data": {
                "workflow_id": workflows.id,
                "name": workflows.name,
                "domain": workflows.domain,
                "parse_source": parse_result.get("source"),
            }
        },
    )
    return workflows


def get_by_id(workflow_id: int, db: Session):
    workflow = workflow.get_by_id(db, workflow_id)
    if not workflow:
        logger.warning(
            "workflow_not_found",
            extra={"extra_data": {"workflow_id": workflow_id}},
        )
        raise ValueError("Workflow not found")
    return workflow


def list_by_domain(domain: str | None, db: Session):
    return workflow.list_by_domin(domain)


def debug_parse(raw_text: str):
    logger.info(
        "debug_parse_called",
        extra={"extra_data": {"raw_text_preview": raw_text[:100]}},
    )
    return parse_workflow_text(raw_text)
