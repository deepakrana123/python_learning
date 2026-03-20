import queue


class InMemoryQueue:

    def __init__(self):
        self.q = queue.Queue()

    def push(self, item):
        self.q.put(item)

    def pull(self):
        return self.q.get()
