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
        q = self.queues.get(stock)
        if q and not q.empty():
            return q.get()
        return None

    def peek(self, stock):
        q = self.queues.get(stock)
        if q and not q.empty():
            with q.mutex:
                if len(q.queue) == 0:
                    return None
                return q.queue[0]

    def size(self, stock):
        return self.queues[stock].qsize()

    def total_size(self):
        with self.lock:
            queues = list(self.queues.values())

        return sum(q.qsize() for q in queues)

    def get_all_stock(self):
        with self.lock:
            return list(self.queues.keys())


notificationQueue = SimpleQueue()
