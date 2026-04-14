from fastapi import FastAPI, Websocket
from realTimeSystem.web_socket_manager import WebSocketManager

app = FastAPI()

ws_manager = WebSocketManager()


@app.websocket("/ws/{stock}")
async def websocket_endpoint(websocket: Websocket, stock: str):
    await ws_manager.connect(websocket, stock)
    try:
        while True:
            await websocket.receive_text()
    except:
        ws_manager.disconnect(websocket, stock)
