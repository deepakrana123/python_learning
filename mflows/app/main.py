from fastapi import FastAPI
from app.db.session import engine, Base

from app.api.worklfow_routes import route as workflow_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="FlowOS AI")


app.include_router(workflow_router)


@app.get("/")
def health():
    return {"message": "FlowOs running"}
