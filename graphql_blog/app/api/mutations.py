import strawberry
from app.api.types import UserType, PostType
from app.api.types import CreateUserInput, CreatePostInput
from app.db import fake_store


@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_user(self, input: CreateUserInput) -> UserType:
        new_user = {
            "id": len(fake_store.users) + 1,
            "username": input.username,
            "email": input.email,
        }
        fake_store.users.append(new_user)
        return UserType(**new_user)

    @strawberry.mutation
    def create_post(self, input: CreatePostInput) -> PostType:
        author = fake_store.get_user_by_id(input.author_id)
        if not author:
            raise ValueError("Author not found")

        new_post = {
            "id": len(fake_store.posts) + 1,
            "title": input.title,
            "content": input.content,
            "author_id": input.author_id,
        }
        fake_store.posts.append(new_post)
        return PostType(**new_post)
