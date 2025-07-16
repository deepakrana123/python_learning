import grpc
import asyncio
import chat_pb2
import chat_pb2_grpc
import time
import uuid

USERNAME = "alice"
PASSWORD = "alicepass"
token = None


def generate_event():
    while True:
        action = input(
            "\nChoose (m=message, e=edit, d=delete, t=typing, p=presence, r=read): "
        )

        if action == "m":
            chat_id = input("Chat ID: ")
            text = input("Your message: ")
            yield chat_pb2.ChatEvent(
                message=chat_pb2.ChatMessage(
                    message_id=str(uuid.uuid4()),
                    sender=USERNAME,
                    message=text,
                    timestamp=int(time.time()),
                    chat_id=chat_id,
                )
            )

        elif action == "e":
            msg_id = input("Message ID to edit: ")
            new_text = input("New message: ")
            yield chat_pb2.ChatEvent(
                edit=chat_pb2.EditRequest(
                    message_id=msg_id, new_message=new_text, sender=USERNAME
                )
            )

        elif action == "d":
            msg_id = input("Message ID to delete: ")
            yield chat_pb2.ChatEvent(
                delete=chat_pb2.DeleteRequest(message_id=msg_id, sender=USERNAME)
            )

        elif action == "t":
            chat_id = input("Chat ID: ")
            typing = input("Typing? (y/n): ") == "y"
            yield chat_pb2.ChatEvent(
                typing=chat_pb2.TypingStatus(
                    user=USERNAME, is_typing=typing, chat_id=chat_id
                )
            )

        elif action == "p":
            online = input("Online? (y/n): ") == "y"
            yield chat_pb2.ChatEvent(
                presence=chat_pb2.PresenceStatus(
                    user=USERNAME, is_online=online, last_seen=int(time.time())
                )
            )

        elif action == "r":
            msg_id = input("Message ID read: ")
            yield chat_pb2.ChatEvent(
                receipt=chat_pb2.ReadReceipt(
                    message_id=msg_id, reader=USERNAME, read_timestamp=int(time.time())
                )
            )


async def login(stub):
    global token
    response = await stub.Login(
        chat_pb2.LoginRequest(username=USERNAME, password=PASSWORD)
    )
    if response.success:
        token = response.token
        print(f"✅ Logged in with token: {token}")
    else:
        print(f"❌ Login failed: {response.error}")
        exit(1)


async def listen(stub):
    metadata = [("authorization", token)]
    async with stub.ChatStream(generate_event(), metadata=metadata) as stream:
        async for event in stream:
            if event.HasField("message"):
                print(f"[{event.message.sender}] {event.message.message}")
            elif event.HasField("edit"):
                print(f"✏️ Message {event.edit.message_id} edited")
            elif event.HasField("delete"):
                print(f"❌ Message {event.delete.message_id} deleted")
            elif event.HasField("typing"):
                print(
                    f"⌨️ {event.typing.user} is {'typing...' if event.typing.is_typing else 'stopped typing'}"
                )
            elif event.HasField("presence"):
                status = "🟢 online" if event.presence.is_online else "🔴 offline"
                print(f"{event.presence.user} is now {status}")
            elif event.HasField("receipt"):
                print(
                    f"👁️ Message {event.receipt.message_id} read by {event.receipt.reader}"
                )


async def run():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        await login(stub)
        await listen(stub)


if __name__ == "__main__":
    asyncio.run(run())
