from queue import Queue
import threading
import time
from fastapi import FastAPI, WebSocket
import asyncio

app = FastAPI()
notification_queue = Queue()


class Event:
    def __init__(self, stock: str, price: float):
        self.stock = stock
        self.price = price


class Rule:
    def __init__(self, stock: str, threshold: str):
        self.stock = stock
        self.threshold = threshold

    def matches(self, event: Event) -> bool:
        return (
            event.stock == self.stock
            and event.price > 0
            and event.price > self.threshold
        )


class Processor:
    def __init__(self, rules: Rule):
        self.rules = rules

    def process(self, event: Event) -> None:
        if event.stock in self.rules:
            for rule in self.rules[event.stock]:
                if rule.matches(event):
                    notification_queue.put(
                        (event.stock, (f"Alret {event.stock} crossed {rule.threshold}"))
                    )


rules_by_stock = {
    "RELIANCE": [
        Rule("RELIANCE", 1500),
        Rule("RELIANCE", 2500),
        Rule("RELIANCE", 9500),
        Rule("RELIANCE", 2500),
        Rule("RELIANCE", 2500),
        Rule("RELIANCE", 2500),
    ],
    "TCS": [Rule("TCS", 500), Rule("TCS", 1500), Rule("TCS", 5500), Rule("TCS", 4500)],
    "BATA": [
        Rule("BATA", 1250),
        Rule("BATA", 2506),
        Rule("BATA", 2502),
        Rule("BATA", 2510),
    ],
    "CAPITAL": [Rule("CAPITAL", 100)],
    "INFY": [],
}

processor = Processor(rules_by_stock)
multithreadQueue = {}
existing_event = [
    Event("TATA", 2600),
    Event("RELIANCE", 1000),
    Event("BATA", 2600),
    Event("TATA", 00),
    Event("CAPITAL", 100),
]
for value in existing_event:
    if value.stock not in multithreadQueue:
        multithreadQueue[value.stock] = Queue()
    multithreadQueue[value.stock].put(value)


def consumer(stock):
    q = multithreadQueue[stock]
    while True:
        if not q.empty():
            event = q.get()
            processor.process(event)
            time.sleep(0.03)
        else:
            time.sleep(0.01)


for stock in multithreadQueue:
    threading.Thread(target=consumer, args=(stock,), daemon=True).start()

#  till there multithreaded system is ready now we move to notfication and dispatch logic and stuff build thinks around that


clients_by_stock = {}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, stock: str):
    await websocket.accept()
    if stock not in clients_by_stock:
        clients_by_stock[stock] = set()

    clients_by_stock[stock].add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        clients_by_stock[stock].remove(websocket)


# @app.websocket("/ws/notifications")
# async def websocket_endpoint(websocket:WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             if not notification_queue:
#                 notification = notification_queue.get()
#                 await websocket.send_text(notification)
#             await asyncio.sleep(0.1)
#     except:
#         await websocket.close()


async def dispatcher():
    while True:
        if not notification_queue.empty():
            stock, message = notification_queue.get()
            dead_clients = []
            for client in clients_by_stock[stock]:
                try:
                    await clients_by_stock[stock].send_text(message)
                except:
                    dead_clients.append(client)
            for dc in dead_clients:
                clients_by_stock[stock].remove(dc)
        await asyncio.sleep(0.03)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
# @app.on_event("startup")
# async def start_dispatcher():
#     asyncio.create_task(dispatcher())
