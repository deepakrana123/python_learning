import threading
import time
import random
from collections import defaultdict, deque
import fnmatch
from datetime import timedelta, datetime


class PubSubSystem:
    def __init__(self):
        self.subscribers = []
        self.messages = defaultdict(dict)
        self.dlq = defaultdict(deque)
        self.processed_ids = set()
        self.ttl_seconds = 60
        self._start_cleanup_task()

    def subscribe(self, topic_pattern, callback):
        self.subscribers.append((topic_pattern, callback))

    def publish(self, topic, message):
        message_id = message.get("id")
        message["timestamp"] = (
            datetime.now()
        )  # time to delete the message after particular mtime
        # self.messages[topic]=message  this is log compaction is which the last entry is fullfilled
        self.messages[topic].append(message)
        for pattern, callback in self.subscribers:
            if fnmatch.fnmatch(topic, pattern):
                threading.Thread(
                    target=callback, args=(callback, topic, message)
                ).start()

    def _deliver_with_retry(self, callback, topic, message, retires=3):
        message_id = message.get("id")
        if message_id in self.processed_ids:
            print(f"[Skip] Already processed message ID: {message_id}")
            return
        delay = 1
        for attempt in range(retires):
            try:
                callback(message)
                return
            except Exception as e:
                time.sleep(delay + random.uniform(0, 1))
                delay *= 2
        self.dlq[topic].append(message)

    def _show_dlq(self):
        for topic, msgs in self.dlq.items():
            print(f"Topic: {topic}")
            for msg in msgs:
                print(f"  - ID: {msg['id']} at {msg['timestamp']}")

    def _start_cleanup_task(self):
        def periodic_clean():
            while True:
                self._cleanup_old_messages(self.ttl_seconds)
                time.sleep(10)

        threading.Thread(target=periodic_clean)

    def _cleanup_old_messages(self, ttl_seconds):
        now = datetime.now()
        expired_cutoff = now - timedelta(seconds=ttl_seconds)
        for topic, queue in self.messages.items():
            original_len = len(queue)
            self.messages[topic] = deque(
                [msg for msg in queue if msg["timestamp"] > expired_cutoff]
            )
            removed = original_len - len(self.messages[topic])
            if removed > 0:
                print(f"[cleanup] removed")
        threading.timer(10, self._cleanup_old_messages, args=(ttl_seconds))
