from app.nlp.parsers import RuleParser
from app.nlp.ast.builder import WorkflowASTBuilder
from app.nlp.ast.validator import WorkflowASTValidator
from app.nlp.complier.workflow_complier import WorkflowComplier
class WorkflowCompilerService:

    def compile_dsl(self, dsl_text):

        nodes = RuleParser().parse(dsl_text)

        ast = WorkflowASTBuilder().build(nodes)

        WorkflowASTValidator().validate(ast)

        return WorkflowComplier().compile(ast)