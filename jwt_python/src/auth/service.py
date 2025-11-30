from sqlmodel.ext.asyncio.session import AsyncSession
from .schema import UserCreateModel
from .models import User
from sqlmodel import select
from .utils import generate_password_hash


class UserService:
    async def get_user(self, email: str, session: AsyncSession) -> User | None:
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def user_exist(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user(email, session)
        return user is not None

    async def create_user(self, data: UserCreateModel, session: AsyncSession) -> User:
        if await self.user_exist(data.email, session):
            raise ValueError("User already exists")

        # Create user object
        new_user = User(
            username=data.username,
            email=data.email,
            hash_password=generate_password_hash(data.password),
            phone_number=data.phone_number,
        )

        try:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
        except Exception as e:
            await session.rollback()
            raise e
