import grpc
import time
import threading
import chat_pb2
import chat_pb2_grpc


def generate_messages():
    while True:
        msg = input("You: ")
        yield chat_pb2.ChatMessage(
            sender="You", message=msg, timestamp=int(time.time())
        )


def listen_for_messages(chat_stub):
    responses = chat_stub.ChatStream(generate_messages())
    for resp in responses:
        print(f"\n[{resp.sender}]: {resp.message}")


def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = chat_pb2_grpc.ChatServiceStub(channel)
    listen_for_messages(stub)


if __name__ == "__main__":
    run()
