from queue import Queue
import threading
import time
from fastapi import FastAPI, WebSocket
import asyncio

app = FastAPI()
q = Queue()
clients = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        clients.remove(websocket)


async def notify_clients(message):
    for client in clients:
        await client.send_text(message)


asyncio.create_task(notify_clients(f"{"event""stock"} crossed threshold"))


class Event:
    def __init__(self, stock, price):
        self.stock = stock
        self.price = price


class Rule:
    def __init__(self, stock, threshold):
        self.stock = stock
        self.threshold = threshold

    def matches(self, event):
        return event.stock == self.stock and event.price > self.threshold


class Processor:
    def __init__(self, rules):
        self.rules = rules

    def process(self, event):
        if event.stock in self.rules:
            for rule in self.rules[event.stock]:
                if rule.matches(event):
                    print(f"ALERT: {event.stock} crossed {rule.threshold}")


# def producer():
#     for i in range(100):
#         q.put(i)


# rules = [
#     Rule("RELIANCE", 2500),
#     Rule("TCS", 6500),
#     Rule("WIPRO", 3500),
#     Rule("INFOYS", 350),
#     Rule("TATA", 2510),
#     Rule("BATA", 250),
# ]
rules_by_stock = {
    "RELIANCE": [
        Rule("RELIANCE", 1500),
        Rule("RELIANCE", 2500),
        Rule("RELIANCE", 9500),
    ],
    "TCS": [Rule("TCS", 500), Rule("TCS", 1500), Rule("TCS", 5500), Rule("TCS", 4500)],
    "BATA": [
        Rule("BATA", 1250),
        Rule("BATA", 2506),
        Rule("BATA", 2502),
        Rule("BATA", 2510),
    ],
    "CAPITAL": [Rule("BATA", 100)],
}

# threading.Thread(target=producer).start()
processor = Processor(rules_by_stock)
multithreadQueue = {}
for value in [
    Event("TATA", 2600),
    Event("RELIANCE", 2600),
    Event("BATA", 2600),
    Event("TATA", 600),
    Event("CAPITAL", 100),
]:
    if value.stock not in multithreadQueue:
        multithreadQueue[value.stock].put(value)

        multithreadQueue[value.stock] = Queue()


def consumer(stock):
    q = multithreadQueue[stock]
    while True:
        if not q.empty():
            event = q.get()
            print(f"[{stock}] Processing {event.stock} {event.price}")
            processor.process(event)
            time.sleep(0.03)


for stock in multithreadQueue:
    threading.Thread(target=consumer, args=(stock,)).start()
