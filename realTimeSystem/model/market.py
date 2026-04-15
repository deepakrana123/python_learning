from dataclasses import dataclass


MAX_PER_STOCK = 5000
GLOBAL_LIMIT = 20000
MAX_NOTIFICATIONS_PER_EVENT = 50
MAX_NOTIFICATION_QUEUE_SIZE = 1000


@dataclass(frozen=True)
class MarketEvent:
    stock: str
    price: float
    timestamp: float

    def __str__(self):
        return f"{self.stock} (Price:{self.price}) {self.timestamp}"

    def __repr__(self):
        return f"Stock(stock={self.stock}) ,price={self.price} , timestamp={self.timestamp}"


companies = [
    ("Apple", 175.50),
    ("Microsoft", 420.75),
    ("Google", 140.25),
    ("Amazon", 185.30),
    ("Tesla", 245.80),
    ("Meta", 330.60),
    ("Netflix", 485.90),
    ("Nvidia", 895.40),
    ("Tata", 815.40),
    ("Adani", 89.40),
]


from dataclasses import dataclass
from typing import Optional
from enum import Enum
from time import time


class Operator(Enum):
    GREATER_THAN = ">"
    LESS_THAN = "<"
    EQUAL = "=="


@dataclass(frozen=True)
class NotificationEvent:
    message: str
    price: float
    user_id: str
    stock: str


@dataclass
class Rule:
    user_id: str
    stock: str
    target_price: float
    operator: Operator
    priority: int = 0
    expires_at: Optional[float] = None

    def is_active(self) -> bool:
        if self.expires_at is None:
            return True
        return time.time() <= self.expires_at

    def matches(self, price: float) -> bool:
        if not self.is_active():
            return False
        if self.operator == Operator.GREATER_THAN:
            return self.target_price > price
        elif self.operator == Operator.LESS_THAN:
            return self.target_price < price
        elif self.operator == Operator.EQUAL:
            return self.target_price == price
        return False


# data class generate __init__,and  __repr__ itself , what __init__ do is to initialize the class, and constructor defination , __repr__ is to return the string representation of the class and __str__ is to return the string representation of the class
