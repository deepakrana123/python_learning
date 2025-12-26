# Browser → WebSockets
# Internal microservices → gRPC
# IoT devices/GPS → MQTT
# Hard real-time (games) → UDP

# Event Source → Ingestion → Queue → Processor → State → Broadcast → Clients
# Example flow:

# Producer → Message create

# Message → Queue me insert

# Queue full → Backpressure

# Consumer → Pull & process

# State update

# Idle → Flush

# Ordering maintained by index/id

# Iska diagram hi HLD ka 50%.

# Step-5: Tradeoffs

# Real-time ke tradeoffs:

# Latency vs Reliability

# Queuing vs Memory pressure

# gRPC vs REST

# Threads vs Event loop

# Bounded queue vs Dropping policy

# Consistency vs Speed

# Jitna honest hoga explanation → utna pro lagoge.
from fastapi import FastAPI, WebSocket
import time
import asyncio


class WSManager:
    def __init__(self):
        self.active = set()

    async def connections(self, ws):
        await ws.accept()
        self.active[ws] = time.time()

    def refresh(self, ws):
        self.active[ws] = time.time()

    def disconnect(self, ws):
        self.active.remove(ws)

    async def heartbeat_checker(self):
        while True:
            now = time.time()
            for ws, last in list(self.active):
                if now - last > 5:
                    print("Heartbeat lost")
                    self.disconnect(ws)
            await asyncio.sleep(1)

    async def broadcast(self, msg: str):
        for ws in list(self.active):
            try:
                await ws.send_text(msg)
            except:
                self.disconnect(ws)


manager = WSManager()
app = FastAPI()


@app.websocket("/ws")
async def websocket_connection_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            data = await ws.receive_text()
            print("Received:", data)
    except:
        manager.disconnect(ws)
