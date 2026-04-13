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
