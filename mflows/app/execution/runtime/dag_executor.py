from app.execution.runtime.dag_scheduler import get_ready_steps
# from app.execution.runtime.step_runner import execute_workflow_step  # OLD: wrong module name — file is step_executor.py
from app.execution.runtime.step_executor import execute_workflow_step
from app.core.logger import logger


def run_dag_execution(
    db,
    workflow_execution,
    dag,
    payload,
):
    steps = dag.get("steps", [])
    completed_steps = set()
    failed_steps = set()

    while True:
        ready_steps = get_ready_steps(
            dag_steps=steps, completed_steps=completed_steps, failed_steps=failed_steps
        )
        if not ready_steps:
            break

        for step in ready_steps:
            result = execute_workflow_step(
                db=db,
                workflow_execution=workflow_execution,
                step_definition=step,
                payload=payload,
            )

            if result["success"]:
                completed_steps.add(step["id"])
            else:
                failed_steps.add(step["id"])

                logger.warning(
                    "dag_step_failed",
                    extra={
                        "extra_data": {
                            "workflow_execution_id": workflow_execution.id,
                            "step_id": step["id"],
                        }
                    },
                )

                # FIX: use break instead of return so while loop exits cleanly
                # and finalize_workflow_execution is always called by runtime_processor
                # OLD: return  — skipped finalizer for remaining ready steps in same iteration
                break

        else:
            # inner for loop completed without break — continue while loop
            continue
        # inner for loop hit break (step failed) — exit while loop too
        break
