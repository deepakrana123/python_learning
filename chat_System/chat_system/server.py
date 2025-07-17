import asyncio
import grpc
import chat_pb2
import chat_pb2_grpc
from collections import defaultdict
import time

user_streams = {}  # user_id → asyncio.Queue
chat_members = defaultdict(set)  # chat_id → set(user_ids)
users = {"alice": "alicepass", "bob": "bobpass", "carol": "carolpass"}
tokens = {}  # token → username


class ChatService(chat_pb2_grpc.ChatServiceServicer):

    async def Login(self, request, context):
        if request.username in users and users[request.username] == request.password:
            token = f"token_{request.username}_{int(time.time())}"
            tokens[token] = request.username
            return chat_pb2.LoginResponse(token=token, success=True)
        return chat_pb2.LoginResponse(success=False, error="Invalid credentials")

    async def ChatStream(self, request_iterator, context):
        queue = asyncio.Queue()
        user_id = None
        chat_id = None

        async def broadcast_all(self, event):
            for uid, queue in user_streams.items():
                await queue.put(event)

        async def handle_incoming():
            nonlocal user_id, chat_id
            async for event in request_iterator:
                if not user_id:
                    # Authenticate from metadata
                    token = dict(context.invocation_metadata()).get("authorization")
                    if token not in tokens:
                        await context.abort(
                            grpc.StatusCode.UNAUTHENTICATED, "Invalid token"
                        )
                    user_id = tokens[token]
                    user_streams[user_id] = queue
                # On first message, join chat
                if event.HasField("message"):
                    chat_id = event.message.chat_id or "default_chat"
                    chat_members[chat_id].add(user_id)
                await self.handle_event(event, user_id)

        async def handle_outgoing():
            while True:
                event = await queue.get()
                yield event

        return await self._combine_streams(handle_incoming(), handle_outgoing())

    async def _combine_streams(self, sender, receiver):
        sender_task = asyncio.create_task(sender)
        receiver_task = asyncio.create_task(receiver.__anext__())

        while True:
            done, _ = await asyncio.wait(
                [sender_task, receiver_task], return_when=asyncio.FIRST_COMPLETED
            )

            if receiver_task in done:
                try:
                    yield receiver_task.result()
                    receiver_task = asyncio.create_task(receiver.__anext__())
                except StopAsyncIteration:
                    break
            if sender_task in done:
                break

    async def handle_event(self, event, sender):
        chat_id = None

        if event.HasField("message"):
            chat_id = event.message.chat_id
            if chat_id == "broadcast":
                await self.broadcast_all(event)
            else:
                await self.broadcast(chat_id, event)
        elif event.HasField("edit"):
            chat_id = "default_chat"
        elif event.HasField("delete"):
            chat_id = "default_chat"
        elif event.HasField("typing"):
            chat_id = event.typing.chat_id
        elif event.HasField("receipt"):
            chat_id = "default_chat"
        elif event.HasField("boardcast"):
            await self.braodcast_all(event)

        if chat_id and chat_id in chat_members:
            for uid in chat_members[chat_id]:
                if uid != sender and uid in user_streams:
                    await user_streams[uid].put(event)
        elif event.HasField("presence"):
            for uid in user_streams:
                if uid != sender:
                    await user_streams[uid].put(event)


async def serve():
    server = grpc.aio.server()
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port("[::]:50051")
    print("🚀 Server running on port 50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
