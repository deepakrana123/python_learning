#  Implement a TTL (Time-To-Live) Cache from scratch

from typing import Any, Dict
import time
import threading


class Ttl:
    def __init__(self):
        self.dicts: Dict[str, Any] = {}
        self.ttl_dicts = {}
        self.lock = threading.Lock()
        self.cleanup_thread = threading.Thread(
            target=self._start_scheduler, daemon=True
        )
        self.cleanup_thread.start()

    def add_to_dicts(self, key, value, ttl):
        with self.lock:
            if key not in self.dicts:
                self.dicts[key] = value
            else:
                self.dicts[key] = value
            self.ttl_dicts[key] = time.time() + ttl

    def _remove_dicts_keys(self):
        remove = []
        curr_time = time.time()
        with self.lock:
            for keys in self.ttl_dicts:
                if self.ttl_dicts[keys] - curr_time <= 0:
                    remove.append(keys)
            for keys in self.dicts:
                if keys in remove:
                    del self.dicts[keys]
                    del self.ttl_dicts[keys]

    def _start_scheduler(self):
        while True:
            with self.lock:
                self._remove_dicts_keys()
            time.sleep(5)
