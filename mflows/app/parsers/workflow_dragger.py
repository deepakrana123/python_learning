from app.parsers.workflow_decomposer import (
    parse_workflow_structure,
)

from app.parsers.orchestrator import (
    parse_workflow_text,
)

from app.parsers.dag_validator import validate_dag


def parse_dag_workflow(text: str):

    decomposed_steps = parse_workflow_structure(text)

    parsed_steps = []

    errors = []

    for step in decomposed_steps:

        parsed = parse_workflow_text(step["text"])

        if not parsed["success"]:

            errors.append(
                {
                    "step_id": step["id"],
                    "errors": parsed.get(
                        "error",
                        [],
                    ),
                }
            )

        parsed_steps.append(
            {
                "id": step["id"],
                "depends_on": (step["depends_on"]),
                "rule": parsed.get(
                    "rule",
                    {},
                ),
                "validation": parsed.get(
                    "validation",
                    {},
                ),
                "success": parsed.get(
                    "success",
                    False,
                ),
                "score": parsed.get(
                    "score",
                    0,
                ),
                "source": parsed.get(
                    "source",
                    "unknown",
                ),
            }
        )
    dag_validation = validate_dag(parsed_steps)
    return {
        "success": (len(errors) == 0 and dag_validation["is_valid"]),
        "steps": parsed_steps,
        "validation": {
            "is_valid": (len(errors) == 0 and dag_validation["is_valid"]),
            "errors": (errors + dag_validation["errors"]),
        },
    }
