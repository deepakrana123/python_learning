from sqlmodel import SQLModel, text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import Config
import ssl
from sqlalchemy.orm import sessionmaker


ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

engine = create_async_engine(
    url=Config.DATABASE_URL,
    connect_args={"ssl": ssl_context},
    echo=True,
)


async def init_db():
    try:
        async with engine.begin() as conn:

            result = await conn.execute(text("SELECT 'OK'"))
            # await conn.run_sync(SQLModel.metadata.create_all)
            print("DB Working:", result.scalar())
    except Exception as e:
        print("DB Error:", e)


async_session_maker = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
