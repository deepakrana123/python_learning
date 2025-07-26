from collections import OrderedDict
import time
import threading


class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


class SimulatedDiskCache:
    def __init__(self):
        self.storage = {}

    def get(self, key):
        time.sleep(0.05)
        return self.storage.get(key)

    def put(self, key, value):
        self.storage[key] = value


class MultiLevelCache:
    def __init__(self, l1_capacity=5):
        self.l1 = LRUCache(capacity=l1_capacity)
        self.l2 = SimulatedDiskCache()

    def get(self, key):
        value = self.l1.get(key)
        if value is not None:
            print(f"[L1 Hit] {key}")
            return value
        value = self.l2.get(key)
        if value is not None:
            print(f"[L2 HIT] {key}")
            self.l1.put(key, value)
            return value
        print(f"[MISS] {key}")
        return None

    def put(self, key, value):
        self.l1.put(key, value)
        self.l2.put(key, value)
        print(f"[Put] {key} =>{value}")


class TTLThreadSafeLRUCache:
    def __init__(self, capacity, default_ttl=30):
        self.capacity = capacity
        self.default_ttl = default_ttl
        self.cache = OrderedDict()
        self.expiry = {}
        self.lock = threading.Lock()

    def _is_expired(self, key):
        return key in self.expiry and time.time() > self.expiry[key]

    def get(self, key):
        with self.lock:
            if key not in self.cache or self._is_expired(key):
                if key in self.cache:
                    print(f"[L1 EXPIRED] {key}")
                    del self.cache[key]
                    del self.expiry[key]
                return None

            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key, value):
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            self.expiry[key] = time.time() + self.default_ttl

            if len(self.cache) > self.capacity:
                oldest_key, _ = self.cache.popitem(last=False)
                del self.expiry[oldest_key]


class TTLThreadSafeSimulatedDiskCache:
    def __init__(self, default_ttl=300):
        self.storage = {}
        self.expiry = {}
        self.lock = threading.Lock()
        self.default_ttl = default_ttl

    def _is_expired(self, key):
        return key in self.expiry and time.time() > self.expiry[key]

    def get(self, key):
        time.sleep(0.05)  # simulate latency
        with self.lock:
            if key not in self.storage or self._is_expired(key):
                if key in self.storage:
                    print(f"[L2 EXPIRED] {key}")
                    del self.storage[key]
                    del self.expiry[key]
                return None
            return self.storage[key]

    def put(self, key, value):
        with self.lock:
            self.storage[key] = value
            self.expiry[key] = time.time() + self.default_ttl


class MultiLevelTTLCache:
    def __init__(self, l1_capacity=5, l1_ttl=60, l2_ttl=300):
        self.l1 = TTLThreadSafeLRUCache(capacity=l1_capacity, default_ttl=l1_ttl)
        self.l2 = TTLThreadSafeSimulatedDiskCache(default_ttl=l2_ttl)

    def get(self, key):
        value = self.l1.get(key)
        if value is not None:
            print(f"[L1 HIT] {key}")
            return value

        value = self.l2.get(key)
        if value is not None:
            print(f"[L2 HIT] {key}")
            self.l1.put(key, value)  # promote to L1
            return value

        print(f"[MISS] {key}")
        return None

    def put(self, key, value):
        print(f"[PUT] {key} => {value}")
        self.l1.put(key, value)
        self.l2.put(key, value)
