from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from src.category.category_schema import (
    CategoryBase,
    CategoryUpdateModal,
    CategoryCreateModel,
    CategoryResponseModal,
)
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.category.service import CategoryService


category_router = APIRouter()
category_service = CategoryService()


@category_router.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "Ok", "message": "Bhai mein sahi chalra"}


@category_router.get(
    "/all", response_model=List[CategoryResponseModal], status_code=status.HTTP_200_OK
)
async def get_all_categories(session: AsyncSession = Depends(get_session)):
    category = await category_service.get_all_categories(session)
    print(category, "category")
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category


@category_router.post(
    "/", response_model=CategoryResponseModal, status_code=status.HTTP_201_CREATED
)
async def create_category(
    category_data: CategoryCreateModel, session: AsyncSession = Depends(get_session)
):
    print(category_data, "category_data")
    return await category_service.create_category(category_data, session)


@category_router.get(
    "/{uid}", response_model=CategoryResponseModal, status_code=status.HTTP_200_OK
)
async def get_category_by_id(uid: str, session: AsyncSession = Depends(get_session)):
    category = await category_service.get_category(uid, session)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category


@category_router.patch(
    "/{uid}", response_model=CategoryResponseModal, status_code=status.HTTP_200_OK
)
async def update_category(
    uid: str,
    category_data: CategoryUpdateModal,
    session: AsyncSession = Depends(get_session),
):
    updated = await category_service.update_category(uid, category_data, session)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return updated


@category_router.delete("/{uid}", status_code=status.HTTP_200_OK)
async def delete_category(uid: str, session: AsyncSession = Depends(get_session)):
    deleted = await category_service.delete_category(uid, session)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return {"detail": "Category deleted successfully"}
