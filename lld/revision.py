# import time


# class Node:
#     def __init__(self, key=0, val=0):
#         self.key = key
#         self.val = val
#         self.prev = None
#         self.next = None


# import heapq
# import threading


# class LRUCache:
#     def __init__(self, capacity, ttl_seconds):
#         self.cache = {}
#         self.size = 0
#         self.tail = Node(0, 0)
#         self.head = Node(0, 0)
#         self.head.next = self.tail
#         self.tail.prev = self.head
#         self.max_capacity = capacity
#         self.heap = []
#         self.ttl_seconds = ttl_seconds
#         self.lock = threading.lock()
#         cleanup_thread = threading.Thread(target=self._cleanup, daemon=True)
#         cleanup_thread.start()

#     def get(self, key: str):
#         with self.lock:
#             now = time.now() + self.ttl_seconds
#             if key not in self.cache:
#                 return -1
#             node = self.cache[key]
#             heapq.heappush(self.heap, (now, key))
#             self._move_to_front(node)
#             return node.val

#     def _add_to_front(self, node):
#         node.prev = self.head
#         node.next = self.head.next
#         self.head.next = node
#         self.head.next.prev = node

#     def _move_to_front(self, node):
#         node.prev.next = node.next
#         node.next.prev = node.prev

#     def _remove_node(self, node):
#         self._move_to_front(node)
#         self._add_to_front(node)

#     def put(self, key, val):
#         with self.locking:
#             now = time.now() + self.ttl_seconds
#             if key in self.cache:
#                 node = self.cache[key]
#                 self._remove_node(node)
#             else:
#                 node = Node(key, val)
#                 self.cache[key] = node
#                 self._add_to_front(node)
#                 self.size += 1
#                 if self.size > self.capacity:
#                     lru = self.tail.prev
#                     self._move_to_front(lru)
#                     del self.cache[lru.key]
#                     self.size -= 1
#             heapq.heappush(self.heap, (now, key))

#     def _cleanup(self):
#         time.sleep(1)
#         with self.lock:
#             now = time.time()
#             while self.heap and self.heap[0][0] <= now:
#                 expire_time, key = heapq.heappop(self.heap)
#                 if key in self.cache:
#                     node, actual_expire = self.cache[key]
#                     if actual_expire == expire_time:
#                         self._remove(node)
#                         del self.cache[key]


# class LFUCache:
#     def __init__(self, capacity):
#         self.cache = {}
#         self.size = 0
#         self.tail = Node(0, 0)
#         self.head = Node(0, 0)
#         self.head.next = self.tail
#         self.tail.prev = self.head
#         self.max_capacity = capacity
#         self.freqMap = {}
#         self.heap = []
#         self.ttl_heap = []

#     def get(self, key: str):
#         if key not in self.dicts:
#             return -1
#         node = self.dicts[key]
#         self.freqMap[key] = self.freqMap.get(key, 0) + 1
#         heapq.heappush(self.heap, (self.freqMap[key], key))
#         self._move_to_front(node)
#         return node.val

#     def _add_to_front(self, node):
#         node.prev = self.head
#         node.next = self.head.next
#         self.head.next = node
#         self.head.next.prev = node

#     def _move_to_front(self, node):
#         node.prev.next = node.next
#         node.next.prev = node.prev

#     def _remove_node(self, node):
#         self._move_to_front(node)
#         self._add_to_front(node)

#     def put(self, key, val):
#         if key in self.dicts:
#             node = self.dicts[key]
#             self.freqMap[key] = self.freqMap.get(key, 0) + 1
#             heapq.heappush(self.heap, (self.freqMap[key], key))
#             self._add_to_front(node)
#         node = Node(key, val)
#         self.dicts[key] = node
#         self.freqMap[key] = self.freqMap.get(key, 0) + 1
#         heapq.heappush(self.heap, (self.freqMap[key], key))
#         self._add_to_front(node)
#         self.size += 1
#         if self.size > self.capacity:
#             val, key = heapq.heappop(self.heap)
#             self._remove_node(self.dicts[key])
#             del self.cache[key]
#             self.size -= 1

import time
import threading


class Node:
    def __init__(self, key, val, expires_at):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None
        self.expires_at = expires_at


class LRUCache:
    def __init__(self, capacity, ttl_seconds):
        self.cache = {}
        self.capacity = capacity
        self.ttl = ttl_seconds
        self.head = Node(0, 0, float("-inf"))
        self.tail = Node(0, 0, float("-inf"))
        self.head.next = self.tail
        self.tail.prev = self.head
        self.lock = threading.Lock()

    def _is_expired(self, node):
        return time.time() > node.expires_at

    def _remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_front(self, node):
        self._remove_node(node)
        self._add_to_front(node)

    def _add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        with self.lock:
            if not key in self.cache:
                return -1
            node = self.cache[key]
            if self._is_expired(node):
                self._remove_node(node)
                del self.cache[key]
                return -1
            self._move_to_front(node)
            return node.val

    def put(self, key, val):
        with self.lock:
            expires_at = time.time() + self.ttl_seconds
            if key in self.cache:
                node = self.cache[key]
                self._move_to_front(node)
            else:
                if (len(self.cache)) >= self.capacity:
                    lru = self.tail.prev
                    self._remove_node(lru)
                    del self.cache[lru.key]
            new_node = Node(key, val, expires_at)
            self.cache[key] = new_node
            self._add_to_front(new_node)


class LFUCache:
    def __init__(self, capacity, ttl_seconds):
        self.cache = {}
        self.freq_map = {}
        self.capacity = capacity
        self.ttl = ttl_seconds
        self.min_freq = 0
        self.lock = threading.Lock()

    # def _remove_node(self, node):
    #     node.prev.next = node.next
    #     node.next.prev = node.prev

    # def _move_to_front(self, node):
    #     self._remove_node(node)
    #     self._add_to_front(node)

    # def _add_to_front(self, node):
    #     node.prev = self.head
    #     node.next = self.head.next
    #     self.head.next.prev = node
    #     self.head.next = node

    def get(self, key):
        with self.lock:
            if not key in self.cache:
                return -1
            node = self.cache[key]
            if time.time() > node.expires_at:
                self._remove_node(node)
                del self.cache[key]
                return -1
            self._update_frequency(node)
            return node.val

    def _update_frequency(self, node):
        old_freq = node.freq
        self.freq_map[old_freq].remove(node)
        if self.freq_map[old_freq].is_empty():
            del self.freq_map[old_freq]
            if old_freq == self.min_freq:
                self.min_freq += 1
        node.freq += 1
        if node.freq not in self.freq_map:
            self.freq_map[node.freq] = DoubleLinkedList()
        self.freq_map[node.freq].add_to_front(node)

    def put(self, key, val):
        with self.lock:
            if self.capacity <= 0:
                return
            expires_at = time.time() + self.ttl_seconds
            if key in self.cache:
                node = self.cache[key]
                node.val = val
                node.expires_at = expires_at
                self._update_frequency(node)
            else:
                if len(self.cache) >= self.capacity:
                    lfu_list = self.freq_map[self.min_freq]
                    lru_within_lfu = lfu_list.remove_form_tail()
                    del self.cache[lru_within_lfu.key]
            new_node = Node(key, val, expires_at, freq=1)
            self.cache[key] = new_node

            if 1 not in self.freq_map:
                self.freq_map[1] = DoubleLinkedList()
            self.freq_map[1].add_to_front(new_node)
            self.min_freq = 1


class DoubleLinkedList:
    def __init__(self):
        self.head = Node(0, 0, 0, 0)
        self.tail = Node(0, 0, 0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def remove(self, node):
        node.prev.nex = node.next
        node.next.prev = node.prev

    def remove_from_tail(self):
        if self.is_empty():
            return None
        node = self.tail.prev
        self.remove(node)
        return node

    def is_empty(self):
        return self.head.next == self.tail


class Node:
    def __init__(self, key, val, expires_at, freq=0):
        self.key = key
        self.val = val
        self.expires_at = expires_at
        self.freq = freq
        self.prev = None
        self.next = None
