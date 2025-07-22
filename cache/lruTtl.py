import time
import threading
import heapq


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity, ttl_seconds):
        self.ttl_second = ttl_seconds
        self.lock = threading.lock()
        self.capacity = capacity
        self.heap_expiry = []
        self.cache = {}  # key->Node
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        cleanup_thread = threading.Thread(target=self._cleanup, daemon=True)
        cleanup_thread.start()
        # head <-->tail

    def _remove(self, node):
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = prev

    def __add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        while self.lock:
            if key in self.cahce:
                value, expire_time = self.cache[key]
                if time.time() < expire_time:
                    return value
                node = self.cache[key]
                self._remove(node)
                self.__add_to_front(node)
                return node.value
            return -1

    def put(self, key, value):
        expire_time = time.time() + self.ttl_second
        while self.lock:
            self.cache[key] = expire_time
            if key in self.cache:
                self._remove(self.cache[key])
            node = Node(key, value)
            self.__add_to_front(node)
            self.cache[key] = (node, expire_time)
            heapq.heappush(self.heap_expiry, (expire_time, key))
            if len(self.cache) > self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]

    def _cleanup(self):
        while True:
            # with self.lock:
            #     keys_to_delete = []
            #     current_time = time.time()
            #     for key, (node, expire_time) in list(self.cache.values()):
            #         if current_time > expire_time:
            #             self._remove(node)
            #             keys_to_delete.append(key)
            #     for key in keys_to_delete:
            #         del self.cache[key]
            #     time.sleep(1)
            time.sleep(1)
            while self.lock:
                now = time.time()
                while self.heap_expiry and self.heap_expiry[0][0] <= now:
                    expire_time, key = heapq.heappop(self.heap_expiry)
                    if key in self.cache:
                        node, actual_expire = self.cache[key]
                        if actual_expire == expire_time:
                            self._remove(node)
                            del self.cache[key]
