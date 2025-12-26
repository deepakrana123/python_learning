from fastapi import WebSocket
from typing import Dict, Set
import asyncio


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, ride_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(ride_id, set()).add(websocket)

    def disconnect(self, ride_id: str, websocket: WebSocket):
        self.active_connections.get(ride_id, set()).discard(websocket)

    async def broadcast(self, ride_id: str, message: str):
        for ws in self.active_connections.get(ride_id, []):
            asyncio.create_task(ws.send_json(message))
