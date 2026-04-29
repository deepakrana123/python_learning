from app.workers.celery_app import celery
from app.execution.dispatcher import execute_action


@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def run_workflow(self, action, payload):
    return execute_action(action, payload)
