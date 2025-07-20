from typing import Dict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connection: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connection[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connection:
            del self.active_connection[user_id]

    async def send_personal_message(self, message: str, user_id: int):
        websocket = self.active_connection[user_id]
        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message):
        for connection in self.active_connection.values():
            await connection.send_text(message)
