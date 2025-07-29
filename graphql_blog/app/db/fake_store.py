# app/db/fake_store.py

users = [
    {"id": 1, "username": "alice", "email": "alice@example.com"},
    {"id": 2, "username": "bob", "email": "bob@example.com"},
]


def get_all_users():
    return users


def get_user_by_id(user_id: int):
    return next((user for user in users if user["id"] == user_id), None)
