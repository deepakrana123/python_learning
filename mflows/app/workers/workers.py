import json
from app.core.redis_client import redis_client
from app.db.session import SessionLocal
from app.execution.runtime_processor import runtime_processor
from app.core.logger import logger


def start_worker():
    print("Polling queue...", flush=True)
    logger.info("workflow_worker_started")
    while True:
        try:
            item = redis_client.brpop("workflow_events", timeout=5)
            if not item:
                continue
            _, raw = item
            payload = json.loads(raw)

            # FIX C5: was passing full event dict — runtime_processor takes workflow_execution_id
            workflow_execution_id = payload.get("workflow_execution_id")
            if not workflow_execution_id:
                logger.error(
                    "worker_missing_workflow_execution_id",
                    extra={"extra_data": {"payload": payload}},
                )
                continue

            logger.info(
                "workflow_event_received",
                extra={"extra_data": {"workflow_execution_id": workflow_execution_id}},
            )

            db = SessionLocal()
            try:
                runtime_processor(db=db, workflow_execution_id=workflow_execution_id)
            finally:
                db.close()

        except Exception as e:
            logger.error(
                "workflow_worker_processing_failed",
                extra={"extra_data": {"error": str(e)}},
            )


if __name__ == "__main__":
    start_worker()
