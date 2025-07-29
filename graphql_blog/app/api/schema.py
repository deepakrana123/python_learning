# app/api/schema.py
import strawberry
from app.api.types import UserType
from app.api.resolvers import resolve_users, resolve_user_by_id


@strawberry.type
class Query:
    users: list[UserType] = strawberry.field(resolver=resolve_users)
    user: UserType | None = strawberry.field(
        resolver=resolve_user_by_id, description="Get user by ID"
    )


schema = strawberry.Schema(query=Query)
