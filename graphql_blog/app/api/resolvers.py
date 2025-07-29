# app/api/resolvers.py
from typing import List, Optional
from app.api.types import UserType
from app.db.fake_store import get_all_users, get_user_by_id


def resolve_users() -> List[UserType]:
    return [UserType(**user) for user in get_all_users()]


def resolve_user_by_id(user_id: int) -> Optional[UserType]:
    user = get_user_by_id(user_id)
    return UserType(**user) if user else None
