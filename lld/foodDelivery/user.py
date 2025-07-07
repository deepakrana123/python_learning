from abc import ABC, abstractmethod
from enum import Enum


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


class Order:
    def __init__(
        self, id, timestamps, orders, customer_details: Customer, status: OrderStatus
    ):
        self.id = id
        self.timestamps = timestamps
        self.customer_details = customer_details
        self.order_status = status
        self.order = orders

    def change_order_status(self, status):
        self.order_status = status

    def modify_order(self, kind):
        pass

    def track_change(self):
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


class DeliveryAssginment:
    @staticmethod
    def assginDelivery(self, method: str) -> DeliveryStrategy:
        method = method.upper()
        if method == "OrderPriority":
            return "Assigned"
        elif method == "by_rating":
            return "by_rating"
        else:
            raise ValueError(f"Unsupported payment method: {method}")
