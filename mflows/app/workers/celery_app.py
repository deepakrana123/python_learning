from celery import Celery  # type: ignore
import os

REDIS_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")


celery = Celery("workflow", broker=REDIS_URL, backend=REDIS_URL)
celery.conf.task_track_started = True
