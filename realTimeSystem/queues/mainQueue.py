from queue import Queue, Empty
from collections import defaultdict
import threading


class PartitionQueue:
    def __init__(self):
        self._queues: dict[str, Queue] = {}
        self._lock = threading.Lock()

    def _get_or_create(self, stock: str) -> Queue:
        q = self._queues.get(stock)
        if q is None:
            with self._lock:
                q = self._queues.get(stock)
                if q is None:
                    q = Queue()
                    self._queues[stock] = q
        return q

    def push(self, stock: str, item, ts: float) -> None:
        self._get_or_create(stock).put((item, ts))

    def pop(self, stock: str, timeout: float = 0.05):
        q = self._queues.get(stock)
        if q is None:
            return None
        try:
            return q.get(timeout=timeout)
        except Empty:
            return None

    def peek(self, stock: str):
        q = self._queues.get(stock)
        if q is None:
            return None
        with q.mutex:
            return q.queue[0] if q.queue else None

    def size(self, stock: str) -> int:
        q = self._queues.get(stock)
        return q.qsize() if q is not None else 0

    def total_size(self) -> int:
        with self._lock:
            queues = list(self._queues.values())
        return sum(q.qsize() for q in queues)

    def stocks(self) -> list[str]:
        with self._lock:
            return list(self._queues.keys())
