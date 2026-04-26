from fastapi import APIRouter
from app.schemas.parser import ParseRequest, ParseResponse

from app.parsers.orchestrator import parse_workflow_text
from app.parsers import metrics


router = APIRouter(prefix="/parse", tags=["Parser"])


@router.post("/", response_model=ParseResponse)
def parse_router(payload: ParseRequest):
    return parse_workflow_text(payload)


@router.get("/metrics")
def get_metrics():
    return metrics.to_dict()
