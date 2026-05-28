import time
import json
from datetime import datetime, timedelta, timezone
from app.db.session import SessionLocal
from app.models.workflow_execution import WorkflowExecution
from app.models.execution_step import ExecutionStep
from app.core.redis_client import redis_client
from app.core.config import PROCESSING_TIMEOUT_SECONDS
from app.repositories.step_retry_history_repo import record_retry_history
from app.core.logger import logger

BATCH_SIZE = 50
WORKFLOW_EVENTS_QUEUE = "workflow_events"


def start_reaper():
    while True:
        db = SessionLocal()
        try:
            timeout_threshold = datetime.now(timezone.utc) - timedelta(
                seconds=PROCESSING_TIMEOUT_SECONDS
            )

            # FIX H1: was filtering status == "PROCESSING" — that status never exists
            # WorkflowExecution uses RUNNING, not PROCESSING
            stuck_executions = (
                db.query(WorkflowExecution)
                .filter(
                    WorkflowExecution.status == "RUNNING",
                    WorkflowExecution.updated_at < timeout_threshold,
                )
                .limit(BATCH_SIZE)
                .all()
            )

            for execution in stuck_executions:
                # FIX H2: was accessing execution.event_id — WorkflowExecution has no event_id
                # Use execution.id (WorkflowExecution primary key)
                logger.warning(
                    "reaper_recovering_stuck_execution",
                    extra={
                        "extra_data": {
                            "workflow_execution_id": execution.id,
                            "workflow_id": execution.workflow_id,
                            "stuck_since": str(execution.updated_at),
                        }
                    },
                )
                execution.status = "FAILED"
                execution.attempts = (execution.attempts or 0) + 1
                execution.last_error = "timeout_recovery: stuck in RUNNING state"

            # Commit DB first — before any Redis writes
            db.commit()

            for execution in stuck_executions:
                # Write timeout recovery to step retry history for all RUNNING steps
                running_steps = (
                    db.query(ExecutionStep)
                    .filter(
                        ExecutionStep.workflow_execution_id == execution.id,
                        ExecutionStep.status == "RUNNING",
                    )
                    .all()
                )
                for step in running_steps:
                    step.status = "FAILED"
                    step.last_error = "timeout_recovery: parent execution timed out"
                    db.commit()

                    record_retry_history(
                        db=db,
                        step_execution=step,
                        attempt_number=(step.attempts or 0) + 1,
                        trigger="timeout_recovery",
                        status_at_attempt="FAILED",
                        error="reaper: execution timed out in RUNNING state",
                    )

                # Re-queue the execution for retry
                # FIX H2: push workflow_execution_id, not event_id
                retry_payload = {"workflow_execution_id": execution.id}
                redis_client.lpush(WORKFLOW_EVENTS_QUEUE, json.dumps(retry_payload))

                logger.info(
                    "reaper_execution_requeued",
                    extra={
                        "extra_data": {
                            "workflow_execution_id": execution.id,
                            "attempts": execution.attempts,
                        }
                    },
                )

        except Exception as e:
            logger.error(
                "reaper_worker_error",
                extra={"extra_data": {"error": str(e)}},
            )
            db.rollback()

        finally:
            db.close()

        time.sleep(5)


if __name__ == "__main__":
    print("Reaper worker started...", flush=True)
    start_reaper()
