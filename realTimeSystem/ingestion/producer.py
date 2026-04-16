import threading
import time
import random
from threading import Lock
from realTimeSystem.model.market import (
    MarketEvent,
    companiesWithPrice,
    GLOBAL_LIMIT,
    MAX_PER_STOCK,
)
from typing import Callable
from realTimeSystem.metrics.metrics import metrics

latest_event_by_stock = {}
latest_lock = threading.Lock()
last_price_stock = {}


def generate_event():
    stock_name, price = random.choice(companiesWithPrice)
    base_price = last_price_stock.get(stock_name, price)
    new_price = base_price + random.uniform(-20, 20)
    last_price_stock[stock_name] = new_price
    timestamp = time.time()
    return stock_name, new_price, timestamp


def start_producer(generate_event: Callable, event_queue) -> None:
    while True:
        stock, price, ts = generate_event()
        metrics.inc("events_generated")
        event = MarketEvent(stock, price, ts)
        stock = event.stock
        with latest_lock:
            latest_event_by_stock[stock] = event
        if event_queue.size(stock) > MAX_PER_STOCK:

            continue
        if event_queue.total_size() > GLOBAL_LIMIT:
            time.sleep(0.05)
            continue

        event_queue.push(stock, stock, event.timestamp)
        time.sleep(0)
