import json
import time
from datetime import datetime, timezone
from app.db.session import SessionLocal
from app.execution.constants import REDIS_RETRY_QUEUE
from app.core.redis_client import redis_client
from app.models.workflow_execution import WorkflowExecution
from app.models.execution_step import ExecutionStep
from app.execution.runtime.retry_executor import execute_retry
from app.repositories.step_retry_history_repo import record_retry_history
from app.core.logger import logger

POLL_INTERVAL = 5


def start_retry_worker():
    while True:
        db = SessionLocal()
        try:
            now = int(time.time())
            due_items = redis_client.zrangebyscore(REDIS_RETRY_QUEUE, 0, now)

            if due_items:
                # FIX H3: atomic pipeline — zrem all due items before processing
                # OLD: zrangebyscore then individual zrem — two workers could claim same item
                pipeline = redis_client.pipeline()
                for item in due_items:
                    pipeline.zrem(REDIS_RETRY_QUEUE, item)
                removed_counts = pipeline.execute()

                for retry_item, removed in zip(due_items, removed_counts):
                    if removed == 0:
                        # Another worker already claimed this item
                        continue

                    payload = json.loads(retry_item)

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
                        continue

                    if workflow_execution.status == "COMPLETED":
                        continue

                    if step_execution.status in ("COMPLETED", "DLQ"):
                        continue

                    retry_executed_at = datetime.now(timezone.utc)

                    execute_retry(
                        db=db,
                        workflow_execution=workflow_execution,
                        step_execution=step_execution,
                    )

                    # Write retry execution history
                    record_retry_history(
                        db=db,
                        step_execution=step_execution,
                        attempt_number=payload.get("attempt", 1),
                        trigger="retry",
                        status_at_attempt=step_execution.status,
                        error=None,
                        retry_scheduled_at=datetime.fromtimestamp(
                            payload.get("retry_at", now), tz=timezone.utc
                        ),
                        retry_executed_at=retry_executed_at,
                    )

        except Exception as e:
            logger.exception(
                "retry_worker_failed",
                extra={"extra_data": {"error": str(e)}},
            )
        finally:
            db.close()

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    start_retry_worker()
