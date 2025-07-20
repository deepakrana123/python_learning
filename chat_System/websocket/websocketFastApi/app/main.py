from fastapi import FastAPI  # type: ignore
from app.routes import auth
from app.db import engine  # type: ignore
from app.models.user import Base
from app.routes import auth, websocket


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(websocket.router)
