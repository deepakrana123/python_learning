from app.nlp.ast.schema import (
    WorkflowAST,
    ASTStep
)


class WorkflowASTBuilder:
    def build(self,parsed_nodes):
        if not parsed_nodes:
            raise ValueError("No nodes found")
        trigger_event=parsed_nodes[0].event
        steps=[]

        for node in parsed_nodes:
            steps.append(
                ASTStep(
                      id=node.step_id,
                    action=node.action,
                    depends_on=node.depends_on,
                )
            )
        return WorkflowAST(
             trigger_event=trigger_event,
            steps=steps,
        )