import time
import threading
import heapq


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LFUCache:
    def __init__(self, capacity, ttl_seconds):
        self.ttl_second = ttl_seconds
        self.lock = threading.lock()
        self.capacity = capacity
        self.frequency_count = {}
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
        with self.lock:
            if key in self.cahce:
                node, expire_time = self.cache[key]
                if time.time() < expire_time:
                    self._remove(node)
                    del self.cache[key]
                    del self.frequency_count[key]
                    return -1
                node = self.cache[key]
                self.frequency_count[key] = self.frequency_count.get(key, 0) + 1
                self._remove(node)
                self.__add_to_front(node)
                return node.value
            return -1

    def getMinimumValue(self, dicts):
        minValue = float("inf")
        key_to_remove = -1
        for key in dicts:
            value = dicts[key]
            if value < minValue:
                minValue = value
                key_to_remove = key
        return key_to_remove

    def put(self, key, value):
        while self.lock:
            expire_time = time.time() + self.ttl_second
            if self.capacity == 0:
                return
            if key in self.cache:
                node, _ = self.cache[key]
                self._remove(self.cache[key])
            if len(self.cache) > self.capacity:
                key_to_delete = self.getMinimumValue(self.cache)
                if key_to_delete is not None:
                    node_to_delete, _ = self.cache[key_to_delete]
                    self._remove(node_to_delete)
                    del self.cache[key_to_delete]
                    del self.frequency_count[key_to_delete]
            node = Node(key, value)
            self.__add_to_front(node)
            self.cache[key] = (node, expire_time)
            self.frequency_count[key] = self.frequency_count.get(key, 0) + 1
            heapq.heappush(self.heap_expiry, (expire_time, key))

    def _cleanup(self):
        while True:
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
                            if key in self.frequency_count:
                                del self.frequency_count[key]
