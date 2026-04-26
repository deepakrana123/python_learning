from sqlalchemy.orm import Session
from app.models.workflow import Workflow


def create(db: Session, name: str, domain: str, raw_input: str, parsed_rule_json=None):
    workflow = Workflow(
        name=name, domain=domain, raw_input=raw_input, parsed_rule_json=parsed_rule_json
    )
    db.add(workflow)
    db.flush()
    return workflow


def get_by_id(db: Session, workflow_id: int):
    return db.query(Workflow).filter(Workflow.id == workflow_id)


def list_by_domain(db: Session, domain: str):
    query = db.query(Workflow)
    if domain:
        query = query.filter(Workflow.domain == domain)
    return query.all()


def delete(db: Session, workflow: Workflow):
    db.delete(workflow)
