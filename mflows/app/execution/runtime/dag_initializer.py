from app.execution.runtime.step_execution_service import create_step_execution
from app.execution.runtime.step_execution_service import mark_step_blocked


def initialize_dag_steps(db, workflow_execution, workflow_steps, payload):
    created_steps = []

    for step_def in workflow_steps:
        depends_on = step_def.get("depends_on")
        initial_status = {"BLOCKED" if depends_on else "PENDING"}
        step = create_step_execution(
            db=db,
            workflow_execution_id=workflow_execution.id,
            step_name=step_def["rule"]["action"],
            input_payload=payload,
            step_id=step_def["id"],
            depends_on=depends_on,
            status=initial_status,
        )
        print(step, "step")

        created_steps.append(step)
        return created_steps
