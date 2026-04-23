from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.models.workflow import Workflow
from app.api.workflows import router as workflow_router
from app.api.events import router as event_router

from app.llm.client import call_llm

print(call_llm("if salary above 50000 approve loan"))
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FlowOS AI")


app.include_router(workflow_router)
app.include_router(event_router)


@app.get("/")
def health():
    return {"message": "FlowOs running"}
