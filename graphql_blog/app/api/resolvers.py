# app/api/resolvers.py
from typing import List, Optional
from app.api.types import UserType, PostType
from app.db.fake_store import (
    get_all_users,
    get_user_by_id,
    get_all_posts,
    get_posts_by_user,
    get_post_by_id,
)


def resolve_users() -> List[UserType]:
    return [UserType(**user) for user in get_all_users()]


def resolve_user_by_id(user_id: int) -> Optional[UserType]:
    user = get_user_by_id(user_id)
    return UserType(**user) if user else None


def resolve_posts() -> List[PostType]:
    return [PostType(**post) for post in get_all_posts()]


def resolve_post_by_user_id(user_id: int) -> Optional[PostType]:
    posts = get_posts_by_user(user_id)
    return [PostType(**post) for post in posts]


def resolve_post_by_id(user_id: int) -> Optional[PostType]:
    posts = get_post_by_id(user_id)
    return PostType(**posts) if posts else None
