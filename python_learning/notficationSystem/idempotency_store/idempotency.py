import threading


class IdempotencyStore:
    def __init__(self):
        self.store = set()
        self.lock = threading.Lock()

    def generate_key(self, task, channel):
        return f"{task.id}:{channel}"

    def exists(self, key):
        with self.lock:
            return key in self.store

    def mark(self, key):
        with self.lock:
            self.store.add(key)
