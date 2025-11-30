from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .schema import UserBaseModel, UserCreateModel
from .utils import (
    create_access_token,
    decode_token,
    verify_password,
    ACCESS_TOKEN_EXPIRY,
    REFRESH_TOKEN_EXPIRY,
)
from fastapi.responses import JSONResponse

auth_router = APIRouter()
auth_service = UserService()


@auth_router.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "Ok", "message": "Bhai mein sahi chalra"}


@auth_router.post(
    "/signup", response_model=UserBaseModel, status_code=status.HTTP_200_OK
)
async def create_user_Account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await auth_service.user_exist(email, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User already existfound"
        )
    user = await auth_service.create_user(user_data, session)
    return user


@auth_router.post("/login")
async def login_users(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    password = user_data.password
    user = await auth_service.get_user(email, session)
    if not user:
        raise HTTPException(status_code=403, detail="Invalid user")

    if not verify_password(password, user_data.hash_password):
        raise HTTPException(status_code=403, detail="Invalid password")

    access_token = create_access_token(
        user_data={"email": user.email, "uid": str(user.uid)},
        refresh=False,
        expiry=ACCESS_TOKEN_EXPIRY,
    )
    refresh_token = create_access_token(
        user_data={"email": user.email, "uid": str(user.uid)},
        refresh=True,
        expiry=REFRESH_TOKEN_EXPIRY,
    )
    return JSONResponse(
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {"email": user.email, "uid": str(user.uid)},
        }
    )
