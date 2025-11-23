from fastapi import FastAPI
from src.category.routes import category_router
from contextlib import asynccontextmanager
from src.db.main import init_db

version = "v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up ....")
    await init_db()
    yield
    print("Stoping down")


app = FastAPI(title="Fast Api project", version=version, lifespan=lifespan)
app.include_router(
    category_router, prefix=f"/api/{version}/categories", tags=["Categories"]
)
