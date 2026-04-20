from collections import defaultdict
import random


class WebSocketManager:
    def __init__(self):
        self.client_by_stock = defaultdict(set)

    async def connect(self, websocket, stock):
        await websocket.accept()
        self.client_by_stock[stock].add(websocket)

    def disconnect(self, websocket, stock):
        self.client_by_stock[stock].remove(websocket)

    async def send(self, stock, message):
        dead_clients = []
        clients = self.client_by_stock[stock]
        if not clients:
            # ─────────────────────────────────────────────
            # PREVIOUS CODE:
            # if random.random() < 0.3:
            #     raise Exception("Various")
            #
            # BUG: Artificial 30% random failure injected even when there are legitimately no clients.
            # This has two problems:
            # 1. It floods the retry queue with failures that aren't real delivery failures —
            #    there's nobody to deliver to, so "failure" is meaningless here.
            # 2. retry_worker will keep retrying these, burning resources, and they'll
            #    eventually land in the DLQ — polluting dead-letter metrics with fake failures.
            # No-clients is a valid no-op, not an error. Just return silently.
            return
        success = 0
        dead_clients = []
        for ws in clients:
            try:
                await ws.send_text(message)
                success += 1
            except:
                dead_clients.append(ws)
        for dc in dead_clients:
            self.client_by_stock[stock].remove(dc)
        if success == 0:
            raise Exception("All websocket sends fails")
