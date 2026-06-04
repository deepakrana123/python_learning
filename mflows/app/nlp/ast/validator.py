from app.nlp.ast.execptions import ASTValidationError

class ASTValidator:
    def validate(self,ast):
        self._validate_trigger(ast)
        self._validate_steps(ast)
        self._validate_dependencies(ast)
        return True

    def _validate_trigger(self,ast):
        if not ast.trigger:
            raise ASTValidationError("trigger missing")
        if not ast.trigger.event:
            raise ASTValidationError("trigger event missing")

    def _validate_steps(self,ast):
        if not ast.steps:
            raise ASTValidationError("workflow has no steps")
        step_ids=set()

        for step in ast.steps:
            if step.id in step_ids:
                raise ASTValidationError( f"duplicate step id: {step.id}")
            step_ids.add(step.id)

    def _validate_dependencies(self,ast):
        step_ids={s.id for s in ast.steps}
        for step in ast.steps:
            for dep in step.depends_on:
                if dep not in step_ids:
                    raise ASTValidationError(  f"unknown dependency {dep}")
                if dep == step.id:
                    raise ASTValidationError(  f"self dependency {step.id}")