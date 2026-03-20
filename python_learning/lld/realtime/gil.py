# import sys

# a = []
# b = a

# a.append("push")
# b.append("push1")
# print(b)
# print(sys.getrefcount(a))
# print(sys.getrefcount(b))

# import asyncio, random, time


# async def event_producer(queue):
#     for i in range(1, 21):  # 20 events
#         event = {
#             "event_id": i,
#             "timestamp": time.time(),
#             "value": random.randint(1, 100),
#         }
#         try:
#             queue.put_nowait(event)
#         except asyncio.QueueFull:
#             print(f"Queue full, dropping event {i}")
#         await asyncio.sleep(0.1)


# async def event_consumer(queue):
#     while True:
#         event = await queue.get()
#         print("Processing event:", event)
#         queue.task_done()


# async def main():
#     q = asyncio.Queue(maxsize=5)
#     asyncio.create_task(event_producer(q))
#     await event_consumer(q)


# asyncio.run(main())

# state = {"sum": 0, "count": 0}


# async def event_consumer(queue):
#     while True:
#         event = await queue.get()
#         state["sum"] += event["value"]
#         state["count"] += 1
#         print("Updated state:", state)
#         queue.task_done()


import asyncio
import random
import time


async def event_producer(queue):
    for i in range(1, 21):
        event = {
            "event_id": i,
            "timestamp": time.time(),
            "value": random.randint(1, 100),
        }

        try:
            queue.put_nowait(event)
            print(f"Produced: {event}")
        except asyncio.QueueFull:
            print(f"❌ Dropped event: {event['event_id']}")
        await asyncio.wait(0.1)


state = {"runs": 0, "balls": 0}


async def event_consumer(queue):
    while True:
        last_id = 0
        try:
            event = await asyncio.wait_for(queue.get(), timeout=1)
            if event["event_id"] < last_id:
                print("ignore event")
            state["runs"] += event["value"] % 6  # random score
            state["balls"] += 1
            last_id = event["event_id"]

            print(f"Updated State: {state}")
            print(f"Consumed: {event}")
            await asyncio.sleep(0.2)
            queue.task_done()
        except asyncio.TimeoutError:
            print("⏱ No events for 1 second → flushing queue")
            while not queue.empty():
                dropped = queue.get_nowait()
                print(f"🗑 Flushed: {dropped}")
                queue.task_done()


async def main():
    queue = asyncio.Queue(maxsize=5)
    asyncio.create_task(event_producer(queue))
    await event_consumer(queue)


asyncio.run(main())
