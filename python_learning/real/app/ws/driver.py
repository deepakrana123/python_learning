from fastapi import WebSocket, WebSocketDisconnect
from app.core.schema import DriverLocationEvent
from app.core.state import live_location
from app.ws.manager import ConnectionManager

manager = ConnectionManager()


async def driver_ws(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            event = DriverLocationEvent(**data)
            current = live_location.get(event.ride_id)

            if current and event.seq <= current["seq"]:
                continue

            live_location[event.ride_id] = event.dict()

            await manager.broadcast(event.ride_id, event.dict())

            print(f"[Driver] Updated ride {event.ride_id}")
    except WebSocketDisconnect:
        print("[Driver] disconnected")
