from queue import Queue
from collections import defaultdict
import threading

# class IngestionQueue:
#     def __init__(self):
#         self.queue = Queue()

#     def push_to_queue(self, stock_event):
#         self.queue.put(stock_event)

#     def pop_to_queue(self):
#         if self.queue:
#             return self.queue.get()
#         return None


# class NotificationQueue:
#     def __init__(self):
#         self.queue = Queue()

#     def push_to_queue(self, message):
#         self.queue.put(message)

#     def pop_to_queue(self):
#         if self.queue:
#             return self.queue.get()
#         return None


class SimpleQueue:
    def __init__(self):
        self.queue = Queue()

    def push(self, item):
        self.queue.put(item)

    def pop(self):
        return self.queue.get()

    def length(self):
        return self.queue.qsize()


class PartitionQueue:
    def __init__(self):
        self.queues = defaultdict(Queue)
        self.lock = threading.Lock()

    def push(self, stock, item, ts):
        self.queues[stock].put((item, ts))

    def pop(self, stock):
        if not self.queues[stock].empty():
            return self.queues[stock].get()
        return None

    def size(self, stock):
        return self.queues[stock].qsize()

    def total_size(self):
        # return sum(q.qsize() for q in self.queues.values())
        with self.lock:
            queues = list(self.queues.values())

        return sum(q.qsize() for q in queues)


event_queue = SimpleQueue()
notificationQueue = SimpleQueue()
