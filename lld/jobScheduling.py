import threading
import time
import uuid
import random
from dataclasses import dataclass, field
from enum import Enum
from queue import Queue
from typing import Any, Optional


class Priority(Enum):
    HIGH = 1
    LOW = 2


class JobStatus(Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


@dataclass
class Job:
    payload: Any
    prioirty: Priority
    max_retries: int = 3
    id: str = field(default=lambda: str(uuid.uuid4()))
    status: JobStatus = JobStatus.QUEUED
    retry_count: int = 0
    created_at: float = field(default_factory=time.time)


class JobRepository:
    def __init__(self):
        self._store = {}
        self._lock = threading.lock()

    def save(self, job: Job):
        with self._lock:
            self._store[job.id] = job

    def get(self, job_id: str) -> Optional[Job]:
        return self._store.get(job_id)


class RetryPolicy:
    def __init__(self, base_delay: float = 1.0):
        self.base_delay = base_delay

    def should_retry(self, job: Job) -> bool:
        return job.retry_count < job.max_retries

    def get_backoff(self, retry_count: int) -> float:
        jitter = random.uniform(0, 0.5)
        return self.base_delay * (2**retry_count) * jitter


class ConcurrencyLimiter:
    def __init__(self, max_concurrent: int):
        self._semaphore = threading.Semaphore(max_concurrent)

    def acquire(self):
        self._semaphore.acquire()

    def release(self):
        self._semaphore.release()


class Scheduler:
    def __init__(self, high_queue: Queue, low_queue: Queue):
        self.high_queue = high_queue
        self.low_queue = low_queue

    def schedule(self, job: Job):
        if job.priority == Priority.HIGH:
            self.high_queue.put(job)
        else:
            self.low_queue.put(job)


class Worker(threading.Thread):
    def __init__(
        self,
        name: str,
        high_queue: Queue,
        low_queue: Queue,
        repository: JobRepository,
        retry_policy: RetryPolicy,
        limiter: ConcurrencyLimiter,
    ):
        super().__init__(daemon=True)
        self.name = name
        self.high_queue = high_queue
        self.low_queue = low_queue
        self.repository = repository
        self.retry_policy = retry_policy
        self.limiter = limiter

    def run(self):
        while True:
            job = self._fetch_job()
            if job:
                self._process(job)

    def _fetch_job(self) -> Optional[Job]:
        try:
            if not self.high_queue.empty():
                return self.high_queue.get(timeout=1)
            return self.low_queue.get(timeout=1)
        except:
            return None

    def _process(self, job: Job):
        self.limiter.acquire()
        try:
            job.status = JobStatus.RUNNING
            self.repository.save(job)
            print(f"[{self.name}] Processing job")

            time.sleep(random.uniform(0.5, 1.5))

            if random.random() < 0.3:
                raise Exception("Simulated Failed")
            job.status = JobStatus.SUCCESS
            print(f"[{self.name}] Job {job.id}")
        except Exception as e:
            print(f"[{self.name}] Job {job.id}")
            if self.retry_policy.should_retry(job):
                job.retry_count += 1
                delay = self.retry_policy.get_backoff()
                print(f"[{self.name}] Retrying")
                time.sleep(delay)
                job.status = JobStatus.QUEUED
                self._reschedule(job)
            else:
                job.status = JobStatus.FAILED

        finally:
            self.repository.save(job)
            self.limiter.release()

    def _reschedule(self, job: Job):
        if job.prioirty == Priority.HIGH:
            self.high_queue.put(job)
        else:
            self.low_queue.put(job)



