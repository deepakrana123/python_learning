from abc import ABC, abstractmethod


class IRateLimiterStrategy(ABC):
    @abstractmethod
    def is_allowed(self, user_id: str) -> tuple[bool, int, int]:
        pass
