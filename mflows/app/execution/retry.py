import time
import json
from app.execution.constants import REDIS_RETRY_QUEUE, REDIS_DLQ
from app.core.redis_client import redis_client
from app.core.logger import logger
from app.execution.retry_policy import calculate_delay


def handle_retry_event(
    workflow_execution,
    step_execution,
    attempts,
    error,
):

    delay = calculate_delay(attempts)
    retry_at = int(time.time()) + delay
    retry_payload = {
        "version": 1,
        "workflow_execution_id": workflow_execution.id,
        "step_execution_id": step_execution.id,
        "attempt": attempts,
        "retry_at": retry_at,
        "correlation_id": workflow_execution.event_id,
    }

    redis_client.zadd(
        REDIS_RETRY_QUEUE,
        {json.dumps(retry_payload): retry_at},
    )

    logger.warning(
        "workflow_retry_scheduled",
        extra={
            "extra_data": {
                "version": 1,
                "workflow_execution_id": workflow_execution.id,
                "workflow_id": workflow_execution.workflow_id,
                "step_execution_id": step_execution.id,
                "attempt": attempts,
                "retry_in_seconds": delay,
                "error": str(error),
                "correlation_id": workflow_execution.event_id,
            }
        },
    )


def handle_dlq_event(
    workflow_execution,
    step_execution,
    attempts,
    error,
):

    dlq_payload = {
        "failed_at": int(time.time()),
        "version": 1,
        "workflow_execution_id": workflow_execution.id,
        "step_execution_id": step_execution.id,
        "attempt": attempts,
        "correlation_id": workflow_execution.event_id,
    }

    redis_client.lpush(
        REDIS_DLQ,
        json.dumps(dlq_payload),
    )

    logger.error(
        "workflow_pushed_to_dlq",
        extra={
            "extra_data": {
                "workflow_execution_id": workflow_execution.id,
                "workflow_id": workflow_execution.workflow_id,
                "step_execution_id": step_execution.id,
                "attempts": attempts,
                "error": str(error),
                "correlation_id": workflow_execution.event_id,
            }
        },
    )
