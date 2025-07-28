import uuid


class User:
    def __init__(self, name, email, phone):
        self.user_id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.phone = phone
