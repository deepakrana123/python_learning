# Event Source → Ingestion → Queue → Processor → State → Broadcast → Clients

# 1️⃣ Event Source

# Jo input data generate kare

# Umpire scoring

# GPS location from driver

# Sensor data

# User actions

# 2️⃣ Ingestion Layer

# Events ko receive karna

# HTTP

# WebSocket

# MQTT

# Kafka

# 3️⃣ Queue (MOST IMPORTANT)

# Events ko buffer karta hai

# Backpressure prevent karta hai

# Ordering maintain karta hai

# Consumer ko non-stop feed deta hai

# 4️⃣ Processing Engine

# Event ko parse karna

# State update

# Business logic

# 5️⃣ State Store

# Latest values store karna

# Latest score

# Latest driver location

# Latest battery %

# 6️⃣ Broadcast

# Clients ko push update

# WebSockets

# SSE

# Push messages

# Pub/Sub

# a bounded async queueu banao
# producer->events generate kare,consumer->events process kare
# queue full hone par event drop ho


import asyncio
import random
import time


async def event_producer(queue):
    for i in range(1, 31):
        event = {
            "event_id": i,
            "timestamp": time.time(),
            "value": random.randint(1, 100),
        }
        try:
            queue.put_nowait(event)
            print(f"Produced:{event}")
        except asyncio.QueueFull:
            print(f"dropped event")
        await asyncio.sleep(0.05)


async def event_consumer(queue):
    while True:
        event = await queue.get()
        print(f"consumer:{event}")
        await asyncio.sleep(0.2)
        queue.task_done()


async def main():
    queue = asyncio.Queue(maxsize=5)
    asyncio.create_task(event_producer)
    await event_consumer(queue)


asyncio.run(main())


# outcome ->queue full hogi , some events drop honge , real-ie system ka backpressure


#  exercise-2,state updated

# goal-> consume events -> state update
# option A:Scoreboard
# state={"runs":0,"balls":0}
# state={"location":(0,0),"distance":0}

state = {"runs": 0, "balls": 0}


async def event_consumer(queue):
    while True:
        event = await queue.get()
        state["runs"] += event["value"] % 6
        state["balls"] += 1
        print(f"updated state:{state}")
        queue.task_done()


# outcome -> real-time state update ka concept,live dhahboard backend ka foundation

state = {"state": "initial", "ordered": time.now()}


async def event_producer_mini_excerise(queue):
    for i in range(1, 40):
        event = {
            "event_id": i,
            "timestamp": time.time(),
            "value": random.randint(1, 100),
        }
        try:
            queue.put_nowait(event)
            print(f"Produced:{event}")
        except asyncio.QueueFull:
            print(f"dropped event")
        await asyncio.sleep(0.05)


async def event_consumer(queue):
    while True:
        event = await queue.get()
        if event["state"] == "this":
            print("this follow value")
            event["state"] = "now"
            queue.put_noawait(event)
        elif event["state"] == "now":
            print("now")


#  python real-time systems mostly asyncio se bante hai
# async queue , async tasks , await sleep , await network IO


# current_state = "IDLE"


# def handle_event(state, event):
#     if state == "IDLE" and event == "card_inserted":
#         return "ENTER_PIN"
#     if state == "ENTER_PIN" and event == "pin_entered":
#         return "SELECT_AMOUNT"
#     if state == "SELECT_AMOUNT" and event == "amount_selected":
#         return "Amount avilable"
#     if state == "DISPENSE_CASH" and event == "cash_dispensed":
#         return "DISPENSE_CASH"
#     if state == "ERROR" and event == "invalid_pin":
#         return "ERROR"
#     if state == "DONE" and event == "cancel":
#         return None

state = {"IDLE", "ENTER_PIN", "SELECT_AMOUNT", "DISPENSE_CASH", "DONE", "ERROR"}

timeout_at = None


def handle_event(state, event):
    global timeout_at

    if state == "IDLE":
        if event == "card_inserted":
            timeout_at = time.time() + 3
            return "WAITING_FOR_WAKEUP"
    elif state == "WAITING_FOR_WAKEUP":
        if event == "internal tick":
            if time.time() >= timeout_at:
                return "ENTER_PIN"
            return "state"
    elif state == "ENTER_PIN":
        if event == "pin_entered":
            return "SELECT_AMOUNT"
        if event == "invalid_pin":
            return "ERROR"
    elif state == "SELECT_AMOUNT":
        if event == "amount_selected":
            return "DISPENSE_CASH"
        if event == "cash_unavailable":
            return "ERROR"
        if event == "cancel":
            return "DONE"
    elif state == "DISPENSE_CASH":
        if event == "cash_dispensed":
            return "DONE"
    elif state == "ERROR":
        if event == "reset":
            return "IDLE"
    elif state == "DONE":
        if event == "finish":
            return "IDLE"

    return state


def loop():
    global state
    while True:
        state = handle_event(state, "internal_tick")
        print("State", state)
        time.sleep(0.2)


arr = ["retry", "cleanup", "heartbeat"]
i = 0


def timesleep():
    global i
    if i < 3:
        time.sleep(0.2)
        print(arr[i])

        i = i + 1


def handle_event(state, event):
    transitions = {
        "IDLE": {"card_inserted": "ENTER_PIN"},
        "ENTER_PIN": {"pin_entered": "SELECT_AMOUNT", "invalid_pin": "ERROR"},
        "SELECT_AMOUNT": {
            "amount_selected": "DISPENSE_CASH",
            "cash_unavailable": "ERROR",
            "cancel": "DONE",
        },
        "DISPENSE_CASH": {"cash_dispensed": "DONE"},
        "ERROR": {"reset": "IDLE"},
        "DONE": {"finish": "IDLE"},
        "WAITING": {"timeout": "IDLE"},
    }

    return transitions.get(state, {}).get(event, state)


timeout_at = None


def handle_event_washing(state, event):
    global timeout_at
    if state == "IDLE":
        if event == "switch_on":
            timeout_at = time.time() + 3
            return "WAITING_FOR_WAKEUP"
    elif state == "WAITING_FOR_WAKEUP":
        if event == "internal_tick":
            if time.time() > timeout_at:
                return "FILL_WATER"
            return state
    elif state == "FILL_WATER":
        if event == "water_filling":
            return "WASH"
        if event == "overflow_water":
            return "ERROR"
    elif state == "WASH":
        if event == "washing_swtich_on":
            timeout_at = time.time() + 3
            return "WAITING_FOR_WASH"
    elif state == "WAITING_FOR_WASH":
        if event == "started_washing":
            return "RISINE"
    elif state == "RISINE":
        if event == "risine_swtich_on":
            timeout_at = time.time() + 3
            return "WAIITNG_FOR_RISINE"
    elif state == "WAIITNG_FOR_RISINE":
        if event == "internal_tick":
            if time.time() > timeout_at:
                return "CLOSED"
            return state
    elif state == "CLOSED":
        return "ERROR"
    elif state == "ERROR":
        if event == "paused":
            return "DOOR_OPEN"


#  fsm gives code duplication , that why we move to hsm , which makes every parent have a child


class State:
    def on_event(self, event):
        return self


class Idle(State):
    def on_event(self, event):
        if event == "switch_on":
            return WashingMode()
        return self


class WashingMode(State):
    def on_event(self, event):
        # Common guards (parent rules)
        if event == "door_open":
            return ErrorMode()

        # Child delegation
        return self.state.on_event(event)

    def __init__(self):
        self.state = FillWater()


class FillWater(State):
    def on_event(self, event):
        if event == "water_ok":
            return Wash()
        return self
