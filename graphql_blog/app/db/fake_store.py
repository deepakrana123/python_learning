# app/db/fake_store.py

users = [
    {"id": 1, "username": "alice", "email": "alice@example.com"},
    {"id": 2, "username": "bob", "email": "bob@example.com"},
]


posts = [
    {"id": 1, "title": "GraphQL Intro", "content": "Basics of GraphQL", "author_id": 1},
    {
        "id": 2,
        "title": "FastAPI Guide",
        "content": "FastAPI with GraphQL",
        "author_id": 1,
    },
    {
        "id": 3,
        "title": "Python Tips",
        "content": "Useful Python tricks",
        "author_id": 2,
    },
]


def get_all_users():
    return users


def get_user_by_id(user_id: int):
    return next((user for user in users if user["id"] == user_id), None)


def get_all_posts():
    return posts


def get_post_by_id(post_id: int):
    return next((post for post in posts if post["id"] == post_id), None)


def get_posts_by_user(user_id: int):
    return [post for post in posts if post["author_id"] == user_id]
