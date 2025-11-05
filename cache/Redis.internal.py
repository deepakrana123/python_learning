import time
import heapq
import threading


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity, ttl_seconds):
        self.ttl_seconds = ttl_seconds
        self.cache = {}
        self.heap_expiry = []
        self.lock = threading.Lock()
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.capacity = capacity
        self.head.next = self.tail
        self.tail.prev = self.head
        cleanup_thread = threading.Thread(target=self._cleanup, daemon=True)
        cleanup_thread.start()

    def __remove(self, node):
        prev = node.prev
        next = node.next
        prev.next = next
        next.prev = prev

    def __add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        with self.lock:
            if key not in self.cache:
                return -1
            if key in self.cache:
                value, expire_time = self.cache[key]
                if time.time() < expire_time:
                    self.__remove(node)
                    del self.cache[key]
                    return -1
                node = self.cache[key]
                self.__remove(node)
                self.__add_to_front(node)
                return node.value

    def put(self, key, value):
        expirey_time = time.time() + self.ttl_seconds
        with self.lock:
            if key in self.cache:
                self.__remove(self.cache[key])
            node = Node(key, value)
            self.__add_to_front(node)
            self.cache[key] = node
            heapq.heappush(self.heap_expiry, (expirey_time, key))
            if len(self.cache) > self.capacity:
                lru = self.tail.prev
                self.__remove(lru)
                del self.cache[lru.key]

    def _cleanup(self):
        while True:
            time.sleep(1)
            now = time.time()
            while self.heap_expiry and self.heap_expiry[0][0] > now:
                expire_time, key = heapq.heappop(self.heap_expiry)
                if key in self.cache:
                    node, actual_expire = self.cache[key]
                    if actual_expire == expire_time:
                        self.__remove(node)
                        del self.cache[node.key]


class LFUCahce:
    def __init__(self, capacity, ttl_seconds):
        self.ttl_second = ttl_seconds
        self.lock = threading.Lock()
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

    def __remove(self, node):
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = node

    def __add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        with self.lock:
            if key not in self.cache:
                return -1
            node, expire_time = self.cache[key]
            if expire_time < time.time():
                self.__remove(node)
                del self.cache[key]
                del self.frequency_count[key]
                return -1
            node = self.cache[key]
            self.__remove(node)
            self.__add_to_front(node)
            self.frequency_count[key] += 1
            return node.value

    def getMinimumValue(self):
        minValue = float("inf")
        key_to_remove = -1
        for key in self.frequency_count:
            if minValue > self.frequency_count[key]:
                minValue = self.frequency_count[key]
                key_to_remove = key
        return key_to_remove

    def put(self, key, value):
        with self.lock:
            expiry_time = time.time() + self.ttl_second
            if self.capacity == 0:
                return
            if key in self.cache:
                node, _ = self.cache[key]
                self.__remove(node)
            if len(self.cache) > self.capacity:
                key_to_delete = self.getMinimumValue()
                if key_to_delete is not None:
                    node_to_delete, _ = self.cache[key_to_delete]
                    self.__remove(node_to_delete)
                    del self.cache[key_to_delete]
                    del self.frequency_count[key_to_delete]
            node = Node(key, value)
            self.__add_to_front(node)
            self.cache[key] = (node, expiry_time)
            self.frequency_count[key] = self.frequency_count.get(key, 0) + 1
            heapq.heappush(self.heap_expiry, (expiry_time, key))

    def _cleanup(self):
        while True:
            time.sleep(1)
            with self.lock:
                now = time.time()
                while self.heap_expiry and self.heap_expiry[0][0] < now:
                    expire_time, key = heapq.heappop(self.heap_expiry)
                    if key in self.cache:
                        node, actual_expire = self.cache[key]
                        if actual_expire == expire_time:
                            self._remove(node)
                            del self.cache[key]
                            if key in self.frequency_count:
                                del self.frequency_count[key]


class MRUCahce:
    def __init__(self, capacity, ttl_seconds):
        self.ttl_second = ttl_seconds
        self.lock = threading.Lock()
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

    def __remove(self, node):
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = node

    def __add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        with self.lock:
            if key not in self.cache:
                return -1
            node, expire_time = self.cache[key]
            if expire_time < time.time():
                self.__remove(node)
                del self.cache[key]
                del self.frequency_count[key]
                return -1
            node = self.cache[key]
            self.__remove(node)
            self.__add_to_front(node)
            self.frequency_count[key] += 1
            return node.value

    def getMaximumValueKey(self):
        maxValue = float("-inf")
        key_to_remove = -1
        for key in self.frequency_count:
            if maxValue < self.frequency_count[key]:
                maxValue = self.frequency_count[key]
                key_to_remove = key
        return key_to_remove

    def put(self, key, value):
        with self.lock:
            expiry_time = time.time() + self.ttl_second
            if self.capacity == 0:
                return
            if key in self.cache:
                node, _ = self.cache[key]
                self.__remove(node)
            if len(self.cache) > self.capacity:
                key_to_delete = self.getMaximumValueKey()
                if key_to_delete is not None:
                    node_to_delete, _ = self.cache[key_to_delete]
                    self.__remove(node_to_delete)
                    del self.cache[key_to_delete]
                    del self.frequency_count[key_to_delete]
            node = Node(key, value)
            self.__add_to_front(node)
            self.cache[key] = (node, expiry_time)
            self.frequency_count[key] = self.frequency_count.get(key, 0) + 1
            heapq.heappush(self.heap_expiry, (expiry_time, key))

    def _cleanup(self):
        while True:
            time.sleep(1)
            with self.lock:
                now = time.time()
                while self.heap_expiry and self.heap_expiry[0][0] < now:
                    expire_time, key = heapq.heappop(self.heap_expiry)
                    if key in self.cache:
                        node, actual_expire = self.cache[key]
                        if actual_expire == expire_time:
                            self._remove(node)
                            del self.cache[key]
                            if key in self.frequency_count:
                                del self.frequency_count[key]
