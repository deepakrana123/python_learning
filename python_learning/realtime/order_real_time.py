import queue
import threading
import time


class Actor:
    def __init__(self, name):
        self.name = name
        self.mailbox = queue.Queue()
        self.running = True
        threading.Thread(target=self._run, daemon=True)

    def send(self, msg):
        self.mailbox.put(msg)

    def _run(self):
        while self.running:
            msg = self.mailbox.get()
            self.receive(msg)

    def receive(self, msg):
        raise NotImplementedError


class Scheduler:
    @staticmethod
    def schedule(delay_sec, actor, message):
        def task():
            time.sleep(delay_sec)
            actor.send(message)

        threading.Thread(target=task, daemon=True)


class PaymentActor(Actor):
    def __init__(self, order_actor):
        super().__init__("PaymentActor")
        self.state = "VERIFYING"
        self.retry = 0
        self.MAX_RETRY = 3
        self.order_actor = order_actor

    def receive(self, msg):
        if self.state in ("SUCCESS", "FAILED"):
            return
        if msg == "START_PAYMENT":
            self._verify()
        elif msg == "RETRY":
            self._verify()

    def _verify(self):
        print("[Payment] Verifying payment ...")
        success = self.retry >= 2
        if success:
            self.state = "SUCCESS"
            self.order_actor.send("PAYMENT_SUCCESS")
        else:
            self.retry += 1
            print("[Payment] Verifying failed ...")
            if self.retry < self.MAX_RETRY:
                Scheduler.schedule(1, self, "RETRY")
            else:
                self.state = "FAILED"
                self.order_actor.send("PAYMENT_FAILURE")


class DeliveryActor(Actor):
    def __init__(self, order_actor):
        super().__init__("DeliveryActor")
        self.state = "PACKING"
        self.order_actor = order_actor

    def receive(self, msg):
        if self.state in ("DELIVERED", "FAILED"):
            return

        if msg == "START_DELIVERY":
            print("[Delivery] Packing order...")
            Scheduler.schedule(1, self, "SHIP")

        elif msg == "SHIP":
            print("[Delivery] Shipped")
            self.state = "DELIVERED"
            self.order_actor.send("DELIVERY_SUCCESS")


class OrderActor(Actor):
    def __init__(self):
        super().__init__("OrderActor")
        self.phase = "INIT"
        self.payment = PaymentActor(self)
        self.delivery = DeliveryActor(self)
        self.inventory = InventoryActory(self)
        self.refund = RefundActor(self)

    def receive(self, msg):
        print("[Order] Phase={self.phase},Event={msg}")
        if self.phase in ("COMPLETED", "FAILED", "CANCELLED"):
            return
        if self.phase == "INIT":
            if msg == "START":
                self.phase = "WAIT_PAYMENT"
                self.payment.send("START_PAYMENT")
        elif self.phase == "WAIT_PAYMENT":
            if msg == "PAYMENT_SUCCESS":
                self.phase = "INVENTORY_AVAILABLE"
                self.inventory.send("CHECK_INVENTORY")
            elif msg == "PAYMENT_FAILED":
                self.phase = "FAILED"
        elif self.phase == "WAIT_INVENTORY":
            if msg == "INVENTORY_SUCCESS":
                self.phase = "WAIT_DELIVERY"
                self.delivery.send("START_DELIVERY")
            elif msg == "INVENTORY_FAILED":
                self.phase = "FAILED"
                refund_id = f"refund:{self.order_id}"
                self.refund.send(
                    {
                        type: "START_REFUND",
                        "refund_id": refund_id,
                        "amount": self.amount,
                    }
                )
        elif self.phase == "WAIT_DELIVERY":
            if msg in ("ORDER_CANCEL", "DELIVERY_FAILED"):
                self.phase = "WAIT_REFUND"
                refund_id = f"refund:{self.order_id}"
                self.refund.send(
                    {
                        type: "START_REFUND",
                        "refund_id": refund_id,
                        "amount": self.amount,
                    }
                )
            if msg == "DELIVERY_SUCCESS":
                self.phase = "COMPLETED"
        elif self.phase == "WAIT_REFUND":
            if msg == "REFUND_SUCCESS":
                self.phase = "FAILED"
            elif msg == "REFUND_FAILED":
                self.phase = "FAILED"


class InventoryActory(Actor):
    def __init__(self, order_actor):
        self.state = "INIT"
        self.order_actor = order_actor

    def receive(self, msg):
        if self.state in ("SUCCESS", "FAILED"):
            return
        if self.state == "INIT":
            if msg == "CHECK_INVENTORY":
                self.state = "CHECKING"
                self._check_inventory()
        elif self.state == "CHECK_INVENTORY":
            if msg == "INVENTORY_AVAILABLE":
                self.state = "RESERVED"
                self.order_actor.send("INVENTORY_AVAILABLE")
            elif msg == "INVENTORY_UNAVAILABLE":
                self.state = "FAILED"
                self.order_actor.send("INVENTORY_UNAVAILABLE")

    def _check_inventory(self):

        avaiable = True
        if avaiable:
            self.send("INVENTORY_AVAILABLE")
        else:
            self.send("INVENTORY_UNAVAILABLE")


class RefundActor(Actor):
    # def __init__(self, order_actor):
    #     super().__init__("RefundActor")
    #     self.state = "INIT"
    #     self.processed_refunds = set()
    #     self.order_actor = order_actor

    # def receive(self, msg):
    #     if self.state in ("SUCCESS", "FAILED"):
    #         return
    #     if self.state == "INIT":
    #         self.state = "REFUND_METHOD_SELECTION"
    #     elif self.state == "REFUND_METHOD_SELECTION":
    #         if msg.startswith("METHOD_"):
    #             self.state = "PROCESSING"
    #             self._process_refund(msg)
    #     elif self.state == "PROCESSING":
    #         if msg == "REFUND_SUCCESS":
    #             self.state = "SUCCESS"
    #             self.order_actor.send("REFUND_DONE")
    #         elif msg == "REFUND_FAILED":
    #             self.state = "FAILED"
    #             self.order_actor.send("REFUND_FAILED")

    # def _process_refund(self, method):
    #     print(f"[Refund] Processing refund via {method}")
    #     Scheduler.schedule(1, self, "REFUND_SUCCESS")

    def __init__(self, order_actor, scheduler):
        super().__init__("RefundActor")
        self.state = "IDLE"
        self.order_actor = order_actor
        self.scheduler = scheduler
        self.retry = 0
        self.MAX_RETRY = 3
        self.refund_id = None
        self.processed_refunds = set()

    def receive(self, msg):
        if self.state in ("SUCCESS", "FAILED"):
            return
        if msg["type"] == "START_REFUND":
            self.refund_id = msg["refund_id"]
            if self.refund_id in self.processed_refunds:
                self.state = "SUCCESS"
                self.order_actor.send("REFUND_SUCCESS")
                return
            self.state = "PROCESSING"
            self._attempt_refund()
        elif msg["type"] == "REFUND_TIMEOUT":
            self._handle_timeout()
        elif msg["type"] == "REFUND_RESPONSE":
            self._handle_response(msg["success"])

    def _attempt_refund(self):
        print(f"[Refund] attempt {self.retry+1}")
        self.scheduler.schedule(
            delay=3, target=self, message={"type": "REFUND_TIMEOUT"}
        )
        success = False if self.retry < 2 else True
        self.send({"type": "REFUND_RESPONSE", "success": success})

    def _handle_timeout(self):
        print("[Refund] Timeout occurred")
        self.retry += 1
        if self.retry >= self.MAX_RETRY:
            self.state = "FAILED"
            self.order_actor.send("REFUND_FAILED")
        else:
            self._attempt_refund()

    def _handle_response(self, success):
        if success:
            self.processed_refunds.add(self.refund_id)
            self.state = "SUCCESS"
            self.order_actor.send("REFUND_SUCCESS")
        else:
            self.retry += 1
            if self.retry >= self.MAX_RETRY:
                self.state = "FAILED"
                self.order_actor.send("REFUND_FAILED")
            else:
                self._attempt_refund()


order = OrderActor()
order.send("START")
time.sleep(5)
print("Final Order State:", order.phase)
