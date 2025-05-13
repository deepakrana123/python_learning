import random
import time
import asyncio


class SagaStore:
    def __init__(self):
        self.saga = {}

    async def save_state(self, order_id, state):
        self.saga[order_id] = state

    async def get_state(self, order_id):
        if order_id in self.saga:
            return self.saga[order_id]
        return None

    async def delete_state(self, order_id):
        if order_id in self.saga:
            del self.saga[order_id]


async def retry_async(operation, retries=3, delay=1, backoff=2, jitter=False):
    attempt = 0
    while attempt < retries:
        try:
            result = operation()
            return result
        except Exception as e:
            attemtt += 1
            print(f"retry {attempt}/{retries}")
            if attempt == retries:
                print("Max retires reached")
                raise
            sleep_time = delay * (backoff ** (attempt - 1))
            if jitter:
                sleep_time += random.uniform(0, 0.5)
            print(f"retrying after {sleep_time}")
            time.sleep(sleep_time)


# aio breaker libary for circuit breaker
class CircuitBreaker:
    def __init__(self, failure_threshold, recovery_timeout):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_failure_time = None

    async def call(self, operation):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time:
                print("CircuitBreaker")
                self.state = "HALF-CREATED"
            else:
                raise Exception("Circuit Breaker")
        try:
            result = await operation()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        if self.state in ["OPEN", "HALF-OPEN"]:
            print("Circuit Breaker")
        self.failure_count = 0
        self.state = "CLOSED"

    def _on_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.last_failure_time = time.time()
            print("CircuitBreaker: To many failure opening circuit")


class InventoryService:
    async def reserve_stock(self, order_id):
        print(f"(inventroy) reserving stock for {order_id}")
        await asyncio.sleep(0.5)
        return True

    async def remove_stock(self, order_id):
        print(f"(inventory) remove order {order_id} from inventory")
        await asyncio.sleep(0.5)
        return True


class PaymentService:
    async def make_payment(self, order_id):
        print(f"[PaymentService] Charging payment for order {order_id}")
        await asyncio.sleep(0.5)
        if random.random() < 0.5:
            raise Exception("Payment ")
        return True

    async def refund(self, order_id):
        print(f"[Payment] for {order_id} done in your required mode")
        return True


class ShippingService:
    async def create_shipment(self, order_id):
        print(f"[Shippment] for {order_id} done in your required mode")
        await asyncio.sleep(0.5)
        return True


# from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


# @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10), retry=retry_if_exception_type(Exception))
# def charge_payment(order_id):
# it can be done wih backoff libary to and tenacity , its retry operations
class SagaOrchestions:
    def __init__(self):
        self.payemnt = PaymentService()
        self.shipping = ShippingService()
        self.inventoy = InventoryService()
        self.payment_circuit_breaker = CircuitBreaker(
            failure_threshold=2, recovery_timeout=2
        )
        self.saga_store = SagaStore()

    async def execute(self, order_id):
        # if not retry(lambda: self.payemnt.make_payment(order_id)):
        #     self.payemnt.make_payment(order_id)
        #     return
        # if not self.payemnt.make_payment(order_id):
        #     print("Saga failed to payment order")
        #     return
        # if not self.shipping.create_shipment(order_id):
        #     print("Saga failed to shipping order")
        #     return
        state = await self.saga_store.get_state(order_id)
        if not state or state == "START":
            if not await self.inventoy.reserve_stock(order_id):
                print("Failed to reserved")
                return
            await self.saga_store.save_state(order_id, "STOCK_RESVERED")

        state = await self.saga_store.get_state(order_id)
        if state == "STOCK_RESERVED":
            try:
                await retry_async(lambda: self.payemnt.make_payment)
                await self.saga_store.save_state(order_id, "PAYMENT_CHARGED")
            except Exception as e:
                print(f"payment failed")
                print(f"starting compensation")
                await self.inventoy.remove_stock(order_id)
                return
        state = await self.saga_store.get_state(order_id)
        if state == "PAYMENT_CHARGED":
            if not await self.shipping.create_shipment(order_id):
                print("failed to create shipment")
                await self.payemnt.refund(order_id)
                await self.inventoy.remove_stock(order_id)
                await self.saga_store.delete_state(order_id)
                return
        await self.saga_store.delete_state(order_id)
