import threading
import time
from collections import OrderedDict
import os


class CDNMemoryCache:
    def __init__(self, capacity=5, ttl=60):
        self.capacity = capacity
        self.ttl = ttl
        self.cache = OrderedDict()
        self.expiry = {}
        self.lock = threading.Lock()

    def _is_expired(self, key):
        return key in self.expiry and time.time() < self.expiry[key]

    def get(self, key):
        with self.lock:
            if key not in self.cache or self._is_expired(key):
                self.cache.pop(key, None)
                self.expiry.pop(key, None)
                return None
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key, value):
        with self.lock:
            self.cache[key] = value
            self.expiry[key] = time.time() + self.ttl
            self.cache.move_to_end(key)
            if len(self.cache) > self.capacity:
                old_key, _ = self.cache.popitem(last=False)
                self.expiry.pop(old_key, None)


class CDNDiskCache:
    def __init__(self, path="./cdn_disk", ttl=30):
        self.path = path
        self.ttl = ttl
        os.makedirs(self.path, exist_ok=True)

    def _file_path(self, key):
        return os.path.join(self.path, key)

    def get(self, key):
        try:
            file_path = self._file_path(key)
            if not os.path.exists(file_path):
                return None

            with open(file_path, "r") as f:
                expiry_line = f.readline().strip()
                expiry = float(expiry_line)
                if time.time() > expiry:
                    os.remove(file_path)
                    return None
                content = f.read()
                return content
        except:
            return None

    def put(self, key, value):
        try:
            file_path = self._file_path(key)
            with open(file_path, "w") as f:
                expiry = time.time() + self.ttl
                f.write(f"{expiry}\n{value}")
        except:
            pass


class CDNCacheSystem:
    def __init__(self, memory_capacity=5, memory_ttl=60, disk_ttl=300):
        self.l1 = CDNMemoryCache(capacity=memory_capacity, ttl=memory_ttl)
        self.l2 = CDNDiskCache(ttl=disk_ttl)

    def fetch_from_origin(self, key):
        time.sleep(0.2)  # Simulate origin fetch latency
        return f"Content for {key} from origin"

    def get(self, key):
        content = self.l1.get(key)
        if content:
            print(f"[L1 HIT] {key}")
            return content

        content = self.l2.get(key)
        if content:
            print(f"[L2 HIT] {key}")
            self.l1.put(key, content)  # promote to L1
            return content

        print(f"[MISS] {key} → Fetching from origin")
        content = self.fetch_from_origin(key)
        self.l1.put(key, content)
        self.l2.put(key, content)
        return content
