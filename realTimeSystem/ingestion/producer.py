import threading
import time
import random
from threading import Lock
from realTimeSystem.model.market import (
    MarketEvent,
    companies,
    GLOBAL_LIMIT,
    MAX_PER_STOCK,
)
from typing import Callable

latest_event_by_stock = {}
latest_lock = threading.Lock()
last_price_stock = {}


def generate_event():
    stock_name, price = random.choice(companies)
    base_price = last_price_stock.get(stock_name, price)
    new_price = base_price + random.uniform(-20, 20)
    last_price_stock[stock_name] = new_price
    timestamp = time.time()
    return stock_name, new_price, timestamp


def start_producer(generate_event: Callable, event_queue) -> None:
    from realTimeSystem.model.market import MarketEvent

    while True:
        stock, price, ts = generate_event()
        event = MarketEvent(stock, price, ts)
        stock = event.stock
        with latest_lock:
            event = latest_event_by_stock.get(stock)
        if event_queue.size(stock) > MAX_PER_STOCK:
            print(f"[BACKPRESSURE] Skipping {stock}")
            continue
        if event_queue.total_size() > GLOBAL_LIMIT:
            print("[GLOBAL BACKPRESSURE] slowing producer")
            time.sleep(0.05)
            continue

        event_queue.push(stock, stock)
        print(f"[Producer] Generated:{event}", event_queue.total_size())
        time.sleep(0.01)
