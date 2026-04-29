from sqlalchemy.orm import Session
from app.schemas.workflow import WorkflowCreate
from app.repositories import workflow
from app.parsers.orchestrator import parse_workflow_text

ALLOWED_DOMAINS = {"support", "loan"}


def create_workflow_service(payload: WorkflowCreate, db: Session):
    if payload.domain not in ALLOWED_DOMAINS:
        raise ValueError("Invalid domain")
    parse_result = parse_workflow_text(payload.raw_input)
    if not parse_result["validation"]["is_valid"]:
        raise ValueError("Workflow text is invalid")
    print(parse_result, "parse_result")
    workflows = workflow.create(
        db=db,
        name=payload.name,
        domain=payload.domain,
        raw_input=payload.raw_input,
        parsed_rule_json=parse_result.get("data", {}),
    )
    db.commit()
    db.refresh(workflows)
    return workflows


def get_by_id(workflow_id: int, db: Session):
    workflow = workflow.get_by_id(db, workflow_id)
    if not workflow:
        raise ValueError("Workflow not found")
    return workflow


def list_by_domain(domain: str | None, db: Session):
    return workflow.list_by_domin(domain)


def debug_parse(raw_text: str):
    return parse_workflow_text(raw_text)
