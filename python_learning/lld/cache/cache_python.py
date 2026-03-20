import time
from collections import defaultdict, OrderedDict


class Content:
    def __init__(self, content_id, format, size, ttl, popularity, geo_affinity):
        self.id = content_id
        self.format = format
        self.size = size
        self.ttl = ttl
        self.popularity = popularity
        self.timestamp = time.time()
        self.geo_affinity = geo_affinity

    def is_expired(self):
        return (time.time() - self.timestamp) > self.ttl


class CacheNode:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.store = OrderedDict()
        self.frequency = defaultdict(int)

    def has(self, key):
        if key not in self.store:
            return False
        if self.store[key].is_expired():
            self.remove(key)
            return False
        return True

    def get(self, key):
        if self.has(key):
            self.frequency[key] += 1
            self.store.move_to_end(key)
            return self.store[key]
        return None

    def put(self, key, content):
        if key in self.store:
            self.store.move_to_end(key)
        else:
            if len(self.store) >= self.capacity:
                self.evict()
        self.store[key] = content
        self.frequency[key] += 1

    def evict(self):
        least_user = min(self.frequency, key=self.frequency.get)
        self.remove(least_user)

    def remove(self, key):
        if key in self.store:
            del self.store[key]
        if key in self.frequency:
            del self.frequency[key]


class CDNLayer:
    def __init__(self, name):
        self.name = name
        self.local_caches = {}
        self.regional_caches = {}

    def add_cache_layer(self, region, l1_capacity, l2_capacity):
        self.local_caches[region] = CacheNode(f"{region}_L1", l1_capacity)
        self.regional_caches[region] = CacheNode(f"{region}_L2", l2_capacity)

    def fetch_contnet(self, region, content):
        key = (content.id, content.format)
        l1 = self.local_caches.get(region)
        l2 = self.local_caches.get(region)
        if l1 and l1.has(key):
            return l1.get(key)
        elif l2 and l2.has(key):
            return l2.get(key)
        else:
            # Simulate fetching from origin
            print(f"[ORIGIN FETCH] Content {content.id} not found in {region} cache")
            l2.put(key, content)  # Store in L2
            return content


import time
from collections import defaultdict, deque


class SlidingWindowRateLimiter:
    def __init__(self, limit, window_size):
        self.limit = limit
        self.window_size = window_size
        self.user_request = defaultdict(deque)

    def is_allowed(self, user_id):
        current_time = time.time()
        window = self.user_request[user_id]

        while window and window[0] <= current_time - self.window_size:
            window.popleft()


# simple in memoray rate limiter
