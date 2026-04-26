from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from app.routes.workflows import router as workflow_router
from app.routes.events import router as event_router
from app.routes.parsers import router as parser_router


app = FastAPI(
    title="FlowOS AI",
    version="1.0.0",
    description="AI workflow automation engine",
)


app.include_router(workflow_router, prefix="/api")
app.include_router(event_router, prefix="/api")
app.include_router(parser_router, prefix="/api")


@app.get("/")
def health():
    return {"message": "FlowOs running"}
