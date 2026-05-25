from app.models.execution_step import ExecutionStep


def unlock_blocked_steps(db, workflow_execution_id):
    all_steps = (
        db.query(ExecutionStep)
        .filter(ExecutionStep.workflow_execution_id == workflow_execution_id)
        .all()
    )

    step_map = {step.step_id: step for step in all_steps}
    for step in all_steps:
        if step.status != "BLOCKED":
            continue
        deps = step.depends_on or []

        all_completed = all(
            step_map[d].status == "COMPELETED" for d in deps if d in step_map
        )
        if all_completed:
            step.status = "PENDING"
    db.commit()


def get_runnable_steps(db, workflow_execution_id):

    return (
        db.query(ExecutionStep)
        .filter(
            ExecutionStep.workflow_execution_id == workflow_execution_id,
            ExecutionStep.status == "PENDING",
        )
        .all()
    )


def get_ready_steps(dag_steps, completed_steps, failed_steps):
    ready = []
    for step in dag_steps:
        step_id = step["id"]

        if step_id in completed_steps:
            continue

        if step_id in failed_steps:
            continue

        depends_on = step.get("depends_on", [])
        dependencies_satisfied = all(dep in completed_steps for dep in depends_on)

        if dependencies_satisfied:
            ready.append(step)
    return ready
