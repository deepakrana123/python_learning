from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from .category_schema import CategoryCreateModel, CategoryUpdateModal
from .models import Category


class CategoryService:

    async def get_all_categories(self, session: AsyncSession):
        statement = select(Category).order_by(desc(Category.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_category(self, uid: str, session: AsyncSession):
        statement = select(Category).where(Category.uid == uid)
        result = await session.exec(statement)
        return result.first()

    async def create_category(self, data: CategoryCreateModel, session: AsyncSession):
        new_category = Category(**data.model_dump())
        try:
            session.add(new_category)
            await session.commit()
            await session.refresh(new_category)
            return new_category
        except Exception as e:
            await session.rollback()
            raise e

    async def update_category(
        self, uid: str, update_data: CategoryUpdateModal, session: AsyncSession
    ):
        category = await self.get_category(uid, session)
        if not category:
            return None
        updated_dict = update_data.model_dump(exclude_unset=True)
        try:
            for key, value in updated_dict:
                setattr(category, key, value)
            await session.commit()
            await session.refresh(category)
            return category
        except Exception as e:
            await session.rollback()
            raise e

    async def delete_category(self, uid: str, session: AsyncSession):
        category = await self.get_category(uid, session)
        if not category:
            return None
        try:
            await session.delete(category)
            await session.commit()
            return True
        except Exception as e:
            await session.rollback()
            raise e
