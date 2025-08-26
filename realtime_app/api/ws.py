from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, topic: str, websocket: WebSocket):
        await websocket.accept()
        if topic not in self.active_connections:
            self.active_connections[topic] = []
        self.active_connections[topic].append(websocket)

    def disconnect(self, topic: str, websocket: WebSocket):
        if topic not in self.active_connections:
            self.active_connections[topic].remove(websocket)
            if not self.active_connections[topic]:
                del self.active_connections[topic]

    async def send_to_topic(self, topic: str, message: str):
        if topic in self.active_connections:
            for connections in self.active_connections[topic]:
                await connections.send_json(message)


ws_manager = ConnectionManager()
