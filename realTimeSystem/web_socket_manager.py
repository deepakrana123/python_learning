from collections import defaultdict


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
        for ws in self.client_by_stock[stock]:
            try:
                await ws.send_text(message)
            except:
                dead_clients.append(ws)

        for dc in dead_clients:
            self.client_by_stock[stock].remove(dc)
