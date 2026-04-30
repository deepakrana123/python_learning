from app.workers.celery_app import celery
from app.execution.dispatcher import execute_action
from app.core.logger import logger


@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def run_workflow(self, action, payload):
    logger.info(
        "celery_task_started",
        extra={
            "extra_data": {
                "task_id": self.request.id,
                "action": action,
                "retries": self.request.retries,
            }
        },
    )
    try:
        result = execute_action(action, payload)
        logger.info(
            "celery_task_success",
            extra={
                "extra_data": {
                    "task_id": self.request.id,
                    "action": action,
                    "result": result,
                }
            },
        )
        return result
    except Exception as e:
        logger.error(
            "celery_task_failed",
            extra={
                "extra_data": {
                    "task_id": self.request.id,
                    "action": action,
                    "error": str(e),
                    "retries": self.request.retries,
                    "max_retries": self.max_retries,
                }
            },
        )
        raise
