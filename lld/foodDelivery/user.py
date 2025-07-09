from abc import ABC, abstractmethod
from enum import Enum
import time
from functools import wraps


def rate_limit(seconds: int):
    def decorator(func):
        last_called = {}

        @wraps(func)
        def wrapper(cls, *args, **kwrags):
            now = time.time()
            user_key = cls.__name__
            last_time = last_called.get(user_key, 0)
            if now - last_time < seconds:
                return
            last_called[user_key] = now
            return func(cls, *args, **kwrags)

        return wrapper

    return decorator


class OrderStatus(Enum):
    BOOKED = "Booked"
    CONFIRMED = "Confirmed"
    PREPARING = "Preparing"
    DISPATCHED = "Dispatched"
    ON_THE_WAY = "On The Way"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    FAILED = "Failed"
    RETURN_REQUESTED = "Return Requested"
    RETURNED = "Returned"


class User(ABC):
    def __init__(self, userId, name, contactDetails):
        self.userId = userId
        self.name = name
        self.contactDetails = contactDetails

    @abstractmethod
    def get_role(self):
        pass


class Customer(User):
    def get_role(self):
        return "Customer"

    def order_history(self):
        pass


class RestaurantUser(User):

    def get_role(self):
        return "Restaurant"

    def make_menu(self):
        pass

    def order_transncation(self):
        pass


class MenuItem:
    def __init__(self, name, amount, in_stock):
        self.name = name
        self.amount = amount
        self.in_stock = in_stock


class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


class PayByCard(Payment):
    def __init__(self, card_number, cvv, expiry):
        self.card_number = card_number
        self.cvv = cvv
        self.expiry = expiry

    def pay(self, amount):
        print(f"Paying ₹{amount} using Card ending with {self.card_number[-4:]}")


class PayByUPI(Payment):
    def __init__(self, upi_id):
        self.upi_id = upi_id

    def pay(self, amount):
        print(f"Paying ₹{amount} using Card ending with {self.card_number[-4:]}")


class Checkout:
    def __init__(self, strategy):
        self.strategy = strategy

    def change_strategy(self, strategy):
        self.strategy = strategy

    def process_payment(self, amount):
        self.strategy.pay(amount)


class DeliveryStrategy(ABC):
    @abstractmethod
    def assgin(self, order):
        pass


class AssignByOrderPriority(DeliveryStrategy):
    def assign(self, order):
        pass


class AssignByRating(DeliveryStrategy):
    def assign(self, order):
        pass


# class DeliveryAssginment:
#     @staticmethod
#     def assginDelivery(self, method: str) -> DeliveryStrategy:
#         method = method.upper()
#         if method == "OrderPriority":
#             return "Assigned"
#         elif method == "by_rating":
#             return "by_rating"
#         else:
#             raise ValueError(f"Unsupported payment method: {method}")


class Observer(ABC):
    @abstractmethod
    def update(self, data):
        pass


class Subject(Observer):
    def __init__(self):
        self._observers = []

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def notify_observers(self, data):
        for observer in self._observers:
            observer.update(data)


class Order(Subject):
    def __init__(
        self,
        order_id,
        timestamps,
        orders,
        customer_details: Customer,
        status: OrderStatus,
    ):
        super().__init__()
        self.order_id = order_id
        self.timestamps = timestamps
        self.customer_details = customer_details
        self.order_status = status
        self.order = orders

    def change_order_status(self, status):
        self.status = status
        self.notify_observers({"order_id": self.order_id, "new_status": status})

    def modify_order(self, kind):
        pass

    def track_change(self):
        pass


class CustomerApp(Observer):
    def update(self, data):
        print(
            f"[CustomerApp] Order {data['order_id']} updated to {data['new_status'].name}"
        )


class RestaurantDashboard(Observer):
    def update(self, data):
        print(
            f"[RestaurantDashboard] Order {data['order_id']} is now {data['new_status'].name}"
        )


class FeedBackAndRating:
    def __init__(self, order_id, revies):
        pass
