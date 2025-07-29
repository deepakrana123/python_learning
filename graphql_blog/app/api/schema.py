# app/api/schema.py
import strawberry
from app.api.types import UserType, PostType
from app.api.resolvers import (
    resolve_users,
    resolve_user_by_id,
    resolve_posts,
    resolve_post_by_user_id,
)
from app.api.mutations import Mutation


@strawberry.type
class Query:
    users: list[UserType] = strawberry.field(resolver=resolve_users)
    user: UserType | None = strawberry.field(
        resolver=resolve_user_by_id, description="Get user by ID"
    )
    posts: list[PostType] = strawberry.field(resolver=resolve_posts)
    post: PostType | None = strawberry.field(
        resolver=resolve_post_by_user_id, description="Get user by ID"
    )


schema = strawberry.Schema(query=Query, mutation=Mutation)


# query {
#   users {
#     id
#     username
#     posts {
#       title
#     }
#   }
# }


# query {
#   post(postId: 2) {
#     title
#     content
#   }
# }
