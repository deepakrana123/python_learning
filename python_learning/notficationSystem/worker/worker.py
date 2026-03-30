from enum import Enum


class Action(Enum):
    SUCCESS = "SUCCESS"
    RETRY = "RETRY"
    FALLBACK = "FALLBACK"
    DLQ = "DLQ"
    SKIP = "SKIP"


from ..queue.in_memory_queue import QueueManager
import threading
from ..idempotency_store.idempotency import IdempotencyStore
from ..retry_manager.retry_manager import RetryManager
import time


class TaskProcessor:
    def __init__(
        self,
        queue_manager: QueueManager,
        channel_manager: ChannelManager,
    ):
        self.queue_manager = queue_manager
        self.channel_manager = channel_manager

    def process(self, task):
        current_channel = task.channels[task.current_channel_index]

        process_status = self.send(task, current_channel)
        if process_status:
            return Action.SUCCESS
        else:
            if task.attempt < task.max_attempts:
                task.attempt += 1
                return Action.RETRY
            elif task.current_channel_index < len(task.channels) - 1:
                task.current_channel_index += 1
                task.attempt = 0
                return Action.FALLBACK
            else:
                return Action.DLQ

    def send(self, task, current_channel):
        return self.channel_manager.send(task, current_channel)


class Worker:
    def __init__(
        self,
        task_process: TaskProcessor,
        queue_manager: QueueManager,
        retry_manager: RetryManager,
        idempotency_store: IdempotencyStore,
    ):
        self.processor = task_process
        self.queue_manager = queue_manager
        self.retry = retry_manager
        self.idempotency_store = idempotency_store

    def process(self):
        task = self.queue_manager.pull_task()
        if not task:
            time.sleep(0.5)

            return
        key = self.idempotency_store.generate_key(
            task, task.channels[task.current_channel_index]
        )
        if self.idempotency_store.exists(key):
            return
        actions = self.processor.process(task)
        if actions == Action.SUCCESS:
            self.idempotency_store.mark(key)
        elif actions == Action.RETRY:
            delay = self.retry.get_backoff_delay(task.attempt)
            self.queue_manager.push_retry(task, delay)
        elif actions == Action.FALLBACK:
            self.queue_manager.push_main(task, task.priority, task.task_id)
        elif actions == Action.DLQ:
            self.queue_manager.push_dlq(task)


class WorkerPool:
    def __init__(self, num_workers, worker):
        self.worker = worker
        self.num_workers = num_workers
        self.threads = []
        self.stop_event = threading.Event()

    def start(self):
        for _ in range(self.num_workers):
            t = threading.Thread(target=self.run)
            t.start()
            self.threads.append(t)

    def stop(self):
        self.stop_event.set()
        for t in self.threads:
            t.join()

    def run(self):
        while not self.stop_event.is_set():
            self.worker.process()
