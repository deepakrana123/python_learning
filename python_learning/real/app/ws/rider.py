from fastapi import WebSocket, WebSocketDisconnect
from app.ws.manager import ConnectionManager
from app.core.state import live_locations
import asyncio

manager = ConnectionManager()


async def rider_ws(websocket: WebSocket, ride_id: str):
    await manager.connect(ride_id, websocket)

    if ride_id in live_locations:
        await websocket.send_json(live_locations[ride_id])

    try:
        while True:
            await asyncio.sleep(3)
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ride_id, websocket)
