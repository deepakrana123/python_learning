import json
import time
from app.db.session import SessionLocal
from app.execution.constants import REDIS_RETRY_QUEUE
from app.core.redis_client import redis_client
from app.models.workflow_execution import WorkflowExecution
from app.models.execution_step import ExecutionStep
from app.execution.runtime.retry_executor import execute_retry

from app.core.logger import logger

POLL_INTERVAL = 5


def start_retry_worker():
    while True:
        db = SessionLocal()
        try:
            now = int(time.time())
            retries = redis_client.zrangebyscore(REDIS_RETRY_QUEUE, 0, now)
            for retry_item in retries:
                payload = json.loads(retry_item)
                removed = redis_client.zrem(
                    REDIS_RETRY_QUEUE,
                    retry_item,
                )

                if removed == 0:
                    continue
                workflow_execution = (
                    db.query(WorkflowExecution)
                    .filter(WorkflowExecution.id == payload["workflow_execution_id"])
                    .first()
                )
                step_execution = (
                    db.query(ExecutionStep)
                    .filter(ExecutionStep.id == payload["step_execution_id"])
                    .first()
                )

                if not workflow_execution or not step_execution:
                    logger.error(
                        "retry_execution_missing_entities",
                        extra={"extra_data": payload},
                    )
                    redis_client.zrem(
                        REDIS_RETRY_QUEUE,
                        retry_item,
                    )

                    continue
                if workflow_execution.status == "COMPLETED":
                    continue

                if step_execution.status == "COMPLETED":
                    continue
                execute_retry(
                    db=db,
                    workflow_execution=workflow_execution,
                    step_execution=step_execution,
                )
                redis_client.zrem(
                    REDIS_RETRY_QUEUE,
                    retry_item,
                )

        except Exception as e:
            logger.exception(
                "retry_worker_failed",
                extra={
                    "extra_data": {
                        "error": str(e),
                    }
                },
            )
        finally:
            db.close()
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    start_retry_worker()
