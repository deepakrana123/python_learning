from app.parsers.workflow_dragger import parse_dag_workflow

workflow = """

@1:
payment_due send_reminder

@2:
payment_due escalate_case

@3 @depends(@1,@2):
payment_due close_ticket

"""

result = parse_dag_workflow(workflow)

print(result)
