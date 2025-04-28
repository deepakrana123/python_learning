import time
import threading
from collections import deque

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity,check_interval=1):
        self.capacity = capacity
        self.map = {}
        self.expiryMap={}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.prev = self.head
        self.lock=threading.Lock()
        self.check_interval=check_interval
        self._start_scheduler()
    
    def _start_scheduler(self):
        def scheduler():
            while True:
                time.sleep(self.check_interval)
                self._cleanup_expired_keys()
        threading.Thread(target=scheduler,daemo=True).start()
    def _cleanup_expired_keys(self):
        with self.lock:
            now=time.time()
            expired_keys=[k for k,t in self.expiryMap.items() if t <= now]
            for key in expired_keys:
                self._remove_key(key)
    
    def _remove_key(self,key):
        if key in self.map:
            self._remove(self.map[key])
            del self.map[key]
        if key in self.expiryMap:
            del self.expiryMap[key]
    def _remove(self, node):
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = prev

    def get(self, key):
        if key in self.map:
            if time.time()> self.expiryMap.get(key):
                self._remove_key(key)
                return -1
            node = self.map[key]
            self._remove(node)
            self._insert_At_front(node)
            return node.value
        return -1
    
    def _insert_at_front(self,node):
        node.next=self.head.next
        node.prev=self.head
        self.head.next.prev=node
        self.head.next=node

    def put(self, key, value,ttl=None):
        if key in self.map:
            self._remove(self.map[key])
        node = Node(key, value)
        self._insert_At_front(node)
        self.map[key] = node
        if ttl:
            self.expiry_map[key] = time.time() + ttl
        if len(self.map) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.map(lru.key)



class Node:
    def __init__(self,key,value,frequency=1):
        self.key=key
        self.value=value
        self.frequency=frequency
        self.prev=None
        self.next=None

class DLL:
    def __init__(self):
        self.head=Node(None,None)
        self.tail=Node(None,None)
        self.head.next=self.tail
        self.tail.prev=self.head
        self.size=0
    
    def insert_at_front(self,node):
        node.next=self.head.next
        node.prev=self.head
        self.head.prev.next=node.next
        self.head.next=node
    
    def remove_node(self,node):
        node.prev.next=node.next
        node.next.prev=node.prev
        self.size-=1
    
    def remove_last(self):
        if self.size==0:
            return None
        last_node=self.tail.prev
        self.remove_node(last_node)
        return last_node
    
    def is_empty(self):
        return self.size==0


class LFUCache:
    def __init__(self,capacity):
        self.capacity=capacity
        self.key_map={}
        self.freq={}
        self.min_freq=0
        self.size=0
    
    def _update_freq(self,node):
        old_freq=node.freq
        self.freq_map[old_freq].remove_node(node)
        if self.freq[old_freq].is_empty():
            del self.freq[old_freq]
            if self.min_freq==old_freq:
                self.min_freq+=1
        node.freq+=1
        new_freq=node.freq
        if new_freq not in self.freq:
            self.freq[new_freq]=DLL()
        self.freq[new_freq].insert_at_front(node)
    
    def get(self,key):
        if key not in self.key_map:
            return -1
        node=self.key_map[key]
        self._update_freq(node)
        return node.value
    
    def put(self,key,value):
        if self.capacity==0:
            return
        if key in self.key_map:
            node=self.key_map[key]
            node.value=value
            self._update_freq(node)
        else:
            if self.size>=self.capacity:
                min_list=self.freq[self.min_freq]
                node_to_remove=min_list.remove_last()
                del self.key_map[node_to_remove.key]
                if min_list.is_empty():
                    del self.freq_map[self.min_freq]
                self.size-=1
        new_node=Node(key,value)
        self.min_freq+=1
        if self.min_freq not in self.freq:
            self.freq[self.min_freq]=DLL()
        self.freq_map[self.min_freq].insert_at_front(new_node)
        self.key_map[key] = new_node
        self.size += 1



class MFUCache:
    def __init__(self,capacity):
        self.capacity=capacity
        self.key_map={}
        self.freq={}
        self.max_freq=0
        self.size=0
    
    def _update_freq(self,node):
        old_freq=node.freq
        self.freq_map[old_freq].remove_node(node)
        if self.freq[old_freq].is_empty():
            del self.freq[old_freq]
            if self.max_freq==old_freq:
                self.max_freq+=1
        node.freq+=1
        new_freq=node.freq
        self.max_freq=max(self.max_freq,new_freq)
        if new_freq not in self.freq:
            self.freq[new_freq]=DLL()
        self.freq[new_freq].insert_at_front(node)
    
    def get(self,key):
        if key not in self.key_map:
            return -1
        node=self.key_map[key]
        self._update_freq(node)
        return node.value
    
    def put(self,key,value):
        if self.capacity==0:
            return
        if key in self.key_map:
            node=self.key_map[key]
            node.value=value
            self._update_freq(node)
        else:
            if self.size>=self.capacity:
                min_list=self.freq[self.max_freq]
                node_to_remove=min_list.remove_last()
                del self.key_map[node_to_remove.key]
                if min_list.is_empty():
                    del self.freq_map[self.max_freq]
                self.size-=1
        new_node=Node(key,value)
        self.max_freq+=1
        if self.max_freq not in self.freq:
            self.freq[self.max_freq]=DLL()
        self.freq_map[self.max_freq].insert_at_front(new_node)
        self.key_map[key] = new_node
        self.size += 1



class FIFO:
    def __init__(self,capacity):
        self.key_map={}
        self.queue=deque()
        self.capacity=capacity
        self.size=0
    
    def get(self,key):
        if key not in self.key_map:
            return None
        return self.key_map[key]
    
    def put(self,key,value):
        if self.size>=self.capacity:
            key,value=self.queue.popleft()
            del self.key_map[key]
            return key
        if key in self.key_map:
            self.key_map[key]=value
            return key
        self.key_map[key]=value
        self.queue.append((key,value))


def is_correct(x,times):
    return  times-x >60

class SlidingWindowTimeLeft:
    def __init__(self,size,user):
        self.size=size
        self.user=user
        self.sildingMap={}
    
    def apiRequest(self,user):
        now=int(time.time())
        if user in self.sildingMap:
            self.sildingMap[user]=[]
        self.sildingMap[user]=list(filter(lambda x: x>=now- 60, self.sildingMap[user]))
        if len(self.sildingMap[user])>=self.size:
            return 'Size is full'
        self.sildingMap[user].append(now)


class CacheInvalidation:
    def __init__(self,user,ttl):
        self.user=user
        self.sildingMap={}
        self.lock=threading.Lock()
        self.ttl=ttl
        self.scheduled_threads = {}
        self.lock = threading.Lock()
    def _putInDb(self,data,user):
        pass
    
    def writeThorugh(self,user,data):
        while self.lock:
            if user in self.sildingMap:
                self.sildingMap[user]=data
            else:self.sildingMap[user]=data
            self.putInDb(data,user)
    
    def getDataWriteThrough(self,user):
        while self.lock:
            if user in self.sildingMap:
                return self.sildingMap[user]
            return 'No data found will fetch form db'
    
    def writeback(self,user,data,check_interval):
        while self.lock:
            if user in self.sildingMap and self.sildingMap[user]!=data:
                self.sildingMap[user]=data
                if user not in self.scheduled_threads:
                    self._start_scheduler(data,user,check_interval)
            self.sildingMap[user]=data
    def writettl(self,user,data):
        while self.lock:
            if user in self.sildingMap and self.sildingMap[user]!=data:
                self._start_scheduler_ttl(data,user)
            self.sildingMap[user]=data
        
    def _start_scheduler(self,data,user,check_interval):
        def scheduler():
            time.sleep(check_interval)
            with self.lock:
                self._putInDb(data,user)
                del self.sildingMap[user]
        self.scheduled_threads[user]=threading.Thread(target=scheduler,daemon=True)
        self.scheduled_threads[user].start()
    def _start_scheduler_ttl(self,data,user):
        def scheduler():
            time.sleep(self.ttl)
            with self.lock:
                if user in self.sildingMap:
                    del self.sildingMap[user]
                self._putInDb(data, user)
                del self.scheduled_threads[user]
        self.scheduled_threads[user]=threading.Thread(target=scheduler,daemon=True)
        self.scheduled_threads[user].start()
        


class TTL:
    def __init__(self):
        # self.user=user
        self.sildingMap={}
        self.expiryMap={}
        self.lock=threading.Lock()
        self.scheduled_threads = {}
      
        
    def _start_schedular(self,user):
        time.sleep(self.expiryMap[user] - int(time.time()))
        with self.lock:
            if user in self.sildingMap:
                del self.sildingMap[user]
                del self.scheduled_threads[user]
    def put(self,data,user,ttl):
        with self.lock:
            current_time=int(time.time())
            new_expiry_time = current_time + ttl
            if user in self.sildingMap:
                if self.sildingMap[user]!=data:
                    self.sildingMap[user]=data
                if self.expiryMap[user] !=int(time.time()) + ttl:
                    if user not in self.scheduled_threads:
                        self.scheduled_threads[user].join()
                    self.expiryMap[user] = new_expiry_time
                    self._get_schedular_start(user)
            else:
                self.expiryMap[user]=ttl+int(time.time())
                self.sildingMap[user]=data
                self._get_schedular_start(user)
    def _get_schedular_start(self,user):
        self.scheduled_threads[user]=threading.Thread(target=self._start_schedular,daemon=True)
        self.scheduled_threads[user].start()



class MLCacheRecommendation:
    def __init__(self,trendingData):
        self.user_cache={}
        self.user_cache_Expiry={}
        self.user_trending=trendingData
        self.user_session={}
        self.user_session_expiry={}
        self.user_contextual={}
        self.scheduled_threads={}
        self.scheduled_threads_session={}
    
    def _start_schedular_session(self,user):
        time.sleep(self.user_session_expiry[user] - int(time.time()))
        with self.lock:
            if user in self.user_cache:
                del self.user_session[user]
                del self.scheduled_threads_session[user]
                
    def _start_schedular(self,user_id):
        while True:
            time.sleep(1)
            with self.lock:
                expiry = self.user_cache_Expiry.get(user_id)
                if expiry is None or expiry > int(time.time()):
                    break  
                self.user_cache.pop(user_id, None)
                self.user_cache_Expiry.pop(user_id, None)
                self.scheduled_threads.pop(user_id, None)
                break
   
    def putData(self, user_id, user_ttl, user_data):
        with self.lock:
            current_time = int(time.time())
            new_expiry = current_time + user_ttl

            if user_id in self.user_cache:
                existing_data = self.user_cache[user_id]
                existing_expiry = self.user_cache_Expiry.get(user_id, 0)

                # Only update if data or TTL changed
                if existing_data != user_data or existing_expiry != new_expiry:
                    self.user_cache[user_id] = user_data
                    self.user_cache_Expiry[user_id] = new_expiry
                    self._get_schedular_start(user_id)
            else:
                self.user_cache[user_id] = user_data
                self.user_cache_Expiry[user_id] = new_expiry
                self._get_schedular_start(user_id)

    def putDataSession(self, session_id, session_ttl, session_data):
        with self.lock:
            current_time = int(time.time())
            new_expiry = current_time + session_ttl

            if session_id in self.user_session:
                existing_data = self.user_session[session_id]
                existing_expiry = self.user_session_expiry.get(session_id, 0)

                if existing_data != session_data or existing_expiry != new_expiry:
                    if session_id in self.scheduled_threads_session:
                        self.scheduled_threads_session[session_id].join() 

                self.user_session[session_id] = session_data
                self.user_session_expiry[session_id] = new_expiry
                self._get_schedular_start_session(session_id)
            else:
                self.user_session[session_id] = session_data
                self.user_session_expiry[session_id] = new_expiry
                self._get_schedular_start_session(session_id)

    def _get_schedular_start(self,user_id):
        self.scheduled_threads[user_id]=threading.Thread(target=self._start_schedular,daemon=True)
        self.scheduled_threads[user_id].start()
    
    def _get_schedular_start_session(self,session_id):
        if session_id in self.scheduled_threads_session:
            self.scheduled_threads_session[session_id]=threading.Thread(target=self._start_schedular_session,daemon=True)
            self.scheduled_threads_session[session_id].start()
    
    def putUserContext(self,keys,data):
        with self.lock:
            self.user_contextual[keys]=data
    
    def putUserTrending(self,keys,trending):
        with self.lock:
            if keys in self.user_trending:
                self.user_trending[keys]=trending
            else:
                self.user_trending[keys]=trending


    def getUserData(self,user_id,session_id,context_key=None,trend_key=None):
        with self.lock:
            if user_id in self.user_cache and user_id in self.user_cache_Expiry:
                return self.user_cache[user_id]
            if session_id in self.user_session:
                return self.user_session[session_id]
            context = self.user_contextual.get(context_key, [])
            trend = self.user_trending.get(trend_key, [])
            return context + trend, "contextual+trending"      
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # Store key -> node reference
        self.dll_head = DoublyLinkedListNode(None)  # Dummy head
        self.dll_tail = DoublyLinkedListNode(None)  # Dummy tail
        self.dll_head.next = self.dll_tail
        self.dll_tail.prev = self.dll_head

    def _move_to_front(self, node):
        """Moves the node to the front (most recently used)."""
        node.prev.next = node.next
        node.next.prev = node.prev
        node.next = self.dll_head.next
        node.prev = self.dll_head
        self.dll_head.next.prev = node
        self.dll_head.next = node

    def _evict_lru(self):
        """Evict the least recently used item from the cache."""
        lru_node = self.dll_tail.prev
        self.dll_tail.prev = lru_node.prev
        lru_node.prev.next = self.dll_tail
        del self.cache[lru_node.key]

    def get(self, input_data):
        
        node = self.cache[key]
        key = self._get_cache_key(input_data)  
        if key in self.cache:
            self._move_to_front(node)
            return node.data
        else:
            return None 

    def put(self, input_data, data):
      
        key = self._get_cache_key(input_data)  
        if key in self.cache:
            node = self.cache[key]
            node.data = data
            self._move_to_front(node)
        else:
            
            if len(self.cache) >= self.capacity:
                self._evict_lru()
            new_node = DoublyLinkedListNode(key, data)
            self.cache[key] = new_node
            self._move_to_front(new_node)

    def _get_cache_key(self, input_data):
        """Generate a unique key based on the input data."""
        return hash(str(input_data))  

class DoublyLinkedListNode:
    def __init__(self, key=None, data=None):
        self.key = key  
        self.data = data  
        self.prev = None
        self.next = None
