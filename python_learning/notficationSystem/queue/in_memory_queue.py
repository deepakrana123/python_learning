import heapq
import datetime
import threading


class QueueInterface:
    def push(task):
        pass

    def pull():
        pass

    def is_empty():
        pass

    def peek():
        pass


class InMemoaryQueue(QueueInterface):
    def __init__(self, max_size=1000):
        self.queue = []
        self.count = 0
        self.lock = threading.Lock()
        self.max_size = max_size

    def push(self, item, priority, task_id):
        with self.lock:
            if len(self.queue) >= self.max_size:
                return False
            heapq.heappush(
                self.queue,
                (-priority, datetime.datetime.now(), self.count, task_id, item),
            )
            self.count += 1
            return True

    def pull(self):
        with self.lock:
            if self.queue:
                _, _, _, _, item = heapq.heappop(self.queue)
                return item
            return None

    def size(self):
        with self.lock:
            return len(self.queue)

    def capacity(self):
        return self.max_size


class RetryMemoryQueue(QueueInterface):
    def __init__(self):
        self.retry_queue = []
        self.count = 0
        self.lock = threading.Lock()

    def push(self, item, delay):
        with self.lock:
            next_retry = datetime.datetime.now() + datetime.timedelta(seconds=delay)
            heapq.heappush(self.retry_queue, (next_retry, self.count, item))
            self.count += 1

    def pull(self):
        with self.lock:
            now = datetime.datetime.now()
            if self.retry_queue and self.retry_queue[0][0] <= now:
                _, _, item = heapq.heappop(self.retry_queue)
                return item
            else:
                return None

    def peek(self):
        with self.lock:
            if self.retry_queue:
                next_retry, _, _ = self.retry_queue[0]
                return next_retry
            return None

    def is_empty(self):
        return len(self.retry_queue) == 0


class DLQ:
    def __init__(self):
        self.dlq = []
        self.lock = threading.Lock()

    def push(self, item):
        with self.lock:
            self.dlq.append(item)


class QueueManager:
    def __init__(self, main_queue, retry_queue, dlq):
        self.main_queue = main_queue
        self.retry_queue = retry_queue
        self.dlq = dlq

    def push_main(self, task, priority, task_id):
        self.main_queue.push(task, priority, task_id)

    def push_retry(self, task, delay_second, task_id):
        self.retry_queue.push(task, delay_second, task_id)

    def push_dlq(self, task):
        self.dlq.push(task)

    def pull_task(self):
        now = datetime.datetime.now()
        if not self.retry_queue.is_empty():
            next_retry = self.retry_queue.peek()
            if next_retry and next_retry <= now:
                return self.retry_queue.pull()
        return self.main_queue.pull()
