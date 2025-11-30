# Event Source → Ingestion → Queue → Processor → State → Broadcast → Clients

# 1️⃣ Event Source

# Jo input data generate kare

# Umpire scoring

# GPS location from driver

# Sensor data

# User actions

# 2️⃣ Ingestion Layer

# Events ko receive karna

# HTTP

# WebSocket

# MQTT

# Kafka

# 3️⃣ Queue (MOST IMPORTANT)

# Events ko buffer karta hai

# Backpressure prevent karta hai

# Ordering maintain karta hai

# Consumer ko non-stop feed deta hai

# 4️⃣ Processing Engine

# Event ko parse karna

# State update

# Business logic

# 5️⃣ State Store

# Latest values store karna

# Latest score

# Latest driver location

# Latest battery %

# 6️⃣ Broadcast

# Clients ko push update

# WebSockets

# SSE

# Push messages

# Pub/Sub

# a bounded async queueu banao
# producer->events generate kare,consumer->events process kare
# queue full hone par event drop ho


import asyncio
import random
import time


async def event_producer(queue):
    for i in range(1, 31):
        event = {
            "event_id": i,
            "timestamp": time.time(),
            "value": random.randint(1, 100),
        }
        try:
            queue.put_nowait(event)
            print(f"Produced:{event}")
        except asyncio.QueueFull:
            print(f"dropped event")
        await asyncio.sleep(0.05)


async def event_consumer(queue):
    while True:
        event = await queue.get()
        print(f"consumer:{event}")
        await asyncio.sleep(0.2)
        queue.task_done()


async def main():
    queue = asyncio.Queue(maxsize=5)
    asyncio.create_task(event_producer)
    await event_consumer(queue)


asyncio.run(main())


# outcome ->queue full hogi , some events drop honge , real-ie system ka backpressure


#  exercise-2,state updated

# goal-> consume events -> state update
# option A:Scoreboard
# state={"runs":0,"balls":0}
# state={"location":(0,0),"distance":0}

state = {"runs": 0, "balls": 0}


async def event_consumer(queue):
    while True:
        event = await queue.get()
        state["runs"] += event["value"] % 6
        state["balls"] += 1
        print(f"updated state:{state}")
        queue.task_done()


# outcome -> real-time state update ka concept,live dhahboard backend ka foundation
