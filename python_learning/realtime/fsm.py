# Event Source → Ingestion → Queue → Processor → State → Broadcast → Clients

# multi fsm , a single fsm quickly becomes exhuasted , too larege and complex and impossible to debug
#  so what we do we break fsm on the basis of requriement to build single responsibility system


# Event bsus(central communication system)

import threading
from queue import Queue


class EventBus:
    def __init__(self):
        self.subscribers = {}
        self.lock = threading.Lock()

    def subscribe(self, event_type, handler):
        with self.lock:
            self.subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event_type, data=None):
        handlers = []
        with self.lock:
            handlers = self.subscribers.get(event_type)
        for handler in handlers:
            handler(data)


class BaseFSM:
    def __init__(self, name):
        self.name = name
        self.state = None

    def transition(self, to_state):
        print(f"[{self.name}] {self.state}->")
        self.state = to_state

    def handle(self, event):
        raise NotImplementedError


class CaptureFSM(BaseFSM):
    def __init__(self, bus):
        super().__init__("CaptureFSM")
        self.bus = bus
        self.state = "IDLE"

    def start_capture(self):
        self.transition("CAPTURING")
        self.bus.publish("capture_done", {"image": "raw_image_data"})


class EncoderFSM(BaseFSM):
    def __init__(self, bus):
        super().__init__("EncoderFSM")
        self.bus = bus
        self.state = "IDLE"
        bus.subscribe("capture_done", self.handle)

    def handle(self, data):
        self.transition("Encoding")
        encoded = f"encoded({data['image']})"
        self.bus.publish("encode_done", {"image": encoded})
        self.transition("IDLE")


class UploadFSM(BaseFSM):
    def __init__(self, bus):
        super().__init__(bus)
        self.bus = bus
        self.state = "IDLE"
        bus.subscribe("encode_done", self.handle)

    def handle(self, data):
        self.transition("UPLOADING")
        print("Uploading", data["image"])
        self.transition("IDLE")


bus = EventBus()

capture = CaptureFSM(bus)
encoder = EncoderFSM(bus)
upload = UploadFSM(bus)

capture.start_capture()


#  async mulit-fsm , real time systems rarely execute in single loop

import asyncio
from collections import defaultdict


class AsyncEventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event_type, handler):
        self.subscribers[event_type].append(handler)

    async def publish(self, event_type, data):
        handlers = self.subscribers(event_type, [])
        for h in handlers:
            asyncio.create_task(h(data))


class AsyncFSM:
    def __init__(self, name):
        self.name = name
        self.state = "IDLE"

    def transition(self, to):
        print(f"[{self.name}] {self.state} → {to}")
        self.state = to

    async def handle(self, data):
        raise NotImplementedError


class CaptureFSM(AsyncFSM):
    def __init__(self, bus):
        super().__init__("CaptureFSM")
        self.bus = bus

    async def start(self):
        self.transition("CAPTURING")
        await asyncio.sleep(1)
        await self.bus.publish("capture_done", {"image": "raw"})
        self.transition("IDLE")


class EncoderFSM(AsyncFSM):
    def __init__(self, bus):
        super().__init__("Encoder")
        self.bus = bus
        bus.subscribe("capture_done")

    async def handle(self, data):
        self.transition("ENCODING")
        await asyncio.sleep(0.5)
        encoded = f"encoded({data})"
        await self.bus.publish("encode_done", {"image": encoded})
        self.transition("IDLE")


class UploaderFSM(AsyncFSM):
    def __init__(self, bus):
        super().__init__("Upload")
        self.bus = bus
        bus.subscribe("encode_decoded")

    async def handle(self, data):
        self.transition("Uploading")
        await asyncio.sleep(0.7)
        print("Uploaded:", data)
        self.transition("IDLE")


async def main():
    bus = AsyncEventBus()
    capture = CaptureFSM(bus)
    encoder = EncoderFSM(bus)
    upload = UploaderFSM(bus)

    while True:
        await capture.start()
        await asyncio.sleep(2)


asyncio.run(main())

# What is a Hierarchical FSM (HFSM)?

# A hierarchical FSM means:

# A parent state contains child states inside it.

# Enter parent = child automatically starts.

# Exit parent = child is terminated/reset.

# Parent decides high-level mode, child handles fine details.


class PaymentFSM:
    def __init__(self):
        self.state = "VERIFYING"
        self.retry = 0
        self.MAX_RETRY = 3

    def handle(self, event):
        if self.state == "VERIFYING":
            if event == "payment_success":
                self.state = "SUCCESS"
            elif event == "payment_failed":
                self.state = "RETRY"
        elif self.state == "RETRY":
            if event == "retry":
                if self.retry < self.MAX_RETRY:
                    self.retry += 1
                    self.state = "VERIFYING"
                else:
                    self.state = "FAILED"
        if self.state in ("SUCCESS", "FAILED"):
            return self.state
        return self.state


class TableDrivenPaymentFSM:
    def __init__(self):
        self.state = "VERIFYING"
        self.retry = 0
        self.MAX_RETRY = 3
        self.table = {
            ("VERIFYING", "success"): ("SUCCESS", None),
            ("VERIFYING", "fail"): ("RETRY", self.increment_retry),
            ("RETRY", "retry"): ("VERIFYING", None),
            ("RETRY", "max_retry"): ("FAILED", None),
            ("SUCCESS", "*"): ("SUCCESS", None),
            ("FAILED", "*"): ("FAILED", None),
        }

    def increment_retry(self):
        self.retry += 1

    def handle(self, event):
        if self.state == "RETRY" and self.retry >= self.MAX_RETRY:
            event = "max_retry"
        key = (self.state, event)
        if key not in self.table:
            key = (self.state, "*")
        next_state, action = self.table[key]
        if action:
            action()
        self.state = next_state
        return self.state


class TableDrivenDeliveryFSM:
    def __init__(self):
        self.state = "PACKING"
        self.retry = 0
        self.MAX_RETRY = 3
        self.table = {
            ("PACKING", "success"): ("SHIPPED", None),
            ("PACKING", "fail"): ("FAILED", None),
            # ("RETRY", "retry"): ("PACKING", None),
            # ("RETRY", "max_retry"): ("FAILED", None),
            ("SHIPPED", "*"): ("SHIPPED", None),
            ("FAILED", "*"): ("FAILED", None),
        }

    def handle(self, event):
        key = (self.state, event)
        if key not in self.table:
            key = (self.state, "*")
        next_state, action = self.table[key]
        if action:
            action()
        self.state = next_state
        return self.state


class TableDrivenOrder:
    def __init__(self):
        self.state = "ORDER_ACTIVE"
        self.payment_fsm = TableDrivenPaymentFSM()
        self.delivery_fsm = TableDrivenDeliveryFSM()

    def handle_payment_event(self, event):
        if self.state != "ORDER_ACTIVE":
            return self.state
        payment_state = self.payment_fsm.handle(event)
        delivery_state = self.delivery_fsm.handle(event)

        if payment_state == "FAILED":
            self.state = "ORDER_FAILED"
        elif payment_state == "SUCCESS":
            self.state = "ORDER_SUCCESS"
        elif delivery_state == "FAILED":
            self.state = "ORDER_FAILED"
        elif delivery_state == "SUCCESS":
            self.state = "ORDER_SUCCESS"
        return self.state
