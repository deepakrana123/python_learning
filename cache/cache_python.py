import time
import threading
import heapq
from collections import defaultdict, OrderedDict


class LFUCacheTTL:
    def __init__(self, capacity, ttl_seconds):
        self.capacity = capacity
        self.ttl_seconds = ttl_seconds
        self.cache = {}
        self.freq_map = defaultdict(OrderedDict)
        self.ttl_heap = []
        self.min_freq = 0
        self.lock = threading.Lock()
        cleanup_thread = threading.Thread(target=self._clean_expired, daemon=True)
        cleanup_thread.start()

    def _is_expired(self, expire_time):
        return time.time() > expire_time

    def get(self, key):
        with self.lock:
            if key not in self.cache:
                return -1
            value, freq, expire_time = self.cache[key]
            if self._is_expired(expire_time):
                self._evict(key)
                return -1
        del self.freq_map[freq][key]
        if not self.freq_map[freq]:
            del self.freq_map[freq]
            if freq == self.min_freq:
                self.min_freq += 1
        new_freq = freq + 1
