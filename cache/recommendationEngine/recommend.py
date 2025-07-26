import threading
import time
import random


class TTLCache:
    def __init__(self, default_ttl=900):
        self.store = {}
        self.expiry = {}
        self.ttl = default_ttl
        self.lock = threading.Lock()

    def get(self, key):
        with self.lock:
            if key in self.store and time.time() < self.expiry[key]:
                return self.store[key]

            self.store.pop(key, None)
            self.expiry.pop(key, None)
            return None

    def put(self, key, value):
        with self.lock:
            self.store[key] = value
            self.expiry[key] = time.time() + self.ttl


class ModelEngine:
    def compute_recommendation(self, user_id):
        time.sleep(0.2)
        return [f"item_{random.randint(100,999)}" for _ in range(5)]


class RecommendationEngine:
    def __init__(self, cache_ttl=900):
        self.cache = TTLCache(default_ttl=cache_ttl)
        self.model = ModelEngine()

    def get_recommendations(self, user_id):
        cached = self.cache.get(user_id)
        if cached:
            print(f"[Cache Hit ] for user {user_id}")
            return cached
        print(f"[CACHE MISS] Computing for user {user_id}")
        recommendations = self.model.compute_recommendations(user_id)
        self.cache.put(user_id, recommendations)
        return recommendations
