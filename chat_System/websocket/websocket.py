import time


class User:
    def __init__(self, user_id: str, username: str, online: bool):
        self.user_id = user_id
        self.username = username
        self.online = False
        self.last_seen = None


class Message:
    def __init__(self, message_id: str, sender: str, receiver: str, content: str):
        self.message_id = message_id
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.timestamp = time.time()
        self.edited = False
        self.deleted = False

    def edit(self, new_content: str):
        if not self.deleted:
            self.content = new_content
            self.edited = True
            print(f"Message {self.message_id}")
        else:
            print("Can't edit a deleted")

    def delete(self):
        self.deleted = True
        self.content = "[deleted]"
        print(f"message {self.message_id}")


class ChatSession:
    def __init__(self, user1: User, user2: User):
        self.user1 = user1
        self.user2 = user2
        self.messages: list[Message] = []

    def send_message(self, message: Message):
        self.messages.append(message)
        print(f"message send from {message.sender}")

    def edit_message(self, message_id: str, editor_id: str, new_content: str):
        for msg in self.messages:
            if msg.message_id == message_id:
                msg.edit(new_content)
                return
        print("Message not found or not editable")

    def delete_message(self, message_id: str, deleted_id: str):
        for msg in self.messages:
            if msg.message_id == message_id:
                msg.delete()
                return
        print("Message not found or not editable")


class ChatManager:
    def __init__(self):
        self.sessions: dict[tuple[str, str], ChatSession] = {}

    def get_or_create_session(self, user1: User, user2: User):
        key = tuple(sorted([user1.user_id, user2.user_id]))
        if key not in self.sessions:
            self.sessions[key] = ChatSession(user1, user2)
        return self.sessions[key]

    def send_message(self, form_id: User, to_id: User, content: str, message_id: str):
        session = self.get_or_create_session(form_id, to_id)
        message = Message(message_id, form_id, to_id, content)
        session.send_message(message)


class DeliveryManager:
    def __init__(self):
        self.online_users: dict[str, User] = {}

    def mark_online(self, user: User):
        user.online = True
        self.online_users[user.user_id] = user

    def mark_offline(self, user: User):
        user.online = False
        user.last_seen = time.time()
        self.online_users.pop(user.user_id, None)

    def is_online(self, user_id: str):
        return user_id in self.online_users

    def is_online(self, user_id: str):
        return (
            self.online_users.get(user_id).last_seen
            if user_id not in self.online_users
            else None
        )


class GroupChatSession:
    def __init__(self, group_id: str, group_name: str, members: list[User]):
        self.group_id = group_id
        self.group_name = group_name
        self.members = {user.user_id: user for user in members}
        self.messages: list[Message] = []

    def send_message(self, message: Message):
        if message.sender.user_id in self.members:
            self.messages.append(message)
        else:
            print("User isnot a member")

    def add_member(self, user: User):
        self.members[user.user_id] = user

    def remove_member(self, user_id):
        if user_id in self.members:
            del self.members[user_id]

    def edit_message(self, message_id: str, editor_id: str, new_content: str):
        for msg in self.messages:
            if msg.message_id == message_id and msg.sender.user_id == editor_id:
                msg.edit(new_content, editor_id)
                return

    def delete_message(self, message_id: str, deleted_id: str):
        for msg in self.messages:
            if msg.message_id == message_id and msg.sender.user_id == deleted_id:
                msg.delete()
                return


class TypingIndicator:
    def __init__(self):
        self.typing_users: dict[str, set[str]] = {}

    def start_typing(self, session_id: str, user_id: str):
        if session_id not in self.typing_users:
            self.typing_users[session_id] = user_id
        self.typing_users[session_id].add(user_id)
        print(f"user {user_id}")

    def stop_typing(self, session_id: str, user_id: str):
        if session_id in self.typing_users:
            self.typing_users[session_id].discard(user_id)
            if not self.typing_users[session_id]:
                del self.typing_users[session_id]

    def get_Typing_user(self, session_id):
        return list(self.typing_users.get(session_id, set()))
