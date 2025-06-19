from enum import Enum
from abc import ABC
from datetime import datetime
from datetime import timedelta


class OrderStatus(Enum):
    UNSHIPPED = "Unshipped"
    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    RETURNED = "Returned"


class AccountStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    SUSPENDED = "Suspended"
    CLOSED = "Closed"
    PENDING_VERIFICATION = "Pending Verification"
    BANNED = "Banned"


class ShipmentStatus(Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    IN_TRANSIT = "In Transit"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"
    FAILED_ATTEMPT = "Failed Attempt"
    RETURNED = "Returned"
    CANCELLED = "Cancelled"


class PaymentStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"
    REFUNDED = "Refunded"
    PARTIALLY_REFUNDED = "Partially Refunded"
    AUTHORIZED = "Authorized"
    DECLINED = "Declined"


class Address:
    def __init__(self, street, city, state, zip_code, country):
        self.__street = street
        self.__city = city
        self.__state = state
        self.__zip = zip_code
        self.__country = country


class Account:
    def __init__(
        self,
        userName,
        password,
        name,
        shippingAddress,
        email,
        phone,
        status=AccountStatus,
    ):
        self.username = userName
        self.password = password
        self.status = status.ACTIVE
        self.name = name
        self.shippingAddres = shippingAddress
        self.email = email
        self.phone = phone
        self.__credit_card = []
        self.__bank_accounts = []

    def add_product():
        return

    def add_product_review():
        return

    def reset_password():
        return


#  class are those class which can be used are can be inheirted by other class


class Customer(ABC):
    def __init__(self, cart: ShppingCart):
        self.__cart = cart
        self.__order = []

    def get_cart_detail(self):
        return self.__cart

    def add_to_cart(self, item):
        self.__cart.append(item)
        return self.__cart

    def remove_to_cart(self, item):
        self.__cart.filter(())


class Guest(Customer):
    def register_account(self):
        return None


class Member(Customer):
    def __init__(self, account):
        self.account = account

    def place_order(self, order):
        None


class ProductCategory:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Product:
    def __init__(self, name, descriptions, price, seller_account, category):
        self.__name = name
        self.__descriptions = descriptions
        self.__price = price
        self.__availableItemCount = 0
        self.__category = category
        self.__selller = seller_account

    def get_available_count(self):
        return self.__availableItemCount

    def update_price(self, new_price):
        None


class ProductReview:
    def __init__(self, rating, review):
        self.rating = rating
        self.review = review

    def getRating(self):
        None


class Item:
    def __init__(self, productId, quantity, price):
        self.__productId = productId
        self.__quantity = quantity
        self.__price = price

    def update_quantity(self, updateQuantity):
        self.__quantity = updateQuantity


class ShppingCart:
    def __init__(self):
        self.__items = []

    def add_cart(self, item):
        self.__items.append(item)

    def remove_cart(self, items):
        self.__items = [
            item for item in self.__items if item.productId != items.productId
        ]
        return self.__items

    def add_cart(self, item, quantity):
        for existing_item in self.__items:
            if existing_item.productId == item.productId:
                existing_item.updateQuantity(quantity + item.quantity)
        self.__items.append(item)

    def getCart(self):
        return self.__items

    def clear_cart(self):
        self.__items = []

    def checkout(self, orderService):
        orderService.create_order_form_cart(self.__items)


class Customer(ABC):
    def __init__(self, cart: ShppingCart):
        self.__cart = cart
        self.__order = []

    def get_cart_detail(self):
        return self.__cart


class OrderLog:
    def __init__(self, orderId, status=OrderStatus):
        self.orderId = orderId
        self.status = status.PENDING
        self.date = datetime.date.today()


class Order:
    def __init__(self, orderId, status=OrderStatus):
        self.orderId = orderId
        self.status = status.PENDING
        self.date = datetime.today().date()
        self.__order_log = []

    def send_for_shippment(self, shipment_service):
        if self.status == OrderStatus.PENDING:
            shippment = shipment_service.create_shippment(self.orderId)
            self.status = OrderStatus.SHIPPED
            self.add_order_log("Order shipped" + self.orderId + self.status)
        else:
            Exception("Not in state to proceed the order")

    def make_payment(self, payment_service):
        success = payment_service.make_payment(self.orderId)
        if success:
            self.status = OrderStatus.CONFIRMED
            self.add_order_log("Payment confirmed")
        else:
            self.add_order_log("Payment failed")

    def add_order_log(self, message):
        self.__order_log.append(message)


class ShipmentLog:
    def __init__(self, shippmentId, shipment_method):
        self.orderId = shippmentId
        self.__shipment_date = datetime.date.today()
        self.__estimated_arrival = datetime.date.today()
        self.__shipment_method = shipment_method
        self.__shipmentLogs = []

    def add_shipment():
        None


class Notification(ABC):
    def __init__(self, notificationId, content):
        self.notificationId = notificationId
        self.content = content
        self.__created_on = datetime.date.today()

    def send_notification(self):
        None


class SmsNotification(Notification):
    def send_notification(self):
        print("through sms")


class MobileNotification(Notification):
    def send_notification(self):
        print("through mobile notfication")


class Search(ABC):
    def search_products_by_name(self, name):
        None

    def search_products_by_category(self, category):
        None


class Catalog(Search):
    def __init__(self):
        self.__product_names = {}
        self.__product_categories = {}

    def search_products_by_name(self, name):
        return self.product_names.get(name)

    def search_products_by_category(self, category):
        return self.product_categories.get(category)


class OrderService:
    def __init__(self):
        self.orders = {}

    def create_order_form_cart(self, userId, cart_items):
        orderId = f"ORD-{userId}-{datetime.now().timestamp()}"
        order = Order(orderId)
        self.orders[orderId] = order
        print(f"Order {orderId} created with {len(cart_items)} items")
        return order

    def cancel_order(self, orderId, shipment_service, payment_service):
        order = self.orders.get(orderId)
        if not order:
            Exception("Order doesnot exist")
        total_fee = 0
        shipment_ids = shipment_service.get_shippment_for_orders(orderId)

        for shipment in shipment_ids:
            if shipment_service.is_in_transit(shipment):
                total_fee += shipment_service.cancel_shipment_fee(shipment)
            else:
                total_fee += shipment_service.cancel_shipment_fee(shipment)
        payment_service.issue_refund(orderId, total_fee)
        order.status = OrderStatus.CANCELLED
        order.add_order_log("Order cancelled with refund fee: " + str(total_fee))
        return True


class PaymentService:
    def __init__(self):
        self.__payments = {}

    def create_payments(self, orderId):
        retries = self.__payments.get(orderId, (PaymentStatus.PENDING, 0))[1]
        if retries >= 3:
            self.__payments[orderId] = (PaymentStatus.FAILED, retries)
            return
        success = self.simulate_payment_gateway()
        if success:
            self.__payments[orderId] = (PaymentStatus.COMPLETED, retries)
            return True
        else:
            self.__payments[orderId] = (PaymentStatus.FAILED, retries + 1)
            return False

    def simulate_payment_gateway():
        from random import choice

        return choice([True, False])

    def issue_refund(self, orderId, totalFee):
        if orderId in self.__payments:
            self.__payments[orderId] = (PaymentStatus.REFUNDED, 0)
        else:
            Exception("Order doesnot exist")


class NotificationService:
    def send_order_notification(self, user, content):
        notifcation = MobileNotification(user, content)
        notifcation.send_notification()
        return notifcation

    def send_sms_notification(self, user, content):
        notifcation = SmsNotification(user, content)
        notifcation.send_notification()
        return notifcation


class ShippmentService:
    def __init__(self):
        self.__shipments = {}

    def create_shipment(self, orderId):
        shippmendId = f"ORD-{orderId}-{datetime.now().timestamp()}"
        self.__shipments[shippmendId] = (ShipmentStatus.IN_TRANSIT, orderId)
        print(f"Order {shippmendId} created with {shippmendId} items")
        return shippmendId

    def get_shippments_for_orderid(self, orderId):
        return [sid for sid, (_, oid) in self.__shipments.items() if oid == orderId]

    def is_in_transit(self, shipmentId):
        status, _ = self.__shipments.get(shipmentId, (None, None))
        return status in (ShipmentStatus.IN_TRANSIT, ShipmentStatus.SHIPPED)

    def cancel_shipment_with_fee(self, shipmentId):
        print(f"Shipment {shipmentId} cancelled with transit fee")
        self.__shipments[shipmentId] = (
            ShipmentStatus.CANCELLED,
            self.__shipments[shipmentId][1],
        )
        return 100

    def cancel_shipment(self, shipmentId):
        print(f"Shipment {shipmentId} cancelled with transit fee")
        self.__shipments[shipmentId] = (
            ShipmentStatus.CANCELLED,
            self.__shipments[shipmentId][1],
        )
