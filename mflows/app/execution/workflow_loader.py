from app.models.workflow import Workflow


def load_active_workflows(db):
    return (
        db.query(Workflow)
        .filter(Workflow.status == "active")
        .order_by(Workflow.priority.desc())
        .all()
    )
