import asyncio


def notification_consumer(stock, notification_queue, ws_manager):
    while True:
        msg = notification_queue.pop(stock)
        if msg:
            print(f"[Notify--{stock}] {msg}")
            asyncio.run(ws_manager.send(stock, msg))
