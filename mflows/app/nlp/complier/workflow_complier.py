class WorkflowComplier:
    def complie(self,ast):
        workflow_definition = {
            "trigger": {
                "event_type": ast.trigger_event
            },
            "steps": []
        }

        for step in ast.steps:
            workflow_definition["steps"].append(
                   {
                    "id": step.id,
                    "action": step.action,
                    "depends_on": step.depends_on,
                    "config": {}
                }
            )
        return workflow_definition