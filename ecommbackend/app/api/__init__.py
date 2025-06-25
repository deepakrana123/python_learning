from fastapi import FastAPI
from app.api.v1 import auth, cart

app = FastAPI()
app.include_router(auth.router, prefix="/api/v1")
app.include_router(cart.router, prefix="/api/v1")
