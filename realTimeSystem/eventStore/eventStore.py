import threading



class EventStore:
    def __init__(self):
        self.store = {}
        self.lock = threading.Lock()

    def set(self, stock, event):
        with self.lock:
            self.store[stock] = event

    def get(self, stock):
        with self.lock:
            return self.store.get(stock)
