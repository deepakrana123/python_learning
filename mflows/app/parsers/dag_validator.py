def validate_dag(steps):
    errors = []
    step_ids = {step["id"] for step in steps}

    for step in steps:
        current_id = step["id"]
        dependencies = step.get(
            "depends_on",
            [],
        )

        if current_id in dependencies:
            errors.append(f"{current_id} cannot depend on itself")

        for dep in dependencies:
            if dep not in step_ids:
                errors.append(f"{current_id} depends on unknown step {dep}")

    cycle_errors = detect_cycles(steps)
    errors.extend(cycle_errors)
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
    }


def detect_cycles(steps):

    graph = {}

    # initialize all nodes
    for step in steps:

        graph.setdefault(
            step["id"],
            [],
        )

    # build dependency -> dependent graph
    for step in steps:

        current = step["id"]

        for dep in step.get(
            "depends_on",
            [],
        ):

            graph.setdefault(
                dep,
                [],
            ).append(current)

    visited = set()

    visiting = set()

    errors = []

    def dfs(node):

        if node in visiting:

            errors.append(f"Cycle detected at {node}")

            return

        if node in visited:
            return

        visiting.add(node)

        for neighbor in graph.get(node, []):

            dfs(neighbor)

        visiting.remove(node)

        visited.add(node)

    for node in graph:

        dfs(node)

    return errors
