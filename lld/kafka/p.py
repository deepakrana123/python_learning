import threading
from collections import defaultdict, deque
import time
import fnmatch


class PubSub:
    def __init__(self):
        self.topics = defaultdict(list)  # subscriber
        self.messages = defaultdict(
            deque
        )  # message queue fir persitance and if offline to send message when it is online

    def subscribe(self, topic, callback):
        self.topics[topic].append(callback)
        print(f"Subscribed to topic '{topic}")
        for msg in self.messages[topic]:
            threading.Thread(target=callback, args=(msg,)).start()

    def publish(self, topic, message):
        self.messages[topic].append(message)  # persistmessage
        if topic in self.topics:
            for callback in self.topics[topic]:
                threading.Thread(target=callback, args=(message,)).start()


def subscriber_one(message):
    print(f"[Subscriber One] Received: {message}")
    time.sleep(1)


def subscriber_two(message):
    print(f"[Subscriber Two] Received: {message}")
    time.sleep(1)


# Using the PubSub system
pubsub = PubSub()
pubsub.subscribe("sports", subscriber_one)
pubsub.subscribe("sports", subscriber_two)

pubsub.publish("sports", "Football match starts at 7 PM.")


class WildcardPubSub:
    def __ini__(self):
        self.subscribers = []  # list of (topic_pattern,callback)
        self.messages = defaultdict(deque)

    def subscribe(self, topic_pattern, callback):
        self.subscribers.append((topic_pattern, callback))
        print(f"subscribed to pattern {topic_pattern}")
        for topic, msg_queue in self.messages.items():
            if fnmatch.fnmatch(topic, topic_pattern):
                for msg in msg_queue:
                    threading.Thread(target=callback, args=(msg,)).start()

    def publish(self, topic, message):
        self.messages[topic].append(message)
        for pattern, callback in self.subscribers:
            if fnmatch.fnmatch(topic, pattern):
                threading.Thread(target=callback, arg=(message,)).start()
