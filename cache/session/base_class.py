from abc import ABC, abstractmethod


class CacheStore(ABC):
    @abstractmethod
    def put(self, key, value, ttl_seconds):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def remove(self, key):
        pass

    @abstractmethod
    def contains(self, key) -> bool:
        pass
