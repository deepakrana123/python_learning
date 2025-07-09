# #  to many encaplustion leads to junk code

# #  startgey + composotion helps there

# # Encapsulation = how you protect and expose data/behavior

# # Composition = a design choice that helps you encapsulate better, especially as complexity grows

# from abc import ABC, abstractmethod
# from enum import Enum
# from functools import wraps
# import time


# class Observer(ABC):
#     @abstractmethod
#     def update(self, data):
#         pass


# class Subject(Observer):
#     def __init__(self):
#         self._observers = []

#     def add_observer(self, observer: Observer):
#         self._observers.append(observer)

#     def remove_observer(self, observer: Observer):
#         self._observers.remove(observer)

#     def notify_observers(self, data):
#         for observer in self._observers:
#             observer.update(data)


# class OrderStatus(Enum):
#     BOOKED = "Booked"
#     CONFIRMED = "Confirmed"
#     PREPARING = "Preparing"
#     DISPATCHED = "Dispatched"
#     ON_THE_WAY = "On The Way"
#     DELIVERED = "Delivered"
#     CANCELLED = "Cancelled"
#     FAILED = "Failed"
#     RETURN_REQUESTED = "Return Requested"
#     RETURNED = "Returned"


# class UserStatus(Enum):
#     ACTIVE = "ACTIVE"
#     BLOCKED = "BLOCKED"
#     DELETED = "DELETED"


# # wraps help to get the doc_name and name
# def rate_limit(seconds: int):
#     def decorator(func):
#         last_called = {}

#         @wraps(func)
#         def wrapper(cls, *args, **kwrags):
#             now = time.time()
#             user_key = cls.__name__
#             last_time = last_called.get(user_key, 0)
#             if now - last_time < seconds:
#                 return
#             last_called[user_key] = now
#             return func(cls, *args, **kwrags)

#         return wrapper

#     return decorator


# def retry(max_attempts=3, delay=1):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(cls, *args, **kwrags):
#             attempts = 0
#             while attempts < max_attempts:
#                 result = func(*args, **kwrags)
#                 if result:
#                     return result
#                 attempts += 1
#                 print(f"Retrying... attempt {attempts + 1}")
#                 time.sleep(delay)
#             print("All retry attempts failed.")
#             return False

#         return wrapper

#     return decorator


# class RoleStrategy(ABC):
#     @abstractmethod
#     def get_role(self):
#         pass

#     @abstractmethod
#     def perform_role_action(self):
#         pass


# class CustomerRole(RoleStrategy):
#     def get_role(self):
#         return "Customer"

#     def perform_role_action(self):
#         print("Viewing order history...")


# class RestaurantRole(RoleStrategy):
#     def get_role(self):
#         return "Restaurant"

#     def perform_role_action(self):
#         print("Managing restaurant menu...")


# class AdminRole(RoleStrategy):
#     def get_role(self):
#         return "Admin"

#     def perform_role_action(self):
#         print("Managing platform settings...")


# class User:
#     def __init__(
#         self,
#         user_id,
#         name,
#         contact_details,
#         role_strategy: RoleStrategy,
#         status: UserStatus,
#     ):
#         self.user_id = user_id
#         self.name = name
#         self.contact_details = contact_details
#         self.role_strategy = role_strategy
#         self.user_status = status

#     def get_stragey_role(self):
#         return self.roleStrategy.get_role()

#     def perform_actions(self):
#         return self.roleStrategy.perform_role_action()


# class SessionManager:
#     current_user = None

#     @classmethod
#     @rate_limit(10)
#     def login(cls, user):
#         cls.current_user = user

#     @classmethod
#     def logout(cls):
#         cls.current_user = None

#     @classmethod
#     def get_current_user(cls):
#         return cls.current_user


# class Menu(ABC):
#     @abstractmethod
#     def display(self, indent=0):
#         pass


# class MenuItem(Menu):
#     def __init__(self, name, amount, description):
#         self.name = name
#         self.amount = amount
#         self.description = description

#     def display(self, indent=0):
#         print("  " * indent + f"- {self.name} (${self.amount}): {self.description}")


# class MenuCategory(Menu):
#     def __init__(self, name):
#         self.name = name
#         self.contents = []

#     def add(self, component):
#         self.contents.append(component)

#     def remove(self, component):
#         self.contents = [item for item in self.contents if component.name != item.name]

#     def display(self, indent):
#         print("  " * indent + f"[Box: {self.name}]")
#         for component in self.contents:
#             component.display(indent + 1)


# class ItemCustomization:
#     def __init__(self, menu_item):
#         self.menu_item = menu_item

#     def display(self):
#         self.menu_item.display()


# class SizeOption(ItemCustomization):
#     def __init__(self, menu_item, size):
#         super().__init__(menu_item)
#         self.size = size

#     def display(self):
#         self.menu_item.display()
#         print(f"  • Size: {self.size}")


# class SizeOption(ItemCustomization):
#     def __init__(self, menu_item, spice_level):
#         super().__init__(menu_item)
#         self.spice_level = spice_level

#     def display(self):
#         self.menu_item.display()
#         print(f"  • Size: {self.spice_level}")


# class SizeOption(ItemCustomization):
#     def __init__(self, menu_item, toppings):
#         super().__init__(menu_item)
#         self.toppings = toppings

#     def display(self):
#         self.menu_item.display()
#         print(f"  • Size: {self.toppings}")


# class Payment(ABC):
#     @abstractmethod
#     def pay(self, amount):
#         pass


# class PayByCard(Payment):
#     def __init__(self, card_number, cvv, expiry):
#         self.card_number = card_number
#         self.cvv = cvv
#         self.expiry = expiry

#     def pay(self, amount):
#         print(f"Paying ₹{amount} using Card ending with {self.card_number[-4:]}")
#         return True

#     def refund(self, amount):
#         print(f"Paying ₹{amount} using Card ending with {self.card_number[-4:]}")


# class PayByUPI(Payment):
#     def __init__(self, upi_id):
#         self.upi_id = upi_id

#     def pay(self, amount):
#         print(f"Paying ₹{amount} using Card ending with {self.card_number[-4:]}")
#         return False

#     def refund(self, amount):
#         print(f"Paying ₹{amount} using Card ending with {self.card_number[-4:]}")


# class Checkout:
#     def __init__(self, strategy, status):
#         self.strategy = strategy
#         self.status = status

#     def change_strategy(self, strategy):
#         self.strategy = strategy

#     def process_payment(self, amount):
#         a = self.strategy.pay(amount)
#         if a:
#             self.status = "Success"
#         else:
#             self.status = "Failure"

#     def process_refund(self, amount):
#         self.strategy.refund(amount)


# class Transcation:
#     def __init__(self):
#         self.trancation = []

#     def add(self, payment):
#         self.trancation.append(payment)

#     def show_history(self):
#         for payment in self.trancation:
#             print(payment)


# class CustomerApp(Observer):
#     def update(self, data):
#         print(
#             f"[CustomerApp] Order {data['order_id']} updated to {data['new_status'].name}"
#         )


# class RestaurantDashboard(Observer):
#     def update(self, data):
#         print(
#             f"[RestaurantDashboard] Order {data['order_id']} is now {data['new_status'].name}"
#         )


# class OrderState(ABC):
#     @abstractmethod
#     def next(self, order, new_state):
#         pass

#     @abstractmethod
#     def name(self):
#         pass


# class PendingState(OrderState):
#     def next(self, order, new_state):
#         if isinstance(new_state, PreparingState):
#             order.set_state(new_state)
#         elif isinstance(new_state, CancelledState):
#             order.set_state(new_state)
#         else:
#             print("Invalid transition")

#     def name(self):
#         return OrderStatus.PREPARING


# class PreparingState(OrderState):
#     def next(self, order, new_state):
#         if isinstance(new_state, CancelledState):
#             print("")
#         elif isinstance(new_state, DeliveredState):
#             order.set_state(new_state)
#         else:
#             print("Invalid transition")

#     def name(self):
#         return OrderStatus.PREPARING


# class CancelledState(OrderState):
#     def next(self, order, new_state):

#         print("Invalid transition")

#     def name(self):
#         return OrderStatus.CANCELLED


# class DeliveredState(OrderState):
#     def next(self, order, new_state):
#         print("Order already delivered. No further changes allowed.")

#     def name(self):
#         return OrderStatus.DELIVERED


# class Order(Subject):
#     def __init__(
#         self, order_id, orders, customer_details: User, status: UserStatus, timestamps
#     ):
#         super().__init__()
#         self.order_id = order_id
#         self.timestamps = timestamps
#         self.customer_details = customer_details
#         self.order_items = orders
#         self.state = status

#     def set_state(self, new_state):
#         self.state = new_state
#         self.notify_observers(
#             {
#                 "order_id": self.order_id,
#                 "new_status": new_state.name().value,
#                 "timestamp": time.time(),
#             }
#         )

#     def change_order_status(self, new_status: OrderStatus):
#         self.state.next(self, new_status)

#     def get_state(self):
#         return self.state.name().value

from abc import ABC, abstractmethod
from enum import Enum
from functools import wraps
import time

# -------------------- Observer Pattern --------------------
# Observer is used to notify subscribers (CustomerApp, RestaurantDashboard) about changes in order status.


class Observer(ABC):
    @abstractmethod
    def update(self, data):
        pass


class Subject(Observer):  # Subject part of the Observer pattern
    def __init__(self):
        self._observers = []

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def notify_observers(self, data):
        for observer in self._observers:
            observer.update(data)


# -------------------- Enum for Clean State Handling --------------------
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


class UserStatus(Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    DELETED = "DELETED"


# -------------------- Decorator Pattern --------------------
# These are decorators to add behavior (rate_limit, retry) without modifying core logic.


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


def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(cls, *args, **kwrags):
            attempts = 0
            while attempts < max_attempts:
                result = func(*args, **kwrags)
                if result:
                    return result
                attempts += 1
                print(f"Retrying... attempt {attempts + 1}")
                time.sleep(delay)
            print("All retry attempts failed.")
            return False

        return wrapper

    return decorator


# -------------------- Strategy Pattern --------------------
# RoleStrategy allows runtime role switching for users (Customer, Admin, Restaurant)


class RoleStrategy(ABC):
    @abstractmethod
    def get_role(self):
        pass

    @abstractmethod
    def perform_role_action(self):
        pass


class CustomerRole(RoleStrategy):
    def get_role(self):
        return "Customer"

    def perform_role_action(self):
        print("Viewing order history...")


class RestaurantRole(RoleStrategy):
    def get_role(self):
        return "Restaurant"

    def perform_role_action(self):
        print("Managing restaurant menu...")


class AdminRole(RoleStrategy):
    def get_role(self):
        return "Admin"

    def perform_role_action(self):
        print("Managing platform settings...")


class User:
    def __init__(
        self,
        user_id,
        name,
        contact_details,
        role_strategy: RoleStrategy,
        status: UserStatus,
    ):
        self.user_id = user_id
        self.name = name
        self.contact_details = contact_details
        self.role_strategy = role_strategy
        self.user_status = status

    def get_stragey_role(self):
        return self.roleStrategy.get_role()

    def perform_actions(self):
        return self.roleStrategy.perform_role_action()


# -------------------- Singleton-like Session Manager --------------------
# Centralized session management using class methods


class SessionManager:
    current_user = None

    @classmethod
    @rate_limit(10)  # Decorator used here
    def login(cls, user):
        cls.current_user = user

    @classmethod
    def logout(cls):
        cls.current_user = None

    @classmethod
    def get_current_user(cls):
        return cls.current_user


# -------------------- Composite Pattern --------------------
# Menu and MenuItem form a tree-like structure.
# MenuCategory can contain other Menu or MenuItems.


class Menu(ABC):
    @abstractmethod
    def display(self, indent=0):
        pass


class MenuItem(Menu):
    def __init__(self, name, amount, description):
        self.name = name
        self.amount = amount
        self.description = description

    def display(self, indent=0):
        print("  " * indent + f"- {self.name} (${self.amount}): {self.description}")


class MenuCategory(Menu):
    def __init__(self, name):
        self.name = name
        self.contents = []

    def add(self, component):
        self.contents.append(component)

    def remove(self, component):
        self.contents = [item for item in self.contents if component.name != item.name]

    def display(self, indent):
        print("  " * indent + f"[Box: {self.name}]")
        for component in self.contents:
            component.display(indent + 1)


# -------------------- Decorator Pattern for Item Customization --------------------
# Dynamically add features (size, spice level, toppings) to MenuItems.


class ItemCustomization:
    def __init__(self, menu_item):
        self.menu_item = menu_item

    def display(self):
        self.menu_item.display()


class SizeOption(ItemCustomization):
    def __init__(self, menu_item, size):
        super().__init__(menu_item)
        self.size = size

    def display(self):
        self.menu_item.display()
        print(f"  • Size: {self.size}")


# You accidentally reused class names. These should be renamed to `SpiceLevelOption`, `ToppingsOption`.

# -------------------- Strategy Pattern (again) --------------------
# Different payment strategies for checkout.


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
        return True

    def refund(self, amount):
        print(f"Refunding ₹{amount} to Card ending with {self.card_number[-4:]}")


class PayByUPI(Payment):
    def __init__(self, upi_id):
        self.upi_id = upi_id

    def pay(self, amount):
        print(f"Paying ₹{amount} using UPI ID {self.upi_id}")
        return False

    def refund(self, amount):
        print(f"Refunding ₹{amount} to UPI ID {self.upi_id}")


class Checkout:
    def __init__(self, strategy, status):
        self.strategy = strategy
        self.status = status

    def change_strategy(self, strategy):
        self.strategy = strategy

    def process_payment(self, amount):
        a = self.strategy.pay(amount)
        self.status = "Success" if a else "Failure"

    def process_refund(self, amount):
        self.strategy.refund(amount)


class Transcation:
    def __init__(self):
        self.trancation = []

    def add(self, payment):
        self.trancation.append(payment)

    def show_history(self):
        for payment in self.trancation:
            print(payment)


# -------------------- Observer Pattern (again) --------------------


class CustomerApp(Observer):
    def update(self, data):
        print(f"[CustomerApp] Order {data['order_id']} updated to {data['new_status']}")


class RestaurantDashboard(Observer):
    def update(self, data):
        print(
            f"[RestaurantDashboard] Order {data['order_id']} is now {data['new_status']}"
        )


# -------------------- State Pattern --------------------
# Each OrderState represents a concrete state.
# Order delegates status transitions to current state object.


class OrderState(ABC):
    @abstractmethod
    def next(self, order, new_state):
        pass

    @abstractmethod
    def name(self):
        pass


class PendingState(OrderState):
    def next(self, order, new_state):
        if isinstance(new_state, PreparingState):
            order.set_state(new_state)
        elif isinstance(new_state, CancelledState):
            order.set_state(new_state)
        else:
            print("Invalid transition")

    def name(self):
        return OrderStatus.BOOKED


class PreparingState(OrderState):
    def next(self, order, new_state):
        if isinstance(new_state, DeliveredState):
            order.set_state(new_state)
        elif isinstance(new_state, CancelledState):
            print("Can't cancel while preparing")
        else:
            print("Invalid transition")

    def name(self):
        return OrderStatus.PREPARING


class CancelledState(OrderState):
    def next(self, order, new_state):
        print("Invalid transition")

    def name(self):
        return OrderStatus.CANCELLED


class DeliveredState(OrderState):
    def next(self, order, new_state):
        print("Order already delivered. No further changes allowed.")

    def name(self):
        return OrderStatus.DELIVERED


class Order(Subject):  # Combines Subject + State Pattern
    def __init__(
        self,
        order_id,
        orders,
        customer_details: User,
        status: UserStatus,
        timestamps=None,
    ):
        super().__init__()
        self.order_id = order_id
        self.timestamps = timestamps
        self.customer_details = customer_details
        self.order_items = orders
        self.state = status  # Should be set to a state object (like PendingState())

    def set_state(self, new_state):
        self.state = new_state
        self.notify_observers(
            {
                "order_id": self.order_id,
                "new_status": new_state.name().value,
                "timestamp": time.time(),
            }
        )

    def change_order_status(self, new_status: OrderStatus):
        self.state.next(self, new_status)

    def get_state(self):
        return self.state.name().value
