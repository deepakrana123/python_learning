# app/api/types.py
import strawberry
from typing import List


@strawberry.input
class CreateUser:
    username: str
    email: str


@strawberry.input
class CreatePostInput:
    title: str
    content: str
    author_id: int


@strawberry.type
class PostType:
    id: int
    title: str
    content: str
    author_id: int


@strawberry.type
class UserType:
    id: int
    username: str
    email: str

    @strawberry.field
    def posts(self) -> List[PostType]:
        from app.db.fake_store import get_posts_by_user

        return [PostType(**post) for post in get_posts_by_user(self.id)]
