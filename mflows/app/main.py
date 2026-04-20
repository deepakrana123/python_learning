from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.models.workflow import Workflow
from app.api.workflow_routes import router as workflow_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FlowOS AI")


app.include_router(workflow_router)


@app.get("/")
def health():
    return {"message": "FlowOs running"}
