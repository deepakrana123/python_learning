from enum import Enum


class PaymentStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"
    REFUNDED = "Refunded"
    PARTIALLY_REFUNDED = "Partially Refunded"
    AUTHORIZED = "Authorized"
    DECLINED = "Declined"


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
