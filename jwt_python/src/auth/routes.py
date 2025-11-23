from fastapi import APIRouter, status, Depends, HTTPException
from typing import List

from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

auth_router = APIRouter()


@auth_router.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "Ok", "message": "Bhai mein sahi chalra"}
