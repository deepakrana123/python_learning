# import json
# import time
# from app.core.redis_client import redis_client
# from app.core.logger import logger

# RETRY_QUEUE = "workflow_retry"
# MAIN_QUEUE = "workflow_events"


# def start_retry_worker():
#     while True:
#         try:
#             now = int(time.time())
#             due_events = redis_client.zrangebyscore(RETRY_QUEUE, 0, now)

#             if due_events:
#                 pipeline = redis_client.pipeline()
#                 for raw_event in due_events:
#                     pipeline.zrem(RETRY_QUEUE, raw_event)
#                 removed_counts = pipeline.execute()

#                 for raw_event, removed in zip(due_events, removed_counts):
#                     if removed == 0:
#                         continue

#                     retry_data = json.loads(raw_event)
#                     redis_client.lpush(MAIN_QUEUE, json.dumps(retry_data))

#                     logger.info(
#                         "event_requeued",
#                         extra={"extra_data": {"event_id": retry_data.get("event_id")}},
#                     )

#             time.sleep(1)

#         except Exception as e:
#             logger.error(
#                 "retry_worker_error",
#                 extra={"extra_data": {"error": str(e)}},
#             )
#             time.sleep(1)


# if __name__ == "__main__":
#     start_retry_worker()


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

                if not workflow_execution:
                    logger.error(
                        "retry_execution_missing_entities",
                        extra={"extra_data": payload},
                    )
                    redis_client.zrem(
                        REDIS_RETRY_QUEUE,
                        retry_item,
                    )

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
