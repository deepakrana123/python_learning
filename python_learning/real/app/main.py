from fastapi import FastAPI, WebSocket
from app.ws.driver import driver_ws
from app.ws.rider import rider_ws

app = FastAPI()


@app.websocket("/ws/driver")
async def driver_endpoint(websocket: WebSocket):
    await driver_ws(websocket)


@app.websocket("/ws/rider/{ride_id}")
async def rider_endpoint(websocket: WebSocket, ride_id: str):
    await rider_ws(websocket, ride_id)
